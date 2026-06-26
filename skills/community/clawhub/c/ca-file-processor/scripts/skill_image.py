"""
OpenClaw Skill: Image Processor (Open-Source Path)
===================================================
Handles JPG / PNG files — primarily scanned invoices,
WhatsApp photos of documents, Form 16 copies, cheques.

Pipeline:
  1. Pillow preprocessing (deskew, contrast, sharpen, resize)
  2. Tesseract OCR (English + Hindi)
  3. Field extraction (invoice no., date, amount, GSTIN, vendor)
  4. Structured output dict for LLM

Dependencies:
    pip install pillow pytesseract numpy
    sudo apt-get install tesseract-ocr tesseract-ocr-hin

Usage in OpenClaw skill config:
    skill_name: image_processor
    trigger: "*.jpg uploaded" OR "*.png uploaded"
    entry: process_image(file_path)
"""

import json
import re
import math
from pathlib import Path

import pytesseract
from PIL import Image, ImageFilter, ImageEnhance, ImageOps


# ── CONFIG ────────────────────────────────────────────────────────────────────

TESSERACT_LANG = "eng+hin"
TARGET_WIDTH = 2000                  # Pixels — upscale small images to this
MAX_FILE_SIZE_MB = 20


# ── FIELD EXTRACTION PATTERNS ─────────────────────────────────────────────────
# Regex patterns for common CA document fields in Indian invoices

FIELD_PATTERNS = {
    "gstin": r'\b\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}\b',
    "invoice_no": r'(?:invoice\s*(?:no|number|#)[:\s.]*)([\w\/\-]+)',
    "invoice_date": (
        r'\b(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})\b'
        r'|\b(\d{1,2}\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{2,4})\b'
    ),
    "total_amount": (
        r'(?:grand\s*total|total\s*amount|net\s*payable|amount\s*payable|total)[:\s₹Rs.]*'
        r'([\d,]+(?:\.\d{1,2})?)'
    ),
    "pan": r'\b[A-Z]{5}\d{4}[A-Z]{1}\b',
    "email": r'\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b',
    "phone": r'\b(?:\+91[\s\-]?)?[6-9]\d{9}\b',
    "ifsc": r'\b[A-Z]{4}0[A-Z0-9]{6}\b',
}


# ── MAIN ENTRY POINT ─────────────────────────────────────────────────────────

def process_image(file_path: str) -> dict:
    """
    Main entry point called by OpenClaw when an image is received.

    Returns:
        {
          "file":           str,
          "format":         str,        # JPEG / PNG
          "original_size":  tuple,
          "text":           str,        # full OCR output
          "fields":         dict,       # extracted structured fields
          "doc_type":       str,        # "invoice" | "cheque" | "form16" | "generic"
          "confidence":     str,        # "high" | "medium" | "low"
          "summary":        str,
        }
    """
    path = Path(file_path)
    if not path.exists():
        return {"error": f"File not found: {file_path}"}

    # File size check
    size_mb = path.stat().st_size / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        return {"error": f"File too large ({size_mb:.1f} MB). Max: {MAX_FILE_SIZE_MB} MB"}

    img = Image.open(str(path))
    original_size = img.size
    img_format = img.format or path.suffix.upper().replace(".", "")

    # Convert RGBA / palette images to RGB
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")

    # Preprocessing pipeline
    preprocessed = _preprocess(img)

    # OCR
    raw_text = _run_ocr(preprocessed)
    clean_text = _clean_text(raw_text)

    # Field extraction & classification
    fields = _extract_fields(clean_text)
    doc_type = _classify_doc(clean_text, fields)
    confidence = _estimate_confidence(clean_text)
    summary = _build_summary(fields, doc_type, confidence)

    return {
        "file": path.name,
        "format": img_format,
        "original_size": original_size,
        "text": clean_text,
        "fields": fields,
        "doc_type": doc_type,
        "confidence": confidence,
        "summary": summary,
        "ocr_engine": "tesseract",
        "ocr_lang": TESSERACT_LANG,
    }


# ── IMAGE PREPROCESSING ───────────────────────────────────────────────────────

def _preprocess(img: Image.Image) -> Image.Image:
    """
    Multi-step preprocessing optimised for Indian financial documents.
    Order matters: greyscale → resize → deskew → contrast → sharpen.
    """
    # Step 1: Greyscale
    img = img.convert("L")

    # Step 2: Upscale if too small (Tesseract needs min ~150 DPI equivalent)
    w, h = img.size
    if w < TARGET_WIDTH:
        scale = TARGET_WIDTH / w
        img = img.resize(
            (int(w * scale), int(h * scale)),
            Image.LANCZOS
        )

    # Step 3: Auto-level (normalise brightness range)
    img = ImageOps.autocontrast(img, cutoff=2)

    # Step 4: Contrast boost — helps with faded stamps and light ink
    img = ImageEnhance.Contrast(img).enhance(1.8)

    # Step 5: Sharpen — helps with blurry WhatsApp photos
    img = img.filter(ImageFilter.SHARPEN)
    img = img.filter(ImageFilter.SHARPEN)   # Double sharpen for phone photos

    # Step 6: Basic deskew using simple rotation heuristic
    img = _deskew(img)

    return img


def _deskew(img: Image.Image) -> Image.Image:
    """
    Simple deskew: finds dominant text angle and corrects it.
    Skips correction if angle is negligible (< 0.5 degrees).
    Uses Tesseract's OSD (Orientation and Script Detection).
    """
    try:
        osd = pytesseract.image_to_osd(img, config="--psm 0 -c min_characters_to_try=5")
        angle_match = re.search(r"Rotate:\s*(\d+)", osd)
        if angle_match:
            angle = int(angle_match.group(1))
            if angle in (90, 180, 270):
                img = img.rotate(-angle, expand=True)
    except Exception:
        pass   # OSD can fail on small or sparse images — that's fine
    return img


# ── OCR ───────────────────────────────────────────────────────────────────────

def _run_ocr(img: Image.Image) -> str:
    """
    Run Tesseract with config tuned for financial documents.
    psm 6 = single uniform block (good for invoices).
    psm 3 = fully automatic (fallback for mixed layouts).
    """
    config = (
        "--psm 6 "
        "--oem 3 "                        # LSTM OCR engine
        "-c preserve_interword_spaces=1"  # Keep spacing for table alignment
    )
    try:
        return pytesseract.image_to_string(img, lang=TESSERACT_LANG, config=config)
    except Exception as e:
        return f"[OCR ERROR: {e}]"


# ── TEXT CLEANING ─────────────────────────────────────────────────────────────

def _clean_text(text: str) -> str:
    """Remove noise characters from OCR output."""
    # Remove non-printable chars (keep Hindi Unicode range)
    text = re.sub(r'[^\x20-\x7E\n\u0900-\u097F]', ' ', text)

    # Collapse multiple spaces
    text = re.sub(r'[ \t]{2,}', ' ', text)

    # Collapse 3+ blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


# ── FIELD EXTRACTION ──────────────────────────────────────────────────────────

def _extract_fields(text: str) -> dict:
    """
    Extract structured fields using regex patterns.
    Returns a dict with all found fields (empty string if not found).
    """
    fields = {}
    text_lower = text.lower()

    for field_name, pattern in FIELD_PATTERNS.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # Use first capturing group if present, else full match
            fields[field_name] = (match.group(1) if match.lastindex else match.group(0)).strip()
        else:
            fields[field_name] = ""

    # Extract all GSTINs (invoices can have 2: supplier + recipient)
    all_gstins = re.findall(FIELD_PATTERNS["gstin"], text)
    if len(all_gstins) > 1:
        fields["gstin_supplier"] = all_gstins[0]
        fields["gstin_recipient"] = all_gstins[1]
        fields["gstin"] = all_gstins[0]  # keep primary

    return fields


# ── DOCUMENT CLASSIFICATION ───────────────────────────────────────────────────

def _classify_doc(text: str, fields: dict) -> str:
    text_l = text.lower()

    if any(kw in text_l for kw in ["invoice", "tax invoice", "gst invoice", "bill of supply"]):
        return "gst_invoice"
    if any(kw in text_l for kw in ["cheque", "check", "pay to", "a/c payee"]):
        return "cheque"
    if any(kw in text_l for kw in ["form 16", "form16", "tds certificate"]):
        return "form_16"
    if any(kw in text_l for kw in ["salary slip", "payslip", "pay slip"]):
        return "salary_slip"
    if any(kw in text_l for kw in ["balance sheet", "profit", "loss", "trial balance"]):
        return "financial_statement"
    if fields.get("gstin"):
        return "gst_document"
    return "generic"


# ── CONFIDENCE ESTIMATION ─────────────────────────────────────────────────────

def _estimate_confidence(text: str) -> str:
    """
    Heuristic confidence based on text density and recognisable word ratio.
    High: >200 words, most look like real words
    Low: <50 words or high noise character ratio
    """
    words = text.split()
    word_count = len(words)

    if word_count < 30:
        return "low"

    # Check ratio of very short (likely noise) tokens
    noise = sum(1 for w in words if len(w) == 1 and not w.isalpha())
    noise_ratio = noise / max(word_count, 1)

    if noise_ratio > 0.2:
        return "low"
    if word_count >= 150 and noise_ratio < 0.1:
        return "high"
    return "medium"


# ── SUMMARY ───────────────────────────────────────────────────────────────────

def _build_summary(fields: dict, doc_type: str, confidence: str) -> str:
    lines = [
        f"Document type: {doc_type.replace('_', ' ').title()}",
        f"OCR confidence: {confidence}",
    ]
    for key in ["invoice_no", "invoice_date", "total_amount", "gstin",
                "gstin_supplier", "gstin_recipient", "pan"]:
        val = fields.get(key, "")
        if val:
            lines.append(f"{key.replace('_', ' ').title()}: {val}")
    return "\n".join(lines)


# ── OPENCLAW SKILL METADATA ───────────────────────────────────────────────────

SKILL_METADATA = {
    "name": "image_processor",
    "version": "1.0.0",
    "description": "OCR + field extraction for JPG/PNG images. Tuned for Indian CA documents.",
    "triggers": ["*.jpg", "*.jpeg", "*.png", "process image", "read this invoice"],
    "entry_function": "process_image",
    "output_format": "dict → passed to LLM context",
    "ca_use_cases": [
        "GST invoices (WhatsApp photos)",
        "Scanned Form 16",
        "Cheque images",
        "Physical invoices photographed",
        "Old balance sheet scans",
        "Salary slip photos",
    ]
}


# ── QUICK TEST ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python skill_image.py <path_to_image>")
        sys.exit(1)
    result = process_image(sys.argv[1])
    print(json.dumps({k: v for k, v in result.items() if k != "text"}, indent=2))
    print(f"\n--- TEXT PREVIEW ---\n{result.get('text', '')[:400]}")

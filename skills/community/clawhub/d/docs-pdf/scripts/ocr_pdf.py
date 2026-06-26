#!/usr/bin/env python3
"""
ocr_pdf.py — Run OCR on a scanned PDF and save the result as .txt.

Usage:
    python scripts/ocr_pdf.py scan.pdf
    python scripts/ocr_pdf.py scan.pdf --lang chi_sim+eng
    python scripts/ocr_pdf.py scan.pdf --dpi 600 --psm 6 --preprocess
    python scripts/ocr_pdf.py ./scans/ --batch             # process all PDFs in a folder
"""
import argparse
import sys
from pathlib import Path

def preprocess_image(img):
    """Improve OCR accuracy through image enhancement."""
    from PIL import ImageFilter, ImageEnhance
    import numpy as np

    img = img.convert("L")
    # Upscale if too small
    if img.width < 1500:
        scale = 1500 / img.width
        from PIL import Image
        img = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
    img = ImageEnhance.Contrast(img).enhance(1.8)
    img = img.filter(ImageFilter.SHARPEN)
    import numpy as np
    arr = np.array(img)
    arr = ((arr > arr.mean()) * 255).astype("uint8")
    from PIL import Image
    return Image.fromarray(arr)

def check_has_text(pdf_path: Path) -> bool:
    """Check if PDF already contains selectable text (not a pure scan)."""
    try:
        import pdfplumber
        with pdfplumber.open(str(pdf_path)) as pdf:
            for page in pdf.pages[:3]:  # check first 3 pages
                text = page.extract_text()
                if text and len(text.strip()) > 50:
                    return True
    except ImportError:
        pass  # pdfplumber not installed, skip check
    return False


def ocr_one(pdf_path: Path, lang: str, dpi: int, psm: int, do_preprocess: bool) -> str:
    from pdf2image import convert_from_path
    import pytesseract

    # Warn if PDF already has selectable text
    if check_has_text(pdf_path):
        print(
            f"  ⚠ This PDF already contains selectable text.\n"
            f"    For native-text PDFs, pdfplumber gives better results:\n"
            f"      python scripts/extract_text.py {pdf_path}\n"
            f"    Continuing with OCR anyway...",
            file=sys.stderr,
        )

    print(f"  Converting to images ({dpi} DPI)...")
    images = convert_from_path(str(pdf_path), dpi=dpi)
    pages  = []
    for i, img in enumerate(images, 1):
        print(f"  OCR page {i}/{len(images)}...", end="\r", flush=True)
        if do_preprocess:
            img = preprocess_image(img)
        text = pytesseract.image_to_string(img, lang=lang, config=f"--psm {psm} --oem 3")
        pages.append(f"=== Page {i} ===\n{text}")
    print()
    return "\n\n".join(pages)

def main():
    parser = argparse.ArgumentParser(description="OCR scanned PDF")
    parser.add_argument("input",                     help="Input PDF or directory")
    parser.add_argument("--output",    "-o",         help="Output .txt path or directory")
    parser.add_argument("--lang",      default="chi_sim+eng",
                        help="Tesseract language(s) (default: chi_sim+eng)")
    parser.add_argument("--dpi",       type=int, default=300, help="Render DPI (default: 300)")
    parser.add_argument("--psm",       type=int, default=6,   help="Page segmentation mode (default: 6)")
    parser.add_argument("--preprocess",action="store_true",   help="Apply image preprocessing")
    parser.add_argument("--batch",     action="store_true",   help="Process all PDFs in input directory")
    args = parser.parse_args()

    src = Path(args.input)

    if args.batch or src.is_dir():
        pdfs   = sorted(src.glob("*.pdf"))
        outdir = Path(args.output) if args.output else src
        outdir.mkdir(parents=True, exist_ok=True)
        print(f"Batch OCR: {len(pdfs)} PDFs in {src}")
        for pdf in pdfs:
            print(f"\nProcessing {pdf.name}...")
            text    = ocr_one(pdf, args.lang, args.dpi, args.psm, args.preprocess)
            out_txt = outdir / pdf.with_suffix(".txt").name
            out_txt.write_text(text, encoding="utf-8")
            print(f"  ✓ → {out_txt.name}")
        print(f"\n✓ Done: {len(pdfs)} files")
    else:
        if not src.exists():
            print(f"File not found: {src}", file=sys.stderr)
            sys.exit(1)
        print(f"OCR: {src.name}")
        text    = ocr_one(src, args.lang, args.dpi, args.psm, args.preprocess)
        out_txt = Path(args.output) if args.output else src.with_suffix(".txt")
        out_txt.write_text(text, encoding="utf-8")
        print(f"✓ → {out_txt}  ({len(text):,} chars)")

if __name__ == "__main__":
    main()

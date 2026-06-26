#!/usr/bin/env python3
"""
Make Searchable PDF with proper text layer using bounding boxes.

Supported:
- Input PDF (multipage) -> convert to images then embed text layer
- Input image (single page) -> image + text

We use the OCR result's layoutParsingResults[].prunedResult to place text
at the correct locations. If bboxes are missing, fall back to full-text overlay.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional

try:
    from PIL import Image
except ImportError:
    print("Pillow not installed. Install: pip install pillow", file=sys.stderr)
    sys.exit(1)

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    import io
except ImportError:
    print("reportlab not available. Install: pip install reportlab", file=sys.stderr)
    sys.exit(1)

# PDF input support
try:
    from pdf2image import convert_from_path
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False


# =============================================================================
# Fragment extraction from prunedResult
# =============================================================================

def extract_text_fragments(pruned: Any) -> List[Dict[str, Any]]:
    """
    Walk through prunedResult structure and collect items that have both text and bbox/polygon.
    Returns list of dicts with keys 'text' and 'bbox' (x,y,w,h).
    """
    fragments = []

    def walk(node: Any):
        if isinstance(node, dict):
            # Check if this node looks like a text fragment with bbox
            text = node.get("text")
            bbox = node.get("bbox") or node.get("polygon") or node.get("box") or node.get("position")
            if isinstance(text, str) and bbox:
                # Normalize bbox to (x, y, w, h)
                norm = normalize_bbox(bbox)
                if norm:
                    x, y, w, h = norm
                    fragments.append({
                        "text": text,
                        "x": x,
                        "y": y,
                        "w": w,
                        "h": h,
                    })
            # Recurse into values
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(pruned)
    return fragments


def normalize_bbox(bbox: Any) -> Optional[Tuple[float, float, float, float]]:
    """
    Convert various bbox formats to (x, y, w, h) with top-left origin.
    Supported:
      - [x, y, w, h]
      - [x0, y0, x1, y1] (bottom-right or top-right? assume x1>=x0, y1>=y0)
      - [x0, y0, x1, y1, x2, y2, x3, y3] (polygon four points)
    """
    if not isinstance(bbox, (list, tuple)):
        return None
    coords = list(bbox)
    if len(coords) == 4:
        x0, y0, x1, y1 = coords
        # Determine if it's [x,y,w,h] or [x0,y0,x1,y1]
        # If x1 < x0 or y1 < y0, it's likely w,h positive. But if both x1 >= x0 and y1 >= y0, ambiguous.
        # We'll assume if x1 - x0 is huge compared to typical coordinates, it's x1,y1; but not reliable.
        # Simple heuristic: if x1 > x0 and y1 > y0 and (x1 - x0) > 10 and (y1 - y0) > 10, could be either.
        # We'll check: if x1 < x0 or y1 < y0, then it's definitely w,h; else we treat as x0,y0,x1,y1.
        if x1 >= x0 and y1 >= y0:
            # Could be either. But if x0 and y0 are typically small and x1,y0 large, that's normal for both definitions.
            # However, if the values represent coordinates, x0 is left, x1 is right; width = x1 - x0.
            # If they represent width, x1 would be x0+width, so also >= x0. Same for y.
            # So we cannot differentiate.
            # We'll assume it's (x0, y0, width, height) if the numbers are small (like <1000)? Not reliable.
            # We'll require that if the third element is less than the first or fourth less than second, then it's w,h.
            # But both formats have positive width and height, so third >= first and fourth >= second typically.
            # Actually, if w and h are small they could be less than x0,y0 if x0,y0 are large? Not typical.
            # Many OCR returns absolute coordinates (x0,y0,x1,y1). So I'll assume that interpretation.
            w = x1 - x0
            h = y1 - y0
            if w < 0 or h < 0:
                # fallback: treat as w,h directly
                return (x0, y0, x1, y1)
            return (x0, y0, w, h)
        else:
            # x1 < x0 or y1 < y0 => treat as w,h
            return (x0, y0, x1, y1)
    elif len(coords) == 8:
        # Polygon: 4 points (x0,y0,x1,y1,x2,y2,x3,y3)
        xs = coords[0::2]
        ys = coords[1::2]
        x0 = min(xs)
        y0 = min(ys)
        x1 = max(xs)
        y1 = max(ys)
        return (x0, y0, x1 - x0, y1 - y0)
    return None


# =============================================================================
# Searchable PDF creation
# =============================================================================

def make_searchable_pdf(
    input_path: Path,
    ocr_result: Dict[str, Any],
    output_path: Path,
) -> bool:
    """
    Generate a searchable PDF.

    Args:
        input_path: Path to original image or PDF
        ocr_result: Full OCR result containing layoutParsingResults (with prunedResult and markdown)
        output_path: Where to save the searchable PDF
    Returns:
        True on success
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    suffix = input_path.suffix.lower()

    # Prepare image(s) for each page
    images: List[Image.Image] = []
    if suffix == ".pdf":
        if not PDF2IMAGE_AVAILABLE:
            print("pdf2image not installed. Install: pip install pdf2image and system poppler", file=sys.stderr)
            return False
        try:
            # Convert PDF to images (200 DPI)
            pil_images = convert_from_path(str(input_path), dpi=200)
            images = [img.convert("RGB") for img in pil_images]
        except Exception as e:
            print(f"Failed to convert PDF to images: {e}", file=sys.stderr)
            return False
    else:
        try:
            img = Image.open(str(input_path)).convert("RGB")
            images = [img]
        except Exception as e:
            print(f"Failed to open image: {e}", file=sys.stderr)
            return False

    # Extract layout data
    layout_pages = ocr_result.get("layoutParsingResults", [])
    if not layout_pages:
        print("No layoutParsingResults in OCR result; cannot build precise text layer", file=sys.stderr)
        return False

    # If fewer pages than images, pad or truncate
    if len(layout_pages) < len(images):
        print(f"Warning: OCR has {len(layout_pages)} pages but input has {len(images)} images. Truncating.", file=sys.stderr)
        images = images[:len(layout_pages)]
    elif len(layout_pages) > len(images):
        layout_pages = layout_pages[:len(images)]

    # Create multi-page PDF
    c = None
    try:
        for page_idx, (img, page_layout) in enumerate(zip(images, layout_pages)):
            width, height = img.size  # pixels, we'll use as points (1:1)
            if c is None:
                c = canvas.Canvas(str(output_path), pagesize=(width, height))
            else:
                c.setPageSize((width, height))

            # Draw image as background
            c.drawImage(ImageReader(img), 0, 0, width=width, height=height)

            # Try to get fragments
            pruned = page_layout.get("prunedResult", {})
            fragments = extract_text_fragments(pruned)

            if fragments:
                # Use fragments to place text precisely
                c.setFillColorRGB(1, 1, 1)  # white (invisible on white background)
                c.setFont("Helvetica", 10)  # base, will adjust per fragment
                for frag in fragments:
                    text = frag["text"]
                    x = frag["x"]
                    y = frag["y"]
                    w = frag["w"]
                    h = frag["h"]
                    # Convert from top-left origin to bottom-left origin
                    y_pdf = height - y - h
                    # Estimate font size: use h, but ensure not too small
                    font_size = max(8, min(int(h * 0.9), 72))
                    c.setFont("Helvetica", font_size)
                    # Draw each line if multi-line
                    lines = text.split("\n")
                    line_height = font_size * 1.2
                    for i, line in enumerate(lines):
                        c.drawString(x, y_pdf - i * line_height, line)
            else:
                # Fallback: overlay full page text at bottom left in white
                page_text = page_layout.get("markdown", {}).get("text", "")
                if page_text:
                    c.setFillColorRGB(1, 1, 1)
                    c.setFont("Helvetica", 8)
                    text_obj = c.beginText(10, 20)
                    for line in page_text.split("\n")[:100]:
                        text_obj.textLine(line[:200])
                    c.drawText(text_obj)

            c.showPage()

        c.save()
        return True
    except Exception as e:
        print(f"Error creating searchable PDF: {e}", file=sys.stderr)
        return False


# =============================================================================
# Command-line interface (backward compatible)
# =============================================================================

if __name__ == "__main__":
    """
    Usage (legacy):
      python make_searchable_pdf.py <input_path> <ocr_text_path> <output_pdf>

    New usage (with full OCR result):
      python make_searchable_pdf.py <input_path> <ocr_result_json> <output_pdf> --json
    """
    if len(sys.argv) < 4:
        print("Usage: make_searchable_pdf.py <input_path> <ocr_data_path> <output_pdf> [--json]")
        print("  If --json not given, ocr_data_path is plain text file (legacy).")
        print("  With --json, ocr_data_path is a JSON file containing full OCR result.")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    ocr_data_path = Path(sys.argv[2])
    output_pdf = Path(sys.argv[3])
    use_json = "--json" in sys.argv

    if use_json:
        import json
        with open(ocr_data_path, "r", encoding="utf-8") as f:
            ocr_result = json.load(f)
        success = make_searchable_pdf(input_path, ocr_result, output_pdf)
    else:
        # Legacy: just overlay text at bottom
        ocr_text = ocr_data_path.read_text(encoding="utf-8")
        # Need to create a dummy OCR result
        dummy_result = {
            "layoutParsingResults": [
                {
                    "markdown": {"text": ocr_text},
                    "prunedResult": {}
                }
            ]
        }
        success = make_searchable_pdf(input_path, dummy_result, output_pdf)

    sys.exit(0 if success else 1)

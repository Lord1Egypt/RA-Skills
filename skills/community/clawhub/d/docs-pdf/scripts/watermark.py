#!/usr/bin/env python3
"""
watermark.py — Add a text or image watermark to every page of a PDF.

Usage (text watermark):
    python scripts/watermark.py input.pdf --text "CONFIDENTIAL"
    python scripts/watermark.py input.pdf --text "DRAFT" --color "#FF0000" --alpha 0.1
    python scripts/watermark.py input.pdf --text "内部文件" --size 72 --angle 30

Usage (image watermark):
    python scripts/watermark.py input.pdf --image logo.png
    python scripts/watermark.py input.pdf --image logo.png --alpha 0.3 --position center
    python scripts/watermark.py input.pdf --image logo.png --scale 0.5 --position bottom-right
"""
import argparse
import io
import sys
from pathlib import Path
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader, PdfWriter


def build_text_watermark(
    text: str,
    font_size: int,
    color: str,
    alpha: float,
    angle: float,
    pagesize: tuple,
) -> bytes:
    W, H = pagesize
    buf  = io.BytesIO()
    c    = rl_canvas.Canvas(buf, pagesize=pagesize)
    c.saveState()
    c.setFillColor(HexColor(color))
    c.setFillAlpha(alpha)
    c.setFont("Helvetica-Bold", font_size)
    c.translate(W / 2, H / 2)
    c.rotate(angle)
    c.drawCentredString(0, 0, text)
    c.restoreState()
    c.save()
    buf.seek(0)
    return buf.read()


def build_image_watermark(
    image_path: str,
    alpha: float,
    position: str,
    scale: float,
    pagesize: tuple,
) -> bytes:
    from PIL import Image as PILImage

    W, H = pagesize
    buf  = io.BytesIO()
    c    = rl_canvas.Canvas(buf, pagesize=pagesize)

    # Load image and get dimensions
    img = PILImage.open(image_path)
    img_w, img_h = img.size

    # Apply scaling
    draw_w = img_w * scale
    draw_h = img_h * scale

    # Ensure image fits within page
    if draw_w > W * 0.9:
        ratio = (W * 0.9) / draw_w
        draw_w *= ratio
        draw_h *= ratio
    if draw_h > H * 0.9:
        ratio = (H * 0.9) / draw_h
        draw_w *= ratio
        draw_h *= ratio

    # Calculate position
    positions = {
        "center":       ((W - draw_w) / 2, (H - draw_h) / 2),
        "top-left":     (20, H - draw_h - 20),
        "top-right":    (W - draw_w - 20, H - draw_h - 20),
        "bottom-left":  (20, 20),
        "bottom-right": (W - draw_w - 20, 20),
    }
    x, y = positions.get(position, positions["center"])

    c.saveState()
    c.setFillAlpha(alpha)
    c.drawImage(
        ImageReader(image_path),
        x, y, draw_w, draw_h,
        preserveAspectRatio=True,
        mask="auto",
    )
    c.restoreState()
    c.save()
    buf.seek(0)
    return buf.read()


def main():
    parser = argparse.ArgumentParser(description="Add text or image watermark to PDF")
    parser.add_argument("input",              help="Input PDF")
    parser.add_argument("--output",  "-o",    help="Output PDF (default: <input>_wm.pdf)")

    # Text watermark options
    text_group = parser.add_argument_group("text watermark")
    text_group.add_argument("--text",   "-t",  help="Watermark text")
    text_group.add_argument("--color",         default="#888888", help="Hex color (default: #888888)")
    text_group.add_argument("--size",          type=int,   default=60,   help="Font size (default: 60)")
    text_group.add_argument("--angle",         type=float, default=45,   help="Rotation degrees (default: 45)")

    # Image watermark options
    img_group = parser.add_argument_group("image watermark")
    img_group.add_argument("--image",  "-img", help="Path to watermark image (PNG/JPG)")
    img_group.add_argument("--position",       default="center",
                           choices=["center", "top-left", "top-right", "bottom-left", "bottom-right"],
                           help="Image position (default: center)")
    img_group.add_argument("--scale",          type=float, default=1.0,
                           help="Image scale factor (default: 1.0)")

    # Shared options
    parser.add_argument("--alpha",   type=float, default=0.15, help="Opacity 0–1 (default: 0.15)")
    args = parser.parse_args()

    if not args.text and not args.image:
        print("Error: Provide either --text or --image for watermark.", file=sys.stderr)
        sys.exit(1)
    if args.text and args.image:
        print("Error: Use either --text or --image, not both.", file=sys.stderr)
        sys.exit(1)

    src = Path(args.input)
    dst = Path(args.output) if args.output else src.with_stem(src.stem + "_wm")

    reader   = PdfReader(str(src))
    first    = reader.pages[0]
    pw       = float(first.mediabox.width)
    ph       = float(first.mediabox.height)
    pagesize = (pw, ph)

    if args.text:
        wm_bytes = build_text_watermark(
            args.text, args.size, args.color, args.alpha, args.angle, pagesize
        )
        label = f'text "{args.text}"'
    else:
        img_path = Path(args.image)
        if not img_path.exists():
            print(f"Error: Image not found: {img_path}", file=sys.stderr)
            sys.exit(1)
        wm_bytes = build_image_watermark(
            str(img_path), args.alpha, args.position, args.scale, pagesize
        )
        label = f'image "{img_path.name}"'

    wm_page = PdfReader(io.BytesIO(wm_bytes)).pages[0]

    writer = PdfWriter()
    for page in reader.pages:
        page.merge_page(wm_page)
        writer.add_page(page)

    with open(dst, "wb") as f:
        writer.write(f)
    print(f"✓ Watermark ({label}) applied to {len(reader.pages)} pages → {dst}")


if __name__ == "__main__":
    main()

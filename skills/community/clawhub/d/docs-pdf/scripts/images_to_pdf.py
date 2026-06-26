#!/usr/bin/env python3
"""
images_to_pdf.py — Convert images to a single PDF document.

Supports: JPEG, PNG, TIFF, BMP, GIF, WEBP.

Usage:
    python scripts/images_to_pdf.py photo1.jpg photo2.png -o album.pdf
    python scripts/images_to_pdf.py "scans/*.jpg" -o document.pdf --page-size A4
    python scripts/images_to_pdf.py "photos/*.png" -o album.pdf --fit contain --margin 20
    python scripts/images_to_pdf.py image.png -o output.pdf --page-size Letter --landscape
"""
import argparse
import glob
import sys
from pathlib import Path

from reportlab.lib.pagesizes import (
    A3, A4, A5, letter, legal,
    landscape as rl_landscape,
)
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


PAGE_SIZES = {
    "A3": A3,
    "A4": A4,
    "A5": A5,
    "Letter": letter,
    "Legal": legal,
}

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp", ".gif", ".webp"}


def collect_images(patterns: list[str], sort: bool = True) -> list[Path]:
    """Resolve glob patterns to image file paths."""
    paths = []
    for pattern in patterns:
        expanded = glob.glob(pattern)
        if expanded:
            paths.extend(Path(p) for p in expanded)
        else:
            p = Path(pattern)
            if p.exists():
                paths.append(p)
            else:
                print(f"  ⚠ Not found: {pattern}", file=sys.stderr)

    # Filter to image files only
    paths = [p for p in paths if p.suffix.lower() in IMAGE_EXTENSIONS]
    if sort:
        paths.sort()
    return paths


def get_image_size(img_path: Path) -> tuple[float, float]:
    """Get image dimensions in pixels using PIL."""
    from PIL import Image
    with Image.open(img_path) as img:
        return img.size  # (width, height)


def fit_image(img_w: float, img_h: float,
              page_w: float, page_h: float,
              margin: float, fit: str) -> tuple[float, float, float, float]:
    """Calculate image position and size for the given fit mode.

    Returns (x, y, draw_w, draw_h).
    """
    avail_w = page_w - 2 * margin
    avail_h = page_h - 2 * margin

    if fit == "stretch":
        return margin, margin, avail_w, avail_h

    # Compute scale factor
    scale_w = avail_w / img_w
    scale_h = avail_h / img_h

    if fit == "contain":
        scale = min(scale_w, scale_h)
    elif fit == "cover":
        scale = max(scale_w, scale_h)
    else:  # "original"
        scale = 1.0

    draw_w = img_w * scale
    draw_h = img_h * scale

    # Center on page
    x = margin + (avail_w - draw_w) / 2
    y = margin + (avail_h - draw_h) / 2

    return x, y, draw_w, draw_h


def main():
    parser = argparse.ArgumentParser(
        description="Convert images to a single PDF document"
    )
    parser.add_argument("inputs", nargs="+",
                        help="Image files or glob patterns")
    parser.add_argument("--output", "-o", required=True,
                        help="Output PDF path")
    parser.add_argument("--page-size", "-s",
                        choices=list(PAGE_SIZES.keys()),
                        default="A4",
                        help="Page size (default: A4)")
    parser.add_argument("--landscape", action="store_true",
                        help="Use landscape orientation")
    parser.add_argument("--fit",
                        choices=["contain", "cover", "stretch", "original"],
                        default="contain",
                        help="How to fit image on page (default: contain)")
    parser.add_argument("--margin", "-m", type=float, default=10,
                        help="Page margin in mm (default: 10)")
    parser.add_argument("--no-sort", action="store_true",
                        help="Don't sort files alphabetically")
    parser.add_argument("--dpi", type=int, default=0,
                        help="If >0, auto-size page to image at this DPI")
    args = parser.parse_args()

    images = collect_images(args.inputs, sort=not args.no_sort)
    if not images:
        print("No image files found.", file=sys.stderr)
        sys.exit(1)

    # Check PIL is available
    try:
        from PIL import Image
    except ImportError:
        print("Pillow is required: pip install Pillow --break-system-packages",
              file=sys.stderr)
        sys.exit(1)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    margin = args.margin * mm
    page_size = PAGE_SIZES[args.page_size]
    if args.landscape:
        page_size = rl_landscape(page_size)

    c = canvas.Canvas(str(out_path))
    total = len(images)

    for idx, img_path in enumerate(images, 1):
        try:
            img_w, img_h = get_image_size(img_path)

            # Auto-size page to image if DPI is specified
            if args.dpi > 0:
                pw = (img_w / args.dpi) * 72 + 2 * margin
                ph = (img_h / args.dpi) * 72 + 2 * margin
                c.setPageSize((pw, ph))
                x, y, dw, dh = fit_image(img_w, img_h, pw, ph, margin, args.fit)
            else:
                pw, ph = page_size
                c.setPageSize((pw, ph))
                x, y, dw, dh = fit_image(img_w, img_h, pw, ph, margin, args.fit)

            c.drawImage(str(img_path), x, y, width=dw, height=dh,
                        preserveAspectRatio=(args.fit != "stretch"),
                        anchor="c")
            c.showPage()
            print(f"  [{idx}/{total}] {img_path.name}  ({img_w}×{img_h}px)")

        except Exception as e:
            print(f"  ✗ Skipped {img_path.name}: {e}", file=sys.stderr)

    c.save()
    result_size = out_path.stat().st_size
    size_str = f"{result_size/1024:.1f} KB" if result_size < 1024*1024 else f"{result_size/1024/1024:.1f} MB"
    print(f"\n✓ {total} images → {out_path}  ({size_str})")


if __name__ == "__main__":
    main()

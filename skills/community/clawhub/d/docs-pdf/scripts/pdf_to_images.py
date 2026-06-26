#!/usr/bin/env python3
"""
pdf_to_images.py — Convert PDF pages to images.

Requires: poppler (pdftotext/pdftoppm) installed, plus pdf2image Python package.

Usage:
    python scripts/pdf_to_images.py input.pdf
    python scripts/pdf_to_images.py input.pdf -o pages/ --format png --dpi 200
    python scripts/pdf_to_images.py input.pdf --pages 1-5 --format jpeg --dpi 300
    python scripts/pdf_to_images.py input.pdf --single-file first   # first page only (thumbnail)
"""
import argparse
import sys
from pathlib import Path


def parse_page_range(spec: str, total: int) -> tuple[int, int]:
    """Parse '3-7' → (first_page=3, last_page=7) for pdf2image (1-indexed)."""
    if "-" in spec:
        parts = spec.split("-")
        first = int(parts[0])
        last = min(int(parts[1]), total)
    else:
        first = int(spec)
        last = first
    return first, last


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF pages to images"
    )
    parser.add_argument("input", help="Input PDF file")
    parser.add_argument("--output", "-o", default=".",
                        help="Output directory (default: current dir)")
    parser.add_argument("--format", "-f",
                        choices=["png", "jpeg", "tiff", "ppm"],
                        default="png",
                        help="Output image format (default: png)")
    parser.add_argument("--dpi", "-d", type=int, default=200,
                        help="Resolution in DPI (default: 200)")
    parser.add_argument("--pages", "-p",
                        help="Page range, e.g. '1-5' or '3' (default: all)")
    parser.add_argument("--single-file",
                        choices=["first", "last"],
                        help="Output only first or last page (for thumbnails)")
    parser.add_argument("--prefix", default=None,
                        help="Filename prefix (default: PDF stem)")
    args = parser.parse_args()

    try:
        from pdf2image import convert_from_path, pdfinfo_from_path
    except ImportError:
        print("pdf2image is required: pip install pdf2image --break-system-packages",
              file=sys.stderr)
        print("Also requires poppler: brew install poppler (macOS) or "
              "apt-get install poppler-utils (Linux)", file=sys.stderr)
        sys.exit(1)

    src = Path(args.input)
    if not src.exists():
        print(f"File not found: {src}", file=sys.stderr)
        sys.exit(1)

    outdir = Path(args.output)
    outdir.mkdir(parents=True, exist_ok=True)

    prefix = args.prefix or src.stem
    fmt = args.format.upper()
    if fmt == "JPEG":
        ext = "jpg"
    else:
        ext = args.format.lower()

    # Get total pages
    try:
        info = pdfinfo_from_path(str(src))
        total = info.get("Pages", 0)
    except Exception:
        from pypdf import PdfReader
        total = len(PdfReader(str(src)).pages)

    print(f"Converting {src.name}  ({total} pages, {args.dpi} DPI, {args.format})...")

    # Determine page range
    convert_kwargs = {
        "dpi": args.dpi,
        "fmt": args.format,
    }

    if args.single_file == "first":
        convert_kwargs["first_page"] = 1
        convert_kwargs["last_page"] = 1
    elif args.single_file == "last":
        convert_kwargs["first_page"] = total
        convert_kwargs["last_page"] = total
    elif args.pages:
        first, last = parse_page_range(args.pages, total)
        convert_kwargs["first_page"] = first
        convert_kwargs["last_page"] = last

    images = convert_from_path(str(src), **convert_kwargs)

    first_page = convert_kwargs.get("first_page", 1)
    saved = 0
    for i, img in enumerate(images):
        page_num = first_page + i
        out_file = outdir / f"{prefix}_page{page_num:04d}.{ext}"
        img.save(str(out_file), fmt)
        w, h = img.size
        file_size = out_file.stat().st_size
        size_str = f"{file_size/1024:.0f}KB"
        print(f"  Page {page_num:>4d}: {w}×{h}px  {size_str}  → {out_file.name}")
        saved += 1

    print(f"\n✓ {saved} images saved to {outdir}/")


if __name__ == "__main__":
    main()

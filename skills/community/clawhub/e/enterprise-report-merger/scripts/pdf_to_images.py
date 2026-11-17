#!/usr/bin/env python3
"""
PDF to Images Converter — 将 PDF 每页转为高分辨率 PNG 图片。

用途：当 PDF 为扫描件/图片型（pdfplumber 无法提取文本）时，
将 PDF 页面转为图片，然后由智能体通过多模态视觉能力读取表格数据。

Usage:
  python pdf_to_images.py --input report.pdf --output-dir ./pdf_images
  python pdf_to_images.py --input report.pdf --output-dir ./pdf_images --dpi 300 --pages "0-5"
  python pdf_to_images.py --input report.pdf --output-dir ./pdf_images --format png --quality 95

Output:
  生成 page_001.png, page_002.png, ... 到指定目录。
  同时输出 JSON 摘要到 stdout，包含每页图片路径和文本检测信息。
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("ERROR: PyMuPDF is required. Install with: pip install PyMuPDF", file=sys.stderr)
    sys.exit(1)


def detect_pdf_type(pdf_path: str) -> dict:
    """
    Detect whether a PDF is text-based or image-based (scanned).

    Returns dict with:
      - type: 'text' | 'image' | 'mixed'
      - total_pages: int
      - text_pages: list of page indices with extractable text
      - image_pages: list of page indices that are image-only
      - text_ratio: percentage of pages with text
    """
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    text_pages = []
    image_pages = []

    for i in range(total_pages):
        page = doc[i]
        text = page.get_text().strip()
        # A page is considered "text" if it has substantial text (> 50 chars)
        if len(text) > 50:
            text_pages.append(i)
        else:
            image_pages.append(i)

    doc.close()

    if not image_pages:
        pdf_type = 'text'
    elif not text_pages:
        pdf_type = 'image'
    else:
        pdf_type = 'mixed'

    text_ratio = len(text_pages) / total_pages * 100 if total_pages > 0 else 0

    return {
        'type': pdf_type,
        'total_pages': total_pages,
        'text_pages': text_pages,
        'image_pages': image_pages,
        'text_ratio': round(text_ratio, 1),
    }


def pdf_to_images(pdf_path: str, output_dir: str,
                  dpi: int = 300, pages: str | None = None,
                  fmt: str = 'png', quality: int = 95) -> list[dict]:
    """
    Convert PDF pages to high-resolution images.

    Args:
        pdf_path: Path to PDF file.
        output_dir: Directory to save images.
        dpi: Resolution (default 300 for OCR quality).
        pages: Page range string like "0-5" or "0,2,4". None = all pages.
        fmt: Image format ('png' or 'jpeg').
        quality: JPEG quality (1-100), ignored for PNG.

    Returns:
        List of dicts: [{page: int, path: str, width: int, height: int}, ...]
    """
    os.makedirs(output_dir, exist_ok=True)

    doc = fitz.open(pdf_path)
    total_pages = len(doc)

    # Parse page range
    if pages:
        target_pages = _parse_page_range(pages, total_pages)
    else:
        target_pages = list(range(total_pages))

    # Calculate zoom factor from DPI (PDF default is 72 DPI)
    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)

    results = []
    for page_num in target_pages:
        if page_num >= total_pages:
            continue

        page = doc[page_num]
        pix = page.get_pixmap(matrix=matrix)

        # Generate filename with zero-padded page number
        ext = 'png' if fmt == 'png' else 'jpg'
        filename = f'page_{page_num + 1:03d}.{ext}'
        filepath = os.path.join(output_dir, filename)

        if fmt == 'png':
            pix.save(filepath)
        else:
            pix.save(filepath, jpg_quality=quality)

        results.append({
            'page': page_num,
            'path': os.path.abspath(filepath),
            'width': pix.width,
            'height': pix.height,
        })
        print(f'  Page {page_num + 1}/{total_pages} → {filename} ({pix.width}x{pix.height})')

    doc.close()
    return results


def _parse_page_range(pages_str: str, total: int) -> list[int]:
    """Parse page range string like '0-5' or '0,2,4' to list of ints."""
    result = []
    parts = pages_str.split(',')
    for part in parts:
        part = part.strip()
        if '-' in part:
            start, end = part.split('-', 1)
            start = int(start.strip())
            end = int(end.strip())
            result.extend(range(start, min(end + 1, total)))
        else:
            n = int(part)
            if n < total:
                result.append(n)
    return result


def main():
    parser = argparse.ArgumentParser(description='Convert PDF pages to images for visual table extraction')
    parser.add_argument('--input', '-i', required=True, help='Path to PDF file')
    parser.add_argument('--output-dir', '-o', required=True, help='Output directory for images')
    parser.add_argument('--dpi', type=int, default=300, help='Image resolution DPI (default: 300)')
    parser.add_argument('--pages', type=str, default=None, help='Page range like "0-5" or "0,2,4"')
    parser.add_argument('--format', choices=['png', 'jpeg'], default='png', help='Image format')
    parser.add_argument('--quality', type=int, default=95, help='JPEG quality 1-100 (default: 95)')
    parser.add_argument('--detect-only', action='store_true', help='Only detect PDF type, do not convert')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"ERROR: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Step 1: Detect PDF type
    print(f"Analyzing PDF: {args.input}")
    info = detect_pdf_type(args.input)
    print(f"  Type: {info['type']}")
    print(f"  Total pages: {info['total_pages']}")
    print(f"  Text pages: {info['text_pages']}")
    print(f"  Image pages: {info['image_pages']}")
    print(f"  Text ratio: {info['text_ratio']}%")

    if args.detect_only:
        print(json.dumps(info, ensure_ascii=False, indent=2))
        return

    # Step 2: Convert to images
    if info['type'] == 'text':
        print(f"\nNote: This PDF is text-based. pdfplumber can extract tables directly.")
        print(f"Converting to images anyway (use --detect-only to skip)...")

    print(f"\nConverting to images (DPI={args.dpi}, format={args.format})...")
    results = pdf_to_images(
        args.input, args.output_dir,
        dpi=args.dpi, pages=args.pages,
        fmt=args.format, quality=args.quality
    )

    print(f"\nDone! {len(results)} images saved to: {os.path.abspath(args.output_dir)}")
    print(f"\nImage paths (for visual table extraction):")
    for r in results:
        print(f"  {r['path']}")

    # Output JSON summary
    summary = {
        'pdf_info': info,
        'images': results,
        'output_dir': os.path.abspath(args.output_dir),
    }
    print(f"\n--- JSON Summary ---")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

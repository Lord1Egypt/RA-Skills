#!/usr/bin/env python3
"""
QR-Renderer: Converts ASCII QR code matrices (█, ▀, ▄, space) into high-definition PNGs.
Useful for headless server environments where terminal output cannot be easily scanned.

Usage:
    python3 cli_qr_refiner.py <input_txt_path> <output_png_path> [scale]

Examples:
    python3 cli_qr_refiner.py /tmp/qr_source.txt /tmp/qr_output.png
    python3 cli_qr_refiner.py /tmp/qr_source.txt /tmp/qr_output.png 15
"""

import sys
from PIL import Image, ImageDraw


def render_qr(input_path: str, output_path: str, scale: int = 10) -> None:
    """
    Render ASCII QR code (█ ▀ ▄) as high-definition PNG.

    Args:
        input_path:  Path to text file containing ASCII QR code
        output_path: Path to output PNG file
        scale:       Pixel size per character cell (default 10)
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f if line.strip()]

    if not lines:
        print(f"[QR-Renderer] Error: empty input file '{input_path}'")
        sys.exit(1)

    height = len(lines)
    width = max(len(line) for line in lines)

    # Each char cell: width = scale, height = scale * 2
    # (half blocks ▀ ▄ are half-height, so we double the scale for proper rendering)
    cell_w = scale
    cell_h = scale * 2

    img = Image.new('RGB', (width * cell_w, height * cell_h), color='white')
    draw = ImageDraw.Draw(img)

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            x0 = x * cell_w
            y0 = y * cell_h
            x1 = x0 + cell_w
            y1 = y0 + cell_h

            if char == '█':
                # Full block: fill entire cell
                draw.rectangle([x0, y0, x1 - 1, y1 - 1], fill='black')
            elif char == '▀':
                # Upper half block: fill top half
                draw.rectangle([x0, y0, x1 - 1, y0 + cell_h // 2 - 1], fill='black')
            elif char == '▄':
                # Lower half block: fill bottom half
                draw.rectangle([x0, y0 + cell_h // 2, x1 - 1, y1 - 1], fill='black')
            # space and any other char → leave white (background)

    img.save(output_path, 'PNG')
    print(f"[QR-Renderer] HD QR Code generated at: {output_path}")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 cli_qr_refiner.py <input_txt> <output_png> [scale]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    scale = int(sys.argv[3]) if len(sys.argv) > 3 else 10

    render_qr(input_file, output_file, scale)

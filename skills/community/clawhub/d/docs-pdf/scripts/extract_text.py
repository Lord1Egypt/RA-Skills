#!/usr/bin/env python3
"""
extract_text.py — Extract all text from a PDF, page by page, to a .txt file.

Usage:
    python scripts/extract_text.py input.pdf
    python scripts/extract_text.py input.pdf --output result.txt
    python scripts/extract_text.py input.pdf --pages 1-5
    python scripts/extract_text.py input.pdf --layout   # preserve layout spacing
"""
import argparse
from pathlib import Path
import pdfplumber

def parse_page_range(spec: str, total: int) -> list[int]:
    """Parse '1-5,7,9-11' → [0,1,2,3,4,6,8,9,10] (0-indexed)."""
    indices = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            indices.update(range(int(a) - 1, min(int(b), total)))
        else:
            indices.add(int(part) - 1)
    return sorted(indices)

def main():
    parser = argparse.ArgumentParser(description="Extract text from PDF")
    parser.add_argument("input",              help="Input PDF path")
    parser.add_argument("--output", "-o",     help="Output .txt path (default: same name)")
    parser.add_argument("--pages",  "-p",     help="Page range, e.g. 1-5 or 1,3,5-8")
    parser.add_argument("--layout", "-l",     action="store_true",
                        help="Preserve layout spacing")
    args = parser.parse_args()

    src = Path(args.input)
    dst = Path(args.output) if args.output else src.with_suffix(".txt")

    with pdfplumber.open(src) as pdf:
        total  = len(pdf.pages)
        pages  = parse_page_range(args.pages, total) if args.pages else list(range(total))
        chunks = []

        for i in pages:
            page = pdf.pages[i]
            text = page.extract_text(x_tolerance=3, y_tolerance=3) or ""
            chunks.append(f"{'='*60}\nPage {i+1} of {total}\n{'='*60}\n{text}")
            print(f"  Page {i+1}/{total}: {len(text)} chars")

    output = "\n\n".join(chunks)
    dst.write_text(output, encoding="utf-8")
    print(f"\n✓ {len(pages)} pages → {dst}  ({len(output):,} chars)")

if __name__ == "__main__":
    main()

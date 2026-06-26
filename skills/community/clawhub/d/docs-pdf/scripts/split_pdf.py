#!/usr/bin/env python3
"""
split_pdf.py — Split a PDF by page ranges or into individual pages.

Usage:
    python scripts/split_pdf.py input.pdf --each           # one file per page
    python scripts/split_pdf.py input.pdf --ranges 1-5 6-10 11-20
    python scripts/split_pdf.py input.pdf --every 10       # chunks of 10 pages
    python scripts/split_pdf.py input.pdf --output ./parts/
"""
import argparse
import sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter

def write_pages(reader, indices: list[int], out_path: Path):
    w = PdfWriter()
    for i in indices:
        w.add_page(reader.pages[i])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        w.write(f)
    print(f"  → {out_path.name}  ({len(indices)} pages)")

def parse_range(spec: str, total: int) -> list[int]:
    """'1-5' → [0,1,2,3,4]"""
    a, b = spec.split("-")
    return list(range(int(a) - 1, min(int(b), total)))

def main():
    parser = argparse.ArgumentParser(description="Split PDF into parts")
    parser.add_argument("input",            help="Input PDF")
    parser.add_argument("--output", "-o",   default=".", help="Output directory")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--each",    action="store_true",
                       help="One file per page")
    group.add_argument("--ranges",  nargs="+", metavar="START-END",
                       help="Page ranges, e.g. 1-5 6-10")
    group.add_argument("--every",   type=int, metavar="N",
                       help="Split into chunks of N pages")
    args = parser.parse_args()

    src    = Path(args.input)
    outdir = Path(args.output)
    reader = PdfReader(str(src))
    total  = len(reader.pages)
    stem   = src.stem

    print(f"Splitting {src.name}  ({total} pages)...")

    if args.each:
        for i in range(total):
            write_pages(reader, [i], outdir / f"{stem}_p{i+1:04d}.pdf")

    elif args.ranges:
        for spec in args.ranges:
            try:
                indices = parse_range(spec, total)
                a, b    = spec.split("-")
                write_pages(reader, indices, outdir / f"{stem}_{a}-{b}.pdf")
            except Exception as e:
                print(f"  ⚠ Bad range '{spec}': {e}", file=sys.stderr)

    elif args.every:
        n     = args.every
        chunk = 0
        for start in range(0, total, n):
            chunk += 1
            indices = list(range(start, min(start + n, total)))
            label   = f"{start+1}-{indices[-1]+1}"
            write_pages(reader, indices, outdir / f"{stem}_part{chunk:02d}_{label}.pdf")

    print(f"\n✓ Done  ({total} pages processed)")

if __name__ == "__main__":
    main()

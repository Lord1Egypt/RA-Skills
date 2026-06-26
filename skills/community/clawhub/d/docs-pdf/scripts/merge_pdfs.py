#!/usr/bin/env python3
"""
merge_pdfs.py — Merge multiple PDF files into one.

Usage:
    python scripts/merge_pdfs.py a.pdf b.pdf c.pdf --output merged.pdf
    python scripts/merge_pdfs.py "reports/*.pdf" --output merged.pdf --sort
    python scripts/merge_pdfs.py --list files.txt --output merged.pdf
"""
import argparse
import glob
import sys
from pathlib import Path
from pypdf import PdfWriter, PdfReader

def resolve_inputs(raw: list[str], sort: bool) -> list[Path]:
    paths = []
    for item in raw:
        expanded = glob.glob(item)
        if expanded:
            paths.extend(Path(p) for p in expanded)
        else:
            p = Path(item)
            if p.exists():
                paths.append(p)
            else:
                print(f"  ⚠ Not found: {item}", file=sys.stderr)
    if sort:
        paths.sort()
    return paths

def main():
    parser = argparse.ArgumentParser(description="Merge PDF files")
    parser.add_argument("inputs",   nargs="*",     help="PDF files or glob patterns")
    parser.add_argument("--output", "-o", required=True, help="Output PDF path")
    parser.add_argument("--list",   "-l", help="Text file with one PDF path per line")
    parser.add_argument("--sort",   action="store_true", help="Sort inputs alphabetically")
    args = parser.parse_args()

    raw = list(args.inputs or [])
    if args.list:
        lines = Path(args.list).read_text().splitlines()
        raw.extend(l.strip() for l in lines if l.strip())

    paths = resolve_inputs(raw, args.sort)
    if not paths:
        print("No input files found.")
        sys.exit(1)

    writer    = PdfWriter()
    total_pgs = 0

    for path in paths:
        try:
            reader = PdfReader(str(path))
            n      = len(reader.pages)
            writer.append(reader)
            total_pgs += n
            print(f"  + {path.name}  ({n} page{'s' if n!=1 else ''})")
        except Exception as e:
            print(f"  ✗ Skipped {path.name}: {e}", file=sys.stderr)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "wb") as f:
        writer.write(f)
    print(f"\n✓ {len(paths)} files, {total_pgs} pages → {out}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
reorder_pdf.py — Reorder pages in a PDF document.

Supports flexible page ordering: specific pages, ranges, reverse, and remainder.

Usage:
    python scripts/reorder_pdf.py input.pdf --order "3,1,2,4-" -o reordered.pdf
    python scripts/reorder_pdf.py input.pdf --order "5,4,3,2,1" -o reversed_first5.pdf
    python scripts/reorder_pdf.py input.pdf --reverse -o reversed.pdf
    python scripts/reorder_pdf.py input.pdf --order "2,1,3-" -o swapped.pdf

Order syntax:
    3       → page 3
    1-5     → pages 1 through 5
    4-      → page 4 through the last page
    reverse → all pages in reverse

Examples:
    "3,1,2,4-"   → page 3 first, then 1, 2, then 4 to end
    "5-1"         → pages 5,4,3,2,1 (reverse range)
    "1,1,2"       → page 1 duplicated, then page 2
"""
import argparse
import sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter


def parse_order(spec: str, total: int) -> list[int]:
    """Parse order specification into 0-indexed page list.

    Supports: single page, range (a-b), open range (a-), reverse range (5-1).
    """
    pages = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue

        if "-" in part:
            segments = part.split("-", 1)
            start_str = segments[0].strip()
            end_str = segments[1].strip()

            if not start_str:
                # "-5" → pages 1 to 5
                start = 1
                end = int(end_str)
                pages.extend(range(start - 1, end))
            elif not end_str:
                # "4-" → page 4 to last
                start = int(start_str)
                pages.extend(range(start - 1, total))
            else:
                start = int(start_str)
                end = int(end_str)
                if start <= end:
                    pages.extend(range(start - 1, end))
                else:
                    # reverse range: "5-1" → [4,3,2,1,0]
                    pages.extend(range(start - 1, end - 2, -1))
        else:
            page_num = int(part)
            if page_num < 1 or page_num > total:
                print(f"  ⚠ Page {page_num} out of range (1-{total}), skipping",
                      file=sys.stderr)
                continue
            pages.append(page_num - 1)

    return pages


def main():
    parser = argparse.ArgumentParser(
        description="Reorder pages in a PDF document"
    )
    parser.add_argument("input", help="Input PDF file")
    parser.add_argument("--output", "-o", required=True,
                        help="Output PDF path")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--order",
                       help='Page order spec, e.g. "3,1,2,4-"')
    group.add_argument("--reverse", action="store_true",
                       help="Reverse all pages")
    parser.add_argument("--keep-metadata", action="store_true", default=True,
                        help="Copy metadata from original (default: true)")
    args = parser.parse_args()

    src = Path(args.input)
    if not src.exists():
        print(f"File not found: {src}", file=sys.stderr)
        sys.exit(1)

    reader = PdfReader(str(src))
    total = len(reader.pages)
    print(f"Input: {src.name}  ({total} pages)")

    if args.reverse:
        page_indices = list(range(total - 1, -1, -1))
        print(f"  Mode: reverse all pages")
    else:
        page_indices = parse_order(args.order, total)
        if not page_indices:
            print("No valid pages in order specification.", file=sys.stderr)
            sys.exit(1)
        print(f"  Order: {[i + 1 for i in page_indices]}")

    # Validate
    for idx in page_indices:
        if idx < 0 or idx >= total:
            print(f"  ⚠ Page index {idx + 1} out of range (1-{total})",
                  file=sys.stderr)
            sys.exit(1)

    writer = PdfWriter()
    for idx in page_indices:
        writer.add_page(reader.pages[idx])

    # Copy metadata
    if args.keep_metadata and reader.metadata:
        writer.add_metadata(reader.metadata)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "wb") as f:
        writer.write(f)

    print(f"\n✓ {len(page_indices)} pages → {out}")
    if len(page_indices) != total:
        print(f"  ℹ Original had {total} pages, output has {len(page_indices)}")


if __name__ == "__main__":
    main()

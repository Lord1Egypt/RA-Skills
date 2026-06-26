#!/usr/bin/env python3
"""
list_fonts.py — List all fonts used in a PDF document.

Shows font name, type, encoding, and which pages use each font.

Usage:
    python scripts/list_fonts.py input.pdf
    python scripts/list_fonts.py input.pdf --json
    python scripts/list_fonts.py input.pdf --pages 1-5
    python scripts/list_fonts.py *.pdf
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from pypdf import PdfReader


def extract_fonts(pdf_path: Path, page_range: str = None) -> dict:
    """Extract font information from a PDF file."""
    reader = PdfReader(str(pdf_path))
    total = len(reader.pages)

    if page_range:
        indices = parse_range(page_range, total)
    else:
        indices = list(range(total))

    # font_key → {info + pages}
    fonts = {}
    font_pages = defaultdict(set)

    for i in indices:
        page = reader.pages[i]
        page_fonts = _get_page_fonts(page)
        for font_key, font_info in page_fonts.items():
            if font_key not in fonts:
                fonts[font_key] = font_info
            font_pages[font_key].add(i + 1)

    # Build result
    result = []
    for font_key in sorted(fonts.keys()):
        info = fonts[font_key]
        info["pages"] = sorted(font_pages[font_key])
        info["page_count"] = len(info["pages"])
        result.append(info)

    return {
        "file": str(pdf_path),
        "total_pages": total,
        "pages_scanned": len(indices),
        "font_count": len(result),
        "fonts": result,
    }


def _get_page_fonts(page) -> dict:
    """Extract fonts from a single page's resources."""
    fonts = {}

    resources = page.get("/Resources")
    if not resources:
        return fonts

    font_dict = resources.get("/Font")
    if not font_dict:
        return fonts

    font_obj = font_dict.get_object() if hasattr(font_dict, "get_object") else font_dict

    for font_name, font_ref in font_obj.items():
        try:
            font = font_ref.get_object() if hasattr(font_ref, "get_object") else font_ref

            base_font = str(font.get("/BaseFont", "unknown"))
            if base_font.startswith("/"):
                base_font = base_font[1:]

            # Clean up subset prefix (e.g., "ABCDEF+ArialMT" → "ArialMT")
            clean_name = base_font
            if "+" in base_font and len(base_font.split("+")[0]) == 6:
                clean_name = base_font.split("+", 1)[1]

            font_type = str(font.get("/Subtype", "unknown"))
            if font_type.startswith("/"):
                font_type = font_type[1:]

            encoding = str(font.get("/Encoding", ""))
            if encoding.startswith("/"):
                encoding = encoding[1:]

            # Check if embedded
            font_descriptor = font.get("/FontDescriptor")
            is_embedded = False
            if font_descriptor:
                fd = font_descriptor.get_object() if hasattr(font_descriptor, "get_object") else font_descriptor
                is_embedded = any(
                    fd.get(key) is not None
                    for key in ("/FontFile", "/FontFile2", "/FontFile3")
                )

            fonts[base_font] = {
                "name": clean_name,
                "full_name": base_font,
                "resource_name": font_name,
                "type": font_type,
                "encoding": encoding or "default",
                "embedded": is_embedded,
            }
        except Exception:
            fonts[str(font_name)] = {
                "name": str(font_name),
                "full_name": str(font_name),
                "resource_name": font_name,
                "type": "unknown",
                "encoding": "unknown",
                "embedded": False,
            }

    return fonts


def parse_range(spec: str, total: int) -> list[int]:
    """Parse '1-5,7' → [0,1,2,3,4,6]."""
    indices = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            indices.update(range(int(a) - 1, min(int(b), total)))
        else:
            indices.add(int(part) - 1)
    return sorted(indices)


def print_fonts(data: dict) -> None:
    """Pretty-print font information."""
    print(f"\n{'='*60}")
    print(f"📄 {data['file']}")
    print(f"{'='*60}")
    print(f"  Pages scanned: {data['pages_scanned']}/{data['total_pages']}")
    print(f"  Fonts found:   {data['font_count']}")
    print()

    if not data["fonts"]:
        print("  No fonts found (might be an image-based/scanned PDF)")
        return

    # Table header
    print(f"  {'Font Name':<35} {'Type':<12} {'Embedded':<10} {'Encoding':<15} {'Pages'}")
    print(f"  {'─'*35} {'─'*12} {'─'*10} {'─'*15} {'─'*20}")

    for f in data["fonts"]:
        embedded = "✓ Yes" if f["embedded"] else "✗ No"
        pages_str = _compact_pages(f["pages"])
        print(f"  {f['name']:<35} {f['type']:<12} {embedded:<10} {f['encoding']:<15} {pages_str}")

    print()

    # Warnings
    non_embedded = [f["name"] for f in data["fonts"] if not f["embedded"]]
    if non_embedded:
        print(f"  ⚠ {len(non_embedded)} non-embedded font(s) — may display differently on other systems:")
        for name in non_embedded[:5]:
            print(f"    • {name}")
        if len(non_embedded) > 5:
            print(f"    ... and {len(non_embedded) - 5} more")
    print()


def _compact_pages(pages: list[int]) -> str:
    """Compact page list: [1,2,3,5,7,8,9] → '1-3, 5, 7-9'."""
    if not pages:
        return ""
    if len(pages) <= 3:
        return ", ".join(str(p) for p in pages)

    ranges = []
    start = pages[0]
    end = pages[0]
    for p in pages[1:]:
        if p == end + 1:
            end = p
        else:
            ranges.append(f"{start}-{end}" if start != end else str(start))
            start = end = p
    ranges.append(f"{start}-{end}" if start != end else str(start))
    return ", ".join(ranges)


def main():
    parser = argparse.ArgumentParser(
        description="List all fonts used in a PDF document"
    )
    parser.add_argument("inputs", nargs="+", help="Input PDF file(s)")
    parser.add_argument("--json", "-j", action="store_true",
                        help="Output as JSON")
    parser.add_argument("--pages", "-p",
                        help="Page range to scan, e.g. '1-5'")
    args = parser.parse_args()

    all_data = []
    for pattern in args.inputs:
        from glob import glob as g
        expanded = g(pattern)
        paths = [Path(p) for p in expanded] if expanded else [Path(pattern)]

        for path in paths:
            if not path.exists():
                print(f"  ✗ Not found: {path}", file=sys.stderr)
                continue
            try:
                data = extract_fonts(path, args.pages)
                all_data.append(data)
                if not args.json:
                    print_fonts(data)
            except Exception as e:
                print(f"  ✗ Error reading {path}: {e}", file=sys.stderr)

    if args.json:
        output = all_data if len(all_data) > 1 else (all_data[0] if all_data else {})
        print(json.dumps(output, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()

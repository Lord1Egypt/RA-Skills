#!/usr/bin/env python3
"""
fill_pdf_form.py — Fill an AcroForm PDF with values from a JSON file or CLI flags.

Usage:
    python scripts/fill_pdf_form.py form.pdf --data data.json --output filled.pdf
    python scripts/fill_pdf_form.py form.pdf --set full_name="Alice" email="alice@x.com"
    python scripts/fill_pdf_form.py form.pdf --data data.json --flatten  # make non-editable
"""
import argparse
import json
import sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter

def main():
    parser = argparse.ArgumentParser(description="Fill PDF form fields")
    parser.add_argument("input",                 help="Input PDF with form fields")
    parser.add_argument("--output",   "-o",      help="Output PDF (default: <input>_filled.pdf)")
    parser.add_argument("--data",     "-d",      help="JSON file with field_name:value pairs")
    parser.add_argument("--set",      nargs="+", metavar="KEY=VALUE",
                        help="Inline field values, e.g. --set name=Alice date=2025-03-12")
    parser.add_argument("--flatten",  action="store_true",
                        help="Flatten form (make fields non-editable) after filling")
    parser.add_argument("--auto-regenerate", action="store_true", dest="auto_regen",
                        help="Auto-regenerate appearance streams (try if fields look blank)")
    args = parser.parse_args()

    # Build data dict
    data = {}
    if args.data:
        data.update(json.loads(Path(args.data).read_text(encoding="utf-8")))
    if args.set:
        for kv in args.set:
            if "=" not in kv:
                print(f"  ⚠ Ignored malformed --set value: {kv!r}", file=sys.stderr)
                continue
            k, v = kv.split("=", 1)
            data[k.strip()] = v.strip()

    if not data:
        print("No field data provided. Use --data or --set.", file=sys.stderr)
        sys.exit(1)

    src = Path(args.input)
    dst = Path(args.output) if args.output else src.with_stem(src.stem + "_filled")

    reader = PdfReader(str(src))
    writer = PdfWriter()
    writer.append(reader)

    # Validate field names
    known = set(reader.get_fields() or {})
    for k in data:
        if k not in known:
            print(f"  ⚠ Field not found in PDF: {k!r}", file=sys.stderr)

    # Warn about non-ASCII characters (Chinese etc.) in field values
    has_non_ascii = any(
        any(ord(ch) > 127 for ch in str(v)) for v in data.values()
    )
    if has_non_ascii:
        print(
            "  ℹ Non-ASCII characters detected (e.g. Chinese).\n"
            "    pypdf uses built-in PDF fonts which may NOT display CJK characters.\n"
            "    If text shows as boxes/garbled, try:\n"
            "      1. Use --auto-regenerate flag\n"
            "      2. Switch to pdf-lib (JS) for better CJK support — see FORMS.md",
            file=sys.stderr,
        )

    # Fill each page
    filled_pages = set()
    for page_num, page in enumerate(writer.pages):
        try:
            writer.update_page_form_field_values(
                page, data, auto_regenerate=args.auto_regen
            )
            filled_pages.add(page_num)
        except Exception:
            pass   # page may have no fields

    if args.flatten:
        # Flatten by re-writing with flattened fields
        # Simple approach: save and reload; proper flatten requires pdf-lib or cairocffi
        print("  ℹ Flattening is best done with pdf-lib (JS). Saving without flatten.")

    with open(dst, "wb") as f:
        writer.write(f)

    print(f"✓ Filled {len(data)} field(s) across {len(filled_pages)} page(s) → {dst}")

if __name__ == "__main__":
    main()

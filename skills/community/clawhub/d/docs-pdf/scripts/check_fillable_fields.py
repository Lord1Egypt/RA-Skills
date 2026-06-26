#!/usr/bin/env python3
"""
check_fillable_fields.py — List all form fields in a PDF.

Usage:
    python scripts/check_fillable_fields.py form.pdf
    python scripts/check_fillable_fields.py form.pdf --json
"""
import argparse
import json
import sys
from pathlib import Path
from pypdf import PdfReader

FIELD_TYPES = {
    "/Tx":  "Text",
    "/Btn": "Button/Checkbox/Radio",
    "/Ch":  "Dropdown/ListBox",
    "/Sig": "Signature",
}

def main():
    parser = argparse.ArgumentParser(description="List PDF form fields")
    parser.add_argument("input",           help="Input PDF path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    reader = PdfReader(args.input)
    fields = reader.get_fields()

    if not fields:
        print("No fillable fields found in this PDF.")
        print("This is likely a flat (non-fillable) or scanned document.")
        sys.exit(0)

    if args.json:
        out = {}
        for name, field in fields.items():
            out[name] = {
                "type":    FIELD_TYPES.get(field.get("/FT",""), field.get("/FT","")),
                "value":   str(field.get("/V", "")),
                "default": str(field.get("/DV", "")),
                "options": [str(o) for o in (field.get("/Opt") or [])],
            }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    print(f"Found {len(fields)} field(s) in {Path(args.input).name}:\n")
    print(f"{'Field Name':<35} {'Type':<22} {'Current Value'}")
    print("-" * 75)
    for name, field in sorted(fields.items()):
        ftype = FIELD_TYPES.get(field.get("/FT", ""), field.get("/FT", "unknown"))
        value = str(field.get("/V", "[empty]"))
        opts  = field.get("/Opt")
        print(f"  {name:<33} {ftype:<22} {value}")
        if opts:
            print(f"    Options: {[str(o) for o in opts]}")

if __name__ == "__main__":
    main()

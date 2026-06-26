#!/usr/bin/env python3
"""
Render a .docx template using a JSON data file.

Usage:
  docxtpl-render-json.py template.docx data.json output.docx
  docxtpl-render-json.py template.docx data.json output.docx --autoescape
  docxtpl-render-json.py template.docx data.json output.docx -o
"""

import argparse
import json
import sys
from pathlib import Path

from docxtpl import DocxTemplate


def main():
    parser = argparse.ArgumentParser(description="Render a docx template from a JSON file")
    parser.add_argument("template", help="Path to .docx template")
    parser.add_argument("json", help="Path to JSON file with context data")
    parser.add_argument("output", help="Path to save the generated .docx")
    parser.add_argument("--autoescape", action="store_true",
                        help="Enable auto-escaping for XML special chars")
    parser.add_argument("--overwrite", "-o", action="store_true",
                        help="Overwrite output file if it exists")

    args = parser.parse_args()

    out = Path(args.output)
    if out.exists() and not args.overwrite:
        print(f"Error: {out} already exists. Use --overwrite to replace.", file=sys.stderr)
        sys.exit(1)

    with open(args.json) as f:
        context = json.load(f)

    doc = DocxTemplate(args.template)
    doc.render(context, autoescape=args.autoescape)
    doc.save(str(out))
    print(f"✅ Generated: {out}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Render a .docx template with variables passed as key=value pairs.

Usage:
  docxtpl-render.py template.docx output.docx name="Alice" department="Cardiology"
  docxtpl-render.py template.docx output.docx --json '{"name":"Alice","age":30}'
  docxtpl-render.py template.docx output.docx -f data.json
"""

import argparse
import json
import sys
from pathlib import Path

from docxtpl import DocxTemplate


def parse_kv(kv: str) -> tuple:
    key, _, val = kv.partition("=")
    if not key or not _:
        raise ValueError(f"Invalid key=value: {kv}")
    return key.strip(), val.strip()


def main():
    parser = argparse.ArgumentParser(description="Render a docx template from CLI arguments")
    parser.add_argument("template", help="Path to .docx template")
    parser.add_argument("output", help="Path to save the generated .docx")
    parser.add_argument("vars", nargs="*", metavar="key=value",
                        help="Template variables as key=value pairs")
    parser.add_argument("--json", "-j", help="JSON string with context data")
    parser.add_argument("--file", "-f", help="JSON file with context data")
    parser.add_argument("--autoescape", action="store_true",
                        help="Enable auto-escaping for XML special chars")
    parser.add_argument("--overwrite", "-o", action="store_true",
                        help="Overwrite output file if it exists")

    args = parser.parse_args()

    out = Path(args.output)
    if out.exists() and not args.overwrite:
        print(f"Error: {out} already exists. Use --overwrite to replace.", file=sys.stderr)
        sys.exit(1)

    # Build context
    context = {}

    # 1. key=value pairs
    for kv in args.vars:
        try:
            k, v = parse_kv(kv)
            context[k] = v
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    # 2. JSON string
    if args.json:
        try:
            extra = json.loads(args.json)
            context.update(extra)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}", file=sys.stderr)
            sys.exit(1)

    # 3. JSON file
    if args.file:
        try:
            with open(args.file) as f:
                extra = json.load(f)
            context.update(extra)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading {args.file}: {e}", file=sys.stderr)
            sys.exit(1)

    if not context:
        print("Warning: No context variables provided. Template will be rendered as-is.", file=sys.stderr)

    # Render
    doc = DocxTemplate(args.template)
    doc.render(context, autoescape=args.autoescape)
    doc.save(str(out))
    print(f"✅ Generated: {out}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
List all undeclared template variables in a .docx template.

Usage:
  docxtpl-list-vars.py template.docx
  docxtpl-list-vars.py template.docx --existing '{"name":"Alice"}'  # omit already-known vars
  docxtpl-list-vars.py template.docx --json                         # JSON output
"""

import argparse
import json
import sys
from pathlib import Path

from docxtpl import DocxTemplate


def main():
    parser = argparse.ArgumentParser(description="List template variables in a docx template")
    parser.add_argument("template", help="Path to .docx template")
    parser.add_argument("--existing", help="JSON string of already known variables to exclude")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON array")
    parser.add_argument("--file", "-f", help="JSON file of already known variables")
    parser.add_argument("--count", action="store_true", help="Only show variable count")

    args = parser.parse_args()

    if not Path(args.template).exists():
        print(f"Error: {args.template} not found", file=sys.stderr)
        sys.exit(1)

    context = {}
    if args.existing:
        context.update(json.loads(args.existing))
    if args.file:
        with open(args.file) as f:
            context.update(json.load(f))

    doc = DocxTemplate(args.template)
    missing = doc.get_undeclared_template_variables(context=context or None)

    if args.count:
        print(len(missing))
        return

    if not missing:
        print("✅ All template variables are declared.")
        return

    missing_sorted = sorted(missing)

    if args.json:
        print(json.dumps(missing_sorted, indent=2))
    else:
        print(f"Missing variables ({len(missing_sorted)}):")
        for v in missing_sorted:
            print(f"  {v}")


if __name__ == "__main__":
    main()

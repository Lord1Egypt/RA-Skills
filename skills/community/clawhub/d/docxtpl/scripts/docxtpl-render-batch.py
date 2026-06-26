#!/usr/bin/env python3
"""
Batch render a .docx template from a CSV/TSV file.

Each row in the CSV becomes one rendered document, named by an ID column.

Usage:
  docxtpl-render-batch.py template.csv output_dir template.docx
  docxtpl-render-batch.py template.csv output_dir template.docx --id-column patient_id
  docxtpl-render-batch.py template.csv output_dir template.docx --delimiter tab
  docxtpl-render-batch.py template.csv output_dir template.docx --suffix _report
  docxtpl-render-batch.py template.csv output_dir template.docx --dry-run
"""

import argparse
import csv
import json
import sys
from pathlib import Path

from docxtpl import DocxTemplate


def main():
    parser = argparse.ArgumentParser(description="Batch render docx templates from a CSV/TSV file")
    parser.add_argument("datafile", help="Path to CSV/TSV file")
    parser.add_argument("output_dir", help="Directory to save generated files")
    parser.add_argument("template", help="Path to .docx template")
    parser.add_argument("--id-column", default="id",
                        help="Column name to use as output filename base (default: 'id')")
    parser.add_argument("--delimiter", choices=["comma", "tab", "pipe"], default="comma",
                        help="Field delimiter (default: comma)")
    parser.add_argument("--suffix", default="",
                        help="Suffix appended to output filenames before .docx")
    parser.add_argument("--encoding", default="utf-8",
                        help="File encoding (default: utf-8)")
    parser.add_argument("--overwrite", "-o", action="store_true",
                        help="Overwrite existing output files")
    parser.add_argument("--limit", type=int,
                        help="Limit number of rows to process")
    parser.add_argument("--start", type=int, default=0,
                        help="Start from row index (0-based)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would be generated without writing files")
    parser.add_argument("--autoescape", action="store_true",
                        help="Enable auto-escaping for XML special chars")
    parser.add_argument("--summary", action="store_true",
                        help="Print summary at the end")

    args = parser.parse_args()

    delimiters = {"comma": ",", "tab": "\t", "pipe": "|"}
    delim = delimiters[args.delimiter]

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Load template
    tpl = DocxTemplate(args.template)

    # Read data
    with open(args.datafile, encoding=args.encoding, newline="") as f:
        reader = csv.DictReader(f, delimiter=delim)
        rows = list(reader)

    if args.id_column not in rows[0] if rows else {}:
        print(f"Error: Column '{args.id_column}' not found in data file. "
              f"Available columns: {list(rows[0].keys()) if rows else 'none'}",
              file=sys.stderr)
        sys.exit(1)

    if args.start:
        rows = rows[args.start:]
    if args.limit:
        rows = rows[:args.limit]

    generated = 0
    skipped = 0

    for i, row in enumerate(rows):
        base_name = row[args.id_column].strip()
        if not base_name:
            print(f"Warning: Row {i} has empty {args.id_column}, skipping", file=sys.stderr)
            skipped += 1
            continue

        output_path = out_dir / f"{base_name}{args.suffix}.docx"
        if output_path.exists() and not args.overwrite:
            print(f"Skip (exists): {output_path}", file=sys.stderr)
            skipped += 1
            continue

        if args.dry_run:
            print(f"[DRY RUN] Would generate: {output_path}")
            generated += 1
            continue

        tpl.render(row, autoescape=args.autoescape)
        tpl.save(str(output_path))
        tpl.reset_replacements()
        print(f"✅ {output_path}")
        generated += 1

    if args.summary or args.dry_run:
        print(f"\n--- Summary: {generated} generated, {skipped} skipped ---")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
concat.py - Stack multiple CSV / TSV / JSONL files vertically (UNION ALL).

By default, the output header is the UNION of all input headers in the order
they first appear. Cells missing in an input are written as the empty string.
Use --strict to require every input to have exactly the same header.

Streams one input at a time; peak memory does not depend on the number or
size of input files.

Usage:
    concat.py OUTPUT INPUT1 INPUT2 [INPUT3 ...]

Options:
    --strict             require every input to have an identical header
    --add-source COL     add a column named COL with the source filename
                         (or --source-stem to use the file stem)
    --source-stem        use the file stem (no extension) rather than full name
    --dedupe             drop exact duplicate rows across all inputs
    --json               emit machine-readable summary on stdout
    -h, --help           show this help

Examples:
    concat.py all.csv jan.csv feb.csv mar.csv
    concat.py all.csv shard_*.csv --add-source origin --source-stem
    concat.py all.jsonl events_*.jsonl --dedupe

Exit codes:
    0  success
    1  result is empty (no rows produced)
    2  bad arguments / unsafe path / missing file / strict-header mismatch /
       missing output extension
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import List

from _common import open_table, safe_path

ALLOWED_OUTPUT_EXTS = {".csv", ".tsv", ".jsonl"}


def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("output", nargs="?")
    p.add_argument("inputs", nargs="*")
    p.add_argument("--strict", action="store_true")
    p.add_argument("--add-source", dest="add_source")
    p.add_argument("--source-stem", dest="source_stem", action="store_true")
    p.add_argument("--dedupe", action="store_true")
    p.add_argument("--json", dest="as_json", action="store_true")
    p.add_argument("-h", "--help", action="store_true")
    args = p.parse_args()

    if args.help or not args.output or len(args.inputs) < 1:
        print(__doc__)
        return 0 if args.help else 2

    try:
        out_path = safe_path(args.output)
        in_paths = [safe_path(p) for p in args.inputs]
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    ext = out_path.suffix.lower()
    if ext not in ALLOWED_OUTPUT_EXTS:
        print(f"Error: unsupported output extension '{ext}'. "
              f"Allowed: {', '.join(sorted(ALLOWED_OUTPUT_EXTS))}.", file=sys.stderr)
        return 2

    for p in in_paths:
        if not p.is_file():
            print(f"Error: not a file: {p}", file=sys.stderr)
            return 2

    # First pass: gather headers in order of first appearance (also check --strict)
    union_header: List[str] = []
    seen: set = set()
    first_header: List[str] = []
    for i, path in enumerate(in_paths):
        with open_table(path) as (_kind, header, _it):
            if i == 0:
                first_header = list(header)
            elif args.strict and list(header) != first_header:
                print(f"Error: --strict header mismatch.\n"
                      f"  {in_paths[0]}: {first_header}\n"
                      f"  {path}: {list(header)}", file=sys.stderr)
                return 2
            for col in header:
                if col not in seen:
                    seen.add(col)
                    union_header.append(col)

    if args.add_source:
        if args.add_source in seen:
            print(f"Error: --add-source column '{args.add_source}' already exists "
                  f"in input headers", file=sys.stderr)
            return 2
        union_header.append(args.add_source)

    # Second pass: stream rows
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fmt = "jsonl" if ext == ".jsonl" else ("tsv" if ext == ".tsv" else "csv")

    rows_written = 0
    dedupe_set: set = set()
    per_file_counts: List[dict] = []

    with open(out_path, "w", encoding="utf-8", newline="") as fout:
        if fmt == "jsonl":
            def emit(row):
                fout.write(json.dumps(row, ensure_ascii=False) + "\n")
        else:
            delim = "\t" if fmt == "tsv" else ","
            csvw = csv.DictWriter(fout, fieldnames=union_header, delimiter=delim,
                                  extrasaction="ignore")
            csvw.writeheader()
            def emit(row):
                csvw.writerow(row)

        for path in in_paths:
            kept_from_file = 0
            with open_table(path) as (_kind, _hdr, reader):
                tag = path.stem if args.source_stem else path.name
                for row in reader:
                    out_row = {c: row.get(c, "") for c in union_header}
                    if args.add_source:
                        out_row[args.add_source] = tag
                    if args.dedupe:
                        key = tuple(out_row.get(c, "") for c in union_header)
                        if key in dedupe_set:
                            continue
                        dedupe_set.add(key)
                    emit(out_row)
                    rows_written += 1
                    kept_from_file += 1
            per_file_counts.append({"file": str(path), "rows_written": kept_from_file})

    summary = {
        "output": str(out_path),
        "inputs": [str(p) for p in in_paths],
        "rows_written": rows_written,
        "columns": union_header,
        "strict": args.strict,
        "dedupe": args.dedupe,
        "per_file": per_file_counts,
    }
    if args.as_json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"Concat: {len(in_paths)} files -> {out_path} ({rows_written} rows, "
              f"{len(union_header)} columns)")

    return 0 if rows_written > 0 else 1


if __name__ == "__main__":
    sys.exit(main())

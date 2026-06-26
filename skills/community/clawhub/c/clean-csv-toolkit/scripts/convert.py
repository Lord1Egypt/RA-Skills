#!/usr/bin/env python3
"""
Convert between tabular formats: CSV, TSV, JSON Lines, and Markdown table.

Input format is auto-detected from extension and content. Output format is
picked from the output file extension:
  .csv      -> comma-separated values
  .tsv      -> tab-separated values
  .jsonl    -> JSON Lines (one object per line)
  .json     -> JSON array of objects
  .md       -> GitHub-flavored Markdown table

Usage:
  python3 convert.py <input> <output>
  python3 convert.py data.csv data.jsonl
  python3 convert.py data.jsonl data.md
  python3 convert.py data.csv data.json --pretty

Exit codes:
  0 = success
  1 = conversion failed mid-stream
  2 = bad arguments / missing input / unsafe path / unsupported extension
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Dict, List

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from _common import (
    safe_path,
    open_table,
    print_error,
)


ALLOWED_OUT = {".csv", ".tsv", ".jsonl", ".json", ".md"}


def write_csv(out: Path, headers: List[str], rows: List[Dict[str, str]],
              delimiter: str = ",") -> None:
    with out.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=headers, delimiter=delimiter)
        writer.writeheader()
        for r in rows:
            writer.writerow({h: r.get(h, "") for h in headers})


def write_jsonl(out: Path, headers: List[str], rows: List[Dict[str, str]]) -> None:
    with out.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps({h: r.get(h, "") for h in headers},
                                ensure_ascii=False) + "\n")


def write_json(out: Path, headers: List[str], rows: List[Dict[str, str]],
               pretty: bool) -> None:
    payload = [{h: r.get(h, "") for h in headers} for r in rows]
    indent = 2 if pretty else None
    with out.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=indent)
        fh.write("\n")


def _md_escape(value: str) -> str:
    """Pipe and newline characters break markdown tables; escape them."""
    return value.replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ").replace("\r", "")


def write_md(out: Path, headers: List[str], rows: List[Dict[str, str]]) -> None:
    with out.open("w", encoding="utf-8") as fh:
        fh.write("| " + " | ".join(_md_escape(h) for h in headers) + " |\n")
        fh.write("|" + "|".join(" --- " for _ in headers) + "|\n")
        for r in rows:
            cells = [_md_escape(str(r.get(h, ""))) for h in headers]
            fh.write("| " + " | ".join(cells) + " |\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[1])
    parser.add_argument("input", help="Input file (.csv / .tsv / .jsonl / .json)")
    parser.add_argument("output", help="Output file (extension picks format)")
    parser.add_argument("--pretty", action="store_true",
                        help="Pretty-print JSON output (only affects .json)")
    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Suppress non-error stdout")
    args = parser.parse_args()

    try:
        in_path = safe_path(args.input).resolve()
        out_path = safe_path(args.output).resolve()
    except ValueError as e:
        print_error(str(e))
        return 2

    if not in_path.is_file():
        print_error(f"input not a file: {in_path}")
        return 2

    ext = out_path.suffix.lower()
    if ext not in ALLOWED_OUT:
        print_error(
            f"unsupported output extension {ext!r}. "
            f"Allowed: {', '.join(sorted(ALLOWED_OUT))}."
        )
        return 2

    try:
        with open_table(in_path) as (kind, headers, row_iter):
            if not headers:
                print_error("input has no header row")
                return 2
            rows: List[Dict[str, str]] = list(row_iter)
    except Exception as e:
        print_error(f"could not read {in_path}: {e.__class__.__name__}: {e}")
        return 2

    out_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        if ext == ".csv":
            write_csv(out_path, headers, rows, delimiter=",")
        elif ext == ".tsv":
            write_csv(out_path, headers, rows, delimiter="\t")
        elif ext == ".jsonl":
            write_jsonl(out_path, headers, rows)
        elif ext == ".json":
            write_json(out_path, headers, rows, pretty=args.pretty)
        elif ext == ".md":
            write_md(out_path, headers, rows)
    except Exception as e:
        print_error(f"write failed: {e.__class__.__name__}: {e}")
        return 1

    if not args.quiet:
        print(f"Converted {kind} -> {ext.lstrip('.')}: "
              f"{len(rows)} rows, {len(headers)} cols -> {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

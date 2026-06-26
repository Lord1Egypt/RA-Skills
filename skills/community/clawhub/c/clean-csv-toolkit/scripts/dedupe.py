#!/usr/bin/env python3
"""
Remove duplicate rows from a CSV / TSV / JSONL file.

Two modes:
  - Full-row dedup (default): two rows are duplicates iff every column value matches.
  - Keyed dedup: pass --key col1,col2,... ; rows are duplicates iff the chosen
    key columns all match. Useful when only one canonical row per id is wanted.

Outputs a clean copy (without duplicates) and a separate JSONL report of the
rows that were removed and why.

Usage:
  python3 dedupe.py <input> <clean_output> [--key col1,col2,...]
                                           [--removed-report removed.jsonl]
                                           [--keep first|last]
                                           [--case-insensitive]
                                           [--trim]

Exit codes:
  0 = success (at least one input row processed)
  1 = no rows in input
  2 = bad arguments / missing input / unsafe path
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from _common import (
    safe_path,
    sniff_dialect,
    sniff_encoding,
    open_table,
    print_error,
)


def make_key(row: Dict[str, str], key_columns: List[str],
             case_insensitive: bool, trim: bool) -> Tuple[str, ...]:
    parts: List[str] = []
    for c in key_columns:
        v = row.get(c, "")
        if v is None:
            v = ""
        v = str(v)
        if trim:
            v = v.strip()
        if case_insensitive:
            v = v.lower()
        parts.append(v)
    return tuple(parts)


def dedupe(input_path: Path, output_path: Path, key_columns: Optional[List[str]],
           keep: str, removed_report: Optional[Path],
           case_insensitive: bool, trim: bool) -> Dict:
    encoding = sniff_encoding(input_path)

    with open_table(input_path, encoding=encoding) as (kind, headers, rows):
        if not headers:
            raise ValueError("input has no header row")

        if key_columns:
            missing = [c for c in key_columns if c not in headers]
            if missing:
                raise ValueError(
                    f"key column(s) not present in header: {', '.join(missing)}"
                )
            cols_for_key = key_columns
        else:
            cols_for_key = headers

        # First pass: collect rows. For 'last' policy, we need to know which
        # row index for each key is the last occurrence.
        all_rows: List[Dict[str, str]] = list(rows)
        if not all_rows:
            return {
                "rows_in": 0,
                "rows_out": 0,
                "duplicates_removed": 0,
                "keep_policy": keep,
                "key_columns": cols_for_key,
            }

        seen: Dict[Tuple[str, ...], int] = {}  # key -> chosen row index
        removed: List[Tuple[int, Dict[str, str], Tuple[str, ...]]] = []

        for idx, row in enumerate(all_rows):
            key = make_key(row, cols_for_key, case_insensitive, trim)
            if key not in seen:
                seen[key] = idx
            else:
                if keep == "first":
                    removed.append((idx, row, key))
                else:  # keep == 'last'
                    prev_idx = seen[key]
                    removed.append((prev_idx, all_rows[prev_idx], key))
                    seen[key] = idx

        keep_indices = set(seen.values())
        kept_rows = [all_rows[i] for i in sorted(keep_indices)]

        # Write clean output as CSV with the same headers
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=headers)
            writer.writeheader()
            for r in kept_rows:
                writer.writerow({h: r.get(h, "") for h in headers})

        # Write removed-report (JSONL) if requested
        if removed_report is not None:
            removed_report.parent.mkdir(parents=True, exist_ok=True)
            with removed_report.open("w", encoding="utf-8") as fh:
                for idx, row, key in removed:
                    fh.write(json.dumps({
                        "original_row_index": idx + 1,  # 1-based, header is row 0
                        "key": list(key),
                        "row": row,
                    }, ensure_ascii=False) + "\n")

        return {
            "rows_in": len(all_rows),
            "rows_out": len(kept_rows),
            "duplicates_removed": len(removed),
            "keep_policy": keep,
            "key_columns": cols_for_key,
            "clean_output": str(output_path),
            "removed_report": str(removed_report) if removed_report else None,
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[1])
    parser.add_argument("input", help="Path to a .csv / .tsv / .jsonl file")
    parser.add_argument("output", help="Path for the deduplicated CSV output")
    parser.add_argument("--key", default="",
                        help="Comma-separated list of key columns. "
                             "If omitted, full row is the key.")
    parser.add_argument("--removed-report", default="",
                        help="Optional JSONL path; receives one entry per removed row")
    parser.add_argument("--keep", choices=("first", "last"), default="first",
                        help="Which occurrence to keep when duplicates are found "
                             "(default: first)")
    parser.add_argument("--case-insensitive", action="store_true",
                        help="Compare key column values case-insensitively")
    parser.add_argument("--trim", action="store_true",
                        help="Strip surrounding whitespace from key column values "
                             "before comparison")
    parser.add_argument("--json", action="store_true", help="Emit JSON summary")
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

    removed_path: Optional[Path] = None
    if args.removed_report:
        try:
            removed_path = safe_path(args.removed_report).resolve()
        except ValueError as e:
            print_error(str(e))
            return 2

    key_columns: Optional[List[str]] = None
    if args.key.strip():
        key_columns = [c.strip() for c in args.key.split(",") if c.strip()]
        if not key_columns:
            print_error("--key must contain at least one column name")
            return 2

    try:
        report = dedupe(
            in_path, out_path, key_columns,
            keep=args.keep, removed_report=removed_path,
            case_insensitive=args.case_insensitive, trim=args.trim,
        )
    except ValueError as e:
        print_error(str(e))
        return 2
    except Exception as e:
        print_error(f"dedupe failed: {e.__class__.__name__}: {e}")
        return 2

    if report["rows_in"] == 0:
        print_error("input has no data rows")
        return 1

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"rows_in:             {report['rows_in']}")
        print(f"rows_out:            {report['rows_out']}")
        print(f"duplicates_removed:  {report['duplicates_removed']}")
        print(f"key_columns:         {', '.join(report['key_columns'])}")
        print(f"keep_policy:         {report['keep_policy']}")
        print(f"clean_output:        {report['clean_output']}")
        if report["removed_report"]:
            print(f"removed_report:      {report['removed_report']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

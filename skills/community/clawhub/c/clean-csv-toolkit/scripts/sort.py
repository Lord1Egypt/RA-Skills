#!/usr/bin/env python3
"""
sort.py - Sort a CSV / TSV / JSONL file by one or more columns.

Type-aware: each --by column is sorted numerically when ALL its values
parse as numbers, otherwise lexicographically. Stable sort preserves
original row order for ties.

Loads all rows into memory (a real external merge-sort would be overkill
for stdlib; for the sizes this skill targets, in-memory sort comfortably
handles 1M rows on a typical laptop).

Usage:
    sort.py INPUT OUTPUT --by COL[:asc|:desc][,COL2[:asc|:desc]...]

Options:
    --by COL[:DIR][,COL[:DIR]...]   sort keys; :asc (default) or :desc per column
    --numeric                       force numeric comparison on all sort cols
                                    (rows where the column is non-numeric sort last)
    --case-insensitive              case-fold string comparisons
    --limit N                       write only the first N rows after sorting
    --json                          emit machine-readable summary on stdout
    -h, --help                      show this help

Examples:
    sort.py sales.csv sorted.csv --by revenue:desc
    sort.py users.csv sorted.csv --by country:asc,signup_date:desc
    sort.py logs.csv top10.csv --by timestamp:desc --limit 10

Exit codes:
    0  success
    1  input is empty
    2  bad arguments / unsafe path / missing file / missing column
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import List, Tuple

from _common import open_table, safe_path

ALLOWED_OUTPUT_EXTS = {".csv", ".tsv", ".jsonl"}


def parse_keys(spec: str) -> List[Tuple[str, str]]:
    out: List[Tuple[str, str]] = []
    for piece in spec.split(","):
        piece = piece.strip()
        if not piece:
            continue
        if ":" in piece:
            col, direction = piece.rsplit(":", 1)
            direction = direction.strip().lower()
            if direction not in ("asc", "desc"):
                raise ValueError(f"bad sort direction '{direction}' (expected asc/desc)")
        else:
            col, direction = piece, "asc"
        out.append((col.strip(), direction))
    if not out:
        raise ValueError("--by cannot be empty")
    return out


def to_number(v: str):
    try:
        return int(v)
    except (TypeError, ValueError):
        pass
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("input", nargs="?")
    p.add_argument("output", nargs="?")
    p.add_argument("--by")
    p.add_argument("--numeric", action="store_true")
    p.add_argument("--case-insensitive", dest="case_insensitive", action="store_true")
    p.add_argument("--limit", type=int)
    p.add_argument("--json", dest="as_json", action="store_true")
    p.add_argument("-h", "--help", action="store_true")
    args = p.parse_args()

    if args.help or not args.input or not args.output:
        print(__doc__)
        return 0 if args.help else 2
    if not args.by:
        print("Error: --by COL[:DIR][,...] is required", file=sys.stderr)
        return 2

    try:
        in_path = safe_path(args.input)
        out_path = safe_path(args.output)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    if not in_path.is_file():
        print(f"Error: not a file: {in_path}", file=sys.stderr)
        return 2

    ext = out_path.suffix.lower()
    if ext not in ALLOWED_OUTPUT_EXTS:
        print(f"Error: unsupported output extension '{ext}'. "
              f"Allowed: {', '.join(sorted(ALLOWED_OUTPUT_EXTS))}.", file=sys.stderr)
        return 2

    try:
        keys = parse_keys(args.by)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    # Pull all rows; validate columns and decide per-col numeric vs string mode
    with open_table(in_path) as (_kind, header, reader):
        for col, _d in keys:
            if col not in header:
                print(f"Error: sort column '{col}' not in header", file=sys.stderr)
                return 2
        rows = list(reader)

    if not rows:
        print("Warning: input has zero data rows", file=sys.stderr)
        if args.as_json:
            print(json.dumps({"output": str(out_path), "rows": 0}, indent=2))
        return 1

    # For each sort key, decide if numeric works on every row (or numeric forced)
    numeric_cols: List[bool] = []
    for col, _d in keys:
        if args.numeric:
            numeric_cols.append(True)
            continue
        ok = True
        for r in rows:
            v = r.get(col, "")
            if v == "":
                continue
            if to_number(v) is None:
                ok = False
                break
        numeric_cols.append(ok)

    # Python's sort is stable. To support per-key asc/desc with mixed types,
    # we sort from the LEAST significant key to the MOST significant key.
    for (col, direction), is_num in reversed(list(zip(keys, numeric_cols))):
        reverse = (direction == "desc")
        if is_num:
            def key_fn(r, c=col):
                n = to_number(r.get(c, ""))
                # Push empty/non-numeric values to the end regardless of direction
                if n is None:
                    return (1, 0.0)
                return (0, n)
        elif args.case_insensitive:
            def key_fn(r, c=col):
                return r.get(c, "").casefold()
        else:
            def key_fn(r, c=col):
                return r.get(c, "")
        rows.sort(key=key_fn, reverse=reverse)

    if args.limit and args.limit > 0:
        rows = rows[: args.limit]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fmt = "jsonl" if ext == ".jsonl" else ("tsv" if ext == ".tsv" else "csv")
    with open(out_path, "w", encoding="utf-8", newline="") as fout:
        if fmt == "jsonl":
            for r in rows:
                fout.write(json.dumps(r, ensure_ascii=False) + "\n")
        else:
            delim = "\t" if fmt == "tsv" else ","
            w = csv.DictWriter(fout, fieldnames=header, delimiter=delim, extrasaction="ignore")
            w.writeheader()
            for r in rows:
                w.writerow(r)

    summary = {
        "input": str(in_path),
        "output": str(out_path),
        "rows": len(rows),
        "keys": [{"col": c, "dir": d, "numeric": n}
                 for (c, d), n in zip(keys, numeric_cols)],
    }
    if args.as_json:
        print(json.dumps(summary, indent=2))
    else:
        key_desc = ", ".join(f"{c}:{d}{'(num)' if n else ''}"
                             for (c, d), n in zip(keys, numeric_cols))
        print(f"Sort: {len(rows)} rows by {key_desc} -> {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

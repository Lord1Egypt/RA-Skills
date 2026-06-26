#!/usr/bin/env python3
"""
merge.py - Join two CSV/TSV/JSONL files on one or more key columns.

Supports inner, left, right, and outer joins. Streams the right side into
memory (indexed by key) and the left side row-by-row, so peak memory is
roughly the size of the right file.

Usage:
    merge.py LEFT RIGHT OUTPUT --on KEY[,KEY2...] [options]

Options:
    --on COL[,COL2...]     join key column(s); required
    --left-on COL[,...]    join key(s) for LEFT (if different from RIGHT)
    --right-on COL[,...]   join key(s) for RIGHT (if different from LEFT)
    --how inner|left|right|outer
                           join type (default: inner)
    --suffix-left STR      suffix for LEFT-side duplicate columns (default: _x)
    --suffix-right STR     suffix for RIGHT-side duplicate columns (default: _y)
    --json                 emit a machine-readable summary to stdout
    -h, --help             show this help

Exit codes:
    0  success
    1  no rows matched (inner join produced 0 rows)
    2  bad arguments / missing files / unsafe paths / missing key column
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

from _common import open_table, safe_path

ALLOWED_OUTPUT_EXTS = {".csv", ".tsv", ".jsonl"}


def parse_keys(spec: str) -> List[str]:
    return [k.strip() for k in spec.split(",") if k.strip()]


def index_right(path: Path, keys: List[str]) -> Tuple[List[str], Dict[Tuple[str, ...], List[Dict[str, str]]]]:
    """Read RIGHT entirely into a dict keyed by the join keys."""
    index: Dict[Tuple[str, ...], List[Dict[str, str]]] = {}
    with open_table(path) as (_kind, header, reader):
        missing = [k for k in keys if k not in header]
        if missing:
            print(f"Error: right-side key(s) not found in header: {','.join(missing)}",
                  file=sys.stderr)
            raise SystemExit(2)
        for row in reader:
            key = tuple(row.get(k, "") for k in keys)
            index.setdefault(key, []).append(row)
    return header, index


def merged_header(left_header: List[str], right_header: List[str],
                  left_keys: List[str], right_keys: List[str],
                  suffix_left: str, suffix_right: str) -> Tuple[List[str], Dict[str, str], Dict[str, str]]:
    """Produce a deduplicated header. Returns header, left_rename, right_rename."""
    # The join keys themselves use the LEFT-side names (canonical).
    out: List[str] = list(left_header)
    left_rename: Dict[str, str] = {c: c for c in left_header}
    right_rename: Dict[str, str] = {}
    # Right-side keys are dropped from output (we keep the LEFT names).
    right_non_key = [c for c in right_header if c not in right_keys]
    for col in right_non_key:
        if col in out:
            # Disambiguate: rename LEFT occurrence too if we haven't already
            new_left = col + suffix_left
            new_right = col + suffix_right
            # Find and rename in `out`
            idx = out.index(col)
            out[idx] = new_left
            # Update left rename map
            for k, v in list(left_rename.items()):
                if v == col:
                    left_rename[k] = new_left
            out.append(new_right)
            right_rename[col] = new_right
        else:
            out.append(col)
            right_rename[col] = col
    return out, left_rename, right_rename


def write_row(writer, fmt: str, row: Dict[str, str]) -> None:
    if fmt == "jsonl":
        writer.write(json.dumps(row, ensure_ascii=False) + "\n")
    else:
        writer.writerow(row)


def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("left", nargs="?")
    p.add_argument("right", nargs="?")
    p.add_argument("output", nargs="?")
    p.add_argument("--on")
    p.add_argument("--left-on")
    p.add_argument("--right-on")
    p.add_argument("--how", default="inner", choices=("inner", "left", "right", "outer"))
    p.add_argument("--suffix-left", default="_x")
    p.add_argument("--suffix-right", default="_y")
    p.add_argument("--json", dest="as_json", action="store_true")
    p.add_argument("-h", "--help", action="store_true")
    args = p.parse_args()

    if args.help or not args.left or not args.right or not args.output:
        print(__doc__)
        return 0 if args.help else 2

    # Key resolution
    if args.on:
        left_keys = right_keys = parse_keys(args.on)
    elif args.left_on and args.right_on:
        left_keys = parse_keys(args.left_on)
        right_keys = parse_keys(args.right_on)
        if len(left_keys) != len(right_keys):
            print("Error: --left-on and --right-on must have the same number of columns",
                  file=sys.stderr)
            return 2
    else:
        print("Error: provide --on KEY or both --left-on and --right-on", file=sys.stderr)
        return 2

    try:
        left_path = safe_path(args.left)
        right_path = safe_path(args.right)
        out_path = safe_path(args.output)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    if not left_path.is_file():
        print(f"Error: not a file: {left_path}", file=sys.stderr)
        return 2
    if not right_path.is_file():
        print(f"Error: not a file: {right_path}", file=sys.stderr)
        return 2

    ext = out_path.suffix.lower()
    if ext not in ALLOWED_OUTPUT_EXTS:
        print(f"Error: unsupported output extension '{ext}'. "
              f"Allowed: {', '.join(sorted(ALLOWED_OUTPUT_EXTS))}.", file=sys.stderr)
        return 2

    # Index RIGHT
    try:
        right_header, right_index = index_right(right_path, right_keys)
    except SystemExit as e:
        return int(e.code) if isinstance(e.code, int) else 2
    except Exception as e:
        print(f"Error: failed to read right file: {e}", file=sys.stderr)
        return 2

    # Build output header (peek)
    with open_table(left_path) as (_kind, left_header, _it):
        missing = [k for k in left_keys if k not in left_header]
        if missing:
            print(f"Error: left-side key(s) not found in header: {','.join(missing)}",
                  file=sys.stderr)
            return 2

    out_header, left_rename, right_rename = merged_header(
        left_header, right_header, left_keys, right_keys,
        args.suffix_left, args.suffix_right,
    )

    fmt = "jsonl" if ext == ".jsonl" else ("tsv" if ext == ".tsv" else "csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows_written = 0
    left_only = 0
    right_only = 0
    matched = 0
    matched_right_keys: set = set()

    with open(out_path, "w", encoding="utf-8", newline="") as fout:
        if fmt == "jsonl":
            writer = fout
        else:
            delim = "\t" if fmt == "tsv" else ","
            writer = csv.DictWriter(fout, fieldnames=out_header, delimiter=delim,
                                    extrasaction="ignore")
            writer.writeheader()

        with open_table(left_path) as (_kind, _hdr, left_reader):
            for lrow in left_reader:
                key = tuple(lrow.get(k, "") for k in left_keys)
                rmatches = right_index.get(key, [])
                if rmatches:
                    matched += 1
                    matched_right_keys.add(key)
                    for rrow in rmatches:
                        merged: Dict[str, str] = {}
                        for lc, lc_out in left_rename.items():
                            merged[lc_out] = lrow.get(lc, "")
                        for rc, rc_out in right_rename.items():
                            merged[rc_out] = rrow.get(rc, "")
                        write_row(writer, fmt, merged)
                        rows_written += 1
                else:
                    if args.how in ("left", "outer"):
                        merged = {}
                        for lc, lc_out in left_rename.items():
                            merged[lc_out] = lrow.get(lc, "")
                        for rc, rc_out in right_rename.items():
                            merged[rc_out] = ""
                        write_row(writer, fmt, merged)
                        rows_written += 1
                        left_only += 1

        if args.how in ("right", "outer"):
            for rkey, rrows in right_index.items():
                if rkey in matched_right_keys:
                    continue
                for rrow in rrows:
                    merged = {}
                    # Fill LEFT side with blanks, except for keys which we
                    # populate from the right-side key values.
                    for lc, lc_out in left_rename.items():
                        if lc in left_keys:
                            idx = left_keys.index(lc)
                            merged[lc_out] = rkey[idx]
                        else:
                            merged[lc_out] = ""
                    for rc, rc_out in right_rename.items():
                        merged[rc_out] = rrow.get(rc, "")
                    write_row(writer, fmt, merged)
                    rows_written += 1
                    right_only += 1

    summary = {
        "left": str(left_path),
        "right": str(right_path),
        "output": str(out_path),
        "how": args.how,
        "on_left": left_keys,
        "on_right": right_keys,
        "rows_written": rows_written,
        "matched_rows": matched,
        "left_only_rows": left_only,
        "right_only_rows": right_only,
    }

    if args.as_json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"Merge: {left_path.name} {args.how} {right_path.name} on {','.join(left_keys)}")
        print(f"  Output: {out_path} ({rows_written} rows)")
        print(f"  Matched: {matched}, Left-only: {left_only}, Right-only: {right_only}")

    if args.how == "inner" and rows_written == 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

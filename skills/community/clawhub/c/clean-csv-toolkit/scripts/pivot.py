#!/usr/bin/env python3
"""
pivot.py - Group-by aggregation and wide pivots for CSV/TSV/JSONL.

Two modes:

  GROUP-BY (default):
      pivot.py INPUT OUTPUT --group-by COL[,COL2...] \\
                            --agg COL:FUNC[,COL:FUNC...]

  WIDE PIVOT (set --pivot-on):
      pivot.py INPUT OUTPUT --group-by ROW_COL --pivot-on COL_COL \\
                            --agg VAL_COL:FUNC

Aggregation functions: count, sum, avg/mean, min, max, first, last, nunique

Options:
    --group-by COL[,COL...]    grouping column(s); required
    --agg COL:FUNC[,...]       aggregations to compute
    --pivot-on COL             when set, produces a wide pivot table; --agg must
                               specify exactly one VALUE:FUNC pair
    --sort-by COL[,COL...]     sort output by these columns (default: group keys)
    --desc                     sort descending
    --fill VALUE               fill value for empty wide-pivot cells (default: "")
    --json                     emit a machine-readable summary to stdout
    -h, --help                 show this help

Exit codes:
    0  success
    1  empty result (no groups produced)
    2  bad arguments / missing files / unsafe paths / missing columns
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

from _common import open_table, safe_path

ALLOWED_OUTPUT_EXTS = {".csv", ".tsv", ".jsonl", ".md"}
ALLOWED_FUNCS = {"count", "sum", "avg", "mean", "min", "max", "first", "last", "nunique"}


def parse_cols(spec: str) -> List[str]:
    return [c.strip() for c in spec.split(",") if c.strip()]


def parse_agg(spec: str) -> List[Tuple[str, str]]:
    out: List[Tuple[str, str]] = []
    for piece in spec.split(","):
        piece = piece.strip()
        if not piece:
            continue
        if ":" not in piece:
            raise ValueError(f"bad --agg spec '{piece}', expected COL:FUNC")
        col, func = piece.rsplit(":", 1)
        col, func = col.strip(), func.strip().lower()
        if func not in ALLOWED_FUNCS:
            raise ValueError(f"unknown agg function '{func}'. "
                             f"Allowed: {', '.join(sorted(ALLOWED_FUNCS))}")
        out.append((col, func))
    if not out:
        raise ValueError("--agg cannot be empty")
    return out


def to_number(v: str):
    if v is None or v == "":
        return None
    try:
        return int(v)
    except (TypeError, ValueError):
        pass
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _sort_key(row: Dict[str, str], cols: List[str]):
    """Build a sort key that prefers numeric ordering when a column is fully
    numeric in this row, else falls back to string."""
    out = []
    for c in cols:
        v = row.get(c, "")
        n = to_number(v)
        # (0, number) sorts before (1, string), so keep types consistent per col
        out.append((0, n) if n is not None else (1, v))
    return tuple(out)


def format_number(x) -> str:
    if isinstance(x, float):
        if x.is_integer():
            return str(int(x))
        # Trim long floats
        return f"{x:.6f}".rstrip("0").rstrip(".")
    return str(x)


class Accum:
    __slots__ = ("count", "ssum", "nmin", "nmax", "first", "last", "seen", "n_numeric")

    def __init__(self) -> None:
        self.count = 0
        self.ssum = 0.0
        self.nmin = None
        self.nmax = None
        self.first = None
        self.last = None
        self.seen: set = set()
        self.n_numeric = 0

    def push(self, raw: str) -> None:
        self.count += 1
        if self.first is None:
            self.first = raw
        self.last = raw
        self.seen.add(raw)
        n = to_number(raw)
        if n is not None:
            self.n_numeric += 1
            self.ssum += n
            if self.nmin is None or n < self.nmin:
                self.nmin = n
            if self.nmax is None or n > self.nmax:
                self.nmax = n

    def value(self, func: str):
        if func == "count":
            return self.count
        if func == "sum":
            return format_number(self.ssum) if self.n_numeric else ""
        if func in ("avg", "mean"):
            return format_number(self.ssum / self.n_numeric) if self.n_numeric else ""
        if func == "min":
            return format_number(self.nmin) if self.nmin is not None else ""
        if func == "max":
            return format_number(self.nmax) if self.nmax is not None else ""
        if func == "first":
            return self.first if self.first is not None else ""
        if func == "last":
            return self.last if self.last is not None else ""
        if func == "nunique":
            return len(self.seen)
        return ""


def write_table(out_path: Path, header: List[str], rows: List[Dict[str, str]]) -> None:
    ext = out_path.suffix.lower()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if ext == ".jsonl":
        with open(out_path, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        return
    if ext == ".md":
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("| " + " | ".join(header) + " |\n")
            f.write("| " + " | ".join(["---"] * len(header)) + " |\n")
            for r in rows:
                f.write("| " + " | ".join(str(r.get(h, "")) for h in header) + " |\n")
        return
    delim = "\t" if ext == ".tsv" else ","
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header, delimiter=delim, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("input", nargs="?")
    p.add_argument("output", nargs="?")
    p.add_argument("--group-by")
    p.add_argument("--agg")
    p.add_argument("--pivot-on")
    p.add_argument("--sort-by")
    p.add_argument("--desc", action="store_true")
    p.add_argument("--fill", default="")
    p.add_argument("--json", dest="as_json", action="store_true")
    p.add_argument("-h", "--help", action="store_true")
    args = p.parse_args()

    if args.help or not args.input or not args.output:
        print(__doc__)
        return 0 if args.help else 2

    if not args.group_by:
        print("Error: --group-by is required", file=sys.stderr)
        return 2
    if not args.agg:
        print("Error: --agg is required", file=sys.stderr)
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

    group_cols = parse_cols(args.group_by)
    try:
        aggs = parse_agg(args.agg)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    wide = bool(args.pivot_on)
    if wide and len(aggs) != 1:
        print("Error: --pivot-on requires exactly one --agg COL:FUNC pair", file=sys.stderr)
        return 2

    # Validate columns (peek headers only)
    with open_table(in_path) as (_kind, header, _it):
        for c in group_cols:
            if c not in header:
                print(f"Error: group-by column '{c}' not found in header", file=sys.stderr)
                return 2
        for col, _func in aggs:
            if col not in header:
                print(f"Error: agg column '{col}' not found in header", file=sys.stderr)
                return 2
        if wide and args.pivot_on not in header:
            print(f"Error: --pivot-on column '{args.pivot_on}' not found in header",
                  file=sys.stderr)
            return 2

    # Single streaming pass
    if not wide:
        # accum[group_key][agg_index] = Accum
        groups: Dict[Tuple[str, ...], List[Accum]] = {}
        with open_table(in_path) as (_kind, _hdr, reader):
            for row in reader:
                key = tuple(row.get(c, "") for c in group_cols)
                bucket = groups.get(key)
                if bucket is None:
                    bucket = [Accum() for _ in aggs]
                    groups[key] = bucket
                for i, (col, _func) in enumerate(aggs):
                    bucket[i].push(row.get(col, ""))

        if not groups:
            print("Warning: input produced no groups", file=sys.stderr)
            if args.as_json:
                print(json.dumps({"output": str(out_path), "groups": 0, "wide": False}, indent=2))
            return 1

        header_out: List[str] = list(group_cols)
        for col, func in aggs:
            header_out.append(f"{col}_{func}")

        rows_out: List[Dict[str, str]] = []
        for key, bucket in groups.items():
            r: Dict[str, str] = {}
            for i, c in enumerate(group_cols):
                r[c] = key[i]
            for i, (col, func) in enumerate(aggs):
                r[f"{col}_{func}"] = str(bucket[i].value(func))
            rows_out.append(r)

        sort_cols = parse_cols(args.sort_by) if args.sort_by else group_cols
        try:
            rows_out.sort(key=lambda r: _sort_key(r, sort_cols), reverse=args.desc)
        except TypeError:
            pass

        write_table(out_path, header_out, rows_out)

        summary = {"output": str(out_path), "groups": len(rows_out),
                   "wide": False, "group_by": group_cols,
                   "agg": [{"col": c, "func": f} for c, f in aggs]}
        if args.as_json:
            print(json.dumps(summary, indent=2))
        else:
            print(f"Pivot: grouped {len(rows_out)} rows by {','.join(group_cols)} -> {out_path}")
        return 0

    # Wide pivot
    val_col, val_func = aggs[0]
    pivot_col = args.pivot_on
    table: Dict[Tuple[str, ...], Dict[str, Accum]] = {}
    pivot_values: List[str] = []
    pivot_seen: set = set()
    with open_table(in_path) as (_kind, _hdr, reader):
        for row in reader:
            row_key = tuple(row.get(c, "") for c in group_cols)
            col_key = row.get(pivot_col, "")
            if col_key not in pivot_seen:
                pivot_seen.add(col_key)
                pivot_values.append(col_key)
            bucket = table.get(row_key)
            if bucket is None:
                bucket = {}
                table[row_key] = bucket
            acc = bucket.get(col_key)
            if acc is None:
                acc = Accum()
                bucket[col_key] = acc
            acc.push(row.get(val_col, ""))

    if not table:
        print("Warning: input produced no groups", file=sys.stderr)
        if args.as_json:
            print(json.dumps({"output": str(out_path), "groups": 0, "wide": True}, indent=2))
        return 1

    header_out = list(group_cols) + pivot_values
    rows_out = []
    for row_key, bucket in table.items():
        r = {}
        for i, c in enumerate(group_cols):
            r[c] = row_key[i]
        for pv in pivot_values:
            acc = bucket.get(pv)
            r[pv] = str(acc.value(val_func)) if acc is not None else args.fill
        rows_out.append(r)

    sort_cols = parse_cols(args.sort_by) if args.sort_by else group_cols
    try:
        rows_out.sort(key=lambda r: _sort_key(r, sort_cols), reverse=args.desc)
    except TypeError:
        pass

    write_table(out_path, header_out, rows_out)

    summary = {"output": str(out_path), "rows": len(rows_out),
               "wide": True, "group_by": group_cols, "pivot_on": pivot_col,
               "value": val_col, "func": val_func,
               "pivot_values": pivot_values}
    if args.as_json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"Wide pivot: {len(rows_out)} rows x {len(pivot_values)} columns -> {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

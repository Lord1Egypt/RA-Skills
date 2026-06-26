#!/usr/bin/env python3
"""Lightweight CSV analyzer using only Python stdlib."""

import argparse
import csv
import math
import sys
from collections import defaultdict


def load_csv(path):
    """Load CSV and return headers + rows."""
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)
    return [h.strip() for h in headers], rows


def is_numeric(val):
    try:
        float(val)
        return True
    except (ValueError, TypeError):
        return False


def col_index(headers, name):
    name_lower = name.strip().lower()
    for i, h in enumerate(headers):
        if h.lower() == name_lower:
            return i
    raise ValueError(f"Column '{name}' not found. Available: {headers}")


def numeric_values(rows, idx):
    return [float(r[idx]) for r in rows if idx < len(r) and is_numeric(r[idx])]


def mean(vals):
    return sum(vals) / len(vals) if vals else 0


def median(vals):
    s = sorted(vals)
    n = len(s)
    if n == 0: return 0
    if n % 2 == 1: return s[n // 2]
    return (s[n // 2 - 1] + s[n // 2]) / 2


def stdev(vals):
    if len(vals) < 2: return 0
    m = mean(vals)
    return math.sqrt(sum((x - m) ** 2 for x in vals) / (len(vals) - 1))


def cmd_stats(args):
    headers, rows = load_csv(args.file)
    print(f"File: {args.file}")
    print(f"Rows: {len(rows)}")
    print(f"Columns: {len(headers)}\n")

    for i, h in enumerate(headers):
        vals = [r[i] for r in rows if i < len(r) and r[i].strip()]
        nums = numeric_values(rows, i)
        uniq = len(set(v for v in vals))

        if len(nums) > len(vals) * 0.5 and nums:
            print(f"  {h} (numeric): min={min(nums):.2f} max={max(nums):.2f} "
                  f"mean={mean(nums):.2f} median={median(nums):.2f} "
                  f"stdev={stdev(nums):.2f} non-null={len(vals)}")
        else:
            top3 = sorted(set(vals), key=lambda v: -sum(1 for x in vals if x == v))[:3]
            print(f"  {h} (text): unique={uniq} non-null={len(vals)} "
                  f"top=[{', '.join(top3)}]")


def cmd_filter(args):
    headers, rows = load_csv(args.file)
    # Parse --where "column>value"
    import re
    m = re.match(r"(\w+)\s*(>=|<=|!=|>|<|==|=)\s*(.+)", args.where)
    if not m:
        print(f"Error: Cannot parse filter: {args.where}")
        sys.exit(1)

    col_name, op, val = m.group(1), m.group(2), m.group(3).strip()
    idx = col_index(headers, col_name)
    if op == "=": op = "=="

    def matches(row_val):
        if is_numeric(row_val) and is_numeric(val):
            a, b = float(row_val), float(val)
            return eval(f"a {op} b")
        else:
            if op == "==": return row_val.strip() == val
            if op == "!=": return row_val.strip() != val
            return False

    filtered = [r for r in rows if idx < len(r) and matches(r[idx])]
    print(f"Filtered: {len(filtered)}/{len(rows)} rows match '{args.where}'")

    if args.output:
        with open(args.output, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(headers)
            w.writerows(filtered)
        print(f"Saved to {args.output}")
    else:
        # Print first 20
        for r in filtered[:20]:
            print("  " + " | ".join(r[:6]))
        if len(filtered) > 20:
            print(f"  ... ({len(filtered) - 20} more rows)")


def cmd_top(args):
    headers, rows = load_csv(args.file)
    idx = col_index(headers, args.column)
    valid = [(r, float(r[idx])) for r in rows if idx < len(r) and is_numeric(r[idx])]
    valid.sort(key=lambda x: x[1], reverse=True)

    print(f"Top {args.n} by {args.column}:")
    for r, v in valid[:args.n]:
        print(f"  {v:>12.2f} | " + " | ".join(r[:5]))


def cmd_bottom(args):
    headers, rows = load_csv(args.file)
    idx = col_index(headers, args.column)
    valid = [(r, float(r[idx])) for r in rows if idx < len(r) and is_numeric(r[idx])]
    valid.sort(key=lambda x: x[1])

    print(f"Bottom {args.n} by {args.column}:")
    for r, v in valid[:args.n]:
        print(f"  {v:>12.2f} | " + " | ".join(r[:5]))


def cmd_anomalies(args):
    headers, rows = load_csv(args.file)
    idx = col_index(headers, args.column)
    nums = numeric_values(rows, idx)
    if len(nums) < 3:
        print("Not enough data for anomaly detection")
        return

    m = mean(nums)
    s = stdev(nums)
    threshold = args.sigma

    print(f"Anomalies in {args.column} (>{threshold}σ from mean {m:.2f}, stdev {s:.2f}):")
    count = 0
    for r in rows:
        if idx < len(r) and is_numeric(r[idx]):
            v = float(r[idx])
            z = abs(v - m) / s if s > 0 else 0
            if z > threshold:
                count += 1
                print(f"  z={z:.1f} value={v:.2f} | " + " | ".join(r[:5]))
    print(f"\n{count} anomalies found out of {len(nums)} values")


def cmd_group(args):
    headers, rows = load_csv(args.file)
    by_idx = col_index(headers, args.by)

    groups = defaultdict(list)
    for r in rows:
        if by_idx < len(r):
            groups[r[by_idx]].append(r)

    agg_specs = []
    for a in (args.agg or ["count:*"]):
        func, col = a.split(":", 1)
        agg_specs.append((func, col))

    print(f"Grouped by {args.by} ({len(groups)} groups):")
    for key in sorted(groups.keys()):
        grp = groups[key]
        parts = [f"{key} ({len(grp)} rows)"]
        for func, col in agg_specs:
            if col == "*" and func == "count":
                parts.append(f"count={len(grp)}")
            else:
                cidx = col_index(headers, col)
                vals = [float(r[cidx]) for r in grp if cidx < len(r) and is_numeric(r[cidx])]
                if func == "sum":
                    parts.append(f"sum({col})={sum(vals):,.2f}")
                elif func == "mean":
                    parts.append(f"mean({col})={mean(vals):,.2f}")
                elif func == "count":
                    parts.append(f"count({col})={len(vals)}")
                elif func == "min":
                    parts.append(f"min({col})={min(vals):,.2f}" if vals else f"min({col})=N/A")
                elif func == "max":
                    parts.append(f"max({col})={max(vals):,.2f}" if vals else f"max({col})=N/A")
        print("  " + " | ".join(parts))


def main():
    parser = argparse.ArgumentParser(description="CSV Analyzer")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("stats"); p.add_argument("file")
    p = sub.add_parser("filter"); p.add_argument("file"); p.add_argument("--where", required=True); p.add_argument("--output")
    p = sub.add_parser("top"); p.add_argument("file"); p.add_argument("--column", required=True); p.add_argument("--n", type=int, default=10)
    p = sub.add_parser("bottom"); p.add_argument("file"); p.add_argument("--column", required=True); p.add_argument("--n", type=int, default=10)
    p = sub.add_parser("anomalies"); p.add_argument("file"); p.add_argument("--column", required=True); p.add_argument("--sigma", type=float, default=2.0)
    p = sub.add_parser("group"); p.add_argument("file"); p.add_argument("--by", required=True); p.add_argument("--agg", nargs="+")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmds = {"stats": cmd_stats, "filter": cmd_filter, "top": cmd_top, "bottom": cmd_bottom, "anomalies": cmd_anomalies, "group": cmd_group}
    cmds[args.command](args)


if __name__ == "__main__":
    main()

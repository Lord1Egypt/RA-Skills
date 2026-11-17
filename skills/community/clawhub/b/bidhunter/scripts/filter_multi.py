#!/usr/bin/env python3
"""
filter_multi.py - Multi-dimension filtering for bid qualifications (BidHunter v1.5, A4).

Post-filters qualification output (qual_*.jsonl) by budget range, region, and
industry. Reads from stdin or a file, writes filtered JSONL to stdout.

Usage:
  python3 filter_multi.py <qual_file.jsonl> [--min 1000000] [--max 50000000] \
        [--region 天津] [--industry 能源] [--verdict investable,needs_review]

Budget is compared in CNY (parsed from title by qual_check). Region matches if
the region string appears in title or region_info. Industry matches if the
industry category string contains the given keyword.
"""
import json
import sys
import os
import argparse


def load(path):
    items = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return items


def matches(it, args):
    # verdict filter
    if args.verdict:
        wanted = set(args.verdict.split(","))
        if it.get("verdict") not in wanted:
            return False
    # budget
    if args.min is not None or args.max is not None:
        b = it.get("budget")
        if b is None:
            return False
        if args.min is not None and b < args.min:
            return False
        if args.max is not None and b > args.max:
            return False
    # region
    if args.region:
        regions = args.region.split(",")
        title = it.get("title", "")
        ri = it.get("region_info", {}) or {}
        hit = any(r in title or r in (ri.get("region", "") or "") for r in regions)
        if not hit:
            return False
    # industry
    if args.industry:
        inds = args.industry.split(",")
        ind = it.get("industry", "") or ""
        if not any(i in ind for i in inds):
            return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("qual_file")
    ap.add_argument("--min", type=int, default=None, help="最低预算(元)")
    ap.add_argument("--max", type=int, default=None, help="最高预算(元)")
    ap.add_argument("--region", default=None, help="地区关键词,逗号分隔")
    ap.add_argument("--industry", default=None, help="行业类目关键词,逗号分隔")
    ap.add_argument("--verdict", default=None, help="保留的判定,逗号分隔")
    ap.add_argument("--out", default=None, help="输出文件(默认stdout)")
    args = ap.parse_args()

    items = load(args.qual_file)
    kept = [it for it in items if matches(it, args)]

    out = args.out or sys.stdout
    if args.out:
        f = open(args.out, "w", encoding="utf-8")
    else:
        f = sys.stdout
    for it in kept:
        f.write(json.dumps(it, ensure_ascii=False) + "\n")
    if args.out:
        f.close()

    total = len(items)
    print(f"# filter: kept {len(kept)}/{total}", file=sys.stderr)


if __name__ == "__main__":
    main()

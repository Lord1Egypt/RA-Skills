#!/usr/bin/env python3
"""CSV Tool Pro - Swiss army knife for CSV files. Zero external dependencies."""

import csv
import json
import sys
import os
import re
import argparse
import statistics
from collections import Counter, defaultdict
from io import StringIO

def detect_delimiter(filepath):
    """Auto-detect CSV delimiter."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            sample = f.read(4096)
    except:
        with open(filepath, 'r', encoding='gbk', errors='replace') as f:
            sample = f.read(4096)
    sniffer = csv.Sniffer()
    try:
        dialect = sniffer.sniff(sample, delimiters=',\t;|')
        return dialect.delimiter
    except csv.Error:
        return ','

def read_csv(filepath, delimiter=None):
    """Read CSV file, return (headers, rows)."""
    if delimiter is None:
        delimiter = detect_delimiter(filepath)
    encodings = ['utf-8-sig', 'utf-8', 'gbk', 'latin-1']
    for enc in encodings:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                reader = csv.reader(f, delimiter=delimiter)
                rows = list(reader)
            if rows:
                headers = rows[0]
                data = rows[1:]
                return headers, data, enc
        except (UnicodeDecodeError, csv.Error):
            continue
    raise ValueError(f"Cannot read {filepath} with any supported encoding")

def write_csv(filepath, headers, rows, delimiter=','):
    """Write CSV file."""
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerow(headers)
        writer.writerows(rows)

def cmd_view(args):
    headers, rows, _ = read_csv(args.file)
    n = args.rows or len(rows)
    rows = rows[:n]
    # Calculate column widths
    cols = [str(h) for h in headers]
    widths = [len(c) for c in cols]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(widths):
                widths[i] = max(widths[i], min(len(str(cell)), 50))
    # Print table
    def fmt_row(cells):
        parts = []
        for i, c in enumerate(cells):
            s = str(c)[:50] if i < len(widths) else str(c)[:50]
            parts.append(s.ljust(widths[i] if i < len(widths) else 10))
        return ' | '.join(parts)
    sep = '-+-'.join('-' * w for w in widths)
    print(fmt_row(headers))
    print(sep)
    for row in rows:
        print(fmt_row(row))
    print(f"\n{len(rows)} rows x {len(headers)} columns")

def cmd_filter(args):
    headers, rows, _ = read_csv(args.file)
    col_idx = None
    for i, h in enumerate(headers):
        if h.lower() == args.column.lower():
            col_idx = i
            break
    if col_idx is None:
        print(f"Column '{args.column}' not found. Available: {', '.join(headers)}")
        return
    filtered = []
    for row in rows:
        if col_idx >= len(row):
            continue
        val = row[col_idx]
        if args.regex:
            if re.search(args.value, str(val)):
                filtered.append(row)
        elif args.numeric:
            try:
                if float(val) > float(args.value):
                    filtered.append(row)
            except (ValueError, TypeError):
                pass
        else:
            if str(val).lower() == args.value.lower():
                filtered.append(row)
    write_csv(args.output or 'filtered.csv', headers, filtered)
    print(f"Filtered {len(filtered)}/{len(rows)} rows → {args.output or 'filtered.csv'}")

def cmd_sort(args):
    headers, rows, _ = read_csv(args.file)
    col_idx = None
    for i, h in enumerate(headers):
        if h.lower() == args.column.lower():
            col_idx = i
            break
    if col_idx is None:
        print(f"Column '{args.column}' not found")
        return
    reverse = args.order == 'desc'
    try:
        rows.sort(key=lambda r: float(r[col_idx]) if col_idx < len(r) else 0, reverse=reverse)
    except (ValueError, TypeError):
        rows.sort(key=lambda r: r[col_idx] if col_idx < len(r) else '', reverse=reverse)
    write_csv(args.output or args.file, headers, rows)
    print(f"Sorted by {args.column} ({args.order}) → {args.output or args.file}")

def cmd_dedupe(args):
    headers, rows, _ = read_csv(args.file)
    col_idx = None
    for i, h in enumerate(headers):
        if h.lower() == args.column.lower():
            col_idx = i
            break
    if col_idx is None:
        print(f"Column '{args.column}' not found")
        return
    seen = set()
    unique = []
    for row in rows:
        key = row[col_idx] if col_idx < len(row) else ''
        if key not in seen:
            seen.add(key)
            unique.append(row)
    write_csv(args.output or 'deduped.csv', headers, unique)
    print(f"Deduplicated: {len(rows)} → {len(unique)} rows → {args.output or 'deduped.csv'}")

def cmd_merge(args):
    all_headers = []
    all_rows = []
    for f in args.files:
        headers, rows, _ = read_csv(f)
        if not all_headers:
            all_headers = headers
        all_rows.extend(rows)
    write_csv(args.output or 'merged.csv', all_headers, all_rows)
    print(f"Merged {len(args.files)} files → {len(all_rows)} rows → {args.output or 'merged.csv'}")

def cmd_to_json(args):
    headers, rows, _ = read_csv(args.file)
    result = []
    for row in rows:
        obj = {}
        for i, h in enumerate(headers):
            obj[h] = row[i] if i < len(row) else ''
        result.append(obj)
    out = args.output or args.file.rsplit('.', 1)[0] + '.json'
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Converted {len(result)} rows → {out}")

def cmd_to_yaml(args):
    headers, rows, _ = read_csv(args.file)
    lines = []
    for row in rows:
        lines.append('-')
        for i, h in enumerate(headers):
            val = row[i] if i < len(row) else ''
            lines.append(f'  {h}: "{val}"')
    out = args.output or args.file.rsplit('.', 1)[0] + '.yaml'
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    print(f"Converted {len(rows)} rows → {out}")

def cmd_to_markdown(args):
    headers, rows, _ = read_csv(args.file)
    lines = ['| ' + ' | '.join(str(h) for h in headers) + ' |']
    lines.append('| ' + ' | '.join('---' for _ in headers) + ' |')
    for row in rows:
        lines.append('| ' + ' | '.join(str(c) for c in row) + ' |')
    out = args.output or args.file.rsplit('.', 1)[0] + '.md'
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    print(f"Converted {len(rows)} rows → {out}")

def cmd_stats(args):
    headers, rows, _ = read_csv(args.file)
    for i, h in enumerate(headers):
        values = []
        for row in rows:
            if i < len(row):
                try:
                    values.append(float(row[i]))
                except (ValueError, TypeError):
                    pass
        if values:
            print(f"\n📊 {h}")
            print(f"   Count:  {len(values)}")
            print(f"   Mean:   {statistics.mean(values):.2f}")
            print(f"   Median: {statistics.median(values):.2f}")
            print(f"   Min:    {min(values):.2f}")
            print(f"   Max:    {max(values):.2f}")
            if len(values) > 1:
                print(f"   StdDev: {statistics.stdev(values):.2f}")

def cmd_frequency(args):
    headers, rows, _ = read_csv(args.file)
    col_idx = None
    for i, h in enumerate(headers):
        if h.lower() == args.column.lower():
            col_idx = i
            break
    if col_idx is None:
        print(f"Column '{args.column}' not found")
        return
    counter = Counter(row[col_idx] for row in rows if col_idx < len(row))
    print(f"\n📊 Frequency: {args.column}")
    for val, cnt in counter.most_common(20):
        pct = cnt / len(rows) * 100
        bar = '█' * int(pct / 2)
        print(f"   {str(val)[:30]:30s} {cnt:6d} ({pct:5.1f}%) {bar}")

def cmd_pivot(args):
    headers, rows, _ = read_csv(args.file)
    row_col = row_val = col_col = col_val = val_col = None
    for i, h in enumerate(headers):
        hl = h.lower()
        if hl == args.row_column.lower(): row_col = i
        if hl == args.col_column.lower(): col_col = i
        if hl == args.val_column.lower(): val_col = i
    if None in (row_col, col_col, val_col):
        print("One or more columns not found")
        return
    pivot = defaultdict(lambda: defaultdict(float))
    row_keys = set()
    col_keys = set()
    for row in rows:
        rk = row[row_col] if row_col < len(row) else ''
        ck = row[col_col] if col_col < len(row) else ''
        try:
            v = float(row[val_col]) if val_col < len(row) else 0
        except (ValueError, TypeError):
            v = 0
        pivot[rk][ck] += v
        row_keys.add(rk)
        col_keys.add(ck)
    # Print pivot table
    col_keys = sorted(col_keys)
    print(f"\n📊 Pivot: {args.row_column} × {args.col_column} → sum({args.val_column})")
    print(f"{'':20s}", end='')
    for ck in col_keys:
        print(f"{ck:>12s}", end='')
    print(f"{'TOTAL':>12s}")
    for rk in sorted(row_keys):
        total = 0
        print(f"{rk:20s}", end='')
        for ck in col_keys:
            v = pivot[rk].get(ck, 0)
            total += v
            print(f"{v:12.2f}", end='')
        print(f"{total:12.2f}")

def main():
    parser = argparse.ArgumentParser(description='CSV Tool Pro')
    sub = parser.add_subparsers(dest='command')
    
    p = sub.add_parser('view', help='View CSV file')
    p.add_argument('file'); p.add_argument('-n', '--rows', type=int)
    
    p = sub.add_parser('filter', help='Filter rows')
    p.add_argument('file'); p.add_argument('-c', '--column', required=True)
    p.add_argument('-v', '--value', required=True)
    p.add_argument('-r', '--regex', action='store_true')
    p.add_argument('--numeric', action='store_true')
    p.add_argument('-o', '--output')
    
    p = sub.add_parser('sort', help='Sort by column')
    p.add_argument('file'); p.add_argument('-c', '--column', required=True)
    p.add_argument('-o', '--order', choices=['asc', 'desc'], default='asc')
    p.add_argument('--output')
    
    p = sub.add_parser('dedupe', help='Remove duplicates')
    p.add_argument('file'); p.add_argument('-c', '--column', required=True)
    p.add_argument('-o', '--output')
    
    p = sub.add_parser('merge', help='Merge CSVs')
    p.add_argument('files', nargs='+'); p.add_argument('-o', '--output')
    
    p = sub.add_parser('to-json', help='Convert to JSON')
    p.add_argument('file'); p.add_argument('-o', '--output')
    
    p = sub.add_parser('to-yaml', help='Convert to YAML')
    p.add_argument('file'); p.add_argument('-o', '--output')
    
    p = sub.add_parser('to-markdown', help='Convert to Markdown')
    p.add_argument('file'); p.add_argument('-o', '--output')
    
    p = sub.add_parser('stats', help='Column statistics')
    p.add_argument('file')
    
    p = sub.add_parser('frequency', help='Value frequency')
    p.add_argument('file'); p.add_argument('-c', '--column', required=True)
    
    p = sub.add_parser('pivot', help='Pivot table')
    p.add_argument('file')
    p.add_argument('--row-column', required=True)
    p.add_argument('--col-column', required=True)
    p.add_argument('--val-column', required=True)
    
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return
    
    cmds = {
        'view': cmd_view, 'filter': cmd_filter, 'sort': cmd_sort,
        'dedupe': cmd_dedupe, 'merge': cmd_merge, 'to-json': cmd_to_json,
        'to-yaml': cmd_to_yaml, 'to-markdown': cmd_to_markdown,
        'stats': cmd_stats, 'frequency': cmd_frequency, 'pivot': cmd_pivot,
    }
    cmds[args.command](args)

if __name__ == '__main__':
    main()

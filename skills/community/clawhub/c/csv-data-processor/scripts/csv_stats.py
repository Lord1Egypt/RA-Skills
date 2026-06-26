#!/usr/bin/env python3
"""Compute statistics from CSV data: numeric stats, value counts, row counts."""

import argparse, csv, json, sys
from collections import Counter

def main():
    p = argparse.ArgumentParser(description='Compute CSV statistics')
    p.add_argument('file', help='CSV file path')
    p.add_argument('--delimiter', default=',')
    p.add_argument('--encoding', default='utf-8')
    p.add_argument('--numeric', help='Comma-separated column names for numeric stats')
    p.add_argument('--counts', help='Column name for value frequency counts')
    p.add_argument('--json', action='store_true', help='JSON output')
    args = p.parse_args()

    with open(args.file, 'r', encoding=args.encoding) as f:
        reader = csv.DictReader(f, delimiter=args.delimiter)
        data = list(reader)

    if not data:
        print("(no data)")
        return

    result = {
        'file': args.file,
        'rows': len(data),
        'columns': len(reader.fieldnames),
        'column_names': reader.fieldnames,
    }

    output_lines = []
    output_lines.append(f"File: {args.file}")
    output_lines.append(f"Rows: {len(data)}  |  Columns: {len(reader.fieldnames)}")
    output_lines.append(f"Columns: {', '.join(reader.fieldnames)}")
    output_lines.append("")

    # Numeric stats
    if args.numeric:
        cols = [c.strip() for c in args.numeric.split(',')]
        num_stats = {}
        output_lines.append("--- Numeric Statistics ---")
        for col in cols:
            vals = []
            for row in data:
                try:
                    vals.append(float(row.get(col, 0)))
                except (ValueError, TypeError):
                    pass
            if vals:
                n = len(vals)
                mn = min(vals)
                mx = max(vals)
                avg = sum(vals) / n
                sorted_vals = sorted(vals)
                median = sorted_vals[n // 2]
                num_stats[col] = {'min': mn, 'max': mx, 'avg': round(avg, 4), 'median': median, 'count': n}
                output_lines.append(f"\n{col}:")
                output_lines.append(f"  count: {n}")
                output_lines.append(f"  min: {mn}")
                output_lines.append(f"  max: {mx}")
                output_lines.append(f"  avg: {avg:.4f}")
                output_lines.append(f"  median: {median}")
        result['numeric_stats'] = num_stats

    # Value counts
    if args.counts:
        counter = Counter(row.get(args.counts, '') for row in data)
        output_lines.append(f"\n--- Value Counts: {args.counts} ---")
        cnt_sorted = counter.most_common()
        for val, count in cnt_sorted[:20]:
            pct = count / len(data) * 100
            bar = '█' * int(pct / 2)
            output_lines.append(f"  {str(val):20s} {count:>5d} ({pct:5.1f}%) {bar}")
        if len(cnt_sorted) > 20:
            output_lines.append(f"  ... {len(cnt_sorted) - 20} more values")
        result['value_counts'] = {col: count for col, count in cnt_sorted}

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print('\n'.join(output_lines))

if __name__ == '__main__':
    main()

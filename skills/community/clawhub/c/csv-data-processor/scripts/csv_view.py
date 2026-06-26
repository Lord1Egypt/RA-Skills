#!/usr/bin/env python3
"""View CSV data with head/tail, sampling, and column summaries."""

import argparse, csv, json, sys

def load_csv(path, delimiter, encoding, has_header):
    with open(path, 'r', encoding=encoding) as f:
        reader = csv.reader(f, delimiter=delimiter)
        rows = list(reader)
    if has_header and rows:
        header = rows[0]
        data = rows[1:]
    else:
        header = [f"col{i}" for i in range(len(rows[0]))] if rows else []
        data = rows
    return header, data

def stats(header, data):
    lines = ["--- Column Summary ---"]
    for i, col in enumerate(header):
        vals = [r[i] for r in data if i < len(r) and r[i].strip()]
        numeric = []
        for v in vals:
            try:
                numeric.append(float(v))
            except ValueError:
                pass
        lines.append(f"\n{col}:")
        lines.append(f"  non-null: {len(vals)}/{len(data)}")
        if numeric:
            lines.append(f"  numeric: {len(numeric)} values")
            lines.append(f"  min/avg/max: {min(numeric):.2f} / {sum(numeric)/len(numeric):.2f} / {max(numeric):.2f}")
        unique = set(vals)
        lines.append(f"  unique: {len(unique)}")
        if len(unique) <= 10 and unique:
            lines.append(f"  values: {', '.join(str(u) for u in unique)}")
    return '\n'.join(lines)

def format_table(header, data, max_rows=20):
    if not data:
        return "(no data)"
    widths = [len(c) for c in header]
    for row in data[:max_rows]:
        for i, v in enumerate(row):
            widths[i] = max(widths[i], len(str(v)))
    sep = '+' + '+'.join('-' * (w + 2) for w in widths) + '+'
    header_line = '| ' + ' | '.join(c.ljust(w) for c, w in zip(header, widths)) + ' |'
    lines = [sep, header_line, sep]
    for row in data[:max_rows]:
        r = [str(v) if i < len(row) else '' for i, v in enumerate(row)]
        lines.append('| ' + ' | '.join(str(v).ljust(w) for v, w in zip(r, widths)) + ' |')
    lines.append(sep)
    if len(data) > max_rows:
        lines.append(f"... {len(data) - max_rows} more rows ({len(data)} total)")
    else:
        lines.append(f"({len(data)} rows)")
    return '\n'.join(lines)

def main():
    p = argparse.ArgumentParser(description='View CSV data')
    p.add_argument('file', help='CSV file path')
    p.add_argument('--delimiter', default=',')
    p.add_argument('--encoding', default='utf-8')
    p.add_argument('--no-header', action='store_true', help='File has no header row')
    p.add_argument('--head', type=int, default=20, help='Rows to show')
    p.add_argument('--stats', action='store_true', help='Show column statistics')
    p.add_argument('--json', action='store_true', help='Output as JSON')
    args = p.parse_args()

    header, data = load_csv(args.file, args.delimiter, args.encoding, not args.no_header)

    if args.json:
        result = {
            'file': args.file,
            'columns': len(header),
            'rows': len(data),
            'headers': header,
            'sample': [dict(zip(header, r)) for r in data[:args.head]]
        }
        print(json.dumps(result, indent=2))
    else:
        print(f"File: {args.file}  |  {len(header)} columns x {len(data)} rows")
        print(format_table(header, data, args.head))
        if args.stats:
            print(stats(header, data))

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Parse CSV, TSV, or JSON data into normalized metrics format for report generation."""

import argparse
import csv
import json
import sys
import os
from io import StringIO


def detect_format(filepath):
    """Auto-detect file format from extension and content."""
    ext = os.path.splitext(filepath)[1].lower()
    if ext in ('.json',):
        return 'json'
    if ext in ('.csv',):
        return 'csv'
    if ext in ('.tsv',):
        return 'tsv'
    # Sniff content
    with open(filepath, 'r', encoding='utf-8') as f:
        sample = f.read(2048)
    try:
        json.loads(sample if len(sample) < 2048 else sample)
        return 'json'
    except (json.JSONDecodeError, ValueError):
        pass
    if '\t' in sample and sample.count('\t') > sample.count(','):
        return 'tsv'
    return 'csv'


def detect_metric_type(values):
    """Detect whether a column contains currency, percentages, counts, or rates."""
    sample = [str(v).strip() for v in values if v not in (None, '', 'N/A', '-')][:20]
    if not sample:
        return 'unknown'

    currency_count = sum(1 for v in sample if v.startswith('$') or v.startswith('€') or v.startswith('£'))
    pct_count = sum(1 for v in sample if v.endswith('%'))

    if currency_count > len(sample) * 0.5:
        return 'currency'
    if pct_count > len(sample) * 0.5:
        return 'percentage'

    # Try to parse as numbers
    numeric_count = 0
    has_decimal = False
    for v in sample:
        cleaned = v.replace(',', '').replace('$', '').replace('€', '').replace('£', '').replace('%', '')
        try:
            num = float(cleaned)
            numeric_count += 1
            if '.' in cleaned:
                has_decimal = True
        except ValueError:
            pass

    if numeric_count > len(sample) * 0.5:
        if has_decimal:
            return 'rate'
        return 'count'
    return 'text'


def parse_numeric(value):
    """Parse a string value into a number, stripping currency/percent symbols."""
    if value in (None, '', 'N/A', '-'):
        return None
    s = str(value).strip().replace(',', '').replace('$', '').replace('€', '').replace('£', '').replace('%', '')
    try:
        return float(s)
    except ValueError:
        return None


def compute_stats(values):
    """Compute basic statistics for a list of numeric values."""
    nums = [v for v in values if v is not None]
    if not nums:
        return {}
    total = sum(nums)
    avg = total / len(nums)
    return {
        'count': len(nums),
        'total': round(total, 2),
        'average': round(avg, 2),
        'min': round(min(nums), 2),
        'max': round(max(nums), 2),
    }


def parse_csv_data(filepath, delimiter=','):
    """Parse CSV/TSV file into structured data."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    reader = csv.DictReader(StringIO(content), delimiter=delimiter)
    rows = list(reader)

    if not rows:
        return {'error': 'No data rows found', 'headers': [], 'rows': []}

    headers = list(rows[0].keys())

    # Analyze each column
    columns = {}
    for header in headers:
        values = [row.get(header, '') for row in rows]
        metric_type = detect_metric_type(values)
        col_info = {
            'name': header,
            'type': metric_type,
            'sample_values': values[:5],
        }
        if metric_type in ('currency', 'percentage', 'count', 'rate'):
            numeric_values = [parse_numeric(v) for v in values]
            col_info['stats'] = compute_stats(numeric_values)
        columns[header] = col_info

    return {
        'format': 'csv',
        'row_count': len(rows),
        'headers': headers,
        'columns': columns,
        'rows': rows,
    }


def parse_json_data(filepath):
    """Parse JSON file into structured data."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Handle array of objects
    if isinstance(data, list) and data and isinstance(data[0], dict):
        headers = list(data[0].keys())
        columns = {}
        for header in headers:
            values = [row.get(header, '') for row in data]
            metric_type = detect_metric_type(values)
            col_info = {
                'name': header,
                'type': metric_type,
                'sample_values': values[:5],
            }
            if metric_type in ('currency', 'percentage', 'count', 'rate'):
                numeric_values = [parse_numeric(v) for v in values]
                col_info['stats'] = compute_stats(numeric_values)
            columns[header] = col_info

        return {
            'format': 'json_array',
            'row_count': len(data),
            'headers': headers,
            'columns': columns,
            'rows': data,
        }

    # Handle flat key-value object
    if isinstance(data, dict):
        metrics = {}
        for key, value in data.items():
            if isinstance(value, (int, float)):
                metrics[key] = {
                    'value': value,
                    'type': 'percentage' if 'rate' in key.lower() or 'pct' in key.lower() or 'percent' in key.lower() else 'count',
                }
            elif isinstance(value, str):
                parsed = parse_numeric(value)
                if parsed is not None:
                    metrics[key] = {'value': parsed, 'type': detect_metric_type([value])}
                else:
                    metrics[key] = {'value': value, 'type': 'text'}
            elif isinstance(value, list):
                metrics[key] = {'value': f'[{len(value)} items]', 'type': 'list', 'count': len(value)}
            elif isinstance(value, dict):
                metrics[key] = {'value': f'{{{len(value)} keys}}', 'type': 'object', 'keys': list(value.keys())}

        return {
            'format': 'json_object',
            'metrics': metrics,
        }

    return {'format': 'json_unknown', 'raw_type': type(data).__name__}


def main():
    parser = argparse.ArgumentParser(description='Parse data files into normalized metrics format')
    parser.add_argument('input', help='Input file path (CSV, TSV, or JSON)')
    parser.add_argument('--format', choices=['csv', 'tsv', 'json', 'auto'], default='auto',
                        help='Input format (default: auto-detect)')
    parser.add_argument('--output', '-o', help='Output file path (default: stdout)')
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(json.dumps({'error': f'File not found: {args.input}'}), file=sys.stderr)
        sys.exit(1)

    fmt = args.format if args.format != 'auto' else detect_format(args.input)

    if fmt == 'json':
        result = parse_json_data(args.input)
    elif fmt == 'tsv':
        result = parse_csv_data(args.input, delimiter='\t')
    else:
        result = parse_csv_data(args.input, delimiter=',')

    result['source_file'] = os.path.basename(args.input)
    output = json.dumps(result, indent=2, default=str)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f'Parsed data written to {args.output}')
    else:
        print(output)


if __name__ == '__main__':
    main()

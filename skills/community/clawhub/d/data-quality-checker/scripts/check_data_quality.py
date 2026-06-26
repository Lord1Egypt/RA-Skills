#!/usr/bin/env python3
"""
Data Quality Checker — Validate CSV/JSON data for quality issues.

Detects: missing values, duplicates, type inconsistencies, outliers,
format violations, schema drift, and common data entry errors.

No external dependencies — pure Python stdlib.
"""

import argparse
import csv
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean, median, stdev


def detect_file_type(path):
    ext = Path(path).suffix.lower()
    if ext == '.csv':
        return 'csv'
    elif ext in ('.json', '.jsonl', '.ndjson'):
        return 'json'
    elif ext in ('.tsv',):
        return 'tsv'
    return None


def load_csv(path, delimiter=','):
    rows = []
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        headers = reader.fieldnames or []
        for row in reader:
            rows.append(row)
    return headers, rows


def load_json(path):
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read().strip()

    # Try JSON array
    if content.startswith('['):
        data = json.loads(content)
        if data and isinstance(data[0], dict):
            headers = list(data[0].keys())
            return headers, data
        return [], data

    # Try JSONL/NDJSON
    rows = []
    headers_set = set()
    for line in content.split('\n'):
        line = line.strip()
        if line:
            obj = json.loads(line)
            if isinstance(obj, dict):
                headers_set.update(obj.keys())
                rows.append(obj)
    headers = sorted(headers_set)
    return headers, rows


def load_data(path):
    ftype = detect_file_type(path)
    if ftype == 'csv':
        return load_csv(path)
    elif ftype == 'tsv':
        return load_csv(path, delimiter='\t')
    elif ftype == 'json':
        return load_json(path)
    else:
        # Try CSV first, then JSON
        try:
            return load_csv(path)
        except Exception:
            return load_json(path)


# --- Checks ---

def check_missing_values(headers, rows):
    """Detect missing/empty values per column."""
    issues = []
    total = len(rows)
    if total == 0:
        return issues

    for col in headers:
        missing = 0
        for row in rows:
            val = row.get(col, '')
            if val is None or (isinstance(val, str) and val.strip() in ('', 'null', 'NULL', 'None', 'N/A', 'n/a', 'NA', '-')):
                missing += 1
        if missing > 0:
            pct = (missing / total) * 100
            severity = 'critical' if pct > 50 else 'warning' if pct > 10 else 'info'
            issues.append({
                'check': 'missing_values',
                'column': col,
                'severity': severity,
                'message': f'{missing}/{total} rows ({pct:.1f}%) have missing values',
                'count': missing,
            })
    return issues


def check_duplicates(headers, rows):
    """Detect duplicate rows."""
    issues = []
    if not rows:
        return issues

    # Full row duplicates
    seen = Counter()
    for row in rows:
        key = tuple(sorted((k, str(v)) for k, v in row.items()))
        seen[key] += 1

    dupes = sum(1 for c in seen.values() if c > 1)
    total_dupe_rows = sum(c - 1 for c in seen.values() if c > 1)
    if dupes > 0:
        issues.append({
            'check': 'duplicate_rows',
            'severity': 'warning',
            'message': f'{total_dupe_rows} duplicate rows found ({dupes} unique rows repeated)',
            'count': total_dupe_rows,
        })

    # Per-column uniqueness check (find potential ID columns)
    for col in headers:
        values = [str(row.get(col, '')) for row in rows if row.get(col)]
        if not values:
            continue
        unique = len(set(values))
        total = len(values)
        # If column looks like an ID (high cardinality) but has dupes
        if unique > total * 0.9 and unique < total:
            dupe_count = total - unique
            issues.append({
                'check': 'duplicate_values',
                'column': col,
                'severity': 'warning',
                'message': f'Potential ID column "{col}" has {dupe_count} duplicate values',
                'count': dupe_count,
            })

    return issues


def infer_type(value):
    """Infer the data type of a string value."""
    if value is None:
        return 'null'
    if not isinstance(value, str):
        if isinstance(value, bool):
            return 'boolean'
        if isinstance(value, int):
            return 'integer'
        if isinstance(value, float):
            return 'float'
        return type(value).__name__

    v = value.strip()
    if v in ('', 'null', 'NULL', 'None'):
        return 'null'
    if v.lower() in ('true', 'false', 'yes', 'no'):
        return 'boolean'
    try:
        int(v)
        return 'integer'
    except (ValueError, OverflowError):
        pass
    try:
        float(v)
        return 'float'
    except (ValueError, OverflowError):
        pass

    # Date patterns
    date_patterns = [
        r'^\d{4}-\d{2}-\d{2}$',
        r'^\d{2}/\d{2}/\d{4}$',
        r'^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}',
    ]
    for pat in date_patterns:
        if re.match(pat, v):
            return 'date'

    # Email
    if re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', v):
        return 'email'

    # URL
    if re.match(r'^https?://', v):
        return 'url'

    return 'string'


def check_type_consistency(headers, rows):
    """Check if columns have consistent data types."""
    issues = []
    if not rows:
        return issues

    for col in headers:
        type_counts = Counter()
        for row in rows:
            val = row.get(col)
            if val is None or (isinstance(val, str) and val.strip() in ('', 'null', 'NULL', 'None')):
                continue
            type_counts[infer_type(val)] += 1

        if len(type_counts) > 1:
            total = sum(type_counts.values())
            dominant_type = type_counts.most_common(1)[0]
            minority_types = [(t, c) for t, c in type_counts.items() if t != dominant_type[0]]
            minority_count = sum(c for _, c in minority_types)
            if minority_count > 0:
                pct = (minority_count / total) * 100
                severity = 'warning' if pct > 5 else 'info'
                type_breakdown = ', '.join(f'{t}: {c}' for t, c in type_counts.most_common())
                issues.append({
                    'check': 'type_inconsistency',
                    'column': col,
                    'severity': severity,
                    'message': f'Mixed types in "{col}": {type_breakdown} ({pct:.1f}% non-dominant)',
                    'count': minority_count,
                })

    return issues


def check_outliers(headers, rows):
    """Detect statistical outliers in numeric columns (IQR method)."""
    issues = []
    if len(rows) < 10:
        return issues

    for col in headers:
        nums = []
        for row in rows:
            val = row.get(col, '')
            try:
                nums.append(float(val))
            except (ValueError, TypeError):
                pass

        if len(nums) < 10:
            continue

        nums_sorted = sorted(nums)
        q1_idx = len(nums_sorted) // 4
        q3_idx = (3 * len(nums_sorted)) // 4
        q1 = nums_sorted[q1_idx]
        q3 = nums_sorted[q3_idx]
        iqr = q3 - q1

        if iqr == 0:
            continue

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outliers = [n for n in nums if n < lower or n > upper]

        if outliers:
            pct = (len(outliers) / len(nums)) * 100
            severity = 'warning' if pct > 5 else 'info'
            issues.append({
                'check': 'outliers',
                'column': col,
                'severity': severity,
                'message': f'{len(outliers)} outliers ({pct:.1f}%) in "{col}" (range: {min(nums):.2f}-{max(nums):.2f}, IQR bounds: {lower:.2f}-{upper:.2f})',
                'count': len(outliers),
            })

    return issues


def check_format_patterns(headers, rows):
    """Detect format inconsistencies (emails, phones, dates, etc.)."""
    issues = []
    if not rows:
        return issues

    patterns = {
        'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        'phone': r'^[\+]?[\d\s\-\(\)]{7,15}$',
        'url': r'^https?://[^\s]+$',
        'uuid': r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
        'date_iso': r'^\d{4}-\d{2}-\d{2}',
        'date_us': r'^\d{2}/\d{2}/\d{4}$',
    }

    for col in headers:
        values = [str(row.get(col, '')).strip() for row in rows if row.get(col)]
        if len(values) < 5:
            continue

        # Check if column matches a known pattern
        for pname, pat in patterns.items():
            matches = sum(1 for v in values if re.match(pat, v, re.IGNORECASE))
            if matches > len(values) * 0.5 and matches < len(values):
                # Mostly matches but some don't
                violations = len(values) - matches
                issues.append({
                    'check': 'format_violation',
                    'column': col,
                    'severity': 'warning',
                    'message': f'{violations} values in "{col}" don\'t match {pname} format ({matches}/{len(values)} match)',
                    'count': violations,
                })

    return issues


def check_whitespace(headers, rows):
    """Detect leading/trailing whitespace and inconsistent casing."""
    issues = []
    if not rows:
        return issues

    for col in headers:
        ws_count = 0
        for row in rows:
            val = row.get(col, '')
            if isinstance(val, str) and val != val.strip():
                ws_count += 1

        if ws_count > 0:
            issues.append({
                'check': 'whitespace',
                'column': col,
                'severity': 'info',
                'message': f'{ws_count} values in "{col}" have leading/trailing whitespace',
                'count': ws_count,
            })

    return issues


def check_empty_columns(headers, rows):
    """Detect columns that are entirely empty."""
    issues = []
    if not rows:
        return issues

    for col in headers:
        non_empty = sum(1 for row in rows if row.get(col) and str(row.get(col, '')).strip())
        if non_empty == 0:
            issues.append({
                'check': 'empty_column',
                'column': col,
                'severity': 'warning',
                'message': f'Column "{col}" is entirely empty',
                'count': len(rows),
            })

    return issues


def check_schema_drift(headers, rows):
    """Detect rows with extra or missing keys (JSON data)."""
    issues = []
    if not rows:
        return issues

    expected = set(headers)
    extra_keys = Counter()
    missing_keys = Counter()

    for row in rows:
        row_keys = set(row.keys())
        for k in row_keys - expected:
            extra_keys[k] += 1
        for k in expected - row_keys:
            missing_keys[k] += 1

    for k, count in extra_keys.items():
        issues.append({
            'check': 'schema_drift',
            'column': k,
            'severity': 'warning',
            'message': f'Unexpected key "{k}" found in {count} rows',
            'count': count,
        })

    for k, count in missing_keys.items():
        if count < len(rows):
            issues.append({
                'check': 'schema_drift',
                'column': k,
                'severity': 'info',
                'message': f'Key "{k}" missing from {count} rows',
                'count': count,
            })

    return issues


def compute_quality_score(issues, total_rows, total_cols):
    """Compute overall quality score 0-100."""
    if total_rows == 0:
        return 0

    total_cells = total_rows * total_cols
    if total_cells == 0:
        return 100

    # Weight by severity
    deductions = 0
    for issue in issues:
        count = issue.get('count', 0)
        sev = issue.get('severity', 'info')
        weight = {'critical': 3, 'warning': 1.5, 'info': 0.5}.get(sev, 1)
        deductions += (count / total_cells) * weight * 20

    score = max(0, min(100, 100 - deductions))
    return round(score, 1)


def format_terminal(report):
    """Format report for terminal output."""
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"  DATA QUALITY REPORT")
    lines.append(f"{'='*60}")
    lines.append(f"  File:    {report['file']}")
    lines.append(f"  Rows:    {report['rows']:,}")
    lines.append(f"  Columns: {report['columns']}")
    lines.append(f"  Score:   {report['quality_score']}/100")
    lines.append(f"{'='*60}\n")

    # Group by severity
    for sev in ['critical', 'warning', 'info']:
        sev_issues = [i for i in report['issues'] if i['severity'] == sev]
        if sev_issues:
            icon = {'critical': '!!!', 'warning': '(!)', 'info': '(i)'}[sev]
            lines.append(f"  {icon} {sev.upper()} ({len(sev_issues)})")
            lines.append(f"  {'-'*40}")
            for issue in sev_issues:
                col = f' [{issue["column"]}]' if 'column' in issue else ''
                lines.append(f"    {issue['check']}{col}: {issue['message']}")
            lines.append('')

    if not report['issues']:
        lines.append("  No issues found! Data looks clean.")

    lines.append(f"{'='*60}")
    return '\n'.join(lines)


def format_markdown(report):
    """Format report as markdown."""
    lines = []
    lines.append(f"# Data Quality Report\n")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| File | `{report['file']}` |")
    lines.append(f"| Rows | {report['rows']:,} |")
    lines.append(f"| Columns | {report['columns']} |")
    lines.append(f"| Quality Score | **{report['quality_score']}/100** |")
    lines.append(f"| Issues Found | {len(report['issues'])} |")
    lines.append('')

    for sev in ['critical', 'warning', 'info']:
        sev_issues = [i for i in report['issues'] if i['severity'] == sev]
        if sev_issues:
            icon = {'critical': '🔴', 'warning': '🟡', 'info': '🔵'}[sev]
            lines.append(f"## {icon} {sev.capitalize()} Issues\n")
            for issue in sev_issues:
                col = f' `{issue["column"]}`' if 'column' in issue else ''
                lines.append(f"- **{issue['check']}**{col}: {issue['message']}")
            lines.append('')

    if not report['issues']:
        lines.append("No issues found! Data looks clean.")

    return '\n'.join(lines)


def format_json_output(report):
    """Format as JSON."""
    return json.dumps(report, indent=2)


def validate_against_schema(headers, rows, schema_path):
    """Validate data against a JSON schema file."""
    issues = []
    with open(schema_path, 'r') as f:
        schema = json.load(f)

    required = schema.get('required', [])
    properties = schema.get('properties', {})

    for col in required:
        if col not in headers:
            issues.append({
                'check': 'schema_required',
                'column': col,
                'severity': 'critical',
                'message': f'Required column "{col}" is missing from data',
                'count': len(rows),
            })

    for col, rules in properties.items():
        if col not in headers:
            continue

        expected_type = rules.get('type')
        min_val = rules.get('minimum')
        max_val = rules.get('maximum')
        pattern = rules.get('pattern')
        enum_vals = rules.get('enum')
        min_length = rules.get('minLength')
        max_length = rules.get('maxLength')

        violations = 0
        for row in rows:
            val = row.get(col, '')
            if val is None or (isinstance(val, str) and not val.strip()):
                continue

            # Type check
            if expected_type:
                actual = infer_type(val)
                if expected_type == 'number' and actual not in ('integer', 'float'):
                    violations += 1
                    continue
                elif expected_type == 'integer' and actual != 'integer':
                    violations += 1
                    continue
                elif expected_type == 'string' and actual not in ('string', 'email', 'url', 'date'):
                    violations += 1
                    continue

            # Range
            if min_val is not None or max_val is not None:
                try:
                    num = float(val)
                    if min_val is not None and num < min_val:
                        violations += 1
                    if max_val is not None and num > max_val:
                        violations += 1
                except (ValueError, TypeError):
                    pass

            # Pattern
            if pattern:
                if not re.match(pattern, str(val)):
                    violations += 1

            # Enum
            if enum_vals:
                if str(val) not in [str(e) for e in enum_vals]:
                    violations += 1

            # Length
            sv = str(val)
            if min_length is not None and len(sv) < min_length:
                violations += 1
            if max_length is not None and len(sv) > max_length:
                violations += 1

        if violations > 0:
            issues.append({
                'check': 'schema_violation',
                'column': col,
                'severity': 'warning',
                'message': f'{violations} values in "{col}" violate schema rules',
                'count': violations,
            })

    return issues


def generate_schema(headers, rows, output_path=None):
    """Auto-generate a JSON schema from data."""
    schema = {
        'type': 'object',
        'properties': {},
        'required': [],
    }

    for col in headers:
        types = Counter()
        values = []
        for row in rows:
            val = row.get(col)
            if val is not None and str(val).strip():
                t = infer_type(val)
                types[t] += 1
                values.append(val)

        if not types:
            schema['properties'][col] = {'type': 'string'}
            continue

        dominant = types.most_common(1)[0][0]
        type_map = {
            'integer': 'integer',
            'float': 'number',
            'boolean': 'boolean',
            'email': 'string',
            'url': 'string',
            'date': 'string',
            'string': 'string',
        }
        json_type = type_map.get(dominant, 'string')

        prop = {'type': json_type}

        # Add format for special types
        if dominant == 'email':
            prop['format'] = 'email'
        elif dominant == 'url':
            prop['format'] = 'uri'
        elif dominant == 'date':
            prop['format'] = 'date-time'

        # Add numeric range
        if json_type in ('integer', 'number'):
            nums = []
            for v in values:
                try:
                    nums.append(float(v))
                except (ValueError, TypeError):
                    pass
            if nums:
                prop['minimum'] = min(nums)
                prop['maximum'] = max(nums)

        # Add string length
        if json_type == 'string' and dominant == 'string':
            lengths = [len(str(v)) for v in values]
            if lengths:
                prop['minLength'] = min(lengths)
                prop['maxLength'] = max(lengths)

        # Check if all non-empty
        missing = len(rows) - len(values)
        if missing == 0:
            schema['required'].append(col)

        # Enum for low-cardinality columns
        unique = set(str(v) for v in values)
        if 2 <= len(unique) <= 20 and len(unique) < len(values) * 0.3:
            prop['enum'] = sorted(unique)

        schema['properties'][col] = prop

    result = json.dumps(schema, indent=2)
    if output_path:
        with open(output_path, 'w') as f:
            f.write(result)
        print(f"Schema written to {output_path}")
    else:
        print(result)

    return schema


def main():
    parser = argparse.ArgumentParser(
        description='Data Quality Checker — validate CSV/JSON data for quality issues'
    )
    parser.add_argument('file', help='Path to CSV, JSON, or JSONL file')
    parser.add_argument('--format', '-f', choices=['terminal', 'markdown', 'json'],
                        default='terminal', help='Output format (default: terminal)')
    parser.add_argument('--schema', '-s', help='JSON schema file to validate against')
    parser.add_argument('--generate-schema', '-g', nargs='?', const='-',
                        help='Generate schema from data (optional: output path)')
    parser.add_argument('--checks', '-c',
                        help='Comma-separated checks to run (default: all). '
                             'Options: missing,duplicates,types,outliers,formats,whitespace,empty,drift')
    parser.add_argument('--severity', choices=['info', 'warning', 'critical'],
                        help='Minimum severity to show')
    parser.add_argument('--output', '-o', help='Write report to file')

    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    try:
        headers, rows = load_data(args.file)
    except Exception as e:
        print(f"Error loading data: {e}", file=sys.stderr)
        sys.exit(1)

    if args.generate_schema is not None:
        out = args.generate_schema if args.generate_schema != '-' else None
        generate_schema(headers, rows, out)
        return

    # Select checks
    all_checks = {
        'missing': check_missing_values,
        'duplicates': check_duplicates,
        'types': check_type_consistency,
        'outliers': check_outliers,
        'formats': check_format_patterns,
        'whitespace': check_whitespace,
        'empty': check_empty_columns,
        'drift': check_schema_drift,
    }

    if args.checks:
        selected = [c.strip() for c in args.checks.split(',')]
        checks = {k: v for k, v in all_checks.items() if k in selected}
    else:
        checks = all_checks

    # Run checks
    issues = []
    for name, check_fn in checks.items():
        issues.extend(check_fn(headers, rows))

    # Schema validation
    if args.schema:
        if os.path.isfile(args.schema):
            issues.extend(validate_against_schema(headers, rows, args.schema))
        else:
            print(f"Warning: Schema file not found: {args.schema}", file=sys.stderr)

    # Filter by severity
    if args.severity:
        severity_order = {'info': 0, 'warning': 1, 'critical': 2}
        min_sev = severity_order[args.severity]
        issues = [i for i in issues if severity_order.get(i['severity'], 0) >= min_sev]

    # Sort: critical > warning > info
    severity_sort = {'critical': 0, 'warning': 1, 'info': 2}
    issues.sort(key=lambda x: severity_sort.get(x['severity'], 9))

    score = compute_quality_score(issues, len(rows), len(headers))

    report = {
        'file': args.file,
        'rows': len(rows),
        'columns': len(headers),
        'column_names': headers,
        'quality_score': score,
        'issues': issues,
        'checked_at': datetime.now().isoformat(),
    }

    # Format output
    if args.format == 'terminal':
        output = format_terminal(report)
    elif args.format == 'markdown':
        output = format_markdown(report)
    else:
        output = format_json_output(report)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Report written to {args.output}")
    else:
        print(output)

    # Exit code based on severity
    has_critical = any(i['severity'] == 'critical' for i in issues)
    has_warning = any(i['severity'] == 'warning' for i in issues)
    if has_critical:
        sys.exit(2)
    elif has_warning:
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()

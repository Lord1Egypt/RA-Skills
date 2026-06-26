#!/usr/bin/env python3
"""Validate .env files against schemas, compare environments, and detect common mistakes.

Usage:
    python3 validate_env.py .env                          # Validate with auto-detected rules
    python3 validate_env.py .env --schema env-schema.json # Validate against schema
    python3 validate_env.py --diff .env.dev .env.prod     # Compare two env files
    python3 validate_env.py --generate-schema .env        # Generate schema from existing .env
    python3 validate_env.py .env --output json            # JSON report
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# --- Common mistake detectors ---

COMMON_MISTAKES = [
    {
        'id': 'trailing_space',
        'pattern': r'.+\s+$',
        'check': lambda k, v, raw: raw.rstrip('\n') != raw.rstrip(),
        'message': 'Trailing whitespace in value (may cause unexpected behavior)',
        'severity': 'warning',
    },
    {
        'id': 'unquoted_space',
        'check': lambda k, v, raw: ' ' in v and not (v.startswith('"') or v.startswith("'")) and '="' not in raw and "='" not in raw,
        'message': 'Value contains spaces but is not quoted',
        'severity': 'warning',
    },
    {
        'id': 'placeholder',
        'check': lambda k, v, raw: any(p in v.lower() for p in ['change_me', 'todo', 'xxx', 'your_', 'replace_this', '<your', 'fixme']),
        'message': 'Value appears to be a placeholder',
        'severity': 'error',
    },
    {
        'id': 'empty_value',
        'check': lambda k, v, raw: v == '' and '=' in raw,
        'message': 'Variable is defined but empty',
        'severity': 'info',
    },
    {
        'id': 'duplicate_quote',
        'check': lambda k, v, raw: (v.startswith('""') or v.startswith("''")) and len(v) > 2,
        'message': 'Value has double-nested quotes',
        'severity': 'warning',
    },
    {
        'id': 'url_no_protocol',
        'check': lambda k, v, raw: any(s in k.upper() for s in ['URL', 'ENDPOINT', 'HOST', 'URI']) and v and not v.startswith(('http://', 'https://', 'postgres://', 'mysql://', 'redis://', 'mongodb://', 'amqp://', 'smtp://', 'localhost', '127.', '0.0.0.0')),
        'message': 'URL-like variable missing protocol prefix',
        'severity': 'warning',
    },
    {
        'id': 'port_out_of_range',
        'check': lambda k, v, raw: 'PORT' in k.upper() and v.isdigit() and (int(v) < 1 or int(v) > 65535),
        'message': 'Port number out of valid range (1-65535)',
        'severity': 'error',
    },
    {
        'id': 'suspicious_secret',
        'check': lambda k, v, raw: any(s in k.upper() for s in ['SECRET', 'PASSWORD', 'KEY', 'TOKEN']) and len(v) < 8 and v not in ('', 'true', 'false'),
        'message': 'Secret/password value is suspiciously short (< 8 chars)',
        'severity': 'warning',
    },
    {
        'id': 'boolean_inconsistent',
        'check': lambda k, v, raw: v.lower() in ('yes', 'no', 'on', 'off', '1', '0') and any(s in k.upper() for s in ['ENABLE', 'DISABLE', 'FLAG', 'ACTIVE', 'DEBUG', 'VERBOSE']),
        'message': 'Consider using true/false for boolean values (more standard)',
        'severity': 'info',
    },
    {
        'id': 'mixed_case_key',
        'check': lambda k, v, raw: k != k.upper() and '_' in k,
        'message': 'Key uses mixed case (convention: UPPER_SNAKE_CASE)',
        'severity': 'info',
    },
    {
        'id': 'inline_comment',
        'check': lambda k, v, raw: ' #' in v and not (v.startswith('"') or v.startswith("'")),
        'message': 'Possible inline comment (not supported in all parsers)',
        'severity': 'warning',
    },
]

# --- Type inference ---

TYPE_PATTERNS = {
    'integer': r'^\d+$',
    'float': r'^\d+\.\d+$',
    'boolean': r'^(true|false|yes|no|on|off|1|0)$',
    'url': r'^https?://',
    'email': r'^[^@]+@[^@]+\.[^@]+$',
    'ip': r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',
    'port': r'^\d{1,5}$',
    'path': r'^[/~]',
    'connection_string': r'^(postgres|mysql|mongodb|redis|amqp)://',
    'string': r'.*',
}

def infer_type(key, value):
    """Infer the type of an env value."""
    if not value:
        return 'string'
    if 'PORT' in key.upper():
        return 'port'
    if any(s in key.upper() for s in ['URL', 'ENDPOINT', 'URI']):
        return 'url'
    if any(s in key.upper() for s in ['EMAIL', 'MAIL_TO', 'MAIL_FROM']):
        return 'email'
    for type_name, pattern in TYPE_PATTERNS.items():
        if type_name == 'string':
            continue
        if re.match(pattern, value, re.IGNORECASE):
            return type_name
    return 'string'

# --- .env parser ---

def parse_env_file(path):
    """Parse a .env file and return list of (key, value, raw_line, line_num)."""
    entries = []
    try:
        with open(path, 'r') as f:
            lines = f.readlines()
    except (OSError, IOError) as e:
        print(f"Error: Cannot read {path}: {e}", file=sys.stderr)
        sys.exit(1)

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Skip empty lines and comments
        if not stripped or stripped.startswith('#'):
            continue

        # Handle export prefix
        if stripped.startswith('export '):
            stripped = stripped[7:]

        # Parse key=value
        if '=' not in stripped:
            entries.append((stripped, '', line, i, 'invalid'))
            continue

        key, _, value = stripped.partition('=')
        key = key.strip()

        # Handle quoted values
        value = value.strip()
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]

        entries.append((key, value, line, i, 'valid'))

    return entries

# --- Schema ---

def load_schema(path):
    """Load a validation schema from JSON.

    Schema format:
    {
        "variables": {
            "DATABASE_URL": {
                "type": "connection_string",
                "required": true,
                "description": "PostgreSQL connection string",
                "pattern": "^postgres://",
                "examples": ["postgres://user:pass@localhost:5432/db"]
            },
            "PORT": {
                "type": "port",
                "required": true,
                "default": "3000",
                "min": 1,
                "max": 65535
            },
            "DEBUG": {
                "type": "boolean",
                "required": false,
                "default": "false"
            }
        }
    }
    """
    with open(path) as f:
        return json.load(f)

def generate_schema(entries, output_path=None):
    """Generate a schema from existing .env entries."""
    schema = {'variables': {}}

    for key, value, raw, line_num, status in entries:
        if status == 'invalid':
            continue
        var_type = infer_type(key, value)
        var_def = {
            'type': var_type,
            'required': True,
        }
        if value:
            var_def['example'] = value
        if any(s in key.upper() for s in ['SECRET', 'PASSWORD', 'KEY', 'TOKEN', 'API_KEY']):
            var_def['sensitive'] = True
        schema['variables'][key] = var_def

    result = json.dumps(schema, indent=2)

    if output_path:
        Path(output_path).write_text(result)
        print(f"Schema written to {output_path}", file=sys.stderr)
    else:
        print(result)

    return schema

# --- Validators ---

def validate_against_schema(entries, schema):
    """Validate entries against a schema."""
    issues = []
    variables = schema.get('variables', {})
    found_keys = set()

    for key, value, raw, line_num, status in entries:
        found_keys.add(key)

        if key not in variables:
            issues.append({
                'key': key,
                'line': line_num,
                'severity': 'info',
                'message': f'Variable not defined in schema',
            })
            continue

        var_def = variables[key]

        # Type check
        expected_type = var_def.get('type', 'string')
        if expected_type == 'integer' and value and not value.isdigit():
            issues.append({
                'key': key, 'line': line_num, 'severity': 'error',
                'message': f'Expected integer, got "{value}"',
            })
        elif expected_type == 'boolean' and value.lower() not in ('true', 'false', 'yes', 'no', '1', '0', 'on', 'off', ''):
            issues.append({
                'key': key, 'line': line_num, 'severity': 'error',
                'message': f'Expected boolean, got "{value}"',
            })
        elif expected_type == 'port' and value:
            if not value.isdigit() or int(value) < 1 or int(value) > 65535:
                issues.append({
                    'key': key, 'line': line_num, 'severity': 'error',
                    'message': f'Invalid port: {value} (must be 1-65535)',
                })
        elif expected_type == 'url' and value and not re.match(r'^(https?|postgres|mysql|mongodb|redis|amqp|smtp|ftp)://', value):
            issues.append({
                'key': key, 'line': line_num, 'severity': 'error',
                'message': f'Expected URL with protocol prefix',
            })

        # Pattern check
        pattern = var_def.get('pattern')
        if pattern and value and not re.match(pattern, value):
            issues.append({
                'key': key, 'line': line_num, 'severity': 'error',
                'message': f'Value does not match pattern: {pattern}',
            })

        # Range check
        if value and value.isdigit():
            num = int(value)
            if 'min' in var_def and num < var_def['min']:
                issues.append({
                    'key': key, 'line': line_num, 'severity': 'error',
                    'message': f'Value {num} is below minimum {var_def["min"]}',
                })
            if 'max' in var_def and num > var_def['max']:
                issues.append({
                    'key': key, 'line': line_num, 'severity': 'error',
                    'message': f'Value {num} exceeds maximum {var_def["max"]}',
                })

    # Check required variables
    for var_name, var_def in variables.items():
        if var_def.get('required', False) and var_name not in found_keys:
            issues.append({
                'key': var_name,
                'line': 0,
                'severity': 'error',
                'message': 'Required variable is missing',
            })

    return issues

def run_common_checks(entries):
    """Run common mistake checks on all entries."""
    issues = []

    # Check for duplicate keys
    seen_keys = {}
    for key, value, raw, line_num, status in entries:
        if status == 'invalid':
            issues.append({
                'key': key, 'line': line_num, 'severity': 'error',
                'message': f'Invalid line (no = sign): "{raw.strip()}"',
            })
            continue

        if key in seen_keys:
            issues.append({
                'key': key, 'line': line_num, 'severity': 'warning',
                'message': f'Duplicate key (first defined on line {seen_keys[key]})',
            })
        seen_keys[key] = line_num

        # Run common mistake checks
        for check in COMMON_MISTAKES:
            try:
                if 'check' in check and check['check'](key, value, raw):
                    issues.append({
                        'key': key,
                        'line': line_num,
                        'severity': check['severity'],
                        'message': check['message'],
                        'check_id': check['id'],
                    })
            except Exception:
                pass

    return issues

# --- Diff ---

def diff_env_files(path1, path2):
    """Compare two env files and report differences."""
    entries1 = parse_env_file(path1)
    entries2 = parse_env_file(path2)

    vars1 = {k: v for k, v, _, _, s in entries1 if s == 'valid'}
    vars2 = {k: v for k, v, _, _, s in entries2 if s == 'valid'}

    keys1 = set(vars1.keys())
    keys2 = set(vars2.keys())

    only_in_1 = sorted(keys1 - keys2)
    only_in_2 = sorted(keys2 - keys1)
    common = sorted(keys1 & keys2)

    different = []
    for k in common:
        if vars1[k] != vars2[k]:
            different.append(k)

    return {
        'file1': str(path1),
        'file2': str(path2),
        'only_in_file1': only_in_1,
        'only_in_file2': only_in_2,
        'different_values': different,
        'identical': [k for k in common if k not in different],
        'vars1': vars1,
        'vars2': vars2,
    }

# --- Output formatters ---

def format_text(issues, entries, filepath):
    """Format validation results as text."""
    lines = [f"Validating: {filepath}", ""]

    if not issues:
        lines.append("No issues found.")
        return '\n'.join(lines)

    errors = [i for i in issues if i['severity'] == 'error']
    warnings = [i for i in issues if i['severity'] == 'warning']
    infos = [i for i in issues if i['severity'] == 'info']

    lines.append(f"Found {len(issues)} issue(s): {len(errors)} error(s), {len(warnings)} warning(s), {len(infos)} info(s)")
    lines.append("")

    for severity, label, items in [('error', 'ERRORS', errors), ('warning', 'WARNINGS', warnings), ('info', 'INFO', infos)]:
        if items:
            lines.append(f"--- {label} ---")
            for issue in items:
                loc = f"line {issue['line']}" if issue['line'] else 'missing'
                lines.append(f"  [{severity.upper()}] {issue['key']} ({loc}): {issue['message']}")
            lines.append("")

    return '\n'.join(lines)

def format_diff_text(diff_result):
    """Format diff results as text."""
    lines = [f"Comparing: {diff_result['file1']} vs {diff_result['file2']}", ""]

    if diff_result['only_in_file1']:
        lines.append(f"Only in {diff_result['file1']}:")
        for k in diff_result['only_in_file1']:
            lines.append(f"  - {k}")
        lines.append("")

    if diff_result['only_in_file2']:
        lines.append(f"Only in {diff_result['file2']}:")
        for k in diff_result['only_in_file2']:
            lines.append(f"  + {k}")
        lines.append("")

    if diff_result['different_values']:
        lines.append("Different values:")
        for k in diff_result['different_values']:
            v1 = diff_result['vars1'][k]
            v2 = diff_result['vars2'][k]
            # Mask secrets
            if any(s in k.upper() for s in ['SECRET', 'PASSWORD', 'KEY', 'TOKEN']):
                v1 = v1[:3] + '***' if len(v1) > 3 else '***'
                v2 = v2[:3] + '***' if len(v2) > 3 else '***'
            lines.append(f"  ~ {k}:")
            lines.append(f"    < {v1}")
            lines.append(f"    > {v2}")
        lines.append("")

    total_vars = len(set(list(diff_result['vars1'].keys()) + list(diff_result['vars2'].keys())))
    identical = len(diff_result['identical'])
    lines.append(f"Summary: {total_vars} total vars, {identical} identical, "
                 f"{len(diff_result['only_in_file1'])} only in file1, "
                 f"{len(diff_result['only_in_file2'])} only in file2, "
                 f"{len(diff_result['different_values'])} different")

    return '\n'.join(lines)

def format_markdown(issues, entries, filepath):
    """Format as markdown report."""
    lines = [f"# Environment Validation: `{filepath}`", ""]

    if not issues:
        lines.append("No issues found.")
        return '\n'.join(lines)

    errors = [i for i in issues if i['severity'] == 'error']
    warnings = [i for i in issues if i['severity'] == 'warning']
    infos = [i for i in issues if i['severity'] == 'info']

    lines.append(f"**{len(issues)} issue(s) found:** {len(errors)} error(s), {len(warnings)} warning(s), {len(infos)} info(s)")
    lines.append("")

    if errors:
        lines.append("## Errors")
        lines.append("| Variable | Line | Issue |")
        lines.append("|----------|------|-------|")
        for i in errors:
            loc = i['line'] if i['line'] else '-'
            lines.append(f"| `{i['key']}` | {loc} | {i['message']} |")
        lines.append("")

    if warnings:
        lines.append("## Warnings")
        lines.append("| Variable | Line | Issue |")
        lines.append("|----------|------|-------|")
        for i in warnings:
            lines.append(f"| `{i['key']}` | {i['line']} | {i['message']} |")
        lines.append("")

    if infos:
        lines.append("## Info")
        lines.append("| Variable | Line | Issue |")
        lines.append("|----------|------|-------|")
        for i in infos:
            loc = i['line'] if i['line'] else '-'
            lines.append(f"| `{i['key']}` | {loc} | {i['message']} |")
        lines.append("")

    return '\n'.join(lines)

# --- Main ---

def main():
    parser = argparse.ArgumentParser(
        description='Validate .env files against schemas and detect common mistakes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s .env                            Validate with common checks
  %(prog)s .env --schema env-schema.json   Validate against schema
  %(prog)s --diff .env.dev .env.prod       Compare two environments
  %(prog)s --generate-schema .env          Generate schema from .env
  %(prog)s .env --output json              JSON report
        """
    )

    parser.add_argument('env_file', nargs='?', help='.env file to validate')
    parser.add_argument('--schema', help='JSON schema file for validation')
    parser.add_argument('--diff', nargs=2, metavar='FILE', help='Compare two env files')
    parser.add_argument('--generate-schema', metavar='ENV_FILE', help='Generate schema from .env file')
    parser.add_argument('--output', choices=['text', 'json', 'markdown'], default='text', help='Output format (default: text)')
    parser.add_argument('-o', '--out', help='Output file path')
    parser.add_argument('--ignore', action='append', default=[], help='Check IDs to ignore (repeatable)')
    parser.add_argument('--severity', choices=['error', 'warning', 'info'], default='info', help='Minimum severity to report (default: info)')

    args = parser.parse_args()

    # Schema generation mode
    if args.generate_schema:
        entries = parse_env_file(args.generate_schema)
        generate_schema(entries, args.out)
        sys.exit(0)

    # Diff mode
    if args.diff:
        diff_result = diff_env_files(args.diff[0], args.diff[1])
        if args.output == 'json':
            result = json.dumps(diff_result, indent=2)
        elif args.output == 'markdown':
            result = format_diff_text(diff_result)  # Use text for markdown too
        else:
            result = format_diff_text(diff_result)

        if args.out:
            Path(args.out).write_text(result)
            print(f"Report written to {args.out}", file=sys.stderr)
        else:
            print(result)

        has_issues = bool(diff_result['only_in_file1'] or diff_result['only_in_file2'] or diff_result['different_values'])
        sys.exit(1 if has_issues else 0)

    # Validation mode
    if not args.env_file:
        parser.error("Provide a .env file to validate, or use --diff or --generate-schema")

    entries = parse_env_file(args.env_file)

    # Run checks
    issues = run_common_checks(entries)

    # Schema validation
    if args.schema:
        schema = load_schema(args.schema)
        issues.extend(validate_against_schema(entries, schema))

    # Filter by severity
    severity_order = {'error': 2, 'warning': 1, 'info': 0}
    min_sev = severity_order[args.severity]
    issues = [i for i in issues if severity_order.get(i['severity'], 0) >= min_sev]

    # Filter by ignored checks
    if args.ignore:
        issues = [i for i in issues if i.get('check_id') not in args.ignore]

    # Sort: errors first, then warnings, then info
    issues.sort(key=lambda x: -severity_order.get(x['severity'], 0))

    # Output
    if args.output == 'json':
        result = json.dumps({'file': args.env_file, 'issues': issues, 'total': len(issues)}, indent=2)
    elif args.output == 'markdown':
        result = format_markdown(issues, entries, args.env_file)
    else:
        result = format_text(issues, entries, args.env_file)

    if args.out:
        Path(args.out).write_text(result)
        print(f"Report written to {args.out}", file=sys.stderr)
    else:
        print(result)

    # Exit codes
    errors = [i for i in issues if i['severity'] == 'error']
    if errors:
        sys.exit(2)
    warnings = [i for i in issues if i['severity'] == 'warning']
    if warnings:
        sys.exit(1)
    sys.exit(0)

if __name__ == '__main__':
    main()

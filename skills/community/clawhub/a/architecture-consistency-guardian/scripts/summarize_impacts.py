#!/usr/bin/env python3
"""Aggregate scan results into an impact summary for consistency reports.

Reads JSON output from grep_legacy.py or scan_contract_drift.py and produces
structured impact summaries suitable for Phase 8 reports.

Usage:
    python3 grep_legacy.py <dir> <patterns...> --json | python3 summarize_impacts.py
    python3 scan_contract_drift.py <dir> --json | python3 summarize_impacts.py
    python3 summarize_impacts.py --file scan_results.json [--source-of-truth runtime_config.py]
"""

import argparse
import json
import sys
from collections import defaultdict


def classify_file(filepath):
    """Classify a file into a role category."""
    path_lower = filepath.lower()

    if any(k in path_lower for k in ['test_', '_test.', 'tests/', 'test/']):
        return 'test'
    if path_lower.endswith('.md'):
        return 'documentation'
    if any(k in path_lower for k in ['config', 'settings', 'env']):
        return 'configuration'
    if any(k in path_lower for k in ['migration', 'schema', 'alembic']):
        return 'schema'
    if any(k in path_lower for k in ['skill.md', 'readme']):
        return 'documentation'
    return 'source'


def detect_input_type(data):
    """Detect supported input types and normalize their tool identity."""
    if isinstance(data, dict) and {'tool', 'schema_version', 'results'}.issubset(data.keys()):
        tool = data.get('tool')
        if tool == 'grep_legacy':
            return 'grep_legacy_schema'
        if tool == 'scan_contract_drift':
            return 'scan_contract_drift_schema'
        return 'unknown_schema'
    if isinstance(data, dict):
        return 'grep_legacy_legacy'
    if isinstance(data, list):
        return 'scan_contract_drift_legacy'
    return 'unsupported'


def normalize_grep_items(data):
    input_type = detect_input_type(data)
    if input_type == 'grep_legacy_schema':
        return data.get('results', []), data.get('errors', []), data.get('scan_root')

    items = []
    for filepath, hits in data.items():
        for hit in hits:
            items.append({
                'filepath': filepath,
                'line': hit.get('line'),
                'text': hit.get('text', ''),
                'pattern': hit.get('pattern', 'unknown'),
            })
    return items, [], None


def normalize_drift_items(data):
    input_type = detect_input_type(data)
    if input_type == 'scan_contract_drift_schema':
        return data.get('results', []), data.get('errors', []), data.get('scan_root')
    return data, [], None


def summarize_grep(results, source_of_truth=None):
    if not results:
        return {
            'summary_kind': 'grep_legacy',
            'total_files': 0,
            'total_hits': 0,
            'clean': True,
            'by_category': {},
            'by_pattern': {},
            'source_of_truth_affected': False,
            'source_of_truth': source_of_truth,
        }

    by_category = defaultdict(lambda: {'files': set(), 'hits': 0})
    by_pattern = defaultdict(lambda: {'files': set(), 'hits': 0})
    affected_files = set()

    for item in results:
        filepath = item['filepath']
        pattern = item.get('pattern', 'unknown')
        category = classify_file(filepath)
        affected_files.add(filepath)
        by_category[category]['files'].add(filepath)
        by_category[category]['hits'] += 1
        by_pattern[pattern]['files'].add(filepath)
        by_pattern[pattern]['hits'] += 1

    sot_affected = False
    if source_of_truth:
        sot_affected = any(source_of_truth in filepath for filepath in affected_files)

    return {
        'summary_kind': 'grep_legacy',
        'total_files': len(affected_files),
        'total_hits': len(results),
        'clean': len(results) == 0,
        'by_category': {
            key: {'files': sorted(value['files']), 'hits': value['hits']}
            for key, value in sorted(by_category.items())
        },
        'by_pattern': {
            key: {'files': sorted(value['files']), 'hits': value['hits']}
            for key, value in sorted(by_pattern.items())
        },
        'source_of_truth_affected': sot_affected,
        'source_of_truth': source_of_truth,
    }


def summarize_drift(results, source_of_truth=None):
    if not results:
        return {
            'summary_kind': 'scan_contract_drift',
            'total_findings': 0,
            'total_impacted_files': 0,
            'total_hits': 0,
            'clean': True,
            'by_category': {},
            'by_severity': {},
            'affected_files': [],
            'source_of_truth_affected': False,
            'source_of_truth': source_of_truth,
        }

    by_category = defaultdict(lambda: {'findings': 0, 'hits': 0})
    by_severity = defaultdict(lambda: {'findings': 0})
    affected_files = set()
    total_hits = 0

    for item in results:
        category = item.get('category', 'unknown')
        severity = item.get('severity', 'unknown')
        hit_count = item.get('hit_count', len(item.get('evidence', [])))
        by_category[category]['findings'] += 1
        by_category[category]['hits'] += hit_count
        by_severity[severity]['findings'] += 1
        total_hits += hit_count
        affected_files.update(item.get('files', []))

    sot_affected = False
    if source_of_truth:
        sot_affected = any(source_of_truth in filepath for filepath in affected_files)

    return {
        'summary_kind': 'scan_contract_drift',
        'total_findings': len(results),
        'total_impacted_files': len(affected_files),
        'total_hits': total_hits,
        'clean': len(results) == 0,
        'by_category': dict(sorted(by_category.items())),
        'by_severity': dict(sorted(by_severity.items())),
        'affected_files': sorted(affected_files),
        'source_of_truth_affected': sot_affected,
        'source_of_truth': source_of_truth,
    }


def summarize(data, source_of_truth=None):
    input_type = detect_input_type(data)

    if input_type in {'grep_legacy_schema', 'grep_legacy_legacy'}:
        items, errors, scan_root = normalize_grep_items(data)
        summary = summarize_grep(items, source_of_truth=source_of_truth)
    elif input_type in {'scan_contract_drift_schema', 'scan_contract_drift_legacy'}:
        items, errors, scan_root = normalize_drift_items(data)
        summary = summarize_drift(items, source_of_truth=source_of_truth)
    elif input_type == 'unknown_schema':
        raise ValueError('Unsupported schema tool. Expected grep_legacy or scan_contract_drift.')
    else:
        raise ValueError('Unsupported JSON format. Expected legacy output or unified scan schema.')

    summary['input_type'] = input_type
    summary['scan_root'] = scan_root
    summary['errors'] = errors
    return summary


def print_grep_summary(summary):
    if summary['clean']:
        print('✅ Clean — no legacy residue detected.')
        return

    print('## Impact Summary\n')
    print(f"- **Input type**: `grep_legacy`")
    print(f"- **Total files affected**: {summary['total_files']}")
    print(f"- **Total hits**: {summary['total_hits']}")

    if summary.get('source_of_truth'):
        status = '⚠️ YES' if summary['source_of_truth_affected'] else '✅ No'
        print(f"- **Source of truth ({summary['source_of_truth']}) affected**: {status}")

    print('\n### By file category\n')
    print('| Category | Files | Hits |')
    print('|----------|-------|------|')
    for cat, data in sorted(summary['by_category'].items(), key=lambda x: -x[1]['hits']):
        print(f"| {cat} | {len(data['files'])} | {data['hits']} |")

    print('\n### By pattern\n')
    print('| Pattern | Files | Hits |')
    print('|---------|-------|------|')
    for pat, data in sorted(summary['by_pattern'].items(), key=lambda x: -x[1]['hits']):
        display = pat[:60] + '...' if len(pat) > 60 else pat
        print(f"| `{display}` | {len(data['files'])} | {data['hits']} |")

    print('\n### Affected files\n')
    all_files = set()
    for data in summary['by_category'].values():
        all_files.update(data['files'])
    for filepath in sorted(all_files):
        print(f"- `{filepath}` ({classify_file(filepath)})")


def print_drift_summary(summary):
    if summary['clean']:
        print('✅ Clean — no contract drift detected.')
        return

    print('## Contract Drift Summary\n')
    print(f"- **Input type**: `scan_contract_drift`")
    print(f"- **Total findings**: {summary['total_findings']}")
    print(f"- **Impacted files**: {summary['total_impacted_files']}")
    print(f"- **Total evidence hits**: {summary['total_hits']}")

    if summary.get('source_of_truth'):
        status = '⚠️ YES' if summary['source_of_truth_affected'] else '✅ No'
        print(f"- **Source of truth ({summary['source_of_truth']}) affected**: {status}")

    print('\n### By category\n')
    print('| Category | Findings | Hits |')
    print('|----------|----------|------|')
    for category, data in sorted(summary['by_category'].items(), key=lambda x: -x[1]['findings']):
        print(f"| {category} | {data['findings']} | {data['hits']} |")

    print('\n### By severity\n')
    print('| Severity | Findings |')
    print('|----------|----------|')
    for severity, data in sorted(summary['by_severity'].items(), key=lambda x: x[0]):
        print(f"| {severity} | {data['findings']} |")

    print('\n### Affected files\n')
    for filepath in summary['affected_files']:
        print(f"- `{filepath}` ({classify_file(filepath)})")


def print_summary(summary):
    if summary['summary_kind'] == 'grep_legacy':
        print_grep_summary(summary)
    elif summary['summary_kind'] == 'scan_contract_drift':
        print_drift_summary(summary)
    else:
        raise ValueError(f"Unsupported summary kind: {summary['summary_kind']}")

    if summary.get('errors'):
        print('\n### Non-fatal errors\n')
        for err in summary['errors']:
            print(f"- `{err.get('filepath', 'unknown')}`: {err['message']}")


def main():
    parser = argparse.ArgumentParser(
        description='Aggregate scan results into an impact summary.'
    )
    parser.add_argument('--file', help='JSON file from grep_legacy.py or scan_contract_drift.py (default: stdin)')
    parser.add_argument('--source-of-truth', help='Canonical file path to check')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    if args.file:
        with open(args.file) as f:
            data = json.load(f)
    else:
        if sys.stdin.isatty():
            print('Error: Provide --file or pipe JSON from grep_legacy.py/scan_contract_drift.py --json', file=sys.stderr)
            sys.exit(1)
        data = json.load(sys.stdin)

    try:
        summary = summarize(data, source_of_truth=args.source_of_truth)
    except ValueError as exc:
        print(f'Error: {exc}', file=sys.stderr)
        sys.exit(2)

    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print_summary(summary)


if __name__ == '__main__':
    main()

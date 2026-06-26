#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from auditlib.backend_extractors import build_java_dto_index, extract_backend_endpoints, extract_security_rules
from auditlib.compare import compare_surfaces
from auditlib.frontend_extractors import extract_frontend_endpoints
from auditlib.report import render_markdown, summarize_findings

SEVERITY_RANK = {'low': 1, 'medium': 2, 'high': 3}


def parse_excludes(values: list[str]) -> list[str]:
    out: list[str] = []
    for value in values:
        for part in value.split(','):
            cleaned = part.strip()
            if cleaned:
                out.append(cleaned)
    return sorted(set(out))


def build_report(frontend, backend, frontend_paths, backend_paths, findings, unknowns, next_actions, risk_level, stats):
    return {
        'summary': {
            'audited_surfaces': [str(p) for p in frontend_paths],
            'backend_roots': [str(p) for p in backend_paths],
            'frontend_endpoints_found': len(frontend),
            'backend_endpoints_found': len(backend),
            'exact_matches': stats['frontend_exact_matches'],
            'dynamic_path_matches': stats['frontend_dynamic_matches'],
            'missing_backend_endpoints': stats['frontend_missing'],
            'method_mismatches': stats['frontend_method_mismatches'],
            'path_mismatches': stats['frontend_path_mismatches'],
            'hint_mismatches': stats['hint_mismatches'],
            'ambiguous_unmatched_frontend_calls': stats['frontend_ambiguous_unmatched'],
            'backend_only_endpoints': stats['backend_only'],
            'findings': len(findings),
            'risk_level': risk_level,
            'finding_breakdown': summarize_findings(findings),
        },
        'frontend_endpoints': [asdict(x) for x in frontend],
        'backend_endpoints': [asdict(x) for x in backend],
        'findings': [asdict(x) for x in findings],
        'unknowns': unknowns,
        'next_actions': next_actions,
    }


def print_summary(report: dict):
    summary = report['summary']
    print(f"Frontend endpoints: {summary['frontend_endpoints_found']}")
    print(f"Backend endpoints: {summary['backend_endpoints_found']}")
    print(f"Exact matches: {summary['exact_matches']}")
    print(f"Dynamic matches: {summary['dynamic_path_matches']}")
    print(f"Missing backend: {summary['missing_backend_endpoints']}")
    print(f"Method mismatches: {summary['method_mismatches']}")
    print(f"Path mismatches: {summary['path_mismatches']}")
    print(f"Hint mismatches: {summary['hint_mismatches']}")
    print(f"Backend-only: {summary['backend_only_endpoints']}")
    print(f"Findings: {summary['findings']}")
    print(f"Risk: {summary['risk_level']}")


def main():
    parser = argparse.ArgumentParser(description='Static frontend-backend contract audit')
    parser.add_argument('--frontend', action='append', default=[], help='Frontend root path (repeatable)')
    parser.add_argument('--backend', action='append', default=[], help='Backend root path (repeatable)')
    parser.add_argument('--output-dir', required=True, help='Directory to write audit outputs')
    parser.add_argument('--exclude', action='append', default=[], help='Directory/file path parts to ignore (repeatable or comma-separated)')
    parser.add_argument('--format', choices=['both', 'json', 'md'], default='both', help='Output file format')
    parser.add_argument('--summary-only', action='store_true', help='Print summary only; still writes selected output files')
    parser.add_argument('--fail-on', choices=['none', 'low', 'medium', 'high'], default='none', help='Exit non-zero if findings reach this severity or higher')
    args = parser.parse_args()

    frontend_paths = [Path(p).expanduser().resolve() for p in args.frontend]
    backend_paths = [Path(p).expanduser().resolve() for p in args.backend]
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    excludes = parse_excludes(args.exclude)
    if excludes:
        os.environ['AUDIT_EXCLUDE_PARTS'] = ','.join(excludes)

    frontend = []
    for root in frontend_paths:
        if root.exists():
            frontend.extend(extract_frontend_endpoints(root))

    backend = []
    for root in backend_paths:
        if root.exists():
            dto_index = build_java_dto_index(root)
            security_rules = extract_security_rules(root)
            backend.extend(extract_backend_endpoints(root, dto_index, security_rules))

    findings, unknowns, next_actions, risk_level, stats = compare_surfaces(frontend, backend)
    report = build_report(frontend, backend, frontend_paths, backend_paths, findings, unknowns, next_actions, risk_level, stats)

    if args.format in {'both', 'json'}:
        json_path = output_dir / 'audit-report.json'
        json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        if not args.summary_only:
            print(f'Wrote {json_path}')
    if args.format in {'both', 'md'}:
        md_path = output_dir / 'audit-report.md'
        md_path.write_text(render_markdown(frontend, backend, findings, unknowns, next_actions, risk_level, stats), encoding='utf-8')
        if not args.summary_only:
            print(f'Wrote {md_path}')

    if excludes and not args.summary_only:
        print('Excluded path parts: ' + ', '.join(excludes))
    print_summary(report)

    if args.fail_on != 'none':
        threshold = SEVERITY_RANK[args.fail_on]
        highest = max((SEVERITY_RANK.get(f.severity, 0) for f in findings), default=0)
        if highest >= threshold:
            return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

#!/usr/bin/env python3
"""Detect multiple competing sources of truth in a codebase.

Scans for patterns that indicate contract drift:
- Multiple files defining the same config constant
- Multiple files writing to the same DB table
- Multiple files defining status/state value sets
- Multiple files acting as conflicting architecture entry points

Usage:
    python3 scan_contract_drift.py <directory> [--pattern-file <file>] [--ext .py .md]
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone


SCHEMA_VERSION = "1.0"
BUILTIN_PATTERNS = {
    "config_definition": [
        r'^\s*(?!DB_PATH\b|DATABASE_PATH\b|MEMORY_DB_PATH\b)[A-Z_]+PATH\s*=\s*["\'/]',
        r'^\s*[A-Z_]+DIR\s*=\s*["\'/]',
        r'^\s*[A-Z_]+URL\s*=\s*["\'/]',
        r'^\s*DB_PATH\s*=',
        r'^\s*DATABASE_PATH\s*=',
        r'^\s*MEMORY_DB_PATH\s*=',
        r'os\.environ\.get\(["\'][A-Z_]+PATH',
        r'os\.environ\[["\'][A-Z_]+PATH',
    ],
    "table_write": [
        r'INSERT\s+INTO\s+\w+',
        r'UPDATE\s+\w+\s+SET',
        r'\.execute\(["\']INSERT',
        r'\.execute\(["\']UPDATE',
        r'cursor\.execute.*INSERT',
        r'cursor\.execute.*UPDATE',
    ],
    "state_definition": [
        r'STATUS_VALUES\s*=',
        r'VALID_STATES\s*=',
        r'STATE_TRANSITIONS\s*=',
        r'ALLOWED_TRANSITIONS\s*=',
        r'status.*=.*["\']draft["\'].*["\']pending',
        r'lifecycle_status',
    ],
    "entry_point": [
        r'^\s*def\s+(create_app|build_app|configure_app|register_routes|register_handlers)\s*\(',
        r'^\s*def\s+(write_[a-z0-9_]+|persist_[a-z0-9_]+|save_[a-z0-9_]+_state)\s*\(',
        r'^\s*class\s+\w+(Manager|Coordinator|Orchestrator|Service)\b',
    ],
}
DEFAULT_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx', '.md', '.yaml', '.yml',
    '.json', '.toml', '.cfg', '.ini', '.sql',
}
DEFAULT_IGNORE_DIRS = {
    '.git', '__pycache__', 'node_modules', '.venv', 'venv',
    '.mypy_cache', '.pytest_cache', 'dist', 'build', '.egg-info',
}
NON_CANONICAL_DIR_HINTS = {'references', 'templates', 'assets', 'tests', 'fixtures'}


def is_non_canonical_path(relpath):
    parts = relpath.split(os.sep)
    return any(part in NON_CANONICAL_DIR_HINTS for part in parts)


def utc_now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_payload(scan_root, results=None, summary=None, errors=None):
    return {
        "tool": "scan_contract_drift",
        "schema_version": SCHEMA_VERSION,
        "scan_root": os.path.abspath(scan_root),
        "generated_at": utc_now_iso(),
        "results": results or [],
        "summary": summary or {},
        "errors": errors or [],
    }


def load_custom_patterns(filepath):
    """Load patterns from a file. Format: category:regex per line."""
    patterns = defaultdict(list)
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if ':' in line:
                cat, pat = line.split(':', 1)
                patterns[cat.strip()].append(pat.strip())
            else:
                patterns["custom"].append(line)
    return dict(patterns)


def compile_pattern_groups(patterns):
    compiled = {}
    for category, pats in patterns.items():
        compiled[category] = [(pat, re.compile(pat)) for pat in pats]
    return compiled


def scan_for_drift(directory, compiled_patterns, extensions, ignore_dirs):
    """Scan directory for contract drift patterns.

    Returns:
        tuple[dict, list]: results, errors
    """
    results = defaultdict(lambda: defaultdict(list))
    errors = []

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for fname in files:
            ext = os.path.splitext(fname)[1]
            if ext not in extensions:
                continue
            fpath = os.path.join(root, fname)
            if os.path.islink(fpath):
                continue
            try:
                with open(fpath, 'r', errors='replace') as f:
                    for line_no, line in enumerate(f, 1):
                        for category, pats in compiled_patterns.items():
                            for original, matcher in pats:
                                if matcher.search(line):
                                    results[category][original].append({
                                        "filepath": os.path.relpath(fpath, directory),
                                        "line": line_no,
                                        "text": line.rstrip(),
                                    })
            except (OSError, UnicodeDecodeError) as exc:
                errors.append({
                    "type": "file_read_error",
                    "filepath": fpath,
                    "message": str(exc),
                })

    return results, errors


def analyze_drift(results, mode="default"):
    """Analyze results to find competing sources (same pattern in multiple files)."""
    drift_warnings = []

    for category, pattern_hits in results.items():
        for pat, hits in pattern_hits.items():
            files = sorted({h["filepath"] for h in hits})
            if len(files) <= 1:
                continue

            if mode == "strict":
                effective_hits = hits
                ignored_hits = []
            else:
                effective_hits = [h for h in hits if not is_non_canonical_path(h["filepath"])]
                ignored_hits = [h for h in hits if is_non_canonical_path(h["filepath"])]
                effective_hits = effective_hits or hits

            effective_files = sorted({h["filepath"] for h in effective_hits})
            if len(effective_files) <= 1:
                continue

            severity = "high" if category in ("config_definition", "state_definition") else "medium"
            if mode == "lite" and category in ("entry_point", "table_write"):
                severity = "low"
            evidence = sorted(effective_hits, key=lambda item: (item["filepath"], item["line"]))[:10]
            warning = {
                "category": category,
                "pattern": pat,
                "files": effective_files,
                "hit_count": len(effective_hits),
                "severity": severity,
                "evidence": evidence,
            }
            if ignored_hits and effective_hits != hits:
                warning["ignored_reference_files"] = sorted({h["filepath"] for h in ignored_hits})
            drift_warnings.append(warning)

    severity_order = {"high": 0, "medium": 1, "low": 2}
    drift_warnings.sort(key=lambda w: (severity_order.get(w["severity"], 9), -w["hit_count"], w["category"]))
    return drift_warnings


def build_summary(warnings):
    by_category = defaultdict(int)
    by_severity = defaultdict(int)
    impacted_files = set()
    evidence_hits = 0

    for warning in warnings:
        by_category[warning["category"]] += 1
        by_severity[warning["severity"]] += 1
        impacted_files.update(warning["files"])
        evidence_hits += warning["hit_count"]

    return {
        "total_findings": len(warnings),
        "total_impacted_files": len(impacted_files),
        "total_hits": evidence_hits,
        "by_category": dict(sorted(by_category.items())),
        "by_severity": dict(sorted(by_severity.items())),
    }


def print_report(payload):
    warnings = payload["results"]
    if payload["errors"] and not warnings:
        print(f"Error: {payload['errors'][0]['message']}", file=sys.stderr)
        return
    if not warnings:
        print("✅ No contract drift detected. Each pattern maps to a single file.")
        return

    print(f"⚠️  Detected {len(warnings)} potential contract drift(s):\n")
    print("| Severity | Category | Pattern | Files | Hits |")
    print("|----------|----------|---------|-------|------|")
    for warning in warnings:
        sev = "🔴" if warning["severity"] == "high" else "🟡"
        files_str = ", ".join(warning["files"][:3])
        if len(warning["files"]) > 3:
            files_str += f" (+{len(warning['files']) - 3} more)"
        print(f"| {sev} {warning['severity']} | {warning['category']} | `{warning['pattern'][:50]}` | {files_str} | {warning['hit_count']} |")

    print("\n## Details\n")
    for warning in warnings:
        sev = "🔴" if warning["severity"] == "high" else "🟡"
        print(f"### {sev} {warning['category']}: `{warning['pattern'][:60]}`")
        print(f"Found in {len(warning['files'])} files:")
        for filepath in warning["files"]:
            print(f"  - {filepath}")
        if warning.get("evidence"):
            print("Evidence:")
            for item in warning["evidence"][:5]:
                text = item["text"][:120] + "..." if len(item["text"]) > 120 else item["text"]
                print(f"  - {item['filepath']}:L{item['line']} — {text}")
        print()

    if payload["errors"]:
        print("## Non-fatal errors\n")
        for err in payload["errors"]:
            print(f"- `{err.get('filepath', 'unknown')}`: {err['message']}")


def main():
    parser = argparse.ArgumentParser(
        description="Detect competing sources of truth (contract drift) in a codebase."
    )
    parser.add_argument("directory", help="Root directory to scan")
    parser.add_argument("--pattern-file", help="Custom pattern file (category:regex per line)")
    parser.add_argument("--ext", nargs="*", default=None,
                        help="File extensions to scan")
    parser.add_argument("--ignore-dir", nargs="*", default=None,
                        help="Directory names to skip")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")
    parser.add_argument("--mode", choices=("default", "lite", "strict"), default="default",
                        help="default ignores reference/test evidence, lite also down-ranks lower-risk categories, strict counts all hits")
    parser.add_argument("--builtin-only", action="store_true",
                        help="Use only built-in patterns (ignore --pattern-file)")

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a directory", file=sys.stderr)
        sys.exit(1)

    extensions = set(args.ext) if args.ext else DEFAULT_EXTENSIONS
    ignore_dirs = set(args.ignore_dir) if args.ignore_dir else DEFAULT_IGNORE_DIRS

    patterns = {category: list(values) for category, values in BUILTIN_PATTERNS.items()}
    if args.pattern_file and not args.builtin_only:
        custom = load_custom_patterns(args.pattern_file)
        for cat, pats in custom.items():
            patterns.setdefault(cat, []).extend(pats)

    try:
        compiled_patterns = compile_pattern_groups(patterns)
    except re.error as exc:
        payload = build_payload(
            args.directory,
            results=[],
            summary={"total_findings": 0, "total_impacted_files": 0, "total_hits": 0},
            errors=[{
                "type": "invalid_regex",
                "message": f"Invalid drift pattern: {exc}",
            }],
        )
        if args.json:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            print(payload["errors"][0]["message"], file=sys.stderr)
        sys.exit(2)

    scan_results, errors = scan_for_drift(args.directory, compiled_patterns, extensions, ignore_dirs)
    warnings = analyze_drift(scan_results, mode=args.mode)
    payload = build_payload(args.directory, results=warnings, summary=build_summary(warnings), errors=errors)

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print_report(payload)

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()

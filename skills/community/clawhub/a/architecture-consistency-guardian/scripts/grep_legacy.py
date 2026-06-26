#!/usr/bin/env python3
"""Scan directories for legacy name/path/status residue.

Usage:
    python3 grep_legacy.py <directory> <pattern1> [pattern2] ... [--ext .py .md]
    python3 grep_legacy.py <directory> "DB_PATH.*=.*/" --regex --json
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone


SCHEMA_VERSION = "1.0"
DEFAULT_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx', '.md', '.yaml', '.yml',
    '.json', '.toml', '.cfg', '.ini', '.sql', '.sh', '.bash',
}
DEFAULT_IGNORE_DIRS = {
    '.git', '__pycache__', 'node_modules', '.venv', 'venv',
    '.mypy_cache', '.pytest_cache', 'dist', 'build', '.egg-info',
}


def utc_now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_payload(scan_root, results=None, summary=None, errors=None):
    return {
        "tool": "grep_legacy",
        "schema_version": SCHEMA_VERSION,
        "scan_root": os.path.abspath(scan_root),
        "generated_at": utc_now_iso(),
        "results": results or [],
        "summary": summary or {},
        "errors": errors or [],
    }


def compile_patterns(patterns, use_regex=False):
    compiled = []
    for pat in patterns:
        if use_regex:
            compiled.append((pat, re.compile(pat)))
        else:
            compiled.append((pat, pat))
    return compiled


def scan_file(filepath, compiled_patterns, use_regex=False):
    """Scan a single file for pattern matches.

    Returns:
        tuple[list[dict], list[dict]]: hits, errors
    """
    hits = []
    errors = []
    try:
        with open(filepath, 'r', errors='replace') as f:
            for line_no, line in enumerate(f, 1):
                for original, matcher in compiled_patterns:
                    matched = bool(matcher.search(line)) if use_regex else original in line
                    if matched:
                        hits.append({
                            "line": line_no,
                            "text": line.rstrip(),
                            "pattern": original,
                            "match_type": "regex" if use_regex else "literal",
                        })
    except (OSError, UnicodeDecodeError) as exc:
        errors.append({
            "type": "file_read_error",
            "filepath": filepath,
            "message": str(exc),
        })
    return hits, errors


def scan_directory(directory, compiled_patterns, extensions, ignore_dirs, use_regex=False):
    """Walk directory and scan files.

    Returns:
        tuple[list[dict], list[dict]]: results, errors
    """
    results = []
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
            hits, file_errors = scan_file(fpath, compiled_patterns, use_regex)
            errors.extend(file_errors)
            if hits:
                rel = os.path.relpath(fpath, directory)
                for hit in hits:
                    results.append({
                        "filepath": rel,
                        **hit,
                    })
    return results, errors


def build_summary(results):
    by_pattern = defaultdict(lambda: {"files": set(), "hits": 0})
    by_file = defaultdict(int)
    for item in results:
        filepath = item["filepath"]
        pattern = item["pattern"]
        by_file[filepath] += 1
        by_pattern[pattern]["files"].add(filepath)
        by_pattern[pattern]["hits"] += 1

    return {
        "total_files": len(by_file),
        "total_hits": len(results),
        "by_pattern": {
            pat: {
                "files": sorted(data["files"]),
                "file_count": len(data["files"]),
                "hits": data["hits"],
            }
            for pat, data in sorted(by_pattern.items())
        },
    }


def print_results(payload):
    results = payload["results"]
    if payload["errors"] and not results:
        print(f"Error: {payload['errors'][0]['message']}", file=sys.stderr)
        return
    if not results:
        print("✅ No legacy residue found.")
        return

    summary = payload["summary"]
    print(f"⚠️  Found {summary['total_hits']} hit(s) across {summary['total_files']} file(s):\n")

    print("## Summary by pattern\n")
    print("| Pattern | Files | Hits |")
    print("|---------|-------|------|")
    for pat, data in summary["by_pattern"].items():
        print(f"| `{pat}` | {data['file_count']} | {data['hits']} |")

    print("\n## Detail\n")
    grouped = defaultdict(list)
    for item in results:
        grouped[item["filepath"]].append(item)

    for filepath in sorted(grouped):
        print(f"### {filepath}")
        for hit in grouped[filepath]:
            display = hit["text"][:120] + "..." if len(hit["text"]) > 120 else hit["text"]
            print(f"  L{hit['line']}: {display}  ← `{hit['pattern']}`")
        print()

    if payload["errors"]:
        print("## Non-fatal errors\n")
        for err in payload["errors"]:
            print(f"- `{err.get('filepath', 'unknown')}`: {err['message']}")


def main():
    parser = argparse.ArgumentParser(
        description="Scan for legacy name/path/status residue in a codebase."
    )
    parser.add_argument("directory", help="Root directory to scan")
    parser.add_argument("patterns", nargs="+", help="Patterns to search for")
    parser.add_argument("--ext", nargs="*", default=None,
                        help="File extensions to include (e.g., .py .md)")
    parser.add_argument("--ignore-dir", nargs="*", default=None,
                        help="Directory names to skip")
    parser.add_argument("--regex", action="store_true",
                        help="Treat patterns as regular expressions")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON instead of markdown")

    args = parser.parse_args()

    extensions = set(args.ext) if args.ext else DEFAULT_EXTENSIONS
    ignore_dirs = set(args.ignore_dir) if args.ignore_dir else DEFAULT_IGNORE_DIRS

    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a directory", file=sys.stderr)
        sys.exit(1)

    try:
        compiled_patterns = compile_patterns(args.patterns, args.regex)
    except re.error as exc:
        payload = build_payload(
            args.directory,
            results=[],
            summary={"total_files": 0, "total_hits": 0, "by_pattern": {}},
            errors=[{
                "type": "invalid_regex",
                "message": f"Invalid regular expression: {exc}",
            }],
        )
        if args.json:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            print(payload["errors"][0]["message"], file=sys.stderr)
        sys.exit(2)

    results, errors = scan_directory(args.directory, compiled_patterns, extensions, ignore_dirs, args.regex)
    payload = build_payload(args.directory, results=results, summary=build_summary(results), errors=errors)

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print_results(payload)

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()

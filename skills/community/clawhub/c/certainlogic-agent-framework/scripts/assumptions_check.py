#!/usr/bin/env python3
"""
Assumptions Check — pre-delivery fact verification gate.

Scans a file for unverified claims, wrong entity names, broken paths,
and suspicious patterns before delivering to the principal.

Usage:
    python3 assumptions_check.py <file>
    python3 assumptions_check.py <file1> <file2> ...
"""
import re
import sys
from pathlib import Path


# Patterns that signal unverified claims or risky language
ASSUMPTION_PATTERNS = [
    (r'\b(I think|I believe|I assume|must be|probably|likely|presumably)\b',
     "Unverified claim — phrase suggests assumption, not fact"),
    (r'\b(should be|should work|should handle)\b',
     "Unverified expectation — 'should' without evidence"),
    (r'\bDelaware\b',
     "Entity jurisdiction check — verify correct state"),
    (r'\b(always|never|everyone|nobody|all|none)\b',
     "Absolute claim — verify scope"),
    (r'\.\./\.\./|\.\./\.\./\.\./',
     "Suspicious relative path — verify it resolves correctly"),
    (r'`[^`]+`\s*(doesn\'t exist|not found|missing)',
     "Referenced file or path may be broken"),
]


def check_file(path):
    """Check a single file for assumption red flags."""
    path = Path(path)
    if not path.exists():
        return [f"File not found: {path}"]

    text = path.read_text()
    issues = []

    for pattern, message in ASSUMPTION_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            line_num = text[:match.start()].count("\n") + 1
            ctx_start = max(0, match.start() - 40)
            ctx_end = min(len(text), match.end() + 40)
            context = text[ctx_start:ctx_end].replace("\n", " ").strip()
            issues.append(f"  Line {line_num}: {message}\n    → ...{context}...")

    return issues


def main():
    files = sys.argv[1:]
    if not files:
        print("Usage: python3 assumptions_check.py <file> [file...]")
        sys.exit(1)

    all_issues = []
    for f in files:
        issues = check_file(f)
        if issues:
            print(f"\n{'='*60}")
            print(f"ASSUMPTION CHECK — {len(issues)} issue(s) in '{f}'")
            print(f"{'='*60}")
            for i in issues:
                print(i)
            all_issues.extend(issues)

    if all_issues:
        print(f"\n⚠️  {len(all_issues)} total issues found. Fix before delivering.")
        sys.exit(1)
    else:
        for f in files:
            print(f"ASSUMPTIONS_CHECK ✓ '{f}' — clean")
        sys.exit(0)


if __name__ == "__main__":
    main()
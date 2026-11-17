#!/usr/bin/env python3
"""Check that a slimmed instruction file is a verbatim subset of the original.

Usage: subset_check.py original.md slim.md

A line counts as a pointer (exempt) when it starts with '>' or matches a
"see/refer/read ... .md" shape. Everything else must exist verbatim.
Exit code 1 when any non-pointer line is missing.
"""
import re
import sys

POINTER = re.compile(r"^\s*>|(?:\bsee\b|\brefer\b|\bread\b|详见|参见|见|读)\b.*\.md", re.I)


def lines_of(path):
    return [l.rstrip() for l in open(path, encoding="utf-8").read().split("\n")]


def main(orig, slim):
    base = lines_of(orig)
    base_set = set(l for l in base if l.strip())
    upd = lines_of(slim)
    missing, pointers, checked = [], 0, 0
    for i, l in enumerate(upd, 1):
        s = l.strip()
        if not s:
            continue
        if POINTER.search(l):
            pointers += 1
            continue
        checked += 1
        if l not in base_set:
            missing.append((i, s[:120]))
    out = {
        "original": orig,
        "slim": slim,
        "non_pointer_lines_checked": checked,
        "pointer_lines": pointers,
        "missing": len(missing),
        "missing_samples": missing[:10],
        "verdict": "PASS" if not missing else "FAIL",
    }
    import json
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if not missing else 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1], sys.argv[2]))

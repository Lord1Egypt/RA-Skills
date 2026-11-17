#!/usr/bin/env python3
"""Scan files for command-guard bypass forms. Read-only.

Usage: bypass_scan.py FILE [FILE...]
"""
import json
import re
import sys

BINS = r"(rm|mv|chmod|chown|dd|sudo|launchctl|osascript|kill|diskutil)"
PATTERNS = [
    ("absolute-path", re.compile(r"(?:^|[\s'\"=])/(?:usr/)?(?:local/)?s?bin/" + BINS + r"\b")),
    ("shell-nested", re.compile(r"\b(?:bash|sh|zsh)\s+-c\b")),
    ("interpreter", re.compile(r"\bpython[0-9.]*\s+-c\b|\bnode\s+-e\b|\bperl\s+-e\b")),
    ("pipe-to-shell", re.compile(r"\b(?:curl|wget)\b[^|\n]*\|\s*(?:bash|sh|zsh)\b")),
    ("eval", re.compile(r"\beval\b\s+[\(\"'$]")),
]


def scan(path):
    hits = []
    try:
        lines = open(path, encoding="utf-8", errors="replace").read().split("\n")
    except Exception as e:
        return [{"file": path, "error": str(e)}]
    for i, line in enumerate(lines, 1):
        for name, pat in PATTERNS:
            if pat.search(line):
                hits.append({"file": path, "line": i, "pattern": name, "snippet": line.strip()[:160]})
    return hits


def main(paths):
    out = []
    for p in paths:
        out.extend(scan(p))
    print(json.dumps({
        "files": paths,
        "hits": len(out),
        "results": out,
        "note": "Scanner only. A hit is a review item, not proof of exploitability.",
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1:]))

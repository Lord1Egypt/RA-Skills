#!/usr/bin/env python3
"""Count conditional markers in instruction files with one fixed pattern set.

Usage:
    cond_count.py A.md B.md
    cond_count.py --sections A.md B.md

Compare versions only with the same script and the same patterns.
Character counts use UTF-8 decoding, never byte counts.
"""
import json
import re
import sys

PATTERNS = {
    "must": r"必须|务必|must|shall|required|never|do not|don't",
    "prohibition": r"禁止|不得|不准|不许|绝不|严禁|勿用|请勿|不可|不应|不能|不要|forbidden|prohibited",
    "conditional": r"当[^。\n]{0,30}?时|如果|若(?=[^。\n]{0,20}[，,])|\bwhen\b|\bif\b",
    "threshold": r"[≥≤]|超过|至少|最多|不少于|不超过|at least|at most|more than|less than|>=|<=|<|>",
    "verdict": r"即违规|视为|才算|方可|才能|counts as|treated as|considered",
}


def counts_of(text):
    return {name: len(re.findall(pat, text, re.I)) for name, pat in PATTERNS.items()}


def scan(path):
    text = open(path, encoding="utf-8").read()
    c = counts_of(text)
    return {
        "file": path,
        "lines": len(text.split("\n")),
        "chars": len(text),
        "counts": c,
        "total": sum(c.values()),
    }


def sections(path):
    text = open(path, encoding="utf-8").read()
    lines = text.split("\n")
    heads = [i for i, l in enumerate(lines) if l.startswith("#")]
    print(path)
    if not heads:
        r = scan(path)
        print("   (no headings) chars=%d total=%d" % (r["chars"], r["total"]))
        return
    start = 0
    if heads[0] > 0:
        heads = [0] + heads
    for k, i in enumerate(heads):
        j = heads[k + 1] if k + 1 < len(heads) else len(lines)
        seg = "\n".join(lines[i:j])
        c = counts_of(seg)
        label = lines[i][:44] if i < len(lines) else ""
        print("   %-46s L%d-%d chars=%5d total=%d %s" % (label, i + 1, j, len(seg), sum(c.values()), json.dumps(c)))


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    if argv[0] in ("--sections", "-s"):
        for p in argv[1:]:
            sections(p)
        return 0
    for p in argv:
        r = scan(p)
        print(json.dumps(r, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

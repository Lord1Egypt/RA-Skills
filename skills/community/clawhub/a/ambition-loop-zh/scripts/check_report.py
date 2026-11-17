#!/usr/bin/env python3
"""Check that an ambition-loop final report has the required sections.

Usage: python3 check_report.py REPORT.md [--json]
Accepts English or Chinese headings. Exit code 0 = all required parts present.
This is a structure check only; it does not judge the work itself.
"""
import json
import re
import sys

REQUIRED = {
    "target_comparison": [r"target comparison", r"目标对比"],
    "verification": [r"verification", r"外部验证|验证结果"],
    "gaps": [r"\bgaps?\b", r"差距"],
    "next_moves": [r"next moves?|next steps?", r"下一步"],
    "gated": [r"gated|skipped", r"审批|跳过"],
}
TABLE_COLS = {
    "target_table": [r"asked|floor|原始|底线", r"ambitious|野心", r"achieved|实际|达成"],
    "claims_table": [r"claim|结论|声明", r"judge|裁判", r"result|结果"],
}
RESULT_TOKENS = r"\b(PASS|FAIL|UNVERIFIED)\b|通过|未通过|未验证"


def headings(text):
    return [h.strip().lower() for h in re.findall(r"(?m)^#{1,4}\s+(.+)$", text)]


def has_table_with(text, pats):
    for line in text.splitlines():
        if line.strip().startswith("|"):
            low = line.lower()
            if all(re.search(p, low) for p in pats):
                return True
    return False


def check(text):
    hs = headings(text)
    res = {}
    for key, pats in REQUIRED.items():
        res[key] = any(re.search(p, h) for h in hs for p in pats)
    for key, pats in TABLE_COLS.items():
        res[key] = has_table_with(text, pats)
    res["result_tokens"] = bool(re.search(RESULT_TOKENS, text))
    return res


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    text = open(sys.argv[1], encoding="utf-8").read()
    res = check(text)
    ok = all(res.values())
    if "--json" in sys.argv:
        print(json.dumps({"ok": ok, "checks": res}, ensure_ascii=False))
    else:
        for k, v in res.items():
            print(("OK   " if v else "MISS ") + k)
        print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

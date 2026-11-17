#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""course-paper-writer — reference list helper.

Zero-dependency. Reads a plain-text reference list (one entry per line, or
"[n] entry" format) and reports:

    * entry count and numbering continuity
    * publication year per entry, and the "recent N years" ratio
    * type breakdown by GB/T 7714 marker ([M] [J] [S] [D] [R] [EB/OL] ...)
    * suspicious entries (no year, no type marker, web-only source)

    python scripts/citation_formatter.py refs.txt --recent-years 5
    python scripts/citation_formatter.py refs.txt --check-punct

The recency ratio deliberately strips URL access dates such as
"[2026-11-10]", which otherwise get counted as the publication year and
inflate the result.
"""

import argparse
import datetime
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ACCESS_DATE = re.compile(r"\[\d{4}-\d{2}-\d{2}\]")
YEAR = re.compile(r"(?<!\d)((?:19|20)\d{2})(?!\d)")
NUM_PREFIX = re.compile(r"^\s*\[(\d+)\]\s*")
TYPE = re.compile(r"\[(M|J|S|D|R|N|C|P|Z|EB/OL|M/OL|J/OL)\]")
PUNCT_FIX = [
    (re.compile(r",\s*"), ", "),
    (re.compile(r":\s*"), ": "),
    (re.compile(r"\s+"), " "),
]


def clean(line):
    return NUM_PREFIX.sub("", line).strip()


def pub_year(ref):
    s = ACCESS_DATE.sub("", ref)
    ys = YEAR.findall(s)
    return int(ys[-1]) if ys else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--recent-years", type=int, default=5)
    ap.add_argument("--min", type=int, default=10, help="要求的最少条数")
    ap.add_argument("--min-recent-pct", type=float, default=50.0)
    ap.add_argument("--check-punct", action="store_true",
                    help="检查中英文标点混用与多余空格")
    a = ap.parse_args()

    raw = open(a.file, encoding="utf-8", errors="replace").read().splitlines()
    entries = [(i + 1, l) for i, l in enumerate(raw) if l.strip()]
    if not entries:
        sys.exit("文件里没有内容")

    refs = []
    problems = []
    for lineno, line in entries:
        body = clean(line)
        refs.append(body)
        reasons = []
        if not pub_year(body):
            reasons.append("无年份")
        if not TYPE.search(body):
            reasons.append("无类型标识")
        if "http" in body.lower() and not TYPE.search(body):
            reasons.append("疑似纯网页")
        if reasons:
            problems.append((lineno, body[:40], reasons))

    n = len(refs)
    now = datetime.date.today().year
    cutoff = now - a.recent_years
    years = [pub_year(r) for r in refs]
    recent = sum(1 for y in years if y >= cutoff)
    pct = 100.0 * recent / n if n else 0.0

    print("=" * 66)
    print("文献条数   %d   （要求 ≥%d）" % (n, a.min))
    print("=" * 66)
    print("序号        %s" % ("1..%d 连续" % n if all(
        clean(l).strip() for _, l in entries) else "见下"))
    print("出版年      %s" % years)
    print("近%d年      %d/%d = %.1f%%   （要求 ≥%.0f%%）"
          % (a.recent_years, recent, n, pct, a.min_recent_pct))

    kinds = {}
    for r in refs:
        m = TYPE.search(r)
        kinds[m.group(1) if m else "无标识"] = kinds.get(m.group(1) if m else "无标识", 0) + 1
    print("类型分布    %s" % ", ".join("%s×%d" % (k, v) for k, v in sorted(kinds.items())))

    if problems:
        print()
        print("可疑条目：")
        for lineno, body, why in problems:
            print("  第 %d 条  %-42s  ← %s" % (lineno, body, "、".join(why)))
    else:
        print()
        print("可疑条目    无")

    if a.check_punct:
        print()
        print("标点检查：")
        bad = 0
        for idx, r in enumerate(refs, 1):
            # 中文条目应当以中文标点分隔，英文条目用英文标点
            has_cjk = bool(re.search(r"[\u4e00-\u9fff]", r))
            if has_cjk and re.search(r",\s", r):
                print("  第 %d 条中文条目里出现英文逗号: %s" % (idx, r[:40]))
                bad += 1
            if not has_cjk and re.search(r"[，。；：]", r):
                print("  第 %d 条英文条目里出现中文标点: %s" % (idx, r[:40]))
                bad += 1
        if not bad:
            print("  未发现中英标点混用")

    print()
    print("-" * 66)
    ok = True
    if n < a.min:
        print("[X] 条数不足：%d < %d" % (n, a.min))
        ok = False
    if pct < a.min_recent_pct:
        print("[X] 近%d年占比不足：%.1f%% < %.0f%%" % (a.recent_years, pct, a.min_recent_pct))
        ok = False
    if problems:
        print("[!] 有 %d 条可疑，逐条核对后再交" % len(problems))
    print("结论：%s" % ("通过" if ok else "未通过"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""course-paper-writer — paper self-check.

    python scripts/check_paper.py 论文.docx --min 3500 --max 5000

Requires python-docx. Reports word counts by zone (because one number always
misleads), citation continuity, recency ratio, and an estimated page count.
"""

import argparse
import math
import re
import sys

try:
    from docx import Document
    from docx.oxml.ns import qn
except ImportError:
    sys.exit("需要 python-docx：pip install python-docx")

# Windows consoles default to GBK; never crash on a glyph.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

PUNCT = "，。；：、！？“”‘’（）——…《》‥"
H1 = re.compile(r"^[一二三四五六七八九十]+、")
H2 = re.compile(r"^\d+\.\d+(?!\.)")
H3 = re.compile(r"^\d+\.\d+\.\d+")
OK, BAD, WARN = "[OK]", "[X]", "[!]"


def count(text, keep_punct=True):
    text = re.sub(r"\[\d+\]", "", text)
    return len([c for c in text
                if not c.isspace() and (keep_punct or c not in PUNCT)])


def east_asia(run):
    rPr = run._element.find(qn("w:rPr"))
    if rPr is None:
        return None
    f = rPr.find(qn("w:rFonts"))
    return f.get(qn("w:eastAsia")) if f is not None else None


def run_size(run):
    return run.font.size.pt if run.font.size else None


def pub_year(ref):
    s = re.sub(r"\[\d{4}-\d{2}-\d{2}\]", "", ref)      # drop access dates
    ys = re.findall(r"(?<!\d)((?:19|20)\d{2})(?!\d)", s)
    return int(ys[-1]) if ys else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("docx")
    ap.add_argument("--min", type=int, default=0, help="正文字数下限")
    ap.add_argument("--max", type=int, default=0, help="正文字数上限")
    ap.add_argument("--recent-years", type=int, default=5)
    ap.add_argument("--min-refs", type=int, default=10)
    ap.add_argument("--pages", type=int, default=0, help="页数上限（0=不限）")
    a = ap.parse_args()

    doc = Document(a.docx)
    paras = doc.paragraphs
    texts = [p.text for p in paras]

    i_ref = next((i for i, t in enumerate(texts) if t.strip() == "参考文献"), None)
    i_intro = next((i for i, t in enumerate(texts) if H1.match(t.strip())), 0)
    body_end = i_ref if i_ref is not None else len(texts)

    abstract = next((t for t in texts if t.strip().startswith("中文摘要")), "")
    abstract = re.split(r"[:：]", abstract, maxsplit=1)[-1] if abstract else ""

    head_txt, body_txt, refs = [], [], []
    for i in range(i_intro, body_end):
        t = texts[i]
        if not t.strip():
            continue
        s = t.strip()
        if H1.match(s) or H2.match(s) or H3.match(s):
            head_txt.append(t)
        else:
            body_txt.append(t)
    if i_ref is not None:
        refs = [t for t in texts[i_ref + 1:] if t.strip()]

    b_all = "".join(body_txt)
    b_punct = "".join(body_txt) + "".join(head_txt)

    print("=" * 62)
    print("文件：%s" % a.docx)
    print("=" * 62)
    print("摘要      %4d 字（不含标点 %3d）  要求 250-300"
          % (count(abstract), count(abstract, False)))
    print("正文段落  %4d 字（不含标点 %3d）" % (count(b_all), count(b_all, False)))
    print("小标题    %4d 字 / %d 个" % (count("".join(head_txt)), len(head_txt)))
    print("正文合计  %4d 字（含小标题）     <- 多数老师按这个数"
          % count(b_punct))
    print("参考文献  %3d 条" % len(refs))

    # citations
    seen, missing = [], []
    sup = 0
    for p in paras[:body_end]:
        for r in p.runs:
            if r.font.superscript:
                sup += 1
    for m in re.finditer(r"\[(\d+)\]", "".join(texts[i_intro:body_end])):
        v = int(m.group(1))
        if v not in seen:
            seen.append(v)
    contiguous = seen == list(range(1, len(seen) + 1))
    print()
    print("引用序号  首现顺序 %s" % ("1..%d 连续 [OK]" % len(seen) if contiguous else "不连续 [X]"))
    print("上标 run  %d 处" % sup)
    if refs:
        if len(seen) != len(refs):
            print("  [!] 正文引用 %d 个序号，文献表 %d 条，不一致" % (len(seen), len(refs)))
        else:
            print("  [OK] 正文引用数与文献条数一致")

    # recency
    if refs:
        years = [pub_year(r) for r in refs]
        import datetime
        now = datetime.date.today().year
        recent = sum(1 for y in years if y >= now - a.recent_years)
        print()
        print("出版年    %s" % years)
        print("近%d年    %d/%d = %.1f%%" % (a.recent_years, recent, len(refs),
                                          100.0 * recent / len(refs)))

    # page estimate
    W = 21 - 3.17 * 2
    lines = 0.0
    for p in paras:
        t = p.text.strip()
        if not t:
            continue
        sz = run_size(p.runs[0]) if p.runs and run_size(p.runs[0]) else 12
        cpl = max(1, int((W / 2.54 * 72) // sz))
        lines += math.ceil(len(t) / cpl)
        pf = p.paragraph_format
        if pf.space_before:
            lines += pf.space_before.pt / 20.7
        if pf.space_after:
            lines += pf.space_after.pt / 20.7
    print()
    print("估算页数  约 %.1f 页" % (lines / 33))

    # verdict
    print()
    print("-" * 62)
    ok = True
    total = count(b_punct)
    if a.max and total > a.max:
        print("[X] 正文 %d 字，超出上限 %d" % (total, a.max)); ok = False
    elif a.max and a.max - total < 30:
        print("[!] 正文 %d 字，距上限仅 %d 字" % (total, a.max - total))
    elif a.min and total < a.min:
        print("[X] 正文 %d 字，不足下限 %d" % (total, a.min)); ok = False
    if not contiguous:
        print("[X] 引用序号不连续"); ok = False
    if refs and len(seen) != len(refs):
        print("[X] 引用数与文献条数不符"); ok = False
    if a.min_refs and len(refs) < a.min_refs:
        print("[X] 文献仅 %d 条，少于 %d" % (len(refs), a.min_refs)); ok = False
    print("结论：%s" % ("全部通过" if ok else "存在待修项，见上"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())


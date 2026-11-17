#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_freshness.py — 时效性校验（文章交付前的硬门禁）

查三件事，因为这三件事打印出来就是事故：
  1. FUTURE  事件日期 > 本期出版日  → 把还没发生的事写成已发生
  2. STALE   事件日期早于收录窗口   → 旧闻充新刊
  3. STATED  正文里的相对时间词     → 「将于/拟于/尚未/预计」付印当天必须复核

日期从两处取，优先级：
  unit.meta / block.meta 里写的 "2026.04.10"、"2026.08"
  找不到则退到正文首句里的 "2026 年 4 月 10 日"

用法：
  python check_freshness.py --content content.json --issue-date 2026-09-17
  python check_freshness.py --content content.json --issue-date 2026-09-17 --window 5 --json

命令里的 `python`：Windows 用 `python`，macOS/Linux 用 `python3`。
"""
import argparse
import datetime
import io
import json
import os
import re
import sys

# 相对时间词：出现即说明这条有「未定」成分，付印前必须重查
STATED = (
    "将于", "拟于", "预计", "计划", "有望", "尚未", "还没", "仍在",
    "力争", "打算", "下一步", "待公布", "或于", "明年",
)

DATE_PATTERNS = (
    # 2026.04.10 / 2026-04-10 / 2026/04/10
    (re.compile(r"(20\d\d)[.\-/](\d{1,2})(?:[.\-/](\d{1,2}))?"),
     lambda m: (int(m.group(1)), int(m.group(2)), int(m.group(3) or 1))),
    # 2026 年 4 月 10 日
    (re.compile(r"(20\d\d)\s*年\s*(\d{1,2})\s*月(?:\s*(\d{1,2})\s*日)?"),
     lambda m: (int(m.group(1)), int(m.group(2)), int(m.group(3) or 1))),
)

# 只看动作日期，避免把文号里的年份当事件日
META_STRIP = re.compile(r"[（(][^）)]*[）)]")


def first_date(text):
    """取文本里第一个可解析日期；返回 (y, m, d) 或 None。"""
    t = META_STRIP.sub(" ", str(text or ""))
    best = None
    for pat, conv in DATE_PATTERNS:
        for m in pat.finditer(t):
            try:
                cand = conv(m)
            except Exception:
                continue
            if (1900 < cand[0] < 2100) and 1 <= cand[1] <= 12:
                if best is None or cand < best:
                    best = cand
    return best


def to_date(t):
    return datetime.date(*t) if t else None


def months_between(a, b):
    """a、b 相差多少个月（a 早于 b 为正）。"""
    return (b.year - a.year) * 12 + (b.month - a.month)


def iter_items(content):
    """yield (定位, 标题, 日期串, 正文, 类型)"""
    for pi, page in enumerate(content.get("pages", [])):
        for ui, u in enumerate(page.get("units", []) or []):
            yield ("P%02d unit[%d]" % (pi + 1, ui),
                   u.get("title", ""), u.get("meta", ""),
                   u.get("body", ""), "unit")
        blocks = page.get("blocks", []) or []
        head = ""
        for bi, b in enumerate(blocks):
            if b.get("type") in ("h1", "h2", "title") and b.get("text"):
                head = b["text"]
            if b.get("type") in ("p", "li", "quote", "note", "abstract"):
                yield ("P%02d block[%d]" % (pi + 1, bi),
                       head, b.get("meta", ""), b.get("text", ""), "block")


def check(content, issue_date, window):
    issues = []
    seen_events = []

    # 例外清单：写在 content.json 的 meta.freshness_exceptions 里，
    # 形如 [{"match":"标题前缀","reason":"为什么它不是旧闻"}]
    exceptions = (content.get("meta") or {}).get("freshness_exceptions") or []
    exc_idx = [(e.get("match", ""), e.get("reason", "")) for e in exceptions]

    def explained(t):
        # 用子串包含而非前缀：标题里的关键词常出现在中间（如「零关税」「mBridge」），
        # startswith 会让这些例外永远匹配不上。
        for m, _r in exc_idx:
            if m and m in str(t or ""):
                return True
        return False

    issue_date0 = issue_date
    suppressed = 0
    for loc, title, meta, body, kind in iter_items(content):
        text = body or ""
        raw = "%s %s" % (meta or "", text)

        md = first_date(meta) if meta else None
        bd = first_date(text[:60]) if text else None
        ev = md or bd

        if ev:
            d = to_date(ev)
            # 收录区间只看「法规动态」；深度文章引用历史日期是正常的，进来会污染区间
            if kind == "unit":
                seen_events.append((loc, d))
            age = (issue_date - d).days
            gap = months_between(d, issue_date)
            if d > issue_date:
                # FUTURE 同样要走例外：「已公布未生效」的预告条目、
                # 以及征求意见截止日这类程序性期限，都是期刊的正常内容，
                # 前提是正文已标注状态。此前只让 STALE 走例外，
                # 导致这类条目无论如何都报 ERROR。
                if explained(title):
                    suppressed += 1
                    continue
                issues.append({
                    "level": "ERROR", "rule": "FUTURE", "loc": loc,
                    "title": title[:40], "date": d.isoformat(),
                    "msg": "事件日期在本期出版日(%s)之后 %d 天——把未发生写成了已发生"
                           % (issue_date.isoformat(), age * -1),
                })
            elif gap > window and kind == "unit":
                # 只有「法规动态」条目才查新旧；深度文章本来就是回顾性叙述，
                # 拿里面的历史日期判 STALE 属于误报。
                if explained(title):
                    suppressed += 1
                    continue
                issues.append({
                    "level": "WARN", "rule": "STALE", "loc": loc,
                    "title": title[:40], "date": d.isoformat(),
                    "msg": "早于收录窗口(%d 个月)——距今 %d 个月，应确认是否仍属本期动态"
                           % (window, gap),
                })

        for w in STATED:
            if w in raw:
                seg = raw[max(0, raw.find(w) - 26): raw.find(w) + 30]
                issues.append({
                    "level": "INFO", "rule": "STATED", "loc": loc,
                    "title": title[:40], "date": "",
                    "msg": "含「%s」——付印当天须复核该状态是否已变化 | …%s…" % (w, seg),
                })
                break

    if seen_events:
        ds = sorted(d for _, d in seen_events)
        span = "收录区间 %s → %s" % (ds[0].isoformat(), ds[-1].isoformat())
    else:
        span = "未解析到任何事件日期"
    return issues, span, suppressed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--content", required=True)
    ap.add_argument("--issue-date", required=True,
                    help="本期出版日 YYYY-MM-DD；也可用 today")
    ap.add_argument("--window", type=int, default=6,
                    help="收录窗口（月），超出判 STALE，默认 6")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true",
                    help="存在 ERROR 时退出码 1，供 CI / 门禁使用")
    a = ap.parse_args()

    if a.issue_date == "today":
        issue_date = datetime.date.today()
    else:
        issue_date = datetime.date(*[int(x) for x in a.issue_date.split("-")])

    with io.open(a.content, "r", encoding="utf-8") as f:
        content = json.load(f)

    issues, span, suppressed = check(content, issue_date, a.window)

    if a.json:
        print(json.dumps({"issue_date": issue_date.isoformat(),
                          "window_months": a.window, "span": span,
                          "issues": issues}, ensure_ascii=False, indent=1))
    else:
        order = {"ERROR": 0, "WARN": 1, "INFO": 2}
        issues.sort(key=lambda x: (order.get(x["level"], 9), x["rule"], x["loc"]))
        cnt = {}
        for i in issues:
            cnt[i["level"]] = cnt.get(i["level"], 0) + 1
        if suppressed:
            print("  豁免 %d 条（meta.freshness_exceptions 已载明理由）" % suppressed)
        print("时效校验  %s  %s" % (a.content, span))
        print("  出版日 %s · 窗口 %d 个月 · 共 %d 条定位"
              % (issue_date.isoformat(), a.window,
                 sum(1 for _ in iter_items(content))))
        print("  ERROR %d / WARN %d / INFO %d"
              % (cnt.get("ERROR", 0), cnt.get("WARN", 0), cnt.get("INFO", 0)))
        print()
        for i in issues:
            print("  [%s] %-6s %-14s %s" % (i["level"], i["rule"], i["loc"], i["msg"]))
            if i["title"]:
                print("          └ %s" % i["title"])
        if not issues:
            print("  无时效问题。")

    if a.strict and any(i["level"] == "ERROR" for i in issues):
        sys.exit(1)


if __name__ == "__main__":
    main()

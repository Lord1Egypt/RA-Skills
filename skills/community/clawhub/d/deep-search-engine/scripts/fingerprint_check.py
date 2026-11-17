#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""三要素全文验证：标题含主体 + 发布日期在窗口内 + 正文含指纹。

Hard Rule 2 的执行器：无三要素证据不得写「已发布」。改标题版（标题不含主体但
指纹命中）单独标注，计入分发。

用法：
  python fingerprint_check.py --url "https://caijing.chinadaily.com.cn/a/202608/24/WSxxxx.html" \
      --subject "示例主体" --window 2026-08-01:2026-08-25 \
      --fp "上下文基础设施" --fp "test-time compute" --fp "2万个集群"

输出：JSON verdict 字段：
  PASS       — 三要素全中（标题含主体 + 日期窗口命中 + ≥1 指纹命中）
  RETITLED   — 标题不含主体但 ≥1 指纹命中（改标题版转载）
  UNCERTAIN  — 页面无法完整抓取或仅部分命中（进 pending_queue，不写已发布）
  FAIL       — 指纹全部 MISS（与目标无关，剔除）
"""
import argparse
import json
import re
import sys
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

DATE_PATTERNS = [
    # HTML meta 优先：og:release_date / article:published_time / itemprop datePublished
    r'property="og:release_date"\s+content="(\d{4}-\d{2}-\d{2})',
    r'property="article:published_time"\s+content="(\d{4}-\d{2}-\d{2})',
    r'itemprop="datePublished"\s+content="(\d{4}-\d{2}-\d{2})',
    r'"(?:pubDate|publish_time|publishDate|datePublished)"\s*[:=]\s*"(\d{4}-\d{2}-\d{2})',
    # 正文日期：2026年8月21日 / 2026-08-21 / 2026.8.21
    r'(\d{4})年(\d{1,2})月(\d{1,2})日',
    r'(\d{4})-(\d{2})-(\d{2})',
    r'(\d{4})\.(\d{1,2})\.(\d{1,2})',
]


def fetch(url: str, timeout: int = 30):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Accept": "text/html,application/xhtml+xml,*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.geturl(), r.read().decode("utf-8", "ignore")


def extract_title(html: str) -> str:
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
    if not m:
        return ""
    t = re.sub(r"<[^>]+>", "", m.group(1))
    return re.sub(r"\s+", " ", t).strip()


def extract_dates(html: str) -> list[str]:
    found = []
    for pat in DATE_PATTERNS:
        for m in re.finditer(pat, html):
            g = m.groups()
            if len(g) == 3:
                try:
                    found.append(f"{int(g[0]):04d}-{int(g[1]):02d}-{int(g[2]):02d}")
                except ValueError:
                    pass
            elif len(g) == 1:
                found.append(g[0])
    return sorted(set(found))


def in_window(dates: list[str], start: str, end: str) -> str | None:
    for d in dates:
        if start <= d <= end:
            return d
    return None


def strip_tags(html: str) -> str:
    html = re.sub(r"<script.*?</script>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<style.*?</style>", " ", html, flags=re.S | re.I)
    return re.sub(r"<[^>]+>", " ", html)


def main() -> int:
    ap = argparse.ArgumentParser(description="Three-element verification: title + date window + fingerprints")
    ap.add_argument("--url", required=True)
    ap.add_argument("--subject", required=True, help="主体名（应出现在标题中，如公司/产品名）")
    ap.add_argument("--window", help="日期窗口 起:止（YYYY-MM-DD:YYYY-MM-DD）")
    ap.add_argument("--fp", action="append", required=True,
                    help="正文指纹（独特长句/独有表述），可多次 --fp")
    a = ap.parse_args()

    try:
        final_url, html = fetch(a.url)
    except Exception as e:
        print(json.dumps({"url": a.url, "verdict": "UNCERTAIN",
                          "error": f"{type(e).__name__}: {e}",
                          "hint": "重试一次；仍失败换 WebFetch/curl 交叉验证；JS 渲染页换 WebFetch"},
                         ensure_ascii=False))
        return 1

    title = extract_title(html)
    body = strip_tags(html)
    dates = extract_dates(html)

    if len(body.strip()) < 200:
        print(json.dumps({"url": a.url, "final_url": final_url, "verdict": "UNCERTAIN",
                          "reason": "正文过短（疑 JS 渲染或拦截页），换 WebFetch 通道",
                          "title": title}, ensure_ascii=False))
        return 0

    fps = {fp: ("HIT" if fp in body or fp in html else "MISS") for fp in a.fp}
    hit_count = sum(1 for v in fps.values() if v == "HIT")

    subject_in_title = a.subject in title or a.subject.lower() in title.lower()

    start = end = None
    if a.window:
        start, end = a.window.split(":")
    date_hit = in_window(dates, start, end) if (start and end) else (dates[0] if dates else None)

    if hit_count == 0:
        verdict = "FAIL"
    elif subject_in_title and (date_hit or not a.window) and hit_count >= 1:
        verdict = "PASS"
    elif hit_count >= 1 and not subject_in_title:
        verdict = "RETITLED"
    else:
        verdict = "UNCERTAIN"

    result = {
        "url": a.url, "final_url": final_url, "verdict": verdict,
        "title": title, "subject": a.subject, "subject_in_title": subject_in_title,
        "dates_found": dates[:8], "date_hit": date_hit,
        "fingerprints": fps, "fingerprint_hits": f"{hit_count}/{len(a.fp)}",
    }
    print(json.dumps(result, ensure_ascii=False, indent=1))
    return 0 if verdict in ("PASS", "RETITLED") else 1


if __name__ == "__main__":
    sys.exit(main())

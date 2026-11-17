#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Google News RSS 查询（含 site: 域名定向）。

用法：
  python gnews_query.py --query "企业搜索 上下文基础设施"
  python gnews_query.py --query "企业搜索" --site chinadaily.com.cn --when 7d
  python gnews_query.py --query "..." --site csdn.net --when 30d --out result.json

输出：JSON {url, count, items: [{title, link, pubDate, source}]}
注意：Google News 对部分中文通稿站不索引（见 references/channel-matrix.md 盲区表），
site: 查询返回 0 条不代表该站未发布——必须走百度通道（baidu_search.py）补验。
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def build_url(query: str, site: str | None, when: str | None) -> str:
    q = query
    if site:
        q = f"{q} site:{site}"
    if when:
        q = f"{q} when:{when}"
    return ("https://news.google.com/rss/search?q="
            + urllib.parse.quote(q)
            + "&hl=zh-CN&gl=CN&ceid=CN:zh-Hans")


def fetch(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "ignore")


def parse_items(xml_text: str) -> list[dict]:
    root = ET.fromstring(xml_text)
    items = []
    for item in root.iter("item"):
        items.append({
            "title": (item.findtext("title") or "").strip(),
            "link": (item.findtext("link") or "").strip(),
            "pubDate": (item.findtext("pubDate") or "").strip(),
            "source": (item.findtext("source") or "").strip(),
        })
    return items


def main() -> int:
    ap = argparse.ArgumentParser(description="Google News RSS query (optional site: filter)")
    ap.add_argument("--query", required=True, help="查询词（关键词/独特长句）")
    ap.add_argument("--site", help="限定域名（site: 过滤）")
    ap.add_argument("--when", default="30d", help="时间窗，如 7d/30d（默认 30d）")
    ap.add_argument("--out", help="结果另存 JSON 文件路径")
    a = ap.parse_args()

    url = build_url(a.query, a.site, a.when)
    try:
        xml_text = fetch(url)
        items = parse_items(xml_text)
    except Exception as e:
        print(json.dumps({"url": url, "error": f"{type(e).__name__}: {e}",
                          "hint": "重试一次；连续失败换 curl 交叉验证"}, ensure_ascii=False))
        return 1

    result = {"url": url, "count": len(items), "items": items}
    out = json.dumps(result, ensure_ascii=False, indent=1)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(out)
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())

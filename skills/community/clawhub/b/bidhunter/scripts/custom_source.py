#!/usr/bin/env python3
"""
custom_source.py - Config-driven generic source loader (BidHunter v1.5, A5).

Lets users add any platform without writing a bash adapter. Define sources in
sources.json (see sources.example.json). Supports json / rss / html modes.

Usage:
  python3 custom_source.py <sources.json> [source_name]
  Prints JSON lines: {"id","title","source","url","publish_time"}

Each source spec:
  {
    "name": "my_platform",
    "mode": "json",                       # json | rss | html
    "url": "https://x/list?date={DATE}", # {DATE} replaced with YYYY-MM-DD
    "headers": {"Authorization": "Bearer xxx"},   # optional
    "items_path": "data.list",           # json: dotted path to array
    "fields": {"id":"id","title":"title","url":"url","publish_time":"time"},
    "url_prefix": "https://x/detail?id=" # optional, prepended to id if url missing
  }
"""
import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"


def _get(url, headers):
    req = urllib.request.Request(url, headers={**{"User-Agent": UA}, **(headers or {})})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", "replace")


def _dig(obj, path):
    cur = obj
    for p in path.split("."):
        if isinstance(cur, dict) and p in cur:
            cur = cur[p]
        elif isinstance(cur, list) and p.isdigit():
            cur = cur[int(p)]
        else:
            return None
    return cur


def parse_json(spec, date_str):
    url = spec["url"].replace("{DATE}", date_str)
    raw = _get(url, spec.get("headers"))
    data = json.loads(raw)
    items = _dig(data, spec.get("items_path", "data.list")) or []
    if not isinstance(items, list):
        items = []
    out = []
    fmap = spec.get("fields", {})
    prefix = spec.get("url_prefix", "")
    for it in items:
        title = _dig(it, fmap.get("title", "title")) if fmap else it.get("title")
        if not title:
            continue
        uid = _dig(it, fmap.get("id", "id")) if fmap else it.get("id")
        u = _dig(it, fmap.get("url", "url")) if fmap else it.get("url")
        if not u and uid:
            u = prefix + str(uid)
        out.append({
            "id": str(uid or title)[:80],
            "title": str(title),
            "source": spec["name"],
            "url": u or "",
            "publish_time": str(_dig(it, fmap.get("publish_time", "publish_time")) or "")[:30],
        })
    return out


def parse_rss(spec, date_str):
    import xml.etree.ElementTree as ET
    url = spec["url"].replace("{DATE}", date_str)
    raw = _get(url, spec.get("headers"))
    root = ET.fromstring(raw)
    out = []
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link = item.findtext("link") or ""
        pub = item.findtext("pubDate") or ""
        if title:
            out.append({"id": link or title[:80], "title": title, "source": spec["name"],
                        "url": link, "publish_time": pub[:30]})
    return out


def parse_html(spec, date_str):
    import re
    url = spec["url"].replace("{DATE}", date_str)
    raw = _get(url, spec.get("headers"))
    # simple: find <a ...>title</a> pairs, capture title+maybe href
    out = []
    for m in re.finditer(r"<a[^>]+href=[\"']([^\"']+)[\"'][^>]*>([^<]{6,120})</a>", raw):
        href, title = m.group(1), m.group(2).strip()
        if any(k in title for k in ("招标", "采购", "投标", "竞谈", "询价")):
            out.append({"id": href[:80], "title": title, "source": spec["name"],
                        "url": href, "publish_time": ""})
    return out


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 custom_source.py <sources.json> [name]", file=sys.stderr)
        sys.exit(1)
    spec_file = sys.argv[1]
    only = sys.argv[2] if len(sys.argv) > 2 else None
    date_str = datetime.now().strftime("%Y-%m-%d")
    with open(spec_file, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    sources = cfg.get("sources", [])
    count = 0
    for spec in sources:
        if only and spec.get("name") != only:
            continue
        try:
            mode = spec.get("mode", "json")
            if mode == "json":
                items = parse_json(spec, date_str)
            elif mode == "rss":
                items = parse_rss(spec, date_str)
            elif mode == "html":
                items = parse_html(spec, date_str)
            else:
                items = []
            for it in items:
                print(json.dumps(it, ensure_ascii=False))
                count += 1
        except Exception as e:
            print(f"WARN: source {spec.get('name')} failed: {e}", file=sys.stderr)
    print(f"custom_source: emitted {count} items", file=sys.stderr)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
CN Hot Trends — 中文+全球热榜聚合器
一键获取百度、头条、V2EX、Hacker News、GitHub 热点数据

Usage:
  python3 fetch_trends.py [--sources baidu,toutiao,v2ex,hn,github] [--limit 10] [--format json|text|markdown] [--proxy http://127.0.0.1:7897]
"""

import json
import sys
import subprocess
import urllib.parse
import argparse
from datetime import datetime, timedelta


def curl_fetch(url, proxy=None, timeout=15):
    """Fetch URL using curl subprocess (more reliable proxy support)."""
    cmd = ["curl", "-s", "-L", "--max-time", str(timeout),
           "-H", "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"]
    if proxy:
        cmd += ["--proxy", proxy]
    cmd.append(url)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
        return result.stdout
    except Exception:
        return None


def fetch_baidu(limit=15, proxy=None):
    """Fetch Baidu realtime hot search."""
    html = curl_fetch("https://top.baidu.com/board?tab=realtime", proxy=proxy)
    if not html:
        return []
    import re
    items = []
    words = re.findall(r'"word"\s*:\s*"([^"]+)"', html)
    scores = re.findall(r'"hotScore"\s*:\s*"?(\d+)"?', html)
    for i, word in enumerate(words[:limit]):
        score = scores[i] if i < len(scores) else "0"
        items.append({
            "rank": i + 1,
            "title": word,
            "hot": score,
            "url": f"https://www.baidu.com/s?wd={urllib.parse.quote(word)}"
        })
    return items


def fetch_toutiao(limit=15, proxy=None):
    """Fetch Toutiao hot board."""
    data = curl_fetch("https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc", proxy=proxy)
    if not data:
        return []
    try:
        obj = json.loads(data)
    except json.JSONDecodeError:
        return []
    items = []
    for i, item in enumerate(obj.get("data", [])[:limit]):
        items.append({
            "rank": i + 1,
            "title": item.get("Title", ""),
            "hot": str(item.get("HotValue", 0)),
            "url": item.get("Url", ""),
        })
    return items


def fetch_v2ex(limit=15, proxy=None):
    """Fetch V2EX hot topics."""
    data = curl_fetch("https://www.v2ex.com/api/topics/hot.json", proxy=proxy)
    if not data:
        return []
    try:
        topics = json.loads(data)
    except json.JSONDecodeError:
        return []
    items = []
    for i, t in enumerate(topics[:limit]):
        items.append({
            "rank": i + 1,
            "title": t.get("title", ""),
            "node": t.get("node", {}).get("title", ""),
            "author": t.get("member", {}).get("username", ""),
            "replies": t.get("replies", 0),
            "url": t.get("url", ""),
        })
    return items


def fetch_hackernews(limit=15, proxy=None):
    """Fetch Hacker News top stories."""
    ids_data = curl_fetch("https://hacker-news.firebaseio.com/v0/topstories.json", proxy=proxy)
    if not ids_data:
        return []
    try:
        ids = json.loads(ids_data)[:limit]
    except json.JSONDecodeError:
        return []
    items = []
    for i, story_id in enumerate(ids):
        item_data = curl_fetch(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json", proxy=proxy)
        if item_data:
            try:
                item = json.loads(item_data)
                items.append({
                    "rank": i + 1,
                    "title": item.get("title", ""),
                    "score": item.get("score", 0),
                    "author": item.get("by", ""),
                    "comments": item.get("descendants", 0),
                    "url": item.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                })
            except json.JSONDecodeError:
                continue
    return items


def fetch_github_trending(limit=10, proxy=None):
    """Fetch GitHub repos created in last 7 days, sorted by stars."""
    date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    url = f"https://api.github.com/search/repositories?q=created:>{date}&sort=stars&order=desc&per_page={limit}"
    data = curl_fetch(url, proxy=proxy)
    if not data:
        return []
    try:
        obj = json.loads(data)
    except json.JSONDecodeError:
        return []
    items = []
    for i, repo in enumerate(obj.get("items", [])[:limit]):
        items.append({
            "rank": i + 1,
            "name": repo.get("full_name", ""),
            "description": (repo.get("description") or "")[:100],
            "stars": repo.get("stargazers_count", 0),
            "language": repo.get("language") or "N/A",
            "url": repo.get("html_url", ""),
        })
    return items


SOURCES = {
    "baidu": ("百度热榜", fetch_baidu),
    "toutiao": ("今日头条", fetch_toutiao),
    "v2ex": ("V2EX", fetch_v2ex),
    "hn": ("Hacker News", fetch_hackernews),
    "github": ("GitHub 热门新项目", fetch_github_trending),
}


def format_text(results):
    lines = []
    for source_name, items in results.items():
        lines.append(f"\n{'='*50}")
        lines.append(f"📊 {source_name}")
        lines.append(f"{'='*50}")
        for item in items:
            hot = item.get("hot") or item.get("score") or item.get("stars") or item.get("replies", "")
            hot_str = f" (🔥{hot})" if hot else ""
            title = item.get("title") or item.get("name", "")
            lines.append(f"  {item['rank']}. {title}{hot_str}")
    return "\n".join(lines)


def format_markdown(results):
    lines = [f"# 🔥 热榜聚合 — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"]
    for source_name, items in results.items():
        lines.append(f"## {source_name}\n")
        lines.append("| # | 标题 | 热度 | 链接 |")
        lines.append("|---|------|------|------|")
        for item in items:
            hot = item.get("hot") or str(item.get("score") or item.get("stars") or item.get("replies", ""))
            title = item.get("title") or item.get("name", "")
            url = item.get("url", "")
            link = f"[🔗]({url})" if url else ""
            lines.append(f"| {item['rank']} | {title} | {hot} | {link} |")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="CN Hot Trends — 中文+全球热榜聚合器")
    parser.add_argument("--sources", default="baidu,toutiao,v2ex,hn,github")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--format", choices=["json", "text", "markdown"], default="json")
    parser.add_argument("--proxy", default=None, help="HTTP proxy (e.g. http://127.0.0.1:7897)")
    args = parser.parse_args()

    sources = [s.strip() for s in args.sources.split(",")]
    results = {}

    for src in sources:
        if src not in SOURCES:
            print(f"⚠️ Unknown source: {src}", file=sys.stderr)
            continue
        name, fetcher = SOURCES[src]
        try:
            items = fetcher(args.limit, proxy=args.proxy)
            if items:
                results[name] = items
            else:
                print(f"⚠️ {name}: no data returned", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ {name}: {e}", file=sys.stderr)

    if args.format == "json":
        print(json.dumps(results, ensure_ascii=False, indent=2))
    elif args.format == "text":
        print(format_text(results))
    elif args.format == "markdown":
        print(format_markdown(results))


if __name__ == "__main__":
    main()

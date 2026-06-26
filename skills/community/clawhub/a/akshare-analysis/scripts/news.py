#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "akshare>=1.0.0",
# ]
# ///
"""
Search stock news by keyword(s).

Usage:
    uv run news.py KEYWORD [KEYWORD2 ...]
    uv run news.py 00700 腾讯 港股 --json
"""

import argparse
import json
from datetime import datetime

import akshare as ak


def search_news(keywords: list[str], max_per_keyword: int = 10) -> list[dict]:
    """Search news by multiple keywords, merge and dedupe."""
    seen = set()
    results = []

    for kw in keywords:
        try:
            df = ak.stock_news_em(symbol=kw)
            if df is None or df.empty:
                continue

            for _, row in df.head(max_per_keyword).iterrows():
                # Dedupe by title
                title = str(row.get("新闻标题", ""))
                if title and title not in seen:
                    seen.add(title)
                    results.append({
                        "keyword": kw,
                        "title": title,
                        "time": str(row.get("发布时间", "")),
                        "source": str(row.get("文章来源", "")),
                        "content": str(row.get("新闻内容", ""))[:500],  # truncate long content
                    })
        except Exception as e:
            print(f"Warning: Failed to search '{kw}': {e}", flush=True)

    # Sort by time (newest first)
    results.sort(key=lambda x: x["time"], reverse=True)
    return results


def format_text(news: list[dict]) -> str:
    if not news:
        return "No news found."

    lines = ["=" * 60, f"News Search Results ({len(news)} articles)", "=" * 60, ""]
    for i, n in enumerate(news, 1):
        lines.append(f"[{i}] {n['title']}")
        lines.append(f"    来源: {n['source']} | 时间: {n['time']} | 关键词: {n['keyword']}")
        if n['content']:
            lines.append(f"    摘要: {n['content'][:200]}...")
        lines.append("")
    lines.append("=" * 60)
    return "\n".join(lines)


def format_json(news: list[dict]) -> str:
    return json.dumps({
        "generated_at": datetime.now().isoformat(),
        "keywords": keywords,
        "count": len(news),
        "news": news,
    }, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search stock news by keywords")
    parser.add_argument("keywords", nargs="+", help="Keywords to search (ticker, name, etc.)")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--max", type=int, default=10, help="Max articles per keyword")
    args = parser.parse_args()

    keywords = args.keywords

    news = search_news(keywords, max_per_keyword=args.max)

    if args.json:
        print(format_json(news))
    else:
        print(format_text(news))

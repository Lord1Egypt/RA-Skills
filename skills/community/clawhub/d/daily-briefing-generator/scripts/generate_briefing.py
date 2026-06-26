#!/usr/bin/env python3
"""Daily Briefing Generator — 每日简报生成"""
import argparse, os, sys
from datetime import datetime

def search_tavily(query: str, api_key: str, max_results: int = 5) -> list:
    try:
        from tavily import TavilyClient
    except ImportError:
        return [{"title": "[Tavily未安装]", "url": "", "content": "pip install tavily-python"}]
    if not api_key:
        return [{"title": "[无API Key]", "url": "", "content": "请设置 TAVILY_API_KEY"}]
    try:
        client = TavilyClient(api_key=api_key)
        result = client.search(query=query, search_depth="advanced", max_results=max_results)
        return result.get("results", [])
    except Exception as e:
        return [{"title": f"[搜索失败: {e}]", "url": "", "content": ""}]

def build_briefing(sources: list, max_items: int, language: str = "zh") -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [f"# 每日简报\n", f"**日期**: {today}\n", f"## 今日要点\n"]
    seen = set()
    count = 0
    for kw in sources:
        results = search_tavily(kw, os.environ.get("TAVILY_API_KEY", ""), max_results)
        lines.append(f"### {kw}\n")
        for r in results:
            title = r.get("title", "")
            url = r.get("url", "")
            content = r.get("content", "")[:150]
            if title and title not in seen and count < max_items * len(sources):
                seen.add(title)
                count += 1
                lines.append(f"**{count}. {title}**\n")
                lines.append(f"链接: {url}\n{content}...\n\n")
    lines.append(f"\n---\n*由 daily-briefing-generator 生成 | {today}*")
    return "".join(lines)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--sources", required=True, help="逗号分隔的信息源关键词")
    p.add_argument("--max-items", type=int, default=5)
    p.add_argument("--output", default="")
    p.add_argument("--language", default="zh")
    args = p.parse_args()
    sources = [s.strip() for s in args.sources.split(",") if s.strip()]
    result = build_briefing(sources, args.max_items, args.language)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"简报已保存: {args.output}")
    else:
        print(result)

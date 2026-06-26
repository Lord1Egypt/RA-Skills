#!/usr/bin/env python3
"""
自然语言搜索入口 — 从中文自然语言中提取关键词并调用抖音爬虫。

用法:
  python scripts/nl_search.py "搜索一下海鲜视频"
  python scripts/nl_search.py "看看抖音热榜有什么"
  python scripts/nl_search.py "找一些海鲜售卖相关的视频文案"
"""

import argparse
import json
import re
import sys
from pathlib import Path

# 将项目根目录加入 path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from scraper import DouyinScraper, write_json, write_csv

# ── 简易关键词提取 ──────────────────────────────────────────────

def parse_nl(text: str) -> dict:
    """从自然语言中提取 command / keyword / limit。"""
    text = text.strip()

    # 热榜类
    if re.search(r"热榜|热搜|热门|排行榜|trending", text):
        cat_match = re.search(r"([\u4e00-\u9fff]{1,4})[的]?(?:热榜|热搜|热门|排行榜)", text)
        category = cat_match.group(1) if cat_match else ""
        return {"command": "hot", "category": category, "limit": 20}

    # 搜索类 — 提取关键词
    # 去掉常见前缀（含可选的量词 一下/一些/点 等）
    cleaned = re.sub(
        r"^(搜索|搜|找|查|看看|帮我|请|我想|能不能|能不能帮我|来)[一下些点]*(?:看看)?(?:抖音|视频)?",
        "",
        text,
    )
    # 去掉后缀
    cleaned = re.sub(r"(相关|有关|的)?(?:视频|文案|内容|帖子|东西).*$", "", cleaned)
    keyword = cleaned.strip() or text.strip()

    # 提取 limit
    limit_match = re.search(r"(\d+)\s*[条个篇]", text)
    limit = int(limit_match.group(1)) if limit_match else 10

    return {"command": "search", "keyword": keyword, "limit": limit}


def main() -> None:
    parser = argparse.ArgumentParser(description="抖音自然语言搜索")
    parser.add_argument("query", help="自然语言搜索请求，如 '搜索一下海鲜视频'")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--format", "-f", choices=["json", "csv"], default="json")
    args = parser.parse_args()

    parsed = parse_nl(args.query)
    scraper = DouyinScraper()

    print(f"🧠 解析结果: {json.dumps(parsed, ensure_ascii=False)}")

    if parsed["command"] == "search":
        items = scraper.search(parsed["keyword"], parsed["limit"])
    else:
        items = scraper.hot(parsed.get("category", ""), parsed["limit"])

    # 打印结果
    for i, item in enumerate(items, 1):
        print(f"{i}. {item.title} | {item.author} | ▶{item.play_count} 👍{item.like_count} | {item.url}")

    # 保存
    if args.output:
        out = Path(args.output)
        if args.format == "csv":
            write_csv(items, out)
        else:
            write_json(items, out)
        print(f"\n💾 已保存到: {args.output}")


if __name__ == "__main__":
    main()

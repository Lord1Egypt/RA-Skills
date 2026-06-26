#!/usr/bin/env python3
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dynamic_guard  # type: ignore


def detect_intent(query: str) -> str:
    # Align intent with dynamic subtype first.
    if dynamic_guard.detect_subtype(query):
        return "dynamic"

    q = query.lower()
    rules = [
        ("dynamic", ["今天", "明天", "实时", "现在", "余票", "票价", "价格", "库存", "可订", "航班", "酒店", "机票", "stock", "price", "availability", "live"]),
        ("document", ["pdf", "白皮书", "报告", "paper", "论文", "文档", "docs", "api", "manual"]),
        ("comparison", ["对比", "哪个好", "区别", "vs", "versus", "compare", "better"]),
        ("experience", ["评价", "体验", "好用吗", "踩坑", "评测", "教程", "推荐", "review", "opinion", "experience"]),
        ("navigation", ["官网", "入口", "地址", "在哪里", "official site", "website", "homepage"]),
        ("fact", []),
    ]
    for intent, kws in rules:
        if any(k in q for k in kws):
            return intent
    return "fact"


def detect_route(query: str, intent: str) -> str:
    q = query.lower()
    domestic_hits = sum(1 for k in [
        "上海", "北京", "赤峰", "知乎", "小红书", "微博", "公众号", "b站", "航班", "机票", "酒店", "携程", "飞猪", "去哪儿", "douban", "zhihu", "bilibili"
    ] if k in q)
    global_hits = sum(1 for k in [
        "github", "api", "docs", "stack overflow", "reddit", "wikipedia", "arxiv", "scholar", "open source", "release", "changelog"
    ] if k in q)

    if intent == "dynamic" and domestic_hits >= global_hits:
        return "domestic-first"
    if global_hits > domestic_hits + 1:
        return "global-first"
    if domestic_hits > global_hits + 1:
        return "domestic-first"
    return "mixed"


def suggest_sites(intent: str, route: str):
    if intent == "dynamic":
        return ["real-time page", "official page", "ota/platform page"]
    if intent == "experience" and route != "global-first":
        return ["Zhihu", "Xiaohongshu", "Bilibili", "Weibo"]
    if intent == "document":
        return ["official docs", "GitHub", "Google Scholar/arXiv"]
    if route == "domestic-first":
        return ["Baidu", "Bing CN", "Zhihu", "Bilibili"]
    if route == "global-first":
        return ["Google", "DuckDuckGo", "Brave", "GitHub"]
    return ["Bing CN", "Google", "DuckDuckGo"]


def main():
    if len(sys.argv) < 2:
        print("Usage: query_router.py <query>", file=sys.stderr)
        sys.exit(1)
    query = " ".join(sys.argv[1:])
    intent = detect_intent(query)
    route = detect_route(query, intent)
    result = {
        "query": query,
        "intent": intent,
        "route": route,
        "suggestedSites": suggest_sites(intent, route)
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

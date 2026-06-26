#!/usr/bin/env python3
"""
使用 NewsAPI 搜索电池行业新闻
API: https://newsapi.org/ (免费额度: 100 requests/day)
注册获取 API Key: https://newsapi.org/register
"""

import json
from datetime import datetime
from typing import List, Dict
from pathlib import Path

try:
    from newsapi import NewsApiClient
except ImportError:
    print("Please install: pip install newsapi-python")
    exit(1)


# 可以在这里设置 API Key，或通过环境变量 NEWS_API_KEY
# NEWS_API_KEY = "your-api-key-here"
import os
NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "")


def search_with_newsapi(query: str, country: str = "us") -> List[Dict]:
    """使用 NewsAPI 搜索"""
    if not NEWS_API_KEY:
        print("  NewsAPI key not set, skipping...")
        return []

    try:
        newsapi = NewsApiClient(api_key=NEWS_API_KEY)
        # 根据国家选择来源
        country_codes = {
            "中国": "cn",
            "美国": "us",
            "印度": "in",
            "俄罗斯": "ru",
            "韩国": "kr"
        }
        lang = country_codes.get(country, "en")

        # 搜索新闻
        articles = newsapi.get_everything(
            q=query,
            language=lang if lang != "en" else "en",
            sort_by="relevancy",
            page_size=10
        )

        results = []
        if articles and articles.get("articles"):
            for art in articles["articles"]:
                if art.get("title") and art["title"] != "[Removed]":
                    results.append({
                        "country": country,
                        "title": art["title"],
                        "url": art.get("url", ""),
                        "description": art.get("description", ""),
                        "source": art.get("source", {}).get("name", ""),
                        "published_at": art.get("publishedAt", ""),
                        "query": query,
                        "search_time": datetime.now().isoformat()
                    })
        return results
    except Exception as e:
        print(f"  NewsAPI error: {e}")
        return []


async def main():
    """主函数"""
    print("[START] Searching battery industry news via NewsAPI...")

    if not NEWS_API_KEY:
        print("WARNING: NEWS_API_KEY not set. Please set environment variable or edit this file.")
        print("Get free API key at: https://newsapi.org/register")
        print()

    # 搜索配置
    SEARCH_QUERIES = {
        "中国": ["battery subsidy policy China 2026", "锂电池补贴政策", "energy storage China"],
        "美国": ["battery manufacturing subsidy US 2026", "EV tax credit battery", "IRA battery incentive"],
        "印度": ["battery subsidy India PLI 2026", "ALMM battery India", "FAME EV subsidy"],
        "俄罗斯": ["battery subsidy Russia EV 2026", "аккумулятор субсидия Россия"],
        "韩国": ["battery subsidy Korea 2026", "한국 배터리 보조금", "EV battery Korea"]
    }

    all_news = []
    for country, queries in SEARCH_QUERIES.items():
        print(f"  Searching {country}...")
        for query in queries:
            results = search_with_newsapi(query, country)
            all_news.extend(results)
            print(f"    Query '{query}': {len(results)} results")
        print(f"    Country total: {sum(1 for n in all_news if n['country'] == country)}")

    # 去重
    seen_urls = set()
    unique_news = []
    for news in all_news:
        if news["url"] not in seen_urls:
            seen_urls.add(news["url"])
            unique_news.append(news)

    today = datetime.now().strftime("%Y%m%d")
    output_file = Path(__file__).parent.parent / "data" / f"news_raw_{today}.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(unique_news, f, ensure_ascii=False, indent=2)

    print(f"\n[DONE] Total: {len(unique_news)} unique news")
    print(f"Output: {output_file}")
    return unique_news


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

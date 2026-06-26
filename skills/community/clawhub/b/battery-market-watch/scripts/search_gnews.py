#!/usr/bin/env python3
"""
使用 GNews API 搜索电池行业新闻
GNews: https://gnews.io/ (免费额度: 100 requests/day)
不需要 API Key 可以使用基础搜索
"""

import json
from datetime import datetime
from typing import List, Dict
from pathlib import Path

try:
    from gnews import GNews
except ImportError:
    print("Please install: pip install gnews")
    exit(1)


# GNews 不需要 API Key（免费版有速率限制）
# 可选：设置 API Key 获取更高配额
# GNEWS_API_KEY = "your-api-key"
import os
GNEWS_API_KEY = os.environ.get("GNEWS_API_KEY", "")


def search_with_gnews(query: str, country: str) -> List[Dict]:
    """使用 GNews 搜索"""
    try:
        gn = GNews(language='en', country=country if country else 'US', max_results=10)
        articles = gn.get_news(query)

        results = []
        for art in articles:
            if art.get("title"):
                results.append({
                    "country": country,
                    "title": art["title"],
                    "url": art.get("url", ""),
                    "description": art.get("description", ""),
                    "publisher": art.get("publisher", {}).get("name", ""),
                    "published_at": art.get("published date", ""),
                    "query": query,
                    "search_time": datetime.now().isoformat()
                })
        return results
    except Exception as e:
        print(f"  GNews error: {e}")
        return []


async def main():
    """主函数"""
    print("[START] Searching battery industry news via GNews...")

    # 搜索配置 - GNews 使用 ISO 国家代码
    COUNTRY_CODES = {
        "中国": "CN",
        "美国": "US",
        "印度": "IN",
        "俄罗斯": "RU",
        "韩国": "KR"
    }

    SEARCH_QUERIES = {
        "中国": ["battery subsidy policy", "lithium battery subsidy", "energy storage policy"],
        "美国": ["battery manufacturing subsidy", "EV tax credit battery", "IRA battery incentive"],
        "印度": ["battery subsidy India PLI", "ALMM battery India", "FAME EV subsidy"],
        "俄罗斯": ["battery subsidy Russia EV", "аккумулятор субсидия Россия"],
        "韩国": ["battery subsidy Korea", "EV battery Korea policy"]
    }

    all_news = []
    for country, queries in SEARCH_QUERIES.items():
        print(f"  Searching {country}...")
        cc = COUNTRY_CODES.get(country, "US")

        for query in queries:
            results = search_with_gnews(query, cc)
            all_news.extend(results)
            print(f"    Query '{query}': {len(results)} results")
            import time
            time.sleep(1)  # 避免请求过快

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

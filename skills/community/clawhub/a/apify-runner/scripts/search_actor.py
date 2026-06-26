#!/usr/bin/env python3
"""
Apify Store Actor 搜索 + 质量筛选
输入：搜索关键词
输出：Top N 候选 Actor（按综合分排序）
"""

import json
import sys
import argparse
import requests

STORE_API = "https://api.apify.com/v2/store"

# 质量筛选阈值
MIN_SUCCESS_RATE = 0.95
MIN_RUNS_30D = 1000
MIN_RATING = 4.0
VALID_NOTICES = {"NONE"}


def search_actors(query, limit=10):
    """搜索 Apify Store"""
    resp = requests.get(STORE_API, params={"search": query, "limit": limit})
    resp.raise_for_status()
    return resp.json().get("data", {}).get("items", [])


def score_actor(item):
    """综合评分：成功率 × 评分 × log(运行量)"""
    import math
    stats = item.get("stats", {})
    run_stats = stats.get("publicActorRunStats30Days", {})
    total = run_stats.get("TOTAL", 0)
    succeeded = run_stats.get("SUCCEEDED", 0)
    success_rate = succeeded / total if total > 0 else 0
    rating = item.get("actorReviewRating", 0) or 0
    # 综合分 = 成功率 × 评分 × log10(运行量+1)
    score = success_rate * rating * math.log10(total + 1)
    return score


def filter_and_rank(items):
    """筛选 + 排序"""
    results = []
    for item in items:
        stats = item.get("stats", {})
        run_stats = stats.get("publicActorRunStats30Days", {})
        total = run_stats.get("TOTAL", 0)
        succeeded = run_stats.get("SUCCEEDED", 0)
        success_rate = succeeded / total if total > 0 else 0
        rating = item.get("actorReviewRating", 0) or 0
        notice = item.get("notice", "UNKNOWN")

        # 筛选
        if notice not in VALID_NOTICES:
            continue
        if success_rate < MIN_SUCCESS_RATE:
            continue
        if total < MIN_RUNS_30D:
            continue
        if rating < MIN_RATING:
            continue

        actor_id = f"{item['username']}/{item['name']}"
        pricing = item.get("currentPricingInfo", {})
        pricing_model = pricing.get("pricingModel", "unknown")

        results.append({
            "actor_id": actor_id,
            "title": item.get("title", ""),
            "description": item.get("description", "")[:200],
            "rating": round(rating, 1),
            "success_rate": round(success_rate * 100, 1),
            "runs_30d": total,
            "pricing_model": pricing_model,
            "score": round(score_actor(item), 2),
            "url": f"https://apify.com/{actor_id}",
            "md_url": f"https://apify.com/{actor_id}.md",
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def main():
    parser = argparse.ArgumentParser(description="搜索 Apify Store Actor")
    parser.add_argument("query", help="搜索关键词")
    parser.add_argument("--limit", type=int, default=10, help="搜索返回数量")
    parser.add_argument("--top", type=int, default=3, help="输出 Top N")
    args = parser.parse_args()

    items = search_actors(args.query, args.limit)
    ranked = filter_and_rank(items)[:args.top]

    if not ranked:
        print(json.dumps({"status": "no_results", "query": args.query, "candidates": []}, ensure_ascii=False, indent=2))
        sys.exit(0)

    print(json.dumps({"status": "ok", "query": args.query, "candidates": ranked}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

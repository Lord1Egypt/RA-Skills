#!/usr/bin/env python3
"""
摆摊品类智能匹配器 - 基于用户画像推荐最佳品类
用法: python product_matcher.py --budget 1000 --city-type "一线城市" --season "夏季" --experience "新手"
"""

import argparse
import json
import sys
from typing import Dict, Any, List

# 品类数据库
PRODUCTS = [
    # 美食类
    {"name": "手打柠檬茶", "category": "美食饮品", "min_budget": 400, "profit_rate": 0.83, "difficulty": 1, "best_season": "夏季", "city_fit": ["一线", "新一线", "二线"], "daily_range": "500-1200", "competition": "高"},
    {"name": "铁板鱿鱼", "category": "美食小吃", "min_budget": 800, "profit_rate": 0.65, "difficulty": 2, "best_season": "四季", "city_fit": ["一线", "新一线", "二线", "三线"], "daily_range": "800-1500", "competition": "中"},
    {"name": "煎饼果子", "category": "美食小吃", "min_budget": 500, "profit_rate": 0.65, "difficulty": 2, "best_season": "四季", "city_fit": ["一线", "新一线", "二线", "三线", "四线"], "daily_range": "500-1000", "competition": "高"},
    {"name": "烤冷面", "category": "美食小吃", "min_budget": 400, "profit_rate": 0.68, "difficulty": 1, "best_season": "四季", "city_fit": ["一线", "新一线", "二线", "三线", "四线"], "daily_range": "600-1000", "competition": "中"},
    {"name": "臭豆腐", "category": "美食小吃", "min_budget": 500, "profit_rate": 0.70, "difficulty": 2, "best_season": "四季", "city_fit": ["新一线", "二线", "三线"], "daily_range": "700-1200", "competition": "中"},
    {"name": "烤串", "category": "美食小吃", "min_budget": 1500, "profit_rate": 0.55, "difficulty": 3, "best_season": "夏季", "city_fit": ["一线", "新一线", "二线", "三线", "四线"], "daily_range": "1000-2000", "competition": "高"},
    {"name": "卤味", "category": "美食小吃", "min_budget": 1000, "profit_rate": 0.60, "difficulty": 3, "best_season": "四季", "city_fit": ["一线", "新一线", "二线", "三线"], "daily_range": "600-1200", "competition": "中"},
    {"name": "冰粉/糖水", "category": "美食饮品", "min_budget": 300, "profit_rate": 0.80, "difficulty": 1, "best_season": "夏季", "city_fit": ["新一线", "二线", "三线", "四线"], "daily_range": "300-600", "competition": "低"},
    {"name": "烤红薯", "category": "美食小吃", "min_budget": 300, "profit_rate": 0.80, "difficulty": 1, "best_season": "冬季", "city_fit": ["一线", "新一线", "二线", "三线", "四线"], "daily_range": "300-600", "competition": "低"},
    {"name": "关东煮", "category": "美食小吃", "min_budget": 600, "profit_rate": 0.48, "difficulty": 1, "best_season": "冬季", "city_fit": ["一线", "新一线", "二线", "三线"], "daily_range": "500-800", "competition": "低"},
    # 文创类
    {"name": "串珠手链DIY", "category": "手作文创", "min_budget": 200, "profit_rate": 0.80, "difficulty": 2, "best_season": "四季", "city_fit": ["一线", "新一线", "二线"], "daily_range": "200-500", "competition": "低"},
    {"name": "幸运盲盒", "category": "手作文创", "min_budget": 200, "profit_rate": 0.65, "difficulty": 1, "best_season": "四季", "city_fit": ["一线", "新一线", "二线", "三线"], "daily_range": "200-500", "competition": "中"},
    {"name": "DIY涂鸦石膏", "category": "手作文创", "min_budget": 300, "profit_rate": 0.82, "difficulty": 1, "best_season": "四季", "city_fit": ["一线", "新一线", "二线", "三线"], "daily_range": "300-600", "competition": "低"},
    {"name": "非遗文创小物", "category": "手作文创", "min_budget": 300, "profit_rate": 0.75, "difficulty": 3, "best_season": "四季", "city_fit": ["一线", "新一线"], "daily_range": "200-500", "competition": "极低"},
    # 日用百货
    {"name": "手机贴膜", "category": "日用百货", "min_budget": 300, "profit_rate": 0.80, "difficulty": 2, "best_season": "四季", "city_fit": ["一线", "新一线", "二线", "三线", "四线"], "daily_range": "300-600", "competition": "高"},
    {"name": "手机壳", "category": "日用百货", "min_budget": 400, "profit_rate": 0.68, "difficulty": 1, "best_season": "四季", "city_fit": ["一线", "新一线", "二线", "三线", "四线"], "daily_range": "200-500", "competition": "高"},
    {"name": "小风扇/冰袖", "category": "日用百货", "min_budget": 400, "profit_rate": 0.58, "difficulty": 1, "best_season": "夏季", "city_fit": ["一线", "新一线", "二线", "三线", "四线"], "daily_range": "300-600", "competition": "中"},
    {"name": "暖手宝", "category": "日用百货", "min_budget": 400, "profit_rate": 0.65, "difficulty": 1, "best_season": "冬季", "city_fit": ["一线", "新一线", "二线", "三线", "四线"], "daily_range": "300-500", "competition": "中"},
    # 儿童经济
    {"name": "泡泡机", "category": "儿童玩具", "min_budget": 400, "profit_rate": 0.65, "difficulty": 1, "best_season": "春夏", "city_fit": ["一线", "新一线", "二线", "三线", "四线"], "daily_range": "300-600", "competition": "中"},
    {"name": "发光气球", "category": "儿童玩具", "min_budget": 200, "profit_rate": 0.62, "difficulty": 1, "best_season": "四季", "city_fit": ["一线", "新一线", "二线", "三线", "四线"], "daily_range": "200-500", "competition": "中"},
    {"name": "发光陀螺", "category": "儿童玩具", "min_budget": 200, "profit_rate": 0.65, "difficulty": 1, "best_season": "四季", "city_fit": ["二线", "三线", "四线"], "daily_range": "150-300", "competition": "低"},
]

DIFFICULTY_MAP = {1: "简单 ★☆☆", 2: "中等 ★★☆", 3: "较难 ★★★"}
COMPETITION_SORT = {"极低": 10, "低": 8, "中": 5, "高": 3}


def get_current_season() -> str:
    """根据当前月份判断季节"""
    from datetime import datetime
    month = datetime.now().month
    if 3 <= month <= 5:
        return "春季"
    elif 6 <= month <= 8:
        return "夏季"
    elif 9 <= month <= 11:
        return "秋季"
    else:
        return "冬季"


def match_products(
    budget: float = 1000,
    city_type: str = "二线",
    season: str = "auto",
    experience: str = "新手",
    prefer_category: str = "",
    prefer_low_competition: bool = False,
) -> List[Dict]:
    """根据用户画像匹配最佳品类"""

    if season == "auto":
        season = get_current_season()

    # 经验水平映射难度限制
    max_difficulty = 1 if experience == "新手" else (2 if experience == "有经验" else 3)

    # 季节匹配映射
    season_map = {
        "春季": ["四季", "春季", "春夏"],
        "夏季": ["四季", "夏季", "春夏"],
        "秋季": ["四季", "秋季"],
        "冬季": ["四季", "冬季"],
    }
    valid_seasons = season_map.get(season, ["四季", season])

    results = []
    for p in PRODUCTS:
        # 预算过滤
        if budget < p["min_budget"]:
            continue

        # 城市适配
        if city_type not in p["city_fit"]:
            continue

        # 难度过滤
        if p["difficulty"] > max_difficulty:
            continue

        # 季节匹配
        if p["best_season"] not in valid_seasons:
            continue

        # 品类过滤
        if prefer_category and p["category"] != prefer_category:
            continue

        # 竞争度过滤
        if prefer_low_competition and p["competition"] not in ["极低", "低"]:
            continue

        # 综合评分
        profit_score = p["profit_rate"] * 40  # 利润率占40%
        season_score = 25 if p["best_season"] in ["四季", season] else (15 if p["best_season"] in valid_seasons else 5)
        comp_score = COMPETITION_SORT.get(p["competition"], 5) * 3.5  # 竞争度占35%

        overall = profit_score + season_score + comp_score

        results.append({
            **p,
            "difficulty_label": DIFFICULTY_MAP.get(p["difficulty"], "未知"),
            "overall_score": round(overall, 1),
            "category_icon": {"美食饮品": "🍹", "美食小吃": "🍢", "手作文创": "🎨", "日用百货": "🏠", "儿童玩具": "👶"}.get(p["category"], "📦"),
        })

    # 按综合评分排序
    results.sort(key=lambda x: x["overall_score"], reverse=True)
    return results


def main():
    parser = argparse.ArgumentParser(description="摆摊品类智能匹配器")
    parser.add_argument("--budget", type=float, default=1000, help="启动预算（元）")
    parser.add_argument("--city-type", type=str, default="二线", help="城市等级（一线/新一线/二线/三线/四线）")
    parser.add_argument("--season", type=str, default="auto", help="季节（春季/夏季/秋季/冬季/auto）")
    parser.add_argument("--experience", type=str, default="新手", help="经验水平（新手/有经验/老手）")
    parser.add_argument("--category", type=str, default="", help="偏好品类（留空=不限制）")
    parser.add_argument("--low-comp", action="store_true", help="只看低竞争品类")
    parser.add_argument("--limit", type=int, default=8, help="返回结果数")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")

    args = parser.parse_args()

    matches = match_products(
        budget=args.budget,
        city_type=args.city_type,
        season=args.season,
        experience=args.experience,
        prefer_category=args.category,
        prefer_low_competition=args.low_comp,
    )

    top_matches = matches[:args.limit]

    if args.json:
        print(json.dumps({
            "user_profile": {
                "budget": args.budget,
                "city_type": args.city_type,
                "season": get_current_season() if args.season == "auto" else args.season,
                "experience": args.experience,
            },
            "total_matches": len(matches),
            "results": top_matches,
        }, ensure_ascii=False, indent=2))
    else:
        print("=" * 60)
        print("🛍️  摆摊品类智能推荐")
        print("=" * 60)
        print(f"\n👤 预算: ¥{args.budget} | 城市: {args.city_type} | 季节: {args.season} | 经验: {args.experience}")
        print(f"📊 共匹配 {len(matches)} 个品类，展示 Top {min(args.limit, len(matches))}:\n")

        for i, p in enumerate(top_matches, 1):
            bar = "🟢" if p["overall_score"] >= 75 else ("🟡" if p["overall_score"] >= 60 else "🟠")
            print(f"  {i:2d}. {p['category_icon']} {p['name']} {bar} {p['overall_score']}分")
            print(f"      品类: {p['category']} | 难度: {p['difficulty_label']} | 竞争: {p['competition']}")
            print(f"      启动: ¥{p['min_budget']}+ | 毛利: {p['profit_rate']*100:.0f}% | 日流水: ¥{p['daily_range']}")

        print("\n" + "=" * 60)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""多日菜单规划器 — 营养均衡、不重复、考虑时令"""

import sys
import json
import random
import argparse
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parent))
from recipe_db import load_recipes


# 餐食结构模板
MEAL_STRUCTURE = {
    "午餐": {"荤菜": 1, "素菜": 1, "汤": 1, "主食": 1},
    "晚餐": {"荤菜": 1, "素菜": 1, "汤": 0, "主食": 1},
}

# 营养目标（每天）
DAILY_NUTRITION_TARGETS = {
    "蛋白质来源": 2,  # 每天至少 2 种不同蛋白质
    "蔬菜种类": 3,    # 每天至少 3 种蔬菜
    "烹饪方式": 2,    # 每天至少 2 种烹饪方式
}

# 季节时令推荐
SEASONAL_RECOMMENDATIONS = {
    "春": {"蔬菜": ["春笋", "韭菜", "菠菜", "荠菜", "香椿"], "肉类": ["鸡", "猪肉"], "风格": "清淡生发"},
    "夏": {"蔬菜": ["苦瓜", "冬瓜", "黄瓜", "丝瓜", "茄子"], "肉类": ["鸭", "鱼", "虾"], "风格": "清热解暑"},
    "秋": {"蔬菜": ["莲藕", "山药", "南瓜", "百合", "白萝卜"], "肉类": ["牛肉", "羊肉"], "风格": "滋阴润燥"},
    "冬": {"蔬菜": ["白菜", "萝卜", "土豆", "红薯", "冬笋"], "肉类": ["羊肉", "牛肉", "猪肉"], "风格": "温补御寒"},
}


def get_current_season() -> str:
    """获取当前季节"""
    from datetime import datetime
    month = datetime.now().month
    if 3 <= month <= 5:
        return "春"
    elif 6 <= month <= 8:
        return "夏"
    elif 9 <= month <= 11:
        return "秋"
    else:
        return "冬"


def plan_meals(days: int = 5, people: int = 2, preferences: list[str] = None,
               excluded: list[str] = None, meal_types: list[str] = None) -> dict:
    """
    规划多日菜单

    Args:
        days: 规划天数
        people: 用餐人数
        preferences: 偏好（菜系、口味等）
        excluded: 排除的食材/菜系
        meal_types: 规划哪些餐（默认 ["午餐", "晚餐"]）
    """
    if meal_types is None:
        meal_types = ["午餐", "晚餐"]

    recipes = load_recipes()
    if not recipes:
        return {"error": "菜谱数据库未加载"}

    preferences = preferences or []
    excluded = excluded or []

    # 预处理菜谱
    categorized = defaultdict(list)
    for r in recipes:
        cat = r["category"]
        categorized[cat].append(r)

    # 筛选
    def filter_recipes(recipe_list, prefs, excl):
        result = list(recipe_list)
        if prefs:
            result = [r for r in result if any(
                p in r.get("cuisine", "") or
                p in r.get("name", "") or
                p in str(r.get("ingredient_tags", []))
                for p in prefs
            )]
        if excl:
            result = [r for r in result if not any(
                e in r.get("cuisine", "") or
                e in str(r.get("ingredient_tags", []))
                for e in excl
            )]
        return result

    meat_recipes = filter_recipes(categorized.get("荤菜", []), preferences, excluded)
    veg_recipes = filter_recipes(categorized.get("素菜", []), preferences, excluded)
    soup_recipes = filter_recipes(categorized.get("汤羹类", []), preferences, excluded)
    stable_recipes = filter_recipes(categorized.get("主食", []), preferences, excluded)
    cold_recipes = filter_recipes(categorized.get("凉菜", []), preferences, excluded)

    season = get_current_season()
    seasonal = SEASONAL_RECOMMENDATIONS[season]

    # 生成每日菜单
    daily_menus = []
    used_recipes = set()
    nutrition_tracker = defaultdict(list)

    for day in range(days):
        day_menu = {"day": day + 1, "meals": {}}
        day_proteins = set()
        day_veggies = set()
        day_methods = set()

        for meal_type in meal_types:
            structure = MEAL_STRUCTURE.get(meal_type, {"荤菜": 1, "素菜": 1, "汤": 0, "主食": 1})
            meal = {"dishes": [], "estimated_cost": 0}

            # 选荤菜
            if structure.get("荤菜", 0) > 0:
                available = [r for r in meat_recipes if r["name"] not in used_recipes]
                if not available:
                    available = meat_recipes
                if available:
                    # 优先选蛋白质来源不重复的
                    scored = []
                    for r in available:
                        score = 0
                        tags = r.get("ingredient_tags", [])
                        # 蛋白质多样性加分
                        protein_sources = [t for t in tags if t in ["鸡肉", "猪肉", "牛肉", "鱼肉", "虾", "羊肉", "鸭肉"]]
                        for ps in protein_sources:
                            if ps not in day_proteins:
                                score += 5
                        # 季节适配加分
                        for tag in tags:
                            if tag in seasonal.get("肉类", []):
                                score += 3
                        # 避免昨天吃过的
                        if r["name"] in used_recipes:
                            score -= 10
                        scored.append((score, r))
                    scored.sort(key=lambda x: -x[0])
                    chosen = scored[0][1]
                    meal["dishes"].append(chosen)
                    used_recipes.add(chosen["name"])
                    for tag in chosen.get("ingredient_tags", []):
                        if tag in ["鸡肉", "猪肉", "牛肉", "鱼肉", "虾", "羊肉", "鸭肉", "鸡蛋", "豆腐"]:
                            day_proteins.add(tag)
                    if "炒" in chosen["name"] or "烧" in chosen["name"]:
                        day_methods.add("炒/烧")
                    elif "蒸" in chosen["name"]:
                        day_methods.add("蒸")
                    elif "炖" in chosen["name"] or "煲" in chosen["name"]:
                        day_methods.add("炖/煲")
                    meal["estimated_cost"] += 25

            # 选素菜
            if structure.get("素菜", 0) > 0:
                available = [r for r in veg_recipes if r["name"] not in used_recipes]
                if not available:
                    available = veg_recipes
                if available:
                    chosen = random.choice(available[:min(20, len(available))])
                    meal["dishes"].append(chosen)
                    used_recipes.add(chosen["name"])
                    for tag in chosen.get("ingredient_tags", []):
                        if tag in seasonal.get("蔬菜", []) + ["青菜", "白菜", "茄子", "土豆", "豆角"]:
                            day_veggies.add(tag)
                    meal["estimated_cost"] += 10

            # 选汤
            if structure.get("汤", 0) > 0:
                available = [r for r in soup_recipes if r["name"] not in used_recipes]
                if not available:
                    available = soup_recipes
                if available:
                    chosen = random.choice(available[:min(15, len(available))])
                    meal["dishes"].append(chosen)
                    used_recipes.add(chosen["name"])
                    meal["estimated_cost"] += 12

            # 选主食
            if structure.get("主食", 0) > 0:
                available = [r for r in stable_recipes if r["name"] not in used_recipes]
                if not available:
                    available = stable_recipes
                if available:
                    chosen = random.choice(available[:min(10, len(available))])
                    meal["dishes"].append(chosen)
                    used_recipes.add(chosen["name"])
                    meal["estimated_cost"] += 5

            # 如果没有匹配的主食，默认米饭
            has_staple = any("饭" in d["name"] or "面" in d["name"] or "馒头" in d["name"] for d in meal["dishes"])
            if not has_staple and structure.get("主食", 0) > 0:
                meal["dishes"].append({"name": "米饭", "is_default": True})
                meal["estimated_cost"] += 2

            meal["estimated_cost"] *= people
            day_menu["meals"][meal_type] = meal

        day_menu["nutrition_summary"] = {
            "proteins": list(day_proteins),
            "veggies": list(day_veggies),
            "methods": list(day_methods),
            "protein_count": len(day_proteins),
            "veggie_count": len(day_veggies),
            "method_count": len(day_methods),
        }

        daily_menus.append(day_menu)

    # 总体统计
    all_meat = set()
    all_veggie = set()
    total_cost = 0
    for dm in daily_menus:
        for meal in dm["meals"].values():
            total_cost += meal["estimated_cost"]
        for p in dm["nutrition_summary"]["proteins"]:
            all_meat.add(p)
        for v in dm["nutrition_summary"]["veggies"]:
            all_veggie.add(v)

    return {
        "days": days,
        "people": people,
        "season": season,
        "seasonal_tip": f"当前{season}季，推荐{seasonal['风格']}饮食",
        "daily_menus": daily_menus,
        "summary": {
            "total_cost": total_cost,
            "protein_variety": len(all_meat),
            "veggie_variety": len(all_veggie),
            "total_dishes": len(used_recipes),
        },
    }


def format_menu_plan(plan: dict) -> str:
    """格式化菜单计划"""
    lines = []
    lines.append(f"\n📅 {plan['days']}天{plan['people']}人份菜单规划")
    lines.append(f"🌿 {plan['seasonal_tip']}")
    lines.append("=" * 60)

    for dm in plan["daily_menus"]:
        lines.append(f"\n{'='*60}")
        lines.append(f"📆 第{dm['day']}天")
        lines.append(f"{'='*60}")

        for meal_type, meal in dm["meals"].items():
            emoji = {"午餐": "🌞", "晚餐": "🌙"}.get(meal_type, "🍽️")
            lines.append(f"\n  {emoji} **{meal_type}** (约¥{meal['estimated_cost']}):")
            for dish in meal["dishes"]:
                if dish.get("is_default"):
                    lines.append(f"    🍚 {dish['name']}")
                else:
                    lines.append(f"    • {dish['name']} ({dish['cuisine']} | {'⭐'*dish['difficulty']} | ⏱{dish['cooking_time']+dish['prep_time']}分钟)")

        ns = dm["nutrition_summary"]
        lines.append(f"\n  📊 营养简报: 蛋白质×{ns['protein_count']} | 蔬菜×{ns['veggie_count']} | 烹饪方式×{ns['method_count']}")

    lines.append(f"\n{'='*60}")
    s = plan["summary"]
    lines.append(f"📊 总体统计:")
    lines.append(f"  💰 预估总花费: ¥{s['total_cost']}")
    lines.append(f"  🥩 蛋白质种类: {s['protein_variety']}种")
    lines.append(f"  🥬 蔬菜种类: {s['veggie_variety']}种")
    lines.append(f"  🍽️ 不重复菜品: {s['total_dishes']}道")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="多日菜单规划器")
    parser.add_argument("--days", type=int, default=5, help="规划天数")
    parser.add_argument("--people", type=int, default=2, help="用餐人数")
    parser.add_argument("--prefs", type=str, help="偏好，逗号分隔（川菜/粤菜/清淡/辣等）")
    parser.add_argument("--exclude", type=str, help="排除，逗号分隔（牛肉/海鲜/辣等）")
    parser.add_argument("--meals", type=str, default="午餐,晚餐", help="规划餐次，逗号分隔")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    args = parser.parse_args()

    prefs = [p.strip() for p in args.prefs.split(",") if p.strip()] if args.prefs else []
    excl = [e.strip() for e in args.exclude.split(",") if e.strip()] if args.exclude else []
    meals = [m.strip() for m in args.meals.split(",") if m.strip()]

    plan = plan_meals(args.days, args.people, prefs, excl, meals)

    if args.json:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
    else:
        print(format_menu_plan(plan))


if __name__ == "__main__":
    main()

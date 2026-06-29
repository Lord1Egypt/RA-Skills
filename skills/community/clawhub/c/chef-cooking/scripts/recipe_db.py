#!/usr/bin/env python3
"""菜谱数据库查询引擎 — 加载 recipes.json，多维度查询匹配"""

import json
import os
import sys
import argparse
from pathlib import Path
from typing import Optional

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RECIPES_FILE = DATA_DIR / "recipes.json"


def load_recipes() -> list[dict]:
    """加载菜谱数据库"""
    if not RECIPES_FILE.exists():
        print(f"❌ 菜谱数据库未找到: {RECIPES_FILE}", file=sys.stderr)
        return []
    with open(RECIPES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("recipes", [])


def search_by_name(recipes: list[dict], keyword: str) -> list[dict]:
    """按菜名模糊搜索"""
    keyword = keyword.strip().lower()
    results = []
    for r in recipes:
        if keyword in r["name"].lower():
            results.append(r)
    # 精确匹配排前面
    results.sort(key=lambda r: 0 if r["name"].lower() == keyword else 1)
    return results


def search_by_cuisine(recipes: list[dict], cuisine: str) -> list[dict]:
    """按菜系搜索"""
    cuisine_map = {
        "川": "川菜", "川菜": "川菜", "四川": "川菜",
        "粤": "粤菜", "粤菜": "粤菜", "广东": "粤菜",
        "鲁": "鲁菜", "鲁菜": "鲁菜", "山东": "鲁菜",
        "苏": "苏菜", "苏菜": "苏菜", "江苏": "苏菜",
        "浙": "浙菜", "浙菜": "浙菜", "浙江": "浙菜",
        "闽": "闽菜", "闽菜": "闽菜", "福建": "闽菜",
        "湘": "湘菜", "湘菜": "湘菜", "湖南": "湘菜",
        "徽": "徽菜", "徽菜": "徽菜", "安徽": "徽菜",
        "家常": "家常菜", "家常菜": "家常菜",
        "汤": "汤羹类", "汤羹": "汤羹类", "汤羹类": "汤羹类",
        "凉菜": "凉菜", "凉拌": "凉菜",
        "主食": "主食", "饭": "主食", "面": "主食",
    }
    target = cuisine_map.get(cuisine, cuisine)
    return [r for r in recipes if r["cuisine"] == target]


def search_by_ingredients(recipes: list[dict], ingredients: list[str]) -> list[dict]:
    """按食材搜索 — 返回包含任意指定食材的菜谱，按匹配度排序"""
    scored = []
    for r in recipes:
        all_text = json.dumps(r, ensure_ascii=False).lower()
        score = 0
        matched = []
        for ing in ingredients:
            ing_lower = ing.strip().lower()
            if ing_lower in all_text:
                # 检查是否在 ingredient_tags 中（权重更高）
                if ing_lower in [t.lower() for t in r.get("ingredient_tags", [])]:
                    score += 3
                else:
                    score += 1
                matched.append(ing.strip())
        if score > 0:
            scored.append((r, score, matched))
    scored.sort(key=lambda x: (-x[1], x[0]["difficulty"]))
    return [item[0] for item in scored], [(item[1], item[2]) for item in scored]


def search_by_tags(recipes: list[dict], tags: list[str]) -> list[dict]:
    """按营养标签/分类搜索"""
    results = []
    for r in recipes:
        all_tags = r.get("nutrition_tags", []) + [r.get("category", "")]
        if any(tag in all_tags for tag in tags):
            results.append(r)
    return results


def search_by_difficulty(recipes: list[dict], max_diff: int) -> list[dict]:
    """按难度筛选"""
    return [r for r in recipes if r["difficulty"] <= max_diff]


def search_by_time(recipes: list[dict], max_time: int) -> list[dict]:
    """按总耗时筛选"""
    return [r for r in recipes if (r["cooking_time"] + r["prep_time"]) <= max_time]


def get_recipe_detail(recipes: list[dict], name: str) -> Optional[dict]:
    """获取菜谱详情（精确匹配）"""
    name = name.strip()
    for r in recipes:
        if r["name"] == name:
            return r
    return None


def list_cuisines(recipes: list[dict]) -> dict[str, int]:
    """列出所有菜系及菜谱数量"""
    counts = {}
    for r in recipes:
        cuisine = r["cuisine"]
        counts[cuisine] = counts.get(cuisine, 0) + 1
    return counts


def format_recipe_summary(r: dict) -> str:
    """格式化菜谱摘要"""
    diff_stars = "⭐" * r["difficulty"]
    total_time = r["cooking_time"] + r["prep_time"]
    return (
        f"  {r['name']} | {r['cuisine']} | {r['category']} | "
        f"难度{diff_stars} | ⏱{total_time}分钟 | {r['servings']}"
    )


def format_recipe_full(r: dict) -> str:
    """格式化完整菜谱"""
    lines = []
    lines.append(f"\n{'='*50}")
    lines.append(f"🍽️  {r['name']}")
    lines.append(f"{'='*50}")
    lines.append(f"菜系: {r['cuisine']} | 类别: {r['category']} | 难度: {'⭐'*r['difficulty']} | 份量: {r['servings']}")
    lines.append(f"备菜: {r['prep_time']}分钟 | 烹饪: {r['cooking_time']}分钟 | 总耗时: {r['cooking_time']+r['prep_time']}分钟")
    lines.append(f"难度说明: {r.get('difficulty_reason', '无')}")

    lines.append(f"\n📋 食材:")
    for ing in r["ingredients"]:
        notes = f" ({ing['notes']})" if ing.get("notes") else ""
        lines.append(f"  • {ing['name']}: {ing['amount']}{notes}")

    lines.append(f"\n🧂 调料:")
    for s in r["seasonings"]:
        lines.append(f"  • {s['name']}: {s['amount']}")

    lines.append(f"\n🔥 步骤:")
    for step in r["steps"]:
        phase_icon = {"备料": "🔪", "处理": "🧼", "烹饪": "🔥", "装盘": "🍽️"}.get(step["phase"], "📌")
        tip = f" 💡{step['tips']}" if step.get("tips") else ""
        lines.append(f"  {phase_icon} [{step['phase']}] {step['step_number']}. {step['action']} ({step['time']}){tip}")

    if r.get("tips"):
        lines.append(f"\n💡 技巧:")
        for t in r["tips"]:
            lines.append(f"  • {t}")

    if r.get("safety_notes"):
        lines.append(f"\n⚠️ 安全提示:")
        for s in r["safety_notes"]:
            lines.append(f"  • {s}")

    if r.get("allergens"):
        lines.append(f"\n🚨 过敏原: {', '.join(r['allergens'])}")

    nut_tags = r.get("nutrition_tags", [])
    if nut_tags:
        lines.append(f"\n🏷️ 营养标签: {', '.join(nut_tags)}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="菜谱数据库查询引擎")
    parser.add_argument("--search", type=str, help="按菜名搜索")
    parser.add_argument("--cuisine", type=str, help="按菜系搜索")
    parser.add_argument("--ingredients", type=str, help="按食材搜索，逗号分隔")
    parser.add_argument("--tags", type=str, help="按营养标签搜索，逗号分隔")
    parser.add_argument("--max-difficulty", type=int, help="最高难度")
    parser.add_argument("--max-time", type=int, help="最长总时间(分钟)")
    parser.add_argument("--detail", type=str, help="查看菜谱详情(精确菜名)")
    parser.add_argument("--list-cuisines", action="store_true", help="列出所有菜系")
    parser.add_argument("--count", type=int, default=5, help="返回结果数量")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    args = parser.parse_args()

    recipes = load_recipes()
    if not recipes:
        sys.exit(1)

    # 列出菜系
    if args.list_cuisines:
        counts = list_cuisines(recipes)
        for cuisine, count in sorted(counts.items(), key=lambda x: -x[1]):
            print(f"  {cuisine}: {count}道")
        return

    # 查看详情
    if args.detail:
        r = get_recipe_detail(recipes, args.detail)
        if r:
            if args.json:
                print(json.dumps(r, ensure_ascii=False, indent=2))
            else:
                print(format_recipe_full(r))
        else:
            print(f"❌ 未找到菜谱: {args.detail}")
        return

    # 组合搜索
    results = recipes
    search_desc = []

    if args.search:
        results = search_by_name(results, args.search)
        search_desc.append(f"菜名包含'{args.search}'")

    if args.cuisine:
        results = search_by_cuisine(results, args.cuisine)
        search_desc.append(f"菜系={args.cuisine}")

    if args.ingredients:
        ings = [i.strip() for i in args.ingredients.split(",") if i.strip()]
        results, scores = search_by_ingredients(results, ings)
        search_desc.append(f"食材={args.ingredients}")

    if args.tags:
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
        results = search_by_tags(results, tags)
        search_desc.append(f"标签={args.tags}")

    if args.max_difficulty:
        results = search_by_difficulty(results, args.max_difficulty)
        search_desc.append(f"难度≤{args.max_difficulty}")

    if args.max_time:
        results = search_by_time(results, args.max_time)
        search_desc.append(f"总耗时≤{args.max_time}分钟")

    # 输出结果
    if args.json:
        print(json.dumps(results[:args.count], ensure_ascii=False, indent=2))
    else:
        desc = " + ".join(search_desc) if search_desc else "全部菜谱"
        print(f"\n🔍 搜索条件: {desc}")
        print(f"📊 找到 {len(results)} 道菜，显示前 {min(args.count, len(results))} 道:\n")
        for r in results[:args.count]:
            print(format_recipe_summary(r))
        if len(results) > args.count:
            print(f"\n... 还有 {len(results) - args.count} 道菜，请缩小搜索范围")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""智能菜谱推荐 — 输入食材，推荐最佳匹配菜品"""

import sys
import json
import argparse
from pathlib import Path

# 添加父目录到 path，以便导入 recipe_db
sys.path.insert(0, str(Path(__file__).resolve().parent))
from recipe_db import load_recipes, search_by_ingredients, format_recipe_summary


def generate_recommendations(ingredients: list[str], count: int = 3) -> dict:
    """
    根据食材列表推荐菜品
    返回: {ingredients, recommendations: [{recipe, match_score, matched_ingredients}], summary}
    """
    recipes = load_recipes()
    if not recipes:
        return {"error": "菜谱数据库未加载", "ingredients": ingredients, "recommendations": []}

    matched_recipes, scores = search_by_ingredients(recipes, ingredients)

    recommendations = []
    for i, (recipe, (score, matched)) in enumerate(zip(matched_recipes, scores)):
        if i >= count * 3:  # 多取一些做分类
            break
        # 计算匹配率
        match_rate = len(matched) / len(ingredients) if ingredients else 0
        recommendations.append({
            "recipe": recipe,
            "match_score": score,
            "matched_ingredients": matched,
            "match_rate": round(match_rate * 100)
        })

    # 按匹配度分组
    high_match = [r for r in recommendations if r["match_score"] >= len(ingredients) * 2]
    medium_match = [r for r in recommendations if len(ingredients) <= r["match_score"] < len(ingredients) * 2]
    low_match = [r for r in recommendations if r["match_score"] < len(ingredients)]

    # 精选推荐: 优先高匹配，补充中匹配
    selected = []
    seen_names = set()

    for r in high_match:
        if len(selected) >= count:
            break
        if r["recipe"]["name"] not in seen_names:
            selected.append(r)
            seen_names.add(r["recipe"]["name"])

    for r in medium_match:
        if len(selected) >= count:
            break
        if r["recipe"]["name"] not in seen_names:
            selected.append(r)
            seen_names.add(r["recipe"]["name"])

    for r in low_match:
        if len(selected) >= count:
            break
        if r["recipe"]["name"] not in seen_names:
            selected.append(r)
            seen_names.add(r["recipe"]["name"])

    # 如果内置数据库匹配不够，生成 LLM 提示
    need_llm = len(selected) < count

    # 分析食材可做的菜类型
    category_hint = analyze_ingredient_categories(ingredients)

    return {
        "ingredients": ingredients,
        "recommendations": selected,
        "total_matches": len(matched_recipes),
        "need_llm": need_llm,
        "category_hint": category_hint,
        "summary": generate_summary(selected, ingredients, need_llm)
    }


def analyze_ingredient_categories(ingredients: list[str]) -> str:
    """分析食材类型，给出烹饪方向建议"""
    meats = ["鸡", "鸭", "猪", "牛", "羊", "鱼", "虾", "蟹", "肉", "排骨", "里脊", "五花"]
    veggies = ["菜", "椒", "茄", "豆", "瓜", "菇", "笋", "葱", "姜", "蒜", "芹", "菠", "韭", "花"]
    eggs_tofu = ["蛋", "豆腐", "豆干"]
    seafood = ["鱼", "虾", "蟹", "贝", "蛤", "蚝", "鱿", "鳗", "鲍", "参"]

    has_meat = any(any(m in ing for m in meats) for ing in ingredients)
    has_veggie = any(any(v in ing for v in veggies) for ing in ingredients)
    has_egg_tofu = any(any(e in ing for e in eggs_tofu) for ing in ingredients)
    has_seafood = any(any(s in ing for s in seafood) for ing in ingredients)

    if has_meat and has_veggie:
        return "荤素搭配，适合炒菜、炖菜"
    elif has_meat:
        return "肉类为主，适合红烧、炖煮、爆炒"
    elif has_seafood:
        return "海鲜为主，适合清蒸、白灼、红烧"
    elif has_egg_tofu and has_veggie:
        return "蛋豆类+蔬菜，适合快炒、凉拌、汤品"
    elif has_veggie:
        return "蔬菜为主，适合清炒、凉拌、汤品"
    else:
        return "可根据口味选择烹饪方式"


def generate_summary(recommendations: list[dict], ingredients: list[str], need_llm: bool) -> str:
    """生成推荐摘要文本"""
    lines = []
    lines.append(f"\n🍳 根据你的食材 ({', '.join(ingredients)})，推荐以下菜品：\n")

    medals = ["🥇", "🥈", "🥉"]
    for i, rec in enumerate(recommendations):
        medal = medals[i] if i < len(medals) else "📌"
        r = rec["recipe"]
        total_time = r["cooking_time"] + r["prep_time"]
        matched = rec["matched_ingredients"]
        unmatched = [ing for ing in ingredients if ing not in matched]
        lines.append(f"{medal} **{r['name']}** — {r['cuisine']} | ⏱{total_time}分钟 | 难度{'⭐'*r['difficulty']}")
        lines.append(f"   匹配食材: {', '.join(matched)}")
        if unmatched:
            lines.append(f"   未用食材: {', '.join(unmatched)} (可搭配做配菜)")
        lines.append(f"   说明: {r.get('difficulty_reason', '家常易做')}")
        lines.append("")

    if need_llm:
        lines.append("💡 内置数据库匹配有限，可使用联网搜索获取更多菜品灵感。")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="智能菜谱推荐")
    parser.add_argument("--ingredients", type=str, required=True, help="食材列表，逗号分隔")
    parser.add_argument("--count", type=int, default=3, help="推荐数量")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    args = parser.parse_args()

    ingredients = [i.strip() for i in args.ingredients.split(",") if i.strip()]
    if not ingredients:
        print("❌ 请提供至少一种食材")
        sys.exit(1)

    result = generate_recommendations(ingredients, args.count)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["summary"])
        if result["category_hint"]:
            print(f"🧭 烹饪方向: {result['category_hint']}")
        print(f"\n📊 数据库共匹配 {result['total_matches']} 道相关菜品")
        if result["need_llm"]:
            print("🌐 建议联网搜索获取更多灵感")

        # 输出推荐菜品的 JSON 供后续使用
        recs_json = [r["recipe"] for r in result["recommendations"]]
        print("\n---RECIPES_JSON---")
        print(json.dumps(recs_json, ensure_ascii=False))


if __name__ == "__main__":
    main()

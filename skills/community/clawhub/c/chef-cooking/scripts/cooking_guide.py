#!/usr/bin/env python3
"""烹饪步骤指导 — 四阶段详细步骤输出"""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from recipe_db import load_recipes, get_recipe_detail, format_recipe_full


def generate_guide(recipe_name: str, recipes: list[dict] = None) -> dict:
    """生成菜谱详细步骤指导"""
    if recipes is None:
        recipes = load_recipes()

    recipe = get_recipe_detail(recipes, recipe_name)

    if not recipe:
        # 模糊搜索
        from recipe_db import search_by_name
        matches = search_by_name(recipes, recipe_name)
        if matches:
            return {
                "found": False,
                "recipe_name": recipe_name,
                "suggestions": [m["name"] for m in matches[:5]],
                "message": f"未精确匹配，您是否要找: {', '.join(m['name'] for m in matches[:5])}"
            }
        return {"found": False, "recipe_name": recipe_name, "suggestions": [], "message": "未找到该菜谱"}

    # 格式化步骤
    phase_icons = {"备料": "🔪", "处理": "🧼", "烹饪": "🔥", "装盘": "🍽️"}
    steps_formatted = []
    for step in recipe["steps"]:
        steps_formatted.append({
            "phase": step["phase"],
            "icon": phase_icons.get(step["phase"], "📌"),
            "step_number": step["step_number"],
            "action": step["action"],
            "time": step.get("time", ""),
            "tips": step.get("tips", "")
        })

    # 按阶段分组
    phases = {}
    for step in steps_formatted:
        phase = step["phase"]
        if phase not in phases:
            phases[phase] = []
        phases[phase].append(step)

    return {
        "found": True,
        "recipe": recipe,
        "steps_formatted": steps_formatted,
        "phases": phases,
        "total_time": recipe["cooking_time"] + recipe["prep_time"],
        "difficulty_stars": "⭐" * recipe["difficulty"]
    }


def print_guide(result: dict):
    """打印格式化步骤指导"""
    if not result["found"]:
        print(result["message"])
        if result.get("suggestions"):
            for s in result["suggestions"]:
                print(f"  • {s}")
        return

    r = result["recipe"]
    print(format_recipe_full(r))


def main():
    parser = argparse.ArgumentParser(description="烹饪步骤指导")
    parser.add_argument("--recipe", type=str, required=True, help="菜名")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    args = parser.parse_args()

    result = generate_guide(args.recipe)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_guide(result)


if __name__ == "__main__":
    main()

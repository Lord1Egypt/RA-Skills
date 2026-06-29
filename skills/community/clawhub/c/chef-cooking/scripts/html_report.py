#!/usr/bin/env python3
"""交互式卡片 HTML 报告生成器 — 菜谱卡片式展示，食材清单+步骤时间轴+技巧提示"""

import sys
import json
import argparse
import os
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parent))
from recipe_db import load_recipes, get_recipe_detail
from recipe_generator import generate_recommendations


CSS_STYLE = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
    background: #f8f5f0;
    color: #333;
    line-height: 1.6;
    padding: 20px;
    max-width: 800px;
    margin: 0 auto;
}
.header {
    text-align: center;
    padding: 30px 20px;
    background: linear-gradient(135deg, #e8532e, #f08a5d);
    color: white;
    border-radius: 16px;
    margin-bottom: 24px;
    box-shadow: 0 4px 20px rgba(232,83,46,0.3);
}
.header h1 { font-size: 28px; margin-bottom: 8px; }
.header .subtitle { font-size: 14px; opacity: 0.9; }
.recipe-card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border-left: 4px solid #e8532e;
    transition: transform 0.2s, box-shadow 0.2s;
}
.recipe-card:hover { transform: translateY(-2px); box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
.recipe-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px; }
.recipe-name { font-size: 22px; font-weight: 700; color: #2d2d2d; }
.recipe-meta { display: flex; gap: 12px; flex-wrap: wrap; align-items: center; }
.meta-tag {
    display: inline-flex; align-items: center; gap: 4px;
    padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 600;
}
.meta-tag.cuisine { background: #fff3e0; color: #e65100; }
.meta-tag.difficulty { background: #fce4ec; color: #c62828; }
.meta-tag.time { background: #e8f5e9; color: #2e7d32; }
.meta-tag.servings { background: #e3f2fd; color: #1565c0; }
.ingredients-section, .steps-section, .tips-section, .safety-section {
    margin-top: 20px;
}
.section-title {
    font-size: 16px; font-weight: 700; margin-bottom: 12px;
    display: flex; align-items: center; gap: 8px;
    color: #2d2d2d;
}
.section-title .icon { font-size: 20px; }
.ingredient-grid {
    display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 8px;
}
.ingredient-item {
    display: flex; justify-content: space-between; align-items: center;
    padding: 8px 12px; background: #fafafa; border-radius: 8px;
    font-size: 14px;
}
.ingredient-item .name { font-weight: 500; }
.ingredient-item .amount { color: #888; font-size: 13px; }
.seasoning-grid {
    display: flex; flex-wrap: wrap; gap: 8px;
}
.seasoning-item {
    padding: 6px 14px; background: #fff8e1; border-radius: 20px;
    font-size: 13px; border: 1px solid #ffe082;
}
.step-timeline { position: relative; padding-left: 28px; }
.step-timeline::before {
    content: ''; position: absolute; left: 8px; top: 0; bottom: 0;
    width: 2px; background: #e0e0e0;
}
.step-item {
    position: relative; margin-bottom: 16px; padding: 12px 16px;
    background: #fafafa; border-radius: 10px;
}
.step-item::before {
    content: ''; position: absolute; left: -24px; top: 16px;
    width: 12px; height: 12px; border-radius: 50%;
    background: #e8532e; border: 2px solid white;
    box-shadow: 0 0 0 2px #e8532e;
}
.step-phase {
    font-size: 11px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1px; color: #e8532e; margin-bottom: 4px;
}
.step-action { font-size: 15px; font-weight: 500; margin-bottom: 4px; }
.step-meta { font-size: 12px; color: #888; display: flex; gap: 12px; }
.step-tip { font-size: 12px; color: #ff9800; margin-top: 6px; padding: 6px 10px; background: #fff8e1; border-radius: 6px; }
.tips-list { display: flex; flex-direction: column; gap: 8px; }
.tip-item {
    display: flex; align-items: flex-start; gap: 8px; padding: 10px 14px;
    background: #fff8e1; border-radius: 10px; font-size: 14px;
    border-left: 3px solid #ff9800;
}
.safety-note {
    display: flex; align-items: flex-start; gap: 8px; padding: 12px 16px;
    background: #ffebee; border-radius: 10px; font-size: 14px; color: #c62828;
    border-left: 3px solid #c62828; margin-bottom: 8px;
}
.allergen-warning {
    display: flex; align-items: flex-start; gap: 8px; padding: 10px 14px;
    background: #fff3e0; border-radius: 10px; font-size: 14px; color: #e65100;
    margin-top: 12px;
}
.nutrition-tags { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 12px; }
.nutrition-tag { padding: 3px 10px; background: #e8f5e9; color: #2e7d32; border-radius: 20px; font-size: 11px; font-weight: 500; }
.meal-plan-card {
    background: white; border-radius: 16px; padding: 20px;
    margin-bottom: 16px; box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.meal-day { font-size: 18px; font-weight: 700; color: #e8532e; margin-bottom: 12px; }
.meal-slot { margin-bottom: 12px; }
.meal-slot-title { font-size: 14px; font-weight: 600; color: #666; margin-bottom: 6px; }
.meal-dishes { display: flex; flex-wrap: wrap; gap: 8px; }
.meal-dish {
    padding: 6px 14px; background: #f5f5f5; border-radius: 20px;
    font-size: 13px;
}
.meal-nutrition { font-size: 12px; color: #888; margin-top: 8px; padding-top: 8px; border-top: 1px solid #eee; }
.summary-box {
    background: linear-gradient(135deg, #2d2d2d, #444);
    color: white; border-radius: 16px; padding: 20px;
    margin-bottom: 20px;
}
.summary-box h3 { font-size: 16px; margin-bottom: 12px; }
.summary-stats { display: flex; gap: 16px; flex-wrap: wrap; }
.summary-stat { text-align: center; }
.summary-stat .num { font-size: 28px; font-weight: 700; }
.summary-stat .label { font-size: 12px; opacity: 0.8; }
.tips-search-box { margin-bottom: 20px; }
.tips-card {
    background: white; border-radius: 16px; padding: 20px;
    margin-bottom: 16px; box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.tips-q { font-size: 16px; font-weight: 700; color: #2d2d2d; margin-bottom: 10px; }
.tips-a { font-size: 14px; color: #555; white-space: pre-line; }
.tips-category {
    display: inline-block; padding: 2px 8px; background: #e3f2fd;
    color: #1565c0; border-radius: 10px; font-size: 11px; margin-bottom: 8px;
}
.safety-severity {
    display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 700;
    margin-bottom: 8px;
}
.safety-severity.danger { background: #ffcdd2; color: #b71c1c; }
.safety-severity.warning { background: #fff9c4; color: #f57f17; }
.safety-severity.info { background: #bbdefb; color: #0d47a1; }
.empty-state {
    text-align: center; padding: 60px 20px; color: #999;
}
.empty-state .emoji { font-size: 48px; margin-bottom: 12px; }
.back-link { display: block; text-align: center; margin-top: 20px; color: #e8532e; text-decoration: none; }
.footer { text-align: center; margin-top: 40px; padding: 20px; color: #aaa; font-size: 12px; }
@media (max-width: 600px) {
    body { padding: 12px; }
    .recipe-header { flex-direction: column; gap: 8px; }
    .ingredient-grid { grid-template-columns: 1fr 1fr; }
}
"""


def generate_recipe_html(recipes_data: list[dict], title: str = "AI 智能厨助 · 菜谱推荐") -> str:
    """生成菜谱卡片 HTML"""

    cards_html = ""
    for r in recipes_data:
        if isinstance(r, dict) and r.get("name"):
            # 食材清单
            ingredients_html = ""
            for ing in r.get("ingredients", []):
                notes = f' <span style="color:#aaa;font-size:12px;">{ing.get("notes","")}</span>' if ing.get("notes") else ""
                ingredients_html += f'<div class="ingredient-item"><span class="name">{ing["name"]}</span><span class="amount">{ing["amount"]}{notes}</span></div>'

            # 调料
            seasonings_html = ""
            for s in r.get("seasonings", []):
                seasonings_html += f'<span class="seasoning-item">{s["name"]}: {s["amount"]}</span>'

            # 步骤时间轴
            steps_html = ""
            phase_icons = {"备料": "🔪", "处理": "🧼", "烹饪": "🔥", "装盘": "🍽️"}
            current_phase = None
            for step in r.get("steps", []):
                phase = step.get("phase", "")
                if phase != current_phase:
                    current_phase = phase
                icon = phase_icons.get(phase, "📌")
                tip_html = f'<div class="step-tip">💡 {step["tips"]}</div>' if step.get("tips") else ""
                steps_html += f"""
                <div class="step-item">
                    <div class="step-phase">{icon} {phase}</div>
                    <div class="step-action">{step['step_number']}. {step['action']}</div>
                    <div class="step-meta">⏱ {step.get('time', '')}</div>
                    {tip_html}
                </div>"""

            # 技巧
            tips_html = ""
            for t in r.get("tips", []):
                tips_html += f'<div class="tip-item">💡 {t}</div>'

            # 安全提示
            safety_html = ""
            for s in r.get("safety_notes", []):
                safety_html += f'<div class="safety-note">⚠️ {s}</div>'

            # 过敏原
            allergen_html = ""
            if r.get("allergens"):
                allergen_html = f'<div class="allergen-warning">🚨 过敏原提示：{", ".join(r["allergens"])}</div>'

            # 营养标签
            nut_html = ""
            for n in r.get("nutrition_tags", []):
                nut_html += f'<span class="nutrition-tag">{n}</span>'

            total_time = r.get("cooking_time", 0) + r.get("prep_time", 0)
            difficulty_stars = "⭐" * r.get("difficulty", 1)

            cards_html += f"""
            <div class="recipe-card">
                <div class="recipe-header">
                    <div class="recipe-name">{r['name']}</div>
                </div>
                <div class="recipe-meta">
                    <span class="meta-tag cuisine">🍳 {r.get('cuisine', '')}</span>
                    <span class="meta-tag difficulty">{difficulty_stars}</span>
                    <span class="meta-tag time">⏱ {total_time}分钟</span>
                    <span class="meta-tag servings">🍽️ {r.get('servings', '')}</span>
                </div>
                <div class="ingredients-section">
                    <div class="section-title"><span class="icon">📋</span>食材清单</div>
                    <div class="ingredient-grid">{ingredients_html}</div>
                </div>
                <div class="ingredients-section">
                    <div class="section-title"><span class="icon">🧂</span>调料</div>
                    <div class="seasoning-grid">{seasonings_html}</div>
                </div>
                <div class="steps-section">
                    <div class="section-title"><span class="icon">🔥</span>烹饪步骤</div>
                    <div class="step-timeline">{steps_html}</div>
                </div>
                {f'<div class="tips-section"><div class="section-title"><span class="icon">💡</span>技巧提示</div><div class="tips-list">{tips_html}</div></div>' if r.get("tips") else ""}
                {f'<div class="tips-section"><div class="section-title"><span class="icon">⚠️</span>安全提示</div>{safety_html}</div>' if r.get("safety_notes") else ""}
                {allergen_html}
                {f'<div class="nutrition-tags">{nut_html}</div>' if r.get("nutrition_tags") else ""}
            </div>"""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>{CSS_STYLE}</style>
</head>
<body>
<div class="header">
    <h1>🍳 {title}</h1>
    <div class="subtitle">AI 智能家庭厨助 · 让每顿饭都简单美味</div>
</div>
{cards_html}
<div class="footer">🤖 由 AI 智能厨助生成 · {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
</body>
</html>"""


def generate_menu_html(plan: dict) -> str:
    """生成菜单规划 HTML"""
    daily_html = ""
    for dm in plan.get("daily_menus", []):
        meals_html = ""
        for meal_type, meal in dm.get("meals", {}).items():
            emoji = {"午餐": "🌞", "晚餐": "🌙"}.get(meal_type, "🍽️")
            dishes_html = ""
            for dish in meal.get("dishes", []):
                if dish.get("is_default"):
                    dishes_html += f'<span class="meal-dish">🍚 {dish["name"]}</span>'
                else:
                    dishes_html += f'<span class="meal-dish">{dish["name"]}</span>'
            meals_html += f"""
            <div class="meal-slot">
                <div class="meal-slot-title">{emoji} {meal_type} (约¥{meal['estimated_cost']})</div>
                <div class="meal-dishes">{dishes_html}</div>
            </div>"""

        ns = dm.get("nutrition_summary", {})
        nutrition_html = f"🥩 蛋白质×{ns.get('protein_count',0)} | 🥬 蔬菜×{ns.get('veggie_count',0)} | 🔥 烹饪方式×{ns.get('method_count',0)}"

        daily_html += f"""
        <div class="meal-plan-card">
            <div class="meal-day">📆 第{dm['day']}天</div>
            {meals_html}
            <div class="meal-nutrition">📊 {nutrition_html}</div>
        </div>"""

    s = plan.get("summary", {})
    summary_html = f"""
    <div class="summary-box">
        <h3>📊 {plan['days']}天菜单规划总览</h3>
        <div class="summary-stats">
            <div class="summary-stat"><div class="num">¥{s.get('total_cost', 0)}</div><div class="label">预估花费</div></div>
            <div class="summary-stat"><div class="num">{s.get('protein_variety', 0)}种</div><div class="label">蛋白质种类</div></div>
            <div class="summary-stat"><div class="num">{s.get('veggie_variety', 0)}种</div><div class="label">蔬菜种类</div></div>
            <div class="summary-stat"><div class="num">{s.get('total_dishes', 0)}道</div><div class="label">不重复菜品</div></div>
        </div>
    </div>"""

    season = plan.get("season", "")
    season_tip = plan.get("seasonal_tip", "")

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>菜单规划 — AI 智能厨助</title>
<style>{CSS_STYLE}</style>
</head>
<body>
<div class="header">
    <h1>📅 菜单规划</h1>
    <div class="subtitle">{plan['days']}天{plan['people']}人份 · 🌿 {season_tip}</div>
</div>
{summary_html}
{daily_html}
<div class="footer">🤖 由 AI 智能厨助生成 · {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
</body>
</html>"""


def generate_tips_html(tips_data: dict, query: str = "") -> str:
    """生成烹饪技巧 HTML"""
    cards = ""
    for t in tips_data.get("results", []):
        sev = t.get("severity", "")
        sev_html = ""
        if sev:
            sev_class = {"danger": "danger", "warning": "warning", "info": "info"}.get(sev, "")
            sev_labels = {"danger": "🔴 危险", "warning": "🟡 注意", "info": "🔵 知识"}
            sev_html = f'<span class="safety-severity {sev_class}">{sev_labels.get(sev, "")}</span>'

        cat = t.get("category", "")
        cat_html = f'<span class="tips-category">{cat}</span>' if cat else ""

        cards += f"""
        <div class="tips-card">
            {sev_html}{cat_html}
            <div class="tips-q">❓ {t['q']}</div>
            <div class="tips-a">{t['a']}</div>
        </div>"""

    title = f"烹饪技巧 · {query}" if query else "烹饪技巧知识库"

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>{CSS_STYLE}</style>
</head>
<body>
<div class="header">
    <h1>💡 {title}</h1>
    <div class="subtitle">找到 {tips_data.get('count', 0)} 条相关内容</div>
</div>
{cards}
<div class="footer">🤖 由 AI 智能厨助生成 · {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
</body>
</html>"""


def generate_index_html() -> str:
    """生成首页 HTML"""
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI 智能家庭厨助</title>
<style>{CSS_STYLE}</style>
</head>
<body>
<div class="header">
    <h1>🍳 AI 智能家庭厨助</h1>
    <div class="subtitle">输入食材，推荐菜谱 · 烹饪步骤指导 · 菜单规划 · 技巧问答 · 厨房安全</div>
</div>

<div class="recipe-card">
    <div class="recipe-name">🎯 快速开始</div>
    <p style="margin-top:12px;color:#666;">在对话中告诉我：</p>
    <div style="margin-top:12px;display:flex;flex-direction:column;gap:8px;">
        <div class="tip-item">🥬 "冰箱里有鸡蛋、西红柿、青椒，能做什么菜？"</div>
        <div class="tip-item">🐷 "红烧肉怎么做？"</div>
        <div class="tip-item">📅 "帮我规划本周5天晚餐"</div>
        <div class="tip-item">💡 "炒青菜怎么保持翠绿？"</div>
        <div class="tip-item">🛡️ "发芽的土豆能吃吗？"</div>
    </div>
</div>

<div class="recipe-card">
    <div class="recipe-name">📊 数据库统计</div>
    <div class="summary-stats" style="margin-top:12px;">
        <div class="summary-stat"><div class="num">219+</div><div class="label">道菜谱</div></div>
        <div class="summary-stat"><div class="num">12</div><div class="label">个菜系</div></div>
        <div class="summary-stat"><div class="num">100+</div><div class="label">条烹饪技巧</div></div>
        <div class="summary-stat"><div class="num">20+</div><div class="label">条安全知识</div></div>
    </div>
</div>

<div class="footer">🤖 由 AI 智能厨助驱动 · 覆盖八大菜系+家常菜 · {datetime.now().strftime('%Y-%m-%d')}</div>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="HTML 报告生成器")
    parser.add_argument("--type", type=str, default="recipes",
                        choices=["recipes", "menu", "tips", "safety", "index"],
                        help="报告类型")
    parser.add_argument("--recipe", type=str, help="菜名（recipes 类型）")
    parser.add_argument("--ingredients", type=str, help="食材列表（recipes 类型）")
    parser.add_argument("--tips-query", type=str, help="技巧搜索关键词")
    parser.add_argument("--tips-category", type=str, help="技巧分类")
    parser.add_argument("--plan-json", type=str, help="菜单规划 JSON 文件路径")
    parser.add_argument("--output", type=str, help="输出文件路径")
    args = parser.parse_args()

    html = ""

    if args.type == "index":
        html = generate_index_html()

    elif args.type == "recipes":
        recipes = load_recipes()
        recipes_data = []

        if args.recipe:
            r = get_recipe_detail(recipes, args.recipe)
            if r:
                recipes_data = [r]
            else:
                from recipe_db import search_by_name
                matches = search_by_name(recipes, args.recipe)
                recipes_data = matches[:5]
        elif args.ingredients:
            ings = [i.strip() for i in args.ingredients.split(",") if i.strip()]
            result = generate_recommendations(ings, 3)
            recipes_data = [r["recipe"] for r in result.get("recommendations", [])]

        if recipes_data:
            title = f"菜谱 · {args.recipe or '食材推荐'}"
            html = generate_recipe_html(recipes_data, title)
        else:
            html = generate_recipe_html([], "未找到匹配菜谱")

    elif args.type == "menu":
        if args.plan_json and os.path.exists(args.plan_json):
            with open(args.plan_json, "r", encoding="utf-8") as f:
                plan = json.load(f)
            html = generate_menu_html(plan)
        else:
            from meal_planner import plan_meals
            plan = plan_meals(5, 2)
            html = generate_menu_html(plan)

    elif args.type == "tips":
        from cooking_tips import search_tips
        tips = search_tips(args.tips_query, args.tips_category)
        html = generate_tips_html(tips, args.tips_query or "")

    elif args.type == "safety":
        from kitchen_safety import search_safety
        safety = search_safety(args.tips_query, args.tips_category)
        html = generate_tips_html(safety, args.tips_query or "")

    # 确定输出路径
    if args.output:
        out_path = Path(args.output)
    else:
        out_dir = Path(__file__).resolve().parent.parent / "outputs"
        out_dir.mkdir(exist_ok=True)
        out_path = out_dir / f"chef_{args.type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    # Use ASCII-safe output to avoid GBK encoding issues on Windows
    print(f"Report generated: {out_path}")
    print(str(out_path))  # 输出路径供调用方使用


if __name__ == "__main__":
    main()

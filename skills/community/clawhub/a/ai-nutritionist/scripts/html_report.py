"""
AI营养师 — 交互式HTML报告生成器
支持6种报告类型：饮食方案/体质食疗/慢病管理/运动营养/特殊人群/营养素详解
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nutrition_engine import NutritionEngine


def generate_meal_plan_report(profile, plan, output_path):
    """生成饮食方案HTML报告"""
    macros = plan["profile_summary"]
    week = plan["week_plan"]
    shopping = plan["shopping_list"]
    prep_tips = plan["prep_tips"]

    # Build meal cards HTML
    week_html = ""
    for day in week:
        meals_html = ""
        for mtype, meal in day["meals"].items():
            if mtype == "snacks":
                for s in meal:
                    items_str = "、".join(s["items"])
                    meals_html += f"""
                    <div class="meal-card snack">
                        <div class="meal-label">🍪 {s['name']}</div>
                        <div class="meal-items">{items_str}</div>
                        <div class="meal-meta">{s['estimated_kcal']}kcal | 蛋白{s['protein_g']}g</div>
                    </div>"""
            else:
                items_str = "、".join(meal["items"])
                emoji = {"breakfast": "🌅", "lunch": "☀️", "dinner": "🌙"}[mtype]
                label = {"breakfast": "早餐", "lunch": "午餐", "dinner": "晚餐"}[mtype]
                meals_html += f"""
                <div class="meal-card">
                    <div class="meal-label">{emoji} {label} <span class="meal-name">({meal['name']})</span></div>
                    <div class="meal-items">{items_str}</div>
                    <div class="meal-meta">{meal['estimated_kcal']}kcal | 蛋白{meal['protein_g']}g | ⏱{meal['prep_time_min']}min | {meal['target_pct']}</div>
                </div>"""

        week_html += f"""
        <div class="day-block">
            <h3>📅 Day {day['day']} — {day['day_name']}</h3>
            <div class="meals-grid">{meals_html}</div>
        </div>"""

    # Shopping list HTML
    shopping_html = ""
    for cat, items in shopping.items():
        items_html = "、".join(items)
        shopping_html += f'<div class="shop-cat"><strong>{cat}：</strong>{items_html}</div>'

    # Prep tips
    tips_html = "".join([f"<li>{tip}</li>" for tip in prep_tips])

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI营养师 — 个性化饮食方案</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; background: #f5f7fa; color: #2c3e50; line-height:1.6; }}
.container {{ max-width:900px; margin:0 auto; padding:20px; }}
.hero {{ background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color:white; padding:40px 30px; border-radius:16px; margin-bottom:24px; }}
.hero h1 {{ font-size:2em; margin-bottom:8px; }}
.hero p {{ opacity:0.9; font-size:1.1em; }}

.stats {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(130px,1fr)); gap:12px; margin-bottom:24px; }}
.stat-card {{ background:white; border-radius:12px; padding:16px; text-align:center; box-shadow:0 2px 8px rgba(0,0,0,0.06); }}
.stat-value {{ font-size:1.6em; font-weight:700; color:#43e97b; }}
.stat-label {{ font-size:0.85em; color:#7f8c8d; margin-top:4px; }}

.macro-bar {{ background:white; border-radius:12px; padding:20px; margin-bottom:24px; box-shadow:0 2px 8px rgba(0,0,0,0.06); }}
.macro-bar h3 {{ margin-bottom:16px; font-size:1.1em; }}
.bar-row {{ display:flex; align-items:center; margin-bottom:10px; }}
.bar-label {{ width:110px; font-size:0.9em; color:#555; }}
.bar-track {{ flex:1; height:20px; background:#ecf0f1; border-radius:10px; overflow:hidden; }}
.bar-fill {{ height:100%; border-radius:10px; transition:width 1s; }}
.bar-value {{ width:90px; text-align:right; font-size:0.9em; font-weight:600; padding-left:10px; }}
.bar-protein {{ background:linear-gradient(90deg, #e74c3c, #c0392b); }}
.bar-fat {{ background:linear-gradient(90deg, #f39c12, #e67e22); }}
.bar-carbs {{ background:linear-gradient(90deg, #3498db, #2980b9); }}

.section-title {{ font-size:1.3em; margin:30px 0 16px; padding-bottom:8px; border-bottom:2px solid #43e97b; }}

.day-block {{ background:white; border-radius:12px; padding:20px; margin-bottom:16px; box-shadow:0 2px 8px rgba(0,0,0,0.06); }}
.day-block h3 {{ color:#43e97b; margin-bottom:12px; font-size:1.1em; }}
.meals-grid {{ display:flex; flex-direction:column; gap:10px; }}
.meal-card {{ background:#f8f9fa; border-radius:10px; padding:12px 16px; border-left:4px solid #43e97b; }}
.meal-card.snack {{ border-left-color:#f39c12; }}
.meal-label {{ font-weight:600; font-size:1em; margin-bottom:4px; }}
.meal-name {{ font-weight:400; color:#7f8c8d; font-size:0.9em; }}
.meal-items {{ color:#555; font-size:0.9em; margin-bottom:4px; }}
.meal-meta {{ font-size:0.8em; color:#7f8c8d; }}

.shop-section {{ background:white; border-radius:12px; padding:20px; margin-bottom:24px; box-shadow:0 2px 8px rgba(0,0,0,0.06); }}
.shop-cat {{ padding:6px 0; font-size:0.95em; border-bottom:1px dashed #ecf0f1; }}
.shop-cat:last-child {{ border-bottom:none; }}

.prep-section {{ background:white; border-radius:12px; padding:20px; margin-bottom:24px; box-shadow:0 2px 8px rgba(0,0,0,0.06); }}
.prep-section ul {{ padding-left:20px; }}
.prep-section li {{ margin-bottom:6px; color:#555; }}

.disclaimer {{ background:#fff3cd; border:1px solid #ffc107; border-radius:8px; padding:16px; margin-top:20px; font-size:0.85em; color:#856404; }}

@media print {{ body {{ background:white; }} }}
</style>
</head>
<body>
<div class="container">
    <div class="hero">
        <h1>🥗 个性化饮食方案</h1>
        <p>基于《中国居民膳食指南2022》+ AI智能推荐 | {profile.get('goal', '健康饮食')}计划</p>
    </div>

    <div class="stats">
        <div class="stat-card"><div class="stat-value">{macros['每日热量']}</div><div class="stat-label">每日热量</div></div>
        <div class="stat-card"><div class="stat-value">{macros['蛋白质']}</div><div class="stat-label">蛋白质/天</div></div>
        <div class="stat-card"><div class="stat-value">{macros['脂肪']}</div><div class="stat-label">脂肪/天</div></div>
        <div class="stat-card"><div class="stat-value">{macros['碳水化合物']}</div><div class="stat-label">碳水/天</div></div>
        <div class="stat-card"><div class="stat-value">{macros['BMR']}</div><div class="stat-label">基础代谢</div></div>
        <div class="stat-card"><div class="stat-value">{macros['BMI']}</div><div class="stat-label">BMI</div></div>
    </div>

    <div class="macro-bar">
        <h3>📊 三大营养素配比</h3>
        {_macro_bar_html(macros)}
    </div>

    <h2 class="section-title">📋 {len(week)}天饮食方案</h2>
    {week_html}

    <h2 class="section-title">🛒 购物清单</h2>
    <div class="shop-section">{shopping_html}</div>

    <h2 class="section-title">👨‍🍳 备餐技巧</h2>
    <div class="prep-section"><ul>{tips_html}</ul></div>

    <div class="disclaimer">
        ⚠️ <strong>免责声明：</strong>本饮食方案为AI基于通用营养学知识生成的参考建议，不构成专业医疗意见。
        如有特殊健康状况，请咨询医生或注册营养师。食物份量可根据个人饱腹感适度调整。
    </div>
</div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path


def _macro_bar_html(macros):
    """生成营养素柱状条HTML"""
    protein = macros.get("蛋白质", "0g").replace("g", "")
    fat = macros.get("脂肪", "0g").replace("g", "")
    carbs = macros.get("碳水化合物", "0g").replace("g", "")
    total_g = float(protein) + float(fat) + float(carbs)
    if total_g == 0:
        return ""
    p_pct = int(float(protein) / total_g * 100)
    f_pct = int(float(fat) / total_g * 100)
    c_pct = 100 - p_pct - f_pct

    return f"""
    <div class="bar-row"><span class="bar-label">🔥 蛋白质</span><div class="bar-track"><div class="bar-fill bar-protein" style="width:{p_pct}%"></div></div><span class="bar-value">{protein}g ({p_pct}%)</span></div>
    <div class="bar-row"><span class="bar-label">🧈 脂肪</span><div class="bar-track"><div class="bar-fill bar-fat" style="width:{f_pct}%"></div></div><span class="bar-value">{fat}g ({f_pct}%)</span></div>
    <div class="bar-row"><span class="bar-label">🍚 碳水</span><div class="bar-track"><div class="bar-fill bar-carbs" style="width:{c_pct}%"></div></div><span class="bar-value">{carbs}g ({c_pct}%)</span></div>"""


def generate_tcm_report(tcm_result, output_path):
    """生成中医体质食疗报告"""
    c = tcm_result["constitution"]
    ident = tcm_result["identification"]

    rec_html = "".join([f'<span class="food-tag good">{f}</span>' for f in c["recommend"]])
    avoid_html = "".join([f'<span class="food-tag bad">{f}</span>' for f in c["avoid"]]) if c["avoid"] else '<span class="food-tag">无</span>'
    feat_html = "".join([f"<li>{f}</li>" for f in c["key_features"]])
    disease_html = "".join([f"<li>{d}</li>" for d in c["tendency_diseases"]]) if c["tendency_diseases"] else "<li>无明显倾向</li>"

    confidence_color = {"高": "#27ae60", "中": "#f39c12", "低": "#e74c3c"}.get(ident["confidence"], "#7f8c8d")

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI营养师 — 中医体质辨识与食疗</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif; background: #fdf6f0; color: #3d2b1f; line-height:1.6; }}
.container {{ max-width:850px; margin:0 auto; padding:20px; }}
.hero {{ background: linear-gradient(135deg, #d4a373 0%, #e9c46a 50%, #f4a261 100%); color:white; padding:40px 30px; border-radius:16px; margin-bottom:24px; text-align:center; }}
.hero h1 {{ font-size:2em; margin-bottom:8px; }}
.hero .type-badge {{ display:inline-block; background:rgba(255,255,255,0.25); padding:8px 24px; border-radius:20px; font-size:1.3em; margin-top:12px; }}
.confidence {{ display:inline-block; background:#fff; color:{confidence_color}; padding:4px 12px; border-radius:12px; font-size:0.8em; margin-left:8px; }}

.card {{ background:white; border-radius:14px; padding:24px; margin-bottom:20px; box-shadow:0 2px 12px rgba(0,0,0,0.05); }}
.card h3 {{ color:#d4a373; margin-bottom:12px; font-size:1.15em; display:flex; align-items:center; gap:8px; }}

.feature-list li {{ padding:6px 0; color:#555; }}
.food-tags {{ display:flex; flex-wrap:wrap; gap:8px; }}
.food-tag {{ padding:6px 16px; border-radius:20px; font-size:0.9em; }}
.food-tag.good {{ background:#e8f5e9; color:#2e7d32; border:1px solid #a5d6a7; }}
.food-tag.bad {{ background:#fbe9e7; color:#c62828; border:1px solid #ef9a9a; }}

.principle {{ background:#fff8e1; border-left:4px solid #ffc107; padding:16px; border-radius:8px; margin:16px 0; font-size:1em; }}

.lifestyle {{ background:#e3f2fd; border-radius:10px; padding:16px; color:#1565c0; }}

.all-scores {{ display:grid; grid-template-columns:repeat(3, 1fr); gap:8px; margin-top:12px; }}
.score-item {{ text-align:center; padding:8px; border-radius:8px; font-size:0.85em; }}
.score-item.primary {{ background:#fff3e0; border:2px solid #ff9800; font-weight:600; }}
.score-value {{ display:block; font-size:1.4em; font-weight:700; color:#d4a373; }}

.disclaimer {{ background:#fff3cd; border:1px solid #ffc107; border-radius:8px; padding:16px; margin-top:20px; font-size:0.85em; color:#856404; }}
</style>
</head>
<body>
<div class="container">
    <div class="hero">
        <h1>🌿 中医体质辨识</h1>
        <div class="type-badge">
            {c['name']}
            <span class="confidence">置信度: {ident['confidence']}</span>
        </div>
        <p style="margin-top:12px;opacity:0.9;">基于中医体质学说 · 9种体质分类</p>
    </div>

    <div class="card">
        <h3>🔍 体质特征</h3>
        <ul class="feature-list">{feat_html}</ul>
    </div>

    <div class="card">
        <h3>⚠️ 易感倾向</h3>
        <ul class="feature-list">{disease_html}</ul>
    </div>

    <div class="card">
        <h3>📊 体质评分分布</h3>
        <div class="all-scores">
            {_scores_html(ident.get("all_scores", {}), ident["primary"])}
        </div>
    </div>

    <div class="card">
        <h3>🍽️ 食疗原则</h3>
        <div class="principle">{c['food_principle']}</div>
    </div>

    <div class="card">
        <h3>✅ 推荐食材</h3>
        <div class="food-tags">{rec_html}</div>
    </div>

    <div class="card">
        <h3>❌ 需避免</h3>
        <div class="food-tags">{avoid_html}</div>
    </div>

    <div class="card">
        <h3>🏃 生活建议</h3>
        <div class="lifestyle">{c['lifestyle']}</div>
    </div>

    <div class="disclaimer">
        ⚠️ <strong>免责声明：</strong>体质自评结果仅供参考，基于中医体质学说。重要健康决策建议面诊中医师。
        本系统不能替代专业中医诊断。
    </div>
</div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path


def _scores_html(scores, primary):
    """体质评分HTML"""
    html = ""
    for name, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        cls = "score-item primary" if name == primary else "score-item"
        html += f'<div class="{cls}"><span class="score-value">{score}</span>{name}</div>'
    return html


def generate_disease_report(disease_name, data, output_path):
    """生成慢病营养报告"""
    rec_html = "".join([f'<span class="food-tag good">{f}</span>' for f in data["recommend"]])
    avoid_html = "".join([f'<span class="food-tag bad">{f}</span>' for f in data["avoid"]])
    caution_html = "".join([f'<span class="food-tag caution">{f}</span>' for f in data.get("caution", [])])
    key_nut_html = "".join([f"<li>{n}</li>" for n in data["key_nutrients"]])

    macro_html = ""
    if "macro_targets" in data:
        for k, v in data["macro_targets"].items():
            macro_html += f"<div class='macro-item'><strong>{k}:</strong> {v}</div>"

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI营养师 — {disease_name}饮食管理</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif; background:#f0f4f8; color:#2c3e50; line-height:1.6; }}
.container {{ max-width:850px; margin:0 auto; padding:20px; }}
.hero {{ background:linear-gradient(135deg, #667eea 0%, #764ba2 100%); color:white; padding:40px 30px; border-radius:16px; margin-bottom:24px; text-align:center; }}
.hero h1 {{ font-size:2em; margin-bottom:8px; }}
.card {{ background:white; border-radius:14px; padding:24px; margin-bottom:20px; box-shadow:0 2px 12px rgba(0,0,0,0.05); }}
.card h3 {{ color:#667eea; margin-bottom:12px; font-size:1.15em; }}
.principle {{ background:#e8eaf6; border-left:4px solid #5c6bc0; padding:16px; border-radius:8px; margin:16px 0; font-size:1.05em; }}
.macro-item {{ padding:6px 0; border-bottom:1px dashed #e0e0e0; }}
.macro-item:last-child {{ border-bottom:none; }}
.food-tags {{ display:flex; flex-wrap:wrap; gap:8px; }}
.food-tag {{ padding:6px 16px; border-radius:20px; font-size:0.9em; }}
.food-tag.good {{ background:#e8f5e9; color:#2e7d32; border:1px solid #a5d6a7; }}
.food-tag.bad {{ background:#fbe9e7; color:#c62828; border:1px solid #ef9a9a; }}
.food-tag.caution {{ background:#fff3e0; color:#e65100; border:1px solid #ffcc80; }}
.special-note {{ background:#e8f5e9; border-radius:10px; padding:16px; color:#2e7d32; font-weight:500; }}
.disclaimer {{ background:#fff3cd; border:1px solid #ffc107; border-radius:8px; padding:16px; margin-top:20px; font-size:0.85em; color:#856404; }}
</style>
</head>
<body>
<div class="container">
    <div class="hero">
        <h1>🩺 {disease_name} 饮食管理</h1>
        <p style="opacity:0.9;">基于临床营养指南 · AI个性化建议</p>
    </div>

    <div class="card">
        <h3>📋 核心原则</h3>
        <div class="principle">{data['core_principle']}</div>
    </div>

    <div class="card">
        <h3>🎯 关键营养素目标</h3>
        {macro_html}
    </div>

    <div class="card">
        <h3>💊 关键营养素</h3>
        <ul style="padding-left:20px;">{key_nut_html}</ul>
    </div>

    <div class="card">
        <h3>✅ 推荐食物</h3>
        <div class="food-tags">{rec_html}</div>
    </div>

    <div class="card">
        <h3>❌ 需避免</h3>
        <div class="food-tags">{avoid_html}</div>
    </div>

    <div class="card">
        <h3>⚠️ 注意事项</h3>
        <div class="food-tags">{caution_html}</div>
    </div>

    <div class="card">
        <h3>💡 特别提醒</h3>
        <div class="special-note">{data.get('special_notes', '')}</div>
    </div>

    <div class="disclaimer">
        ⚠️ <strong>免责声明：</strong>本报告为营养教育参考，不能替代医生诊断和治疗方案。慢病患者请在医生指导下调整饮食。
    </div>
</div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path


def generate_sports_report(goal, data, output_path):
    """生成运动营养报告"""
    tips_html = "".join([f"<li>{t}</li>" for t in data["tips"]])
    supp_html = "".join([f'<span class="food-tag">{s}</span>' for s in data["supplements"]])

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI营养师 — {goal}运动营养策略</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif; background:#f5f5f5; color:#2c3e50; line-height:1.6; }}
.container {{ max-width:850px; margin:0 auto; padding:20px; }}
.hero {{ background:linear-gradient(135deg, #ff512f 0%, #f09819 100%); color:white; padding:40px 30px; border-radius:16px; margin-bottom:24px; text-align:center; }}
.hero h1 {{ font-size:2em; margin-bottom:8px; }}
.card {{ background:white; border-radius:14px; padding:24px; margin-bottom:20px; box-shadow:0 2px 12px rgba(0,0,0,0.05); }}
.card h3 {{ color:#ff512f; margin-bottom:12px; font-size:1.15em; }}
.stat-grid {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(180px,1fr)); gap:12px; }}
.stat-item {{ background:#fff5f0; border-radius:10px; padding:16px; text-align:center; }}
.stat-num {{ font-size:1.5em; font-weight:700; color:#ff512f; }}
.stat-label {{ font-size:0.85em; color:#777; margin-top:4px; }}
.food-tags {{ display:flex; flex-wrap:wrap; gap:8px; }}
.food-tag {{ padding:6px 16px; border-radius:20px; font-size:0.9em; background:#fff3e0; color:#e65100; border:1px solid #ffcc80; }}
.tips {{ padding-left:20px; }}
.tips li {{ margin-bottom:8px; color:#555; }}
.workout-box {{ background:#e8f5e9; border-radius:8px; padding:16px; margin:12px 0; }}
.workout-box h4 {{ color:#2e7d32; margin-bottom:8px; }}
.disclaimer {{ background:#fff3cd; border:1px solid #ffc107; border-radius:8px; padding:16px; margin-top:20px; font-size:0.85em; color:#856404; }}
</style>
</head>
<body>
<div class="container">
    <div class="hero">
        <h1>💪 {goal}运动营养</h1>
        <p style="opacity:0.9;">科学营养 × 高效训练</p>
    </div>

    <div class="stat-grid">
        <div class="stat-item">
            <div class="stat-num">{data['protein_g_per_kg'][0]}-{data['protein_g_per_kg'][1]}g/kg</div>
            <div class="stat-label">蛋白质需求</div>
        </div>
        <div class="stat-item">
            <div class="stat-num">{data.get('calorie_surplus','')}{data.get('calorie_deficit','')}{data.get('calorie_target','')}</div>
            <div class="stat-label">热量调整</div>
        </div>
    </div>

    <div class="card">
        <h3>🍚 碳水策略</h3>
        <p>{data['carbs_strategy']}</p>
    </div>

    <div class="card">
        <h3>🧈 脂肪策略</h3>
        <p>{data['fat_strategy']}</p>
    </div>

    <div class="card">
        <h3>🏋️ 训练前营养</h3>
        <div class="workout-box"><h4>⏰ 训练前</h4><p>{data['pre_workout']}</p></div>
    </div>

    <div class="card">
        <h3>🔋 训练后营养</h3>
        <div class="workout-box"><h4>⏰ 训练后（黄金恢复窗口）</h4><p>{data['post_workout']}</p></div>
    </div>

    <div class="card">
        <h3>💊 补剂建议</h3>
        <div class="food-tags">{supp_html}</div>
    </div>

    <div class="card">
        <h3>💡 实用技巧</h3>
        <ul class="tips">{tips_html}</ul>
    </div>

    <div class="disclaimer">
        ⚠️ <strong>免责声明：</strong>补剂使用请结合个人情况，必要时咨询运动营养师。蛋白粉/肌酸等补剂请从正规渠道购买。
    </div>
</div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path


def generate_nutrient_report(nutrient_info, output_path):
    """生成营养素详解报告"""
    name = nutrient_info["name"]
    top_foods_html = ""
    for food, amount in nutrient_info.get("top_foods", [])[:8]:
        bar_width = min(100, amount / max(n[1] for n in nutrient_info.get("top_foods", [(1,1)])) * 100)
        top_foods_html += f"""
        <div class="food-row">
            <span class="food-name">{food}</span>
            <div class="food-bar"><div class="food-bar-fill" style="width:{int(bar_width)}%"></div></div>
            <span class="food-amount">{amount}{nutrient_info['unit'].split('/')[0]}</span>
        </div>"""

    def_html = "".join([f"<li>{d}</li>" for d in nutrient_info.get("deficiency", [])])
    excess_html = "".join([f"<li>{e}</li>" for e in nutrient_info.get("excess", ["（无明确过量危害）"])]) if nutrient_info.get("excess") else "<li>（无明确过量危害）</li>"
    promote_html = "、".join(nutrient_info.get("absorption", {}).get("促进", ["（无）"]))
    inhibit_html = "、".join(nutrient_info.get("absorption", {}).get("抑制", ["（无）"]))

    ul_display = f"{nutrient_info['ul']}{nutrient_info['unit']}" if nutrient_info.get("ul") else "未设定"

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI营养师 — {name}深度解读</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif; background:#f0f7ff; color:#1a237e; line-height:1.6; }}
.container {{ max-width:850px; margin:0 auto; padding:20px; }}
.hero {{ background:linear-gradient(135deg, #667eea 0%, #764ba2 100%); color:white; padding:40px 30px; border-radius:16px; margin-bottom:24px; text-align:center; }}
.hero h1 {{ font-size:2em; margin-bottom:8px; }}
.hero .subtitle {{ opacity:0.85; font-size:1em; }}
.card {{ background:white; border-radius:14px; padding:24px; margin-bottom:20px; box-shadow:0 2px 12px rgba(0,0,0,0.05); }}
.card h3 {{ color:#5c6bc0; margin-bottom:12px; font-size:1.15em; }}
.rda-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; }}
.rda-item {{ background:#e8eaf6; border-radius:10px; padding:16px; text-align:center; }}
.rda-value {{ font-size:1.4em; font-weight:700; color:#3949ab; }}
.rda-label {{ font-size:0.85em; color:#7986cb; }}
.food-row {{ display:flex; align-items:center; padding:8px 0; border-bottom:1px solid #e8eaf6; }}
.food-name {{ width:120px; font-weight:500; }}
.food-bar {{ flex:1; height:16px; background:#e8eaf6; border-radius:8px; overflow:hidden; margin:0 12px; }}
.food-bar-fill {{ height:100%; border-radius:8px; background:linear-gradient(90deg, #5c6bc0, #7986cb); }}
.food-amount {{ font-size:0.9em; color:#5c6bc0; font-weight:600; min-width:70px; }}
.ul-list {{ padding-left:20px; }}
.ul-list li {{ margin-bottom:6px; color:#444; }}
.fact-box {{ background:#e8eaf6; border-radius:8px; padding:16px; margin:12px 0; }}
.note {{ background:#fff8e1; border-left:4px solid #ffc107; padding:16px; border-radius:8px; margin-top:16px; color:#f57f17; }}
.disclaimer {{ background:#fff3cd; border:1px solid #ffc107; border-radius:8px; padding:16px; margin-top:20px; font-size:0.85em; color:#856404; }}
</style>
</head>
<body>
<div class="container">
    <div class="hero">
        <h1>🔬 {name}</h1>
        <p class="subtitle">{nutrient_info.get('function', '')}</p>
    </div>

    <div class="card">
        <h3>📊 每日推荐摄入量 (DRI 2024)</h3>
        <div class="rda-grid">
            <div class="rda-item"><div class="rda-value">{nutrient_info['rda_male']}{nutrient_info['unit']}</div><div class="rda-label">男性</div></div>
            <div class="rda-item"><div class="rda-value">{nutrient_info['rda_female']}{nutrient_info['unit']}</div><div class="rda-label">女性</div></div>
        </div>
        <div class="fact-box" style="margin-top:12px;">
            <strong>可耐受最高摄入量 (UL):</strong> {ul_display}
        </div>
    </div>

    <div class="card">
        <h3>⚠️ 缺乏症状</h3>
        <ul class="ul-list">{def_html}</ul>
    </div>

    <div class="card">
        <h3>🚫 过量危害</h3>
        <ul class="ul-list">{excess_html}</ul>
    </div>

    <div class="card">
        <h3>🍽️ 最佳食物来源 (每100g含量)</h3>
        {top_foods_html}
    </div>

    <div class="card">
        <h3>🧪 吸收影响因素</h3>
        <div class="fact-box">
            <strong>✅ 促进吸收:</strong> {promote_html}
        </div>
        <div class="fact-box">
            <strong>❌ 抑制吸收:</strong> {inhibit_html}
        </div>
    </div>

    <div class="note">
        💡 <strong>温馨提示：</strong>{nutrient_info.get('note', '')}
    </div>

    <div class="disclaimer">
        ⚠️ <strong>免责声明：</strong>营养信息参考《中国居民膳食营养素参考摄入量(DRIs 2024)》。个体需求因人而异，补充剂使用建议在医生或营养师指导下进行。
    </div>
</div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path


def generate_special_pop_report(population, data, output_path):
    """生成特殊人群营养报告"""
    # Flatten age groups or trimesters
    sections = ""
    if "trimesters" in data:
        for stage, info in data["trimesters"].items():
            nutrients = "".join([f"<li><strong>{k}:</strong> {v}</li>" for k, v in info["key_nutrients"].items()])
            special = "".join([f'<span class="food-tag good">{f}</span>' for f in info.get("special_foods", [])])
            avoid = "".join([f'<span class="food-tag bad">{a}</span>' for a in info.get("avoid", [])])
            sections += f"""
            <div class="card">
                <h3>📅 {stage}</h3>
                <div class="stat-row"><strong>额外热量:</strong> {info['extra_calories']}kcal/天</div>
                <h4 style="margin-top:12px;color:#e91e63;">关键营养素</h4>
                <ul style="padding-left:20px;">{nutrients}</ul>
                <h4 style="margin-top:12px;color:#4caf50;">推荐食物</h4>
                <div class="food-tags">{special}</div>
                <h4 style="margin-top:12px;color:#f44336;">需避免</h4>
                <div class="food-tags">{avoid}</div>
            </div>"""
    elif "age_groups" in data:
        for group, info in data["age_groups"].items():
            nutrients = "".join([f"<li><strong>{k}:</strong> {v}</li>" for k, v in info["key_nutrients"].items()])
            tips = "".join([f"<li>{t}</li>" for t in info["tips"]])
            sections += f"""
            <div class="card">
                <h3>👶 {group}</h3>
                <h4 style="color:#e91e63;">关键营养素</h4>
                <ul style="padding-left:20px;">{nutrients}</ul>
                <h4 style="margin-top:12px;color:#2196f3;">实用建议</h4>
                <ul style="padding-left:20px;">{tips}</ul>
            </div>"""
    else:
        # Elderly or other
        concerns = "".join([f'<span class="food-tag caution">{c}</span>' for c in data.get("key_concerns", [])])
        nutrients = "".join([f"<li><strong>{k}:</strong> {v}</li>" for k, v in data.get("key_nutrients", {}).items()])
        texture = "".join([f"<li>{t}</li>" for t in data.get("food_texture", [])])
        tips = "".join([f"<li>{t}</li>" for t in data.get("tips", [])])
        sections = f"""
        <div class="card"><h3>⚠️ 重点关注</h3><div class="food-tags">{concerns}</div></div>
        <div class="card"><h3>💊 关键营养素</h3><ul style="padding-left:20px;">{nutrients}</ul></div>
        <div class="card"><h3>🍜 饮食质地建议</h3><ul style="padding-left:20px;">{texture}</ul></div>
        <div class="card"><h3>💡 实用建议</h3><ul style="padding-left:20px;">{tips}</ul></div>"""

    general_tips = "".join([f"<li>{t}</li>" for t in data.get("general_tips", data.get("tips", []))])

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI营养师 — {population}营养指南</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif; background:#fce4ec; color:#880e4f; line-height:1.6; }}
.container {{ max-width:850px; margin:0 auto; padding:20px; }}
.hero {{ background:linear-gradient(135deg, #e91e63 0%, #f06292 100%); color:white; padding:40px 30px; border-radius:16px; margin-bottom:24px; text-align:center; }}
.hero h1 {{ font-size:2em; margin-bottom:8px; }}
.card {{ background:white; border-radius:14px; padding:24px; margin-bottom:20px; box-shadow:0 2px 12px rgba(0,0,0,0.05); }}
.card h3 {{ color:#e91e63; margin-bottom:12px; font-size:1.15em; }}
.stat-row {{ background:#fce4ec; border-radius:8px; padding:12px; font-size:1.1em; }}
.food-tags {{ display:flex; flex-wrap:wrap; gap:8px; margin-top:8px; }}
.food-tag {{ padding:5px 14px; border-radius:20px; font-size:0.85em; }}
.food-tag.good {{ background:#e8f5e9; color:#2e7d32; border:1px solid #a5d6a7; }}
.food-tag.bad {{ background:#fbe9e7; color:#c62828; border:1px solid #ef9a9a; }}
.food-tag.caution {{ background:#e8eaf6; color:#283593; border:1px solid #9fa8da; }}
.disclaimer {{ background:#fff3cd; border:1px solid #ffc107; border-radius:8px; padding:16px; margin-top:20px; font-size:0.85em; color:#856404; }}
</style>
</head>
<body>
<div class="container">
    <div class="hero">
        <h1>🤱 {population}营养指南</h1>
        <p style="opacity:0.9;">基于DRIs 2024 · 专业关怀</p>
    </div>
    {sections}
    <div class="disclaimer">
        ⚠️ <strong>免责声明：</strong>本指南为营养教育参考，具体营养方案请结合定期体检结果，
        在医生或注册营养师指导下实施。
    </div>
</div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path


# ============================================================
# CLI 入口
# ============================================================

def main():
    """命令行测试入口"""
    import argparse

    parser = argparse.ArgumentParser(description="AI营养师 HTML报告生成器")
    parser.add_argument("--type", choices=["meal", "tcm", "disease", "sports", "nutrient", "special"],
                        required=True, help="报告类型")
    parser.add_argument("--output", default=None, help="输出路径")
    parser.add_argument("--profile", default=None, help="用户画像JSON文件路径")

    # For specific types
    parser.add_argument("--disease", default="糖尿病", help="慢病类型")
    parser.add_argument("--goal", default="减脂", help="目标")
    parser.add_argument("--nutrient", default="铁", help="营养素名称")
    parser.add_argument("--population", default="孕期", help="特殊人群")

    parser.add_argument("--tcm-answers", default=None, help="体质自评答案JSON")

    args = parser.parse_args()

    engine = NutritionEngine()

    # Determine output path
    if args.output:
        output = args.output
    else:
        cwd = os.getcwd()
        output = os.path.join(cwd, f"ai-nutritionist-{args.type}-report.html")

    if args.type == "meal":
        # Load or build profile
        if args.profile and os.path.exists(args.profile):
            with open(args.profile, "r", encoding="utf-8") as f:
                profile = json.load(f)
        else:
            profile = engine.build_profile({
                "age": 30, "gender": "男", "height": 175, "weight": 70,
                "goal": args.goal, "activity_level": "中度活动"
            })
        plan = engine.generate_meal_plan(profile, days=7)
        path = generate_meal_plan_report(profile, plan, output)
        print(f"✅ 饮食方案报告已生成: {path}")

    elif args.type == "tcm":
        if args.tcm_answers:
            answers = json.loads(args.tcm_answers)
        else:
            answers = {"energy": "容易疲劳", "cold": "怕冷", "stool": "稀溏"}
        result = engine.identify_tcm_constitution(answers)
        path = generate_tcm_report(result, output)
        print(f"✅ 体质食疗报告已生成: {path}")

    elif args.type == "disease":
        data = engine.disease_nutrition_guide(args.disease)
        if "error" in data:
            print(f"❌ {data['error']}")
            return
        path = generate_disease_report(args.disease, data, output)
        print(f"✅ 慢病营养报告已生成: {path}")

    elif args.type == "sports":
        data = engine.sports_nutrition_guide(args.goal)
        if "error" in data:
            print(f"❌ {data['error']}")
            return
        path = generate_sports_report(args.goal, data, output)
        print(f"✅ 运动营养报告已生成: {path}")

    elif args.type == "nutrient":
        data = engine.nutrient_info(args.nutrient)
        if "error" in data:
            print(f"❌ {data['error']}")
            print(f"可用营养素: {', '.join(data.get('available', []))}")
            return
        path = generate_nutrient_report(data, output)
        print(f"✅ 营养素报告已生成: {path}")

    elif args.type == "special":
        data = engine.special_population_guide(args.population)
        if "error" in data:
            print(f"❌ {data['error']}")
            return
        path = generate_special_pop_report(args.population, data, output)
        print(f"✅ 特殊人群营养报告已生成: {path}")


if __name__ == "__main__":
    main()

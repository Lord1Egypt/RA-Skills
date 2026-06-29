#!/usr/bin/env python3
"""
HTML 营养报告生成器
生成交互式可视化营养报告
"""

import json
from pathlib import Path
from datetime import date, datetime, timedelta
from .nutrition_calc import NutritionCalc


def generate_daily_report(calc: NutritionCalc, dt: date = None) -> str:
    """生成单日营养报告 HTML"""
    if dt is None:
        dt = date.today()

    daily = calc.calc_daily(dt)
    dri = calc.get_dri_for_user()
    rating = calc.rate_diet(daily, dri)

    # 计算各营养素百分比进度条
    bars = {
        "energy": min(daily["energy"] / dri["energy"] * 100, 150) if dri["energy"] else 0,
        "protein": min(daily["protein"] / dri["protein"] * 100, 200) if dri["protein"] else 0,
        "fat": min(daily["fat"] / dri["fat"] * 100, 150) if dri["fat"] else 0,
        "carbs": min(daily["carbs"] / dri["carbs"] * 100, 150) if dri["carbs"] else 0,
        "fiber": min(daily["fiber"] / dri["fiber"] * 100, 150) if dri["fiber"] else 0,
    }

    grade_color = {"A": "#22c55e", "B": "#3b82f6", "C": "#f59e0b", "D": "#ef4444"}

    meals_html = ""
    for i, meal in enumerate(daily.get("meals", [])):
        n = meal.get("nutrition", {})
        items_str = ", ".join([
            f'{item.get("foodName", "?")} {item.get("amount_g", "?")}g'
            for item in meal.get("items", [])
        ]) or "无记录"
        meals_html += f"""
        <div class="meal-card">
            <div class="meal-header">
                <span class="meal-name">{meal.get('meal', f'第{i+1}餐')}</span>
                <span class="meal-time">{meal.get('time', '')}</span>
            </div>
            <div class="meal-items">{items_str}</div>
            <div class="meal-nutrition">
                <span>{n.get('energy', 0)} kcal</span>
                <span>P: {n.get('protein', 0)}g</span>
                <span>F: {n.get('fat', 0)}g</span>
                <span>C: {n.get('carbs', 0)}g</span>
            </div>
        </div>"""

    feedback_html = ""
    for fb in rating.get("feedback", []):
        icon = {"good": "✅", "warn": "⚠️", "info": "ℹ️"}.get(fb["type"], "ℹ️")
        feedback_html += f'<div class="feedback-item feedback-{fb["type"]}">{icon} {fb["msg"]}</div>'

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>营养日报 - {dt.strftime('%Y年%m月%d日')}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f0fdf4; padding: 20px; }}
.container {{ max-width: 600px; margin: 0 auto; }}
.header {{ text-align: center; padding: 24px 0; }}
.header h1 {{ font-size: 22px; color: #166534; }}
.header .date {{ color: #6b7280; font-size: 14px; margin-top: 4px; }}

.score-card {{ background: white; border-radius: 16px; padding: 24px; text-align: center; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
.score-circle {{ display: inline-flex; align-items: center; justify-content: center; width: 80px; height: 80px; border-radius: 50%; background: {grade_color.get(rating['grade'], '#ef4444')}; color: white; font-size: 32px; font-weight: bold; }}
.score-label {{ margin-top: 8px; font-size: 14px; color: #6b7280; }}

.nutrients-card {{ background: white; border-radius: 16px; padding: 24px; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
.nutrient-bar {{ margin-bottom: 16px; }}
.nutrient-label {{ display: flex; justify-content: space-between; margin-bottom: 4px; font-size: 14px; }}
.nutrient-name {{ font-weight: 500; color: #374151; }}
.nutrient-value {{ color: #6b7280; }}
.nutrient-track {{ height: 8px; background: #e5e7eb; border-radius: 4px; overflow: hidden; }}
.nutrient-fill {{ height: 100%; border-radius: 4px; transition: width 0.3s; }}
.nutrient-fill.green {{ background: #22c55e; }}
.nutrient-fill.blue {{ background: #3b82f6; }}
.nutrient-fill.orange {{ background: #f59e0b; }}
.nutrient-fill.red {{ background: #ef4444; }}

.meals-card {{ background: white; border-radius: 16px; padding: 20px; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
.meals-card h3 {{ font-size: 16px; color: #166534; margin-bottom: 12px; }}
.meal-card {{ padding: 12px; background: #f9fafb; border-radius: 10px; margin-bottom: 8px; }}
.meal-header {{ display: flex; justify-content: space-between; font-size: 14px; }}
.meal-name {{ font-weight: 600; color: #374151; }}
.meal-time {{ color: #9ca3af; }}
.meal-items {{ font-size: 13px; color: #6b7280; margin-top: 4px; }}
.meal-nutrition {{ display: flex; gap: 12px; margin-top: 8px; font-size: 12px; color: #9ca3af; }}

.feedback-card {{ background: white; border-radius: 16px; padding: 20px; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
.feedback-card h3 {{ font-size: 16px; color: #166534; margin-bottom: 12px; }}
.feedback-item {{ padding: 8px 12px; border-radius: 8px; font-size: 14px; margin-bottom: 6px; }}
.feedback-good {{ background: #f0fdf4; color: #166534; }}
.feedback-warn {{ background: #fef3c7; color: #92400e; }}
.feedback-info {{ background: #eff6ff; color: #1e40af; }}

.no-data {{ text-align: center; padding: 40px; color: #9ca3af; font-size: 15px; }}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>🍽️ 营养日报</h1>
        <div class="date">{dt.strftime('%Y年%m月%d日 %A')}</div>
    </div>

    <div class="score-card">
        <div class="score-circle">{rating['score']}</div>
        <div class="score-label">饮食评分 (满分100)</div>
    </div>

    <div class="nutrients-card">
        <h3 style="font-size:16px;color:#166534;margin-bottom:16px;">📊 营养素摄入</h3>
        {_nutrient_bar("🔥 热量", daily['energy'], dri['energy'], 'kcal', bars['energy'])}
        {_nutrient_bar("🥩 蛋白质", daily['protein'], dri['protein'], 'g', bars['protein'])}
        {_nutrient_bar("🧈 脂肪", daily['fat'], dri['fat'], 'g', bars['fat'])}
        {_nutrient_bar("🍚 碳水", daily['carbs'], dri['carbs'], 'g', bars['carbs'])}
        {_nutrient_bar("🥬 膳食纤维", daily['fiber'], dri['fiber'], 'g', bars['fiber'])}
    </div>

    <div class="meals-card">
        <h3>📝 今日饮食记录</h3>
        {meals_html if meals_html else '<div class="no-data">今天还没有饮食记录<br>试试说"我早餐吃了..." 📱</div>'}
    </div>

    <div class="feedback-card">
        <h3>💡 AI 建议</h3>
        {feedback_html if feedback_html else '<div class="no-data">先记录饮食来获取建议吧~</div>'}
    </div>
</div>
</body>
</html>"""
    return html


def generate_weekly_report(calc: NutritionCalc) -> str:
    """生成周报告 HTML"""
    trend = calc.calc_trend(7)
    dri = calc.get_dri_for_user()
    today = date.today()

    # 计算周平均
    avg = {
        "energy": sum(trend["energy"]) / max(len(trend["energy"]), 1),
        "protein": sum(trend["protein"]) / max(len(trend["protein"]), 1),
        "fat": sum(trend["fat"]) / max(len(trend["fat"]), 1),
        "carbs": sum(trend["carbs"]) / max(len(trend["carbs"]), 1),
        "fiber": sum(trend["fiber"]) / max(len(trend["fiber"]), 1),
    }

    # 分析
    insights = []
    if avg["protein"] < dri["protein"] * 0.8:
        insights.append("本周蛋白质摄入偏低，建议每餐增加一份优质蛋白源（鸡胸肉、鱼、豆腐、蛋类）")
    if avg["fiber"] < dri["fiber"] * 0.6:
        insights.append("膳食纤维严重不足！每天多吃一份绿叶蔬菜和一份水果")
    if avg["fat"] > dri["fat"] * 1.3:
        insights.append("脂肪摄入偏高，注意减少油炸食品和肥肉")
    if avg["energy"] < dri["energy"] * 0.85:
        insights.append("热量摄入偏低，可能影响代谢和精力，适当增加主食")
    elif avg["energy"] > dri["energy"] * 1.15:
        insights.append("热量摄入超标，建议控制份量，增加蔬菜占比")
    else:
        insights.append("热量控制整体不错，继续保持！")

    record_days = sum(1 for e in trend["energy"] if e > 0)
    if record_days < 4:
        insights.append(f"本周仅记录了 {record_days} 天，坚持记录才能看到趋势哦")

    insight_html = "".join([f'<div class="feedback-item feedback-info">💡 {i}</div>' for i in insights])

    # 简易趋势图数据
    chart_data = json.dumps({
        "labels": trend["dates"],
        "energy": trend["energy"],
        "protein": trend["protein"],
        "fat": trend["fat"],
        "carbs": trend["carbs"],
        "energyTarget": dri["energy"],
        "proteinTarget": dri["protein"],
    })

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>营养周报</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f0fdf4; padding: 20px; }}
.container {{ max-width: 700px; margin: 0 auto; }}
.header {{ text-align: center; padding: 24px 0; }}
.header h1 {{ font-size: 22px; color: #166534; }}
.header .sub {{ color: #6b7280; font-size: 14px; }}

.card {{ background: white; border-radius: 16px; padding: 20px; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
.card h3 {{ font-size: 16px; color: #166534; margin-bottom: 12px; }}

.avg-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }}
.avg-item {{ background: #f9fafb; border-radius: 10px; padding: 12px; text-align: center; }}
.avg-value {{ font-size: 20px; font-weight: bold; color: #166534; }}
.avg-label {{ font-size: 12px; color: #6b7280; margin-top: 2px; }}
.avg-target {{ font-size: 11px; color: #9ca3af; }}

.chart-container {{ height: 280px; }}

.feedback-item {{ padding: 8px 12px; border-radius: 8px; font-size: 14px; margin-bottom: 6px; background: #eff6ff; color: #1e40af; }}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>📈 营养周报</h1>
        <div class="sub">{(today - timedelta(days=7)).strftime('%m/%d')} - {today.strftime('%m/%d')}</div>
    </div>

    <div class="card">
        <h3>📊 本周平均摄入</h3>
        <div class="avg-grid">
            <div class="avg-item">
                <div class="avg-value">{avg['energy']:.0f}</div>
                <div class="avg-label">热量 kcal</div>
                <div class="avg-target">目标 {dri['energy']}</div>
            </div>
            <div class="avg-item">
                <div class="avg-value">{avg['protein']:.0f}</div>
                <div class="avg-label">蛋白质 g</div>
                <div class="avg-target">目标 {dri['protein']}</div>
            </div>
            <div class="avg-item">
                <div class="avg-value">{avg['fat']:.0f}</div>
                <div class="avg-label">脂肪 g</div>
                <div class="avg-target">目标 {dri['fat']}</div>
            </div>
            <div class="avg-item">
                <div class="avg-value">{avg['carbs']:.0f}</div>
                <div class="avg-label">碳水 g</div>
                <div class="avg-target">目标 {dri['carbs']}</div>
            </div>
            <div class="avg-item">
                <div class="avg-value">{avg['fiber']:.0f}</div>
                <div class="avg-label">纤维 g</div>
                <div class="avg-target">目标 {dri['fiber']}</div>
            </div>
            <div class="avg-item">
                <div class="avg-value">{record_days}/7</div>
                <div class="avg-label">记录天数</div>
                <div class="avg-target">坚持就是胜利</div>
            </div>
        </div>
    </div>

    <div class="card">
        <h3>📈 热量趋势</h3>
        <div class="chart-container">
            <canvas id="energyChart"></canvas>
        </div>
    </div>

    <div class="card">
        <h3>💡 本周洞察</h3>
        {insight_html}
    </div>
</div>

<script>
const data = {chart_data};
new Chart(document.getElementById('energyChart'), {{
    type: 'bar',
    data: {{
        labels: data.labels,
        datasets: [{{
            label: '每日热量 (kcal)',
            data: data.energy,
            backgroundColor: data.energy.map(v => v > data.energyTarget ? '#fca5a5' : '#86efac'),
            borderRadius: 6,
        }}]
    }},
    options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{
            legend: {{ display: false }},
            annotation: {{ annotations: {{ target: {{ type: 'line', yMin: data.energyTarget, yMax: data.energyTarget, borderColor: '#ef4444', borderWidth: 1, borderDash: [5,5], label: {{ content: '目标', enabled: true }} }} }} }}
        }},
        scales: {{
            y: {{ beginAtZero: false, grid: {{ color: '#f3f4f6' }} }},
            x: {{ grid: {{ display: false }} }}
        }}
    }}
}});
</script>
</body>
</html>"""
    return html


def _nutrient_bar(name: str, actual: float, target: float, unit: str, pct: float) -> str:
    """生成营养素进度条 HTML"""
    color_class = "green" if 80 <= pct <= 120 else "orange" if 60 <= pct < 80 or 120 < pct <= 140 else "red"
    return f"""
    <div class="nutrient-bar">
        <div class="nutrient-label">
            <span class="nutrient-name">{name}</span>
            <span class="nutrient-value">{actual:.0f} / {target} {unit}</span>
        </div>
        <div class="nutrient-track">
            <div class="nutrient-fill {color_class}" style="width: {min(pct, 150):.0f}%"></div>
        </div>
    </div>"""


if __name__ == "__main__":
    calc = NutritionCalc()
    report = generate_daily_report(calc)
    Path("test_report.html").write_text(report, encoding="utf-8")
    print("测试报告已生成: test_report.html")

#!/usr/bin/env python3
"""
摆摊综合决策报告生成器 - 生成交互式HTML可视化报告
用法: python report_generator.py --output report.html --data '{"products": [...], "profit": {...}, "location": {...}}'
"""

import argparse
import json
import sys
import os
from datetime import datetime
from typing import Dict, Any, List


def generate_html_report(data: Dict[str, Any]) -> str:
    """生成完整的交互式HTML报告"""

    products = data.get("products", [])
    profit = data.get("profit", {})
    location = data.get("location", {})
    user_profile = data.get("user_profile", {})
    weather_tips = data.get("weather_tips", [])
    competitor_analysis = data.get("competitor_analysis", {})
    pain_point_checklist = data.get("pain_point_checklist", [])

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 构建品类推荐卡片
    product_cards = ""
    if products:
        for i, p in enumerate(products[:6]):
            score_color = "#10b981" if p.get("overall_score", 0) >= 75 else ("#f59e0b" if p.get("overall_score", 0) >= 60 else "#ef4444")
            product_cards += f"""
            <div class="product-card" style="border-left: 4px solid {score_color}">
                <div class="product-rank">#{i+1}</div>
                <div class="product-info">
                    <div class="product-name">{p.get('category_icon', '📦')} {p.get('name', '未知品类')}</div>
                    <div class="product-meta">
                        <span class="tag">{p.get('category', '')}</span>
                        <span class="tag">{p.get('difficulty_label', '')}</span>
                        <span class="tag">竞争: {p.get('competition', '未知')}</span>
                    </div>
                    <div class="product-stats">
                        <div class="stat"><strong>¥{p.get('min_budget', 0)}+</strong>启动金</div>
                        <div class="stat"><strong>{p.get('profit_rate', 0)*100:.0f}%</strong>毛利率</div>
                        <div class="stat"><strong>¥{p.get('daily_range', '')}</strong>日流水</div>
                    </div>
                </div>
                <div class="product-score" style="color: {score_color}">{p.get('overall_score', 0)}分</div>
            </div>"""

    # 利润分析区域
    daily = profit.get("daily", {})
    monthly = profit.get("monthly", {})
    breakeven = profit.get("breakeven", {})
    assessment = profit.get("assessment", {})
    payback = profit.get("payback", {})

    profit_html = ""
    if profit:
        margin_pct = daily.get("margin_pct", 0)
        margin_color = "#10b981" if margin_pct >= 35 else ("#f59e0b" if margin_pct >= 20 else "#ef4444")

        # 成本结构条
        cost_bars = ""
        cost_breakdown = daily.get("cost_breakdown", {})
        colors = ["#ef4444", "#f59e0b", "#3b82f6", "#8b5cf6", "#10b981", "#6b7280"]
        for j, (name, pct) in enumerate(cost_breakdown.items()):
            cost_bars += f"""
            <div style="margin-bottom:6px">
                <div style="display:flex;justify-content:space-between;font-size:12px"><span>{name}</span><span>{pct}%</span></div>
                <div style="background:#f3f4f6;border-radius:4px;height:6px;margin-top:2px">
                    <div style="width:{pct}%;height:100%;background:{colors[j % len(colors)]};border-radius:4px"></div>
                </div>
            </div>"""

        profit_html = f"""
        <div class="section">
            <h2>💰 利润精算</h2>
            <div class="profit-grid">
                <div class="profit-card highlight" style="border-color: {margin_color}">
                    <div class="profit-label">日净利润</div>
                    <div class="profit-value" style="color: {margin_color}">¥{daily.get('profit', 0):.2f}</div>
                    <div class="profit-sub">利润率 {margin_pct}%</div>
                </div>
                <div class="profit-card">
                    <div class="profit-label">月利润（出摊{daily.get('working_days', 26) or '26'}天）</div>
                    <div class="profit-value">¥{monthly.get('profit', 0):.2f}</div>
                    <div class="profit-sub">月营收 ¥{monthly.get('revenue', 0):.2f}</div>
                </div>
                <div class="profit-card">
                    <div class="profit-label">盈亏平衡点</div>
                    <div class="profit-value">¥{breakeven.get('daily_revenue_needed', 0):.2f}/天</div>
                    <div class="profit-sub">固定成本 ¥{breakeven.get('fixed_daily_cost', 0):.2f}/天</div>
                </div>
                <div class="profit-card">
                    <div class="profit-label">回本周期</div>
                    <div class="profit-value">{payback.get('days', 'N/A')}天</div>
                    <div class="profit-sub">总投资 ¥{payback.get('total_investment', 0)}</div>
                </div>
            </div>
            <div class="cost-breakdown">
                <h3>成本结构</h3>
                {cost_bars}
            </div>
            <div class="health-badge" style="background: {margin_color}20; border-color: {margin_color}">
                <strong>🏥 {assessment.get('health', '')}</strong>: {assessment.get('advice', '')}
            </div>
            {"".join(f'<div class="tip-item">🔧 {opt}</div>' for opt in assessment.get('optimizations', []))}
        </div>"""

    # 选址评估
    location_html = ""
    if location:
        detail_scores = location.get("detail_scores", {})
        score_bars = ""
        for key, detail in detail_scores.items():
            raw = detail.get("raw_score", 5)
            bar_width = raw * 10
            score_bars += f"""
            <div style="margin-bottom:8px">
                <div style="display:flex;justify-content:space-between;font-size:12px"><span>{detail.get('factor', '')}（权重{detail.get('weight', '')}）</span><span>{raw}/10</span></div>
                <div style="background:#f3f4f6;border-radius:4px;height:8px;margin-top:2px">
                    <div style="width:{bar_width}%;height:100%;background:linear-gradient(90deg,#3b82f6,#10b981);border-radius:4px"></div>
                </div>
            </div>"""

        total_score = location.get("total_score", 0)
        score_color = "#10b981" if total_score >= 65 else ("#f59e0b" if total_score >= 50 else "#ef4444")

        location_html = f"""
        <div class="section">
            <h2>📍 选址评估</h2>
            <div class="location-score" style="text-align:center;margin-bottom:20px">
                <div style="font-size:48px;font-weight:700;color:{score_color}">{total_score}<span style="font-size:20px">/100</span></div>
                <div style="font-size:16px;margin-top:4px">{location.get('grade', '')}</div>
                <div style="color:#6b7280;margin-top:4px">{location.get('advice', '')}</div>
            </div>
            {score_bars}
            <div style="margin-top:16px">
                <h3>行动建议</h3>
                {"".join(f'<div class="tip-item">{item}</div>' for item in location.get('action_items', []))}
            </div>
        </div>"""

    # 天气应对
    weather_html = ""
    if weather_tips:
        weather_html = """
        <div class="section">
            <h2>🌦️ 天气应对策略</h2>
            <div class="weather-grid">
        """ + "".join(f"""
                <div class="weather-card">
                    <div class="weather-icon">{tip.get('icon', '☀️')}</div>
                    <div class="weather-title">{tip.get('condition', '')}</div>
                    <div class="weather-desc">{tip.get('advice', '')}</div>
                </div>
        """ for tip in weather_tips) + """
            </div>
        </div>"""

    # 痛点检查清单
    checklist_html = ""
    if pain_point_checklist:
        checklist_html = """
        <div class="section">
            <h2>✅ 出摊前检查清单</h2>
        """ + "".join(f"""
            <div class="checklist-item">
                <span class="check-box">{'✅' if item.get('checked') else '⬜'}</span>
                <span class="check-label">{item.get('label', '')}</span>
                <span class="check-severity {'p0' if item.get('severity') == 'P0' else 'p1' if item.get('severity') == 'P1' else 'p2'}">{item.get('severity', 'P2')}</span>
            </div>
        """ for item in pain_point_checklist) + """
        </div>"""

    # 竞品分析
    competitor_html = ""
    if competitor_analysis:
        competitors = competitor_analysis.get("nearby_competitors", [])
        comp_rows = ""
        for c in competitors:
            comp_rows += f"""
            <tr>
                <td>{c.get('name', '')}</td>
                <td>{c.get('distance', '')}</td>
                <td>{c.get('price_range', '')}</td>
                <td><span class="tag">{c.get('strength', '')}</span></td>
            </tr>"""

        competitor_html = f"""
        <div class="section">
            <h2>🔍 竞品分析</h2>
            <table class="comp-table">
                <thead><tr><th>竞品名称</th><th>距离</th><th>价格带</th><th>优势</th></tr></thead>
                <tbody>{comp_rows}</tbody>
            </table>
            <div class="tip-item">💡 {competitor_analysis.get('strategy', '建议差异化选品，找到竞品薄弱的市场空白')}</div>
        </div>"""

    # 最终建议
    final_recommendation = data.get("final_recommendation", {})

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>摆摊创业决策报告</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f5f5f5; color: #1f2937; line-height: 1.6; }}
.header {{ background: linear-gradient(135deg, #f97316 0%, #ef4444 100%); color: white; padding: 40px 20px; text-align: center; }}
.header h1 {{ font-size: 28px; margin-bottom: 8px; }}
.header p {{ opacity: 0.9; font-size: 14px; }}
.container {{ max-width: 900px; margin: 0 auto; padding: 20px; }}
.section {{ background: white; border-radius: 12px; padding: 24px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
.section h2 {{ font-size: 20px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #f97316; display: inline-block; }}
.product-card {{ display: flex; align-items: center; padding: 16px; background: #fafafa; border-radius: 8px; margin-bottom: 10px; transition: transform 0.2s; }}
.product-card:hover {{ transform: translateX(4px); box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
.product-rank {{ font-size: 24px; font-weight: 700; color: #d1d5db; min-width: 40px; }}
.product-info {{ flex: 1; margin-left: 12px; }}
.product-name {{ font-size: 16px; font-weight: 600; margin-bottom: 4px; }}
.product-meta {{ display: flex; gap: 6px; margin-bottom: 6px; }}
.tag {{ display: inline-block; padding: 2px 8px; background: #fef3c7; color: #92400e; border-radius: 4px; font-size: 11px; }}
.product-stats {{ display: flex; gap: 16px; font-size: 13px; color: #6b7280; }}
.stat strong {{ color: #1f2937; }}
.product-score {{ font-size: 20px; font-weight: 700; min-width: 60px; text-align: center; }}
.profit-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-bottom: 20px; }}
.profit-card {{ background: #fafafa; border: 2px solid #e5e7eb; border-radius: 10px; padding: 16px; text-align: center; }}
.profit-card.highlight {{ border-width: 3px; }}
.profit-label {{ font-size: 12px; color: #6b7280; margin-bottom: 4px; }}
.profit-value {{ font-size: 24px; font-weight: 700; margin-bottom: 4px; }}
.profit-sub {{ font-size: 12px; color: #9ca3af; }}
.cost-breakdown {{ background: #fafafa; border-radius: 8px; padding: 16px; margin: 16px 0; }}
.health-badge {{ padding: 12px 16px; border-radius: 8px; border: 1px solid; margin: 12px 0; font-size: 14px; }}
.tip-item {{ padding: 8px 12px; background: #fef3c7; border-radius: 6px; margin-bottom: 6px; font-size: 13px; }}
.weather-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; }}
.weather-card {{ background: #f0f9ff; border-radius: 10px; padding: 16px; text-align: center; }}
.weather-icon {{ font-size: 32px; margin-bottom: 8px; }}
.weather-title {{ font-weight: 600; margin-bottom: 4px; }}
.weather-desc {{ font-size: 12px; color: #6b7280; }}
.checklist-item {{ display: flex; align-items: center; gap: 12px; padding: 10px 0; border-bottom: 1px solid #f3f4f6; }}
.check-box {{ font-size: 18px; }}
.check-label {{ flex: 1; font-size: 14px; }}
.check-severity {{ padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; }}
.check-severity.p0 {{ background: #fecaca; color: #991b1b; }}
.check-severity.p1 {{ background: #fed7aa; color: #9a3412; }}
.check-severity.p2 {{ background: #fef3c7; color: #92400e; }}
.comp-table {{ width: 100%; border-collapse: collapse; margin: 12px 0; }}
.comp-table th {{ background: #fef3c7; padding: 10px; text-align: left; font-size: 13px; }}
.comp-table td {{ padding: 10px; border-bottom: 1px solid #f3f4f6; font-size: 13px; }}
.final-section {{ background: linear-gradient(135deg, #fef3c7 0%, #fef9c3 100%); border: 2px solid #f59e0b; }}
.final-section h2 {{ border-bottom-color: #f59e0b; }}
.recommendation-card {{ background: white; border-radius: 8px; padding: 16px; margin-bottom: 10px; border-left: 4px solid #f97316; }}
.rec-title {{ font-weight: 700; font-size: 16px; margin-bottom: 4px; }}
.rec-desc {{ font-size: 13px; color: #6b7280; }}
.footer {{ text-align: center; padding: 30px; color: #9ca3af; font-size: 12px; }}
.quick-actions {{ display: flex; gap: 10px; margin-top: 16px; flex-wrap: wrap; }}
.btn {{ padding: 8px 16px; border: none; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 500; }}
.btn-primary {{ background: #f97316; color: white; }}
.btn-secondary {{ background: #fef3c7; color: #92400e; }}
@media print {{ body {{ background: white; }} .section {{ box-shadow: none; border: 1px solid #e5e7eb; }} }}
</style>
</head>
<body>
<div class="header">
    <h1>🛒 摆摊创业决策报告</h1>
    <p>生成时间: {now} | 基于市场调研数据与经营模型分析</p>
</div>

<div class="container">
    <!-- 用户画像 -->
    {f'''<div class="section">
        <h2>👤 你的画像</h2>
        <div class="product-stats" style="gap:24px;">
            <div class="stat"><strong>预算:</strong> ¥{user_profile.get('budget', '--')}</div>
            <div class="stat"><strong>城市:</strong> {user_profile.get('city_type', '--')}</div>
            <div class="stat"><strong>季节:</strong> {user_profile.get('season', '--')}</div>
            <div class="stat"><strong>经验:</strong> {user_profile.get('experience', '--')}</div>
        </div>
    </div>''' if user_profile else ''}

    <!-- 品类推荐 -->
    {f'''<div class="section">
        <h2>🎯 品类推荐 Top {min(len(products), 6)}</h2>
        {product_cards}
    </div>''' if products else ''}

    <!-- 利润分析 -->
    {profit_html}

    <!-- 选址评估 -->
    {location_html}

    <!-- 天气策略 -->
    {weather_html}

    <!-- 竞品分析 -->
    {competitor_html}

    <!-- 检查清单 -->
    {checklist_html}

    <!-- 最终建议 -->
    {f'''<div class="section final-section">
        <h2>🏁 最终建议</h2>
        {"".join(f'<div class="recommendation-card"><div class="rec-title">{r.get("title", "")}</div><div class="rec-desc">{r.get("description", "")}</div></div>' for r in final_recommendation.get('recommendations', []))}
        <div class="tip-item" style="margin-top:12px">💪 {final_recommendation.get('motivation', '摆摊是微型创业，关键在于快速验证+持续优化。先小规模试水，跑通模型再放大！')}</div>
    </div>''' if final_recommendation else ''}

    <div class="footer">
        <p>📊 数据来源：2025年市场调研 | ⚠️ 报告仅供参考，具体经营请结合当地实际情况</p>
        <p>摆摊创业助手 · 让每一次出摊都心中有数</p>
    </div>
</div>

<script>
// 交互功能：点击品类卡片展开详情
document.querySelectorAll('.product-card').forEach(card => {{
    card.style.cursor = 'pointer';
    card.addEventListener('click', function() {{
        this.classList.toggle('expanded');
    }});
}});
</script>

</body>
</html>"""

    return html


def main():
    parser = argparse.ArgumentParser(description="摆摊综合决策报告生成器")
    parser.add_argument("--output", type=str, default="baitan_report.html", help="输出HTML文件路径")
    parser.add_argument("--data", type=str, default="{}", help="JSON数据字符串")
    parser.add_argument("--data-file", type=str, default="", help="从JSON文件读取数据")

    args = parser.parse_args()

    data = {}
    if args.data_file:
        with open(args.data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        try:
            data = json.loads(args.data)
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}", file=sys.stderr)
            sys.exit(1)

    html = generate_html_report(data)

    output_path = args.output
    if not os.path.isabs(output_path):
        output_path = os.path.join(os.getcwd(), output_path)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ 报告已生成: {output_path}")
    print(f"   文件大小: {len(html)} 字符")


if __name__ == "__main__":
    main()

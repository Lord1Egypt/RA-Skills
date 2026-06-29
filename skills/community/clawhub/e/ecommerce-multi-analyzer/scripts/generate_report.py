#!/usr/bin/env python3
"""
电商多平台商品数据分析报告生成器
输入：JSON数据文件
输出：交互式HTML分析报告
"""

import json
import sys
import os
from datetime import datetime

# --- 平台配色方案 ---
PLATFORM_COLORS = {
    "京东":   {"bg": "#E4393C", "text": "#FFFFFF"},
    "淘宝":   {"bg": "#FF5000", "text": "#FFFFFF"},
    "天猫":   {"bg": "#FF0036", "text": "#FFFFFF"},
    "拼多多": {"bg": "#E02E24", "text": "#FFFFFF"},
    "抖音电商": {"bg": "#010101", "text": "#FFFFFF"},
    "1688":   {"bg": "#FF6A00", "text": "#FFFFFF"},
    "苏宁易购": {"bg": "#FFCC00", "text": "#333333"},
    "唯品会": {"bg": "#DE3D96", "text": "#FFFFFF"},
}

PLATFORM_ICONS = {
    "京东": "📦", "淘宝": "🛒", "天猫": "🐱", "拼多多": "🔪",
    "抖音电商": "🎵", "1688": "🏭", "苏宁易购": "🦁", "唯品会": "💄",
}


def load_data(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def fmt_price(p):
    if p is None:
        return "暂无"
    return f"¥{p:,.2f}"


def fmt_count(n):
    if n is None:
        return "暂无"
    if n >= 10000:
        return f"{n/10000:.1f}万"
    return str(n)


def rating_stars(rating):
    if rating is None:
        return "暂无评分"
    full = int(rating)
    half = 1 if rating - full >= 0.5 else 0
    empty = 5 - full - half
    return "★" * full + "☆" * empty + f" {rating}"


def platform_badge(platform):
    c = PLATFORM_COLORS.get(platform, {"bg": "#666", "text": "#FFF"})
    icon = PLATFORM_ICONS.get(platform, "🏪")
    return f'<span style="background:{c["bg"]};color:{c["text"]};padding:4px 10px;border-radius:20px;font-size:13px;font-weight:600;display:inline-block;margin:2px;">{icon} {platform}</span>'


def generate_html(data):
    src = data.get("source_product", {})
    cross = data.get("cross_platform", [])
    analysis = data.get("analysis", {})
    advice = data.get("advice", {})

    all_platforms = [src] + cross
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # --- 价格对比数据 (for Chart.js) ---
    price_labels = []
    price_data = []
    price_colors = []
    score_labels = []
    score_data = []
    score_colors = []

    for p in all_platforms:
        plat = p.get("platform", "未知")
        price = p.get("price")
        rating = p.get("rating")
        color = PLATFORM_COLORS.get(plat, {"bg": "#666"})["bg"]
        icon = PLATFORM_ICONS.get(plat, "🏪")

        if price:
            price_labels.append(f"{icon} {plat}")
            price_data.append(price)
            price_colors.append(color)
        if rating:
            score_labels.append(f"{icon} {plat}")
            score_data.append(rating)
            score_colors.append(color)

    # 推荐平台高亮
    rec_plat = analysis.get("best_value", {}).get("platform", "")
    low_plat = analysis.get("lowest_price", {}).get("platform", "")
    high_plat = analysis.get("highest_price", {}).get("platform", "")

    # 构建平台卡片
    def build_platform_card(p, highlight=""):
        plat = p.get("platform", "未知")
        icon = PLATFORM_ICONS.get(plat, "🏪")
        color = PLATFORM_COLORS.get(plat, {"bg": "#333", "text": "#FFF"})
        is_highlight = plat == highlight
        border = f'border: 3px solid {color["bg"]};' if is_highlight else ""
        badge_class = "highlight-card" if is_highlight else ""

        price = p.get("price")
        orig_price = p.get("original_price")
        rating = p.get("rating")
        reviews = p.get("review_count")
        shop = p.get("shop_name", "未知店铺")
        note = p.get("note", "")
        url = p.get("url", "")

        price_html = ""
        if price:
            price_html += f'<div class="card-price">{fmt_price(price)}</div>'
            if orig_price and orig_price > price:
                discount = int((1 - price / orig_price) * 100)
                price_html += f'<div class="card-orig">{fmt_price(orig_price)} <span class="discount-tag">-{discount}%</span></div>'

        stars = rating_stars(rating) if rating else "暂无评分"

        return f'''
        <div class="platform-card {badge_class}" style="{border}">
            <div class="card-header">
                {platform_badge(plat)}
                {f'<span class="best-tag">🏆 最推荐</span>' if is_highlight else ''}
            </div>
            <div class="card-title">{p.get("title", "未知商品")}</div>
            {price_html}
            <div class="card-stars">{stars}</div>
            <div class="card-meta">
                <span>📝 {fmt_count(reviews)} 评价</span>
                <span>🏪 {shop}</span>
            </div>
            {f'<div class="card-note">📌 {note}</div>' if note else ''}
            {f'<a href="{url}" target="_blank" class="card-link">🔗 查看商品</a>' if url else ''}
        </div>
        '''

    cards_html = ""
    # 源商品卡片
    cards_html += build_platform_card(src, rec_plat)
    # 跨平台商品卡片
    for p in cross:
        cards_html += build_platform_card(p, rec_plat)

    # 购买建议
    advice_html = ""
    if advice:
        watch_items = ""
        for w in advice.get("watch_out", []):
            watch_items += f"<li>{w}</li>"

        advice_html = f'''
        <div class="advice-section">
            <div class="advice-header">💡 购买建议</div>
            <div class="advice-recommend">
                <span class="advice-label">{advice.get("buy_recommendation", "")}</span>
                <p>{advice.get("reason", "")}</p>
            </div>
            {f'<div class="advice-watch"><strong>⚠️ 注意事项：</strong><ul>{watch_items}</ul></div>' if watch_items else ''}
            {f'<div class="advice-trend">📈 {advice.get("price_trend_note", "")}</div>' if advice.get("price_trend_note") else ''}
        </div>
        '''

    # 分析指标卡片
    lowest = analysis.get("lowest_price", {})
    highest = analysis.get("highest_price", {})
    best_rated = analysis.get("best_rated", {})

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>电商多平台商品分析报告</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 30px 20px; }}
.container {{ max-width: 1100px; margin: 0 auto; }}

/* Header */
.report-header {{ background: rgba(255,255,255,0.95); border-radius: 20px; padding: 35px 40px; margin-bottom: 25px; box-shadow: 0 20px 60px rgba(0,0,0,0.15); text-align: center; }}
.report-header h1 {{ font-size: 32px; font-weight: 800; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 8px; }}
.report-header .subtitle {{ color: #888; font-size: 14px; }}
.report-header .product-title {{ font-size: 20px; color: #333; margin-top: 12px; font-weight: 600; }}

/* KPI Grid */
.kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 25px; }}
@media (max-width: 768px) {{ .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
.kpi-card {{ background: rgba(255,255,255,0.95); border-radius: 16px; padding: 22px; text-align: center; box-shadow: 0 8px 30px rgba(0,0,0,0.08); transition: transform 0.2s; }}
.kpi-card:hover {{ transform: translateY(-3px); }}
.kpi-value {{ font-size: 30px; font-weight: 800; color: #333; }}
.kpi-label {{ font-size: 13px; color: #999; margin-top: 6px; }}
.kpi-lowest {{ color: #27ae60; }}
.kpi-highest {{ color: #e74c3c; }}
.kpi-spread {{ color: #f39c12; }}
.kpi-bestrated {{ color: #667eea; }}

/* Charts Row */
.charts-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 25px; }}
@media (max-width: 768px) {{ .charts-row {{ grid-template-columns: 1fr; }} }}
.chart-box {{ background: rgba(255,255,255,0.95); border-radius: 16px; padding: 25px; box-shadow: 0 8px 30px rgba(0,0,0,0.08); }}
.chart-box h3 {{ font-size: 16px; color: #555; margin-bottom: 15px; font-weight: 600; }}
.chart-box canvas {{ max-height: 280px; }}

/* Platform Cards */
.platform-cards {{ margin-bottom: 25px; }}
.platform-cards h3 {{ font-size: 18px; color: #fff; margin-bottom: 15px; font-weight: 600; display: flex; align-items: center; gap: 8px; }}
.platform-card {{ background: rgba(255,255,255,0.95); border-radius: 14px; padding: 20px 24px; margin-bottom: 12px; box-shadow: 0 6px 20px rgba(0,0,0,0.06); transition: all 0.2s; border: 2px solid transparent; }}
.platform-card:hover {{ transform: translateX(4px); box-shadow: 0 10px 30px rgba(0,0,0,0.12); }}
.highlight-card {{ background: linear-gradient(135deg, #fef9e7, #fdebd0); }}
.card-header {{ display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }}
.best-tag {{ background: linear-gradient(135deg, #f39c12, #e67e22); color: #fff; padding: 3px 12px; border-radius: 12px; font-size: 12px; font-weight: 700; animation: pulse 2s infinite; }}
@keyframes pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0.7; }} }}
.card-title {{ font-size: 15px; color: #333; font-weight: 500; margin-bottom: 8px; line-height: 1.5; }}
.card-price {{ font-size: 26px; font-weight: 800; color: #e74c3c; display: inline-block; margin-right: 12px; }}
.card-orig {{ font-size: 14px; color: #999; text-decoration: line-through; display: inline-block; }}
.discount-tag {{ background: #e74c3c; color: #fff; font-size: 11px; padding: 2px 8px; border-radius: 8px; text-decoration: none; font-weight: 600; margin-left: 4px; }}
.card-stars {{ font-size: 14px; color: #f39c12; margin: 6px 0; }}
.card-meta {{ display: flex; gap: 16px; font-size: 13px; color: #888; margin: 6px 0; }}
.card-note {{ font-size: 13px; color: #666; background: #f0f0f0; padding: 6px 12px; border-radius: 8px; margin-top: 8px; }}
.card-link {{ display: inline-block; margin-top: 8px; color: #667eea; text-decoration: none; font-size: 13px; font-weight: 500; }}
.card-link:hover {{ text-decoration: underline; }}

/* Advice */
.advice-section {{ background: rgba(255,255,255,0.95); border-radius: 16px; padding: 30px; margin-bottom: 25px; box-shadow: 0 8px 30px rgba(0,0,0,0.08); }}
.advice-header {{ font-size: 22px; font-weight: 700; color: #333; margin-bottom: 18px; }}
.advice-recommend {{ background: linear-gradient(135deg, #27ae60, #2ecc71); color: #fff; padding: 20px 24px; border-radius: 12px; margin-bottom: 16px; }}
.advice-label {{ font-size: 18px; font-weight: 700; display: block; margin-bottom: 6px; }}
.advice-recommend p {{ font-size: 14px; opacity: 0.95; line-height: 1.6; }}
.advice-watch {{ background: #fef9e7; padding: 16px 20px; border-radius: 10px; border-left: 4px solid #f39c12; margin-bottom: 12px; }}
.advice-watch ul {{ margin: 6px 0 0 18px; line-height: 1.8; font-size: 14px; color: #666; }}
.advice-trend {{ font-size: 14px; color: #667eea; background: #f0f4ff; padding: 12px 16px; border-radius: 10px; }}

/* Footer */
.report-footer {{ text-align: center; padding: 20px; color: rgba(255,255,255,0.6); font-size: 12px; }}
</style>
</head>
<body>
<div class="container">

    <!-- Header -->
    <div class="report-header">
        <h1>📊 电商多平台商品分析报告</h1>
        <div class="subtitle">生成时间：{now} | AI 自动化分析</div>
        <div class="product-title">🎯 {src.get("title", "未知商品")}</div>
    </div>

    <!-- KPI Cards -->
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-value kpi-lowest">{fmt_price(lowest.get("price"))}</div>
            <div class="kpi-label">💰 最低价 ({lowest.get("platform", "N/A")})</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-value kpi-highest">{fmt_price(highest.get("price"))}</div>
            <div class="kpi-label">📈 最高价 ({highest.get("platform", "N/A")})</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-value kpi-spread">{analysis.get("price_spread_pct", 0):.1f}%</div>
            <div class="kpi-label">📉 价差幅度</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-value kpi-bestrated">★ {best_rated.get("rating", "-")}</div>
            <div class="kpi-label">⭐ 最高评分 ({best_rated.get("platform", "N/A")})</div>
        </div>
    </div>

    <!-- Charts -->
    <div class="charts-row">
        <div class="chart-box">
            <h3>💲 各平台价格对比</h3>
            <canvas id="priceChart"></canvas>
        </div>
        <div class="chart-box">
            <h3>⭐ 各平台评分对比</h3>
            <canvas id="scoreChart"></canvas>
        </div>
    </div>

    <!-- Platform Detail Cards -->
    <div class="platform-cards">
        <h3>🛍️ 各平台商品详情</h3>
        {cards_html}
    </div>

    <!-- Buying Advice -->
    {advice_html}

    <!-- Source Link -->
    <div class="report-footer">
        数据来源：各电商平台公开信息 | 报告由 AI 自动生成，仅供参考 | {now}
    </div>
</div>

<script>
// 价格对比柱状图
const priceCtx = document.getElementById('priceChart').getContext('2d');
new Chart(priceCtx, {{
    type: 'bar',
    data: {{
        labels: {json.dumps(price_labels, ensure_ascii=False)},
        datasets: [{{
            label: '价格 (¥)',
            data: {json.dumps(price_data)},
            backgroundColor: {json.dumps(price_colors)},
            borderRadius: 8,
            borderSkipped: false,
        }}]
    }},
    options: {{
        responsive: true,
        maintainAspectRatio: true,
        plugins: {{
            legend: {{ display: false }},
            tooltip: {{
                callbacks: {{
                    label: function(ctx) {{ return '¥' + ctx.parsed.y.toFixed(2); }}
                }}
            }}
        }},
        scales: {{
            y: {{
                beginAtZero: false,
                ticks: {{ callback: function(v) {{ return '¥' + v; }} }},
                grid: {{ color: '#f0f0f0' }}
            }},
            x: {{ grid: {{ display: false }} }}
        }}
    }}
}});

// 评分对比雷达图
const scoreCtx = document.getElementById('scoreChart').getContext('2d');
new Chart(scoreCtx, {{
    type: 'bar',
    data: {{
        labels: {json.dumps(score_labels, ensure_ascii=False)},
        datasets: [{{
            label: '评分 (满分5.0)',
            data: {json.dumps(score_data)},
            backgroundColor: {json.dumps(score_colors)},
            borderRadius: 8,
            borderSkipped: false,
        }}]
    }},
    options: {{
        responsive: true,
        maintainAspectRatio: true,
        plugins: {{
            legend: {{ display: false }},
        }},
        scales: {{
            y: {{
                min: 4.0,
                max: 5.0,
                ticks: {{ stepSize: 0.2, callback: function(v) {{ return v.toFixed(1); }} }},
                grid: {{ color: '#f0f0f0' }}
            }},
            x: {{ grid: {{ display: false }} }}
        }}
    }}
}});
</script>
</body>
</html>'''

    return html


def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_report.py <input_json> <output_html>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)

    data = load_data(input_file)
    html = generate_html(data)

    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Report generated: {output_file}")
    print(f"File size: {len(html):,} bytes")


if __name__ == "__main__":
    main()

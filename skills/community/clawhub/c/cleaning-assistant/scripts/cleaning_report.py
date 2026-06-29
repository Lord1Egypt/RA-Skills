#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能保洁助手 - HTML可视化报告生成器
月度保洁报告：概览卡片 + 频次热力图 + 房间分布饼图 + 耗时趋势 + 记录列表
"""

import json
import sys
from pathlib import Path
from datetime import datetime, date
from calendar import monthrange

# Fix Windows GBK encoding for emoji output
import io
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SKILL_DIR = Path(__file__).parent.parent


def generate_report(year: int, month: int, summary: dict, entries: list) -> str:
    """生成月度保洁报告HTML"""

    total_count = summary.get("total_count", 0)
    total_duration = summary.get("total_duration", 0)
    avg_duration = summary.get("avg_duration", 0)
    active_days = summary.get("active_days", 0)
    daily = summary.get("daily", [])
    rooms = summary.get("rooms", {})

    # 本月天数
    _, days_in_month = monthrange(year, month)

    # 评分
    score, score_label, score_color = _calc_score(total_count, active_days, days_in_month)

    # 房间颜色映射
    room_colors = {
        "厨房": "#ff6b6b", "卫生间": "#4ecdc4", "客厅": "#45b7d1",
        "卧室": "#96ceb4", "阳台": "#ffeaa7", "书房": "#dfe6e9",
        "玄关": "#fab1a0", "储物间": "#a29bfe", "全屋": "#6c5ce7",
    }

    # 房间饼图数据
    room_labels = json.dumps(list(rooms.keys()), ensure_ascii=False)
    room_counts = json.dumps([rooms[r]["count"] for r in rooms])
    room_durations = json.dumps([rooms[r]["duration"] for r in rooms])
    room_colors_js = json.dumps([room_colors.get(r, "#b2bec3") for r in rooms])

    # 热力图数据 - 本月每一天
    daily_map = {}
    for d in daily:
        day = int(d["date"].split("-")[2]) if "-" in d["date"] else 0
        daily_map[day] = d["cnt"]

    heatmap_data = []
    for day in range(1, days_in_month + 1):
        cnt = daily_map.get(day, 0)
        dur_val = 0
        for d in daily:
            if d["date"]:
                d_day = int(d["date"].split("-")[2]) if "-" in d["date"] else 0
                if d_day == day:
                    dur_val = d["dur"]
                    break
        heatmap_data.append({
            "day": day,
            "count": cnt,
            "duration": dur_val,
            "color": _heat_color(cnt),
        })

    # 日趋势图数据
    trend_dates = json.dumps([f"{day}日" for day in range(1, days_in_month + 1)], ensure_ascii=False)
    trend_counts = json.dumps([daily_map.get(day, 0) for day in range(1, days_in_month + 1)])

    # 记录表格
    table_rows = ""
    for e in entries[:30]:
        rooms_display = e.get("rooms", "")
        duration = e.get("duration_min", 0)
        hours = duration // 60
        mins = duration % 60
        dur_display = f"{hours}小时{mins}分" if hours > 0 else f"{mins}分钟"
        note = e.get("note", "")[:20] or "-"
        table_rows += f"""
        <tr>
            <td>{e.get('date', '')}</td>
            <td><span class="room-tag">{rooms_display}</span></td>
            <td>{dur_display}</td>
            <td>{note}</td>
        </tr>"""

    # 热门房间Top5
    top_rooms = sorted(rooms.items(), key=lambda x: -x[1]["count"])[:5]
    top_rooms_html = ""
    for i, (r_name, r_data) in enumerate(top_rooms):
        rank = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i]
        color = room_colors.get(r_name, "#b2bec3")
        top_rooms_html += f"""
        <div class="top-room">
            <span class="rank">{rank}</span>
            <span class="room-name" style="color:{color}">{r_name}</span>
            <span class="room-stat">{r_data['count']}次 · {r_data['duration']}分钟</span>
        </div>"""

    # AI建议
    tips = _generate_tips(total_count, active_days, days_in_month, rooms, avg_duration)
    tips_html = "\n".join([f'<div class="tip-item">{t}</div>' for t in tips])

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{year}年{month}月 保洁报告</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei', sans-serif;
    background: linear-gradient(135deg, #f5f7fa 0%, #e8f4f8 100%);
    padding: 20px;
    min-height: 100vh;
    color: #2d3436;
}}
.container {{ max-width: 800px; margin: 0 auto; }}

.header {{
    text-align: center;
    padding: 30px 20px;
    background: white;
    border-radius: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}}
.header .icon {{ font-size: 48px; margin-bottom: 8px; }}
.header h1 {{ font-size: 26px; font-weight: 800; color: #2d3436; }}
.header .subtitle {{ color: #636e72; font-size: 14px; margin-top: 4px; }}

.score-card {{
    background: linear-gradient(135deg, {score_color} 0%, {score_color}dd 100%);
    border-radius: 20px;
    padding: 28px;
    color: white;
    margin-bottom: 20px;
    box-shadow: 0 8px 25px {score_color}44;
    display: flex;
    align-items: center;
    justify-content: space-between;
}}
.score-num {{ font-size: 56px; font-weight: 900; line-height: 1; }}
.score-label {{ font-size: 18px; opacity: 0.9; margin-top: 4px; }}
.score-detail {{ text-align: right; font-size: 13px; opacity: 0.85; line-height: 1.8; }}

.stats-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 20px;
}}
.stat-card {{
    background: white;
    border-radius: 16px;
    padding: 18px 14px;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}}
.stat-card .stat-value {{ font-size: 28px; font-weight: 800; color: #2d3436; }}
.stat-card .stat-label {{ font-size: 12px; color: #636e72; margin-top: 4px; }}
.stat-card .stat-emoji {{ font-size: 20px; margin-bottom: 4px; }}

.chart-section {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 20px;
}}
.chart-card {{
    background: white;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}}
.chart-card h3 {{ font-size: 15px; color: #2d3436; margin-bottom: 14px; font-weight: 700; }}
.chart-box {{ height: 220px; }}

.chart-full {{
    background: white;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}}
.chart-full h3 {{ font-size: 15px; color: #2d3436; margin-bottom: 14px; font-weight: 700; }}

.heatmap {{
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    margin-top: 8px;
}}
.heat-cell {{
    width: 32px;
    height: 32px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    color: #fff;
    font-weight: 600;
    cursor: default;
    position: relative;
    transition: transform 0.2s;
}}
.heat-cell:hover {{ transform: scale(1.2); z-index: 10; }}
.heat-cell.empty {{ background: #f0f0f0; color: #ccc; }}

.top-rooms {{
    margin-bottom: 20px;
}}
.top-room {{
    background: white;
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}}
.top-room .rank {{ font-size: 20px; }}
.top-room .room-name {{ font-weight: 700; font-size: 15px; }}
.top-room .room-stat {{ margin-left: auto; color: #636e72; font-size: 13px; }}

.records-table {{
    width: 100%;
    border-collapse: collapse;
    background: white;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    margin-bottom: 20px;
}}
.records-table th {{
    background: #f8f9fa;
    padding: 12px 16px;
    text-align: left;
    font-size: 12px;
    color: #636e72;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}
.records-table td {{
    padding: 12px 16px;
    border-top: 1px solid #f0f0f0;
    font-size: 13px;
}}
.records-table tr:hover td {{ background: #f8f9fa; }}
.room-tag {{
    display: inline-block;
    background: #e8f4f8;
    color: #2d9cdb;
    padding: 2px 10px;
    border-radius: 10px;
    font-size: 12px;
    font-weight: 500;
}}

.tips-section {{
    background: white;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}}
.tips-section h3 {{ font-size: 15px; color: #2d3436; margin-bottom: 12px; font-weight: 700; }}
.tip-item {{
    padding: 10px 14px;
    margin-bottom: 8px;
    background: #f0fdf4;
    border-radius: 10px;
    font-size: 13px;
    color: #166534;
    border-left: 3px solid #22c55e;
    line-height: 1.6;
}}
.tip-item.warn {{
    background: #fef2f2;
    color: #991b1b;
    border-left-color: #ef4444;
}}

.footer {{
    text-align: center;
    color: #b2bec3;
    font-size: 12px;
    padding: 20px 0;
}}

@media (max-width: 640px) {{
    .stats-grid {{ grid-template-columns: repeat(2, 1fr); }}
    .chart-section {{ grid-template-columns: 1fr; }}
    .score-card {{ flex-direction: column; text-align: center; gap: 12px; }}
    .score-detail {{ text-align: center; }}
}}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="icon">🧹</div>
        <h1>{year}年{month}月 保洁报告</h1>
        <div class="subtitle">让家保持干净整洁 🏠✨</div>
    </div>

    <div class="score-card">
        <div>
            <div class="score-num">{score}</div>
            <div class="score-label">{score_label}</div>
        </div>
        <div class="score-detail">
            本月保洁 {total_count} 次<br>
            活跃 {active_days} 天 / {days_in_month} 天<br>
            总耗时 {total_duration//60}小时{total_duration%60}分钟
        </div>
    </div>

    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-emoji">📋</div>
            <div class="stat-value">{total_count}</div>
            <div class="stat-label">保洁次数</div>
        </div>
        <div class="stat-card">
            <div class="stat-emoji">⏱️</div>
            <div class="stat-value">{total_duration//60:.0f}时{total_duration%60:02d}分</div>
            <div class="stat-label">总耗时</div>
        </div>
        <div class="stat-card">
            <div class="stat-emoji">📅</div>
            <div class="stat-value">{active_days}</div>
            <div class="stat-label">活跃天数</div>
        </div>
        <div class="stat-card">
            <div class="stat-emoji">⚡</div>
            <div class="stat-value">{avg_duration:.0f}分</div>
            <div class="stat-label">平均每次</div>
        </div>
    </div>

    {"".join(top_rooms_html) if top_rooms_html else ''}
    {
    f'''<div class="top-room">
            <span class="rank">📊</span>
            <span class="room-name" style="color:#636e72">暂无记录</span>
            <span class="room-stat">开始记录你的第一次保洁吧</span>
        </div>''' if not top_rooms_html else ''
    }

    <div class="chart-section">
        <div class="chart-card">
            <h3>🏠 房间清洁次数分布</h3>
            <div class="chart-box">
                <canvas id="roomPieChart"></canvas>
            </div>
        </div>
        <div class="chart-card">
            <h3>⏱️ 房间清洁耗时分布</h3>
            <div class="chart-box">
                <canvas id="durationPieChart"></canvas>
            </div>
        </div>
    </div>

    <div class="chart-full">
        <h3>📅 本月每日保洁频次</h3>
        <div class="chart-box" style="height:200px;">
            <canvas id="trendChart"></canvas>
        </div>
    </div>

    <div class="chart-full">
        <h3>🗓️ 保洁热力图</h3>
        <div style="font-size:12px; color:#636e72; margin-bottom:10px;">
            颜色越深 = 保洁次数越多 | 鼠标悬停查看详情
        </div>
        <div class="heatmap">
            {"".join([
                f'<div class="heat-cell {"empty" if h["count"]==0 else ""}" '
                f'style="background:{h["color"]}" '
                f'title="{month}月{h["day"]}日: {"无记录" if h["count"]==0 else f"{h["count"]}次, {h["duration"]}分钟"}"'
                f'>'
                f'{"-" if h["count"]==0 else h["day"]}'
                f'</div>'
                for h in heatmap_data
            ])}
        </div>
    </div>

    <div class="tips-section">
        <h3>💡 AI 保洁建议</h3>
        {tips_html}
    </div>

    <div style="background:white;border-radius:16px;padding:16px 20px;margin-bottom:20px;box-shadow:0 2px 10px rgba(0,0,0,0.04);">
        <h3 style="font-size:15px;color:#2d3436;margin-bottom:12px;font-weight:700;">📋 最近保洁记录</h3>
        <table class="records-table">
            <thead>
                <tr><th>日期</th><th>区域</th><th>耗时</th><th>备注</th></tr>
            </thead>
            <tbody>
                {table_rows if table_rows else '<tr><td colspan="4" style="text-align:center;color:#b2bec3;padding:40px;">本月暂无保洁记录 🧹<br>试试说"今天打扫了厨房"来记录吧</td></tr>'}
            </tbody>
        </table>
    </div>

    <div class="footer">由 WorkBuddy 智能保洁助手生成 · {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
</div>

<script>
// 房间清洁次数饼图
new Chart(document.getElementById('roomPieChart'), {{
    type: 'doughnut',
    data: {{
        labels: {room_labels},
        datasets: [{{
            data: {room_counts},
            backgroundColor: {room_colors_js},
            borderWidth: 0,
        }}]
    }},
    options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{
            legend: {{
                position: 'bottom',
                labels: {{ boxWidth: 10, padding: 12, font: {{ size: 11 }} }}
            }}
        }}
    }}
}});

// 房间清洁耗时饼图
new Chart(document.getElementById('durationPieChart'), {{
    type: 'doughnut',
    data: {{
        labels: {room_labels},
        datasets: [{{
            data: {room_durations},
            backgroundColor: {room_colors_js},
            borderWidth: 0,
        }}]
    }},
    options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{
            legend: {{
                position: 'bottom',
                labels: {{ boxWidth: 10, padding: 12, font: {{ size: 11 }} }}
            }}
        }}
    }}
}});

// 日趋势图
new Chart(document.getElementById('trendChart'), {{
    type: 'bar',
    data: {{
        labels: {trend_dates},
        datasets: [{{
            label: '保洁次数',
            data: {trend_counts},
            backgroundColor: {trend_counts}.map(v => {{
                if (v >= 2) return '#22c55e';
                if (v >= 1) return '#4ecdc4';
                return '#e5e7eb';
            }}),
            borderRadius: 6,
            borderSkipped: false,
        }}]
    }},
    options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{ legend: {{ display: false }} }},
        scales: {{
            y: {{
                beginAtZero: true,
                max: Math.max(3, ...{trend_counts}),
                ticks: {{ stepSize: 1, font: {{ size: 11 }} }},
                grid: {{ color: '#f0f0f0' }}
            }},
            x: {{
                grid: {{ display: false }},
                ticks: {{ font: {{ size: 10 }}, maxRotation: 0 }}
            }}
        }}
    }}
}});
</script>
</body>
</html>"""

    return html


def _calc_score(count: int, active_days: int, days_in_month: int) -> tuple:
    """计算月度保洁评分 0-100"""
    if count == 0:
        return 0, "还没开始", "#b2bec3"
    ratio = active_days / days_in_month
    score = min(100, int(count * 4 + ratio * 40))
    if score >= 80:
        return score, "清洁达人 🏆", "#22c55e"
    elif score >= 60:
        return score, "做得不错 👍", "#4ecdc4"
    elif score >= 30:
        return score, "继续加油 💪", "#f59e0b"
    return score, "刚起步 🌱", "#f97316"


def _heat_color(count: int) -> str:
    """热力图颜色"""
    if count == 0:
        return "#f0f0f0"
    elif count == 1:
        return "#a8e6cf"
    elif count == 2:
        return "#4ecdc4"
    elif count == 3:
        return "#2d9cdb"
    else:
        return "#1a5276"


def _generate_tips(count: int, active_days: int, days_in_month: int,
                   rooms: dict, avg_duration: float) -> list:
    """生成AI建议"""
    tips = []

    if count == 0:
        tips.append("本月还没有保洁记录！哪怕每天花5分钟整理桌面，也是好的开始 🌱")
        tips.append("试试从厨房和卫生间开始，这两个区域最需要定期清洁")
        return tips

    ratio = active_days / days_in_month

    if ratio >= 0.8:
        tips.append("🌟 太棒了！本月几乎每天都保持了清洁，卫生习惯非常好")
    elif ratio >= 0.5:
        tips.append("👍 本月保洁频率不错，保持下去就能养成好习惯")
    elif ratio >= 0.3:
        tips.append("💡 保洁频率建议提升，可以从小区域开始，每天15分钟就好")
    else:
        tips.append("📅 本月保洁频率偏低，建议制定一个固定的保洁时间，比如每周日上午")

    if avg_duration > 90:
        tips.append("⏱️ 单次保洁时间较长，可以考虑分时段清洁，避免一次太累")
    elif avg_duration < 15:
        tips.append("⚡ 单次保洁时间较短，下次试试多花点时间做深度清洁")

    # 房间建议
    room_names = list(rooms.keys())
    if "厨房" not in room_names:
        tips.append("🍳 厨房是油污重灾区，建议每周至少深度清洁1次")
    if "卫生间" not in room_names:
        tips.append("🚿 卫生间容易滋生细菌，建议每周清洁2-3次")
    if "卧室" not in room_names:
        tips.append("😴 卧室清洁影响睡眠质量，建议每周打扫+换床单")

    # 通用建议
    tips.append("🧴 检查一下保洁用品是否充足：洗洁精、洁厕灵、百洁布、垃圾袋是消耗最快的")
    tips.append("📋 下个月试试按房间分区制定保洁计划，效率会更高")

    return tips


def main():
    if len(sys.argv) < 5:
        print(json.dumps({"error": "Usage: cleaning_report.py <year> <month> <summary_json> <entries_json> [output_path]"},
                        ensure_ascii=False))
        sys.exit(1)

    year = int(sys.argv[1])
    month = int(sys.argv[2])
    summary = json.loads(sys.argv[3])
    entries = json.loads(sys.argv[4])

    output_path = sys.argv[5] if len(sys.argv) > 5 else None
    if output_path is None:
        output_path = str(SKILL_DIR / "data" / f"cleaning_report_{year}_{month:02d}.html")

    html = generate_report(year, month, summary, entries)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(html, encoding="utf-8")

    print(json.dumps({"ok": True, "path": output_path}, ensure_ascii=False))


if __name__ == "__main__":
    main()

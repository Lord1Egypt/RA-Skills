#!/usr/bin/env python3
"""
多 Agent 日报 Dashboard 生成器
生成 HTML 可视化页面
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# 可配置的工作区列表
WORKSPACES = [
    "/home/colbert/.openclaw/workspace-coding-advisor",
    # 添加更多工作区路径...
]

def get_workspace_stats(workspace_path):
    """获取工作区统计"""
    report_dir = Path(workspace_path) / "memory/daily-reports"
    index_file = report_dir / "INDEX.md"
    
    stats = {
        "name": Path(workspace_path).name,
        "path": workspace_path,
        "total": 0,
        "success": 0,
        "failed": 0,
        "skipped": 0,
        "missed": 0,
        "caught_up": 0,
        "recent": [],
        "quality_scores": [],
    }
    
    if not index_file.exists():
        return stats
    
    for line in index_file.read_text().splitlines():
        if not line.startswith("|") or "日期" in line or "---" in line:
            continue
        if "2026-" not in line:
            continue
            
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 4:
            continue
            
        date = parts[1]
        status = parts[3]
        
        stats["total"] += 1
        
        if status == "success":
            stats["success"] += 1
        elif status == "failed":
            stats["failed"] += 1
        elif status == "skipped":
            stats["skipped"] += 1
        elif status == "missed":
            stats["missed"] += 1
        elif status == "caught-up":
            stats["caught_up"] += 1
        
        # 最近14天记录
        if "2026-04-" in date:
            day = int(date.split("-")[2])
            if day >= 7:
                stats["recent"].append((date, parts[2], status))
    
    return stats

def generate_html(all_stats):
    """生成 HTML Dashboard"""
    
    total_success = sum(s["success"] for s in all_stats)
    total_failed = sum(s["failed"] for s in all_stats)
    total_missed = sum(s["missed"] for s in all_stats)
    total_caught = sum(s["caught_up"] for s in all_stats)
    total_skipped = sum(s["skipped"] for s in all_stats)
    total = sum(s["total"] for s in all_stats)
    
    success_rate = (total_success / total * 100) if total > 0 else 0
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>码虫日报 Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f7fa;
            padding: 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        
        h1 {{ 
            color: #1a1a2e;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 16px;
            margin-bottom: 25px;
        }}
        
        .header h1 {{ color: white; margin-bottom: 10px; }}
        .header .subtitle {{ opacity: 0.9; }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 25px;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        
        .stat-card.success {{ border-left: 4px solid #52c41a; }}
        .stat-card.failed {{ border-left: 4px solid #ff4d4f; }}
        .stat-card.missed {{ border-left: 4px solid #faad14; }}
        .stat-card.caught {{ border-left: 4px solid #1890ff; }}
        .stat-card.skipped {{ border-left: 4px solid #8c8c8c; }}
        
        .stat-card .number {{
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .stat-card .label {{ color: #666; font-size: 14px; }}
        
        .agent-section {{
            background: white;
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        
        .agent-section h2 {{
            color: #1a1a2e;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .agent-stats {{
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            margin-bottom: 15px;
        }}
        
        .agent-stat {{
            padding: 8px 15px;
            background: #f5f7fa;
            border-radius: 8px;
            font-size: 14px;
        }}
        
        .agent-stat span {{ font-weight: bold; }}
        
        .success-rate {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }}
        
        .rate-high {{ background: #d4edda; color: #155724; }}
        .rate-mid {{ background: #fff3cd; color: #856404; }}
        .rate-low {{ background: #f8d7da; color: #721c24; }}
        
        .calendar {{
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 4px;
            margin-top: 15px;
        }}
        
        .calendar-header {{
            font-size: 12px;
            color: #999;
            text-align: center;
            padding: 5px;
        }}
        
        .calendar-day {{
            aspect-ratio: 1;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 11px;
            font-weight: 500;
        }}
        
        .day-success {{ background: #52c41a; color: white; }}
        .day-failed {{ background: #ff4d4f; color: white; }}
        .day-missed {{ background: #faad14; color: white; }}
        .day-skipped {{ background: #e8e8e8; color: #999; }}
        .day-caught {{ background: #1890ff; color: white; }}
        .day-empty {{ background: #f5f7fa; color: #ccc; }}
        
        .footer {{
            text-align: center;
            color: #999;
            margin-top: 30px;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐛 码虫日报 Dashboard</h1>
            <div class="subtitle">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card success">
                <div class="number" style="color: #52c41a;">{total_success}</div>
                <div class="label">✅ 发送成功</div>
            </div>
            <div class="stat-card failed">
                <div class="number" style="color: #ff4d4f;">{total_failed}</div>
                <div class="label">❌ 发送失败</div>
            </div>
            <div class="stat-card missed">
                <div class="number" style="color: #faad14;">{total_missed}</div>
                <div class="label">⚠️ 漏发</div>
            </div>
            <div class="stat-card caught">
                <div class="number" style="color: #1890ff;">{total_caught}</div>
                <div class="label">📝 已补录</div>
            </div>
            <div class="stat-card skipped">
                <div class="number" style="color: #8c8c8c;">{total_skipped}</div>
                <div class="label">⏭️ 跳过</div>
            </div>
        </div>
        
        <div style="text-align: center; margin-bottom: 25px;">
            <span style="font-size: 18px; color: #666;">总体发送成功率</span>
            <span style="font-size: 36px; font-weight: bold; margin-left: 15px;" 
                  class="{'rate-high' if success_rate >= 80 else 'rate-mid' if success_rate >= 50 else 'rate-low'}">
                {success_rate:.1f}%
            </span>
        </div>
"""
    
    weekday_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    
    for stats in all_stats:
        rate = (stats["success"] / stats["total"] * 100) if stats["total"] > 0 else 0
        rate_class = "rate-high" if rate >= 80 else "rate-mid" if rate >= 50 else "rate-low"
        
        html += f"""
        <div class="agent-section">
            <h2>📁 {stats['name']}</h2>
            <div class="agent-stats">
                <div class="agent-stat">✅ <span>{stats['success']}</span> 成功</div>
                <div class="agent-stat">❌ <span>{stats['failed']}</span> 失败</div>
                <div class="agent-stat">⚠️ <span>{stats['missed']}</span> 漏发</div>
                <div class="agent-stat">📝 <span>{stats['caught_up']}</span> 已补</div>
                <div class="agent-stat">📊 共 <span>{stats['total']}</span> 条</div>
                <span class="success-rate {rate_class}">{rate:.1f}% 成功率</span>
            </div>
            
            <div class="calendar">
                <div class="calendar-header">一</div>
                <div class="calendar-header">二</div>
                <div class="calendar-header">三</div>
                <div class="calendar-header">四</div>
                <div class="calendar-header">五</div>
                <div class="calendar-header">六</div>
                <div class="calendar-header">日</div>
"""
        
        # 生成最近14天的日历
        recent = sorted(stats["recent"])[:14]
        status_map = {s[0]: s[2] for s in recent}
        
        for i in range(14, 0, -1):
            day_num = 20 - i + 1  # 4月的日期
            if day_num < 7:
                continue
            date_key = f"2026-04-{day_num:02d}"
            status = status_map.get(date_key, "")
            
            if status == "success":
                cls = "day-success"
            elif status == "failed":
                cls = "day-failed"
            elif status == "missed":
                cls = "day-missed"
            elif status == "caught-up":
                cls = "day-caught"
            elif status == "skipped":
                cls = "day-skipped"
            else:
                cls = "day-empty"
            
            html += f'<div class="calendar-day {cls}">{day_num}</div>'
        
        html += "</div></div>"
    
    html += f"""
        <div class="footer">
            <p>码虫日报监控系统 | 数据来源: memory/daily-reports/INDEX.md</p>
        </div>
    </div>
</body>
</html>"""
    
    return html

def main():
    if len(sys.argv) > 1:
        output_path = sys.argv[1]
    else:
        output_path = "/tmp/daily-report-dashboard.html"
    
    all_stats = []
    for workspace in WORKSPACES:
        if os.path.exists(workspace):
            stats = get_workspace_stats(workspace)
            if stats["total"] > 0:
                all_stats.append(stats)
    
    html = generate_html(all_stats)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ Dashboard 已生成: {output_path}")
    print(f"   打开浏览器查看: file://{output_path}")

if __name__ == "__main__":
    main()

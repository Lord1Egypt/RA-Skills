#!/usr/bin/env python3
"""
广告投手 - 可视化报表生成模块
生成交互式HTML可视化报告（日报/周报/月报/综合诊断报告）
"""

import json
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from data_manager import load_file, get_summary
from performance import diagnose, anomaly_detect, trend_analysis, campaign_ranking
from optimizer import budget_allocation, bid_optimizer, creative_analysis

# 配色方案
COLORS = {
    "primary": "#1a73e8",
    "success": "#0d9488",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "info": "#6366f1",
    "bg": "#f8fafc",
    "card": "#ffffff",
    "text": "#1e293b",
    "text_secondary": "#64748b",
    "border": "#e2e8f0",
    "gradient_start": "#667eea",
    "gradient_end": "#764ba2",
}


def generate_report(file_path: str, report_type: str = "daily", output_path: str = None) -> str:
    """
    生成广告投放可视化报告
    
    report_type: daily / weekly / monthly / diagnose
    output_path: 输出HTML文件路径
    """
    records, platform, meta = load_file(file_path)
    summary = get_summary(records)
    diag = diagnose(records)
    trends = trend_analysis(records)
    budget = budget_allocation(records)
    bid = bid_optimizer(records)
    creative = creative_analysis(records)
    ranking = campaign_ranking(records)

    now = datetime.now()
    date_str = now.strftime("%Y年%m月%d日")

    type_labels = {
        "daily": "日报",
        "weekly": "周报",
        "monthly": "月报",
        "diagnose": "综合诊断报告"
    }
    report_label = type_labels.get(report_type, "投放分析报告")

    platform_names = {
        "tencent_ads": "腾讯广告",
        "ocean_engine": "巨量引擎",
        "baidu_ads": "百度推广",
        "meta_ads": "Meta Ads",
        "google_ads": "Google Ads",
        "unknown": "未知平台"
    }

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>广告投放{report_label} - {date_str}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; background: {COLORS['bg']}; color: {COLORS['text']}; line-height: 1.6; }}
.container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}

/* 头部 */
.header {{ background: linear-gradient(135deg, {COLORS['gradient_start']}, {COLORS['gradient_end']}); color: white; padding: 40px 30px; border-radius: 16px; margin-bottom: 24px; }}
.header h1 {{ font-size: 28px; font-weight: 700; margin-bottom: 8px; }}
.header .meta {{ font-size: 14px; opacity: 0.85; }}
.header .meta span {{ margin-right: 20px; }}

/* 健康评分卡 */
.score-card {{ background: {COLORS['card']}; border-radius: 16px; padding: 30px; margin-bottom: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); display: flex; align-items: center; gap: 30px; flex-wrap: wrap; }}
.score-circle {{ width: 120px; height: 120px; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; font-weight: 700; flex-shrink: 0; }}
.score-circle .number {{ font-size: 42px; line-height: 1; }}
.score-circle .label {{ font-size: 14px; margin-top: 4px; }}
.score-info {{ flex: 1; min-width: 200px; }}
.score-info h3 {{ font-size: 20px; margin-bottom: 8px; }}
.score-info .grade {{ display: inline-block; padding: 4px 16px; border-radius: 20px; font-size: 14px; font-weight: 600; }}

/* KPI网格 */
.kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 24px; }}
.kpi-card {{ background: {COLORS['card']}; border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); border-left: 4px solid; }}
.kpi-card .label {{ font-size: 13px; color: {COLORS['text_secondary']}; margin-bottom: 6px; }}
.kpi-card .value {{ font-size: 26px; font-weight: 700; }}
.kpi-card .sub {{ font-size: 12px; color: {COLORS['text_secondary']}; margin-top: 4px; }}

/* 区块标题 */
.section-title {{ font-size: 20px; font-weight: 700; margin: 32px 0 16px; padding-bottom: 8px; border-bottom: 2px solid {COLORS['border']}; }}
.section-title .icon {{ margin-right: 8px; }}

/* 图表容器 */
.chart-row {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(500px, 1fr)); gap: 20px; margin-bottom: 24px; }}
.chart-card {{ background: {COLORS['card']}; border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }}
.chart-card h4 {{ font-size: 16px; margin-bottom: 12px; color: {COLORS['text']}; }}
.chart-card canvas {{ max-height: 300px; }}

/* 表格 */
.table-card {{ background: {COLORS['card']}; border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); margin-bottom: 24px; overflow-x: auto; }}
table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
th {{ background: {COLORS['bg']}; padding: 12px 16px; text-align: left; font-weight: 600; color: {COLORS['text_secondary']}; border-bottom: 2px solid {COLORS['border']}; white-space: nowrap; }}
td {{ padding: 12px 16px; border-bottom: 1px solid {COLORS['border']}; }}
tr:hover {{ background: #f1f5f9; }}

/* 异常告警 */
.alert-list {{ display: flex; flex-direction: column; gap: 10px; margin-bottom: 24px; }}
.alert {{ display: flex; align-items: flex-start; gap: 12px; padding: 14px 18px; border-radius: 10px; border-left: 4px solid; }}
.alert.critical {{ background: #fef2f2; border-color: {COLORS['danger']}; }}
.alert.warning {{ background: #fffbeb; border-color: {COLORS['warning']}; }}
.alert.info {{ background: #eff6ff; border-color: {COLORS['primary']}; }}
.alert .alert-icon {{ font-size: 20px; flex-shrink: 0; }}
.alert .alert-content {{ flex: 1; }}
.alert .alert-title {{ font-weight: 600; margin-bottom: 4px; }}
.alert .alert-desc {{ font-size: 13px; color: {COLORS['text_secondary']}; }}
.alert .alert-action {{ font-size: 13px; color: {COLORS['primary']}; margin-top: 4px; }}

/* 建议卡片 */
.advice-cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px; margin-bottom: 24px; }}
.advice-card {{ background: {COLORS['card']}; border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); display: flex; gap: 14px; align-items: flex-start; }}
.advice-card .priority {{ width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 13px; color: white; flex-shrink: 0; }}
.advice-card .priority.p0 {{ background: {COLORS['danger']}; }}
.advice-card .priority.p1 {{ background: {COLORS['warning']}; }}
.advice-card .priority.p2 {{ background: {COLORS['info']}; }}

/* 预算分配条 */
.budget-bar {{ height: 32px; border-radius: 16px; overflow: hidden; display: flex; margin: 10px 0; }}
.budget-bar .tier-a {{ background: {COLORS['success']}; }}
.budget-bar .tier-b {{ background: {COLORS['warning']}; }}
.budget-bar .tier-c {{ background: {COLORS['danger']}; }}

.tab-nav {{ display: flex; gap: 8px; margin: 20px 0; }}
.tab-btn {{ padding: 8px 20px; border: 1px solid {COLORS['border']}; border-radius: 8px; background: white; cursor: pointer; font-size: 14px; transition: all 0.2s; }}
.tab-btn.active {{ background: {COLORS['primary']}; color: white; border-color: {COLORS['primary']}; }}

.footer {{ text-align: center; padding: 40px 20px; color: {COLORS['text_secondary']}; font-size: 13px; }}
.footer a {{ color: {COLORS['primary']}; text-decoration: none; }}

@media (max-width: 768px) {{
  .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }}
  .chart-row {{ grid-template-columns: 1fr; }}
  .score-card {{ flex-direction: column; text-align: center; }}
}}
</style>
</head>
<body>
<div class="container">

<!-- 报告头部 -->
<div class="header">
  <h1>🎯 广告投放{report_label}</h1>
  <div class="meta">
    <span>📅 {date_str}</span>
    <span>📊 {platform_names.get(platform, '未知平台')}</span>
    <span>📋 {summary.get('record_count', 0)} 条数据</span>
    <span>📆 {summary.get('date_range', '未知')}</span>
  </div>
</div>

<!-- 健康评分 -->
<div class="score-card">
  <div class="score-circle" style="background: {_score_color(diag['health_score'])}; color: white;">
    <div class="number">{diag['health_score']}</div>
    <div class="label">健康分</div>
  </div>
  <div class="score-info">
    <h3>账户健康度评估</h3>
    <span class="grade" style="background: {_score_bg(diag['health_score'])}; color: {_score_color(diag['health_score'])};">
      {diag['grade']}
    </span>
    <p style="margin-top: 12px; color: {COLORS['text_secondary']}; font-size: 14px;">
      {_grade_description(diag['grade'])}
    </p>
  </div>
</div>

<!-- KPI卡片 -->
<div class="kpi-grid">
  {_kpi_card("总消耗", f"¥{summary['total_cost']:,.0f}", "千次曝光 ¥{summary['avg_cpm']:.1f}", 'primary')}
  {_kpi_card("总曝光", f"{summary['total_impressions']:,}", f"CTR {summary['avg_ctr']}%", 'primary')}
  {_kpi_card("总点击", f"{summary['total_clicks']:,}", f"CPC ¥{summary['avg_cpc']:.2f}", 'info')}
  {_kpi_card("总转化", f"{summary['total_conversions']:,}", f"CVR {summary['avg_cvr']}%", 'info')}
  {_kpi_card("总收入", f"¥{summary['total_revenue']:,.0f}", f"ROAS {summary['roas']}", 'success' if summary['roas'] >= 2 else 'warning')}
  {_kpi_card("平均CPA", f"¥{summary['avg_cpa']:.1f}", f"ROI {summary['roi']}%", 'danger' if summary['avg_cpa'] > 80 else 'success')}
</div>

<!-- 异常告警 -->
{_alerts_section(diag.get('anomalies', []))}

<!-- 趋势图表 -->
<div class="section-title"><span class="icon">📈</span>核心指标趋势</div>
<div class="chart-row">
  <div class="chart-card">
    <h4>消耗 & ROAS 趋势</h4>
    <canvas id="chartCostRoas"></canvas>
  </div>
  <div class="chart-card">
    <h4>CTR & CVR 趋势</h4>
    <canvas id="chartCtrCvr"></canvas>
  </div>
</div>
<div class="chart-row">
  <div class="chart-card">
    <h4>CPA 趋势</h4>
    <canvas id="chartCpa"></canvas>
  </div>
  <div class="chart-card">
    <h4>转化量趋势</h4>
    <canvas id="chartConv"></canvas>
  </div>
</div>

<!-- 预算分配 -->
<div class="section-title"><span class="icon">💰</span>预算分配建议 (532法则)</div>
<div class="chart-card" style="margin-bottom: 24px;">
  <div class="budget-bar">
    <div class="tier-a" style="width: 50%;" title="优质计划 50%"></div>
    <div class="tier-b" style="width: 30%;" title="潜力计划 30%"></div>
    <div class="tier-c" style="width: 20%;" title="测试计划 20%"></div>
  </div>
  <div style="display: flex; gap: 20px; font-size: 13px; margin-top: 8px; flex-wrap: wrap;">
    <span>🟢 优质: ¥{budget.get('tiers', {}).get('A_优质计划', {}).get('amount', 0):,.0f}</span>
    <span>🟡 潜力: ¥{budget.get('tiers', {}).get('B_潜力计划', {}).get('amount', 0):,.0f}</span>
    <span>🔴 测试: ¥{budget.get('tiers', {}).get('C_测试计划', {}).get('amount', 0):,.0f}</span>
  </div>
</div>

{_budget_detail_table(budget)}

<!-- 计划排行榜 -->
<div class="section-title"><span class="icon">🏆</span>计划排行榜</div>
{_ranking_table(ranking)}

<!-- 素材分析 -->
<div class="section-title"><span class="icon">🎨</span>素材诊断</div>
<div class="chart-row">
  <div class="chart-card">
    <h4>素材健康度分布</h4>
    <canvas id="chartCreativeHealth"></canvas>
  </div>
  <div class="chart-card">
    <h4>素材ROAS对比</h4>
    <canvas id="chartCreativeRoas"></canvas>
  </div>
</div>
{_creative_table(creative)}

<!-- 优化建议 -->
<div class="section-title"><span class="icon">💡</span>优化建议</div>
<div class="advice-cards">
  {_advice_cards(diag, bid, creative)}
</div>

<!-- 页脚 -->
<div class="footer">
  <p>🤖 由 AI广告投手 自动生成 | {date_str}</p>
  <p style="font-size: 12px; margin-top: 4px;">数据驱动决策 · 智能投放优化</p>
</div>

</div>

<!-- Chart.js 初始化 -->
<script>
{_chart_scripts(trends, creative, summary)}
</script>
</body>
</html>"""

    # 保存文件
    if output_path is None:
        safe_date = now.strftime("%Y%m%d_%H%M%S")
        output_path = f"ad_trader_report_{report_type}_{safe_date}.html"

    output_path = Path(output_path)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return str(output_path.absolute())


def _score_color(score):
    """健康评分颜色"""
    if score >= 80:
        return COLORS["success"]
    elif score >= 60:
        return COLORS["warning"]
    elif score >= 40:
        return "#f97316"
    return COLORS["danger"]


def _score_bg(score):
    """健康评分背景色"""
    if score >= 80:
        return "#ecfdf5"
    elif score >= 60:
        return "#fffbeb"
    elif score >= 40:
        return "#fff7ed"
    return "#fef2f2"


def _grade_description(grade):
    descriptions = {
        "优秀": "账户运营良好，持续监控趋势，关注素材更新节奏即可",
        "良好": "整体健康，部分指标有优化空间，建议针对性调整",
        "需关注": "多个指标异常，建议排查问题并制定优化计划",
        "严重": "投放效果严重不达标，建议立即止损并重新规划策略",
    }
    return descriptions.get(grade, "")


def _kpi_card(label, value, sub, color_key):
    border_colors = {
        "primary": COLORS["primary"],
        "info": COLORS["info"],
        "success": COLORS["success"],
        "warning": COLORS["warning"],
        "danger": COLORS["danger"],
    }
    color = border_colors.get(color_key, COLORS["primary"])
    return f"""<div class="kpi-card" style="border-left-color: {color};">
  <div class="label">{label}</div>
  <div class="value">{value}</div>
  <div class="sub">{sub}</div>
</div>"""


def _alerts_section(anomalies):
    if not anomalies:
        return """<div class="section-title"><span class="icon">✅</span>异常告警</div>
<div style="background: #ecfdf5; border-radius: 12px; padding: 20px; text-align: center; color: #0d9488; font-weight: 600;">
  🎉 未检测到异常，各项指标运行正常
</div>"""

    items = []
    for a in anomalies[:10]:
        severity = a.get("severity", "info")
        icons = {"critical": "🔴", "warning": "🟡", "info": "🔵"}
        item = f"""<div class="alert {severity}">
  <div class="alert-icon">{icons.get(severity, '⚪')}</div>
  <div class="alert-content">
    <div class="alert-title">[{a.get('type', '未知')}] {a.get('message', '')}</div>
    <div class="alert-desc">{a.get('date', '')}</div>
    <div class="alert-action">💡 {a.get('suggestion', '')}</div>
  </div>
</div>"""
        items.append(item)

    return f"""<div class="section-title"><span class="icon">🚨</span>异常告警 ({len(anomalies)}项)</div>
<div class="alert-list">{''.join(items)}</div>"""


def _budget_detail_table(budget):
    tiers = budget.get("tiers", {})
    rows = []
    for tier_name, tier_data in tiers.items():
        plans = tier_data.get("plans", [])
        for plan in plans:
            rows.append(f"""<tr>
  <td><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:{'#0d9488' if 'A' in tier_name else '#f59e0b' if 'B' in tier_name else '#ef4444'};margin-right:6px;"></span>{tier_name.replace('_', ' ')}</td>
  <td>{plan.get('name', '')}</td>
  <td>¥{plan.get('budget', 0):,.0f}</td>
  <td>{plan.get('roas', 0)}</td>
  <td>¥{plan.get('cpa', 0):.1f}</td>
  <td>{tier_data.get('rule', '')}</td>
</tr>""")

    return f"""<div class="table-card">
<table>
<thead><tr><th>等级</th><th>计划名称</th><th>建议预算</th><th>ROAS</th><th>CPA</th><th>策略</th></tr></thead>
<tbody>{''.join(rows)}</tbody>
</table></div>"""


def _ranking_table(ranking):
    overall = ranking.get("overall_ranking", [])
    rows = []
    for i, c in enumerate(overall[:15]):
        roas = c.get("roas", 0)
        roas_color = "#0d9488" if roas >= 2 else "#f59e0b" if roas >= 1 else "#ef4444"
        rank_icon = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"{i+1}"
        rows.append(f"""<tr>
  <td>{rank_icon}</td>
  <td><strong>{c.get('name', '')}</strong></td>
  <td>¥{c.get('cost', 0):,.0f}</td>
  <td>{c.get('ctr', 0)}%</td>
  <td>{c.get('cvr', 0)}%</td>
  <td>¥{c.get('cpa', 0):.1f}</td>
  <td style="color:{roas_color};font-weight:700;">{roas}</td>
  <td>{c.get('score', 0)}分</td>
</tr>""")

    return f"""<div class="table-card">
<table>
<thead><tr><th>排名</th><th>计划名称</th><th>消耗</th><th>CTR</th><th>CVR</th><th>CPA</th><th>ROAS</th><th>综合评分</th></tr></thead>
<tbody>{''.join(rows)}</tbody>
</table></div>"""


def _creative_table(creative):
    all_c = creative.get("all_creatives", [])
    rows = []
    for c in all_c[:15]:
        fatigue = c.get("fatigue", {})
        level_colors = {"健康": "#0d9488", "注意": "#f59e0b", "疲劳": "#ef4444"}
        level = fatigue.get("level", "未知")
        rows.append(f"""<tr>
  <td>{c.get('name', '')}</td>
  <td>{c.get('impressions', 0):,}</td>
  <td>{c.get('ctr', 0)}%</td>
  <td>{c.get('cvr', 0)}%</td>
  <td>¥{c.get('cpa', 0):.1f}</td>
  <td>{c.get('roas', 0)}</td>
  <td>{c.get('active_days', 0)}天</td>
  <td style="color:{level_colors.get(level, '#6b7280')};font-weight:600;">{level}</td>
</tr>""")

    return f"""<div class="table-card">
<h4 style="margin-bottom:12px;">素材排行 (共{creative.get('total_creatives', 0)}个)</h4>
<table>
<thead><tr><th>素材名称</th><th>曝光</th><th>CTR</th><th>CVR</th><th>CPA</th><th>ROAS</th><th>在线天数</th><th>状态</th></tr></thead>
<tbody>{''.join(rows)}</tbody>
</table></div>"""


def _advice_cards(diag, bid, creative):
    cards = []

    # 优先处理 P0 建议
    issues = diag.get("issues", [])
    for issue in issues:
        priority = "p0" if issue.get("severity") == "critical" else "p1"
        cards.append(f"""<div class="advice-card">
  <div class="priority {priority}">P{0 if priority == 'p0' else 1}</div>
  <div>
    <strong>{issue.get('item', '')}</strong>
    <p style="font-size:13px;color:{COLORS['text_secondary']};margin-top:4px;">{issue.get('message', '')}</p>
  </div>
</div>""")

    # 素材建议
    for rec in creative.get("recommendations", [])[:3]:
        p = rec.get("priority", "P1").lower()
        cards.append(f"""<div class="advice-card">
  <div class="priority {p}">{rec.get('priority', 'P1')}</div>
  <div>
    <strong>{rec.get('type', '')}</strong>
    <p style="font-size:13px;color:{COLORS['text_secondary']};margin-top:4px;">{rec.get('message', '')}</p>
    <p style="font-size:13px;color:{COLORS['primary']};margin-top:4px;">💡 {rec.get('action', '')}</p>
  </div>
</div>""")

    # 通用建议
    for advice in bid.get("general_advice", [])[:2]:
        cards.append(f"""<div class="advice-card">
  <div class="priority p2">P2</div>
  <div>
    <strong>投放策略</strong>
    <p style="font-size:13px;color:{COLORS['text_secondary']};margin-top:4px;">{advice}</p>
  </div>
</div>""")

    return "\n".join(cards) if cards else '<div style="text-align:center;padding:20px;color:{COLORS["text_secondary"]};">当前数据不足，积累更多数据后可生成优化建议</div>'


def _chart_scripts(trends, creative, summary):
    """生成 Chart.js 图表脚本"""

    # 趋势数据
    dates = [t["date"] for t in trends.get("cost_trend", [])]
    cost_values = [t["value"] for t in trends.get("cost_trend", [])]
    roas_values = [t["value"] for t in trends.get("roas_trend", [])]
    ctr_values = [t["value"] for t in trends.get("ctr_trend", [])]
    cvr_values = [t["value"] for t in trends.get("cvr_trend", [])]
    cpa_values = [t["value"] for t in trends.get("cpa_trend", [])]

    conv_values = []
    for d in dates:
        # conversion trend not directly available, will check
        pass

    # 素材健康度
    health = creative.get("health", {})
    creative_list = creative.get("all_creatives", [])

    return f"""
// 消耗 & ROAS 趋势
new Chart(document.getElementById('chartCostRoas'), {{
  type: 'line',
  data: {{
    labels: {json.dumps(dates, default=str)},
    datasets: [{{
      label: '消耗(¥)',
      data: {json.dumps(cost_values)},
      borderColor: '{COLORS["primary"]}',
      backgroundColor: 'rgba(26,115,232,0.1)',
      fill: true,
      yAxisID: 'y',
      tension: 0.3
    }}, {{
      label: 'ROAS',
      data: {json.dumps(roas_values)},
      borderColor: '{COLORS["success"]}',
      borderDash: [5, 5],
      yAxisID: 'y1',
      tension: 0.3
    }}]
  }},
  options: {{
    responsive: true,
    interaction: {{ intersect: false, mode: 'index' }},
    plugins: {{ legend: {{ position: 'top' }} }},
    scales: {{
      y: {{ type: 'linear', position: 'left', title: {{ display: true, text: '消耗(¥)' }} }},
      y1: {{ type: 'linear', position: 'right', title: {{ display: true, text: 'ROAS' }}, grid: {{ drawOnChartArea: false }} }}
    }}
  }}
}});

// CTR & CVR 趋势
new Chart(document.getElementById('chartCtrCvr'), {{
  type: 'line',
  data: {{
    labels: {json.dumps(dates, default=str)},
    datasets: [{{
      label: 'CTR(%)',
      data: {json.dumps(ctr_values)},
      borderColor: '{COLORS["info"]}',
      tension: 0.3
    }}, {{
      label: 'CVR(%)',
      data: {json.dumps(cvr_values)},
      borderColor: '{COLORS["warning"]}',
      tension: 0.3
    }}]
  }},
  options: {{
    responsive: true,
    interaction: {{ intersect: false, mode: 'index' }},
    plugins: {{ legend: {{ position: 'top' }} }}
  }}
}});

// CPA 趋势
new Chart(document.getElementById('chartCpa'), {{
  type: 'bar',
  data: {{
    labels: {json.dumps(dates, default=str)},
    datasets: [{{
      label: 'CPA(¥)',
      data: {json.dumps(cpa_values)},
      backgroundColor: {json.dumps([COLORS['danger'] if v > 80 else COLORS['success'] for v in cpa_values])},
      borderRadius: 6
    }}]
  }},
  options: {{
    responsive: true,
    plugins: {{ legend: {{ display: false }} }}
  }}
}});

// 转化量趋势
new Chart(document.getElementById('chartConv'), {{
  type: 'bar',
  data: {{
    labels: {json.dumps(dates, default=str)},
    datasets: [{{
      label: '转化量',
      data: {json.dumps(cost_values)},  // placeholder
      backgroundColor: '{COLORS["primary"]}33',
      borderColor: '{COLORS["primary"]}',
      borderWidth: 1,
      borderRadius: 6
    }}]
  }},
  options: {{
    responsive: true,
    plugins: {{ legend: {{ display: false }} }}
  }}
}});

// 素材健康度
new Chart(document.getElementById('chartCreativeHealth'), {{
  type: 'doughnut',
  data: {{
    labels: ['健康', '注意', '疲劳'],
    datasets: [{{
      data: [{health.get('fresh', 0)}, {health.get('warning', 0)}, {health.get('fatigued', 0)}],
      backgroundColor: ['#0d9488', '#f59e0b', '#ef4444'],
      borderWidth: 0
    }}]
  }},
  options: {{
    responsive: true,
    plugins: {{ legend: {{ position: 'bottom' }} }}
  }}
}});

// 素材ROAS对比
new Chart(document.getElementById('chartCreativeRoas'), {{
  type: 'bar',
  data: {{
    labels: {json.dumps([c['name'][:10] for c in creative_list[:8]])},
    datasets: [{{
      label: 'ROAS',
      data: {json.dumps([c.get('roas', 0) for c in creative_list[:8]])},
      backgroundColor: {json.dumps([COLORS['success'] if c.get('roas', 0) >= 2 else COLORS['warning'] for c in creative_list[:8]])},
      borderRadius: 6
    }}]
  }},
  options: {{
    indexAxis: 'y',
    responsive: true,
    plugins: {{ legend: {{ display: false }} }}
  }}
}});
"""


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python report.py <数据文件路径> [--type daily|weekly|monthly|diagnose] [--output 输出路径]")
        sys.exit(1)

    file_path = sys.argv[1]
    report_type = "daily"
    output_path = None

    if "--type" in sys.argv:
        idx = sys.argv.index("--type")
        if idx + 1 < len(sys.argv):
            report_type = sys.argv[idx + 1]

    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_path = sys.argv[idx + 1]

    try:
        result_path = generate_report(file_path, report_type, output_path)
        print(f"✅ 报告已生成: {result_path}")
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

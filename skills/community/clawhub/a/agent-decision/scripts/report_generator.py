#!/usr/bin/env python3
"""
AI Agent 开发决策辅助报告生成器
Generate professional interactive feasibility decision report for AI Agent development.
"""

import json
import sys
from datetime import datetime
from pathlib import Path


# ============================================================
# Scoring Engine
# ============================================================

DIMENSIONS = {
    "tech_maturity": {"name": "技术成熟度", "weight": 0.15, "icon": "🧠", "color": "#6366F1"},
    "competition": {"name": "竞品格局", "weight": 0.15, "icon": "⚔️", "color": "#F59E0B"},
    "market": {"name": "市场前景", "weight": 0.15, "icon": "📈", "color": "#10B981"},
    "industry_fit": {"name": "行业适配", "weight": 0.10, "icon": "🎯", "color": "#3B82F6"},
    "dev_feasibility": {"name": "开发可行性", "weight": 0.15, "icon": "🔧", "color": "#8B5CF6"},
    "stability": {"name": "系统稳定性", "weight": 0.10, "icon": "🛡️", "color": "#EC4899"},
    "cost_control": {"name": "成本可控性", "weight": 0.10, "icon": "💰", "color": "#F97316"},
    "promotion": {"name": "推广潜力", "weight": 0.10, "icon": "🚀", "color": "#14B8A6"},
}


def calculate_total_score(scores: dict) -> dict:
    """Calculate weighted total score and rating."""
    total = 0
    dim_scores = {}
    for key, dim in DIMENSIONS.items():
        s = scores.get(key, 50)
        dim_scores[key] = s
        total += s * dim["weight"]

    total = round(total, 1)

    if total >= 80:
        rating = "✅ 强烈建议做"
        rating_desc = "技术成熟度与市场机会明确，Agent生态红利期，建议尽快立项推进"
        color = "#10B981"
        bg = "#ECFDF5"
        icon = "🚀"
        decision_class = "strong-yes"
    elif total >= 65:
        rating = "🟡 谨慎推进"
        rating_desc = "有一定市场机会，但需差异化定位并验证核心技术假设（如幻觉率、ROI）"
        color = "#F59E0B"
        bg = "#FFFBEB"
        icon = "🔍"
        decision_class = "cautious"
    elif total >= 50:
        rating = "⚠️ 暂缓观望"
        rating_desc = "当前条件下风险较高，建议先做MVP验证核心价值假设，再决定是否全量投入"
        color = "#F97316"
        bg = "#FFF7ED"
        icon = "⏸️"
        decision_class = "wait"
    else:
        rating = "❌ 不建议做"
        rating_desc = "技术瓶颈、市场竞争或成本结构存在重大风险，建议调整方向或等待技术突破"
        color = "#EF4444"
        bg = "#FEF2F2"
        icon = "🛑"
        decision_class = "no"

    return {
        "total": total,
        "dimensions": dim_scores,
        "rating": rating,
        "rating_desc": rating_desc,
        "color": color,
        "bg": bg,
        "icon": icon,
        "decision_class": decision_class,
    }


def safe_get(d, key, default=""):
    """Safely get dict value."""
    if isinstance(d, dict):
        return d.get(key, default)
    return default


def make_score_bar(score, max_score=100):
    """Generate HTML score bar."""
    pct = min(score / max_score, 1.0)
    if score >= 80:
        color = "#10B981"
    elif score >= 65:
        color = "#3B82F6"
    elif score >= 50:
        color = "#F59E0B"
    else:
        color = "#EF4444"

    return f"""<div style="display:flex;align-items:center;gap:10px;margin:6px 0;">
  <div style="flex:1;height:10px;background:#E5E7EB;border-radius:5px;overflow:hidden;">
    <div style="width:{pct*100}%;height:100%;background:{color};border-radius:5px;transition:width 1s ease;"></div>
  </div>
  <span style="font-weight:700;font-size:14px;color:{color};min-width:45px;text-align:right;">{score}分</span>
</div>"""


def make_tag(text, color="#3B82F6"):
    return f'<span style="display:inline-block;padding:3px 10px;background:{color}15;color:{color};border-radius:12px;font-size:12px;font-weight:600;margin:2px;">{text}</span>'


# ============================================================
# Radar Chart JS (Canvas-based, inline)
# ============================================================

RADAR_CHART_JS = """
<script>
function drawRadar() {
    const canvas = document.getElementById('radarChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const W = canvas.width, H = canvas.height;
    const cx = W/2, cy = H/2;
    const radius = Math.min(cx, cy) - 40;
    const dims = DIMENSIONS_DATA;
    const scores = SCORES_DATA;
    const n = dims.length;

    // Grid and labels
    ctx.strokeStyle = '#E5E7EB';
    ctx.fillStyle = '#6B7280';
    ctx.font = '13px -apple-system, PingFang SC, Microsoft YaHei, sans-serif';
    ctx.textAlign = 'center';

    for (let level = 1; level <= 5; level++) {
        const r = radius * level / 5;
        ctx.beginPath();
        for (let i = 0; i < n; i++) {
            const angle = (Math.PI * 2 * i / n) - Math.PI / 2;
            const x = cx + r * Math.cos(angle);
            const y = cy + r * Math.sin(angle);
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        }
        ctx.closePath();
        ctx.stroke();
    }

    // Axis lines and labels
    for (let i = 0; i < n; i++) {
        const angle = (Math.PI * 2 * i / n) - Math.PI / 2;
        const x = cx + radius * Math.cos(angle);
        const y = cy + radius * Math.sin(angle);
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(x, y);
        ctx.stroke();

        // Label
        const lx = cx + (radius + 28) * Math.cos(angle);
        const ly = cy + (radius + 28) * Math.sin(angle);
        ctx.fillStyle = '#374151';
        ctx.font = 'bold 12px -apple-system, PingFang SC, Microsoft YaHei, sans-serif';
        ctx.fillText(dims[i].name, lx, ly + 4);

        // Score label
        const sx = cx + (radius + 50) * Math.cos(angle);
        const sy = cy + (radius + 50) * Math.sin(angle);
        ctx.fillStyle = dims[i].color;
        ctx.font = 'bold 13px -apple-system, PingFang SC, Microsoft YaHei, sans-serif';
        ctx.fillText(scores[i] + '分', sx, sy + 4);
    }

    // Data polygon
    ctx.beginPath();
    ctx.fillStyle = 'rgba(99,102,241,0.15)';
    ctx.strokeStyle = '#6366F1';
    ctx.lineWidth = 2.5;
    for (let i = 0; i < n; i++) {
        const angle = (Math.PI * 2 * i / n) - Math.PI / 2;
        const r = radius * scores[i] / 100;
        const x = cx + r * Math.cos(angle);
        const y = cy + r * Math.sin(angle);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    }
    ctx.closePath();
    ctx.fill();
    ctx.stroke();

    // Data points
    for (let i = 0; i < n; i++) {
        const angle = (Math.PI * 2 * i / n) - Math.PI / 2;
        const r = radius * scores[i] / 100;
        const x = cx + r * Math.cos(angle);
        const y = cy + r * Math.sin(angle);
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, Math.PI * 2);
        ctx.fillStyle = dims[i].color;
        ctx.fill();
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 2;
        ctx.stroke();
    }
}

// Run on load
window.addEventListener('DOMContentLoaded', drawRadar);
window.addEventListener('resize', drawRadar);
</script>
"""


# ============================================================
# HTML Report Generator
# ============================================================

def generate_report(data: dict) -> str:
    """Generate the complete HTML decision report."""

    name = safe_get(data, "name", "未命名Agent产品")
    direction = safe_get(data, "direction", "未指定方向")
    now = datetime.now().strftime("%Y年%m月%d日 %H:%M")

    # Scores
    scores = safe_get(data, "scores", {})
    score_result = calculate_total_score(scores)

    # Sections
    tech = safe_get(data, "tech", {})
    competitors = safe_get(data, "competitors", {})
    market = safe_get(data, "market", {})
    industry = safe_get(data, "industry", {})
    feasibility = safe_get(data, "feasibility", {})
    stability = safe_get(data, "stability", {})
    cost = safe_get(data, "cost", {})
    promotion = safe_get(data, "promotion", {})

    # ============================================================
    # CSS
    # ============================================================
    css = f"""
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif; background: #0F172A; color: #E2E8F0; line-height:1.7; }}
  .container {{ max-width: 960px; margin: 0 auto; padding: 24px; }}

  /* Cover */
  .cover {{ background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%); color: white; padding: 64px 48px; border-radius: 20px; text-align: center; margin-bottom: 28px; position: relative; overflow: hidden; }}
  .cover::before {{ content: ''; position: absolute; top: -30%; right: -15%; width: 500px; height: 500px; background: radial-gradient(circle, rgba(99,102,241,0.4) 0%, transparent 70%); border-radius: 50%; }}
  .cover::after {{ content: ''; position: absolute; bottom: -20%; left: -10%; width: 400px; height: 400px; background: radial-gradient(circle, rgba(236,72,153,0.2) 0%, transparent 70%); border-radius: 50%; }}
  .cover h1 {{ font-size: 36px; font-weight: 900; margin-bottom: 10px; position: relative; z-index:1; }}
  .cover .subtitle {{ font-size: 17px; opacity: 0.75; position: relative; z-index:1; }}
  .cover .date {{ font-size: 13px; opacity: 0.5; margin-top: 16px; position: relative; z-index:1; }}
  .cover .badge {{ display:inline-block; background: rgba(255,255,255,0.15); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2); border-radius: 20px; padding: 6px 18px; font-size: 13px; margin-top: 16px; position: relative; z-index:1; }}

  /* Score Card */
  .score-card {{ background: {score_result['bg']}; border: 2px solid {score_result['color']}; border-radius: 20px; padding: 40px; text-align: center; margin-bottom: 28px; }}
  .score-card .big-score {{ font-size: 80px; font-weight: 900; color: {score_result['color']}; line-height: 1; letter-spacing: -2px; }}
  .score-card .rating {{ font-size: 26px; font-weight: 700; color: {score_result['color']}; margin: 10px 0; }}
  .score-card .rating-desc {{ font-size: 15px; color: #6B7280; max-width: 560px; margin: 0 auto; }}

  /* Section */
  .section {{ background: #1E293B; border: 1px solid #334155; border-radius: 20px; padding: 36px; margin-bottom: 22px; }}
  .section h2 {{ font-size: 22px; font-weight: 700; color: #F1F5F9; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }}
  .section h3 {{ font-size: 17px; font-weight: 600; color: #CBD5E1; margin: 20px 0 10px; }}
  .section h4 {{ font-size: 14px; font-weight: 600; color: #94A3B8; margin: 12px 0 6px; text-transform:uppercase; letter-spacing:0.5px; }}
  .section p {{ color: #94A3B8; font-size: 14px; margin-bottom: 10px; }}
  .section ul {{ padding-left: 22px; margin: 8px 0; }}
  .section li {{ color: #94A3B8; font-size: 14px; margin: 5px 0; }}

  /* Dimension Grid */
  .dim-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin: 18px 0; }}
  @media (max-width: 700px) {{ .dim-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
  .dim-card {{ background: #0F172A; border: 1px solid #334155; border-radius: 14px; padding: 20px 14px; text-align: center; transition: transform 0.2s, border-color 0.2s; cursor: default; }}
  .dim-card:hover {{ transform: translateY(-2px); border-color: #6366F1; }}
  .dim-card .dim-icon {{ font-size: 26px; margin-bottom: 8px; }}
  .dim-card .dim-name {{ font-size: 12px; color: #64748B; margin-bottom: 6px; }}
  .dim-card .dim-score {{ font-size: 32px; font-weight: 900; letter-spacing: -1px; }}
  .dim-card .dim-weight {{ font-size: 11px; color: #475569; margin-top: 2px; }}

  /* Info Card */
  .info-card {{ background: #1E1B4B; border-left: 4px solid #6366F1; border-radius: 0 10px 10px 0; padding: 18px 22px; margin: 14px 0; }}
  .info-card.warn {{ background: #2D1B0E; border-color: #F59E0B; }}
  .info-card.success {{ background: #0B2E1F; border-color: #10B981; }}
  .info-card.danger {{ background: #2D0E0E; border-color: #EF4444; }}

  /* Table */
  table {{ width: 100%; border-collapse: collapse; margin: 14px 0; font-size: 13px; }}
  th {{ background: #0F172A; padding: 12px 16px; text-align: left; font-weight: 600; color: #CBD5E1; border-bottom: 2px solid #334155; }}
  td {{ padding: 12px 16px; border-bottom: 1px solid #1E293B; color: #94A3B8; }}
  tr:hover td {{ background: rgba(99,102,241,0.05); }}

  /* Tags */
  .tag {{ display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; margin: 2px; }}
  .tag-blue {{ background: #1E3A5F; color: #60A5FA; }}
  .tag-green {{ background: #064E3B; color: #34D399; }}
  .tag-yellow {{ background: #78350F; color: #FBBF24; }}
  .tag-red {{ background: #7F1D1D; color: #FCA5A5; }}
  .tag-purple {{ background: #4C1D95; color: #C4B5FD; }}

  /* Risk Matrix */
  .risk-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }}
  @media (max-width: 600px) {{ .risk-grid {{ grid-template-columns: 1fr; }} }}
  .risk-item {{ background: #0F172A; border: 1px solid #334155; border-radius: 12px; padding: 18px; }}
  .risk-item .risk-level {{ font-size: 12px; font-weight: 700; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px; }}

  /* Radar Container */
  .radar-wrap {{ background: #0F172A; border-radius: 16px; padding: 20px; margin: 16px 0; display: flex; justify-content: center; }}
  .radar-wrap canvas {{ max-width: 100%; height: auto; }}

  /* Timeline */
  .timeline {{ position: relative; padding-left: 24px; margin: 14px 0; }}
  .timeline::before {{ content: ''; position: absolute; left: 8px; top: 0; bottom: 0; width: 2px; background: #334155; }}
  .timeline-item {{ position: relative; margin-bottom: 18px; padding-left: 20px; }}
  .timeline-item::before {{ content: ''; position: absolute; left: -20px; top: 6px; width: 12px; height: 12px; border-radius: 50%; background: #6366F1; border: 2px solid #1E293B; }}
  .timeline-item .tl-title {{ font-weight: 700; color: #F1F5F9; font-size: 14px; }}
  .timeline-item .tl-desc {{ color: #94A3B8; font-size: 13px; margin-top: 2px; }}

  /* Progress Ring (Mini) */
  .progress-ring {{ display: inline-flex; align-items: center; gap: 8px; }}
  .progress-ring svg {{ width: 48px; height: 48px; }}

  /* Footer */
  .footer {{ text-align: center; padding: 30px; color: #475569; font-size: 12px; }}

  /* Flash highlight */
  @keyframes pulse {{ 0%,100% {{ box-shadow: 0 0 0 0 {score_result['color']}40; }} 50% {{ box-shadow: 0 0 0 12px {score_result['color']}00; }} }}
  .pulse {{ animation: pulse 2s infinite; }}

  /* Print */
  @media print {{ body {{ background: white; color: #1F2937; }} .section {{ background: white; border: 1px solid #E5E7EB; }} }}
"""

    # ============================================================
    # HTML Build
    # ============================================================
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Agent 开发可行性决策报告 - {name}</title>
<style>{css}</style>
</head>
<body>
<div class="container">

  <!-- ===== COVER ===== -->
  <div class="cover">
    <h1>🤖 {name}</h1>
    <div class="subtitle">{direction}</div>
    <div class="badge">🧬 AI Agent 开发可行性决策报告</div>
    <div class="date">评估时间：{now} &nbsp;|&nbsp; 数据来源：公开信息综合分析</div>
  </div>

  <!-- ===== SCORE CARD ===== -->
  <div class="score-card pulse">
    <div class="big-score">{score_result['total']}</div>
    <div class="rating">{score_result['icon']} {score_result['rating']}</div>
    <div class="rating-desc">{score_result['rating_desc']}</div>
  </div>

  <!-- ===== RADAR CHART ===== -->
  <div class="section">
    <h2>📊 八维度能力雷达图</h2>
    <div class="radar-wrap">
      <canvas id="radarChart" width="480" height="480"></canvas>
    </div>
"""
    # Dimension cards
    html += '<div class="dim-grid">'
    for key, dim in DIMENSIONS.items():
        s = score_result["dimensions"].get(key, 50)
        if s >= 80:
            sc = "#10B981"
        elif s >= 65:
            sc = "#3B82F6"
        elif s >= 50:
            sc = "#F59E0B"
        else:
            sc = "#EF4444"
        html += f"""
      <div class="dim-card">
        <div class="dim-icon">{dim['icon']}</div>
        <div class="dim-name">{dim['name']}</div>
        <div class="dim-score" style="color:{sc}">{s}</div>
        <div class="dim-weight">权重 {int(dim['weight']*100)}%</div>
      </div>"""
    html += '\n    </div>\n  </div>\n'

    # ============================================================
    # 1. 技术选型分析
    # ============================================================
    tech_score = safe_get(tech, "score", safe_get(scores, "tech_maturity", 50))
    tech_llm_options = safe_get(tech, "llm_options", [])
    tech_frameworks = safe_get(tech, "frameworks", [])
    tech_architecture = safe_get(tech, "architecture", "待评估")
    tech_detail = safe_get(tech, "detail", "暂无详细数据")

    html += f"""
  <!-- 1. Tech Selection -->
  <div class="section">
    <h2>🧠 一、技术选型分析</h2>
    {make_score_bar(tech_score)}
    <p>{tech_detail}</p>
"""

    if tech_llm_options:
        html += '<h3>🤖 LLM 模型推荐</h3><table><tr><th>模型</th><th>精度</th><th>速度</th><th>成本</th><th>推荐场景</th><th>风险提示</th></tr>'
        for opt in tech_llm_options:
            html += f"<tr><td>{safe_get(opt,'name')}</td><td>{safe_get(opt,'accuracy')}</td><td>{safe_get(opt,'speed')}</td><td>{safe_get(opt,'cost')}</td><td>{safe_get(opt,'scenario')}</td><td style='font-size:12px;color:#FCA5A5'>{safe_get(opt,'risk')}</td></tr>"
        html += '</table>'

    if tech_frameworks:
        html += '<h3>🏗️ Agent 框架选型</h3><table><tr><th>框架</th><th>类型</th><th>优势</th><th>劣势</th><th>适用阶段</th></tr>'
        for fw in tech_frameworks:
            html += f"<tr><td><strong>{safe_get(fw,'name')}</strong></td><td>{safe_get(fw,'type')}</td><td style='color:#34D399'>{safe_get(fw,'pros')}</td><td style='color:#FCA5A5'>{safe_get(fw,'cons')}</td><td>{safe_get(fw,'stage')}</td></tr>"
        html += '</table>'

    html += f"""
    <div class="info-card success">
      <strong>🏆 推荐架构方案：</strong>{tech_architecture}
    </div>
  </div>
"""

    # ============================================================
    # 2. 竞品格局分析
    # ============================================================
    comp_count = safe_get(competitors, "count", "未知")
    comp_top3 = safe_get(competitors, "top3", [])
    comp_detail = safe_get(competitors, "detail", "暂无详细数据")
    comp_saturation = safe_get(competitors, "saturation", "中等")
    comp_diff = safe_get(competitors, "differentiation", "暂无差异化分析")

    sat_color = "#34D399" if "低" in str(comp_saturation) else ("#FBBF24" if "中" in str(comp_saturation) else "#FCA5A5")
    sat_icon = "🟢" if "低" in str(comp_saturation) else ("🟡" if "中" in str(comp_saturation) else "🔴")

    html += f"""
  <!-- 2. Competitors -->
  <div class="section">
    <h2>⚔️ 二、竞品格局分析</h2>
    <div class="info-card">
      <strong>已发现竞品数量：</strong><span style="font-size:24px;font-weight:900;color:{sat_color};margin:0 8px;">{comp_count}</span> 个
      &nbsp;&nbsp;市场饱和度：<span style="color:{sat_color};font-weight:700;">{sat_icon} {comp_saturation}</span>
    </div>
    <p>{comp_detail}</p>
"""

    if comp_top3:
        html += '<h3>🏅 头部竞品拆解</h3><table><tr><th>排名</th><th>产品名称</th><th>核心能力</th><th>定价</th><th>优劣势</th></tr>'
        for i, cp in enumerate(comp_top3, 1):
            html += f"<tr><td>#{i}</td><td><strong>{safe_get(cp,'name')}</strong></td><td>{safe_get(cp,'features')}</td><td>{safe_get(cp,'pricing')}</td><td>{safe_get(cp,'swot')}</td></tr>"
        html += '</table>'

    html += f"""
    <div class="info-card">
      <strong>💡 差异化机会：</strong>{comp_diff}
    </div>
  </div>
"""

    # ============================================================
    # 3. 市场前景分析
    # ============================================================
    mkt_size = safe_get(market, "size", "待评估")
    mkt_growth = safe_get(market, "growth", "待评估")
    mkt_forecast = safe_get(market, "forecast", "暂无预测数据")
    mkt_detail = safe_get(market, "detail", "暂无详细数据")
    mkt_segments = safe_get(market, "segments", [])

    html += f"""
  <!-- 3. Market -->
  <div class="section">
    <h2>📈 三、市场前景分析</h2>
    <div class="info-card success">
      <strong>当前市场规模：</strong><span style="font-size:28px;font-weight:900;color:#34D399;">{mkt_size}</span>
      &nbsp;&nbsp;年增长率：<span style="color:#34D399;font-weight:700;font-size:18px;">{mkt_growth}</span>
    </div>
    <p>{mkt_detail}</p>
    <h3>🔮 市场预测</h3>
    <p>{mkt_forecast}</p>
"""
    if mkt_segments:
        html += '<h3>🎯 细分赛道机会</h3><table><tr><th>细分赛道</th><th>当前规模</th><th>增长潜力</th><th>Agent适配度</th><th>机会评估</th></tr>'
        for seg in mkt_segments:
            html += f"<tr><td>{safe_get(seg,'name')}</td><td>{safe_get(seg,'size')}</td><td>{safe_get(seg,'growth')}</td><td>{safe_get(seg,'fit')}</td><td>{safe_get(seg,'opportunity')}</td></tr>"
        html += '</table>'
    html += '  </div>\n'

    # ============================================================
    # 4. 行业趋势分析
    # ============================================================
    ind_trend = safe_get(industry, "trend", "平稳发展")
    ind_hot_scenarios = safe_get(industry, "hot_scenarios", [])
    ind_detail = safe_get(industry, "detail", "暂无详细数据")
    ind_investment = safe_get(industry, "investment", "暂无数据")

    trend_icon = "📈" if "上升" in str(ind_trend) or "快速" in str(ind_trend) else ("📉" if "下降" in str(ind_trend) else "➡️")
    trend_color = "#34D399" if "上升" in str(ind_trend) or "快速" in str(ind_trend) else ("#FCA5A5" if "下降" in str(ind_trend) else "#FBBF24")

    html += f"""
  <!-- 4. Industry -->
  <div class="section">
    <h2>🌊 四、行业趋势分析</h2>
    <div class="info-card">
      <strong>Agent 行业趋势：</strong><span style="color:{trend_color};font-weight:700;font-size:16px;">{trend_icon} {ind_trend}</span>
    </div>
    <p>{ind_detail}</p>
"""
    if ind_hot_scenarios:
        html += '<h3>🔥 热门落地场景</h3><table><tr><th>场景</th><th>热度</th><th>代表性产品</th><th>技术难度</th><th>商业化阶段</th></tr>'
        for sc in ind_hot_scenarios:
            html += f"<tr><td>{safe_get(sc,'name')}</td><td>{safe_get(sc,'heat')}</td><td>{safe_get(sc,'examples')}</td><td>{safe_get(sc,'difficulty')}</td><td>{safe_get(sc,'stage')}</td></tr>"
        html += '</table>'

    html += f"""
    <div class="info-card">
      <strong>💰 投资热度：</strong>{ind_investment}
    </div>
  </div>
"""

    # ============================================================
    # 5. 开发可行性评估
    # ============================================================
    fea_difficulty = safe_get(feasibility, "difficulty", "中等")
    fea_team_match = safe_get(feasibility, "team_match", "待评估")
    fea_timeline = safe_get(feasibility, "timeline", "3-6个月")
    fea_detail = safe_get(feasibility, "detail", "暂无详细数据")
    fea_risks = safe_get(feasibility, "risks", [])
    fea_milestones = safe_get(feasibility, "milestones", [])

    diff_icon = "🟢" if "低" in str(fea_difficulty) else ("🟡" if "中" in str(fea_difficulty) else "🔴")

    html += f"""
  <!-- 5. Feasibility -->
  <div class="section">
    <h2>🔧 五、开发可行性评估</h2>
    <div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:14px;">
      <div style="flex:1;min-width:180px;background:#0F172A;border-radius:12px;padding:20px;text-align:center;border:1px solid #334155;">
        <div style="font-size:12px;color:#64748B;margin-bottom:4px;">技术难度</div>
        <div style="font-size:28px;">{diff_icon}</div>
        <div style="font-weight:700;color:#CBD5E1;">{fea_difficulty}</div>
      </div>
      <div style="flex:1;min-width:180px;background:#0F172A;border-radius:12px;padding:20px;text-align:center;border:1px solid #334155;">
        <div style="font-size:12px;color:#64748B;margin-bottom:4px;">团队匹配度</div>
        <div style="font-size:28px;">{fea_team_match}</div>
      </div>
      <div style="flex:1;min-width:180px;background:#0F172A;border-radius:12px;padding:20px;text-align:center;border:1px solid #334155;">
        <div style="font-size:12px;color:#64748B;margin-bottom:4px;">预计开发周期</div>
        <div style="font-size:20px;font-weight:900;color:#6366F1;">{fea_timeline}</div>
      </div>
    </div>
    <p>{fea_detail}</p>
"""
    if fea_risks:
        html += '<h3>⚠️ 开发阶段风险点</h3>'
        for r in fea_risks:
            html += f'<div class="info-card warn"><strong>{safe_get(r,"title")}：</strong>{safe_get(r,"desc")} <span style="font-size:12px;color:#FBBF24;">→ {safe_get(r,"mitigation")}</span></div>'

    if fea_milestones:
        html += '<h3>🗓️ 建议里程碑</h3><div class="timeline">'
        for ms in fea_milestones:
            html += f'<div class="timeline-item"><div class="tl-title">{safe_get(ms,"phase")}</div><div class="tl-desc">{safe_get(ms,"desc")} | {safe_get(ms,"duration")}</div></div>'
        html += '</div>'

    html += '  </div>\n'

    # ============================================================
    # 6. 系统稳定性方案
    # ============================================================
    stab_hallucination = safe_get(stability, "hallucination_control", "待评估")
    stab_reliability = safe_get(stability, "reliability", "待评估")
    stab_monitoring = safe_get(stability, "monitoring", "待评估")
    stab_detail = safe_get(stability, "detail", "暂无详细数据")
    stab_strategies = safe_get(stability, "strategies", [])

    html += f"""
  <!-- 6. Stability -->
  <div class="section">
    <h2>🛡️ 六、系统稳定性方案</h2>
    <p>{stab_detail}</p>
"""
    html += '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:12px 0;">'
    html += f'<div class="info-card"><strong>🎯 幻觉控制</strong><br><span style="font-size:13px;color:#94A3B8;">{stab_hallucination}</span></div>'
    html += f'<div class="info-card success"><strong>✅ 可靠性设计</strong><br><span style="font-size:13px;color:#94A3B8;">{stab_reliability}</span></div>'
    html += f'<div class="info-card warn"><strong>📡 监控体系</strong><br><span style="font-size:13px;color:#94A3B8;">{stab_monitoring}</span></div>'
    html += '</div>'

    if stab_strategies:
        html += '<h3>🔧 稳定性保障策略清单</h3><table><tr><th>策略</th><th>实施方式</th><th>优先级</th><th>效果预期</th></tr>'
        for st in stab_strategies:
            html += f"<tr><td><strong>{safe_get(st,'name')}</strong></td><td>{safe_get(st,'impl')}</td><td>{safe_get(st,'priority')}</td><td>{safe_get(st,'effect')}</td></tr>"
        html += '</table>'
    html += '  </div>\n'

    # ============================================================
    # 7. 成本预算估算
    # ============================================================
    cost_api = safe_get(cost, "api_monthly", "待估算")
    cost_infra = safe_get(cost, "infra", "待估算")
    cost_labor = safe_get(cost, "labor", "待估算")
    cost_total = safe_get(cost, "total_annual", "待估算")
    cost_detail = safe_get(cost, "detail", "暂无详细数据")
    cost_items = safe_get(cost, "items", [])

    html += f"""
  <!-- 7. Cost -->
  <div class="section">
    <h2>💰 七、成本预算估算</h2>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:16px;">
      <div style="background:#0F172A;border-radius:12px;padding:16px;text-align:center;border:1px solid #334155;">
        <div style="font-size:11px;color:#64748B;">🤖 API月成本</div>
        <div style="font-size:18px;font-weight:900;color:#F97316;">{cost_api}</div>
      </div>
      <div style="background:#0F172A;border-radius:12px;padding:16px;text-align:center;border:1px solid #334155;">
        <div style="font-size:11px;color:#64748B;">🖥️ 基础设施</div>
        <div style="font-size:18px;font-weight:900;color:#3B82F6;">{cost_infra}</div>
      </div>
      <div style="background:#0F172A;border-radius:12px;padding:16px;text-align:center;border:1px solid #334155;">
        <div style="font-size:11px;color:#64748B;">👥 人力投入</div>
        <div style="font-size:18px;font-weight:900;color:#8B5CF6;">{cost_labor}</div>
      </div>
      <div style="background:#0F172A;border-radius:12px;padding:16px;text-align:center;border:1px solid #334155;">
        <div style="font-size:11px;color:#64748B;">📊 年度总TCO</div>
        <div style="font-size:18px;font-weight:900;color:#EC4899;">{cost_total}</div>
      </div>
    </div>
    <p>{cost_detail}</p>
"""
    if cost_items:
        html += '<h3>💸 成本明细</h3><table><tr><th>成本项</th><th>月均</th><th>年均</th><th>备注</th></tr>'
        for ci in cost_items:
            html += f"<tr><td>{safe_get(ci,'name')}</td><td>{safe_get(ci,'monthly')}</td><td>{safe_get(ci,'annual')}</td><td style='font-size:12px;'>{safe_get(ci,'note')}</td></tr>"
        html += '</table>'
    html += '  </div>\n'

    # ============================================================
    # 8. 推广策略建议
    # ============================================================
    promo_gtm = safe_get(promotion, "gtm", "待制定")
    promo_channels = safe_get(promotion, "channels", [])
    promo_pricing = safe_get(promotion, "pricing", "待确定")
    promo_detail = safe_get(promotion, "detail", "暂无详细数据")
    promo_phases = safe_get(promotion, "phases", [])

    html += f"""
  <!-- 8. Promotion -->
  <div class="section">
    <h2>🚀 八、推广策略建议</h2>
    <div class="info-card success">
      <strong>🎯 GTM 策略：</strong>{promo_gtm}
    </div>
    <p>{promo_detail}</p>
    <h3>📢 定价模式建议</h3>
    <div class="info-card"><strong>{promo_pricing}</strong></div>
"""
    if promo_channels:
        html += '<h3>📣 获客渠道矩阵</h3><table><tr><th>渠道</th><th>类型</th><th>预期CPA</th><th>优先级</th><th>策略要点</th></tr>'
        for ch in promo_channels:
            html += f"<tr><td>{safe_get(ch,'name')}</td><td>{safe_get(ch,'type')}</td><td>{safe_get(ch,'cpa')}</td><td>{safe_get(ch,'priority')}</td><td>{safe_get(ch,'tactics')}</td></tr>"
        html += '</table>'

    if promo_phases:
        html += '<h3>📅 推广阶段规划</h3><div class="timeline">'
        for ph in promo_phases:
            html += f'<div class="timeline-item"><div class="tl-title">{safe_get(ph,"phase")}</div><div class="tl-desc">{safe_get(ph,"desc")} | 目标：{safe_get(ph,"target")}</div></div>'
        html += '</div>'
    html += '  </div>\n'

    # ============================================================
    # 9. 风险矩阵
    # ============================================================
    risks = safe_get(data, "risks", {})
    risk_items = safe_get(risks, "items", [])

    if not risk_items:
        # Default risk items
        risk_items = [
            {"category": "技术风险", "level": "中", "desc": "LLM能力边界不确定，幻觉率可能影响用户体验", "mitigation": "多模型fallback + 人工兜底 + 输出校验层"},
            {"category": "市场风险", "level": "中", "desc": "Agent赛道拥挤，头部产品可能快速覆盖长尾需求", "mitigation": "垂直场景深耕 + 数据壁垒构建"},
            {"category": "竞争风险", "level": "高", "desc": "大厂（字节/阿里/腾讯）可能推出同类免费产品", "mitigation": "差异化定位 + 私域运营 + 快速迭代"},
            {"category": "合规风险", "level": "中高", "desc": "AI生成内容标识法规、数据安全法、个人信息保护法", "mitigation": "合规前置 + 法务审查 + C2PA标识"},
            {"category": "成本风险", "level": "中", "desc": "LLM API价格波动 + 用户量增长导致边际成本上升", "mitigation": "自托管模型 + Token优化 + 分层定价"},
            {"category": "运营风险", "level": "中低", "desc": "用户留存难、付费转化低、Prompt漂移", "mitigation": "A/B测试 + 用户反馈闭环 + Prompt版本管理"},
        ]

    html += """
  <!-- 9. Risk Matrix -->
  <div class="section">
    <h2>⚠️ 九、风险矩阵</h2>
    <div class="risk-grid">
"""
    level_map = {"高": ("🔴 高风险", "#EF4444"), "中高": ("🟠 中高风险", "#F97316"), "中": ("🟡 中等风险", "#F59E0B"), "中低": ("🟢 中低风险", "#10B981"), "低": ("🟢 低风险", "#10B981")}

    for r in risk_items:
        cat = safe_get(r, "category", "")
        lvl = safe_get(r, "level", "中")
        lbl, lc = level_map.get(lvl, ("🟡 中等风险", "#F59E0B"))
        html += f"""      <div class="risk-item">
        <div class="risk-level" style="color:{lc}">{lbl} &nbsp;|&nbsp; {cat}</div>
        <div style="color:#E2E8F0;font-weight:600;margin:4px 0;">{safe_get(r, 'desc', '')}</div>
        <div style="color:#94A3B8;font-size:12px;">💡 应对：{safe_get(r, 'mitigation', '')}</div>
      </div>
"""
    html += """    </div>
  </div>
"""

    # ============================================================
    # 10. 综合决策建议
    # ============================================================
    html += f"""
  <!-- 10. Final Decision -->
  <div class="section" style="border:2px solid {score_result['color']};">
    <h2>🎯 十、综合决策建议</h2>
    <div class="info-card" style="background:{score_result['bg']};border-color:{score_result['color']};">
      <strong style="font-size:18px;">{score_result['icon']} 最终建议：{score_result['rating']}</strong>
      <p style="margin-top:6px;">{score_result['rating_desc']}</p>
    </div>

    <h3>📋 加权评分汇总</h3>
    <table>
      <tr><th>评估维度</th><th>得分</th><th>权重</th><th>加权得分</th><th>评价</th></tr>
"""
    for key, dim in DIMENSIONS.items():
        s = score_result["dimensions"].get(key, 50)
        w = dim["weight"]
        ws = round(s * w, 1)
        if s >= 80:
            ev = "优秀"
            et = "tag-green"
        elif s >= 65:
            ev = "良好"
            et = "tag-blue"
        elif s >= 50:
            ev = "一般"
            et = "tag-yellow"
        else:
            ev = "薄弱"
            et = "tag-red"
        html += f"""      <tr><td>{dim['icon']} {dim['name']}</td><td><strong>{s}</strong></td><td>{int(w*100)}%</td><td><strong>{ws}</strong></td><td><span class="tag {et}">{ev}</span></td></tr>
"""
    html += f"""      <tr style="background:#1E1B4B;font-weight:700;"><td colspan="3">📊 综合加权总分</td><td style="font-size:24px;color:{score_result['color']};">{score_result['total']}</td><td><span class="tag tag-purple">满分100</span></td></tr>
    </table>

    <h3>🗺️ 建议行动路线图</h3>
    <div class="timeline">
      <div class="timeline-item">
        <div class="tl-title">Phase 1: 验证期（第1-2个月）</div>
        <div class="tl-desc">技术可行性验证 → MVP原型开发 → 核心用户内测 → 幻觉率基线测试</div>
      </div>
      <div class="timeline-item">
        <div class="tl-title">Phase 2: 打磨期（第3-4个月）</div>
        <div class="tl-desc">Prompt优化迭代 → 评测体系建设 → 多模型Fallback → 付费模式验证</div>
      </div>
      <div class="timeline-item">
        <div class="tl-title">Phase 3: 增长期（第5-6个月）</div>
        <div class="tl-desc">正式上线发布 → 渠道推广 → 用户增长 → 监控告警体系完善</div>
      </div>
      <div class="timeline-item">
        <div class="tl-title">Phase 4: 规模化（第7-12个月）</div>
        <div class="tl-desc">多Agent协作 → 知识库扩展 → 成本优化 → 企业级功能迭代</div>
      </div>
    </div>

    <div class="info-card warn">
      <strong>⚡ 关键决策检查点：</strong>第2个月末进行Go/No-Go决策评审 — 幻觉率&lt;5%、用户满意度&gt;4.0/5、日活留存&gt;30% 为继续标准
    </div>
  </div>

  <!-- Footer -->
  <div class="footer">
    <p>🤖 AI Agent 开发可行性决策报告 &nbsp;|&nbsp; 生成时间：{now} &nbsp;|&nbsp; 仅供决策参考，不构成投资建议</p>
    <p style="margin-top:4px;">报告基于公开信息综合分析生成 &nbsp;|&nbsp; 数据可能存在时效性偏差</p>
  </div>

</div>
"""
    # ============================================================
    # JavaScript data for Radar Chart
    # ============================================================
    dims_js = []
    scores_js = []
    for key, dim in DIMENSIONS.items():
        dims_js.append({"name": dim["name"], "color": dim["color"]})
        scores_js.append(score_result["dimensions"].get(key, 50))

    js_data = f"""
<script>
const DIMENSIONS_DATA = {json.dumps(dims_js, ensure_ascii=False)};
const SCORES_DATA = {json.dumps(scores_js)};
</script>
"""
    html += js_data
    html += RADAR_CHART_JS
    html += "\n</body>\n</html>"

    return html


# ============================================================
# CLI Entry Point
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="AI Agent 开发决策报告生成器")
    parser.add_argument("--name", required=True, help="产品名称")
    parser.add_argument("--direction", required=True, help="产品方向")
    parser.add_argument("--output", required=True, help="输出HTML文件路径")
    parser.add_argument("--scores", default="{}", help="JSON格式的8维度评分")
    parser.add_argument("--tech", default="{}", help="JSON格式的技术选型数据")
    parser.add_argument("--competitors", default="{}", help="JSON格式的竞品数据")
    parser.add_argument("--market", default="{}", help="JSON格式的市场数据")
    parser.add_argument("--industry", default="{}", help="JSON格式的行业数据")
    parser.add_argument("--feasibility", default="{}", help="JSON格式的可行性数据")
    parser.add_argument("--stability", default="{}", help="JSON格式的稳定性数据")
    parser.add_argument("--cost", default="{}", help="JSON格式的成本数据")
    parser.add_argument("--promotion", default="{}", help="JSON格式的推广数据")
    parser.add_argument("--risks", default="{}", help="JSON格式的风险数据")

    args = parser.parse_args()

    data = {
        "name": args.name,
        "direction": args.direction,
        "scores": json.loads(args.scores),
        "tech": json.loads(args.tech),
        "competitors": json.loads(args.competitors),
        "market": json.loads(args.market),
        "industry": json.loads(args.industry),
        "feasibility": json.loads(args.feasibility),
        "stability": json.loads(args.stability),
        "cost": json.loads(args.cost),
        "promotion": json.loads(args.promotion),
        "risks": json.loads(args.risks),
    }

    html = generate_report(data)
    Path(args.output).write_text(html, encoding="utf-8")
    print(f"✅ 报告已生成: {args.output}")


if __name__ == "__main__":
    main()

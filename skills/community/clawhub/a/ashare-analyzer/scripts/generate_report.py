#!/usr/bin/env python3
"""
Generate a self-contained HTML analysis report from data bundle + narrative JSON.

Usage:
  python generate_report.py --data data_002418.json --narrative narrative_002418.json --outdir ./output
"""
import argparse
import base64
import json
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


# ============================================================
# Helpers
# ============================================================

def _f(v, fmt=".2f", suffix="", prefix="", default="-"):
    """Format a number safely."""
    if v is None:
        return default
    try:
        return f"{prefix}{float(v):{fmt}}{suffix}"
    except (TypeError, ValueError):
        return default


def _pct(v, fmt="+.2f", default="-"):
    """Format a percentage with sign."""
    if v is None:
        return default
    try:
        v = float(v)
        return f"{v:+{fmt.strip('+')}}%"
    except (TypeError, ValueError):
        return default


def _img_to_base64(path):
    """Read image file and return base64 data URI."""
    if not path or not os.path.isfile(path):
        return ""
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("ascii")
    ext = os.path.splitext(path)[1].lower()
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg"}.get(ext.lstrip("."), "image/png")
    return f"data:{mime};base64,{data}"


def pct_today_label(pct):
    if pct is None:
        return "暂缺"
    if pct > 9.8:
        return "涨停"
    if pct < -9.8:
        return "跌停"
    if pct > 0:
        return "上涨"
    if pct < 0:
        return "下跌"
    return "平盘"


def pe_label(pe):
    if pe is None:
        return "暂缺"
    if pe < 0:
        return f"{pe:.2f}x <span class='warn'>⚠️亏损股，PE失真</span>"
    if pe > 200:
        return f"{pe:.2f}x <span class='warn'>（估值极高）</span>"
    return f"{pe:.2f}x"


def roe_label(roe):
    if roe is None:
        return "暂缺"
    if roe > 15:
        return f"{roe:.2f}% <span class='good'>（优秀）</span>"
    if roe > 10:
        return f"{roe:.2f}% <span class='good'>（良好）</span>"
    if roe > 5:
        return f"{roe:.2f}% （一般）"
    if roe > 1:
        return f"{roe:.2f}% <span class='warn'>（较差）</span>"
    if roe > 0:
        return f"{roe:.2f}% <span class='warn'>（极差）</span>"
    return f"{roe:.2f}% <span class='warn'>⚠️亏损</span>"


def fundamental_source_label(src):
    mapping = {
        "tushare": "tushare pro（基本面）",
        "akshare": "akshare（基本面）",
        "baostock": "baostock（基本面）",
        "eastmoney": "东方财富数据中心（基本面）",
        "eastmoney_datacenter": "东方财富数据中心（基本面）",
    }
    return mapping.get(src, "网络公开资料（基本面）")


def price_source_label(src):
    mapping = {
        "tushare": "tushare pro（价量）",
        "tencent": "腾讯财经（价量）",
    }
    return mapping.get(src, src or "未知")


def star_html(n, max_n=5):
    """Generate star rating HTML."""
    return "<span class='stars'>" + "★" * n + "<span class='star-dim'>" + "★" * (max_n - n) + "</span></span>"


def impact_badge(level):
    colors = {"高": "#e74c3c", "中高": "#e67e22", "中": "#f39c12", "低": "#3498db"}
    c = colors.get(level, "#8892a0")
    return f"<span class='badge' style='background:{c}'>{level}</span>"


# ============================================================
# HTML Template
# ============================================================

def build_html(data, narrative, kline_b64, compare_b64):
    meta = data["meta"]
    price = data["price"]
    fin = data.get("financials") or {}
    mbiz = data.get("main_business") or {}
    tech = data.get("technicals") or {}
    mkt = data.get("market_compare") or {}
    peers = data.get("peers") or []
    sources = meta.get("data_sources") or {}

    # Extract actual peer data sources from _source fields
    peer_rt_srcs = set()
    peer_fund_srcs = set()
    for p in peers:
        src = p.get("_source", "")
        for part in src.split("｜"):
            if part.startswith("行情:"):
                peer_rt_srcs.add(part.split(":", 1)[1])
            elif part.startswith("基本面:"):
                peer_fund_srcs.add(part.split(":", 1)[1])
    peer_rt_label = "、".join(sorted(peer_rt_srcs)) if peer_rt_srcs else "未知"
    peer_fund_label = "、".join(sorted(peer_fund_srcs)) if peer_fund_srcs else "未知"

    n = narrative  # shorthand
    name = meta["name"]
    code6 = meta["code6"]
    date = meta["analysis_date"]

    # Build peer comparison table rows
    peer_headers = "".join(f"<th>{p['name']}<br><span class='peer-src'>{p.get('source','').split(':')[0]}</span></th>" for p in peers)
    peer_row = lambda fn: "".join(f"<td>{fn(p)}</td>" for p in peers)

    # Main business table
    biz_rows = ""
    products = mbiz.get("by_product") or mbiz.get("by_industry") or []
    for item in products[:5]:
        ratio = (item.get("revenue_ratio") or 0) * 100
        if ratio < 1 and "其他" in item.get("item", ""):
            continue
        rev_yi = (item.get("revenue") or 0) / 1e8
        gm = (item.get("gross_margin") or 0) * 100
        biz_rows += f"<tr><td>{item['item']}</td><td>{rev_yi:.2f}</td><td>{ratio:.1f}%</td><td>{gm:.2f}%</td></tr>"

    # Catalysts & risks
    cat_html = ""
    for c in n.get("catalysts", []):
        cat_html += f"<li><strong>{c['title']}</strong> {impact_badge(c.get('impact','中'))}：{c['desc']}</li>"
    risk_html = ""
    for r in n.get("risks", []):
        risk_html += f"<li><strong>{r['title']}</strong> {impact_badge(r.get('impact','中'))}：{r['desc']}</li>"

    # Stars
    stars = n.get("stars", {})
    stars_comment = n.get("stars_comment", {})

    # Technical score color
    ts = n.get("tech_score", 0)
    if ts >= 5:
        ts_color = "#2ecc71"
        ts_word = "偏多"
    elif ts >= 2:
        ts_color = "#f5c518"
        ts_word = "中性偏多"
    elif ts >= -1:
        ts_color = "#8892a0"
        ts_word = "中性"
    elif ts >= -4:
        ts_color = "#e67e22"
        ts_word = "中性偏空"
    else:
        ts_color = "#e74c3c"
        ts_word = "偏空"

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} ({code6}) 综合分析报告</title>
<style>
:root {{
  --bg: #1a2332;
  --card: #1e2a3a;
  --border: #2a3544;
  --text: #d0d5dc;
  --muted: #8892a0;
  --accent: #f5c518;
  --up: #e74c3c;
  --down: #2ecc71;
  --warn: #e67e22;
  --good: #2ecc71;
}}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
  font-family: -apple-system, "Microsoft YaHei", "SimHei", "Noto Sans CJK SC", sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.7;
  padding: 20px;
  max-width: 1100px;
  margin: 0 auto;
}}
h1 {{ font-size: 1.8em; color: var(--accent); margin-bottom: 4px; }}
h2 {{ font-size: 1.25em; color: var(--text); border-bottom: 2px solid var(--border); padding-bottom: 6px; margin: 28px 0 14px; }}
.subtitle {{ color: var(--muted); margin-bottom: 20px; }}
.card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 16px;
}}
.card-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 12px;
  margin-bottom: 16px;
}}
.kpi {{ text-align: center; padding: 14px 8px; }}
.kpi .label {{ font-size: 0.82em; color: var(--muted); }}
.kpi .value {{ font-size: 1.45em; font-weight: 700; margin-top: 2px; }}
.kpi .value.up {{ color: var(--up); }}
.kpi .value.down {{ color: var(--down); }}
.kpi .value.accent {{ color: var(--accent); }}
.chart-img {{ width: 100%; border-radius: 8px; margin: 8px 0; }}
table {{ width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 0.92em; }}
th, td {{ padding: 8px 10px; text-align: right; border-bottom: 1px solid var(--border); }}
th {{ color: var(--muted); font-weight: 600; text-align: right; }}
th:first-child, td:first-child {{ text-align: left; }}
tr.target {{ background: rgba(245,197,24,0.08); font-weight: 600; }}
.warn {{ color: var(--warn); }}
.good {{ color: var(--good); }}
.badge {{
  display: inline-block;
  padding: 1px 8px;
  border-radius: 10px;
  font-size: 0.78em;
  color: #fff;
  margin-left: 4px;
}}
.peer-src {{ font-size: 0.75em; color: var(--muted); font-weight: normal; }}
.stars {{ color: var(--accent); letter-spacing: 2px; }}
.star-dim {{ color: var(--border); }}
.section-tag {{
  display: inline-block;
  background: var(--accent);
  color: var(--bg);
  padding: 2px 10px;
  border-radius: 4px;
  font-size: 0.82em;
  font-weight: 700;
  margin-bottom: 8px;
}}
ul {{ padding-left: 20px; }}
li {{ margin: 6px 0; }}
.disclaimer {{
  margin-top: 32px;
  padding: 16px;
  background: rgba(142,146,160,0.08);
  border-radius: 8px;
  font-size: 0.85em;
  color: var(--muted);
  text-align: center;
}}
.score-big {{
  font-size: 2.2em;
  font-weight: 800;
  margin-right: 8px;
}}
.score-label {{
  display: inline-block;
  padding: 3px 12px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.9em;
}}
.star-row {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 0;
  border-bottom: 1px solid var(--border);
}}
.star-row:last-child {{ border-bottom: none; }}
.star-label {{ flex: 0 0 80px; font-weight: 600; }}
.star-value {{ flex: 0 0 80px; }}
.star-comment {{ flex: 1; color: var(--muted); font-size: 0.9em; }}
.src-tag {{
  display: block;
  margin-top: 6px;
  font-size: 0.75em;
  color: #5a6577;
  font-style: italic;
}}
</style>
</head>
<body>

<h1>{name} ({code6}) 综合分析</h1>
<p class="subtitle">数据截止：{date}收盘</p>

<!-- ==================== 一、公司速览 ==================== -->
<h2>一、公司速览</h2>
<div class="card">
  <p><strong>行业：</strong>{meta.get('industry','-')}
     <strong>概念板块：</strong>{n.get('concepts','-')}</p>
</div>

<div class="card-grid">
  <div class="kpi">
    <div class="label">股价</div>
    <div class="value {'up' if (price.get('pct_today') or 0) > 0 else 'down'}">{_f(price.get('close'),'.2f','元')}</div>
    <div class="label">{_pct(price.get('pct_today'))} {pct_today_label(price.get('pct_today'))}</div>
  </div>
  <div class="kpi">
    <div class="label">总市值</div>
    <div class="value accent">{_f(price.get('total_mv_yi'),'.1f','亿')}</div>
  </div>
  <div class="kpi">
    <div class="label">PE(TTM)</div>
    <div class="value">{pe_label(price.get('pe_ttm'))}</div>
  </div>
  <div class="kpi">
    <div class="label">PB</div>
    <div class="value">{_f(price.get('pb'),'.2f','x')}</div>
  </div>
  <div class="kpi">
    <div class="label">ROE</div>
    <div class="value">{roe_label(fin.get('roe'))}</div>
  </div>
  <div class="kpi">
    <div class="label">毛利率</div>
    <div class="value">{_f(fin.get('gross_margin'),'.2f','%')}</div>
  </div>
  <div class="kpi">
    <div class="label">换手率</div>
    <div class="value">{_f(price.get('turnover_rate'),'.2f','%')}</div>
  </div>
  <div class="kpi">
    <div class="label">成交额</div>
    <div class="value">{_f(price.get('amount_yi'),'.2f','亿')}</div>
  </div>
</div>

<div class="card">
  <p><strong>最新财报（{fin.get('report_name','-')}）：</strong>
     营收 {_f(fin.get('revenue_yi'),'.2f','亿')}（{_pct(fin.get('revenue_yoy_pct'))}%），
     归母净利 {_f(fin.get('net_profit_wan'),'.0f','万')}（{_pct(fin.get('net_profit_yoy_pct'))}%）</p>
  <p style="margin-top:8px">
    <strong>近期涨跌：</strong>
    1周 {_pct(tech.get('pct_1w'))}% ｜
    1月 <span style="color:{'var(--up)' if (tech.get('pct_1m') or 0) > 0 else 'var(--down)'}">{_pct(tech.get('pct_1m'))}%</span> ｜
    1年 <span style="color:{'var(--up)' if (tech.get('pct_1y') or 0) > 0 else 'var(--down)'}">{_pct(tech.get('pct_1y'))}%</span>
  </p>
  <span class="src-tag">数据来源：实时行情 → 腾讯财经（qt.gtimg.cn）｜财报数据 → {fundamental_source_label(fin.get('source', sources.get('fundamental_used')))}</span>
</div>

<div class="card" style="border-left:3px solid var(--accent); background:rgba(245,197,24,0.05);">
  <p>{n.get('company_comment','')}</p>
</div>

<!-- ==================== 二、K线图 ==================== -->
<h2>二、K线图</h2>
<div class="card">
  {"<img class='chart-img' src='" + kline_b64 + "' alt='K线图'>" if kline_b64 else "<p>K线图暂缺</p>"}
  <p style="margin-top:10px">
    年内最高：<strong style="color:var(--up)">{_f(tech.get('year_high'),'.2f','元')}</strong>（{tech.get('year_high_date','-')}）
    年内最低：<strong style="color:var(--down)">{_f(tech.get('year_low'),'.2f','元')}</strong>（{tech.get('year_low_date','-')}）
  </p>
  <p style="margin-top:4px">{n.get('price_position','')}</p>
  <span class="src-tag">数据来源：K线价量 → {price_source_label(sources.get('price'))}</span>
</div>
<h2>三、主营业务构成</h2>
<div class="card">
  <p style="margin-bottom:8px"><span class="section-tag">{mbiz.get('report_name','-')}</span></p>
  <table>
    <tr><th>业务</th><th>收入（亿元）</th><th>占比</th><th>毛利率</th></tr>
    {biz_rows}
  </table>
  <p style="margin-top:8px;color:var(--muted)">按地区：{n.get('region_summary','-')}</p>
  <p style="margin-top:4px">{n.get('business_comment','')}</p>
  <span class="src-tag">数据来源：东方财富（RPT_F10_FN_MAINOP）</span>
</div>
<h2>四、技术面评分</h2>
<div class="card">
  <p style="margin-bottom:12px">
    <span class="score-big" style="color:{ts_color}">{ts:+d}/10</span>
    <span class="score-label" style="background:{ts_color}20; color:{ts_color}">{ts_word}</span>
    <span style="color:var(--muted); margin-left:8px">{n.get('tech_brief','')}</span>
  </p>
  <table>
    <tr><th>指标</th><th>数值</th><th>判断</th></tr>
    <tr><td>均线排列</td><td>MA5={_f(tech.get('ma5'))} &gt; MA10={_f(tech.get('ma10'))} &gt; MA20={_f(tech.get('ma20'))} &gt; MA60={_f(tech.get('ma60'))}</td><td>{n.get('ma_verdict','-')}</td></tr>
    <tr><td>RSI(14)</td><td>{_f(tech.get('rsi14'))}</td><td>{n.get('rsi_verdict','-')}</td></tr>
    <tr><td>MACD</td><td>DIF={_f(tech.get('macd_dif'))}, DEA={_f(tech.get('macd_dea'))}, 柱={_f(tech.get('macd_hist'))}</td><td>{n.get('macd_verdict','-')}</td></tr>
    <tr><td>布林带</td><td>上轨={_f(tech.get('bb_upper'))}, 下轨={_f(tech.get('bb_lower'))}, 偏离={_f(tech.get('bb_deviation_pct'),'.1f','%')}</td><td>{n.get('bb_verdict','-')}</td></tr>
    <tr><td>KDJ</td><td>K={_f(tech.get('kdj_k'),'.0f')}, D={_f(tech.get('kdj_d'),'.0f')}, J={_f(tech.get('kdj_j'),'.0f')}</td><td>{n.get('kdj_verdict','-')}</td></tr>
    <tr><td>成交量</td><td>换手率 {_f(price.get('turnover_rate'),'.2f','%')}</td><td>{n.get('vol_verdict','-')}</td></tr>
  </table>
  <p style="margin-top:10px">
    关键支撑：<strong>{_f(tech.get('ma5'))}（MA5）</strong> / {_f(tech.get('ma10'))}（MA10） / {_f(tech.get('ma20'))}（MA20）<br>
    关键阻力：<strong>{_f(tech.get('year_high'))}（52周新高）</strong>
  </p>
  <span class="src-tag">数据来源：基于{price_source_label(sources.get('price'))}OHLCV数据本地计算（含120日预热）</span>
</div>
<h2>五、大盘 &amp; 同行业对比</h2>
<div class="card">
  {"<img class='chart-img' src='" + compare_b64 + "' alt='对比图'>" if compare_b64 else ""}
</div>
<div class="card">
  <p><strong>vs 沪深300</strong></p>
  <table>
    <tr><th>周期</th><th>{name}</th><th>沪深300</th></tr>
    <tr><td>近1月</td><td style="color:{'var(--up)' if (tech.get('pct_1m') or 0) > 0 else 'var(--down)'}">{_pct(tech.get('pct_1m'))}%</td><td>{_pct(mkt.get('csi300_pct_1m'))}%</td></tr>
    <tr><td>近1年</td><td style="color:{'var(--up)' if (tech.get('pct_1y') or 0) > 0 else 'var(--down)'}">{_pct(tech.get('pct_1y'))}%</td><td>{_pct(mkt.get('csi300_pct_1y'))}%</td></tr>
  </table>
  <p style="margin-top:6px">{n.get('market_comment','')}</p>
  <span class="src-tag">数据来源：沪深300指数 → {price_source_label(sources.get('price'))}</span>
</div>
  <div style="overflow-x:auto">
  <table>
    <tr><th>指标</th><th><strong>{name}</strong></th>{peer_headers}</tr>
    <tr><td>来源</td><td>(目标)</td>{peer_row(lambda p: f"<span class='peer-src'>{p.get('source','').split(':')[0]}</span>")}</tr>
    <tr class="target"><td>股价</td><td>{_f(price.get('close'),'.2f')}</td>{peer_row(lambda p: _f(p.get('close'),'.2f'))}</tr>
    <tr><td>市值(亿)</td><td>{_f(price.get('total_mv_yi'),'.1f')}</td>{peer_row(lambda p: _f(p.get('total_mv_yi'),'.1f'))}</tr>
    <tr><td>PE(TTM)</td><td>{_f(price.get('pe_ttm'),'.2f')}</td>{peer_row(lambda p: _f(p.get('pe_ttm'),'.2f'))}</tr>
    <tr><td>ROE</td><td>{_f(fin.get('roe'),'.2f','%')}</td>{peer_row(lambda p: _f(p.get('roe'),'.2f','%'))}</tr>
    <tr><td>毛利率</td><td>{_f(fin.get('gross_margin'),'.2f','%')}</td>{peer_row(lambda p: _f(p.get('gross_margin'),'.2f','%'))}</tr>
    <tr><td>营收增速</td><td>{_pct(fin.get('revenue_yoy_pct'))}%</td>{peer_row(lambda p: _pct(p.get('revenue_yoy'))+"%")}</tr>
    <tr><td>利润增速</td><td>{_pct(fin.get('net_profit_yoy_pct'))}%</td>{peer_row(lambda p: _pct(p.get('net_profit_yoy'))+"%")}</tr>
    <tr><td>1年涨幅</td><td style="color:{'var(--up)' if (tech.get('pct_1y') or 0) > 0 else 'var(--down)'}">{_pct(tech.get('pct_1y'))}%</td>{peer_row(lambda p: f"<span style='color:var(--up)'>{_pct(p.get('pct_1y'))}%</span>")}</tr>
  </table>
  </div>
  <div style="margin-top:10px">
    <p><strong>📌 关键发现：</strong></p>
    <ul>
      {"".join(f"<li>{f}</li>" for f in n.get('peer_findings', []))}
    </ul>
  </div>
  <span class="src-tag">数据来源：同行业选股 → 东方财富F10板块（ssbk）｜实时行情 → {peer_rt_label}｜基本面 → {peer_fund_label}</span>
</div>
<h2>六、核心催化剂 &amp; 风险</h2>
<div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
  <div class="card" style="border-left:3px solid var(--good)">
    <p style="font-weight:700; margin-bottom:8px; color:var(--good)">催化剂 🚀</p>
    <ul>{cat_html}</ul>
  </div>
  <div class="card" style="border-left:3px solid var(--warn)">
    <p style="font-weight:700; margin-bottom:8px; color:var(--warn)">风险 ⚠️</p>
    <ul>{risk_html}</ul>
  </div>
</div>

<!-- ==================== 七、买卖建议 ==================== -->
<h2>七、买卖建议</h2>
<div class="card" style="border-left:3px solid var(--accent)">
  <p style="font-size:1.1em; font-weight:700; margin-bottom:12px">{n.get('overall_judgment','')}</p>
</div>

<div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
  <div class="card">
    <p style="font-weight:700; color:var(--accent); margin-bottom:8px">📌 短线（几天～2周）</p>
    <p>技术面：{n.get('short_term',{}).get('tech','-')}</p>
    <p>支撑位 <strong>{n.get('short_term',{}).get('support','-')}</strong> / 阻力位 <strong>{n.get('short_term',{}).get('resist','-')}</strong></p>
    <p>操作建议：<strong>{n.get('short_term',{}).get('advice','-')}</strong></p>
    <p>止损参考：<strong style="color:var(--down)">{n.get('short_term',{}).get('stop_loss','-')}</strong></p>
  </div>
  <div class="card">
    <p style="font-weight:700; color:var(--accent); margin-bottom:8px">📌 中线（1～3个月）</p>
    <p>核心驱动力：{n.get('mid_term',{}).get('drivers','-')}</p>
    <p>估值判断：{n.get('mid_term',{}).get('valuation','-')}</p>
    <p>中期支撑：<strong>{n.get('mid_term',{}).get('support','-')}</strong></p>
    <p>建议：<strong>{n.get('mid_term',{}).get('advice','-')}</strong>，目标 <strong>{n.get('mid_term',{}).get('target','-')}</strong></p>
    <p>情景分析：{n.get('mid_term',{}).get('scenarios','-')}</p>
  </div>
</div>

<div class="card">
  <div class="star-row"><span class="star-label">基本面</span><span class="star-value">{star_html(stars.get('fundamental',0))}</span><span class="star-comment">{stars_comment.get('fundamental','')}</span></div>
  <div class="star-row"><span class="star-label">题材概念</span><span class="star-value">{star_html(stars.get('concept',0))}</span><span class="star-comment">{stars_comment.get('concept','')}</span></div>
  <div class="star-row"><span class="star-label">技术面</span><span class="star-value">{star_html(stars.get('tech',0))}</span><span class="star-comment">{stars_comment.get('tech','')}</span></div>
  <div class="star-row"><span class="star-label">时机</span><span class="star-value">{star_html(stars.get('timing',0))}</span><span class="star-comment">{stars_comment.get('timing','')}</span></div>
</div>

<div class="card" style="border-left:3px solid var(--accent); background:rgba(245,197,24,0.05);">
  <p style="font-size:1.1em; font-weight:700">{n.get('one_liner','')}</p>
</div>

<!-- ==================== 免责声明 ==================== -->
<div class="disclaimer">
  ⚠️ 以上分析仅供参考，不构成投资建议。<br>
  数据来源：{price_source_label(sources.get('price'))}、东方财富（板块+主营业务）、{fundamental_source_label(sources.get('fundamental_used'))}。<br>
  报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
</div>

</body>
</html>"""
    return html


# ============================================================
# Main
# ============================================================

def main():
    ap = argparse.ArgumentParser(description="Generate HTML stock analysis report")
    ap.add_argument("--data", required=True, help="Path to data_<code>.json")
    ap.add_argument("--narrative", required=True, help="Path to narrative JSON (Claude-generated)")
    ap.add_argument("--outdir", default="./output", help="Output directory")
    args = ap.parse_args()

    # Load data
    with open(args.data, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Load narrative
    with open(args.narrative, "r", encoding="utf-8") as f:
        narrative = json.load(f)

    code6 = data["meta"]["code6"]

    # Resolve chart paths
    data_dir = os.path.dirname(os.path.abspath(args.data))
    kline_path = os.path.join(data_dir, f"kline_{code6}.png")
    compare_path = os.path.join(data_dir, f"compare_{code6}.png")

    kline_b64 = _img_to_base64(kline_path)
    compare_b64 = _img_to_base64(compare_path)

    # Build HTML
    html = build_html(data, narrative, kline_b64, compare_b64)

    # Write output
    os.makedirs(args.outdir, exist_ok=True)
    out_path = os.path.join(args.outdir, f"report_{code6}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(json.dumps({
        "ok": True,
        "output": out_path,
        "code6": code6,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

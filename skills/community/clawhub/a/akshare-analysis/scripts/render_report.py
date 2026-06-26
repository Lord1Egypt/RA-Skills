#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Render HTML report from a report directory produced by analyze.py --report.

Usage:
    uv run render_report.py ~/stock-reports/20260329_030822_00700
"""

import argparse
import json
import os
import re
import sys


def _pct(v, decimals=1):
    return "N/A" if v is None else f"{v:.{decimals}f}%"


def _num(v, decimals=2):
    return "N/A" if v is None else f"{v:.{decimals}f}"


def render(report_dir: str) -> str:
    data_path = os.path.join(report_dir, "data.json")
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found", file=sys.stderr)
        sys.exit(1)

    with open(data_path, encoding="utf-8") as f:
        d = json.load(f)

    chart_data_path = os.path.join(report_dir, "chart_data.json")
    chart_data_json = "{}"
    if os.path.exists(chart_data_path):
        with open(chart_data_path, encoding="utf-8") as f:
            chart_data_json = f.read()

    sig = d["signal"]
    market_label = "港股" if d["market"] == "hk" else "A股"
    generated_at = d["generated_at"][:19].replace("T", " ")

    # Three horizon cards
    horizon_labels = {"short": "短期 (≤2周)", "medium": "中期 (2周~6月)", "long": "长期 (6月+)"}
    rec_labels = {"BUY": "买入 ▲", "HOLD": "持有 —", "SELL": "卖出 ▼"}
    rec_colors = {"BUY": "#26a641", "HOLD": "#d29922", "SELL": "#f85149"}
    horizons_parts = []
    for key in ["short", "medium", "long"]:
        hs = sig[key]
        rec = hs["recommendation"]
        color = rec_colors.get(rec, "#888")
        pts = "\n".join(f"<li>{p}</li>" for p in hs.get("points", [])) or "<li>数据不足</li>"
        horizons_parts.append(f"""<div class="card">
      <div class="horizon-header">
        <span class="horizon-label">{horizon_labels[key]}</span>
        <span class="badge" style="background:{color}22;color:{color}">{rec_labels.get(rec, rec)}</span>
        <span class="confidence">置信度 {hs['confidence']:.0f}%</span>
      </div>
      <ul class="points">{pts}</ul>
    </div>""")
    horizons_html = "\n".join(horizons_parts)

    # Financials
    fin = d.get("financials", {})
    fin_items = [
        ("P/E", _num(fin.get("pe"))),
        ("P/B", _num(fin.get("pb"))),
        ("ROE", _pct(fin.get("roe"))),
        ("净利率", _pct(fin.get("net_margin"))),
        ("利润增长", _pct(fin.get("profit_growth"))),
        ("营收增长", _pct(fin.get("revenue_growth"))),
        ("资产负债率", _pct(fin.get("debt_ratio"))),
        ("股息率", _pct(fin.get("dividend_yield"))),
    ]
    financials_html = "\n".join(
        f'<div class="fin-item"><span class="fin-label">{k}</span><span class="fin-value">{v}</span></div>'
        for k, v in fin_items if v != "N/A"
    )

    # Technicals
    tech = d.get("technicals", {})
    kdj = tech.get("kdj")
    pp = tech.get("pivot_points")
    tech_items = [
        ("MA5", _num(tech.get("ma5"))),
        ("MA20", _num(tech.get("ma20"))),
        ("MA60", _num(tech.get("ma60"))),
        ("EMA50", _num(tech.get("ema50"))),
        ("EMA200", _num(tech.get("ema200"))),
        ("RSI(14)", _num(tech.get("rsi_14"), 1)),
        ("ADX(14)", _num(tech.get("adx_14"), 1)),
        ("KDJ K/D/J", f"{kdj['k']:.0f}/{kdj['d']:.0f}/{kdj['j']:.0f}" if kdj else "N/A"),
        ("MFI(14)", _num(tech.get("mfi_14"), 1)),
        ("CCI(20)", _num(tech.get("cci_20"), 1)),
        ("ATR(14)", _num(tech.get("atr_14"))),
        ("BB带宽", _num(tech.get("bb_bandwidth"), 1)),
        ("波动率(20日)", _pct(tech.get("hist_volatility_20"))),
        ("OBV趋势", tech.get("obv_trend") or "N/A"),
        ("K线形态", tech.get("candlestick_pattern") or "无"),
        ("Pivot PP", _num(pp.get("pp")) if pp else "N/A"),
        ("近1月涨跌", _pct(tech.get("change_1m_pct"))),
        ("近3月涨跌", _pct(tech.get("change_3m_pct"))),
        ("52周高", _num(tech.get("high_52w"))),
        ("52周低", _num(tech.get("low_52w"))),
    ]
    technicals_html = "\n".join(
        f'<div class="fin-item"><span class="fin-label">{k}</span><span class="fin-value">{v}</span></div>'
        for k, v in tech_items if v != "N/A"
    )

    # AI analysis - check ai_analysis.md first, fallback to data.json
    ai_md_path = os.path.join(report_dir, "ai_analysis.md")
    ai_section = ""
    if os.path.exists(ai_md_path):
        # Parse ai_analysis.md with frontmatter
        try:
            with open(ai_md_path, encoding="utf-8") as f:
                content = f.read()
            # Split by H2 sections
            sections = re.split(r'^##\s+', content, flags=re.MULTILINE)
            cards = []
            for sec in sections[1:]:  # Skip first part (frontmatter)
                if not sec.strip():
                    continue
                parts = sec.strip().split('\n', 1)
                if not parts:
                    continue
                title = parts[0]
                body_text = parts[1].strip() if len(parts) > 1 else ""
                # Convert markdown links/bold to simple text
                body_text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', body_text)
                body_text = re.sub(r'\*\*([^*]+)\*\*', r'\1', body_text)
                cards.append(f"""<div class="ai-card">
              <div class="ai-card-title">{title}</div>
              <div class="ai-card-body">{body_text}</div>
            </div>""")
            if cards:
                ai_section = f'<div class="ai-section"><h2>AI 分析</h2><div class="ai-grid">' + "".join(cards) + '</div></div>'
        except Exception as e:
            print(f"Warning: Failed to parse ai_analysis.md: {e}", file=sys.stderr)
    else:
        ai_analysis = d.get("ai_analysis")
        ai_section = f'<div class="ai-box"><h3>AI 综合分析</h3>{ai_analysis}</div>' if ai_analysis else ""

    # Analyst forecasts
    forecasts = d.get("analyst_forecasts") or []
    if forecasts:
        rows = "\n".join(
            f"<tr><td>{f.get('broker','')}</td><td>{f.get('rating','')}</td>"
            f"<td>{f.get('target_price','N/A')}</td><td>{f.get('date','')}</td></tr>"
            for f in forecasts
        )
        analyst_section = f"""<div class="card" style="margin-bottom:16px">
      <h3>分析师预测</h3>
      <table class="analyst-table">
        <thead><tr><th>机构</th><th>评级</th><th>目标价</th><th>更新日期</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>"""
    else:
        analyst_section = ""

    html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{d['ticker']} {d['name']} 分析报告</title>
<script src="https://unpkg.com/lightweight-charts@4.2.0/dist/lightweight-charts.standalone.production.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #f5f7fa; color: #333; }}
  .container {{ max-width: 1400px; margin: 0 auto; padding: 16px; }}
  header {{ display: flex; align-items: center; gap: 12px; margin-bottom: 20px; border-bottom: 1px solid #e0e0e0; padding-bottom: 16px; flex-wrap: wrap; }}
  .ticker {{ font-size: 1.5rem; font-weight: 700; color: #1a1a2e; }}
  .meta {{ color: #666; font-size: 0.85rem; margin-top: 4px; }}
  .grid {{ display: grid; grid-template-columns: 1fr; gap: 12px; margin-bottom: 12px; }}
  @media (min-width: 768px) {{ .grid {{ grid-template-columns: 1fr 1fr 1fr; }} }}
  @media (min-width: 768px) {{ .grid-2 {{ grid-template-columns: 1fr 1fr; }} }}
  .card {{ background: #fff; border-radius: 10px; padding: 14px; border: 1px solid #e0e0e0; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }}
  .card h3 {{ font-size: 0.72rem; text-transform: uppercase; letter-spacing: 1px; color: #888; margin-bottom: 10px; }}
  .horizon-header {{ display: flex; align-items: center; gap: 8px; margin-bottom: 10px; flex-wrap: wrap; }}
  .horizon-label {{ font-size: 0.88rem; font-weight: 600; color: #1a1a2e; }}
  .badge {{ padding: 3px 10px; border-radius: 12px; font-weight: 600; font-size: 0.8rem; }}
  .confidence {{ color: #888; font-size: 0.78rem; }}
  .points {{ list-style: none; }}
  .points li {{ padding: 3px 0; font-size: 0.8rem; border-bottom: 1px solid #f0f0f0; color: #444; }}
  .points li::before {{ content: "▸ "; color: #aaa; }}
  .fin-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4px; }}
  @media (min-width: 480px) {{ .fin-grid {{ grid-template-columns: 1fr 1fr 1fr; }} }}
  .fin-item {{ display: flex; justify-content: space-between; font-size: 0.78rem; padding: 4px 0; border-bottom: 1px solid #f0f0f0; }}
  .fin-label {{ color: #666; }}
  .fin-value {{ font-weight: 600; color: #333; }}
  .ai-box {{ background: #fff; border-radius: 10px; padding: 14px; border: 1px solid #e0e0e0; margin-bottom: 12px; white-space: pre-wrap; font-size: 0.83rem; line-height: 1.6; color: #444; }}
  .ai-box h3 {{ font-size: 0.72rem; text-transform: uppercase; letter-spacing: 1px; color: #888; margin-bottom: 10px; }}
  .ai-section {{ margin-bottom: 16px; }}
  .ai-section h2 {{ font-size: 1rem; color: #1a1a2e; margin-bottom: 12px; }}
  .ai-grid {{ display: grid; grid-template-columns: 1fr; gap: 10px; }}
  @media (min-width: 768px) {{ .ai-grid {{ grid-template-columns: 1fr 1fr; }} }}
  .ai-card {{ background: #fff; border-radius: 10px; padding: 14px; border: 1px solid #e0e0e0; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }}
  .ai-card-title {{ font-size: 0.85rem; font-weight: 600; color: #1a1a2e; margin-bottom: 8px; border-bottom: 2px solid #58a6ff; padding-bottom: 6px; }}
  .ai-card-body {{ font-size: 0.8rem; line-height: 1.5; color: #555; white-space: pre-wrap; }}
  .analyst-table {{ width: 100%; border-collapse: collapse; font-size: 0.78rem; }}
  .analyst-table th {{ text-align: left; color: #666; font-weight: 500; padding: 6px; border-bottom: 1px solid #e0e0e0; background: #f8f9fa; }}
  .analyst-table td {{ padding: 6px; border-bottom: 1px solid #f0f0f0; color: #444; }}
  .chart-container {{ background: #fff; border-radius: 10px; border: 1px solid #e0e0e0; box-shadow: 0 1px 3px rgba(0,0,0,0.06); margin-bottom: 12px; overflow: hidden; }}
  .chart-title {{ padding: 10px 14px 0; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 1px; color: #888; }}
  .chart-legend {{ padding: 4px 14px 8px; font-size: 0.72rem; color: #888; display: flex; gap: 12px; flex-wrap: wrap; }}
  .legend-item {{ display: flex; align-items: center; gap: 4px; }}
  .legend-dot {{ width: 8px; height: 2px; border-radius: 1px; }}
  footer {{ text-align: center; color: #999; font-size: 0.7rem; margin-top: 24px; padding-top: 16px; border-top: 1px solid #e0e0e0; }}
</style>
</head>
<body>
<div class="container">
  <header>
    <div>
      <div class="ticker">{d['ticker']} <span style="font-size:1.1rem;color:#8b949e">{d['name']}</span></div>
      <div class="meta">{market_label} &nbsp;·&nbsp; 当前价: {d['current_price']} &nbsp;·&nbsp; 生成时间: {generated_at}</div>
    </div>
  </header>

  {ai_section}

  <div class="grid">
    {horizons_html}
  </div>

  <div class="chart-container">
    <div class="chart-title">K线图 · 最近180日</div>
    <div class="chart-legend">
      <span class="legend-item"><span class="legend-dot" style="background:#58a6ff"></span>MA20</span>
      <span class="legend-item"><span class="legend-dot" style="background:#f0883e"></span>EMA50</span>
      <span class="legend-item"><span class="legend-dot" style="background:#ff7b72;border-top:1px dashed #ff7b72;height:0"></span>EMA200</span>
      <span class="legend-item"><span class="legend-dot" style="background:#8b949e"></span>BB</span>
    </div>
    <div id="chart-main" style="height:320px"></div>
    <div id="chart-volume" style="height:80px"></div>
  </div>

  <div class="grid grid-2" style="margin-bottom:12px">
    <div class="chart-container" style="margin-bottom:0">
      <div class="chart-title">RSI (14)</div>
      <div id="chart-rsi" style="height:120px"></div>
    </div>
    <div class="chart-container" style="margin-bottom:0">
      <div class="chart-title">MACD (12,26,9)</div>
      <div id="chart-macd" style="height:120px"></div>
    </div>
  </div>

  <div class="chart-container">
    <div class="chart-title">KDJ (9,3,3)</div>
    <div class="chart-legend">
      <span class="legend-item"><span class="legend-dot" style="background:#58a6ff"></span>K</span>
      <span class="legend-item"><span class="legend-dot" style="background:#f0883e"></span>D</span>
      <span class="legend-item"><span class="legend-dot" style="background:#3fb950"></span>J</span>
    </div>
    <div id="chart-kdj" style="height:120px"></div>
  </div>

  <div class="grid grid-2">
    <div class="card">
      <h3>财务指标</h3>
      <div class="fin-grid">{financials_html}</div>
    </div>
    <div class="card">
      <h3>技术指标</h3>
      <div class="fin-grid">{technicals_html}</div>
    </div>
  </div>

  {analyst_section}

  <footer>⚠️ 本报告仅供参考，不构成投资建议。</footer>
</div>

<script>
const CD = {chart_data_json};

const OPTS = {{
  layout: {{ background: {{ color: '#ffffff' }}, textColor: '#333' }},
  grid: {{ vertLines: {{ color: '#f0f0f0' }}, horzLines: {{ color: '#f0f0f0' }} }},
  crosshair: {{ mode: 1 }},
  timeScale: {{ borderColor: '#e0e0e0', timeVisible: true }},
  rightPriceScale: {{ borderColor: '#e0e0e0' }},
}};

// ── Main chart ──
const mainChart = LightweightCharts.createChart(document.getElementById('chart-main'), {{
  ...OPTS, height: 320,
  handleScroll: {{ mouseWheel: true, pressedMouseMove: true }},
  handleScale: {{ mouseWheel: true, pinch: true }},
}});
const candleSeries = mainChart.addCandlestickSeries({{
  upColor: '#26a641', downColor: '#f85149',
  borderUpColor: '#26a641', borderDownColor: '#f85149',
  wickUpColor: '#26a641', wickDownColor: '#f85149',
}});
candleSeries.setData(CD.ohlcv);

const ma20s = mainChart.addLineSeries({{ color: '#58a6ff', lineWidth: 1, priceLineVisible: false }});
ma20s.setData(CD.ma20);
const ema50s = mainChart.addLineSeries({{ color: '#f0883e', lineWidth: 1, priceLineVisible: false }});
ema50s.setData(CD.ema50);
const ema200s = mainChart.addLineSeries({{ color: '#ff7b72', lineWidth: 1, lineStyle: 1, priceLineVisible: false }});
ema200s.setData(CD.ema200);
const bbUs = mainChart.addLineSeries({{ color: '#8b949e', lineWidth: 1, lineStyle: 2, priceLineVisible: false }});
bbUs.setData(CD.bb_upper);
const bbLs = mainChart.addLineSeries({{ color: '#8b949e', lineWidth: 1, lineStyle: 2, priceLineVisible: false }});
bbLs.setData(CD.bb_lower);

// ── Volume chart ──
const volChart = LightweightCharts.createChart(document.getElementById('chart-volume'), {{
  ...OPTS, height: 80,
}});
const volSeries = volChart.addHistogramSeries({{
  priceFormat: {{ type: 'volume' }},
  priceScaleId: '',
}});
volSeries.priceScale().applyOptions({{ scaleMargins: {{ top: 0.1, bottom: 0 }} }});
volSeries.setData(CD.ohlcv.map(d => ({{
  time: d.time,
  value: d.volume,
  color: d.close >= d.open ? '#26a64166' : '#f8514966',
}})));

// ── RSI chart ──
const rsiChart = LightweightCharts.createChart(document.getElementById('chart-rsi'), {{
  ...OPTS, height: 120,
}});
const rsiSeries = rsiChart.addLineSeries({{ color: '#d2a8ff', lineWidth: 1, priceLineVisible: false }});
rsiSeries.setData(CD.rsi);
[70, 30].forEach(v => {{
  const s = rsiChart.addLineSeries({{ color: v === 70 ? '#f85149' : '#26a641', lineWidth: 1, lineStyle: 2, priceLineVisible: false }});
  s.setData(CD.rsi.map(d => ({{ time: d.time, value: v }})));
}});

// ── MACD chart ──
const macdChart = LightweightCharts.createChart(document.getElementById('chart-macd'), {{
  ...OPTS, height: 120,
}});
const macdHistSeries = macdChart.addHistogramSeries({{ priceLineVisible: false }});
macdHistSeries.setData(CD.macd_hist.map(d => ({{
  time: d.time, value: d.value,
  color: d.value >= 0 ? '#26a64188' : '#f8514988',
}})));
const macdLine = macdChart.addLineSeries({{ color: '#58a6ff', lineWidth: 1, priceLineVisible: false }});
macdLine.setData(CD.macd);
const sigLine = macdChart.addLineSeries({{ color: '#f0883e', lineWidth: 1, priceLineVisible: false }});
sigLine.setData(CD.macd_signal);

// ── KDJ chart ──
const kdjChart = LightweightCharts.createChart(document.getElementById('chart-kdj'), {{
  ...OPTS, height: 120,
}});
const kLine = kdjChart.addLineSeries({{ color: '#58a6ff', lineWidth: 1, priceLineVisible: false }});
kLine.setData(CD.kdj_k);
const dLine = kdjChart.addLineSeries({{ color: '#f0883e', lineWidth: 1, priceLineVisible: false }});
dLine.setData(CD.kdj_d);
const jLine = kdjChart.addLineSeries({{ color: '#3fb950', lineWidth: 1, priceLineVisible: false }});
jLine.setData(CD.kdj_j);
[80, 20].forEach(v => {{
  const s = kdjChart.addLineSeries({{ color: v === 80 ? '#f85149' : '#26a641', lineWidth: 1, lineStyle: 2, priceLineVisible: false }});
  s.setData(CD.kdj_k.map(d => ({{ time: d.time, value: v }})));
}});

// Sync time scales
const charts = [mainChart, volChart, rsiChart, macdChart, kdjChart];
charts.forEach(c => {{
  c.timeScale().subscribeVisibleLogicalRangeChange(range => {{
    if (range) charts.forEach(o => {{ if (o !== c) o.timeScale().setVisibleLogicalRange(range); }});
  }});
}});
mainChart.timeScale().fitContent();
</script>
</body>
</html>"""

    out_path = os.path.join(report_dir, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Report rendered: {out_path}")
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Render HTML report from report directory")
    parser.add_argument("report_dir", help="Path to report directory (contains data.json)")
    args = parser.parse_args()
    render(os.path.expanduser(args.report_dir))


if __name__ == "__main__":
    main()

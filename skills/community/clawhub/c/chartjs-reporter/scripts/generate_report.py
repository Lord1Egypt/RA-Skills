#!/usr/bin/env python3
"""
chartjs-reporter: generate_report.py
将结构化数据转换为自包含的 Chart.js HTML 可视化报告。

用法：
  python generate_report.py --title "标题" --data '{"kpis":[...],"charts":[...]}' --output report.html
  或直接 import build_report 函数使用。
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


# ── 默认调色板 ──────────────────────────────────────────────────────────────
PALETTE = [
    "#38bdf8", "#818cf8", "#34d399", "#fbbf24", "#fb923c",
    "#f472b6", "#a78bfa", "#4ade80", "#60a5fa", "#facc15",
]

KPI_COLORS = {
    "blue":   ("var(--accent)",  "#1e293b"),
    "green":  ("var(--green)",   "#1e293b"),
    "yellow": ("var(--yellow)",  "#1e293b"),
    "purple": ("var(--accent2)", "#1e293b"),
    "red":    ("var(--red)",     "#1e293b"),
}


# ── KPI 卡片 HTML ────────────────────────────────────────────────────────────
def _render_kpis(kpis: list) -> str:
    if not kpis:
        return ""
    cards = []
    for kpi in kpis:
        color_var, _ = KPI_COLORS.get(kpi.get("color", "blue"), KPI_COLORS["blue"])
        cards.append(f"""
      <div class="kpi">
        <div class="kpi-label">{kpi.get('label', '')}</div>
        <div class="kpi-value" style="color:{color_var}">{kpi.get('value', '')}</div>
        <div class="kpi-sub">{kpi.get('sub', '')}</div>
      </div>""")
    return f'<div class="kpi-row">{"".join(cards)}\n    </div>'


# ── 单张图表 JS 配置 ──────────────────────────────────────────────────────────
def _chart_js_config(chart: dict, idx: int) -> str:
    ctype = chart.get("type", "bar")
    labels = json.dumps(chart.get("labels", []), ensure_ascii=False)
    title = chart.get("title", f"图表{idx+1}")
    raw_datasets = chart.get("datasets", [])

    # 处理水平柱状图别名
    index_axis = ""
    if ctype == "horizontalBar":
        ctype = "bar"
        index_axis = 'indexAxis: "y",'

    # 为每个 dataset 自动注入颜色
    datasets_js_parts = []
    for i, ds in enumerate(raw_datasets):
        color = PALETTE[i % len(PALETTE)]
        label = json.dumps(ds.get("label", ""), ensure_ascii=False)
        data = json.dumps(ds.get("data", []))

        if ctype in ("doughnut", "pie"):
            # 多色背景
            bg_colors = json.dumps([PALETTE[j % len(PALETTE)] for j in range(len(ds.get("data", [])))])
            ds_str = f"""{{
          label: {label},
          data: {data},
          backgroundColor: {bg_colors},
          borderWidth: 2,
          borderColor: "#1e293b"
        }}"""
        elif ctype == "line":
            fill = str(ds.get("fill", True)).lower()
            ds_str = f"""{{
          label: {label},
          data: {data},
          borderColor: "{color}",
          backgroundColor: "{color}22",
          tension: 0.4,
          fill: {fill},
          pointRadius: 4,
          pointBackgroundColor: "{color}"
        }}"""
        else:  # bar / grouped bar
            ds_str = f"""{{
          label: {label},
          data: {data},
          backgroundColor: "{color}",
          borderRadius: 6
        }}"""
        datasets_js_parts.append(ds_str)

    datasets_js = ",\n        ".join(datasets_js_parts)

    # y轴 tick 格式（数值大于 999 时加 k）
    y_tick = ""
    if ctype not in ("doughnut", "pie"):
        y_tick = "callback: v => v >= 1000 ? (v/1000).toFixed(0)+'k' : v,"

    scales_block = ""
    if ctype not in ("doughnut", "pie"):
        scales_block = f"""
      scales: {{
        x: {{ grid: {{ color: "#1e293b" }}, ticks: {{ color: "#94a3b8" }} }},
        y: {{ grid: {{ color: "#334155" }}, ticks: {{ color: "#94a3b8", {y_tick} }} }}
      }},"""

    legend_display = "false" if len(raw_datasets) <= 1 and ctype not in ("doughnut", "pie") else "true"
    legend_pos = '"right"' if ctype in ("doughnut", "pie") else '"top"'

    return f"""new Chart(document.getElementById('chart{idx}'), {{
    type: '{ctype}',
    data: {{
      labels: {labels},
      datasets: [{datasets_js}]
    }},
    options: {{
      responsive: true,
      maintainAspectRatio: false,
      {index_axis}
      {scales_block}
      plugins: {{
        legend: {{ display: {legend_display}, position: {legend_pos}, labels: {{ color: "#94a3b8", font: {{ size: 12 }} }} }},
        title: {{ display: false }}
      }}
    }}
  }});"""


# ── 图表区 HTML ──────────────────────────────────────────────────────────────
def _render_charts(charts: list) -> str:
    if not charts:
        return ""

    n = len(charts)
    if n == 1:
        cols = "1fr"
    elif n % 3 == 0 and n >= 3:
        cols = "1fr 1fr 1fr"
    else:
        cols = "1fr 1fr"

    cards_html = []
    for i, chart in enumerate(charts):
        title = chart.get("title", f"图表{i+1}")
        cards_html.append(f"""
      <div class="chart-card">
        <h3>{title}</h3>
        <div class="chart-wrap"><canvas id="chart{i}"></canvas></div>
      </div>""")

    return f"""<div class="charts-grid" style="grid-template-columns:{cols}">
      {"".join(cards_html)}
    </div>"""


# ── 表格区 HTML ──────────────────────────────────────────────────────────────
def _render_tables(tables: list) -> str:
    if not tables:
        return ""

    tables_html = []
    for table in tables:
        title = table.get("title", "")
        columns = table.get("columns", [])
        data = table.get("data", [])
        highlight_col = table.get("highlight", "")

        # 表头
        header_cells = "".join([f"<th>{col}</th>" for col in columns])

        # 表体
        rows_html = []
        for row in data:
            cells_html = []
            for i, col in enumerate(columns):
                value = row.get(col, "")
                cell_html = f"<td>{value}</td>"
                # 高亮列添加样式
                if highlight_col and col == highlight_col:
                    # 根据数值添加颜色
                    cell_html = f'<td class="highlight-{_get_rate_level(value)}">{value}</td>'
                cells_html.append(cell_html)
            rows_html.append(f"<tr>{''.join(cells_html)}</tr>")

        tables_html.append(f"""
      <div class="table-card">
        <h3>{title}</h3>
        <table>
          <thead>
            <tr>{header_cells}</tr>
          </thead>
          <tbody>
            {"".join(rows_html)}
          </tbody>
        </table>
      </div>""")

    return f"""<div class="tables-section">
      {"".join(tables_html)}
    </div>"""


# ── 退货率级别判断 ─────────────────────────────────────────────────────────
def _get_rate_level(value: str) -> str:
    """根据退货率返回级别"""
    try:
        # 移除百分号并转为浮点数
        num = float(value.replace('%', '').replace('万', '').strip())
        if '万' in value:
            # 处理金额情况
            return 'normal'
        if num >= 90:
            return 'danger'
        elif num >= 75:
            return 'warning'
        elif num >= 65:
            return 'medium'
        else:
            return 'good'
    except:
        return 'normal'


# ── 主构建函数 ───────────────────────────────────────────────────────────────
def build_report(
    title: str,
    subtitle: str = "",
    kpis: list = None,
    charts: list = None,
    tables: list = None,
    footer: str = "",
) -> str:
    kpis = kpis or []
    charts = charts or []
    tables = tables or []
    footer = footer or f"由 chartjs-reporter 技能生成 · {datetime.now().strftime('%Y-%m-%d %H:%M')}"

    kpi_html = _render_kpis(kpis)
    chart_html = _render_charts(charts)
    table_html = _render_tables(tables)
    chart_scripts = "\n  ".join(_chart_js_config(c, i) for i, c in enumerate(charts))

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>{title}</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
  <style>
    :root {{
      --bg:#0f172a; --card:#1e293b; --border:#334155;
      --accent:#38bdf8; --accent2:#818cf8;
      --green:#34d399; --yellow:#fbbf24; --red:#f87171;
      --text:#e2e8f0; --muted:#94a3b8;
    }}
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;padding:28px}}
    h1{{font-size:1.75rem;font-weight:700;color:var(--accent);margin-bottom:4px}}
    .subtitle{{color:var(--muted);font-size:.88rem;margin-bottom:28px}}
    /* KPI */
    .kpi-row{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px;margin-bottom:28px}}
    .kpi{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px 22px}}
    .kpi-label{{color:var(--muted);font-size:.75rem;letter-spacing:.05em;text-transform:uppercase;margin-bottom:6px}}
    .kpi-value{{font-size:1.85rem;font-weight:700;margin-bottom:4px}}
    .kpi-sub{{color:var(--muted);font-size:.8rem}}
    /* 图表 */
    .charts-grid{{display:grid;gap:20px;margin-bottom:24px}}
    .chart-card{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px 22px}}
    .chart-card h3{{font-size:.85rem;color:var(--muted);font-weight:600;margin-bottom:14px;text-transform:uppercase;letter-spacing:.04em}}
    .chart-wrap{{position:relative;height:240px}}
    /* 表格 */
    .tables-section{{display:grid;gap:20px}}
    .table-card{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px 22px}}
    .table-card h3{{font-size:.85rem;color:var(--muted);font-weight:600;margin-bottom:14px;text-transform:uppercase;letter-spacing:.04em}}
    table{{width:100%;border-collapse:collapse;font-size:.85rem}}
    thead{{border-bottom:2px solid var(--border)}}
    th{{text-align:left;padding:10px 12px;color:var(--accent);font-weight:600;white-space:nowrap}}
    tbody tr{{border-bottom:1px solid var(--border);transition:background .15s}}
    tbody tr:hover{{background:rgba(56,189,248,.08)}}
    td{{padding:9px 12px;color:var(--text);vertical-align:middle}}
    /* 高亮样式 */
    .highlight-danger{{color:var(--red);font-weight:600;background:rgba(248,113,113,.12);border-radius:4px;padding:2px 6px}}
    .highlight-warning{{color:var(--yellow);font-weight:600;background:rgba(251,191,36,.12);border-radius:4px;padding:2px 6px}}
    .highlight-medium{{color:var(--text);background:rgba(148,163,184,.12);border-radius:4px;padding:2px 6px}}
    .highlight-good{{color:var(--green);font-weight:600;background:rgba(52,211,153,.12);border-radius:4px;padding:2px 6px}}
    .highlight-normal{{color:var(--text)}}
    footer{{text-align:center;color:var(--muted);font-size:.75rem;margin-top:8px}}
  </style>
</head>
<body>
  <h1>📊 {title}</h1>
  <p class="subtitle">{subtitle}</p>

  {kpi_html}
  {chart_html}
  {table_html}

  <footer>{footer}</footer>
  <script>
  {chart_scripts}
  </script>
</body>
</html>"""


# ── CLI 入口 ─────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="生成 Chart.js HTML 可视化报告")
    parser.add_argument("--title",    required=True, help="报告标题")
    parser.add_argument("--subtitle", default="",    help="副标题")
    parser.add_argument("--data",     required=True, help='JSON 字符串，含 kpis 和 charts 字段')
    parser.add_argument("--output",   default="report.html", help="输出 HTML 文件路径")
    parser.add_argument("--footer",   default="",    help="页脚文字")
    args = parser.parse_args()

    try:
        data = json.loads(args.data)
    except json.JSONDecodeError as e:
        print(f"❌ --data 不是合法 JSON：{e}", file=sys.stderr)
        sys.exit(1)

    html = build_report(
        title=args.title,
        subtitle=args.subtitle,
        kpis=data.get("kpis", []),
        charts=data.get("charts", []),
        footer=args.footer,
    )

    out = Path(args.output)
    out.write_text(html, encoding="utf-8")
    print(f"✅ 报告已生成：{out.resolve()}")


if __name__ == "__main__":
    main()

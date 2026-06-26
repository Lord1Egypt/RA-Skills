"""
HTML生成器 - 根据数据分析结果生成可视化看板HTML
支持5种颜色主题: THEME_BLUE / THEME_RED / THEME_GREEN / THEME_PURPLE / THEME_ORANGE
"""

import re
from datetime import datetime

# ─────────────────────────────────────────────────────────────────
# 主题CSS变量映射
# ─────────────────────────────────────────────────────────────────
THEME_CSS = {
    "THEME_BLUE": """
    --bg-primary: #0a0e1a;
    --bg-secondary: #0f1829;
    --bg-card: #141e38;
    --border: #1e2d4a;
    --border-light: #1a2640;
    --accent: #4a9eff;
    --accent-dim: rgba(74,158,255,0.08);
    --accent-border: rgba(74,158,255,0.3);
    --red: #ff4757;
    --red-dim: rgba(255,71,87,0.08);
    --red-border: rgba(255,71,87,0.3);
    --green: #2ed573;
    --green-dim: rgba(46,213,115,0.08);
    --green-border: rgba(46,213,115,0.3);
    --yellow: #ffd700;
    --orange: #ffa502;
    --orange-dim: rgba(255,165,2,0.08);
    --orange-border: rgba(255,165,2,0.3);
    --cyan: #00d2d3;
    --text-primary: #ffffff;
    --text-secondary: #e0e6f0;
    --text-muted: #6b7fa3;
    --text-body: #c8d4e8;
    """,
    "THEME_RED": """
    --bg-primary: #1a0a0a;
    --bg-secondary: #1a0f0f;
    --bg-card: #251414;
    --border: #3a1a1a;
    --border-light: #2a1515;
    --accent: #ff4757;
    --accent-dim: rgba(255,71,87,0.08);
    --accent-border: rgba(255,71,87,0.3);
    --red: #ff6b7a;
    --red-dim: rgba(255,71,87,0.1);
    --red-border: rgba(255,71,87,0.4);
    --green: #5dde8f;
    --green-dim: rgba(46,213,115,0.08);
    --green-border: rgba(46,213,115,0.3);
    --yellow: #ffd700;
    --orange: #ff7c4d;
    --orange-dim: rgba(255,124,77,0.08);
    --orange-border: rgba(255,124,77,0.3);
    --cyan: #ff4757;
    --text-primary: #fff5f5;
    --text-secondary: #f0d0d0;
    --text-muted: #a08080;
    --text-body: #ddc8c8;
    """,
    "THEME_GREEN": """
    --bg-primary: #0a1a0e;
    --bg-secondary: #0f1a12;
    --bg-card: #142018;
    --border: #1a2d1e;
    --border-light: #152518;
    --accent: #2ed573;
    --accent-dim: rgba(46,213,115,0.08);
    --accent-border: rgba(46,213,115,0.3);
    --red: #ff6b6b;
    --red-dim: rgba(255,71,87,0.08);
    --red-border: rgba(255,71,87,0.3);
    --green: #5dff9e;
    --green-dim: rgba(46,213,115,0.1);
    --green-border: rgba(46,213,115,0.4);
    --yellow: #ffd700;
    --orange: #ffa502;
    --orange-dim: rgba(255,165,2,0.08);
    --orange-border: rgba(255,165,2,0.3);
    --cyan: #00d2d3;
    --text-primary: #f0fff4;
    --text-secondary: #d0f0d8;
    --text-muted: #70a080;
    --text-body: #c0dcc0;
    """,
    "THEME_PURPLE": """
    --bg-primary: #0f0a1a;
    --bg-secondary: #150f1a;
    --bg-card: #1a1425;
    --border: #251a35;
    --border-light: #1e1428;
    --accent: #a55eea;
    --accent-dim: rgba(165,94,234,0.08);
    --accent-border: rgba(165,94,234,0.3);
    --red: #ff6b9d;
    --red-dim: rgba(255,71,87,0.08);
    --red-border: rgba(255,71,87,0.3);
    --green: #7bed9f;
    --green-dim: rgba(46,213,115,0.08);
    --green-border: rgba(46,213,115,0.3);
    --yellow: #ffd700;
    --orange: #ffa502;
    --orange-dim: rgba(255,165,2,0.08);
    --orange-border: rgba(255,165,2,0.3);
    --cyan: #a55eea;
    --text-primary: #f8f0ff;
    --text-secondary: #e0d0f0;
    --text-muted: #9080a8;
    --text-body: #d8c8e8;
    """,
    "THEME_ORANGE": """
    --bg-primary: #1a120a;
    --bg-secondary: #1f150f;
    --bg-card: #28201a;
    --border: #352a1a;
    --border-light: #2a2015;
    --accent: #ffa502;
    --accent-dim: rgba(255,165,2,0.08);
    --accent-border: rgba(255,165,2,0.3);
    --red: #ff6b6b;
    --red-dim: rgba(255,71,87,0.08);
    --red-border: rgba(255,71,87,0.3);
    --green: #5dde8f;
    --green-dim: rgba(46,213,115,0.08);
    --green-border: rgba(46,213,115,0.3);
    --yellow: #ffd700;
    --orange: #ff9f43;
    --orange-dim: rgba(255,159,67,0.1);
    --orange-border: rgba(255,159,67,0.4);
    --cyan: #ffa502;
    --text-primary: #fff8f0;
    --text-secondary: #f0e0c8;
    --text-muted: #a09070;
    --text-body: #ddd0b8;
    """,
}

# ─────────────────────────────────────────────────────────────────
# 样式模板（CSS变量通过 :root 注入，无 body class）
# ─────────────────────────────────────────────────────────────────
STYLE = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  background: var(--bg-primary);
  color: var(--text-secondary);
  font-family: 'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', sans-serif;
  font-size: 13px;
  line-height: 1.6;
  padding: 20px;
}
.card {
  max-width: 1100px;
  margin: 0 auto;
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 40px rgba(0,0,0,0.6);
}
.header {
  background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-card) 100%);
  border-bottom: 1px solid var(--border);
  padding: 20px 28px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}
.header-left .brand {
  color: var(--accent);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-bottom: 4px;
}
.header-left .title {
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: 1px;
}
.header-right {
  text-align: right;
  font-size: 11px;
  color: var(--text-muted);
  line-height: 1.8;
}
.header-right span { color: var(--accent); }
.meta-bar {
  background: var(--bg-secondary);
  padding: 12px 28px;
  display: flex;
  gap: 32px;
  font-size: 12px;
  border-bottom: 1px solid var(--border-light);
  color: var(--text-muted);
  flex-wrap: wrap;
}
.meta-bar .item strong { color: var(--yellow); }
.section-header {
  background: linear-gradient(90deg, var(--bg-secondary) 0%, transparent 100%);
  padding: 12px 28px;
  border-left: 4px solid var(--accent);
  font-size: 14px;
  font-weight: 700;
  color: var(--accent);
  letter-spacing: 1px;
  margin-top: 24px;
  margin-bottom: 12px;
}
.section-header.red { border-left-color: var(--red); color: var(--red); }
.section-header.green { border-left-color: var(--green); color: var(--green); }
.section-header.orange { border-left-color: var(--orange); color: var(--orange); }
.section-header.cyan { border-left-color: var(--cyan); color: var(--cyan); }
.section-header.yellow { border-left-color: var(--yellow); color: var(--yellow); }
.table-wrap { padding: 0 20px 8px; }
table { width: 100%; border-collapse: collapse; font-size: 12px; }
th {
  background: var(--bg-card);
  color: var(--accent);
  padding: 8px 12px;
  text-align: left;
  font-weight: 600;
  border-bottom: 1px solid var(--border);
}
td { padding: 7px 12px; border-bottom: 1px solid var(--border-light); color: var(--text-body); }
tr:hover td { background: var(--bg-secondary); }
td .red { color: var(--red); font-weight: 600; }
td .green { color: var(--green); font-weight: 600; }
td .orange { color: var(--orange); font-weight: 600; }
td .yellow { color: var(--yellow); font-weight: 600; }
td .cyan { color: var(--cyan); font-weight: 600; }
td .blue { color: var(--accent); font-weight: 600; }
td .gray { color: var(--text-muted); }
.fin-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 10px;
  padding: 0 20px 8px;
}
.fin-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: 8px;
  padding: 12px 14px;
  position: relative;
  overflow: hidden;
}
.fin-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: var(--accent);
}
.fin-label { font-size: 10px; color: var(--text-muted); margin-bottom: 4px; }
.fin-val { font-size: 18px; font-weight: 700; color: var(--text-primary); }
.fin-sub { font-size: 10px; color: var(--green); margin-top: 2px; }
.fin-sub.orange { color: var(--orange); }
.fin-sub.red { color: var(--red); }
.timeline { padding: 0 20px 8px; }
.timeline-item {
  display: flex;
  align-items: flex-start;
  padding: 8px 0;
  border-bottom: 1px solid var(--border-light);
  gap: 12px;
}
.timeline-item:last-child { border-bottom: none; }
.tl-time { min-width: 80px; font-size: 11px; color: var(--text-muted); font-weight: 600; padding-top: 2px; }
.tl-tag {
  padding: 1px 8px;
  border-radius: 10px;
  font-size: 10px;
  font-weight: 700;
  white-space: nowrap;
  margin-right: 8px;
  display: inline-block;
}
.tl-tag.red { background: var(--red-dim); color: var(--red); border: 1px solid var(--red-border); }
.tl-tag.orange { background: var(--orange-dim); color: var(--orange); border: 1px solid var(--orange-border); }
.tl-tag.green { background: var(--green-dim); color: var(--green); border: 1px solid var(--green-border); }
.tl-tag.blue { background: var(--accent-dim); color: var(--accent); border: 1px solid var(--accent-border); }
.tl-tag.yellow { background: rgba(255,215,0,0.1); color: var(--yellow); border: 1px solid rgba(255,215,0,0.3); }
.tl-event { font-size: 12px; color: var(--text-body); flex: 1; }
.compare-header, .compare-row {
  display: grid;
  padding: 0 20px;
}
.compare-header div {
  padding: 8px 12px;
  font-size: 11px;
  font-weight: 700;
}
.compare-row {
  border-bottom: 1px solid var(--border-light);
}
.compare-row:last-child { border-bottom: none; }
.compare-row:hover { background: var(--bg-secondary); }
.compare-row div { padding: 7px 12px; font-size: 12px; }
.compare-row .label { color: var(--text-muted); font-weight: 500; }
.compare-row .val-accent { color: var(--green); }
.compare-row .val-warn { color: var(--red); }
.compare-row .val-neutral { color: var(--text-body); }
.swot-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  padding: 0 20px 8px;
}
.swot-box {
  border-radius: 8px;
  padding: 14px;
}
.swot-box.s { background: var(--accent-dim); border: 1px solid var(--accent-border); }
.swot-box.w { background: var(--red-dim); border: 1px solid var(--red-border); }
.swot-box.o { background: var(--green-dim); border: 1px solid var(--green-border); }
.swot-box.t { background: var(--orange-dim); border: 1px solid var(--orange-border); }
.swot-box h4 { font-size: 13px; font-weight: 700; margin-bottom: 8px; }
.swot-box.s h4 { color: var(--accent); }
.swot-box.w h4 { color: var(--red); }
.swot-box.o h4 { color: var(--green); }
.swot-box.t h4 { color: var(--orange); }
.swot-box ul { list-style: none; padding: 0; }
.swot-box li { font-size: 11px; color: var(--text-body); padding: 3px 0; }
.swot-box li::before { content: '• '; }
.four-dim {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  padding: 0 20px 8px;
}
.dim-box {
  border-radius: 8px;
  padding: 14px;
  border: 1px solid;
}
.dim-box.blue { background: var(--accent-dim); border-color: var(--accent-border); }
.dim-box.blue .dim-title { color: var(--accent); }
.dim-box.red { background: var(--red-dim); border-color: var(--red-border); }
.dim-box.red .dim-title { color: var(--red); }
.dim-box.green { background: var(--green-dim); border-color: var(--green-border); }
.dim-box.green .dim-title { color: var(--green); }
.dim-box.yellow { background: var(--orange-dim); border-color: var(--orange-border); }
.dim-box.yellow .dim-title { color: var(--orange); }
.dim-title {
  font-size: 12px;
  font-weight: 700;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.dim-box ul { list-style: none; padding: 0; }
.dim-box li { font-size: 11px; color: var(--text-body); padding: 3px 0; }
.dim-box li::before { content: '▸ '; font-size: 10px; }
.source-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 10px;
  padding: 0 20px 8px;
}
.source-item {
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: 8px;
  padding: 10px 14px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.source-item .emoji { font-size: 18px; }
.source-item .label { font-size: 11px; color: var(--text-muted); }
.source-item .count { font-size: 18px; font-weight: 700; color: var(--accent); margin-left: auto; }
.footer {
  background: var(--bg-secondary);
  border-top: 1px solid var(--border-light);
  padding: 14px 28px;
  font-size: 10px;
  color: var(--text-muted);
  text-align: center;
  margin-top: 24px;
}
.footer .tag {
  display: inline-block;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  padding: 2px 10px;
  border-radius: 10px;
  margin: 0 4px;
  color: var(--accent);
}
@media (max-width: 768px) {
  .swot-grid, .four-dim, .fin-grid { grid-template-columns: 1fr; }
  .compare-header, .compare-row { grid-template-columns: 100px 1fr 1fr; }
  .header { flex-direction: column; gap: 10px; }
  .header-right { text-align: left; }
}
"""

# ─────────────────────────────────────────────────────────────────
# 主生成函数
# ─────────────────────────────────────────────────────────────────
def generate_html(data: dict, theme: str = "THEME_BLUE", title: str = "数据可视化看板") -> str:
    """
    data格式:
    {
        "title": str,
        "subtitle": str,
        "meta": {"key": "val"},
        "sections": [
            {"type": "fin_grid", "data": {"cards": [{"label","val","sub","sub_color"}]}},
            {"type": "timeline", "data": {"events": [{"time","tags":[],"tag_colors":[],"event"}]}},
            {"type": "compare", "data": {"headers":[], "rows":[{"label","values":[],"class":""}]}},
            {"type": "swot", "data": {"S":[],"W":[],"O":[],"T":[]}},
            {"type": "four_dim", "data": {"attack":[],"defend":[],"opportunity":[],"threat":[]}},
            {"type": "table", "data": {"headers":[], "rows":[[]]}},
            {"type": "source_stats", "data": [{"emoji","label","count"}]},
            {"type": "interview", "data": {"rows":[{"scene","topic","expected","exp_class"}]}},
            {"type": "section_header", "data": {"text":"","color":""}},
        ]
    }
    """
    css_vars = THEME_CSS.get(theme, THEME_CSS["THEME_BLUE"])
    sections_html = build_sections(data.get("sections", []))
    footer_html = build_footer()
    header_html = build_header(data)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
:root {{
  {css_vars}
}}
{STYLE}
</style>
</head>
<body>
<div class="card">
  {header_html}
  {sections_html}
  {footer_html}
</div>
</body>
</html>"""


def build_header(data: dict) -> str:
    title = data.get("title", "数据可视化看板")
    meta = data.get("meta", {})
    meta_html = "".join(f'<div>📌 <strong>{k}</strong> <span>{v}</span></div>' for k, v in meta.items())
    return f"""  <div class="header">
    <div class="header-left">
      <div class="brand">MINHUA HOLDINGS · AI VISUALIZER</div>
      <div class="title">{title}</div>
    </div>
    <div class="header-right">
      {meta_html}
    </div>
  </div>"""


def build_sections(sections: list) -> str:
    result = ""
    for sec in sections:
        s_type = sec.get("type", "")
        s_data = sec.get("data", {})
        if s_type == "fin_grid":
            result += build_fin_grid(s_data)
        elif s_type == "timeline":
            result += build_timeline(s_data)
        elif s_type == "compare":
            result += build_compare(s_data)
        elif s_type == "swot":
            result += build_swot(s_data)
        elif s_type == "four_dim":
            result += build_four_dim(s_data)
        elif s_type == "table":
            result += build_table(s_data)
        elif s_type == "source_stats":
            result += build_source_stats(s_data)
        elif s_type == "interview":
            result += build_interview(s_data)
        elif s_type == "section_header":
            result += f'<div class="section-header {s_data.get("color","")}">{s_data.get("text","")}</div>\n'
    return result


def build_fin_grid(data: dict) -> str:
    cards = data.get("cards", [])
    cards_html = ""
    for c in cards:
        sub_color = c.get("sub_color", "green")
        cards_html += f"""    <div class="fin-card">
      <div class="fin-label">{c.get('label','')}</div>
      <div class="fin-val">{c.get('val','')}</div>
      <div class="fin-sub {sub_color}">{c.get('sub','')}</div>
    </div>"""
    return '<div class="section-header">📊 数据概览</div>\n<div class="fin-grid">\n' + cards_html + '\n</div>\n'


def build_timeline(data: dict) -> str:
    events = data.get("events", [])
    items = ""
    for e in events:
        tags_html = "".join(
            f'<span class="tl-tag {tc}">{tt}</span>'
            for tc, tt in zip(e.get("tag_colors", []), e.get("tags", []))
        )
        items += f"""    <div class="timeline-item">
      <div class="tl-time">{e.get('time','')}</div>
      <div>{tags_html}</div>
      <div class="tl-event">{e.get('event','')}</div>
    </div>"""
    return '<div class="section-header red">📰 重大事件时间轴</div>\n<div class="timeline">\n' + items + '\n</div>\n'


def build_compare(data: dict) -> str:
    headers = data.get("headers", [])
    rows = data.get("rows", [])
    n_cols = len(headers) if headers else 2
    col_widths = f"grid-template-columns: 160px " + " 1fr " * (n_cols - 1)
    hdr_html = "".join(f'<div>{h}</div>' for h in headers)
    rows_html = ""
    for row in rows:
        vals = row.get("values", [])
        label = row.get("label", "")
        cls = row.get("class", "val-neutral")
        vals_html = "".join(f'<div class="{cls}">{v}</div>' for v in vals)
        rows_html += f'<div class="compare-row" style="{col_widths}"><div class="label">{label}</div>{vals_html}</div>\n'
    hdr_style = f'{col_widths}; padding: 0 20px;'
    return f'<div class="section-header">⚔️ 对比分析</div>\n<div class="compare-header" style="{hdr_style}">{hdr_html}</div>\n{rows_html}'


def build_swot(data: dict) -> str:
    boxes = [
        ("s", "✅ S 优势", data.get("S", [])),
        ("w", "⚠️ W 劣势", data.get("W", [])),
        ("o", "🌟 O 机会", data.get("O", [])),
        ("t", "🚨 T 威胁", data.get("T", [])),
    ]
    boxes_html = ""
    for cls, title, items in boxes:
        items_html = "".join(f"<li>{i}</li>" for i in items)
        boxes_html += f'<div class="swot-box {cls}"><h4>{title}</h4><ul>{items_html}</ul></div>'
    return '<div class="section-header">💼 SWOT 分析</div>\n<div class="swot-grid">\n' + boxes_html + '\n</div>\n'


def build_four_dim(data: dict) -> str:
    dims = [
        ("blue", "🔵 进攻动作", data.get("attack", [])),
        ("red", "🔴 防守压力", data.get("defend", [])),
        ("green", "🟢 战略机会", data.get("opportunity", [])),
        ("yellow", "🟡 潜在威胁", data.get("threat", [])),
    ]
    dims_html = ""
    for cls, title, items in dims:
        items_html = "".join(f"<li>{i}</li>" for i in items)
        dims_html += f'<div class="dim-box {cls}"><div class="dim-title">{title}</div><ul>{items_html}</ul></div>'
    return '<div class="section-header">🚀 战略四维分析</div>\n<div class="four-dim">\n' + dims_html + '\n</div>\n'


def build_table(data: dict) -> str:
    headers = data.get("headers", [])
    rows = data.get("rows", [])
    hdr_html = "".join(f"<th>{h}</th>" for h in headers)
    rows_html = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>\n" for row in rows)
    return f'<div class="table-wrap">\n<table><thead><tr>{hdr_html}</tr></thead><tbody>{rows_html}</tbody></table>\n</div>\n'


def build_source_stats(data: dict) -> str:
    items = "".join(
        f'''<div class="source-item">
  <span class="emoji">{s.get('emoji','')}</span>
  <div><div class="label">{s.get('label','')}</div></div>
  <div class="count">{s.get('count','')}</div>
</div>'''
        for s in data
    )
    return '<div class="section-header">📚 来源分布</div>\n<div class="source-stats">\n' + items + '\n</div>\n'


def build_interview(data: dict) -> str:
    rows = data.get("rows", [])
    hdr = "<th>场景</th><th>切入话题</th><th>预期反应</th>"
    rows_html = "".join(
        f"<tr><td>{r.get('scene','')}</td><td>{r.get('topic','')}</td><td class='{r.get('exp_class','')}'>{r.get('expected','')}</td></tr>\n"
        for r in rows
    )
    return f"""<div class="section-header cyan">🎯 访谈切入点建议</div>
<div class="table-wrap"><table><thead><tr>{hdr}</tr></thead><tbody>{rows_html}</tbody></table></div>\n"""


def build_footer() -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"""  <div class="footer">
    <span class="tag">🧠 AI可视化生成</span>
    <span class="tag">{now}</span>
  </div>"""

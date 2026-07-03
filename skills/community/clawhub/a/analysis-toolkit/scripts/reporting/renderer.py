"""renderer.py — 生成自包含 HTML 报告（Chart.js CDN → matplotlib base64 双模）"""
import io, os, base64, uuid

_MPL_AVAILABLE = None

def _check_matplotlib():
    global _MPL_AVAILABLE
    if _MPL_AVAILABLE is None:
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            _MPL_AVAILABLE = True
        except ImportError:
            _MPL_AVAILABLE = False
    return _MPL_AVAILABLE


def _fig_to_base64(fig):
    """将 matplotlib Figure 转为 base64 PNG"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')


# ─── Chart.js renderers ──────────────────────────────────────

def _render_chartjs_scatter(x_data, y_data, labels, title, xlabel, ylabel):
    """生成 Chart.js 散点图 HTML"""
    data_pts = ",".join(
        f"{{x:{x:.4f},y:{y:.4f},label:\"{lbl}\"}}"
        for x, y, lbl in zip(x_data, y_data, labels)
    )
    return f"""
    new Chart(ctx, {{
        type: 'scatter',
        data: {{
            datasets: [{{
                label: '{title}',
                data: [{data_pts}],
                backgroundColor: '#3498db',
                pointRadius: 5
            }}]
        }},
        options: {{
            scales: {{
                x: {{ title: {{ display: true, text: '{xlabel}' }} }},
                y: {{ title: {{ display: true, text: '{ylabel}' }} }}
            }}
        }}
    }});"""


def _render_chartjs_line(x_labels, y_values, title, xlabel, ylabel):
    """生成 Chart.js 折线图 HTML"""
    x_json = json.dumps(x_labels)
    y_json = json.dumps(y_values)
    return f"""
    new Chart(ctx, {{
        type: 'line',
        data: {{
            labels: {x_json},
            datasets: [{{
                label: '{title}',
                data: {y_json},
                borderColor: '#3498db',
                fill: false,
                tension: 0.1
            }}]
        }},
        options: {{
            responsive: true,
            scales: {{
                x: {{ title: {{ display: true, text: '{xlabel}' }} }},
                y: {{ title: {{ display: true, text: '{ylabel}' }} }}
            }}
        }}
    }});"""


def _render_chartjs_bar(labels, values, title, xlabel, ylabel):
    x_json = json.dumps(labels)
    y_json = json.dumps(values)
    return f"""
    new Chart(ctx, {{
        type: 'bar',
        data: {{
            labels: {x_json},
            datasets: [{{
                label: '{title}',
                data: {y_json},
                backgroundColor: '#3498db'
            }}]
        }},
        options: {{
            scales: {{
                x: {{ title: {{ display: true, text: '{xlabel}' }} }},
                y: {{ title: {{ display: true, text: '{ylabel}' }} }}
            }}
        }}
    }});"""


# ─── Main render function ──────────────────────────────────

import json

def build_html(markdown_body, chart_js_code=None, fig=None, title="分析报告"):
    """
    生成自包含 HTML 报告。
    如果提供了 chart_js_code，用 Chart.js CDN。
    如果提供了 matplotlib fig，回退为 base64 图片嵌入。
    如果都有，优先用 Chart.js。
    """
    chart_section = ""
    js_include = ""

    if chart_js_code:
        # Chart.js CDN 模式
        js_include = '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>'
        chart_section = f"""
        <div class="chart-container">
            <canvas id="chart_{uuid.uuid4().hex[:8]}"></canvas>
        </div>
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            var ctx = document.getElementById('chart_{uuid.uuid4().hex[:8]}').getContext('2d');
            {chart_js_code}
        }});
        </script>
        """
    elif fig is not None and _check_matplotlib():
        # matplotlib base64 回退
        img_b64 = _fig_to_base64(fig)
        chart_section = f'<div class="chart-container"><img src="data:image/png;base64,{img_b64}" style="max-width:100%"></div>'

    md_html = _md_to_html(markdown_body)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
{js_include}
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
       max-width: 960px; margin: 0 auto; padding: 20px; background: #f8f9fa; }}
h2 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 6px; }}
h3 {{ color: #34495e; }}
table {{ border-collapse: collapse; width: 100%; margin: 12px 0; background: white; }}
th, td {{ border: 1px solid #ddd; padding: 8px 12px; text-align: left; }}
th {{ background: #3498db; color: white; }}
tr:nth-child(even) {{ background: #f2f6fa; }}
.chart-container {{ background: white; padding: 16px; border-radius: 8px;
                   box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin: 16px 0; }}
</style>
</head>
<body>
<h1>{title}</h1>
{md_html}
{chart_section}
</body>
</html>"""


def _md_to_html(md_text):
    """极简 markdown → HTML 转换（仅支持表格和标题）"""
    import re
    lines = md_text.strip().split("\n")
    html_parts = []
    in_table = False
    for line in lines:
        if line.startswith("|") and line.endswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            # 跳过分隔行 (|---|)
            if all(c == "" or c.replace("-", "").strip() == "" for c in cells):
                if in_table:
                    # 结束表头，把上一行改为 <th>
                    if html_parts and html_parts[-1].startswith("<tr>"):
                        html_parts[-1] = html_parts[-1].replace("<td>", "<th>").replace("</td>", "</th>")
                    continue
            if not in_table:
                html_parts.append("<table>")
                in_table = True
            html_parts.append("<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
        else:
            if in_table:
                html_parts.append("</table>")
                in_table = False
            if line.startswith("### "):
                html_parts.append(f"<h3>{line[4:]}</h3>")
            elif line.startswith("## "):
                html_parts.append(f"<h2>{line[3:]}</h2>")
            elif line.strip():
                html_parts.append(f"<p>{line}</p>")
    if in_table:
        html_parts.append("</table>")
    return "\n".join(html_parts)


def save_html(html_str, output_dir=None, filename=None):
    """保存 HTML 到文件，返回路径"""
    if output_dir is None:
        # 数据目录：~/.workbuddy/skills/.standardization/analysis-toolkit/data/reports/
        renderer_dir = os.path.dirname(os.path.abspath(__file__))
        skill_dir = os.path.dirname(os.path.dirname(renderer_dir))  # scripts/
        skills_root = os.path.dirname(skill_dir)  # skills/analysis-toolkit → skills/
        output_dir = os.path.join(skills_root, ".standardization", "analysis-toolkit", "data", "reports")
    os.makedirs(output_dir, exist_ok=True)
    if filename is None:
        filename = f"report_{uuid.uuid4().hex[:12]}.html"
    path = os.path.join(output_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html_str)
    return path

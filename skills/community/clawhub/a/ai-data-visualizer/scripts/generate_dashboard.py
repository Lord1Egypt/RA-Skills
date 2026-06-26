#!/usr/bin/env python3
"""
AI Data Visualizer - Generate interactive HTML dashboards from data.
Usage:
  python generate_dashboard.py data.csv [-o output.html] [--theme dark|light]
  python generate_dashboard.py --json data.json [-o output.html]
  python generate_dashboard.py --stdin < data.csv [-o output.html]
"""

import argparse
import csv
import json
import sys
import re
import os
from datetime import datetime
from collections import Counter
from io import StringIO

# ---------------------------------------------------------------------------
# Data Parsing
# ---------------------------------------------------------------------------

def parse_csv(path):
    """Parse CSV file and return headers + rows."""
    with open(path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        rows = list(reader)
    return headers, rows


def parse_json(path):
    """Parse JSON array of objects."""
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, list) and data:
        headers = list(data[0].keys())
    elif isinstance(data, dict):
        headers = list(data.keys())
        data = [data]
    else:
        headers = []
        data = []
    return headers, data


def read_stdin():
    """Read CSV from stdin."""
    content = sys.stdin.read()
    reader = csv.DictReader(StringIO(content))
    headers = reader.fieldnames or []
    rows = list(reader)
    return headers, rows


def load_data(source, is_json=False, is_stdin=False):
    if is_stdin:
        return read_stdin()
    if is_json:
        return parse_json(source)
    return parse_csv(source)


# ---------------------------------------------------------------------------
# Column Type Detection
# ---------------------------------------------------------------------------

def try_float(val):
    try:
        f = float(val.strip().replace(',', '').replace('¥', '').replace('$', '').replace('%', ''))
        return f
    except:
        return None


DATE_PATTERNS = [
    (r'^\d{4}-\d{2}-\d{2}([T ]\d{2}:\d{2}(:\d{2})?)?', '%Y-%m-%d'),
    (r'^\d{4}/\d{2}/\d{2}', '%Y/%m/%d'),
    (r'^\d{2}/\d{2}/\d{4}', '%m/%d/%Y'),
    (r'^\d{2}-\d{2}-\d{4}', '%d-%m-%Y'),
    (r'^\d{4}年\d{1,2}月\d{1,2}日', None),
    (r'^\d{4}年\d{1,2}月', None),
]


def try_date(val):
    val = val.strip()
    for pattern, _ in DATE_PATTERNS:
        if re.match(pattern, val):
            for _, fmt in DATE_PATTERNS:
                if fmt:
                    try:
                        datetime.strptime(val, fmt)
                        return True
                    except:
                        continue
            if any(c in val for c in ['-', '/', 'year', 'month', 'day']):
                if re.search(r'\d{4}', val):
                    return True
    return False


def detect_column_type(values):
    """Detect type for a column: 'numeric', 'datetime', 'categorical', 'text'."""
    non_empty = [v for v in values if v.strip() != '']
    if not non_empty:
        return 'text'

    numeric_count = sum(1 for v in non_empty if try_float(v) is not None)
    if numeric_count / len(non_empty) >= 0.8:
        return 'numeric'

    date_count = sum(1 for v in non_empty if try_date(v))
    if date_count / len(non_empty) >= 0.8:
        return 'datetime'

    unique_count = len(set(non_empty))
    if unique_count <= 30 and unique_count / len(non_empty) <= 0.5:
        return 'categorical'

    return 'text'


def analyze_columns(headers, rows):
    """Analyze all columns and return type per header."""
    result = {}
    for h in headers:
        values = [row.get(h, '') for row in rows]
        col_type = detect_column_type(values)
        unique_vals = [v for v in set(values) if v.strip()]
        result[h] = {
            'type': col_type,
            'unique': unique_vals,
            'count': len(values),
            'nulls': sum(1 for v in values if v.strip() == ''),
        }
    return result


# ---------------------------------------------------------------------------
# Chart Selection
# ---------------------------------------------------------------------------

def select_charts(analysis):
    """Select chart configurations based on column analysis."""
    charts = []
    numeric_cols = [h for h, a in analysis.items() if a['type'] == 'numeric']
    categorical_cols = [h for h, a in analysis.items() if a['type'] == 'categorical']
    datetime_cols = [h for h, a in analysis.items() if a['type'] == 'datetime']

    # Strategy 1: Time series (datetime + numeric)
    if datetime_cols and numeric_cols:
        x_col = datetime_cols[0]
        for y_col in numeric_cols[:3]:
            charts.append({
                'type': 'line',
                'title': f'{y_col} Trend',
                'x': x_col,
                'y': y_col,
            })

    # Strategy 2: Category comparison (categorical + numeric)
    if categorical_cols and numeric_cols:
        x_col = categorical_cols[0]
        cat_info = analysis[x_col]
        if len(cat_info['unique']) <= 15:
            for y_col in numeric_cols[:2]:
                charts.append({
                    'type': 'bar',
                    'title': f'{y_col} by {x_col} Comparison',
                    'x': x_col,
                    'y': y_col,
                    'colorSet': 'category10',
                })
                if len(numeric_cols) == 1:
                    charts.append({
                        'type': 'pie',
                        'title': f'{y_col} Proportion Distribution',
                        'x': x_col,
                        'y': y_col,
                        'colorSet': 'category10',
                    })

    # Strategy 3: Numeric correlation (2+ numeric columns)
    if len(numeric_cols) >= 2 and not datetime_cols:
        x_col = numeric_cols[0]
        y_col = numeric_cols[1]
        charts.append({
            'type': 'scatter',
            'title': f'Relationship: {x_col} vs {y_col}',
            'x': x_col,
            'y': y_col,
        })

    # Strategy 4: Fallback - show all numeric columns as horizontal bar
    if not charts and numeric_cols:
        for y_col in numeric_cols[:5]:
            charts.append({
                'type': 'bar',
                'title': y_col,
                'x': 'index',
                'y': y_col,
                'colorSet': 'default',
            })

    return charts


# ---------------------------------------------------------------------------
# Data Aggregation for Charts
# ---------------------------------------------------------------------------

def numeric_val(v):
    f = try_float(v)
    return f if f is not None else 0


def aggregate_data(headers, rows, chart_cfg):
    """Aggregate data for a given chart config."""
    x_col = chart_cfg['x']
    y_col = chart_cfg['y']
    ctype = chart_cfg['type']

    if ctype == 'line':
        sorted_rows = sorted(rows, key=lambda r: r.get(x_col, ''))
        labels = [r.get(x_col, '') for r in sorted_rows]
        values = [numeric_val(r.get(y_col, '')) for r in sorted_rows]
        return labels, values

    elif ctype in ('bar', 'pie'):
        groups = {}
        for row in rows:
            k = row.get(x_col, 'Unknown')
            v = numeric_val(row.get(y_col, ''))
            if k not in groups:
                groups[k] = []
            groups[k].append(v)
        if ctype == 'bar':
            labels = list(groups.keys())
            values = [round(sum(v) / len(v), 2) for v in groups.values()]
        else:
            labels = list(groups.keys())
            values = [round(sum(v), 2) for v in groups.values()]
        return labels, values

    elif ctype in ('scatter',):
        points = []
        for r in rows:
            xv = numeric_val(r.get(x_col, ''))
            yv = numeric_val(r.get(y_col, ''))
            points.append({'x': xv, 'y': yv})
        return [], points

    return [], []


# ---------------------------------------------------------------------------
# Statistics Summary
# ---------------------------------------------------------------------------

def compute_summary(analysis, rows, numeric_cols):
    """Compute data summary statistics."""
    summary = []
    for col in numeric_cols:
        vals = [try_float(r.get(col, '')) for r in rows if try_float(r.get(col, '')) is not None]
        if vals:
            vals_sorted = sorted(vals)
            n = len(vals)
            summary.append({
                'col': col,
                'count': n,
                'sum': round(sum(vals), 2),
                'mean': round(sum(vals) / n, 2),
                'min': round(min(vals), 2),
                'max': round(max(vals), 2),
                'median': round(vals_sorted[n // 2], 2),
            })
    return summary


# ---------------------------------------------------------------------------
# HTML Generation
# ---------------------------------------------------------------------------

CHART_COLORS = {
    'category10': ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de',
                   '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'],
    'default': ['#5B8FF9', '#5AD8A6', '#5D7092', '#F6BD16', '#E86452',
                '#6DC8EC', '#945FB9', '#FF9845', '#1E9493', '#FF99C3'],
}


def get_chart_config(chart_cfg, labels, values, color_set='default'):
    """Generate Chart.js config for a given chart."""
    colors = CHART_COLORS.get(color_set, CHART_COLORS['default'])
    
    if chart_cfg['type'] == 'line':
        return {
            'type': 'line',
            'data': {
                'labels': labels,
                'datasets': [{
                    'label': chart_cfg['y'],
                    'data': values,
                    'borderColor': colors[0],
                    'backgroundColor': colors[0] + '20',
                    'fill': True,
                    'tension': 0.4,
                    'pointRadius': 3,
                }]
            },
            'options': {
                'responsive': True,
                'plugins': {'legend': {'display': True}},
                'scales': {
                    'y': {'beginAtZero': True},
                    'x': {'ticks': {'maxRotation': 45}}
                }
            }
        }
    
    elif chart_cfg['type'] == 'bar':
        return {
            'type': 'bar',
            'data': {
                'labels': labels,
                'datasets': [{
                    'label': chart_cfg['y'],
                    'data': values,
                    'backgroundColor': colors,
                    'borderRadius': 4,
                }]
            },
            'options': {
                'responsive': True,
                'plugins': {'legend': {'display': False}},
                'scales': {
                    'y': {'beginAtZero': True},
                    'x': {'ticks': {'maxRotation': 45}}
                }
            }
        }
    
    elif chart_cfg['type'] == 'pie':
        return {
            'type': 'doughnut',
            'data': {
                'labels': labels,
                'datasets': [{
                    'data': values,
                    'backgroundColor': colors,
                    'borderWidth': 2,
                }]
            },
            'options': {
                'responsive': True,
                'plugins': {
                    'legend': {'display': True, 'position': 'right'}
                }
            }
        }
    
    elif chart_cfg['type'] == 'scatter':
        return {
            'type': 'scatter',
            'data': {
                'datasets': [{
                    'label': f'{chart_cfg["x"]} vs {chart_cfg["y"]}',
                    'data': values if isinstance(values, list) else [],
                    'backgroundColor': colors[0],
                    'pointRadius': 5,
                }]
            },
            'options': {
                'responsive': True,
                'scales': {
                    'x': {'title': {'display': True, 'text': chart_cfg['x']}},
                    'y': {'title': {'display': True, 'text': chart_cfg['y']}}
                }
            }
        }
    
    return {}


# ---------------------------------------------------------------------------
# Main HTML Template
# ---------------------------------------------------------------------------

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
:root {{
  --bg: #f0f2f5;
  --card: #ffffff;
  --text: #1f2937;
  --text-secondary: #6b7280;
  --border: #e5e7eb;
  --accent: #4f46e5;
}}
[data-theme="dark"] {{
  --bg: #0f172a;
  --card: #1e293b;
  --text: #f1f5f9;
  --text-secondary: #94a3b8;
  --border: #334155;
  --accent: #818cf8;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans SC", sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
}}
header {{
  background: var(--card);
  border-bottom: 1px solid var(--border);
  padding: 16px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 100;
}}
header h1 {{ font-size: 20px; font-weight: 700; }}
.theme-toggle {{
  background: var(--accent);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}}
.main {{ max-width: 1400px; margin: 0 auto; padding: 24px; }}
.stats-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 32px;
}}
.stat-card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
}}
.stat-card .label {{ font-size: 13px; color: var(--text-secondary); margin-bottom: 4px; }}
.stat-card .value {{ font-size: 28px; font-weight: 700; }}
.charts-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}}
.chart-card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
}}
.chart-card h3 {{ font-size: 16px; font-weight: 600; margin-bottom: 16px; }}
.chart-wrap {{ position: relative; height: 300px; }}
.data-table-wrap {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  overflow-x: auto;
}}
table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
th, td {{ padding: 10px 16px; text-align: left; border-bottom: 1px solid var(--border); }}
th {{ background: var(--bg); font-weight: 600; position: sticky; top: 0; }}
tr:hover {{ background: var(--bg); }}
@media (max-width: 600px) {{
  .charts-grid {{ grid-template-columns: 1fr; }}
  .main {{ padding: 16px; }}
}}
</style>
</head>
<body>
<header>
  <h1>📊 {title}</h1>
  <button class="theme-toggle" onclick="toggleTheme()">🌓 Toggle Theme</button>
</header>
<div class="main">
  <div class="stats-grid" id="statsGrid"></div>
  <div class="charts-grid" id="chartsGrid"></div>
  <div class="data-table-wrap">
    <h3 style="margin-bottom:16px;">📋 Raw Data</h3>
    <table id="dataTable"><table>
  </div>
</div>
<script>
const CHART_DATA = {chart_data};
const TABLE_HEADERS = {headers};
const TABLE_ROWS = {table_rows};

function initTheme() {{
  const t = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', t);
}}
function toggleTheme() {{
  const cur = document.documentElement.getAttribute('data-theme');
  const next = cur === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
  // Update chart colors
  Object.values(Chart.instances).forEach(c => c.update());
}}
initTheme();

// Render stats
function renderStats() {{
  const grid = document.getElementById('statsGrid');
  const stats = CHART_DATA.stats || [];
  grid.innerHTML = stats.map(s => `
    <div class="stat-card">
      <div class="label">${{s.label}}</div>
      <div class="value">${{s.value}}</div>
    </div>
  `).join('');
}}

// Render charts
function renderCharts() {{
  const grid = document.getElementById('chartsGrid');
  grid.innerHTML = '';
  CHART_DATA.charts.forEach((c, i) => {{
    const card = document.createElement('div');
    card.className = 'chart-card';
    card.innerHTML = `<h3>${{c.title}}</h3><div class="chart-wrap"><canvas id="chart${{i}}"></canvas></div>`;
    grid.appendChild(card);
    new Chart(document.getElementById(`chart${{i}}`), c.config);
  }});
}}

// Render table
function renderTable() {{
  const table = document.getElementById('dataTable');
  let html = '<thead><tr>' + TABLE_HEADERS.map(h => `<th>${{h}}</th>`).join('') + '</tr></thead>';
  html += '<tbody>' + TABLE_ROWS.map(r => 
    '<tr>' + TABLE_HEADERS.map(h => `<td>${{r[h] || ''}}</td>`).join('') + '</tr>'
  ).join('') + '</tbody>';
  table.innerHTML = html;
}}

renderStats();
renderCharts();
renderTable();
</script>
</body>
</html>'''


def generate_html(headers, rows, analysis, output_path, title='Data Visualization Dashboard', theme='light'):
    """Generate the HTML dashboard file."""
    numeric_cols = [h for h, a in analysis.items() if a['type'] == 'numeric']
    charts = select_charts(analysis)
    
    # Build chart data for JS
    chart_data_list = []
    for cfg in charts:
        labels, values = aggregate_data(headers, rows, cfg)
        color_set = cfg.get('colorSet', 'default')
        config = get_chart_config(cfg, labels, values, color_set)
        chart_data_list.append({
            'title': cfg['title'],
            'config': config
        })
    
    # Build stats
    total_rows = len(rows)
    total_cols = len(headers)
    numeric_count = len(numeric_cols)
    
    stats = [
        {'label': 'Rows', 'value': total_rows},
        {'label': 'Columns', 'value': total_cols},
        {'label': 'Numeric Columns', 'value': numeric_count},
    ]
    if numeric_cols:
        vals = [try_float(r.get(numeric_cols[0], '')) for r in rows if try_float(r.get(numeric_cols[0], '')) is not None]
        if vals:
            stats.append({'label': f'Avg {numeric_cols[0]}', 'value': round(sum(vals)/len(vals), 2)})
    
    # Build table rows (limit to 500 for performance)
    table_rows = []
    for r in rows[:500]:
        row_dict = {h: r.get(h, '') for h in headers}
        table_rows.append(row_dict)
    
    chart_data_js = json.dumps({'charts': chart_data_list, 'stats': stats}, ensure_ascii=False)
    headers_js = json.dumps(headers, ensure_ascii=False)
    table_rows_js = json.dumps(table_rows, ensure_ascii=False)
    
    html = HTML_TEMPLATE.format(
        title=title,
        chart_data=chart_data_js,
        headers=headers_js,
        table_rows=table_rows_js
    )
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Dashboard generated: {output_path}")
    print(f"   Charts: {len(charts)} | Rows: {total_rows} | Cols: {total_cols}")


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='Generate interactive HTML dashboard from data')
    parser.add_argument('input', nargs='?', help='Input CSV or JSON file')
    parser.add_argument('-o', '--output', default='dashboard.html', help='Output HTML file path')
    parser.add_argument('--json', action='store_true', help='Input is JSON format')
    parser.add_argument('--stdin', action='store_true', help='Read from stdin (CSV)')
    parser.add_argument('--theme', default='light', choices=['light', 'dark'], help='Default theme')
    parser.add_argument('--title', default='Data Visualization Dashboard', help='Dashboard title')
    
    args = parser.parse_args()
    
    if not args.stdin and not args.input:
        parser.print_help()
        sys.exit(1)
    
    headers, rows = load_data(args.input, is_json=args.json, is_stdin=args.stdin)
    
    if not headers:
        print("Error: No data loaded. Check file format.")
        sys.exit(1)
    
    print(f"Loaded: {len(rows)} rows × {len(headers)} columns")
    print(f"Headers: {headers}")
    
    analysis = analyze_columns(headers, rows)
    print("\nColumn analysis:")
    for h, a in analysis.items():
        print(f"  {h}: {a['type']} ({a['count']} values, {len(a['unique'])} unique)")
    
    generate_html(headers, rows, analysis, args.output, title=args.title, theme=args.theme)


if __name__ == '__main__':
    main()
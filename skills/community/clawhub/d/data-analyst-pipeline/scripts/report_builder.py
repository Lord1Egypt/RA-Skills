"""
HTML report builder for data analysis results.
Generates a self-contained interactive HTML report with scorecards, charts, and insights.
"""
import os
import sys
import json
import base64
import pandas as pd
from datetime import datetime
from pathlib import Path


def build_report(df: pd.DataFrame, audit_results: dict, eda_results: dict,
                 charts: dict, output_path: str, dataset_name: str = "Dataset") -> str:
    """
    Build a complete HTML analysis report.

    Args:
        df: Cleaned DataFrame
        audit_results: From data_auditor.audit_data()
        eda_results: From eda_runner.run_eda()
        charts: From visualizer.generate_all_charts() (name -> filepath(s))
        output_path: Output HTML file path
        dataset_name: Name for the report title

    Returns:
        Path to the generated HTML file
    """
    charts_html = _collect_charts_html(charts)

    report_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Data Analysis Report — {dataset_name}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif; background: #f5f7fa; color: #2c3e50; line-height: 1.6; }}
.container {{ max-width: 1200px; margin: 0 auto; padding: 32px 20px; }}
/* Header */
.header {{ background: linear-gradient(135deg, #2c3e50, #3498db); color: white; padding: 40px 32px; border-radius: 16px; margin-bottom: 24px; }}
.header h1 {{ font-size: 28px; margin-bottom: 8px; }}
.header .meta {{ opacity: 0.8; font-size: 14px; }}
/* Score Cards */
.score-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 24px; }}
.score-card {{ background: white; border-radius: 12px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center; }}
.score-card .value {{ font-size: 36px; font-weight: 700; margin: 8px 0; }}
.score-card .label {{ font-size: 13px; color: #7f8c8d; text-transform: uppercase; letter-spacing: 0.5px; }}
.grade-a .value {{ color: #27ae60; }}
.grade-b .value {{ color: #3498db; }}
.grade-c .value {{ color: #f39c12; }}
.grade-d .value {{ color: #e74c3c; }}
/* Sections */
.section {{ background: white; border-radius: 12px; padding: 32px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
.section h2 {{ font-size: 20px; color: #2c3e50; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #3498db; }}
.section h3 {{ font-size: 16px; color: #34495e; margin: 16px 0 8px; }}
/* Tables */
table {{ width: 100%; border-collapse: collapse; margin: 8px 0 16px; font-size: 13px; }}
th {{ background: #f8f9fa; padding: 10px 12px; text-align: left; border-bottom: 2px solid #dee2e6; font-weight: 600; color: #495057; }}
td {{ padding: 8px 12px; border-bottom: 1px solid #e9ecef; }}
tr:hover {{ background: #f8f9fa; }}
/* Charts */
.charts-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(450px, 1fr)); gap: 20px; margin: 16px 0; }}
.chart-item {{ background: #f8f9fa; border-radius: 8px; padding: 16px; text-align: center; }}
.chart-item img {{ max-width: 100%; height: auto; border-radius: 6px; }}
.chart-item .caption {{ font-size: 12px; color: #7f8c8d; margin-top: 8px; }}
.single-chart img {{ max-width: 100%; border-radius: 6px; }}
/* Issues */
.issue-list {{ list-style: none; }}
.issue-list li {{ padding: 8px 12px; margin: 4px 0; border-radius: 6px; font-size: 13px; border-left: 3px solid; }}
.issue-list li.warning {{ background: #fff3cd; border-color: #f39c12; color: #856404; }}
.issue-list li.error {{ background: #f8d7da; border-color: #e74c3c; color: #721c24; }}
/* Badges */
.badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; }}
.badge-ok {{ background: #d4edda; color: #155724; }}
.badge-warn {{ background: #fff3cd; color: #856404; }}
.badge-err {{ background: #f8d7da; color: #721c24; }}
/* Footer */
.footer {{ text-align: center; color: #95a5a6; font-size: 12px; margin-top: 32px; padding: 16px; }}
/* Responsive */
@media (max-width: 768px) {{
  .charts-grid {{ grid-template-columns: 1fr; }}
  .score-grid {{ grid-template-columns: repeat(2, 1fr); }}
  .container {{ padding: 16px; }}
}}
</style>
</head>
<body>
<div class="container">

  <!-- Header -->
  <div class="header">
    <h1>📊 Data Analysis Report</h1>
    <div class="meta">
      <strong>{dataset_name}</strong> &nbsp;|&nbsp;
      Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} &nbsp;|&nbsp;
      {eda_results['overview']['rows']:,} rows &times; {eda_results['overview']['columns']} cols
    </div>
  </div>

  <!-- Score Cards -->
  <div class="score-grid">
    <div class="score-card grade-{audit_results['summary']['score']['grade'].lower()}">
      <div class="label">Data Quality</div>
      <div class="value">{audit_results['summary']['score']['score']}</div>
      <div style="font-size: 12px; color: #7f8c8d;">Grade {audit_results['summary']['score']['grade']}</div>
    </div>
    <div class="score-card">
      <div class="label">Rows</div>
      <div class="value" style="color: #2c3e50;">{eda_results['overview']['rows']:,}</div>
    </div>
    <div class="score-card">
      <div class="label">Columns</div>
      <div class="value" style="color: #2c3e50;">{eda_results['overview']['columns']}</div>
    </div>
    <div class="score-card">
      <div class="label">Missing</div>
      <div class="value" style="color: {'#e74c3c' if eda_results['overview']['missing_pct'] > 5 else '#27ae60'};">{eda_results['overview']['missing_pct']}%</div>
    </div>
  </div>

  <!-- Issues -->
  {_build_issues_section(audit_results)}

  <!-- Numeric Summary -->
  {_build_numeric_table(eda_results)}

  <!-- Categorical Summary -->
  {_build_categorical_table(eda_results)}

  <!-- Correlation -->
  {_build_correlation_section(eda_results)}

  <!-- Charts -->
  <div class="section">
    <h2>📈 Visualizations</h2>
    {charts_html}
  </div>

  <!-- Outliers -->
  {_build_outliers_section(audit_results)}

  <div class="footer">
    Generated by Data Analyst Skill &bull; {datetime.now().year}
  </div>

</div>
</body>
</html>"""

    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_html)

    print(f"[ReportBuilder] Report saved to: {output_path}")
    return output_path


def _collect_charts_html(charts: dict) -> str:
    """Collect all chart images and embed as base64 HTML."""
    html_parts = []
    chart_names = {
        'distributions': 'Distribution Histograms',
        'boxplots': 'Box Plots',
        'correlation_heatmap': 'Correlation Heatmap',
        'missing_values': 'Missing Values',
        'categorical_top': 'Categorical Distributions',
        'pairplot': 'Pair Plot Matrix',
        'target_vs_features': 'Target vs Features',
    }

    for key, paths in charts.items():
        if not paths:
            continue
        if isinstance(paths, str):
            paths = [paths]

        name = chart_names.get(key, key.replace('_', ' ').title())

        if len(paths) == 1:
            html_parts.append(f'''
            <div class="single-chart">
              <h3>{name}</h3>
              <img src="{_img_to_b64(paths[0])}" alt="{name}">
            </div>''')
        else:
            items = '\n'.join(f'''
              <div class="chart-item">
                <img src="{_img_to_b64(p)}" alt="{name}">
                <div class="caption">{name} #{i+1}/{len(paths)}</div>
              </div>''' for i, p in enumerate(paths))
            html_parts.append(f'<h3>{name}</h3><div class="charts-grid">{items}</div>')

    return '\n'.join(html_parts)


def _img_to_b64(path: str) -> str:
    """Convert image at path to base64 data URI."""
    if not path or not os.path.exists(path):
        return ''
    with open(path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
    ext = Path(path).suffix.lower().replace('.', '')
    return f'data:image/{ext};base64,{b64}'


def _build_issues_section(audit: dict) -> str:
    """Build issue list section."""
    issues = audit['summary'].get('issues', [])
    score_detail = audit['summary'].get('score', {})

    ded_html = ''
    for d in score_detail.get('deductions', []):
        ded_html += f'<li class="warning">{d}</li>'

    if not issues and not ded_html:
        return '''<div class="section">
          <h2>🔍 Data Quality Audit</h2>
          <p style="color: #27ae60;">✅ No issues detected. Data quality looks excellent!</p>
        </div>'''

    issue_html = '\n'.join(f'<li class="warning">{i}</li>' for i in issues)

    return f'''<div class="section">
      <h2>🔍 Data Quality Audit</h2>
      <h3>Quality Score Deductions</h3>
      <ul class="issue-list">{ded_html or '<li>No deductions</li>'}</ul>
      <h3>Top Issues ({len(issues)} total)</h3>
      <ul class="issue-list">{issue_html or '<li>No issues found</li>'}</ul>
    </div>'''


def _build_numeric_table(eda: dict) -> str:
    """Build numeric summary table."""
    summary = eda.get('numeric_summary', [])
    if not summary:
        return ''

    rows = '\n'.join(f'''
      <tr>
        <td>{s['column']}</td>
        <td>{s['count']:,}</td>
        <td>{s['missing']}</td>
        <td>{s['mean']}</td>
        <td>{s['std']}</td>
        <td>{s['min']}</td>
        <td>{s['q25']}</td>
        <td>{s['median']}</td>
        <td>{s['q75']}</td>
        <td>{s['max']}</td>
        <td>{s['skewness']}</td>
      </tr>''' for s in summary)

    return f'''<div class="section">
      <h2>📋 Numeric Features Summary</h2>
      <div style="overflow-x: auto;">
        <table>
          <thead><tr>
            <th>Column</th><th>Count</th><th>Missing</th><th>Mean</th><th>Std</th>
            <th>Min</th><th>Q25</th><th>Median</th><th>Q75</th><th>Max</th><th>Skew</th>
          </tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </div>'''


def _build_categorical_table(eda: dict) -> str:
    """Build categorical summary table."""
    summary = eda.get('categorical_summary', [])
    if not summary:
        return ''

    rows = '\n'.join(f'''
      <tr>
        <td>{s['column']}</td>
        <td>{s['count']:,}</td>
        <td>{s['unique']}</td>
        <td>{s['missing']}</td>
        <td>{s['top_value']}</td>
        <td>{s['top_count']:,}</td>
        <td>{s['top_pct']}%</td>
      </tr>''' for s in summary)

    return f'''<div class="section">
      <h2>📋 Categorical Features Summary</h2>
      <div style="overflow-x: auto;">
        <table>
          <thead><tr>
            <th>Column</th><th>Count</th><th>Unique</th><th>Missing</th>
            <th>Top Value</th><th>Top Count</th><th>Top %</th>
          </tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </div>'''


def _build_correlation_section(eda: dict) -> str:
    """Build top correlation pairs section."""
    corr = eda.get('correlation', {})
    top = corr.get('top_correlations', [])
    if not top:
        return ''

    rows = '\n'.join(f'''
      <tr>
        <td>{c['feature1']}</td>
        <td>{c['feature2']}</td>
        <td>{c['correlation']}</td>
        <td><span class="badge badge-{'ok' if c['strength'] == 'strong' else 'warn'}">{c['strength']}</span></td>
        <td>{c['direction']}</td>
      </tr>''' for c in top[:15])

    return f'''<div class="section">
      <h2>🔗 Top Correlations</h2>
      <table>
        <thead><tr>
          <th>Feature 1</th><th>Feature 2</th><th>Correlation</th><th>Strength</th><th>Direction</th>
        </tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>'''


def _build_outliers_section(audit: dict) -> str:
    """Build outlier summary."""
    l4 = audit.get('layer4_readiness', {})
    outliers = l4.get('outliers', {})
    if not outliers:
        return ''

    rows = '\n'.join(f'''
      <tr>
        <td>{col}</td>
        <td>{info['count']:,}</td>
        <td>{info['percentage']:.1f}%</td>
        <td>{info['lower_bound']}</td>
        <td>{info['upper_bound']}</td>
      </tr>''' for col, info in sorted(outliers.items(), key=lambda x: x[1]['percentage'], reverse=True)[:15])

    return f'''<div class="section">
      <h2>⚠️ Outlier Detection (IQR Method)</h2>
      <table>
        <thead><tr>
          <th>Column</th><th>Outliers</th><th>%</th><th>Lower Bound</th><th>Upper Bound</th>
        </tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>'''


if __name__ == "__main__":
    print("ReportBuilder module — import and use build_report()")

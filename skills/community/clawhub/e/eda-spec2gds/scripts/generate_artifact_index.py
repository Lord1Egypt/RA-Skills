#!/usr/bin/env python3
from pathlib import Path
import json
import sys
import html

ROOT = Path('/root/.openclaw/workspace/skills/eda-spec2gds/eda-runs/simple_fifo_demo').resolve()
REPORTS = ROOT / 'reports'
INDEX = REPORTS / 'index.html'


def load_json(path: Path, default=None):
    if default is None:
        default = {}
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return default


def fmt(v):
    if v is None:
        return '-'
    if isinstance(v, float):
        return f'{v:.6g}'
    return str(v)


def ppa_table(ppa):
    summary = ppa.get('summary', {}) if ppa else {}
    if not summary:
        return '<p>No PPA data yet.</p>'
    rows = []
    for section, vals in summary.items():
        rows.append(f'<tr><th colspan="2" style="text-align:left;background:#f6f6f6">{html.escape(section.title())}</th></tr>')
        for k, v in vals.items():
            rows.append(f'<tr><td>{html.escape(k)}</td><td><code>{html.escape(fmt(v))}</code></td></tr>')
    return '<table style="border-collapse:collapse;width:100%">' + ''.join(
        f'<tr style="border-top:1px solid #eee">{r[4:-5] if r.startswith("<tr>") else r}</tr>' if r.startswith('<tr><td') else r
        for r in rows
    ) + '</table>'


def ppa_details_block(ppa):
    details = ppa.get('details', {}) if ppa else {}
    metric_count = ppa.get('raw_metric_count', '-') if ppa else '-'
    if not details:
        return '<p>No detailed PPA yet.</p>'
    blocks = [f'<p><strong>Raw metric count:</strong> <code>{html.escape(fmt(metric_count))}</code></p>']
    for section, vals in details.items():
        blocks.append(f'<h3>{html.escape(section)}</h3>')
        if not vals:
            blocks.append('<p>-</p>')
            continue
        rows = ''.join(f'<tr><td>{html.escape(k)}</td><td><code>{html.escape(fmt(v))}</code></td></tr>' for k, v in vals.items())
        blocks.append(f'<table style="border-collapse:collapse;width:100%">{rows}</table>')
    return ''.join(blocks)


def status_badge(status):
    colors = {'done': '#1f7a1f', 'started': '#b36b00', 'unknown': '#666'}
    color = colors.get(status, '#666')
    return f'<span style="display:inline-block;padding:2px 8px;border-radius:999px;background:{color};color:white;font-size:12px">{html.escape(status)}</span>'


def render_stages(progress):
    stages = progress.get('stages', []) if progress else []
    if not stages:
        return '<p>No stage progress yet.</p>'
    items = []
    for s in stages:
        items.append(f"<tr><td>{html.escape(s['name'])}</td><td>{status_badge(s['status'])}</td></tr>")
    return '<table style="border-collapse:collapse;width:100%">' + ''.join(items) + '</table>'


def render_tail(lines):
    if not lines:
        return '<pre>No log yet.</pre>'
    return '<pre>' + html.escape('\n'.join(lines)) + '</pre>'


def render_artifacts(artifacts):
    files = artifacts.get('artifacts', []) if artifacts else []
    if not files:
        return '<p>No artifacts listed yet.</p>'
    lis = ''.join(f'<li><code>{html.escape(x)}</code></li>' for x in files[:200])
    return f'<ul>{lis}</ul>'


def main():
    results = load_json(REPORTS / 'openlane-results.json', {})
    ppa = load_json(REPORTS / 'ppa.json', {})
    progress = load_json(REPORTS / 'progress.json', {})
    artifacts = load_json(REPORTS / 'artifacts-index.json', {})
    summary = (REPORTS / 'demo-summary.md').read_text(encoding='utf-8', errors='ignore') if (REPORTS / 'demo-summary.md').exists() else 'No summary yet.'
    preview = 'simple_fifo_preview.png' if (REPORTS / 'simple_fifo_preview.png').exists() else None
    html_text = f'''<!doctype html>
<html><head><meta charset="utf-8"><title>EDA Demo Artifacts</title>
<meta http-equiv="refresh" content="10">
<style>
body {{ font-family: Arial, sans-serif; max-width: 1280px; margin: 24px auto; padding: 0 16px; color:#111; }}
pre {{ background: #111; color: #eee; padding: 12px; overflow: auto; white-space: pre-wrap; }}
code {{ background: #f2f2f2; padding: 2px 6px; }}
img {{ max-width: 100%; border: 1px solid #ddd; }}
.card {{ border: 1px solid #ddd; border-radius: 10px; padding: 16px; margin: 16px 0; }}
.small {{ color: #666; font-size: 13px; }}
td, th {{ padding: 8px; border-top: 1px solid #eee; text-align:left; vertical-align:top; }}
.grid {{ display:grid; grid-template-columns: 1.2fr 1fr; gap:16px; align-items:start; }}
.grid2 {{ display:grid; grid-template-columns: 1fr 1fr; gap:16px; align-items:start; }}
</style></head>
<body>
<h1>EDA Demo Artifacts</h1>
<div class="card">
  <p><strong>Project:</strong> <code>{html.escape(results.get('project_dir',''))}</code></p>
  <p><strong>Latest run:</strong> <code>{html.escape(results.get('latest_run',''))}</code></p>
  <p><strong>GDS:</strong> <code>{html.escape(results.get('gds',''))}</code></p>
  <p class="small">Auto-refresh every 10s.</p>
</div>
<div class="grid">
  <div class="card">
    <h2>Preview</h2>
    {f'<img src="{preview}" alt="GDS preview">' if preview else '<p>No preview image yet.</p>'}
  </div>
  <div class="card">
    <h2>PPA</h2>
    {ppa_table(ppa)}
  </div>
</div>
<div class="grid2">
  <div class="card">
    <h2>Progress</h2>
    {render_stages(progress)}
  </div>
  <div class="card">
    <h2>Artifacts</h2>
    {render_artifacts(artifacts)}
  </div>
</div>
<div class="grid2">
  <div class="card">
    <h2>flow.log tail</h2>
    {render_tail(progress.get('tails', {}).get('flow.log', []))}
  </div>
  <div class="card">
    <h2>warning.log tail</h2>
    {render_tail(progress.get('tails', {}).get('warning.log', []))}
  </div>
</div>
<div class="card">
  <h2>Summary</h2>
  <pre>{html.escape(summary)}</pre>
</div>
<div class="card">
  <h2>Detailed PPA</h2>
  {ppa_details_block(ppa)}
</div>
<div class="card">
  <h2>Raw result JSON</h2>
  <pre>{html.escape(json.dumps(results, indent=2, ensure_ascii=False))}</pre>
</div>
</body></html>'''
    INDEX.write_text(html_text, encoding='utf-8')
    print(INDEX)


if __name__ == '__main__':
    main()

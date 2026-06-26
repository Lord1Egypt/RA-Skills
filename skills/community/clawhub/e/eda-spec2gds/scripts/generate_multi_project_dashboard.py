#!/usr/bin/env python3
from pathlib import Path
import json
import html

BASE = Path('/root/.openclaw/workspace/skills/eda-spec2gds/eda-runs').resolve()
OUT = BASE / '_dashboard'


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


def find_latest_run(project: Path):
    runs = sorted(project.glob('constraints/runs/*'))
    runs = [p for p in runs if p.is_dir()]
    # Prefer runs with actual results (final directory)
    for r in reversed(runs):
        if (r / 'final').exists():
            return r
    return runs[-1] if runs else None


def get_run_timestamp(run_dir):
    """Extract timestamp from run directory name (e.g., RUN_2026-03-16_10-33-03)"""
    if not run_dir:
        return None
    name = run_dir.name
    # Try to parse RUN_YYYY-MM-DD_HH-MM-SS format
    import re
    match = re.search(r'RUN_(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})', name)
    if match:
        return match.group(1).replace('_', ' ').replace('-', ':')
    return name


def infer_project_status(project: Path, latest, summary: str):
    if latest and (latest / 'final' / 'gds').exists():
        return 'pass'
    s = (summary or '').lower()
    if 'fail' in s or 'error' in s:
        return 'fail'
    if latest is not None:
        return 'running'
    return 'unknown'


def collect_project(project: Path):
    reports = project / 'reports'
    latest = find_latest_run(project)
    ppa = load_json(reports / 'ppa.json', {})
    summary = (reports / 'demo-summary.md').read_text(encoding='utf-8', errors='ignore') if (reports / 'demo-summary.md').exists() else ''
    raw_spec = (project / 'input' / 'raw-spec.md').read_text(encoding='utf-8', errors='ignore') if (project / 'input' / 'raw-spec.md').exists() else ''
    normalized_spec = (project / 'input' / 'normalized-spec.yaml').read_text(encoding='utf-8', errors='ignore') if (project / 'input' / 'normalized-spec.yaml').exists() else ''
    preview = reports / 'simple_fifo_preview.png'
    if not preview.exists():
        preview = reports / 'simple_counter_preview.png'
    if not preview.exists():
        imgs = sorted(reports.glob('*preview*.png'))
        preview = imgs[0] if imgs else None
    gds = None
    if latest:
        gds_files = sorted((latest / 'final' / 'gds').glob('*.gds')) if (latest / 'final' / 'gds').exists() else []
        gds = str(gds_files[0].relative_to(BASE)) if gds_files else None
    progress = load_json(reports / 'progress.json', {})
    artifacts = load_json(reports / 'artifacts-index.json', {})
    run_history = load_json(reports / 'run-history.json', {})
    run_compare = load_json(reports / 'run-compare.json', {})
    diagnosis = load_json(reports / 'diagnosis.json', {})
    final_dir = None
    def_file = None
    odb_file = None
    if latest and (latest / 'final').exists():
        final_dir = str((latest / 'final').relative_to(BASE))
        defs = sorted((latest / 'final' / 'def').glob('*.def')) if (latest / 'final' / 'def').exists() else []
        odbs = sorted((latest / 'final' / 'odb').glob('*.odb')) if (latest / 'final' / 'odb').exists() else []
        def_file = str(defs[0].relative_to(BASE)) if defs else None
        odb_file = str(odbs[0].relative_to(BASE)) if odbs else None
    try:
        normalized_spec_obj = json.loads(json.dumps({}))
    except Exception:
        normalized_spec_obj = {}
    # Minimal YAML-ish extraction without adding a parser dependency.
    spec_desc = ''
    top_module = ''
    for line in normalized_spec.splitlines():
        if line.startswith('description:') and not spec_desc:
            spec_desc = line.split(':', 1)[1].strip()
        if line.startswith('top_module:') and not top_module:
            top_module = line.split(':', 1)[1].strip()
    raw_spec_brief = raw_spec.strip().splitlines()[0] if raw_spec.strip() else ''
    return {
        'name': project.name,
        'path': str(project.relative_to(BASE)),
        'latest_run': str(latest.relative_to(BASE)) if latest else None,
        'preview': str(preview.relative_to(BASE)) if preview and preview.exists() else None,
        'gds': gds,
        'def': def_file,
        'odb': odb_file,
        'final_dir': final_dir,
        'ppa': ppa,
        'summary': summary,
        'raw_spec': raw_spec,
        'raw_spec_brief': raw_spec_brief,
        'normalized_spec': normalized_spec,
        'spec_desc': spec_desc,
        'top_module': top_module,
        'progress': progress,
        'artifacts': artifacts,
        'run_history': run_history,
        'run_compare': run_compare,
        'diagnosis': diagnosis,
        'status': infer_project_status(project, latest, summary),
    }


def ppa_brief(ppa):
    summary = ppa.get('summary', {}) if ppa else {}
    area = summary.get('area', {})
    timing = summary.get('timing', {})
    power = summary.get('power', {})
    checks = summary.get('checks', {})
    return [
        ('utilization', area.get('utilization')),
        ('setup_wns', timing.get('setup_wns')),
        ('hold_wns', timing.get('hold_wns')),
        ('power_total', power.get('total')),
        ('lvs_errors', checks.get('lvs_errors')),
        ('magic_drc_errors', checks.get('magic_drc_errors')),
    ]


def group_stage_name(name: str):
    n = name.lower()
    if any(x in n for x in ['verilator', 'yosys', 'lint', 'synth', 'jsonheader']):
        return 'Lint & Synthesis'
    if any(x in n for x in ['floorplan', 'pdn', 'tapendcap', 'cutrows', 'ioplacement', 'macro', 'obstruction']):
        return 'Floorplan & PDN'
    if any(x in n for x in ['globalplacement', 'detailedplacement', 'cts', 'repairdesign', 'stamidpnr', 'resizer']):
        return 'Placement & CTS'
    if any(x in n for x in ['globalrouting', 'detailedrouting', 'antenn', 'wirelength', 'fillinsertion', 'rcx']):
        return 'Routing'
    if any(x in n for x in ['sta', 'lvs', 'magic', 'netgen', 'report', 'manufacturability', 'trdrc', 'disconnectedpins']):
        return 'Signoff & Reports'
    return 'Other'


def render_grouped_stages(progress):
    stages = progress.get('stages', []) if progress else []
    if not stages:
        return '<p class="muted">No progress yet.</p>'
    groups = {}
    for s in stages:
        groups.setdefault(group_stage_name(s.get('name', '')), []).append(s)
    order = ['Lint & Synthesis', 'Floorplan & PDN', 'Placement & CTS', 'Routing', 'Signoff & Reports', 'Other']
    parts = []
    for g in order:
        items = groups.get(g, [])
        if not items:
            continue
        done = sum(1 for x in items if x.get('status') in ['done', 'pass'])
        total = len(items)
        rows = ''.join(f'<tr><td>{html.escape(x.get("name",""))}</td><td><span class="status {html.escape(x.get("status","unknown"))}">{html.escape(x.get("status",""))}</span></td></tr>' for x in items)
        parts.append(f'<details class="detail-group" open><summary>{html.escape(g)} <span class="muted">({done}/{total})</span></summary><table class="stage-table">{rows}</table></details>')
    return ''.join(parts)


def render_project_page(data):
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / f"{data['name']}.html"
    preview_html = f'<img src="../{html.escape(data["preview"])}" style="max-width:100%;border:1px solid #d8dee8;border-radius:16px;background:#fff">' if data.get('preview') else '<p class="muted">No preview yet.</p>'
    ppa_rows = ''.join(f'<tr><td>{html.escape(k)}</td><td><code>{html.escape(fmt(v))}</code></td></tr>' for k, v in ppa_brief(data.get('ppa', {})))
    details = data.get('ppa', {}).get('details', {})
    metric_count = data.get('ppa', {}).get('raw_metric_count', '-')
    detail_blocks = [f'<p><strong>Raw metric count:</strong> <code>{html.escape(fmt(metric_count))}</code></p>']
    for section, vals in details.items():
        title = section.replace('_', ' ')
        if not vals:
            detail_blocks.append(f'<details class="detail-group"><summary>{html.escape(title)}</summary><p class="muted">-</p></details>')
        else:
            rows = ''.join(f'<tr><td>{html.escape(k)}</td><td><code>{html.escape(fmt(v))}</code></td></tr>' for k, v in vals.items())
            detail_blocks.append(f'<details class="detail-group"><summary>{html.escape(title)}</summary><table class="metric-table">{rows}</table></details>')
    grouped_stages = render_grouped_stages(data.get('progress', {}))
    artifacts = ''.join(f'<li><code>{html.escape(x)}</code></li>' for x in data.get('artifacts', {}).get('artifacts', [])[:120]) or '<li>-</li>'
    flow_tail = '\n'.join(data.get('progress', {}).get('tails', {}).get('flow.log', [])) or 'No flow log yet.'
    warn_tail = '\n'.join(data.get('progress', {}).get('tails', {}).get('warning.log', [])) or 'No warning log yet.'
    diagnosis = data.get('diagnosis', {})
    compare = data.get('run_compare', {})
    baseline = compare.get('baseline') or {}
    current = compare.get('current') or {}
    delta_map = compare.get('delta') or {}
    compare_metrics = ['die_area', 'utilization', 'setup_wns', 'hold_wns', 'power_total', 'route_drc_errors', 'lvs_errors', 'magic_drc_errors', 'max_slew_violations']
    compare_rows = ''.join(
        f'<tr><td>{html.escape(m)}</td><td><code>{html.escape(fmt(baseline.get(m)))}</code></td><td><code>{html.escape(fmt(current.get(m)))}</code></td><td><code>{html.escape(fmt(delta_map.get(m)))}</code></td></tr>'
        for m in compare_metrics
    ) or '<tr><td colspan="4">No compare data yet.</td></tr>'
    history_rows = ''.join(
        f'<tr><td><code>{html.escape(r.get("run",""))}</code></td><td><span class="status {html.escape(r.get("status","unknown"))}">{html.escape(r.get("status",""))}</span></td><td><code>{html.escape(fmt(r.get("utilization")))}</code></td><td><code>{html.escape(fmt(r.get("setup_wns")))}</code></td><td><code>{html.escape(fmt(r.get("power_total")))}</code></td></tr>'
        for r in data.get('run_history', {}).get('runs', [])
    ) or '<tr><td colspan="5">No run history yet.</td></tr>'
    gds_link = f'<a href="../{html.escape(data["gds"])}" download class="btn primary">Download GDS</a>' if data.get('gds') else ''
    def_link = f'<a href="../{html.escape(data["def"])}" download class="btn dark">Download DEF</a>' if data.get('def') else ''
    odb_link = f'<a href="../{html.escape(data["odb"])}" download class="btn quiet">Download ODB</a>' if data.get('odb') else ''
    project_status = data.get('status', 'unknown')
    html_text = f'''<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(data['name'])}</title>
    <meta http-equiv="refresh" content="60">
    <style>
    :root{{--bg:#f6f7fb;--panel:#ffffff;--text:#111827;--muted:#6b7280;--line:#e5e7eb;--blue:#2563eb;--blue2:#1d4ed8;--shadow:0 10px 30px rgba(15,23,42,.06)}}
    body{{font-family:Arial,sans-serif;max-width:1240px;margin:24px auto;padding:0 16px;background:var(--bg);color:var(--text)}}
    .topbar{{display:flex;justify-content:space-between;align-items:center;margin-bottom:18px}}
    .muted{{color:var(--muted)}}
    .card{{border:1px solid var(--line);border-radius:18px;padding:18px;margin:16px 0;background:var(--panel);box-shadow:var(--shadow)}}
    .hero{{display:flex;justify-content:space-between;align-items:end;gap:16px}}
    .hero h1{{margin:0 0 6px 0;font-size:32px}}
    .actions{{display:flex;gap:10px;flex-wrap:wrap}}
    .btn{{display:inline-block;padding:11px 15px;border-radius:12px;text-decoration:none;font-weight:600;border:1px solid transparent}}
    .btn.primary{{background:linear-gradient(135deg,var(--blue),var(--blue2));color:white}}
    .btn.dark{{background:#111827;color:white}}
    .btn.quiet{{background:#eef2f7;color:#111827;border-color:#d8dee8}}
    code{{background:#f3f4f6;padding:2px 6px;border-radius:6px}}
    pre{{background:#0f172a;color:#e5e7eb;padding:14px;border-radius:14px;white-space:pre-wrap;word-wrap:break-word;word-break:break-all;overflow-x:auto;max-width:100%}}
    td,th{{padding:9px 10px;border-top:1px solid #edf0f4;vertical-align:top;text-align:left}}
    .metric-table,.stage-table{{width:100%;border-collapse:collapse}}
    .grid{{display:grid;grid-template-columns:1.15fr 1fr;gap:16px}}
    .grid2{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
    @media (max-width:900px){{.grid,.grid2{{grid-template-columns:1fr}}}}
    @media (max-width:600px){{body{{margin:0;padding:0}} .card{{border-radius:0;margin:0;border-left:0;border-right:0}} .hero{{padding:16px}} h1{{font-size:24px}} .metric-row{{grid-template-columns:1fr}}}}
    @media (max-width: 900px){{.grid,.grid2{{grid-template-columns:1fr}} .hero{{display:block}} .actions{{margin-top:12px}}}}
    @media (max-width: 600px){{body{{margin:0;padding:0}} .card{{border-radius:0;margin:0;border-left:0;border-right:0}} .hero{{padding:16px}} h1{{font-size:24px}} .metric-row{{grid-template-columns:1fr}}}}
    .status{{display:inline-block;padding:4px 10px;border-radius:999px;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.02em}}
    .status.done,.status.pass{{background:#dcfce7;color:#166534}}
    .status.started,.status.running{{background:#fef3c7;color:#92400e}}
    .status.fail{{background:#fee2e2;color:#991b1b}}
    .status.unknown{{background:#e5e7eb;color:#374151}}
    .detail-group{{border:1px solid #e8ecf2;border-radius:14px;padding:0 14px;margin:12px 0;background:#fbfcfe}}
    .detail-group summary{{cursor:pointer;list-style:none;padding:14px 0;font-weight:700;text-transform:capitalize}}
    .detail-group summary::-webkit-details-marker{{display:none}}
    ul{{margin:0;padding-left:18px}}
    img{{display:block}}
    @media (max-width: 900px){{.grid,.grid2{{grid-template-columns:1fr}} .hero,.topbar{{display:block}} .actions{{margin-top:12px}}}}
    </style></head><body>
    <div class="topbar"><a href="index.html" class="muted">← Back to dashboard</a><div class="muted">Auto-refresh every 60s</div></div>
    <div class="card hero"><div><div class="status {html.escape(project_status)}">{html.escape(project_status)}</div><h1>{html.escape(data['name'])}</h1><div class="muted">Project detail page with PPA, logs, artifacts, and output downloads.</div></div><div class="actions">{gds_link}{def_link}{odb_link}</div></div>
    <div class="card"><p><strong>Latest run:</strong> <code>{html.escape(fmt(data.get('latest_run')))}</code></p><p><strong>GDS:</strong> <code>{html.escape(fmt(data.get('gds')))}</code></p></div>
    <div class="grid"><div class="card"><h2>Preview</h2>{preview_html}</div><div class="card"><h2>PPA brief</h2><table class="metric-table">{ppa_rows}</table></div></div>
    <div class="grid2"><div class="card"><h2>Spec</h2><details class="detail-group" open><summary>Raw spec</summary><pre>{html.escape(data.get('raw_spec','No raw spec'))}</pre></details><details class="detail-group" open><summary>Normalized spec</summary><pre>{html.escape(data.get('normalized_spec','No normalized spec'))}</pre></details></div><div class="card"><h2>Progress</h2>{grouped_stages}</div></div>
    <div class="grid2"><div class="card"><h2>Artifacts</h2><ul>{artifacts}</ul></div><div class="card"><h2>flow.log tail</h2><pre>{html.escape(flow_tail)}</pre></div></div>
    <div class="grid2"><div class="card"><h2>Diagnosis</h2><p><strong>Kind:</strong> <code>{html.escape(diagnosis.get('kind','-'))}</code></p><p><strong>Summary:</strong> {html.escape(diagnosis.get('summary','-'))}</p><p><strong>Suggestion:</strong> {html.escape(diagnosis.get('suggestion','-'))}</p></div><div class="card"><h2>Run history</h2><table class="metric-table"><tr><th>Run</th><th>Status</th><th>Util</th><th>Setup WNS</th><th>Power</th></tr>{history_rows}</table></div></div>
    <div class="card"><h2>Run compare</h2><p><strong>Baseline:</strong> <code>{html.escape((baseline.get('run') if baseline else '-') or '-')}</code> &nbsp; <strong>Current:</strong> <code>{html.escape((current.get('run') if current else '-') or '-')}</code></p><table class="metric-table"><tr><th>Metric</th><th>Baseline</th><th>Current</th><th>Delta</th></tr>{compare_rows}</table></div>
    <div class="card"><h2>warning.log tail</h2><pre>{html.escape(warn_tail)}</pre></div>
    <div class="card"><h2>Summary</h2><pre>{html.escape(json.dumps(data.get('ppa',{}).get('summary',{}), indent=2, ensure_ascii=False))}</pre></div>
    <div class="card"><h2>PPA details</h2>{''.join(detail_blocks)}</div>
    </body></html>'''
    p.write_text(html_text, encoding='utf-8')


def main():
    import os
    projects = [p for p in BASE.iterdir() if p.is_dir() and not p.name.startswith('_')]
    data = []
    for p in projects:
        d = collect_project(p)
        # Use directory modification time for sorting
        mtime = os.path.getmtime(p)
        d['_mtime'] = mtime
        data.append(d)
    
    # Sort by mtime descending (newest first)
    data.sort(key=lambda x: x['_mtime'], reverse=True)
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for d in data:
        preview = f'<a href="{html.escape(d["name"])}.html">open</a>'
        gds_download = f'<a href="../{html.escape(d["gds"])}" download>download</a>' if d.get('gds') else '-'
        summary = d.get('ppa', {}).get('summary', {})
        util = summary.get('area', {}).get('utilization')
        wns = summary.get('timing', {}).get('setup_wns')
        power = summary.get('power', {}).get('total')
        timestamp = d.get('timestamp') or '-'
        rows.append(f'<tr><td><a href="{html.escape(d["name"])}.html">{html.escape(d["name"])}</a></td><td><code>{html.escape(timestamp)}</code></td><td><code>{html.escape(fmt(d.get("latest_run")))}</code></td><td><code>{html.escape(fmt(util))}</code></td><td><code>{html.escape(fmt(wns))}</code></td><td><code>{html.escape(fmt(power))}</code></td><td>{gds_download}</td><td>{preview}</td></tr>')
        render_project_page(d)
    cards = []
    for d in data:
        summary = d.get('ppa', {}).get('summary', {})
        util = summary.get('area', {}).get('utilization')
        wns = summary.get('timing', {}).get('setup_wns')
        power = summary.get('power', {}).get('total')
        status = d.get('status', 'unknown')
        spec_brief = d.get('raw_spec_brief') or d.get('spec_desc') or 'No spec summary'
        top_module = d.get('top_module') or '-'
        gds_link = f'<a class="mini-btn" href="../{html.escape(d["gds"])}" download>Download GDS</a>' if d.get('gds') else '<span class="muted">No GDS</span>'
        preview = f'<img src="../{html.escape(d["preview"])}" alt="preview">' if d.get('preview') else '<div class="preview-empty">No preview</div>'
        cards.append(
            '<div class="project-card">'
            f'<div class="preview-wrap">{preview}</div>'
            f'<div class="project-head"><div><div class="status {html.escape(status)}">{html.escape(status)}</div><h3><a href="{html.escape(d["name"])}.html">{html.escape(d["name"])}</a></h3><div class="muted small">{html.escape(fmt(d.get("latest_run")))}</div><div class="muted small" style="margin-top:6px">{html.escape(spec_brief)}</div><div class="muted small">top module: <code>{html.escape(top_module)}</code></div></a></h3><div class="muted small">{html.escape(fmt(d.get("latest_run")))}</div></div><a class="detail-link" href="{html.escape(d["name"])}.html">Open</a></div>'
            '<div class="metric-row">'
            f'<div class="metric"><span>Utilization</span><strong>{html.escape(fmt(util))}</strong></div>'
            f'<div class="metric"><span>Setup WNS</span><strong>{html.escape(fmt(wns))}</strong></div>'
            f'<div class="metric"><span>Total Power</span><strong>{html.escape(fmt(power))}</strong></div>'
            '</div>'
            f'<div class="card-actions">{gds_link}</div>'
            '</div>'
        )
    index = OUT / 'index.html'
    html_text = '<!doctype html><html><head><meta charset="utf-8"><title>EDA Dashboard</title><meta http-equiv="refresh" content="60"><style>:root{--bg:#f6f7fb;--panel:#fff;--text:#111827;--muted:#6b7280;--line:#e5e7eb;--shadow:0 12px 32px rgba(15,23,42,.07);--blue:#2563eb;--blue-soft:#eef2ff}body{font-family:Arial,sans-serif;max-width:1280px;margin:24px auto;padding:0 16px;background:var(--bg);color:var(--text)}.hero{display:flex;justify-content:space-between;align-items:end;gap:16px}.muted{color:var(--muted)}.small{font-size:12px}.card{border:1px solid var(--line);background:var(--panel);border-radius:18px;padding:18px;margin:16px 0;box-shadow:var(--shadow)}.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:16px 0}.kpi{background:white;border:1px solid var(--line);border-radius:18px;padding:16px;box-shadow:var(--shadow)}.kpi .label{font-size:12px;color:var(--muted)}.kpi .value{font-size:28px;font-weight:700;margin-top:8px}.projects{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin-top:18px}.project-card{background:white;border:1px solid var(--line);border-radius:20px;overflow:hidden;box-shadow:var(--shadow)}.preview-wrap{aspect-ratio:16/9;background:linear-gradient(180deg,#f8fafc,#eef2f7);display:flex;align-items:center;justify-content:center;border-bottom:1px solid var(--line)}.preview-wrap img{width:100%;height:100%;object-fit:contain}.preview-empty{color:var(--muted)}.project-head{display:flex;justify-content:space-between;gap:12px;padding:16px 16px 8px 16px;align-items:start}.project-head h3{margin:8px 0 6px 0;font-size:20px}.project-head a{text-decoration:none;color:inherit}.detail-link,.mini-btn{display:inline-block;padding:9px 12px;border-radius:10px;text-decoration:none;font-weight:600}.detail-link{background:var(--blue-soft);color:#1d4ed8}.mini-btn{background:#111827;color:#fff}.metric-row{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;padding:0 16px 16px 16px}.metric{border:1px solid var(--line);background:#fafbfc;border-radius:14px;padding:12px}.metric span{display:block;font-size:12px;color:var(--muted);margin-bottom:6px}.metric strong{font-size:18px}.card-actions{padding:0 16px 16px 16px}.section-title{margin:24px 0 8px 0;font-size:18px}.status{display:inline-block;padding:4px 10px;border-radius:999px;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.02em}.status.done,.status.pass{background:#dcfce7;color:#166534}.status.started,.status.running{background:#fef3c7;color:#92400e}.status.fail{background:#fee2e2;color:#991b1b}.status.unknown{background:#e5e7eb;color:#374151}@media (max-width:1000px){.projects{grid-template-columns:1fr}.kpis{grid-template-columns:1fr 1fr}.hero{display:block}}</style></head><body><div class="hero"><div><h1>EDA Multi-Project Dashboard</h1><p class="muted">Overview of active demo projects, latest runs, top-line PPA, and downloadable outputs.</p></div><div class="muted">Auto-refresh every 60s</div></div><div class="kpis"><div class="kpi"><div class="label">Projects</div><div class="value">' + str(len(data)) + '</div></div><div class="kpi"><div class="label">Runs with GDS</div><div class="value">' + str(sum(1 for d in data if d.get('gds'))) + '</div></div><div class="kpi"><div class="label">Detail Pages</div><div class="value">' + str(len(data)) + '</div></div><div class="kpi"><div class="label">Dashboard</div><div class="value">MVP</div></div></div><div class="section-title">Projects (sorted by time, newest first)</div><div class="projects">' + ''.join(cards) + '</div></body></html>'
    index.write_text(html_text, encoding='utf-8')
    print(index)


if __name__ == '__main__':
    main()

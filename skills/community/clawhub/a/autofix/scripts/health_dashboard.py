#!/usr/bin/env python3
"""
health_dashboard.py — Autofix v6.0-M4: Interactive Health Dashboard

Generates an interactive HTML dashboard from the unified diagnosis report,
designed for rendering via OpenClaw Canvas.

Two modes:
  1. generate — collect diagnosis data + render HTML (default)
  2. serve    — write HTML to a known path for Canvas embedding

Usage:
    python scripts/health_dashboard.py                          # Generate + print HTML
    python scripts/health_dashboard.py --file path/to/output.html  # Write to file
    python scripts/health_dashboard.py --canvas                 # Generate + stage for Canvas

Design theme: 极简野蛮 (Brutalist Minimalism)
- High-contrast, no gradients
- Monospace-primary, bold borders
- Severity-coded left-edge indicators
"""

import json
import os
import subprocess
import sys
import textwrap
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────

HOME_DIR = Path.home()
SKILL_DIR = HOME_DIR / ".openclaw" / "workspace" / "skills" / "autofix"
SCRIPTS_DIR = SKILL_DIR / "scripts"
CANVAS_DIR = HOME_DIR / ".openclaw" / "canvas" / "documents"
BASELINE_FILE = SCRIPTS_DIR / "diagnosis_baseline.json"

SEV_EMOJI = {"🔴": "CRIT", "🟠": "HIGH", "🟡": "MED", "🟢": "OK"}
SEV_COLOR = {"🔴": "#d32f2f", "🟠": "#f57c00", "🟡": "#fbc02d", "🟢": "#388e3c"}


def collect_diagnosis_data() -> dict:
    """Run diagnosis_formatter.py and collect structured data."""
    formatter = SCRIPTS_DIR / "diagnosis_formatter.py"
    if not formatter.exists():
        return {"error": "diagnosis_formatter.py not found"}

    try:
        r = subprocess.run(
            [sys.executable, str(formatter), "--json"],
            capture_output=True, text=True, timeout=150,
        )
        stdout = r.stdout.strip()
        json_start = stdout.find("{")
        if json_start < 0:
            return {"error": f"No JSON in output: {stdout[:300]}"}
        return json.loads(stdout[json_start:])
    except json.JSONDecodeError as e:
        return {"error": f"JSON parse error: {e}"}
    except subprocess.TimeoutExpired:
        return {"error": "Timeout collecting diagnosis data"}
    except Exception as e:
        return {"error": str(e)}


def load_baseline_summary() -> dict:
    """Load baseline timestamp and overall severity for comparison."""
    if not BASELINE_FILE.exists():
        return {}
    try:
        with open(BASELINE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def generate_html(data: dict) -> str:
    """Generate a brutalist-minimalist HTML dashboard."""
    if "error" in data:
        return f"<h1>❌ Error</h1><pre>{data['error']}</pre>"

    summary = data.get("summary", {})
    overall = data.get("overall_severity", "🟢")
    items = data.get("items", [])
    errors = data.get("errors", [])
    version = data.get("version", "6.0-M4")
    timestamp = data.get("timestamp", datetime.now().isoformat())

    overall_color = SEV_COLOR.get(overall, "#666")

    # Build category groups
    categories = {}
    for item in items:
        cat = item.get("category", "其他")
        if cat not in categories:
            categories[cat] = {"🔴": 0, "🟠": 0, "🟡": 0, "🟢": 0, "items": []}
        s = item.get("severity", "🟢")
        if s in categories[cat]:
            categories[cat][s] += 1
        categories[cat]["items"].append(item)

    # Sort categories by worst item
    cat_order = sorted(categories.keys(),
                       key=lambda c: min(
                           (SEV_EMOJI.get(it.get("severity", "🟢"), "OK")
                            for it in categories[c]["items"]),
                           key=lambda x: {"CRIT": 0, "HIGH": 1, "MED": 2, "OK": 3}.get(x, 3)))

    # Build severity bar data
    total = sum(summary.values())
    bar_html = ""
    if total > 0:
        for s, name in [("🔴", "CRIT"), ("🟠", "HIGH"), ("🟡", "MED"), ("🟢", "OK")]:
            count = summary.get(s, 0)
            pct = (count / total) * 100 if total > 0 else 0
            color = SEV_COLOR.get(s, "#666")
            if count > 0:
                bar_html += (f'<div style="background:{color};width:{pct}%;'
                             f'min-width:30px;text-align:center;color:white;'
                             f'font-size:13px;font-weight:700;padding:6px 0;">'
                             f'{name} {count}</div>')

    # Build items HTML grouped by category
    items_html = ""
    for cat in cat_order:
        cat_data = categories[cat]
        cat_sev = "🟢"
        for s in ["🔴", "🟠", "🟡"]:
            if cat_data[s] > 0:
                cat_sev = s
                break
        cat_color = SEV_COLOR.get(cat_sev, "#666")
        worst_count = sum(1 for it in cat_data["items"]
                          if it.get("severity") in ("🔴", "🟠"))

        items_html += f'''
        <div style="margin:16px 0;background:white;border-left:4px solid {cat_color};
                    box-shadow:0 1px 3px rgba(0,0,0,0.08);border-radius:4px;">
          <div style="padding:12px 16px;display:flex;justify-content:space-between;
                      align-items:center;border-bottom:1px solid #eee;
                      font-weight:600;font-size:15px;">
            <span>{cat}</span>
            <span style="font-size:13px;color:#888;">
              🔴{cat_data["🔴"]} 🟠{cat_data["🟠"]} 🟡{cat_data["🟡"]} 🟢{cat_data["🟢"]}
            </span>
          </div>
          <div style="padding:4px 0;">'''

        for item in cat_data["items"]:
            s = item.get("severity", "🟢")
            title = item.get("title", "")
            detail = item.get("detail", "")
            suggestion = item.get("suggestion", "")
            color = SEV_COLOR.get(s, "#666")
            sev_label = SEV_EMOJI.get(s, "?")

            items_html += f'''
            <div style="padding:10px 16px;border-bottom:1px solid #f0f0f0;
                        display:flex;align-items:flex-start;gap:10px;">
              <span style="background:{color};color:white;font-size:11px;
                          font-weight:700;padding:2px 6px;border-radius:3px;
                          white-space:nowrap;margin-top:2px;">{sev_label}</span>
              <div style="flex:1;min-width:0;">
                <div style="font-size:14px;font-weight:500;color:#333;
                            white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{title[:100]}</div>'''

            if detail and detail != title:
                # Truncate detail
                d = detail[:150] + "..." if len(detail) > 150 else detail
                items_html += f'<div style="font-size:12px;color:#888;margin-top:2px;">{d}</div>'

            if suggestion:
                items_html += (f'<div style="font-size:12px;color:{color};'
                              f'margin-top:3px;">💡 {suggestion[:120]}</div>')

            items_html += '</div></div>'

        items_html += '</div></div>'

    # Build suggestion list
    suggestions = [it for it in items if it.get("suggestion")]
    suggestions_html = ""
    for sug in suggestions:
        s = sug.get("severity", "🟡")
        color = SEV_COLOR.get(s, "#666")
        suggestions_html += (f'<div style="padding:8px 12px;margin:4px 0;'
                            f'border-left:3px solid {color};background:#fafafa;'
                            f'font-size:13px;">'
                            f'<strong style="color:{color};">{SEV_EMOJI.get(s)}</strong> '
                            f'{sug["suggestion"][:150]}</div>')

    # Error messages
    errors_html = ""
    for err in errors:
        errors_html += f'<div style="padding:8px;color:#d32f2f;">❌ {err}</div>'

    # Baseline comparison info
    baseline_info = ""
    baseline = load_baseline_summary()
    if baseline:
        b_sev = baseline.get("overall_severity", "")
        b_time = baseline.get("timestamp", "")[:16].replace("T", " ")
        if b_sev:
            b_color = SEV_COLOR.get(b_sev, "#666")
            baseline_info = (f'<div style="padding:12px;border:2px dashed {b_color};'
                            f'border-radius:4px;margin:16px 0;font-size:13px;">'
                            f'📋 基线对比: 上次 {b_sev} (保存于 {b_time})<br>'
                            f'当前 {overall} | '
                            f'运行 <code>--compare</code> 查看详细变化</div>')

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OpenClaw 健康仪表盘</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:'JetBrains Mono','SF Mono',monospace; background:#1a1a2e; color:#e0e0e0; padding:20px; }}
  .card {{ background:#16213e; border-radius:6px; padding:20px; margin:16px 0; }}
  .sev-dot {{ display:inline-block; width:12px; height:12px; border-radius:50%; margin-right:6px; }}
  code {{ background:#0f3460; padding:2px 6px; border-radius:3px; font-size:12px; }}
  .item {{ transition:background 0.15s; }}
  .item:hover {{ background:rgba(255,255,255,0.04); }}
</style>
</head>
<body>

<!-- Header -->
<div class="card" style="display:flex;justify-content:space-between;align-items:center;border-bottom:3px solid {overall_color};">
  <div>
    <div style="font-size:24px;font-weight:700;">🔬 OpenClaw Health</div>
    <div style="font-size:12px;color:#888;">{timestamp[:16].replace('T',' ')} · v{version}</div>
  </div>
  <div style="text-align:right;">
    <div style="font-size:36px;font-weight:700;color:{overall_color};">{overall}</div>
    <div style="font-size:12px;color:#888;">OVERALL</div>
  </div>
</div>

<!-- Summary Bar -->
<div class="card" style="padding:12px 20px;">
  <div style="display:flex;gap:0;border-radius:4px;overflow:hidden;">
    {bar_html}
  </div>
  <div style="display:flex;justify-content:space-between;margin-top:8px;font-size:12px;color:#888;">
    <span>共 {total} 项检测</span>
    <span>🔴 {summary.get('🔴',0)} · 🟠 {summary.get('🟠',0)} · 🟡 {summary.get('🟡',0)} · 🟢 {summary.get('🟢',0)}</span>
  </div>
</div>

<!-- Baseline -->
{baseline_info}

<!-- Suggestions -->
<div class="card">
  <div style="font-size:14px;font-weight:700;margin-bottom:10px;">📋 建议操作</div>
  {suggestions_html if suggestions_html else '<div style="color:#888;font-size:13px;">✅ 无待处理建议</div>'}
</div>

<!-- Categories -->
<div class="card">
  <div style="font-size:14px;font-weight:700;margin-bottom:10px;">📊 分类详情</div>
  {items_html}
</div>

<!-- Errors -->
{'' if not errors_html else f'<div class="card"><div style="font-size:14px;font-weight:700;margin-bottom:10px;">⚠️ 诊断错误</div>{errors_html}</div>'}

<!-- Footer -->
<div style="text-align:center;padding:12px;font-size:11px;color:#555;">
  autofix v{version} · 来源: openclaw doctor + runtime_health_check + api_key_validator<br>
  <code>cd ~/.openclaw/workspace/skills/autofix && python scripts/diagnosis_formatter.py</code>
</div>

</body>
</html>'''
    return html


def write_html(html: str, filepath: str = None) -> str:
    """Write HTML to file, return the path."""
    if not filepath:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = str(CANVAS_DIR / f"health_dashboard_{ts}" / "index.html")

    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    return str(path)


def stage_for_canvas(html: str) -> str:
    """Write to a stable Canvas path for embedding."""
    canvas_path = CANVAS_DIR / "health_dashboard" / "index.html"
    canvas_path.parent.mkdir(parents=True, exist_ok=True)
    canvas_path.write_text(html, encoding="utf-8")
    return str(canvas_path)


def main():
    # Collect data
    data = collect_diagnosis_data()

    # Generate HTML
    html = generate_html(data)

    # Determine output mode
    if "--canvas" in sys.argv or "--embed" in sys.argv:
        path = stage_for_canvas(html)
        print(f"✅ Dashboard staged: {path}")
        print(f"   Canvas ref: health_dashboard")
        print(f"   URL: /__openclaw__/canvas/documents/health_dashboard/index.html")
    elif "--file" in sys.argv:
        idx = sys.argv.index("--file")
        if idx + 1 < len(sys.argv):
            path = write_html(html, sys.argv[idx + 1])
            print(f"✅ Dashboard written: {path}")
    else:
        # Print HTML to stdout (pipe to file or canvas)
        print(html)


if __name__ == "__main__":
    main()

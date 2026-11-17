#!/usr/bin/env python3
"""Render a lightweight ClawVision Lite HTML summary. English-only, no extras."""

import argparse
import json
import sys
from pathlib import Path

PRESET = {
    "font_family": "Inter",
    "title_size": "22px",
    "radius": "14px",
    "shadow": "0 2px 8px rgba(0,0,0,.08)",
    "bg": "#f5f6f8",
    "card": "#ffffff",
    "text": "#1a1a1a",
    "muted": "#666666",
    "accent": "#2a9df4",
    "green": "#4cd964",
    "orange": "#ff9500",
    "red": "#ff3b30",
    "border": "#e5e7eb",
    "card_alt": "#f8f9fa",
}


def _hex6(c: str) -> str:
    c = c.lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    return c


def _rgb(c: str) -> str:
    h = _hex6(c)
    return f"{int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)}"


def _css() -> str:
    p = PRESET
    rgb = _rgb(p["accent"])
    return f"""
:root{{--bg:{p['bg']};--card:{p['card']};--text:{p['text']};--muted:{p['muted']};--accent:{p['accent']};--accent-rgb:{rgb};--green:{p['green']};--orange:{p['orange']};--red:{p['red']};--border:{p['border']};--card-bg-alt:{p['card_alt']};--radius:{p['radius']};--shadow:{p['shadow']}}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:{p['font_family']},-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;background:var(--bg);color:var(--text);line-height:1.45}}
.wrap{{max-width:820px;margin:0 auto;padding:24px}}
header{{margin-bottom:20px}}
header h1{{font-size:{p['title_size']};font-weight:800;margin:0 0 6px;letter-spacing:-0.5px}}
header p{{color:var(--muted);margin:0;font-size:15px}}
.badge{{display:inline-block;background:rgba(var(--accent-rgb),.12);color:var(--accent);font-size:12px;font-weight:700;padding:5px 12px;border-radius:14px;margin-bottom:14px;letter-spacing:.5px;text-transform:uppercase}}
.tabs{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:20px}}
.tab{{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:9px 15px;font-size:13px;cursor:pointer;transition:.15s}}
.tab.active{{background:var(--accent);color:#fff;border-color:var(--accent)}}
.panel{{display:none;background:var(--card);border-radius:var(--radius);padding:22px;box-shadow:var(--shadow)}}
.panel.active{{display:block;min-height:420px}}
.lead{{color:var(--muted);font-size:16px;margin-bottom:18px;line-height:1.5}}
.flow{{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:16px 0}}
.flow-item{{background:var(--card-bg-alt);border:1px solid var(--border);border-radius:var(--radius);padding:12px 16px;min-width:110px;text-align:center}}
.flow-item strong{{display:block;font-size:14px;margin-bottom:3px}}
.flow-item small{{color:var(--muted);font-size:12px}}
.arrow{{color:var(--muted);font-size:18px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-top:14px}}
.card{{background:var(--card-bg-alt);border-radius:var(--radius);padding:16px}}
.card h3{{margin:0 0 6px;font-size:17px;color:var(--accent)}}
.card p{{margin:0;color:var(--muted);font-size:13px}}
.checklist{{margin:0;padding:0;list-style:none}}
.checklist li{{display:flex;justify-content:space-between;align-items:center;padding:12px 0;border-bottom:1px solid var(--border);font-size:14px}}
.checklist li:last-child{{border-bottom:none}}
.status{{font-size:12px;font-weight:700;color:var(--green);background:rgba(76,217,100,.12);padding:3px 10px;border-radius:10px}}
.status.pending{{color:var(--orange);background:rgba(255,149,0,.12)}}
.status.blocked{{color:var(--red);background:rgba(255,59,48,.12)}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
ul.clean{{padding-left:18px;margin:0}}
ul.clean li{{margin-bottom:6px;font-size:13px}}
@media(max-width:600px){{.two{{grid-template-columns:1fr}}}}
"""


def _h(text: str) -> str:
    return (
        (text or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render_html(summary: dict) -> str:
    title = _h(summary.get("title", "ClawVision Lite summary"))
    subtitle = _h(summary.get("subtitle", ""))
    main_takeaway = _h(summary.get("main_takeaway", ""))
    format_takeaway = _h(summary.get("format_takeaway", ""))
    next_takeaway = _h(summary.get("next_takeaway", ""))

    flow_items = ""
    for item in summary.get("flow", []):
        label = item.get("label", "")
        sub = item.get("sub", "")
        if label in ("→", "->"):
            flow_items += f'<div class="arrow">{_h(label)}</div>\n'
        else:
            flow_items += f'<div class="flow-item"><strong>{_h(label)}</strong><small>{_h(sub)}</small></div>\n'

    metric_cards = ""
    for m in summary.get("metrics", []):
        metric_cards += f'<div class="card"><h3>{_h(m.get("title", ""))}</h3><p>{_h(m.get("text", ""))}</p></div>\n'

    dos = "".join(f"<li>{_h(d)}</li>\n" for d in summary.get("dos", []))
    donts = "".join(f"<li>{_h(d)}</li>\n" for d in summary.get("donts", []))

    checklist = ""
    for c in summary.get("checklist", []):
        status = c.get("status", "pending")
        checklist += f'<li>{_h(c.get("text", ""))} <span class="status {status}">{_h(status)}</span></li>\n'

    next_steps = "".join(f"<li>{_h(s)}</li>\n" for s in summary.get("next_steps", []))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>{_css()}</style>
</head>
<body>
<div class="wrap">
  <span class="badge">ClawVision Lite · Summary</span>
  <header>
    <h1>{title}</h1>
    <p>{subtitle}</p>
  </header>
  <div class="tabs">
    <div class="tab active" data-tab="main">Main takeaway</div>
    <div class="tab" data-tab="format">Format</div>
    <div class="tab" data-tab="built">What we built</div>
    <div class="tab" data-tab="next">Next steps</div>
  </div>
  <div id="main" class="panel active">
    <p class="lead">{main_takeaway}</p>
    <div class="flow">{flow_items}</div>
    <div class="grid">{metric_cards}</div>
  </div>
  <div id="format" class="panel">
    <p class="lead">{format_takeaway}</p>
    <div class="two">
      <div class="card"><h3>Do</h3><ul class="clean">{dos}</ul></div>
      <div class="card"><h3>Don't</h3><ul class="clean">{donts}</ul></div>
    </div>
  </div>
  <div id="built" class="panel">
    <ul class="checklist">{checklist}</ul>
  </div>
  <div id="next" class="panel">
    <p class="lead">{next_takeaway}</p>
    <ul class="clean">{next_steps}</ul>
  </div>
</div>
<script>
document.querySelectorAll('.tab').forEach(t => t.addEventListener('click', () => {{
  document.querySelectorAll('.tab').forEach(x => x.classList.remove('active'));
  document.querySelectorAll('.panel').forEach(x => x.classList.remove('active'));
  t.classList.add('active');
  document.getElementById(t.dataset.tab).classList.add('active');
}}));
</script>
</body>
</html>"""
    return html


def main():
    parser = argparse.ArgumentParser(description="Render ClawVision Lite HTML summary.")
    parser.add_argument("--summary", "-s", default="-", help="Path to JSON summary or - for stdin")
    parser.add_argument("--output", "-o", required=True, help="Output directory")
    parser.add_argument("--slug", help="Output slug (default: derived from title)")
    args = parser.parse_args()

    if args.summary == "-":
        raw = sys.stdin.read()
    else:
        raw = Path(args.summary).read_text(encoding="utf-8")
    summary = json.loads(raw)

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    title = summary.get("title", "summary")
    slug = args.slug or "".join(c if c.isalnum() else "-" for c in title).strip("-").lower() or "summary"

    html_path = out_dir / f"{slug}.html"
    html_path.write_text(render_html(summary), encoding="utf-8")
    print(f"HTML: {html_path}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Render a conversation summary as a self-contained HTML card + PNG."""

import argparse
import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


TEMPLATE = r"""<!DOCTYPE html>
<html lang="{{lang}}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{title}}</title>
<style>
:root{--bg:#f5f6f8;--card:#fff;--text:#1a1a1a;--muted:#666;--accent:#2a9df4;--green:#4cd964;--orange:#ff9500;--red:#ff3b30;--border:#e5e7eb;}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;background:var(--bg);color:var(--text);line-height:1.45}
.wrap{max-width:760px;margin:0 auto;padding:20px}
header{margin-bottom:18px}
header h1{font-size:22px;font-weight:700;margin:0 0 4px}
header p{color:var(--muted);margin:0;font-size:14px}
.badge{display:inline-block;background:#eef6ff;color:var(--accent);font-size:12px;font-weight:600;padding:4px 10px;border-radius:12px;margin-bottom:12px}
.tabs{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:18px}
.tab{background:var(--card);border:1px solid var(--border);border-radius:20px;padding:8px 14px;font-size:13px;cursor:pointer;transition:.15s}
.tab.active{background:var(--accent);color:#fff;border-color:var(--accent)}
.panel{display:none;background:var(--card);border-radius:16px;padding:18px;box-shadow:0 2px 8px rgba(0,0,0,.04)}
.panel.active{display:block}
.lead{color:var(--muted);font-size:15px;margin-bottom:16px}
.flow{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:16px 0}
.flow-item{background:#f8f9fa;border:1px solid var(--border);border-radius:12px;padding:10px 14px;min-width:110px;text-align:center}
.flow-item strong{display:block;font-size:14px;margin-bottom:2px}
.flow-item small{color:var(--muted);font-size:12px}
.arrow{color:var(--muted);font-size:18px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-top:12px}
.card{background:#f8f9fa;border-radius:14px;padding:14px}
.card h3{margin:0 0 6px;font-size:16px}
.card p{margin:0;color:var(--muted);font-size:13px}
.checklist{margin:0;padding:0;list-style:none}
.checklist li{display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid var(--border);font-size:14px}
.checklist li:last-child{border-bottom:none}
.status{font-size:12px;font-weight:600;color:var(--green)}
.status.pending{color:var(--orange)}
.status.blocked{color:var(--red)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:12px}
ul.clean{padding-left:18px;margin:0}
ul.clean li{margin-bottom:6px;font-size:13px}
@media(max-width:600px){.two{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="wrap">
  <span class="badge">OpenClaw · Conversation summary</span>
  <header>
    <h1>{{title}}</h1>
    <p>{{subtitle}}</p>
  </header>

  <div class="tabs">
    <div class="tab active" data-tab="main">{{tab_main}}</div>
    <div class="tab" data-tab="format">{{tab_format}}</div>
    <div class="tab" data-tab="built">{{tab_built}}</div>
    <div class="tab" data-tab="next">{{tab_next}}</div>
  </div>

  <div id="main" class="panel active">
    <p class="lead">{{main_takeaway}}</p>
    <div class="flow">{{flow_items}}</div>
    <div class="grid">{{metric_cards}}</div>
  </div>

  <div id="format" class="panel">
    <p class="lead">{{format_takeaway}}</p>
    <div class="two">
      <div class="card">
        <h3>{{dos_title}}</h3>
        <ul class="clean">{{dos}}</ul>
      </div>
      <div class="card">
        <h3>{{donts_title}}</h3>
        <ul class="clean">{{donts}}</ul>
      </div>
    </div>
  </div>

  <div id="built" class="panel">
    <ul class="checklist">{{checklist}}</ul>
  </div>

  <div id="next" class="panel">
    <p class="lead">{{next_takeaway}}</p>
    <ul class="clean">{{next_steps}}</ul>
  </div>
</div>
<script>
document.querySelectorAll('.tab').forEach(t=>t.addEventListener('click',()=>{
  document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));
  document.querySelectorAll('.panel').forEach(x=>x.classList.remove('active'));
  t.classList.add('active');
  document.getElementById(t.dataset.tab).classList.add('active');
}));
</script>
</body>
</html>
"""


def _h(text: str) -> str:
    """Minimal HTML escape."""
    return (
        (text or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render_html(summary: dict, lang: str = "en") -> str:
    is_ru = lang.startswith("ru")
    tab_main = "Главный вывод" if is_ru else "Main takeaway"
    tab_format = "Формат" if is_ru else "Format"
    tab_built = "Что построено" if is_ru else "What we built"
    tab_next = "Что дальше" if is_ru else "Next steps"
    dos_title = "Do" if not is_ru else "Нормально"
    donts_title = "Don't" if not is_ru else "Риски"

    html = TEMPLATE
    html = html.replace("{{lang}}", _h(lang))
    html = html.replace("{{title}}", _h(summary.get("title", "Conversation summary")))
    html = html.replace("{{subtitle}}", _h(summary.get("subtitle", "")))
    html = html.replace("{{tab_main}}", tab_main)
    html = html.replace("{{tab_format}}", tab_format)
    html = html.replace("{{tab_built}}", tab_built)
    html = html.replace("{{tab_next}}", tab_next)
    html = html.replace("{{main_takeaway}}", _h(summary.get("main_takeaway", "")))
    html = html.replace("{{format_takeaway}}", _h(summary.get("format_takeaway", "")))
    html = html.replace("{{next_takeaway}}", _h(summary.get("next_takeaway", "")))
    html = html.replace("{{dos_title}}", dos_title)
    html = html.replace("{{donts_title}}", donts_title)

    flow_items = ""
    for item in summary.get("flow", []):
        label = item.get("label", "")
        sub = item.get("sub", "")
        if label in ("→", "->"):
            flow_items += f'<div class="arrow">{_h(label)}</div>\n'
        else:
            flow_items += (
                f'<div class="flow-item"><strong>{_h(label)}</strong>'
                f'<small>{_h(sub)}</small></div>\n'
            )
    html = html.replace("{{flow_items}}", flow_items)

    metric_cards = ""
    for m in summary.get("metrics", []):
        metric_cards += (
            f'<div class="card"><h3>{_h(m.get("title", ""))}</h3>'
            f'<p>{_h(m.get("text", ""))}</p></div>\n'
        )
    html = html.replace("{{metric_cards}}", metric_cards)

    dos = "".join(f"<li>{_h(d)}</li>\n" for d in summary.get("dos", []))
    html = html.replace("{{dos}}", dos)

    donts = "".join(f"<li>{_h(d)}</li>\n" for d in summary.get("donts", []))
    html = html.replace("{{donts}}", donts)

    checklist = ""
    for c in summary.get("checklist", []):
        status = c.get("status", "pending")
        checklist += (
            f'<li>{_h(c.get("text", ""))} '
            f'<span class="status {status}">{_h(status)}</span></li>\n'
        )
    html = html.replace("{{checklist}}", checklist)

    next_steps = "".join(f"<li>{_h(s)}</li>\n" for s in summary.get("next_steps", []))
    html = html.replace("{{next_steps}}", next_steps)

    return html


def screenshot_html(html_path: Path, png_path: Path, width: int = 900, height: int = 650):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": width, "height": height})
        page.goto(f"file:///{html_path.as_posix()}")
        page.screenshot(path=str(png_path), full_page=False)
        browser.close()


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", text) or "summary"


def main():
    parser = argparse.ArgumentParser(description="Render conversation summary visual.")
    parser.add_argument("--summary", "-s", help="Path to JSON summary or '-' for stdin")
    parser.add_argument("--output", "-o", required=True, help="Output directory")
    parser.add_argument("--slug", help="Output slug (default: derived from title)")
    parser.add_argument("--lang", default="en", help="Language code for UI labels")
    parser.add_argument("--png", action="store_true", help="Also render PNG screenshot")
    args = parser.parse_args()

    if args.summary == "-" or args.summary is None:
        raw = sys.stdin.read()
    else:
        raw = Path(args.summary).read_text(encoding="utf-8")

    summary = json.loads(raw)
    html = render_html(summary, lang=args.lang)

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    slug = args.slug or slugify(summary.get("title", "summary"))
    html_path = out_dir / f"{slug}.html"
    html_path.write_text(html, encoding="utf-8")

    result = {"html": str(html_path)}

    if args.png:
        png_path = out_dir / f"{slug}.png"
        screenshot_html(html_path, png_path)
        result["png"] = str(png_path)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

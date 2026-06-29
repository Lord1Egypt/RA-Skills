#!/usr/bin/env python3
"""Apple HIG-inspired visualization generator. Outputs PNG screenshots."""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import uuid


APPLE_COLORS = ["#007AFF", "#34C759", "#FF9500", "#FF3B30", "#AF52DE", "#5AC8FA", "#FFCC00"]


def css_base(dark: bool, width: int, height: int) -> str:
    bg = "#1C1C1E" if dark else "#F5F5F7"
    card_bg = "#2C2C2E" if dark else "#FFFFFF"
    text = "#F5F5F7" if dark else "#1D1D1F"
    sub = "#8E8E93" if dark else "#6E6E73"
    shadow = "none" if dark else "0 4px 20px rgba(0,0,0,0.08)"

    return f"""
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
    background: {bg};
    color: {text};
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", Arial, sans-serif;
    width: {width}px;
    min-height: {height}px;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 32px;
    gap: 24px;
}}
.title {{
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -0.3px;
    color: {text};
    align-self: flex-start;
}}
.card {{
    background: {card_bg};
    border-radius: 16px;
    padding: 28px 32px;
    box-shadow: {shadow};
    width: 100%;
}}
.sub {{ color: {sub}; font-size: 13px; font-weight: 500; }}
@keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: translateY(0); }} }}
.card {{ animation: fadeIn 300ms ease-out both; }}
svg text {{ font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", Arial, sans-serif; }}
"""


def build_bar_html(data: dict, title: str, dark: bool, width: int, height: int) -> str:
    labels = data.get("labels", [])
    values = data.get("values", [])
    unit = data.get("unit", "")
    if not labels or not values:
        raise ValueError("bar chart requires 'labels' and 'values'")

    max_val = max(values) if values else 1
    bar_area_h = max(height - 200, 200)
    bar_w = max(20, (width - 96) // max(len(values), 1) - 12)

    bars_svg = ""
    label_els = ""
    value_els = ""
    for i, (lbl, val) in enumerate(zip(labels, values)):
        color = APPLE_COLORS[i % len(APPLE_COLORS)]
        bar_h = int((val / max_val) * bar_area_h * 0.85)
        x = 48 + i * (bar_w + 12)
        y = bar_area_h - bar_h
        bars_svg += f"""
        <rect x="{x}" y="{bar_area_h}" width="{bar_w}" height="0" rx="6" fill="{color}" opacity="0.9">
          <animate attributeName="height" from="0" to="{bar_h}" dur="0.5s" begin="{i * 0.08}s" fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1"/>
          <animate attributeName="y" from="{bar_area_h}" to="{y}" dur="0.5s" begin="{i * 0.08}s" fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1"/>
        </rect>"""
        label_els += f'<text x="{x + bar_w // 2}" y="{bar_area_h + 20}" text-anchor="middle" font-size="12" fill="#8E8E93">{lbl}</text>'
        value_els += f'<text x="{x + bar_w // 2}" y="{y - 6}" text-anchor="middle" font-size="12" font-weight="600" fill="{"#F5F5F7" if dark else "#1D1D1F"}">{val}</text>'

    svg_w = 48 + len(values) * (bar_w + 12)
    unit_label = f'<text x="{svg_w - 10}" y="16" text-anchor="end" font-size="11" fill="#8E8E93">{unit}</text>' if unit else ""

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{css_base(dark, width, height)}
</style></head><body>
<div class="title">{title}</div>
<div class="card">
<svg width="{svg_w}" height="{bar_area_h + 30}" style="overflow:visible">
  {unit_label}
  {bars_svg}
  {label_els}
  {value_els}
</svg>
</div>
</body></html>"""


def build_line_html(data: dict, title: str, dark: bool, width: int, height: int) -> str:
    labels = data.get("labels", [])
    values = data.get("values", [])
    unit = data.get("unit", "")
    if not labels or not values:
        raise ValueError("line chart requires 'labels' and 'values'")

    chart_w = width - 96
    chart_h = max(height - 180, 180)
    min_v, max_v = min(values), max(values)
    rng = max_v - min_v or 1

    def px(i, v):
        x = int(i * chart_w / max(len(values) - 1, 1))
        y = int(chart_h - ((v - min_v) / rng) * chart_h * 0.85 - chart_h * 0.075)
        return x, y

    pts = [px(i, v) for i, v in enumerate(values)]

    # Smooth bezier path
    def bezier_path(pts):
        if len(pts) < 2:
            return f"M{pts[0][0]},{pts[0][1]}"
        d = f"M{pts[0][0]},{pts[0][1]}"
        for i in range(1, len(pts)):
            x0, y0 = pts[i - 1]
            x1, y1 = pts[i]
            cx = (x0 + x1) // 2
            d += f" C{cx},{y0} {cx},{y1} {x1},{y1}"
        return d

    path_d = bezier_path(pts)
    close_d = f" L{pts[-1][0]},{chart_h} L{pts[0][0]},{chart_h} Z"
    grad_id = "lineGrad"
    accent = APPLE_COLORS[0]

    circles = "".join(
        f'<circle cx="{x}" cy="{y}" r="4" fill="{accent}" opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="{0.5 + i * 0.05}s" fill="freeze"/>'
        f'</circle>'
        for i, (x, y) in enumerate(pts)
    )

    lbl_step = max(1, len(labels) // 6)
    x_labels = "".join(
        f'<text x="{pts[i][0]}" y="{chart_h + 18}" text-anchor="middle" font-size="11" fill="#8E8E93">{labels[i]}</text>'
        for i in range(0, len(labels), lbl_step)
    )

    dark_stop = "#1C1C1E" if dark else "#F5F5F7"
    unit_label = f'<text x="{chart_w}" y="-6" text-anchor="end" font-size="11" fill="#8E8E93">{unit}</text>' if unit else ""

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{css_base(dark, width, height)}
</style></head><body>
<div class="title">{title}</div>
<div class="card">
<svg width="{chart_w}" height="{chart_h + 28}" style="overflow:visible">
  <defs>
    <linearGradient id="{grad_id}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="{dark_stop}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="lineClip">
      <rect width="0" height="{chart_h + 10}">
        <animate attributeName="width" from="0" to="{chart_w}" dur="0.7s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1"/>
      </rect>
    </clipPath>
  </defs>
  {unit_label}
  <g clip-path="url(#lineClip)">
    <path d="{path_d}{close_d}" fill="url(#{grad_id})"/>
    <path d="{path_d}" fill="none" stroke="{accent}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  {circles}
  {x_labels}
</svg>
</div>
</body></html>"""


def build_donut_html(data: dict, title: str, dark: bool, width: int, height: int) -> str:
    segments = data.get("segments", [])
    if not segments:
        raise ValueError("donut chart requires 'segments'")

    total = sum(s.get("value", 0) for s in segments) or 1
    cx, cy = 140, 140
    r_outer, r_inner = 110, 68
    stroke_w = r_outer - r_inner

    def arc_path(start_angle, end_angle, ro, ri):
        import math
        sa, ea = math.radians(start_angle - 90), math.radians(end_angle - 90)
        laf = 1 if (end_angle - start_angle) > 180 else 0
        x1o, y1o = cx + ro * math.cos(sa), cy + ro * math.sin(sa)
        x2o, y2o = cx + ro * math.cos(ea), cy + ro * math.sin(ea)
        x1i, y1i = cx + ri * math.cos(ea), cy + ri * math.sin(ea)
        x2i, y2i = cx + ri * math.cos(sa), cy + ri * math.sin(sa)
        return f"M{x1o:.2f},{y1o:.2f} A{ro},{ro} 0 {laf},1 {x2o:.2f},{y2o:.2f} L{x1i:.2f},{y1i:.2f} A{ri},{ri} 0 {laf},0 {x2i:.2f},{y2i:.2f} Z"

    paths = ""
    legend = ""
    angle = 0
    for i, seg in enumerate(segments):
        val = seg.get("value", 0)
        color = seg.get("color") or APPLE_COLORS[i % len(APPLE_COLORS)]
        sweep = (val / total) * 360
        end_angle = angle + sweep - (1 if len(segments) > 1 else 0)
        p = arc_path(angle, end_angle, r_outer, r_inner)
        paths += f'<path d="{p}" fill="{color}" opacity="0.9"/>\n'
        angle += sweep
        pct = f"{val / total * 100:.1f}%"
        lbl_color = "#F5F5F7" if dark else "#1D1D1F"
        sub_color = "#8E8E93"
        legend += f"""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">
          <div style="width:10px;height:10px;border-radius:50%;background:{color};flex-shrink:0"></div>
          <div>
            <div style="font-size:14px;font-weight:600;color:{lbl_color}">{seg.get('label','')}</div>
            <div style="font-size:12px;color:{sub_color}">{val} · {pct}</div>
          </div>
        </div>"""

    text_color = "#F5F5F7" if dark else "#1D1D1F"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{css_base(dark, width, height)}
.donut-wrap {{ display:flex; align-items:center; gap:40px; }}
</style></head><body>
<div class="title">{title}</div>
<div class="card">
<div class="donut-wrap">
<svg width="{cx*2}" height="{cy*2}">
  {paths}
  <text x="{cx}" y="{cy - 6}" text-anchor="middle" font-size="28" font-weight="700" fill="{text_color}">{len(segments)}</text>
  <text x="{cx}" y="{cy + 18}" text-anchor="middle" font-size="13" fill="#8E8E93">segments</text>
</svg>
<div>{legend}</div>
</div>
</div>
</body></html>"""


def build_progress_html(data: dict, title: str, dark: bool, width: int, height: int) -> str:
    items = data.get("items", [])
    if not items:
        raise ValueError("progress chart requires 'items'")

    import math
    r = 52
    stroke_w = 10
    size = (r + stroke_w) * 2 + 4
    text_color = "#F5F5F7" if dark else "#1D1D1F"
    track_color = "#3A3A3C" if dark else "#E5E5EA"

    cards = ""
    for i, item in enumerate(items):
        val = item.get("value", 0)
        mx = item.get("max", 100) or 100
        color = item.get("color") or APPLE_COLORS[i % len(APPLE_COLORS)]
        pct = min(val / mx, 1.0)
        circ = 2 * math.pi * r
        dash = pct * circ
        gap = circ - dash
        rotate = -90
        label = item.get("label", "")
        val_str = str(val)
        unit = f"/{mx}" if mx != 100 else f"{int(pct*100)}%"

        cards += f"""
        <div style="display:flex;flex-direction:column;align-items:center;gap:8px;min-width:120px">
          <svg width="{size}" height="{size}">
            <circle cx="{size//2}" cy="{size//2}" r="{r}" fill="none" stroke="{track_color}" stroke-width="{stroke_w}"/>
            <circle cx="{size//2}" cy="{size//2}" r="{r}" fill="none" stroke="{color}" stroke-width="{stroke_w}"
              stroke-linecap="round"
              stroke-dasharray="{dash:.2f} {gap:.2f}"
              transform="rotate({rotate} {size//2} {size//2})">
              <animate attributeName="stroke-dasharray" from="0 {circ:.2f}" to="{dash:.2f} {gap:.2f}" dur="0.7s" begin="{i * 0.1}s" fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1"/>
            </circle>
            <text x="{size//2}" y="{size//2 - 4}" text-anchor="middle" font-size="18" font-weight="700" fill="{text_color}">{val_str}</text>
            <text x="{size//2}" y="{size//2 + 14}" text-anchor="middle" font-size="11" fill="#8E8E93">{unit}</text>
          </svg>
          <div style="font-size:13px;font-weight:600;color:{text_color};text-align:center">{label}</div>
        </div>"""

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{css_base(dark, width, height)}
.ring-row {{ display:flex; flex-wrap:wrap; gap:28px; justify-content:center; }}
</style></head><body>
<div class="title">{title}</div>
<div class="card">
<div class="ring-row">{cards}</div>
</div>
</body></html>"""


def build_statcard_html(data: dict, title: str, dark: bool, width: int, height: int) -> str:
    stats = data.get("stats", [])
    if not stats:
        raise ValueError("stat-card requires 'stats'")

    text_color = "#F5F5F7" if dark else "#1D1D1F"
    card_bg = "#2C2C2E" if dark else "#FFFFFF"
    sub_color = "#8E8E93"
    inner_shadow = "none" if dark else "0 2px 12px rgba(0,0,0,0.06)"

    cols = min(len(stats), 3)
    card_html = ""
    for i, stat in enumerate(stats):
        color = stat.get("color") or APPLE_COLORS[i % len(APPLE_COLORS)]
        trend = stat.get("trend", "")
        unit = stat.get("unit", "")
        card_html += f"""
        <div style="background:{card_bg};border-radius:16px;padding:24px;box-shadow:{inner_shadow};
                    display:flex;flex-direction:column;gap:6px;animation:fadeIn 300ms ease-out {i * 0.06}s both;">
          <div style="font-size:13px;font-weight:600;color:{sub_color};text-transform:uppercase;letter-spacing:0.5px">{stat.get('label','')}</div>
          <div style="font-size:36px;font-weight:700;color:{color};letter-spacing:-1px;line-height:1">{stat.get('value','')}</div>
          <div style="font-size:13px;color:{sub_color}">{unit}</div>
          {'<div style="font-size:12px;font-weight:500;color:' + sub_color + ';margin-top:4px">' + trend + '</div>' if trend else ''}
        </div>"""

    outer_bg = "#1C1C1E" if dark else "#F5F5F7"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{css_base(dark, width, height)}
.stat-grid {{
    display: grid;
    grid-template-columns: repeat({cols}, 1fr);
    gap: 16px;
    width: 100%;
}}
</style></head><body>
<div class="title">{title}</div>
<div class="stat-grid">{card_html}</div>
</body></html>"""


def build_hbar_html(data: dict, title: str, dark: bool, width: int, height: int) -> str:
    items = data.get("items", [])
    if not items:
        raise ValueError("hbar requires 'items'")

    text_color = "#F5F5F7" if dark else "#1D1D1F"
    sub_color = "#8E8E93"
    track_color = "#E5E5EA" if not dark else "#3A3A3C"
    card_bg = "#2C2C2E" if dark else "#FFFFFF"
    shadow = "none" if dark else "0 4px 20px rgba(0,0,0,0.08)"

    rows = ""
    for i, item in enumerate(items):
        val = item.get("value", 0)
        mx = item.get("max", 100) or 100
        label = item.get("label", "")
        sublabel = item.get("sublabel", "")
        color = item.get("color") or APPLE_COLORS[i % len(APPLE_COLORS)]
        pct = min(val / mx * 100, 100)
        delay = i * 0.08

        rows += f"""
        <div style="display:flex;flex-direction:column;gap:8px;animation:fadeIn 300ms ease-out {delay}s both;">
          <div style="display:flex;justify-content:space-between;align-items:baseline;">
            <span style="font-size:15px;font-weight:600;color:{text_color}">{label}</span>
            <span style="font-size:13px;color:{sub_color}">{sublabel}</span>
          </div>
          <div style="position:relative;height:10px;background:{track_color};border-radius:999px;overflow:hidden;">
            <div style="position:absolute;left:0;top:0;height:100%;width:0;background:{color};border-radius:999px;
                        animation:grow{i} 0.6s {delay}s cubic-bezier(0.25,0.1,0.25,1) forwards;"></div>
          </div>
          <style>@keyframes grow{i} {{ to {{ width: {pct:.1f}%; }} }}</style>
        </div>"""

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{css_base(dark, width, height)}
</style></head><body>
<div class="title">{title}</div>
<div class="card" style="display:flex;flex-direction:column;gap:20px;">
{rows}
</div>
</body></html>"""


BUILDERS = {
    "bar": build_bar_html,
    "line": build_line_html,
    "donut": build_donut_html,
    "progress": build_progress_html,
    "hbar": build_hbar_html,
    "stat-card": build_statcard_html,
}


def screenshot_with_playwright(html_path: str, output: str, width: int, height: int) -> bool:
    try:
        result = subprocess.run(
            ["npx", "--yes", "playwright", "screenshot",
             "--browser", "chromium",
             "--viewport-size", f"{width},{height}",
             "--wait-for-timeout", "800",
             f"file://{html_path}", output],
            capture_output=True, text=True, timeout=60
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def screenshot_with_pyppeteer(html_path: str, output: str, width: int, height: int) -> bool:
    try:
        import asyncio
        import pyppeteer

        async def _take():
            browser = await pyppeteer.launch(headless=True, args=["--no-sandbox"])
            page = await browser.newPage()
            await page.setViewport({"width": width, "height": height})
            await page.goto(f"file://{html_path}")
            await page.waitForTimeout(600)
            await page.screenshot({"path": output, "fullPage": False})
            await browser.close()

        asyncio.get_event_loop().run_until_complete(_take())
        return True
    except Exception as e:
        print(f"pyppeteer error: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Apple HIG visualization generator")
    parser.add_argument("--type", required=True, choices=["bar", "line", "donut", "progress", "hbar", "stat-card"])
    parser.add_argument("--title", required=True)
    parser.add_argument("--data", required=True)
    parser.add_argument("--output", default="/tmp/apple-viz-output.png")
    parser.add_argument("--width", type=int, default=800)
    parser.add_argument("--height", type=int, default=500)
    parser.add_argument("--dark", action="store_true")
    args = parser.parse_args()

    try:
        data = json.loads(args.data)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in --data: {e}", file=sys.stderr)
        sys.exit(1)

    builder = BUILDERS[args.type]
    html = builder(data, args.title, args.dark, args.width, args.height)

    tmp_html = f"/tmp/apple-viz-{uuid.uuid4().hex[:8]}.html"
    with open(tmp_html, "w") as f:
        f.write(html)

    print(f"HTML generated: {tmp_html}", file=sys.stderr)

    ok = screenshot_with_playwright(tmp_html, args.output, args.width, args.height)
    if not ok:
        print("Playwright not available, trying pyppeteer...", file=sys.stderr)
        ok = screenshot_with_pyppeteer(tmp_html, args.output, args.width, args.height)

    if ok:
        try:
            os.remove(tmp_html)
        except OSError:
            pass
        print(args.output)
        sys.exit(0)
    else:
        print(f"Screenshot failed. HTML available at: {tmp_html}", file=sys.stderr)
        print(f"HTML_ONLY:{tmp_html}")
        sys.exit(1)


if __name__ == "__main__":
    main()

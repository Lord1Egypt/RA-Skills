"""Generate session analytics charts for ClawVision.

Adapts ideas from smart-charts@neuhanli (ClawHub):
- session data -> ECharts pipeline
- self-contained HTML (ECharts inlined)
- multi-chart batch
- fact-based annotations

Dependencies: only standard library + playwright (already used by ClawVision).
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from playwright.sync_api import sync_playwright

# Bundled ECharts 5.x minified (Apache-2.0). Saved locally to avoid CDN.
_ECHARTS_JS = Path(__file__).with_name("echarts.min.js")
ECHARTS_SRC = _ECHARTS_JS.read_text(encoding="utf-8") if _ECHARTS_JS.exists() else None

if ECHARTS_SRC is None:
    ECHARTS_URL = "https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"
else:
    ECHARTS_URL = None

LIGHT_THEME = {
    "bg": "#f5f6f8",
    "card": "#ffffff",
    "text": "#1a1a1a",
    "muted": "#666666",
    "accent": "#2a9df4",
    "green": "#4cd964",
    "orange": "#ff9500",
    "red": "#ff3b30",
    "border": "#e5e7eb",
}

DARK_THEME = {
    "bg": "#0f1115",
    "card": "#1a1d23",
    "text": "#e8e8e8",
    "muted": "#9aa0a6",
    "accent": "#4aa8ff",
    "green": "#5dd877",
    "orange": "#ffae33",
    "red": "#ff6659",
    "border": "#2c3038",
}


def normalize_col(name: str) -> str:
    """Normalize column names like smart-charts does."""
    if name is None or str(name).lower() == "nan":
        return "unnamed"
    s = str(name).strip().lower()
    s = re.sub(r"[^\w\s\u4e00-\u9fff]", "_", s)
    s = re.sub(r"[\s_]+", "_", s)
    s = s.strip("_")
    return s or "unnamed"


def parse_timestamp(ts) -> Optional[datetime]:
    if not ts:
        return None
    if isinstance(ts, (int, float)):
        return datetime.fromtimestamp(ts, tz=timezone.utc)
    try:
        return datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
    except Exception:
        return None


def session_to_records(messages: List[dict]) -> List[dict]:
    """Convert OpenClaw session messages into normalized records."""
    rows = []
    for idx, msg in enumerate(messages):
        role = msg.get("role") or "unknown"
        text = msg.get("content") or ""
        dt = parse_timestamp(msg.get("timestamp") or msg.get("created_at"))
        if dt is None:
            dt = datetime.now(timezone.utc)
        rows.append({
            "index": idx,
            "role": role,
            "role_normalized": normalize_col(role),
            "text": text,
            "text_length": len(text) if isinstance(text, str) else 0,
            "timestamp": dt,
            "has_tools": bool(msg.get("tool_calls") or msg.get("tool_results")),
        })
    return rows


def compute_metrics(records: List[dict]) -> dict:
    if not records:
        return {
            "message_count_by_role": {},
            "avg_message_length_by_role": {},
            "messages_over_time": [],
            "tool_usage_counts": {},
        }
    role_counts = Counter(r["role"] for r in records)
    role_lengths = defaultdict(list)
    for r in records:
        role_lengths[r["role"]].append(r["text_length"])
    avg_len = {role: round(sum(vals) / len(vals), 1) for role, vals in role_lengths.items()}

    # 5-minute buckets
    buckets = defaultdict(lambda: defaultdict(int))
    for r in records:
        ts = r["timestamp"]
        bucket = ts.replace(minute=(ts.minute // 5) * 5, second=0, microsecond=0)
        buckets[bucket.isoformat()][r["role"]] += 1

    # Ensure chronological order
    sorted_times = sorted(buckets.keys())
    messages_over_time = [
        {"time": t, "count": sum(buckets[t].values())}
        for t in sorted_times
    ]

    tool_counts = Counter(r["role"] for r in records if r["has_tools"])

    return {
        "message_count_by_role": dict(role_counts),
        "avg_message_length_by_role": avg_len,
        "messages_over_time": messages_over_time,
        "tool_usage_counts": dict(tool_counts),
    }


def _render_echarts(div_id: str, option: dict, theme: dict, height: int = 360) -> str:
    option_json = json.dumps(option, ensure_ascii=False, indent=2)
    return f"""
<div id="{div_id}" style="width:100%;height:{height}px;background:{theme['card']};border:1px solid {theme['border']};border-radius:12px;padding:12px;box-sizing:border-box;"></div>
<script>
window._clawvision_chart_options = window._clawvision_chart_options || [];
window._clawvision_chart_options.push({{id: '{div_id}', option: {option_json}}});
</script>
"""


def _render_init_script(theme: dict) -> str:
    return """
<script>
(function(){
  window._clawvision_charts = [];
  (window._clawvision_chart_options || []).forEach(function(cfg){
    var chartDom = document.getElementById(cfg.id);
    if (chartDom && typeof echarts !== 'undefined'){
      var chart = echarts.init(chartDom, null, {renderer: 'svg'});
      chart.setOption(cfg.option);
      window._clawvision_charts.push(chart);
    }
  });
})();
</script>
"""


def build_role_distribution(records: List[dict], theme: dict, annotation: str = "") -> tuple:
    counts = Counter(r["role"] for r in records)
    data = [{"name": name, "value": value} for name, value in counts.most_common()]
    option = {
        "title": {"text": "Messages by role", "left": "center", "textStyle": {"color": theme["text"]}, "subtext": annotation, "subtextStyle": {"color": theme["muted"], "fontSize": 12}},
        "tooltip": {"trigger": "item", "formatter": "{b}: {c} ({d}%)"},
        "legend": {"bottom": 0, "textStyle": {"color": theme["muted"]}},
        "color": [theme["accent"], theme["green"], theme["orange"], theme["red"], "#9b59b6", "#f1c40f"],
        "series": [{
            "type": "pie",
            "radius": ["40%", "70%"],
            "avoidLabelOverlap": False,
            "itemStyle": {"borderRadius": 8, "borderColor": theme["card"], "borderWidth": 2},
            "label": {"show": True, "color": theme["text"]},
            "data": data,
        }],
    }
    return ("role_distribution", option)


def build_timeline(records: List[dict], theme: dict, annotation: str = "") -> tuple:
    if not records:
        return ("timeline", {})
    # 5-minute buckets per role
    buckets = defaultdict(lambda: defaultdict(int))
    for r in records:
        ts = r["timestamp"]
        bucket = ts.replace(minute=(ts.minute // 5) * 5, second=0, microsecond=0)
        buckets[bucket][r["role"]] += 1

    sorted_buckets = sorted(buckets.keys())
    times = [t.isoformat() for t in sorted_buckets]
    roles = sorted({r["role"] for r in records})
    palette = [theme["accent"], theme["green"], theme["orange"], theme["red"], "#9b59b6", "#f1c40f"]
    series = []
    for i, role in enumerate(roles):
        series.append({
            "name": role,
            "type": "line",
            "smooth": True,
            "stack": "Total",
            "areaStyle": {},
            "emphasis": {"focus": "series"},
            "data": [buckets[b][role] for b in sorted_buckets],
            "color": palette[i % len(palette)],
        })
    option = {
        "title": {"text": "Activity timeline", "left": "center", "textStyle": {"color": theme["text"]}, "subtext": annotation, "subtextStyle": {"color": theme["muted"], "fontSize": 12}},
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "cross"}},
        "legend": {"bottom": 0, "textStyle": {"color": theme["muted"]}},
        "grid": {"left": "3%", "right": "4%", "bottom": "15%", "containLabel": True},
        "xAxis": {"type": "category", "boundaryGap": False, "data": times, "axisLabel": {"color": theme["muted"]}, "axisLine": {"lineStyle": {"color": theme["border"]}}},
        "yAxis": {"type": "value", "axisLabel": {"color": theme["muted"]}, "splitLine": {"lineStyle": {"color": theme["border"]}}},
        "series": series,
        "dataZoom": [{"type": "inside", "start": 0, "end": 100}, {"start": 0, "end": 100, "height": 20, "bottom": 30}],
    }
    return ("timeline", option)


def build_tool_usage(records: List[dict], theme: dict, annotation: str = "") -> tuple:
    counts = Counter(r["role"] for r in records if r["has_tools"])
    labels = list(counts.keys()) if counts else ["no tools"]
    values = list(counts.values()) if counts else [0]
    option = {
        "title": {"text": "Tool usage by role", "left": "center", "textStyle": {"color": theme["text"]}, "subtext": annotation, "subtextStyle": {"color": theme["muted"], "fontSize": 12}},
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "grid": {"left": "3%", "right": "4%", "bottom": "10%", "containLabel": True},
        "xAxis": {"type": "category", "data": labels, "axisLabel": {"color": theme["muted"]}, "axisLine": {"lineStyle": {"color": theme["border"]}}},
        "yAxis": {"type": "value", "axisLabel": {"color": theme["muted"]}, "splitLine": {"lineStyle": {"color": theme["border"]}}},
        "series": [{
            "type": "bar",
            "data": values,
            "itemStyle": {"borderRadius": [6, 6, 0, 0], "color": theme["orange"]},
            "label": {"show": True, "position": "top", "color": theme["text"]},
        }],
    }
    return ("tool_usage", option)


def generate_charts_html(records: List[dict], preset: dict, annotations: Dict[str, str] = None, dark: bool = False) -> str:
    annotations = annotations or {}
    theme = (DARK_THEME if dark else LIGHT_THEME).copy()
    if preset:
        theme["accent"] = preset.get("light", {}).get("accent", theme["accent"])
        theme["green"] = preset.get("light", {}).get("green", theme["green"])
        theme["orange"] = preset.get("light", {}).get("orange", theme["orange"])
        theme["red"] = preset.get("light", {}).get("red", theme["red"])
        if dark and "dark" in preset:
            theme["accent"] = preset["dark"].get("accent", theme["accent"])
            theme["green"] = preset["dark"].get("green", theme["green"])
            theme["orange"] = preset["dark"].get("orange", theme["orange"])
            theme["red"] = preset["dark"].get("red", theme["red"])

    charts = [
        build_role_distribution(records, theme, annotations.get("role_distribution", "")),
        build_timeline(records, theme, annotations.get("timeline", "")),
        build_tool_usage(records, theme, annotations.get("tool_usage", "")),
    ]

    body_parts = []
    for idx, (chart_id, option) in enumerate(charts):
        body_parts.append(_render_echarts(f"chart_{idx}", option, theme, height=360))
        body_parts.append("<div style=\"height:20px\"></div>")

    echarts_block = ""
    if ECHARTS_SRC:
        echarts_block = f"<script>{ECHARTS_SRC}</script>"
    elif ECHARTS_URL:
        echarts_block = f'<script src="{ECHARTS_URL}"></script>'

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ClawVision Session Analytics</title>
<style>
body{{margin:0;padding:24px;font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;background:{theme['bg']};color:{theme['text']};}}
.wrap{{max-width:900px;margin:0 auto;}}
h1{{font-size:22px;margin:0 0 18px;}}
</style>
{echarts_block}
</head>
<body>
<div class="wrap">
<h1>Session Analytics</h1>
{''.join(body_parts)}
</div>
{_render_init_script(theme)}
</body>
</html>"""
    return html


def render_charts_to_png(html: str, output_path: Path, width: int = 900, height: int = 1200):
    tmp_html = output_path.with_suffix(".tmp.html")
    tmp_html.write_text(html, encoding="utf-8")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": width, "height": height})
            page.goto(f"file:///{tmp_html.as_posix()}")
            page.wait_for_load_state("networkidle")
            # Ensure ECharts instances rendered SVG/canvas
            page.wait_for_function("(typeof echarts !== 'undefined') && (window._clawvision_charts || []).length === 3", timeout=5000)
            page.wait_for_timeout(600)
            page.screenshot(path=str(output_path), full_page=True)
            browser.close()
    finally:
        tmp_html.unlink(missing_ok=True)


def generate_for_session(messages: List[dict], output_dir: Path, slug: str, preset: dict = None, annotations: Dict[str, str] = None) -> dict:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    records = session_to_records(messages)
    metrics = compute_metrics(records)

    html_light = generate_charts_html(records, preset, annotations, dark=False)
    html_dark = generate_charts_html(records, preset, annotations, dark=True)

    light_path = output_dir / f"{slug}_charts.html"
    dark_path = output_dir / f"{slug}_charts_dark.html"
    png_path = output_dir / f"{slug}_charts.png"

    light_path.write_text(html_light, encoding="utf-8")
    dark_path.write_text(html_dark, encoding="utf-8")
    render_charts_to_png(html_light, png_path)

    return {
        "metrics": metrics,
        "charts_html_light": str(light_path),
        "charts_html_dark": str(dark_path),
        "charts_png": str(png_path),
    }


def main():
    parser = argparse.ArgumentParser(description="Generate ClawVision session analytics charts.")
    parser.add_argument("--session", "-i", required=True, help="Path to session JSON file")
    parser.add_argument("--output", "-o", required=True, help="Output directory")
    parser.add_argument("--slug", "-s", default="session", help="Output slug")
    args = parser.parse_args()

    session_path = Path(args.session)
    if not session_path.exists():
        print(json.dumps({"error": f"File not found: {session_path}"}, ensure_ascii=False))
        sys.exit(1)

    data = json.loads(session_path.read_text(encoding="utf-8"))
    messages = data if isinstance(data, list) else data.get("messages", [])
    result = generate_for_session(messages, Path(args.output), args.slug)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

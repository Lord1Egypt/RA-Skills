#!/usr/bin/env python3
"""Render a simple, dependency-free SVG chart from CSV data.

This is intentionally modest: it creates reviewable first-pass bar, dot, line,
and scatter charts with labels and honest defaults. Use full plotting libraries
for publication-grade output when available.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

DATE_RE = re.compile(r"^(\d{4}-\d{1,2}-\d{1,2}|\d{4}-\d{1,2}|\d{1,2}/\d{1,2}/\d{2,4})$")
PALETTE = ["#222222", "#666666", "#999999", "#444444", "#777777", "#bbbbbb"]


def to_float(value: Any) -> Optional[float]:
    try:
        if value is None or str(value).strip() == "":
            return None
        return float(str(value).replace(",", ""))
    except ValueError:
        return None


def read_csv(path: Path) -> List[Dict[str, str]]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
    except FileNotFoundError:
        raise SystemExit(f"Error: CSV file not found: {path}")
    except csv.Error as exc:
        raise SystemExit(f"Error: could not parse CSV: {exc}")
    if not rows:
        raise SystemExit("Error: CSV has no data rows.")
    return rows


def infer_chart(rows: List[Dict[str, str]], x: str, y: str, group: Optional[str]) -> str:
    xs = [r.get(x, "") for r in rows]
    x_numeric = sum(1 for v in xs if to_float(v) is not None) / max(1, len(xs)) > 0.85
    x_date = sum(1 for v in xs if DATE_RE.match(str(v).strip())) / max(1, len(xs)) > 0.5
    if x_date:
        return "line"
    if x_numeric:
        return "scatter"
    unique_x = len(set(xs))
    return "bar" if unique_x <= 25 and not group else "dot"


def scale(value: float, domain_min: float, domain_max: float, range_min: float, range_max: float) -> float:
    if math.isclose(domain_min, domain_max):
        return (range_min + range_max) / 2
    return range_min + (value - domain_min) / (domain_max - domain_min) * (range_max - range_min)


def nice_ticks(vmin: float, vmax: float, count: int = 5) -> List[float]:
    if math.isclose(vmin, vmax):
        return [vmin]
    span = vmax - vmin
    raw_step = span / max(1, count - 1)
    mag = 10 ** math.floor(math.log10(abs(raw_step)))
    norm = raw_step / mag
    if norm <= 1:
        step = 1 * mag
    elif norm <= 2:
        step = 2 * mag
    elif norm <= 5:
        step = 5 * mag
    else:
        step = 10 * mag
    start = math.floor(vmin / step) * step
    ticks = []
    val = start
    while val <= vmax + step * 0.5 and len(ticks) < 20:
        if val >= vmin - step * 0.1:
            ticks.append(0.0 if math.isclose(val, 0.0) else val)
        val += step
    return ticks


def fmt_num(v: float) -> str:
    if abs(v) >= 1000 or (abs(v) < 0.01 and not math.isclose(v, 0)):
        return f"{v:.2g}"
    if math.isclose(v, round(v)):
        return str(int(round(v)))
    return f"{v:.3g}"


def aggregate(rows: List[Dict[str, str]], x: str, y: str, group: Optional[str]) -> List[Dict[str, Any]]:
    acc: Dict[Tuple[str, str], List[float]] = defaultdict(list)
    for r in rows:
        yv = to_float(r.get(y))
        if yv is None:
            continue
        xv = str(r.get(x, ""))
        gv = str(r.get(group, "")) if group else ""
        acc[(xv, gv)].append(yv)
    data = []
    for (xv, gv), vals in acc.items():
        data.append({"x": xv, "group": gv, "y": sum(vals) / len(vals), "n": len(vals)})
    return data


def svg_text(x: float, y: float, text: str, size: int = 11, anchor: str = "middle", extra: str = "") -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial, sans-serif" font-size="{size}" text-anchor="{anchor}" {extra}>{html.escape(text)}</text>'


def render(rows: List[Dict[str, str]], x: str, y: str, chart: str, group: Optional[str], title: str, width: int, height: int) -> Tuple[str, Dict[str, Any]]:
    data = aggregate(rows, x, y, group)
    if not data:
        raise SystemExit("Error: no numeric y values found after parsing.")
    if chart == "auto":
        chart = infer_chart(rows, x, y, group)
    if chart not in {"bar", "dot", "line", "scatter"}:
        raise SystemExit("Error: --chart must be one of auto, bar, dot, line, scatter.")

    margin = {"left": 72, "right": 32 if not group else 90, "top": 58, "bottom": 74}
    plot_x0, plot_y0 = margin["left"], margin["top"]
    plot_x1, plot_y1 = width - margin["right"], height - margin["bottom"]
    plot_w, plot_h = plot_x1 - plot_x0, plot_y1 - plot_y0
    yvals = [d["y"] for d in data]
    if chart == "bar":
        ymin, ymax = min(0, min(yvals)), max(0, max(yvals))
    else:
        pad = (max(yvals) - min(yvals)) * 0.08 or 1.0
        ymin, ymax = min(yvals) - pad, max(yvals) + pad
        if min(yvals) >= 0 and ymin < 0:
            ymin = 0
    ticks = nice_ticks(ymin, ymax)
    if ticks:
        ymin = min(ymin, min(ticks)); ymax = max(ymax, max(ticks))

    elements = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', '<rect width="100%" height="100%" fill="white"/>']
    elements.append(svg_text(width/2, 26, title or f"{y} by {x}", size=16))
    elements.append(svg_text(width/2, height-16, x, size=12))
    elements.append(f'<text x="18" y="{height/2:.1f}" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" transform="rotate(-90 18 {height/2:.1f})">{html.escape(y)}</text>')

    # Grid and y axis labels
    for t in ticks:
        yy = scale(t, ymin, ymax, plot_y1, plot_y0)
        elements.append(f'<line x1="{plot_x0}" y1="{yy:.1f}" x2="{plot_x1}" y2="{yy:.1f}" stroke="#dddddd" stroke-width="1"/>')
        elements.append(svg_text(plot_x0-8, yy+4, fmt_num(t), size=10, anchor="end"))
    elements.append(f'<line x1="{plot_x0}" y1="{plot_y0}" x2="{plot_x0}" y2="{plot_y1}" stroke="#333333" stroke-width="1"/>')
    elements.append(f'<line x1="{plot_x0}" y1="{plot_y1}" x2="{plot_x1}" y2="{plot_y1}" stroke="#333333" stroke-width="1"/>')

    warnings: List[str] = []
    groups = sorted(set(d["group"] for d in data)) if group else [""]
    group_color = {g: PALETTE[i % len(PALETTE)] for i, g in enumerate(groups)}

    if chart in {"bar", "dot", "line"}:
        xcats = sorted(set(d["x"] for d in data), key=lambda v: (not DATE_RE.match(str(v)), str(v)))
        xpos = {cat: plot_x0 + (i + 0.5) * plot_w / max(1, len(xcats)) for i, cat in enumerate(xcats)}
        # x labels, sampled if dense
        step = max(1, math.ceil(len(xcats) / 12))
        for i, cat in enumerate(xcats):
            if i % step == 0 or i == len(xcats) - 1:
                elements.append(svg_text(xpos[cat], plot_y1+18, str(cat), size=10, anchor="middle", extra='transform="rotate(35 {:.1f} {:.1f})"'.format(xpos[cat], plot_y1+18) if len(str(cat)) > 8 else ""))
        if chart == "bar":
            if group:
                warnings.append("Grouped bars are simplified; consider dot plots or small multiples if many groups need comparison.")
            bw = plot_w / max(1, len(xcats)) * 0.72 / max(1, len(groups))
            zero_y = scale(0, ymin, ymax, plot_y1, plot_y0)
            for d in data:
                gi = groups.index(d["group"])
                cx = xpos[d["x"]] - (len(groups)-1)*bw/2 + gi*bw
                yy = scale(d["y"], ymin, ymax, plot_y1, plot_y0)
                top, bottom = min(yy, zero_y), max(yy, zero_y)
                elements.append(f'<rect x="{cx-bw/2:.1f}" y="{top:.1f}" width="{bw:.1f}" height="{max(1,bottom-top):.1f}" fill="{group_color[d["group"]]}"/>')
        elif chart == "dot":
            for d in data:
                gi = groups.index(d["group"])
                jitter = (gi - (len(groups)-1)/2) * 8
                cx = xpos[d["x"]] + jitter
                yy = scale(d["y"], ymin, ymax, plot_y1, plot_y0)
                elements.append(f'<circle cx="{cx:.1f}" cy="{yy:.1f}" r="4" fill="{group_color[d["group"]]}"/>')
        else:  # line
            for g in groups:
                series = sorted([d for d in data if d["group"] == g], key=lambda d: xcats.index(d["x"]))
                pts = [(xpos[d["x"]], scale(d["y"], ymin, ymax, plot_y1, plot_y0), d) for d in series]
                path = " ".join(("M" if i == 0 else "L") + f" {px:.1f} {py:.1f}" for i, (px, py, _) in enumerate(pts))
                elements.append(f'<path d="{path}" fill="none" stroke="{group_color[g]}" stroke-width="2"/>')
                for px, py, _ in pts:
                    elements.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.6" fill="{group_color[g]}"/>')
                if group and pts:
                    px, py, _ = pts[-1]
                    elements.append(svg_text(px+6, py+4, str(g), size=10, anchor="start"))
    else:  # scatter
        xnums: List[float] = []
        points: List[Tuple[float, float, str]] = []
        for r in rows:
            xv = to_float(r.get(x)); yv = to_float(r.get(y))
            if xv is None or yv is None:
                continue
            gv = str(r.get(group, "")) if group else ""
            xnums.append(xv); points.append((xv, yv, gv))
        if not points:
            raise SystemExit("Error: scatter chart requires numeric x and y values.")
        xmin, xmax = min(xnums), max(xnums)
        xpad = (xmax-xmin)*0.08 or 1.0
        xmin, xmax = xmin-xpad, xmax+xpad
        xticks = nice_ticks(xmin, xmax)
        for t in xticks:
            xx = scale(t, xmin, xmax, plot_x0, plot_x1)
            elements.append(f'<line x1="{xx:.1f}" y1="{plot_y0}" x2="{xx:.1f}" y2="{plot_y1}" stroke="#eeeeee" stroke-width="1"/>')
            elements.append(svg_text(xx, plot_y1+18, fmt_num(t), size=10))
        for xv, yv, gv in points:
            xx = scale(xv, xmin, xmax, plot_x0, plot_x1)
            yy = scale(yv, ymin, ymax, plot_y1, plot_y0)
            elements.append(f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="3.5" fill="{group_color.get(gv, PALETTE[0])}" opacity="0.85"/>')

    if group and chart != "line":
        lx, ly = plot_x1 + 10, plot_y0 + 12
        for i, g in enumerate(groups):
            yleg = ly + i*18
            elements.append(f'<rect x="{lx}" y="{yleg-9}" width="10" height="10" fill="{group_color[g]}"/>')
            elements.append(svg_text(lx+14, yleg, str(g), size=10, anchor="start"))

    elements.append(svg_text(plot_x0, height-4, f"Generated as a first-pass SVG; verify source, units, uncertainty, and accessibility before publication.", size=9, anchor="start"))
    elements.append("</svg>")
    metadata = {"chart": chart, "x": x, "y": y, "group": group, "rows_input": len(rows), "points_rendered": len(data), "warnings": warnings, "integrity_defaults": ["bar charts include zero baseline", "axes and units should be reviewed", "source and uncertainty must be added if relevant"]}
    return "\n".join(elements), metadata


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Render a simple SVG chart from CSV using dependency-free, honest defaults.")
    parser.add_argument("--csv", type=Path, required=True, help="Input CSV with a header row.")
    parser.add_argument("--x", required=True, help="Column for x/category/time/relationship axis.")
    parser.add_argument("--y", required=True, help="Numeric column for y axis.")
    parser.add_argument("--group", help="Optional grouping column.")
    parser.add_argument("--chart", choices=("auto", "bar", "dot", "line", "scatter"), default="auto")
    parser.add_argument("--title", default="", help="Chart title.")
    parser.add_argument("--width", type=int, default=900)
    parser.add_argument("--height", type=int, default=520)
    parser.add_argument("--output", type=Path, required=True, help="Output SVG path.")
    parser.add_argument("--metadata", type=Path, help="Optional JSON metadata output path.")
    args = parser.parse_args(argv)

    if args.width < 400 or args.height < 300:
        print("Error: width must be >=400 and height >=300.", file=sys.stderr)
        return 2
    rows = read_csv(args.csv)
    headers = set(rows[0].keys())
    for col in [args.x, args.y, args.group]:
        if col and col not in headers:
            print(f"Error: column not found: {col}", file=sys.stderr)
            return 2
    svg, meta = render(rows, args.x, args.y, args.chart, args.group, args.title, args.width, args.height)
    args.output.write_text(svg, encoding="utf-8")
    if args.metadata:
        args.metadata.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "metadata": meta}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

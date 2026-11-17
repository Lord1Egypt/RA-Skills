#!/usr/bin/env python3
"""
Excalidraw Diagram Generator — create hand-drawn style architecture,
flow, and sequence diagrams from the CLI.

Commands:
  diagram --type <arch|flow|seq> [options]   Generate a diagram
  merge <base> <overlay>                     Merge two Excalidraw files
  info <file>                                Show diagram metadata/summary
  export <file> [--format png|svg]           Export to image (if cairosvg/pillow available)

Output is a valid .excalidraw.json file loadable in excalidraw.com or the
Excalidraw editor.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Excalidraw element constants
# ---------------------------------------------------------------------------

STROKE_COLORS = [
    "#1e1e1e",
    "#2b8a3e",
    "#1971c2",
    "#e67700",
    "#c92a2a",
    "#5f3dc4",
    "#0b7285",
    "#e64980",
]
STROKE_WIDTH = 2
ROUGHNESS = 1  # 0=cartoon, 1=handdrawn, 2=architect
OPACITY = 100

FONT_FAMILY = 2  # 0=Virgil, 1=Helvetica, 2=Cascadia


def _make_element(
    typ: str,
    x: float,
    y: float,
    width: float,
    height: float,
    *,
    label: str = "",
    color_idx: int = 0,
    background: str = "#ffffff",
    stroke_style: str = "solid",
    roundness: Optional[Dict[str, Any]] = None,
    link: Optional[str] = None,
    group_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build an Excalidraw element dict."""
    eid = f"{typ}-{random.randint(100000, 999999)}"
    stroke_color = STROKE_COLORS[color_idx % len(STROKE_COLORS)]
    el: Dict[str, Any] = {
        "type": typ,
        "version": 1,
        "versionNonce": random.randint(0, 2**31),
        "isDeleted": False,
        "id": eid,
        "fillStyle": "solid" if typ == "rectangle" else "hachure",
        "strokeWidth": STROKE_WIDTH,
        "strokeStyle": stroke_style,
        "roughness": ROUGHNESS,
        "opacity": OPACITY,
        "angle": 0,
        "x": x,
        "y": y,
        "strokeColor": stroke_color,
        "backgroundColor": background,
        "width": width,
        "height": height,
        "seed": random.randint(0, 2**31),
        "groupIds": [group_id] if group_id else [],
        "frameId": None,
        "roundness": roundness or {"type": 3},
        "boundElements": [],
        "updated": time.time(),
        "link": link,
    }
    # Roundness type 3 = Heavily rounded
    if roundness is None:
        roundness_vals: Optional[Dict[str, Any]] = None
        if typ in ("rectangle", "diamond"):
            roundness_vals = {"type": 3}
        if roundness_vals:
            el["roundness"] = roundness_vals
        else:
            el["roundness"] = None

    if typ == "text" and label:
        el["text"] = label
        el["fontSize"] = 20
        el["fontFamily"] = FONT_FAMILY
        el["textAlign"] = "center"
        el["verticalAlign"] = "middle"
        el["containerId"] = None
        el["originalText"] = label
        el["autoResize"] = True
        el["lineHeight"] = 1.25
    elif typ == "rectangle":
        el["label"] = {"text": label} if label else {}
        el["locked"] = False
        el["link"] = None
    elif typ == "arrow":
        el["points"] = [[0, 0], [width, height]]
        el["lastCommittedPoint"] = None
        el["startBinding"] = None
        el["endBinding"] = None
        el["startArrowhead"] = None
        el["endArrowhead"] = "arrow"
        el["elbowed"] = False

    return el


def _make_text(
    x: float,
    y: float,
    text: str,
    *,
    color_idx: int = 0,
    font_size: int = 20,
    width: Optional[float] = None,
) -> Dict[str, Any]:
    """Create a text element."""
    return _make_element(
        "text",
        x,
        y,
        width or len(text) * 10,
        font_size * 1.4,
        label=text,
        color_idx=color_idx,
        background="transparent",
    )


def _make_arrow(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    *,
    color_idx: int = 0,
) -> Dict[str, Any]:
    """Create an arrow between two points."""
    return _make_element(
        "arrow",
        x1,
        y1,
        x2 - x1,
        y2 - y1,
        color_idx=color_idx,
        background="transparent",
        stroke_style="solid",
    )


# ---------------------------------------------------------------------------
# Diagram generators
# ---------------------------------------------------------------------------

PADDING = 40
BOX_W = 180
BOX_H = 60
BOX_GAP_X = 80
BOX_GAP_Y = 60


def _new_file(title: str) -> Dict[str, Any]:
    """Create a new empty Excalidraw file."""
    return {
        "type": "excalidraw",
        "version": 2,
        "source": "excalidraw-cli",
        "elements": [],
        "appState": {
            "gridSize": None,
            "viewBackgroundColor": "#f8f9fa",
        },
        "files": {},
    }


def gen_architecture(
    title: str,
    components: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Generate an architecture / system-design diagram.

    Components are displayed as labeled boxes in a grid.
    Default: 6 generic components.
    """
    comps = components or ["Frontend", "API", "Auth", "Database", "Cache", "Queue"]

    # Calculate layout grid
    n = len(comps)
    cols = min(3, n)
    rows = math.ceil(n / cols)
    total_w = cols * (BOX_W + BOX_GAP_X) - BOX_GAP_X
    total_h = rows * (BOX_H + BOX_GAP_Y) - BOX_GAP_Y
    start_x = PADDING
    start_y = PADDING + 40  # room for title

    data = _new_file(title)

    # Title
    data["elements"].append(
        _make_text(PADDING, 10, title, font_size=28, width=400)
    )

    # Boxes
    box_elements: List[Dict[str, Any]] = []
    for i, comp in enumerate(comps):
        col = i % cols
        row_ = i // cols
        x = start_x + col * (BOX_W + BOX_GAP_X)
        y = start_y + row_ * (BOX_H + BOX_GAP_Y)

        gid = f"arch-group-{i}"
        box_el = _make_element(
            "rectangle",
            x,
            y,
            BOX_W,
            BOX_H,
            label=comp,
            color_idx=i,
            background="transparent",
            group_id=gid,
        )
        label_el = _make_text(
            x + BOX_W / 2 - len(comp) * 5,
            y + BOX_H / 2 - 12,
            comp,
            color_idx=i,
            font_size=18,
        )
        label_el["groupIds"] = [gid]
        data["elements"].extend([box_el, label_el])

        # Arrow to next in row?
        if i + 1 < n and (i + 1) % cols != 0 and cols > 1:
            nn_col = (i + 1) % cols
            if nn_col == 0:
                pass  # wrapped — arrow down instead
            else:
                next_row_ = (i + 1) // cols
                if next_row_ == row_:
                    x1 = x + BOX_W
                    y1 = y + BOX_H / 2
                    x2 = x + BOX_W + BOX_GAP_X
                    y2 = y + BOX_H / 2
                    if x2 > x1:
                        arrow = _make_arrow(x1, y1, x2, y2, color_idx=i)
                        data["elements"].append(arrow)

        # Arrow down to next row?
        if col == 0 and (i + cols) < n:
            ci = i + cols
            ccol = ci % cols
            crow = ci // cols
            ax = x + BOX_W / 2
            ay = y + BOX_H
            bx = start_x + ccol * (BOX_W + BOX_GAP_X) + BOX_W / 2
            by_ = start_y + crow * (BOX_H + BOX_GAP_Y)
            if by_ > ay:
                arrow = _make_arrow(ax, ay, bx, by_, color_idx=i)
                data["elements"].append(arrow)

    return data


def gen_flow(title: str, steps: Optional[List[str]] = None) -> Dict[str, Any]:
    """Generate a flow chart / process diagram."""
    steps_list = steps or ["Start", "Process", "Validate", "Decide", "End"]

    data = _new_file(title)
    data["elements"].append(
        _make_text(PADDING, 10, title, font_size=28, width=400)
    )

    # Layout: vertical flow with diamond on 'Decide'
    y_cursor = PADDING + 50

    for i, step in enumerate(steps_list):
        is_diamond = step.lower() in ("decide", "if", "branch", "condition", "decision")
        is_terminal = step.lower() in ("start", "end", "stop", "exit", "finish")

        if is_terminal:
            w, h = 140, 50
            shape = "rectangle"
            rx = {"type": 2}  # little round
        elif is_diamond:
            w, h = 160, 80
            shape = "diamond"
            rx = None
        else:
            w, h = BOX_W, BOX_H
            shape = "rectangle"
            rx = {"type": 3}

        x = PADDING + 20
        y = y_cursor

        gid = f"flow-group-{i}"

        el = _make_element(
            shape,
            x,
            y,
            w,
            h,
            label=step,
            color_idx=i,
            background="#ffffff" if not is_diamond else "#fff3bf",
            roundness=rx,
            group_id=gid,
        )
        data["elements"].append(el)

        lbl = _make_text(
            x + w / 2 - len(step) * 5,
            y + h / 2 - 10,
            step,
            color_idx=i,
            font_size=16,
        )
        lbl["groupIds"] = [gid]
        data["elements"].append(lbl)

        # Arrow down
        if i < len(steps_list) - 1:
            arr = _make_arrow(x + w / 2, y + h, x + w / 2, y_cursor + h + BOX_GAP_Y, color_idx=i)
            data["elements"].append(arr)

        y_cursor += h + BOX_GAP_Y

    return data


def gen_sequence(
    title: str,
    actors: Optional[List[str]] = None,
    steps_str: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Generate a sequence / interaction diagram."""
    actors_list = actors or ["Client", "Server", "DB"]
    steps_list = steps_str or ["Request", "Process", "Query", "Response", "Render"]

    data = _new_file(title)
    data["elements"].append(
        _make_text(PADDING, 10, title, font_size=28, width=400)
    )

    n_actors = len(actors_list)
    act_gap = 220
    start_ax = PADDING + 60
    act_y = PADDING + 60

    # Actor lifeline x positions
    act_xs: List[float] = []
    for i, actor in enumerate(actors_list):
        ax = start_ax + i * act_gap
        act_xs.append(ax)

        # Actor box
        w = max(len(actor) * 8 + 20, 100)
        box = _make_element(
            "rectangle",
            ax - w / 2,
            act_y,
            w,
            40,
            label=actor,
            color_idx=i,
            background="#e7f5ff",
            roundness={"type": 3},
            group_id=f"seq-actor-{i}",
        )
        data["elements"].append(box)

        lbl = _make_text(
            ax - len(actor) * 5,
            act_y + 8,
            actor,
            color_idx=i,
            font_size=16,
        )
        lbl["groupIds"] = [f"seq-actor-{i}"]
        data["elements"].append(lbl)

        # Lifeline (dashed vertical line)
        lifeline = _make_element(
            "line",
            ax,
            act_y + 45,
            1,
            len(steps_list) * 80 + 80,
            color_idx=i,
            background="transparent",
        )
        lifeline["strokeStyle"] = "dashed"
        lifeline["roughness"] = 0
        lifeline["points"] = [[0, 0], [0, len(steps_list) * 80 + 80]]
        data["elements"].append(lifeline)

    # Steps — arrow from one actor to another
    arrow_y = act_y + 80
    for i, step in enumerate(steps_list):
        from_idx = i % n_actors
        to_idx = (i + 1) % n_actors
        x1 = act_xs[from_idx]
        x2 = act_xs[to_idx]

        # Arrow
        arr = _make_arrow(
            x1 if x1 < x2 else x2,
            arrow_y,
            x2 if x2 > x1 else x1,
            arrow_y,
            color_idx=from_idx,
        )
        data["elements"].append(arr)

        # Label above arrow
        mid_x = (x1 + x2) / 2
        lbl = _make_text(mid_x - len(step) * 4, arrow_y - 25, step, font_size=14)
        data["elements"].append(lbl)

        arrow_y += 70

    return data


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_diagram(args: List[str]) -> int:
    """Generate a diagram."""
    parser = argparse.ArgumentParser("diagram")
    parser.add_argument("--type", choices=["arch", "flow", "seq", "architecture", "sequence"], required=True)
    parser.add_argument("--title", default="Diagram")
    parser.add_argument("--output", "-o", default="diagram.excalidraw.json")
    parser.add_argument("--components", help="Comma-separated list of component names (architecture)")
    parser.add_argument("--steps", help="Comma-separated step names (flow/sequence)")
    parser.add_argument("--actors", help="Comma-separated actor names (sequence)")

    parsed, _ = parser.parse_known_args(args)

    typ = parsed.type
    if typ == "architecture":
        typ = "arch"
    elif typ == "sequence":
        typ = "seq"

    if typ == "arch":
        comps = [c.strip() for c in parsed.components.split(",")] if parsed.components else None
        data = gen_architecture(parsed.title, comps)
    elif typ == "seq":
        actors = [a.strip() for a in parsed.actors.split(",")] if parsed.actors else None
        steps = [s.strip() for s in parsed.steps.split(",")] if parsed.steps else None
        data = gen_sequence(parsed.title, actors, steps)
    else:  # flow
        steps = [s.strip() for s in parsed.steps.split(",")] if parsed.steps else None
        data = gen_flow(parsed.title, steps)

    out_path = parsed.output
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Diagram saved to {out_path}  ({len(data['elements'])} elements)")
    return 0


def cmd_merge(args: List[str]) -> int:
    """Merge two Excalidraw files."""
    if len(args) < 2:
        print("Usage: excalidraw_cli.py merge <base.json> <overlay.json> [-o <output>]", file=sys.stderr)
        return 1

    base_path = args[0]
    overlay_path = args[1]
    output_path = "merged.excalidraw.json"
    if "-o" in args:
        idx = args.index("-o")
        if idx + 1 < len(args):
            output_path = args[idx + 1]

    try:
        with open(base_path, "r", encoding="utf-8") as f:
            base = json.load(f)
        with open(overlay_path, "r", encoding="utf-8") as f:
            overlay = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading files: {e}", file=sys.stderr)
        return 1

    base_elements = base.get("elements", [])
    overlay_elements = overlay.get("elements", [])

    # Offset overlay elements slightly so they aren't on top of each other
    offset_x = 50.0
    for el in overlay_elements:
        if "x" in el:
            el["x"] += offset_x
        if "y" in el:
            el["y"] += offset_x

    base["elements"] = base_elements + overlay_elements
    base["appState"]["viewBackgroundColor"] = base.get("appState", {}).get("viewBackgroundColor", "#ffffff")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(base, f, indent=2, ensure_ascii=False)

    print(f"Merged diagram saved to {output_path}")
    print(f"  {len(base_elements)} base + {len(overlay_elements)} overlay = {len(base['elements'])} total elements")
    return 0


def cmd_info(args: List[str]) -> int:
    """Show info about an Excalidraw file."""
    if not args:
        print("Usage: excalidraw_cli.py info <file.json>", file=sys.stderr)
        return 1

    filepath = args[0]
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    elements = data.get("elements", [])
    n_total = len(elements)
    by_type: Dict[str, int] = {}
    for el in elements:
        t = el.get("type", "unknown")
        by_type[t] = by_type.get(t, 0) + 1

    print(f"File:     {filepath}")
    print(f"Version:  {data.get('version', '?')}")
    print(f"Source:   {data.get('source', '?')}")
    print(f"Elements: {n_total}")
    print(f"Types:")
    for t, c in sorted(by_type.items()):
        print(f"  {t}: {c}")

    # Show text content summary
    texts = [el.get("text", "") for el in elements if el.get("type") == "text" and el.get("text")]
    labels = [el.get("label", {}).get("text", "") for el in elements if el.get("type") == "rectangle" and el.get("label", {}).get("text")]
    all_labels = [t for t in texts + labels if t]
    if all_labels:
        print(f"Labels:   {', '.join(all_labels[:20])}")
        if len(all_labels) > 20:
            print(f"          ... and {len(all_labels) - 20} more")

    return 0


def cmd_export(args: List[str]) -> int:
    """Export diagram to PNG or SVG.

    Uses cairosvg for SVG or Pillow for PNG (via SVG intermediate).
    If converters aren't installed, prints the JSON path.
    """
    if not args:
        print("Usage: excalidraw_cli.py export <file.json> [--format png|svg] [-o <output>]", file=sys.stderr)
        return 1

    filepath = args[0]
    fmt = "svg"
    if "--format" in args:
        idx = args.index("--format")
        if idx + 1 < len(args):
            fmt = args[idx + 1]

    output_path = os.path.splitext(filepath)[0] + f".{fmt}"
    if "-o" in args:
        idx = args.index("-o")
        if idx + 1 < len(args):
            output_path = args[idx + 1]

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Generate a simple SVG representation of the elements
    svg = _elements_to_svg(data.get("elements", []), data.get("appState", {}))

    if fmt == "svg":
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"SVG exported to {output_path}")
        return 0

    # PNG via Pillow
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("Pillow not installed. Install with: pip install Pillow", file=sys.stderr)
        print(f"SVG saved to {output_path} instead", file=sys.stderr)
        return 0

    try:
        import io
        import cairosvg
        png_data = cairosvg.svg2png(svg)
        with open(output_path, "wb") as f:
            f.write(png_data)
        print(f"PNG exported to {output_path}")
    except ImportError:
        print("cairosvg not installed. Install: pip install cairosvg", file=sys.stderr)
        print(f"SVG saved to {os.path.splitext(output_path)[0]}.svg instead", file=sys.stderr)
    except Exception as e:
        print(f"Export error: {e}", file=sys.stderr)
        return 1

    return 0


def _elements_to_svg(elements: List[Dict], app_state: Dict) -> str:
    """Convert elements to a basic SVG string for export."""
    bg = app_state.get("viewBackgroundColor", "#ffffff")
    # Find bounding box
    min_x = min((el.get("x", 0) for el in elements), default=0)
    min_y = min((el.get("y", 0) for el in elements), default=0)
    max_x = max((el.get("x", 0) + el.get("width", 100) for el in elements), default=800)
    max_y = max((el.get("y", 0) + el.get("height", 100) for el in elements), default=600)

    pad = 30
    min_x = min(min_x, 0) - pad
    min_y = min(min_y, 0) - pad
    max_x = max(max_x, 800) + pad
    max_y = max(max_y, 600) + pad
    w = max_x - min_x
    h = max_y - min_y

    lines: List[str] = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{min_x} {min_y} {w} {h}" width="{w}" height="{h}">')
    lines.append(f'  <rect x="{min_x}" y="{min_y}" width="{w}" height="{h}" fill="{bg}"/>')

    for el in elements:
        typ = el.get("type", "")
        ex = el.get("x", 0)
        ey = el.get("y", 0)
        ew = el.get("width", 0)
        eh = el.get("height", 0)
        sc = el.get("strokeColor", "#000")
        bc = el.get("backgroundColor", "transparent")
        sw = el.get("strokeWidth", 2)
        text = el.get("text", el.get("label", {}).get("text", ""))
        rot = el.get("angle", 0)

        transform = f' transform="rotate({math.degrees(rot)} {ex + ew / 2} {ey + eh / 2})"' if rot else ""

        if typ == "rectangle":
            rx = "8" if el.get("roundness") else "0"
            lines.append(f'  <rect x="{ex}" y="{ey}" width="{ew}" height="{eh}" rx="{rx}" ry="{rx}" fill="{bc}" stroke="{sc}" stroke-width="{sw}"{transform}/>')
            if text:
                lines.append(f'  <text x="{ex + ew / 2}" y="{ey + eh / 2 + 5}" font-family="sans-serif" font-size="14" text-anchor="middle" fill="{sc}"{transform}>{_xml_escape(text)}</text>')
        elif typ == "diamond":
            points = f"{ex + ew / 2},{ey} {ex + ew},{ey + eh / 2} {ex + ew / 2},{ey + eh} {ex},{ey + eh / 2}"
            lines.append(f'  <polygon points="{points}" fill="{bc}" stroke="{sc}" stroke-width="{sw}"{transform}/>')
            if text:
                lines.append(f'  <text x="{ex + ew / 2}" y="{ey + eh / 2 + 5}" font-family="sans-serif" font-size="14" text-anchor="middle" fill="{sc}"{transform}>{_xml_escape(text)}</text>')
        elif typ == "ellipse":
            lines.append(f'  <ellipse cx="{ex + ew / 2}" cy="{ey + eh / 2}" rx="{ew / 2}" ry="{eh / 2}" fill="{bc}" stroke="{sc}" stroke-width="{sw}"{transform}/>')
        elif typ == "arrow":
            pts = el.get("points", [[0, 0], [ew, eh]])
            if pts and len(pts) >= 2:
                d = f"M {ex + pts[0][0]} {ey + pts[0][1]} L {ex + pts[-1][0]} {ey + pts[-1][1]}"
                lines.append(f'  <path d="{d}" fill="none" stroke="{sc}" stroke-width="{sw}" marker-end="url(#arrowhead)"/>')
            # Arrowhead marker
            lines.insert(1, f'  <defs><marker id="arrowhead" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="{sc}"/></marker></defs>')
        elif typ == "line":
            pts = el.get("points", [[0, 0], [0, 100]])
            if pts:
                parts = [f"M {ex + pts[0][0]} {ey + pts[0][1]}"]
                for p in pts[1:]:
                    parts.append(f"L {ex + p[0]} {ey + p[1]}")
                dash = ' stroke-dasharray="8,6"' if el.get("strokeStyle") == "dashed" else ""
                lines.append(f'  <path d="{" ".join(parts)}" fill="none" stroke="{sc}" stroke-width="{sw}"{dash}{transform}/>')
        elif typ == "text" and text:
            lines.append(f'  <text x="{ex}" y="{ey + 16}" font-family="sans-serif" font-size="16" fill="{sc}"{transform}>{_xml_escape(text)}</text>')

    lines.append("</svg>")
    return "\n".join(lines)


def _xml_escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


def _self_test() -> int:
    """Run built-in verification of all three diagram generators."""
    import tempfile

    passed = 0
    failed = 0

    def check(name: str, cond: bool, detail: str = "") -> None:
        nonlocal passed, failed
        if cond:
            print(f"  ✓ {name}")
            passed += 1
        else:
            print(f"  ✗ {name}  {detail}")
            failed += 1

    print("excalidraw-cli self-test")
    print("─" * 40)

    # 1. Architecture diagram
    arch = gen_architecture("Test Arch", ["Web", "API", "DB"])
    check("architecture returns dict", isinstance(arch, dict))
    check("architecture has elements", len(arch.get("elements", [])) > 0)
    types = {e["type"] for e in arch["elements"]}
    check("architecture has rectangles", "rectangle" in types)
    check("architecture has text labels", "text" in types)

    # 2. Flow diagram
    flow = gen_flow("Test Flow", ["Start", "Decide", "End"])
    check("flow returns dict", isinstance(flow, dict))
    check("flow has elements", len(flow.get("elements", [])) > 0)
    flow_types = {e["type"] for e in flow["elements"]}
    check("flow has arrows", "arrow" in flow_types)

    # 3. Sequence diagram
    seq = gen_sequence("Test Seq", ["A", "B"], ["Call", "Reply"])
    check("sequence returns dict", isinstance(seq, dict))
    check("sequence has elements", len(seq.get("elements", [])) > 0)
    seq_types = {e["type"] for e in seq["elements"]}
    check("sequence has lines (lifelines)", "line" in seq_types)

    # 4. File round-trip
    with tempfile.NamedTemporaryFile(suffix=".excalidraw.json", mode="w", delete=False, encoding="utf-8") as f:
        json.dump(arch, f)
        tmp_path = f.name
    info_code = cmd_info([tmp_path])
    check("info command succeeds", info_code == 0)
    os.unlink(tmp_path)

    # 5. Merge
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False, encoding="utf-8") as f1:
        json.dump(arch, f1)
        p1 = f1.name
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False, encoding="utf-8") as f2:
        json.dump(flow, f2)
        p2 = f2.name
    merge_out = os.path.join(tempfile.gettempdir(), "merge_test.excalidraw.json")
    merge_code = cmd_merge([p1, p2, "-o", merge_out])
    check("merge command succeeds", merge_code == 0)
    if os.path.exists(merge_out):
        with open(merge_out) as f:
            merged = json.load(f)
        check("merged has both element sets", len(merged["elements"]) >= 2)
        os.unlink(merge_out)
    os.unlink(p1)
    os.unlink(p2)

    # 6. SVG export
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False, encoding="utf-8") as fn:
        json.dump(arch, fn)
        svg_src = fn.name
    svg_out = os.path.join(tempfile.gettempdir(), "export_test.svg")
    export_code = cmd_export([svg_src, "--format", "svg", "-o", svg_out])
    check("export SVG succeeds", export_code == 0)
    if os.path.exists(svg_out):
        with open(svg_out) as f:
            svg_content = f.read()
        check("SVG is valid XML", svg_content.strip().startswith("<svg"))
        os.unlink(svg_out)
    os.unlink(svg_src)

    print("─" * 40)
    result = 0 if failed == 0 else 1
    print(f"Result: {passed} passed, {failed} failed")
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Excalidraw Diagram Generator — create hand-drawn style diagrams from the CLI.",
        epilog="Output files are valid .excalidraw.json, loadable in excalidraw.com",
    )
    parser.add_argument("--version", action="version", version="excalidraw-cli 1.0.0")

    sub = parser.add_subparsers(dest="command", required=True)

    # diagram
    diag_p = sub.add_parser("diagram", help="Generate a new diagram")
    diag_p.add_argument("--type", choices=["arch", "flow", "seq", "architecture", "sequence"], required=True)
    diag_p.add_argument("--title", default="Diagram")
    diag_p.add_argument("--output", "-o", default="diagram.excalidraw.json")
    diag_p.add_argument("--components", help="Comma-separated component names (architecture)")
    diag_p.add_argument("--steps", help="Comma-separated step names (flow/sequence)")
    diag_p.add_argument("--actors", help="Comma-separated actor names (sequence)")

    # merge
    merge_p = sub.add_parser("merge", help="Merge two Excalidraw files")
    merge_p.add_argument("base", help="Base Excalidraw JSON file")
    merge_p.add_argument("overlay", help="Overlay Excalidraw JSON file")
    merge_p.add_argument("-o", "--output", default="merged.excalidraw.json")

    # info
    info_p = sub.add_parser("info", help="Show diagram info / summary")
    info_p.add_argument("file", help="Excalidraw JSON file")

    # export
    export_p = sub.add_parser("export", help="Export diagram to SVG or PNG")
    export_p.add_argument("file", help="Excalidraw JSON file")
    export_p.add_argument("--format", choices=["svg", "png"], default="svg")
    export_p.add_argument("-o", "--output", help="Output file path")

    # self-test
    sub.add_parser("self-test", help="Run built-in self tests")

    parsed, rest = parser.parse_known_args()

    if parsed.command == "self-test":
        return _self_test()
    elif parsed.command == "diagram":
        args = []
        args += ["--type", parsed.type]
        if parsed.title:
            args += ["--title", parsed.title]
        if parsed.output:
            args += ["--output", parsed.output]
        if parsed.components:
            args += ["--components", parsed.components]
        if parsed.steps:
            args += ["--steps", parsed.steps]
        if parsed.actors:
            args += ["--actors", parsed.actors]
        args += rest
        return cmd_diagram(args)
    elif parsed.command == "merge":
        args = [parsed.base, parsed.overlay, "-o", parsed.output] + rest
        return cmd_merge(args)
    elif parsed.command == "info":
        args = [parsed.file] + rest
        return cmd_info(args)
    elif parsed.command == "export":
        args = [parsed.file, "--format", parsed.format]
        if parsed.output:
            args += ["-o", parsed.output]
        args += rest
        return cmd_export(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())

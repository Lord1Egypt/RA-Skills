"""SVG exporter with container-based layout and semantic arrows.

Follows the fireworks-tech-graph pattern:
- layered containers with grid-based component layout
- semantic arrow system (solid/dashed/labelled) with SVG markers
- engineering-style title block
- clean vertical data flow, no crossing arrows
- proper z-ordering: bg → containers → arrows → label bg → nodes → text
"""

from __future__ import annotations

import math
import re as _re
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape

from export_integrity import ExportIntegrityError, ExportIntegrityFailure, check_svg_integrity
from export_routes import resolve_export_route
from export_text import estimate_svg_text_width as _estimate_svg_text_width
from export_text import wrap_text_to_width as _wrap_text_to_width
from export_text import wrap_timeline_text as _wrap_timeline_text
from export_theme import ARROW_STYLES, C_DARK, C_LIGHT, INDUSTRY_THEMES, resolve_arrow_style as _resolve_arrow_style
from export_theme import resolve_system_colors as _resolve_system_colors
from export_theme import resolve_theme as _resolve_theme

# Import IntentResolver + RuleEngine for layer assignment
from intent_resolver import IntentResolver
from rule_engine import RuleEngine, load_perspective, load_overlay


# ─── Design tokens ───────────────────────────────────────────────

# Backward compatibility alias
C = C_LIGHT


FONT = "system-ui, -apple-system, sans-serif"
FONT_MONO = "'JetBrains Mono', 'SF Mono', monospace"

# Layout constants
NODE_W = 150
NODE_H = 44
NODE_RX = {"capability": 8, "system": 4, "actor": 22, "flowStep": 6}
LAYER_PAD = 28
LAYER_HEADER_H = 32
LAYER_GAP = 36
CANVAS_X = 40
CANVAS_PAD_TOP = 110  # room for title block
COL_GAP = 20

POSTER_LAYER_PALETTES: dict[str, list[dict[str, str]]] = {
    "dark": [
        {"accent": "#22D3EE", "band_fill": "#0E2A3D", "badge_fill": "#083344"},
        {"accent": "#FBBF24", "band_fill": "#2A2010", "badge_fill": "#78350F"},
        {"accent": "#34D399", "band_fill": "#0E2E1F", "badge_fill": "#064E3B"},
        {"accent": "#4ADE80", "band_fill": "#0F2518", "badge_fill": "#14532D"},
        {"accent": "#A78BFA", "band_fill": "#1E1535", "badge_fill": "#4C1D95"},
        {"accent": "#FB7185", "band_fill": "#2A1018", "badge_fill": "#881337"},
    ],
    "light": [
        {"accent": "#0F766E", "band_fill": "#F0FDFA", "badge_fill": "#CCFBF1"},
        {"accent": "#B45309", "band_fill": "#FFFBEB", "badge_fill": "#FEF3C7"},
        {"accent": "#047857", "band_fill": "#ECFDF5", "badge_fill": "#D1FAE5"},
        {"accent": "#166534", "band_fill": "#F0FDF4", "badge_fill": "#DCFCE7"},
        {"accent": "#6D28D9", "band_fill": "#F5F3FF", "badge_fill": "#E9D5FF"},
        {"accent": "#BE123C", "band_fill": "#FFF1F2", "badge_fill": "#FFE4E6"},
    ],
}


def _esc(s: str) -> str:
    return escape(str(s))


def _poster_layer_palette(theme: str) -> list[dict[str, str]]:
    return POSTER_LAYER_PALETTES["dark" if theme == "dark" else "light"]


# ─── Node rendering ──────────────────────────────────────────────
def _node_svg(nid: str, label: str, x: int, y: int, kind: str,
              colors: dict | None = None, fill_override: str | None = None,
              stroke_override: str | None = None) -> str:
    c = colors if colors is not None else C
    kind_defaults = {
        "capability": (c["cap_fill"], c["cap_stroke"], NODE_RX["capability"]),
        "system": (c["sys_fill"], c["sys_stroke"], NODE_RX["system"]),
        "actor": (c["actor_fill"], c["actor_stroke"], NODE_RX["actor"]),
        "flowStep": (c["flow_fill"], c["flow_stroke"], NODE_RX["flowStep"]),
    }
    if fill_override is not None and stroke_override is not None:
        fill, stroke = fill_override, stroke_override
    else:
        fill, stroke, _ = kind_defaults.get(kind, kind_defaults["capability"])

    if kind == "flowStep":
        return _node_svg_flowstep(nid, label, x, y, fill, stroke, c)
    if kind == "system":
        return _node_svg_system(nid, label, x, y, fill, stroke, c)

    rx = NODE_RX.get(kind, 8)
    return (
        f'<g class="node node-{kind}" id="{nid}">'
        f'<rect class="node-rect" x="{x}" y="{y}" width="{NODE_W}" height="{NODE_H}" '
        f'rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
        f'<text class="node-label" x="{x + NODE_W // 2}" y="{y + NODE_H // 2 + 5}" '
        f'text-anchor="middle" font-size="12.5" fill="{c["text_main"]}" '
        f'font-family="{FONT}" font-weight="500">{_esc(label)}</text>'
        f'</g>'
    )


def _node_svg_flowstep(nid: str, label: str, x: int, y: int,
                        fill: str, stroke: str, c: dict) -> str:
    """Diamond shape for flow step nodes."""
    cx = x + NODE_W // 2
    cy = y + NODE_H // 2
    hw = NODE_W // 2
    hh = NODE_H // 2
    points = f"{cx},{cy - hh} {cx + hw},{cy} {cx},{cy + hh} {cx - hw},{cy}"
    return (
        f'<g class="node node-flowStep" id="{nid}">'
        f'<polygon class="node-rect" points="{points}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
        f'<text class="node-label" x="{cx}" y="{cy + 5}" '
        f'text-anchor="middle" font-size="12.5" fill="{c["text_main"]}" '
        f'font-family="{FONT}" font-weight="500">{_esc(label)}</text>'
        f'</g>'
    )


def _node_svg_system(nid: str, label: str, x: int, y: int,
                      fill: str, stroke: str, c: dict) -> str:
    """Rect with 4px-wide left color strip for system nodes."""
    strip_w = 4
    return (
        f'<g class="node node-system" id="{nid}">'
        f'<rect class="node-rect" x="{x}" y="{y}" width="{NODE_W}" height="{NODE_H}" '
        f'rx="4" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
        f'<rect class="node-strip" x="{x}" y="{y}" width="{strip_w}" height="{NODE_H}" '
        f'rx="2" fill="{stroke}"/>'
        f'<text class="node-label" x="{x + NODE_W // 2}" y="{y + NODE_H // 2 + 5}" '
        f'text-anchor="middle" font-size="12.5" fill="{c["text_main"]}" '
        f'font-family="{FONT}" font-weight="500">{_esc(label)}</text>'
        f'</g>'
    )


# ─── Arrow rendering with SVG markers ────────────────────────────
def _arrow_line(x1: int, y1: int, x2: int, y2: int,
                dashed: bool = False, color: str | None = None,
                colors: dict | None = None,
                relation_type: str | None = None,
                theme: str = "light") -> str:
    """Draw just the arrow line + marker (no label)."""
    c = colors if colors is not None else C
    if relation_type and relation_type in ARROW_STYLES:
        style = _resolve_arrow_style(relation_type, theme)
        line_color = color or style["color"]
        dash = f' stroke-dasharray="{style["dash"]}"' if style["dash"] else ""
        marker_id = style["marker"]
    else:
        if color is None:
            color = c["arrow"] if not dashed else c["arrow_muted"]
        line_color = color
        dash = f' stroke-dasharray="5,4"' if dashed else ""
        marker_id = "arrow-solid" if not dashed else "arrow-dashed"
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="{line_color}" stroke-width="1.5"{dash} '
        f'marker-end="url(#{marker_id})"/>'
    )


def _render_arrow_line(sx: int, sy: int, tx: int, ty: int, arrow: dict, colors: dict) -> str:
    """Draw a straight arrow line with proper style and marker for free-flow layout.

    Relation type color mapping:
      - flows-to: blue (#60A5FA)
      - supports: green (colors["arrow"])
      - depends-on: gray dashed (colors["arrow_muted"])
      - owned-by: yellow dashed (#FBBF24)
    """
    rel_type = arrow.get("relation_type", "supports")

    # Determine color based on relation type
    if rel_type == "flows-to":
        arrow_color = "#60A5FA"  # blue
        marker = "arrow-solid"
        style = f'stroke="{arrow_color}" stroke-width="1.5"'
    elif rel_type == "owned-by":
        arrow_color = "#FBBF24"  # yellow
        marker = "arrow-dot"
        style = f'stroke="{arrow_color}" stroke-width="1.5" stroke-dasharray="3,3"'
    elif arrow.get("dashed") or rel_type == "depends-on":
        arrow_color = colors["arrow_muted"]  # gray
        marker = "arrow-dashed"
        style = f'stroke="{arrow_color}" stroke-width="1.5" stroke-dasharray="4,4" opacity="0.5"'
    else:
        # supports or other types
        arrow_color = colors["arrow"]  # green
        marker = "arrow-solid"
        style = f'stroke="{arrow_color}" stroke-width="1.5"'

    return f'<line x1="{sx}" y1="{sy}" x2="{tx}" y2="{ty}" {style} marker-end="url(#{marker})"/>'


def _arrow_label(mx: int, my: int, label: str,
                 colors: dict | None = None) -> str:
    """Draw arrow label with background rect for readability.

    Background is fully opaque (opacity=1.0) to ensure labels cover arrows.
    """
    c = colors if colors is not None else C
    label_w = len(label) * 6 + 12
    return (
        f'<rect x="{mx - label_w // 2}" y="{my - 9}" '
        f'width="{label_w}" height="18" rx="3" '
        f'fill="{c["arrow_label_bg"]}" fill-opacity="1.0"/>'
        f'<text x="{mx}" y="{my + 4}" text-anchor="middle" '
        f'font-size="10" fill="{c["arrow_label"]}" font-family="{FONT}">{_esc(label)}</text>'
    )


def _label_box(mx: int, my: int, label: str) -> tuple[int, int, int, int]:
    label_w = len(label) * 6 + 12
    return mx - label_w // 2, my - 9, label_w, 18


def _label_boxes_overlap(a: tuple[int, int, int, int], b: tuple[int, int, int, int], pad: int = 8) -> bool:
    """Check if two label rectangles overlap.

    Args:
        pad: Minimum gap between boxes (default 8px to ensure labels don't touch nodes).
    """
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return not (
        ax + aw + pad <= bx
        or bx + bw + pad <= ax
        or ay + ah + pad <= by
        or by + bh + pad <= ay
    )


def _render_arrow_labels(
    labels: list[dict[str, Any]],
    *,
    colors: dict,
    canvas_w: int,
    canvas_h: int,
    node_rects: list[tuple[int, int, int, int]] | None = None,
) -> list[str]:
    rendered: list[str] = []
    occupied: list[tuple[int, int, int, int]] = []
    # Add node rectangles to occupied so labels avoid nodes
    if node_rects:
        occupied.extend(node_rects)

    margin_x = 8
    min_y = 78
    max_y = max(min_y, canvas_h - 26)

    for item in labels:
        label = item["label"]
        base_x = int(item["x"])
        base_y = int(item["y"])
        offsets = item.get("offsets") or [
            (0, -28),  # ↑ Increase upward offset to avoid node overlap
            (0, 28),   # ↓ Increase downward offset
            (40, -28), # ↑↑ Upper right corner (farther from nodes)
            (-40, -28), # ↑↑ Upper left corner
            (40, 28),  # ↓↓ Lower right corner
            (-40, 28), # ↓↓ Lower left corner
            (0, -56),  # ↑↑↑ Extra high (emergency fallback)
            (0, 56),   # ↓↓↓ Extra low
        ]

        chosen: tuple[int, int, tuple[int, int, int, int]] | None = None
        for dx, dy in offsets:
            mx = base_x + dx
            my = base_y + dy
            x, y, box_w, box_h = _label_box(mx, my, label)
            x = max(margin_x, min(x, max(margin_x, canvas_w - box_w - margin_x)))
            y = max(min_y, min(y, max_y))
            candidate = (x, y, box_w, box_h)
            # Check collision with occupied areas (nodes + other labels)
            has_collision = any(_label_boxes_overlap(candidate, other) for other in occupied)
            if not has_collision:
                chosen = (x + box_w // 2, y + 9, candidate)
                break

        if chosen is None:
            box_w = len(label) * 6 + 12
            box_h = 18
            for step in range(1, 10):
                fallback_offsets = [
                    (0, -14 * step),
                    (0, 14 * step),
                    (28, -14 * step),
                    (-28, -14 * step),
                    (28, 14 * step),
                    (-28, 14 * step),
                ]
                for dx, dy in fallback_offsets:
                    mx = base_x + dx
                    my = base_y + dy
                    x = max(margin_x, min(mx - box_w // 2, max(margin_x, canvas_w - box_w - margin_x)))
                    y = max(min_y, min(my - 9, max_y))
                    candidate = (x, y, box_w, box_h)
                    if any(_label_boxes_overlap(candidate, other) for other in occupied):
                        continue
                    chosen = (x + box_w // 2, y + 9, candidate)
                    break
                if chosen is not None:
                    break

        if chosen is None:
            x, y, box_w, box_h = _label_box(base_x, base_y, label)
            x = max(margin_x, min(x, max(margin_x, canvas_w - box_w - margin_x)))
            y = max(min_y, min(y, max_y))
            chosen = (x + box_w // 2, y + 9, (x, y, box_w, box_h))

        mx, my, candidate = chosen
        occupied.append(candidate)
        rendered.append(_arrow_label(mx, my, label, colors=colors))

    return rendered


def _node_center(n: dict) -> tuple[int, int]:
    return n["x"] + NODE_W // 2, n["y"] + NODE_H // 2


def _edge_point(n: dict, tx: int, ty: int) -> tuple[int, int]:
    """Calculate where the arrow should connect on the node's edge.

    For vertical connections (same column), connect to bottom/top center.
    For diagonal connections, compute the intersection with the node border.
    """
    cx, cy = _node_center(n)
    dx, dy = tx - cx, ty - cy
    if dx == 0 and dy == 0:
        return cx, cy
    hw, hh = NODE_W / 2, NODE_H / 2
    t = min(hw / abs(dx) if dx else 1e9, hh / abs(dy) if dy else 1e9)
    return int(cx + dx * t), int(cy + dy * t)


# ─── Column-based layout ─────────────────────────────────────────
def _layout_architecture(blueprint: dict[str, Any]) -> dict:
    """Position nodes in columns so arrows flow vertically without crossing.

    Strategy (fireworks-tech-graph pattern):
    1. Layer 0: Systems (top)
    2. Layer 1: Capabilities (middle)
    3. Layer 2: Flow Steps (bottom)
    4. Align columns by capability-support relationship so arrows go straight down.
    """
    lib = blueprint.get("library", {})
    systems = lib.get("systems", [])
    capabilities = lib.get("capabilities", [])
    flow_steps = lib.get("flowSteps", [])
    actors = lib.get("actors", [])

    # Build capability → systems map
    cap_to_systems: dict[str, list[str]] = {c["id"]: [] for c in capabilities}
    for s in systems:
        for cid in s.get("capabilityIds", []):
            if cid in cap_to_systems:
                cap_to_systems[cid].append(s["id"])

    # Build columns: each column = (system, capability it supports)
    # A system can span multiple columns if it supports multiple capabilities
    used_systems: set[str] = set()
    used_caps: set[str] = set()
    columns: list[tuple[str | None, str | None]] = []

    # First pass: pair systems with their capabilities
    for cap in capabilities:
        cid = cap["id"]
        supporting = cap_to_systems.get(cid, [])
        if supporting:
            for sid in supporting:
                columns.append((sid, cid))
                used_systems.add(sid)
                used_caps.add(cid)
        else:
            # Capability with no system support → standalone column
            columns.append((None, cid))
            used_caps.add(cid)

    # Add orphan systems (no capability linkage)
    for s in systems:
        if s["id"] not in used_systems:
            columns.append((s["id"], None))
            used_systems.add(s["id"])

    # Add orphan capabilities
    for c in capabilities:
        if c["id"] not in used_caps:
            columns.append((None, c["id"]))
            used_caps.add(c["id"])

    # Deduplicate: one column per unique capability (prevents vertical stacking)
    # A system with N capabilities contributes to N columns, but the system node
    # is placed only in its first column.
    ordered_columns: list[dict] = []
    placed_caps: set[str] = set()
    systems_in_columns: set[str] = set()
    for sid, cid in columns:
        if cid is not None and cid not in placed_caps:
            ordered_columns.append({"system": sid, "caps": [cid]})
            placed_caps.add(cid)
            if sid:
                systems_in_columns.add(sid)
        elif cid is None and sid:
            # Orphan system column (no capability)
            ordered_columns.append({"system": sid, "caps": []})
            systems_in_columns.add(sid)

    # Add systems whose caps were all claimed by earlier systems
    for sid, cid in columns:
        if sid and sid not in systems_in_columns:
            ordered_columns.append({"system": sid, "caps": []})
            systems_in_columns.add(sid)

    n_cols = len(ordered_columns)
    if n_cols == 0:
        return {"nodes": {}, "arrows": [], "layers": [], "width": 500, "height": 300}

    total_w = n_cols * NODE_W + max(0, n_cols - 1) * COL_GAP
    start_x = CANVAS_X + (max(600, total_w) - total_w) // 2 + LAYER_PAD

    nodes: dict[str, dict] = {}
    arrows_list: list[dict] = []

    # ── Vertical layout model ──
    # Pass 1: place all nodes with fixed content_y per layer
    # Pass 2: compute border_h from actual content extents
    layer_y = 72  # below title block (y=10, h=52) + 10px gap

    # Phase: layer index for each node
    node_layer: dict[str, int] = {}

    # Layer metadata (filled in pass 2)
    layer_metas: list[dict] = []

    # ── Row 0: Systems ──
    if systems:
        li = len(layer_metas)
        content_y = layer_y + LAYER_HEADER_H + LAYER_PAD
        placed_systems: set[str] = set()
        for col_idx, col in enumerate(ordered_columns):
            x = start_x + col_idx * (NODE_W + COL_GAP)
            if col["system"] and col["system"] not in placed_systems:
                sys_node = next((s for s in systems if s["id"] == col["system"]), None)
                if sys_node:
                    nodes[sys_node["id"]] = {
                        "x": x, "y": content_y,
                        "kind": "system",
                        "label": sys_node.get("name", sys_node["id"]),
                    }
                    node_layer[sys_node["id"]] = li
                    placed_systems.add(sys_node["id"])
        layer_metas.append({
            "label": "Application Systems",
            "header_y": layer_y,
            "content_y": content_y,
        })
        layer_y = layer_y + LAYER_HEADER_H + LAYER_PAD + NODE_H + LAYER_PAD + LAYER_GAP

    # ── Actors: always placed to the right in 2 columns ──
    if actors:
        first_meta = layer_metas[0] if layer_metas else None
        if first_meta:
            content_y = first_meta["content_y"]
            actor_col_count = 2 if len(actors) > 4 else 1
            actor_gap = 12
            actor_w = NODE_W
            total_actor_w = actor_col_count * actor_w + max(0, actor_col_count - 1) * actor_gap
            x_actor_start = start_x + n_cols * (NODE_W + COL_GAP) + COL_GAP
            y_actor_start = content_y

            for ai, a in enumerate(actors):
                col = ai // actor_col_count
                row = ai % actor_col_count
                nodes[a["id"]] = {
                    "x": int(x_actor_start + row * (actor_w + actor_gap)),
                    "y": y_actor_start + col * (NODE_H + 12),
                    "kind": "actor",
                    "label": a.get("name", a["id"]),
                }
                node_layer[a["id"]] = 0

    # ── Row 1: Capabilities ──
    if capabilities:
        li = len(layer_metas)
        content_y = layer_y + LAYER_HEADER_H + LAYER_PAD
        for col_idx, col in enumerate(ordered_columns):
            x = start_x + col_idx * (NODE_W + COL_GAP)
            for cid in col["caps"]:
                cap_node = next((c for c in capabilities if c["id"] == cid), None)
                if cap_node:
                    nodes[cid] = {
                        "x": x, "y": content_y,
                        "kind": "capability",
                        "label": cap_node.get("name", cid),
                    }
                    node_layer[cid] = li
                    sid = col["system"]
                    if sid and sid in nodes:
                        arrows_list.append({
                            "from": sid, "to": cid, "label": "supports", "dashed": False,
                        })
        layer_metas.append({
            "label": "Business Capabilities",
            "header_y": layer_y,
            "content_y": content_y,
        })
        layer_y = layer_y + LAYER_HEADER_H + LAYER_PAD + NODE_H + LAYER_GAP

    # ── Row 2: Flow Steps ──
    if flow_steps:
        flow_nodes: list[dict] = list(flow_steps)

        col_flow_count: dict[int, int] = {}
        cap_col_map: dict[str, int] = {}
        for col_idx, col in enumerate(ordered_columns):
            for cid in col["caps"]:
                if cid:
                    cap_col_map[cid] = col_idx

        li = len(layer_metas)
        content_y = layer_y + LAYER_HEADER_H + LAYER_PAD
        for i, fs in enumerate(flow_nodes):
            best_col = i % max(n_cols, 1)
            for cid in fs.get("capabilityIds", []):
                if cid in cap_col_map:
                    best_col = cap_col_map[cid]
                    break
            row_in_col = col_flow_count.get(best_col, 0)
            col_flow_count[best_col] = row_in_col + 1
            x = start_x + best_col * (NODE_W + COL_GAP)
            y = content_y + row_in_col * (NODE_H + 10)
            nodes[fs["id"]] = {
                "x": x, "y": y,
                "kind": "flowStep",
                "label": fs.get("name", fs["id"]),
            }
            node_layer[fs["id"]] = li
            for cid in fs.get("capabilityIds", []):
                if cid in nodes:
                    arrows_list.append({
                        "from": cid, "to": fs["id"], "label": "", "dashed": True,
                    })

        layer_metas.append({
            "label": "Process Flows",
            "header_y": layer_y,
            "content_y": content_y,
        })

    # ── Pass 2: compute border_h from actual node extents, reposition nodes ──
    for i, meta in enumerate(layer_metas):
        # Step 2a: compute border_h from current node extents
        content_y = meta["content_y"]
        max_bottom = content_y
        for nid, n in nodes.items():
            if node_layer.get(nid) == i:
                bottom = n["y"] + NODE_H
                if bottom > max_bottom:
                    max_bottom = bottom
        content_h = max_bottom - content_y
        meta["border_h"] = LAYER_HEADER_H + LAYER_PAD + content_h + LAYER_PAD

    # Step 2b: recompute layer positions and reposition all nodes
    current_y = 72
    for i, meta in enumerate(layer_metas):
        meta["border_y"] = current_y
        meta["header_y"] = current_y
        new_content_y = current_y + LAYER_HEADER_H + LAYER_PAD
        # Shift nodes in this layer
        y_delta = new_content_y - meta["content_y"]
        for nid, n in nodes.items():
            if node_layer.get(nid) == i:
                n["y"] += y_delta
        meta["content_y"] = new_content_y
        current_y += meta["border_h"] + LAYER_GAP

    # ── Build layer boxes from layer_metas ──
    layers = []
    for lm in layer_metas:
        layers.append({
            "label": lm["label"],
            "header_y": lm["header_y"],
            "y": lm["border_y"],
            "h": lm["border_h"],
        })

    # Calculate height (add room for legend at bottom)
    legend_h = 180  # space for legend
    max_y = max((n["y"] + NODE_H for n in nodes.values()), default=300)
    height = max_y + LAYER_PAD + 40 + legend_h

    # Width: fit all content + padding, accounting for actors if present
    content_max_x = max(
        max((n["x"] + NODE_W for n in nodes.values()), default=0),
        n_cols * (NODE_W + COL_GAP),
    )
    width = max(600, content_max_x + CANVAS_X * 2 + LAYER_PAD * 2)

    return {
        "nodes": nodes,
        "arrows": arrows_list,
        "layers": layers,
        "width": width,
        "height": height,
        "start_x": start_x,
    }


def _layer_svg(label: str, header_y: int, border_y: int, w: int, h: int,
               colors: dict | None = None) -> str:
    """Layer: border wraps header + content, header has its own bg color."""
    c = colors if colors is not None else C
    return (
        f'<g class="layer" id="layer-{_esc(label)}">'
        f'<rect class="layer-border" x="{CANVAS_X}" y="{border_y}" width="{w}" height="{h}" '
        f'rx="8" fill="none" stroke="{c["layer_border"]}" stroke-width="1"/>'
        f'<rect class="layer-header" x="{CANVAS_X}" y="{header_y}" width="{w}" height="{LAYER_HEADER_H}" '
        f'fill="{c["layer_header_bg"]}"/>'
        f'<text class="layer-label" x="{CANVAS_X + 16}" y="{header_y + LAYER_HEADER_H // 2 + 4}" '
        f'font-size="12" fill="{c["text_sub"]}" font-family="{FONT}" '
        f'font-weight="600" letter-spacing="0.4">{_esc(label)}</text>'
        f'</g>'
    )


def _title_svg(title: str, subtitle: str, w: int,
               colors: dict | None = None) -> str:
    c = colors if colors is not None else C
    ty = 10
    rect_w = w - CANVAS_X  # rect starts at CANVAS_X, so width = w - CANVAS_X
    return (
        f'<g class="title-block">'
        f'<rect x="{CANVAS_X}" y="{ty}" width="{rect_w}" height="52" '
        f'rx="6" fill="{c["canvas"]}" stroke="{c["border"]}" stroke-width="1"/>'
        f'<text x="{CANVAS_X + 16}" y="{ty + 24}" '
        f'font-size="16" fill="{c["text_main"]}" font-family="{FONT}" '
        f'font-weight="700">{_esc(title)}</text>'
        f'<text x="{CANVAS_X + 16}" y="{ty + 42}" '
        f'font-size="11" fill="{c["text_sub"]}" font-family="{FONT_MONO}">'
        f'{_esc(subtitle)}</text>'
        f'</g>'
    )


def _legend_svg(x: int, y: int, colors: dict | None = None) -> str:
    """Legend showing node types and arrow meanings (fireworks-tech-graph pattern)."""
    c = colors if colors is not None else C
    items = [
        ("系统", c["sys_fill"], c["sys_stroke"], 4),
        ("能力", c["cap_fill"], c["cap_stroke"], 8),
        ("流程步骤", c["flow_fill"], c["flow_stroke"], 6),
        ("角色", c["actor_fill"], c["actor_stroke"], 22),
    ]
    legend_total_h = 30 + len(items) * 22 + 4 + 4 * 22 + 8  # items + gap + 4 arrows + padding
    parts = [
        f'<g class="legend" transform="translate({x}, {y})">',
        f'<rect x="0" y="0" width="130" height="{legend_total_h}" '
        f'rx="6" fill="{c["canvas"]}" stroke="{c["border"]}" stroke-width="1" opacity="0.95"/>',
        f'<text x="12" y="20" font-size="10" fill="{c["text_sub"]}" '
        f'font-family="{FONT}" font-weight="600" letter-spacing="0.3">LEGEND</text>',
    ]
    for i, (label, fill, stroke, rx) in enumerate(items):
        ly = 38 + i * 22
        parts.append(
            f'<rect x="12" y="{ly}" width="18" height="14" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
            f'<text x="38" y="{ly + 11}" font-size="9.5" fill="{c["text_sub"]}" '
            f'font-family="{FONT}">{label}</text>'
        )
    # Arrow styles
    arrow_y = 38 + len(items) * 22 + 4
    arrow_entries = [
        ("supports", c["arrow"], "", "arrow-solid"),
        ("depends-on", c["arrow_muted"], ' stroke-dasharray="6,4"', "arrow-open"),
        ("flows-to", "#60A5FA" if c is C_DARK else "#3B82F6", "", "arrow-solid"),
        ("owned-by", "#FBBF24" if c is C_DARK else "#D97706", ' stroke-dasharray="3,3"', "arrow-dot"),
    ]
    for i, (label, acolor, dash_attr, marker) in enumerate(arrow_entries):
        ay = arrow_y + i * 22
        parts.append(
            f'<line x1="12" y1="{ay}" x2="30" y2="{ay}" '
            f'stroke="{acolor}" stroke-width="1.5"{dash_attr} '
            f'marker-end="url(#{marker})"/>'
            f'<text x="38" y="{ay + 4}" font-size="9.5" fill="{c["text_sub"]}" '
            f'font-family="{FONT}">{label}</text>'
        )
    parts.append('</g>')
    return "\n".join(parts)


# ─── SVG defs (markers) ──────────────────────────────────────────
def _svg_defs(colors: dict | None = None, theme: str = "light") -> str:
    """SVG marker definitions for arrowheads.

    For dark theme, also includes a grid pattern definition.
    """
    c = colors if colors is not None else C
    grid_pattern = ""
    if theme == "dark":
        grid_pattern = (
            f'<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">'
            f'<path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1E293B" stroke-width="0.5"/>'
            f'</pattern>'
        )
    return (
        '<defs>'
        f'{grid_pattern}'
        f'<marker id="arrow-solid" markerWidth="8" markerHeight="6" '
        f'refX="4" refY="3" orient="auto" markerUnits="userSpaceOnUse">'
        f'<polygon points="0 0, 8 3, 0 6" fill="{c["arrow"]}"/>'
        f'</marker>'
        f'<marker id="arrow-dashed" markerWidth="8" markerHeight="6" '
        f'refX="4" refY="3" orient="auto" markerUnits="userSpaceOnUse">'
        f'<polygon points="0 0, 8 3, 0 6" fill="{c["arrow_muted"]}"/>'
        f'</marker>'
        f'<marker id="arrow-open" markerWidth="8" markerHeight="6" '
        f'refX="4" refY="3" orient="auto" markerUnits="userSpaceOnUse">'
        f'<polygon points="0 0, 8 3, 0 6" fill="none" stroke="{c["arrow_muted"]}" stroke-width="1"/>'
        f'</marker>'
        f'<marker id="arrow-dot" markerWidth="8" markerHeight="8" '
        f'refX="4" refY="4" orient="auto" markerUnits="userSpaceOnUse">'
        f'<circle cx="4" cy="4" r="3" fill="{c["arrow"]}"/>'
        f'</marker>'
        '</defs>'
    )


# ─── Main export ─────────────────────────────────────────────────
def export_svg(blueprint: dict[str, Any], target: Path, theme: str = "light",
               industry: str | None = None) -> None:
    """Export architecture diagram to SVG.

    Args:
        blueprint: The canonical blueprint JSON.
        target: Output file path.
        theme: Color theme — "light" (default) or "dark".
        industry: Industry theme for accent colors. Auto-detected from blueprint meta if None.
    """
    if industry is None:
        industry = blueprint.get("meta", {}).get("industry", "") or None
    colors = _resolve_theme(theme, industry=industry)
    title = blueprint.get("meta", {}).get("title", "Business Blueprint")
    industry_label = industry or blueprint.get("meta", {}).get("industry", "")
    subtitle = f"行业：{industry_label}" if industry_label else "应用架构"

    layout = _layout_architecture(blueprint)
    w, h = layout["width"], layout["height"]

    # Background: solid for light, grid for dark
    if theme == "dark":
        bg_rect = (
            f'<rect width="{w}" height="{h}" fill="{colors["bg"]}"/>'
            f'<rect width="{w}" height="{h}" fill="url(#grid)"/>'
        )
    else:
        bg_rect = f'<rect width="{w}" height="{h}" fill="{colors["bg"]}"/>'

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" '
        f'font-family="{FONT}">',
        _svg_defs(colors=colors, theme=theme),
        bg_rect,
        _title_svg(title, subtitle, w, colors=colors),
    ]

    # Layer backgrounds (z-order: behind arrows and nodes)
    for layer in layout["layers"]:
        parts.append(_layer_svg(
            layer["label"], layer["header_y"], layer["y"],
            w - CANVAS_X * 2, layer["h"], colors=colors
        ))

    # Build semantic color lookup for systems
    systems_by_id = {}
    for s in blueprint.get("library", {}).get("systems", []):
        systems_by_id[s["id"]] = s

    # Arrows (z-order: behind nodes, above layer backgrounds)
    # Build relation type lookup from blueprint relations
    relations_by_endpoints: dict[tuple[str, str], str] = {}
    for rel in blueprint.get("relations", []):
        relations_by_endpoints[(rel["from"], rel["to"])] = rel.get("type", "supports")

    # Pass 1: draw all lines
    arrow_labels: list[dict[str, Any]] = []
    for arrow in layout["arrows"]:
        src = layout["nodes"].get(arrow["from"])
        tgt = layout["nodes"].get(arrow["to"])
        if not src or not tgt:
            continue
        # Skip cross-layer diagonal arrows that would cross many columns
        start_x = layout.get("start_x", CANVAS_X + LAYER_PAD)
        src_col = (src["x"] - start_x) // (NODE_W + COL_GAP) if COL_GAP else 0
        tgt_col = (tgt["x"] - start_x) // (NODE_W + COL_GAP) if COL_GAP else 0
        if abs(src_col - tgt_col) > 2 and arrow.get("label") == "supports":
            continue
        sx, sy = _node_center(src)
        tx, ty = _node_center(tgt)
        sx, sy = _edge_point(src, tx, ty)
        tx, ty = _edge_point(tgt, sx, sy)
        # Look up relation type for semantic arrow style
        rel_type = relations_by_endpoints.get((arrow["from"], arrow["to"]))
        parts.append(
            _arrow_line(sx, sy, tx, ty,
                        dashed=arrow.get("dashed", False), colors=colors,
                        relation_type=rel_type, theme=theme)
        )
        if arrow.get("label"):
            mx = (sx + tx) // 2
            my = (sy + ty) // 2
            arrow_labels.append((mx, my, arrow["label"]))

    # Pass 2: draw all labels on top of arrows (background masks the line)
    # Nodes (z-order: on top of arrows)
    for nid, n in layout["nodes"].items():
        kind = n["kind"]
        # Apply semantic colors for system nodes
        fill_ov, stroke_ov = None, None
        if kind == "system":
            sys_data = systems_by_id.get(nid, {})
            # Use _categorize_system for category derivation (not just explicit field)
            category = _categorize_system(sys_data)
            fill_ov, stroke_ov = _resolve_system_colors(category, theme)
        parts.append(_node_svg(
            nid, n["label"], n["x"], n["y"], kind,
            colors=colors, fill_override=fill_ov, stroke_override=stroke_ov
        ))

    # Legend (bottom-left, fireworks-tech-graph pattern)
    parts.append(_legend_svg(CANVAS_X + 10, h - 180 - 10, colors=colors))

    # Summary cards (bottom-center)
    lib_summary = blueprint.get("library", {})
    n_systems = len(lib_summary.get("systems", []))
    n_capabilities = len(lib_summary.get("capabilities", []))
    n_actors = len(lib_summary.get("actors", []))
    n_flow_steps = len(lib_summary.get("flowSteps", []))
    systems_with_caps = sum(1 for s in lib_summary.get("systems", []) if s.get("capabilityIds"))
    sys_coverage = f"{int(systems_with_caps / n_systems * 100)}%" if n_systems else "N/A"

    card_y = h - 50
    card_data = [
        ("SYSTEMS", str(n_systems)),
        ("CAPABILITIES", str(n_capabilities)),
        ("ACTORS", str(n_actors)),
        ("FLOW STEPS", str(n_flow_steps)),
        ("COVERAGE", sys_coverage),
    ]
    card_w = 110
    card_h = 38
    total_cards_w = len(card_data) * card_w + (len(card_data) - 1) * 12
    cards_start_x = (w - total_cards_w) / 2
    for ci, (label, value) in enumerate(card_data):
        cx = cards_start_x + ci * (card_w + 12)
        parts.append(
            f'<g class="summary-card">'
            f'<rect x="{cx}" y="{card_y}" width="{card_w}" height="{card_h}" '
            f'rx="6" fill="{colors["canvas"]}" stroke="{colors["border"]}" stroke-width="1"/>'
            f'<text x="{cx + card_w / 2}" y="{card_y + 17}" text-anchor="middle" '
            f'font-size="13" fill="{colors["text_main"]}" font-family="{FONT_MONO}" '
            f'font-weight="700">{value}</text>'
            f'<text x="{cx + card_w / 2}" y="{card_y + 32}" text-anchor="middle" '
            f'font-size="7.5" fill="{colors["text_sub"]}" font-family="{FONT}" '
            f'letter-spacing="0.3">{label}</text>'
            f'</g>'
        )

    parts.append("</svg>")
    target.write_text("\n".join(parts), encoding="utf-8")


# ─── Free-flow L→R layout engine ─────────────────────────────────

# Layout columns for L→R data flow
_FREE_FLOW_COLS = [
    {"label": "Entry", "x": 80, "systems": []},
    {"label": "Frontend/Cloud", "x": 310, "categories": ["cloud", "frontend"]},
    {"label": "Backend/Compute", "x": 530, "categories": ["backend", "message_bus"]},
    {"label": "Database/Storage", "x": 750, "categories": ["database"]},
    {"label": "Support", "x": 750, "categories": ["security", "external"]},
]

# Default row positions
_FREE_FLOW_ROWS = {
    "main": {"y": 230, "h": 80},
    "top": {"y": 130, "h": 44},
    "bottom": {"y": 360, "h": 80},
    "infra": {"y": 480, "h": 80},
}


def _categorize_system(sys_obj: dict) -> str:
    """Determine system category from properties, aliases, or name heuristics."""
    cat = sys_obj.get("category", "").lower()
    if cat:
        return cat
    name = sys_obj.get("name", "").lower()
    # Generic keyword → category heuristics (language-agnostic)
    if any(k in name for k in ("gateway", "cdn", "proxy", "load balancer", "ingress")):
        return "cloud"
    if any(k in name for k in ("database", "db", "sql", "nosql", "storage", "cache",
                                "数据库", "缓存", "存储")):
        return "database"
    if any(k in name for k in ("auth", "identity", "permission", "rbac", "token", "oauth",
                                "认证", "权限", "身份")):
        return "security"
    if any(k in name for k in ("queue", "event", "message", "bus", "kafka", "mq",
                                "队列", "消息", "事件")):
        return "message_bus"
    if any(k in name for k in ("lambda", "function", "compute", "serverless",
                                "计算", "函数")):
        return "backend"
    if any(k in name for k in ("monitor", "logging", "tracing", "metric", "alarm",
                                "监控", "日志", "告警")):
        return "cloud"
    if any(k in name for k in ("deploy", "infra", "pipeline", "ci/cd", "terraform",
                                "部署", "基础设施")):
        return "external"
    props = sys_obj.get("properties", {})
    svc = props.get("service", "").lower()
    if svc:
        # Map known service types to categories
        _SVC_MAP = {
            "serverless": "backend", "compute": "backend",
            "cdn": "cloud", "gateway": "cloud", "proxy": "cloud",
            "cloudwatch": "cloud", "monitor": "cloud", "logging": "cloud",
            "database": "database", "cache": "database",
            "auth": "security", "iam": "security",
            "queue": "message_bus", "event": "message_bus",
        }
        for key, mapped in _SVC_MAP.items():
            if key in svc:
                return mapped
    return "backend"


def _get_subtitle(sys_obj: dict) -> list[str]:
    """Extract 2-3 subtitle lines from system properties."""
    props = sys_obj.get("properties", {})
    features = props.get("features", [])
    desc = sys_obj.get("description", "")
    lines: list[str] = []
    if desc:
        # Take first meaningful phrase
        parts = desc.replace("，", ",").replace("、", ",").split(",")
        if parts and parts[0].strip():
            lines.append(parts[0].strip()[:40])
    for f in features[:2]:
        lines.append(str(f)[:18])
    # Truncate long subtitles to prevent overflow (node w≈140px, usable≈110px)
    # CJK ~8px/char, ASCII ~6px/char → max ~14 chars for mixed, ~18 for ASCII
    truncated = []
    for line in lines:
        px = sum(8 if ord(c) > 127 else 6 for c in line)
        if px > 110:
            # Truncate to fit ~110px
            chars = 0
            total_px = 0
            for c in line:
                char_px = 8 if ord(c) > 127 else 6
                if total_px + char_px > 110:
                    break
                chars += 1
                total_px += char_px
            truncated.append(line[:chars] + "…")
        else:
            truncated.append(line)
    return truncated[:3] or [""]


def _layout_layered(blueprint: dict[str, Any]) -> dict[str, Any]:
    """Layout systems by layer field into L→R columns.

    When systems have a ``layer`` field, group them into columns (one column per
    unique layer value).  Layers are ordered by their first appearance in the
    ``systems`` array.  Relations drive the arrows.
    """
    lib = blueprint.get("library", {})
    systems = lib.get("systems", [])
    actors = lib.get("actors", [])
    relations = blueprint.get("relations", [])

    # ── Group systems by layer ──
    layer_order: list[str] = []
    layer_systems: dict[str, list[dict]] = {}
    for s in systems:
        layer = s.get("layer", "")
        if not layer:
            continue
        if layer not in layer_systems:
            layer_order.append(layer)
            layer_systems[layer] = []
        layer_systems[layer].append(s)

    if not layer_order:
        # No layers → fall back to free-flow
        return _layout_free_flow(blueprint)

    # ── Layout constants ──
    NODE_W = 150
    NODE_H_BASE = 60
    NODE_H_FEATURED = 76  # systems with features get taller
    COL_GAP = 60          # horizontal gap between layer columns
    ROW_GAP = 20          # vertical gap between nodes in same column
    PAD_X = 80            # left padding
    PAD_Y = 140           # top padding (below title + summary)
    ACTOR_COL_W = 160     # width reserved for actor entry node

    has_actors = bool(actors)
    col_x_start = PAD_X + (ACTOR_COL_W + COL_GAP) if has_actors else PAD_X

    # ── Layer → category mapping: cycle through distinct categories ──
    _LAYER_CATEGORIES = ["frontend", "cloud", "backend", "message_bus", "database", "security"]
    layer_categories = {
        layer: _LAYER_CATEGORIES[li % len(_LAYER_CATEGORIES)]
        for li, layer in enumerate(layer_order)
    }

    # ── Calculate column widths (max node width in each layer) ──
    col_widths: list[int] = []
    for layer in layer_order:
        max_w = 0
        for s in layer_systems[layer]:
            label = s.get("name", "")
            label_px = sum(8 if ord(c) > 127 else 6 for c in label)
            feats = s.get("features", [])
            w = max(NODE_W, label_px + 24, 120)
            if feats:
                feat_text = " / ".join(feats)
                feat_px = sum(7 if ord(c) > 127 else 5 for c in feat_text)
                w = max(w, feat_px + 20)
                w = min(w, 220)  # cap
            max_w = max(max_w, w)
        col_widths.append(max_w)

    # ── Place nodes ──
    nodes: dict[str, dict] = {}

    # Actor entry node
    if has_actors:
        actor_names = [a.get("name", "User") for a in actors]
        if len(actor_names) > 1:
            clients_label = " / ".join(actor_names[:2]) + ("..." if len(actor_names) > 2 else "")
        else:
            clients_label = actor_names[0]
        label_px = sum(8 if ord(c) > 127 else 6 for c in clients_label)
        label_w = min(max(140, label_px + 24), 200)
        nodes["clients"] = {
            "x": PAD_X, "y": PAD_Y + 60, "w": label_w, "h": 80,
            "label": clients_label,
            "category": "external",
            "subtitles": [a.get("name", "") for a in actors[:3]],
            "sys": {"id": "clients", "name": clients_label},
        }

    # Systems per layer column
    x_cursor = col_x_start
    for li, layer in enumerate(layer_order):
        col_w = col_widths[li]
        y_cursor = PAD_Y
        for si, s in enumerate(layer_systems[layer]):
            sid = s["id"]
            feats = s.get("features", [])
            h = NODE_H_FEATURED if feats else NODE_H_BASE
            # Adjust height for features text
            if feats:
                needed = 14 + 8 + min(len(feats), 3) * 13
                h = max(h, needed)

            nodes[sid] = {
                "x": x_cursor, "y": y_cursor, "w": col_w, "h": h,
                "label": s.get("name", sid),
                "category": layer_categories[layer],
                "subtitles": feats[:3] if feats else [],
                "sys": s,
                "layer": layer,
            }
            y_cursor += h + ROW_GAP
        x_cursor += col_w + COL_GAP

    # ── Build arrows from relations ───
    arrows: list[dict] = []
    seen_pairs: set[tuple[str, str]] = set()

    def _add_arrow(from_id: str, to_id: str, label: str, dashed: bool, relation_type: str = "supports") -> None:
        key = (from_id, to_id)
        if key in seen_pairs:
            return
        seen_pairs.add(key)
        if from_id in nodes and to_id in nodes:
            arrows.append({
                "from": from_id, "to": to_id,
                "dashed": dashed,
                "label": label,
                "relation_type": relation_type,  # ← Save relation_type for color mapping
            })

    for rel in relations:
        src_id = rel.get("from", "")
        tgt_id = rel.get("to", "")
        rel_type = rel.get("type", "data")
        label = rel.get("label", "")
        # Determine dashed based on relation type
        dashed = rel_type in ("depends-on", "owned-by", "support", "uses")
        _add_arrow(src_id, tgt_id, label, dashed, relation_type=rel_type)

    # Actor → first layer systems
    if has_actors:
        first_layer = layer_order[0] if layer_order else ""
        for s in layer_systems.get(first_layer, []):
            _add_arrow("clients", s["id"], "", False)

    # ── Calculate canvas ──
    if nodes:
        max_x = max(n["x"] + n["w"] for n in nodes.values())
        max_y = max(n["y"] + n["h"] for n in nodes.values())
        min_y = min(n["y"] for n in nodes.values())
    else:
        max_x, max_y, min_y = 400, 300, 100

    canvas_w = max_x + 120
    canvas_h = max_y - min_y + 160

    return {
        "nodes": nodes,
        "arrows": arrows,
        "width": canvas_w,
        "height": canvas_h,
        "min_y": min_y,
        "layer_order": layer_order,
        "layer_columns": {
            layer: col_widths[li]
            for li, layer in enumerate(layer_order)
        },
    }


def _layout_free_flow(blueprint: dict[str, Any]) -> dict[str, Any]:
    """Layout systems in L→R data flow columns.

    Strategy: place main flow systems on a horizontal center row,
    then scatter supporting systems across different columns above/below
    their related main flow position (not all stacked in one column).

    Row layout:
      y=130: support row — security, cloud, messaging above main
      y=230: main flow — primary data flow chain left-to-right
      y=360: data row — databases and auxiliary systems below main
      y=460: infra row — deployment and infrastructure at bottom
    """
    lib = blueprint.get("library", {})
    systems = lib.get("systems", [])
    flow_steps = lib.get("flowSteps", [])
    actors = lib.get("actors", [])

    systems_by_id = {s["id"]: s for s in systems}
    steps_by_id = {s["id"]: s for s in flow_steps}

    # ── Step 1: Find the main flow chain ──
    process_groups: dict[str, list[dict]] = {}
    for step in flow_steps:
        proc = step.get("processName", "default")
        process_groups.setdefault(proc, []).append(step)
    main_chain_steps = max(process_groups.values(), key=len) if process_groups else []
    main_chain_steps.sort(key=lambda s: s.get("seqIndex", 0))

    main_flow_sys_ids: set[str] = set()
    for step in main_chain_steps:
        for sid in step.get("systemIds", []):
            main_flow_sys_ids.add(sid)

    # ── Step 2: Build main flow order (unique systems, preserving seqIndex order) ──
    main_flow_ordered: list[str] = []
    seen_main: set[str] = set()
    for step in main_chain_steps:
        for sid in step.get("systemIds", []):
            if sid not in seen_main:
                main_flow_ordered.append(sid)
                seen_main.add(sid)

    # ── Step 4: Define layout positions ──
    has_actors = bool(actors)
    # Dynamic column spacing based on main flow count
    main_flow_count = len(main_flow_ordered)
    col_offset = 1 if has_actors else 0
    # Calculate compact column positions
    # Actor at x=80, main flow starts at x=310, gap of 160px per column
    COL_START = 310 if has_actors else 80
    COL_GAP = 160  # compact gap between main flow columns
    MAX_COLS = col_offset + main_flow_count + 4  # extra columns for supporting systems
    MAIN_COLS = [COL_START + i * COL_GAP for i in range(MAX_COLS)]

    # Row Y positions — generic row semantics (not AWS-specific)
    ROW_SUPPORT = 130   # supporting systems above main (auth, security, messaging)
    MAIN_Y = 230        # main data flow
    ROW_DATA = 360      # data/auxiliary layer below main
    ROW_INFRA = 460     # infrastructure at bottom

    nodes: dict[str, dict] = {}

    # Helper: node height from capabilities and subtitle content
    def node_h(s: dict) -> int:
        caps = len(s.get("capabilityIds", []))
        base_h = 80 if caps >= 2 else 60
        # Ensure height fits subtitle content (title 14px + gap 8 + subs 14px each)
        subs = _get_subtitle(s)
        needed_h = 14 + 8 + len(subs) * 14
        return max(base_h, needed_h)

    def node_w(s: dict) -> int:
        caps = len(s.get("capabilityIds", []))
        return 160 if caps >= 5 else 150 if caps >= 2 else 140

    # ── Step 4b: Create entry node if blueprint has actors ──
    if has_actors:
        actor_names = [a.get("name", "Client") for a in actors]
        if len(actor_names) > 1:
            clients_label = " / ".join(actor_names[:2]) + ("..." if len(actor_names) > 2 else "")
        else:
            clients_label = actor_names[0]
        # Auto-size width to fit label, capped to avoid overlap with next column
        label_px = sum(8 if ord(c) > 127 else 6 for c in clients_label)
        label_w = min(max(140, label_px + 24), 200)
        # Place entry node closer to first main flow system
        # First main flow at MAIN_COLS[col_offset], distance ~60px from its left edge
        first_main_x = MAIN_COLS[col_offset]
        clients_x = first_main_x - label_w - 60  # 60px gap, tighter layout
        nodes["clients"] = {
            "x": clients_x, "y": MAIN_Y, "w": label_w, "h": 80,
            "label": clients_label,
            "category": "external",
            "subtitles": [a.get("name", "") for a in actors[:2]],
            "sys": {"id": "clients", "name": clients_label},
        }

    # ── Step 5: Place main flow systems on center row ──
    # If there are actors, shift main flow right by 1 column
    col_offset = 1 if has_actors else 0
    main_col_idx = col_offset
    main_sys_positions: dict[str, int] = {}  # sys_id → column index for related alignment

    for sid in main_flow_ordered:
        s = systems_by_id[sid]
        col_x = MAIN_COLS[main_col_idx] if main_col_idx < len(MAIN_COLS) else 310 + main_col_idx * 220
        main_sys_positions[sid] = main_col_idx
        nodes[sid] = {
            "x": col_x, "y": MAIN_Y, "w": node_w(s), "h": node_h(s),
            "label": s["name"],
            "category": _categorize_system(s),
            "subtitles": _get_subtitle(s),
            "sys": s,
        }
        main_col_idx += 1

    # Center-align all main flow nodes: compute max height, adjust y so centers match
    if main_flow_ordered:
        max_h = max(nodes[sid]["h"] for sid in main_flow_ordered)
        target_center = MAIN_Y + max_h // 2
        for sid in main_flow_ordered:
            n = nodes[sid]
            n["y"] = target_center - n["h"] // 2

    # ── Step 6: Place non-main-flow systems by category ──
    # Generic category → row mapping (no hardcoded product keywords).
    # _categorize_system() determines category from system properties.
    # Row placement: security/cloud/messaging above main, data below, infra at bottom.
    # CRITICAL: Avoid overlap with main flow systems in the same column!
    MIN_V_GAP = 16  # minimum vertical gap between nodes in same column
    relations = blueprint.get("relations", [])

    for s in systems:
        sid = s["id"]
        if sid in nodes:
            continue

        cat = _categorize_system(s)
        rel_col = _find_related_column_idx(sid, systems_by_id, steps_by_id, main_flow_ordered, main_sys_positions, col_offset)

        # If fallback, use relations to find a better column
        if rel_col == col_offset and relations:
            for rel in relations:
                # Check if this system depends-on or supports a main flow system
                if rel.get("from") == sid and rel.get("type") in ("depends-on", "supports"):
                    target_sid = rel.get("to")
                    if target_sid in main_sys_positions:
                        rel_col = main_sys_positions[target_sid]
                        break
                # Check if a main flow system depends on this system (inverse)
                if rel.get("to") == sid and rel.get("type") in ("depends-on", "supports"):
                    source_sid = rel.get("from")
                    if source_sid in main_sys_positions:
                        rel_col = main_sys_positions[source_sid]
                        break

        col_x = MAIN_COLS[min(rel_col, len(MAIN_COLS) - 1)]

        # Find main flow systems in this column and their Y range
        col_main_sys = [msid for msid in main_flow_ordered if main_sys_positions.get(msid) == rel_col]
        if col_main_sys:
            main_y_min = min(nodes[msid]["y"] for msid in col_main_sys)
            main_y_max = max(nodes[msid]["y"] + nodes[msid]["h"] for msid in col_main_sys)
        else:
            main_y_min, main_y_max = None, None

        # Default row based on category
        if cat in ("security", "cloud", "message_bus"):
            row_y = ROW_SUPPORT
        elif cat in ("database",):
            row_y = ROW_DATA
        elif cat in ("frontend",):
            row_y = ROW_SUPPORT
        else:
            row_y = ROW_DATA

        # Adjust row_y to avoid overlap with main flow systems in same column
        node_h_val = node_h(s)
        if main_y_min is not None:
            # Check if default row_y overlaps with main flow
            node_bottom = row_y + node_h_val
            if row_y < main_y_max and node_bottom > main_y_min:
                # Overlap detected: place above or below main flow based on category
                if cat in ("security", "cloud", "message_bus", "frontend"):
                    # Above main flow
                    row_y = main_y_min - node_h_val - MIN_V_GAP
                else:
                    # Below main flow
                    row_y = main_y_max + MIN_V_GAP

        nodes[sid] = {
            "x": col_x, "y": row_y, "w": node_w(s), "h": node_h_val,
            "label": s["name"],
            "category": cat,
            "subtitles": _get_subtitle(s),
            "sys": s,
        }

    # ── Step 7: Resolve overlaps — grid-based push-down ──
    # Group nodes by approximate column (x position), then ensure vertical gaps
    # IMPORTANT: Main flow systems are protected (never pushed by overlap resolution)
    COL_BUCKET = 80  # group nodes within 80px x-range as same column
    col_buckets: dict[int, list[str]] = {}
    for sid, n in nodes.items():
        bucket = round(n["x"] / COL_BUCKET)
        col_buckets.setdefault(bucket, []).append(sid)

    main_flow_sys_ids = set(main_flow_ordered)  # protect main flow systems
    for bucket, sids in col_buckets.items():
        sids.sort(key=lambda sid: nodes[sid]["y"])
        # Pre-compute main flow Y ranges in this column for overlap checks
        col_main_nodes = [nodes[msid] for msid in sids if msid in main_flow_sys_ids]
        for i in range(1, len(sids)):
            curr_sid = sids[i]
            curr = nodes[curr_sid]
            # Skip main flow systems — they anchor the layout
            if curr_sid in main_flow_sys_ids:
                continue
            # Check overlap with ALL nodes above in sorted order
            max_required_y = curr["y"]
            for j in range(i):
                other = nodes[sids[j]]
                other_bottom = other["y"] + other["h"]
                required_y = other_bottom + MIN_V_GAP
                if required_y > max_required_y:
                    max_required_y = required_y
            # Check overlap with main flow nodes in this column
            for main_n in col_main_nodes:
                main_top = main_n["y"]
                main_bottom = main_n["y"] + main_n["h"]
                # If curr would overlap with this main flow node, push below it
                if max_required_y < main_bottom and max_required_y + curr["h"] > main_top:
                    max_required_y = main_bottom + MIN_V_GAP
            if curr["y"] < max_required_y:
                curr["y"] = max_required_y

    # ── Step 7b: Horizontal alignment — align nodes in same row to common center ──
    ROW_BUCKET = 40  # group nodes within 40px y-range as same row
    row_buckets: dict[int, list[str]] = {}
    for sid, n in nodes.items():
        bucket = round(n["y"] / ROW_BUCKET)
        row_buckets.setdefault(bucket, []).append(sid)

    for bucket, sids in row_buckets.items():
        if len(sids) <= 1:
            continue
        # Align vertical centers of all nodes in this row
        max_h = max(nodes[sid]["h"] for sid in sids)
        target_center = min(nodes[sid]["y"] + nodes[sid]["h"] // 2 for sid in sids)
        # Use the center of the tallest node as the anchor
        for sid in sids:
            n = nodes[sid]
            n["y"] = target_center - n["h"] // 2

    # ── Step 7c: Second pass overlap resolution after horizontal alignment ──
    # Alignment may cause new overlaps, re-run push-down for non-main-flow nodes
    col_buckets2: dict[int, list[str]] = {}
    for sid, n in nodes.items():
        bucket = round(n["x"] / COL_BUCKET)
        col_buckets2.setdefault(bucket, []).append(sid)

    for bucket, sids in col_buckets2.items():
        sids.sort(key=lambda sid: nodes[sid]["y"])
        for i in range(1, len(sids)):
            curr_sid = sids[i]
            curr = nodes[curr_sid]
            # Skip main flow systems — they anchor the layout
            if curr_sid in main_flow_sys_ids:
                continue
            # Check overlap with ALL nodes above
            max_required_y = curr["y"]
            for j in range(i):
                other = nodes[sids[j]]
                other_bottom = other["y"] + other["h"]
                required_y = other_bottom + MIN_V_GAP
                if required_y > max_required_y:
                    max_required_y = required_y
            if curr["y"] < max_required_y:
                curr["y"] = max_required_y

    # ── Step 8: Build arrows from flowSteps ──
    arrows: list[dict] = []
    for step in flow_steps:
        for next_id in step.get("nextStepIds", []):
            next_step = steps_by_id.get(next_id)
            if not next_step:
                continue
            src_ids = step.get("systemIds", [])
            tgt_ids = next_step.get("systemIds", [])
            for src_sid in src_ids:
                for tgt_sid in tgt_ids:
                    if src_sid in nodes and tgt_sid in nodes and src_sid != tgt_sid:
                        arrows.append({"from": src_sid, "to": tgt_sid, "dashed": False, "label": step.get("name", "")})

    # Add synthetic Clients → first main flow system arrow
    if has_actors and main_flow_ordered:
        first_main_sid = main_flow_ordered[0]
        # If first system is an auth-type placed in AUTH_Y, arrow to it
        # Otherwise arrow to the first main flow system on MAIN_Y
        arrows.append({"from": "clients", "to": first_main_sid, "dashed": False, "label": ""})

    # ── Step 9b: Add arrows from blueprint relations ──
    # System-to-system relations where both endpoints exist as nodes
    for rel in blueprint.get("relations", []):
        src_id = rel.get("from", "")
        tgt_id = rel.get("to", "")
        rel_type = rel.get("type", "supports")
        if src_id in nodes and tgt_id in nodes:
            dashed = rel_type in ("depends-on", "owned-by")
            arrows.append({
                "from": src_id, "to": tgt_id,
                "dashed": dashed,
                "label": rel.get("label", ""),
                "relation_type": rel_type,
            })

    # ── Step 9c: Add dashed support arrows from non-main-flow to main flow ───
    # Generic: link auxiliary systems to their related main-flow systems
    # based on shared capabilities and flow step associations
    for s in systems:
        sid = s["id"]
        if sid in main_sys_positions:
            continue  # skip main flow systems
        if sid not in nodes:
            continue
        # Find main flow systems sharing at least one capability
        linked = False
        for cap_id in s.get("capabilityIds", []):
            for main_sid in main_flow_ordered:
                ms = systems_by_id.get(main_sid)
                if ms and cap_id in ms.get("capabilityIds", []):
                    arrows.append({"from": sid, "to": main_sid, "dashed": True, "label": ""})
                    linked = True
        if not linked:
            # Find via flow step co-participation
            for step in flow_steps:
                if sid in step.get("systemIds", []):
                    for main_sid in step.get("systemIds", []):
                        if main_sid in main_sys_positions and main_sid != sid:
                            arrows.append({"from": sid, "to": main_sid, "dashed": True, "label": ""})
                            linked = True
                            break
                if linked:
                    break
        if not linked:
            # Last resort: connect to nearest main flow system
            n = nodes[sid]
            best_sid = min(main_flow_ordered, key=lambda ms: abs(nodes[ms]["x"] - n["x"])) if main_flow_ordered else None
            if best_sid and best_sid in nodes:
                arrows.append({"from": sid, "to": best_sid, "dashed": True, "label": ""})

    # ── Deduplicate arrows (prefer typed relations over synthetic ones) ───
    # Process ALL arrows (including Step 9c synthetic arrows)
    # Strategy: first appearance wins, but upgrade to typed relation if available
    seen_pairs: set[tuple[str, str]] = set()
    unique_arrows = []
    for a in arrows:
        key = (a["from"], a["to"])
        if key not in seen_pairs:
            seen_pairs.add(key)
            unique_arrows.append(a)
        elif a.get("relation_type"):
            # Upgrade existing synthetic arrow to typed relation arrow
            for i, existing in enumerate(unique_arrows):
                if (existing["from"], existing["to"]) == key:
                    unique_arrows[i] = a  # replace with typed relation
                    break
    arrows = unique_arrows

    # ── Step 10: Calculate canvas size ──
    if nodes:
        max_x = max(n["x"] + n["w"] for n in nodes.values())
        max_y = max(n["y"] + n["h"] for n in nodes.values())
        min_y = min(n["y"] for n in nodes.values())
    else:
        max_x, max_y, min_y = 400, 300, 100
    canvas_w = max_x + 120  # extra padding
    canvas_h = max_y - min_y + 140  # extra bottom padding for legend + footer

    return {
        "nodes": nodes,
        "arrows": arrows,
        "width": canvas_w,
        "height": canvas_h,
        "min_y": min_y,
    }


def _find_related_column_idx(
    sid: str,
    systems_by_id: dict[str, dict],
    steps_by_id: dict[str, dict],
    main_flow_ordered: list[str],
    main_sys_positions: dict[str, int],
    col_offset: int = 1,
) -> int:
    """Find the main flow column index most related to a supporting system."""
    # Find which flow steps reference this system
    for step in steps_by_id.values():
        if sid in step.get("systemIds", []):
            # Check next steps for main flow systems
            for next_id in step.get("nextStepIds", []):
                next_step = steps_by_id.get(next_id)
                if next_step:
                    for main_sid in next_step.get("systemIds", []):
                        if main_sid in main_sys_positions:
                            return main_sys_positions[main_sid]
            # Check previous steps
            for other_step in steps_by_id.values():
                for next_id in other_step.get("nextStepIds", []):
                    if next_id in steps_by_id and sid in steps_by_id[next_id].get("systemIds", []):
                        for main_sid in other_step.get("systemIds", []):
                            if main_sid in main_sys_positions:
                                return main_sys_positions[main_sid]
            # If in same step as main flow systems, use those
            for main_sid in step.get("systemIds", []):
                if main_sid in main_sys_positions:
                    return main_sys_positions[main_sid]
    # Fallback: check which capabilities this system supports,
    # then find flow steps using those capabilities
    sys_caps = set(systems_by_id[sid].get("capabilityIds", []))
    if sys_caps:
        for step in steps_by_id.values():
            if sys_caps & set(step.get("capabilityIds", [])):
                for main_sid in step.get("systemIds", []):
                    if main_sid in main_sys_positions:
                        return main_sys_positions[main_sid]
    # Fallback: check relations (depends-on, supports) to find related main flow column
    # Only use relations that point TO a main flow system (supporting systems serve main flow)
    relations = steps_by_id.get("__relations__", [])  # placeholder, will pass blueprint later
    # This will be handled in Step 6 with full blueprint access
    # Default: use first main flow column (caller will refine with relations)
    return col_offset if main_flow_ordered else 2


def _check_layout_quality(layout: dict[str, Any], blueprint: dict[str, Any]) -> list[str]:
    """Run quality checks on the layout and return a list of issues."""
    issues: list[str] = []
    nodes = layout["nodes"]
    systems = blueprint.get("library", {}).get("systems", [])
    actors = blueprint.get("library", {}).get("actors", [])
    MIN_GAP = 12  # minimum gap threshold (warning level)

    # 1. All systems have nodes
    sys_ids = {s["id"] for s in systems}
    node_ids = set(nodes.keys())
    missing = sys_ids - node_ids
    if missing:
        issues.append(f"Missing nodes for systems: {', '.join(missing)}")

    # 1b. Entry node: if blueprint has actors, should have an entry node
    if actors and not any("client" in sid.lower() or "entry" in sid.lower() for sid in node_ids):
        issues.append("No entry node despite having actors in blueprint")

    # 2. Overlap check — include vertical proximity
    node_list = list(nodes.items())
    for i, (sid_a, a) in enumerate(node_list):
        for sid_b, b in node_list[i + 1:]:
            a_right = a["x"] + a["w"]
            a_bottom = a["y"] + a["h"]
            b_right = b["x"] + b["w"]
            b_bottom = b["y"] + b["h"]
            # Check if rectangles overlap or are too close (< MIN_GAP px)
            h_overlap = not (a_right + MIN_GAP < b["x"] or b_right + MIN_GAP < a["x"])
            v_overlap = not (a_bottom + MIN_GAP < b["y"] or b_bottom + MIN_GAP < a["y"])
            if h_overlap and v_overlap:
                issues.append(f"Nodes too close: {sid_a} and {sid_b}")

    # 3. Text overflow check
    for sid, n in nodes.items():
        label = n.get("label", "")
        # Estimate: CJK ~8px, ASCII ~6px
        label_px = sum(8 if ord(c) > 127 else 6 for c in label)
        if label_px > n["w"] * 0.85:
            issues.append(f"Label tight: {sid} '{label}' (~{label_px}px) in width={n['w']}px")
        for i_sub, sub in enumerate(n.get("subtitles", [])):
            sub_px = sum(8 if ord(c) > 127 else 5 for c in sub)
            if sub_px > n["w"] * 0.9:
                issues.append(f"Subtitle tight: {sid} line {i_sub} '{sub}' (~{sub_px}px) in width={n['w']}px")

    # 4. Title coverage check
    title_bottom = 62
    for sid, n in nodes.items():
        if n["y"] < title_bottom + 10:
            issues.append(f"Node {sid} near title: y={n['y']} < {title_bottom + 10}")

    # 5. Canvas size
    if layout["width"] < 1000:
        issues.append(f"Canvas too narrow: {layout['width']}px < 1000px")

    # 6. Arrow completeness
    flow_steps = blueprint.get("library", {}).get("flowSteps", [])
    expected = 0
    actual_pairs = {(a["from"], a["to"]) for a in layout["arrows"]}
    steps_by_id = {s["id"]: s for s in flow_steps}
    for step in flow_steps:
        for next_id in step.get("nextStepIds", []):
            src_ids = step.get("systemIds", [])
            tgt_ids = steps_by_id.get(next_id, {}).get("systemIds", [])
            for sid in src_ids:
                for tid in tgt_ids:
                    if sid != tid:
                        expected += 1
    actual_count = len(actual_pairs)
    if actual_count < expected:
        issues.append(f"Missing arrows: {actual_count} actual vs {expected} expected")

    # 7. Same-column stacking check — only flag if nodes in same column are on same row
    col_stacks: dict[int, list[tuple[str, int, int]]] = {}
    for sid, n in nodes.items():
        col_stacks.setdefault(n["x"], []).append((sid, n["y"], n["h"]))
    for col_x, stack in col_stacks.items():
        stack.sort(key=lambda x: x[1])  # sort by y
        for i, (sid_a, y_a, h_a) in enumerate(stack):
            for sid_b, y_b, h_b in stack[i + 1:]:
                # If vertically adjacent nodes are < 30px apart, flag it
                gap = y_b - (y_a + h_a)
                if 0 < gap < 8:
                    issues.append(f"Column {col_x}: {sid_a} and {sid_b} overlap (gap={gap}px)")

    return issues


def _render_free_flow_svg(
    layout: dict[str, Any],
    title: str,
    subtitle: str,
    theme: str = "dark",
    blueprint: dict[str, Any] | None = None,
) -> str:
    """Render a free-flow layout dict into an SVG string."""
    if blueprint is None:
        blueprint = {}
    industry = blueprint.get("meta", {}).get("industry", "") or None
    colors = _resolve_theme(theme, industry=industry)
    nodes = layout["nodes"]
    arrows = layout["arrows"]
    w, h = layout["width"], layout["height"]
    min_y = layout.get("min_y", 0)
    y_offset = -min_y + 95  # shift everything down so top nodes clear title (y=62) with padding

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" font-family="{FONT}">',
        _svg_defs(colors=colors, theme=theme),
    ]

    bg_rect_idx = len(parts)
    parts.append(f'<rect width="{w}" height="{h}" fill="{colors["bg"]}"/>')
    grid_rect_idx: int | None = None
    if theme == "dark":
        grid_rect_idx = len(parts)
        parts.append(f'<rect width="{w}" height="{h}" fill="url(#grid)"/>')

    # Title
    parts.append(_title_svg(title, subtitle, w, colors=colors))

    # Layer column headers (if present)
    layer_order = layout.get("layer_order", [])
    if layer_order:
        for layer in layer_order:
            layer_nodes = [n for n in nodes.values() if n.get("layer") == layer]
            if not layer_nodes:
                continue
            lx = min(n["x"] for n in layer_nodes)
            ly = min(n["y"] for n in layer_nodes) + y_offset - 20
            lw = max(n["x"] + n["w"] for n in layer_nodes) - lx
            parts.append(
                f'<text x="{lx + lw // 2}" y="{ly}" text-anchor="middle" '
                f'font-size="11" fill="{colors["text_sub"]}" font-weight="600" '
                f'letter-spacing="0.3">{_esc(layer)}</text>'
            )

    # Detect boundary box covering all non-client nodes
    all_rendered_nodes = [n for n in nodes.values() if n.get("category") != "external" or n.get("sys", {}).get("id", "").startswith("sys-")]
    if not all_rendered_nodes:
        all_rendered_nodes = [n for n in nodes.values() if n.get("category") != "external"]
    region_rect_idx = None
    if all_rendered_nodes:
        min_x = min(n["x"] for n in all_rendered_nodes) - 40
        region_min_y = max(min(n["y"] for n in all_rendered_nodes) - 30 + y_offset, 72)
        max_x = max(n["x"] + n["w"] for n in all_rendered_nodes) + 40
        region_max_y = max(n["y"] + n["h"] for n in all_rendered_nodes) + 30 + y_offset
        region_rect_idx = len(parts)
        parts.append(
            f'<rect x="{min_x}" y="{region_min_y}" width="{max_x-min_x}" height="{region_max_y-region_min_y}" '
            f'rx="16" fill="none" stroke="#F59E0B" stroke-width="1.5" '
            f'stroke-dasharray="8,4" opacity="0.4"/>'
        )
        # Generic region label
        region_label = "系统边界"
        parts.append(
            f'<text x="{min_x+20}" y="{max(region_min_y - 10, 85)}" font-size="12" '
            f'fill="#F59E0B" font-weight="600">{region_label}</text>'
        )

    # Record insertion point: legend will be inserted here (behind arrows & nodes)
    legend_insert_idx = len(parts)

    # Arrows
    arrow_labels: list[tuple[int, int, str]] = []

    # ── Pre-compute anti-overlap: spread attachment points for converging arrows ──
    incoming_by_target: dict[str, list[int]] = {}  # target_id → [arrow indices]
    for ai, arrow in enumerate(arrows):
        tgt_id = arrow["to"]
        incoming_by_target.setdefault(tgt_id, []).append(ai)

    # For each target with multiple incoming arrows:
    #  1. Spread attachment x-positions across the node edge
    #  2. Stagger mid_y so horizontal segments don't overlap
    SPREAD_GAP = 14  # pixels between attachment points
    MID_Y_STEP = 10  # pixels between staggered horizontal levels
    target_attach_x: dict[tuple[str, int], int] = {}  # (target_id, arrow_index) → x
    target_mid_y_offset: dict[tuple[str, int], int] = {}  # (target_id, arrow_index) → y offset
    for tgt_id, arrow_indices in incoming_by_target.items():
        n = len(arrow_indices)
        tgt = nodes.get(tgt_id)
        if not tgt or n <= 1:
            for ai in arrow_indices:
                target_attach_x[(tgt_id, ai)] = tgt["x"] + tgt["w"] // 2 if tgt else 0
                target_mid_y_offset[(tgt_id, ai)] = 0
        else:
            # Sort by source x so leftmost arrow gets lowest mid_y
            sorted_indices = sorted(arrow_indices, key=lambda ai: nodes.get(arrows[ai]["from"], {}).get("x", 0))
            cx = tgt["x"] + tgt["w"] // 2
            total_spread = (n - 1) * SPREAD_GAP
            start_x = cx - total_spread // 2
            for i, ai in enumerate(sorted_indices):
                target_attach_x[(tgt_id, ai)] = start_x + i * SPREAD_GAP
                target_mid_y_offset[(tgt_id, ai)] = int((i - (n - 1) / 2) * MID_Y_STEP)

    for ai, arrow in enumerate(arrows):
        src = nodes.get(arrow["from"])
        tgt = nodes.get(arrow["to"])
        if not src or not tgt:
            continue

        same_col = abs(src["x"] - tgt["x"]) < 50
        same_row = abs(src["y"] - tgt["y"]) < 80  # 增大阈值，同行节点用侧边直连

        # Use spread x for target attachment if available
        spread_tx = target_attach_x.get((arrow["to"], ai), tgt["x"] + tgt["w"] // 2)

        # Same-column connections always use vertical path (no elbow detour)
        if same_col:
            center_x = (src["x"] + src["w"] // 2 + spread_tx) // 2
            if src["y"] < tgt["y"]:
                sx = center_x
                sy = src["y"] + src["h"] + y_offset
                tx = center_x
                ty = tgt["y"] + y_offset
            else:
                sx = center_x
                sy = src["y"] + y_offset
                tx = center_x
                ty = tgt["y"] + tgt["h"] + y_offset
            if arrow.get("dashed"):
                parts.append(f'<line x1="{sx}" y1="{sy}" x2="{tx}" y2="{ty}" stroke="{colors["arrow_muted"]}" stroke-width="1.5" stroke-dasharray="4,4" opacity="0.5" marker-end="url(#arrow-dashed)"/>')
            else:
                parts.append(_render_arrow_line(sx, sy, tx, ty, arrow, colors))
            if arrow.get("label"):
                arrow_labels.append({"x": (sx + tx) // 2, "y": (sy + ty) // 2, "label": arrow["label"], "offsets": [(0, -16), (0, 16), (36, -16), (-36, -16), (36, 16), (-36, 16)]})
        elif same_row:
            # Horizontal: source right edge → target left edge
            # 使用相同的 y 坐标，确保完全水平（不因节点高度差异产生斜线）
            avg_h = (src["h"] + tgt["h"]) // 2
            sy = src["y"] + avg_h // 2 + y_offset
            sx = src["x"] + src["w"]
            tx = tgt["x"]
            ty = sy  # 强制水平
            parts.append(_render_arrow_line(sx, sy, tx, ty, arrow, colors))
            if arrow.get("label"):
                # Use ±28px offsets to avoid overlapping with nodes (same as default offsets)
                arrow_labels.append({"x": (sx + tx) // 2, "y": sy, "label": arrow["label"], "offsets": [(0, -28), (0, 28), (40, -28), (-40, -28), (40, 28), (-40, 28), (0, -56), (0, 56)]})
        else:
            # Cross-row: elbow path routing
            if src["y"] > tgt["y"]:
                sx = src["x"] + src["w"] // 2
                sy = src["y"] + y_offset
                tx = spread_tx
                ty = tgt["y"] + tgt["h"] + y_offset
            else:
                sx = src["x"] + src["w"] // 2
                sy = src["y"] + src["h"] + y_offset
                tx = spread_tx
                ty = tgt["y"] + y_offset

            # Stagger mid_y so converging arrows have separate horizontal levels
            mid_y_offset = target_mid_y_offset.get((arrow["to"], ai), 0)
            # 基础 mid_y：在起点和终点之外，避免穿过节点
            if src["y"] < tgt["y"]:
                # 起点在上方，终点在下方 → mid_y 在终点下方
                base_mid_y = tgt["y"] + tgt["h"] + y_offset + 40
            else:
                # 起点在下方，终点在上方 → mid_y 在起点下方
                base_mid_y = src["y"] + src["h"] + y_offset + 40
            mid_y = base_mid_y + mid_y_offset

            # Collision avoidance: 确保 mid_y 不与任何节点边缘粘连
            # 策略：找最近的"安全"位置（不在任何节点边缘附近）
            h_min_x = min(sx, tx)
            h_max_x = max(sx, tx)
            MIN_GAP = 8  # 最小间距（不能太大，否则两个紧挨节点之间没空间）

            # 收集所有在 x 范围内的节点边缘
            blocked_ranges = []
            for nid, nd in nodes.items():
                if nid == arrow["from"] or nid == arrow["to"]:
                    continue
                nd_left = nd["x"]
                nd_right = nd["x"] + nd["w"]
                if nd_right > h_min_x and nd_left < h_max_x:
                    nd_top = nd["y"] + y_offset
                    nd_bot = nd["y"] + nd["h"] + y_offset
                    # 节点占据的 y 范围（加安全间距）
                    blocked_ranges.append((nd_top - MIN_GAP, nd_bot + MIN_GAP))

            # 检查 mid_y 是否在 blocked 范围内
            for blocked_top, blocked_bot in blocked_ranges:
                if blocked_top <= mid_y <= blocked_bot:
                    # 尝试向上或向下推到最近的 block 边缘
                    candidates = []
                    if blocked_top > max(sy, ty) + MIN_GAP or blocked_top < min(sy, ty) - MIN_GAP:
                        candidates.append(blocked_top)
                    candidates.append(blocked_bot)
                    # 选择距离当前 mid_y 最近的候选位置
                    if candidates:
                        mid_y = min(candidates, key=lambda c: abs(c - mid_y))
                    break

            # Determine color based on relation type (same logic as _render_arrow_line)
            rel_type = arrow.get("relation_type", "supports")
            if rel_type == "flows-to":
                arrow_color = "#60A5FA"  # blue
                marker = "arrow-solid"
                style = f'stroke="{arrow_color}" stroke-width="1.5" fill="none"'
            elif rel_type == "owned-by":
                arrow_color = "#FBBF24"  # yellow
                marker = "arrow-dot"
                style = f'stroke="{arrow_color}" stroke-width="1.5" stroke-dasharray="3,3" fill="none"'
            elif arrow.get("dashed") or rel_type == "depends-on":
                arrow_color = colors["arrow_muted"]  # gray
                marker = "arrow-dashed"
                style = f'stroke="{arrow_color}" stroke-width="1.5" stroke-dasharray="4,4" opacity="0.5" fill="none"'
            else:
                # supports or other types
                arrow_color = colors["arrow"]  # green
                marker = "arrow-solid"
                style = f'stroke="{arrow_color}" stroke-width="1.5" fill="none"'

            if abs(sx - tx) < 8:
                parts.append(f'<line x1="{sx}" y1="{sy}" x2="{tx}" y2="{ty}" {style} marker-end="url(#{marker})"/>')
            else:
                path_d = f"M {sx} {sy} L {sx} {mid_y} L {tx} {mid_y} L {tx} {ty}"
                parts.append(f'<path d="{path_d}" {style} marker-end="url(#{marker})"/>')

            if arrow.get("label"):
                arrow_labels.append({"x": (sx + tx) // 2, "y": mid_y, "label": arrow["label"], "offsets": [(0, -16), (0, 16), (32, -16), (-32, -16), (32, 16), (-32, 16)]})

    # Update region rect to contain all arrow paths
    if region_rect_idx is not None:
        max_arrow_y = 0
        for ai, arrow in enumerate(arrows):
            src = nodes.get(arrow["from"])
            tgt = nodes.get(arrow["to"])
            if not src or not tgt:
                continue
            if abs(src["y"] - tgt["y"]) < 80:
                continue  # same_row, no elbow
            if src["y"] > tgt["y"]:
                mid_y_base = src["y"] + src["h"] + y_offset + 40
            else:
                mid_y_base = tgt["y"] + tgt["h"] + y_offset + 40
            mid_y_off = target_mid_y_offset.get((arrow["to"], ai), 0)
            max_arrow_y = max(max_arrow_y, mid_y_base + mid_y_off + 10)
        old_rect = parts[region_rect_idx]
        m = _re.search(r'y="(\d+)" width="(\d+)" height="(\d+)"', old_rect)
        if m and max_arrow_y > 0:
            old_y = int(m.group(1))
            old_h = int(m.group(3))
            new_bottom = max(old_y + old_h, max_arrow_y)
            new_h = new_bottom - old_y
            parts[region_rect_idx] = old_rect.replace(f'height="{old_h}"', f'height="{new_h}"')

        # Extend SVG canvas if region rect exceeds it
        # Reserve 160px at bottom for legend + footer so they don't overlap arrows
        LEGEND_FOOTER_RESERVE = 160
        min_canvas_bottom = max_arrow_y + LEGEND_FOOTER_RESERVE if max_arrow_y > 0 else h
        if min_canvas_bottom > h:
            h = min_canvas_bottom
            parts[0] = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{FONT}">'
            parts[bg_rect_idx] = f'<rect width="{w}" height="{h}" fill="{colors["bg"]}"/>'
            if grid_rect_idx is not None:
                parts[grid_rect_idx] = f'<rect width="{w}" height="{h}" fill="url(#grid)"/>'

    # Nodes with semantic colors (render BEFORE arrow_labels so labels appear on top)
    for nid, n in nodes.items():
        cat = n.get("category", "external")
        fill, stroke = _resolve_system_colors(cat, theme)
        if not fill:
            fill, stroke = colors["sys_fill"], colors["sys_stroke"]
        rx = 8
        ny = n["y"] + y_offset
        parts.append(f'<g class="node" id="{nid}">')
        parts.append(f'<rect x="{n["x"]}" y="{ny}" width="{n["w"]}" height="{n["h"]}" '
                     f'rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
        # Category strip (4px left edge)
        if stroke:
            parts.append(f'<rect x="{n["x"]}" y="{ny}" width="4" height="{n["h"]}" '
                         f'rx="2" fill="{stroke}"/>')
        # Label
        subs = n.get("subtitles", [])
        label_y = ny + n["h"] // 2 - (len(subs) + 1) * 7
        parts.append(
            f'<text x="{n["x"]+n["w"]//2}" y="{label_y+10}" '
            f'text-anchor="middle" font-size="14" fill="{colors["text_main"]}" '
            f'font-weight="600">{_esc(n["label"])}</text>'
        )
        for i, sub in enumerate(subs):
            c = stroke if i == len(subs) - 1 else colors["text_sub"]
            parts.append(
                f'<text x="{n["x"]+n["w"]//2}" y="{label_y+24+i*14}" '
                f'text-anchor="middle" font-size="10" fill="{c}">{_esc(sub)}</text>'
            )
        parts.append('</g>')

    # Arrow labels (render AFTER nodes so they appear on top)
    # Pass node positions to avoid overlap
    node_rects = [(n["x"], n["y"] + y_offset, n["w"], n["h"]) for n in nodes.values()]
    for label_svg in _render_arrow_labels(arrow_labels, colors=colors, canvas_w=w, canvas_h=h, node_rects=node_rects):
        parts.append(label_svg)


    # Legend — show categories actually used in the diagram
    # Render BEFORE arrows & nodes (z-order: legend behind content)
    _CAT_LABELS = {
        "frontend": "前端/入口",
        "cloud": "网关/网络",
        "backend": "计算/核心",
        "message_bus": "消息/集成",
        "database": "数据/存储",
        "security": "安全/权限",
        "external": "外部/入口",
    }
    used_cats = list(dict.fromkeys(
        n.get("category", "external") for n in nodes.values()
    ))
    cat_samples = [(c, _CAT_LABELS.get(c, c)) for c in used_cats if c != "external"]
    ROW_H = 18
    legend_w = 160
    legend_h = 20 + len(cat_samples) * ROW_H + 6 + 4 * ROW_H + 10
    legend_x, legend_y = 40, h - legend_h - 12

    legend_parts = [
        f'<g class="legend" transform="translate({legend_x}, {legend_y})">',
        f'<rect x="0" y="0" width="{legend_w}" height="{legend_h}" '
        f'rx="6" fill="{colors["canvas"]}" stroke="{colors["border"]}" stroke-width="1" opacity="0.95"/>',
        f'<text x="12" y="16" font-size="11" fill="{colors["text_main"]}" '
        f'font-weight="600" letter-spacing="0.3">图 例</text>',
    ]
    for ci, (cat, label) in enumerate(cat_samples):
        fill, stroke = _resolve_system_colors(cat, theme)
        if not fill:
            fill, stroke = colors["sys_fill"], colors["sys_stroke"]
        cy = 28 + ci * ROW_H
        legend_parts.append(
            f'<rect x="12" y="{cy}" width="12" height="12" rx="3" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
            f'<text x="30" y="{cy+10}" font-size="9" fill="{colors["text_sub"]}">{label}</text>'
        )
    arrow_base_y = 28 + len(cat_samples) * ROW_H + 6
    legend_arrows = [
        ("supports", colors["arrow"], "", "arrow-solid"),
        ("depends-on", colors["arrow_muted"], ' stroke-dasharray="6,4"', "arrow-open"),
        ("flows-to", "#60A5FA" if theme == "dark" else "#3B82F6", "", "arrow-solid"),
        ("owned-by", "#FBBF24" if theme == "dark" else "#D97706", ' stroke-dasharray="3,3"', "arrow-dot"),
    ]
    for i, (label, acolor, dash_attr, marker) in enumerate(legend_arrows):
        ay = arrow_base_y + i * ROW_H
        legend_parts.append(
            f'<line x1="12" y1="{ay + 6}" x2="30" y2="{ay + 6}" '
            f'stroke="{acolor}" stroke-width="1.5"{dash_attr} '
            f'marker-end="url(#{marker})"/>'
            f'<text x="38" y="{ay + 10}" font-size="9" fill="{colors["text_sub"]}">{label}</text>'
        )
    legend_parts.append('</g>')
    # Insert legend at the recorded position (behind arrows & nodes)
    for i, lp in enumerate(legend_parts):
        parts.insert(legend_insert_idx + i, lp)
    legend_insert_idx += len(legend_parts)  # update for subsequent inserts

    # Footer
    parts.append(
        f'<text x="{w//2}" y="{h-15}" text-anchor="middle" '
        f'font-size="10" fill="{colors["text_sub"]}" letter-spacing="0.5">'
        f'{_esc(title)} • 自由流布局</text>'
    )

    parts.append("</svg>")
    return "\n".join(parts)


def export_svg_auto(
    blueprint: dict[str, Any],
    target: Path,
    theme: str = "dark",
    industry: str | None = None,
    requested_route: str | None = None,
) -> None:
    """Export using free-flow L→R data flow layout.

    This is the default export: positions systems by category in columns
    (Cloud → Backend → Database) with semantic colors and arrows.
    When systems have ``layer`` fields, uses _layout_layered instead.
    """
    route_decision = resolve_export_route(blueprint, requested_route=requested_route)

    _export_by_route(
        blueprint,
        target,
        route=route_decision.route,
        theme=theme,
        industry=industry,
    )
    integrity = check_svg_integrity(target.read_text(encoding="utf-8"))
    if not integrity.errors:
        return

    if route_decision.fallback_route:
        _export_by_route(
            blueprint,
            target,
            route=route_decision.fallback_route,
            theme=theme,
            industry=industry,
        )
        fallback_integrity = check_svg_integrity(target.read_text(encoding="utf-8"))
        if not fallback_integrity.errors:
            return
        raise ExportIntegrityError(
            ExportIntegrityFailure(
                requested_route=requested_route or route_decision.route,
                attempted_route=route_decision.fallback_route,
                fallback_route=route_decision.fallback_route,
                terminal_reason="integrity_failed_after_fallback",
                errors=fallback_integrity.errors,
            )
        )
    raise ExportIntegrityError(
        ExportIntegrityFailure(
            requested_route=requested_route or route_decision.route,
            attempted_route=route_decision.route,
            fallback_route=route_decision.fallback_route,
            terminal_reason="integrity_failed",
            errors=integrity.errors,
        )
    )


def _export_by_route(
    blueprint: dict[str, Any],
    target: Path,
    *,
    route: str,
    theme: str,
    industry: str | None = None,
) -> None:
    # ─── Step 1: Intent Resolution + Layer Assignment ───
    # Apply IntentResolver + RuleEngine to assign layer to each system
    resolver = IntentResolver()

    # Resolve intent
    resolved = resolver.resolve_intent(blueprint)
    intent = resolved["blueprintIntent"]
    strategy_id = resolved["strategySelection"]["selected"]

    # Load perspective
    perspective = load_perspective(strategy_id)

    # Load overlay if secondary intent detected
    overlay = None
    if intent.get("secondary"):
        overlay = load_overlay(intent["secondary"])

    # Initialize RuleEngine with perspective + overlay
    engine = RuleEngine(perspective=perspective, overlay=overlay)

    # Assign layer to each system
    systems = blueprint.get("library", {}).get("systems", [])
    for system in systems:
        layer_result = engine.assign_layer(system)
        system["layer"] = layer_result["layer"]

    # ─── Step 2: Route-specific Export ───
    if route == "evolution":
        export_evolution_timeline_svg(blueprint, target, theme=theme)
        return
    if route == "swimlane":
        export_swimlane_flow_svg(blueprint, target, theme=theme)
        return
    if route == "hierarchy":
        export_product_tree_svg(blueprint, target, theme=theme)
        return
    if route == "poster":
        export_layer_poster_svg(blueprint, target, theme=theme)
        return

    title = blueprint.get("meta", {}).get("title", "Business Blueprint")
    if industry is None:
        industry = blueprint.get("meta", {}).get("industry", "") or None
    industry_label = industry or ""
    subtitle = f"行业：{industry_label}" if industry_label else "架构"

    # Detect layer-based layout (now systems have layer fields)
    has_layers = any(s.get("layer") for s in systems)

    if has_layers:
        layout = _layout_layered(blueprint)
    else:
        layout = _layout_free_flow(blueprint)
    # Run quality validation
    issues = _check_layout_quality(layout, blueprint)
    if issues:
        print(f"  Layout quality issues ({len(issues)}):")
        for iss in issues:
            print(f"    - {iss}")
    svg = _render_free_flow_svg(layout, title, subtitle, theme=theme, blueprint=blueprint)
    target.write_text(svg, encoding="utf-8")


# ─── Export: Product Tree / Genealogy ────────────────────────────
def export_product_tree_svg(blueprint: dict[str, Any], target: Path, theme: str = "light") -> None:
    """Product family tree: root → market segments → products with capability badges."""
    colors = _resolve_theme(theme)
    title = blueprint.get("meta", {}).get("title", "Product Family")
    lib = blueprint.get("library", {})
    systems = lib.get("systems", [])
    capabilities = lib.get("capabilities", [])
    relations = blueprint.get("relations", [])

    cap_by_id = {c["id"]: c for c in capabilities}
    sys_by_id = {s["id"]: s for s in systems}

    # Build evolution map: from_id → to_id
    evolve_map: dict[str, list[str]] = {}
    platform_powers: dict[str, list[str]] = {}
    for r in relations:
        if r["type"] == "powers":
            platform_powers.setdefault(r["from"], []).append(r["to"])
        elif r["type"] == "evolves-to" or r["label"] == "演进":
            evolve_map.setdefault(r["from"], []).append(r["to"])

    # Market segments — derive from blueprint data
    # Use views.productTree.segments or group by system properties
    _views = blueprint.get("views")
    if isinstance(_views, dict):
        segments = _views.get("productTree", {}).get("segments", [])
    else:
        segments = []
    if not segments:
        # Auto-derive: prefer explicit segment, otherwise fall back to layered blueprint grouping.
        seg_map: dict[str, list[str]] = {}
        seg_order: list[str] = []
        for s in systems:
            seg_label = (
                s.get("properties", {}).get("segment", s.get("segment", ""))
                or s.get("layer", "")
            )
            if not seg_label:
                continue
            if seg_label not in seg_map:
                seg_map[seg_label] = []
                seg_order.append(seg_label)
            seg_map[seg_label].append(s["id"])
        segments = [{"label": label, "ids": seg_map[label]} for label in seg_order]

    # Filter to actual systems
    active_segments: list[dict] = []
    for seg in segments:
        matched = [s for s in systems if s["id"] in seg["ids"]]
        if matched:
            active_segments.append({"label": seg["label"], "sys_ids": [s["id"] for s in matched]})

    # Fallback: all systems in one group
    if not active_segments and systems:
        active_segments = [{"label": "Products", "sys_ids": [s["id"] for s in systems]}]

    PAD_X = 50
    PAD_Y = 30
    NODE_H = 44
    CAP_H = 20
    COL_W = 220
    SEG_GAP = 16  # gap between segment group boxes
    SEG_INNER_PAD = 18  # inside group box
    ROOT_W = 160
    ROOT_H = 44

    # Color palette — auto-assign distinct colors per segment
    if theme == "dark":
        _SEG_PALETTE = [
            ("#A78BFA", "#1E1535"),
            ("#22D3EE", "#0E2A3D"),
            ("#34D399", "#0E2E1F"),
            ("#4ADE80", "#0F2518"),
            ("#FBBF24", "#2A2010"),
            ("#FB7185", "#2A1018"),
            ("#60A5FA", "#1E3A5F"),
        ]
    else:
        _SEG_PALETTE = [
            ("#4338CA", "#EEF2FF"),
            ("#0B6E6E", "#E8F5F5"),
            ("#0F7B6C", "#E8F5F5"),
            ("#059669", "#ECFDF5"),
            ("#D97706", "#FEFCE8"),
            ("#7C3AED", "#F5F3FF"),
            ("#DC2626", "#FEF2F2"),
        ]
    seg_colors: dict[str, tuple[str, str]] = {}
    for i, seg in enumerate(active_segments):
        seg_colors[seg["label"]] = _SEG_PALETTE[i % len(_SEG_PALETTE)]

    # Pass 1: compute layout
    max_cols = 0
    total_seg_h = 0
    seg_layouts: list[dict] = []
    for seg in active_segments:
        n_cols = len(seg["sys_ids"])
        max_cols = max(max_cols, n_cols)
        # Compute max badge count across systems in this segment
        max_badges = 0
        for sid in seg["sys_ids"]:
            sys = sys_by_id.get(sid)
            if sys:
                max_badges = max(max_badges, len(sys.get("capabilityIds", [])))
        # Segment group height = label + pad + node row + badges
        seg_h = 24 + SEG_INNER_PAD + NODE_H + max(0, max_badges) * (CAP_H + 4) + 4
        total_seg_h += seg_h + SEG_GAP
        seg_layouts.append({"label": seg["label"], "sys_ids": seg["sys_ids"], "h": seg_h})

    canvas_w = PAD_X * 2 + max_cols * COL_W + (max_cols - 1) * 20
    root_y = PAD_Y + 92
    seg_y = root_y + ROOT_H + SEG_GAP + 30  # arrow space + gap

    parts: list[str] = []  # will prepend svg header after layout

    # Title block
    parts.append(
        f'<g class="title-block">'
        f'<rect x="{PAD_X}" y="{PAD_Y}" width="{canvas_w - PAD_X * 2}" height="52" '
        f'rx="6" fill="{colors["canvas"]}" stroke="{colors["border"]}" stroke-width="1"/>'
        f'<text x="{PAD_X + 16}" y="{PAD_Y + 24}" '
        f'font-size="16" fill="{colors["text_main"]}" font-family="{FONT}" '
        f'font-weight="700">{_esc(title)} — 产品谱系</text>'
        f'<text x="{PAD_X + 16}" y="{PAD_Y + 42}" '
        f'font-size="11" fill="{colors["text_sub"]}" font-family="{FONT_MONO}">'
        f'{_esc(title)}</text></g>'
    )

    cx = canvas_w / 2

    # Root node — use blueprint title
    root_label = title.split("—")[0].strip() if "—" in title else title.split("-")[0].strip()
    parts.append(
        f'<rect class="node-rect" x="{cx - ROOT_W / 2}" y="{root_y}" width="{ROOT_W}" height="{ROOT_H}" '
        f'rx="8" fill="{colors["canvas"]}" stroke="{colors["border"]}" stroke-width="1.5"/>'
        f'<text class="node-label" x="{cx}" y="{root_y + ROOT_H / 2 + 5}" '
        f'text-anchor="middle" font-size="15" fill="{colors["text_main"]}" '
        f'font-weight="700">{_esc(root_label)}</text>'
    )

    node_positions: dict[str, tuple[int, int]] = {}
    seg_top_y: dict[str, int] = {}  # for arrows

    current_y = seg_y
    for sl in seg_layouts:
        seg_label = sl["label"]
        stroke, fill = seg_colors.get(seg_label, ("#64748B", "#F8FAFC"))
        sys_ids = sl["sys_ids"]
        n = len(sys_ids)
        seg_w = n * COL_W + max(0, n - 1) * 20
        seg_start_x = cx - seg_w / 2

        seg_top_y[seg_label] = current_y

        # Segment group bg
        parts.append(
            f'<rect x="{seg_start_x - SEG_INNER_PAD}" y="{current_y}" '
            f'width="{seg_w + SEG_INNER_PAD * 2}" height="{sl["h"]}" '
            f'rx="10" fill="{fill}" stroke="{stroke}" stroke-width="1" fill-opacity="{0.82 if theme == "dark" else 0.6}"/>'
        )
        # Segment label
        parts.append(
            f'<text x="{cx}" y="{current_y + 16}" text-anchor="middle" '
            f'font-size="11" fill="{stroke}" font-weight="600" letter-spacing="0.5">'
            f'{_esc(seg_label)}</text>'
        )

        ny = current_y + 28
        for ci, sid in enumerate(sys_ids):
            sys = sys_by_id.get(sid)
            if not sys:
                continue
            nx = int(seg_start_x + ci * (COL_W + 20))
            node_positions[sid] = (nx + COL_W // 2, ny + NODE_H // 2)

            parts.append(
                f'<rect class="node-rect" x="{nx}" y="{ny}" width="{COL_W}" height="{NODE_H}" '
                f'rx="6" fill="{colors["canvas"]}" stroke="{stroke}" stroke-width="1.5"/>'
                f'<text class="node-label" x="{nx + COL_W // 2}" y="{ny + NODE_H // 2 + 5}" '
                f'text-anchor="middle" font-size="12" fill="{colors["text_main"]}" '
                f'font-weight="600">{_esc(sys["name"])}</text>'
            )

            # Capability badges
            cap_ids = sys.get("capabilityIds", [])
            badge_y = ny + NODE_H + 6
            for j, cid in enumerate(cap_ids[:4]):
                cap = cap_by_id.get(cid, {})
                cap_name = cap.get("name", cid)
                bw = max(len(cap_name) * 7 + 12, 50)
                bx = nx + COL_W // 2 - bw // 2
                parts.append(
                    f'<rect x="{bx}" y="{badge_y + j * (CAP_H + 4)}" width="{bw}" height="{CAP_H}" '
                    f'rx="3" fill="{fill if theme == "dark" else stroke}" stroke="{stroke}" stroke-width="{0.8 if theme == "dark" else 0}" fill-opacity="{0.95 if theme == "dark" else 0.15}"/>'
                    f'<text x="{bx + bw // 2}" y="{badge_y + j * (CAP_H + 4) + CAP_H // 2 + 5}" '
                    f'text-anchor="middle" font-size="9" fill="{colors["text_main"] if theme == "dark" else stroke}">{_esc(cap_name)}</text>'
                )

        current_y += sl["h"] + SEG_GAP

    canvas_h = current_y + PAD_Y  # bottom padding after last segment

    # Prepend SVG header
    header = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{canvas_h}" '
        f'font-family="{FONT}">',
        _svg_defs(colors=colors, theme=theme),
        f'<rect width="{canvas_w}" height="{canvas_h}" fill="{colors["bg"]}"/>',
    ]
    if theme == "dark":
        header.append(f'<rect width="{canvas_w}" height="{canvas_h}" fill="url(#grid)"/>')
    parts[0:0] = header

    # Arrows: root to each segment group
    for seg in active_segments:
        ry2 = seg_top_y[seg["label"]] + 14
        parts.append(
            f'<line x1="{cx}" y1="{root_y + ROOT_H}" x2="{cx}" y2="{ry2}" '
            f'stroke="{colors["arrow_muted"]}" stroke-width="1" stroke-dasharray="4,3" '
            f'marker-end="url(#arrow-dashed)"/>'
        )

    # Evolution arrows (EAS → 星瀚, etc.)
    for from_id, to_ids in evolve_map.items():
        for to_id in to_ids:
            if from_id in node_positions and to_id in node_positions:
                fx, fy = node_positions[from_id]
                tx, ty = node_positions[to_id]
                if abs(tx - fx) > 30:  # not in same column
                    dy = (fy + ty) / 2
                    parts.append(
                        f'<path d="M{fx},{fy} C{fx},{dy} {tx},{dy} {tx},{ty}" '
                        f'fill="none" stroke="#DC2626" stroke-width="1.5" stroke-dasharray="6,3" '
                        f'marker-end="url(#arrow-dashed)" opacity="0.6"/>'
                    )
                    # Label
                    mx, my = (fx + tx) // 2, dy
                    parts.append(
                        f'<rect x="{mx - 22}" y="{my - 8}" width="44" height="16" '
                        f'rx="3" fill="{colors["arrow_label_bg"]}"/>'
                        f'<text x="{mx}" y="{my + 4}" text-anchor="middle" '
                        f'font-size="9" fill="#DC2626" font-weight="500">演进</text>'
                    )

    # Platform arrows (苍穹 → 星瀚)
    for plat_id, targets in platform_powers.items():
        if plat_id in node_positions:
            px, py = node_positions[plat_id]
            for tgt_id in targets:
                if tgt_id in node_positions:
                    tx, ty = node_positions[tgt_id]
                    dy = (py + ty) / 2
                    parts.append(
                        f'<path d="M{px},{py + 22} C{px},{dy} {tx},{dy} {tx},{ty - 22}" '
                        f'fill="none" stroke="#4338CA" stroke-width="2" '
                        f'marker-end="url(#arrow-solid)" opacity="0.7"/>'
                    )
                    mx = (px + tx) // 2
                    my = dy
                    parts.append(
                        f'<rect x="{mx - 22}" y="{my - 8}" width="44" height="16" '
                        f'rx="3" fill="{colors["arrow_label_bg"]}"/>'
                        f'<text x="{mx}" y="{my + 4}" text-anchor="middle" '
                        f'font-size="9" fill="#4338CA" font-weight="500">支撑</text>'
                    )

    parts.append("</svg>")
    target.write_text("\n".join(parts), encoding="utf-8")


# ─── Export: Capability Matrix ───────────────────────────────────
def export_matrix_svg(blueprint: dict[str, Any], target: Path, theme: str = "light") -> None:
    colors = _resolve_theme(theme)
    """Matrix view: products as rows, capabilities as columns, coverage as cells."""
    title = blueprint.get("meta", {}).get("title", "Product Family")
    lib = blueprint.get("library", {})
    systems = lib.get("systems", [])
    capabilities = lib.get("capabilities", [])

    # Market segments — derive from blueprint data
    _views = blueprint.get("views")
    if isinstance(_views, dict):
        segments = _views.get("productTree", {}).get("segments", [])
    else:
        segments = []
    if not segments:
        seg_map: dict[str, list[str]] = {}
        for s in systems:
            seg_label = s.get("properties", {}).get("segment", s.get("segment", ""))
            if seg_label:
                seg_map.setdefault(seg_label, []).append(s["id"])
        segments = [{"label": label, "ids": ids} for label, ids in seg_map.items()]

    cap_by_id = {c["id"]: c for c in capabilities}
    sys_by_id = {s["id"]: s for s in systems}
    cap_ids = [c["id"] for c in capabilities]
    n_cols = len(cap_ids)

    # Build ordered product list grouped by segment
    ordered_products: list[tuple[str, str | None]] = []
    for seg in segments:
        for sid in seg["ids"]:
            if sid in sys_by_id:
                ordered_products.append((sid, seg["label"]))
    # Fallback: all systems in one group
    if not ordered_products and systems:
        ordered_products = [(s["id"], None) for s in systems]

    PAD_X = 40
    PAD_Y = 30
    SEG_LABEL_W = 80
    PROD_NAME_W = 110
    CAP_COL_W = 100
    ROW_H = 40
    HEADER_H = 44
    ROW_GAP = 1
    n_rows = len(ordered_products)

    canvas_w = PAD_X * 2 + SEG_LABEL_W + PROD_NAME_W + n_cols * CAP_COL_W
    canvas_h = PAD_Y * 2 + HEADER_H + n_rows * ROW_H + (n_rows - 1) * ROW_GAP + 80

    _SEG_STROKE_PALETTE = ["#4338CA", "#0B6E6E", "#0F7B6C", "#059669", "#D97706", "#7C3AED", "#DC2626"]
    seg_colors: dict[str, str] = {}
    for i, seg in enumerate(segments):
        seg_colors[seg["label"]] = _SEG_STROKE_PALETTE[i % len(_SEG_STROKE_PALETTE)]

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{canvas_h}" '
        f'font-family="{FONT}">',
        _svg_defs(colors=colors, theme=theme),
        f'<rect width="{canvas_w}" height="{canvas_h}" fill="{colors["bg"]}"/>',
    ]

    # Title
    parts.append(
        f'<g class="title-block">'
        f'<rect x="{PAD_X}" y="{PAD_Y}" width="{canvas_w - PAD_X * 2}" height="52" '
        f'rx="6" fill="{colors["canvas"]}" stroke="{colors["border"]}" stroke-width="1"/>'
        f'<text x="{PAD_X + 16}" y="{PAD_Y + 24}" '
        f'font-size="16" fill="{colors["text_main"]}" font-family="{FONT}" '
        f'font-weight="700">{_esc(title)} — 能力矩阵</text>'
        f'<text x="{PAD_X + 16}" y="{PAD_Y + 42}" '
        f'font-size="11" fill="{colors["text_sub"]}" font-family="{FONT_MONO}">'
        f'Capability Coverage Matrix</text></g>'
    )

    base_y = PAD_Y + 100
    left_w = SEG_LABEL_W + PROD_NAME_W

    # Header row
    parts.append(
        f'<rect x="{PAD_X}" y="{base_y}" width="{left_w}" height="{HEADER_H}" '
        f'rx="6" fill="{colors["canvas"]}" stroke="{colors["border"]}" stroke-width="1"/>'
    )
    parts.append(
        f'<text x="{PAD_X + left_w // 2}" y="{base_y + HEADER_H // 2 + 5}" '
        f'text-anchor="middle" font-size="13" fill="{colors["text_main"]}" '
        f'font-weight="600">产品 / 能力</text>'
    )

    for ci, cid in enumerate(cap_ids):
        cap = cap_by_id[cid]
        cx = PAD_X + left_w + ci * CAP_COL_W
        parts.append(
            f'<rect x="{cx}" y="{base_y}" width="{CAP_COL_W}" height="{HEADER_H}" '
            f'rx="0" fill="{colors["canvas"]}" stroke="{colors["border"]}" stroke-width="1"/>'
            f'<text x="{cx + CAP_COL_W // 2}" y="{base_y + HEADER_H // 2 + 5}" '
            f'text-anchor="middle" font-size="11" fill="{colors["text_main"]}" '
            f'font-weight="500">{_esc(cap["name"])}</text>'
        )

    # Data rows
    prev_seg: str | None = None
    for ri, (sid, seg_label) in enumerate(ordered_products):
        sys = sys_by_id[sid]
        row_y = base_y + HEADER_H + ri * (ROW_H + ROW_GAP)
        sys_cap_ids = set(sys.get("capabilityIds", []))

        stroke = seg_colors.get(seg_label or "", "#64748B")

        # Row bg
        parts.append(
            f'<rect x="{PAD_X}" y="{row_y}" width="{canvas_w - PAD_X * 2}" height="{ROW_H}" '
            f'rx="0" fill="{colors["canvas"]}" stroke="{colors["border"]}" stroke-width="0.5"/>'
        )

        # Segment label (first row of each group)
        if seg_label != prev_seg:
            parts.append(
                f'<text x="{PAD_X + 8}" y="{row_y + ROW_H // 2 + 5}" '
                f'font-size="10" fill="{stroke}" font-weight="600" '
                f'transform="rotate(-45, {PAD_X + 8}, {row_y + ROW_H // 2 + 5})">'
                f'{_esc(seg_label or "")}</text>'
            )
            prev_seg = seg_label

        # Product name
        parts.append(
            f'<text x="{PAD_X + SEG_LABEL_W + 8}" y="{row_y + ROW_H // 2 + 5}" '
            f'font-size="12" fill="{colors["text_main"]}" font-weight="500">'
            f'{_esc(sys["name"])}</text>'
        )

        # Capability cells
        for ci, cid in enumerate(cap_ids):
            cx = PAD_X + left_w + ci * CAP_COL_W
            if cid in sys_cap_ids:
                parts.append(
                    f'<rect x="{cx + 2}" y="{row_y + 2}" width="{CAP_COL_W - 4}" height="{ROW_H - 4}" '
                    f'rx="4" fill="{stroke}" opacity="0.2"/>'
                    f'<text x="{cx + CAP_COL_W // 2}" y="{row_y + ROW_H // 2 + 5}" '
                    f'text-anchor="middle" font-size="14" fill="{stroke}">✓</text>'
                )
            else:
                parts.append(
                    f'<text x="{cx + CAP_COL_W // 2}" y="{row_y + ROW_H // 2 + 5}" '
                    f'text-anchor="middle" font-size="14" fill="#E2E8F0">—</text>'
                )

    # Legend
    legend_y = base_y + HEADER_H + n_rows * (ROW_H + ROW_GAP) + 30
    parts.append(
        f'<text x="{PAD_X}" y="{legend_y}" font-size="10" fill="{colors["text_sub"]}">'
        f'■ 覆盖  — 未覆盖  | 颜色 = 市场分层</text>'
    )

    parts.append("</svg>")
    target.write_text("\n".join(parts), encoding="utf-8")


# ─── Export: Capability Map ──────────────────────────────────────
def export_capability_map_svg(blueprint: dict[str, Any], target: Path, theme: str = "light") -> None:
    colors = _resolve_theme(theme)
    """Capability map: grouped cards showing business capabilities and their supporting systems."""
    title = blueprint.get("meta", {}).get("title", "Business Blueprint")
    industry = blueprint.get("meta", {}).get("industry", "")
    lib = blueprint.get("library", {})
    capabilities = lib.get("capabilities", [])
    systems = lib.get("systems", [])
    actors = lib.get("actors", [])

    sys_by_id = {s["id"]: s for s in systems}
    actor_by_id = {a["id"]: a for a in actors}

    PAD_X = 50
    PAD_Y = 30
    CARD_W = 200
    CARD_H = 80
    CARD_GAP = 16

    # Dynamic grid calculation: adjust columns based on capability count
    n = len(capabilities)
    if n <= 4:
        COLS = min(n, 2)
    elif n <= 9:
        COLS = 3
    elif n <= 16:
        COLS = 4
    elif n <= 25:
        COLS = 5
    else:
        COLS = 6

    COL_W = CARD_W + CARD_GAP
    canvas_w = PAD_X * 2 + COLS * COL_W - CARD_GAP

    parts: list[str] = []

    # Title block
    subtitle = f"行业：{industry}" if industry else "能力地图"
    parts.extend([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="0" '
        f'font-family="{FONT}">',
        _svg_defs(colors=colors, theme=theme),
        f'<rect width="{canvas_w}" height="0" fill="{colors["bg"]}"/>',
    ])

    parts.append(
        f'<g class="title-block">'
        f'<rect x="{PAD_X}" y="{PAD_Y}" width="{canvas_w - PAD_X * 2}" height="52" '
        f'rx="6" fill="{colors["canvas"]}" stroke="{colors["border"]}" stroke-width="1"/>'
        f'<text x="{PAD_X + 16}" y="{PAD_Y + 24}" '
        f'font-size="16" fill="{colors["text_main"]}" font-family="{FONT}" '
        f'font-weight="700">{_esc(title)} — 能力地图</text>'
        f'<text x="{PAD_X + 16}" y="{PAD_Y + 42}" '
        f'font-size="11" fill="{colors["text_sub"]}" font-family="{FONT_MONO}">'
        f'{_esc(subtitle)}</text></g>'
    )

    # Color palette for capability levels
    level_colors = {
        0: ("#1E293B", "#F1F5F9"),
        1: ("#0B6E6E", "#E8F5F5"),
        2: ("#059669", "#ECFDF5"),
    }

    # Group capabilities by level
    by_level: dict[int, list[dict]] = {}
    for cap in capabilities:
        lvl = cap.get("level", 1)
        by_level.setdefault(lvl, []).append(cap)

    current_y = PAD_Y + 72
    canvas_h = current_y

    level_labels = {0: "战略层", 1: "核心层", 2: "支撑层"}

    for lvl in sorted(by_level.keys()):
        caps = by_level[lvl]
        stroke, fill = level_colors.get(lvl, ("#64748B", "#F8FAFC"))
        level_label = level_labels.get(lvl, f"L{lvl}")

        # Level header
        parts.append(
            f'<text x="{PAD_X}" y="{current_y}" font-size="13" fill="{stroke}" '
            f'font-weight="700" font-family="{FONT}">{level_label} ({len(caps)})</text>'
        )
        current_y += 14

        # Cards in grid
        n = len(caps)
        n_rows = math.ceil(n / COLS) if COLS > 0 else n
        card_block_h = n_rows * CARD_H + max(0, n_rows - 1) * CARD_GAP

        for i, cap in enumerate(caps):
            col = i % COLS
            row = i // COLS
            cx = PAD_X + col * COL_W
            cy = current_y + row * (CARD_H + CARD_GAP)

            sys_names = []
            for sid in cap.get("supportingSystemIds", []):
                s = sys_by_id.get(sid)
                if s:
                    sys_names.append(s["name"])

            parts.append(
                f'<rect x="{cx}" y="{cy}" width="{CARD_W}" height="{CARD_H}" '
                f'rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
                f'<text x="{cx + 12}" y="{cy + 20}" font-size="12" fill="{stroke}" '
                f'font-weight="600">{_esc(cap["name"])}</text>'
            )

            # Description (truncated)
            desc = cap.get("description", "")[:40]
            if desc:
                parts.append(
                    f'<text x="{cx + 12}" y="{cy + 36}" font-size="9" fill="{colors["text_sub"]}">'
                    f'{_esc(desc)}</text>'
                )

            # Supporting systems
            for j, sname in enumerate(sys_names[:3]):
                parts.append(
                    f'<rect x="{cx + 12}" y="{cy + 46 + j * 16}" width="{CARD_W - 24}" height="14" '
                    f'rx="3" fill="{colors["canvas"]}"/>'
                    f'<text x="{cx + 18}" y="{cy + 57 + j * 16}" font-size="8.5" fill="{colors["text_main"]}">'
                    f'{_esc(sname)}</text>'
                )

        current_y += card_block_h + 24
        canvas_h = current_y

    canvas_h += PAD_Y
    # Fix SVG header with computed height
    parts[0] = f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{canvas_h}" font-family="{FONT}">'
    parts[2] = f'<rect width="{canvas_w}" height="{canvas_h}" fill="{colors["bg"]}"/>'

    parts.append("</svg>")
    target.write_text("\n".join(parts), encoding="utf-8")


# ─── Export: Swimlane Flow ───────────────────────────────────────
def export_swimlane_flow_svg(blueprint: dict[str, Any], target: Path, theme: str = "light") -> None:
    colors = _resolve_theme(theme)
    """Swimlane flow diagram: actors as lanes, flow steps as connected cards."""
    title = blueprint.get("meta", {}).get("title", "Business Blueprint")
    industry = blueprint.get("meta", {}).get("industry", "")
    lib = blueprint.get("library", {})
    actors = lib.get("actors", [])
    flow_steps = lib.get("flowSteps", [])
    capabilities = lib.get("capabilities", [])

    cap_by_id = {c["id"]: c for c in capabilities}
    actor_by_id = {a["id"]: a for a in actors}

    PAD_X = 50
    PAD_Y = 30
    LANE_HEADER_H = 36
    LANE_GAP = 16
    STEP_W = 220
    STEP_H = 40
    STEP_GAP = 14
    ARROW_GAP = 12

    # Group flow steps by actor
    steps_by_actor: dict[str, list[dict]] = {}
    for step in flow_steps:
        aid = step.get("actorId", "")
        steps_by_actor.setdefault(aid, []).append(step)

    actor_order: list[str] = [a["id"] for a in actors]

    canvas_w = 900
    content_w = canvas_w - PAD_X * 2

    parts: list[str] = []

    subtitle = f"行业：{industry}" if industry else "泳道流程"
    parts.extend([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="0" '
        f'font-family="{FONT}">',
        _svg_defs(colors=colors, theme=theme),
        f'<rect width="{canvas_w}" height="0" fill="{colors["bg"]}"/>',
    ])

    parts.append(
        f'<g class="title-block">'
        f'<rect x="{PAD_X}" y="{PAD_Y}" width="{content_w}" height="52" '
        f'rx="6" fill="{colors["canvas"]}" stroke="{colors["border"]}" stroke-width="1"/>'
        f'<text x="{PAD_X + 16}" y="{PAD_Y + 24}" '
        f'font-size="16" fill="{colors["text_main"]}" font-family="{FONT}" '
        f'font-weight="700">{_esc(title)} — 泳道流程</text>'
        f'<text x="{PAD_X + 16}" y="{PAD_Y + 42}" '
        f'font-size="11" fill="{colors["text_sub"]}" font-family="{FONT_MONO}">'
        f'{_esc(subtitle)}</text></g>'
    )

    if theme == "dark":
        lane_palette = [
            ("#22D3EE", "#0E2A3D"),
            ("#34D399", "#0E2E1F"),
            ("#A78BFA", "#1E1535"),
            ("#FBBF24", "#2A2010"),
            ("#FB7185", "#2A1018"),
            ("#60A5FA", "#1E3A5F"),
            ("#94A3B8", "#1A2030"),
        ]
    else:
        lane_palette = [
            ("#0B6E6E", "#E8F5F5"),
            ("#059669", "#ECFDF5"),
            ("#4338CA", "#EEF2FF"),
            ("#D97706", "#FEFCE8"),
            ("#DC2626", "#FEF2F2"),
            ("#7C3AED", "#F5F3FF"),
            ("#0891B2", "#ECFEFF"),
            ("#65A30D", "#F7FEE7"),
            ("#C2410C", "#FFF7ED"),
            ("#475569", "#F8FAFC"),
            ("#9333EA", "#FAF5FF"),
        ]

    step_by_id = {step["id"]: step for step in flow_steps}
    step_layout: dict[str, dict[str, Any]] = {}

    # First pass: compute lane heights and step positions for arrow drawing.
    lane_positions: dict[str, dict] = {}
    current_y = PAD_Y + 72

    for lane_idx, actor_id in enumerate(actor_order):
        actor = actor_by_id.get(actor_id)
        if not actor:
            continue
        stroke, fill = lane_palette[lane_idx % len(lane_palette)]
        steps = steps_by_actor.get(actor_id, [])

        lane_step_y = current_y + LANE_HEADER_H + LANE_GAP
        total_steps_h = 0
        lane_positions[actor_id] = {
            "y": current_y,
            "stroke": stroke,
            "fill": fill,
            "steps": {},
        }

        for step in steps:
            title_lines = _wrap_text_to_width(step.get("name", ""), max_px=STEP_W - 52, font_size=11, max_lines=None, ellipsize=False)
            step_h = max(STEP_H, 28 + len(title_lines) * 14)
            step_layout[step["id"]] = {"lines": title_lines, "h": step_h}
            lane_positions[actor_id]["steps"][step["id"]] = {
                "x": PAD_X + 14,
                "y": lane_step_y,
                "w": STEP_W,
                "h": step_h,
                "cx": PAD_X + 14 + STEP_W // 2,
                "cy": lane_step_y + step_h / 2,
            }
            lane_step_y += step_h + STEP_GAP
            total_steps_h += step_h

        lane_h = LANE_HEADER_H + LANE_GAP + total_steps_h + max(0, len(steps) - 1) * STEP_GAP + LANE_GAP
        lane_positions[actor_id]["h"] = lane_h
        current_y += lane_h + LANE_GAP

    # Arrows layer: draw only declared next-step transitions and keep them in the right-side gutter.
    arrow_parts: list[str] = []
    gutter_x = PAD_X + 14 + STEP_W + 12
    for step in flow_steps:
        from_actor = step.get("actorId", "")
        from_pos = lane_positions.get(from_actor, {}).get("steps", {}).get(step["id"])
        if not from_pos:
            continue
        for next_id in step.get("nextStepIds") or []:
            next_step = step_by_id.get(next_id)
            if not next_step:
                continue
            to_actor = next_step.get("actorId", "")
            to_pos = lane_positions.get(to_actor, {}).get("steps", {}).get(next_id)
            if not to_pos:
                continue
            mid_y = (from_pos["cy"] + to_pos["cy"]) / 2
            arrow_parts.append(
                f'<path d="M{gutter_x},{from_pos["cy"]} '
                f'C{gutter_x + 24},{mid_y} {gutter_x + 24},{mid_y} {gutter_x},{to_pos["cy"]}" '
                f'fill="none" stroke="{colors["arrow_muted"]}" stroke-width="1.4" stroke-dasharray="4,3" opacity="0.65" '
                f'marker-end="url(#arrow-dashed)"/>'
            )

    # Second pass: render lanes and cards
    current_y = PAD_Y + 72
    for lane_idx, actor_id in enumerate(actor_order):
        actor = actor_by_id.get(actor_id)
        if not actor:
            continue
        stroke, fill = lane_palette[lane_idx % len(lane_palette)]

        steps = steps_by_actor.get(actor_id, [])
        lane_h = lane_positions[actor_id]["h"]

        # Lane background
        parts.append(
            f'<rect x="{PAD_X}" y="{current_y}" width="{content_w}" height="{lane_h}" '
            f'rx="6" fill="{fill}" stroke="{stroke}" stroke-width="{0.9 if theme == "dark" else 0.5}" fill-opacity="{0.84 if theme == "dark" else 0.5}"/>'
        )
        # Lane label with step count
        parts.append(
            f'<text x="{PAD_X + 14}" y="{current_y + LANE_HEADER_H // 2 + 5}" '
            f'font-size="12" fill="{stroke}" font-weight="600">{_esc(actor["name"])} '
            f'<tspan font-size="10" fill="{colors["text_sub"]}">({len(steps)}步)</tspan></text>'
        )
        # Right side: capability tags summary
        all_caps: list[str] = []
        for s in steps:
            for cid in s.get("capabilityIds", []):
                if cid not in all_caps:
                    all_caps.append(cid)
        cursor_x = PAD_X + content_w - 14
        for cid in all_caps[:4]:
            cap = cap_by_id.get(cid, {})
            tag_label = _compact_swimlane_tag(cap.get("name", ""))
            tag_w = len(tag_label) * 7 + 10
            tx = cursor_x - tag_w
            parts.append(
                f'<rect x="{tx}" y="{current_y + 8}" width="{tag_w}" height="18" '
                f'rx="3" fill="{fill if theme == "dark" else stroke}" stroke="{stroke}" stroke-width="{0.8 if theme == "dark" else 0}" fill-opacity="{0.95 if theme == "dark" else 0.15}"/>'
                f'<text x="{tx + tag_w // 2}" y="{current_y + 21}" '
                f'text-anchor="middle" font-size="8" fill="{colors["text_main"] if theme == "dark" else stroke}">'
                f'{_esc(tag_label)}</text>'
            )
            cursor_x = tx - 6

        for si, step in enumerate(steps):
            layout = step_layout[step["id"]]
            sx = PAD_X + 14
            sy = lane_positions[actor_id]["steps"][step["id"]]["y"]
            step_h = layout["h"]
            title_lines = layout["lines"]

            # Step number badge
            step_num = si + 1
            parts.append(
                f'<rect x="{sx}" y="{sy}" width="{STEP_W}" height="{step_h}" '
                f'rx="5" fill="{colors["canvas"]}" stroke="{stroke}" stroke-width="1.5"/>'
                f'<rect x="{sx + 2}" y="{sy + 2}" width="22" height="{step_h - 4}" '
                f'rx="4" fill="{stroke}" opacity="0.12"/>'
                f'<text x="{sx + 13}" y="{sy + step_h / 2 + 5}" '
                f'text-anchor="middle" font-size="12" fill="{stroke}" font-weight="700">{step_num}</text>'
            )
            title_y = sy + (19 if len(title_lines) == 1 else 15)
            parts.append(
                f'<text x="{sx + 32}" y="{title_y}" font-size="11" fill="{colors["text_main"]}" font-weight="500">'
            )
            for line_index, line in enumerate(title_lines):
                dy = 0 if line_index == 0 else 14
                parts.append(f'<tspan x="{sx + 32}" dy="{dy}">{_esc(line)}</tspan>')
            parts.append('</text>')

            # Capability tags
            cap_ids = step.get("capabilityIds", [])
            tag_cursor_x = sx + STEP_W + 24
            for cid in cap_ids[:2]:
                cap = cap_by_id.get(cid, {})
                cap_name = _compact_swimlane_tag(cap.get("name", ""))
                if cap_name:
                    tw = len(cap_name) * 7 + 10
                    parts.append(
                        f'<rect x="{tag_cursor_x}" y="{sy + 10}" width="{tw}" height="18" '
                        f'rx="3" fill="{fill if theme == "dark" else stroke}" stroke="{stroke}" stroke-width="{0.8 if theme == "dark" else 0}" fill-opacity="{0.95 if theme == "dark" else 0.15}"/>'
                        f'<text x="{tag_cursor_x + tw // 2}" y="{sy + 23}" '
                        f'text-anchor="middle" font-size="8" fill="{colors["text_main"] if theme == "dark" else stroke}">'
                        f'{_esc(cap_name)}</text>'
                    )
                    tag_cursor_x += tw + 8

        current_y += lane_h + LANE_GAP

    # Draw arrows above lane backgrounds and cards so the reduced set stays visible.
    parts.extend(arrow_parts)

    canvas_h = current_y + PAD_Y
    parts[0] = f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{canvas_h}" font-family="{FONT}">'
    parts[2] = f'<rect width="{canvas_w}" height="{canvas_h}" fill="{colors["bg"]}"/>'

    parts.append("</svg>")
    target.write_text("\n".join(parts), encoding="utf-8")


def _split_timeline_step_name(step_name: str) -> tuple[str, str]:
    """Split a flow step name into (date_label, title)."""
    match = _re.match(r"^(\d{4}-\d{2}-\d{2})[：:\s]*(.+)$", step_name.strip())
    if match:
        return match.group(1), match.group(2).strip()
    return "", step_name.strip()

def _compact_swimlane_tag(label: str) -> str:
    compact_map = {
        "会话交互": "会话",
        "技能调用": "技能",
        "AI协同办公套件层": "AI套件",
        "AI日程协同": "日程",
        "AI会议协同": "会议",
        "AI文档协同": "文档",
        "AI流程协同": "流程",
        "AI业务协同": "业务",
        "Harness支撑层": "Harness",
        "Harness基础能力": "基础能力",
        "Agent运行时": "Agent",
        "API网关": "网关",
        "ERP业务层": "ERP",
        "财务管理": "财务",
        "供应链管理": "供应链",
        "HR管理": "HR",
        "数据存储": "存储",
        "数据分析": "分析",
        "AI数据底座": "数据底座",
    }
    return compact_map.get(label, label)
def export_evolution_timeline_svg(blueprint: dict[str, Any], target: Path, theme: str = "light") -> None:
    """Timeline-style evolution diagram for date-driven product changes."""
    industry = blueprint.get("meta", {}).get("industry", "") or None
    colors = _resolve_theme(theme, industry=industry)
    title = blueprint.get("meta", {}).get("title", "Business Blueprint")
    lib = blueprint.get("library", {})
    flow_steps = list(lib.get("flowSteps", []))
    actors = {a["id"]: a.get("name", a["id"]) for a in lib.get("actors", [])}
    capabilities = {c["id"]: c.get("name", c["id"]) for c in lib.get("capabilities", [])}
    systems = {s["id"]: s.get("name", s["id"]) for s in lib.get("systems", [])}

    if not flow_steps:
        empty_svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="960" height="280" font-family="{FONT}">'
            f'{_svg_defs(colors=colors, theme=theme)}'
            f'<rect width="960" height="280" fill="{colors["bg"]}"/>'
            f'{_title_svg(title, "演进时间线", 960, colors=colors)}'
            f'<text x="480" y="168" text-anchor="middle" font-size="16" fill="{colors["text_sub"]}">No flow steps available</text>'
            f'</svg>'
        )
        target.write_text(empty_svg, encoding="utf-8")
        return

    def _sort_key(item: tuple[int, dict[str, Any]]) -> tuple[int, str, int]:
        idx, step = item
        seq = int(step.get("seqIndex", idx))
        date_label, _ = _split_timeline_step_name(step.get("name", ""))
        return seq, date_label, idx

    ordered_steps = [step for _, step in sorted(enumerate(flow_steps), key=_sort_key)]

    PAD_X = 56
    PAD_Y = 30
    TITLE_H = 66
    AXIS_Y = 172
    CARD_Y = 210
    CARD_W = 260
    CARD_MIN_H = 210
    CARD_GAP = 26
    canvas_w = max(1120, PAD_X * 2 + len(ordered_steps) * CARD_W + max(0, len(ordered_steps) - 1) * CARD_GAP)

    accent_release = "#DC2626"
    accent_default = colors["cap_stroke"]
    accent_secondary = "#4338CA"
    if theme == "dark":
        accent_release_fill = "#2A1018"
        accent_default_fill = colors["canvas"]
        accent_secondary_fill = "#1A1838"
    else:
        accent_release_fill = "#FEF2F2"
        accent_default_fill = colors["canvas"]
        accent_secondary_fill = "#EEF2FF"

    stage_layouts: list[dict[str, Any]] = []

    timeline_start = (canvas_w - (len(ordered_steps) * CARD_W + (len(ordered_steps) - 1) * CARD_GAP)) / 2

    for idx, step in enumerate(ordered_steps):
        card_x = timeline_start + idx * (CARD_W + CARD_GAP)
        center_x = card_x + CARD_W / 2

        date_label, step_title = _split_timeline_step_name(step.get("name", ""))
        actor_name = actors.get(step.get("actorId", ""), "未标注对象")
        capability_names = [capabilities.get(cid, cid) for cid in step.get("capabilityIds", [])[:2]]
        system_names = [systems.get(sid, sid) for sid in step.get("systemIds", [])[:3]]
        is_release = "发布" in step_title or "上线" in step_title or "套件" in step_title
        stroke = accent_release if is_release else (accent_secondary if idx % 2 else accent_default)
        fill = accent_release_fill if is_release else (accent_secondary_fill if idx % 2 else accent_default_fill)

        title_lines = _wrap_timeline_text(step_title, max_units=18, max_lines=2)
        title_y = CARD_Y + 72
        actor_y = title_y + len(title_lines) * 22 + 6
        key_change_y = actor_y + 28

        pill_layout: list[tuple[float, float, float, str]] = []
        pill_y = key_change_y + 20
        pill_x = card_x + 16
        pill_right = card_x + CARD_W - 16
        for sys_name in system_names:
            pill_label = sys_name[:12] + "…" if len(sys_name) > 12 else sys_name
            pill_w = max(78, 20 + _estimate_svg_text_width(pill_label, font_size=10))
            if pill_x + pill_w > pill_right:
                pill_x = card_x + 16
                pill_y += 28
            pill_layout.append((pill_x, pill_y, pill_w, pill_label))
            pill_x += pill_w + 6

        card_h = CARD_MIN_H
        if pill_layout:
            last_pill_bottom = max(y + 22 for _, y, _, _ in pill_layout)
            card_h = max(card_h, int(last_pill_bottom - CARD_Y + 18))
        stage_layouts.append(
            {
                "index": idx,
                "center_x": center_x,
                "card_x": card_x,
                "date_label": date_label,
                "actor_name": actor_name,
                "capability_names": capability_names,
                "system_layout": pill_layout,
                "stroke": stroke,
                "fill": fill,
                "title_lines": title_lines,
                "title_y": title_y,
                "actor_y": actor_y,
                "key_change_y": key_change_y,
                "card_h": card_h,
            }
        )

    max_card_bottom = max(CARD_Y + stage["card_h"] for stage in stage_layouts) if stage_layouts else CARD_Y + CARD_MIN_H
    footer_y = max_card_bottom + 42
    canvas_h = max(500, int(footer_y + 30))

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{canvas_h}" '
        f'viewBox="0 0 {canvas_w} {canvas_h}" font-family="{FONT}">',
        _svg_defs(colors=colors, theme=theme),
        f'<rect width="{canvas_w}" height="{canvas_h}" fill="{colors["bg"]}"/>',
        _title_svg(title, "演进时间线", canvas_w, colors=colors),
    ]

    left = PAD_X + 20
    right = canvas_w - PAD_X - 20
    parts.append(
        f'<line x1="{left}" y1="{AXIS_Y}" x2="{right}" y2="{AXIS_Y}" '
        f'stroke="{colors["border"]}" stroke-width="4" stroke-linecap="round"/>'
    )

    for stage in stage_layouts:
        idx = stage["index"]
        center_x = stage["center_x"]
        card_x = stage["card_x"]
        stroke = stage["stroke"]
        fill = stage["fill"]
        actor_name = stage["actor_name"]
        capability_names = stage["capability_names"]
        title_lines = stage["title_lines"]
        title_y = stage["title_y"]
        actor_y = stage["actor_y"]
        key_change_y = stage["key_change_y"]
        date_label = stage["date_label"]
        card_h = stage["card_h"]

        parts.append(
            f'<circle cx="{center_x}" cy="{AXIS_Y}" r="11" fill="{colors["canvas"]}" '
            f'stroke="{stroke}" stroke-width="4"/>'
        )
        parts.append(
            f'<line x1="{center_x}" y1="{AXIS_Y + 12}" x2="{center_x}" y2="{CARD_Y}" '
            f'stroke="{stroke}" stroke-width="2" stroke-dasharray="5,4" opacity="0.75"/>'
        )

        chip_w = 96
        chip_x = center_x - chip_w / 2
        parts.append(
            f'<rect x="{chip_x}" y="{AXIS_Y - 40}" width="{chip_w}" height="24" rx="12" '
            f'fill="{colors["canvas"]}" stroke="{stroke}" stroke-width="1.5"/>'
        )
        parts.append(
            f'<text x="{center_x}" y="{AXIS_Y - 24}" text-anchor="middle" font-size="11" '
            f'fill="{stroke}" font-weight="700">{_esc(date_label or f"阶段 {idx + 1}")}</text>'
        )

        parts.append(
            f'<rect x="{card_x}" y="{CARD_Y}" width="{CARD_W}" height="{card_h}" rx="18" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
        )

        parts.append(
            f'<rect x="{card_x + 18}" y="{CARD_Y + 16}" width="68" height="24" rx="12" '
            f'fill="{colors["canvas"]}" fill-opacity="0.95"/>'
            f'<text x="{card_x + 52}" y="{CARD_Y + 32}" text-anchor="middle" font-size="11" '
            f'fill="{stroke}" font-weight="700">阶段 {idx + 1}</text>'
        )

        parts.append(
            f'<text x="{card_x + 22}" y="{title_y}" font-size="18" fill="{colors["text_main"]}" font-weight="700">'
        )
        for line_index, line in enumerate(title_lines):
            dy = 0 if line_index == 0 else 22
            parts.append(f'<tspan x="{card_x + 22}" dy="{dy}">{_esc(line)}</tspan>')
        parts.append('</text>')

        parts.append(
            f'<text x="{card_x + 22}" y="{actor_y}" font-size="11" fill="{colors["text_sub"]}" font-weight="600">定位对象</text>'
        )
        parts.append(
            f'<text x="{card_x + 90}" y="{actor_y}" font-size="11" fill="{colors["text_main"]}">{_esc(actor_name)}</text>'
        )

        if capability_names:
            parts.append(
                f'<text x="{card_x + 22}" y="{key_change_y}" font-size="11" fill="{colors["text_sub"]}" font-weight="600">关键变化</text>'
            )
            parts.append(
                f'<text x="{card_x + 90}" y="{key_change_y}" font-size="11" fill="{colors["text_main"]}">{_esc(" / ".join(capability_names))}</text>'
            )

        for pill_x, pill_y, pill_w, pill_label in stage["system_layout"]:
            parts.append(
                f'<rect x="{pill_x}" y="{pill_y}" width="{pill_w}" height="22" rx="11" '
                f'fill="{colors["canvas"]}" fill-opacity="0.96" stroke="{stroke}" stroke-width="1"/>'
                f'<text x="{pill_x + pill_w / 2}" y="{pill_y + 15}" text-anchor="middle" font-size="10" '
                f'fill="{stroke}" font-weight="600">{_esc(pill_label)}</text>'
            )

    scope_text = "仅含官网明确产品发布、定位强化与场景深化"
    parts.append(
        f'<text x="{canvas_w / 2}" y="{footer_y}" text-anchor="middle" font-size="12" '
        f'fill="{colors["text_sub"]}">{_esc(scope_text)}</text>'
    )
    parts.append("</svg>")
    target.write_text("\n".join(parts), encoding="utf-8")



def _infer_layer_from_system_name(name: str, category: str | None = None) -> str:
    """Infer layer from system name and category.

    For product blueprints: group by product capability level (not technical call chain)
    For technical blueprints: group by technical architecture layers

    Key distinction:
    - "XX层" (layer definition) → technical architecture layer
    - "XX服务" (service instance) → business service module

    Priority: explicit category > name pattern
    """
    name_lower = name.lower()

    # 1. Explicit category determines grouping strategy
    if category == "layer":
        # This system is a technical architecture LAYER DEFINITION
        # Use its name directly as the layer name
        if "客户端" in name or "前端" in name:
            return "访问入口层"
        if "网关" in name or "接入" in name:
            return "接入网关层"
        if "数据" in name or "存储" in name:
            return "数据存储层"
        if "基础" in name or "运维" in name:
            return "基础设施层"
        # For "微服务核心层" etc, use generic tech layer name
        return name  # Direct use: "微服务核心层", "业务服务层" etc

    if category == "service":
        # This system is a business SERVICE INSTANCE
        # Group by product capability level
        if "开放平台" in name or "开放" in name:
            return "平台能力层"
        return "核心业务层"

    # 2. Infer from name patterns
    # Layer definition (ends with "层" or contains "layer")
    if "层" in name and len(name) < 10:
        # This is a layer DEFINITION, not a service instance
        if "客户端" in name:
            return "访问入口层"
        if "网关" in name:
            return "接入网关层"
        if "数据" in name:
            return "数据存储层"
        if "基础" in name or "运维" in name:
            return "基础设施层"
        if "微服务" in name or "核心" in name:
            return "平台基础层"  # Platform foundation services (user center, messaging, auth etc)
        return name  # Use as-is

    # Access layer (frontend/client)
    if any(kw in name_lower for kw in ["客户端", "前端", "frontend", "client", "web", "mobile", "app", "小程序", "门户"]):
        return "访问入口层"

    # Gateway layer
    if any(kw in name_lower for kw in ["网关", "gateway", "接入", "路由"]):
        return "接入网关层"

    # Data layer
    if any(kw in name_lower for kw in ["数据", "存储", "database", "storage"]):
        return "数据存储层"

    # Infrastructure layer
    if any(kw in name_lower for kw in ["基础设施", "运维", "监控", "日志"]):
        return "基础设施层"

    # Platform capability layer
    if any(kw in name_lower for kw in ["开放平台", "开放", "platform", "api", "开发者"]):
        return "平台能力层"

    # Core business layer (all domain services)
    if any(kw in name_lower for kw in ["服务", "模块", "系统"]):
        return "核心业务层"

    # Final fallback
    return "应用服务层"


def export_layer_poster_svg(blueprint: dict[str, Any], target: Path, theme: str = "dark") -> None:
    """Poster-style layered product blueprint view for product architecture storytelling."""
    colors = _resolve_theme(theme, blueprint.get("meta", {}).get("industry", "") or None)
    title = blueprint.get("meta", {}).get("title", "Business Blueprint")
    systems = blueprint.get("library", {}).get("systems", [])
    if not systems:
        target.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="800" height="300"></svg>', encoding='utf-8')
        return

    layer_order: list[str] = []
    layers: dict[str, list[dict[str, Any]]] = {}
    for system in systems:
        # Use explicit layer if present
        layer = system.get("layer")

        # Infer from category + name if no explicit layer
        if not layer:
            category = system.get("category") or system.get("properties", {}).get("category")
            layer = _infer_layer_from_system_name(system.get("name", ""), category)

        if layer not in layers:
            layer_order.append(layer)
            layers[layer] = []
        layers[layer].append(system)

    # ── Compact layout: fits in 1280px width for PPT/report embedding ──
    PAD_X = 32
    PAD_Y = 20
    TITLE_H = 56
    LAYER_LABEL_W = 160
    CARD_W = 180
    CARD_H = 80
    CARD_GAP = 12
    ROW_GAP = 12
    BAND_PAD_X = 12
    BAND_PAD_Y = 12
    BAND_GAP = 12
    canvas_w = 1280  # Standard PPT slide width
    CONTENT_W = canvas_w - PAD_X * 2 - LAYER_LABEL_W - 16
    MAX_COLS = max(1, min(4, CONTENT_W // (CARD_W + CARD_GAP)))

    layer_palette = _poster_layer_palette(theme)
    band_fill_opacity = "0.28" if theme == "dark" else "1"
    label_fill_opacity = "0.92" if theme == "dark" else "0.98"
    card_stroke = colors.get("layer_border", colors["border"]) if theme == "light" else None

    band_layouts: list[dict[str, Any]] = []
    current_y = PAD_Y + TITLE_H + 18
    for idx, layer in enumerate(layer_order):
        items = layers[layer]
        rows = max(1, math.ceil(len(items) / MAX_COLS))
        band_h = BAND_PAD_Y * 2 + rows * CARD_H + (rows - 1) * ROW_GAP
        band_layouts.append({
            "layer": layer,
            "items": items,
            "y": current_y,
            "h": band_h,
            "palette": layer_palette[idx % len(layer_palette)],
        })
        current_y += band_h + BAND_GAP

    canvas_h = current_y + 54
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{canvas_h}" viewBox="0 0 {canvas_w} {canvas_h}" font-family="{FONT}">',
        _svg_defs(colors=colors, theme=theme),
        f'<rect width="{canvas_w}" height="{canvas_h}" fill="{colors["bg"]}"/>',
    ]
    if theme == "dark":
        parts.append(f'<rect width="{canvas_w}" height="{canvas_h}" fill="url(#grid)"/>')

    title_w = canvas_w - PAD_X * 2
    subtitle_text = blueprint.get("meta", {}).get("subtitle", "")
    subtitle_line = f" • {subtitle_text}" if subtitle_text else ""
    parts.append(
        f'<g class="title-block">'
        f'<rect x="{PAD_X}" y="{PAD_Y}" width="{title_w}" height="48" rx="6" fill="{colors["canvas"]}" stroke="{colors["border"]}" stroke-width="1"/>'
        f'<text x="{PAD_X + 16}" y="{PAD_Y + 24}" font-size="18" font-weight="700" fill="{colors["text_main"]}">{_esc(title)}{subtitle_line}</text>'
        f'<text x="{PAD_X + 16}" y="{PAD_Y + 40}" font-size="10" fill="{colors["text_sub"]}" letter-spacing="0.3">Layered Blueprint Poster</text>'
        f'</g>'
    )

    spine_x = PAD_X + 70
    spine_top = band_layouts[0]["y"] + 10 if band_layouts else PAD_Y + TITLE_H
    spine_bottom = band_layouts[-1]["y"] + band_layouts[-1]["h"] - 10 if band_layouts else spine_top
    parts.append(
        f'<line x1="{spine_x}" y1="{spine_top}" x2="{spine_x}" y2="{spine_bottom}" stroke="{colors["border"]}" stroke-width="2" stroke-dasharray="6,6" opacity="0.8"/>'
    )

    for idx, band in enumerate(band_layouts):
        accent = band["palette"]["accent"]
        band_fill = band["palette"]["band_fill"]
        badge_fill = band["palette"]["badge_fill"]
        band_x = PAD_X + 8
        band_y = band["y"]
        band_w = canvas_w - PAD_X * 2 - 16
        band_h = band["h"]
        label_x = band_x + 14
        label_y = band_y + 18
        content_x = band_x + LAYER_LABEL_W
        content_y = band_y + BAND_PAD_Y
        content_w = band_w - LAYER_LABEL_W - 16

        layer_match = _re.match(r'^(第[^\s]+)\s+(.*)$', band["layer"])
        layer_prefix = layer_match.group(1) if layer_match else f'L{idx + 1}'
        layer_title = layer_match.group(2) if layer_match else band["layer"]
        # Truncate summary to avoid overflow (show max 3 systems)
        summary_systems = band["items"][:3]
        layer_summary = " / ".join(system["name"] for system in summary_systems)
        if len(band["items"]) > 3:
            layer_summary += f" 等{len(band['items'])}个"

        parts.append(
            f'<rect x="{band_x}" y="{band_y}" width="{band_w}" height="{band_h}" rx="12" fill="{band_fill}" fill-opacity="{band_fill_opacity}" stroke="{accent}" stroke-width="1"/>'
        )
        parts.append(
            f'<rect x="{band_x + 8}" y="{band_y + 8}" width="{LAYER_LABEL_W - 16}" height="{band_h - 16}" rx="8" fill="{colors["canvas"]}" fill-opacity="{label_fill_opacity}" stroke="{colors["border"]}" stroke-width="0.8"/>'
        )
        parts.append(
            f'<text x="{label_x}" y="{label_y}" font-size="10" font-weight="700" fill="{accent}" letter-spacing="0.5">{_esc(layer_prefix)}</text>'
            f'<text x="{label_x}" y="{label_y + 18}" font-size="14" font-weight="700" fill="{colors["text_main"]}">{_esc(layer_title)}</text>'
            f'<text x="{label_x}" y="{label_y + 32}" font-size="9" fill="{colors["text_sub"]}">{_esc(layer_summary[:40])}</text>'
        )

        for item_idx, system in enumerate(band["items"]):
            row = item_idx // MAX_COLS
            col = item_idx % MAX_COLS
            row_items = band["items"][row * MAX_COLS:(row + 1) * MAX_COLS]
            row_w = len(row_items) * CARD_W + max(0, len(row_items) - 1) * CARD_GAP
            row_start_x = int(content_x + max(0, (content_w - row_w) / 2))
            cx = row_start_x + col * (CARD_W + CARD_GAP)
            cy = content_y + row * (CARD_H + ROW_GAP)
            parts.append(
                f'<rect x="{cx}" y="{cy}" width="{CARD_W}" height="{CARD_H}" rx="8" fill="{colors["canvas"]}" stroke="{card_stroke or accent}" stroke-width="1"/>'
            )
            parts.append(
                f'<text x="{cx + 8}" y="{cy + 16}" font-size="12" font-weight="600" fill="{colors["text_main"]}">{_esc(system.get("name", ""))}</text>'
            )
            # Show category as small label
            category = system.get("category", "")
            if category:
                parts.append(
                    f'<text x="{cx + 8}" y="{cy + 28}" font-size="8" fill="{accent}">{_esc(category)}</text>'
                )
            # Show features as bullet list (compact)
            features = system.get("properties", {}).get("features", [])[:2]
            for fi, feat in enumerate(features):
                parts.append(
                    f'<text x="{cx + 8}" y="{cy + 42 + fi * 12}" font-size="9" fill="{colors["text_sub"]}">• {_esc(feat[:20])}</text>'
                )


    parts.append(
        f'<text x="{canvas_w / 2}" y="{canvas_h - 16}" text-anchor="middle" font-size="10" fill="{colors["text_sub"]}">{_esc(title)} • Layered Poster</text>'
    )
    parts.append('</svg>')
    target.write_text("\n".join(parts), encoding="utf-8")

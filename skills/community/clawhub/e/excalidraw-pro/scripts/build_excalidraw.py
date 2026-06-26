#!/usr/bin/env python3
"""
build_excalidraw.py - Convert structured diagram JSON to .excalidraw format.

Usage:
    python build_excalidraw.py --input diagram.json --output result.excalidraw
    python build_excalidraw.py --input diagram.json  # outputs to <title>.excalidraw
"""

import argparse
import json
import math
import random
import sys
import time
import uuid
from pathlib import Path


# ─── Excalidraw defaults ────────────────────────────────────────────────────

STROKE_COLOR = "#1e1e1e"
BG_TRANSPARENT = "transparent"
BG_LIGHT_BLUE = "#dbe4ff"
BG_LIGHT_GREEN = "#d3f9d8"
BG_LIGHT_YELLOW = "#fff9db"
BG_LIGHT_PINK = "#ffdeeb"
FILL_SOLID = "solid"
ROUGHNESS = 1
FONT_SIZE = 16
FONT_FAMILY = 1  # Virgil (handwritten)
LINE_HEIGHT = 1.25
NODE_W = 160
NODE_H = 60
DIAMOND_W = 160
DIAMOND_H = 80
OVAL_W = 140
OVAL_H = 60
H_GAP = 80   # horizontal gap between nodes
V_GAP = 80   # vertical gap between levels


def new_id() -> str:
    return str(uuid.uuid4())[:20]


def seed() -> int:
    return random.randint(100000, 999999)


def timestamp() -> int:
    return int(time.time() * 1000)


# ─── Base element builders ───────────────────────────────────────────────────

def make_rect(x, y, w, h, label, bg=BG_TRANSPARENT, roundness=3) -> dict:
    eid = new_id()
    elements = []
    rect = {
        "id": eid,
        "type": "rectangle",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0,
        "strokeColor": STROKE_COLOR,
        "backgroundColor": bg,
        "fillStyle": FILL_SOLID if bg != BG_TRANSPARENT else "hachure",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": ROUGHNESS,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": {"type": roundness},
        "seed": seed(),
        "version": 1,
        "versionNonce": seed(),
        "isDeleted": False,
        "boundElements": [],
        "updated": timestamp(),
        "link": None,
        "locked": False,
    }
    elements.append(rect)
    if label:
        elements.append(make_text_in(eid, x, y, w, h, label))
    return elements, eid


def make_ellipse(x, y, w, h, label, bg=BG_TRANSPARENT) -> dict:
    eid = new_id()
    elements = []
    el = {
        "id": eid,
        "type": "ellipse",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0,
        "strokeColor": STROKE_COLOR,
        "backgroundColor": bg,
        "fillStyle": FILL_SOLID if bg != BG_TRANSPARENT else "hachure",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": ROUGHNESS,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": {"type": 2},
        "seed": seed(),
        "version": 1,
        "versionNonce": seed(),
        "isDeleted": False,
        "boundElements": [],
        "updated": timestamp(),
        "link": None,
        "locked": False,
    }
    elements.append(el)
    if label:
        elements.append(make_text_in(eid, x, y, w, h, label))
    return elements, eid


def make_diamond(x, y, w, h, label, bg=BG_TRANSPARENT) -> dict:
    eid = new_id()
    elements = []
    el = {
        "id": eid,
        "type": "diamond",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0,
        "strokeColor": STROKE_COLOR,
        "backgroundColor": bg,
        "fillStyle": FILL_SOLID if bg != BG_TRANSPARENT else "hachure",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": ROUGHNESS,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": {"type": 2},
        "seed": seed(),
        "version": 1,
        "versionNonce": seed(),
        "isDeleted": False,
        "boundElements": [],
        "updated": timestamp(),
        "link": None,
        "locked": False,
    }
    elements.append(el)
    if label:
        elements.append(make_text_in(eid, x, y, w, h, label))
    return elements, eid


def make_text_in(container_id, x, y, w, h, text) -> dict:
    return {
        "id": new_id(),
        "type": "text",
        "x": x + 8,
        "y": y + h / 2 - FONT_SIZE * LINE_HEIGHT / 2,
        "width": w - 16,
        "height": FONT_SIZE * LINE_HEIGHT,
        "angle": 0,
        "strokeColor": STROKE_COLOR,
        "backgroundColor": BG_TRANSPARENT,
        "fillStyle": "hachure",
        "strokeWidth": 1,
        "strokeStyle": "solid",
        "roughness": ROUGHNESS,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": None,
        "seed": seed(),
        "version": 1,
        "versionNonce": seed(),
        "isDeleted": False,
        "boundElements": None,
        "updated": timestamp(),
        "link": None,
        "locked": False,
        "text": text,
        "fontSize": FONT_SIZE,
        "fontFamily": FONT_FAMILY,
        "textAlign": "center",
        "verticalAlign": "middle",
        "containerId": container_id,
        "originalText": text,
        "lineHeight": LINE_HEIGHT,
    }


def make_standalone_text(x, y, text, size=FONT_SIZE, bold=False) -> dict:
    return {
        "id": new_id(),
        "type": "text",
        "x": x, "y": y,
        "width": max(len(text) * size * 0.6, 100),
        "height": size * LINE_HEIGHT,
        "angle": 0,
        "strokeColor": STROKE_COLOR,
        "backgroundColor": BG_TRANSPARENT,
        "fillStyle": "hachure",
        "strokeWidth": 1,
        "strokeStyle": "solid",
        "roughness": ROUGHNESS,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": None,
        "seed": seed(),
        "version": 1,
        "versionNonce": seed(),
        "isDeleted": False,
        "boundElements": None,
        "updated": timestamp(),
        "link": None,
        "locked": False,
        "text": text,
        "fontSize": size,
        "fontFamily": FONT_FAMILY,
        "textAlign": "center",
        "verticalAlign": "top",
        "containerId": None,
        "originalText": text,
        "lineHeight": LINE_HEIGHT,
    }


def make_arrow(start_id, end_id, start_x, start_y, end_x, end_y, label=None) -> list:
    aid = new_id()
    elements = []
    arrow = {
        "id": aid,
        "type": "arrow",
        "x": start_x,
        "y": start_y,
        "width": abs(end_x - start_x),
        "height": abs(end_y - start_y),
        "angle": 0,
        "strokeColor": STROKE_COLOR,
        "backgroundColor": BG_TRANSPARENT,
        "fillStyle": "hachure",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": ROUGHNESS,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": {"type": 2},
        "seed": seed(),
        "version": 1,
        "versionNonce": seed(),
        "isDeleted": False,
        "boundElements": [],
        "updated": timestamp(),
        "link": None,
        "locked": False,
        "points": [[0, 0], [end_x - start_x, end_y - start_y]],
        "lastCommittedPoint": None,
        "startBinding": {"elementId": start_id, "focus": 0, "gap": 6},
        "endBinding": {"elementId": end_id, "focus": 0, "gap": 6},
        "startArrowhead": None,
        "endArrowhead": "arrow",
    }
    elements.append(arrow)
    if label:
        mid_x = (start_x + end_x) / 2 - 30
        mid_y = (start_y + end_y) / 2 - 12
        elements.append(make_standalone_text(mid_x, mid_y, label, size=13))
    return elements


def make_line(x1, y1, x2, y2, dashed=False) -> dict:
    return {
        "id": new_id(),
        "type": "line",
        "x": x1, "y": y1,
        "width": abs(x2 - x1),
        "height": abs(y2 - y1),
        "angle": 0,
        "strokeColor": "#868e96",
        "backgroundColor": BG_TRANSPARENT,
        "fillStyle": "hachure",
        "strokeWidth": 1,
        "strokeStyle": "dashed" if dashed else "solid",
        "roughness": 0,
        "opacity": 60,
        "groupIds": [],
        "frameId": None,
        "roundness": None,
        "seed": seed(),
        "version": 1,
        "versionNonce": seed(),
        "isDeleted": False,
        "boundElements": None,
        "updated": timestamp(),
        "link": None,
        "locked": False,
        "points": [[0, 0], [x2 - x1, y2 - y1]],
        "lastCommittedPoint": None,
        "startBinding": None,
        "endBinding": None,
        "startArrowhead": None,
        "endArrowhead": None,
    }


# ─── Diagram builders ────────────────────────────────────────────────────────

def build_flowchart(data: dict) -> list:
    """Top-down BFS layout for flowcharts."""
    nodes = {n["id"]: n for n in data.get("nodes", [])}
    edges = data.get("edges", [])

    # Build adjacency
    children = {nid: [] for nid in nodes}
    parents = {nid: [] for nid in nodes}
    for e in edges:
        children[e["from"]].append(e["to"])
        parents[e["to"]].append(e["from"])

    # BFS to assign levels
    roots = [nid for nid in nodes if not parents[nid]]
    if not roots:
        roots = [list(nodes.keys())[0]]

    levels = {}
    queue = [(r, 0) for r in roots]
    visited = set()
    while queue:
        nid, lv = queue.pop(0)
        if nid in visited:
            continue
        visited.add(nid)
        levels[nid] = max(levels.get(nid, 0), lv)
        for c in children[nid]:
            queue.append((c, lv + 1))

    # Group by level
    by_level = {}
    for nid, lv in levels.items():
        by_level.setdefault(lv, []).append(nid)

    # Assign coordinates
    coords = {}
    for lv, nids in sorted(by_level.items()):
        total_w = len(nids) * NODE_W + (len(nids) - 1) * H_GAP
        x_start = -total_w / 2
        for i, nid in enumerate(nids):
            x = x_start + i * (NODE_W + H_GAP)
            y = lv * (NODE_H + V_GAP)
            coords[nid] = (x, y)

    all_elements = []
    node_ids = {}

    # Draw nodes
    for nid, node in nodes.items():
        if nid not in coords:
            continue
        x, y = coords[nid]
        shape = node.get("shape", "rectangle")
        label = node.get("label", nid)

        if shape == "oval":
            elems, eid = make_ellipse(x, y, OVAL_W, OVAL_H, label, BG_LIGHT_GREEN)
        elif shape == "diamond":
            elems, eid = make_diamond(x, y, DIAMOND_W, DIAMOND_H, label, BG_LIGHT_YELLOW)
        else:
            elems, eid = make_rect(x, y, NODE_W, NODE_H, label, BG_LIGHT_BLUE)

        all_elements.extend(elems)
        node_ids[nid] = eid

    # Draw edges
    for e in edges:
        fid = e["from"]
        tid = e["to"]
        if fid not in coords or tid not in coords:
            continue
        fx, fy = coords[fid]
        tx, ty = coords[tid]
        sx = fx + NODE_W / 2
        sy = fy + NODE_H
        ex = tx + NODE_W / 2
        ey = ty
        label = e.get("label")
        all_elements.extend(make_arrow(node_ids[fid], node_ids[tid], sx, sy, ex, ey, label))

    return all_elements


def build_architecture(data: dict) -> list:
    """Grid layout with optional group boxes."""
    all_elements = []
    node_ids = {}
    coords = {}

    groups = data.get("groups", [])
    loose_nodes = data.get("nodes", [])
    edges = data.get("edges", [])

    COLS = 3
    GRP_PAD = 20
    GRP_GAP = 40
    x_offset = 0

    all_node_lists = []
    if groups:
        for grp in groups:
            all_node_lists.append(("group", grp))
    if loose_nodes:
        all_node_lists.append(("loose", {"nodes": loose_nodes}))

    for kind, item in all_node_lists:
        nodes = item.get("nodes", [])
        cols = min(COLS, len(nodes))
        rows = math.ceil(len(nodes) / cols) if cols else 1
        inner_w = cols * NODE_W + (cols - 1) * H_GAP
        inner_h = rows * NODE_H + (rows - 1) * V_GAP

        if kind == "group":
            grp_x = x_offset
            grp_y = 60  # leave room for label
            grp_w = inner_w + 2 * GRP_PAD
            grp_h = inner_h + 2 * GRP_PAD + 30
            grp_elems, _ = make_rect(grp_x, 40, grp_w, grp_h + 20, None, bg=BG_TRANSPARENT)
            # group label
            grp_elems[0]["strokeStyle"] = "dashed"
            grp_elems[0]["roughness"] = 0
            all_elements.extend(grp_elems)
            all_elements.append(make_standalone_text(grp_x + 10, 44, item.get("label", ""), size=14))
            node_x0 = grp_x + GRP_PAD
            node_y0 = 80
        else:
            node_x0 = x_offset
            node_y0 = 40

        for i, node in enumerate(nodes):
            row = i // cols
            col = i % cols
            nx = node_x0 + col * (NODE_W + H_GAP)
            ny = node_y0 + row * (NODE_H + V_GAP)
            coords[node["id"]] = (nx, ny)
            elems, eid = make_rect(nx, ny, NODE_W, NODE_H, node.get("label", node["id"]), BG_LIGHT_BLUE)
            all_elements.extend(elems)
            node_ids[node["id"]] = eid

        if kind == "group":
            grp_w = inner_w + 2 * GRP_PAD
            x_offset += grp_w + GRP_GAP
        else:
            x_offset += inner_w + GRP_GAP

    # Draw edges
    for e in edges:
        fid, tid = e["from"], e["to"]
        if fid not in coords or tid not in coords:
            continue
        fx, fy = coords[fid]
        tx, ty = coords[tid]
        sx = fx + NODE_W
        sy = fy + NODE_H / 2
        ex = tx
        ey = ty + NODE_H / 2
        all_elements.extend(make_arrow(node_ids[fid], node_ids[tid], sx, sy, ex, ey, e.get("label")))

    return all_elements


def build_mindmap(data: dict) -> list:
    """Radial layout from center root."""
    all_elements = []
    node_ids = {}
    coords = {}

    root_label = data.get("root", "Root")
    branches = data.get("branches", [])

    cx, cy = 0, 0
    root_elems, root_eid = make_ellipse(cx - 80, cy - 30, 160, 60, root_label, BG_LIGHT_PINK)
    all_elements.extend(root_elems)
    root_center = (cx, cy)

    branch_count = len(branches)
    for bi, branch in enumerate(branches):
        angle = (2 * math.pi / branch_count) * bi - math.pi / 2
        br = 260  # branch radius
        bx = cx + br * math.cos(angle)
        by = cy + br * math.sin(angle)
        coords[f"branch_{bi}"] = (bx, by)
        b_elems, b_eid = make_rect(bx - NODE_W / 2, by - NODE_H / 2, NODE_W, NODE_H,
                                    branch.get("label", ""), BG_LIGHT_BLUE)
        all_elements.extend(b_elems)
        node_ids[f"branch_{bi}"] = b_eid

        # Arrow: root → branch
        all_elements.extend(make_arrow(root_eid, b_eid, cx, cy, bx - NODE_W / 2, by))

        children = branch.get("children", [])
        child_count = len(children)
        for ci, child_label in enumerate(children):
            spread = 60
            offset = (ci - (child_count - 1) / 2) * spread
            cr = br + 200
            child_angle = angle + math.radians(offset * 0.3)
            cx2 = cx + cr * math.cos(child_angle)
            cy2 = cy + cr * math.sin(child_angle)
            c_elems, c_eid = make_rect(cx2 - NODE_W / 2, cy2 - NODE_H / 2, NODE_W, NODE_H,
                                        child_label, BG_TRANSPARENT)
            all_elements.extend(c_elems)
            all_elements.extend(make_arrow(b_eid, c_eid, bx, by, cx2, cy2))

    return all_elements


def build_sequence(data: dict) -> list:
    """Vertical timeline with actor columns."""
    all_elements = []
    actors = data.get("actors", [])
    messages = data.get("messages", [])

    COL_W = 200
    ROW_H = 70
    ACTOR_H = 50
    TIMELINE_START_Y = 80
    TOTAL_H = TIMELINE_START_Y + (len(messages) + 1) * ROW_H

    actor_x = {}
    for i, actor in enumerate(actors):
        x = i * COL_W
        actor_x[actor] = x + COL_W / 2 - NODE_W / 2
        # Actor box
        elems, _ = make_rect(x + COL_W / 2 - NODE_W / 2, 0, NODE_W, ACTOR_H, actor, BG_LIGHT_BLUE)
        all_elements.extend(elems)
        # Lifeline
        all_elements.append(make_line(
            x + COL_W / 2, ACTOR_H,
            x + COL_W / 2, TOTAL_H,
            dashed=True
        ))

    for mi, msg in enumerate(messages):
        frm = msg.get("from", "")
        to = msg.get("to", "")
        label = msg.get("label", "")
        y = TIMELINE_START_Y + mi * ROW_H

        if frm not in actor_x or to not in actor_x:
            continue

        fx = actor_x[frm] + NODE_W / 2 + (NODE_W / 2)
        tx = actor_x[to] + NODE_W / 2 + (NODE_W / 2)

        # Find actor column center
        frm_idx = actors.index(frm)
        to_idx = actors.index(to)
        sx = frm_idx * COL_W + COL_W / 2
        ex = to_idx * COL_W + COL_W / 2

        aid = new_id()
        arrow = {
            "id": aid,
            "type": "arrow",
            "x": sx, "y": y,
            "width": abs(ex - sx), "height": 0,
            "angle": 0,
            "strokeColor": STROKE_COLOR,
            "backgroundColor": BG_TRANSPARENT,
            "fillStyle": "hachure",
            "strokeWidth": 2,
            "strokeStyle": "solid",
            "roughness": 0,
            "opacity": 100,
            "groupIds": [],
            "frameId": None,
            "roundness": None,
            "seed": seed(),
            "version": 1,
            "versionNonce": seed(),
            "isDeleted": False,
            "boundElements": [],
            "updated": timestamp(),
            "link": None,
            "locked": False,
            "points": [[0, 0], [ex - sx, 0]],
            "lastCommittedPoint": None,
            "startBinding": None,
            "endBinding": None,
            "startArrowhead": None,
            "endArrowhead": "arrow",
        }
        all_elements.append(arrow)
        all_elements.append(make_standalone_text((sx + ex) / 2 - 40, y - 20, label, size=13))

    return all_elements


# ─── Main ────────────────────────────────────────────────────────────────────

BUILDERS = {
    "flowchart": build_flowchart,
    "architecture": build_architecture,
    "mindmap": build_mindmap,
    "sequence": build_sequence,
}


def build(input_path: str, output_path: str | None = None):
    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)

    diagram_type = data.get("type", "flowchart").lower()
    title = data.get("title", "diagram")

    builder = BUILDERS.get(diagram_type)
    if not builder:
        print(f"ERROR: Unknown diagram type '{diagram_type}'. Supported: {list(BUILDERS.keys())}", file=sys.stderr)
        sys.exit(1)

    elements = builder(data)

    excalidraw = {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {
            "gridSize": None,
            "viewBackgroundColor": "#ffffff",
        },
        "files": {},
    }

    if not output_path:
        safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title)
        output_path = f"{safe_title}.excalidraw"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(excalidraw, f, ensure_ascii=False, indent=2)

    print(f"✓ Generated: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Convert diagram JSON to .excalidraw file")
    parser.add_argument("--input", "-i", required=True, help="Input JSON file")
    parser.add_argument("--output", "-o", help="Output .excalidraw file path")
    args = parser.parse_args()
    build(args.input, args.output)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build an Excalidraw diagram from a small JSON spec (stdlib only, no network).

The spec describes nodes, edges and optional groups. This script does the
parts a language model gets wrong when it writes Excalidraw JSON by hand:
layout, label sizing, text-in-shape and arrow bindings, unique IDs and the
Obsidian file wrapper. The output is deterministic: the same spec always
produces the same file.

Usage:
    build_diagram.py --spec spec.json --out "Diagrams/flow.excalidraw.md"
    build_diagram.py --spec - --out flow.excalidraw --format excalidraw < spec.json

Prints one JSON object with ok, path, format, counts and warnings. It never
overwrites an existing file unless --force is given.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PALETTE: Dict[str, Tuple[str, str]] = {
    # name: (stroke, fill)
    "blue": ("#1971c2", "#a5d8ff"),
    "green": ("#2f9e44", "#b2f2bb"),
    "red": ("#e03131", "#ffc9c9"),
    "orange": ("#e8590c", "#ffd8a8"),
    "purple": ("#9c36b5", "#d0bfff"),
    "yellow": ("#e67700", "#fff3bf"),
    "cyan": ("#0c8599", "#c3fae8"),
    "pink": ("#c2255c", "#eebefa"),
    "gray": ("#495057", "#e9ecef"),
    "white": ("#1e1e1e", "transparent"),
}
TEXT_COLOR = "#1e1e1e"
SHAPES = {"rectangle", "ellipse", "diamond"}
FONTS = {"excalifont": 5, "virgil": 1, "helvetica": 2, "cascadia": 3, "nunito": 6, "lilita": 7, "comic": 8}

NODE_FONT = 20
EDGE_FONT = 16
GROUP_FONT = 18
TITLE_FONT = 28
LINE_HEIGHT = 1.25
PAD_X = 24
PAD_Y = 18
MIN_W = 140
MIN_H = 70
LAYER_GAP = 110
SLOT_GAP = 60
BAND_GAP = 90
GROUP_PAD = 30
ARROW_GAP = 4
OBSIDIAN_SOURCE = "https://github.com/zsviczian/obsidian-excalidraw-plugin"
STANDARD_SOURCE = "https://excalidraw.com"
ID_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


class SpecError(ValueError):
    pass


# --------------------------------------------------------------------------- ids


def _digest(*parts: str) -> bytes:
    return hashlib.sha256("\x1f".join(parts).encode("utf-8")).digest()


def make_id(*parts: str) -> str:
    raw = int.from_bytes(_digest("id", *parts)[:16], "big")
    out = []
    for _ in range(20):
        raw, rem = divmod(raw, len(ID_ALPHABET))
        out.append(ID_ALPHABET[rem])
    return "".join(out)


def make_seed(*parts: str) -> int:
    return int.from_bytes(_digest("seed", *parts)[:4], "big") % 2_000_000_000 + 1


# --------------------------------------------------------------------------- text


def _char_width(ch: str) -> float:
    if unicodedata.east_asian_width(ch) in ("W", "F"):
        return 1.0
    if ch in "il.,:;'|!":
        return 0.35
    if ch.isupper() or ch in "mwMW@%":
        return 0.72
    return 0.6


def text_size(text: str, font_size: int) -> Tuple[float, float]:
    lines = text.split("\n") or [""]
    width = max(sum(_char_width(c) for c in line) for line in lines) * font_size
    height = len(lines) * font_size * LINE_HEIGHT
    return round(width, 2), round(height, 2)


# --------------------------------------------------------------------------- spec


def load_spec(raw: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(raw, dict):
        raise SpecError("spec must be a JSON object")
    direction = str(raw.get("direction", "TB")).upper()
    if direction not in {"TB", "LR"}:
        raise SpecError("direction must be TB or LR")

    groups: List[Dict[str, str]] = []
    group_ids = set()
    for g in raw.get("groups", []) or []:
        gid = str(g.get("id", "")).strip() if isinstance(g, dict) else ""
        if not gid or gid in group_ids:
            raise SpecError(f"group id missing or duplicated: {g!r}")
        group_ids.add(gid)
        groups.append({"id": gid, "label": str(g.get("label", gid)), "color": str(g.get("color", "gray"))})

    nodes: List[Dict[str, Any]] = []
    seen = set()
    for n in raw.get("nodes", []) or []:
        if not isinstance(n, dict):
            raise SpecError(f"node must be an object: {n!r}")
        nid = str(n.get("id", "")).strip()
        if not nid or nid in seen:
            raise SpecError(f"node id missing or duplicated: {nid!r}")
        seen.add(nid)
        shape = str(n.get("shape", "rectangle"))
        if shape not in SHAPES:
            raise SpecError(f"node {nid}: shape must be one of {sorted(SHAPES)}")
        color = str(n.get("color", "blue"))
        if color not in PALETTE:
            raise SpecError(f"node {nid}: color must be one of {sorted(PALETTE)}")
        group = n.get("group")
        if group is not None and str(group) not in group_ids:
            raise SpecError(f"node {nid}: unknown group {group!r}")
        rank = n.get("rank")
        if rank is not None and (not isinstance(rank, int) or rank < 0):
            raise SpecError(f"node {nid}: rank must be a non-negative integer")
        nodes.append({
            "id": nid,
            "label": str(n.get("label", nid)),
            "shape": shape,
            "color": color,
            "group": str(group) if group is not None else None,
            "rank": rank,
            "link": n.get("link"),
        })
    if not nodes:
        raise SpecError("spec has no nodes")

    edges: List[Dict[str, Any]] = []
    for e in raw.get("edges", []) or []:
        if not isinstance(e, dict):
            raise SpecError(f"edge must be an object: {e!r}")
        src, dst = str(e.get("from", "")), str(e.get("to", ""))
        if src not in seen or dst not in seen:
            raise SpecError(f"edge {src!r} -> {dst!r} references an unknown node")
        if src == dst:
            raise SpecError(f"self-loop on {src!r} is not supported")
        style = str(e.get("style", "solid"))
        if style not in {"solid", "dashed", "dotted"}:
            raise SpecError(f"edge {src}->{dst}: style must be solid, dashed or dotted")
        edges.append({
            "from": src,
            "to": dst,
            "label": str(e["label"]) if e.get("label") else "",
            "style": style,
            "both": bool(e.get("bidirectional", False)),
        })

    theme = str(raw.get("theme", "sketch"))
    if theme not in {"sketch", "clean"}:
        raise SpecError("theme must be sketch or clean")
    font_name = str(raw.get("font", "excalifont")).lower()
    if font_name not in FONTS:
        raise SpecError(f"font must be one of {sorted(FONTS)}")
    return {
        "title": str(raw.get("title", "")).strip(),
        "direction": direction,
        "theme": theme,
        "font": FONTS[font_name],
        "groups": groups,
        "nodes": nodes,
        "edges": edges,
    }


# --------------------------------------------------------------------------- layout


def assign_layers(nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> Dict[str, int]:
    order = [n["id"] for n in nodes]
    succ: Dict[str, List[str]] = {nid: [] for nid in order}
    for e in edges:
        succ[e["from"]].append(e["to"])

    # Drop back edges found by DFS in declaration order, so cycles still lay out.
    state: Dict[str, int] = {}
    back = set()
    for root in order:
        if root in state:
            continue
        stack = [(root, iter(succ[root]))]
        state[root] = 1
        while stack:
            node, it = stack[-1]
            nxt = next(it, None)
            if nxt is None:
                state[node] = 2
                stack.pop()
            elif state.get(nxt) == 1:
                back.add((node, nxt))
            elif nxt not in state:
                state[nxt] = 1
                stack.append((nxt, iter(succ[nxt])))

    pinned = {n["id"]: n["rank"] for n in nodes if n["rank"] is not None}
    layer = {nid: pinned.get(nid, 0) for nid in order}
    dag = [(e["from"], e["to"]) for e in edges if (e["from"], e["to"]) not in back]
    for _ in range(len(order)):
        changed = False
        for a, b in dag:
            if b in pinned:
                continue
            if layer[b] < layer[a] + 1:
                layer[b] = layer[a] + 1
                changed = True
        if not changed:
            break
    return layer


def order_layers(
    nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]], layer: Dict[str, int]
) -> Dict[str, float]:
    """Barycenter ordering, a few sweeps. Returns a sort key per node."""
    pos = {n["id"]: float(i) for i, n in enumerate(nodes)}
    neighbours: Dict[str, List[str]] = {n["id"]: [] for n in nodes}
    for e in edges:
        neighbours[e["from"]].append(e["to"])
        neighbours[e["to"]].append(e["from"])
    max_layer = max(layer.values())
    for sweep in range(4):
        layers = range(1, max_layer + 1) if sweep % 2 == 0 else range(max_layer - 1, -1, -1)
        ref = -1 if sweep % 2 == 0 else 1
        for lv in layers:
            members = [nid for nid in pos if layer[nid] == lv]
            keys = {}
            for nid in members:
                adj = [pos[m] for m in neighbours[nid] if layer[m] == lv + ref]
                keys[nid] = sum(adj) / len(adj) if adj else pos[nid]
            for rank_, nid in enumerate(sorted(members, key=lambda x: (keys[x], pos[x]))):
                pos[nid] = rank_ + keys[nid] * 1e-3
    return pos


def node_box(node: Dict[str, Any]) -> Tuple[float, float]:
    tw, th = text_size(node["label"], NODE_FONT)
    w = max(MIN_W, tw + 2 * PAD_X)
    h = max(MIN_H, th + 2 * PAD_Y)
    if node["shape"] == "diamond":
        w, h = w * 1.5, h * 1.6
    elif node["shape"] == "ellipse":
        w, h = w * 1.25, h * 1.3
    return round(w / 10) * 10, round(h / 10) * 10


def layout(spec: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
    nodes, edges = spec["nodes"], spec["edges"]
    layer = assign_layers(nodes, edges)
    sort_key = order_layers(nodes, edges, layer)
    tb = spec["direction"] == "TB"
    size = {n["id"]: node_box(n) for n in nodes}
    main = {nid: (h if tb else w) for nid, (w, h) in size.items()}
    cross = {nid: (w if tb else h) for nid, (w, h) in size.items()}

    # Bands: one per group plus one for ungrouped nodes, in order of first use.
    band_order: List[Optional[str]] = []
    for n in nodes:
        if n["group"] not in band_order:
            band_order.append(n["group"])
    max_layer = max(layer.values())

    layer_extent = [0.0] * (max_layer + 1)
    for nid, lv in layer.items():
        layer_extent[lv] = max(layer_extent[lv], main[nid])
    label_room = GROUP_FONT * LINE_HEIGHT + 10 if spec["groups"] else 0
    layer_gap = LAYER_GAP + (EDGE_FONT * 2 if any(e["label"] for e in edges) else 0) + label_room
    layer_start = []
    cursor = 0.0
    for lv in range(max_layer + 1):
        layer_start.append(cursor)
        cursor += layer_extent[lv] + layer_gap

    boxes: Dict[str, Dict[str, float]] = {}
    cross_cursor = 0.0
    for band in band_order:
        members = [n["id"] for n in nodes if n["group"] == band]
        slot = max(cross[m] for m in members) + SLOT_GAP
        per_layer: Dict[int, List[str]] = {}
        for m in members:
            per_layer.setdefault(layer[m], []).append(m)
        slots = max(len(v) for v in per_layer.values())
        band_width = slots * slot
        for lv, ids in per_layer.items():
            ids.sort(key=lambda x: sort_key[x])
            offset = (slots - len(ids)) * slot / 2
            for i, nid in enumerate(ids):
                c_center = cross_cursor + offset + i * slot + slot / 2
                m_center = layer_start[lv] + layer_extent[lv] / 2
                w, h = size[nid]
                cx, cy = (c_center, m_center) if tb else (m_center, c_center)
                boxes[nid] = {"x": round(cx - w / 2), "y": round(cy - h / 2), "w": w, "h": h}
        cross_cursor += band_width + BAND_GAP
    return boxes


# --------------------------------------------------------------------------- geometry


def border_point(box: Dict[str, float], shape: str, toward: Tuple[float, float]) -> Tuple[float, float]:
    cx, cy = box["x"] + box["w"] / 2, box["y"] + box["h"] / 2
    dx, dy = toward[0] - cx, toward[1] - cy
    if dx == 0 and dy == 0:
        return cx, cy
    hw, hh = box["w"] / 2, box["h"] / 2
    if shape == "ellipse":
        t = 1 / ((dx / hw) ** 2 + (dy / hh) ** 2) ** 0.5
    elif shape == "diamond":
        t = 1 / (abs(dx) / hw + abs(dy) / hh)
    else:
        t = min(hw / abs(dx) if dx else float("inf"), hh / abs(dy) if dy else float("inf"))
    length = (dx * dx + dy * dy) ** 0.5
    t_gap = t + ARROW_GAP / length
    return cx + dx * t_gap, cy + dy * t_gap


def segment_hits_box(p: Tuple[float, float], q: Tuple[float, float], box: Dict[str, float]) -> bool:
    """Liang-Barsky clip of segment pq against a slightly shrunk box."""
    x0, y0, x1, y1 = box["x"] + 2, box["y"] + 2, box["x"] + box["w"] - 2, box["y"] + box["h"] - 2
    t0, t1 = 0.0, 1.0
    dx, dy = q[0] - p[0], q[1] - p[1]
    for pk, qk in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
        if pk == 0:
            if qk < 0:
                return False
            continue
        r = qk / pk
        if pk < 0:
            t0 = max(t0, r)
        else:
            t1 = min(t1, r)
        if t0 > t1:
            return False
    return True


# --------------------------------------------------------------------------- elements


def _base(eid: str, etype: str, x: float, y: float, w: float, h: float, theme: str) -> Dict[str, Any]:
    return {
        "id": eid,
        "type": etype,
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "angle": 0,
        "strokeColor": TEXT_COLOR,
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 1 if theme == "sketch" else 0,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": None,
        "seed": make_seed(eid),
        "version": 1,
        "versionNonce": make_seed("nonce", eid),
        "isDeleted": False,
        "boundElements": None,
        "updated": 1,
        "link": None,
        "locked": False,
    }


def _text(eid: str, text: str, x: float, y: float, size: int, font: int, theme: str,
          container: Optional[str] = None, align: str = "center", color: str = TEXT_COLOR) -> Dict[str, Any]:
    w, h = text_size(text, size)
    el = _base(eid, "text", round(x - (w / 2 if align == "center" else 0), 2), round(y - h / 2, 2), w, h, theme)
    el.update({
        "strokeColor": color,
        "text": text,
        "originalText": text,
        "fontSize": size,
        "fontFamily": font,
        "textAlign": align,
        "verticalAlign": "middle" if container else "top",
        "containerId": container,
        "autoResize": True,
        "lineHeight": LINE_HEIGHT,
    })
    return el


def build_elements(spec: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[str]]:
    theme, font = spec["theme"], spec["font"]
    boxes = layout(spec)
    by_id = {n["id"]: n for n in spec["nodes"]}
    warnings: List[str] = []
    elements: List[Dict[str, Any]] = []
    shape_ids = {nid: make_id("node", nid) for nid in by_id}

    # Group frames go first so they render behind everything else.
    top_offset = 0.0
    if spec["title"]:
        top_offset = TITLE_FONT * LINE_HEIGHT + 40
    for g in spec["groups"]:
        members = [boxes[n["id"]] for n in spec["nodes"] if n["group"] == g["id"]]
        if not members:
            warnings.append(f"group {g['id']} has no nodes; skipped")
            continue
        x0 = min(b["x"] for b in members) - GROUP_PAD
        y0 = min(b["y"] for b in members) - GROUP_PAD - GROUP_FONT * LINE_HEIGHT - 6
        x1 = max(b["x"] + b["w"] for b in members) + GROUP_PAD
        y1 = max(b["y"] + b["h"] for b in members) + GROUP_PAD
        stroke, fill = PALETTE.get(g["color"], PALETTE["gray"])
        gid = make_id("group", g["id"])
        frame = _base(gid, "rectangle", x0, y0 + top_offset, x1 - x0, y1 - y0, theme)
        frame.update({"strokeColor": stroke, "backgroundColor": fill, "strokeStyle": "dashed",
                      "opacity": 35, "roundness": {"type": 3}})
        elements.append(frame)
        elements.append(_text(make_id("group-label", g["id"]), g["label"], x0 + 14,
                              y0 + top_offset + 10 + GROUP_FONT * LINE_HEIGHT / 2, GROUP_FONT, font, theme,
                              align="left", color=stroke))

    for b in boxes.values():
        b["y"] += top_offset

    if spec["title"]:
        x0 = min(b["x"] for b in boxes.values())
        x1 = max(b["x"] + b["w"] for b in boxes.values())
        y0 = min(b["y"] for b in boxes.values()) - top_offset
        if spec["groups"]:
            y0 -= GROUP_PAD + GROUP_FONT * LINE_HEIGHT + 6
        elements.append(_text(make_id("title"), spec["title"], (x0 + x1) / 2,
                              y0 + TITLE_FONT * LINE_HEIGHT / 2, TITLE_FONT, font, theme))

    shapes: Dict[str, Dict[str, Any]] = {}
    for n in spec["nodes"]:
        b = boxes[n["id"]]
        stroke, fill = PALETTE[n["color"]]
        sid, tid = shape_ids[n["id"]], make_id("label", n["id"])
        shape = _base(sid, n["shape"], b["x"], b["y"], b["w"], b["h"], theme)
        shape.update({"strokeColor": stroke, "backgroundColor": fill,
                      "roundness": {"type": 3} if n["shape"] == "rectangle" else {"type": 2},
                      "boundElements": [{"id": tid, "type": "text"}]})
        if n["link"]:
            shape["link"] = str(n["link"])
        shapes[n["id"]] = shape
        elements.append(shape)
        elements.append(_text(tid, n["label"], b["x"] + b["w"] / 2, b["y"] + b["h"] / 2,
                              NODE_FONT, font, theme, container=sid))

    tb = spec["direction"] == "TB"
    lane = 0
    for i, e in enumerate(spec["edges"]):
        a, b = boxes[e["from"]], boxes[e["to"]]
        others = [box for nid, box in boxes.items() if nid not in (e["from"], e["to"])]
        ca = (a["x"] + a["w"] / 2, a["y"] + a["h"] / 2)
        cb = (b["x"] + b["w"] / 2, b["y"] + b["h"] / 2)
        p = border_point(a, by_id[e["from"]]["shape"], cb)
        q = border_point(b, by_id[e["to"]]["shape"], ca)
        route = [p, q]
        if any(segment_hits_box(p, q, box) for box in others):
            # Detour around the whole drawing on the far side of the cross axis
            # (right for TB, top for LR), one lane per detoured edge.
            lane += 1
            if tb:
                side = max(bx["x"] + bx["w"] for bx in boxes.values()) + 40 * lane
                p = (a["x"] + a["w"] + ARROW_GAP, ca[1])
                q = (b["x"] + b["w"] + ARROW_GAP, cb[1])
                route = [p, (side, p[1]), (side, q[1]), q]
            else:
                side = min(bx["y"] for bx in boxes.values()) - 40 * lane
                p = (ca[0], a["y"] - ARROW_GAP)
                q = (cb[0], b["y"] - ARROW_GAP)
                route = [p, (p[0], side), (q[0], side), q]
        pts = [[round(x - p[0], 2), round(y - p[1], 2)] for x, y in route]
        xs = [pt[0] for pt in pts]
        ys = [pt[1] for pt in pts]
        aid = make_id("edge", str(i), e["from"], e["to"])
        arrow = _base(aid, "arrow", round(p[0], 2), round(p[1], 2),
                      round(max(xs) - min(xs), 2), round(max(ys) - min(ys), 2), theme)
        arrow.update({
            "strokeColor": "#495057",
            "strokeStyle": e["style"],
            "roundness": {"type": 2} if len(route) == 2 else None,
            "points": pts,
            "lastCommittedPoint": None,
            "startBinding": {"elementId": shape_ids[e["from"]], "focus": 0, "gap": ARROW_GAP, "fixedPoint": None},
            "endBinding": {"elementId": shape_ids[e["to"]], "focus": 0, "gap": ARROW_GAP, "fixedPoint": None},
            "startArrowhead": "arrow" if e["both"] else None,
            "endArrowhead": "arrow",
            "elbowed": False,
        })
        for end in (e["from"], e["to"]):
            shapes[end]["boundElements"].append({"id": aid, "type": "arrow"})
        elements.append(arrow)
        if e["label"]:
            lid = make_id("edge-label", str(i), e["from"], e["to"])
            arrow["boundElements"] = [{"id": lid, "type": "text"}]
            mid_a, mid_b = route[len(route) // 2 - 1], route[len(route) // 2]
            elements.append(_text(lid, e["label"], (mid_a[0] + mid_b[0]) / 2, (mid_a[1] + mid_b[1]) / 2,
                                  EDGE_FONT, font, theme, container=aid))
        for seg_a, seg_b in zip(route, route[1:]):
            hit = next((nid for nid, box in boxes.items()
                        if nid not in (e["from"], e["to"]) and segment_hits_box(seg_a, seg_b, box)), None)
            if hit:
                warnings.append(
                    f"edge {e['from']} -> {e['to']} crosses node {hit}; "
                    "consider a rank, a different direction or reordering nodes"
                )
                break
    return elements, warnings


# --------------------------------------------------------------------------- output


def scene(elements: List[Dict[str, Any]], source: str) -> Dict[str, Any]:
    return {
        "type": "excalidraw",
        "version": 2,
        "source": source,
        "elements": elements,
        "appState": {"gridSize": 20, "viewBackgroundColor": "#ffffff"},
        "files": {},
    }


def obsidian_markdown(elements: List[Dict[str, Any]], tags: List[str]) -> str:
    data = json.dumps(scene(elements, OBSIDIAN_SOURCE), ensure_ascii=False, indent="\t")
    text_lines = []
    for el in elements:
        if el["type"] == "text":
            text_lines.append(f"{el['text']} ^{el['id']}\n")
    tag_list = ", ".join(tags)
    return (
        "---\n\n"
        "excalidraw-plugin: parsed\n"
        f"tags: [{tag_list}]\n\n"
        "---\n"
        "==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠== "
        "You can decompress Drawing data with the command palette: 'Decompress current Excalidraw file'. "
        "For more info check in plugin settings under 'Saving'\n\n\n"
        "# Excalidraw Data\n\n"
        "## Text Elements\n"
        + "\n".join(text_lines)
        + "\n%%\n"
        "## Drawing\n"
        "```json\n"
        f"{data}\n"
        "```\n"
        "%%\n"
    )


def detect_format(path: Path, requested: str) -> str:
    if requested != "auto":
        return requested
    if path.name.endswith(".excalidraw"):
        return "excalidraw"
    if path.suffix == ".md":
        return "obsidian"
    raise SpecError("cannot infer format: use a .md or .excalidraw file name, or pass --format")


def build(raw_spec: Dict[str, Any], fmt: str, tags: Optional[List[str]] = None) -> Tuple[str, Dict[str, Any]]:
    spec = load_spec(raw_spec)
    elements, warnings = build_elements(spec)
    if fmt == "obsidian":
        content = obsidian_markdown(elements, tags or ["excalidraw"])
    else:
        content = json.dumps(scene(elements, STANDARD_SOURCE), ensure_ascii=False, indent=2) + "\n"
    xs: List[float] = []
    ys: List[float] = []
    for el in elements:
        if "points" in el:
            xs += [el["x"] + pt[0] for pt in el["points"]]
            ys += [el["y"] + pt[1] for pt in el["points"]]
        else:
            xs += [el["x"], el["x"] + el["width"]]
            ys += [el["y"], el["y"] + el["height"]]
    info = {
        "nodes": len(spec["nodes"]),
        "edges": len(spec["edges"]),
        "groups": len(spec["groups"]),
        "elements": len(elements),
        "canvas": {"width": round(max(xs) - min(xs)), "height": round(max(ys) - min(ys))},
        "warnings": warnings,
    }
    return content, info


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--spec", required=True, help="spec JSON file, or - for stdin")
    parser.add_argument("--out", required=True, help="output file (.excalidraw.md / .md or .excalidraw)")
    parser.add_argument("--format", choices=["auto", "obsidian", "excalidraw"], default="auto")
    parser.add_argument("--tag", action="append", default=None, help="extra frontmatter tag (Obsidian only)")
    parser.add_argument("--force", action="store_true", help="overwrite an existing file")
    parser.add_argument("--stdout", action="store_true", help="print the file instead of writing it")
    args = parser.parse_args(argv)

    def fail(msg: str) -> int:
        print(json.dumps({"ok": False, "error": msg}, ensure_ascii=False))
        return 1

    try:
        text = sys.stdin.read() if args.spec == "-" else Path(args.spec).read_text(encoding="utf-8")
        raw = json.loads(text)
        out = Path(args.out).expanduser()
        fmt = detect_format(out, args.format)
        tags = ["excalidraw"] + [t for t in (args.tag or []) if t and t != "excalidraw"]
        content, info = build(raw, fmt, tags)
    except (OSError, ValueError) as exc:
        return fail(str(exc))

    if args.stdout:
        sys.stdout.write(content)
        return 0
    if out.exists() and not args.force:
        return fail(f"{out} already exists; ask the user, then rerun with --force to overwrite")
    if not out.parent.is_dir():
        return fail(f"folder does not exist: {out.parent}")
    try:
        out.write_text(content, encoding="utf-8")
    except OSError as exc:
        return fail(str(exc))
    print(json.dumps({"ok": True, "path": str(out), "format": fmt, **info}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())

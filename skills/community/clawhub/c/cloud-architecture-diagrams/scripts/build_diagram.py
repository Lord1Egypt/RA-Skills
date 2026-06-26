#!/usr/bin/env python3
"""
Build a Microsoft-style architecture diagram from a spec, emitting BOTH an
editable .excalidraw (JSON) and an editable .drawio (mxGraph XML), with real
msicons.com icons embedded as base64 (no external dependencies once written).

Design: the spec is turned into a flat list of drawing PRIMITIVES (rect, image,
text, arrow, badge) ONCE, then each backend serializes the same primitives.
That guarantees the two files look the same and keeps the format-specific code
small.

----------------------------------------------------------------------------
SPEC FORMAT (JSON)
----------------------------------------------------------------------------
{
  "title": "MARS Support Architecture",          # optional, drawn top-left
  "canvas": {"width": 1600, "height": 880},       # optional, auto if omitted
  "zones": [                                      # dashed grouping containers
    {"id":"azure","label":"Azure","x":420,"y":60,"width":860,"height":760}
  ],
  "nodes": [
    # A "card": white rounded box with an icon + bold title (+ optional desc).
    {"id":"entra","title":"Entra ID","desc":"User Auth & Authorization",
     "icon":"Entra ID","x":140,"y":150,"width":230,"height":92},
    # An icon-only node (no card): set "card": false. Good for Users, logos.
    {"id":"user","title":"Users","icon":"User","x":40,"y":360,
     "width":70,"height":70,"card":false}
    # If an icon can't be matched well it degrades to a labeled box.
    # Provide "icon_url" to bypass matching and use an exact icon.
  ],
  "edges": [
    {"from":"user","to":"mars","label":"Token Exchange","dir":"both"},
    {"from":"classifier","to":"mcp","label":"Retrieve & classify",
     "dir":"both","color":"#1565c0"}
    # dir: "to" (default) | "both" | "from"
    # optional "waypoints":[[x,y],...] to force routing; else auto L-route.
  ],
  "badges": [ {"n":1,"x":150,"y":120} ]           # optional numbered step circles
}
----------------------------------------------------------------------------
USAGE
    python build_diagram.py spec.json --out-prefix mydiagram
        -> mydiagram.excalidraw  and  mydiagram.drawio
    python build_diagram.py spec.json --out-prefix d --cache ./_icons
"""
import argparse
import base64
import html
import json
import re
import sys
import time
import urllib.request
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from find_icon import search as icon_search, score as icon_score

SKILL_ROOT = Path(__file__).resolve().parent.parent
MIN_SHAPE_SCORE = 0.9
# draw.io native-shape providers (vector stencils that ship with diagrams.net).
_SHAPE_PROVIDERS = {"aws", "gcp", "azure"}


def _load_shapes():
    p = Path(__file__).resolve().parent.parent / "references" / "drawio-shape-index.json"
    return json.loads(p.read_text("utf-8")) if p.exists() else []


def resolve_drawio_shape(node: dict, providers):
    """Best native draw.io stencil for this node, or None. Scoped to the
    node's / spec's provider (only aws|gcp|azure have native stencils).
    A node can pin an exact key via "drawio_shape":"mxgraph.aws4.lambda"."""
    pin = node.get("drawio_shape")
    if isinstance(pin, str):
        byk = {s["key"]: s for s in _SHAPES}
        s = byk.get(pin, {})
        return {"key": pin, "color": s.get("color"),
                "provider": s.get("shape_provider", "aws")}
    q = node.get("icon")
    if not q or not _SHAPES:
        return None
    provs = [node["provider"]] if node.get("provider") else (providers or [])
    allow = {p for p in provs if p in _SHAPE_PROVIDERS}
    if not allow:
        return None
    pool = [s for s in _SHAPES if s["shape_provider"] in allow]
    if not pool:
        return None
    best = max(pool, key=lambda s: icon_score(q, s))
    if icon_score(q, best) < MIN_SHAPE_SCORE:
        return None
    return {"key": best["key"], "color": best.get("color"),
            "provider": best["shape_provider"]}

ICON_CACHE = Path("./_icon_cache")
MIN_SCORE = 0.9          # below this, treat as "no confident icon"
ICON_PAD = 10            # px padding of icon inside a card

# ----------------------------------------------------------------------------
# Icon fetching
# ----------------------------------------------------------------------------

def fetch_svg(url: str, cache: Path) -> str | None:
    """Return raw SVG text (cached on disk)."""
    cache.mkdir(parents=True, exist_ok=True)
    fname = re.sub(r"[^A-Za-z0-9._-]", "_", url.split("/")[-1])
    f = cache / fname
    try:
        if not f.exists():
            safe = urllib.parse.quote(url, safe=":/?#[]@!$&'()*+,;=~")
            data = urllib.request.urlopen(safe, timeout=30).read()
            f.write_bytes(data)
        return f.read_text("utf-8", "replace")
    except Exception as e:
        print(f"  ! could not fetch {url}: {e}", file=sys.stderr)
        return None


def read_local_svg(rel_path: str) -> str | None:
    try:
        return (SKILL_ROOT / rel_path).read_text("utf-8", "replace")
    except Exception as e:
        print(f"  ! could not read bundled icon {rel_path}: {e}", file=sys.stderr)
        return None


def resolve_icon(node: dict, cache: Path, providers=None) -> tuple[str | None, str]:
    """Return (raw_svg_or_None, note). Honors node['icon_url'] if given.
    A node may set its own 'provider' to override the diagram default."""
    if node.get("icon_url"):
        return fetch_svg(node["icon_url"], cache), node["icon_url"]
    q = node.get("icon")
    if not q:
        return None, "(no icon specified)"
    node_providers = [node["provider"]] if node.get("provider") else providers
    hits = icon_search(q, 1, _INDEX, node_providers)
    if not hits or hits[0]["score"] < MIN_SCORE:
        best = hits[0] if hits else None
        return None, f"(weak match for '{q}': {best['name'] if best else 'none'} -> labeled box)"
    top = hits[0]
    if top.get("file"):                       # bundled local icon (aws / azure)
        return read_local_svg(top["file"]), f"{q} -> {top['name']} [{top.get('provider')}]"
    return fetch_svg(top["url"], cache), f"{q} -> {top['name']} [{top.get('provider')}]"


# ----------------------------------------------------------------------------
# Spec -> primitives
# ----------------------------------------------------------------------------

CARD_FILL = "#ffffff"
CARD_STROKE = "#c8c8c8"
ZONE_STROKE = "#9aa0a6"
TITLE_COLOR = "#1f1f1f"
DESC_COLOR = "#5f6368"


def anchor(node: dict, side: str) -> tuple[float, float]:
    x, y, w, h = node["x"], node["y"], node["width"], node["height"]
    return {
        "left":   (x, y + h / 2),
        "right":  (x + w, y + h / 2),
        "top":    (x + w / 2, y),
        "bottom": (x + w / 2, y + h),
        "center": (x + w / 2, y + h / 2),
    }[side]


def pick_sides(a: dict, b: dict) -> tuple[str, str]:
    """Choose exit/entry sides from relative geometry for clean routing."""
    ax, ay = a["x"] + a["width"] / 2, a["y"] + a["height"] / 2
    bx, by = b["x"] + b["width"] / 2, b["y"] + b["height"] / 2
    dx, dy = bx - ax, by - ay
    if abs(dx) >= abs(dy):
        return ("right", "left") if dx >= 0 else ("left", "right")
    return ("bottom", "top") if dy >= 0 else ("top", "bottom")


def route(a: dict, b: dict, waypoints) -> list[list[float]]:
    s_side, e_side = pick_sides(a, b)
    sx, sy = anchor(a, s_side)
    ex, ey = anchor(b, e_side)
    if waypoints:
        return [[sx, sy], *[list(p) for p in waypoints], [ex, ey]]
    # simple orthogonal elbow if both axes differ meaningfully
    if abs(sx - ex) > 8 and abs(sy - ey) > 8:
        if s_side in ("left", "right"):
            mid = (sx + ex) / 2
            return [[sx, sy], [mid, sy], [mid, ey], [ex, ey]]
        else:
            mid = (sy + ey) / 2
            return [[sx, sy], [sx, mid], [ex, mid], [ex, ey]]
    return [[sx, sy], [ex, ey]]


def build_primitives(spec: dict, cache: Path) -> list[dict]:
    prims: list[dict] = []
    notes: list[str] = []
    providers = spec.get("providers") or ([spec["provider"]] if spec.get("provider") else None)
    use_shapes = bool(spec.get("drawio_shapes"))

    # zones first (drawn behind)
    for z in spec.get("zones", []):
        prims.append({"kind": "rect", "x": z["x"], "y": z["y"],
                      "w": z["width"], "h": z["height"],
                      "fill": z.get("fill", "none"),
                      "stroke": z.get("color", ZONE_STROKE),
                      "dashed": z.get("style", "dashed") == "dashed",
                      "rounded": True, "opacity": z.get("opacity", 100)})
        if z.get("label"):
            prims.append({"kind": "text", "x": z["x"] + 16, "y": z["y"] + 12,
                          "text": z["label"], "size": 20, "bold": True,
                          "color": TITLE_COLOR})

    nodes_by_id = {n["id"]: n for n in spec.get("nodes", [])}

    # edges next (drawn under nodes so arrowheads tuck behind icons cleanly)
    for e in spec.get("edges", []):
        a, b = nodes_by_id.get(e["from"]), nodes_by_id.get(e["to"])
        if not a or not b:
            print(f"  ! edge references missing node: {e}", file=sys.stderr)
            continue
        pts = route(a, b, e.get("waypoints"))
        d = e.get("dir", "to")
        prims.append({"kind": "arrow", "points": pts,
                      "color": e.get("color", "#5f6368"),
                      "start_head": d in ("from", "both"),
                      "end_head": d in ("to", "both"),
                      "label": e.get("label", ""),
                      "dashed": e.get("style") == "dashed"})

    # nodes on top
    for n in spec.get("nodes", []):
        x, y, w, h = n["x"], n["y"], n["width"], n["height"]
        card = n.get("card", True)
        if card:
            prims.append({"kind": "rect", "x": x, "y": y, "w": w, "h": h,
                          "fill": CARD_FILL, "stroke": CARD_STROKE,
                          "dashed": False, "rounded": True, "opacity": 100})
        b64, note = resolve_icon(n, cache, providers)
        shape = resolve_drawio_shape(n, providers) if use_shapes else None
        if shape:
            note += f" | drawio:{shape['key']}"
        notes.append(f"{n['id']}: {note}")
        icon_sz = min(h - 2 * ICON_PAD, 56) if card else min(w, h)
        if b64 or shape:
            ix = x + ICON_PAD if card else x + (w - icon_sz) / 2
            iy = y + (h - icon_sz) / 2 if card else y
            prims.append({"kind": "image", "x": ix, "y": iy,
                          "w": icon_sz, "h": icon_sz, "svg": b64,
                          "drawio_shape": shape})
            text_x = ix + icon_sz + 12 if card else x
        else:
            text_x = x + 14 if card else x
        # title + optional description
        if card:
            prims.append({"kind": "text", "x": text_x, "y": y + 16,
                          "text": n.get("title", ""), "size": 16, "bold": True,
                          "color": TITLE_COLOR})
            if n.get("desc"):
                prims.append({"kind": "text", "x": text_x, "y": y + 40,
                              "text": n["desc"], "size": 13, "bold": False,
                              "color": DESC_COLOR})
        else:
            prims.append({"kind": "text", "x": x + w / 2, "y": y + h + 6,
                          "text": n.get("title", ""), "size": 14, "bold": True,
                          "color": TITLE_COLOR, "center": True})

    # numbered badges on very top
    for badge in spec.get("badges", []):
        prims.append({"kind": "badge", "x": badge["x"], "y": badge["y"],
                      "n": badge["n"]})

    if spec.get("title"):
        prims.insert(0, {"kind": "text", "x": 24, "y": 16,
                         "text": spec["title"], "size": 26, "bold": True,
                         "color": TITLE_COLOR})

    print("Icon resolution:\n  " + "\n  ".join(notes), file=sys.stderr)
    return prims


# ----------------------------------------------------------------------------
# Serializer: Excalidraw
# ----------------------------------------------------------------------------

def _seed():
    _seed.n += 1
    return _seed.n * 100003 % 2147483647
_seed.n = 0


def _ex_base(t, x, y, w, h):
    return {"type": t, "id": f"el{_seed()}", "x": x, "y": y, "width": w,
            "height": h, "angle": 0, "strokeColor": "#1e1e1e",
            "backgroundColor": "transparent", "fillStyle": "solid",
            "strokeWidth": 1, "strokeStyle": "solid", "roughness": 0,
            "opacity": 100, "groupIds": [], "frameId": None,
            "roundness": None, "seed": _seed(), "version": 1,
            "versionNonce": _seed(), "isDeleted": False, "boundElements": [],
            "updated": 1, "link": None, "locked": False}


def to_excalidraw(prims: list[dict]) -> str:
    els, files = [], {}
    for p in prims:
        if p["kind"] == "rect":
            e = _ex_base("rectangle", p["x"], p["y"], p["w"], p["h"])
            e["strokeColor"] = p["stroke"]
            e["backgroundColor"] = "transparent" if p["fill"] == "none" else p["fill"]
            e["strokeStyle"] = "dashed" if p["dashed"] else "solid"
            e["strokeWidth"] = 1.5 if p["dashed"] else 1
            e["roundness"] = {"type": 3} if p["rounded"] else None
            e["opacity"] = p.get("opacity", 100)
            els.append(e)
        elif p["kind"] == "image":
            if not p.get("svg"):
                continue  # native-draw.io-shape-only node; nothing to embed here
            fid = f"icon{_seed()}"
            b64 = base64.b64encode(p["svg"].encode("utf-8")).decode("ascii")
            files[fid] = {"mimeType": "image/svg+xml", "id": fid,
                          "dataURL": "data:image/svg+xml;base64," + b64,
                          "created": int(time.time() * 1000),
                          "lastRetrieved": int(time.time() * 1000)}
            e = _ex_base("image", p["x"], p["y"], p["w"], p["h"])
            e.update({"fileId": fid, "status": "saved", "scale": [1, 1],
                      "strokeColor": "transparent",
                      "backgroundColor": "transparent"})
            els.append(e)
        elif p["kind"] == "text":
            size = p["size"]
            txt = p["text"]
            w = max(8, len(txt) * size * 0.55)
            x = p["x"] - w / 2 if p.get("center") else p["x"]
            e = _ex_base("text", x, p["y"], w, size * 1.25)
            e.update({"text": txt, "fontSize": size,
                      "fontFamily": 2, "textAlign": "center" if p.get("center") else "left",
                      "verticalAlign": "top", "strokeColor": p["color"],
                      "containerId": None, "originalText": txt,
                      "lineHeight": 1.25, "baseline": size})
            els.append(e)
        elif p["kind"] == "arrow":
            pts = p["points"]
            x0, y0 = pts[0]
            rel = [[px - x0, py - y0] for px, py in pts]
            xs = [px for px, _ in pts]
            ys = [py for _, py in pts]
            e = _ex_base("arrow", x0, y0, max(xs) - min(xs), max(ys) - min(ys))
            e.update({"points": rel, "strokeColor": p["color"],
                      "strokeWidth": 2,
                      "strokeStyle": "dashed" if p["dashed"] else "solid",
                      "startArrowhead": "arrow" if p["start_head"] else None,
                      "endArrowhead": "arrow" if p["end_head"] else None,
                      "lastCommittedPoint": None, "startBinding": None,
                      "endBinding": None, "roundness": {"type": 2}})
            els.append(e)
            if p.get("label"):
                mid = pts[len(pts) // 2]
                size = 12
                w = max(8, len(p["label"]) * size * 0.55)
                t = _ex_base("text", mid[0] - w / 2, mid[1] - 18, w, size * 1.25)
                t.update({"text": p["label"], "fontSize": size, "fontFamily": 2,
                          "textAlign": "center", "verticalAlign": "top",
                          "strokeColor": p["color"], "containerId": None,
                          "originalText": p["label"], "lineHeight": 1.25,
                          "baseline": size})
                els.append(t)
        elif p["kind"] == "badge":
            d = 26
            e = _ex_base("ellipse", p["x"], p["y"], d, d)
            e.update({"backgroundColor": "#1a1a1a", "fillStyle": "solid",
                      "strokeColor": "#1a1a1a"})
            els.append(e)
            txt = str(p["n"])
            t = _ex_base("text", p["x"] + d / 2 - 5, p["y"] + 5, 12, 16)
            t.update({"text": txt, "fontSize": 14, "fontFamily": 2,
                      "textAlign": "center", "verticalAlign": "middle",
                      "strokeColor": "#ffffff", "containerId": None,
                      "originalText": txt, "lineHeight": 1.25, "baseline": 14})
            els.append(t)

    doc = {"type": "excalidraw", "version": 2,
           "source": "msicons-architecture-skill", "elements": els,
           "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
           "files": files}
    return json.dumps(doc, indent=2)


# ----------------------------------------------------------------------------
# Serializer: draw.io (mxGraph XML)
# ----------------------------------------------------------------------------

def _esc(s: str) -> str:
    return html.escape(s, quote=True)


def to_drawio(prims: list[dict]) -> str:
    cells, cid = [], [1]

    def nid():
        cid[0] += 1
        return f"c{cid[0]}"

    for p in prims:
        if p["kind"] == "rect":
            fill = "none" if p["fill"] == "none" else p["fill"]
            style = (f"rounded={1 if p['rounded'] else 0};whiteSpace=wrap;html=1;"
                     f"fillColor={fill};strokeColor={p['stroke']};"
                     f"{'dashed=1;' if p['dashed'] else ''}"
                     f"opacity={p.get('opacity',100)};")
            cells.append(f'<mxCell id="{nid()}" value="" style="{_esc(style)}" '
                         f'vertex="1" parent="1"><mxGeometry x="{p["x"]}" '
                         f'y="{p["y"]}" width="{p["w"]}" height="{p["h"]}" '
                         f'as="geometry"/></mxCell>')
        elif p["kind"] == "image":
            shp = p.get("drawio_shape")
            if shp:
                # Native draw.io vector stencil (recolorable, no embedded image).
                key, color, prov = shp["key"], shp.get("color"), shp["provider"]
                if prov == "aws":
                    pkg = key.rsplit(".", 1)[0]  # mxgraph.aws4
                    style = ("sketch=0;outlineConnect=0;fontColor=#232F3E;"
                             "gradientColor=none;fillColor=" + (color or "#232F3E") +
                             ";strokeColor=none;dashed=0;verticalLabelPosition=bottom;"
                             "verticalAlign=top;align=center;html=1;fontSize=12;"
                             "fontStyle=0;aspect=fixed;shape=" + pkg +
                             ".resourceIcon;resIcon=" + key + ";")
                elif prov == "gcp":  # self-colored stencils
                    style = ("sketch=0;outlineConnect=0;html=1;"
                             "verticalLabelPosition=bottom;verticalAlign=top;"
                             "align=center;aspect=fixed;shape=" + key + ";")
                else:  # azure (monochrome) -> give it a fill
                    style = ("sketch=0;html=1;aspect=fixed;strokeColor=none;"
                             "fillColor=" + (color or "#0078D4") +
                             ";verticalLabelPosition=bottom;verticalAlign=top;"
                             "align=center;shape=" + key + ";")
                cells.append(f'<mxCell id="{nid()}" value="" style="{_esc(style)}" '
                             f'vertex="1" parent="1"><mxGeometry x="{p["x"]}" '
                             f'y="{p["y"]}" width="{p["w"]}" height="{p["h"]}" '
                             f'as="geometry"/></mxCell>')
                continue
            if not p.get("svg"):
                continue
            # Percent-encode the raw SVG so the data URI contains no ';' or '='
            # that would break mxGraph's style-string parser (key=val;key=val).
            enc = urllib.parse.quote(p["svg"], safe="")
            style = ("shape=image;html=1;imageAspect=0;aspect=fixed;"
                     "verticalAlign=top;strokeColor=none;"
                     "image=data:image/svg+xml," + enc + ";")
            cells.append(f'<mxCell id="{nid()}" value="" style="{_esc(style)}" '
                         f'vertex="1" parent="1"><mxGeometry x="{p["x"]}" '
                         f'y="{p["y"]}" width="{p["w"]}" height="{p["h"]}" '
                         f'as="geometry"/></mxCell>')
        elif p["kind"] == "text":
            align = "center" if p.get("center") else "left"
            style = (f"text;html=1;align={align};verticalAlign=top;"
                     f"fontColor={p['color']};fontSize={p['size']};"
                     f"{'fontStyle=1;' if p['bold'] else ''}")
            w = max(40, len(p["text"]) * p["size"] * 0.6)
            x = p["x"] - w / 2 if p.get("center") else p["x"]
            cells.append(f'<mxCell id="{nid()}" value="{_esc(p["text"])}" '
                         f'style="{_esc(style)}" vertex="1" parent="1">'
                         f'<mxGeometry x="{x}" y="{p["y"]}" width="{w}" '
                         f'height="{p["size"]*1.4:.0f}" as="geometry"/></mxCell>')
        elif p["kind"] == "arrow":
            pts = p["points"]
            startA = "classic" if p["start_head"] else "none"
            endA = "classic" if p["end_head"] else "none"
            style = (f"endArrow={endA};startArrow={startA};html=1;rounded=1;"
                     f"strokeColor={p['color']};strokeWidth=2;"
                     f"{'dashed=1;' if p['dashed'] else ''}")
            mids = "".join(f'<mxPoint x="{x}" y="{y}" />' for x, y in pts[1:-1])
            cells.append(
                f'<mxCell id="{nid()}" value="{_esc(p.get("label",""))}" '
                f'style="{_esc(style)}" edge="1" parent="1">'
                f'<mxGeometry relative="1" as="geometry">'
                f'<mxPoint x="{pts[0][0]}" y="{pts[0][1]}" as="sourcePoint"/>'
                f'<mxPoint x="{pts[-1][0]}" y="{pts[-1][1]}" as="targetPoint"/>'
                f'<Array as="points">{mids}</Array></mxGeometry></mxCell>')
        elif p["kind"] == "badge":
            d = 26
            style = ("ellipse;whiteSpace=wrap;html=1;fillColor=#1a1a1a;"
                     "strokeColor=#1a1a1a;fontColor=#ffffff;fontStyle=1;"
                     "fontSize=14;")
            cells.append(f'<mxCell id="{nid()}" value="{p["n"]}" '
                         f'style="{_esc(style)}" vertex="1" parent="1">'
                         f'<mxGeometry x="{p["x"]}" y="{p["y"]}" width="{d}" '
                         f'height="{d}" as="geometry"/></mxCell>')

    body = "\n        ".join(cells)
    return (
        '<mxfile host="app.diagrams.net" type="device">\n'
        '  <diagram name="Architecture" id="arch1">\n'
        '    <mxGraphModel dx="1422" dy="800" grid="1" gridSize="10" '
        'guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" '
        'pageScale="1" pageWidth="1600" pageHeight="900" math="0" shadow="0">\n'
        '      <root>\n'
        '        <mxCell id="0" />\n'
        '        <mxCell id="1" parent="0" />\n'
        f'        {body}\n'
        '      </root>\n'
        '    </mxGraphModel>\n'
        '  </diagram>\n'
        '</mxfile>\n'
    )


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec", help="path to spec JSON (or - for stdin)")
    ap.add_argument("--out-prefix", default="architecture")
    ap.add_argument("--cache", default=str(ICON_CACHE))
    ap.add_argument("--only", choices=["excalidraw", "drawio"], help="emit one format")
    ap.add_argument("--drawio-shapes", action="store_true",
                    help="use draw.io native vector stencils in the .drawio output "
                         "(AWS/GCP/Azure) instead of embedded SVG; Excalidraw still "
                         "uses embedded SVG")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.spec == "-" else Path(args.spec).read_text()
    spec = json.loads(raw)
    if args.drawio_shapes:
        spec["drawio_shapes"] = True
    cache = Path(args.cache)

    prims = build_primitives(spec, cache)

    written = []
    if args.only in (None, "excalidraw"):
        out = Path(f"{args.out_prefix}.excalidraw")
        out.write_text(to_excalidraw(prims))
        written.append(str(out))
    if args.only in (None, "drawio"):
        out = Path(f"{args.out_prefix}.drawio")
        out.write_text(to_drawio(prims))
        written.append(str(out))

    print("Wrote: " + ", ".join(written))


# Load index once at import (used by resolve_icon).
_IDX_PATH = Path(__file__).resolve().parent.parent / "references" / "icon-index.json"
_INDEX = json.loads(_IDX_PATH.read_text("utf-8")) if _IDX_PATH.exists() else []
_SHAPES = _load_shapes()

if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Layout library for hand-drawn-style Excalidraw study notes (stdlib only).

Builds a multi-page A4 scene in the "Maven notes" template:
  - Virgil hand-drawn headings (magenta title; orange/green/red sections)
  - Cascadia mono blue body with '-->' definitions, '*' bullets, numbered steps
  - pale-yellow rounded diagram nodes with gray arrows
  - magenta command boxes with gray labels

Usage: import this module from a per-lecture driver (see
examples/example_board.py), call the helpers to lay out pages, then:

    import make_notes as mb
    mb.frame(0, "Page 1 - ...")
    ... helpers with page=0 ...
    mb.save("NN-slug", outdir=".")   # writes .excalidraw + .html, validates

The HTML mirrors the scene layout and loads the real Excalidraw webfonts;
print it to PDF with any headless Chrome (preferCSSPageSize=True).
"""
import json, random, html as htmlmod

# ---- palette (Excalidraw standard shades) ----
MAGENTA = "#c2255c"
ORANGE  = "#e8590c"
GREEN   = "#2f9e44"
RED     = "#e03131"
BLUE    = "#1971c2"
GRAY    = "#495057"
YELLOW  = "#ffec99"
NODE_BORDER = "#f08c00"

PAGE_W, PAGE_H = 794, 1123   # A4 @96dpi
MARGIN = 56
CONTENT_W = PAGE_W - 2 * MARGIN
PAGE_GAP = 90

VIRGIL, MONO = 1, 3          # Excalidraw fontFamily codes (2 = Helvetica)
MONO_FACTOR = 0.60           # avg glyph width in em, for wrapping estimates
VIRGIL_FACTOR = 0.50
LH = 1.25                    # lineHeight

_elements = []
_n = 0
_rng = random.Random(42)


def reset():
    """Clear the scene (call before building a new board)."""
    global _elements, _n
    _elements = []
    _n = 0


def _base(typ, x, y, w, h, stroke, bg="transparent", page=0, frame=None):
    global _n
    _n += 1
    return {
        "id": f"el-{_n:04d}", "type": typ,
        "x": x, "y": y + page * (PAGE_H + PAGE_GAP),
        "width": w, "height": h, "angle": 0,
        "strokeColor": stroke, "backgroundColor": bg,
        "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
        "roughness": 1, "opacity": 100, "groupIds": [],
        "frameId": frame, "roundness": None,
        "seed": _rng.randint(1, 2**31), "version": 1,
        "versionNonce": _rng.randint(1, 2**31),
        "isDeleted": False, "boundElements": None,
        "updated": 1732000000000, "link": None, "locked": False,
        "_page": page,
    }


def frame(page, name):
    """Named page frame (lets the user export per page on excalidraw.com)."""
    f = _base("frame", MARGIN - 24, 24, PAGE_W - 2 * (MARGIN - 24),
              PAGE_H - 48, "#adb5bd", page=page)
    f["name"] = name
    _elements.append(f)
    return f["id"]


def wrap_lines(text, width_px, size, factor):
    maxc = max(8, int(width_px / (size * factor)))
    out = []
    for raw in text.split("\n"):
        if len(raw) <= maxc:
            out.append(raw)
            continue
        indent = raw[:len(raw) - len(raw.lstrip())]
        cur = ""
        for word in raw.split(" "):
            if not word:
                continue
            trial = (cur + " " + word) if cur else word
            if len(trial) <= maxc:
                cur = trial
            else:
                out.append(cur)
                cur = indent + "  " + word
        if cur:
            out.append(cur)
    return out


def text(x, y, s, size, color, family=MONO, page=0, align="left",
         width=None, frame=None):
    """Pre-wrapped text block; returns the y just below it."""
    factor = MONO_FACTOR if family == MONO else VIRGIL_FACTOR
    lines = wrap_lines(s, width or CONTENT_W, size, factor)
    txt = "\n".join(lines)
    w = width if width is not None else max(len(l) for l in lines) * size * factor
    h = len(lines) * size * LH
    e = _base("text", x, y, w, h, color, page=page, frame=frame)
    e.update({"fontSize": size, "fontFamily": family, "text": txt,
              "textAlign": align, "verticalAlign": "top", "containerId": None,
              "originalText": txt, "lineHeight": LH})
    _elements.append(e)
    return y + h


def title(s, page=0, frame=None, y=64, size=36):
    """Centered magenta hand-drawn main title; returns y below it."""
    w = len(s) * size * VIRGIL_FACTOR
    return text((PAGE_W - w) / 2, y, s, size, MAGENTA, VIRGIL, page=page,
                align="center", width=w, frame=frame)


def heading(s, color=ORANGE, page=0, frame=None, y=None, size=22):
    """Hand-drawn section heading; returns y below it."""
    return text(MARGIN, y, s, size, color, VIRGIL, page=page, frame=frame)


def rect(x, y, w, h, page=0, stroke=NODE_BORDER, bg=YELLOW, frame=None,
         dashed=False):
    e = _base("rectangle", x, y, w, h, stroke, bg=bg, page=page, frame=frame)
    e["roundness"] = {"type": 3}
    if dashed:
        e["strokeStyle"] = "dashed"
    _elements.append(e)
    return e


def arrow(x1, y1, x2, y2, page=0, color=GRAY, dashed=False, frame=None):
    e = _base("arrow", x1, y1, abs(x2 - x1), abs(y2 - y1), color,
              page=page, frame=frame)
    e.update({"points": [[0, 0], [x2 - x1, y2 - y1]],
              "lastCommittedPoint": None, "startBinding": None,
              "endBinding": None, "startArrowhead": None,
              "endArrowhead": "arrow"})
    if dashed:
        e["strokeStyle"] = "dotted"
    _elements.append(e)
    return e


def node(cx, y, w, h, label, page=0, size=16, color=BLUE, frame=None):
    """Yellow rounded diagram node with centered mono label; cx = center x."""
    x = cx - w / 2
    rect(x, y, w, h, page=page, frame=frame)
    lines = label.split("\n")
    th = len(lines) * size * LH
    tw = max(len(l) for l in lines) * size * MONO_FACTOR
    text(cx - tw / 2, y + (h - th) / 2, label, size, color, page=page,
         align="center", width=tw, frame=frame)
    return (x, y, w, h)


def alabel(x, y, s, page=0, color=BLUE, size=13, frame=None):
    """Small arrow/diagram caption."""
    return text(x, y, s, size, color, page=page, frame=frame)


def command_box(x, y, w, commands, label="Commands:", page=0, frame=None,
                size=15):
    """Dark-outlined rounded box with magenta mono commands + gray label.

    commands: str with \\n between lines. Returns y below the box.
    """
    text(x, y, label, 14, GRAY, page=page, frame=frame)
    by = y + 22
    lines = commands.split("\n")
    bh = len(lines) * size * LH + 20
    rect(x, by, w, bh, page=page, stroke=GRAY, bg="transparent", frame=frame)
    text(x + 12, by + 10, commands, size, MAGENTA, page=page, frame=frame)
    return by + bh


def scene_json():
    els = []
    for e in _elements:
        e = dict(e)
        e.pop("_page", None)
        els.append(e)
    return {"type": "excalidraw", "version": 2,
            "source": "https://excalidraw.com",
            "elements": els,
            "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
            "files": {}}


def validate():
    """Schema + same-column text-overlap check. Returns (n_elements, overlaps)."""
    req = {"id", "type", "x", "y", "width", "height", "angle", "strokeColor",
           "backgroundColor", "fillStyle", "strokeWidth", "strokeStyle",
           "roughness", "opacity", "groupIds", "frameId", "roundness",
           "seed", "version", "versionNonce", "isDeleted", "boundElements",
           "updated", "link", "locked"}
    for e in _elements:
        missing = req - set(e)
        assert not missing, (e["id"], missing)
    texts = [e for e in _elements if e["type"] == "text"]
    overlaps = 0
    for i, a in enumerate(texts):
        for b in texts[i + 1:]:
            if a["_page"] != b["_page"]:
                continue
            if (abs(a["x"] - b["x"]) < 40
                    and a["x"] < b["x"] + b["width"]
                    and b["x"] < a["x"] + a["width"]):
                if not (a["y"] + a["height"] <= b["y"] + 1
                        or b["y"] + b["height"] <= a["y"] + 1):
                    overlaps += 1
                    print("OVERLAP:", a["text"][:30].replace("\n", " "),
                          "<->", b["text"][:30].replace("\n", " "))
    return len(_elements), overlaps


def page_end_y(page):
    """Lowest content y on a page (must stay < PAGE_H)."""
    ys = [e["y"] - page * (PAGE_H + PAGE_GAP) + e["height"]
          for e in _elements if e["_page"] == page and e["type"] != "frame"]
    return max(ys) if ys else 0


def render_html(path):
    pages = {}
    for e in _elements:
        pages.setdefault(e["_page"], []).append(e)
    css = """
@font-face { font-family:'Virgil'; src:url('https://excalidraw.com/Virgil.woff2') format('woff2'); }
@font-face { font-family:'Cascadia'; src:url('https://excalidraw.com/Cascadia.woff2') format('woff2'); }
@page { size: A4 portrait; margin: 0; }
html,body { margin:0; padding:0; background:#fff; }
.page { position:relative; width:794px; height:1123px; overflow:hidden;
         page-break-after:always; background:#fff; }
.page:last-child { page-break-after:auto; }
.el { position:absolute; }
.txt { white-space:pre; line-height:1.25; }
svg.ov { position:absolute; left:0; top:0; pointer-events:none; }
"""
    parts = [f"<style>{css}</style>"]
    for p in sorted(pages):
        parts.append(f'<div class="page" id="page{p+1}">')
        svg = ['<svg class="ov" width="794" height="1123">'
               '<defs><marker id="ah" markerWidth="10" markerHeight="10" '
               'refX="7" refY="3.5" orient="auto">'
               '<path d="M0,0 L8,3.5 L0,7 Z" fill="context-stroke"/></marker></defs>']
        for e in pages[p]:
            if e["type"] == "frame":
                continue
            y = e["y"] - p * (PAGE_H + PAGE_GAP)
            x = e["x"]
            if e["type"] == "rectangle":
                bg = (e["backgroundColor"]
                      if e["backgroundColor"] != "transparent" else "#fff")
                parts.append(
                    f'<div class="el" style="left:{x}px;top:{y}px;'
                    f'width:{e["width"]}px;height:{e["height"]}px;'
                    f'border:1.5px solid {e["strokeColor"]};'
                    f'border-radius:12px;background:{bg};'
                    f'box-sizing:border-box;"></div>')
            elif e["type"] == "text":
                fam = "Virgil" if e["fontFamily"] == VIRGIL else "Cascadia"
                parts.append(
                    f'<div class="el txt" style="left:{x}px;top:{y}px;'
                    f'width:{e["width"]}px;font-family:\'{fam}\';'
                    f'font-size:{e["fontSize"]}px;color:{e["strokeColor"]};'
                    f'text-align:{e["textAlign"]};">'
                    f'{htmlmod.escape(e["text"])}</div>')
            elif e["type"] in ("arrow", "line"):
                (dx, dy) = e["points"][1]
                dash = (' stroke-dasharray="2 6" stroke-linecap="round"'
                        if e["strokeStyle"] == "dotted" else "")
                head = (' marker-end="url(#ah)"'
                        if e["type"] == "arrow" else "")
                svg.append(
                    f'<line x1="{x}" y1="{y}" x2="{x+dx}" y2="{y+dy}" '
                    f'stroke="{e["strokeColor"]}" stroke-width="1.5"'
                    f'{dash}{head}/>')
        svg.append("</svg>")
        parts.append("".join(svg))
        parts.append("</div>")
    with open(path, "w", encoding="utf-8") as f:
        f.write("<!doctype html><html><head><meta charset='utf-8'></head>"
                "<body>" + "".join(parts) + "</body></html>")


def save(slug, outdir="."):
    """Write <slug>.excalidraw + <slug>.html; print validation summary."""
    n, overlaps = validate()
    pages = sorted({e["_page"] for e in _elements})
    for p in pages:
        end = page_end_y(p)
        print(f"page {p+1} ends at y={end:.0f} / {PAGE_H}"
              + ("  <-- OVERFLOW!" if end >= PAGE_H else ""))
    with open(f"{outdir}/{slug}.excalidraw", "w", encoding="utf-8") as f:
        json.dump(scene_json(), f, ensure_ascii=False, indent=1)
    render_html(f"{outdir}/{slug}.html")
    print(f"elements={n} overlaps={overlaps}")
    if overlaps:
        raise SystemExit("Fix overlaps before exporting PDF.")
    return f"{outdir}/{slug}.excalidraw", f"{outdir}/{slug}.html"

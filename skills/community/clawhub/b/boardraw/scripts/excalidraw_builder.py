#!/usr/bin/env python3
"""
excalidraw_builder.py — Python helper for building valid .excalidraw files.

Why this exists: the .excalidraw JSON schema has several fragile
requirements (random ids, seed/versionNonce, two-way boundElements
references between shapes/text/arrows, points relative to the element's
own x/y, etc). Hand-writing this JSON is error prone. This module handles
all of that so you can focus on layout and content.

Typical usage
-------------
    from excalidraw_builder import ExcalidrawDoc

    doc = ExcalidrawDoc()

    start = doc.diamond(40, 40, 160, 80, bg="blue")
    doc.label(start, "开始?")

    step1 = doc.rectangle(40, 200, 160, 80, bg="green")
    doc.label(step1, "处理数据")

    doc.arrow(start, step1)

    doc.save("/tmp/flow.excalidraw")

See SKILL.md for layout conventions and references/excalidraw-schema.md
for the raw JSON schema if you ever need to hand-edit an element.
"""

import json
import random
import string
import time

# ---------------------------------------------------------------------------
# Excalidraw's default color palette (hex). Passing a name string for any
# `stroke=` / `bg=` argument below will be looked up here; you can also pass
# a raw hex string directly.
# ---------------------------------------------------------------------------
STROKE_COLORS = {
    "black": "#1e1e1e",
    "red": "#e03131",
    "green": "#2f9e44",
    "blue": "#1971c2",
    "orange": "#f08c00",
}

BG_COLORS = {
    "transparent": "transparent",
    "red": "#ffc9c9",
    "green": "#b2f2bb",
    "blue": "#a5d8ff",
    "yellow": "#ffec99",
    "orange": "#ffd8a8",
    "violet": "#d0bfff",
}


def _color(value, table):
    if value is None:
        return None
    return table.get(value, value)  # fall back to treating it as raw hex


def _id(n=16):
    alphabet = string.ascii_letters + string.digits
    return "".join(random.choices(alphabet, k=n))


def _seed():
    return random.randint(1, 2**31 - 1)


def _now_ms():
    return int(time.time() * 1000)


def _text_size(text, font_size):
    """Rough width/height estimate for a text run (good enough for layout;
    Excalidraw recomputes exact metrics itself when the file is opened)."""
    lines = text.split("\n")
    longest = max((len(line) for line in lines), default=0)
    width = max(10, longest * font_size * 0.6)
    height = len(lines) * font_size * 1.25
    return width, height


def _segment_hits_rect(p1, p2, rect):
    """True if segment p1->p2 intersects axis-aligned rect (xmin,ymin,xmax,ymax).
    Liang-Barsky line clipping — used by find_crossings()."""
    x0, y0 = p1
    x1, y1 = p2
    xmin, ymin, xmax, ymax = rect
    dx, dy = x1 - x0, y1 - y0
    p = [-dx, dx, -dy, dy]
    q = [x0 - xmin, xmax - x0, y0 - ymin, ymax - y0]
    u1, u2 = 0.0, 1.0
    for pi, qi in zip(p, q):
        if pi == 0:
            if qi < 0:
                return False
        else:
            t = qi / pi
            if pi < 0:
                if t > u2:
                    return False
                if t > u1:
                    u1 = t
            else:
                if t < u1:
                    return False
                if t < u2:
                    u2 = t
    return u1 <= u2


class ExcalidrawDoc:
    """Accumulates elements and writes out a complete .excalidraw file."""

    def __init__(self):
        self.elements = []

    # -- low level -----------------------------------------------------

    def _base(self, type_, x, y, width, height, **overrides):
        el = {
            "id": _id(),
            "type": type_,
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "angle": 0,
            "strokeColor": "#1e1e1e",
            "backgroundColor": "transparent",
            "fillStyle": "hachure",
            "strokeWidth": 2,
            "strokeStyle": "solid",
            "roughness": 1,
            "opacity": 100,
            "groupIds": [],
            "frameId": None,
            "roundness": None,
            "seed": _seed(),
            "version": 1,
            "versionNonce": _seed(),
            "isDeleted": False,
            "boundElements": [],
            "updated": _now_ms(),
            "link": None,
            "locked": False,
        }
        el.update(overrides)
        self.elements.append(el)
        return el

    # -- shapes ----------------------------------------------------------

    def rectangle(self, x, y, w, h, stroke="black", bg="transparent",
                  rounded=True, fill_style="hachure", roughness=1,
                  stroke_width=2, **kw):
        return self._base(
            "rectangle", x, y, w, h,
            strokeColor=_color(stroke, STROKE_COLORS),
            backgroundColor=_color(bg, BG_COLORS),
            fillStyle=fill_style, roughness=roughness, strokeWidth=stroke_width,
            roundness={"type": 3} if rounded else None,
            **kw,
        )

    def ellipse(self, x, y, w, h, stroke="black", bg="transparent",
                fill_style="hachure", roughness=1, stroke_width=2, **kw):
        return self._base(
            "ellipse", x, y, w, h,
            strokeColor=_color(stroke, STROKE_COLORS),
            backgroundColor=_color(bg, BG_COLORS),
            fillStyle=fill_style, roughness=roughness, strokeWidth=stroke_width,
            **kw,
        )

    def diamond(self, x, y, w, h, stroke="black", bg="transparent",
                fill_style="hachure", roughness=1, stroke_width=2, **kw):
        return self._base(
            "diamond", x, y, w, h,
            strokeColor=_color(stroke, STROKE_COLORS),
            backgroundColor=_color(bg, BG_COLORS),
            fillStyle=fill_style, roughness=roughness, strokeWidth=stroke_width,
            **kw,
        )

    def frame(self, x, y, w, h, name="Frame"):
        """An Excalidraw frame (a named region). Add elements to it with
        put_in_frame()."""
        return self._base("frame", x, y, w, h, name=name, strokeColor="#1e1e1e",
                           backgroundColor="transparent")

    def put_in_frame(self, element, frame_el):
        element["frameId"] = frame_el["id"]

    # -- text --------------------------------------------------------------

    def text(self, x, y, text, font_size=20, stroke="black",
              align="left", vertical_align="top", font_family=2, **kw):
        width, height = _text_size(text, font_size)
        return self._base(
            "text", x, y, width, height,
            text=text, originalText=text, fontSize=font_size, fontFamily=font_family,
            textAlign=align, verticalAlign=vertical_align,
            containerId=None, lineHeight=1.25,
            strokeColor=_color(stroke, STROKE_COLORS),
            **kw,
        )

    def label(self, container, text, font_size=20, stroke="black", font_family=2):
        """Bind a centered text label inside a shape (rectangle/ellipse/
        diamond/frame). This is the normal way to put a title/word on a
        node — do NOT create a free-floating text element on top of a shape,
        bind it instead so it moves with the shape.

        font_family defaults to 2 (Helvetica/Normal). Font 1 (Excalifont,
        the default hand-drawn font) has poor/no CJK glyph coverage and can
        render Chinese/Japanese/Korean text as broken or mismatched glyphs
        — only use font_family=1 for short English/Latin titles where the
        hand-drawn look is wanted."""
        width, height = _text_size(text, font_size)
        tx = container["x"] + (container["width"] - width) / 2
        ty = container["y"] + (container["height"] - height) / 2
        t = self._base(
            "text", tx, ty, width, height,
            text=text, originalText=text, fontSize=font_size, fontFamily=font_family,
            textAlign="center", verticalAlign="middle",
            containerId=container["id"], lineHeight=1.25,
            strokeColor=_color(stroke, STROKE_COLORS),
        )
        container["boundElements"].append({"id": t["id"], "type": "text"})
        return t

    # -- connectors ----------------------------------------------------

    def arrow(self, start_el, end_el, stroke="black", stroke_width=2,
              start_arrowhead=None, end_arrowhead="arrow", label=None,
              font_size=16, font_family=2, **kw):
        """Straight arrow bound between the centers of two elements.
        Excalidraw clips it to each shape's edge automatically via bindings.

        Use this ONLY when the two nodes are directly adjacent (same column
        or same row with no other node blocking the straight path). For all
        other cases — parallel nodes merging into one, loop-back arrows that
        skip multiple steps — use elbow_arrow() instead."""
        sx = start_el["x"] + start_el["width"] / 2
        sy = start_el["y"] + start_el["height"] / 2
        ex = end_el["x"] + end_el["width"] / 2
        ey = end_el["y"] + end_el["height"] / 2
        x, y = min(sx, ex), min(sy, ey)
        w, h = abs(ex - sx) or 1, abs(ey - sy) or 1
        points = [[sx - x, sy - y], [ex - x, ey - y]]
        el = self._base(
            "arrow", x, y, w, h,
            points=points, lastCommittedPoint=None,
            startBinding={"elementId": start_el["id"], "focus": 0, "gap": 4},
            endBinding={"elementId": end_el["id"], "focus": 0, "gap": 4},
            startArrowhead=start_arrowhead, endArrowhead=end_arrowhead,
            strokeColor=_color(stroke, STROKE_COLORS), strokeWidth=stroke_width,
            **kw,
        )
        start_el["boundElements"].append({"id": el["id"], "type": "arrow"})
        end_el["boundElements"].append({"id": el["id"], "type": "arrow"})
        if label:
            mx, my = x + w / 2, y + h / 2
            fw, fh = _text_size(label, font_size)
            self._base(
                "text", mx - fw / 2, my - fh / 2, fw, fh,
                text=label, originalText=label, fontSize=font_size, fontFamily=font_family,
                textAlign="center", verticalAlign="middle",
                containerId=el["id"], lineHeight=1.25,
                strokeColor=_color(stroke, STROKE_COLORS),
            )
        return el

    def elbow_arrow(self, start_el, end_el, exit="bottom", enter="top",
                     bend=None, waypoints=None, stroke="black", stroke_width=2,
                     start_arrowhead=None, end_arrowhead="arrow",
                     label=None, font_size=16, font_family=2, **kw):
        """Right-angle ("elbow") arrow between two elements' edges.

        Use this INSTEAD OF arrow() whenever the two elements are not
        directly above/below or left/right of each other with a clear
        straight path between them — e.g. several parallel nodes merging
        into one node below, a decision branching sideways, or any
        connection where a straight line would cut diagonally across
        other nodes. A straight diagonal line crossing unrelated nodes is
        the #1 cause of messy-looking diagrams; elbow_arrow avoids it by
        routing in clean horizontal/vertical segments instead.

        exit / enter: which edge of start_el / end_el the line leaves from
            and arrives at — "top" | "bottom" | "left" | "right". Pick a
            matching axis pair (top/bottom with top/bottom, or left/right
            with left/right) whenever you want the detour to go AROUND a
            row or column rather than across it — e.g. a loop-back that
            needs to clear an entire row of nodes should exit and enter on
            "bottom" (routes below everything), not exit "bottom" / enter
            "right" (that cuts sideways through whatever sits between the
            two elements' vertical span, which is exactly the crossing bug
            this function exists to avoid — always call find_crossings()
            after building to confirm).
        bend: the x (for left/right exits) or y (for top/bottom exits)
            coordinate where the path turns. If omitted, it defaults to
            the midpoint between the two elements — fine for a simple
            merge, but for a long loop-back arrow you should pass an
            explicit value from self.right_lane_x()/self.bottom_lane_y()
            so the detour clears every node in between rather than
            guessing a midpoint that might still overlap something.
        waypoints: optional list of explicit absolute [x, y] points to
            route through between the start and end edge points, for
            routes more complex than a single bend can express (e.g. an
            "S" that has to dodge two separate obstacles). When given,
            this overrides exit/enter/bend's automatic 1-bend routing —
            the path becomes [start_edge, *waypoints, end_edge].
        """
        sx, sy = self._edge_point(start_el, exit)
        ex, ey = self._edge_point(end_el, enter)

        if waypoints:
            pts_abs = [(sx, sy), *[tuple(p) for p in waypoints], (ex, ey)]
        elif exit in ("top", "bottom") and enter in ("top", "bottom"):
            by = bend if bend is not None else (sy + ey) / 2
            pts_abs = [(sx, sy), (sx, by), (ex, by), (ex, ey)]
        elif exit in ("left", "right") and enter in ("left", "right"):
            bx = bend if bend is not None else (sx + ex) / 2
            pts_abs = [(sx, sy), (bx, sy), (bx, ey), (ex, ey)]
        elif exit in ("top", "bottom"):
            pts_abs = [(sx, sy), (sx, ey), (ex, ey)]
        else:
            pts_abs = [(sx, sy), (ex, sy), (ex, ey)]

        # drop zero-length consecutive duplicate points
        dedup = [pts_abs[0]]
        for p in pts_abs[1:]:
            if p != dedup[-1]:
                dedup.append(p)
        pts_abs = dedup

        xs = [p[0] for p in pts_abs]
        ys = [p[1] for p in pts_abs]
        x0, y0 = min(xs), min(ys)
        rel = [[p[0] - x0, p[1] - y0] for p in pts_abs]
        el = self._base(
            "arrow", x0, y0, (max(xs) - x0) or 1, (max(ys) - y0) or 1,
            points=rel, lastCommittedPoint=None,
            startBinding={"elementId": start_el["id"], "focus": 0, "gap": 4},
            endBinding={"elementId": end_el["id"], "focus": 0, "gap": 4},
            startArrowhead=start_arrowhead, endArrowhead=end_arrowhead,
            strokeColor=_color(stroke, STROKE_COLORS), strokeWidth=stroke_width,
            roundness={"type": 2},  # rounds the elbow corners
            **kw,
        )
        start_el["boundElements"].append({"id": el["id"], "type": "arrow"})
        end_el["boundElements"].append({"id": el["id"], "type": "arrow"})
        if label:
            mid = pts_abs[len(pts_abs) // 2] if len(pts_abs) > 2 else \
                ((pts_abs[0][0] + pts_abs[-1][0]) / 2, (pts_abs[0][1] + pts_abs[-1][1]) / 2)
            fw, fh = _text_size(label, font_size)
            self._base(
                "text", mid[0] - fw / 2, mid[1] - fh / 2, fw, fh,
                text=label, originalText=label, fontSize=font_size, fontFamily=font_family,
                textAlign="center", verticalAlign="middle",
                containerId=el["id"], lineHeight=1.25,
                strokeColor=_color(stroke, STROKE_COLORS),
            )
        return el

    def _edge_point(self, el, side):
        x, y, w, h = el["x"], el["y"], el["width"], el["height"]
        return {
            "top": (x + w / 2, y),
            "bottom": (x + w / 2, y + h),
            "left": (x, y + h / 2),
            "right": (x + w, y + h / 2),
        }[side]

    def right_lane_x(self, margin=140):
        """X coordinate clear of every element added so far, for routing
        loop-back / feedback arrows out to the right so they don't cross
        the main flow. Call this AFTER building the main flow, then pass
        it as `bend=` to elbow_arrow(..., exit="right", enter="right")."""
        if not self.elements:
            return margin
        return max(e["x"] + e["width"] for e in self.elements) + margin

    def bottom_lane_y(self, margin=100):
        """Y coordinate clear of every element added so far — same idea as
        right_lane_x() but for routing a detour below everything."""
        if not self.elements:
            return margin
        return max(e["y"] + e["height"] for e in self.elements) + margin

    def find_crossings(self, margin=6):
        """Sanity check: returns a list of (arrow_id, element_id,
        element_type) for every case where an arrow/line's path cuts
        through a shape it is NOT bound to. Call this after building the
        diagram — if it returns anything, that connection is going to look
        like a line stabbing through an unrelated box, so re-route it with
        elbow_arrow() (and right_lane_x()/bottom_lane_y() for the detour)
        or reposition nodes, then check again before saving."""
        shape_types = {"rectangle", "ellipse", "diamond", "frame"}
        shapes = [e for e in self.elements if e["type"] in shape_types]
        arrows = [e for e in self.elements if e["type"] in ("arrow", "line")]
        crossings = []
        for a in arrows:
            bound_ids = set()
            if a.get("startBinding"):
                bound_ids.add(a["startBinding"]["elementId"])
            if a.get("endBinding"):
                bound_ids.add(a["endBinding"]["elementId"])
            abs_pts = [(a["x"] + p[0], a["y"] + p[1]) for p in a["points"]]
            for s in shapes:
                if s["id"] in bound_ids:
                    continue
                rect = (s["x"] + margin, s["y"] + margin,
                        s["x"] + s["width"] - margin, s["y"] + s["height"] - margin)
                if rect[2] <= rect[0] or rect[3] <= rect[1]:
                    continue
                for p1, p2 in zip(abs_pts, abs_pts[1:]):
                    if _segment_hits_rect(p1, p2, rect):
                        crossings.append((a["id"], s["id"], s["type"]))
                        break
        return crossings

    def line(self, points, stroke="black", stroke_width=2, closed=False, **kw):
        """A freeform poly-line through absolute [x, y] points (no
        arrowheads). Good for dividers, borders, simple connectors."""
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        x, y = min(xs), min(ys)
        rel = [[p[0] - x, p[1] - y] for p in points]
        return self._base(
            "line", x, y, max(xs) - x or 1, max(ys) - y or 1,
            points=rel, lastCommittedPoint=None,
            startBinding=None, endBinding=None,
            startArrowhead=None, endArrowhead=None,
            strokeColor=_color(stroke, STROKE_COLORS), strokeWidth=stroke_width,
            **kw,
        )

    # -- grouping --------------------------------------------------------

    def group(self, elements):
        """Group elements so they move together when selected in Excalidraw."""
        gid = _id()
        for el in elements:
            el["groupIds"].append(gid)
        return gid

    # -- output ----------------------------------------------------------

    def to_dict(self, bg="#ffffff"):
        return {
            "type": "excalidraw",
            "version": 2,
            "source": "https://boardraw.app",
            "elements": self.elements,
            "appState": {"gridSize": None, "viewBackgroundColor": bg},
            "files": {},
        }

    def save(self, path, bg="#ffffff"):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(bg), f, ensure_ascii=False, indent=2)
        return path


# ---------------------------------------------------------------------------
# Layout helpers — optional, but they save you from hand-computing
# coordinates for the common cases.
# ---------------------------------------------------------------------------

def grid_positions(count, cols, x0=40, y0=40, cell_w=220, cell_h=140):
    """Yield (x, y) top-left positions for `count` cells in a grid."""
    positions = []
    for i in range(count):
        row, col = divmod(i, cols)
        positions.append((x0 + col * cell_w, y0 + row * cell_h))
    return positions


def vertical_flow_positions(count, x0=40, y0=40, w=180, h=80, gap=90):
    """Top-to-bottom positions for a linear flowchart, all same width."""
    return [(x0, y0 + i * (h + gap)) for i in range(count)]


def horizontal_flow_positions(count, x0=40, y0=40, w=180, h=80, gap=90):
    """Left-to-right positions for a linear flowchart, all same height."""
    return [(x0 + i * (w + gap), y0) for i in range(count)]

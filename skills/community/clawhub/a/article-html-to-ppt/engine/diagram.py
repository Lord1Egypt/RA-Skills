"""Diagram renderers (Phase 2b): diagram_ir -> render_plan elements.

Layout algorithms are migrated from v3's visual_narrative/renderers/* and
translated from python-pptx calls (inches) into builder-agnostic render_plan
elements (integer EMU). Nodes/edges describe structure only — positions,
colors and shapes are resolved here; the builder (PptxGenJS primary,
python-pptx fallback) only translates elements into its own API.

Families (v4.1):
  causal_chain         horizontal chain, arrow-linked, last node accent
  phase_roadmap        staggered horizontal phases (stair), arrow-linked
  layered_architecture vertical layers inside a boundary box, arrow-linked
  drill_down_stair     diagonal stair (x and y step), arrow-linked
  (others)             horizontal node strip — never blank, always ships
"""

from __future__ import annotations

from .layout import _frame, _para, _run, SlideLayout

EMU_PER_IN = 914400
EMU_PER_PT = 12700


def _color(ctx: SlideLayout, token: str, fallback: str) -> str:
    return ctx.style.resolve_color_ref(ctx.style.color(token, fallback))


def _node_text(node: dict, index: int) -> str:
    label = str(node.get("label") or f"节点 {index + 1}")
    role = str(node.get("role") or "")
    detail = str(node.get("detail") or "")
    parts = [p for p in (label, role, detail) if p]
    return "\n".join(parts)


def _primary_nodes(diagram_ir: dict, limit: int = 5) -> list[dict]:
    nodes = diagram_ir.get("nodes", [])
    primary = [n for n in nodes if n.get("priority") != "supporting"]
    if len(primary) < 3:
        primary = list(nodes)[:3]
    return primary[:limit]


def _shape(ctx: SlideLayout, frame: dict, *, shape: str, fill: str | None,
           stroke_color: str, text: str, text_color: str, size_cpt: int,
           weight: int = 600, radius: bool = True, stroke_w_pt: float = 0.8,
           align: str = "center") -> str:
    """Append one shape element and return its element_id."""
    eid = ctx.eid("diagram")
    element = {
        "element_id": eid, "type": "shape",
        "shape": "round_rect" if radius else "rect",
        "frame": _frame(frame["x"], frame["y"], frame["w"], frame["h"]),
        "stroke": {"color": stroke_color,
                   "width_emu": int(stroke_w_pt * EMU_PER_PT)},
        "paragraphs": [_para([_run(text, ctx.style, size_cpt, color=text_color,
                                   weight=weight)], align=align,
                             line_height_pct=120)],
        "editable": True, "semantic_role": "diagram_node",
    }
    if radius:
        element["corner_radius_emu"] = int(0.08 * EMU_PER_IN)
    if fill is None:
        element.pop("fill", None)
    else:
        element["fill"] = {"color": fill}
    ctx.elements.append(element)
    return eid


def _conn(ctx: SlideLayout, from_id: str, to_id: str, *, color: str,
          width_pt: float = 1.8, arrow: str = "end",
          from_side: str = "auto", to_side: str = "auto") -> None:
    ctx.elements.append({
        "element_id": ctx.eid("diagram-conn"), "type": "connector",
        "from_element": from_id, "to_element": to_id, "route": "straight",
        "from_side": from_side, "to_side": to_side,
        "stroke": {"color": color, "width_emu": int(width_pt * EMU_PER_PT)},
        "arrowhead": arrow,
    })


def _palette(ctx: SlideLayout) -> dict[str, str]:
    return {
        "accent": ctx.style.color("accent"),
        "primary": ctx.style.color("primary"),
        "surface": ctx.style.resolve_color_ref(
            ctx.style.card_tokens.get("default", {}).get("fill", "surface_1")),
        "background": ctx.style.color("background"),
        "text": ctx.style.color("text_primary"),
        "muted": ctx.style.color("text_secondary"),
        "border": ctx.style.color("border"),
    }


# ---- causal_chain -----------------------------------------------------------

def _causal_chain(ctx: SlideLayout, diagram_ir: dict, frame: dict) -> None:
    style = ctx.style
    nodes = _primary_nodes(diagram_ir, limit=5)
    c = _palette(ctx)
    x, y, w, h = frame["x"], frame["y"], frame["w"], frame["h"]
    gap = int(0.32 * EMU_PER_IN)
    node_w = (w - gap * (len(nodes) - 1)) // len(nodes)
    node_h = min(int(1.15 * EMU_PER_IN), h)
    top = y + (h - node_h) // 2
    size = style.size_cpt("body", "small")

    ids: list[str] = []
    for index, node in enumerate(nodes):
        last = index == len(nodes) - 1
        ids.append(_shape(
            ctx, _frame(x + index * (node_w + gap), top, node_w, node_h),
            shape="round_rect", fill=c["accent"] if last else c["surface"],
            stroke_color=c["border"], text=_node_text(node, index),
            text_color=c["background"] if last else c["text"], size_cpt=size))
    for a, b in zip(ids, ids[1:]):
        _conn(ctx, a, b, color=c["accent"],
              from_side="right", to_side="left")


# ---- phase_roadmap ----------------------------------------------------------

def _phase_roadmap(ctx: SlideLayout, diagram_ir: dict, frame: dict) -> None:
    style = ctx.style
    nodes = _primary_nodes(diagram_ir, limit=5)
    c = _palette(ctx)
    x, y, w, h = frame["x"], frame["y"], frame["w"], frame["h"]
    gap = int(0.28 * EMU_PER_IN)
    phase_w = (w - gap * (len(nodes) - 1)) // len(nodes)
    size = style.size_cpt("body", "small")

    ids: list[str] = []
    for index, node in enumerate(nodes):
        last = index == len(nodes) - 1
        stagger = int(index * 0.22 * EMU_PER_IN)
        ids.append(_shape(
            ctx, _frame(x + index * (phase_w + gap), y + stagger,
                        phase_w, int(1.45 * EMU_PER_IN)),
            shape="round_rect", fill=c["accent"] if last else c["surface"],
            stroke_color=c["primary"], text=_node_text(node, index),
            text_color=c["background"] if last else c["text"], size_cpt=size))
    for a, b in zip(ids, ids[1:]):
        _conn(ctx, a, b, color=c["accent"],
              from_side="right", to_side="left")


# ---- layered_architecture ---------------------------------------------------

def _layered_architecture(ctx: SlideLayout, diagram_ir: dict, frame: dict) -> None:
    style = ctx.style
    nodes = _primary_nodes(diagram_ir, limit=6)
    c = _palette(ctx)
    x, y, w, h = frame["x"], frame["y"], frame["w"], frame["h"]

    # Boundary box
    ctx.elements.append({
        "element_id": ctx.eid("diagram-boundary"), "type": "shape", "shape": "rect",
        "frame": _frame(x, y, w, h),
        "stroke": {"color": c["border"], "width_emu": int(0.7 * EMU_PER_PT)},
        "editable": True, "semantic_role": "diagram_boundary",
    })

    gap = int(0.16 * EMU_PER_IN)
    inner_y = y + int(0.38 * EMU_PER_IN)
    layer_h = (h - int(0.55 * EMU_PER_IN) - gap * (len(nodes) - 1)) // len(nodes)
    size = style.size_cpt("body", "small")

    ids: list[str] = []
    for index, node in enumerate(nodes):
        fill = c["surface"] if index % 2 == 0 else c["background"]
        stroke = c["primary"] if index < 2 else c["border"]
        ids.append(_shape(
            ctx, _frame(x + int(0.28 * EMU_PER_IN),
                        inner_y + index * (layer_h + gap),
                        w - int(0.56 * EMU_PER_IN), layer_h),
            shape="round_rect", fill=fill, stroke_color=stroke,
            text=_node_text(node, index), text_color=c["text"], size_cpt=size))
    for a, b in zip(ids, ids[1:]):
        _conn(ctx, a, b, color=c["accent"],
              from_side="bottom", to_side="top")


# ---- drill_down_stair -------------------------------------------------------

def _drill_down_stair(ctx: SlideLayout, diagram_ir: dict, frame: dict) -> None:
    style = ctx.style
    nodes = _primary_nodes(diagram_ir, limit=5)
    c = _palette(ctx)
    x, y, w, h = frame["x"], frame["y"], frame["w"], frame["h"]
    count = len(nodes)
    step_y = min(int(0.92 * EMU_PER_IN), (h - int(0.72 * EMU_PER_IN)) // max(count - 1, 1))
    step_x = min(int(1.05 * EMU_PER_IN), int(w * 0.09))
    size = style.size_cpt("body", "small")

    ids: list[str] = []
    for index, node in enumerate(nodes):
        last = index == count - 1
        ids.append(_shape(
            ctx, _frame(x + index * step_x, y + index * step_y,
                        max(int(2.2 * EMU_PER_IN),
                            w - int(2.0 * EMU_PER_IN) - index * int(step_x * 1.15)),
                        int(0.72 * EMU_PER_IN)),
            shape="round_rect", fill=c["accent"] if last else c["surface"],
            stroke_color=c["accent"], text=_node_text(node, index),
            text_color=c["background"] if last else c["text"], size_cpt=size))
    for a, b in zip(ids, ids[1:]):
        _conn(ctx, a, b, color=c["accent"],
              from_side="right", to_side="left")


# ---- heat_matrix ------------------------------------------------------------

def _format_value(value) -> str:
    number = float(value)
    return str(int(number)) if number.is_integer() else f"{number:g}"


def _heat_matrix(ctx: SlideLayout, diagram_ir: dict, frame: dict) -> None:
    style = ctx.style
    matrix = diagram_ir.get("matrix", {})
    rows = [str(r) for r in matrix.get("rows", [])]
    columns = [str(c) for c in matrix.get("columns", [])]
    values = matrix.get("values", [])
    if (not rows or not columns or not isinstance(values, list)
            or len(values) != len(rows)
            or any(not isinstance(r, list) or len(r) != len(columns) for r in values)):
        ctx.degrade("builder_downgrade", "heat_matrix_data_invalid")
        _node_strip(ctx, diagram_ir, frame)
        return

    c = _palette(ctx)
    x, y, w, h = frame["x"], frame["y"], frame["w"], frame["h"]

    numeric = [float(v) for row in values for v in row]
    minimum, maximum = min(numeric), max(numeric)
    spread = maximum - minimum
    highlighted = {tuple(cell) for cell in matrix.get("highlighted_cells", [])
                   if isinstance(cell, list) and len(cell) == 2}
    suffix = str(matrix.get("value_suffix") or "")

    label_w = int(1.35 * EMU_PER_IN)
    header_h = int(0.45 * EMU_PER_IN)
    legend_h = int(0.55 * EMU_PER_IN)
    grid_w = w - label_w
    grid_h = min(h - header_h - legend_h, int(3.5 * EMU_PER_IN))
    cell_w = grid_w // max(len(columns), 1)
    cell_h = grid_h // max(len(rows), 1)
    size = style.size_cpt("body", "small")

    # column headers
    for ci, column in enumerate(columns):
        ctx.elements.append({
            "element_id": ctx.eid("hm-col"), "type": "textbox",
            "frame": _frame(x + label_w + ci * cell_w, y, cell_w, header_h),
            "paragraphs": [_para([_run(column, style, size, color=c["muted"],
                                       weight=style.weight("semibold", 600))],
                                 align="center")],
            "valign": "middle", "editable": True, "semantic_role": "matrix_header",
        })

    # row labels + cells
    for ri, row_label in enumerate(rows):
        row_y = y + header_h + ri * cell_h
        ctx.elements.append({
            "element_id": ctx.eid("hm-row"), "type": "textbox",
            "frame": _frame(x, row_y, label_w - int(0.08 * EMU_PER_IN), cell_h),
            "paragraphs": [_para([_run(row_label, style, size, color=c["text"],
                                       weight=style.weight("semibold", 600))])],
            "valign": "middle", "editable": True, "semantic_role": "matrix_row_label",
        })
        for ci, value in enumerate(values[ri]):
            number = float(value)
            ratio = (number - minimum) / spread if spread else 0.5
            high = ratio >= 0.52
            hl = (ri, ci) in highlighted
            fill = c["accent"] if high else c["surface"]
            text_color = c["background"] if high else c["text"]
            ctx.elements.append({
                "element_id": ctx.eid("hm-cell"), "type": "shape", "shape": "rect",
                "frame": _frame(x + label_w + ci * cell_w + int(0.02 * EMU_PER_IN),
                                row_y + int(0.02 * EMU_PER_IN),
                                cell_w - int(0.04 * EMU_PER_IN),
                                cell_h - int(0.04 * EMU_PER_IN)),
                "fill": {"color": fill},
                "stroke": {"color": c["accent"] if hl else c["background"],
                           "width_emu": int((2.0 if hl else 0.7) * EMU_PER_PT)},
                "paragraphs": [_para([_run(f"{_format_value(value)}{suffix}", style,
                                           size, color=text_color,
                                           weight=style.weight("bold", 700)
                                           if hl else 400)], align="center")],
                "editable": True, "semantic_role": "matrix_cell",
            })

    # legend
    legend_y = y + header_h + grid_h + int(0.16 * EMU_PER_IN)
    for li, (label, fill) in enumerate((("低", c["surface"]), ("高", c["accent"]))):
        ctx.elements.append({
            "element_id": ctx.eid("hm-legend"), "type": "shape", "shape": "rect",
            "frame": _frame(x + label_w + li * int(0.62 * EMU_PER_IN), legend_y,
                            int(0.52 * EMU_PER_IN), int(0.28 * EMU_PER_IN)),
            "fill": {"color": fill},
            "stroke": {"color": c["border"], "width_emu": int(0.7 * EMU_PER_PT)},
            "paragraphs": [_para([_run(label, style, 900,
                                       color=c["background"] if li else c["text"])],
                                 align="center")],
            "editable": True, "semantic_role": "matrix_legend",
        })


# ---- fallback node strip ----------------------------------------------------

def _node_strip(ctx: SlideLayout, diagram_ir: dict, frame: dict) -> None:
    style = ctx.style
    nodes = diagram_ir.get("nodes", [])[:6]
    if not nodes:
        ctx.degrade("builder_downgrade", "diagram_nodes_empty")
        return
    c = _palette(ctx)
    x, y, w, h = frame["x"], frame["y"], frame["w"], frame["h"]
    gap = int(0.2 * EMU_PER_IN)
    node_w = (w - gap * (len(nodes) - 1)) // len(nodes)
    node_h = min(int(1.1 * EMU_PER_IN), h)
    top = y + (h - node_h) // 2
    size = style.size_cpt("body", "small")
    for index, node in enumerate(nodes):
        _shape(ctx, _frame(x + index * (node_w + gap), top, node_w, node_h),
               shape="round_rect", fill=c["surface"], stroke_color=c["border"],
               text=_node_text(node, index), text_color=c["text"], size_cpt=size)


# ---- chart ------------------------------------------------------------------

_CHART_TYPE_MAP = {"column": "column", "bar": "bar", "line": "line", "pie": "pie"}


def layout_chart(ctx: SlideLayout, chart: dict, frame: dict) -> None:
    """Emit a native chart element. Series colors resolve from the style's
    data_series palette; the builder renders the concrete chart."""
    style = ctx.style
    rp_type = _CHART_TYPE_MAP.get(chart["type"], "column")
    if chart["type"] not in _CHART_TYPE_MAP:
        # combo (column + line overlay) degrades to a column chart for now.
        ctx.degrade("chart_fallback", f"chart_{chart['type']}_column")

    palette = style.colors.get("data_series", [])
    if not palette:
        palette = [style.color("primary"), style.color("accent"),
                   style.color("positive"), style.color("text_secondary")]
    series = [{"name": s["name"], "values": s["values"],
               "color": palette[idx % len(palette)]}
              for idx, s in enumerate(chart["data"]["series"])]

    ctx.elements.append({
        "element_id": ctx.eid("chart"), "type": "chart",
        "frame": _frame(frame["x"], frame["y"], frame["w"], frame["h"]),
        "chart_type": rp_type,
        "categories": chart["data"]["categories"],
        "series": series, "legend": "bottom", "semantic_role": "chart",
    })


# ---- dispatcher -------------------------------------------------------------

_RENDERERS = {
    "causal_chain": _causal_chain,
    "phase_roadmap": _phase_roadmap,
    "layered_architecture": _layered_architecture,
    "drill_down_stair": _drill_down_stair,
    "heat_matrix": _heat_matrix,
    "interaction_storyboard": _node_strip,
    "product_ui_overview": _node_strip,
}


def layout_diagram(ctx: SlideLayout, diagram_ir: dict, frame: dict) -> None:
    dtype = diagram_ir.get("diagram_type", "")
    if dtype != "heat_matrix" and not diagram_ir.get("nodes"):
        ctx.degrade("builder_downgrade", "diagram_nodes_empty")
        _node_strip(ctx, diagram_ir, frame)
        return
    renderer = _RENDERERS.get(dtype)
    if renderer is None:
        ctx.degrade("builder_downgrade", f"diagram_{dtype}_unknown")
        renderer = _node_strip
    elif renderer is _node_strip:
        ctx.degrade("diagram_fallback", f"diagram_{dtype}_strip")
    renderer(ctx, diagram_ir, frame)

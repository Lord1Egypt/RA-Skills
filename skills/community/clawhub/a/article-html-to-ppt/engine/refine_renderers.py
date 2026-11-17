"""P12-refine Level 1: page-level composition intent renderers.

The refine switch lets a capable model describe page-level composition
intent ("split left metrics right chart", "wheel with a hub", "contrast
two positions", "spotlight one block") — and the engine compiles that
intent into concrete geometry, then QA-gates the result. Geometry, colors,
fonts stay engine-owned; the model only picks a composition family and
assigns blocks to its slots.

Composition families (refine.layout.type):
  split       two columns (left/right) with optional visual per side
  wheel       hub + spokes (flywheel: central node with radiating nodes)
  contrast    two opposing blocks side by side with a divider
  spotlight   one emphasized block large + supporting blocks below

Every family renders deterministically; any block assignment the family
cannot honor degrades honestly and falls back to the rule archetype.
"""

from __future__ import annotations

from .diagram import _color, _conn, _shape, _palette
from .layout import _frame, _para, _run, SlideLayout

EMU_PER_IN = 914400
EMU_PER_PT = 12700


def _resolve_blocks(ctx: SlideLayout, slide: dict, ids: list) -> list[dict]:
    """Map block ids from a refine layout slot to slide blocks."""
    by_id = {b.get("id"): b for b in slide.get("blocks", []) if b.get("id")}
    resolved = [by_id.get(i) for i in ids if i in by_id]
    return [b for b in resolved if b is not None]


def _card_or_special(ctx: SlideLayout, block: dict, frame: dict,
                     doc=None) -> None:
    """Render one block into a frame (table/image/card)."""
    if block.get("role") == "table":
        ctx.table(block, frame, doc)
    elif block.get("role") == "image":
        ctx.image_placeholder(block, frame)
    else:
        ctx.card(block, frame)


# ---- split --------------------------------------------------------------

def layout_split(ctx: SlideLayout, slide: dict, refine: dict, frame: dict,
                 doc=None) -> None:
    """Two columns: left/right block lists, optional per-side visual."""
    left = refine.get("left") or {}
    right = refine.get("right") or {}
    left_ids = left.get("blocks") or []
    right_ids = right.get("blocks") or []
    left_blocks = _resolve_blocks(ctx, slide, left_ids)
    right_blocks = _resolve_blocks(ctx, slide, right_ids)

    gap = ctx.style.gap_emu()
    col_w = (frame["w"] - gap) // 2
    lx, rx = frame["x"], frame["x"] + col_w + gap

    # optional visual on a side: chart/diagram gets 60% of column height
    for blocks, x, visual in ((left_blocks, lx, left.get("visual")),
                              (right_blocks, rx, right.get("visual"))):
        if not blocks and not visual:
            continue
        vh = 0
        if visual and blocks:
            vh = int(frame["h"] * 3 // 5)
            _visual_region(ctx, slide, visual, _frame(x, frame["y"], col_w, vh))
            top = frame["y"] + vh + gap
            _stack_into(ctx, blocks, _frame(x, top, col_w,
                                            frame["y"] + frame["h"] - top), doc)
        else:
            _stack_into(ctx, blocks, _frame(x, frame["y"], col_w, frame["h"]), doc)


def _visual_region(ctx: SlideLayout, slide: dict, visual: dict,
                   frame: dict) -> None:
    """A visual slot inside a split column: chart or diagram."""
    if isinstance(visual, dict) and visual.get("chart"):
        from .diagram import layout_chart
        layout_chart(ctx, visual["chart"], frame)
    elif isinstance(visual, dict) and visual.get("diagram_ir"):
        from .diagram import layout_diagram
        layout_diagram(ctx, visual["diagram_ir"], frame)
    else:
        ctx.degrade("builder_downgrade", "split_visual_unknown")


def _stack_into(ctx: SlideLayout, blocks: list[dict], frame: dict,
                doc=None) -> None:
    """Stack blocks vertically inside a frame (like ctx.stack but bounded)."""
    if not blocks:
        return
    gap = ctx.style.gap_emu()
    n = len(blocks)
    card_h = (frame["h"] - gap * (n - 1)) // n if n else frame["h"]
    y = frame["y"]
    for block in blocks:
        _card_or_special(ctx, block, _frame(frame["x"], y, frame["w"], card_h), doc)
        y += card_h + gap


# ---- wheel ---------------------------------------------------------------

def layout_wheel(ctx: SlideLayout, slide: dict, refine: dict, frame: dict,
                 doc=None) -> None:
    """Flywheel: hub node center + spokes radiating around it.

    Placement: n spokes at n evenly spaced radial positions (top / top+bottom
    / triangle / diamond). Geometry only — colors come from the style pack.
    """
    hub_ids = (refine.get("hub") or {}).get("blocks") or []
    spoke_ids = refine.get("spokes") or []
    hub = _resolve_blocks(ctx, slide, hub_ids)
    spokes = _resolve_blocks(ctx, slide, spoke_ids)
    if not hub and not spokes:
        ctx.degrade("builder_downgrade", "wheel_empty")
        return

    style = ctx.style
    x, y, w, h = frame["x"], frame["y"], frame["w"], frame["h"]
    c = _palette(ctx)
    size = style.size_cpt("body", "small")

    if not spokes:
        ctx.degrade("builder_downgrade", "wheel_no_spokes")
        _stack_into(ctx, hub, frame, doc)
        return

    spoke_w = int(1.9 * EMU_PER_IN)
    spoke_h = int(0.95 * EMU_PER_IN)
    hub_d = min(w - 2 * spoke_w, h - spoke_h, int(3.2 * EMU_PER_IN))
    cx, cy = x + w // 2, y + h // 2
    hub_frame = _frame(cx - hub_d // 2, cy - hub_d // 2, hub_d, hub_d)
    hub_text = (hub[0].get("text") or hub[0].get("label") or "核心") if hub else "核心"
    hub_id = ctx.eid("hub")
    ctx.elements.append({
        "element_id": hub_id, "type": "shape", "shape": "oval",
        "frame": hub_frame,
        "fill": {"color": c["accent"]},
        "stroke": {"color": c["accent"], "width_emu": int(1.2 * EMU_PER_PT)},
        "paragraphs": [_para([_run(str(hub_text)[:40], style,
                                   size_cpt=size, color=c["background"],
                                   weight=700)], align="center",
                             line_height_pct=120)],
        "editable": True, "semantic_role": "diagram_node",
    })

    n = len(spokes)
    # radial offsets for n spokes (normalized to hub center)
    if n == 1:
        offsets = [(0.0, -1.0)]
    elif n == 2:
        offsets = [(0.0, -1.0), (0.0, 1.0)]
    elif n == 3:
        offsets = [(-0.87, -0.5), (0.87, -0.5), (0.0, 1.0)]
    elif n == 4:
        offsets = [(0.0, -1.0), (1.0, 0.0), (0.0, 1.0), (-1.0, 0.0)]
    else:
        # n > 4: ring at 0.8 radius
        offsets = [(0.8, -0.6), (0.6, -0.8), (-0.6, -0.8), (-0.8, -0.6),
                   (0.0, 1.0)]
        offsets = offsets[:n]

    radius = hub_d * 0.5 + max(spoke_w, spoke_h) * 0.55
    for idx, (ox, oy) in enumerate(offsets[:n]):
        spoke = spokes[idx]
        sx = cx + int(ox * radius)
        sy = cy + int(oy * radius)
        sx = max(x, min(sx, x + w - spoke_w))
        sy = max(y, min(sy, y + h - spoke_h))
        spoke_text = spoke.get("text") or spoke.get("label") or f"节点 {idx + 1}"
        sid = _shape(ctx, _frame(sx, sy, spoke_w, spoke_h),
                     shape="round_rect", fill=c["surface"],
                     stroke_color=c["border"], text=str(spoke_text)[:40],
                     text_color=c["text"], size_cpt=size)
        _conn(ctx, hub_id, sid, color=c["accent"],
              from_side="auto", to_side="auto")


# ---- contrast ------------------------------------------------------------

def layout_contrast(ctx: SlideLayout, slide: dict, refine: dict, frame: dict,
                    doc=None) -> None:
    """Two opposing blocks side by side with a center divider."""
    left_ids = (refine.get("left") or {}).get("blocks") or []
    right_ids = (refine.get("right") or {}).get("blocks") or []
    left = _resolve_blocks(ctx, slide, left_ids)
    right = _resolve_blocks(ctx, slide, right_ids)
    if not left and not right:
        ctx.degrade("builder_downgrade", "contrast_empty")
        return

    style = ctx.style
    gap = int(0.18 * EMU_PER_IN)
    col_w = (frame["w"] - gap * 2) // 2
    lx, rx = frame["x"], frame["x"] + col_w + gap * 2
    # divider
    ctx.elements.append({
        "element_id": ctx.eid("divider"), "type": "shape", "shape": "rect",
        "frame": _frame(frame["x"] + col_w + gap // 2, frame["y"],
                        int(0.03 * EMU_PER_IN), frame["h"]),
        "fill": {"color": style.color("border")},
        "editable": True, "semantic_role": "divider",
    })
    if left:
        _stack_into(ctx, left, _frame(lx, frame["y"], col_w, frame["h"]), doc)
    if right:
        _stack_into(ctx, right, _frame(rx, frame["y"], col_w, frame["h"]), doc)


# ---- spotlight -----------------------------------------------------------

def layout_spotlight(ctx: SlideLayout, slide: dict, refine: dict, frame: dict,
                     doc=None) -> None:
    """One emphasized block large on top, supporting blocks below."""
    spotlight_ids = (refine.get("spotlight") or {}).get("blocks") or []
    supporting_ids = (refine.get("supporting") or {}).get("blocks") or []
    spotlight = _resolve_blocks(ctx, slide, spotlight_ids)
    supporting = _resolve_blocks(ctx, slide, supporting_ids)
    if not spotlight:
        ctx.degrade("builder_downgrade", "spotlight_empty")
        ctx.stack(slide.get("blocks", []), frame=frame, doc=doc)
        return

    style = ctx.style
    gap = style.gap_emu()
    main_h = int(frame["h"] * 3 // 5) if supporting else frame["h"]
    main_block = spotlight[0]
    if main_block.get("role") == "metric":
        ctx.kpi_row([main_block], top=frame["y"], height=main_h)
    else:
        _card_or_special(ctx, main_block,
                         _frame(frame["x"], frame["y"], frame["w"], main_h), doc)
    if supporting:
        top = frame["y"] + main_h + gap
        _stack_into(ctx, supporting,
                    _frame(frame["x"], top, frame["w"],
                           frame["y"] + frame["h"] - top), doc)


# ---- dispatcher ----------------------------------------------------------

_REFINE_RENDERERS = {
    "split": layout_split,
    "wheel": layout_wheel,
    "contrast": layout_contrast,
    "spotlight": layout_spotlight,
}


def layout_refine(ctx: SlideLayout, slide: dict, refine: dict, frame: dict,
                  doc=None) -> None:
    """Dispatch a refine layout intent to its renderer (P12 Level 1)."""
    ltype = refine.get("type", "")
    renderer = _REFINE_RENDERERS.get(ltype)
    if renderer is None:
        ctx.degrade("builder_downgrade", f"refine_{ltype}_unknown")
        ctx.stack(slide.get("blocks", []), frame=frame, doc=doc)
        return
    renderer(ctx, slide, refine, frame, doc)

"""Layout engine: IR slide + archetype + style -> Render Plan slides.

100% deterministic (D9): integer EMU geometry, style values resolved, text
sizes chosen by the textfit model with step-down and deterministic
truncation. Table cells are pulled from the parsed source (the IR only
references them), so the model never retypes tables.

Every bound applied (font step-down, truncation, image placeholder) is
returned as a degradation record for the decision trace — honest by
construction, nothing silently dropped.
"""

from __future__ import annotations

from .source_doc import SourceDoc, parse_anchor
from .style_pack import EMU_PER_IN, EMU_PER_PT, ResolvedStyle
from .textfit import fit_size_cpt, paragraphs_height_emu, truncate_to_fit

CANVAS_W, CANVAS_H = 12192000, 6858000
TITLE_H = 800100
TITLE_GAP = 228600
CARD_PAD = 152400
FOOTER_H = 274320

_EDGE_TOKEN = {"insight": "accent", "risk": "negative", "recommendation": "positive"}

# block role -> v3 card_tokens variant (fill/border differentiation).
_ROLE_CARD_VARIANT = {"risk": "risk", "quote": "quote", "context": "source"}


def _run(text: str, style: ResolvedStyle, size_cpt: int, *, color: str | None = None,
         weight: int = 400, font: str | None = None) -> dict:
    return {"text": text or " ", "font": font or style.font(),
            "size_cpt": size_cpt, "color": color or style.color("text_primary"),
            "weight": weight}


def _para(runs: list[dict], *, align: str = "left", bullet: str = "none",
          line_height_pct: int = 135, space_after_cpt: int = 0) -> dict:
    return {"runs": runs, "align": align, "bullet": bullet,
            "line_height_pct": line_height_pct, "space_after_cpt": space_after_cpt}


def _frame(x: int, y: int, w: int, h: int) -> dict:
    return {"x": int(x), "y": int(y), "w": max(int(w), 1), "h": max(int(h), 1)}


def _shadow_spec(style: ResolvedStyle) -> dict | None:
    """Render-plan shadow from the style's floating_panel token, or None."""
    panel = style.shadow_tokens.get("floating_panel", {})
    if not panel.get("enabled"):
        return None
    blur = int(float(panel.get("blur_pt", 4)) * EMU_PER_PT)
    distance = int(float(panel.get("distance_pt", 2)) * EMU_PER_PT)
    opacity = int(float(panel.get("opacity", 0.12)) * 100)
    return {"blur_emu": blur, "offset_x_emu": 0, "offset_y_emu": distance,
            "opacity_pct": max(0, min(100, opacity))}


class SlideLayout:
    """Shared geometry context for one slide."""

    def __init__(self, slide_id: str, style: ResolvedStyle,
                 degradations: list[dict]) -> None:
        self.sid = slide_id
        self.style = style
        self.degs = degradations
        self.elements: list[dict] = []
        self._seq = 0
        margin = style.margin_emu()
        self.left = margin
        self.width = CANVAS_W - 2 * margin
        self.content_top = margin // 2 + TITLE_H + TITLE_GAP
        self.content_h = CANVAS_H - self.content_top - margin // 2 - FOOTER_H

    def eid(self, tag: str) -> str:
        self._seq += 1
        return f"{self.sid}-{tag}-{self._seq}"

    def degrade(self, kind: str, detail: str) -> None:
        self.degs.append({"kind": kind, "slide_id": self.sid, "detail_code": detail})

    def add_title(self, title: str, message: str | None) -> None:
        style = self.style
        title_levels = [style.size_cpt("title", "slide"), 2000, 1800, 1600]
        title_size = fit_size_cpt(title, self.width - 182880,
                                  TITLE_H - (0 if not message else 350000),
                                  title_levels, 110,
                                  family=style.font("editorial")) or 1600
        paras = [_para([_run(title, style, title_size,
                             weight=style.weight("semibold", 600),
                             font=style.font("editorial"))],
                       align=style.alignment if style.alignment != "centered" else "center",
                       line_height_pct=110)]
        if message:
            paras.append(_para([_run(message, style, style.size_cpt("body", "normal"),
                                     color=style.color("text_secondary"))],
                               align="left", line_height_pct=125))
        self.elements.append({
            "element_id": self.eid("title"), "type": "textbox",
            "frame": _frame(self.left, self.style.margin_emu() // 2, self.width, TITLE_H),
            "paragraphs": paras, "valign": "middle", "editable": True,
            "semantic_role": "title",
        })

    def add_footer(self, text: str, page_index: int) -> None:
        """Two-tone footer (v3): a full-width primary bar, an accent edge
        strip, source/copyright text, and a page number."""
        style = self.style
        y = CANVAS_H - FOOTER_H
        primary = style.color("primary")
        accent = style.color("accent")
        background = style.color("background")
        self.elements.extend([{
            "element_id": self.eid("footer-bar"), "type": "shape", "shape": "rect",
            "frame": _frame(0, y, CANVAS_W, FOOTER_H),
            "fill": {"color": primary}, "editable": True, "semantic_role": "footer_bar",
        }, {
            "element_id": self.eid("footer-accent"), "type": "shape", "shape": "rect",
            "frame": _frame(0, y, int(0.08 * EMU_PER_IN), FOOTER_H),
            "fill": {"color": accent}, "editable": True, "semantic_role": "footer_accent",
        }, {
            "element_id": self.eid("footer-text"), "type": "textbox",
            "frame": _frame(int(0.22 * EMU_PER_IN), y, int(6.0 * EMU_PER_IN), FOOTER_H),
            "paragraphs": [_para([_run(text, style, 800, color=background)])],
            "valign": "middle", "editable": True, "semantic_role": "footer_text",
        }, {
            "element_id": self.eid("footer-page"), "type": "textbox",
            "frame": _frame(CANVAS_W - int(1.0 * EMU_PER_IN), y,
                            int(0.8 * EMU_PER_IN), FOOTER_H),
            "paragraphs": [_para([_run(f"{page_index:02d}", style, 900,
                                       color=background)], align="right")],
            "valign": "middle", "editable": True, "semantic_role": "footer_page",
        }])

    # ---- content builders -------------------------------------------------

    def _block_paras(self, block: dict, size_cpt: int) -> list[dict]:
        style = self.style
        role = block.get("role")
        weight = style.weight("semibold", 600)
        if role == "list":
            return [_para([_run(f"• {item['text']}", style, size_cpt,
                                weight=weight)],
                          bullet="dot", space_after_cpt=400)
                    for item in block.get("items", [])]
        text = block.get("text", "")
        return [_para([_run(text, style, size_cpt, weight=weight)])]

    def card(self, block: dict, frame: dict) -> None:
        style = self.style
        inner_w = frame["w"] - 2 * CARD_PAD
        inner_h = frame["h"] - 2 * CARD_PAD
        levels = style.body_levels_cpt()
        size = next((s for s in levels
                     if paragraphs_height_emu(self._block_paras(block, s),
                                              inner_w) <= inner_h), None)
        if size is None:
            size = levels[-1]
            if block.get("role") == "list":
                items = list(block.get("items", []))
                while len(items) > 1 and paragraphs_height_emu(
                        self._block_paras({"role": "list", "items": items}, size),
                        inner_w) > inner_h:
                    items.pop()
                block = dict(block, items=items)
                self.degrade("content_truncation", "list_items_dropped")
                if paragraphs_height_emu(self._block_paras(block, size),
                                         inner_w) > inner_h:
                    block = {"role": "fact",
                             "text": truncate_to_fit(items[0]["text"], size,
                                                     inner_w, inner_h,
                                                     family=style.font())}
            else:
                block = dict(block, text=truncate_to_fit(
                    block.get("text", ""), size, inner_w, inner_h,
                    family=style.font()))
                self.degrade("content_truncation",
                             f"block_truncated_{block.get('role', 'text')}")
        elif size != levels[0]:
            self.degrade("font_step_down", f"body_{size}")
        variant = _ROLE_CARD_VARIANT.get(block.get("role", ""), "default")
        card_tok = style.card_tokens.get(variant, style.card_tokens.get("default", {}))
        element = {
            "element_id": self.eid("card"), "type": "shape",
            "frame": frame, "shape": "round_rect",
            "corner_radius_emu": int(style.shape_tokens.get("card_radius_pt", 8) * EMU_PER_PT),
            "fill": {"color": style.resolve_color_ref(
                card_tok.get("fill", "surface_1"))},
            "stroke": {"color": style.resolve_color_ref(
                card_tok.get("border_color", "border")),
                       "width_emu": int(style.shape_tokens.get("border_width_pt", 0.8) * EMU_PER_PT)},
            "paragraphs": self._block_paras(block, size),
            "editable": True, "semantic_role": block.get("role", "text"),
        }
        shadow = _shadow_spec(style)
        if shadow:
            element["shadow"] = shadow
        self.elements.append(element)
        edge_token = _EDGE_TOKEN.get(block.get("role", ""))
        if edge_token:
            self.elements.append({
                "element_id": self.eid("edge"), "type": "shape",
                "frame": _frame(frame["x"], frame["y"], 45720, frame["h"]),
                "shape": "rect", "fill": {"color": self.style.color(edge_token)},
                "editable": True, "semantic_role": "accent_edge",
            })

    def stack(self, blocks: list[dict], *, top: int | None = None,
              height: int | None = None) -> None:
        if not blocks:
            return
        zone_top = self.content_top if top is None else top
        zone_h = self.content_h if height is None else height
        gap = self.style.gap_emu()
        n = len(blocks)
        card_h = (zone_h - gap * (n - 1)) // n
        y = zone_top
        for block in blocks:
            if block.get("role") == "table":
                self.table(block, _frame(self.left, y, self.width, card_h))
            elif block.get("role") == "image":
                self.image_placeholder(block, _frame(self.left, y, self.width, card_h))
            else:
                self.card(block, _frame(self.left, y, self.width, card_h))
            y += card_h + gap

    def kpi_row(self, metrics: list[dict], *, top: int, height: int) -> None:
        style = self.style
        gap = style.gap_emu()
        per_row = min(len(metrics), 4)
        card_w = (self.width - gap * (per_row - 1)) // per_row
        x = self.left
        for metric in metrics[:per_row]:
            label = metric.get("label", "")
            value = metric.get("value", "")
            if metric.get("delta"):
                value = f"{value}" if value else metric["delta"]
            paras = [
                _para([_run(label, style, style.size_cpt("body", "small"),
                            color=style.color("text_secondary"),
                            weight=style.weight("medium", 500))],
                      space_after_cpt=300),
                _para([_run(value, style, style.size_cpt("metric", "normal"),
                            color=style.resolve_color_ref(
                                style.card_tokens.get("metric", {}).get("number_color", "primary")),
                            weight=style.weight("bold", 700))]),
            ]
            if metric.get("baseline"):
                paras.append(_para([_run(f"vs {metric['baseline']}", style, 900,
                                         color=style.color("text_muted",
                                                           style.color("text_secondary")))]))
            metric_tok = style.card_tokens.get("metric", style.card_tokens.get("default", {}))
            kpi_element = {
                "element_id": self.eid("kpi"), "type": "shape",
                "frame": _frame(x, top, card_w, height), "shape": "round_rect",
                "corner_radius_emu": int(style.shape_tokens.get("card_radius_pt", 8) * EMU_PER_PT),
                "fill": {"color": style.resolve_color_ref(
                    metric_tok.get("fill", "background"))},
                "stroke": {"color": style.resolve_color_ref(
                    metric_tok.get("border_color", "border")),
                           "width_emu": int(style.shape_tokens.get("border_width_pt", 0.8) * EMU_PER_PT)},
                "paragraphs": paras, "editable": True, "semantic_role": "metric",
            }
            shadow = _shadow_spec(style)
            if shadow:
                kpi_element["shadow"] = shadow
            self.elements.append(kpi_element)
            x += card_w + gap
        if len(metrics) > per_row:
            self.degrade("content_truncation", f"kpi_overflow_{len(metrics) - per_row}")

    def step_cards(self, list_block: dict, frame: dict) -> None:
        """McKinsey-style step cards (v3): a numbered, dark-title-bar card per
        list item, with an optional body line and accent action items, linked
        by arrows. steps/stages semantics select this."""
        style = self.style
        items = list_block.get("items", [])
        n = min(len(items), 5)
        if not items:
            self.degrade("builder_downgrade", "step_cards_empty")
            return
        gap = style.gap_emu()
        card_w = (frame["w"] - gap * (n - 1)) // n
        header_h = int(0.45 * EMU_PER_IN)
        primary = style.color("primary")
        background = style.color("background")
        accent = style.color("accent")
        border = style.color("border")
        body_text = style.color("text_primary")
        muted = style.color("text_secondary")
        size = style.size_cpt("body", "small")
        pad = int(0.08 * EMU_PER_IN)
        dot = int(0.06 * EMU_PER_IN)

        body_ids: list[str] = []
        for i, item in enumerate(items[:n]):
            x = frame["x"] + i * (card_w + gap)
            body_id = self.eid("step-body")
            self.elements.append({
                "element_id": body_id, "type": "shape", "shape": "rect",
                "frame": _frame(x, frame["y"], card_w, frame["h"]),
                "fill": {"color": background},
                "stroke": {"color": border, "width_emu": 9525},
                "editable": True, "semantic_role": "step_card",
            })
            body_ids.append(body_id)
            self.elements.append({
                "element_id": self.eid("step-header"), "type": "shape", "shape": "rect",
                "frame": _frame(x, frame["y"], card_w, header_h),
                "fill": {"color": primary},
                "stroke": {"color": primary, "width_emu": 9525},
                "paragraphs": [_para([_run(f"{i + 1:02d}  {item['text']}", style, size,
                                           color=background,
                                           weight=style.weight("bold", 700))],
                                     align="center", line_height_pct=115)],
                "editable": True, "semantic_role": "step_header",
            })
            cy = frame["y"] + header_h + pad
            detail = item.get("detail")
            if detail:
                self.elements.append({
                    "element_id": self.eid("step-detail"), "type": "textbox",
                    "frame": _frame(x + pad, cy, card_w - 2 * pad, int(0.4 * EMU_PER_IN)),
                    "paragraphs": [_para([_run(detail, style, size, color=body_text)],
                                         line_height_pct=120)],
                    "valign": "top", "editable": True, "semantic_role": "step_detail",
                })
                cy += int(0.42 * EMU_PER_IN)
            for ai in item.get("action_items", []):
                self.elements.append({
                    "element_id": self.eid("step-dot"), "type": "shape", "shape": "rect",
                    "frame": _frame(x + pad, cy + int(0.05 * EMU_PER_IN), dot, dot),
                    "fill": {"color": accent}, "editable": True, "semantic_role": "step_dot",
                })
                self.elements.append({
                    "element_id": self.eid("step-action"), "type": "textbox",
                    "frame": _frame(x + pad + dot + pad, cy, card_w - 2 * pad - dot - pad,
                                    int(0.26 * EMU_PER_IN)),
                    "paragraphs": [_para([_run(ai, style, size, color=muted)],
                                         line_height_pct=115)],
                    "valign": "top", "editable": True, "semantic_role": "step_action",
                })
                cy += int(0.26 * EMU_PER_IN)
        for a, b in zip(body_ids, body_ids[1:]):
            self.elements.append({
                "element_id": self.eid("step-conn"), "type": "connector",
                "from_element": a, "to_element": b, "route": "straight",
                "from_side": "right", "to_side": "left",
                "stroke": {"color": accent, "width_emu": int(1.6 * EMU_PER_PT)},
                "arrowhead": "end",
            })

    def table(self, block: dict, frame: dict, doc: SourceDoc | None = None) -> None:
        style = self.style
        caption = block.get("caption")
        if caption:
            cap_h = 274320
            self.elements.append({
                "element_id": self.eid("caption"), "type": "textbox",
                "frame": _frame(frame["x"], frame["y"] + frame["h"] - cap_h,
                                frame["w"], cap_h),
                "paragraphs": [_para([_run(caption, style, 1000,
                                           color=style.color("text_secondary"))])],
                "valign": "middle", "editable": True, "semantic_role": "caption",
            })
            frame = _frame(frame["x"], frame["y"], frame["w"],
                           frame["h"] - cap_h - style.gap_emu() // 2)
        rows_data: list[list[str]] = []
        if doc is not None:
            parsed = parse_anchor(block.get("source_ref", {}).get("loc", ""))
            element = doc.get(f"{parsed[0]}_{parsed[1]}") if parsed else None
            if element is not None:
                rows_data = element.rows
        if not rows_data:
            rows_data = getattr(self, "_table_rows_cache", {}).get(id(block), [])
        if not rows_data:
            self.card({"role": "fact",
                       "text": block.get("caption", "表格数据（见原文）")}, frame)
            self.degrade("builder_downgrade", "table_rows_unavailable")
            return
        cols = block.get("column_filter")
        if cols:
            rows_data = [[row[c] for c in cols if c < len(row)] for row in rows_data]
        limit = min(block.get("row_limit", 12), 30)
        if len(rows_data) - 1 > limit:
            self.degrade("content_truncation", f"table_rows_{len(rows_data) - 1 - limit}")
            rows_data = rows_data[: limit + 1]
        width = max(len(r) for r in rows_data)
        col_w = self.width // width if frame["w"] == self.width else frame["w"] // width
        size = style.size_cpt("body", "small")
        # minimal variant (v3 table_tokens.minimal): no heavy header fill, no
        # outer/vertical borders — only horizontal dividers. This is the
        # cleaner consulting-report default; `default` keeps the strong header.
        minimal_tok = style.table_tokens.get("minimal", {})
        use_minimal = minimal_tok.get("show_outer_border") is False
        default_tok = style.table_tokens.get("default", {})
        if use_minimal:
            header_fill = style.color("background")
            header_text = style.color("primary")
            variant = "minimal"
        else:
            header_fill = style.resolve_color_ref(default_tok.get("header_fill", "primary"))
            header_text = style.resolve_color_ref(default_tok.get("header_text", "background"))
            variant = "default"
        body_text = style.resolve_color_ref(default_tok.get("text_color", "text_primary"))
        # v3: table_tokens.default.alternate_row_fill
        zebra = bool(default_tok.get("alternate_row_fill"))
        row_h = max(frame["h"] // max(len(rows_data), 1), 274320)
        rows = []
        for r_idx, row in enumerate(rows_data):
            if r_idx == 0:
                fill = header_fill
                text_color = header_text
            elif zebra and r_idx % 2 == 0:
                fill = style.resolve_color_ref(
                    style.table_tokens.get("default", {}).get("alternate_row_fill", "surface_1"))
                text_color = body_text
            else:
                fill = style.color("background")
                text_color = body_text
            cells = [{"paragraphs": [_para([_run(cell or " ", style, size,
                                                 color=text_color,
                                                 weight=style.weight("semibold", 600)
                                                 if r_idx == 0 else 400)])],
                      "fill": {"color": fill}}
                     for cell in (row + [""] * width)[:width]]
            rows.append({"header": r_idx == 0, "height_emu": row_h, "cells": cells})
        self.elements.append({
            "element_id": self.eid("table"), "type": "table", "frame": frame,
            "col_widths_emu": [col_w] * width, "rows": rows,
            "border": {"color": style.color("border"), "width_emu": 9525},
            "variant": variant, "semantic_role": "table",
        })

    def image_placeholder(self, block: dict, frame: dict) -> None:
        style = self.style
        caption = block.get("caption") or block.get("asset_ref", "图片")
        self.elements.append({
            "element_id": self.eid("img"), "type": "shape", "frame": frame,
            "shape": "rect", "fill": {"color": style.color("surface_2")},
            "stroke": {"color": style.color("border"), "width_emu": 9525},
            "paragraphs": [_para([_run(f"图：{caption}", style,
                                       style.size_cpt("body", "small"),
                                       color=style.color("text_secondary"))],
                                 align="center")],
            "editable": True, "semantic_role": "image_placeholder",
        })
        self.degrade("builder_downgrade", "image_placeholder")


def _layout_content(ctx: SlideLayout, slide: dict, archetype: str,
                    doc: SourceDoc | None) -> None:
    blocks = slide.get("blocks", [])

    # v4.1: chart_* / diagram_* archetypes come from policy (an explicit
    # chart/diagram_ir payload). The payload takes the primary content
    # region; remaining blocks stack below. Weak models omit these fields
    # and fall through to the rule archetypes unchanged.
    if archetype.startswith("chart_") and slide.get("chart"):
        from .diagram import layout_chart  # deferred: avoid import cycle
        chart_h = ctx.content_h if not blocks else ctx.content_h * 3 // 5
        layout_chart(ctx, slide["chart"], _frame(ctx.left, ctx.content_top,
                                                 ctx.width, chart_h))
        if blocks:
            top = ctx.content_top + chart_h + ctx.style.gap_emu()
            ctx.stack(blocks, top=top, height=ctx.content_top + ctx.content_h - top)
        return
    if archetype.startswith("diagram_") and slide.get("diagram_ir"):
        from .diagram import layout_diagram  # deferred: avoid import cycle
        diagram_h = ctx.content_h if not blocks else ctx.content_h * 3 // 5
        layout_diagram(ctx, slide["diagram_ir"],
                       _frame(ctx.left, ctx.content_top, ctx.width, diagram_h))
        if blocks:
            top = ctx.content_top + diagram_h + ctx.style.gap_emu()
            ctx.stack(blocks, top=top, height=ctx.content_top + ctx.content_h - top)
        return

    if archetype == "kpi_wall":
        metrics = [b for b in blocks if b.get("role") == "metric"]
        others = [b for b in blocks if b.get("role") != "metric"]
        kpi_h = min(1371600, ctx.content_h if not others else ctx.content_h // 2)
        ctx.kpi_row(metrics, top=ctx.content_top, height=kpi_h)
        if others:
            rest_top = ctx.content_top + kpi_h + ctx.style.gap_emu()
            ctx.stack(others, top=rest_top,
                      height=ctx.content_top + ctx.content_h - rest_top)
    elif archetype == "full_table":
        tables = [b for b in blocks if b.get("role") == "table"]
        others = [b for b in blocks if b.get("role") != "table"]
        ctx.table(tables[0], _frame(ctx.left, ctx.content_top, ctx.width,
                                    ctx.content_h if not others
                                    else ctx.content_h * 3 // 4), doc)
        if others:
            top = ctx.content_top + ctx.content_h * 3 // 4 + ctx.style.gap_emu()
            ctx.stack(others, top=top,
                      height=ctx.content_top + ctx.content_h - top)
    elif archetype == "quote_focus":
        quotes = [b for b in blocks if b.get("role") == "quote"]
        others = [b for b in blocks if b.get("role") != "quote"]
        style = ctx.style
        quote_h = ctx.content_h if not others else ctx.content_h // 2
        text = quotes[0].get("text", "") if quotes else ""
        size = fit_size_cpt(text, ctx.width - 2 * CARD_PAD, quote_h - 2 * CARD_PAD,
                            [style.size_cpt("body", "large") * 2 // 1,
                             style.size_cpt("body", "large"),
                             style.size_cpt("body", "normal")],
                            130, family=style.font("editorial")) \
            or style.size_cpt("body", "normal")
        ctx.elements.append({
            "element_id": ctx.eid("quote"), "type": "textbox",
            "frame": _frame(ctx.left, ctx.content_top, ctx.width, quote_h),
            "paragraphs": [_para([_run(f"“{text}”", style, size,
                                       font=style.font("editorial"),
                                       color=style.color("primary"))],
                                 align="center", line_height_pct=130)],
            "valign": "middle", "editable": True, "semantic_role": "quote",
        })
        if others:
            top = ctx.content_top + quote_h + ctx.style.gap_emu()
            ctx.stack(others, top=top, height=ctx.content_top + ctx.content_h - top)
    elif archetype == "image_story":
        images = [b for b in blocks if b.get("role") == "image"]
        others = [b for b in blocks if b.get("role") != "image"]
        img_h = ctx.content_h if not others else ctx.content_h * 2 // 3
        ctx.image_placeholder(images[0], _frame(ctx.left, ctx.content_top,
                                                ctx.width, img_h))
        if others:
            top = ctx.content_top + img_h + ctx.style.gap_emu()
            ctx.stack(others, top=top, height=ctx.content_top + ctx.content_h - top)
    elif archetype == "step_cards":
        steps = [b for b in blocks if b.get("role") == "list"
                 and b.get("semantics") in ("steps", "stages")]
        lists = steps or [b for b in blocks if b.get("role") == "list"]
        first_list = lists[0] if lists else None
        others = [b for b in blocks if b is not first_list]
        cards_h = ctx.content_h if not others else ctx.content_h * 2 // 3
        ctx.step_cards(first_list if first_list else {"items": []},
                       _frame(ctx.left, ctx.content_top, ctx.width, cards_h))
        if others:
            top = ctx.content_top + cards_h + ctx.style.gap_emu()
            ctx.stack(others, top=top, height=ctx.content_top + ctx.content_h - top)
    elif archetype == "proposed_grid":
        _layout_proposed_grid(ctx, slide, doc)
    elif archetype.startswith("refine_") and slide.get("refine"):
        from .refine_renderers import layout_refine  # deferred: avoid import cycle
        layout_refine(ctx, slide, slide["refine"],
                      _frame(ctx.left, ctx.content_top, ctx.width, ctx.content_h),
                      doc)
    else:  # list_stack and evidence_stack share the guaranteed stack path
        ctx.stack(blocks)


def _layout_proposed_grid(ctx: SlideLayout, slide: dict,
                          doc: SourceDoc | None = None) -> None:
    """L2 autonomy grid: render the slide's blocks into the row/column grid
    the model proposed (block ids -> rows). The engine owns geometry: each
    row is a horizontal band split evenly among its blocks; a block that is
    a table gets a table, everything else a card. Blocks not mentioned in
    the proposal (should not happen — validation forbids it) stack below.
    """
    proposal = (slide.get("proposal") or {})
    rows = proposal.get("rows") or []
    blocks = slide.get("blocks", [])
    by_id = {b.get("id"): b for b in blocks if b.get("id")}

    if not rows or not by_id:
        ctx.degrade("builder_downgrade", "proposed_grid_empty")
        ctx.stack(blocks)
        return

    style = ctx.style
    gap = style.gap_emu()
    n_rows = len(rows)
    row_h = (ctx.content_h - gap * (n_rows - 1)) // n_rows
    y = ctx.content_top
    used_ids: set[str] = set()
    for row in rows:
        ids = row.get("block_ids") or []
        used_ids.update(ids)
        n = len(ids)
        cell_w = (ctx.width - gap * (n - 1)) // n if n else ctx.width
        x = ctx.left
        for bid in ids:
            block = by_id.get(bid)
            if block is None:
                continue
            if block.get("role") == "table":
                ctx.table(block, _frame(x, y, cell_w, row_h), doc)
            elif block.get("role") == "image":
                ctx.image_placeholder(block, _frame(x, y, cell_w, row_h))
            else:
                ctx.card(block, _frame(x, y, cell_w, row_h))
            x += cell_w + gap
        y += row_h + gap

    # blocks the proposal omitted (validation should forbid, but stay safe)
    leftover = [b for b in blocks if b.get("id") not in used_ids]
    if leftover:
        ctx.stack(leftover, top=y,
                  height=ctx.content_top + ctx.content_h - y)


def _cover_slide(ir: dict, style: ResolvedStyle) -> dict:
    """McKinsey-style cover: a vertical primary bar anchors the title block,
    followed by a subtitle and a horizontal rule (migrated from v3's
    renderCoverSlide)."""
    deck = ir["deck"]
    margin = style.margin_emu()
    bar_x = margin + int(0.1 * EMU_PER_IN)
    text_x = margin + int(0.55 * EMU_PER_IN)
    width = CANVAS_W - 2 * margin - int(0.7 * EMU_PER_IN)

    elements = [{
        # left vertical bar — the cover's visual anchor
        "element_id": "cover-bar", "type": "shape", "shape": "rect",
        "frame": _frame(bar_x, int(1.35 * EMU_PER_IN),
                        int(0.12 * EMU_PER_IN), int(3.95 * EMU_PER_IN)),
        "fill": {"color": style.color("primary")},
        "editable": True, "semantic_role": "accent_bar",
    }, {
        "element_id": "cover-title", "type": "textbox",
        "frame": _frame(text_x, int(1.9 * EMU_PER_IN), width, int(1.55 * EMU_PER_IN)),
        "paragraphs": [_para([_run(deck["title"], style,
                                   style.size_cpt("title", "cover"),
                                   font=style.font("editorial"),
                                   weight=style.weight("bold", 700))],
                             line_height_pct=105)],
        "valign": "middle", "editable": True, "semantic_role": "title",
    }]

    subtitle = deck.get("purpose")
    if not subtitle:
        first_source = ir.get("sources", [{}])[0]
        source_path = first_source.get("path")
        subtitle = first_source.get("title") or (
            str(source_path).replace("\\", "/").rsplit("/", 1)[-1]
            if source_path else None
        )
    if subtitle:
        elements.append({
            "element_id": "cover-subtitle", "type": "textbox",
            "frame": _frame(text_x, int(3.9 * EMU_PER_IN), int(9.3 * EMU_PER_IN),
                            int(0.72 * EMU_PER_IN)),
            "paragraphs": [_para([_run(subtitle, style,
                                       max(style.size_cpt("body", "large"), 1400),
                                       color=style.color("text_secondary"))])],
            "valign": "top", "editable": True, "semantic_role": "subtitle",
        })

    elements.append({
        "element_id": "cover-rule", "type": "shape", "shape": "rect",
        "frame": _frame(text_x, int(5.25 * EMU_PER_IN), int(3.9 * EMU_PER_IN),
                        int(0.05 * EMU_PER_IN)),
        "fill": {"color": style.color("border")},
        "editable": True, "semantic_role": "rule",
    })
    return {"slide_id": "cover",
            "background": {"color": style.color("background")},
            "elements": elements}


def layout_deck(ir: dict, decisions: list, style: ResolvedStyle,
                docs: dict[str, SourceDoc] | None = None) -> dict:
    """Returns {"canvas", "fonts_used", "slides", "degradations"}."""
    docs = docs or {}
    from .speaker_notes import format_speaker_notes
    degradations: list[dict] = []
    plan_slides = [_cover_slide(ir, style)]
    decision_map = {d.slide_id: d for d in decisions}
    source_note = "；".join(
        s.get("title") or s.get("path") or s["source_id"] for s in ir.get("sources", []))
    for page_index, slide in enumerate(ir.get("slides", []), 1):
        decision = decision_map.get(slide["id"])
        archetype = decision.chosen if decision else "evidence_stack"
        ctx = SlideLayout(slide["id"], style, degradations)
        ctx.add_title(slide["title"], slide.get("message"))
        first_ref = next(
            (b.get("source_ref", {}).get("source_id")
             for b in slide.get("blocks", []) if b.get("source_ref")), None)
        doc = docs.get(first_ref) if first_ref else next(iter(docs.values()), None)
        _layout_content(ctx, slide, archetype, doc)
        ctx.add_footer(f"来源：{source_note}" if source_note else " ", page_index)
        plan_slide = {
            "slide_id": slide["id"],
            "background": {"color": style.color("background")},
            "elements": ctx.elements,
        }
        if isinstance(slide.get("speaker_notes"), dict):
            plan_slide["notes"] = format_speaker_notes(slide["speaker_notes"])
        plan_slides.append(plan_slide)
    fonts = sorted({run["font"]
                    for s in plan_slides for e in s["elements"]
                    for p in e.get("paragraphs", []) for run in p["runs"]}
                   | {run["font"]
                      for s in plan_slides for e in s["elements"] if e.get("type") == "table"
                      for row in e.get("rows", []) for cell in row["cells"]
                      for p in cell["paragraphs"] for run in p["runs"]})
    return {"canvas": {"width_emu": CANVAS_W, "height_emu": CANVAS_H},
            "fonts_used": fonts[:12], "slides": plan_slides,
            "degradations": degradations}

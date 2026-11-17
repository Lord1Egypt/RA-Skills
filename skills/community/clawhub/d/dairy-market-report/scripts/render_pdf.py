#!/usr/bin/env python3
"""Render the 乳制品市场行情报告 as a polished, single-document PDF.

Design goals:
  * Magazine-style cover band with title + period + meta.
  * Sections flow continuously (no forced page break per section) — only the
    cover and the very last page get PageBreaks. Reportlab's KeepTogether /
    KeepInFrame handles the rest.
  * Two-column narrative layout for long text (optional per section).
  * Tables styled with banded rows, soft borders, header band.
  * Color-coded change pills (Chinese market convention: up=red, down=green).
  * Page footer with page number and report title.

The PDF is generated natively with `reportlab` (no HTML, no Chromium, no
Playwright), using the built-in `STSong-Light` CJK font so Chinese text
renders correctly on any system without installing a font file.

Usage:
    python render_pdf.py --data <data.json> --out <report.pdf>
    python render_pdf.py --data <data.json>             # writes <data>.pdf
"""
from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepInFrame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

# Register a CJK-capable font (built-in to reportlab, no font file needed).
pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
CJK = "STSong-Light"

# --- Design tokens ---------------------------------------------------------

# Color palette (cool, professional, magazine-style)
INK = HexColor("#1B2733")           # body text
INK_SOFT = HexColor("#4A5867")      # secondary text
INK_MUTED = HexColor("#7A8896")     # footer / source
NAVY = HexColor("#0E2A47")          # primary brand
NAVY_LIGHT = HexColor("#1F4068")    # hover/secondary brand
ACCENT = HexColor("#D4A24C")        # warm gold accent
ACCENT_DARK = HexColor("#A37A2C")
TEAL = HexColor("#2E7C7B")
SOFT_BG = HexColor("#F4F1EA")       # page background card
BAND_BG = HexColor("#0E2A47")       # header band on cover
RULE = HexColor("#D8D2C2")
RED = HexColor("#B0322B")           # up (Chinese convention)
GREEN = HexColor("#1F7A4D")         # down
GREY_CHIP_BG = HexColor("#E8E5DC")

PAGE_W, PAGE_H = A4
MARGIN_X = 14 * mm
MARGIN_TOP = 14 * mm
MARGIN_BOTTOM = 16 * mm  # extra room for footer
USABLE_W = PAGE_W - 2 * MARGIN_X


# --- Utilities -------------------------------------------------------------

def _classify_change(text: str) -> str:
    if not text or text in ("—", "-", "持平", "暂无", "N/A", ""):
        return "flat"
    s = str(text)
    if s.startswith("+") or "↑" in s or s.endswith("+") or "涨" in s:
        return "up"
    if s.startswith("-") or "↓" in s or s.endswith("-") or "跌" in s:
        return "down"
    return "flat"


def _change_pill_html(change: str) -> str:
    cls = _classify_change(change)
    color = {"up": RED, "down": GREEN, "flat": INK_MUTED}[cls]
    bg = {"up": "#FBEAE7", "down": "#E6F3EC", "flat": "#EDEAE0"}[cls]
    arrow = {"up": "▲", "down": "▼", "flat": "—"}[cls]
    return (
        f'<font color="{color.hexval()}">'
        f'<para backColor="{bg}" borderColor="{color.hexval()}" '
        f'borderWidth="0.4" borderPadding="2" leftIndent="0" rightIndent="0">'
        f'&nbsp;{arrow}&nbsp;{change}&nbsp;</para></font>'
    )


# --- Paragraph styles ------------------------------------------------------

def _style(name: str, **kwargs) -> ParagraphStyle:
    defaults = {
        "fontName": CJK,
        "fontSize": 9.5,
        "leading": 14,
        "textColor": INK,
    }
    defaults.update(kwargs)
    return ParagraphStyle(name=name, **defaults)


# Reusable styles
S_BODY = _style("body", alignment=TA_JUSTIFY)
S_BODY_TIGHT = _style("body_tight", leading=13)
S_TITLE = _style("title", fontSize=26, leading=32, textColor=colors.white, alignment=TA_LEFT)
S_TITLE_SUB = _style("title_sub", fontSize=12, leading=16, textColor=ACCENT, alignment=TA_LEFT)
S_META = _style("meta", fontSize=8.5, leading=12, textColor=colors.white, alignment=TA_LEFT)
S_H1 = _style("h1", fontSize=14, leading=18, textColor=NAVY, spaceBefore=4, spaceAfter=4, fontName=CJK)
S_H2 = _style("h2", fontSize=10.5, leading=14, textColor=NAVY_LIGHT, spaceBefore=4, spaceAfter=2)
S_KPI_LABEL = _style("kpi_label", fontSize=8, leading=10, textColor=INK_SOFT, alignment=TA_CENTER)
S_KPI_VALUE = _style("kpi_value", fontSize=14, leading=18, textColor=NAVY, alignment=TA_CENTER)
S_KPI_CHANGE = _style("kpi_change", fontSize=8, leading=10, alignment=TA_CENTER)
S_TH = _style("th", fontSize=8.5, leading=11, textColor=colors.white, alignment=TA_LEFT, fontName=CJK)
S_TD = _style("td", fontSize=8.5, leading=12, textColor=INK, alignment=TA_LEFT)
S_TD_CENTER = _style("td_c", fontSize=8.5, leading=12, textColor=INK, alignment=TA_CENTER)
S_TD_NUM = _style("td_n", fontSize=8.5, leading=12, textColor=INK, alignment=TA_RIGHT)
S_TD_TXT = _style("td_txt", fontSize=8.5, leading=12, textColor=INK, alignment=TA_LEFT)
S_SMALL = _style("small", fontSize=8, leading=11, textColor=INK_MUTED)
S_FOOTER = _style("footer", fontSize=7.5, leading=10, textColor=INK_MUTED, alignment=TA_CENTER)
S_CALLOUT = _style("callout", fontSize=9, leading=13, textColor=INK)
S_KEY_LABEL = _style("key_label", fontSize=8, leading=10, textColor=ACCENT_DARK)
S_KEY_BODY = _style("key_body", fontSize=9, leading=13, textColor=INK)
S_TOC = _style("toc", fontSize=10, leading=15, textColor=INK)


# --- Building blocks -------------------------------------------------------

def cover_block(meta: dict, key_takeaways: list[str]) -> list:
    """Top band with title + period + a one-line summary + key takeaway list."""
    title = meta.get("title", "乳制品市场行情报告")
    period = meta.get("period", "")
    period_disp = f"{period[:4]} 年 {int(period[4:])} 月" if period and len(period) == 6 else (period or "—")
    sources = meta.get("sources", "")
    generated = meta.get("generated_at") or datetime.now().strftime("%Y-%m-%d")

    # Cover band table (acts as a colored block)
    band_html = (
        f'<para spaceBefore="0" spaceAfter="0">'
        f'<font color="#FFFFFF" size="24"><b>{title}</b></font><br/>'
        f'<font color="#D4A24C" size="13">{period_disp} · 月度报告</font><br/>'
        f'<font color="#9DB1C7" size="8">数据源：{sources}</font><br/>'
        f'<font color="#9DB1C7" size="8">生成时间：{generated}</font>'
        f'</para>'
    )
    band = Table(
        [[Paragraph(band_html, _style("band", leading=18, fontSize=10))]],
        colWidths=[USABLE_W],
        rowHeights=[58 * mm],
    )
    band.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BAND_BG),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("TOPPADDING", (0, 0), (-1, -1), 16),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
    ]))

    flow = [band, Spacer(1, 6 * mm)]

    # Decorative rule
    rule = Table([[""]], colWidths=[USABLE_W], rowHeights=[1.2])
    rule.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ACCENT),
        ("LINEABOVE", (0, 0), (-1, -1), 0, colors.white),
    ]))
    flow += [rule, Spacer(1, 5 * mm)]

    # Key takeaways card
    bullet_items = []
    for t in key_takeaways:
        bullet_items.append(
            f'<font color="{NAVY.hexval()}"><b>●</b></font>&nbsp;&nbsp;{t}'
        )
    bullets_html = "<br/><br/>".join(bullet_items)
    card_html = (
        f'<font color="{ACCENT_DARK.hexval()}" size="9"><b>CORE TAKEAWAYS · 核心结论</b></font>'
        f'<br/><br/>{bullets_html}'
    )
    card = Table(
        [[Paragraph(card_html, _style("card", leading=14, fontSize=9.5))]],
        colWidths=[USABLE_W],
    )
    card.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SOFT_BG),
        ("LINEBEFORE", (0, 0), (-1, -1), 3, ACCENT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    flow += [card, Spacer(1, 4 * mm)]

    # Table of contents
    flow.append(Paragraph("目录 · Table of Contents", _style("toc_title", fontSize=11, leading=14, textColor=NAVY, spaceBefore=2, spaceAfter=4)))
    return flow


def kpi_row(items: list[dict]) -> Table:
    cells = []
    for it in items:
        label = it.get("label", "")
        value = it.get("value", "")
        change = it.get("change", "")
        cls = _classify_change(change)
        arrow = {"up": "▲", "down": "▼", "flat": "—"}[cls]
        color = {"up": RED, "down": GREEN, "flat": INK_MUTED}[cls]
        change_html = (
            f'<font color="{color.hexval()}" size="8.5">'
            f'{arrow} {change}</font>'
        )
        cell_html = (
            f'<para alignment="center" spaceBefore="0" spaceAfter="0">'
            f'<font color="{INK_SOFT.hexval()}" size="8">{label}</font><br/>'
            f'<font color="{NAVY.hexval()}" size="14"><b>{value}</b></font><br/>'
            f'{change_html}</para>'
        )
        cells.append(Paragraph(cell_html, _style("kpi_cell", fontSize=8)))
    n = max(len(items), 1)
    col_w = USABLE_W / n
    t = Table([cells], colWidths=[col_w] * n)
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, NAVY),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, RULE),
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def styled_table(headers: list[str], rows: list[list[str]], col_widths: list[float] | None = None,
                 col_align: list[str] | None = None, change_cols: list[int] | None = None) -> Table:
    """Render a data table. col_align: list of 'l'|'c'|'r' per column.
    change_cols: 0-based indices whose cell content is treated as a change pill.
    """
    change_cols = change_cols or []
    col_align = col_align or ["l"] * len(headers)

    th_cells = [Paragraph(f'<b>{h}</b>', S_TH) for h in headers]
    body_cells = []
    for row in rows:
        cells = []
        for ci, raw in enumerate(row):
            txt = str(raw) if raw is not None else ""
            if ci in change_cols:
                # Render as a colored pill
                cls = _classify_change(txt)
                color = {"up": RED, "down": GREEN, "flat": INK_MUTED}[cls]
                bg = {"up": "#FBEAE7", "down": "#E6F3EC", "flat": "#EDEAE0"}[cls]
                arrow = {"up": "▲", "down": "▼", "flat": "—"}[cls]
                pill = (
                    f'<font color="{color.hexval()}">'
                    f'<para alignment="center" backColor="{bg}" '
                    f'borderPadding="1.5" leftIndent="0" rightIndent="0">'
                    f'&nbsp;{arrow}&nbsp;{txt}&nbsp;</para></font>'
                )
                cells.append(Paragraph(pill, _style("pill", fontSize=8.5, leading=10)))
            else:
                style = {"c": S_TD_CENTER, "r": S_TD_NUM, "l": S_TD_TXT}[col_align[ci] if ci < len(col_align) else "l"]
                cells.append(Paragraph(txt, style))
        body_cells.append(cells)

    data = [th_cells] + body_cells
    if col_widths is None:
        # Even split
        col_widths = [USABLE_W / len(headers)] * len(headers)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), CJK),
        ("FONTSIZE", (0, 0), (-1, 0), 8.5),
        ("LEFTPADDING", (0, 0), (-1, 0), 6),
        ("RIGHTPADDING", (0, 0), (-1, 0), 6),
        ("TOPPADDING", (0, 0), (-1, 0), 5),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
        ("GRID", (0, 0), (-1, -1), 0.25, RULE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 1), (-1, -1), 6),
        ("RIGHTPADDING", (0, 1), (-1, -1), 6),
        ("TOPPADDING", (0, 1), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, HexColor("#F8F6F0")]),
    ]
    t.setStyle(TableStyle(style))
    return t


def callout_block(text: str, bg: str = "#FFF7E6", border: str = "#D4A24C") -> Table:
    text = text.replace("\n", "<br/>")
    inner = Paragraph(text, S_CALLOUT)
    t = Table([[inner]], colWidths=[USABLE_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor(bg)),
        ("LINEBEFORE", (0, 0), (-1, -1), 3, HexColor(border)),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def section_block(section: dict, section_idx: int, total: int) -> list:
    """Build the flow for one section."""
    flow = []

    sid = section.get("id", section_idx + 1)
    title = section.get("title", "")
    flow.append(Paragraph(
        f'<font color="{ACCENT_DARK.hexval()}" size="9">SECTION {sid:02d} / {total:02d}</font><br/>'
        f'<font color="{NAVY.hexval()}" size="14"><b>{title}</b></font>',
        _style("section_title", leading=14, spaceBefore=4, spaceAfter=4),
    ))
    # Decorative rule under section title
    rule = Table([[""]], colWidths=[USABLE_W * 0.15], rowHeights=[1.5])
    rule.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), ACCENT)]))
    flow += [rule, Spacer(1, 3 * mm)]

    narrative = section.get("narrative")
    if narrative:
        flow.append(Paragraph(narrative, S_BODY))
        flow.append(Spacer(1, 2 * mm))

    kpis = section.get("kpis")
    if kpis:
        flow.append(kpi_row(kpis))
        flow.append(Spacer(1, 3 * mm))

    table = section.get("table")
    if table:
        flow.append(styled_table(
            table["headers"],
            table["rows"],
            col_widths=table.get("col_widths"),
            col_align=table.get("col_align"),
            change_cols=table.get("change_cols"),
        ))
        flow.append(Spacer(1, 2 * mm))

    sub_tables = section.get("sub_tables") or []
    for st in sub_tables:
        if st.get("sub_header"):
            flow.append(Paragraph(
                f'<font color="{NAVY_LIGHT.hexval()}" size="10"><b>{st["sub_header"]}</b></font>',
                _style("subh", leading=12, spaceBefore=3, spaceAfter=2),
            ))
        flow.append(styled_table(
            st["headers"],
            st["rows"],
            col_widths=st.get("col_widths"),
            col_align=st.get("col_align"),
            change_cols=st.get("change_cols"),
        ))
        flow.append(Spacer(1, 2 * mm))

    cl = section.get("callout")
    if cl:
        flow.append(callout_block(
            cl["text"],
            bg=cl.get("bg", "#FFF7E6"),
            border=cl.get("border", "#D4A24C"),
        ))
        flow.append(Spacer(1, 2 * mm))

    src = section.get("source")
    if src:
        flow.append(Paragraph(f'<i>数据来源：{src}</i>', S_SMALL))

    flow.append(Spacer(1, 4 * mm))
    return flow


# --- Page templates --------------------------------------------------------

def _on_page(canvas, doc):
    """Draw footer + page number on every page."""
    canvas.saveState()
    # Footer rule
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN_X, MARGIN_BOTTOM - 4 * mm, PAGE_W - MARGIN_X, MARGIN_BOTTOM - 4 * mm)
    # Footer text
    canvas.setFont(CJK, 7.5)
    canvas.setFillColor(INK_MUTED)
    left = "乳制品市场行情报告 · 2023 年 10 月"
    right = f"— {doc.page} —"
    canvas.drawString(MARGIN_X, MARGIN_BOTTOM - 8 * mm, left)
    canvas.drawRightString(PAGE_W - MARGIN_X, MARGIN_BOTTOM - 8 * mm, right)
    # Cover page gets no footer marker — keep it but make it more subtle
    canvas.restoreState()


def _build_doc(out_path: str) -> BaseDocTemplate:
    frame_cover = Frame(
        MARGIN_X, MARGIN_BOTTOM,
        USABLE_W, PAGE_H - MARGIN_TOP - MARGIN_BOTTOM,
        leftPadding=0, rightPadding=0,
        topPadding=0, bottomPadding=0,
        showBoundary=0,
    )
    frame_body = Frame(
        MARGIN_X, MARGIN_BOTTOM,
        USABLE_W, PAGE_H - MARGIN_TOP - MARGIN_BOTTOM,
        leftPadding=0, rightPadding=0,
        topPadding=0, bottomPadding=0,
        showBoundary=0,
    )
    doc = BaseDocTemplate(
        out_path,
        pagesize=A4,
        leftMargin=MARGIN_X,
        rightMargin=MARGIN_X,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM,
        title="乳制品市场行情报告",
        author="dairy-market-report skill",
    )
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[frame_cover], onPage=_on_page),
        PageTemplate(id="body", frames=[frame_body], onPage=_on_page),
    ])
    return doc


# --- Smoke fixture ---------------------------------------------------------

SMOKE_FIXTURE = {
    "meta": {
        "title": "乳制品市场行情报告",
        "period": "202310",
        "sources": "艾格农业《中国乳业研究月报》202309、202310",
    },
    "key_takeaways": [
        "生鲜乳价连降 10 月后现企稳信号，10 月均价 3.73 元/kg，同比 -10.0%。",
        "GDT 三连升后入仓价仍普遍高于国产，进口替代窗口未打开。",
    ],
    "sections": [
        {
            "id": 1,
            "title": "乳业整体形势概览 (smoke test)",
            "kpis": [
                {"label": "生鲜乳价", "value": "3.73 元/kg", "change": "-10.0% YoY"},
                {"label": "乳制品产量", "value": "2,286 万吨", "change": "+3.8% YoY"},
            ],
            "narrative": "本节用于校验 render_pdf.py 渲染管线是否正常。",
            "table": {
                "headers": ["产品", "USD/吨", "涨跌"],
                "rows": [["WMP", "3,059", "+0.4%"], ["SMP", "2,659", "-2.4%"]],
                "change_cols": [2],
            },
            "callout": {"text": "此为冒烟测试 callout。"},
            "source": "艾格农业《中国乳业研究月报》202310 (smoke test)",
        },
    ],
}


# --- Story assembly --------------------------------------------------------

def build_story(data: dict) -> list:
    story = []
    meta = data.get("meta", {})
    sections = data.get("sections", [])
    total = len(sections)

    # ---- Cover page ----
    cover_flow = cover_block(meta, data.get("key_takeaways", []))
    # TOC: render as a 2-column table
    toc_rows = []
    # Pad to even count for cleaner 2-col layout
    sec_pairs = [(i + 1, s.get("title", "")) for i, s in enumerate(sections)]
    if len(sec_pairs) % 2 == 1:
        sec_pairs.append(("", ""))
    for j in range(0, len(sec_pairs), 2):
        left = sec_pairs[j]
        right = sec_pairs[j + 1]
        left_html = (
            f'<para spaceBefore="0" spaceAfter="0">'
            f'<font color="{NAVY.hexval()}" size="9"><b>{left[0]:02d}</b></font>'
            f'&nbsp;&nbsp;<font color="{INK.hexval()}" size="9.5">{left[1]}</font></para>'
        )
        right_html = (
            f'<para spaceBefore="0" spaceAfter="0">'
            f'<font color="{NAVY.hexval()}" size="9"><b>{right[0]:02d}</b></font>'
            f'&nbsp;&nbsp;<font color="{INK.hexval()}" size="9.5">{right[1]}</font></para>'
        )
        toc_rows.append([Paragraph(left_html, S_TOC), Paragraph(right_html, S_TOC)])
    toc_block = Table(
        toc_rows,
        colWidths=[USABLE_W / 2 - 2 * mm, USABLE_W / 2 - 2 * mm],
    )
    toc_block.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("BOX", (0, 0), (-1, -1), 0.5, RULE),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, HexColor("#EDE7D8")),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    cover_flow.append(toc_block)
    cover_flow.append(Spacer(1, 4 * mm))
    cover_flow.append(Paragraph(
        '<i>本报告由 dairy-market-report skill 自动生成 · 仅供内部参考，不构成投资或商业决策建议。</i>',
        S_SMALL,
    ))
    # Wrap the entire cover in KeepInFrame so it stays on one page (or compresses)
    story.append(KeepInFrame(
        USABLE_W,
        PAGE_H - MARGIN_TOP - MARGIN_BOTTOM,
        cover_flow,
        mode="shrink",
    ))
    story.append(PageBreak())

    # ---- Body sections ----
    # Note: do NOT wrap each section in KeepInFrame; that was forcing long
    # sections to shrink to fit one page. Let reportlab flow naturally; the
    # only PageBreak is between the cover and the first body section.
    for idx, sec in enumerate(sections):
        story.extend(section_block(sec, idx, total))

    return story


# --- Main ------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Render dairy report to PDF")
    parser.add_argument("--data", help="Path to a JSON data file. Omit to use the smoke-test fixture.")
    parser.add_argument("--out", help="Output PDF path (defaults to <data>.pdf or ./dairy-report-smoke.pdf)")
    args = parser.parse_args()

    if args.data:
        with open(args.data, "r", encoding="utf-8") as f:
            data = json.load(f)
        out_path = args.out or str(Path(args.data).with_suffix(".pdf"))
    else:
        data = SMOKE_FIXTURE
        out_path = args.out or "./dairy-report-smoke.pdf"

    out_path = os.path.abspath(out_path)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    doc = _build_doc(out_path)
    doc.build(build_story(data))
    print(f"PDF written: {out_path} ({os.path.getsize(out_path):,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

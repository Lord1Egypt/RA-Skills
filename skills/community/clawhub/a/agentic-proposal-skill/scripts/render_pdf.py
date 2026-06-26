#!/usr/bin/env python3
"""Shared CompleteTech-branded Markdown -> PDF renderer + full-page PNG montage.

Generalized from agentic_contract_skill/generate_contract.py so the same
CompleteTech LLC branding (logo, palette, cover, letterhead, watermark, footer)
can be applied to every skill in the library.

Usage:
    python render_branded_pdf.py \
        --markdown doc.md --out out.pdf --png out.png \
        --logo /path/assets/logo.png \
        --title "Statement of Work" --eyebrow "COMPLETETECH LLC" \
        --doc-type "PROPOSAL" \
        --subtitle "Prepared for <b>Northwind Trading Co.</b>" \
        --meta "DOCUMENT NO.=PRO-2026-0188" \
        --meta "DATE=2026-05-24" \
        --meta "PREPARED BY=CompleteTech LLC" \
        --watermark "DEMO DRAFT" \
        --footer "CompleteTech LLC - Innovation at Every Integration"
"""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.platypus import (
    Flowable, ListFlowable, ListItem, PageBreak, Paragraph,
    SimpleDocTemplate, Spacer, Table, TableStyle,
)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

# --------------------------------------------------------------------------- #
# Brand palette (CompleteTech LLC defaults, matching the contract skill)
# --------------------------------------------------------------------------- #
BRAND = {
    "accent": "#1E3A8A",
    "accent_dark": "#0F172A",
    "accent_soft": "#EEF2FF",
    "muted": "#64748B",
    "border": "#E2E8F0",
    "zebra": "#F8FAFC",
    "brand_name": "CompleteTech",
    "brand_tagline": "Innovation at Every Integration",
    "contact": "complete.tech  ·  Timothy.Gregg@complete.tech",
}


def hex_color(raw: Optional[str], fallback: str) -> colors.Color:
    try:
        return colors.HexColor(raw or fallback)
    except Exception:
        return colors.HexColor(fallback)


def palette() -> Dict[str, colors.Color]:
    return {
        "accent": hex_color(BRAND["accent"], "#1E3A8A"),
        "accent_dark": hex_color(BRAND["accent_dark"], "#0F172A"),
        "accent_soft": hex_color(BRAND["accent_soft"], "#EEF2FF"),
        "muted": hex_color(BRAND["muted"], "#64748B"),
        "border": hex_color(BRAND["border"], "#E2E8F0"),
        "zebra": hex_color(BRAND["zebra"], "#F8FAFC"),
        "ink": colors.HexColor("#0F172A"),
        "ink_soft": colors.HexColor("#1E293B"),
        "white": colors.white,
    }


# --------------------------------------------------------------------------- #
# Logo
# --------------------------------------------------------------------------- #
def draw_logo(c: pdf_canvas.Canvas, x: float, y: float, size: float,
              logo_path: Optional[Path], pal: Dict[str, colors.Color],
              on_dark: bool = False) -> None:
    if logo_path and logo_path.exists():
        try:
            c.drawImage(ImageReader(str(logo_path)), x, y, width=size, height=size,
                        preserveAspectRatio=True, mask="auto")
            return
        except Exception:
            pass
    radius = size * 0.18
    c.saveState()
    fill = pal["white"] if on_dark else pal["accent"]
    c.setFillColor(fill)
    c.roundRect(x, y, size, size, radius, stroke=0, fill=1)
    c.setFillColor(pal["accent"] if on_dark else pal["white"])
    c.setFont("Helvetica-Bold", size * 0.5)
    c.drawCentredString(x + size / 2.0, y + size / 2.0 - size * 0.18, "CT")
    c.restoreState()


class LogoFlowable(Flowable):
    def __init__(self, logo_path: Optional[Path], pal: Dict[str, colors.Color], size: float):
        super().__init__()
        self.logo_path = logo_path
        self.pal = pal
        self.size = size
        self.width = size
        self.height = size * 0.5  # logo art is ~2:1, keep cover tidy

    def wrap(self, aW: float, aH: float) -> tuple[float, float]:
        return self.size, self.size * 0.52

    def draw(self):
        if self.logo_path and self.logo_path.exists():
            try:
                img = ImageReader(str(self.logo_path))
                iw, ih = img.getSize()
                ratio = ih / iw
                w = self.size
                h = w * ratio
                self.canv.drawImage(img, 0, 0, width=w, height=h,
                                    preserveAspectRatio=True, mask="auto")
                self.height = h
                return
            except Exception:
                pass
        draw_logo(self.canv, 0, 0, self.size * 0.4, self.logo_path, self.pal)


# --------------------------------------------------------------------------- #
# Styles
# --------------------------------------------------------------------------- #
def make_styles(pal: Dict[str, colors.Color]) -> Dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "CoverEyebrow": ParagraphStyle("CoverEyebrow", parent=base["BodyText"],
            fontName="Helvetica-Bold", fontSize=8.5, leading=11, alignment=TA_CENTER,
            textColor=pal["accent"], spaceAfter=8),
        "CoverDocType": ParagraphStyle("CoverDocType", parent=base["BodyText"],
            fontName="Helvetica-Bold", fontSize=8, leading=10, alignment=TA_CENTER,
            textColor=pal["muted"], spaceAfter=6),
        "CoverTitle": ParagraphStyle("CoverTitle", parent=base["Title"],
            fontName="Helvetica-Bold", fontSize=27, leading=32, alignment=TA_CENTER,
            textColor=pal["ink"], spaceAfter=10),
        "CoverSubtitle": ParagraphStyle("CoverSubtitle", parent=base["BodyText"],
            fontName="Times-Roman", fontSize=12.5, leading=17, alignment=TA_CENTER,
            textColor=pal["ink_soft"], spaceAfter=4),
        "CoverFieldLabel": ParagraphStyle("CoverFieldLabel", parent=base["BodyText"],
            fontName="Helvetica-Bold", fontSize=7.5, leading=10, alignment=TA_LEFT,
            textColor=pal["muted"], spaceAfter=2),
        "CoverFieldValue": ParagraphStyle("CoverFieldValue", parent=base["BodyText"],
            fontName="Helvetica-Bold", fontSize=11, leading=14, alignment=TA_LEFT,
            textColor=pal["ink"], spaceAfter=0),
        "CoverDisclaimer": ParagraphStyle("CoverDisclaimer", parent=base["BodyText"],
            fontName="Times-Italic", fontSize=9, leading=12.5, alignment=TA_CENTER,
            textColor=pal["muted"]),
        "Title": ParagraphStyle("Title", parent=base["Title"], fontName="Helvetica-Bold",
            fontSize=17, leading=21, alignment=TA_LEFT, spaceAfter=12, textColor=pal["ink"]),
        "Heading2": ParagraphStyle("Heading2", parent=base["Heading2"], fontName="Helvetica-Bold",
            fontSize=13, leading=17, spaceBefore=14, spaceAfter=7, textColor=pal["ink"]),
        "Heading3": ParagraphStyle("Heading3", parent=base["Heading3"], fontName="Helvetica-Bold",
            fontSize=10.8, leading=14, spaceBefore=8, spaceAfter=4, textColor=pal["accent"]),
        "Body": ParagraphStyle("Body", parent=base["BodyText"], fontName="Times-Roman",
            fontSize=9.8, leading=13.5, alignment=TA_JUSTIFY, spaceAfter=6, textColor=pal["ink_soft"]),
        "Bullet": ParagraphStyle("Bullet", parent=base["BodyText"], fontName="Times-Roman",
            fontSize=9.8, leading=13.2, leftIndent=8, spaceAfter=3, textColor=pal["ink_soft"]),
        "TableCell": ParagraphStyle("TableCell", parent=base["BodyText"], fontName="Times-Roman",
            fontSize=9, leading=12, spaceAfter=0, textColor=pal["ink_soft"]),
        "TableHeader": ParagraphStyle("TableHeader", parent=base["BodyText"], fontName="Helvetica-Bold",
            fontSize=8.5, leading=11, textColor=pal["white"], spaceAfter=0),
    }


# --------------------------------------------------------------------------- #
# Markdown -> flowables (subset: #/##/###, paragraphs, - bullets, tables,
# > callouts, **bold**, [PAGE_BREAK])
# --------------------------------------------------------------------------- #
BR = "\x00BR\x00"
SECTION_NUMBER_RE = re.compile(r"^\s*(\d+)\.\s+(.+)$")


def inline_markup(text: str) -> str:
    text = text.replace("<br/>", BR)
    esc = html.escape(text, quote=False)
    esc = esc.replace(BR, "<br/>")
    esc = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", esc)
    esc = re.sub(r"__(.+?)__", r"<b>\1</b>", esc)
    return esc


def color_to_hex(c: colors.Color) -> str:
    return "#%02X%02X%02X" % (int(round(c.red * 255)), int(round(c.green * 255)), int(round(c.blue * 255)))


def numbered_heading_markup(text: str, pal: Dict[str, colors.Color]) -> str:
    m = SECTION_NUMBER_RE.match(text)
    if not m:
        return inline_markup(text)
    number, label = m.group(1), m.group(2)
    return (f'<font name="Helvetica-Bold" size="20" color="{color_to_hex(pal["accent"])}">{int(number):02d}</font>'
            f'&nbsp;&nbsp;<font color="{color_to_hex(pal["muted"])}">|</font>&nbsp;&nbsp;{inline_markup(label)}')


def is_table_sep(cells: Sequence[str]) -> bool:
    return all(re.fullmatch(r":?-{3,}:?", c.strip()) for c in cells if c.strip())


def parse_table_rows(lines: Sequence[str]) -> List[List[str]]:
    rows = []
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if is_table_sep(cells):
            continue
        rows.append(cells)
    return rows


def col_widths(rows, available):
    ncols = max((len(r) for r in rows), default=1)
    if ncols == 1:
        return [available]
    if ncols == 2:
        return [available * 0.34, available * 0.66]
    return [available / ncols] * ncols


def make_table(lines, styles, available, pal) -> Table:
    rows = parse_table_rows(lines) or [[""]]
    ncols = max(len(r) for r in rows)
    rows = [list(r) + [""] * (ncols - len(r)) for r in rows]
    data = [[Paragraph(inline_markup(c), styles["TableHeader"] if i == 0 else styles["TableCell"])
             for c in row] for i, row in enumerate(rows)]
    t = Table(data, colWidths=col_widths(rows, available), repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), pal["accent"]),
        ("TEXTCOLOR", (0, 0), (-1, 0), pal["white"]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6, pal["accent_dark"]),
        ("LINEBELOW", (0, -1), (-1, -1), 0.4, pal["border"]),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 7), ("BOTTOMPADDING", (0, 0), (-1, 0), 7),
        ("TOPPADDING", (0, 1), (-1, -1), 6), ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [pal["white"], pal["zebra"]]),
        ("LINEABOVE", (0, 1), (-1, -1), 0.25, pal["border"]),
    ]))
    return t


def make_callout(quote_lines, styles, available, pal) -> Table:
    para = Paragraph(inline_markup(" ".join(quote_lines)).strip(),
                     ParagraphStyle("CalloutBody", parent=styles["Body"], fontName="Times-Italic",
                                    textColor=pal["ink_soft"], leading=13.5, fontSize=9.5,
                                    alignment=TA_LEFT, spaceAfter=0))
    t = Table([[para]], colWidths=[available], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), pal["accent_soft"]),
        ("LINEBEFORE", (0, 0), (0, -1), 3, pal["accent"]),
        ("LEFTPADDING", (0, 0), (-1, -1), 14), ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    return t


def is_block_start(line: str) -> bool:
    s = line.strip()
    return (s.startswith("#") or s.startswith("- ") or s.startswith("|")
            or s.startswith("> ") or s == "[PAGE_BREAK]")


def paragraph_text(lines: Sequence[str]) -> str:
    parts = [(line.strip() + "<br/>") if line.endswith("  ") else line.strip() for line in lines]
    return re.sub(r"<br/>\s+", "<br/>", " ".join(parts))


def markdown_to_story(md, styles, available, pal) -> List[Any]:
    story: List[Any] = []
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.strip()
        if not line:
            i += 1
            continue
        if line == "[PAGE_BREAK]":
            story.append(PageBreak())
            i += 1
            continue
        if line.startswith("# "):
            story.append(Paragraph(inline_markup(line[2:].strip()), styles["Title"]))
            story.append(Spacer(1, 0.05 * inch))
            i += 1
            continue
        if line.startswith("## "):
            story.append(Paragraph(numbered_heading_markup(line[3:].strip(), pal), styles["Heading2"]))
            i += 1
            continue
        if line.startswith("### "):
            story.append(Paragraph(inline_markup(line[4:].strip()), styles["Heading3"]))
            i += 1
            continue
        if line.startswith("> "):
            q = []
            while i < len(lines) and lines[i].strip().startswith("> "):
                q.append(lines[i].strip()[2:])
                i += 1
            story.append(make_callout(q, styles, available, pal))
            continue
        if line.startswith("- "):
            items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(ListItem(Paragraph(inline_markup(lines[i].strip()[2:].strip()), styles["Bullet"]),
                                      leftIndent=12, value="●", bulletColor=pal["accent"]))
                i += 1
            story.append(ListFlowable(items, bulletType="bullet", bulletFontName="Helvetica-Bold",
                                      bulletFontSize=6, leftIndent=20, bulletColor=pal["accent"]))
            story.append(Spacer(1, 0.04 * inch))
            continue
        if line.startswith("|"):
            tl = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                tl.append(lines[i])
                i += 1
            story.append(make_table(tl, styles, available, pal))
            story.append(Spacer(1, 0.10 * inch))
            continue
        para = [raw]
        i += 1
        while i < len(lines) and lines[i].strip() and not is_block_start(lines[i]):
            para.append(lines[i])
            i += 1
        story.append(Paragraph(inline_markup(paragraph_text(para)), styles["Body"]))
    return story


# --------------------------------------------------------------------------- #
# Page furniture
# --------------------------------------------------------------------------- #
def draw_watermark(c, w, h, text):
    if not text:
        return
    c.saveState()
    try:
        c.setFillColor(colors.Color(0.7, 0.7, 0.7, alpha=0.16))
    except TypeError:
        c.setFillColor(colors.HexColor("#D1D5DB"))
    c.translate(w / 2.0, h / 2.0)
    c.rotate(42)
    c.setFont("Helvetica-Bold", 58)
    c.drawCentredString(0, 0, text)
    c.restoreState()


def draw_letterhead_band(c, meta, w, h, pal, logo_path):
    band = 0.95 * inch
    c.saveState()
    c.setFillColor(pal["accent_dark"])
    c.rect(0, h - band, w, band, stroke=0, fill=1)
    c.setFillColor(pal["accent"])
    c.rect(0, h - band - 0.04 * inch, w, 0.04 * inch, stroke=0, fill=1)
    pad = 0.72 * inch
    ls = 0.52 * inch
    draw_logo(c, pad, h - band + (band - ls) / 2.0, ls, logo_path, pal, on_dark=True)
    nx = pad + ls + 0.18 * inch
    c.setFillColor(pal["white"])
    c.setFont("Helvetica-Bold", 13.5)
    c.drawString(nx, h - 0.42 * inch, BRAND["brand_name"])
    c.setFont("Helvetica", 8.5)
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.78))
    c.drawString(nx, h - 0.58 * inch, BRAND["brand_tagline"])
    c.setFont("Helvetica", 7.5)
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.62))
    c.drawString(nx, h - 0.74 * inch, BRAND["contact"])
    right = w - pad
    pairs = meta[:2]
    ys = [(0.36, 0.50), (0.66, 0.80)]
    for (label, value), (ly, vy) in zip(pairs, ys):
        c.setFillColor(colors.Color(1, 1, 1, alpha=0.7))
        c.setFont("Helvetica", 7.2)
        c.drawRightString(right, h - ly * inch, label.upper())
        c.setFillColor(pal["white"])
        c.setFont("Helvetica-Bold", 10.5)
        c.drawRightString(right, h - vy * inch, value)
    c.restoreState()


def draw_compact_header(c, doc_title, doc_id, w, h, pal, logo_path):
    pad = 0.72 * inch
    ls = 0.30 * inch
    draw_logo(c, pad, h - 0.62 * inch, ls, logo_path, pal, on_dark=False)
    tx = pad + ls + 0.12 * inch
    c.saveState()
    c.setFillColor(pal["ink"])
    c.setFont("Helvetica-Bold", 9)
    c.drawString(tx, h - 0.46 * inch, BRAND["brand_name"])
    c.setFillColor(pal["muted"])
    c.setFont("Helvetica", 7.5)
    c.drawString(tx, h - 0.58 * inch, BRAND["brand_tagline"])
    right = w - pad
    c.setFillColor(pal["ink"])
    c.setFont("Helvetica-Bold", 8.8)
    c.drawRightString(right, h - 0.46 * inch, doc_title)
    c.setFillColor(pal["muted"])
    c.setFont("Helvetica", 7.5)
    c.drawRightString(right, h - 0.58 * inch, doc_id)
    c.setStrokeColor(pal["accent"])
    c.setLineWidth(0.8)
    c.line(pad, h - 0.74 * inch, right, h - 0.74 * inch)
    c.restoreState()


def draw_footer(c, doc, footer_text, doc_id, w, pal):
    pad = 0.72 * inch
    right = w - pad
    y = 0.46 * inch
    c.saveState()
    c.setStrokeColor(pal["border"])
    c.setLineWidth(0.5)
    c.line(pad, y + 0.18 * inch, right, y + 0.18 * inch)
    c.setFillColor(pal["accent"])
    c.rect(pad, y + 0.18 * inch, 0.32 * inch, 0.012 * inch, stroke=0, fill=1)
    c.setFillColor(pal["muted"])
    c.setFont("Helvetica", 7.4)
    c.drawString(pad, y, doc_id)
    c.drawCentredString(w / 2, y, footer_text[:120])
    c.setFillColor(pal["ink"])
    c.setFont("Helvetica-Bold", 7.6)
    c.drawRightString(right, y, f"Page {doc.page}")
    c.restoreState()


def page_drawer(cfg, pal, first_page, cover_first):
    def draw(c, doc):
        w, h = doc.pagesize
        draw_watermark(c, w, h, cfg["watermark"])
        if first_page:
            if cover_first:
                draw_footer(c, doc, cfg["footer"], cfg["doc_id"], w, pal)
                return
            draw_letterhead_band(c, cfg["meta"], w, h, pal, cfg["logo"])
        else:
            draw_compact_header(c, cfg["title"], cfg["doc_id"], w, h, pal, cfg["logo"])
        draw_footer(c, doc, cfg["footer"], cfg["doc_id"], w, pal)
    return draw


def cover_flowables(cfg, styles, available, pal) -> List[Any]:
    story: List[Any] = [Spacer(1, 1.25 * inch)]
    logo = LogoFlowable(cfg["logo"], pal, size=2.6 * inch)
    logo.hAlign = "CENTER"
    story.append(logo)
    story.append(Spacer(1, 0.35 * inch))
    if cfg["eyebrow"]:
        story.append(Paragraph(cfg["eyebrow"].upper(), styles["CoverEyebrow"]))
    if cfg["doc_type"]:
        story.append(Paragraph(cfg["doc_type"].upper(), styles["CoverDocType"]))
    story.append(Paragraph(cfg["title"], styles["CoverTitle"]))
    if cfg["subtitle"]:
        story.append(Paragraph(cfg["subtitle"], styles["CoverSubtitle"]))
    story.append(Spacer(1, 0.55 * inch))

    def field(label, value):
        return [Paragraph(label.upper(), styles["CoverFieldLabel"]),
                Paragraph(html.escape(value or "TBD"), styles["CoverFieldValue"])]

    meta = cfg["meta"][:3]
    if meta:
        row = [[field(label, value) for label, value in meta]]
        cw = (available * 0.9) / len(meta)
        chip = Table(row, colWidths=[cw] * len(meta), hAlign="CENTER")
        chip.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), pal["accent_soft"]),
            ("LINEABOVE", (0, 0), (-1, 0), 2, pal["accent"]),
            ("LEFTPADDING", (0, 0), (-1, -1), 16), ("RIGHTPADDING", (0, 0), (-1, -1), 16),
            ("TOPPADDING", (0, 0), (-1, -1), 14), ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(chip)
    story.append(Spacer(1, 0.7 * inch))
    if cfg["disclaimer"]:
        story.append(Paragraph(cfg["disclaimer"], styles["CoverDisclaimer"]))
    story.append(PageBreak())
    return story


def build_pdf(md, cfg, out_path: Path):
    pal = palette()
    styles = make_styles(pal)
    cover = cfg["cover"]
    lm = rm = 0.72 * inch
    top = 0.82 * inch if cover else 1.30 * inch
    doc = SimpleDocTemplate(str(out_path), pagesize=LETTER, leftMargin=lm, rightMargin=rm,
                            topMargin=top, bottomMargin=0.82 * inch, title=cfg["title"],
                            author=BRAND["brand_name"])
    available = LETTER[0] - lm - rm
    story: List[Any] = []
    if cover:
        story.extend(cover_flowables(cfg, styles, available, pal))
    story.extend(markdown_to_story(md, styles, available, pal))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.build(story,
              onFirstPage=page_drawer(cfg, pal, first_page=True, cover_first=cover),
              onLaterPages=page_drawer(cfg, pal, first_page=False, cover_first=cover))


# --------------------------------------------------------------------------- #
# PDF -> PNG montage (all pages, full size, uncropped)
# --------------------------------------------------------------------------- #
def montage(pdf_path: Path, png_path: Path, scale: float = 2.0,
            cols: Optional[int] = None, bg=(244, 246, 251), gutter: int = 26,
            border=(210, 217, 230)) -> None:
    import pypdfium2 as pdfium
    from PIL import Image

    doc = pdfium.PdfDocument(str(pdf_path))
    pages = []
    for i in range(len(doc)):
        page = doc[i]
        bmp = page.render(scale=scale)
        pages.append(bmp.to_pil().convert("RGB"))
    n = len(pages)
    if cols is None:
        cols = 1 if n == 1 else (2 if n <= 4 else 3)
    rows = (n + cols - 1) // cols
    pw, ph = pages[0].size
    bw = 1  # page border width
    cell_w, cell_h = pw + 2 * bw, ph + 2 * bw
    W = gutter + cols * (cell_w + gutter)
    H = gutter + rows * (cell_h + gutter)
    canvas = Image.new("RGB", (W, H), bg)
    bordered = Image.new("RGB", (cell_w, cell_h), border)
    for idx, p in enumerate(pages):
        r, cc = divmod(idx, cols)
        x = gutter + cc * (cell_w + gutter)
        y = gutter + r * (cell_h + gutter)
        tile = bordered.copy()
        tile.paste(p, (bw, bw))
        canvas.paste(tile, (x, y))
    png_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(str(png_path))
    print(f"PNG montage: {png_path} ({n} page(s), {W}x{H})")


# --------------------------------------------------------------------------- #
def parse_meta(items: List[str]) -> List[tuple]:
    out = []
    for it in items:
        if "=" in it:
            k, v = it.split("=", 1)
            out.append((k.strip(), v.strip()))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--markdown", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--png", default=None)
    ap.add_argument("--logo", default=None)
    ap.add_argument("--title", default="Document")
    ap.add_argument("--eyebrow", default="CompleteTech LLC")
    ap.add_argument("--doc-type", default="")
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--meta", action="append", default=[])
    ap.add_argument("--doc-id", default="")
    ap.add_argument("--watermark", default="DEMO DRAFT")
    ap.add_argument("--footer", default="CompleteTech LLC - Innovation at Every Integration - demonstration artifact")
    ap.add_argument("--disclaimer", default="Demonstration artifact generated with realistic placeholder data — not a real client engagement.")
    ap.add_argument("--no-cover", action="store_true")
    ap.add_argument("--scale", type=float, default=2.0)
    ap.add_argument("--cols", type=int, default=None)
    args = ap.parse_args()

    meta = parse_meta(args.meta)
    cfg = {
        "logo": Path(args.logo).resolve() if args.logo else None,
        "title": args.title, "eyebrow": args.eyebrow, "doc_type": args.doc_type,
        "subtitle": args.subtitle, "meta": meta,
        "doc_id": args.doc_id or (meta[0][1] if meta else ""),
        "watermark": args.watermark, "footer": args.footer,
        "disclaimer": args.disclaimer, "cover": not args.no_cover,
    }
    md = Path(args.markdown).read_text(encoding="utf-8")
    out_pdf = Path(args.out).resolve()
    build_pdf(md, cfg, out_pdf)
    print(f"PDF: {out_pdf}")
    if args.png:
        montage(out_pdf, Path(args.png).resolve(), scale=args.scale, cols=args.cols)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

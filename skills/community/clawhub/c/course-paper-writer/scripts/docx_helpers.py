#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""course-paper-writer — DOCX helpers.

Usage:

    from docx_helpers import new_document, add_par, add_rich, CJK
    doc = new_document()
    add_rich(add_par(doc, align="center"), "论文题目", CJK["hei"], 16)
    add_rich(add_par(doc, indent=24), "正文⟦1⟧继续。", CJK["song"], 12)

⟦n⟧ becomes a superscript [n] on render, so citation numbers can be
renumbered without touching formatting.
"""

import re

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

CJK = {
    "song": "宋体",
    "hei": "黑体",
    "kai": "楷体",
    "fangsong": "仿宋",
}

ALIGN = {
    "left": WD_ALIGN_PARAGRAPH.LEFT,
    "center": WD_ALIGN_PARAGRAPH.CENTER,
    "right": WD_ALIGN_PARAGRAPH.RIGHT,
    "justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
}

CITE = re.compile(r"⟦(\d+)⟧")


def new_document(margins=(2.54, 2.54, 3.17, 3.17)):
    """A4 with the usual Chinese course-paper margins (top, bottom, left, right cm)."""
    doc = Document()
    s = doc.sections[0]
    s.page_width, s.page_height = Cm(21.0), Cm(29.7)
    s.top_margin, s.bottom_margin = Cm(margins[0]), Cm(margins[1])
    s.left_margin, s.right_margin = Cm(margins[2]), Cm(margins[3])
    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(12)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), CJK["song"])
    return doc


def set_font(run, cn_font, size_pt, bold=False):
    """Set both the western and the east-asian font. Forgetting eastAsia is the
    single most common cause of wrong-looking Chinese in python-docx output."""
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.font.name = "Times New Roman"
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = rPr.makeelement(qn("w:rFonts"), {})
        rPr.append(rFonts)
    rFonts.set(qn("w:eastAsia"), cn_font)
    rFonts.set(qn("w:ascii"), "Times New Roman")
    rFonts.set(qn("w:hAnsi"), "Times New Roman")


def add_par(doc, align=None, line_spacing=1.5, indent=None,
            before=0, after=0, keep_with_next=False):
    """Add a paragraph. indent is in points: '2 字符' at 小四 = 24."""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    if align:
        p.alignment = ALIGN[align]
    pf.line_spacing = line_spacing
    if indent is not None:
        pf.first_line_indent = Pt(indent)
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    if keep_with_next:
        pf.keep_with_next = True
    return p


def add_rich(par, text, cn_font, size_pt, bold=False):
    """Add text to a paragraph, rendering ⟦n⟧ as a superscript [n]."""
    pos = 0
    for m in CITE.finditer(text):
        if m.start() > pos:
            set_font(par.add_run(text[pos:m.start()]), cn_font, size_pt, bold)
        r = par.add_run("[%s]" % m.group(1))
        set_font(r, cn_font, size_pt, bold)
        r.font.superscript = True
        pos = m.end()
    if pos < len(text):
        set_font(par.add_run(text[pos:]), cn_font, size_pt, bold)
    return par


def renumber(blocks, n_refs):
    """Order citations by first appearance and reorder the reference list.

    blocks: list of (kind, text) with ⟦n⟧ placeholders.
    Returns (blocks, order) where order maps new index -> old 1-based index.
    """
    order = []
    for _, t in blocks:
        for m in CITE.finditer(t):
            v = int(m.group(1))
            if v not in order:
                order.append(v)
    order += [i for i in range(1, n_refs + 1) if i not in order]
    mapping = {old: new for new, old in enumerate(order, 1)}
    blocks = [(k, CITE.sub(lambda m: "⟦%d⟧" % mapping[int(m.group(1))], t))
              for k, t in blocks]
    return blocks, order


def save_with_fallback(doc, path):
    """Save; if Word has the file locked, write a sibling copy instead of dying."""
    import os
    try:
        doc.save(path)
        return path
    except PermissionError:
        root, ext = os.path.splitext(path)
        alt = root + "_修订" + ext
        doc.save(alt)
        return alt

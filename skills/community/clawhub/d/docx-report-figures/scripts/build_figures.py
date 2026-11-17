#!/usr/bin/env python
"""Insert tables, data figures and in-text references into a DOCX report.

Usage:
    python build_figures.py plan.json

The plan is a JSON file (see references/plan-schema.md). The builder copies the
source document, adds `（见表N）/（见图N）` references before the final period of
the anchor paragraph, then places each exhibit right after its anchor paragraph:

    table  ->  caption (above) | three-line table | note
    figure ->  picture          | caption (below) | note

It never rewrites existing paragraphs, and it keeps the three-line table borders
in valid OOXML order so Word renders them reliably.
"""

import argparse
import copy
import json
import shutil
import sys
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT  # noqa: F401  (kept for plans that rotate)
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

ALIGN = {
    "left": WD_ALIGN_PARAGRAPH.LEFT,
    "center": WD_ALIGN_PARAGRAPH.CENTER,
    "right": WD_ALIGN_PARAGRAPH.RIGHT,
    "justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
}

DEFAULTS = {
    "cn_font": "宋体",
    "en_font": "Times New Roman",
    "table_font_pt": 9,
    "table_caption_pt": 10.5,
    "figure_caption_pt": 12,
    "note_pt": 9,
    "figure_width_cm": 14.5,
    "table_width_cm": 14.5,
    "caption_bold": True,
    "note_align": "left",
    "normalize_image_width_cm": None,
}


# --------------------------------------------------------------------------- text

def set_run_font(run, size, bold=False, style=None):
    style = style or DEFAULTS
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.name = style["en_font"]
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    rFonts.set(qn("w:ascii"), style["en_font"])
    rFonts.set(qn("w:hAnsi"), style["en_font"])
    rFonts.set(qn("w:eastAsia"), style["cn_font"])


def find_paragraph(doc, prefix):
    """Locate the paragraph an anchor belongs to.

    A prefix match is preferred; otherwise the first paragraph containing the
    anchor is used (anchors are usually a distinctive sentence fragment).
    """
    exact = [p for p in doc.paragraphs if p.text.strip().startswith(prefix)]
    if len(exact) == 1:
        return exact[0]
    loose = [p for p in doc.paragraphs if prefix in p.text]
    if len(loose) == 1:
        return loose[0]
    if len(loose) > 1:
        print("warning: anchor %r matches %d paragraphs, using the first"
              % (prefix[:20], len(loose)), file=sys.stderr)
        return loose[0]
    hint = [p.text.strip()[:40] for p in doc.paragraphs if p.text.strip()][:3]
    raise SystemExit("anchor paragraph not found: %r\nfirst paragraphs: %s" % (prefix, hint))


def insert_text_at(paragraph, offset, text, style=None):
    """Insert text at a character offset, inheriting the run formatting there."""
    pos = 0
    runs = paragraph.runs
    for run in runs:
        length = len(run.text)
        if pos <= offset <= pos + length:
            local = offset - pos
            before, after = run.text[:local], run.text[local:]
            r = copy.deepcopy(run._r)
            run.text = before
            new_r = copy.deepcopy(r)
            for t in new_r.findall(qn("w:t")):
                new_r.remove(t)
            t = OxmlElement("w:t")
            t.set(qn("xml:space"), "preserve")
            t.text = text
            new_r.append(t)
            run._r.addnext(new_r)
            if after:
                tail = copy.deepcopy(r)
                for t in tail.findall(qn("w:t")):
                    tail.remove(t)
                t2 = OxmlElement("w:t")
                t2.set(qn("xml:space"), "preserve")
                t2.text = after
                tail.append(t2)
                new_r.addnext(tail)
            return True
        pos += length
    if runs:
        last = runs[-1]
        r = copy.deepcopy(last._r)
        for t in r.findall(qn("w:t")):
            r.remove(t)
        t = OxmlElement("w:t")
        t.text = text
        r.append(t)
        last._r.addnext(r)
        return True
    return False


def add_reference(doc, anchor_prefix, text):
    p = find_paragraph(doc, anchor_prefix)
    body = p.text
    idx = body.rfind("。")
    offset = idx if idx >= 0 else len(body)
    insert_text_at(p, offset, text)
    return p


# ------------------------------------------------------------------ table helpers

def _border(el, edge, size, val="single"):
    e = OxmlElement("w:" + edge)
    e.set(qn("w:val"), val)
    if size:
        e.set(qn("w:sz"), str(size))
        e.set(qn("w:space"), "0")
        e.set(qn("w:color"), "000000")
    el.append(e)


def table_borders(table, top=12, bottom=12, header=6):
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge, size in (("top", top), ("left", 0), ("bottom", bottom),
                       ("right", 0), ("insideH", 0), ("insideV", 0)):
        _border(borders, edge, size, "none" if size == 0 else "single")
    tblPr.insert_element_before(borders, "w:shd", "w:tblLayout", "w:tblCellMar",
                                "w:tblLook", "w:tblCaption", "w:tblDescription")
    for cell in table.rows[0].cells:
        tcPr = cell._tc.get_or_add_tcPr()
        b = OxmlElement("w:tcBorders")
        _border(b, "bottom", header)
        tcPr.append(b)


def cell_margins(table, left=85, right=85, top=40, bottom=40):
    tblPr = table._tbl.tblPr
    mar = OxmlElement("w:tblCellMar")
    for edge, w in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        el = OxmlElement("w:" + edge)
        el.set(qn("w:w"), str(w))
        el.set(qn("w:type"), "dxa")
        mar.append(el)
    tblPr.insert_element_before(mar, "w:tblLook", "w:tblCaption", "w:tblDescription")


def no_split(table, repeat_header=True):
    for row in table.rows:
        trPr = row._tr.get_or_add_trPr()
        trPr.append(OxmlElement("w:cantSplit"))
        if repeat_header and row is table.rows[0]:
            trPr.append(OxmlElement("w:tblHeader"))


def set_col_widths(table, widths_cm):
    table.autofit = False
    for row in table.rows:
        for cell, w in zip(row.cells, widths_cm):
            cell.width = Cm(w)
    tblW = table._tbl.tblPr.find(qn("w:tblW"))
    if tblW is not None:
        tblW.set(qn("w:type"), "dxa")
        tblW.set(qn("w:w"), str(int(sum(widths_cm) * 567)))


def fill_cell(cell, text, size, bold=False, align="left", style=None):
    cell.vertical_alignment = 1  # center
    p = cell.paragraphs[0]
    p.alignment = ALIGN[align]
    p.paragraph_format.first_line_indent = Pt(0)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    run = p.add_run(text)
    set_run_font(run, size, bold, style)


# ------------------------------------------------------------------- block builders

def new_paragraph(doc, text, size, bold=False, align="center", style=None,
                  keep_next=False, space_before=6, space_after=3):
    p = doc.add_paragraph()
    p.alignment = ALIGN[align]
    pf = p.paragraph_format
    pf.first_line_indent = Pt(0)
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
    rf = pf.keep_with_next
    pf.keep_with_next = keep_next or rf
    run = p.add_run(text)
    set_run_font(run, size, bold, style)
    return p


def add_table_block(doc, anchor, spec, style):
    number = spec["number"]
    caption = new_paragraph(doc, "表%d　%s" % (number, spec["title"]),
                            style["table_caption_pt"], style["caption_bold"],
                            "center", style, keep_next=True)
    header, rows = spec["header"], spec["rows"]
    widths = spec["widths_cm"]
    table = doc.add_table(rows=len(rows) + 1, cols=len(header))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    align_first = spec.get("align_first", "center")
    aligns = spec.get("aligns") or (["center"] * len(header))
    for j, h in enumerate(header):
        fill_cell(table.rows[0].cells[j], h, style["table_font_pt"], True, "center", style)
    for i, row in enumerate(rows, 1):
        for j, value in enumerate(row):
            a = align_first if j == 0 else aligns[j]
            fill_cell(table.rows[i].cells[j], str(value), style["table_font_pt"], False, a, style)
    set_col_widths(table, widths)
    table_borders(table)
    cell_margins(table)
    no_split(table)

    anchor._p.addnext(caption._p)
    caption._p.addnext(table._tbl)
    node = table._tbl
    if spec.get("note"):
        note = new_paragraph(doc, spec["note"], style["note_pt"], False,
                             style["note_align"], style, space_before=2, space_after=6)
        node.addnext(note._p)
    return caption.text


def add_figure_block(doc, anchor, spec, style):
    number = spec["number"]
    width_cm = spec.get("width_cm", style["figure_width_cm"])
    holder = doc.add_paragraph()
    holder.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = holder.paragraph_format
    pf.first_line_indent = Pt(0)
    pf.space_before = Pt(6)
    pf.space_after = Pt(3)
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
    pf.keep_with_next = True
    holder.add_run().add_picture(str(spec["image"]), width=Cm(width_cm))

    caption = new_paragraph(doc, "图%d　%s" % (number, spec["title"]),
                            style["figure_caption_pt"], False, "center", style,
                            space_before=3, space_after=3)
    anchor._p.addnext(holder._p)
    holder._p.addnext(caption._p)
    node = caption._p
    if spec.get("note"):
        note = new_paragraph(doc, spec["note"], style["note_pt"], False,
                             style["note_align"], style, space_before=0, space_after=6)
        node.addnext(note._p)
    return caption.text


# ---------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    args = ap.parse_args()

    plan = json.loads(Path(args.plan).read_text(encoding="utf-8-sig"))
    style = dict(DEFAULTS)
    style.update(plan.get("style", {}))

    src, out = Path(plan["source"]), Path(plan["output"])
    if src.resolve() == out.resolve():
        raise SystemExit("output must differ from source (the source is never modified)")
    shutil.copyfile(src, out)
    doc = Document(out)

    log = []
    for ref in plan.get("references", []):
        add_reference(doc, ref["anchor"], ref["text"])
        log.append("ref  %s -> %s" % (ref["text"], ref["anchor"][:24]))

    for spec in plan.get("tables", []):
        anchor = find_paragraph(doc, spec["anchor"])
        log.append("table %s" % add_table_block(doc, anchor, spec, style))

    for spec in plan.get("figures", []):
        anchor = find_paragraph(doc, spec["anchor"])
        log.append("figure %s" % add_figure_block(doc, anchor, spec, style))

    target = style.get("normalize_image_width_cm")
    if target:
        for shape in doc.inline_shapes:
            if shape.width > Cm(target + 0.05):
                ratio = Cm(target) / shape.width
                shape.height = int(shape.height * ratio)
                shape.width = Cm(target)
        log.append("normalized legacy images to %.2f cm" % target)

    doc.save(out)
    print("\n".join(log))
    print("saved %s" % out)


if __name__ == "__main__":
    main()



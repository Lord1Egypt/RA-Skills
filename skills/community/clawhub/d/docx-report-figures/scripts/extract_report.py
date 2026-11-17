#!/usr/bin/env python
"""Dump an existing DOCX report to a UTF-8 text inventory.

Usage:
    python extract_report.py report.docx [--out dump.txt]

Output: page setup, every paragraph with its index/style/format summary,
existing tables (cell by cell) and inline images with their sizes. Read the
whole dump before planning any exhibit.
"""

import argparse
import sys
from pathlib import Path

from docx import Document
from docx.shared import Twips


def fmt_para(p):
    pf = p.paragraph_format
    bits = []
    if pf.first_line_indent is not None:
        bits.append("indent=%.2fcm" % (pf.first_line_indent.cm,))
    if pf.line_spacing is not None:
        if pf.line_spacing_rule is not None and "EXACTLY" in str(pf.line_spacing_rule):
            bits.append("ls=%.1fpt" % (pf.line_spacing.pt,))
        else:
            bits.append("ls=%s" % (round(float(pf.line_spacing), 2),))
    if pf.space_before:
        bits.append("before=%.1f" % (pf.space_before.pt,))
    if pf.space_after:
        bits.append("after=%.1f" % (pf.space_after.pt,))
    align = {1: "center", 2: "right", 3: "justify", 0: "left"}.get(
        int(pf.alignment) if pf.alignment is not None else 0, "?")
    bits.append(align)
    sizes = sorted({r.font.size.pt for r in p.runs if r.font.size})
    if sizes:
        bits.append("size=" + "/".join("%g" % s for s in sizes))
    if any(r.font.bold for r in p.runs):
        bits.append("bold")
    return ", ".join(bits)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--out", default=None)
    ap.add_argument("--max-text", type=int, default=0, help="truncate paragraph text to N chars (0 = no limit)")
    args = ap.parse_args()

    doc = Document(args.source)
    out = []
    sec = doc.sections[0]
    out.append("== PAGE ==")
    out.append("size_cm %.2f x %.2f" % (sec.page_width.cm, sec.page_height.cm))
    out.append("margins_cm L%.2f R%.2f T%.2f B%.2f" % (
        sec.left_margin.cm, sec.right_margin.cm, sec.top_margin.cm, sec.bottom_margin.cm))
    out.append("text_width_cm %.2f" % (sec.page_width.cm - sec.left_margin.cm - sec.right_margin.cm))
    out.append("")

    out.append("== PARAGRAPHS (%d) ==" % len(doc.paragraphs))
    for i, p in enumerate(doc.paragraphs):
        text = p.text.replace("\t", " ")
        if args.max_text and len(text) > args.max_text:
            text = text[:args.max_text] + "…"
        out.append("P%03d [%s | %s] %s" % (i, p.style.name, fmt_para(p), text))

    out.append("")
    out.append("== TABLES (%d) ==" % len(doc.tables))
    for ti, t in enumerate(doc.tables, 1):
        out.append("T%d: %d rows x %d cols, style=%s" % (
            ti, len(t.rows), len(t.columns), t.style.name if t.style else None))
        for r in t.rows:
            out.append("   | " + " | ".join(c.text.replace("\n", " ").strip() for c in r.cells))

    out.append("")
    out.append("== IMAGES (%d) ==" % len(doc.inline_shapes))
    for si, shape in enumerate(doc.inline_shapes, 1):
        out.append("I%d: %.2f x %.2f cm" % (si, shape.width.cm, shape.height.cm))

    text = "\n".join(out)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print("wrote %s (%d chars, %d paragraphs)" % (args.out, len(text), len(doc.paragraphs)))
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()

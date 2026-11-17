#!/usr/bin/env python
"""Report the typography of an existing DOCX so inserted exhibits can match it.

Usage:
    python inspect_format.py report.docx [--out format.txt]

Prints page geometry, the body-text formatting combination that dominates the
document, how section headings and figure/table captions are formatted today,
whether real table borders exist, and the width of existing images.
"""

import argparse
import collections
import re
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn


def para_signature(p):
    pf = p.paragraph_format
    sizes = sorted({r.font.size.pt for r in p.runs if r.font.size})
    names = sorted({r.font.name for r in p.runs if r.font.name})
    east = sorted({r._element.rPr.rFonts.get(qn("w:eastAsia"))
                   for r in p.runs if r._element.rPr is not None
                   and r._element.rPr.rFonts is not None
                   and r._element.rPr.rFonts.get(qn("w:eastAsia"))})
    return (
        "size=" + "/".join("%g" % s for s in sizes) if sizes else "size=?",
        "font=" + "/".join(names) if names else "font=?",
        "eastAsia=" + "/".join(east) if east else "eastAsia=?",
        "bold" if any(r.font.bold for r in p.runs) else "regular",
        "indent=%s" % (round(pf.first_line_indent.cm, 2) if pf.first_line_indent is not None else None),
        "ls=%s" % (round(pf.line_spacing.pt, 1) if pf.line_spacing is not None and hasattr(pf.line_spacing, "pt") else None),
        "align=%s" % (int(pf.alignment) if pf.alignment is not None else None),
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    doc = Document(args.source)
    out = []
    sec = doc.sections[0]
    text_width = sec.page_width.cm - sec.left_margin.cm - sec.right_margin.cm
    out.append("page: %.2f x %.2f cm, margins L%.2f R%.2f T%.2f B%.2f, text width %.2f cm" % (
        sec.page_width.cm, sec.page_height.cm,
        sec.left_margin.cm, sec.right_margin.cm, sec.top_margin.cm, sec.bottom_margin.cm, text_width))

    counts = collections.Counter()
    for p in doc.paragraphs:
        if p.text.strip():
            counts[para_signature(p)] += 1
    out.append("")
    out.append("== dominant paragraph formats ==")
    for sig, n in counts.most_common(8):
        out.append("%4d x %s" % (n, " | ".join(sig)))

    out.append("")
    out.append("== section headings (short bold paragraphs) ==")
    for i, p in enumerate(doc.paragraphs):
        t = p.text.strip()
        if not t:
            continue
        bold = any(r.font.bold for r in p.runs)
        sizes = [r.font.size.pt for r in p.runs if r.font.size]
        if bold and len(t) < 40 and sizes and max(sizes) >= 13:
            out.append("P%03d size=%g %s" % (i, max(sizes), t))

    out.append("")
    out.append("== caption-like paragraphs ==")
    for i, p in enumerate(doc.paragraphs):
        t = p.text.strip()
        if re.match(r"^(图|表|Figure|Table)[\s:：0-9]", t) and len(t) < 80:
            out.append("P%03d %s | %s" % (i, " | ".join(para_signature(p)), t))

    out.append("")
    out.append("== tables ==")
    for ti, t in enumerate(doc.tables, 1):
        tblPr = t._tbl.tblPr
        borders = tblPr.find(qn("w:tblBorders"))
        out.append("T%d style=%s borders=%s rows=%d cols=%d" % (
            ti, t.style.name if t.style else None,
            "present" if borders is not None else "none",
            len(t.rows), len(t.columns)))

    out.append("")
    out.append("== images ==")
    for si, shape in enumerate(doc.inline_shapes, 1):
        out.append("I%d %.2f x %.2f cm" % (si, shape.width.cm, shape.height.cm))

    text = "\n".join(out)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print("wrote %s" % args.out)
    else:
        print(text)


if __name__ == "__main__":
    main()

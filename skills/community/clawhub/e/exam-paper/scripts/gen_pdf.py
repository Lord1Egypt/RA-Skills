# -*- coding: utf-8 -*-
"""
Exam Paper PDF Generator
Reads exam data from a JSON file and produces two PDFs: exam paper + answer key.
Usage: python -X utf8 gen_pdf.py <exam.json> [--outdir DIR]
"""
import json, os, sys, platform
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
)
from reportlab.lib import colors

# ── Font ──────────────────────────────────────────────────────────────
def _find_font():
    s = platform.system()
    cands = []
    if s == "Windows":
        windir = os.environ.get("WINDIR", r"C:\Windows")
        lad = os.environ.get("LOCALAPPDATA", "")
        dirs = [os.path.join(windir, "Fonts")]
        if lad:
            dirs.append(os.path.join(lad, "Microsoft", "Windows", "Fonts"))
        for d in dirs:
            for fn, nm in [("msyh.ttc","MSYH"),("simhei.ttf","SimHei"),("simsun.ttc","SimSun")]:
                cands.append((os.path.join(d, fn), nm))
    elif s == "Darwin":
        cands.append(("/System/Library/Fonts/STHeiti Light.ttc","STHeiti"))
    else:
        cands.append(("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc","NotoSansCJK"))
    for fp, nm in cands:
        if os.path.exists(fp):
            try:
                pdfmetrics.registerFont(TTFont(nm, fp))
                return nm
            except Exception:
                pass
    raise RuntimeError("No CJK font found")

FONT = _find_font()
STYLES = getSampleStyleSheet()

def _sty(parent="Normal", **kw):
    return ParagraphStyle("_", parent=STYLES[parent], fontName=FONT, **kw)

# ── Shortcuts ─────────────────────────────────────────────────────────
def P(text, **kw):
    return Paragraph(text, _sty(**kw))

def title(text):
    return P(text, fontSize=20, alignment=TA_CENTER, spaceAfter=4)

def subtitle(text):
    return P(text, fontSize=11, alignment=TA_CENTER, spaceAfter=8)

def sec(text):
    return P(text, fontSize=13, spaceBefore=14, spaceAfter=6,
             textColor=colors.HexColor("#1a1a2e"))

def note(text):
    return P(text, fontSize=10, textColor=colors.HexColor("#555555"))

def body(text):
    return P(text, fontSize=11, leading=20)

def opt(text):
    return P(text, fontSize=11, leading=18, leftIndent=18)

def codeblock(text):
    # escape HTML
    text = text.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    lines = text.split("\n")
    html = "<br/>".join(lines)
    return P(html, fontSize=10, leading=16,
             backColor=colors.HexColor("#f5f5f5"),
             borderPadding=6, leftIndent=10, rightIndent=10,
             spaceBefore=4, spaceAfter=4)

def answer_blank(label="\u7b54\u6848\uff1a___________________________"):
    return P(label, fontSize=11, leftIndent=14)

def info_row(labels):
    cells = [P(l, fontSize=11) for l in labels]
    n = len(cells)
    w = 640 // n
    tbl = Table([cells], colWidths=[w]*n)
    tbl.setStyle(TableStyle([
        ("FONTNAME",(0,0),(-1,-1),FONT),
        ("FONTSIZE",(0,0),(-1,-1),11),
        ("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("TOPPADDING",(0,0),(-1,-1),4),
    ]))
    return tbl

# ── Build exam PDF ────────────────────────────────────────────────────
def build_exam(data, path):
    doc = SimpleDocTemplate(path, pagesize=A4,
                            leftMargin=60, rightMargin=60,
                            topMargin=50, bottomMargin=50)
    S = []
    layout = data.get("layout", {})

    S.append(title(data["title"]))
    S.append(subtitle(data.get("subtitle", "")))
    S.append(Spacer(1, 12))

    info_labels = layout.get("info_labels", [])
    if info_labels:
        S.append(info_row(info_labels))
        S.append(Spacer(1, 10))

    instruction = layout.get("instruction", "")
    if instruction:
        S.append(note(instruction))
        S.append(Spacer(1, 10))

    blank_label = layout.get("answer_label", "\u7b54\u6848\uff1a___________________________")

    for section in data["sections"]:
        stype = section["type"]
        stitle = section["title"]
        count_label = section.get("count_label", "")
        sfull = f"{stitle}\uff08{count_label}\uff09" if count_label else stitle
        S.append(sec(sfull))

        snote = section.get("note", "")
        if snote:
            S.append(note(snote))

        if stype == "choice":
            for q in section["questions"]:
                S.append(Spacer(1, 4))
                S.append(body(f'{q["num"]}. {q["text"]}'))
                for o in q.get("options", []):
                    S.append(opt(o))

        elif stype == "judgment":
            for q in section["questions"]:
                S.append(Spacer(1, 6))
                S.append(body(f'{q["num"]}. {q["text"]}\uff08  \uff09'))

        elif stype == "programming_fill":
            for q in section["questions"]:
                S.append(Spacer(1, 8))
                S.append(body(q.get("label", "")))
                desc = q.get("description", "")
                if desc:
                    S.append(P(desc, fontSize=11, leftIndent=10))
                S.append(Spacer(1, 4))
                code = q.get("code", "")
                if code:
                    S.append(codeblock(code))
                S.append(Spacer(1, 4))
                for fill in q.get("fills", []):
                    S.append(Spacer(1, 8))
                    S.append(body(f'  {fill["num"]} {fill["text"]}'))
                    S.append(Spacer(1, 22))
                    S.append(answer_blank(blank_label))

        S.append(PageBreak())

    footer = layout.get("footer", "")
    if footer:
        S.append(Spacer(1, 30))
        S.append(P(footer, fontSize=13, alignment=TA_CENTER,
                    textColor=colors.HexColor("#c0392b")))

    doc.build(S)
    print("EXAM PDF OK:", path)

# ── Build answer PDF ──────────────────────────────────────────────────
def build_answer(data, path):
    doc = SimpleDocTemplate(path, pagesize=A4,
                            leftMargin=60, rightMargin=60,
                            topMargin=50, bottomMargin=50)
    S = []
    atitle = data.get("answer_title", data["title"] + " - \u53c2\u8003\u7b54\u6848")
    S.append(title(atitle))
    S.append(Spacer(1, 12))

    for section in data["sections"]:
        stype = section["type"]
        stitle = section["title"]
        count_label = section.get("count_label", "")
        sfull = f"{stitle}\uff08{count_label}\uff09" if count_label else stitle
        S.append(sec(sfull))

        if stype == "choice":
            for q in section["questions"]:
                S.append(Spacer(1, 6))
                ans = q.get("answer", "")
                adesc = q.get("answer_desc", "")
                explain = q.get("explanation", "")
                line = f'{q["num"]}. {ans}'
                if adesc:
                    line += f'\uff08{adesc}\uff09'
                S.append(body(line))
                if explain:
                    S.append(P(f'   \u89e3\u6790\uff1a{explain}', fontSize=10, leading=16,
                               textColor=colors.HexColor("#555555")))

        elif stype == "judgment":
            for q in section["questions"]:
                S.append(Spacer(1, 6))
                ans = q.get("answer", "")
                explain = q.get("explanation", "")
                S.append(body(f'{q["num"]}. {ans}'))
                if explain:
                    S.append(P(f'   \u89e3\u6790\uff1a{explain}', fontSize=10, leading=16,
                               textColor=colors.HexColor("#555555")))

        elif stype == "programming_fill":
            S.append(Spacer(1, 8))
            S.append(body(q.get("label", "")))
            for fill in q.get("fills", []):
                S.append(body(f'  {fill["num"]} {fill.get("answer","")}'))

        S.append(PageBreak())

    doc.build(S)
    print("ANSWER PDF OK:", path)

# ── Main ──────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print("Usage: python -X utf8 gen_pdf.py <exam.json> [--outdir DIR]")
        sys.exit(1)
    json_path = sys.argv[1]
    outdir = "."
    if "--outdir" in sys.argv:
        idx = sys.argv.index("--outdir")
        if idx + 1 < len(sys.argv):
            outdir = sys.argv[idx + 1]

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    base = os.path.splitext(os.path.basename(json_path))[0]
    exam_path = os.path.join(outdir, f"{base}.pdf")
    answer_path = os.path.join(outdir, f"{base}_\u7b54\u6848.pdf")

    build_exam(data, exam_path)
    build_answer(data, answer_path)

if __name__ == "__main__":
    main()

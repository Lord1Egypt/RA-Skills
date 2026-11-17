# -*- coding: utf-8 -*-
"""中文专业PDF报告模板 — reportlab + 微软雅黑
用法：复制本文件，只改 OUT 路径和"内容区"（封面/章节/表格数据），直接运行。
验证：pymupdf 打开读 get_text 确认页数/中文/末页结论。
"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, HRFlowable, PageBreak)

# ---------- 字体（Windows 微软雅黑，ttc 必须 subfontIndex=0） ----------
FONT_DIR = "C:/Windows/Fonts"
pdfmetrics.registerFont(TTFont("MSYH",   f"{FONT_DIR}/msyh.ttc",   subfontIndex=0))
pdfmetrics.registerFont(TTFont("MSYHBD", f"{FONT_DIR}/msyhbd.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont("MSYHL",  f"{FONT_DIR}/msyhl.ttc",  subfontIndex=0))

# ---------- 颜色 ----------
C_DARK  = colors.HexColor("#1a1a2e")
C_RED   = colors.HexColor("#c0392b")
C_GREEN = colors.HexColor("#1e8449")
C_AMBER = colors.HexColor("#b9770e")
C_BLUE  = colors.HexColor("#1f4e79")
C_LGRAY = colors.HexColor("#f2f3f5")
C_MGRAY = colors.HexColor("#d9dce1")
C_WHITE = colors.white

# ---------- 样式 ----------
def st(name, **kw):
    base = dict(fontName="MSYH", fontSize=15, leading=24, textColor=C_DARK,
                    alignment=TA_JUSTIFY, spaceAfter=8)
    base.update(kw)
    return ParagraphStyle(name, **base)

S_TITLE = st("title", fontName="MSYHBD", fontSize=34, leading=44, alignment=TA_CENTER, textColor=C_DARK, spaceAfter=8)
S_SUB   = st("sub", fontName="MSYHBD", fontSize=20, leading=28, alignment=TA_CENTER, textColor=C_RED, spaceAfter=6)
S_META  = st("meta", fontName="MSYH", fontSize=13, leading=20, alignment=TA_CENTER, textColor=colors.HexColor("#666666"))
S_H1    = st("h1", fontName="MSYHBD", fontSize=21, leading=30, alignment=TA_LEFT, textColor=C_BLUE, spaceBefore=18, spaceAfter=10)
S_H2    = st("h2", fontName="MSYHBD", fontSize=17, leading=24, alignment=TA_LEFT, textColor=C_DARK, spaceBefore=14, spaceAfter=8)
S_BODY  = st("body", fontSize=15, leading=24)
S_BULLET= st("bullet", fontSize=15, leading=24, leftIndent=20, bulletIndent=6, spaceAfter=4)
S_BOX   = st("box", fontName="MSYHBD", fontSize=15, leading=24, alignment=TA_CENTER, textColor=C_WHITE)
S_SMALL = st("small", fontSize=12, leading=18, textColor=colors.HexColor("#888888"))

# ---------- 表格工具：表头深蓝白字 + 斑马纹 ----------
def make_table(data, widths, header_bg=C_BLUE, fontsize=13, align_center_cols=None):
    t = Table(data, colWidths=widths, repeatRows=1)
    style = [
        ("FONTNAME", (0,0), (-1,-1), "MSYH"),
        ("FONTSIZE", (0,0), (-1,-1), fontsize),
        ("TEXTCOLOR", (0,0), (-1,-1), C_DARK),
        ("BACKGROUND", (0,0), (-1,0), header_bg),
        ("TEXTCOLOR", (0,0), (-1,0), C_WHITE),
        ("FONTNAME", (0,0), (-1,0), "MSYHBD"),
        ("ALIGN", (0,0), (-1,0), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("GRID", (0,0), (-1,-1), 0.5, C_MGRAY),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [C_WHITE, C_LGRAY]),
    ]
    if align_center_cols:
        for c in align_center_cols:
            style.append(("ALIGN", (c,1), (c,-1), "CENTER"))
    t.setStyle(TableStyle(style))
    return t

# ================= 内容区：从这里改 =================
OUT = "output.pdf"   # ← 改成你要输出的路径
DOC_TITLE = "报告标题"          # 封面大标题
DOC_SUB   = "政治眼光 × 资本眼光 · 双光研判 · 完整尽调"
DOC_META  = "九品锦锂e 出品  |  2026-XX-XX"
DOC_SRC   = "数据来源：企业宣传册 + 36氪 / 企查查 等公开数据交叉验证"
FOOTER    = "报告名  |  九品锦锂e 出品"

doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=22*mm, rightMargin=22*mm,
                      topMargin=20*mm, bottomMargin=18*mm,
                      title=DOC_TITLE, author="九品锦锂e")

def on_page(canvas, doc_):
    canvas.saveState()
    canvas.setFont("MSYH", 8.5)
    canvas.setFillColor(colors.HexColor("#888888"))
    canvas.drawString(22*mm, 10*mm, FOOTER)
    canvas.drawRightString(A4[0]-22*mm, 10*mm, f"第 {canvas.getPageNumber()} 页")
    canvas.restoreState()

frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=on_page)])

E = []
# ---- 封面 ----
E.append(Spacer(1, 22*mm))
E.append(Paragraph(DOC_TITLE, S_TITLE))
E.append(Paragraph(DOC_SUB, S_SUB))
E.append(Spacer(1, 8*mm))
E.append(Paragraph(DOC_META, S_META))
E.append(Paragraph(DOC_SRC, S_META))
E.append(Spacer(1, 20*mm))
E.append(HRFlowable(width="100%", thickness=1.2, color=C_RED))
E.append(Spacer(1, 6*mm))
E.append(Paragraph("⚡ 核心结论", S_H2))
E.append(Paragraph("一句话结论……<span color='#c0392b'><b>强调部分</b></span>。", S_BODY))
E.append(Spacer(1, 4*mm))
E.append(Paragraph("政治 ✅ 绿灯  +  资本 ⚠️ 黄灯  =  谨慎入场", S_BOX))
E.append(PageBreak())

# ---- 正文章节示例 ----
E.append(Paragraph("一、公司基本面", S_H1))
E.append(make_table([
    ["维度", "数据", "来源"],
    ["主体", "示例：某公司，2021-08 成立", "来源"],
], [24*mm, 92*mm, 46*mm], align_center_cols=[0]))

E.append(Paragraph("二、结论与下一步", S_H1))
E.append(Paragraph("1. 行动一", S_BULLET))
E.append(Paragraph("2. 行动二", S_BULLET))
E.append(Spacer(1, 8*mm))
E.append(Paragraph("— 九品锦锂e 出品 —", st("sign", fontSize=9.5, leading=14, alignment=TA_CENTER, textColor=colors.HexColor("#999999"))))

doc.build(E)
print("PDF OK:", OUT)
print("size:", os.path.getsize(OUT), "bytes")

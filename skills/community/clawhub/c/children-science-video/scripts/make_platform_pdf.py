#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_platform_pdf.py — 双平台发布文案 Markdown → 中文 PDF

用法：
    python make_platform_pdf.py <input.md> <output.pdf>

Markdown 约定：
    # 文档大标题
    ## 章节（如平台名）
    ### 小节标题
    - 列表项 / 1. 有序列表项
    标签：#话题1 #话题2      -> 楷体强调渲染
    普通段落（**加粗** 行内支持，渲染为黑体）

依赖 reportlab；字体 SimSun / SimHei / SimKai 自动探测常见路径。
emoji 与彩色 keycap（1️⃣）会被转换为可打印形式，文末给出提示。
"""
import os
import re
import sys

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer

FONT_CANDIDATES = {
    "SimSun": [
        r"C:\Windows\Fonts\simsun.ttc",
        r"C:\Windows\Fonts\simsunb.ttf",
        "/usr/share/fonts/truetype/windows/simsun.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/System/Library/Fonts/Supplemental/Songti.ttc",
    ],
    "SimHei": [
        r"C:\Windows\Fonts\simhei.ttf",
        "/usr/share/fonts/truetype/windows/simhei.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/System/Library/Fonts/Supplemental/Hei.ttc",
    ],
    "SimKai": [
        r"C:\Windows\Fonts\simkai.ttf",
        "/usr/share/fonts/truetype/windows/simkai.ttf",
        "/System/Library/Fonts/Supplemental/Kaiti.ttc",
    ],
}

ACCENT = colors.HexColor("#E8734A")   # 暖橙（标题/小节）
INK = colors.HexColor("#333333")      # 正文深灰
MUTED = colors.HexColor("#888888")    # 弱化

KEYCAP_RE = re.compile(r"(\d)\uFE0F?\u20E3")
EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF"
    "\u20D0-\u20FF\uFE0F\u200D\uFE00-\uFE0F]"
)


def register_fonts():
    resolved = {}
    for name, paths in FONT_CANDIDATES.items():
        for p in paths:
            if os.path.exists(p):
                try:
                    pdfmetrics.registerFont(TTFont(name, p))
                    resolved[name] = p
                    break
                except Exception:
                    continue
    for need in ("SimSun", "SimHei"):
        if need not in resolved:
            sys.stderr.write(
                f"[ERROR] 缺少字体 {need}，请安装或在 FONT_CANDIDATES 中补充路径\n"
            )
            sys.exit(3)
    if "SimKai" not in resolved:
        resolved["SimKai"] = resolved["SimSun"]
        pdfmetrics.registerFont(TTFont("SimKai", resolved["SimSun"]))
    pdfmetrics.registerFontFamily(
        "SimSun", normal="SimSun", bold="SimHei",
        italic="SimKai", boldItalic="SimHei",
    )
    return resolved


def clean_text(s):
    s = KEYCAP_RE.sub(r"\1.", s)
    s = EMOJI_RE.sub("", s)
    return s.strip()


def md_inline(s):
    s = (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return s


def build_story(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    styles = {
        "h1": ParagraphStyle("h1", fontName="SimHei", fontSize=20, leading=28,
                             alignment=1, textColor=ACCENT, spaceAfter=6),
        "h2": ParagraphStyle("h2", fontName="SimHei", fontSize=15, leading=22,
                             textColor=ACCENT, spaceBefore=14, spaceAfter=6),
        "h3": ParagraphStyle("h3", fontName="SimHei", fontSize=12.5, leading=19,
                             textColor=INK, spaceBefore=8, spaceAfter=4),
        "body": ParagraphStyle("body", fontName="SimSun", fontSize=11, leading=19,
                               textColor=INK, spaceAfter=5),
        "li": ParagraphStyle("li", fontName="SimSun", fontSize=11, leading=19,
                             textColor=INK, leftIndent=16, spaceAfter=3),
        "tag": ParagraphStyle("tag", fontName="SimKai", fontSize=11, leading=19,
                              textColor=ACCENT, spaceAfter=5),
        "note": ParagraphStyle("note", fontName="SimKai", fontSize=9, leading=15,
                               textColor=MUTED, spaceBefore=10),
    }

    story, emoji_found = [], False
    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            continue
        if EMOJI_RE.search(line) or KEYCAP_RE.search(line):
            emoji_found = True
        if line.startswith("### "):
            story.append(Paragraph(md_inline(clean_text(line[4:])), styles["h3"]))
        elif line.startswith("## "):
            story.append(Paragraph(md_inline(clean_text(line[3:])), styles["h2"]))
            story.append(HRFlowable(width="100%", thickness=0.6, color=ACCENT,
                                    spaceBefore=0, spaceAfter=6))
        elif line.startswith("# "):
            story.append(Paragraph(md_inline(clean_text(line[2:])), styles["h1"]))
            story.append(HRFlowable(width="100%", thickness=1.2, color=ACCENT,
                                    spaceBefore=2, spaceAfter=10))
        elif line.startswith("标签："):
            story.append(Paragraph(md_inline(clean_text(line)), styles["tag"]))
        elif re.match(r"^(-|\d+\.)\s+", line):
            text = re.sub(r"^(-|\d+\.)\s+", "", line)
            story.append(Paragraph("• " + md_inline(clean_text(text)), styles["li"]))
        else:
            story.append(Paragraph(md_inline(clean_text(line)), styles["body"]))
    if emoji_found:
        story.append(Paragraph(
            "注：本 PDF 已剔除 emoji 与彩色序号以保证中文显示稳定，"
            "发布时请以文本版为准，emoji 在各平台可正常使用。",
            styles["note"]))
    return story


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    md_path, pdf_path = sys.argv[1], sys.argv[2]
    if not os.path.exists(md_path):
        sys.stderr.write(f"[ERROR] 输入文件不存在: {md_path}\n")
        return 2
    register_fonts()

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("SimKai", 8)
        canvas.setFillColor(MUTED)
        canvas.drawCentredString(
            A4[0] / 2, 1.2 * cm, f"儿童科普短视频 · 双平台发布文案  第 {doc.page} 页")
        canvas.restoreState()

    out_dir = os.path.dirname(os.path.abspath(pdf_path))
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    doc = SimpleDocTemplate(
        pdf_path, pagesize=A4,
        leftMargin=2.2 * cm, rightMargin=2.2 * cm,
        topMargin=2.0 * cm, bottomMargin=2.2 * cm,
        title="双平台发布文案", author="children-science-video",
    )
    doc.build(build_story(md_path), onFirstPage=footer, onLaterPages=footer)
    print(f"[OK] 已生成: {pdf_path}")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.exit(main())

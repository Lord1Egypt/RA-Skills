"""
generate_pdf.py — PDF报告生成参考模板（v6.1 consulting-report-generator）
基于 reportlab 生成专业PDF文档，CJK字体完美支持
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Theme Contract
NV = HexColor("#051C2C")
D3 = HexColor("#333333")
AB = HexColor("#006BA6")
BG = HexColor("#F2F2F2")

# 注册中文字体（macOS）
FONT_PATHS = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
]

CN_FONT = "Arial"
for fp in FONT_PATHS:
    if os.path.exists(fp):
        try:
            pdfmetrics.registerFont(TTFont("CNFont", fp))
            CN_FONT = "CNFont"
            break
        except:
            continue


def build_styles():
    """构建段落样式"""
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        "CoverTitle", parent=styles["Title"],
        fontName=CN_FONT, fontSize=26,
        textColor=NV, alignment=1, spaceAfter=20
    ))
    styles.add(ParagraphStyle(
        "HeadingCN", parent=styles["Heading1"],
        fontName=CN_FONT, fontSize=18,
        textColor=NV, spaceBefore=16, spaceAfter=8
    ))
    styles.add(ParagraphStyle(
        "SubHeadingCN", parent=styles["Heading2"],
        fontName=CN_FONT, fontSize=14,
        textColor=NV, spaceBefore=12, spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        "BodyCN", parent=styles["Normal"],
        fontName=CN_FONT, fontSize=11,
        textColor=D3, leading=18, spaceAfter=6
    ))
    return styles


def build_table(headers, rows):
    """构建表格"""
    table_data = [headers] + rows
    col_w = 460 / len(headers)
    
    t = Table(table_data, colWidths=[col_w] * len(headers))
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NV),
        ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#FFFFFF")),
        ("FONTNAME", (0, 0), (-1, -1), CN_FONT),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#CCCCCC")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#FFFFFF"), HexColor("#F2F2F2")]),
    ]))
    return t


def generate_report(title, sections, output_path):
    """
    生成完整PDF报告
    
    参数:
        title: 报告标题
        sections: [{"heading": str, "body": [str|list], ...}]
        output_path: 输出路径
    """
    styles = build_styles()
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            topMargin=2*cm, bottomMargin=2*cm)
    
    story = []
    
    # 封面
    story.append(Spacer(1, 40*mm))
    story.append(Paragraph(title, styles["CoverTitle"]))
    story.append(Spacer(1, 10*mm))
    
    # 章节
    for sec in sections:
        story.append(PageBreak())
        story.append(Paragraph(sec["heading"], styles["HeadingCN"]))
        
        for item in sec.get("body", []):
            if isinstance(item, str):
                story.append(Paragraph(item, styles["BodyCN"]))
            elif isinstance(item, list):
                for bullet in item:
                    story.append(Paragraph(f"• {bullet}", styles["BodyCN"]))
    
    doc.build(story)
    print(f"✅ PDF报告已生成: {output_path}")
    return output_path


if __name__ == "__main__":
    generate_report(
        title="精益生产体系深度解析",
        sections=[
            {"heading": "一、精益生产概述", "body": ["精益生产源于丰田生产方式..."]},
            {"heading": "二、总结", "body": ["以上为本报告核心内容"]},
        ],
        output_path="/tmp/report.pdf"
    )

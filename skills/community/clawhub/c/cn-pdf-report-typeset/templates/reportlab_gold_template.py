# -*- coding: utf-8 -*-
# PDF 生成模板（金色系）— 左对齐/大字/紧凑无孤页
# 用法: 复制本文件，只改 OUT 路径和内容区，直接运行。
# 验证: pymupdf 检查页数 / 溢出(阈值按实际边距算) / 每页字数均衡。
#
# ⚠️ 写内容时的两条硬规矩：
# 1) 字符串一律用单引号定界。工具链会把中文引号规范成半角引号，
#    外层用双引号定界会在正文引号处提前闭合，报 SyntaxError。
#    内容里的中文引号改用「」或直接在单引号串里放半角引号。
# 2) 表格单元格里可以写 <b> / <span color='#B8860B'> 内联标记，
#    make_table 现在只转义裸 & ，标签会真正生效；
#    内容里的裸尖括号要自己写成 &lt; 。
import os, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, HRFlowable, PageBreak)

# ---------- 字体（微软雅黑，.ttc 必须 subfontIndex=0） ----------
f = r'C:/Windows/Fonts'
pdfmetrics.registerFont(TTFont('MSYH', f'{f}/msyh.ttc', subfontIndex=0))
pdfmetrics.registerFont(TTFont('MSYHBD', f'{f}/msyhbd.ttc', subfontIndex=0))
pdfmetrics.registerFont(TTFont('MSYHL', f'{f}/msyhl.ttc', subfontIndex=0))

# ---------- 金色系配色（喜金喜土，忌蓝忌火） ----------
C_DARK = colors.HexColor('#1f1f1f')   # 正文近黑
C_RED = colors.HexColor('#B8860B')    # 强调/副题-深土金
C_BLUE = colors.HexColor('#C9A227')   # 表头/标题底-金属金
C_LGRAY = colors.HexColor('#FBF3DE')  # 斑马纹-浅米金
C_MGRAY = colors.HexColor('#D9C9A3')  # 网格线-浅土金
C_WHITE = colors.white


def st(name, **kw):
    # ⛔ alignment 必须 TA_LEFT，禁用 TA_JUSTIFY（中文字间距会被拉宽）
    b = dict(fontName='MSYH', fontSize=17, leading=24, textColor=C_DARK, alignment=TA_LEFT, spaceAfter=6)
    b.update(kw)
    return ParagraphStyle(name, **b)


S_TITLE = st('title', fontName='MSYHBD', fontSize=32, leading=44, alignment=TA_CENTER, spaceAfter=8)
S_SUB = st('sub', fontName='MSYHBD', fontSize=19, leading=27, alignment=TA_CENTER, textColor=C_RED, spaceAfter=6)
S_META = st('meta', fontSize=13, leading=19, alignment=TA_CENTER, textColor=colors.HexColor('#7a6a3a'))
# H1 金属金底白字
S_H1 = st('h1', fontName='MSYHBD', fontSize=22, leading=30, alignment=TA_LEFT, textColor=C_WHITE,
          spaceBefore=13, spaceAfter=8, backColor=C_BLUE, borderPadding=(5, 8, 5, 8), borderColor=C_BLUE, borderWidth=1)
S_H2 = st('h2', fontName='MSYHBD', fontSize=17.5, leading=25, alignment=TA_LEFT, spaceBefore=11, spaceAfter=6)
S_BODY = st('body', fontSize=17, leading=24)
S_BULLET = st('bullet', fontSize=17, leading=24, leftIndent=18, bulletIndent=5, spaceAfter=3)
S_BOX = st('box', fontName='MSYHBD', fontSize=15, leading=23, alignment=TA_CENTER, textColor=C_WHITE)
S_SMALL = st('small', fontSize=12.5, leading=18, textColor=colors.HexColor('#888'))
S_CODE = st('code', fontSize=13, leading=19, leftIndent=14, textColor=colors.HexColor('#8a6d1f'), spaceAfter=4)


def make_table(data, widths, header_bg=C_BLUE, fontsize=14.5, align_center_cols=None):
    def cs(bold=False):
        return ParagraphStyle('c', fontName=('MSYHBD' if bold else 'MSYH'),
                              fontSize=fontsize, leading=fontsize + 5, textColor=C_DARK)

    def wrap(v, bold=False):
        if isinstance(v, str):
            # 只转义裸 & ，保留 <b>/<span> 内联标签；否则表格里的加粗会印成字面文字
            return Paragraph(v.replace('&', '&amp;'), cs(bold))
        return v

    body = [[wrap(c, bold=(ri == 0)) for c in row] for ri, row in enumerate(data)]
    t = Table(body, colWidths=widths, repeatRows=1)
    stl = [('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
           ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
           ('LEFTPADDING', (0, 0), (-1, -1), 6), ('RIGHTPADDING', (0, 0), (-1, -1), 6),
           ('GRID', (0, 0), (-1, -1), 0.5, C_MGRAY),
           ('BACKGROUND', (0, 0), (-1, 0), header_bg),
           ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_LGRAY])]
    if align_center_cols:
        for c in align_center_cols:
            stl.append(('ALIGN', (c, 1), (c, -1), 'CENTER'))
    t.setStyle(TableStyle(stl))
    return t


# ================= 内容区：从这里改 =================
OUT = "output.pdf"   # ← 改成你要输出的路径
DOC_TITLE = '标题'
DOC_SUB = '副题（深土金色）'
DOC_META = '来源  |  日期'
FOOTER = '报告名  |  九品锦锂e 出品'
MARGIN = 17  # mm，边距收窄才装得下大字号；封面元素必须都在第1页内

# 边距 17mm；封面元素必须都在第1页内（不能溢出成空白孤页）
doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=MARGIN * mm, rightMargin=MARGIN * mm,
                      topMargin=15 * mm, bottomMargin=15 * mm, title=DOC_TITLE)
doc.addPageTemplates([PageTemplate(id='p',
    frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='f')],
    onPage=lambda c, d: (c.saveState(), c.setFont('MSYH', 8.5), c.setFillColor(colors.HexColor('#888')),
                         c.drawString(MARGIN * mm, 10 * mm, FOOTER),
                         c.drawRightString(A4[0] - MARGIN * mm, 10 * mm, f'第 {c.getPageNumber()} 页'),
                         c.restoreState()))])

E = []
# ---- 封面：元素控制在一页内，别加太多内容防止溢出成空白页 ----
E.append(Spacer(1, 10 * mm))
E.append(Paragraph(DOC_TITLE, S_TITLE))
E.append(Paragraph(DOC_SUB, S_SUB))
E.append(Spacer(1, 4 * mm))
E.append(Paragraph(DOC_META, S_META))
E.append(Spacer(1, 8 * mm))
E.append(HRFlowable(width='100%', thickness=1.2, color=C_RED))
E.append(Spacer(1, 6 * mm))
E.append(Paragraph('核心一句话', S_H2))
E.append(Paragraph('...', S_BODY))
E.append(PageBreak())

# ---- 正文（自然流动，只在封面后一个 PageBreak）----
E.append(Paragraph('一、章节', S_H1))
E.append(make_table([['列1', '列2'], ['a', 'b']], [80 * mm, 80 * mm]))
E.append(Paragraph('正文段落…', S_BODY))

doc.build(E)
print('PDF OK:', OUT, '|', os.path.getsize(OUT), 'bytes')

# ---- 生成后自检（交付前必跑，取消注释）----
# import pymupdf
# d = pymupdf.open(OUT)
# boundary = d[0].rect.width - MARGIN * mm   # 右边界按实际边距算，别写死 540
# for i, pg in enumerate(d):
#     words = pg.get_text('words')
#     over = [w for w in words if w[2] > boundary + 1 and w[4] != '页']   # 页脚永远超界，要排除
#     txt = pg.get_text()
#     print(f'第{i+1}页 字数={len(txt)}', '溢出:' + str(over[:2]) if over else '')
#     assert '<b>' not in txt and '</b>' not in txt, '内联标签被当文字渲染了，查 make_table 转义'

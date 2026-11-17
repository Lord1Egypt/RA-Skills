# -*- coding: utf-8 -*-
"""
SSC 自动化项目汇总报告 —— 横版 6 页 v1
依据 sample_ssc/P1..P6.png（用户外部出图）做原生重建。

页序：封面(P6) -> 项目进展一览(P1) -> 应用领域(P2) -> 能力沉淀(P3)
      -> 未来路线图(P4) -> 结尾(P5)

内容口径：以用户已确认的 ASCII 稿 / 原始邮件为准
（样图里出图工具把口径写偏了几处：39.3 被标成"覆盖率"、460 被标成"服务员工"、
 应用领域与能力沉淀被换成收益词。本稿已还原为邮件口径。）

原则：所有版式 / 卡片 / 药丸 / 流程圆 / 箭头 / 文字 / 图标均为 PowerPoint
原生可编辑对象，无外部图片素材。
"""
import os

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.oxml.ns import qn, nsdecls
from pptx.oxml import parse_xml

# Output directory: override with env var QIANTI_OUT; defaults to ./output
# next to this script. Never overwrites an existing artifact (auto version bump).
_OUTPUT_DIR = os.environ.get(
    "QIANTI_OUT",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "output"))
os.makedirs(_OUTPUT_DIR, exist_ok=True)


def safe_save_path(path):
    """Return a non-existing path: bump _v2/_v3... suffix instead of overwriting."""
    base, ext = os.path.splitext(path)
    cand, n = path, 1
    while os.path.exists(cand):
        n += 1
        cand = "%s_v%d%s" % (base, n, ext)
    return cand


OUTPUT = os.path.join(_OUTPUT_DIR, "SSC自动化项目汇总_6页_v1.pptx")

# ----------------------------------------------------------------- palette
NAVY       = "102850"   # 深蓝（封面底 / 卡片 / 流程圆）
NAVY_SOFT  = "2C4C74"   # 正文深蓝
YELLOW     = "FDC800"   # LEGO 黄（强调色）
BLUE       = "0046A0"   # 中蓝
RED        = "E3000B"   # LEGO 红
BG_PAGE    = "FBF9F4"   # 内容页奶白底
WHITE      = "FFFFFF"
GRAY       = "7C8798"   # 次级说明文字
TINT_YELLOW = "FDF2CE"  # 示例框浅黄
LINE_SOFT  = "E7E2D8"
COVER_SUB  = "E1E8F3"
COVER_FOOT = "C3CEDF"

FONT = "微软雅黑"
SW, SH = 13.333, 7.5


# ----------------------------------------------------------------- helpers
def E(v):
    return Inches(v)


def no_shadow(shape):
    shape.shadow.inherit = False


def no_line(shape):
    shape.line.fill.background()


def solid(shape, hexc):
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor.from_string(hexc)


def set_font(run, name=FONT):
    rPr = run._r.get_or_add_rPr()
    for tag in ('a:latin', 'a:ea', 'a:cs'):
        el = rPr.find(qn(tag))
        if el is not None:
            rPr.remove(el)
    rPr.append(parse_xml('<a:latin %s typeface="%s"/>' % (nsdecls('a'), name)))
    rPr.append(parse_xml('<a:ea %s typeface="%s"/>' % (nsdecls('a'), name)))
    rPr.append(parse_xml('<a:cs %s typeface="%s"/>' % (nsdecls('a'), name)))


def bg(slide, hexc=BG_PAGE):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = RGBColor.from_string(hexc)


def S(slide, kind, x, y, w, h, fill=None, line_c=None, lw=1.0, adj=None, adj2=None,
      rot=0):
    sh = slide.shapes.add_shape(kind, E(x), E(y), E(w), E(h))
    no_shadow(sh)
    try:
        if adj is not None:
            sh.adjustments[0] = adj
        if adj2 is not None and len(sh.adjustments) > 1:
            sh.adjustments[1] = adj2
    except Exception:
        pass
    if rot:
        sh.rotation = rot
    if fill is None:
        sh.fill.background()
    else:
        solid(sh, fill)
    if line_c is None:
        no_line(sh)
    else:
        sh.line.color.rgb = RGBColor.from_string(line_c)
        sh.line.width = Pt(lw)
    sh.text_frame.word_wrap = True
    return sh


def conn(slide, x1, y1, x2, y2, col, lw, arrow=False):
    cn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, E(x1), E(y1), E(x2), E(y2))
    cn.line.color.rgb = RGBColor.from_string(col)
    cn.line.width = Pt(lw)
    if arrow:
        ln = cn.line._get_or_add_ln()
        ln.append(parse_xml('<a:tailEnd %s type="triangle" w="med" len="med"/>'
                            % nsdecls('a')))
    return cn


def box(slide, x, y, w, h, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(E(x), E(y), E(w), E(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    return tf


def para(tf, text, size, color, bold=True, align=PP_ALIGN.LEFT, first=False,
         line_spacing=None):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    if line_spacing:
        p.line_spacing = line_spacing
    pPr = p._p.get_or_add_pPr()
    pPr.append(parse_xml('<a:buNone %s/>' % nsdecls('a')))
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = RGBColor.from_string(color)
    set_font(r)
    return p


def title_block(slide, text):
    """内容页统一标题：深蓝粗体 + 黄色短下划线。"""
    tf = box(slide, 0.72, 0.38, 9.0, 0.72, anchor=MSO_ANCHOR.MIDDLE)
    para(tf, text, 27, NAVY, bold=True, first=True)
    S(slide, MSO_SHAPE.RECTANGLE, 0.72, 1.16, 1.55, 0.085, fill=YELLOW)


# ----------------------------------------------------------------- icons
# 统一签名 (slide, cx, cy, sz, col, bgc)：col = 图标主色，bgc = 图标所在底板色。
def ic_people(s, cx, cy, sz, col, bgc=WHITE):
    """三人剪影：员工名册 / 团队。"""
    for sgn in (-1, 1):
        hx, hy = cx + sgn * sz * 0.31, cy - sz * 0.10
        S(s, MSO_SHAPE.OVAL, hx - sz * 0.098, hy - sz * 0.098,
          sz * 0.196, sz * 0.196, fill=col)
        S(s, MSO_SHAPE.ROUND_2_SAME_RECTANGLE, hx - sz * 0.155, hy + sz * 0.11,
          sz * 0.31, sz * 0.28, fill=col, adj=0.5, adj2=0)
    S(s, MSO_SHAPE.OVAL, cx - sz * 0.128, cy - sz * 0.35, sz * 0.256, sz * 0.256, fill=col)
    S(s, MSO_SHAPE.ROUND_2_SAME_RECTANGLE, cx - sz * 0.205, cy - sz * 0.05,
      sz * 0.41, sz * 0.40, fill=col, adj=0.5, adj2=0)


def ic_apps(s, cx, cy, sz, col, bgc=WHITE):
    """2x2 应用网格：平台 / M365。"""
    d, g = sz * 0.30, sz * 0.10
    o = (d + g) / 2.0
    for dx, dy in ((-o, -o), (o, -o), (-o, o), (o, o)):
        S(s, MSO_SHAPE.ROUNDED_RECTANGLE, cx + dx - d / 2, cy + dy - d / 2,
          d, d, fill=col, adj=0.28)


def ic_chat(s, cx, cy, sz, col, bgc=WHITE):
    """对话气泡：企业微信 / 员工沟通。"""
    w, h = sz * 0.80, sz * 0.60
    S(s, MSO_SHAPE.ROUNDED_RECTANGLE, cx - w / 2, cy - h * 0.62, w, h, fill=col, adj=0.30)
    S(s, MSO_SHAPE.ISOSCELES_TRIANGLE, cx - w * 0.30, cy + h * 0.28,
      w * 0.26, h * 0.34, fill=col, rot=180)
    for i in (-1, 0, 1):
        S(s, MSO_SHAPE.OVAL, cx + i * sz * 0.19 - sz * 0.048, cy - h * 0.34,
          sz * 0.096, sz * 0.096, fill=bgc)


def ic_bars(s, cx, cy, sz, col, bgc=WHITE):
    """柱状图：报表与周期性任务。"""
    w = sz * 0.175
    base = cy + sz * 0.36
    for i, f in enumerate((0.34, 0.56, 0.78)):
        h = sz * f
        S(s, MSO_SHAPE.ROUNDED_RECTANGLE, cx - sz * 0.31 + i * sz * 0.245,
          base - h, w, h, fill=col, adj=0.35)


def ic_sync(s, cx, cy, sz, col, bgc=WHITE):
    """同步：双向粗箭头。

    实测在卡片图标尺寸（约 0.5"）下，环形箭头怎么做都糊成一团：
    CIRCULAR_ARROW 是一弯细月牙；「双弧 + 双箭头」成蝴蝶结；
    「粗环缺口 + 单箭头」读起来像字母 G。双向箭头简单、饱满、零歧义。
    """
    w, h = sz * 0.86, sz * 0.48
    sh = S(s, MSO_SHAPE.LEFT_RIGHT_ARROW, cx - w / 2, cy - h / 2, w, h, fill=col)
    try:
        sh.adjustments[0] = 0.40
        sh.adjustments[1] = 0.40
    except Exception:
        pass


def ic_bell(s, cx, cy, sz, col, bgc=WHITE):
    """铃铛：团队提醒。"""
    S(s, MSO_SHAPE.OVAL, cx - sz * 0.27, cy - sz * 0.36, sz * 0.54, sz * 0.54, fill=col)
    S(s, MSO_SHAPE.RECTANGLE, cx - sz * 0.27, cy + sz * 0.12, sz * 0.54, sz * 0.15, fill=col)
    S(s, MSO_SHAPE.ROUNDED_RECTANGLE, cx - sz * 0.37, cy + sz * 0.25,
      sz * 0.74, sz * 0.10, fill=col, adj=0.5)
    S(s, MSO_SHAPE.OVAL, cx - sz * 0.068, cy + sz * 0.36, sz * 0.136, sz * 0.136, fill=col)
    S(s, MSO_SHAPE.OVAL, cx - sz * 0.05, cy - sz * 0.47, sz * 0.10, sz * 0.10, fill=col)


def ic_gear(s, cx, cy, sz, col, bgc=WHITE):
    S(s, MSO_SHAPE.GEAR_6, cx - sz * 0.36, cy - sz * 0.36, sz * 0.72, sz * 0.72, fill=col)
    S(s, MSO_SHAPE.OVAL, cx - sz * 0.13, cy - sz * 0.13, sz * 0.26, sz * 0.26, fill=bgc)


def ic_rings(s, cx, cy, sz, col, bgc=WHITE):
    """双环相扣：系统集成。"""
    for dx in (-sz * 0.15, sz * 0.15):
        S(s, MSO_SHAPE.OVAL, cx + dx - sz * 0.225, cy - sz * 0.225,
          sz * 0.45, sz * 0.45, fill=None, line_c=col, lw=sz * 6.0)


def ic_magnifier(s, cx, cy, sz, col, bgc=WHITE):
    r = sz * 0.27
    cy0 = cy - sz * 0.10
    S(s, MSO_SHAPE.OVAL, cx - r, cy0 - r, 2 * r, 2 * r,
      fill=None, line_c=col, lw=sz * 7.0)
    conn(s, cx + r * 0.68, cy0 + r * 0.68, cx + sz * 0.44, cy + sz * 0.40, col, sz * 7.0)


def ic_bulb(s, cx, cy, sz, col, bgc=WHITE):
    """灯泡：延伸机会 / 示例（小尺寸下比礼品盒更易辨识）。"""
    r = sz * 0.30
    S(s, MSO_SHAPE.OVAL, cx - r, cy - sz * 0.48, 2 * r, 2 * r, fill=col)
    S(s, MSO_SHAPE.RECTANGLE, cx - sz * 0.115, cy + sz * 0.08,
      sz * 0.23, sz * 0.20, fill=col)
    S(s, MSO_SHAPE.ROUNDED_RECTANGLE, cx - sz * 0.155, cy + sz * 0.29,
      sz * 0.31, sz * 0.13, fill=col, adj=0.5)


ICONS = {
    "people": ic_people, "apps": ic_apps, "chat": ic_chat, "bars": ic_bars,
    "sync": ic_sync, "bell": ic_bell, "gear": ic_gear, "rings": ic_rings,
    "magnifier": ic_magnifier, "bulb": ic_bulb,
}


def icon(s, name, cx, cy, sz, col, bgc=WHITE):
    ICONS[name](s, cx, cy, sz, col, bgc)


# ----------------------------------------------------------------- pages
def page1_cover(prs):
    """封面（对应样图 P6）。"""
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s, NAVY)
    S(s, MSO_SHAPE.RECTANGLE, 0.36, 0.34, 0.15, 6.82, fill=YELLOW)

    tf = box(s, 1.02, 1.24, 9.80, 1.98)
    para(tf, "SSC Automation", 52, WHITE, bold=True, first=True, line_spacing=1.02)
    para(tf, "Project", 52, WHITE, bold=True, line_spacing=1.02)

    S(s, MSO_SHAPE.RECTANGLE, 1.02, 3.30, 1.05, 0.10, fill=YELLOW)

    tf = box(s, 1.02, 3.60, 9.60, 0.50)
    para(tf, "SSC 自动化项目 · 周期性汇报", 19, COVER_SUB, bold=True, first=True)

    tf = box(s, 1.02, 4.14, 9.90, 0.62)
    para(tf, "减少重复手工 · 流程一致性 · 更好的员工体验", 14, "A9B7CC",
         bold=False, first=True)

    S(s, MSO_SHAPE.RECTANGLE, 1.02, 6.60, 11.31, 0.018, fill="2C4470")
    tf = box(s, 1.02, 6.76, 6.0, 0.42)
    para(tf, "C&B 团队", 11.5, COVER_FOOT, bold=True, first=True)
    tf = box(s, 7.80, 6.76, 4.53, 0.42)
    para(tf, "截至 2026 年 8 月 · Ken Zhang", 11.5, COVER_FOOT, bold=False,
         align=PP_ALIGN.RIGHT, first=True)

    # 装饰块整体收在页脚横线（6.60）之上
    S(s, MSO_SHAPE.STAR_5_POINT, 10.58, 4.62, 0.78, 0.78, fill=YELLOW, rot=-10)
    S(s, MSO_SHAPE.ISOSCELES_TRIANGLE, 11.50, 5.20, 0.78, 0.68, fill=YELLOW, rot=6)
    S(s, MSO_SHAPE.OVAL, 10.94, 5.84, 0.18, 0.18, fill=YELLOW)
    S(s, MSO_SHAPE.OVAL, 11.50, 6.06, 0.24, 0.24, fill=YELLOW)


def page2_metrics(prs):
    """项目进展一览（对应样图 P1）。"""
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    title_block(s, "项目进展一览")

    metrics = [
        (YELLOW, "25",   "个",     "识别机会"),
        (BLUE,   "20",   "个",     "已完成自动化"),
        (RED,    "39.3", "h / 月", "月度节省工时"),
        (NAVY,   "460",  "h / 年", "年度节省工时"),
    ]
    cw, pitch, cy, ch = 2.60, 3.10, 1.48, 2.52
    # 卡片圆角 0.0476*2.52 ≈ 0.12，与顶条 0.5*0.24 = 0.12 对齐
    for i, (col, num, unit, label) in enumerate(metrics):
        x = 0.72 + i * pitch
        S(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, cy, cw, ch, fill=WHITE, adj=0.0476)
        S(s, MSO_SHAPE.ROUND_2_SAME_RECTANGLE, x, cy, cw, 0.24,
          fill=col, adj=0.5, adj2=0)

        tf = box(s, x, cy + 0.38, cw, 1.02, anchor=MSO_ANCHOR.MIDDLE)
        para(tf, num, 48, NAVY, bold=True, align=PP_ALIGN.CENTER, first=True)

        pw = 1.32
        S(s, MSO_SHAPE.ROUNDED_RECTANGLE, x + (cw - pw) / 2, cy + 1.46,
          pw, 0.40, fill=YELLOW, adj=0.5)
        tf = box(s, x + (cw - pw) / 2, cy + 1.46, pw, 0.40, anchor=MSO_ANCHOR.MIDDLE)
        para(tf, unit, 12, NAVY, bold=True, align=PP_ALIGN.CENTER, first=True)

        tf = box(s, x, cy + 1.98, cw, 0.44, anchor=MSO_ANCHOR.MIDDLE)
        para(tf, label, 14.5, NAVY, bold=True, align=PP_ALIGN.CENTER, first=True)

    # ---- 已连接平台流程
    nodes = [
        (2.60, "people", "员工花名册", "HR 系统"),
        (6.666, "apps", "M365", "表单 · 流程"),
        (10.74, "chat", "企业微信", "通知 · 互动"),
    ]
    d, ny = 1.28, 4.48
    for cx, ick, name, sub in nodes:
        S(s, MSO_SHAPE.OVAL, cx - d / 2, ny, d, d, fill=NAVY)
        icon(s, ick, cx, ny + d / 2, d * 0.60, WHITE, NAVY)
        tf = box(s, cx - 1.30, ny + d + 0.14, 2.60, 0.40, anchor=MSO_ANCHOR.MIDDLE)
        para(tf, name, 15, NAVY, bold=True, align=PP_ALIGN.CENTER, first=True)
        tf = box(s, cx - 1.30, ny + d + 0.54, 2.60, 0.34, anchor=MSO_ANCHOR.MIDDLE)
        para(tf, sub, 11.5, GRAY, bold=False, align=PP_ALIGN.CENTER, first=True)
    for i in range(2):
        conn(s, nodes[i][0] + d / 2 + 0.16, ny + d / 2,
             nodes[i + 1][0] - d / 2 - 0.16, ny + d / 2, BLUE, 2.4, arrow=True)

    tf = box(s, 0.72, 6.88, 11.89, 0.34)
    para(tf, "* 数据为项目当前统计，可能随进展更新；工时节省基于 C&B 知识库工作量估算。",
         10.5, GRAY, bold=False, first=True)


def page3_areas(prs):
    """应用领域（对应样图 P2）。"""
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    title_block(s, "应用领域")

    # (x, y, 主题色, 图标, 标题, 要点, 英文标签, 标签文字色)
    cards = [
        (0.72, 1.42, YELLOW, "bars", "报表与周期性任务",
         ["HSS 报表 / GA 报表", "入职跨部门邮件与花名册"], "less manual work", NAVY),
        (6.9165, 1.42, BLUE, "chat", "员工沟通",
         ["入职欢迎 · 生日祝福", "T&C 到期提醒"], "better employee experience", WHITE),
        (0.72, 4.06, RED, "sync", "系统与数据同步",
         ["HC 系统 / Smartsheet / Power BI", "Power Apps / Gaia（进行中）"], "data consistency", WHITE),
        (6.9165, 4.06, YELLOW, "bell", "团队提醒",
         ["入职办理提醒", "政府申报提醒"], "faster follow-up", NAVY),
    ]
    cw, ch = 5.6965, 2.52
    for x, y, col, ick, title, bullets, tag, tag_col in cards:
        S(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, cw, ch, fill=WHITE, adj=0.0476)
        cd = 0.98
        S(s, MSO_SHAPE.OVAL, x + 0.30, y + 0.30, cd, cd, fill=col)
        icon(s, ick, x + 0.30 + cd / 2, y + 0.30 + cd / 2, cd * 0.60, WHITE, col)

        tf = box(s, x + 1.46, y + 0.30, cw - 1.78, cd, anchor=MSO_ANCHOR.MIDDLE)
        para(tf, title, 20, NAVY, bold=True, first=True)

        # 要点：2 行约 0.45"，起点 y+1.36 -> 终点 y+1.81
        tf = box(s, x + 0.36, y + 1.36, cw - 0.72, 0.60)
        for j, ln in enumerate(bullets):
            para(tf, "·  " + ln, 12.5, NAVY_SOFT, bold=False,
                 first=(j == 0), line_spacing=1.34)

        # 标签药丸：让开要点行，落在卡片下沿内侧
        pw = 0.46 + len(tag) * 0.079
        S(s, MSO_SHAPE.ROUNDED_RECTANGLE, x + 0.36, y + 1.94, pw, 0.36,
          fill=col, adj=0.5)
        tf = box(s, x + 0.36, y + 1.94, pw, 0.36, anchor=MSO_ANCHOR.MIDDLE)
        para(tf, tag, 10.5, tag_col, bold=True, align=PP_ALIGN.CENTER, first=True)


def page4_capability(prs):
    """能力沉淀（对应样图 P3）。"""
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    title_block(s, "能力沉淀")

    items = [
        (YELLOW, "gear", "工具落地", "企微 SmartSheet 自动化搭建，\n流程与表单标准化落地。"),
        (NAVY, "rings", "思维转变", "掌握工作流方法与概念，\n用自动化视角看日常任务。"),
        (RED, "magnifier", "机会识别", "从日常操作中发现\n可自动化、可复用的环节。"),
    ]
    cw, pitch, cy, ch = 3.87, 4.03, 1.48, 3.36
    # 圆角 0.0357*3.36 ≈ 0.12，与顶条 0.5*0.24 = 0.12 对齐
    for i, (col, ick, title, desc) in enumerate(items):
        x = 0.72 + i * pitch
        S(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, cy, cw, ch, fill=WHITE, adj=0.0357)
        S(s, MSO_SHAPE.ROUND_2_SAME_RECTANGLE, x, cy, cw, 0.24,
          fill=col, adj=0.5, adj2=0)

        cd = 1.26
        S(s, MSO_SHAPE.OVAL, x + (cw - cd) / 2, cy + 0.50, cd, cd, fill=col)
        icon(s, ick, x + cw / 2, cy + 0.50 + cd / 2, cd * 0.62, WHITE, col)

        tf = box(s, x, cy + 1.88, cw, 0.50, anchor=MSO_ANCHOR.MIDDLE)
        para(tf, title, 20, NAVY, bold=True, align=PP_ALIGN.CENTER, first=True)

        tf = box(s, x + 0.32, cy + 2.46, cw - 0.64, 0.78)
        for j, ln in enumerate(desc.split("\n")):
            para(tf, ln, 12.5, NAVY_SOFT, bold=False, align=PP_ALIGN.CENTER,
                 first=(j == 0), line_spacing=1.38)

    S(s, MSO_SHAPE.ISOSCELES_TRIANGLE, 1.30, 5.52, 0.44, 0.38, fill=YELLOW, rot=90)
    tf = box(s, 1.94, 5.44, 10.4, 0.54, anchor=MSO_ANCHOR.MIDDLE)
    para(tf, "从工具到思维，构建可复制的 SSC 自动化能力。", 18, NAVY, bold=True, first=True)


def page5_roadmap(prs):
    """未来路线图（对应样图 P4）。"""
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    title_block(s, "未来路线图")

    steps = [
        ("1", "Identify", "识别机会", ["梳理痛点与需求", "确定优先级"]),
        ("2", "Evaluate", "评估可行性", ["分析成本 · 收益", "制定方案"]),
        ("3", "Automate", "落地实施", ["开发 · 测试 · 上线", "持续优化"]),
        ("4", "Expand", "规模化推广", ["复制成功经验", "覆盖更多场景"]),
    ]
    d, cx0, pitch, cy = 1.70, 2.16, 3.00, 2.42
    for i, (num, en, cn, subs) in enumerate(steps):
        cx = cx0 + i * pitch
        S(s, MSO_SHAPE.OVAL, cx - d / 2, cy - d / 2, d, d, fill=NAVY)
        tf = box(s, cx - d / 2, cy - d / 2 + 0.16, d, 0.72, anchor=MSO_ANCHOR.MIDDLE)
        para(tf, num, 30, WHITE, bold=True, align=PP_ALIGN.CENTER, first=True)
        tf = box(s, cx - d / 2, cy - d / 2 + 0.86, d, 0.44, anchor=MSO_ANCHOR.MIDDLE)
        para(tf, en, 13.5, WHITE, bold=True, align=PP_ALIGN.CENTER, first=True)
        if i < 3:
            S(s, MSO_SHAPE.CHEVRON, cx + d / 2 - 0.03, cy - 0.20, 0.46, 0.40, fill=YELLOW)

        tf = box(s, cx - 1.05, cy + d / 2 + 0.08, 2.10, 0.40, anchor=MSO_ANCHOR.MIDDLE)
        para(tf, cn, 16, NAVY, bold=True, align=PP_ALIGN.CENTER, first=True)
        tf = box(s, cx - 1.05, cy + d / 2 + 0.50, 2.10, 0.50)
        for j, ln in enumerate(subs):
            para(tf, ln, 11.5, GRAY, bold=False, align=PP_ALIGN.CENTER,
                 first=(j == 0), line_spacing=1.32)

    # 循环回环：右侧下探 -> 横向左行 -> 左侧上行（箭头指向第 1 步）
    # 纵向层级：步骤说明止于 4.27 -> 回环标注 4.38~4.72 -> 回环横线 4.92 -> 示例框 5.14
    xr, xl, yb, yt = 12.44, 0.56, 4.92, 4.34
    conn(s, xr, yt, xr, yb, YELLOW, 2.6)
    conn(s, xr, yb, xl, yb, YELLOW, 2.6)
    conn(s, xl, yb, xl, yt, YELLOW, 2.6, arrow=True)
    tf = box(s, 4.90, 4.38, 3.53, 0.34, anchor=MSO_ANCHOR.MIDDLE)
    para(tf, "持续迭代 · 循环优化", 13, NAVY, bold=True, align=PP_ALIGN.CENTER, first=True)

    # 示例框
    S(s, MSO_SHAPE.ROUNDED_RECTANGLE, 0.90, 5.14, 11.50, 1.62,
      fill=TINT_YELLOW, adj=0.10)
    icon(s, "bulb", 1.62, 5.95, 0.92, NAVY, TINT_YELLOW)
    tf = box(s, 2.42, 5.34, 9.60, 0.42, anchor=MSO_ANCHOR.MIDDLE)
    para(tf, "示例", 14, NAVY, bold=True, first=True)
    tf = box(s, 2.42, 5.80, 9.70, 0.86)
    para(tf, "1. 先从高频、重复、规则明确的流程入手（如入职 / 离职、福利申请）。",
         12.5, NAVY_SOFT, bold=False, first=True, line_spacing=1.4)
    para(tf, "2. 逐步扩展到更多场景，形成可复制的标准化解决方案。",
         12.5, NAVY_SOFT, bold=False, line_spacing=1.4)


def page6_closing(prs):
    """结尾（对应样图 P5）。"""
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s, NAVY)

    tf = box(s, 1.02, 0.94, 8.0, 0.86, anchor=MSO_ANCHOR.MIDDLE)
    para(tf, "Next Steps", 40, WHITE, bold=True, first=True)
    S(s, MSO_SHAPE.RECTANGLE, 1.04, 1.94, 1.35, 0.10, fill=YELLOW)

    tf = box(s, 1.04, 2.34, 10.60, 1.14)
    para(tf, "·  继续从日常运营中识别自动化机会", 17, COVER_SUB,
         bold=False, first=True, line_spacing=1.62)
    para(tf, "·  年底前交付更详细的项目报告", 17, COVER_SUB,
         bold=False, line_spacing=1.62)

    tf = box(s, 1.02, 4.26, 9.0, 1.20, anchor=MSO_ANCHOR.MIDDLE)
    para(tf, "Thank You", 54, WHITE, bold=True, first=True)

    S(s, MSO_SHAPE.RECTANGLE, 1.02, 6.60, 11.31, 0.018, fill="2C4470")
    tf = box(s, 1.02, 6.76, 10.0, 0.40)
    para(tf, "数据来源：SSC Automation Project 周期性汇报 · 2026-08", 10.5,
         "8FA0BC", bold=False, first=True)

    # 装饰块整体收在页脚横线（6.60）之上
    S(s, MSO_SHAPE.STAR_5_POINT, 10.58, 4.38, 0.84, 0.84, fill=YELLOW, rot=-10)
    S(s, MSO_SHAPE.ISOSCELES_TRIANGLE, 11.60, 5.06, 0.84, 0.72, fill=YELLOW, rot=6)
    S(s, MSO_SHAPE.OVAL, 11.00, 5.86, 0.20, 0.20, fill=YELLOW)
    S(s, MSO_SHAPE.OVAL, 11.62, 6.10, 0.26, 0.26, fill=YELLOW)


def main():
    prs = Presentation()
    prs.slide_width = E(SW)
    prs.slide_height = E(SH)
    for fn in (page1_cover, page2_metrics, page3_areas,
               page4_capability, page5_roadmap, page6_closing):
        fn(prs)
    out = safe_save_path(OUTPUT)
    prs.save(out)
    print("saved", out)
    alt = os.path.join(_OUTPUT_DIR, "build", "deck_ssc_render.pptx")
    os.makedirs(os.path.dirname(alt), exist_ok=True)
    alt = safe_save_path(alt)
    prs.save(alt)
    print("saved", alt)


if __name__ == "__main__":
    main()

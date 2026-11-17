#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股涨停板龙虎榜深度研判报告 PPTX 生成器
严格使用 python-pptx（不使用 pptxgenjs / slidep）
- 18 页
- 3 张原生图表：饼图(涨跌家数) + 横向柱状(行业资金) + 横向柱状(概念板块)
- 中文字体统一 PingFang SC（latin + ea）
- 表格不写入 tableStyleId
"""
import copy
import os
import pathlib

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION, XL_TICK_MARK
from pptx.oxml.ns import qn
from lxml import etree

# ---------------- 设计常量（摩根士丹利投研风） ----------------
NAVY      = "002B5C"
NAVY_DK   = "001A3A"
NAVY_LT   = "0A3D6E"
GOLD      = "C5A572"
GOLD_L    = "E4D4B4"
BLUE      = "60A3D9"
BLUE_L    = "E8F1F9"
UP        = "C1272D"   # 涨 = 红（A股习惯）
DOWN      = "1E8449"   # 跌 = 绿
INK       = "12181F"
INK2      = "3C4854"
INK3      = "6B7785"
LINE      = "DDE3EA"
BG_SOFT   = "F6F8FA"
WHITE     = "FFFFFF"
FONT      = "PingFang SC"

SW = Inches(13.333)   # 16:9
SH = Inches(7.5)

OUT = pathlib.Path(os.environ.get("POUT", str(pathlib.Path(__file__).resolve().parent)))
PPTX = OUT / os.environ.get("PFILE", "涨停板龙虎榜深度研判报告-20260911.pptx")


# ---------------- 底层工具 ----------------
def set_face(run, name=FONT):
    """同时设置 latin / ea / cs 字体，保证中文不回退"""
    rPr = run._r.get_or_add_rPr()
    for tag in ("a:latin", "a:ea", "a:cs"):
        el = rPr.find(qn(tag))
        if el is None:
            el = etree.SubElement(rPr, qn(tag))
        el.set("typeface", name)


def style_run(run, size=14, bold=False, color=INK, name=FONT, italic=False):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = RGBColor.from_string(color)
    run.font.name = name
    set_face(run, name)


def no_autofit(tf):
    bodyPr = tf._txBody.find(qn("a:bodyPr"))
    for tag in ("a:normAutofit", "a:spAutoFit"):
        el = bodyPr.find(qn(tag))
        if el is not None:
            bodyPr.remove(el)
    etree.SubElement(bodyPr, qn("a:noAutofit"))


def textbox(slide, l, t, w, h):
    tb = slide.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    return tb, tf


def para(tf, first=False):
    return tf.paragraphs[0] if first else tf.add_paragraph()


def put(tf, text, first=False, size=13, bold=False, color=INK2,
        align=PP_ALIGN.LEFT, space_after=6, space_before=0, line=None):
    p = para(tf, first)
    p.alignment = align
    p.space_after = Pt(space_after)
    if space_before:
        p.space_before = Pt(space_before)
    if line:
        p.line_spacing = line
    r = p.add_run()
    r.text = text
    style_run(r, size=size, bold=bold, color=color)
    return p


def rect(slide, l, t, w, h, fill=None, line=None, line_w=0.75, shape=MSO_SHAPE.RECTANGLE):
    s = slide.shapes.add_shape(shape, l, t, w, h)
    if fill:
        s.fill.solid()
        s.fill.fore_color.rgb = RGBColor.from_string(fill)
    else:
        s.fill.background()
    if line:
        s.line.color.rgb = RGBColor.from_string(line)
        s.line.width = Pt(line_w)
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    return s


def blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


# ---------------- 页面骨架 ----------------
def page_header(slide, no, title, en, dark=False):
    """深色顶栏 + 章节编号 + 标题"""
    bar_h = Inches(0.92)
    rect(slide, 0, 0, SW, bar_h, fill=NAVY_DK if dark else NAVY)
    # 金色短竖条
    rect(slide, Inches(0.52), Inches(0.24), Inches(0.052), Inches(0.44), fill=GOLD)
    # 章节号
    _, tf = textbox(slide, Inches(0.72), Inches(0.16), Inches(0.85), Inches(0.6))
    put(tf, f"{no:02d}", first=True, size=25, bold=True, color=GOLD, space_after=0)
    # 标题
    _, tf2 = textbox(slide, Inches(1.62), Inches(0.14), Inches(11.1), Inches(0.72))
    put(tf2, title, first=True, size=19, bold=True, color=WHITE, space_after=1)
    put(tf2, en, size=9.5, bold=True, color=GOLD_L, space_after=0)
    # 页脚
    _, tf3 = textbox(slide, Inches(0.52), Inches(7.06), Inches(12.3), Inches(0.3))
    put(tf3, "A股涨停板龙虎榜深度研判报告 ｜ 交易日 2026-09-11 ｜ 数据来源：腾讯自选股",
        first=True, size=8.5, color="9AA5B1", space_after=0)


def body_tf(slide, top=1.18, left=0.52, width=12.29, height=5.6):
    _, tf = textbox(slide, Inches(left), Inches(top), Inches(width), Inches(height))
    return tf


# ---------------- 表格（无 tableStyleId） ----------------
def strip_table_style(tbl):
    tblPr = tbl._tbl.find(qn("a:tblPr"))
    if tblPr is None:
        return
    for el in tblPr.findall(qn("a:tableStyleId")):
        tblPr.remove(el)


def cell_border(cell, edges=("B",), color=LINE, w=6350):
    tcPr = cell._tc.get_or_add_tcPr()
    order = {"L": "a:lnL", "R": "a:lnR", "T": "a:lnT", "B": "a:lnB"}
    for e in edges:
        tag = order[e]
        old = tcPr.find(qn(tag))
        if old is not None:
            tcPr.remove(old)
        ln = etree.SubElement(tcPr, qn(tag))
        ln.set("w", str(w))
        ln.set("cap", "flat")
        ln.set("cmpd", "sng")
        ln.set("algn", "ctr")
        fill = etree.SubElement(ln, qn("a:solidFill"))
        clr = etree.SubElement(fill, qn("a:srgbClr"))
        clr.set("val", color)


def cell_fill(cell, color):
    cell.fill.solid()
    cell.fill.fore_color.rgb = RGBColor.from_string(color)


def put_cell(cell, text, size=10.5, bold=False, color=INK2,
             fill=None, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE):
    cell.text = ""
    tf = cell.text_frame
    tf.word_wrap = True
    no_autofit(tf)
    cell.vertical_anchor = anchor
    cell.margin_left = Inches(0.07)
    cell.margin_right = Inches(0.07)
    cell.margin_top = Inches(0.025)
    cell.margin_bottom = Inches(0.025)
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    style_run(r, size=size, bold=bold, color=color)
    if fill:
        cell_fill(cell, fill)
    cell_border(cell, edges=("B",), color=LINE, w=6350)


def make_table(slide, rows, cols, l, t, w, h, col_w=None):
    gt = slide.shapes.add_table(rows, cols, l, t, w, h)
    tbl = gt.table
    strip_table_style(tbl)
    if col_w:
        total = sum(col_w)
        for i, cw in enumerate(col_w):
            tbl.columns[i].width = Emu(int(w * cw / total))
    return tbl


def header_row(tbl, labels, size=10.5, height=Inches(0.34)):
    tbl.rows[0].height = height
    for i, lab in enumerate(labels):
        put_cell(tbl.cell(0, i), lab, size=size, bold=True, color=WHITE,
                 fill=NAVY,
                 align=PP_ALIGN.LEFT if i == 0 else PP_ALIGN.CENTER)


def data_row(tbl, ri, vals, colors=None, bolds=None, aligns=None, size=10.5, height=Inches(0.3)):
    tbl.rows[ri].height = height
    bg = WHITE if ri % 2 == 1 else "FAFBFC"
    n = len(vals)
    for ci in range(n):
        col = colors[ci] if colors else INK2
        bd = bolds[ci] if bolds else (ci == 0)
        al = aligns[ci] if aligns else (PP_ALIGN.LEFT if ci == 0 else PP_ALIGN.CENTER)
        put_cell(tbl.cell(ri, ci), vals[ci], size=size, bold=bd, color=col,
                 fill=bg, align=al)


def bullet_block(slide, l, t, w, h, items, size=12, gap=7, dot_color=GOLD):
    """圆点列表：items = [(text, bold_prefix_len_or_None), ...] 或 [text,...]"""
    _, tf = textbox(slide, Inches(l), Inches(t), Inches(w), Inches(h))
    for i, it in enumerate(items):
        if isinstance(it, tuple):
            head, rest = it
        else:
            head, rest = None, it
        p = para(tf, first=(i == 0))
        p.space_after = Pt(gap)
        p.line_spacing = 1.28
        r0 = p.add_run(); r0.text = "▪  "
        style_run(r0, size=size, bold=True, color=dot_color)
        if head:
            r1 = p.add_run(); r1.text = head
            style_run(r1, size=size, bold=True, color=NAVY)
        r2 = p.add_run(); r2.text = rest
        style_run(r2, size=size, bold=False, color=INK2)
    return tf


# ---------------- 图表样式 ----------------
def style_chart(chart, size=9.5, legend_bottom=True):
    chart.font.size = Pt(size)
    chart.font.name = FONT
    chart.font.color.rgb = RGBColor.from_string(INK2)
    # 统一字体（latin + ea）
    for r in chart._chartSpace.iter(qn("a:defRPr")):
        for tag in ("a:latin", "a:ea", "a:cs"):
            el = r.find(qn(tag))
            if el is None:
                el = etree.SubElement(r, qn(tag))
            el.set("typeface", FONT)
    if legend_bottom:
        chart.has_legend = True
        chart.legend.position = XL_LEGEND_POSITION.BOTTOM
        chart.legend.include_in_layout = False


# ==========================================================
#  开始构建
# ==========================================================
prs = Presentation()
prs.slide_width = SW
prs.slide_height = SH

# ---------- S1 封面 ----------
s = blank(prs)
rect(s, 0, 0, SW, SH, fill=NAVY_DK)
rect(s, Inches(8.6), Inches(-1.5), Inches(6.4), Inches(6.4),
     fill=None, line=NAVY_LT, line_w=1.1, shape=MSO_SHAPE.OVAL)
rect(s, Inches(10.4), Inches(3.6), Inches(4.6), Inches(4.6),
     fill=None, line="123F6B", line_w=1.0, shape=MSO_SHAPE.OVAL)
rect(s, Inches(0.9), Inches(1.5), Inches(0.09), Inches(0.62), fill=GOLD)

_, tf = textbox(s, Inches(1.18), Inches(1.48), Inches(10.5), Inches(0.4))
put(tf, "A-SHARE DAILY INTELLIGENCE  ·  DRAGON-TIGER ANALYSIS",
    first=True, size=11, bold=True, color=GOLD, space_after=0)

_, tf = textbox(s, Inches(1.18), Inches(2.06), Inches(11.2), Inches(1.5))
put(tf, "A股涨停板龙虎榜", first=True, size=42, bold=True, color=WHITE, space_after=0)
p = tf.add_paragraph(); p.space_after = Pt(0)
r = p.add_run(); r.text = "深度研判报告"
style_run(r, size=42, bold=True, color=GOLD)

rect(s, Inches(1.18), Inches(3.86), Inches(0.95), Inches(0.05), fill=GOLD)

_, tf = textbox(s, Inches(1.18), Inches(4.06), Inches(11.0), Inches(0.5))
put(tf, "交易日：2026年9月11日（星期五）　｜　全市场涨停 40 家 · 龙虎榜 57 条记录 · 803 个概念板块",
    first=True, size=14, color="D6DEE7", space_after=0)

# 四个元信息
meta = [("REPORT DATE", "2026-09-11"), ("MARKET", "沪深A股"),
        ("DATA SOURCE", "腾讯自选股"), ("CHAPTERS", "17 章")]
x = 1.18
for k, v in meta:
    _, tf = textbox(s, Inches(x), Inches(4.78), Inches(2.5), Inches(0.62))
    put(tf, k, first=True, size=8.5, bold=True, color="7C8B9C", space_after=1)
    put(tf, v, size=12.5, bold=True, color=WHITE, space_after=0)
    x += 2.72

rect(s, Inches(1.18), Inches(5.62), Inches(11.0), Inches(1.05), fill="0C2E52")
rect(s, Inches(1.18), Inches(5.62), Inches(0.055), Inches(1.05), fill=GOLD)
_, tf = textbox(s, Inches(1.45), Inches(5.76), Inches(10.5), Inches(0.9))
p = tf.paragraphs[0]; p.line_spacing = 1.3
r = p.add_run(); r.text = "一句话定性："
style_run(r, size=11.5, bold=True, color=GOLD)
r = p.add_run()
r.text = ("指数普跌、个股崩塌（上涨占比仅 11%），但资金高度收敛于「覆铜板 / PCB — 被动元件 / MLCC」"
          "这条 AI 算力硬件上游支线，龙虎榜净买入前十中 6 席归属该链条。")
style_run(r, size=11.5, color="E3EAF1")

# ---------- S2 报告结构 ----------
s = blank(prs)
page_header(s, 0, "报告结构：17 章速览", "REPORT STRUCTURE")
groups = [
    ("Ⅰ 全景诊断（01–03）", ["执行摘要与核心结论", "市场全景：指数、量能与赚钱效应", "涨跌分布与情绪温度计"]),
    ("Ⅱ 涨停与龙虎榜（04–09）", ["涨停板全景扫描", "连板梯队与高度分析", "龙虎榜总览", "净买入 TOP10 深度拆解", "净卖出 TOP10 深度拆解", "席位行为结构分析"]),
    ("Ⅲ 主线拆解（10–12）", ["主线一：覆铜板与 PCB 产业链", "主线二：被动元件与 MLCC", "主线三：军工与地面兵装"]),
    ("Ⅳ 资金与推演（13–17）", ["资金流向：行业净流入/流出 TOP10", "概念板块资金面与轮动", "个股资金与筹码结构", "斐波那契关键位与技术推演", "十大专家视角与明日策略"]),
]
x = 0.52
for title, items in groups:
    w = 3.02
    rect(s, Inches(x), Inches(1.28), Inches(w - 0.14), Inches(5.5), fill=BG_SOFT, line=LINE)
    rect(s, Inches(x), Inches(1.28), Inches(w - 0.14), Inches(0.42), fill=NAVY)
    _, tf = textbox(s, Inches(x + 0.14), Inches(1.35), Inches(w - 0.42), Inches(0.32))
    put(tf, title, first=True, size=11.5, bold=True, color=WHITE, space_after=0)
    _, tf = textbox(s, Inches(x + 0.14), Inches(1.84), Inches(w - 0.42), Inches(4.8))
    for i, it in enumerate(items):
        p = para(tf, first=(i == 0)); p.space_after = Pt(8); p.line_spacing = 1.2
        r = p.add_run(); r.text = "— "
        style_run(r, size=10, bold=True, color=GOLD)
        r = p.add_run(); r.text = it
        style_run(r, size=10, color=INK2)
    x += 3.14

# ---------- S3 执行摘要 ----------
s = blank(prs)
page_header(s, 1, "执行摘要：一句话定性", "EXECUTIVE SUMMARY")
rect(s, Inches(0.52), Inches(1.2), Inches(12.29), Inches(1.5), fill="FDFAF3", line=GOLD_L)
rect(s, Inches(0.52), Inches(1.2), Inches(0.06), Inches(1.5), fill=GOLD)
_, tf = textbox(s, Inches(0.82), Inches(1.36), Inches(11.8), Inches(1.25))
p = tf.paragraphs[0]; p.line_spacing = 1.42
r = p.add_run(); r.text = "定性："
style_run(r, size=16, bold=True, color=NAVY)
r = p.add_run()
r.text = ("大盘杀跌、单一主线逆势吸金。"
          "指数普跌且个股崩塌（上涨占比仅 11%），但资金高度收敛于「覆铜板 / PCB — 被动元件 / MLCC」"
          "这条 AI 算力硬件上游支线；半导体单日净流出 100.66 亿元居首，与通信设备（+51.12亿）、"
          "元件（+41.01亿）构成当日最尖锐的资金对立面。")
style_run(r, size=16, bold=True, color=NAVY)

cards = [
    ("上证指数", "3888.11", "-1.18%　失守3900", DOWN),
    ("两市成交额", "1.97万亿", "环比 +3247亿", NAVY),
    ("涨 / 跌家数", "643 / 4870", "上涨占比 11%", DOWN),
    ("涨停 / 跌停", "40 / 21", "跌停放大 10.5 倍", GOLD),
    ("龙虎榜净买首位", "8.12亿", "金安国纪 +7.86%", UP),
]
x = 0.52
for k, v, n, c in cards:
    w = 2.36
    rect(s, Inches(x), Inches(2.92), Inches(w - 0.13), Inches(1.28), fill=BG_SOFT, line=LINE)
    rect(s, Inches(x), Inches(2.92), Inches(w - 0.13), Inches(0.05), fill=c)
    _, tf = textbox(s, Inches(x + 0.16), Inches(3.08), Inches(w - 0.45), Inches(0.28))
    put(tf, k, first=True, size=9.5, color=INK3, space_after=0)
    _, tf = textbox(s, Inches(x + 0.16), Inches(3.36), Inches(w - 0.45), Inches(0.42))
    put(tf, v, first=True, size=20, bold=True, color=c, space_after=0)
    _, tf = textbox(s, Inches(x + 0.16), Inches(3.82), Inches(w - 0.45), Inches(0.28))
    put(tf, n, first=True, size=9, color=INK3, space_after=0)
    x += 2.46

_, tf = textbox(s, Inches(0.52), Inches(4.44), Inches(12.29), Inches(2.4))
put(tf, "五条核心结论", first=True, size=15, bold=True, color=NAVY, space_after=9)
for i, (h, b) in enumerate([
    ("大盘：", "普跌且跌破全部六条均线（MA5/10/20/60/120/250），中证500 跌 1.78% 弱于沪深300 的 0.84%，小盘股是杀跌主力。"),
    ("宽度：", "上涨 643 家 vs 下跌 4,870 家，涨跌比 0.13；但涨停仍有 40 家，结构性做多未完全熄火。"),
    ("主线：", "元件 +1.80%、通信设备 +1.66%、覆铜板 +4.31%、被动元件 +2.22%、MLCC +1.76% —— 七个上涨方向全部同源。"),
    ("资金：", "半导体净流出 100.66 亿（20日累计 -994.29 亿）居首；通信设备 +51.12 亿、元件 +41.01 亿为唯二大幅净流入。"),
    ("龙虎榜：", "净买入前十里 6 席属覆铜板/PCB/被动元件链条，主力资金形成罕见的高浓度共识。"),
], 1):
    p = para(tf); p.space_after = Pt(7); p.line_spacing = 1.3
    r = p.add_run(); r.text = f"{i}. "
    style_run(r, size=11.5, bold=True, color=GOLD)
    r = p.add_run(); r.text = h
    style_run(r, size=11.5, bold=True, color=NAVY)
    r = p.add_run(); r.text = b
    style_run(r, size=11.5, color=INK2)

# ---------- S4 涨跌分布（饼图） ----------
s = blank(prs)
page_header(s, 3, "涨跌分布与情绪温度计", "MARKET BREADTH & SENTIMENT")
_, tf = textbox(s, Inches(0.52), Inches(1.16), Inches(6.1), Inches(0.5))
put(tf, "上涨 643 家、平盘 49 家、下跌 4,870 家。上涨占比仅 11%，属于「情绪低」区间。",
    first=True, size=11.5, color=INK2, space_after=0, line=1.3)

cd = CategoryChartData()
cd.categories = ["下跌", "上涨", "其他（平盘+停牌）"]
cd.add_series("家数", (4870, 643, 61))
gf = s.shapes.add_chart(XL_CHART_TYPE.PIE, Inches(0.42), Inches(1.72), Inches(6.2), Inches(4.6), cd)
ch = gf.chart
style_chart(ch, size=11, legend_bottom=True)
ch.has_legend = True
ch.legend.position = XL_LEGEND_POSITION.BOTTOM
ch.legend.include_in_layout = False
ch.has_title = False
plot = ch.plots[0]
plot.has_data_labels = True
dl = plot.data_labels
dl.show_percentage = True
dl.show_category_name = False
dl.show_value = False
dl.number_format = '0.0%'
dl.number_format_is_linked = False
dl.position = XL_LABEL_POSITION.OUTSIDE_END
dl.font.size = Pt(11)
dl.font.bold = True
dl.font.name = FONT

# 饼图配色（跌绿 / 涨红）
pts = plot.series[0].points
for i, c in enumerate([DOWN, UP, "9AA5B1"]):
    pts[i].format.fill.solid()
    pts[i].format.fill.fore_color.rgb = RGBColor.from_string(c)
    pts[i].format.line.color.rgb = RGBColor.from_string(WHITE)
    pts[i].format.line.width = Pt(1.5)

rect(s, Inches(6.78), Inches(1.72), Inches(6.03), Inches(4.6), fill=BG_SOFT, line=LINE)
_, tf = textbox(s, Inches(7.0), Inches(1.9), Inches(5.62), Inches(4.3))
put(tf, "情绪判定", first=True, size=13.5, bold=True, color=NAVY, space_after=8)
put(tf, "上涨占比 11%（情绪低）＋ 跌停 21 家（较前日 2 家放大 10.5 倍）＋ 涨停 40 家（仍在中性区间）",
    size=11, color=INK2, space_after=9, line=1.32)
put(tf, "→ 市场处于「广度崩塌但结构性做多未熄火」的状态。",
    size=11.5, bold=True, color=NAVY, space_after=9, line=1.32)
put(tf, "这是典型的存量博弈末期特征：大部分股票在被抽血，资金全部押注在极少数主线上。这种状态下，不参与主线就是亏损，参与了主线才是博弈。",
    size=11, color=INK2, space_after=10, line=1.32)
put(tf, "分布明细", size=12, bold=True, color=NAVY, space_after=7)
for txt in ["涨停 40 家 ／ 跌停 21 家；涨幅>7% 30 家、跌幅>7% 85 家",
            "跌幅 2%~5% 档堆积 2,778 家，占全市场 50.0%",
            "跌幅 >5% 合计 294 家（占 5.3%）—— 是普跌，不是跳水"]:
    p = tf.add_paragraph(); p.space_after = Pt(5); p.line_spacing = 1.26
    r = p.add_run(); r.text = "▪  "
    style_run(r, size=10.5, bold=True, color=GOLD)
    r = p.add_run(); r.text = txt
    style_run(r, size=10.5, color=INK2)

# ---------- S5 涨停板全景扫描 ----------
s = blank(prs)
page_header(s, 4, "涨停板全景扫描", "LIMIT-UP LANDSCAPE")
_, tf = textbox(s, Inches(0.52), Inches(1.14), Inches(12.29), Inches(0.5))
put(tf, "全市场涨停 40 家、跌停 21 家。与前一交易日（涨停38 / 跌停仅2）相比，涨停家数持平，但跌停家数从 2 家暴涨至 21 家。",
    first=True, size=11.5, color=INK2, space_after=0, line=1.3)

tbl = make_table(s, 11, 6, Inches(0.52), Inches(1.72), Inches(12.29), Inches(3.9),
                 col_w=[0.6, 1.6, 2.2, 2.4, 3.4, 1.6])
header_row(tbl, ["#", "代码", "名称", "封单量（手）", "所属方向", "信号强度"])
rows = [
    ("1", "sz002790", "瑞尔特", "440,559", "家居用品 / 3连板", "极强", GOLD),
    ("2", "sz002377", "国创高新", "301,084", "基础建设 / 2连板", "强", INK2),
    ("3", "sh600667", "太极实业", "271,258", "半导体封测 / 工程", "强", INK2),
    ("4", "sz002204", "大连重工", "211,248", "重型装备", "强", INK2),
    ("5", "sh600744", "华银电力", "205,115", "电力", "强", INK2),
    ("6", "sz002531", "天顺风能", "132,920", "风电设备", "中", INK3),
    ("7", "sz000993", "闽东电力", "96,880", "电力 / 2连板", "中", INK3),
    ("8", "sh600712", "南宁百货", "92,439", "一般零售", "中", INK3),
    ("9", "sh603421", "鼎信通讯", "89,711", "通信设备 / 2连板", "中", INK3),
    ("10", "sh600491", "ST龙元", "87,096", "房屋建设 / ST", "弱", INK3),
]
for i, (a, b, c, d, e, f, col) in enumerate(rows, 1):
    data_row(tbl, i, [a, b, c, d, e, f],
             colors=[INK3, INK3, NAVY, UP if i <= 5 else INK2, INK2, col],
             bolds=[False, False, True, (i <= 5), False, True],
             aligns=[PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.LEFT,
                     PP_ALIGN.RIGHT, PP_ALIGN.LEFT, PP_ALIGN.CENTER],
             size=10, height=Inches(0.31))

_, tf = textbox(s, Inches(0.52), Inches(5.78), Inches(12.29), Inches(1.2))
p = tf.paragraphs[0]; p.line_spacing = 1.34
r = p.add_run(); r.text = "警示："
style_run(r, size=11.5, bold=True, color=UP)
r = p.add_run()
r.text = ("封单量最大的是瑞尔特（44.06 万手，家居用品）—— 孤立个股、无板块效应，属资金自嗨型涨停，次日接力风险高。"
          "单纯看封单量会误判，必须结合板块宽度。注：连板与封单数据来自 2026-09-10（上游滞后 1 个交易日）。")
style_run(r, size=11.5, color=INK2)

# ---------- S6 连板梯队 ----------
s = blank(prs)
page_header(s, 5, "连板梯队与高度分析", "CONSECUTIVE LIMIT-UP LADDER")
_, tf = textbox(s, Inches(0.52), Inches(1.14), Inches(12.29), Inches(0.4))
put(tf, "全市场有连板记录的个股 40 只，但最高高度只有 4 板。高度不足 = 没有龙头带动情绪。",
    first=True, size=11.5, color=INK2, space_after=0)

ladder = [
    ("4板", "桂林旅游（sz000978）　旅游及景区　— 孤高标", "1 只", UP),
    ("3板", "瑞尔特（sz002790）家居用品　·　云煤能源（sh600792）煤炭开采", "2 只", "D96A2B"),
    ("2板", "新农开发 · 国创高新 · 鼎信通讯 · 闽东电力 · 渝三峡Ａ · 长城电工", "6 只", GOLD),
    ("首板", "津药药业 · 九鼎新材 · 金安国纪 · 京基智农 · 水发燃气 · 诚邦股份\n美能能源 · 湖南发展 · 凯盛新能 · 新力金融 · 华银电力 · 游族网络\n天顺风能 · 南宁百货 · 大连重工 · 克明食品 · 万和电气 等", "30 只", BLUE),
]
y = 1.74
for lv, names, cnt, col in ladder:
    h = 1.62 if lv == "首板" else 0.72
    rect(s, Inches(0.52), Inches(y), Inches(1.05), Inches(h - 0.1), fill=col)
    _, tf = textbox(s, Inches(0.52), Inches(y + (0.1 if lv == "首板" else 0.1)), Inches(1.05), Inches(0.5))
    put(tf, lv, first=True, size=17, bold=True, color=WHITE, align=PP_ALIGN.CENTER, space_after=0)
    rect(s, Inches(1.72), Inches(y), Inches(10.0), Inches(h - 0.1), fill=BG_SOFT, line=LINE)
    _, tf = textbox(s, Inches(1.92), Inches(y + 0.15), Inches(9.6), Inches(h - 0.34))
    first = True
    for line in names.split("\n"):
        put(tf, line, first=first, size=11, color=INK2, space_after=3, line=1.24)
        first = False
    _, tf = textbox(s, Inches(11.86), Inches(y + 0.18), Inches(0.95), Inches(0.42))
    put(tf, cnt, first=True, size=13, bold=True, color=col, align=PP_ALIGN.RIGHT, space_after=0)
    y += h

rect(s, Inches(0.52), Inches(6.06), Inches(12.29), Inches(0.92), fill="FDF3F3", line="F2C9C9")
rect(s, Inches(0.52), Inches(6.06), Inches(0.055), Inches(0.92), fill=UP)
_, tf = textbox(s, Inches(0.78), Inches(6.18), Inches(11.9), Inches(0.72))
p = tf.paragraphs[0]; p.line_spacing = 1.3
r = p.add_run(); r.text = "梯队结论："
style_run(r, size=11.5, bold=True, color=UP)
r = p.add_run()
r.text = ("高度 4 板 + 首板占 75% + 3 板以上仅 3 只 → 这是「低位活跃、高位死亡」的市场。"
          "操作含义：不宜追高，只宜在首板/2 板做低吸；晋级到 3 板后风险收益比急剧恶化。")
style_run(r, size=11.5, color=INK2)

# ---------- S7 龙虎榜总览 ----------
s = blank(prs)
page_header(s, 6, "龙虎榜总览：全市场 57 条记录", "DRAGON-TIGER LIST OVERVIEW")
cards = [
    ("总记录数", "57", "含同一股多榜重复", NAVY),
    ("净买入条目", "25", "买方 25 条", UP),
    ("净卖出条目", "32", "卖方 32 条", DOWN),
    ("最大净买入", "+8.12亿", "金安国纪 +7.86%", UP),
    ("最大净卖出", "-2.31亿", "金健米业 -3.21%", DOWN),
]
x = 0.52
for k, v, n, c in cards:
    w = 2.36
    rect(s, Inches(x), Inches(1.24), Inches(w - 0.13), Inches(1.2), fill=BG_SOFT, line=LINE)
    rect(s, Inches(x), Inches(1.24), Inches(w - 0.13), Inches(0.05), fill=c)
    _, tf = textbox(s, Inches(x + 0.16), Inches(1.4), Inches(w - 0.45), Inches(0.26))
    put(tf, k, first=True, size=9.5, color=INK3, space_after=0)
    _, tf = textbox(s, Inches(x + 0.16), Inches(1.66), Inches(w - 0.45), Inches(0.4))
    put(tf, v, first=True, size=19, bold=True, color=c, space_after=0)
    _, tf = textbox(s, Inches(x + 0.16), Inches(2.08), Inches(w - 0.45), Inches(0.26))
    put(tf, n, first=True, size=9, color=INK3, space_after=0)
    x += 2.46

bullet_block(s, 0.52, 2.72, 12.29, 1.9, [
    ("净买入前三：", "金安国纪（+8.12亿，覆铜板基材）、长盈通（+5.21亿，光纤）、博云新材（+4.03亿，航空装备）"),
    ("净卖出前三：", "金健米业（-2.31亿，农产品加工）、红棉股份（-1.30亿，跌停）、逸豪新材（-1.25亿，PCB 铜箔）"),
    ("结构特征：", "净卖出条目（32）多于净买入（25），与大盘普跌格局一致；但头部的绝对金额被买方垄断"),
], size=11.5, gap=6)

rect(s, Inches(0.52), Inches(4.72), Inches(12.29), Inches(1.62), fill=BG_SOFT, line=LINE)
rect(s, Inches(0.52), Inches(4.72), Inches(0.055), Inches(1.62), fill=GOLD)
_, tf = textbox(s, Inches(0.8), Inches(4.86), Inches(11.85), Inches(1.4))
put(tf, "龙虎榜的核心信息量不在于「谁上榜」，而在于「钱流向哪个行业」",
    first=True, size=13, bold=True, color=NAVY, space_after=8)
p = tf.add_paragraph(); p.line_spacing = 1.32
r = p.add_run()
r.text = ("净买入前十中 6 只归属「覆铜板 / PCB / 被动元件」链条（金安国纪、嘉立创、崇达技术、风华高科、九鼎新材、神宇股份），"
          "另 1 只属军工（博云新材）。这与行业资金流向（通信设备 +51.12亿、元件 +41.01亿）在方向上形成交叉验证 —— "
          "两条独立数据链指向同一结论，可信度显著提高。")
style_run(r, size=11, color=INK2)

# ---------- S8 净买入 TOP10 ----------
s = blank(prs)
page_header(s, 7, "龙虎榜净买入 TOP 10 深度拆解", "TOP NET BUY BREAKDOWN")
tbl = make_table(s, 11, 5, Inches(0.52), Inches(1.2), Inches(12.29), Inches(4.5),
                 col_w=[2.9, 1.7, 2.3, 1.7, 1.8])
header_row(tbl, ["名称 / 代码", "涨跌幅", "净买入额", "成交额", "资金属性"])
rows = [
    ("金安国纪  sz002636", "+7.86%", "+8.12亿", "33.6亿", "主线龙头 / 强共识", UP, GOLD),
    ("长盈通  sh688143", "+15.49%", "+5.21亿", "11.0亿", "光纤 / 科创弹性", UP, INK2),
    ("博云新材  sz002297", "+7.44%", "+4.03亿", "10.2亿", "军工新材料", UP, INK2),
    ("风华高科  sz000636", "+10.00%", "+2.92亿", "28.4亿", "MLCC 龙头 / 封板", UP, GOLD),
    ("风语筑  sh603466", "+10.03%", "+1.96亿", "3.3亿", "数字媒体 / 净买占比高", UP, INK2),
    ("九鼎新材  sz002201", "+10.02%", "+1.94亿", "5.6亿", "电子级玻纤布 / 封板", UP, GOLD),
    ("嘉立创  sz001232", "+10.00%", "+1.87亿", "4.7亿", "PCB 打样平台", UP, GOLD),
    ("神宇股份  sz300563", "+19.98%", "+1.27亿", "2.1亿", "通信设备 / 20cm 涨停", UP, GOLD),
    ("崇达技术  sz002815", "+10.03%", "+1.09亿", "8.8亿", "PCB / 元件行业龙头", UP, GOLD),
    ("再升科技  sh603601", "+8.33%", "+0.90亿", "13.9亿", "玻纤滤材 / 双边巨量", UP, INK3),
]
for i, (a, b, c, d, e, col, ec) in enumerate(rows, 1):
    data_row(tbl, i, [a, b, c, d, e],
             colors=[NAVY, UP, UP, INK2, ec],
             bolds=[True, True, True, False, True],
             aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.RIGHT, PP_ALIGN.RIGHT, PP_ALIGN.LEFT],
             size=10, height=Inches(0.4))

_, tf = textbox(s, Inches(0.52), Inches(5.86), Inches(12.29), Inches(1.1))
p = tf.paragraphs[0]; p.line_spacing = 1.32
r = p.add_run(); r.text = "三个结构性发现："
style_run(r, size=11.5, bold=True, color=NAVY)
r = p.add_run()
r.text = ("① 前十中 6 席属覆铜板/PCB/被动元件链条；② 涨停股占 6 席，资金偏好「已封板」的确定性；"
          "③ 净买入呈极端长尾——第 1 名 8.12 亿是第 10 名 0.90 亿的 9 倍，资金极度集中在最头部 1~2 只标的。")
style_run(r, size=11.5, color=INK2)

# ---------- S9 净卖出 + 链条分歧 ----------
s = blank(prs)
page_header(s, 8, "龙虎榜净卖出 TOP 10 与链条内部分歧", "TOP NET SELL & DIVERGENCE")
tbl = make_table(s, 9, 5, Inches(0.52), Inches(1.2), Inches(12.29), Inches(3.5),
                 col_w=[2.9, 1.6, 2.0, 3.2, 2.6])
header_row(tbl, ["名称 / 代码", "涨跌幅", "净卖出", "所属方向", "信号"])
rows = [
    ("金健米业  sh600127", "-3.21%", "-2.31亿", "农产品加工 / 种植业", "资金撤离"),
    ("红棉股份  sz000523", "-10.09%", "-1.30亿", "纺织 / 跌停", "跌停双杀"),
    ("逸豪新材  sz301176", "+7.28%", "-1.25亿", "PCB 铜箔", "链条分歧"),
    ("北方铜业  sz000737", "-10.01%", "-1.15亿", "工业金属 / 跌停", "有色撤离"),
    ("日出东方  sh603366", "-10.02%", "-0.60亿", "家电 / 跌停", "跌停"),
    ("云煤能源  sh600792", "-4.81%", "-0.59亿", "煤炭 / 3连板失败", "高标退潮"),
    ("超声电子  sz000823", "+10.00%", "-0.53亿", "PCB（涨停却被卖）", "涨停出货"),
    ("敦煌种业  sh600354", "-4.19%", "-0.51亿", "种植业", "资金撤离"),
]
for i, (a, b, c, d, e) in enumerate(rows, 1):
    warn = "分歧" in e or "出货" in e or "退潮" in e
    data_row(tbl, i, [a, b, c, d, e],
             colors=[NAVY, DOWN, DOWN, INK2, UP if warn else INK3],
             bolds=[True, True, True, False, True],
             aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.RIGHT, PP_ALIGN.LEFT, PP_ALIGN.LEFT],
             size=10, height=Inches(0.38))

rect(s, Inches(0.52), Inches(4.88), Inches(12.29), Inches(1.95), fill="FDF3F3", line="F2C9C9")
rect(s, Inches(0.52), Inches(4.88), Inches(0.055), Inches(1.95), fill=UP)
_, tf = textbox(s, Inches(0.8), Inches(5.02), Inches(11.85), Inches(1.7))
put(tf, "最重要的一条警报：链条内部分歧已经出现", first=True, size=13.5, bold=True, color=UP, space_after=8)
p = tf.add_paragraph(); p.line_spacing = 1.32
r = p.add_run()
r.text = ("逸豪新材（PCB 铜箔）净卖出 1.25 亿、超声电子（PCB）涨停却净卖出 0.53 亿。而同链条的金安国纪被净买入 8.12 亿、"
          "嘉立创 +1.87 亿、崇达技术 +1.09 亿。")
style_run(r, size=11, color=INK2)
p = tf.add_paragraph(); p.space_before = Pt(7); p.line_spacing = 1.32
r = p.add_run()
r.text = ("含义：资金不是在「买 PCB 板块」，而是在「精选 PCB 板块里的特定标的」——上游材料（覆铜板/玻纤布/MLCC）被买，"
          "中游制板（铜箔/常规 PCB）被卖。不要用「买板块」的思路做这条链。")
style_run(r, size=11, bold=True, color=NAVY)

# ---------- S10 席位行为 ----------
s = blank(prs)
page_header(s, 9, "席位行为结构分析", "SEAT BEHAVIOUR ANALYSIS")
_, tf = textbox(s, Inches(0.52), Inches(1.14), Inches(12.29), Inches(0.5))
put(tf, "当日机构席位榜（jg）与游资席位榜（yzb）均为空，仅返回全市场合并榜 —— 上榜资金以营业部席位为主导，缺乏机构参与痕迹。",
    first=True, size=11.5, color=INK2, space_after=0, line=1.3)

tbl = make_table(s, 4, 5, Inches(0.52), Inches(1.76), Inches(12.29), Inches(2.1),
                 col_w=[2.4, 3.5, 3.3, 1.5, 2.6])
header_row(tbl, ["行为类型", "特征", "当日典型案例", "买/卖比", "研判"])
rows = [
    ("单向强攻型", "买入远大于卖出，净买占比高", "神宇股份（1.66亿/0.39亿）\n风语筑（2.61亿/0.65亿）", "4.26\n4.01", "资金一致，短期强势"),
    ("双边巨量型", "买卖双侧均超 4 亿，换手极高", "超声电子（8.09亿/8.52亿）\n再升科技（7.38亿/6.48亿）", "0.95\n1.14", "对倒/分歧，博弈激烈"),
    ("温和净买入型", "买卖适中，净额为正但不极端", "崇达技术（4.92亿/3.83亿）\n九鼎新材（3.77亿/1.83亿）", "1.28\n2.06", "健康承接"),
]
for i, (a, b, c, d, e) in enumerate(rows, 1):
    col = UP if i == 2 else (DOWN if i == 3 else INK2)
    data_row(tbl, i, [a, b, c, d, e],
             colors=[NAVY, INK2, INK2, col, col],
             bolds=[True, False, False, True, True],
             aligns=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.LEFT],
             size=10, height=Inches(0.6))

rect(s, Inches(0.52), Inches(4.12), Inches(12.29), Inches(2.6), fill="FDFAF3", line=GOLD_L)
rect(s, Inches(0.52), Inches(4.12), Inches(0.055), Inches(2.6), fill=GOLD)
_, tf = textbox(s, Inches(0.8), Inches(4.26), Inches(11.85), Inches(2.35))
put(tf, "关键识别规则（可复用）", first=True, size=13.5, bold=True, color=NAVY, space_after=8)
p = tf.add_paragraph(); p.line_spacing = 1.32
r = p.add_run(); r.text = "「涨停 + 龙虎榜净卖出」是危险的卖出信号。 "
style_run(r, size=11.5, bold=True, color=UP)
r = p.add_run()
r.text = "当日超声电子最典型：股价封在涨停板上看似强势，但龙虎榜显示资金合计净流出近 1 亿元 —— 有资金借涨停板出货。"
style_run(r, size=11.5, color=INK2)
p = tf.add_paragraph(); p.space_before = Pt(8); p.line_spacing = 1.32
r = p.add_run(); r.text = "反过来，「未封板 + 巨额净买入」是更强的信号。 "
style_run(r, size=11.5, bold=True, color=UP)
r = p.add_run()
r.text = "如金安国纪涨 7.86% 未封板、净买入 8.12 亿，说明资金在盘中主动承接。切勿以涨跌幅作为唯一的强弱判断依据。"
style_run(r, size=11.5, color=INK2)

# ---------- S11 主线一 ----------
s = blank(prs)
page_header(s, 10, "主线一：覆铜板与 PCB 产业链", "MAIN LINE I — CCL & PCB")
_, tf = textbox(s, Inches(0.52), Inches(1.14), Inches(12.29), Inches(0.44))
put(tf, "当日唯一的、也是最强的 主线。概念板块涨幅第一「覆铜板 +4.31%」，行业端「元件 +1.80%」且主力净流入 41.01 亿元居第二。",
    first=True, size=11.5, color=INK2, space_after=0)

tbl = make_table(s, 7, 4, Inches(0.52), Inches(1.72), Inches(12.29), Inches(2.55),
                 col_w=[3.0, 4.4, 2.4, 2.5])
header_row(tbl, ["产业链环节", "代表标的", "涨跌幅", "龙虎榜净额"])
rows = [
    ("电子级玻纤布", "金安国纪 / 九鼎新材 / 山东玻纤", "+7.86% / +10.02% / +6.64%", "+8.12亿 / +1.94亿 / +0.52亿", UP, UP),
    ("覆铜板（CCL）", "金安国纪（主业）", "+7.86%", "+8.12亿", UP, UP),
    ("PCB 制造", "嘉立创 / 崇达技术 / 骏亚科技 / 博敏电子 / 中京电子 / 超声电子", "+10.00% / +10.03% / +10.03%\n+10.01% / +2.09% / +10.00%", "+1.87亿 / +1.09亿 / +0.37亿\n+0.26亿 / -0.33亿 / -0.53亿", UP, DOWN),
    ("PCB 铜箔", "逸豪新材", "+7.28%", "-1.25亿", UP, DOWN),
    ("陶瓷基板", "概念板块", "+1.74%", "—", UP, INK2),
    ("电子布", "概念板块", "+1.73%", "—", UP, INK2),
]
for i, (a, b, c, d, c1, c2) in enumerate(rows, 1):
    data_row(tbl, i, [a, b, c, d],
             colors=[NAVY, INK2, c1, c2],
             bolds=[True, False, True, True],
             aligns=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.RIGHT],
             size=9.5, height=Inches(0.34))

_, tf = textbox(s, Inches(0.52), Inches(4.56), Inches(12.29), Inches(2.3))
put(tf, "驱动逻辑的三层推演", first=True, size=13.5, bold=True, color=NAVY, space_after=8)
for h, b in [
    ("需求端：", "AI 服务器与高速交换机放量。PCB 从普通 FR-4 升级到 M6/M7/M8 级高频高速材料，层数从 8-12 层提升至 16-20 层以上，单台服务器覆铜板用量与价值量同步跃升。"),
    ("供给端：", "Low-Dk / Low-Df 电子级玻纤布与特种树脂全球产能高度集中，扩产周期 18-24 个月。供给刚性 + 需求陡增 = 涨价传导能力极强。"),
    ("资金端：", "龙虎榜净买入前十 6 席属此链条，行业资金端「元件 +41.01亿」居第二、「通信设备 +51.12亿」居第一，两条独立数据链交叉验证。"),
]:
    p = tf.add_paragraph(); p.space_after = Pt(7); p.line_spacing = 1.3
    r = p.add_run(); r.text = "▪  "
    style_run(r, size=11, bold=True, color=GOLD)
    r = p.add_run(); r.text = h
    style_run(r, size=11, bold=True, color=NAVY)
    r = p.add_run(); r.text = b
    style_run(r, size=11, color=INK2)
p = tf.add_paragraph(); p.space_before = Pt(6); p.line_spacing = 1.3
r = p.add_run(); r.text = "风险："
style_run(r, size=11, bold=True, color=UP)
r = p.add_run()
r.text = "链条内部已分化（中游制板被净卖出）；龙头金安国纪未封板，缺少情绪锚定；无第二主线承接，一旦退潮市场没有接力方向。"
style_run(r, size=11, color=INK2)

# ---------- S12 主线二 ----------
s = blank(prs)
page_header(s, 11, "主线二：被动元件与 MLCC", "MAIN LINE II — PASSIVE COMPONENTS")
_, tf = textbox(s, Inches(0.52), Inches(1.14), Inches(12.29), Inches(0.44))
put(tf, "被动元件是覆铜板主线的孪生支线 —— 两者同属「AI 硬件上游被忽略的通用件」。被动元件概念 +2.22%、MLCC +1.76%。",
    first=True, size=11.5, color=INK2, space_after=0)

tbl = make_table(s, 5, 5, Inches(0.52), Inches(1.68), Inches(12.29), Inches(1.95),
                 col_w=[2.2, 2.2, 1.7, 1.8, 4.4])
header_row(tbl, ["标的", "代码", "涨跌幅", "龙虎榜净额", "研判"])
rows = [
    ("风华高科", "sz000636", "+10.00%", "+2.92亿", "MLCC 龙头 / 封板 / 板块共振 —— 当日唯一「三确认」标的"),
    ("九鼎新材", "sz002201", "+10.02%", "+1.94亿", "电子级玻纤布 / 封板，与 MLCC 形成材料端双子星"),
    ("山东玻纤", "sh605006", "+6.64%", "+0.52亿", "玻纤 / 未封板"),
    ("中国巨石", "sh600176", "+2.76%", "—", "玻纤龙头 / 权重股，涨幅温和"),
]
for i, (a, b, c, d, e) in enumerate(rows, 1):
    data_row(tbl, i, [a, b, c, d, e],
             colors=[NAVY, INK3, UP, UP, INK2],
             bolds=[True, False, True, True, False],
             aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.RIGHT, PP_ALIGN.LEFT],
             size=10, height=Inches(0.38))

rect(s, Inches(0.52), Inches(3.88), Inches(6.02), Inches(2.85), fill=BG_SOFT, line=LINE)
_, tf = textbox(s, Inches(0.74), Inches(4.02), Inches(5.6), Inches(2.6))
put(tf, "驱动逻辑：单机用量倍数效应", first=True, size=12.5, bold=True, color=NAVY, space_after=8)
for t in ["AI 服务器单机 MLCC 用量是通用服务器的 4~8 倍",
          "高容值、小型化（0201/01005）产品结构性紧缺",
          "下游原厂已多次发涨价函，价格弹性直接体现在毛利上",
          "与覆铜板不同：MLCC 是纯通用件，一旦进入涨价周期，覆盖面更广、持续更久"]:
    p = tf.add_paragraph(); p.space_after = Pt(6); p.line_spacing = 1.26
    r = p.add_run(); r.text = "▪  "
    style_run(r, size=10.5, bold=True, color=GOLD)
    r = p.add_run(); r.text = t
    style_run(r, size=10.5, color=INK2)

rect(s, Inches(6.79), Inches(3.88), Inches(6.02), Inches(2.85), fill="F2F9F4", line="C6E4D1")
rect(s, Inches(6.79), Inches(3.88), Inches(0.055), Inches(2.85), fill=DOWN)
_, tf = textbox(s, Inches(7.05), Inches(4.02), Inches(5.6), Inches(2.6))
put(tf, "为什么这条支线比覆铜板更值得跟踪", first=True, size=12.5, bold=True, color=NAVY, space_after=8)
for t in ["龙头封板，情绪锚定明确 —— 风华高科涨停，而覆铜板龙头金安国纪未封板",
          "板块宽度更好 —— 被动元件 31/47 上涨（66%），而非覆铜板的 4/5（仅 5 只成分股，代表性弱）",
          "筹码结构更干净 —— 当日净卖出榜中没有被动元件/MLCC 标的，而 PCB 链条已有 3 只被净卖出"]:
    p = tf.add_paragraph(); p.space_after = Pt(7); p.line_spacing = 1.26
    r = p.add_run(); r.text = "▪  "
    style_run(r, size=10.5, bold=True, color=DOWN)
    r = p.add_run(); r.text = t
    style_run(r, size=10.5, color=INK2)
p = tf.add_paragraph(); p.space_before = Pt(6); p.line_spacing = 1.26
r = p.add_run(); r.text = "结论：若只跟踪一条支线，被动元件/MLCC 的「资金纯度」高于 PCB 制板环节。"
style_run(r, size=11, bold=True, color=NAVY)

# ---------- S13 主线三 ----------
s = blank(prs)
page_header(s, 12, "主线三：军工与地面兵装", "MAIN LINE III — DEFENCE")
_, tf = textbox(s, Inches(0.52), Inches(1.14), Inches(12.29), Inches(0.44))
put(tf, "当日唯一能与 AI 硬件链条分庭抗礼的板块。行业端「地面兵装Ⅱ +4.44%」为全行业涨幅第一，且 12/12 全部上涨（100% 板块宽度）。",
    first=True, size=11.5, color=INK2, space_after=0)

tbl = make_table(s, 5, 5, Inches(0.52), Inches(1.72), Inches(12.29), Inches(1.95),
                 col_w=[2.5, 1.7, 1.7, 2.2, 4.2])
header_row(tbl, ["细分方向", "涨跌幅", "上涨家数", "主力净流入", "领涨标的"])
rows = [
    ("地面兵装Ⅱ", "+4.44%", "12/12", "+13.73亿", "光电股份 +10.02%", UP),
    ("军工电子Ⅱ", "+0.02%", "25/60", "+2.80亿", "金信诺 +7.12%", INK3),
    ("航空装备Ⅱ", "-0.44%", "16/46", "-5.50亿", "博云新材 +7.44%", DOWN),
    ("航天装备Ⅱ", "-0.76%", "1/9", "-1.32亿", "新余国科 +3.02%", DOWN),
]
for i, (a, b, c, d, e, c1) in enumerate(rows, 1):
    data_row(tbl, i, [a, b, c, d, e],
             colors=[NAVY, c1, INK2, c1, INK2],
             bolds=[True, True, False, True, False],
             aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.RIGHT, PP_ALIGN.LEFT],
             size=10, height=Inches(0.38))

cards = [
    ("光电股份  sh600184", "+10.02%", "地面兵装Ⅱ 板块领涨股；板块 12/12 全涨，宽度满分"),
    ("博云新材  sz002297", "+7.44%", "龙虎榜净买入 +4.03亿（全市场第 3 位）；航空刹车材料 / 碳碳复合材料"),
    ("内蒙一机  sh600967", "+9.99%", "主战坦克总装，地面兵装核心资产；收盘 14.98"),
]
x = 0.52
for t, v, d in cards:
    rect(s, Inches(x), Inches(3.86), Inches(4.0), Inches(1.5), fill=BG_SOFT, line=LINE)
    rect(s, Inches(x), Inches(3.86), Inches(4.0), Inches(0.05), fill=GOLD)
    _, tf = textbox(s, Inches(x + 0.18), Inches(4.02), Inches(3.7), Inches(0.3))
    put(tf, t, first=True, size=11, bold=True, color=NAVY, space_after=0)
    _, tf = textbox(s, Inches(x + 0.18), Inches(4.3), Inches(3.7), Inches(0.35))
    put(tf, v, first=True, size=16, bold=True, color=UP, space_after=0)
    _, tf = textbox(s, Inches(x + 0.18), Inches(4.72), Inches(3.7), Inches(0.6))
    put(tf, d, first=True, size=9.5, color=INK2, space_after=0, line=1.24)
    x += 4.14

rect(s, Inches(0.52), Inches(5.56), Inches(12.29), Inches(1.28), fill="FDF3F3", line="F2C9C9")
rect(s, Inches(0.52), Inches(5.56), Inches(0.055), Inches(1.28), fill=UP)
_, tf = textbox(s, Inches(0.8), Inches(5.68), Inches(11.85), Inches(1.05))
p = tf.paragraphs[0]; p.line_spacing = 1.3
r = p.add_run(); r.text = "军工的判断：主题脉冲，而非趋势行情。 "
style_run(r, size=12, bold=True, color=UP)
r = p.add_run()
r.text = ("虽「地面兵装 12/12 全涨、主力净流入 13.73 亿」三项数据亮眼，但军工电子仅 +0.02%（25/60）、航空装备 -0.44%、"
          "航天装备 -0.76%（1/9）—— 板块内部没有共振。操作含义：适合短线跟随，不适合中线配置。")
style_run(r, size=11.5, color=INK2)

# ---------- S14 行业资金（柱状图） ----------
s = blank(prs)
page_header(s, 13, "资金流向：行业净流入 / 净流出 TOP 10", "SECTOR FUND FLOW")
_, tf = textbox(s, Inches(0.52), Inches(1.12), Inches(12.29), Inches(0.4))
put(tf, "科技硬件内部大搬家：从半导体撤出，流向通信设备与元件。半导体单日净流出 100.66 亿，超过前两大流入行业之和。",
    first=True, size=11.5, color=INK2, space_after=0)

cd = CategoryChartData()
# 注意：BAR_CLUSTERED 在多数渲染器中自下而上排列，故此处按「显示顺序的倒序」给出，
# 以保证渲染后 通信设备 位于最上方
names = ["电池", "光学光电子", "自动化设备", "证券Ⅱ", "工业金属", "半导体",
         "数字媒体", "风电设备", "玻璃玻纤", "地面兵装Ⅱ", "元件", "通信设备"]
vals = (-23.55, -24.05, -27.37, -40.63, -42.62, -100.66,
        6.36, 6.47, 7.19, 13.73, 41.01, 51.12)
cd.categories = names
cd.add_series("主力净额（亿元）", vals)
gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(0.42), Inches(1.6),
                        Inches(7.9), Inches(4.5), cd)
ch = gf.chart
style_chart(ch, size=10, legend_bottom=False)
ch.has_legend = False
ch.has_title = False
pl = ch.plots[0]
pl.gap_width = 35
pl.has_data_labels = True
dl = pl.data_labels
dl.show_value = True
dl.number_format = '#,##0.0'
dl.number_format_is_linked = False
dl.position = XL_LABEL_POSITION.OUTSIDE_END
dl.font.size = Pt(9.5)
dl.font.bold = True
dl.font.name = FONT
# 正红负绿
for i, v in enumerate(vals):
    pt = pl.series[0].points[i]
    pt.format.fill.solid()
    pt.format.fill.fore_color.rgb = RGBColor.from_string(UP if v >= 0 else DOWN)
    pt.format.line.fill.background()
try:
    va = ch.value_axis
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = RGBColor.from_string("EEF2F6")
    va.tick_labels.number_format = '0'
    va.tick_labels.number_format_is_linked = False
    ca = ch.category_axis
    ca.has_major_gridlines = False
    ca.tick_labels.font.size = Pt(9.5)
    ca.tick_labels.font.name = FONT
except Exception:
    pass

rect(s, Inches(8.5), Inches(1.6), Inches(4.31), Inches(4.5), fill=BG_SOFT, line=LINE)
_, tf = textbox(s, Inches(8.72), Inches(1.76), Inches(3.95), Inches(4.2))
put(tf, "三条必须读出的资金信号", first=True, size=12.5, bold=True, color=NAVY, space_after=9)
for h, b in [
    ("半导体是最大黑洞。", "单日净流出 100.66 亿，20 日累计 -994.29 亿，接近 1,000 亿 —— 中期级别撤离，非短期调仓。"),
    ("通信/元件是 5 日新主线。", "通信设备 5日 +268.38亿但 20日 -201.48亿；元件 5日 +271.54亿、20日 -10.91亿。属新启动主线，筹码尚未充分换手。"),
    ("券商全线下跌。", "证券Ⅱ净流出 40.63 亿、跌 3.10%，50 只成分股 0 只上涨 —— 市场对指数级别行情没有预期。"),
]:
    p = tf.add_paragraph(); p.space_after = Pt(9); p.line_spacing = 1.3
    r = p.add_run(); r.text = "▪  "
    style_run(r, size=10.5, bold=True, color=GOLD)
    r = p.add_run(); r.text = h
    style_run(r, size=10.5, bold=True, color=NAVY)
    r = p.add_run(); r.text = b
    style_run(r, size=10.5, color=INK2)

# ---------- S15 概念板块（柱状图） ----------
s = blank(prs)
page_header(s, 14, "概念板块资金面与轮动", "CONCEPT ROTATION")
_, tf = textbox(s, Inches(0.52), Inches(1.12), Inches(12.29), Inches(0.4))
put(tf, "803 个概念板块参与统计。涨幅 TOP16 中有 8 个实际指向同一条 AI 算力硬件产业趋势，只有军工具备独立逻辑。",
    first=True, size=11.5, color=INK2, space_after=0)

cd = CategoryChartData()
# 同样按倒序给出，保证渲染后 覆铜板 位于最上方
cn = ["昨日首板", "昨日连板", "光纤概念", "科特估", "5.5G", "博通概念",
      "铜缆高速连接器", "中国建材集团", "昨日涨停", "印巴冲突概念", "中兵系",
      "电子布", "陶瓷基板", "MLCC", "被动元件概念", "覆铜板"]
cv = (0.31, 0.38, 0.48, 0.52, 0.68, 0.72,
      0.83, 0.92, 1.02, 1.25, 1.61,
      1.73, 1.74, 1.76, 2.22, 4.31)
cd.categories = cn
cd.add_series("涨跌幅（%）", cv)
gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(0.42), Inches(1.58),
                        Inches(7.9), Inches(4.6), cd)
ch = gf.chart
style_chart(ch, size=9.5, legend_bottom=False)
ch.has_legend = False
ch.has_title = False
pl = ch.plots[0]
pl.gap_width = 32
pl.has_data_labels = True
dl = pl.data_labels
dl.show_value = True
dl.number_format = '+0.00"%"'
dl.number_format_is_linked = False
dl.position = XL_LABEL_POSITION.OUTSIDE_END
dl.font.size = Pt(9)
dl.font.bold = True
dl.font.name = FONT
groups = ["emo", "emo", "up", "emo", "up", "up",
          "up", "emo", "emo", "mil", "mil",
          "up", "up", "up", "up", "up"]
for i, g in enumerate(groups):
    c = UP if g == "up" else (GOLD if g == "mil" else BLUE)
    pt = pl.series[0].points[i]
    pt.format.fill.solid()
    pt.format.fill.fore_color.rgb = RGBColor.from_string(c)
    pt.format.line.fill.background()
try:
    va = ch.value_axis
    va.tick_labels.number_format = '0"%"'
    va.tick_labels.number_format_is_linked = False
    va.major_gridlines.format.line.color.rgb = RGBColor.from_string("EEF2F6")
    ca = ch.category_axis
    ca.has_major_gridlines = False
    ca.tick_labels.font.size = Pt(9)
    ca.tick_labels.font.name = FONT
except Exception:
    pass

rect(s, Inches(8.5), Inches(1.58), Inches(4.31), Inches(4.6), fill=BG_SOFT, line=LINE)
_, tf = textbox(s, Inches(8.72), Inches(1.72), Inches(3.95), Inches(4.35))
put(tf, "配色说明", first=True, size=12, bold=True, color=NAVY, space_after=7)
for label, c, txt in [("红色", UP, "PCB / 被动元件链（8 个概念同源）"),
                      ("金色", GOLD, "军工（中兵系、印巴冲突）"),
                      ("蓝色", BLUE, "情绪指标与外围（昨日涨停/连板/首板、科特估、建材）")]:
    p = tf.add_paragraph(); p.space_after = Pt(5); p.line_spacing = 1.24
    r = p.add_run(); r.text = "■ "
    style_run(r, size=10.5, bold=True, color=c)
    r = p.add_run(); r.text = label + "："
    style_run(r, size=10.5, bold=True, color=NAVY)
    r = p.add_run(); r.text = txt
    style_run(r, size=10.5, color=INK2)
put(tf, "情绪类概念：接力溢价几乎为零", size=11.5, bold=True, color=NAVY,
    space_before=10, space_after=6)
for t in ["昨日涨停 +1.02%、昨日连板 +0.38%、昨日首板 +0.31% —— 正收益但幅度极小",
          "三者 5 日主力净额全为负（-8.18 / -3.45 / -3.58 亿），情绪资金持续流出",
          "「昨日触板」当日 -4.48%（26 只仅 5 只上涨）—— 打板失败一次代价约 -4.5%"]:
    p = tf.add_paragraph(); p.space_after = Pt(5); p.line_spacing = 1.24
    r = p.add_run(); r.text = "▪  "
    style_run(r, size=10, bold=True, color=GOLD)
    r = p.add_run(); r.text = t
    style_run(r, size=10, color=INK2)

# ---------- S16 斐波那契 ----------
s = blank(prs)
page_header(s, 16, "斐波那契关键位与技术推演", "FIBONACCI LEVELS & PROJECTION")
_, tf = textbox(s, Inches(0.52), Inches(1.12), Inches(12.29), Inches(0.4))
put(tf, "上证指数 52 周区间 4,258.86 ~ 3,741.11（幅度 517.75 点），当前收盘 3,888.11。将斐波那契位与均线、布林带做叠加共振分析。",
    first=True, size=11.5, color=INK2, space_after=0)

tbl = make_table(s, 8, 5, Inches(0.52), Inches(1.68), Inches(12.29), Inches(2.9),
                 col_w=[1.7, 1.9, 1.7, 4.5, 2.7])
header_row(tbl, ["斐波那契位", "计算值", "距现价", "共振参照", "性质判断"])
rows = [
    ("78.6%", "4,148.06", "+6.69%", "—", "远期压力", INK3),
    ("61.8%", "4,061.08", "+4.45%", "—", "中期压力", INK3),
    ("50.0%", "3,999.99", "+2.88%", "BOLL 上轨 4,001.75", "双重压力共振", UP),
    ("38.2%", "3,938.89", "+1.31%", "MA20 3,936.76 / BOLL 中轨 / 前收盘 3,934.40", "四线共振，最关键压力", UP),
    ("现价", "3,888.11", "—", "BOLL 下轨 3,871.77 上方", "弱势整理区", NAVY),
    ("23.6%", "3,863.30", "-0.64%", "BOLL 下轨 3,871.77", "第一支撑（已贴近）", DOWN),
    ("52周低", "3,741.11", "-3.78%", "—", "极限支撑", DOWN),
]
for i, (a, b, c, d, e, col) in enumerate(rows, 1):
    data_row(tbl, i, [a, b, c, d, e],
             colors=[col, col, INK2, INK2, col],
             bolds=[True, True, False, False, True],
             aligns=[PP_ALIGN.CENTER, PP_ALIGN.RIGHT, PP_ALIGN.RIGHT, PP_ALIGN.LEFT, PP_ALIGN.LEFT],
             size=9.5, height=Inches(0.34))

rect(s, Inches(0.52), Inches(4.66), Inches(6.02), Inches(2.12), fill=BG_SOFT, line=LINE)
_, tf = textbox(s, Inches(0.74), Inches(4.78), Inches(5.6), Inches(1.9))
put(tf, "技术指标状态", first=True, size=12, bold=True, color=NAVY, space_after=7)
for t in ["均线：MA5 3,937.86 / MA10 3,949.11 / MA20 3,936.76 / MA60 3,945.09 / MA120 3,998.17 / MA250 3,988.40",
          "六条均线密集于 3,936 ~ 3,998，现价跌破全部均线，该区间由支撑转为强压力带",
          "MACD 0.0782（DIF 6.3565 > DEA 6.3174，微弱金叉且近乎黏合）",
          "RSI6 46.26 / RSI12 50.20 / RSI24 49.42 —— 全部中性；BOLL 带宽仅 3.3%，通道收窄"]:
    p = tf.add_paragraph(); p.space_after = Pt(5); p.line_spacing = 1.24
    r = p.add_run(); r.text = "▪  "
    style_run(r, size=10, bold=True, color=GOLD)
    r = p.add_run(); r.text = t
    style_run(r, size=10, color=INK2)

rect(s, Inches(6.79), Inches(4.66), Inches(6.02), Inches(2.12), fill="FDFAF3", line=GOLD_L)
rect(s, Inches(6.79), Inches(4.66), Inches(0.055), Inches(2.12), fill=GOLD)
_, tf = textbox(s, Inches(7.05), Inches(4.78), Inches(5.6), Inches(1.9))
put(tf, "技术面综合定调", first=True, size=12, bold=True, color=NAVY, space_after=7)
p = tf.add_paragraph(); p.line_spacing = 1.3; p.space_after = Pt(6)
r = p.add_run()
r.text = "「跌破六均线 + 布林通道收窄 + MACD 黏合 + RSI 中性」→ 典型变盘前夜形态，但方向未定。"
style_run(r, size=10.5, bold=True, color=NAVY)
p = tf.add_paragraph(); p.line_spacing = 1.3; p.space_after = Pt(6)
r = p.add_run(); r.text = "结合广度数据（上涨占比 11%）判断，向下变盘概率高于向上。下周关键观察 3,863 ~ 3,872 支撑带能否承接。"
style_run(r, size=10.5, color=INK2)
p = tf.add_paragraph(); p.line_spacing = 1.3
r = p.add_run(); r.text = "操作纪律：3,938 未收复前仓位保持中性偏低；跌破 3,863 进一步降仓。"
style_run(r, size=10.5, bold=True, color=UP)

# ---------- S17 十大专家视角 ----------
s = blank(prs)
page_header(s, 17, "十大专家视角与明日可验证预测", "EXPERT MATRIX & TOMORROW'S PLAYBOOK")
tbl = make_table(s, 11, 3, Inches(0.52), Inches(1.16), Inches(12.29), Inches(4.0),
                 col_w=[2.6, 2.9, 6.8])
header_row(tbl, ["视角", "关注核心", "当日结论"])
rows = [
    ("WIND 行业比较", "行业宽度与轮动", "上涨行业 <20%，全面下跌；仅 4 个行业涨幅 >1%"),
    ("全球 CEO 视角", "产业长期趋势", "AI 算力资本开支是唯一确定的产业趋势，覆铜板/被动元件是其上游必受益环节"),
    ("CFO 视角", "现金流与涨价传导", "上游材料供给刚性 + 需求陡增，涨价可验证、可入表；中游制板议价能力弱"),
    ("CXO 视角", "客户结构与订单", "AI 服务器订单占比高的被买（崇达/嘉立创），占比低的被卖（逸豪/超声）"),
    ("股票超级专家", "量价与情绪结构", "40 家涨停但最高仅 4 板，首板占 75%，接力意愿弱 —— 低位活跃、高位死亡"),
    ("财报分析", "业绩可验证性", "「26三季报预增」概念当日 -4.50%，纯预期驱动失效，市场对业绩预期不买单"),
    ("麦肯锡 7S", "组织与执行力", "主线为单一链条，缺乏多点开花的结构支撑，抗风险能力弱"),
    ("摩根士丹利 MD", "资产配置建议", "哑铃策略：一端 AI 硬件上游（进攻），一端军工（主题对冲）；低配半导体、有色、券商"),
    ("StockMasterHunter", "交易信号", "龙虎榜净买入前十 6 席同一链条，跟随主线的胜率显著高于分散试错"),
    ("风险管理", "回撤控制", "单日下跌 4,870 家、跌停 21 家，系统性风险未释放完毕，仓位应降至中性偏低"),
]
for i, (a, b, c) in enumerate(rows, 1):
    data_row(tbl, i, [a, b, c],
             colors=[NAVY, INK3, INK2],
             bolds=[True, False, False],
             aligns=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT],
             size=9.5, height=Inches(0.375))

_, tf = textbox(s, Inches(0.52), Inches(5.28), Inches(12.29), Inches(1.55))
put(tf, "明日（下一交易日）可验证预测 —— 把判断写成可被证伪的具体条件", first=True,
    size=12.5, bold=True, color=NAVY, space_after=8)
for t in ["① 上证指数：下方支撑 3,863~3,872（斐波那契23.6% + BOLL下轨）；上方压力 3,938（38.2% + MA20 四线共振）",
          "② 主线延续：覆铜板/被动元件链条至少 3 只个股上涨；关键看金安国纪（净买 8.12 亿）能否高开不炸",
          "③ 情绪高度：4 板桂林旅游晋级 5 板则情绪修复；炸板则确认高标死亡",
          "④ 资金反转：半导体净流出是否收窄至 50 亿以内；若继续 100 亿级流出，指数难止跌",
          "⑤ 跌停家数：从 21 家回落至 10 家以内视为风险释放；继续放大则需进一步降仓"]:
    p = tf.add_paragraph(); p.space_after = Pt(4); p.line_spacing = 1.24
    r = p.add_run(); r.text = t
    style_run(r, size=10.5, color=INK2)

# ---------- S18 策略与风险 ----------
s = blank(prs)
page_header(s, 17, "策略手册、六条行动与风险提示（17 章续）", "PLAYBOOK · ACTIONS · RISKS")
panels = [
    ("进攻　占比 ≤30%", [("首选", "被动元件/MLCC：风华高科（唯一封板+板块共振+行业净流入三确认）"),
                          ("次选", "覆铜板上游：金安国纪（资金第一但未封板，需等次日承接确认）"),
                          ("规避", "中游制板：逸豪新材、超声电子已被净卖出")], UP),
    ("主题　占比 ≤15%", [("标的", "军工：地面兵装（12/12 全涨、主力净流入 13.73 亿）"),
                          ("限制", "仅限短线跟随，因军工电子/航空/航天三个细分方向均在跌"),
                          ("性质", "持续性依赖地缘消息，无基本面外推能力")], GOLD),
    ("回避　零配置", [("半导体", "20 日净流出 994 亿，持续失血"),
                       ("有色金属", "工业金属 -5.04%，全品种崩塌"),
                       ("证券", "0/50 上涨，净流出 40.63 亿")], DOWN),
]
x = 0.52
for title, items, col in panels:
    rect(s, Inches(x), Inches(1.16), Inches(4.0), Inches(2.02), fill=BG_SOFT, line=LINE)
    rect(s, Inches(x), Inches(1.16), Inches(4.0), Inches(0.36), fill=col)
    _, tf = textbox(s, Inches(x + 0.16), Inches(1.21), Inches(3.7), Inches(0.28))
    put(tf, title, first=True, size=11, bold=True, color=WHITE, space_after=0)
    _, tf = textbox(s, Inches(x + 0.16), Inches(1.6), Inches(3.72), Inches(1.5))
    for i, (h, b) in enumerate(items):
        p = para(tf, first=(i == 0)); p.space_after = Pt(6); p.line_spacing = 1.22
        r = p.add_run(); r.text = h + "："
        style_run(r, size=9.5, bold=True, color=NAVY)
        r = p.add_run(); r.text = b
        style_run(r, size=9.5, color=INK2)
    x += 4.14

rect(s, Inches(0.52), Inches(3.32), Inches(12.29), Inches(2.28), fill="FDFAF3", line=GOLD_L)
rect(s, Inches(0.52), Inches(3.32), Inches(0.055), Inches(2.28), fill=GOLD)
_, tf = textbox(s, Inches(0.8), Inches(3.44), Inches(11.85), Inches(2.05))
put(tf, "六条行动清单：从「书单」到「流程」（本报告即第 4 条的首次落地）",
    first=True, size=12.5, bold=True, color=NAVY, space_after=8)
for h, b in [
    ("1 建立可验证样本：", "已固定三项日频指标 —— 涨停家数 / 连板梯队高度 / 龙虎榜净买入 TOP10，可逐日回溯"),
    ("2 策略写成代码：", "行业 ∈ {元件, 通信设备} AND 主力净流入 > 0 AND 当日涨停 AND 龙虎榜净买入 > 0 → 当日命中风华高科、崇达技术、九鼎新材"),
    ("3 单周风险上限：", "本周上证 5 日 -1.07%；建议单周账户回撤上限设为 3%（约等于 2 次打板失败）"),
    ("4 升级自产研报：", "本报告即首次落地 —— 已写入 5 条可证伪预测，下一交易日收盘后核对"),
    ("5 仓位表：", "单笔 ≤ 总资金 10%，单一主线 ≤ 30%；依据：打板失败单次代价 -4.48%"),
    ("6 每 13 周期望值核算：", "以 13 周为周期回算胜率与盈亏比，用真实数据检验「周10%」假设是否成立"),
]:
    p = tf.add_paragraph(); p.space_after = Pt(4); p.line_spacing = 1.22
    r = p.add_run(); r.text = h
    style_run(r, size=10, bold=True, color=NAVY)
    r = p.add_run(); r.text = b
    style_run(r, size=10, color=INK2)

rect(s, Inches(0.52), Inches(5.74), Inches(12.29), Inches(1.08), fill="FDF3F3", line="F2C9C9")
rect(s, Inches(0.52), Inches(5.74), Inches(0.055), Inches(1.08), fill=UP)
_, tf = textbox(s, Inches(0.8), Inches(5.84), Inches(11.85), Inches(0.9))
p = tf.paragraphs[0]; p.line_spacing = 1.26
r = p.add_run(); r.text = "风险提示："
style_run(r, size=11, bold=True, color=UP)
r = p.add_run()
r.text = ("① 系统性风险未释放（下跌 4,870 家、跌停放大 10.5 倍）；② 主线单点化，无第二主线承接；"
          "③ 链条内部分歧已现（逸豪/超声/中京被净卖出）；④ 最高仅 4 板，打板失败成本 -4.48%，追高即接盘；"
          "⑤ 连板与封单数据来自 2026-09-10（上游滞后 1 日），机构/游资分类席位榜为空。")
style_run(r, size=10.5, color=INK2)
p = tf.add_paragraph(); p.space_before = Pt(4); p.line_spacing = 1.2
r = p.add_run()
r.text = "免责声明：本报告基于公开市场数据与量化统计方法生成，仅供研究参考，不构成投资建议。市场有风险，投资须谨慎。"
style_run(r, size=9, color=INK3)

# ---------------- 保存 ----------------
prs.save(str(PPTX))
print(f"已生成: {PPTX}")
print(f"页数: {len(prs.slides.__iter__.__self__._sldIdLst)}")

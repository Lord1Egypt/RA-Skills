#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""omni2docx — PPTX 汇报渲染器（汇报场景：把文档/提纲变成可讲的 deck）

设计（原创「编辑式极简」体系，离线可复现、零外部资源；层级只靠留白、字重与细灰 hairline，不用色块语言）：
- 近单色 + 单一克制强调色：墨色(ink)为主，强调色仅用于微小标记（序号、短细线），不铺色块。
- 无顶部导航条、无 kicker 角标、无 PART 0X、无填充色块——靠大留白与字号层级建立结构。
- 分页型版式：封面（大留白 + 墨色标题 + 标题下短细线 + 灰副标）→ 目录（序号+标题，无卡片）
  → 章节分隔（右侧幽灵大序号 + 墨色标题，无顶带）→ 内容（墨色结论式标题 + 细灰线
  + KPI 无填充竖线分隔 + 加粗首关键词要点）→ 结束页。不再把正文逐段平铺成上百页。
- 字号层级：封面 40+、页标题 30、正文 19、KPI 40、页码/来源 10。
- 装饰克制：细线(hairline)、幽灵序号、大数字——形状无文本，不触发几何重叠审计；颜色 ≤2（墨+强调）。
- 表格美化：表头墨色加粗 + 底部粗线、行间 hairline；无填充、无竖线、无外框。

约定（C 路线）：内容取舍交给 agent——agent 按 slide 组织好 markdown，引擎只负责把结构
映射为 deck 与制式排版。不做像素级版面复刻。
"""
import argparse
import base64
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_docx import (  # noqa: E402
    DOC_PROFILES, build_outline_map, clean_cjk_spaces, derive_outline_from_markdown,
    extract_footnotes, extract_title, match_outline_level, parse_blocks, strip_emoji,
)

from pptx import Presentation  # noqa: E402
from pptx.util import Inches, Pt, Emu  # noqa: E402
from pptx.oxml.ns import qn  # noqa: E402
from pptx.dml.color import RGBColor  # noqa: E402

# deck 字体/字号制式（汇报场景字号显著大于文档场景，层级差一档以上以保证投影可读）
PPT_PROFILES = {
    "default": {"title_east": "微软雅黑", "body_east": "微软雅黑",
                "title_size": 30, "body_size": 19, "section_size": 34},
    "gov": {"title_east": "黑体", "body_east": "仿宋_GB2312",
            "title_size": 30, "body_size": 20, "section_size": 34},
    "legal": {"title_east": "黑体", "body_east": "仿宋_GB2312",
              "title_size": 28, "body_size": 19, "section_size": 32},
    "finance": {"title_east": "黑体", "body_east": "等线",
                "title_size": 28, "body_size": 18, "section_size": 32},
    "academic": {"title_east": "黑体", "body_east": "宋体",
                 "title_size": 28, "body_size": 19, "section_size": 32},
}

# 编辑式极简主题：近单色 + 单一克制强调色（仅用于微小标记：序号、短细线），
# 本包制式：不铺色块、不建顶部导航条、不用 kicker 角标——层级只靠留白、字重与细灰 hairline。
# primary 保留为强调色别名；hairline=细灰线；muted/faint=灰阶层级。
THEMES = {
    "default":  {"primary": "#8C6A3F", "ink": "#1A1A1A", "accent": "#8C6A3F",
                 "hairline": "#DCDCDC", "muted": "#6E6E6E", "faint": "#9A9A9A",
                 "text": "#2B2B2B"},
    "academic": {"primary": "#2E4A7A", "ink": "#1A1A1A", "accent": "#2E4A7A",
                 "hairline": "#DCDCDC", "muted": "#6E6E6E", "faint": "#9A9A9A",
                 "text": "#2B2B2B"},
    "gov":      {"primary": "#8A2B2B", "ink": "#1A1A1A", "accent": "#8A2B2B",
                 "hairline": "#DCDCDC", "muted": "#6E6E6E", "faint": "#9A9A9A",
                 "text": "#2B2B2B"},
    "legal":    {"primary": "#7A3B2E", "ink": "#1A1A1A", "accent": "#7A3B2E",
                 "hairline": "#DCDCDC", "muted": "#6E6E6E", "faint": "#9A9A9A",
                 "text": "#2B2B2B"},
    "finance":  {"primary": "#1F6F6B", "ink": "#1A1A1A", "accent": "#1F6F6B",
                 "hairline": "#DCDCDC", "muted": "#6E6E6E", "faint": "#9A9A9A",
                 "text": "#2B2B2B"},
}


def rgb(hexstr):
    h = hexstr.lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def tint(hexstr, f):
    """向白色混合 f 比例，得到浅色（用于卡片底/幽灵序号）。"""
    h = hexstr.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r = round(r + (255 - r) * f)
    g = round(g + (255 - g) * f)
    b = round(b + (255 - b) * f)
    return "#%02X%02X%02X" % (r, g, b)


LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)]*)\)")
STAT_RE = re.compile(r"^(约?[\d][\d.,]*)\s*(%|％|倍|‰|个|万|亿|元|美元|￥|\$|年|pct|PP)?$")
# kpi 版式（强制）用宽松抽取：数字开头即入塔，单位=1-2 汉字或 %类（贪婪；CJK 间
# 空格可能已被 plain() 清洗，故不做空格 lookahead），剩余文本作看板标签
STAT_LOOSE_RE = re.compile(r"^(约?[\d][\d.,]*)\s*([%％倍‰]|[一-鿿]{1,2})?\s*(.*)$")


def plain(text):
    """markdown 行内 → PPT 纯文本（去标记、保留可读内容）。"""
    t = text or ""
    t = IMG_RE.sub(lambda m: m.group(1) or "图像", t)
    t = LINK_RE.sub(r"\1", t)
    t = re.sub(r"\*\*(.+?)\*\*(?!\*)", r"\1", t)
    t = re.sub(r"__(.+?)__(?!_)", r"\1", t)
    t = re.sub(r"`(.+?)`", r"\1", t)
    t = re.sub(r"\*([^\s*][^*\n]*)\*", r"\1", t)
    t = re.sub(r"_([^\s_][^_\n]*)_", r"\1", t)
    t = re.sub(r"\[\^([^\]]+)\]", r"[\1]", t)
    return clean_cjk_spaces(t).strip()  # 清 OCR 残留的 CJK 字间空格（拉丁逐字母空格不可还原，不强修)


def set_east(run, east, latin=None):
    rPr = run._r.get_or_add_rPr()
    for tag in ("a:latin", "a:ea", "a:cs"):
        el = rPr.find(qn(tag))
        if el is not None:
            rPr.remove(el)
    from pptx.oxml import parse_xml
    from pptx.oxml.ns import nsdecls
    latin_el = parse_xml('<a:latin %s typeface="%s"/>' % (nsdecls("a"), latin or east))
    ea_el = parse_xml('<a:ea %s typeface="%s"/>' % (nsdecls("a"), east))
    cs_el = parse_xml('<a:cs %s typeface="%s"/>' % (nsdecls("a"), east))
    rPr.append(latin_el)
    rPr.append(ea_el)
    rPr.append(cs_el)


def add_line(tf, text, size, east, bold=False, color=None, level=0, space_after=6,
             align=None, marker=None):
    """加一行。marker=(color_hex, glyph) 时渲染彩色前置 run（如 kicker/要点引导符）。"""
    p = tf.paragraphs[0] if (not tf.paragraphs[0].runs and not tf.paragraphs[0].text) else tf.add_paragraph()
    p.level = level
    p.space_after = Pt(space_after)
    if align is not None:
        p.alignment = align
    if marker:
        rm = p.add_run()
        rm.text = marker[1] + " "
        rm.font.size = Pt(size)
        rm.font.bold = True
        rm.font.color.rgb = rgb(marker[0])
        set_east(rm, east)
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    if color:
        r.font.color.rgb = rgb(color)
    set_east(r, east)
    return p


def fill_solid(shape, hexstr):
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb(hexstr)
    shape.line.fill.background()


def _set_cell_border(cell):
    """给单元格加四边细灰边框（python-pptx Cell 无 border_size，走 XML）。"""
    from pptx.oxml.ns import nsdecls
    from pptx.oxml import parse_xml
    tcPr = cell._tc.get_or_add_tcPr()
    for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
        el = tcPr.find(qn(tag))
        if el is not None:
            tcPr.remove(el)
    node = parse_xml(
        '<a:tcPr %s>'
        '<a:lnL w="6350" cap="flat"><a:solidFill><a:srgbClr val="BFBFBF"/></a:solidFill></a:lnL>'
        '<a:lnR w="6350" cap="flat"><a:solidFill><a:srgbClr val="BFBFBF"/></a:solidFill></a:lnR>'
        '<a:lnT w="6350" cap="flat"><a:solidFill><a:srgbClr val="BFBFBF"/></a:solidFill></a:lnT>'
        '<a:lnB w="6350" cap="flat"><a:solidFill><a:srgbClr val="BFBFBF"/></a:solidFill></a:lnB>'
        '</a:tcPr>' % nsdecls("a"))
    for child in list(node):
        tcPr.append(child)


def _table_hairlines(tbl, n_rows, n_cols, theme):
    """编辑式极简表格边框：表头底部墨色粗线 + 行间 hairline；无填充、无竖向边线、无外框。"""
    from pptx.oxml.ns import nsdecls
    from pptx.oxml import parse_xml
    ink = theme["ink"].lstrip("#")
    hair = theme["hairline"].lstrip("#")
    for r_idx in range(n_rows):
        for c_idx in range(n_cols):
            cell = tbl.cell(r_idx, c_idx)
            tcPr = cell._tc.get_or_add_tcPr()
            for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
                el = tcPr.find(qn(tag))
                if el is not None:
                    tcPr.remove(el)
            is_head = (r_idx == 0)
            node = parse_xml(
                '<a:tcPr %s>'
                '<a:lnB w="%d" cap="flat"><a:solidFill><a:srgbClr val="%s"/></a:solidFill></a:lnB>'
                '</a:tcPr>' % (nsdecls("a"), 12700 if is_head else 6350, ink if is_head else hair))
            for child in list(node):
                tcPr.append(child)


class Deck:
    """带主题与分页型版式的 deck 构造器（原创编辑式极简体系：大留白、细线、近单色）。"""

    def __init__(self, cfg, theme, ratio="16:9"):
        self.prs = Presentation()
        if ratio == "16:9":
            self.prs.slide_width, self.prs.slide_height = Inches(13.333), Inches(7.5)
        elif ratio == "4:3":
            self.prs.slide_width, self.prs.slide_height = Inches(10), Inches(7.5)
        else:  # 自定义尺寸（英寸元组字符串 "13.333,7.5"）
            try:
                w, h = (float(x) for x in str(ratio).split(","))
                self.prs.slide_width, self.prs.slide_height = Inches(w), Inches(h)
            except Exception:
                self.prs.slide_width, self.prs.slide_height = Inches(13.333), Inches(7.5)
        self.cfg = cfg
        self.theme = theme
        self.tint = theme["hairline"]                 # 细线色（替代填充底）
        self.tint2 = theme["faint"]                   # 淡色（幽灵序号）
        self.W = float(self.prs.slide_width)
        self.H = float(self.prs.slide_height)
        self.blank = self.prs.slide_layouts[6]
        self.M = Inches(0.55)            # 统一页边距
        self.mw = self.W - 2 * self.M   # 内容宽度
        self.page_no = 0

    def slide(self, bg=None):
        s = self.prs.slides.add_slide(self.blank)
        if bg:
            s.background.fill.solid()
            s.background.fill.fore_color.rgb = rgb(bg)
        else:
            s.background.fill.solid()
            s.background.fill.fore_color.rgb = rgb("#FFFFFF")
        return s

    @property
    def n_slides(self):
        return len(self.prs.slides._sldIdLst)

    # ---------- 基础形状 ----------
    def _rect(self, s, x, y, w, h, color, line=None, line_w=0.75):
        shp = s.shapes.add_shape(1, x, y, w, h)  # 1 = rectangle（直角，禁圆角）
        shp.fill.solid()
        shp.fill.fore_color.rgb = rgb(color)
        if line:
            shp.line.color.rgb = rgb(line)
            shp.line.width = Pt(line_w)
        else:
            shp.line.fill.background()
        shp.shadow.inherit = False
        return shp

    def _tb(self, s, x, y, w, h):
        tb = s.shapes.add_textbox(x, y, w, h)
        tb.text_frame.word_wrap = True
        return tb.text_frame

    # ---------- 顶栏/页脚 ----------
    def _nav(self, s, section):
        """编辑式极简：不设顶部导航条。保留接口为空。"""
        return s

    def _footer(self, s, source):
        """底部页脚：细灰 hairline + 左来源(灰) + 右页码(灰)；全部 >=10pt。"""
        y = self.H - Inches(0.42)
        self._rect(s, self.M, y, self.mw, Pt(0.75), self.theme["hairline"])
        tf = self._tb(s, self.M, self.H - Inches(0.38), self.mw * 0.7, Inches(0.3))
        add_line(tf, ("来源：" + source) if source else "Omni 解析重建", 10,
                 self.cfg.get("body_east", "微软雅黑"), color=self.theme["muted"])
        self.page_no += 1
        tf2 = self._tb(s, self.W - self.M - Inches(1.2), self.H - Inches(0.38),
                       Inches(1.2), Inches(0.3))
        add_line(tf2, "%02d" % self.page_no, 10, self.cfg.get("body_east", "微软雅黑"),
                 color=self.theme["muted"], align=3)
        return s

    # ---------- 分页型 ----------
    def cover_slide(self, title, subtitle, source):
        s = self.slide()
        # 编辑式极简封面：白底、大留白、墨色大标题、标题下一道短细线、底部灰副标。
        # 无左侧色块、无 kicker 角标、无 accent 色块——分隔只用 hairline。
        rx = self.M
        rw = self.mw
        tf = self._tb(s, rx, Inches(2.3), rw, Inches(2.6))
        add_line(tf, title, self.cfg.get("section_size", 34) + 12,
                 self.cfg.get("title_east", "微软雅黑"), bold=True,
                 color=self.theme["ink"], space_after=14)
        # 标题下短细线（强调色，克制）
        self._rect(s, rx, Inches(5.0), Inches(1.8), Pt(1.5), self.theme["accent"])
        if subtitle:
            tf2 = self._tb(s, rx, Inches(5.25), rw, Inches(1.2))
            add_line(tf2, subtitle, self.cfg.get("body_size", 19),
                     self.cfg.get("body_east", "微软雅黑"), color=self.theme["muted"])
        # 底部来源/署名（淡灰）
        tfm = self._tb(s, rx, self.H - Inches(0.7), rw, Inches(0.4))
        add_line(tfm, (("来源：" + source) if source else "Omni 解析重建")
                 + "　·　汇报版", 12, self.cfg.get("body_east", "微软雅黑"),
                 color=self.theme["faint"])
        return s

    def toc_slide(self, title, entries, source):
        s = self.slide()
        tf = self._tb(s, self.M, Inches(0.7), self.mw, Inches(0.9))
        add_line(tf, "目录", self.cfg.get("section_size", 34),
                 self.cfg.get("title_east", "微软雅黑"), bold=True,
                 color=self.theme["ink"], space_after=8)
        self._rect(s, self.M, Inches(1.65), Inches(1.6), Pt(1.5), self.theme["accent"])
        top = Inches(2.1)
        # 行高自适应：条目多时压缩（不得溢出页底）；>10 条同步降字号保持可读
        avail = self.H - top - Inches(0.85)
        row_h = min(Inches(0.92), avail / max(len(entries), 1))
        tsize = self.cfg.get("body_size", 19) if len(entries) <= 10 else 16
        for i, e in enumerate(entries):
            ey = top + row_h * i
            tfi = self._tb(s, self.M, ey, Inches(0.8), row_h)
            add_line(tfi, "%02d" % (i + 1), 14, self.cfg.get("title_east", "微软雅黑"),
                     bold=True, color=self.theme["faint"])
            tf = self._tb(s, self.M + Inches(0.95), ey, self.mw - Inches(0.95), row_h)
            add_line(tf, e, tsize,
                     self.cfg.get("body_east", "微软雅黑"), color=self.theme["ink"])
        self._footer(s, source)
        return s

    def section_slide(self, title, idx):
        s = self.slide()
        # 大留白 + 右侧幽灵大序号（淡灰，无文本装饰）+ 左侧墨色章节标题 + 底部短细线。
        # 无顶部色带、无 PART 0X kicker。
        nf = self._tb(s, self.W - Inches(5.0), Inches(1.2), Inches(4.3), Inches(4.0))
        add_line(nf, "%02d" % (idx or 1), 180, self.cfg.get("title_east", "微软雅黑"),
                 bold=True, color=self.theme["faint"])
        tf = self._tb(s, Inches(0.9), Inches(3.0), Inches(7.0), Inches(2.4))
        add_line(tf, title, self.cfg.get("section_size", 34) + 4,
                 self.cfg.get("title_east", "微软雅黑"), bold=True, color=self.theme["ink"])
        self._rect(s, Inches(0.92), Inches(5.6), Inches(2.2), Pt(1.5), self.theme["accent"])
        self._footer(s, None)
        return s

    def _title_block(self, s, kicker, title):
        """结论式大标题（墨色）+ 标题下细灰线；无 kicker 角标。返回正文起始 y。"""
        tf = self._tb(s, self.M, Inches(0.6), self.mw, Inches(0.95))
        t = len(title)
        ts = (self.cfg.get("title_size", 30) - 6 if t > 70 else
              self.cfg.get("title_size", 30) - 3 if t > 40 else self.cfg.get("title_size", 30))
        add_line(tf, title, ts, self.cfg.get("title_east", "微软雅黑"), bold=True,
                 color=self.theme["ink"], space_after=2)
        self._rect(s, self.M, Inches(1.55), Inches(1.8), Pt(1.25), self.theme["hairline"])
        return Inches(1.85)

    def content_slide(self, title, kicker, items, tables=None, images=None, notes=None,
                      source=None, section=None, layout="auto"):
        """items: [("bullet"|"text"|"note"|"ol", 文本)]；tables: [(header, rows)]。

        layout（语义版式池，锁定契约——版式锁死、数量由内容决定）：
        auto=现状（自动 KPI 抽取 + 要点/双栏）；kpi=强制 KPI 塔看板（≤4 数字要点）；
        compare=两栏对比（垂直 hairline 中分）；timeline=纵向时间线（左轴+方形节点）。
        前置条件不满足（如 compare 时有表格/图像）自动回退 auto。
        """
        tables = tables or []
        images = images or []
        s = self.slide()
        self._nav(s, section)
        top = self._title_block(s, kicker, title)

        # —— KPI 大数字看板：抽数字型要点，渲染为无填充列（竖 hairline 分隔 + 墨色大数字）——
        # auto：仅纯"数字+单位"条目；kpi（强制）：宽松抽取，剩余文本作看板标签
        max_stats = 3 if layout == "auto" else 4
        stats, rest = [], []
        for kind, text in items:
            t = text.strip()
            if kind in ("bullet", "ol") and len(stats) < max_stats:
                if layout == "kpi":
                    m = STAT_LOOSE_RE.match(t)
                    if m:
                        stats.append((m.group(1), m.group(2) or "",
                                      (m.group(3) or "").strip()))
                        continue
                else:
                    m = STAT_RE.match(t)
                    if m:
                        stats.append((m.group(1), m.group(2) or "", ""))
                        continue
            rest.append((kind, text))
        if layout == "kpi" and not stats:
            layout = "auto"  # 无数字要点，KPI 塔无从谈起——回退
        if layout in ("compare", "timeline") and (tables or images):
            layout = "auto"  # 版式前置条件不满足——回退

        cur_top = top
        if stats:
            n = len(stats)
            cw = self.mw / n
            for i, (num, unit, label) in enumerate(stats):
                cx = self.M + cw * i
                if i > 0:
                    self._rect(s, cx, cur_top + Inches(0.12), Pt(0.75), Inches(0.95), self.theme["hairline"])
                tfn = self._tb(s, cx + Inches(0.2), cur_top + Inches(0.05), cw - Inches(0.3), Inches(0.75))
                add_line(tfn, num + (unit and (" " + unit) or ""), 40,
                         self.cfg.get("title_east", "微软雅黑"), bold=True,
                         color=self.theme["ink"])
                tfl = self._tb(s, cx + Inches(0.2), cur_top + Inches(0.82), cw - Inches(0.3), Inches(0.35))
                add_line(tfl, label or "关键指标", 12, self.cfg.get("body_east", "微软雅黑"),
                         color=self.theme["muted"])
            cur_top = cur_top + Inches(1.25) + Inches(0.2)

        avail_h = self.H - cur_top - Inches(0.7)
        left_w = self.mw * (0.58 if images else 1.0)

        # —— 要点：按版式池分发 ——
        if rest:
            # bullet/text/ol 上页；note（引用/视觉标注）作为静音灰行上页，计入保真
            body_items = [(k, t) for k, t in rest if k in ("bullet", "text", "ol", "note")]
            two_col = len(body_items) >= 6 and all(len(t) <= 42 for _, t in body_items)
            if layout == "compare" and len(body_items) >= 2:
                # 两栏对比：垂直 hairline 中分，左 Before / 右 After
                half = (len(body_items) + 1) // 2
                cols = [body_items[:half], body_items[half:]]
                mid = self.M + self.mw / 2
                self._rect(s, mid, cur_top + Inches(0.05), Pt(0.75),
                           avail_h - Inches(0.2), self.theme["hairline"])
                col_w = self.mw / 2 - Inches(0.45)
                for ci, col in enumerate(cols):
                    cx = self.M if ci == 0 else mid + Inches(0.45)
                    tf = self._tb(s, cx, cur_top, col_w, avail_h)
                    for j, (kind, text) in enumerate(col):
                        self._bullet(tf, kind, text, j, two_col=False)
            elif layout == "timeline" and len(body_items) >= 3:
                # 纵向时间线：左 hairline 轴 + 方形节点（直角铁律，不用圆点）+ 步骤文本
                axis_x = self.M + Inches(0.14)
                self._rect(s, axis_x, cur_top + Inches(0.08), Pt(1),
                           avail_h - Inches(0.2), self.theme["hairline"])
                row_h = min(Inches(1.15), (avail_h - Inches(0.2)) / max(len(body_items), 1))
                for i, (kind, text) in enumerate(body_items):
                    ny = cur_top + Inches(0.1) + row_h * i
                    self._rect(s, axis_x - Inches(0.055), ny + Inches(0.12),
                               Inches(0.11), Inches(0.11), self.theme["accent"])
                    tf = self._tb(s, axis_x + Inches(0.35), ny,
                                  self.mw - Inches(0.7), row_h)
                    self._bullet(tf, "ol" if kind == "ol" else "bullet", text, i, two_col=False)
            elif two_col:
                half = (len(body_items) + 1) // 2
                cols = [body_items[:half], body_items[half:]]
                col_w = (left_w - Inches(0.3)) / 2
                for ci, col in enumerate(cols):
                    cx = self.M + (col_w + Inches(0.3)) * ci
                    tf = self._tb(s, cx, cur_top, col_w, avail_h)
                    for j, (kind, text) in enumerate(col):
                        self._bullet(tf, kind, text, j, two_col=True)
            else:
                tf = self._tb(s, self.M, cur_top, left_w, avail_h)
                for j, (kind, text) in enumerate(body_items):
                    self._bullet(tf, kind, text, j, two_col=False)

        # —— 表格 ——
        for header, rows in tables:
            n_rows, n_cols = len(rows) + 1, max(len(header), max((len(r) for r in rows), default=1))
            tbl_h = min(Inches(0.34) * n_rows + Inches(0.2), avail_h - Inches(0.1))
            gt = s.shapes.add_table(n_rows, n_cols, self.M, cur_top, left_w, tbl_h)
            tbl = gt.table
            fsize = Pt(14 if n_cols <= 3 else 12 if n_cols <= 5 else 10)
            for j, c in enumerate(header):
                cell = tbl.cell(0, j)
                cell.text = plain(c)[:60]
                cell.fill.solid(); cell.fill.fore_color.rgb = rgb("#FFFFFF")
                cell.vertical_anchor = 3
                for p in cell.text_frame.paragraphs:
                    p.alignment = 1
                    for r in p.runs:
                        r.font.size = fsize; r.font.bold = True
                        r.font.color.rgb = rgb(self.theme["ink"])
                        set_east(r, self.cfg.get("title_east", "微软雅黑"))
            for i, row in enumerate(rows, start=1):
                for j, c in enumerate(row[:n_cols]):
                    cell = tbl.cell(i, j)
                    cell.text = plain(c)[:80]
                    cell.fill.solid(); cell.fill.fore_color.rgb = rgb("#FFFFFF")
                    cell.vertical_anchor = 3
                    for p in cell.text_frame.paragraphs:
                        p.alignment = 1
                        for r in p.runs:
                            r.font.size = fsize
                            r.font.color.rgb = rgb(self.theme["text"])
                            set_east(r, self.cfg.get("body_east", "微软雅黑"))
            # 编辑式极简表格：仅表头底部墨色粗线 + 行间 hairline；无填充、无竖线、无外框。
            _table_hairlines(tbl, n_rows, n_cols, self.theme)
            cur_top = cur_top + tbl_h + Inches(0.15)

        for img_bytes, alt in images:
            try:
                s.shapes.add_picture(io.BytesIO(img_bytes),
                                     self.M + left_w + Inches(0.2), top,
                                     width=(self.W - left_w - self.M - Inches(0.4)))
            except Exception:
                pass

        if notes:
            s.notes_slide.notes_text_frame.text = notes
        self._footer(s, source)
        return s

    def _bullet(self, tf, kind, text, idx, two_col):
        """加粗首关键词 + accent 引导符 / 有序编号 / note 静音灰行。"""
        size = self.cfg.get("body_size", 19)
        east = self.cfg.get("body_east", "微软雅黑")
        space = 7 if two_col else 11
        if kind == "note":
            p = tf.paragraphs[0] if (not tf.paragraphs[0].runs and not tf.paragraphs[0].text) else tf.add_paragraph()
            p.space_after = Pt(space)
            r = p.add_run(); r.text = text; r.font.size = Pt(size - 1)
            r.font.color.rgb = rgb(self.theme["muted"]); set_east(r, east)
            return
        if kind == "ol":
            lead, rest = self._split_keyword(text)
            p = tf.paragraphs[0] if (not tf.paragraphs[0].runs and not tf.paragraphs[0].text) else tf.add_paragraph()
            p.space_after = Pt(space)
            rm = p.add_run(); rm.text = "%02d  " % (idx + 1); rm.font.size = Pt(size)
            rm.font.bold = True; rm.font.color.rgb = rgb(self.theme["ink"]); set_east(rm, east)
            self._kw_runs(p, lead, rest, size, east)
            return
        # bullet / text：灰色短引导符 + 加粗首关键词
        lead, rest = self._split_keyword(text)
        p = tf.paragraphs[0] if (not tf.paragraphs[0].runs and not tf.paragraphs[0].text) else tf.add_paragraph()
        p.space_after = Pt(space)
        rm = p.add_run(); rm.text = "—  "; rm.font.size = Pt(size)
        rm.font.bold = True; rm.font.color.rgb = rgb(self.theme["muted"]); set_east(rm, east)
        self._kw_runs(p, lead, rest, size, east)

    @staticmethod
    def _split_keyword(text):
        """取首个分隔符前的片段作为加粗关键词。"""
        m = re.match(r"^([^，,：:；;。\.\s]+)(.*)$", text)
        if m and m.group(2):
            return m.group(1), m.group(2)
        return text, ""

    def _kw_runs(self, p, lead, rest, size, east):
        """加粗首关键词（墨色）+ 正文（次级墨色）；颜色走主题，不硬编码。"""
        if lead:
            r = p.add_run(); r.text = lead; r.font.size = Pt(size); r.font.bold = True
            r.font.color.rgb = rgb(self.theme["ink"]); set_east(r, east)
        if rest:
            r = p.add_run(); r.text = rest; r.font.size = Pt(size); r.font.bold = False
            r.font.color.rgb = rgb(self.theme["text"]); set_east(r, east)

    def closing_slide(self, source):
        s = self.slide()
        tf = self._tb(s, self.M, Inches(3.0), self.mw, Inches(1.2))
        add_line(tf, "谢谢", self.cfg.get("section_size", 34) + 16,
                 self.cfg.get("title_east", "微软雅黑"), bold=True,
                 color=self.theme["ink"], align=2)
        # 中央短细线（强调色，克制）+ 灰副标；无上下色带
        self._rect(s, (self.W - Inches(1.8)) / 2, Inches(4.3), Inches(1.8), Pt(1.5), self.theme["accent"])
        tf2 = self._tb(s, self.M, Inches(4.6), self.mw, Inches(0.6))
        add_line(tf2, "Omni 解析重建 · 汇报版", 13, self.cfg.get("body_east", "微软雅黑"),
                 color=self.theme["muted"], align=2)
        return s

    def save(self, path):
        os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
        self.prs.save(path)


def chunk(items, max_bullets, max_chars):
    """要点过多/过长时切分为多页，避免溢出不可读。"""
    page, pages, chars = [], [], 0
    for it in items:
        page.append(it)
        chars += len(it[1])
        if len(page) >= max_bullets or chars >= max_chars:
            pages.append(page)
            page, chars = [], 0
    if page:
        pages.append(page)
    return pages or [[]]


# --------------------------------------------------------------------------- #
#  语义版式池（锁定版式契约：版式锁死、数量由内容决定，agent 按内容语义选用）
# --------------------------------------------------------------------------- #
LAYOUTS = ("auto", "kpi", "compare", "timeline")
LAYOUT_RE = re.compile(r"<!--\s*layout\s*:\s*([a-zA-Z]+)\s*-->", re.S)
HEAD_RE = re.compile(r"\s*#{1,6}\s+(.*)")


def scan_layouts(md):
    """扫描 markdown 中的版式指令：`<!-- layout:xxx -->`。

    双向绑定：指令写在标题**之前**→绑定到下一个标题；紧跟标题**之后**→向后绑定
    到该标题。返回 (清理后的 md, {标题文本: 版式名})。未知版式名按 auto 处理。
    """
    layouts, pending, out = {}, None, []
    last_heading = None  # 最近一个尚未绑定版式的标题
    for line in md.splitlines():
        m = LAYOUT_RE.fullmatch(line.strip())
        if m:
            name = m.group(1).lower()
            name = name if name in LAYOUTS else "auto"
            if last_heading is not None and last_heading not in layouts:
                layouts[last_heading] = name  # 向后绑定（指令紧跟标题之后）
                last_heading = None
            else:
                pending = name  # 向前绑定（指令在标题之前）
            continue
        m2 = HEAD_RE.match(line)
        if m2:
            h = plain(m2.group(1)).strip()
            if pending:
                layouts[h] = pending
                pending = None
                last_heading = None
            else:
                last_heading = h
        out.append(line)
    return "\n".join(out), layouts


def build(md, cfg, theme, title=None, section_level=1, split_level=2, max_bullets=6,
          max_chars=760, ratio="16:9", strip=False, embed_images=True, prose="notes",
          max_slides=80, source=""):
    """prose：正文段落去向——notes（默认，进演讲者备注）/ body（上正文区）/ skip（丢弃）。

    汇报语义：要点、表格、图像上页；正文细节进备注页，避免长文档被逐段平铺成上百页。
    """
    if strip:
        md = strip_emoji(md)
    md, foot = extract_footnotes(md)
    t_title, md = extract_title(md)
    md, layouts = scan_layouts(md)  # 版式指令：<!-- layout:xxx --> 绑定到其后第一个标题
    doc_title = title or t_title
    blocks = parse_blocks(md)
    deck = Deck(cfg, theme, ratio)

    if doc_title:
        deck.cover_slide(doc_title, None, source)

    cur_title = None
    cur_items, cur_tables, cur_images, cur_notes = [], [], [], []
    pending_notes = []
    capped = [False]
    sec_idx = [0]
    cur_section = [""]

    def room():
        if max_slides and deck.n_slides >= max_slides:
            capped[0] = True
            return False
        return True

    def flush():
        nonlocal cur_items, cur_tables, cur_images, cur_notes, pending_notes
        notes = "\n".join(x for x in (pending_notes + cur_notes) if x).strip() or None
        if not (cur_items or cur_tables or cur_images):
            if cur_title and cur_title != "要点":
                pending_notes = pending_notes + [cur_title] + cur_notes
            else:
                pending_notes = pending_notes + cur_notes
            cur_notes = []
            return
        t = cur_title or "要点"
        layout = layouts.get((cur_title or "").strip(), "auto") if cur_title else "auto"
        pages = chunk(cur_items, max_bullets, max_chars) if cur_items else [[]]
        for pi, pg in enumerate(pages):
            if not room():
                return
            deck.content_slide(t if pi == 0 else "%s（续 %d）" % (t, pi + 1),
                               cur_section[0] or None, pg, cur_tables if pi == 0 else [],
                               cur_images if pi == 0 else [],
                               notes=(notes if pi == 0 else None), source=source,
                               section=cur_section[0] or None,
                               layout=layout)
        cur_items, cur_tables, cur_images, cur_notes = [], [], [], []
        pending_notes = []

    for kind, payload, _ in blocks:
        if kind == "heading":
            lvl, text = int(payload[0]), plain(payload[1])
            if lvl <= section_level:
                flush()
                cur_title = None
                cur_section[0] = text
                sec_idx[0] += 1
                if room():
                    deck.section_slide(text, sec_idx[0])
                continue
            if lvl <= split_level:
                flush()
                cur_title = text
                continue
            cur_items.append(("bullet", text))
            continue
        if kind in ("ul", "ol"):
            for it in payload:
                cur_items.append((("ol" if kind == "ol" else "bullet"), plain(it)))
            continue
        if kind == "table":
            header, rows = payload
            cur_tables.append((header, rows))
            continue
        if kind == "quote":
            cur_items.append(("note", "“%s”" % plain(payload)))
            continue
        if kind == "visual":
            cur_items.append(("note", "%s %s" % (payload[0], plain(payload[1]))))
            continue
        if kind == "hr":
            continue
        text = plain(payload)
        m = IMG_RE.search(text)
        if m and embed_images and m.group(2).startswith("data:image"):
            try:
                raw = base64.b64decode(m.group(2).split(",", 1)[1])
                cur_images.append((raw, m.group(1)))
                text = IMG_RE.sub("", text).strip()
            except Exception:
                pass
        if not text:
            continue
        if prose == "body":
            cur_items.append(("text", text))
        elif prose == "notes":
            cur_notes.append(text)
    flush()
    # 兜底一：文档无标题层级（扫描件/纯正文）时，正文全落备注会产出空 deck——
    # 此时按要点页平铺，保证有可讲的内容页。
    leftover = [x for x in (pending_notes + cur_notes) if x]
    if leftover and deck.n_slides <= (1 if doc_title else 0):
        pages = chunk([("bullet", t) for t in leftover], max_bullets, max_chars)
        for pi, pg in enumerate(pages):
            if not room():
                break
            deck.content_slide("要点" if pi == 0 else "要点（续 %d）" % (pi + 1),
                               cur_section[0] or None, pg,
                               source=source, section=cur_section[0] or None)
        leftover = []
    # 兜底二：deck 正常时，尾部纯正文（如免责声明节）残留的备注不得静默丢弃——
    # 追加到最后一张幻灯片的演讲者备注，保证这一段正文不在这条路径上消失。
    if leftover and deck.prs.slides:
        try:
            last = deck.prs.slides[-1]
            tf = last.notes_slide.notes_text_frame
            tf.text = (tf.text or "") + ("\n" if tf.text else "") + "\n".join(leftover)
        except Exception:
            pass
    if foot:
        try:
            last = deck.prs.slides[-1]
            tf = last.notes_slide.notes_text_frame
            tf.text = (tf.text or "") + "\n注释：" + "；".join(
                "%s %s" % (k, plain(v)) for k, v in foot)
        except Exception:
            pass
    # 结束页
    if room():
        deck.closing_slide(source)
    if capped[0]:
        sys.stderr.write("警告：达到 --max-slides=%d 上限，已截断；"
                         "建议 agent 先提炼提纲再渲染 deck。\n" % max_slides)
    return deck


def main():
    ap = argparse.ArgumentParser(description="文档/提纲 → 汇报用 PPTX deck")
    ap.add_argument("--json", help="中间 JSON（markdown+grounding+outline）")
    ap.add_argument("--md", help="markdown 文件（agent 按 slide 组织好的提纲）")
    ap.add_argument("--out", required=True, help="输出 .pptx")
    ap.add_argument("--profile", default="default",
                    help="deck 制式：default/gov/legal/finance/academic，或内联 JSON / .json 文件")
    ap.add_argument("--title", help="deck 标题")
    ap.add_argument("--section-level", type=int, default=1,
                    help="≤该层级的标题生成章节页（默认 1）")
    ap.add_argument("--split-level", type=int, default=2,
                    help="≤该层级的标题另起内容页（默认 2）")
    ap.add_argument("--max-bullets", type=int, default=6, help="每页最多要点数（超出续页）")
    ap.add_argument("--max-chars", type=int, default=760, help="每页正文字符上限（超出续页）")
    ap.add_argument("--prose", default="notes", choices=["notes", "body", "skip"],
                    help="正文段落去向：notes=演讲者备注（默认，汇报语义）/ body=上正文区 / skip=丢弃")
    ap.add_argument("--ratio", default="16:9", help="16:9 / 4:3 / 自定义 'w,h'（英寸）")
    ap.add_argument("--strip-emoji", action="store_true", help="剥离 emoji/装饰符（验收器同口径）")
    ap.add_argument("--no-images", action="store_true", help="不嵌入 data:image 图像")
    ap.add_argument("--max-slides", type=int, default=80,
                    help="deck 页数上限（默认 80；超出即截断并告警）。0=不限")
    ap.add_argument("--source-label", default="", help="页脚来源署名（默认空）")
    args = ap.parse_args()
    if not args.json and not args.md:
        ap.error("--json 或 --md 必须提供一个")

    p = args.profile.strip()
    if p.startswith("{"):
        cfg = dict(PPT_PROFILES["default"]); cfg.update(json.loads(p))
        theme = dict(THEMES["default"])
    elif p.endswith(".json"):
        cfg = dict(PPT_PROFILES["default"])
        cfg.update(json.load(open(p, encoding="utf-8")))
        theme = dict(THEMES["default"])
    else:
        if p in PPT_PROFILES:
            cfg = PPT_PROFILES[p]
        elif p in DOC_PROFILES:
            d = DOC_PROFILES[p]
            cfg = {"title_east": d.get("heading_east", "微软雅黑"),
                   "body_east": d.get("body_east", "微软雅黑"),
                   "title_size": 30, "body_size": 19, "section_size": 34}
        else:
            ap.error("--profile 未知预设 %r（可选：%s，或 JSON 自定义）"
                     % (p, "/".join(sorted(PPT_PROFILES))))
        theme = THEMES.get(p, THEMES["default"])

    if args.md:
        data = {"markdown": open(args.md, encoding="utf-8").read(), "source": args.md}
    else:
        data = json.load(open(args.json, encoding="utf-8"))

    if data.get("sources") or data.get("analysis"):
        sources = list(data.get("sources") or [])
        analysis = data.get("analysis")
        if analysis:
            ana = dict(analysis) if isinstance(analysis, dict) else {"markdown": str(analysis)}
            ana.setdefault("source", "整合分析")
            sources.insert(0, ana)
    else:
        sources = [data]

    src_label = args.source_label or (sources[0].get("source") if len(sources) == 1 else "")

    if len(sources) > 1:
        merged = []
        for i, s in enumerate(sources):
            name = (s.get("source") or "来源 %d" % (i + 1)).strip()
            merged.append("# %s\n\n%s" % (name, s.get("markdown") or ""))
        data_md = "\n\n".join(merged)
        deck = build(data_md, cfg, theme, title=args.title,
                     section_level=args.section_level, split_level=args.split_level,
                     max_bullets=args.max_bullets, max_chars=args.max_chars,
                     ratio=args.ratio, strip=args.strip_emoji,
                     embed_images=not args.no_images, source=src_label)
    else:
        deck = build(sources[0].get("markdown") or "", cfg, theme, title=args.title,
                     section_level=args.section_level, split_level=args.split_level,
                     max_bullets=args.max_bullets, max_chars=args.max_chars,
                     ratio=args.ratio, strip=args.strip_emoji,
                     embed_images=not args.no_images, source=src_label)
    deck.save(args.out)
    from pptx import Presentation as P
    n = len(P(args.out).slides)
    print("PPTX 已生成：%s（%d 页，%d 字节）"
          % (os.path.abspath(args.out), n, os.path.getsize(args.out)))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
export_pdf.py — 把 StyleSpec + content.json 渲染成 mm 级定位的 **PDF 版面稿**。

为什么单独存在：HTML 版面稿依赖浏览器渲染，一旦受众那边打不开（预览器、
策略禁用 headless、缺字体）就变成「空文件」。PDF 是自洽的：字嵌入版面里，
拿到就有内容。同一份 content.json 出的两个版本，页码与内容一一对应。

用法：
  python export_pdf.py --spec assets/stylespec.json --content content.json --out build/draft.pdf
  python export_pdf.py --content content.json --out draft.pdf --no-autoflow

依赖：`python -m pip install pymupdf`。版式规则与 build_draft.py 共用
同一套网格与高度估算（import 过来复用，不是复制粘贴的第二套）。

命令里的 `python`：Windows 用 `python`，macOS/Linux 用 `python3`。
"""
import argparse
import io
import json
import math
import os
import re
import sys

try:
    import pymupdf
except ImportError:  # pragma: no cover
    sys.stderr.write("[FATAL] 需要 PyMuPDF：python -m pip install pymupdf\n")
    sys.exit(2)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_draft as BD  # noqa: E402  复用网格 / 分页 / 高度估算

# --cta-domain：CTA 行带来源域名（纸刊溯源用），默认关。
CTA_DOMAIN = False

MM_PT = BD.MM_PT          # 1pt = 0.3528mm
MM = 1.0 / BD.MM_PT       # 1mm = 2.8346pt

# 给 insert_htmlbox 的框留的高度余量：内容装不下时它会**静默缩字**（详见 put() 内注释）。
# 1.25 是按实测定的：请求 20pt / 框高 60pt 出 14.28pt，需要约 1.4 倍才不缩；
# 但给满 1.4 会让块与块的视觉间距变松，故取 1.25 兜住绝大多数情况，
# 余下的极端长段由 audit_layout.py 的 body_pt 门禁兜底报出来。
FIT_SLACK = 1.25

# ── 行距换算 ────────────────────────────────────────────────────────
# MuPDF 的 CSS line-height 是乘在**字体自然行盒**（实测约 1.22em）上的，不是乘在字号上。
# 于是写 leading=1.75，成品基线距是 1.75×1.22＝**2.15 倍字号**；
# 而真实刊物（衡石《衡石深度观察》实测 13pt/24.0pt）是 **1.85 倍**。
# 2.15 倍配上正文小字，正是「字小且散」的观感来源。
# LINE_ADJ 把设计值换算成 CSS 值（1.75×0.87≈1.52 → 成品约 1.85 倍），
# LINEBOX 用于把行高估算补到真实高度——估算偏小正是上面缩字的另一个成因。
LINE_ADJ = 0.87
LINEBOX = 1.22

# 让 BD 的分页高度估算用 PDF 的真实行盒口径（详见 build_draft.LINE_H_FACTOR 注释）。
# 必须在任何 BD.expand_pages / block_height_mm 调用之前设置。
BD.LINE_H_FACTOR = LINE_ADJ * LINEBOX


def line_h_mm(size, leading):
    """一行的真实高度（mm）。高度估算必须用它，不能用 size*leading 直接折算。"""
    return size * MM_PT * leading * LINE_ADJ * LINEBOX


def pt(mmv):
    return float(mmv) * MM


def rgb(hexstr, default=(0, 0, 0)):
    r, g, b = BD.hex_rgb(hexstr or "")
    try:
        return (int(r) / 255.0, int(g) / 255.0, int(b) / 255.0)
    except Exception:
        return default


def esc(s):
    return BD.esc(s or "")


def lbl(text):
    """结构字段用：只转义，不收紧空格。「2026.04.10 香港金融管理局」的空格是有意的。

    但要收紧**纯中文日期/期号**里的空格：页脚固定件常写成「2026 年第 8 期」，
    实测（2026-09-18，第 27 期 80 页）这句被原样印进每一页页脚，共 73 处；
    两端对齐时「2026 年」的空格被拉到极限，页脚一行字散成碎块。
    这里只收紧「数字＋年月日期号卷册章」与「第＋数字」两类，
    「2026.04.10 香港金融管理局」这类「数字＋空格＋普通汉字」的结构空格仍然保留。
    """
    t = esc(str(text or ""))
    t = re.sub(r"([0-9]) +([年月日期号卷册章季度])", r"\1\2", t)
    t = re.sub(r"([第]) +([0-9])", r"\1\2", t)
    return t


def _br2nl(t):
    """源数据里的 <br> 归一成真换行。

    必须在 esc() 之前做：否则 <br> 会被转义成字面文本，在 PDF 上印出
    "责任编辑：苗青顾青禾<br>编辑部邮箱：xxx" 这种东西，而 HTML 那边是正常换行的。
    """
    return re.sub(r"(?i)<br\s*/?>", "\n", str(t or ""))


def md(text):
    """极简富文本：**加粗** / __强调__ → <b> / <i>。
    注意别把 BD.text_em 当文本清洗用——它是 em 宽度估算，返回值是 float。"""
    t = BD.zh_space(esc(_br2nl(text)))
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"__(.+?)__", r"<i>\1</i>", t)
    return t.replace("\n", "<br>")


def lines(text, width_mm, size_pt):
    return BD.lines_of(text, width_mm, size_pt)


class Sheet(object):
    """一页纸。维护垂直游标 y(mm)，提供 put / fill / skip。"""

    def __init__(self, page, W, H, pal, families):
        self.p = page
        self.W, self.H = W, H
        self.pal = pal
        self.fam = ",".join('"%s"' % f for f in families)
        self.y = 0.0
        self.warn = []

    # --- 图元 -----------------------------------------------------------
    def fill(self, x, y, w, h, color):
        self.p.draw_rect(pymupdf.Rect(pt(x), pt(y), pt(x + w), pt(y + h)),
                         color=None, fill=rgb(color, (0.63, 0.06, 0.20)))

    def line(self, x, y, w, color, th=0.4):
        self.p.draw_line(pymupdf.Point(pt(x), pt(y)),
                         pymupdf.Point(pt(x + w), pt(y)),
                         color=rgb(color, (0.63, 0.06, 0.20)), width=th)

    def poly(self, points_mm, color):
        shp = self.p.new_shape()
        shp.draw_polyline([pymupdf.Point(pt(a), pt(b)) for a, b in points_mm])
        shp.finish(fill=rgb(color, (1, 1, 1)), closePath=True)
        shp.commit()

    def image(self, path, x, y, w, h):
        try:
            self.p.insert_image(pymupdf.Rect(pt(x), pt(y), pt(x + w), pt(y + h)),
                                filename=path)
            return True
        except Exception as e:
            self.warn.append("插图失败 %s (%s)" % (os.path.basename(str(path)), e))
            return False

    # --- 文字 -----------------------------------------------------------
    def put(self, html, x, y, w, h, size=10.4, leading=1.6, color=None,
            weight="normal", align="left", minh=None):
        """把一段 HTML 写进矩形；返回实际占用高度(mm)。"""
        if not html:
            return 0.0
        hh = max(float(h), float(minh or line_h_mm(size, leading) * 1.05))
        # ── 静默缩字防线 ──────────────────────────────────────────────
        # 实测（2026-09-18，PyMuPDF 1.28.2）：insert_htmlbox 在内容装不下时会
        # **自动缩小字号来塞进框里**，而且返回值 rest 变成 >=0，不会报溢出——
        # 请求 20pt / 框高 60pt 实测只渲染出 14.28pt；框高 20pt 出 7.69pt；
        # 框高 8pt 出 3.08pt。脚本零报错、页面看着正常，字却小了一档。
        # 一本真实交付稿因此把正文 10.4pt 印成 8.4–9.9pt 的 41 个不同字号
        # （每个框内容量不同 → 缩放比例不同），观感就是「字小且散」。
        # 对策：给框留 FIT_SLACK 余量，并夹到页底，保证不会越页。
        hh = min(hh * FIT_SLACK, (self.p.rect.height / MM_PT) - float(y))
        css = ("*{margin:0;padding:0}"
               " p{font-family:%s;font-size:%.2fpt;line-height:%.2f;color:%s;"
               "font-weight:%s;text-align:%s}" %
               (self.fam, size, leading * LINE_ADJ,
                color or self.pal["text"], weight, align))
        frag = html if html.lstrip().startswith("<") else "<p>%s</p>" % html
        r = pymupdf.Rect(pt(x), pt(y), pt(x + w), pt(y + hh))
        try:
            rest = self.p.insert_htmlbox(r, frag, css=css)
        except TypeError:  # 老版本没有 css 参数
            frag = frag.replace("font-family:%s" % self.fam, "")
            try:
                rest = self.p.insert_htmlbox(r, frag)
            except Exception:
                self.warn.append("文字块写入失败: %s" % re.sub(r"<[^>]+>", "", frag)[:30])
                return 0.0
        if isinstance(rest, (int, float)) and rest < -1:
            self.warn.append("文字溢出 %.1fmm @ y=%.0f: %s"
                             % (-rest, y, re.sub(r"<[^>]+>", "", frag)[:30]))
        return hh

    def para(self, text, x, w, size=None, leading=1.75, color=None, weight="normal",
             align="left", lhmm=None, gap=0.0):
        """写一段正文并按行数推进游标。lhmm 为 None 时按 pt 折算行高。"""
        size = size or BD.DEF_BODY_PT
        n = lines(_br2nl(text), w, size)
        lh = lhmm if lhmm is not None else line_h_mm(size, leading)
        hh = n * lh
        self.put(md(text), x, self.y, w, hh, size=size, leading=leading,
                 color=color, weight=weight, align=align)
        self.y += hh + gap
        return hh


# --------------------------------------------------------------------------
# 组件
# --------------------------------------------------------------------------

def draw_chrome(sh, p, pal, has_bg, footer_on=True):
    """页眉 running text + 页脚 foot_text / folio。"""
    rt = p.get("running_text")
    if rt:
        sh.put(lbl(rt), 0, 8.0, sh.W - 18.0, 6.0, size=9.0, leading=1.2,
               color=pal["primary"], align="right")
    if not footer_on:
        return
    ft = p.get("foot_text") or ""
    folio = str(p.get("folio") or "")
    y = sh.H - 15.0
    sh.line(18.0, y - 2.0, sh.W - 36.0, "#E3E3E3", 0.3)
    if ft:
        sh.put(lbl(ft), 18.0, y, sh.W - 60.0, 5.0, size=9.0, leading=1.2,
               color=pal["meta_paper"])
    if folio:
        sh.put(lbl(folio), sh.W - 50.0, y, 30.0, 5.0, size=9.0, leading=1.2,
               color=pal["meta_paper"], weight="bold", align="right")


def draw_cover(sh, p, pal, root):
    f = p.get("fields") or {}
    bg = p.get("images", {}).get("bg") or p.get("bg")
    if bg and sh.image(BD.img_src(bg, root) if hasattr(BD, "img_src") else bg,
                       0, 0, sh.W, sh.H):
        dark = True
    else:
        # 无封面图：主色斜切 + 大刊名，不留白
        sh.fill(0, 0, sh.W, sh.H * 0.58, pal["primary"])
        sh.poly([(0, sh.H * 0.58), (sh.W, sh.H * 0.44),
                 (sh.W, sh.H), (0, sh.H)], "#FFFFFF")
        dark = True
    fg = "#FFFFFF" if dark else pal["text"]

    sh.y = 20.0
    if f.get("org"):
        sh.put(md(f["org"]), 20.0, sh.y, 110.0, 6.0, size=10.0, leading=1.3, color=fg)
    sh.y = 92.0
    if f.get("title"):
        sh.para(f["title"], 20.0, sh.W - 40.0, size=32.0, leading=1.25,
                color=fg, weight="bold", gap=4.0)
    if f.get("subtitle"):
        sh.para(f["subtitle"], 20.0, sh.W - 40.0, size=10.5, leading=1.5,
                color=fg, gap=3.0)
    sh.fill(20.0, sh.y + 2.0, 26.0, 0.8, fg)
    sh.y += 12.0
    # schema 里是 issue_no / yearmonth / year，早期用过 issue_date；三个都认，
    # 只写 year 会把封面做成「第22期 | 2026」，期号年月凭空消失
    meta = "  |  ".join([str(f.get(k, "")) for k in ("issue_no", "yearmonth", "year")
                         if f.get(k)])
    if meta:
        sh.para(meta, 20.0, sh.W - 40.0, size=12.0, leading=1.5, color=fg, gap=2.0)
    if f.get("year"):
        sh.put(md(f["year"]), 20.0, sh.H - 34.0, 80.0, 18.0, size=42.0,
               leading=1.0, color=pal["primary"], weight="bold")


def draw_quote(sh, p, pal):
    f = p.get("fields") or {}
    sh.y = 78.0
    if f.get("quote"):
        sh.put(md("“"), 19.0, sh.y - 6.0, 20.0, 16.0, size=44.0, leading=1.0,
               color=pal["primary"])
        sh.y += 16.0
        sh.para(f.get("quote", ""), 19.0, 150.0, size=14.0, leading=1.8,
                color=pal["primary"], weight="bold", gap=8.0)
    if f.get("source"):
        # 源数据常自带「——」前缀，再拼一次会出现四个破折号，与 HTML 版也不一致
        src = _br2nl(f["source"]).strip()
        if not src.startswith("—"):
            src = "——" + src
        sh.para(src, 19.0, 140.0, size=11.0, leading=1.6,
                color=pal["sec_paper"], align="right", gap=0.0)


def draw_masthead(sh, p, pal):
    f = p.get("fields") or {}
    sh.y = 60.0
    if f.get("title"):
        sh.para(f["title"], 100.0, sh.W - 118.0, size=12.0, leading=1.5,
                color=pal["primary"], weight="bold", gap=5.0)
    names = f.get("names") or []
    if names:
        sh.para(" / ".join(names), 100.0, sh.W - 118.0, size=9.0, leading=1.9,
                color=pal["text"], gap=5.0)
    if f.get("note"):
        sh.para(f["note"], 100.0, sh.W - 118.0, size=9.0, leading=1.6,
                color=pal["sec_paper"])


def draw_toc(sh, p, pal, anchor_map):
    f = p.get("fields") or {}
    sh.y = 30.0
    if f.get("title"):
        sh.para(f["title"], 110.0, 70.0, size=21.5, leading=1.4,
                color="#B0B0B0", align="right", gap=10.0)
    for g in f.get("groups", []):
        sh.fill(31.0, sh.y, sh.W - 62.0, 0.5, pal["primary"])
        sh.y += 4.0
        sh.put("<p>%s&nbsp;&nbsp;%s</p>" % (md(g.get("no", "")), md(g.get("title", ""))),
               31.0, sh.y, sh.W - 62.0, 8.0, size=12.0, leading=1.3,
               color=pal["primary"], weight="bold")
        sh.y += 12.0
        for it in f.get("items", []) if False else (g.get("items") or []):
            pgnum = it.get("page") or anchor_map.get(it.get("ref", ""), "")
            title = it.get("title", "")
            lead = "·" * max(2, int((sh.W - 100.0) / 3.0) - int(len(title) * 1.6))
            frag = ("<p>%s <span style='color:#CFCFCF'>%s</span> "
                    "<span style='color:%s;font-weight:bold'>%s</span></p>"
                    % (md(title), lead, pal["meta_paper"], esc(pgnum)))
            n = max(1, lines(title, sh.W - 100.0, BD.DEF_BODY_PT))
            sh.put(frag, 31.0, sh.y, sh.W - 62.0, n * 6.2, size=BD.DEF_BODY_PT,
                   leading=1.6)
            sh.y += n * 6.2 + 3.0



def _resolve_img(p, root):
    """图源路径解析：content.json 里图多是相对路径（art/diagrams/fig_0.png）。

    只看相对路径 = 只在 cwd 恰好是期刊根目录时才找得到；换目录跑（例如从
    _tools 里调脚本）就会整本静默降级成空图位，图注还在、图没了，看不出来。
    兜底顺序：原样 → 剥掉 file:// 前缀 → 相对 content.json 所在目录。
    读不到就原样返回，由调用方走空图位并显式告警（不再静默）。
    """
    if not p:
        return ""
    s = str(p)
    low = s.lower()
    if low.startswith("file:///"):
        s = s[8:]
    elif low.startswith("file://"):
        s = s[7:]
    if os.path.isfile(s):
        return s
    if root and not os.path.isabs(s):
        cand = os.path.join(root, s)
        if os.path.isfile(cand):
            return cand
    return s


def img_mm(path, max_w, max_h=110.0):
    """按图片真实比例算出摆放尺寸(mm)：先撑满可用宽度，超高再按上限回收。

    早先 figure 是塞进固定 52mm 高的框里等比缩放的，实测 1.6:1 的横图只占到
    84.6mm —— 版心 172mm 的一半，右侧大片空白；而 plan 侧按版心宽算出的
    2031px 又白多了两倍像素。这里改成按比例撑宽，两边的口径才对得上。
    """
    try:
        px = pymupdf.Pixmap(path)
        ratio = px.width / float(px.height or 1)
    except Exception:
        ratio = float(max_w) / float(max_h)
    tw = float(max_w)
    th = tw / ratio if ratio else float(max_h)
    if th > max_h:
        th = float(max_h)
        tw = th * ratio
    return tw, th


def draw_divider(sh, p, pal, idx):
    f = p.get("fields") or {}
    bg = p.get("images", {}).get("bg") or p.get("bg")
    if not (bg and sh.image(bg, 0, 0, sh.W, sh.H)):
        sh.fill(0, 0, sh.W, sh.H, pal["primary"])
    sh.put(md(str(f.get("no") or idx or "")), 0, 78.0, sh.W, 34.0, size=58.0,
           leading=1.0, color="#FFFFFF", weight="bold", align="center")
    sh.put(md(f.get("label", "")), 0, 132.0, sh.W, 14.0, size=20.0, leading=1.4,
           color="#FFFFFF", weight="bold", align="center")
    sh.fill(sh.W / 2 - 15.0, 156.0, 30.0, 0.6, "#FFFFFF")
    # content-schema 与 build_draft 用 subtitle，早期写法用过 sub，两种都要认
    sub = f.get("subtitle") or f.get("sub")
    if sub:
        sh.put(md(sub), 0, 164.0, sh.W, 7.0, size=9.5, leading=1.4,
               color="#FFFFFF", align="center")


def draw_unit_list(sh, p, L, pal, cont):
    f = p.get("fields") or {}
    g = BD.grid_of(L, p.get("grid", "A"))
    x = float(g["left_mm"])
    w = float(g["right_mm"]) - float(g["left_mm"])
    top = float(p.get("top_mm", 42.0)) if not cont else float(p.get("cont_top_mm", 22.0))
    sh.y = top

    if not cont:
        if f.get("kicker"):
            sh.put(lbl(f["kicker"]), x, sh.y, w, 5.0, size=8.5, leading=1.4,
               color=pal["primary"], weight="bold")
            sh.y += 8.0
        if f.get("section"):
            sh.para(f["section"], x, w, size=18.0, leading=1.35, color=pal["primary"],
                    weight="bold", gap=3.0)
        if f.get("dek"):
            sh.line(x, sh.y + 1.0, 0.5, pal["primary"], 0.6)
            sh.put(md(f["dek"]), x + 4.0, sh.y, w - 4.0,
                   lines(f["dek"], w - 8.0, 9.0) * 5.6, size=9.0, leading=1.9,
                   color=pal["sec_paper"])
            sh.y += lines(f["dek"], w - 8.0, 9.0) * 5.6 + 6.0
    else:
        if f.get("section"):
            sh.para("%s（续）" % f["section"], x, w, size=9.0, leading=1.4,
                    color=pal["primary"], gap=5.0)

    bp = L["body_pt"]
    for u in p.get("units", []):
        if u.get("title"):
            sh.line(x, sh.y + 3.0, 0.7, pal["primary"], 0.9)
            sh.put(md(u["title"]), x + 5.0, sh.y, w - 5.0,
                   lines(u["title"], w - 5.0, bp) * 6.4, size=bp, leading=1.5,
                   weight="bold")
            sh.y += lines(u["title"], w - 5.0, bp) * 6.4 + 1.5
        if u.get("meta"):
            sh.put(lbl(u["meta"]), x + 5.0, sh.y, w - 5.0, 5.0, size=8.5, leading=1.5,
               color=pal["meta_paper"])
            sh.y += 7.5
        for para in str(u.get("body", "")).split("\n\n"):
            if para.strip():
                sh.para(para, x + 5.0, w - 5.0, leading=L["leading"], gap=2.5,
                        align="left")
        _ct, _hr = BD.cta_parts(u)
        if _ct and CTA_DOMAIN and _hr:
            _d = BD.cta_domain(_hr)
            if _d:
                _ct = "%s · %s" % (_ct, _d)
        if _ct:
            sh.put(md(_ct), x, sh.y - 1.0, w, 6.0, size=bp, leading=1.4,
                   color=pal["primary"], weight="bold", align="right")
            if _hr:
                # 纸面上看不出区别，但电子刊里这一行是可点的 URI 链接。
                # 热区取右半栏：CTA 是右对齐的，左半留白不该被点中。
                try:
                    sh.p.insert_link({
                        "kind": pymupdf.LINK_URI, "uri": _hr,
                        "from": pymupdf.Rect(pt(x + w * 0.5), pt(sh.y - 1.0),
                                             pt(x + w), pt(sh.y + 5.0))})
                except Exception as e:
                    sh.warn.append("CTA 链接写入失败（%s）" % str(e)[:40])
            sh.y += 6.0
        img = None
        if isinstance(u.get("image"), dict):
            img = u["image"].get("path")
        elif isinstance(u.get("image"), str):
            img = u["image"]
        if img and os.path.exists(img):
            sh.image(img, x + 5.0, sh.y, w - 5.0, 45.0)
            sh.y += 48.0
        sh.y += 4.0


def draw_article(sh, p, L, pal, cont, root):
    f = p.get("fields") or {}
    g = BD.grid_of(L, p.get("grid", "B"))
    x = float(g["left_mm"])
    w = float(g["right_mm"]) - float(g["left_mm"])
    top = float(p.get("top_mm", 20.0)) if not cont else float(p.get("cont_top_mm", 22.0))
    sh.y = top
    bp = L["body_pt"]

    hero = None
    if isinstance(f.get("hero"), dict):
        hero = f["hero"].get("path")
    elif isinstance(f.get("hero"), str):
        hero = f["hero"]
    if not cont and hero and os.path.exists(hero):
        sh.image(hero, x, sh.y, w, 55.0)
        sh.y += 61.0

    if not cont:
        if f.get("section"):
            sh.para(f["section"], x, w, size=8.5, leading=1.4, color=pal["primary"],
                    weight="bold", gap=3.0)
        if f.get("title"):
            sh.para(f["title"], x, w, size=16.0, leading=1.35, color=pal["primary"],
                    weight="bold", gap=4.0)
        if f.get("byline"):
            hh=int(lines(f["byline"], w, 9.0))*5.2
            sh.put(lbl(f["byline"]), x, sh.y, w, hh, size=9.0, leading=1.5,
                   color=pal["meta_paper"], align="right")
            sh.y += hh + 6.0
        if f.get("abstract"):
            ab = f["abstract"]
            n = lines(ab, w - 10.0, 9.0)
            sh.fill(x, sh.y, 0.6, n * 5.4 + 8.0, pal["primary"])
            sh.fill(x, sh.y, w, n * 5.4 + 8.0, "#FAFAFA")
            sh.put(md(ab), x + 5.0, sh.y + 4.0, w - 10.0, n * 5.4, size=9.0,
                   leading=1.9, color=pal["sec_paper"])
            sh.y += n * 5.4 + 12.0
    elif f.get("title"):
        sh.para("%s（续）" % f["title"], x, w, size=9.0, leading=1.4,
                color=pal["primary"], gap=6.0)

    for b in p.get("blocks", []):
        bt = (b.get("type") or "p").lower()
        txt = str(b.get("text", ""))
        if bt in ("h1",):
            n = lines(txt, w - 8.0, 11.5)
            sh.fill(x, sh.y + 1.0, 0.9, n * 7.2, pal["primary"])
            sh.put(md(txt), x + 4.0, sh.y, w - 4.0, n * 7.2, size=11.5,
                   leading=1.5, color=pal["primary"], weight="bold")
            sh.y += n * 7.2 + 5.0
        elif bt in ("h2",):
            sh.para(txt, x, w, size=bd_or(bp), leading=1.5, weight="bold", gap=3.0)
        elif bt in ("li", "bullet"):
            sh.para("• " + txt, x, w - 3.0, leading=L["leading"], gap=2.0,
                    align="left")
        elif bt in ("quote",):
            n = lines(txt, w - 8.0, bp)
            sh.fill(x, sh.y, 0.6, n * 5.6, pal["primary"])
            sh.put(md(txt), x + 4.0, sh.y, w - 8.0, n * 5.6, size=bp,
                   leading=1.75, color=pal["sec_paper"], align="left")
            sh.y += n * 5.6 + 6.0
        elif bt in ("note", "disclaimer", "abstract"):
            sh.para(txt, x, w, size=8.5, leading=1.7, color=pal["sec_paper"], gap=4.0)
        elif bt in ("fig", "figure"):
            raw = b.get("path") or b.get("src")
            path = _resolve_img(raw, root)
            if path and os.path.isfile(path):   # isfile：目录也会 exists() 为真，不能当图片
                tw, th = img_mm(path, w, max_h=110.0)
                sh.image(path, x + (w - tw) / 2.0, sh.y, tw, th)
                sh.y += th + 3.0
            else:
                n = 3
                sh.fill(x, sh.y, w, 16.0, "#F4F4F4")
                sh.put(md(BD.caption_core(b.get("caption")) or "【图位待补】"), x, sh.y + 5.0, w, 6.0,
                       size=8.5, leading=1.4, color="#9A9A9A", align="center")
                sh.y += 20.0
                sh.warn.append("空图位（图源不可读：%s）：%s"
                               % ((raw or "(无路径)")[:40],
                                  (b.get("caption") or "(无图注)")[:26]))
            if b.get("caption"):
                sh.para(b["caption"], x, w, size=8.5, leading=1.5,
                        color=pal["sec_paper"], gap=3.0)
        else:
            sh.para(txt, x, w, leading=L["leading"], gap=2.5, align="left")

    if f.get("disclaimer"):
        n = lines(f["disclaimer"], w - 8.0, 8.5)
        sh.fill(x, sh.y + 2.0, w, n * 4.9 + 8.0, "#F5F5F5")
        sh.put(md(f["disclaimer"]), x + 4.0, sh.y + 6.0, w - 8.0, n * 4.9,
               size=8.5, leading=1.7, color=pal["sec_paper"])
        sh.y += n * 4.9 + 12.0


def bd_or(v):
    return v


def draw_backcover(sh, p, pal):
    f = p.get("fields") or {}
    cols = int(f.get("cols") or 4)
    x0, y0 = 18.0, 16.0
    total = sh.W - 36.0
    cw = total / max(1, cols)
    sh.y = y0
    if f.get("title"):
        sh.put(md(f["title"]), x0, sh.y, total, 8.0, size=12.0, leading=1.4,
               color=pal["primary"], weight="bold")
        sh.y += 12.0
    # content-schema 里封底用 contacts（{name, lines[]}），早期写法用过 groups，
    # 两种都要支持：只认 groups 时，按 schema 填的封底会在 PDF 里整页消失，
    # 而 HTML 那边照常显示 —— 三件套不一致，且是静默的。
    groups = f.get("groups") or []
    if not groups:
        groups = [{"title": c.get("name", ""), "lines": c.get("lines") or []}
                  for c in (f.get("contacts") or [])]
    rowTop = sh.y
    maxbot = rowTop
    for gi, g in enumerate(groups):
        cx = x0 + (gi % cols) * cw
        rowTop = max(rowTop, y0 + 12.0)
        cy = maxbot if gi % cols == 0 and gi else maxbot
        pass
    # 简化：按列分组顺序自上而下滚动排版
    cy = sh.y
    for gi, g in enumerate(groups):
        cx = x0 + (gi % cols) * cw
        if gi % cols == 0 and gi:
            cy = maxbot + 6.0
        yy = cy
        if g.get("title"):
            sh.put(md(g["title"]), cx, yy, cw - 8.0, 6.0, size=8.0, leading=1.4,
                   color=pal["primary"], weight="bold")
            yy += 7.0
        body = "\n".join(str(x) for x in (g.get("lines") or []) if x)
        if body:
            n = lines(body, cw - 8.0, 7.5)
            sh.put(md(body), cx, yy, cw - 8.0, n * 4.6, size=7.5, leading=1.85,
                   color=pal["sec_paper"])
            yy += n * 4.6
        maxbot = max(maxbot, yy + 2.0)


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", default=None)
    ap.add_argument("--content", required=True)
    ap.add_argument("--out", default="draft.pdf")
    ap.add_argument("--no-autoflow", action="store_true")
    ap.add_argument("--jpeg-quality", type=int, default=85)
    ap.add_argument("--cta-domain", action="store_true",
                    help="CTA 行带上来源域名（例：阅读原文 · info.gov.hk），纸刊也能溯源")
    a = ap.parse_args()
    global CTA_DOMAIN
    CTA_DOMAIN = bool(a.cta_domain)

    spec = {}
    if a.spec and os.path.exists(a.spec):
        spec = json.load(io.open(a.spec, encoding="utf-8"))
    content = json.load(io.open(a.content, encoding="utf-8"))
    # 图源基准目录：content.json 在哪，图就从哪找（见 build_draft.CONTENT_ROOT 注释）。
    # 必须在 expand_pages 之前设置——分页估算要按图的真实高度算。
    BD.CONTENT_ROOT = os.path.dirname(os.path.abspath(a.content))
    L = BD.build_layout(spec)
    pal = L["pal"]
    issue = content.get("issue") or {}

    expanded = BD.expand_pages(L, content, not a.no_autoflow)

    # ---- 页码 + anchor 映射（与 HTML 版同一套规则）----
    auto_folio = bool(issue.get("auto_folio"))
    n = 0
    anchor_map = {}
    for q, cont in expanded:
        tpl = q.get("template", "article")
        if q.get("folio") in (None, "", False) and auto_folio and tpl in BD.FOLIO_TPLS:
            n += 1
            q["folio"] = "%02d" % n
        anc = q.get("anchor")
        if anc and not cont and q.get("folio"):
            anchor_map.setdefault(anc, str(q["folio"]))
    L["anchor_map"] = anchor_map

    out_dir = os.path.dirname(os.path.abspath(a.out))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    root = os.path.dirname(os.path.abspath(a.content))

    doc = pymupdf.open()
    allwarn = []
    for i, (p, cont) in enumerate(expanded):
        tpl = p.get("template", "article")
        pg = doc.new_page(width=pt(L["W"]), height=pt(L["H"]))
        sh = Sheet(pg, L["W"], L["H"], pal, L["families"])

        bgrel = p.get("images", {}).get("bg") or p.get("bg")
        if bgrel and tpl not in ("cover", "divider", "backcover"):
            bgabs = bgrel if os.path.isabs(bgrel) else os.path.join(root, bgrel)
            sh.image(bgabs, 0, 0, L["W"], L["H"])

        if tpl not in ("cover", "divider"):
            if not p.get("running_text") and issue.get("running_text"):
                p["running_text"] = issue["running_text"]
            if not p.get("foot_text") and issue.get("foot_text"):
                p["foot_text"] = issue["foot_text"]

        try:
            if tpl == "cover":
                draw_cover(sh, p, pal, root)
            elif tpl == "quote":
                draw_quote(sh, p, pal)
                draw_chrome(sh, p, pal, False, footer_on=False)
            elif tpl == "masthead":
                draw_masthead(sh, p, pal)
                draw_chrome(sh, p, pal, False, footer_on=False)
            elif tpl == "toc":
                draw_toc(sh, p, pal, anchor_map)
                draw_chrome(sh, p, pal, False)
            elif tpl == "divider":
                draw_divider(sh, p, pal, i + 1)
            elif tpl == "unit_list":
                draw_unit_list(sh, p, L, pal, cont)
                draw_chrome(sh, p, pal, False)
            elif tpl == "article":
                draw_article(sh, p, L, pal, cont, root)
                draw_chrome(sh, p, pal, False)
            elif tpl == "backcover":
                draw_backcover(sh, p, pal)
                draw_chrome(sh, p, pal, False)
            else:
                draw_unit_list(sh, p, L, pal, cont)
                draw_chrome(sh, p, pal, False)
        except Exception as e:
            allwarn.append("第%d页(%s)渲染异常: %s" % (i + 1, tpl, e))

        for w in sh.warn:
            allwarn.append("第%d页 %s" % (i + 1, w))
        # 溢出预算：内容游标超过纸张高度即报警
        if tpl in ("unit_list", "article") and sh.y > L["H"] - 12.0:
            allwarn.append("第%d页(%s)内容溢出 %.1fmm"
                           % (i + 1, tpl, sh.y - (L["H"] - 12.0)))

    # 每次 insert_htmlbox 都会注册一份字体；不子集化的话 59 页 = 59 份 CJK 全字库
    # （实测 1.2GB），必须先 subset 再 compact。
    try:
        nfonts = doc.subset_fonts(fallback=False)
    except Exception:
        nfonts = -1
    doc.ez_save(a.out, garbage=4, deflate=True, deflate_images=True)

    size_kb = os.path.getsize(a.out) / 1024.0
    print("PDF  %s  %d 页  %.0f KB" % (a.out, len(expanded), size_kb))
    if allwarn:
        print("  告警 %d：" % len(allwarn))
        for w in allwarn[:25]:
            print("   -", w)
        if len(allwarn) > 25:
            print("   …还有 %d 条" % (len(allwarn) - 25))
    else:
        print("  无告警。")


if __name__ == "__main__":
    main()

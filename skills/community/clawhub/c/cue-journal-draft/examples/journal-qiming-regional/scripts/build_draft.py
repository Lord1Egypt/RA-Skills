#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_draft.py — 把 StyleSpec + 内容清单渲染成 mm 级定位的期刊底稿（HTML / PDF）。

用法：
  python build_draft.py --spec stylespec.json --content content.json --out out/
  python build_draft.py --content content.json --out out/ --stats --no-baseline-gate

三个关键行为（v0.4 起）：

1. **无底图降级**：样刊的页码 / 目录页码 / 编委会 / 分隔页标题原本压在深色满版图上，
   抽出来的色值常是 #FFFFFF。新刊没有底图时这些字会全部隐形。
   现在按「本页有没有底图」切换两套前景色（`--folio-c` 等 CSS 变量），
   并在没有封面图 / 分隔页图时改画纯 CSS 色块版式，不留空白页。

2. **自动分页（--autoflow，默认开）**：unit_list 的条目、article 的 block
   按估算高度装页，装不下自动续页，续页带「（续）」标记。
   给多少内容就出多少页，不用手算一手切。

3. **量级门禁（--stats）**：拿 spec.scale_baseline 对照页数 / 条数 / 字数，
   达成率过低直接打 [FAIL] 并以 exit 1 退出，避免「25 页对 91 页还自我感觉良好」。
   **spec 里没有 scale_baseline 时不再静默放过**，同样按门禁失败处理（exit 1）——
   确有不跑门禁的需求，须显式加 `--no-baseline-gate`。

content.json 结构见 <skill>/references/content-schema.md 的 content 一节。
只依赖标准库。`--pdf` 是**遗留路径**，需要 playwright + chromium（海外下载），
**不要用** —— PDF 一律由 export_pdf.py 自绘，与浏览器策略无关。

命令里的 `python`：Windows 用 `python`，macOS/Linux 用 `python3`。
"""
import argparse
import csv
import html
import json
import math
import os
import re
import sys

DEF_BODY_PT = 10.4

# 行高估算系数。浏览器里 line-height:1.75 就是 1.75 倍字号，所以 HTML 侧这个系数是 1.0；
# 但 MuPDF 的 line-height 乘的是**字体自然行盒**（实测约 1.22em），
# 成品真实行距是 1.75×1.22＝2.15 倍字号，比样刊（实测 1.85 倍）明显松。
# export_pdf.py 导入后会把它改成 LINE_ADJ×LINEBOX，
# 让「分页估算」与「PDF 实际占高」用同一把尺子——两边不一致就会：
# ① 分页器以为装得下、渲染时溢出；② 框给矮了、htmlbox 静默缩字。
# 改这个值前先看 export_pdf.py 里 LINE_ADJ / LINEBOX 的实测注释。
LINE_H_FACTOR = 1.0
DEF_LEADING = 2.15
MM_PT = 0.352778          # 1pt = 0.352778mm
_MULTICOL_WARNED = [False]  # 多栏告警只打一次
FOLIO_TPLS = ("toc", "unit_list", "article", "backcover")


# --------------------------------------------------------------------------
# 颜色与尺寸工具
# --------------------------------------------------------------------------
def hex_rgb(h):
    h = (h or "").strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    try:
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    except Exception:
        return (0, 0, 0)


def luma(h):
    """感知亮度 0–255。#FFFFFF→255。"""
    r, g, b = hex_rgb(h)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def is_unreadable_on_white(h, thr=170.0):
    """在白纸上是否看不见（太浅）。"""
    return luma(h) >= thr


def text_em(s):
    """按全角=1em / 半角≈0.52em 估算一行占多少 em。"""
    s = re.sub(r"<br\s*/?>", "\n", str(s or ""))
    em = 0.0
    for ch in s:
        o = ord(ch)
        if o > 0x2E80:
            em += 1.0
        elif ch in " \t":
            em += 0.28
        elif ch.isdigit():
            em += 0.55
        else:
            em += 0.52
    return em


def lines_of(text, width_mm, body_pt):
    per = max(1.0, width_mm / max(0.1, body_pt * MM_PT))
    n = 0
    for seg in str(text or "").split("\n"):
        n += max(1, int(math.ceil(text_em(seg) / per)))
    return max(1, n)


# --------------------------------------------------------------------------
# 布局归一化
# --------------------------------------------------------------------------
def build_layout(spec):
    canvas = spec.get("canvas", {}) if spec else {}
    w_h = canvas.get("size_mm") or [210, 297]
    W, H = float(w_h[0]), float(w_h[1])

    roles = ((spec or {}).get("palette") or {}).get("roles") or {}
    primary = roles.get("primary") or roles.get("accent") or "#A10F34"
    text = roles.get("text") or "#000000"
    secondary = roles.get("text-secondary") or "#3E3E3E"
    meta = roles.get("meta") or "#7F7F7F"

    # 无底图时使用的「纸上色」：样刊 meta 常是 #FFFFFF（压在深色图上），
    # 白纸上必须换掉，否则页码/目录页码直接隐形。
    meta_paper = primary if is_unreadable_on_white(meta) else meta
    sec_paper = text if is_unreadable_on_white(secondary) else secondary
    pal = {"primary": primary, "text": text, "secondary": secondary, "meta": meta,
           "meta_paper": meta_paper, "sec_paper": sec_paper}

    typo = (spec or {}).get("typography") or {}
    body_pt = float(typo.get("body_size_pt") or DEF_BODY_PT)
    leading = float(typo.get("leading") or DEF_LEADING)
    families = typo.get("families") or ["PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", "sans-serif"]

    grids = dict((spec or {}).get("grids") or {})
    if not grids:
        temps = [t for t in ((spec or {}).get("page_templates") or [])
                 if t.get("grid", {}).get("left_mm") and t.get("grid", {}).get("right_mm")]
        # 零/负宽度网格是抽取噪声（实测某样刊出现 159..107 = -52mm），不能进候选
        temps = [t for t in temps
                 if float(t["grid"]["right_mm"]) - float(t["grid"]["left_mm"]) > 0]
        temps.sort(key=lambda t: -t.get("count", 0))
        narrow = wide = None
        for t in temps:
            g = t["grid"]
            width = g["right_mm"] - g["left_mm"]
            if width < 160 and narrow is None:
                narrow = {"left_mm": g["left_mm"], "right_mm": g["right_mm"]}
            if width >= 160 and wide is None:
                wide = {"left_mm": g["left_mm"], "right_mm": g["right_mm"]}
        if narrow:
            grids["A"] = narrow
        if wide:
            grids["B"] = wide
    if not grids:
        grids = {"A": {"left_mm": 31.7, "right_mm": 175.6},
                 "B": {"left_mm": 19.0, "right_mm": 191.0}}
    cols = int(canvas.get("columns") or 1)
    if cols >= 2 and not _MULTICOL_WARNED[0]:
        _MULTICOL_WARNED[0] = True
        sys.stderr.write(
            "[WARN] 样刊是 %d 栏版面，渲染器只出单栏（版心 %s..%s mm）。"
            "复现双栏需人工排版；若 spec 已给 grids 请核对是否与设计一致。\n"
            % (cols, grids["A"]["left_mm"], grids["A"]["right_mm"]))
    return {"W": W, "H": H, "pal": pal, "body_pt": body_pt, "leading": leading,
            "families": families, "grids": grids,
            "baseline": (spec or {}).get("scale_baseline") or {}}


def grid_of(L, key):
    if isinstance(key, dict):
        return key
    return L["grids"].get(key or "A") or list(L["grids"].values())[0]


def col_width_mm(L, key):
    g = grid_of(L, key)
    return float(g["right_mm"]) - float(g["left_mm"])


def grid_css(L, key, top_mm=None, bottom_mm=None):
    g = grid_of(L, key)
    l = float(g["left_mm"])
    right = float(g["right_mm"])
    s = "margin-left:%.1fmm;width:%.1fmm" % (l, right - l)
    if top_mm is not None:
        s += ";padding-top:%.1fmm" % top_mm
    if bottom_mm is not None:
        s += ";padding-bottom:%.1fmm" % bottom_mm
    return s


def zh_space(s):
    """按中文出版习惯收拾空格。

    内容稿习惯写成「2026 年 4 月 10 日」——读起来清楚，但送进排版引擎是祸：
    这些空格会被当成断词点，两端对齐时每个空格都被拉到极限宽度，
    一行字变成散开的碎块（MuPDF 与浏览器的 text-align:justify 都会这样）。
    这里统一收紧成「2026年4月10日」，英文前后保留空格。
    """
    t = str(s or "")
    han = "[一-鿿　-〿＀-￯]"
    # 空格只要有一侧挨着汉字就删：另一侧可能是数字、百分号或另一个汉字
    t = re.sub(r"(?<=%s|\d|%%) +(?=%s)" % (han, han), "", t)
    t = re.sub(r"(?<=%s) +(?=[\d])" % han, "", t)
    return t


def esc(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def inline(s):
    """极简富文本：**加粗**；<br> 与 \n 都转成 <br>，其余转义。"""
    s = zh_space(str(s or ""))
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    out, buf, i = [], [], 0
    while i < len(s):
        if s.startswith("**", i):
            j = s.find("**", i + 2)
            if j > i:
                out.append(esc("".join(buf)))
                buf = []
                out.append("<strong>" + esc(s[i + 2:j]) + "</strong>")
                i = j + 2
                continue
        buf.append(s[i])
        i += 1
    out.append(esc("".join(buf)))

    return "".join(out).replace("\n", "<br>")


_CAP_DECOR = re.compile(
    r"^\s*(?:[\[【⟨<]\s*(?:图位)?待补(?:图)?\s*[\]】⟩>]\s*[:：]?\s*|图位待补\s*[:：]\s*)"
    r"|\s*[（(]\s*(?:图位)?待补(?:图)?\s*[）)]\s*$"
)


def caption_core(caption):
    """剥掉图注里的「图位待补」占位装饰（前后缀两种写法都出现过）。

    没配过图的图位没人清过这个标记，交付稿里就会「图位待补：X」和下面一行
    「X（图位待补）」重复出现。占位标签自己已经说明状态，图注只留正文。
    """
    s = esc(caption or "")
    prev = None
    while prev != s:          # 前缀 + 后缀可能同时存在，循环剥
        prev = s
        s = _CAP_DECOR.sub("", s).strip()
    return s


def img_src(p):
    if not p:
        return ""
    if str(p).lower().startswith(("http://", "https://", "data:")):
        return str(p)
    _p = _img_abs(p)
    if os.path.isfile(_p):   # 目录不算图源
        return "file:///" + os.path.abspath(_p).replace("\\", "/")
    return str(p)


# --------------------------------------------------------------------------
# 高度估算（自动分页用）
# --------------------------------------------------------------------------
def cta_domain(href):
    """从 URL 取可印在纸面上的域名（去掉 www.）。"""
    if not href:
        return ""
    s = str(href).split("//", 1)[-1].split("/", 1)[0]
    return s[4:] if s.lower().startswith("www.") else s


CTA_DOMAIN = False


def cta_parts(u):
    """CTA 兼容两种写法。

    旧：``"cta": "阅读原文"`` —— 一行字，没有链接，纸刊和电子刊都点不动。
    新：``"cta": {"text": "阅读原文", "href": "https://...", "source": "...", "date": "..."}``。
    ``href`` 在 HTML 里落成 ``<a href>``、在 PDF 里落成 URI 链接热区；
    ``source`` / ``date`` 留给溯源标注与门禁统计。
    """
    c = u.get("cta")
    if isinstance(c, dict):
        return str(c.get("text") or ""), (str(c.get("href") or "").strip())
    return (str(c) if c else ""), ""


def unit_height_mm(L, u, width_mm):
    bp = L["body_pt"]
    lh = bp * MM_PT * L["leading"] * LINE_H_FACTOR
    w = max(20.0, width_mm - 5.0)
    h = lines_of(u.get("title", ""), w, bp) * lh * 1.05 + 2.5
    if u.get("meta"):
        # 日期＋来源那一行：8.5pt × 1.5 行距 ≈ 4.5mm，再算 2mm 段前间距。
        # 漏了这一项，条目多的页会整体下移并溢出页面底部。
        h += 4.5 + 2.0
    for para in str(u.get("body", "")).split("\n\n"):
        if para.strip():
            h += lines_of(para, w, bp) * lh + 2.5
    if u.get("cta"):
        h += lh + 1.0
    if u.get("image"):
        h += 55.0
    return h + 9.0



def img_ratio(path):
    """读图片宽高比。PIL 可用就用 PIL，否则解析 PNG/JPEG 文件头（零依赖）。"""
    try:
        from PIL import Image
        with Image.open(path) as im:
            return im.width / float(im.height or 1)
    except Exception:
        pass
    import struct
    try:
        with open(path, "rb") as f:
            head = f.read(32)
            if head[:8] == b"\x89PNG\r\n\x1a\n":
                w, h = struct.unpack(">II", head[16:24])
                return w / float(h or 1)
            if head[:2] == b"\xff\xd8":
                f.seek(2)
                while True:
                    b = f.read(1)
                    while b and b != b"\xff":
                        b = f.read(1)
                    mk = f.read(1)
                    if not mk:
                        break
                    if 0xC0 <= mk[0] <= 0xCF and mk[0] not in (0xC4, 0xC8, 0xCC):
                        f.read(3)
                        h, w = struct.unpack(">HH", f.read(4))
                        return w / float(h or 1)
                    seg = f.read(2)
                    if len(seg) < 2:
                        break
                    f.seek(struct.unpack(">H", seg)[0] - 2, 1)
    except Exception:
        pass
    return 0.0


# 图源解析根目录：content.json 所在的目录。
# content.json 里的图多是相对路径（art/diagrams/fig_0.png），只在 cwd 恰好是期刊
# 根目录时才找得到。export_pdf / build_draft 会在读 content 后把它填上，
# 分页估算与 HTML 图源就不再依赖 cwd（否则换目录跑：分页器按占位高度算、
# 渲染器按真实高度画，两者打架 → 整本溢出）。
CONTENT_ROOT = ""


def _img_abs(p):
    """相对路径按 CONTENT_ROOT 兜底；已经是绝对路径或http就原样返回。"""
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
    if CONTENT_ROOT and not os.path.isabs(s):
        cand = os.path.join(CONTENT_ROOT, s)
        if os.path.isfile(cand):
            return cand
    return s


def fig_height_mm(b, width_mm, max_h=110.0):
    """figure 块占多高。

    有图时按图片真实比例撑满版心宽（与 export_pdf.img_mm 同一口径）。
    早先这里写死 62mm、export_pdf 把图塞进 52mm 高的框等比缩放，两边口径都不对：
    实测 1.6:1 的横图只摆到 84.6mm 宽，而分页器以为占了 62mm，改准后立刻报溢出。
    无图时沿用旧的占位高度——占位是临时态，不动它以免整本重排。
    """
    path = b.get("path") or b.get("src")
    if not path:
        return 62.0 + (4.0 if b.get("caption") else 0.0)
    import os as _os
    _p = _img_abs(path)
    if not _os.path.isfile(_p):   # isfile：目录也会 exists() 为真
        return 62.0 + (4.0 if b.get("caption") else 0.0)
    ratio = img_ratio(_p)
    if not ratio:
        return 62.0 + (4.0 if b.get("caption") else 0.0)
    h = min(float(width_mm) / ratio, float(max_h))
    return h + 3.0 + (5.0 if b.get("caption") else 0.0)


def block_height_mm(L, b, width_mm):
    bp = L["body_pt"]
    lh = bp * MM_PT * L["leading"] * LINE_H_FACTOR
    t = b.get("type", "p")
    txt = str(b.get("text", ""))
    if t == "figure":
        return fig_height_mm(b, width_mm)
    if t == "h1":
        return lines_of(txt, width_mm, bp) * lh + 9.0
    if t == "h2":
        return lines_of(txt, width_mm, bp) * lh + 7.0
    if t == "li":
        return lines_of(txt, width_mm - 3.5, bp) * lh + 2.0
    if t == "quote":
        return lines_of(txt, width_mm - 4, bp) * lh * 1.1 + 8.0
    if t == "disclaimer":
        return lines_of(txt, width_mm - 8, bp) * lh * 1.7 + 16.0
    if t == "note":
        return lines_of(txt, width_mm, bp) * lh * 0.85 + 4.0
    return lines_of(txt, width_mm, bp) * lh + 2.5


def head_height_mm(L, p, tpl, width_mm):
    """栏目页顶部的 fields 元素要占多少高度。

    kicker / 栏目名 / 导语 / 文章标题 / 署名 / 摘要 都不在 units / blocks 里，
    早期版本把它们漏算，结果整页内容下移、超出部分被 overflow:hidden 静默裁掉。
    """
    f = p.get("fields") or {}
    h = 0.0

    def seg(text, size, leading, gap, w=None):
        return lines_of(text, width_mm if w is None else w, size) * \
            size * MM_PT * leading + gap

    if tpl == "unit_list":
        if f.get("kicker"):
            h += seg(f["kicker"], 8.5, 1.4, 3.0)
        if f.get("section"):
            h += seg(f["section"], 18.0, 1.35, 3.0)
        if f.get("dek"):
            h += seg(f["dek"], 9.0, 1.9, 6.0, width_mm - 8.0)
    elif tpl == "article":
        if f.get("section"):
            h += seg(f["section"], 8.5, 1.4, 3.0)
        if f.get("title"):
            h += seg(f["title"], 16.0, 1.35, 4.0)
        if f.get("byline"):
            h += seg(f["byline"], 9.0, 1.5, 6.0)
        if f.get("abstract"):
            h += seg(f["abstract"], 9.0, 1.9, 12.0, width_mm - 10.0)
        if f.get("hero"):
            h += 61.0
    return h


def paginate(items, height_fn, avail_first_mm, avail_next_mm):
    """按估算高度装页，返回 [(slice, is_continuation), ...]。"""
    pages, cur, h, cap = [], [], 0.0, avail_first_mm
    for it in items:
        ih = height_fn(it)
        if cur and h + ih > cap:
            pages.append((cur, len(pages) > 0))
            cur, h, cap = [it], ih, avail_next_mm
        else:
            cur.append(it)
            h += ih
    if cur or not pages:
        pages.append((cur, len(pages) > 0))
    return pages


# --------------------------------------------------------------------------
# 组件
# --------------------------------------------------------------------------
def chrome(L, page, has_bg):
    """页眉（刊名）+ 页脚（栏目名 + 页码）。"""
    out = []
    running = page.get("running")
    if running is not False:
        txt = (page.get("running_text") or running) if isinstance(running, str) else (page.get("running_text") or "")
        if txt:
            g = grid_of(L, page.get("grid", "A"))
            out.append('<div class="running" style="right:%.1fmm;top:11.0mm">%s</div>'
                       % (L["W"] - float(g["right_mm"]) - 3.0, inline(txt)))
    foot = page.get("foot_text") or (page.get("fields") or {}).get("foot")
    folio = page.get("folio")
    if foot or folio not in (None, False, ""):
        y = float(page.get("folio_y_mm") or L["H"] - 15.0)
        g = grid_of(L, page.get("grid", "A"))
        left = float(g["left_mm"])
        rightmm = L["W"] - float(g["right_mm"]) + 3.0
        out.append('<div class="footbar" style="top:%.1fmm;left:%.1fmm;right:%.1fmm">'
                   % (y, left, rightmm))
        out.append('<span class="foot-text">%s</span>' % inline(foot or ""))
        if folio not in (None, False, ""):
            out.append('<span class="folio">%s</span>' % esc(str(folio)))
        out.append("</div>")
    return "".join(out)


def render_cover(L, p, has_bg):
    f = p.get("fields") or {}
    title = f.get("title") or f.get("name") or ""
    org = f.get("org") or ""
    sub = f.get("subtitle") or f.get("en") or ""
    if has_bg:
        # 有封面图：沿用样刊定位，只补上刊名（图里未必有）
        inner = ""
        if title:
            inner += '<div class="cover-title">%s</div>' % inline(title)
        if sub:
            inner += '<div class="cover-sub">%s</div>' % inline(sub)
        inner += ('<div class="cover-no">%s</div><div class="cover-ym">%s</div>'
                  '<div class="cover-year">%s</div>'
                  % (esc(f.get("issue_no", "")), esc(f.get("yearmonth", "")), esc(f.get("year", ""))))
        if org:
            inner += '<div class="cover-org">%s</div>' % inline(org)
        return '<div class="cover-box" style="left:%.1fmm;bottom:%.1fmm">%s</div>' % (
            float(f.get("x_mm", 36.6)), float(f.get("y_mm", 80.0)), inner)
    # 无封面图：画一版纯 CSS 的封面，避免交出去一页空白
    return ('<div class="cover-fallback">'
            '<div class="cf-top"><div class="cf-org">%s</div></div>'
            '<div class="cf-mid"><div class="cf-title">%s</div>'
            '<div class="cf-sub">%s</div>'
            '<div class="cf-rule"></div>'
            '<div class="cf-meta"><span class="cf-no">%s</span>'
            '<span class="cf-ym">%s</span></div></div>'
            '<div class="cf-year">%s</div></div>'
            % (inline(org), inline(title), inline(sub),
               esc(f.get("issue_no", "")), esc(f.get("yearmonth", "")), esc(f.get("year", ""))))


def render_quote(L, p, has_bg):
    f = p["fields"]
    return ('<div class="quote-box"><div class="quote-mark">“</div>'
            '<div class="quote-text">%s</div><div class="quote-src">%s</div></div>'
            % (inline(f.get("quote", "")), inline(f.get("source", ""))))


def render_masthead(L, p, has_bg):
    f = p["fields"]
    items = "".join('<span class="mh-name">%s</span>' % esc(n) for n in f.get("names", []))
    cls = "mh-box" + ("" if has_bg else " on-paper")
    return ('<div class="%s"><div class="mh-title">%s</div><div class="mh-names">%s</div>'
            '<div class="mh-meta">%s</div></div>'
            % (cls, esc(f.get("title", "编辑部")), items, inline(f.get("note", ""))))


def render_toc(L, p, has_bg):
    f = p["fields"]
    parts = ['<div class="toc-title">%s</div>' % esc(f.get("title", "CONTENTS"))]
    for g in f.get("groups", []):
        parts.append('<div class="toc-group"><span class="toc-no">%s</span>'
                     '<span class="toc-gtitle">%s</span></div>'
                     % (esc(g.get("no", "")), esc(g.get("title", ""))))
        for it in g.get("items", []):
            pg = it.get("page", "")
            if not pg and it.get("ref"):
                pg = (L.get("anchor_map") or {}).get(it["ref"], "")
            parts.append('<div class="toc-item"><span class="toc-ititle">%s</span>'
                         '<span class="toc-lead"></span><span class="toc-ipage">%s</span></div>'
                         % (esc(it.get("title", "")), esc(pg)))
    return '<div class="toc-box">%s</div>' % "".join(parts)


def render_divider(L, p, has_bg):
    f = p.get("fields") or {}
    label = f.get("label") or f.get("section") or ""
    no = f.get("no", "")
    if not label:
        return ""
    if has_bg:
        return '<div class="divider-label">%s</div>' % inline(label)
    # 无图：主色满版 + 白字，保证分隔页不是一页白纸
    return ('<div class="divider-full"><div class="dv-no">%s</div>'
            '<div class="dv-label">%s</div><div class="dv-rule"></div>'
            '<div class="dv-sub">%s</div></div>'
            % (esc(no), inline(label), inline(f.get("subtitle", ""))))


def render_unit_list(L, p, has_bg, cont=False):
    f = p.get("fields") or {}
    grid = p.get("grid", "A")
    w = col_width_mm(L, grid)
    gtop = float(p.get("top_mm", 42.0)) if not cont else float(p.get("cont_top_mm", 22.0))
    out = []
    if not cont:
        if f.get("banner"):
            out.append('<img class="col-img" src="%s">' % img_src(f["banner"]))
        if f.get("kicker"):
            out.append('<div class="kicker">%s</div>' % esc(f["kicker"]))
        out.append('<div class="sec-title">%s</div>' % esc(f.get("section", "")))
        if f.get("dek"):
            out.append('<div class="dek">%s</div>' % inline(f["dek"]))
    else:
        out.append('<div class="cont-mark">%s（续）</div>'
                   % inline(f.get("section", "")))
    for u in p.get("units", []):
        out.append('<div class="unit">')
        out.append('<div class="unit-title">%s</div>' % inline(u.get("title", "")))
        if u.get("meta"):
            out.append('<div class="unit-meta">%s</div>' % esc(u["meta"]))
        for para in str(u.get("body", "")).replace("阅读原文", "").split("\n\n"):
            if para.strip():
                out.append('<p class="unit-body">%s</p>' % inline(para.strip()))
        _ct, _hr = cta_parts(u)
        if _ct and CTA_DOMAIN and _hr:
            _d = cta_domain(_hr)
            if _d:
                _ct = "%s · %s" % (_ct, _d)
        if _ct:
            if _hr:
                out.append('<a class="unit-cta" href="%s" target="_blank" '
                           'rel="noopener">%s</a>' % (esc(_hr), esc(_ct)))
            else:
                out.append('<div class="unit-cta">%s</div>' % esc(_ct))
        if u.get("image"):
            out.append('<img class="unit-img" src="%s">' % img_src(u["image"]))
        out.append("</div>")
    return '<div class="col" style="%s">%s</div>' % (
        grid_css(L, grid, top_mm=gtop), "".join(out))


def render_article(L, p, has_bg, cont=False):
    f = p.get("fields") or {}
    grid = p.get("grid", "B")
    gtop = float(p.get("top_mm", 20.0)) if not cont else float(p.get("cont_top_mm", 22.0))
    out = []
    if not cont:
        if f.get("hero"):
            out.append('<img class="hero" src="%s">' % img_src(f["hero"]))
        if f.get("section"):
            out.append('<div class="art-sec">%s</div>' % inline(f["section"]))
        out.append('<div class="art-title">%s</div>' % inline(f.get("title", "")))
        if f.get("byline"):
            out.append('<div class="art-byline">%s</div>' % inline(f["byline"]))
        if f.get("abstract"):
            out.append('<div class="art-abstract">%s</div>' % inline(f["abstract"]))
    else:
        out.append('<div class="cont-mark">%s（续）</div>' % inline(f.get("title", "")))
    for b in p.get("blocks", []):
        t = b.get("type", "p")
        txt = inline(b.get("text", ""))
        if t == "h1":
            out.append('<div class="art-h1">%s</div>' % txt)
        elif t == "h2":
            out.append('<div class="art-h2">%s</div>' % txt)
        elif t == "li":
            out.append('<div class="art-li">• %s</div>' % txt)
        elif t == "quote":
            out.append('<div class="art-quote">%s</div>' % txt)
        elif t == "note":
            out.append('<div class="art-note">%s</div>' % txt)
        elif t == "figure":
            src = b.get("src") or ""
            if src:
                out.append('<img class="art-fig" src="%s">' % img_src(src))
            else:
                # 占位标签只说明状态；图注由下面的 .art-cap 承载，不在这里重复一遍
                out.append('<div class="fig-slot"><span>图位待补%s</span></div>'
                           % ("" if b.get("caption") else "：" + caption_core(b.get("alt"))))
            if b.get("caption"):
                out.append('<div class="art-cap">%s</div>' % caption_core(b.get("caption")))
        elif t == "disclaimer":
            out.append('<div class="art-disclaimer">%s</div>' % txt)
        else:
            out.append('<p class="art-p">%s</p>' % txt)
    return '<div class="col" style="%s">%s</div>' % (
        grid_css(L, grid, top_mm=gtop), "".join(out))


def render_backcover(L, p, has_bg):
    f = p.get("fields") or {}
    cards = []
    for c in f.get("contacts", []):
        lines = "".join('<div>%s</div>' % inline(x) for x in c.get("lines", []))
        cards.append('<div class="bc-card"><div class="bc-title">%s</div>%s</div>'
                     % (esc(c.get("name", "")), lines))
    head = ('<div class="bc-head">%s</div>' % inline(f.get("title", ""))) if f.get("title") else ""
    return '<div class="bc-grid">%s%s</div>' % (head, "".join(cards))


# --------------------------------------------------------------------------
# 样式
# --------------------------------------------------------------------------
def css(L):
    p = L["pal"]
    fam = ",".join('"%s"' % f for f in L["families"] if " " in f) or '"PingFang SC"'
    return """
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#f2f2f2}
@page{size:%(W).0fmm %(H).0fmm;margin:0}

/* --- 无底图降级：样刊这些元素压在深色图上，白纸上必须换可读色 --- */
.page{--folio-c:%(meta_paper)s;--tocpage-c:%(meta_paper)s;--mh-c:%(text)s;--sub-c:%(sec_paper)s}
.page.hasbg{--folio-c:%(meta)s;--tocpage-c:%(meta)s;--mh-c:#ffffff;--sub-c:#f0f0f0}

.page{position:relative;background:#fff;width:%(W).0fmm;height:%(H).0fmm;overflow:hidden;
      page-break-after:always;break-after:page;font-family:%(fam)s,sans-serif;
      font-size:%(bp).1fpt;line-height:%(ld).2f;color:%(text)s}
.page:last-child{page-break-after:auto}
.page>img.bg{position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover;z-index:0}
.page>.content{position:relative;z-index:2}
.running{position:absolute;font-size:9pt;color:%(pri)s;z-index:3;letter-spacing:1px}
.footbar{position:absolute;display:flex;align-items:baseline;gap:4mm;z-index:3;
         font-size:9pt;color:var(--sub-c);border-top:0.3mm solid #e3e3e3;padding-top:2mm}
.foot-text{flex:1;letter-spacing:1px}
.folio{color:var(--folio-c);font-weight:600;margin-left:auto}

/* cover */
.cover-box{position:absolute;z-index:3;color:%(text)s}
.cover-title{font-size:26pt;font-weight:600;line-height:1.3;margin-bottom:3mm}
.cover-sub{font-size:10pt;color:%(sec_paper)s;margin-bottom:8mm}
.cover-no{font-size:10.4pt;font-weight:600}
.cover-ym{font-size:10.4pt;margin-top:2mm}
.cover-year{font-size:21.5pt;font-weight:600;margin-top:9mm}
.cover-org{font-size:9pt;margin-top:6mm;color:%(sec_paper)s;letter-spacing:2px}
.cover-fallback{position:absolute;inset:0;z-index:3;color:#fff;
  background:linear-gradient(168deg,%(pri)s 0%%,%(pri)s 58%%,#ffffff 58%%,#ffffff 100%%)}
.cf-top{position:absolute;top:20mm;left:20mm;right:20mm}
.cf-org{font-size:10pt;letter-spacing:4px;opacity:.9}
.cf-mid{position:absolute;top:96mm;left:20mm;right:20mm}
.cf-title{font-size:34pt;font-weight:600;line-height:1.25;letter-spacing:2px}
.cf-sub{font-size:10.5pt;margin-top:5mm;opacity:.85;letter-spacing:1px}
.cf-rule{width:26mm;height:0.8mm;background:#fff;margin:9mm 0 7mm;opacity:.9}
.cf-meta{display:flex;gap:6mm;align-items:baseline;font-size:12pt;letter-spacing:2px}
.cf-year{position:absolute;left:20mm;bottom:22mm;font-size:52pt;font-weight:600;
         color:%(pri)s;line-height:1;opacity:.16}

/* quote */
.quote-box{position:absolute;left:19mm;top:78mm;width:150mm;color:%(pri)s}
.quote-mark{font-size:46pt;line-height:0.6;opacity:.35;margin-bottom:4mm}
.quote-text{font-size:14.1pt;font-weight:600;line-height:1.8}
.quote-src{font-size:11pt;margin-top:8mm;text-align:right;padding-right:10mm;color:%(sec_paper)s}

/* masthead */
.mh-box{position:absolute;right:12mm;top:240mm;width:78mm;color:var(--mh-c)}
.mh-box.on-paper{background:#fafafa;border-left:0.8mm solid %(pri)s;padding:6mm 7mm;
                 color:%(text)s;top:200mm}
.mh-title{font-size:9pt;font-weight:600;margin-bottom:3mm}
.mh-names{font-size:7.5pt;line-height:1.9;display:flex;flex-wrap:wrap;gap:0 4mm}
.mh-meta{font-size:7.5pt;margin-top:5mm;color:inherit;opacity:.85}

/* toc */
.toc-box{position:absolute;left:31mm;top:30mm;width:145mm}
.toc-title{font-size:21.5pt;color:#B0B0B0;text-align:right;letter-spacing:3px}
.toc-group{margin-top:13mm;display:flex;align-items:baseline;gap:3mm;
           border-bottom:0.5mm solid %(pri)s;padding-bottom:2mm}
.toc-no{font-size:24pt;color:%(pri)s;font-weight:600;line-height:1}
.toc-gtitle{font-size:12pt;color:%(pri)s;font-weight:600}
.toc-item{display:flex;align-items:baseline;gap:2mm;margin-top:5.5mm;font-size:%(bp).1fpt}
.toc-lead{flex:1;border-bottom:0.3mm dotted #cfcfcf;transform:translateY(-2mm)}
.toc-ipage{color:var(--tocpage-c);font-weight:600}

/* divider */
.divider-label{position:absolute;left:0;right:0;bottom:18mm;text-align:center;
               font-size:12pt;color:#fff;z-index:3;letter-spacing:6px}
.divider-full{position:absolute;inset:0;z-index:3;background:%(pri)s;color:#fff;
  display:flex;flex-direction:column;align-items:center;justify-content:center}
.dv-no{font-size:60pt;font-weight:600;line-height:1;opacity:.28}
.dv-label{font-size:20pt;font-weight:600;letter-spacing:10px;margin-top:6mm;text-indent:10px}
.dv-rule{width:30mm;height:0.6mm;background:#fff;opacity:.7;margin:7mm 0}
.dv-sub{font-size:9.5pt;letter-spacing:2px;opacity:.85}

/* column */
.col{position:relative}
.col-img{width:100%%;object-fit:cover;margin-bottom:6mm}
.kicker{font-size:8.5pt;letter-spacing:3px;color:%(pri)s;font-weight:600;margin-bottom:3mm}
.sec-title{font-size:18pt;font-weight:600;color:%(pri)s;margin-bottom:3mm}
.dek{font-size:9pt;color:var(--sub-c);line-height:1.9;margin-bottom:6mm;
     border-left:0.5mm solid #e3e3e3;padding-left:4mm}
.cont-mark{font-size:9pt;color:%(pri)s;letter-spacing:1px;border-bottom:0.4mm solid %(pri)s;
           padding-bottom:2mm;margin-bottom:6mm}
.unit{position:relative;padding-left:5mm;padding-top:5mm;margin-bottom:6mm;
      border-top:0.3mm solid #ececec;break-inside:avoid}
.unit:first-of-type{border-top:none}
.unit:before{content:"";position:absolute;left:0;top:6.2mm;width:0.7mm;height:7mm;background:%(pri)s}
.unit-title{font-size:%(bp).1fpt;font-weight:600;margin-bottom:2.5mm;line-height:1.5}
.unit-meta{font-size:8.5pt;color:var(--sub-c);margin-bottom:2mm;letter-spacing:.5px}
.unit-body{text-align:justify;margin-bottom:2.5mm}
.unit-cta{text-align:right;font-size:%(bp).1fpt;font-weight:600;color:%(pri)s;margin-top:-1mm}
.unit-img{width:100%%;margin-top:3mm}

/* article */
.hero{width:100%%;object-fit:cover;margin-bottom:8mm}
.art-sec{font-size:8.5pt;letter-spacing:3px;color:%(pri)s;font-weight:600;margin-bottom:3mm}
.art-title{font-size:16pt;font-weight:600;color:%(pri)s;line-height:1.35;margin-bottom:4mm}
.art-byline{font-size:9pt;color:var(--sub-c);text-align:right;margin-bottom:7mm}
.art-abstract{font-size:9pt;color:var(--sub-c);line-height:1.9;margin-bottom:7mm;
  background:#fafafa;padding:4mm 5mm;border-left:0.6mm solid %(pri)s}
.art-h1{font-size:11.5pt;font-weight:600;color:%(pri)s;margin:7mm 0 3mm;
        padding-left:4mm;border-left:0.9mm solid %(pri)s;line-height:1.5}
.art-h2{font-size:%(bp).1fpt;font-weight:600;margin:5mm 0 2mm}
.art-p{text-align:justify;margin-bottom:2.5mm}
.art-li{text-align:justify;margin:0 0 2mm 3.5mm;text-indent:-3.5mm}
.art-quote{margin:4mm 0;padding:3mm 0 3mm 4mm;border-left:0.6mm solid %(pri)s;color:var(--sub-c)}
.art-note{font-size:8.5pt;color:var(--sub-c);margin-top:4mm}
.art-fig{width:100%%;margin:4mm 0 1mm}
.fig-slot{width:100%%;height:52mm;margin:4mm 0 1mm;background:repeating-linear-gradient(
  45deg,#f4f4f4,#f4f4f4 6px,#ebebeb 6px,#ebebeb 12px);
  border:0.3mm dashed #c8c8c8;display:flex;align-items:center;justify-content:center;
  color:#9a9a9a;font-size:8.5pt;letter-spacing:1px}
.art-cap{font-size:8.5pt;color:var(--sub-c);margin-bottom:3mm}
.art-disclaimer{margin-top:8mm;padding:4mm;background:#f5f5f5;font-size:8.5pt;
                color:var(--sub-c);line-height:1.7}

/* backcover */
.bc-head{grid-column:1/-1;font-size:12pt;font-weight:600;color:%(pri)s;
         border-bottom:0.5mm solid %(pri)s;padding-bottom:2mm;margin-bottom:2mm}
.bc-grid{position:absolute;left:18mm;top:16mm;right:18mm;display:grid;
         grid-template-columns:repeat(4,1fr);gap:4mm 6mm;color:var(--sub-c);font-size:7.5pt;
         line-height:1.85}
.bc-title{font-weight:600;color:%(pri)s;margin-bottom:1.5mm;font-size:8pt}
""" % {"W": L["W"], "H": L["H"], "fam": fam, "bp": L["body_pt"], "ld": L["leading"],
       "pri": p["primary"], "text": p["text"], "sec": p["secondary"],
       "sec_paper": p["sec_paper"], "meta": p["meta"], "meta_paper": p["meta_paper"]}


# --------------------------------------------------------------------------
# 主流程
# --------------------------------------------------------------------------
def expand_pages(L, content, autoflow):
    """把逻辑页展开成物理页（自动分页）。返回 [(page_dict, is_cont), ...]。"""
    out = []
    for p in content.get("pages", []):
        tpl = p.get("template", "article")
        if not autoflow or tpl not in ("unit_list", "article"):
            out.append((dict(p), False))
            continue
        grid = p.get("grid", "A" if tpl == "unit_list" else "B")
        w = col_width_mm(L, grid)
        top = float(p.get("top_mm", 42.0 if tpl == "unit_list" else 20.0))
        cont_top = float(p.get("cont_top_mm", 22.0))
        bottom = float(p.get("bottom_mm", 18.0))
        avail_first = L["H"] - top - bottom - head_height_mm(L, p, tpl, w)
        avail_next = L["H"] - cont_top - bottom

        if tpl == "unit_list":
            units = p.get("units") or []
            if not units:
                out.append((dict(p), False))
                continue
            for sl, cont in paginate(units, lambda u: unit_height_mm(L, u, w),
                                     avail_first, avail_next):
                q = dict(p)
                q["units"] = sl
                q["_cont"] = cont
                out.append((q, cont))
        else:
            blocks = p.get("blocks") or []
            if not blocks:
                out.append((dict(p), False))
                continue
            for sl, cont in paginate(blocks, lambda b: block_height_mm(L, b, w),
                                     avail_first, avail_next):
                q = dict(p)
                q["blocks"] = sl
                q["_cont"] = cont
                out.append((q, cont))
    return out


def load_json(path, flag, hint):
    """读入参 JSON：文件缺、坏 JSON、顶层非对象——三种都出一句点名参数的下一步，退 1，零堆栈。

    面承诺的是「对常见操作失误给出可执行的下一步」，而 json.load 直接抛栈时读者拿到的是
    Traceback；这一层把取数错误接住，且发生在建输出目录之前，所以坏输入不会留下半成品。
    """
    if not os.path.exists(path):
        sys.exit("[ERR] %s 指向的文件不存在：%s\n      %s" % (flag, path, hint))
    try:
        with open(path, encoding="utf-8") as f:
            obj = json.load(f)
    except json.JSONDecodeError as e:
        sys.exit("[ERR] %s 不是合法 JSON：%s（第 %s 行第 %s 列）\n      %s"
                 % (flag, e.msg, e.lineno, e.colno, hint))
    except OSError as e:
        sys.exit("[ERR] %s 读不进来：%s\n      %s" % (flag, e, hint))
    if not isinstance(obj, dict):
        sys.exit("[ERR] %s 是 JSON %s，本件只收对象（顶层要是一个 {}）\n      %s"
                 % (flag, type(obj).__name__, hint))
    return obj


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", default=None)
    ap.add_argument("--content", required=True)
    ap.add_argument("--out", default="out")
    ap.add_argument("--pdf", action="store_true")
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--no-baseline-gate", action="store_true",
                    help="--stats 时跳过量级门禁（仅在你明确不做达成率对照时使用）")
    ap.add_argument("--no-autoflow", action="store_true", help="关闭自动分页（自行保证每页装得下）")
    ap.add_argument("--cta-domain", action="store_true",
                    help="CTA 行带上来源域名（例：阅读原文 · info.gov.hk），纸刊也能溯源")
    args = ap.parse_args()
    global CTA_DOMAIN
    CTA_DOMAIN = bool(args.cta_domain)

    spec = {}
    if args.spec:
        spec = load_json(args.spec, "--spec",
                         "样式抽取产出的文件名是 stylespec.json，请检查路径；"
                         "确实要用内置默认网格（不做版式对照）就整个省掉 --spec。")
    content = load_json(args.content, "--content",
                        "内容件由转写／整理步骤产出（每份一个对象）；先回看那一步的回显再重跑。")

    L = build_layout(spec)
    os.makedirs(args.out, exist_ok=True)
    issue = content.get("issue") or {}
    autoflow = not args.no_autoflow

    expanded = expand_pages(L, content, autoflow)

    # 逻辑页数（自动分页之前的真实篇数/栏数），用于量级门禁
    logical = {"pages": len(content.get("pages", [])), "articles": 0, "unit_list": 0}
    for p in content.get("pages", []):
        t = p.get("template")
        if t == "article":
            logical["articles"] += 1
        elif t == "unit_list":
            logical["unit_list"] += 1

    # ---- 页码：显式 folio 优先，否则 auto_folio 时按顺序编号 ----
    auto_folio = bool(issue.get("auto_folio"))
    n = 0
    anchor_map = {}
    for q, cont in expanded:
        tpl = q.get("template", "article")
        if q.get("folio") in (None, "", False) and auto_folio and tpl in FOLIO_TPLS:
            n += 1
            q["folio"] = "%02d" % n
        a = q.get("anchor")
        if a and not cont and q.get("folio"):
            anchor_map.setdefault(a, str(q["folio"]))
    L["anchor_map"] = anchor_map

    pages_html = []
    manifest = []
    stats = {"pages": 0, "units": 0, "unit_chars": [], "figures": 0, "empty_figs": 0,
             "unknown": [], "chars": 0, "tpl": {}, "overflow": [],
             "cta": 0, "cta_href": 0, "no_href": []}

    for i, (p, cont) in enumerate(expanded):
        tpl = p.get("template", "article")
        fn = {"cover": render_cover, "quote": render_quote, "masthead": render_masthead,
              "toc": render_toc, "divider": render_divider, "unit_list": render_unit_list,
              "article": render_article, "backcover": render_backcover}.get(tpl)
        if fn is None:
            stats["unknown"].append({"index": i, "template": tpl})
            fn = render_article
            p = dict(p)
            p["blocks"] = p.get("blocks") or [{"type": "p", "text": ""}]

        bg = p.get("images", {}).get("bg") or p.get("bg")
        has_bg = bool(bg)
        has_chrome = tpl not in ("cover", "divider", "masthead")

        if has_chrome and issue.get("running_text") and not p.get("running_text"):
            p["running_text"] = issue["running_text"]
        if has_chrome and not p.get("foot_text") and issue.get("foot_text"):
            p["foot_text"] = issue["foot_text"]

        try:
            inner = fn(L, p, has_bg, cont) if tpl in ("unit_list", "article") else fn(L, p, has_bg)
        except TypeError:
            inner = fn(L, p)

        # 溢出检测：粗估内容高度 vs 可用高度
        if tpl in ("unit_list", "article"):
            grid = p.get("grid", "A" if tpl == "unit_list" else "B")
            w = col_width_mm(L, grid)
            top = float(p.get("top_mm", 42.0 if tpl == "unit_list" else 20.0)) if not cont \
                else float(p.get("cont_top_mm", 22.0))
            avail = L["H"] - top - float(p.get("bottom_mm", 18.0))
            h = 0.0
            for u in p.get("units", []):
                h += unit_height_mm(L, u, w)
            for b in p.get("blocks", []):
                h += block_height_mm(L, b, w)
            if h > avail + 1.0:
                stats["overflow"].append({"page": i + 1, "tpl": tpl,
                                          "est_mm": round(h, 1), "avail_mm": round(avail, 1)})

        bgtag = ('<img class="bg" src="%s">' % img_src(bg)) if bg else ""
        pages_html.append(
            '<section class="page%s" data-tpl="%s" data-no="%s">%s<div class="content">%s%s</div></section>'
            % (" hasbg" if has_bg else "", esc(tpl), esc(p.get("folio", "")),
               bgtag, chrome(L, p, has_bg) if has_chrome else "", inner))

        stats["pages"] += 1
        stats["tpl"][tpl] = stats["tpl"].get(tpl, 0) + 1
        for u in p.get("units", []):
            stats["units"] += 1
            c = len(u.get("title", "")) + len(u.get("body", ""))
            stats["unit_chars"].append(c)
            stats["chars"] += c
            _ct, _hr = cta_parts(u)
            if _ct:
                stats["cta"] += 1
                if _hr:
                    stats["cta_href"] += 1
                else:
                    stats["no_href"].append((p.get("folio") or str(i + 1),
                                             u.get("title", "")[:24]))
        for b in p.get("blocks", []):
            bt = b.get("type")
            if bt == "figure":
                stats["figures"] += 1
                if not b.get("src"):
                    stats["empty_figs"] += 1
            stats["chars"] += len(str(b.get("text", "")))
        f = p.get("fields") or {}
        if f.get("hero"):
            stats["figures"] += 1
        if f.get("banner"):
            stats["figures"] += 1
        manifest.append({"i": i + 1, "template": tpl, "folio": p.get("folio", ""),
                         "title": f.get("title") or f.get("section") or f.get("label") or ""})

    title = issue.get("title") or "Draft"
    doc = ("<!DOCTYPE html><html lang=\"zh-CN\"><head><meta charset=\"utf-8\">"
           "<title>%s</title><style>%s</style></head><body>%s</body></html>"
           % (esc(title), css(L), "\n".join(pages_html)))

    hp = os.path.join(args.out, "draft.html")
    with open(hp, "w", encoding="utf-8") as f:
        f.write(doc)
    mp = os.path.join(args.out, "manifest.csv")
    with open(mp, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["i", "template", "folio", "title"])
        w.writeheader()
        for row in manifest:
            w.writerow(row)

    print("OK pages=%d units=%d figures=%d(empty %d) chars=%d unknown=%d" % (
        stats["pages"], stats["units"], stats["figures"], stats["empty_figs"],
        stats["chars"], len(stats["unknown"])))
    if stats["cta"]:
        _pct = 100.0 * stats["cta_href"] / stats["cta"]
        print("溯源: CTA %d 条，带原文链接 %d 条（%.0f%%）"
              % (stats["cta"], stats["cta_href"], _pct))
        for _pg, _tt in stats["no_href"][:10]:
            print("   - 缺原文链接 P%s：%s" % (_pg, _tt))
        if len(stats["no_href"]) > 10:
            print("   - ……另有 %d 条" % (len(stats["no_href"]) - 10))
    print("html: %s" % os.path.abspath(hp))
    for u in stats["unknown"]:
        print("  [!] 未知模板 %s @ page %d → 已降级按 article 渲染" % (u["template"], u["index"] + 1))
    for o in stats["overflow"]:
        print("  [!] 第 %d 页(%s) 估算高 %.1fmm > 可用 %.1fmm，可能溢出被裁"
              % (o["page"], o["tpl"], o["est_mm"], o["avail_mm"]))
    if stats["empty_figs"]:
        print("  [!] %d 个图位没有图源（已渲染为占位斜纹块）" % stats["empty_figs"])

    if args.stats:
        uc = sorted(stats["unit_chars"])
        rep = {"pages": stats["pages"], "units": stats["units"], "chars": stats["chars"],
               "figures": stats["figures"], "empty_figs": stats["empty_figs"],
               "tpl": stats["tpl"],
               "unit_chars": {"n": len(uc), "min": uc[0] if uc else 0,
                              "p50": uc[len(uc) // 2] if uc else 0, "max": uc[-1] if uc else 0}}
        base = L.get("baseline") or {}
        if not base and not args.no_baseline_gate:
            print("  [FAIL] 量级门禁未生效：这个 spec 里没有 scale_baseline，"
                  "无法判断本期是不是只有样刊三成厚。")
            print("         ① 正解：换成带 scale_baseline 的 --spec"
                  "（extract_style.py 抽取时一定会写入它）；")
            print("         ② 本次只要计数、明确不做量级门禁：加 --no-baseline-gate。")
            sys.exit(1)
        if args.no_baseline_gate:
            print("  [INFO] 已按 --no-baseline-gate 跳过量级门禁，本次不做达成率对照。")
        if base and not args.no_baseline_gate:
            got = {"pages": stats["pages"], "units": stats["units"],
                   "articles": logical["articles"], "chars": stats["chars"]}
            rep["baseline"] = {}
            for k, want in base.items():
                if not isinstance(want, (int, float)):
                    continue
                v = got.get(k)
                if v is None:
                    continue
                r = round(v / float(want), 3) if want else 0
                rep["baseline"][k] = {"target": want, "actual": v, "ratio": r}
            low = [k for k, v in rep["baseline"].items() if v["ratio"] < 0.6]
            if low:
                rep["FAIL"] = low
        print(json.dumps(rep, ensure_ascii=False))
        if rep.get("FAIL"):
            print("  [FAIL] 量级严重不足：%s（达成率 <60%%）"
                  "—— 这是门禁判定结果，不是脚本崩溃。" % "、".join(rep["FAIL"]))
            sys.exit(1)

    if args.pdf:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            sys.exit("[ERR] --pdf 需要 playwright：pip install playwright && playwright install chromium")
        pdfp = os.path.join(args.out, "draft.pdf")
        with sync_playwright() as pw:
            br = pw.chromium.launch()
            pg = br.new_page()
            pg.goto("file:///" + os.path.abspath(hp).replace("\\", "/"))
            pg.emulate_media(media="print")
            pg.pdf(path=pdfp, width="%dmm" % int(L["W"]), height="%dmm" % int(L["H"]),
                   print_background=True, margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
            br.close()
        print("pdf : %s" % os.path.abspath(pdfp))


if __name__ == "__main__":
    main()

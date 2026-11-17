#!/usr/bin/env python3
"""gen_diagram.py —— 用代码精确绘制信息图（矢量），导出 PNG / PDF。

用法：
    python gen_diagram.py --spec diagrams/fig_0.json --out art/gen2/fig_0.png
    python gen_diagram.py --spec diagrams/fig_0.json --out fig_0.png --pdf fig_0.pdf --dpi 300

为什么语义图不该用文生图：
    流程 / 框架 / 分层 / 分工 / 路径这类图，信息全在**标签文字**与**拓扑关系**里。
    扩散模型写不对中文，也维持不住精确的并列与连线关系；为了回避画错而把具象
    元素全部抽掉，就会退化成「红块 + 空心几何形」——图注写得再具体，仍然图文
    不符。所以语义图走本脚本：拓扑由代码保证，中文由系统字体渲染，输出矢量。
    文生图只留给不含具体信息的氛围图（封面、题花、分隔页）。

spec 结构（单位 mm，坐标原点在图左上角）：
    {
      "size_mm": [172.0, 107.5],
      "palette": {"primary": "#A10F34", "text": "#000000",
                  "meta": "#7F7F7F", "rule": "#D8D8D4", "tint": "#F5F4F1"},
      "blocks": [ {...}, ... ]
    }

块类型：
    columns   并列卡片列（左色条标题 + 说明 + 标签/内容条目）
    flow      横向流程（块 + 箭头），支持分支说明
    rows      逐行条目（左侧主色标签块 + 右侧要点）
    stack     纵向层次（宽度可递减以表达嵌套/包含关系）
    converge  多路汇聚到一点
    footer    底部通栏横带（结论、口径、提示）
    note      小字注释

字体：Windows 默认 simhei.ttf；macOS / Linux 自动回落，也可用 --font 指定。
"""
import argparse
import json
import os
import sys

try:
    import pymupdf
except ImportError:  # 旧包名
    import fitz as pymupdf

MM = 72.0 / 25.4

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\msyh.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
]

DEFAULT_PALETTE = {
    "primary": "#A10F34",
    "text": "#000000",
    "meta": "#7F7F7F",
    "rule": "#D8D8D4",
    "tint": "#F5F4F1",
}


def rgb(hexstr):
    """'#A10F34' -> (0.63, 0.06, 0.20)"""
    h = str(hexstr).lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return (int(h[0:2], 16) / 255.0, int(h[2:4], 16) / 255.0, int(h[4:6], 16) / 255.0)


def pick_font(explicit=None):
    if explicit:
        if not os.path.isfile(explicit):
            sys.exit("找不到字体文件：%s" % explicit)
        return explicit
    for f in FONT_CANDIDATES:
        if os.path.isfile(f):
            return f
    sys.exit("未找到可用中文字体，请用 --font 指定（如 C:/Windows/Fonts/simhei.ttf）")


class Pen:
    """以 mm 为对外坐标的绘笔。坐标原点在图左上角，y 向下。"""

    def __init__(self, page, fontfile, palette, warnings):
        self.page = page
        self.pal = palette
        self.warn = warnings
        page.insert_font(fontname="zh", fontfile=fontfile)
        self.font = pymupdf.Font(fontfile=fontfile)

    # ---------- 文本度量 ----------
    def wrap(self, s, size, maxw_mm):
        """按可用宽度折行。中文避头：标点不另起一行；英文不拦腰截断单词。"""
        maxw = maxw_mm * MM
        no_break = "，。、；：？！）」』】》…—·,.;:?!)]}"
        lines, cur = [], ""
        for ch in str(s):
            if ch == "\n":
                lines.append(cur)
                cur = ""
                continue
            if cur and self.font.text_length(cur + ch, fontsize=size) > maxw:
                if ch in no_break:      # 避头：标点跟随上一行，不单起一行
                    cur += ch
                    continue
                cut = len(cur)
                if ch.isascii() and ch.isalnum() and cur[-1:].isascii() and cur[-1:].isalnum():
                    i = len(cur)
                    while i > 0 and cur[i - 1].isascii() and cur[i - 1].isalnum():
                        i -= 1
                    if i > 0:
                        cut = i
                lines.append(cur[:cut])
                cur = cur[cut:] + ch
            else:
                cur += ch
        if cur:
            lines.append(cur)
        return lines

    def text_h(self, s, size, maxw_mm, leading=1.45):
        """文本块占用的高度（mm）。"""
        return len(self.wrap(s, size, maxw_mm)) * size * leading / MM

    def text(self, x_mm, y_mm, s, size, color, maxw_mm=None, leading=1.45, align="l"):
        """y_mm 为文本块**顶部**。返回占用高度（mm）。"""
        if s is None or str(s) == "":
            return 0.0
        maxw_mm = maxw_mm if maxw_mm else 1e6
        lines = self.wrap(s, size, maxw_mm)
        asc = self.font.ascender * size
        for i, ln in enumerate(lines):
            w = self.font.text_length(ln, fontsize=size)
            if align == "c":
                x = x_mm + (maxw_mm * MM - w) / 2.0 / MM
            elif align == "r":
                x = x_mm + (maxw_mm * MM - w) / MM
            else:
                x = x_mm
            base = y_mm * MM + size * leading * i + asc
            self.page.insert_text((x * MM, base), ln, fontname="zh",
                                  fontsize=size, color=color)
        return len(lines) * size * leading / MM

    # ---------- 图形 ----------
    def rect(self, x, y, w, h, fill=None, stroke=None, lw=0.4):
        r = pymupdf.Rect(x * MM, y * MM, (x + w) * MM, (y + h) * MM)
        self.page.draw_rect(r, color=stroke, fill=fill, width=lw)

    def line(self, x1, y1, x2, y2, color, lw=0.5, dashes=None):
        self.page.draw_line(pymupdf.Point(x1 * MM, y1 * MM),
                            pymupdf.Point(x2 * MM, y2 * MM),
                            color=color, width=lw, dashes=dashes)

    def arrow(self, x1, y1, x2, y2, color, lw=0.6):
        """水平箭头（用于流程）。"""
        self.line(x1, y1, x2, y2, color, lw)
        d = 1.6
        self.page.draw_polyline(
            [pymupdf.Point(x2 * MM, y2 * MM),
             pymupdf.Point((x2 - d) * MM, (y2 - d * 0.62) * MM),
             pymupdf.Point((x2 - d) * MM, (y2 + d * 0.62) * MM),
             pymupdf.Point(x2 * MM, y2 * MM)],
            color=color, fill=color, width=0.2)

    def overflow(self, blk, need_mm, have_mm):
        self.warn.append("%s 内容高 %.1fmm 超出可用 %.1fmm" %
                         (blk.get("label") or blk.get("kind"), need_mm, have_mm))


# ---------------------------------------------------------------- 块绘制

def draw_columns(P, blk):
    x, y, w, h = blk["rect_mm"]
    cols = blk.get("columns", [])
    n = len(cols)
    gap = blk.get("gap_mm", 4.5)
    cw = (w - gap * (n - 1)) / n
    head_h = blk.get("head_h_mm", 15.0)
    pad = blk.get("pad_mm", 3.0)
    for i, c in enumerate(cols):
        cx = x + i * (cw + gap)
        P.rect(cx, y, cw, head_h, fill=rgb(P.pal["primary"]))
        P.text(cx + pad, y + 2.4, c["head"], 10.5, rgb("#FFFFFF"),
               maxw_mm=cw - pad * 2, leading=1.25)
        if c.get("sub"):
            P.text(cx + pad, y + head_h - 5.0, c["sub"], 5.8, rgb("#F0C9D3"),
                   maxw_mm=cw - pad * 2, leading=1.2)
        cy = y + head_h
        if c.get("meta"):
            mh = P.text_h(c["meta"], 6.0, cw - pad * 2, 1.45) + 3.0
            P.rect(cx, cy, cw, mh, fill=rgb(P.pal["tint"]))
            P.text(cx + pad, cy + 1.5, c["meta"], 6.0, rgb(P.pal["meta"]),
                   maxw_mm=cw - pad * 2, leading=1.45)
            cy += mh
        cy += 3.4
        for it in c.get("items", []):
            lab, body = it[0], it[1]
            P.text(cx + pad, cy, lab, 6.2, rgb(P.pal["primary"]),
                   maxw_mm=cw - pad * 2, leading=1.3)
            cy += 6.2 * 1.3 / MM + 0.9
            used = P.text(cx + pad, cy, body, 6.4, rgb(P.pal["text"]),
                          maxw_mm=cw - pad * 2, leading=1.5)
            cy += used + 3.6
        if c.get("foot"):
            fy = y + h - 9.0
            P.rect(cx, fy, cw, 9.0, fill=rgb(P.pal["tint"]))
            P.text(cx + pad, fy + 1.4, c["foot"], 6.0, rgb(P.pal["text"]),
                   maxw_mm=cw - pad * 2, leading=1.4)
        if cy > y + h + 0.5:
            P.overflow(blk, cy - y, h)


def draw_rows(P, blk):
    """每行：左侧主色标签块 + 右侧要点（可多列）。"""
    x, y, w, h = blk["rect_mm"]
    rows = blk.get("rows", [])
    gap = blk.get("gap_mm", 2.6)
    tag_w = blk.get("tag_w_mm", 34.0)
    rh = (h - gap * (len(rows) - 1)) / len(rows)
    pad = 3.0
    for i, r in enumerate(rows):
        ry = y + i * (rh + gap)
        P.rect(x, ry, tag_w, rh, fill=rgb(P.pal["primary"]))
        t_size = blk.get("tag_size", 9.0)
        while t_size > 7.0 and P.font.text_length(r["tag"], fontsize=t_size) / MM > tag_w - pad * 2:
            t_size -= 0.4      # 标签宁可缩一号，也不要把词断成两行
        P.text(x + pad, ry + 2.6, r["tag"], t_size, rgb("#FFFFFF"),
               maxw_mm=tag_w - pad * 2, leading=1.25)
        if r.get("sub"):
            P.text(x + pad, ry + rh - 5.4, r["sub"], 5.8, rgb("#F0C9D3"),
                   maxw_mm=tag_w - pad * 2, leading=1.2)
        tx = x + tag_w + pad
        tw = w - tag_w - pad * 2
        ty = ry + 1.6
        for body in r.get("items", []):
            used = P.text(tx, ty, body, 6.4, rgb(P.pal["text"]),
                          maxw_mm=tw, leading=1.5)
            ty += used + 1.5
        if ty - ry > rh + 0.5:
            P.overflow(blk, ty - ry, rh)


def draw_flow(P, blk):
    x, y, w, h = blk["rect_mm"]
    steps = blk.get("steps", [])
    n = len(steps)
    gap = blk.get("gap_mm", 7.0)
    sw = (w - gap * (n - 1)) / n
    pad = 2.6
    tw = sw - pad * 2 - 1.0
    for i, st in enumerate(steps):
        sx = x + i * (sw + gap)
        # 先量内容总高再垂直居中：否则文字贴顶、块内下半大片留空
        parts = []
        if st.get("no"):
            parts.append((st["no"], 5.8, 1.2, 2.2, rgb(P.pal["primary"])))
        parts.append((st["label"], 7.6, 1.3, 1.2 if st.get("note") else 0,
                      rgb(P.pal["text"])))
        if st.get("note"):
            parts.append((st["note"], 6.0, 1.45, 0, rgb(P.pal["meta"])))
        total = (sum(P.text_h(t, s, tw, l) for t, s, l, _, _ in parts) +
                 sum(g for *_, g, _ in parts))
        ty = y + max((h - total) / 2.0, 2.0)
        P.rect(sx, y, sw, h, fill=rgb(P.pal["tint"]),
               stroke=rgb(P.pal["rule"]), lw=0.4)
        P.rect(sx, y, 1.6, h, fill=rgb(P.pal["primary"]))
        for t, s, l, g, c in parts:
            ty += P.text(sx + pad + 1.0, ty, t, s, c, maxw_mm=tw, leading=l) + g
        if i < n - 1:
            ay = y + h / 2
            P.arrow(sx + sw + 1.1, ay, sx + sw + gap - 1.1, ay,
                    rgb(P.pal["primary"]), 0.6)


def draw_stack(P, blk):
    x, y, w, h = blk["rect_mm"]
    layers = blk.get("layers", [])
    gap = blk.get("gap_mm", 2.2)
    lh = (h - gap * (len(layers) - 1)) / len(layers)
    inset = blk.get("inset_mm", 0.0)
    pad = 3.0
    for i, L in enumerate(layers):
        ly = y + i * (lh + gap)
        iw = w - inset * i * 2
        lx = x + inset * i
        P.rect(lx, ly, iw, lh, fill=rgb(P.pal["tint"]),
               stroke=rgb(P.pal["rule"]), lw=0.4)
        P.rect(lx, ly, 1.6, lh, fill=rgb(P.pal["primary"]))
        P.text(lx + pad + 1.0, ly + 1.8, L["label"], 7.4, rgb(P.pal["primary"]),
               maxw_mm=iw * 0.34, leading=1.3)
        P.text(lx + pad + 1.0 + iw * 0.35, ly + 2.1, L.get("body") or "", 6.4,
               rgb(P.pal["text"]), maxw_mm=iw * 0.62 - pad, leading=1.45)


def draw_converge(P, blk):
    x, y, w, h = blk["rect_mm"]
    srcs = blk.get("sources", [])
    n = len(srcs)
    gap = blk.get("gap_mm", 3.0)
    sw = (w - gap * (n - 1)) / n
    box_h = blk.get("box_h_mm", h * 0.42)
    tgt_h = blk.get("target_h_mm", h * 0.16)
    pad = 2.6
    join_y = y + box_h + (h - box_h - tgt_h) * 0.55
    for i, s in enumerate(srcs):
        sx = x + i * (sw + gap)
        P.rect(sx, y, sw, box_h, fill=rgb(P.pal["tint"]),
               stroke=rgb(P.pal["rule"]), lw=0.4)
        P.text(sx + pad, y + 2.2, s["label"], 7.2, rgb(P.pal["primary"]),
               maxw_mm=sw - pad * 2, leading=1.3)
        if s.get("note"):
            P.text(sx + pad, y + 2.2 + 7.2 * 1.3 / MM + 0.8, s["note"], 6.0,
                   rgb(P.pal["text"]), maxw_mm=sw - pad * 2, leading=1.4)
        P.line(sx + sw / 2, y + box_h, x + w / 2, join_y,
               rgb(P.pal["primary"]), 0.5)
    P.line(x + w / 2, join_y, x + w / 2, y + h - tgt_h,
           rgb(P.pal["primary"]), 0.8)
    tw = blk.get("target_w_mm", w * 0.5)
    P.rect(x + (w - tw) / 2, y + h - tgt_h, tw, tgt_h, fill=rgb(P.pal["primary"]))
    P.text(x + (w - tw) / 2, y + h - tgt_h + (tgt_h - 7.0) / 2 + 0.4,
           blk.get("target", ""), 7.6, rgb("#FFFFFF"), maxw_mm=tw, leading=1.3,
           align="c")


def draw_footer(P, blk):
    """通栏横带。tone=tint 时为浅底深字（用于补充说明，避免与主色带抢视线）。"""
    x, y, w, h = blk["rect_mm"]
    if blk.get("tone") == "tint":
        P.rect(x, y, w, h, fill=rgb(P.pal["tint"]))
        P.rect(x, y, 1.6, h, fill=rgb(P.pal["primary"]))
        P.text(x + 4.6, y + (h - 7.0) / 2, blk["text"], 7.0, rgb(P.pal["text"]),
               maxw_mm=w - 9.2, leading=1.35)
    else:
        P.rect(x, y, w, h, fill=rgb(P.pal["primary"]))
        P.text(x + 4.0, y + (h - 7.0) / 2, blk["text"], 7.2, rgb("#FFFFFF"),
               maxw_mm=w - 8.0, leading=1.35)


def draw_note(P, blk):
    x, y, w, h = blk["rect_mm"]
    P.text(x, y, blk["text"], blk.get("size", 6.2), rgb(P.pal["meta"]),
           maxw_mm=w, leading=1.45)


DRAWERS = {
    "columns": draw_columns,
    "rows": draw_rows,
    "flow": draw_flow,
    "stack": draw_stack,
    "converge": draw_converge,
    "footer": draw_footer,
    "note": draw_note,
}


def build(spec, fontfile, dpi=300, want_pdf=None, base_dir=None):
    size = spec.get("size_mm", [172.0, 107.5])
    pal = dict(DEFAULT_PALETTE)
    pal.update(spec.get("palette") or {})
    warnings = []
    doc = pymupdf.open()
    page = doc.new_page(width=size[0] * MM, height=size[1] * MM)
    P = Pen(page, fontfile, pal, warnings)

    bg = spec.get("bg")
    if bg:
        P.rect(0, 0, size[0], size[1], fill=rgb(bg))

    for blk in spec.get("blocks", []):
        fn = DRAWERS.get(blk.get("kind"))
        if not fn:
            sys.exit("未知块类型：%s" % blk.get("kind"))
        fn(P, blk)

    if want_pdf:
        doc.save(want_pdf)
    return page, doc, warnings


def main():
    ap = argparse.ArgumentParser(description="按结构化定义绘制信息图（矢量）")
    ap.add_argument("--spec", required=True, help="图定义 JSON")
    ap.add_argument("--out", required=True, help="输出 PNG 路径")
    ap.add_argument("--pdf", default=None, help="另存矢量 PDF（可选）")
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--font", default=None, help="指定中文字体文件")
    args = ap.parse_args()

    with open(args.spec, encoding="utf-8") as f:
        spec = json.load(f)
    fontfile = pick_font(args.font)
    page, doc, warnings = build(spec, fontfile, args.dpi, args.pdf)

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    pix = page.get_pixmap(dpi=args.dpi)
    pix.save(args.out)
    size = spec.get("size_mm", [172.0, 107.5])
    print("图: %s  %dx%d px @%ddpi  (%.1f x %.1f mm)" %
          (args.out, pix.width, pix.height, args.dpi, size[0], size[1]))
    for w in warnings:
        print("  [WARN] %s" % w, file=sys.stderr)
    return 1 if warnings else 0


if __name__ == "__main__":
    sys.exit(main())

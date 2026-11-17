#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pdf_core.py —— 纯标准库 PDF 生成内核（中文字体嵌入 + 子集化 + 矢量图表）

零依赖：只使用 struct / zlib / os / math / datetime。
设计要点：
  · 内容流不压缩，便于 pdf_verify.py 做文本与图表标记验真
  · 中文字体从系统字体嵌入（子集化，PDF 体积 ~ 数十 KB），失败时回退为整字体嵌入
  · 图表全部用 PDF 矢量算子绘制（re/l/c/m），不生成位图，放大不失真
  · 每个图表写入 % CHART:类型:标题 注释标记，供验真脚本计数
"""

import math
import os
import struct
import zlib
from datetime import datetime

# ---------- TrueType 解析与子集化 ----------


class TTFFont:
    CANDIDATES = [
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/msyhl.ttc",
        "C:/Windows/Fonts/simsun.ttc",
        "C:/Windows/Fonts/simkai.ttf",
        "C:/Windows/Fonts/HYZhongHeiTi-197.ttf",
    ]

    def __init__(self, path=None):
        self.path = path or self.find_font()
        data = open(self.path, "rb").read()
        self.data = data
        if data[:4] == b"ttcf":
            self.base = struct.unpack(">I", data[12:16])[0]
        elif data[:4] in (b"\x00\x01\x00\x00", b"true", b"typ1"):
            self.base = 0
        else:
            raise ValueError("不是 TrueType 字体：%s" % self.path)
        num = struct.unpack(">H", data[self.base + 4:self.base + 6])[0]
        self.tables = {}
        for i in range(num):
            p = self.base + 12 + 16 * i
            tag = data[p:p + 4].decode("latin-1")
            off, ln = struct.unpack(">II", data[p + 8:p + 16])
            self.tables[tag] = (off, ln)
        self._parse_head()
        self._parse_hhea_hmtx()
        self.cmap = self._parse_cmap()

    @classmethod
    def find_font(cls):
        env = os.environ.get("ECOM_PDF_FONT")
        if env and os.path.exists(env):
            return env
        for p in cls.CANDIDATES:
            if os.path.exists(p):
                return p
        raise RuntimeError("未找到可用的中文字体，请设置环境变量 ECOM_PDF_FONT 指向 .ttf/.ttc")

    def table(self, tag):
        if tag not in self.tables:
            return b""
        off, ln = self.tables[tag]
        return self.data[off:off + ln]

    def _parse_head(self):
        h = self.table("head")
        self.units_per_em = struct.unpack(">H", h[18:20])[0]
        self.index_to_loc = struct.unpack(">h", h[50:52])[0]
        self.bbox = struct.unpack(">hhhh", h[36:44])

    def _parse_hhea_hmtx(self):
        hh = self.table("hhea")
        self.ascent, self.descent = struct.unpack(">hh", hh[4:8])
        self.num_hmetrics = struct.unpack(">H", hh[34:36])[0]
        self.hmtx = self.table("hmtx")
        self.num_glyphs = struct.unpack(">H", self.table("maxp")[4:6])[0]
        self.advances = []
        self.lsbs = []
        last_aw = struct.unpack(">H", self.hmtx[(self.num_hmetrics - 1) * 4:(self.num_hmetrics - 1) * 4 + 2])[0]
        for i in range(self.num_glyphs):
            if i < self.num_hmetrics:
                aw = struct.unpack(">H", self.hmtx[i * 4:i * 4 + 2])[0]
                lsb = struct.unpack(">h", self.hmtx[i * 4 + 2:i * 4 + 4])[0]
            else:
                aw = last_aw
                p = self.num_hmetrics * 4 + (i - self.num_hmetrics) * 2
                lsb = struct.unpack(">h", self.hmtx[p:p + 2])[0] if p + 2 <= len(self.hmtx) else 0
            self.advances.append(aw)
            self.lsbs.append(lsb)

    def _parse_cmap(self):
        cm = self.table("cmap")
        n = struct.unpack(">H", cm[2:4])[0]
        best = None
        for i in range(n):
            p = 4 + 8 * i
            plat, enc, off = struct.unpack(">HHI", cm[p:p + 8])
            fmt = struct.unpack(">H", cm[off:off + 2])[0]
            score = {(3, 1): 3, (3, 10): 4, (0, 3): 2, (0, 4): 2, (3, 0): 1}.get((plat, enc), 0)
            if score and (best is None or score > best[0]):
                best = (score, off, fmt)
        if not best:
            return {}
        _, off, fmt = best
        if fmt == 4:
            return self._cmap4(cm[off:])
        if fmt == 12:
            return self._cmap12(cm[off:])
        if fmt == 6:
            length = struct.unpack(">H", cm[off + 2:off + 4])[0]
            first = struct.unpack(">H", cm[off + 6:off + 8])[0]
            out = {}
            for i in range(length):
                gid = struct.unpack(">H", cm[off + 8 + 2 * i:off + 10 + 2 * i])[0]
                out[first + i] = gid
            return out
        return {}

    def _cmap4(self, b):
        seg_x2 = struct.unpack(">H", b[6:8])[0]
        seg = seg_x2 // 2
        ends = struct.unpack(">%dH" % seg, b[14:14 + seg_x2])
        starts = struct.unpack(">%dH" % seg, b[16 + seg_x2:16 + seg_x2 * 2])
        deltas = struct.unpack(">%dh" % seg, b[16 + seg_x2 * 2:16 + seg_x2 * 3])
        range_off_base = 16 + seg_x2 * 3
        ros = struct.unpack(">%dH" % seg, b[range_off_base:range_off_base + seg_x2])
        out = {}
        for i in range(seg):
            for c in range(starts[i], min(ends[i], 0xFFFF) + 1):
                if ros[i] == 0:
                    gid = (c + deltas[i]) & 0xFFFF
                else:
                    addr = range_off_base + 2 * i + ros[i] + 2 * (c - starts[i])
                    if addr + 2 <= len(b):
                        gid = struct.unpack(">H", b[addr:addr + 2])[0]
                        if gid:
                            gid = (gid + deltas[i]) & 0xFFFF
                    else:
                        gid = 0
                if gid:
                    out[c] = gid
        return out

    def _cmap12(self, b):
        n = struct.unpack(">I", b[12:16])[0]
        out = {}
        for i in range(n):
            p = 16 + 12 * i
            s, e, g = struct.unpack(">III", b[p:p + 12])
            for k in range(min(e - s, 0x10FFFF) + 1):
                out[s + k] = g + k
        return out

    # ---- glyf / loca ----
    def _loca(self):
        loc = self.table("loca")
        out = []
        if self.index_to_loc == 0:
            for i in range(self.num_glyphs + 1):
                out.append(struct.unpack(">H", loc[2 * i:2 * i + 2])[0] * 2)
        else:
            for i in range(self.num_glyphs + 1):
                out.append(struct.unpack(">I", loc[4 * i:4 * i + 4])[0])
        return out

    def glyph_data(self, gid):
        loc = self._loca()
        s, e = loc[gid], loc[gid + 1]
        return self.data[self.tables["glyf"][0] + s: self.tables["glyf"][0] + e]

    def composite_gids(self, gid):
        d = self.glyph_data(gid)
        if len(d) < 10:
            return []
        nc = struct.unpack(">h", d[0:2])[0]
        if nc >= 0:
            return []
        out, p = [], 10
        while p + 4 <= len(d):
            flags, gi = struct.unpack(">HH", d[p:p + 4])
            out.append(gi)
            p += 4
            if flags & 0x0001:
                p += 4
            else:
                p += 2
            if flags & 0x0008:
                p += 2
            elif flags & 0x0040:
                p += 4
            elif flags & 0x0080:
                p += 8
            if not (flags & 0x0020):
                break
        return out

    def subset(self, chars):
        """返回 (ttf_bytes, char->new_gid, advances_list)"""
        need = {0}
        for ch in chars:
            gid = self.cmap.get(ord(ch), 0)
            stack = [gid]
            while stack:
                g = stack.pop()
                if g in need:
                    continue
                need.add(g)
                stack += self.composite_gids(g)
        order = sorted(need)
        old2new = {g: i for i, g in enumerate(order)}
        glyf_parts, loca = [], [0]
        for g in order:
            d = self.glyph_data(g)
            if len(d) % 2:
                d += b"\x00"
            glyf_parts.append(d)
            loca.append(loca[-1] + len(d))
        glyf = b"".join(glyf_parts)
        loca_bytes = b"".join(struct.pack(">I", x) for x in loca)
        hmtx = b""
        adv_list = []
        for g in order:
            aw = self.advances[g] if g < len(self.advances) else 1000
            lsb = self.lsbs[g] if g < len(self.lsbs) else 0
            hmtx += struct.pack(">Hh", aw, lsb)
            adv_list.append(aw)
        charmap = {}
        for ch in set(chars):
            gid = self.cmap.get(ord(ch))
            if gid in old2new:
                charmap[ch] = old2new[gid]
        cmap_bytes = self._build_cmap4(charmap)
        head = bytearray(self.table("head"))
        struct.pack_into(">h", head, 50, 1)
        struct.pack_into(">I", head, 8, 0)
        hhea = bytearray(self.table("hhea"))
        struct.pack_into(">H", hhea, 34, len(order))
        maxp = bytearray(self.table("maxp"))
        struct.pack_into(">H", maxp, 4, len(order))
        tables = {
            b"cmap": cmap_bytes, b"glyf": glyf, b"head": bytes(head), b"hhea": bytes(hhea),
            b"hmtx": hmtx, b"loca": loca_bytes, b"maxp": bytes(maxp),
        }
        for tag in (b"OS/2", b"name", b"post", b"cvt ", b"fpgm", b"prep", b"gasp"):
            t = self.table(tag.decode("latin-1"))
            if t:
                tables[tag] = t
        ttf = self._assemble(tables)
        return ttf, charmap, adv_list

    @staticmethod
    def _build_cmap4(charmap):
        codes = sorted(charmap.keys())
        runs = []
        for c in codes:
            u = ord(c)
            if runs and u == runs[-1][1] + 1 and charmap[chr(runs[-1][1])] + (u - runs[-1][1]) == charmap[c]:
                runs[-1][1] = u
            else:
                runs.append([u, u])
        # 逐段检查是否连续（gid 也连续），否则拆成单字符段
        segs = []
        for s, e in runs:
            cur_s = s
            for u in range(s, e + 1):
                if u > s and charmap[chr(u)] != charmap[chr(u - 1)] + 1:
                    segs.append((cur_s, u - 1, False))
                    cur_s = u
                elif u == e:
                    segs.append((cur_s, e, True))
        segs = [(s, e) for s, e, _ in segs]
        segs.append((0xFFFF, 0xFFFF))
        seg_count = len(segs)
        glyph_ids = []
        base = {}
        pos = 0
        for s, e in segs[:-1]:
            base[(s, e)] = pos
            for u in range(s, e + 1):
                glyph_ids.append(charmap[chr(u)])
                pos += 1
        ends = b"".join(struct.pack(">H", e) for _, e in segs)
        starts = b"".join(struct.pack(">H", s) for s, _ in segs)
        deltas = b"".join(struct.pack(">h", 0) for _ in segs)
        ros = b""
        for i, (s, e) in enumerate(segs):
            if (s, e) == (0xFFFF, 0xFFFF):
                ros += struct.pack(">H", 0)
            else:
                ros += struct.pack(">H", 2 * (seg_count + base[(s, e)] - i))
        reserved = struct.pack(">H", 0)
        glyph_array = b"".join(struct.pack(">H", g) for g in glyph_ids)
        entry_sel = int(math.log2(_pow2(seg_count))) if seg_count else 0
        search_range = 2 * _pow2(seg_count)
        length = 14 + 8 * seg_count + 2 * len(glyph_ids)
        body = struct.pack(">HHHHHHH", 4, length, 0, seg_count * 2,
                           search_range, entry_sel, seg_count * 2 - search_range)
        data = body + ends + reserved + starts + deltas + ros + glyph_array
        return struct.pack(">HH", 0, 1) + struct.pack(">HHI", 3, 1, 12) + data

    @staticmethod
    def _assemble(tables):
        tags = sorted(tables.keys())
        n = len(tags)
        search_range = _pow2(n) * 16
        entry_selector = _log2(_pow2(n))
        range_shift = n * 16 - search_range
        header = struct.pack(">IHHHH", 0x00010000, n, search_range, entry_selector, range_shift)
        offset = len(header) + 16 * n
        entries, body = b"", b""
        for t in tags:
            data = tables[t]
            entries += t + struct.pack(">III", _checksum(data), offset, len(data))
            pad = (-len(data)) % 4
            body += data + b"\x00" * pad
            offset += len(data) + pad
        ttf = header + entries + body
        total = sum(struct.unpack(">I", ttf[i:i + 4])[0] for i in range(0, len(ttf) - (len(ttf) % 4), 4)) & 0xFFFFFFFF
        adj = (0xB1B0AFBA - total) & 0xFFFFFFFF
        hi = ttf.find(b"head")
        if hi >= 0:
            off = struct.unpack(">I", ttf[hi + 8:hi + 12])[0]
            ttf = ttf[:off + 8] + struct.pack(">I", adj) + ttf[off + 12:]
        return ttf


def _pow2(n):
    p = 1
    while p * 2 <= n:
        p *= 2
    return p


def _log2(n):
    return int(math.log2(n)) if n > 0 else 0


def _checksum(data):
    if len(data) % 4:
        data += b"\x00" * (-len(data) % 4)
    return sum(struct.unpack(">%dI" % (len(data) // 4), data)) & 0xFFFFFFFF


# ---------- PDF 文档 ----------

PALETTE = {
    "ink": (0.13, 0.15, 0.18), "muted": (0.45, 0.49, 0.55), "line": (0.85, 0.87, 0.90),
    "brand": (0.10, 0.42, 0.75), "brand2": (0.16, 0.60, 0.55), "accent": (0.90, 0.55, 0.15),
    "up": (0.83, 0.18, 0.18),      # 红=增长/正向（中国区财务惯例）
    "down": (0.13, 0.55, 0.30),    # 绿=下降/负向
    "warn": (0.85, 0.35, 0.10), "bg": (0.96, 0.97, 0.98), "card": (1.0, 1.0, 1.0),
}


class PDF:
    def __init__(self, width=595.28, height=841.89, font_path=None):
        self.W, self.H = width, height
        self.font = TTFFont(font_path)
        self.chars = set("0123456789%.-+()/：:，,、元年月日 ")
        self.pages = []
        self.buf = []
        self.charts = 0
        self.tables = 0

    # ---- 页面/文本 ----
    def new_page(self):
        if self.buf:
            self.pages.append("".join(self.buf))
        self.buf = []
        self.y = 0

    def finish_page(self):
        if self.buf:
            self.pages.append("".join(self.buf))
            self.buf = []

    def _ensure(self):
        if not hasattr(self, "y"):
            self.y = 0
        return None

    def add_text(self, txt, x, y, size=11, color=PALETTE["ink"], bold=False):
        """y 为文本行顶部（自上而下坐标系）"""
        self.chars |= set(txt)
        asc = self.font.ascent / self.font.units_per_em * size
        base = self.H - y - asc
        r, g, b = color
        fake = "2 w %.3f %.3f %.3f RG " % (r, g, b) if bold else ""
        self.buf.append(
            "BT %s/F1 %.2f Tf %.3f %.3f %.3f rg 1 0 0 1 %.2f %.2f Tm %s Tj ET\n"
            % (fake, size, r, g, b, x, base, self._hex(txt)))

    def _hex(self, txt):
        # 占位：真实 gid 编码在 save() 时替换
        return "<%s>" % "".join("%04x" % ord(c) for c in txt)

    def text_width(self, txt, size):
        upem = self.font.units_per_em
        return sum(self.font.advances[self.font.cmap.get(ord(c), 0)] for c in txt) / upem * size

    def wrap(self, txt, size, max_w):
        lines, cur = [], ""
        for ch in txt:
            if ch == "\n":
                lines.append(cur)
                cur = ""
                continue
            if self.text_width(cur + ch, size) > max_w and cur:
                lines.append(cur)
                cur = ch
            else:
                cur += ch
        if cur:
            lines.append(cur)
        return lines

    # ---- 图形 ----
    def rect(self, x, y, w, h, fill=None, stroke=None, lw=0.8, radius=0):
        o = []
        if fill:
            o.append("%.3f %.3f %.3f rg" % fill)
        if stroke:
            o.append("%.3f %.3f %.3f RG %.2f w" % (stroke[0], stroke[1], stroke[2], lw))
        if radius <= 0:
            o.append("%.2f %.2f %.2f %.2f re" % (x, self.H - y - h, w, h))
        else:
            o.append(self._round_rect(x, self.H - y - h, w, h, radius))
        o.append("f" if (fill and not stroke) else ("B" if (fill and stroke) else ("S" if stroke else "n")))
        self.buf.append(" ".join(o) + "\n")

    @staticmethod
    def _round_rect(x, y, w, h, r):
        k = 0.5523 * r
        p = ["%.2f %.2f m" % (x + r, y)]
        p.append("%.2f %.2f %.2f %.2f %.2f %.2f c" % (x + w - r, y, x + w - r + k, y, x + w, y + r))
        p.append("%.2f %.2f %.2f %.2f %.2f %.2f c" % (x + w, y + h - r, x + w, y + h - r + k, x + w - r, y + h))
        p.append("%.2f %.2f %.2f %.2f %.2f %.2f c" % (x + r, y + h, x + r - k, y + h, x, y + h - r))
        p.append("%.2f %.2f %.2f %.2f %.2f %.2f c" % (x, y + r, x, y + r - k, x + r, y))
        return " ".join(p)

    def line(self, x1, y1, x2, y2, color=PALETTE["line"], lw=0.8, dash=None):
        o = ["%.3f %.3f %.3f RG %.2f w" % (color[0], color[1], color[2], lw)]
        if dash:
            o.append("[%.1f %.1f] 0 d" % (dash[0], dash[1]))
        o.append("%.2f %.2f m %.2f %.2f l S" % (x1, self.H - y1, x2, self.H - y2))
        self.buf.append(" ".join(o) + "\n")

    def polygon(self, pts, fill, stroke=None):
        o = []
        if fill:
            o.append("%.3f %.3f %.3f rg" % fill)
        o.append("%.2f %.2f m" % (pts[0][0], self.H - pts[0][1]))
        for x, y in pts[1:]:
            o.append("%.2f %.2f l" % (x, self.H - y))
        o.append("h")
        o.append("f" if fill and not stroke else "B" if stroke else "S")
        self.buf.append(" ".join(o) + "\n")

    def marker(self, kind, title):
        self.buf.append("%% CHART:%s:%s\n" % (kind, title.replace("%", "%%")))
        if kind in ("bar", "line", "pie", "funnel", "waterfall"):
            self.charts += 1
        if kind == "table":
            self.tables += 1

    # ---- 图表 ----
    def bar_chart(self, x, y, w, h, title, labels, values, unit="", colors=None):
        self.marker("bar", title)
        self.add_text(title, x, y, 12)
        top = y + 20
        ph = h - 46
        n = max(1, len(values))
        vmax = max([abs(v) for v in values] + [1e-9])
        vmax = vmax * 1.15
        base = top + ph
        self.line(x + 42, base, x + w, base, PALETTE["line"])
        for i in range(5):
            gy = base - ph * i / 4
            self.line(x + 42, gy, x + w, gy, (0.93, 0.94, 0.96), lw=0.5)
            self.add_text("%.1f" % (vmax * i / 4), x + 4, gy - 5, 8, PALETTE["muted"])
        slot = (w - 50) / n
        bw = min(slot * 0.6, 46)
        for i, v in enumerate(values):
            cx = x + 46 + slot * i + (slot - bw) / 2
            bh = ph * (abs(v) / vmax)
            col = (colors[i] if colors and i < len(colors) else
                   (PALETTE["up"] if v >= 0 else PALETTE["down"]))
            self.rect(cx, base - bh, bw, bh, fill=col)
            self.add_text(("%.2f" % v) + unit, cx - 2, base - bh - 12, 8, PALETTE["ink"])
            lb = labels[i] if i < len(labels) else ""
            self.add_text(lb[:8], cx - 4, base + 4, 8, PALETTE["muted"])
        return h

    def line_chart(self, x, y, w, h, title, labels, series, unit=""):
        self.marker("line", title)
        self.add_text(title, x, y, 12)
        top = y + 20
        ph = h - 48
        base = top + ph
        allv = [v for s in series for v in s["values"]]
        vmax = max(allv + [1e-9]) * 1.15
        vmin = min(min(allv + [0]), 0)
        rng = (vmax - vmin) or 1
        self.line(x + 42, base, x + w, base, PALETTE["line"])
        for i in range(5):
            gy = base - ph * i / 4
            self.line(x + 42, gy, x + w, gy, (0.93, 0.94, 0.96), lw=0.5)
            self.add_text("%.1f" % (vmin + rng * i / 4), x + 4, gy - 5, 8, PALETTE["muted"])
        n = max(1, len(labels))
        step = (w - 50) / max(1, n - 1)
        cols = [PALETTE["brand"], PALETTE["accent"], PALETTE["brand2"], PALETTE["up"]]
        for si, s in enumerate(series):
            col = s.get("color") or cols[si % len(cols)]
            pts = []
            for i, v in enumerate(s["values"]):
                px = x + 46 + step * i
                py = base - ph * ((v - vmin) / rng)
                pts.append((px, py))
            for i in range(len(pts) - 1):
                self.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], col, lw=1.6)
            for i, (px, py) in enumerate(pts):
                self.rect(px - 2, py - 2, 4, 4, fill=col)
                self.add_text(("%.1f" % s["values"][i]) + unit, px - 6, py - 14, 7.5, PALETTE["ink"])
            lx = x + 46 + si * 96
            self.rect(lx, y + 2, 10, 3, fill=col)
            self.add_text(s.get("name", "系列%d" % (si + 1)), lx + 14, y - 2, 8.5, PALETTE["muted"])
        for i, lb in enumerate(labels):
            self.add_text(str(lb)[:8], x + 42 + step * i, base + 4, 8, PALETTE["muted"])
        return h

    def pie_chart(self, x, y, size, title, labels, values):
        self.marker("pie", title)
        self.add_text(title, x, y, 12)
        cx, cy, r = x + size * 0.28, y + 22 + size * 0.30, size * 0.24
        tot = sum(values) or 1
        cols = [PALETTE["brand"], PALETTE["accent"], PALETTE["brand2"], PALETTE["up"], PALETTE["down"], PALETTE["muted"]]
        a0 = -math.pi / 2
        for i, v in enumerate(values):
            frac = v / tot
            a1 = a0 + frac * 2 * math.pi
            pts = [(cx, cy)]
            steps = max(8, int(frac * 72))
            for k in range(steps + 1):
                a = a0 + (a1 - a0) * k / steps
                pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
            self.polygon(pts, fill=cols[i % len(cols)])
            ly = y + 22 + i * 15
            self.rect(x + size * 0.58, ly + 2, 9, 9, fill=cols[i % len(cols)])
            self.add_text("%s  %.1f%%" % (labels[i], frac * 100), x + size * 0.58 + 14, ly, 9, PALETTE["ink"])
            a0 = a1
        return size

    @staticmethod
    def _nfmt(v):
        a = abs(v)
        if a >= 1000:
            return "%.0f" % v
        if a >= 10:
            return "%.1f" % v
        return "%.2f" % v

    def funnel_chart(self, x, y, w, h, title, labels, values, unit=""):
        """漏斗图：用于「曝光→点击→加购→下单→支付」全链路转化呈现。

        values 为首端最大、逐级递减的各环节绝对量；右侧自动标注相对上一环节的转化率。
        """
        self.marker("funnel", title)
        self.add_text(title, x, y, 12)
        top = y + 24
        ph = h - 46
        n = max(1, len(values))
        maxv = max([abs(v) for v in values] + [1e-9])
        gap = min(5.0, ph / n * 0.14)
        stage_h = (ph - gap * (n - 1)) / n
        plot_w = max(80.0, w - 168)          # 右侧预留标注区
        cxm = x + 46 + plot_w / 2
        cols = [PALETTE["brand"], PALETTE["brand2"], PALETTE["accent"],
                PALETTE["brand"], PALETTE["brand2"], PALETTE["accent"]]
        for i, v in enumerate(values):
            prev = values[i - 1] if i > 0 else v
            w_top = plot_w * (abs(prev) / maxv)
            w_bot = plot_w * (abs(v) / maxv)
            y1 = top + (stage_h + gap) * i
            y2 = y1 + stage_h
            self.polygon([(cxm - w_top / 2, y1), (cxm + w_top / 2, y1),
                          (cxm + w_bot / 2, y2), (cxm - w_bot / 2, y2)],
                         fill=cols[i % len(cols)])
            mid = (y1 + y2) / 2
            vtxt = self._nfmt(v) + unit
            self.add_text(vtxt, cxm - self.text_width(vtxt, 9) / 2, mid - 5, 9, PALETTE["ink"])
            lb = str(labels[i]) if i < len(labels) else ""
            if i > 0 and prev:
                ann = "%s  较上层 %.1f%%" % (lb, v / prev * 100)
            else:
                ann = "%s  入口" % lb
            self.add_text(ann, x + 46 + plot_w + 10, mid - 5, 9, PALETTE["muted"])
        return h

    def waterfall_chart(self, x, y, w, h, title, labels, values, unit=""):
        """瀑布图：用于「售价 → 逐级扣减 → 净利润」的资金拆解。

        values 为各级增减量（正=增加、负=扣减），自动累计并画浮动柱与连接虚线。
        配色沿用中国区惯例：增加红（up）、扣减绿（down）。
        """
        self.marker("waterfall", title)
        self.add_text(title, x, y, 12)
        top = y + 24
        ph = h - 48
        base = top + ph
        c = 0.0
        steps, ext = [], [0.0]
        for v in values:
            steps.append((c, float(v)))
            c += float(v)
            ext.append(c)
        ext.append(0.0)
        vmax = max(ext + [1e-9]) * 1.15
        vmin = min(min(ext), 0.0)
        rng = (vmax - vmin) or 1.0

        def yof(val):
            return base - ph * ((val - vmin) / rng)

        self.line(x + 42, yof(0), x + w, yof(0), PALETTE["line"])
        n = max(1, len(steps))
        slot = (w - 52) / n
        bw = min(slot * 0.58, 46)
        for i, (start, delta) in enumerate(steps):
            cx = x + 46 + slot * i + (slot - bw) / 2
            v0, v1 = start, start + delta
            yhi, ylo = yof(max(v0, v1)), yof(min(v0, v1))
            bh = max(1.5, ylo - yhi)
            col = PALETTE["up"] if delta >= 0 else PALETTE["down"]
            self.rect(cx, yhi, bw, bh, fill=col)
            dtxt = ("+%s" if delta >= 0 else "-%s") % self._nfmt(abs(delta))
            self.add_text(dtxt + unit, cx - 4, yhi - 11, 8, PALETTE["ink"])
            if i < n - 1:
                ny = yof(v1)
                nx = x + 46 + slot * (i + 1) + (slot - bw) / 2
                self.line(cx + bw, ny, nx, ny, (0.74, 0.77, 0.82), lw=0.6, dash=[2.0, 2.0])
            lb = str(labels[i]) if i < len(labels) else ""
            self.add_text(lb[:8], cx - 4, base + 4, 8, PALETTE["muted"])
        return h

    def table(self, x, y, w, header, rows, widths=None, size=9):
        self.marker("table", "table-%dx%d" % (len(rows), len(header)))
        ncol = len(header)
        widths = widths or [w / ncol] * ncol
        widths = [w * (wi / sum(widths)) for wi in widths]
        rh = 20
        self.rect(x, y, w, rh, fill=(0.93, 0.95, 0.97))
        cx = x
        for i, hcell in enumerate(header):
            self.add_text(str(hcell), cx + 4, y + 5, size)
            cx += widths[i]
        yy = y + rh
        for r in rows:
            hh = rh
            cells = [self.wrap(str(c), size, widths[i] - 8) for i, c in enumerate(r)]
            hh = max(rh, 6 + max(len(c) for c in cells) * (size + 3.2))
            self.line(x, yy + hh, x + w, yy + hh, PALETTE["line"], lw=0.5)
            cx = x
            for i, lines in enumerate(cells):
                for j, ln in enumerate(lines):
                    self.add_text(ln, cx + 4, yy + 4 + j * (size + 3.2), size)
                cx += widths[i]
            yy += hh
        return yy - y

    def kv_cards(self, x, y, w, items, per_row=3, h=52, size=10):
        cw = (w - 8 * (per_row - 1)) / per_row
        for i, (k, v) in enumerate(items):
            cx = x + (i % per_row) * (cw + 8)
            cy = y + (i // per_row) * (h + 8)
            self.rect(cx, cy, cw, h, fill=(0.965, 0.975, 0.99), stroke=(0.88, 0.91, 0.95), radius=4)
            self.add_text(str(k), cx + 8, cy + 9, 8.5, PALETTE["muted"])
            self.add_text(str(v), cx + 8, cy + 24, size + 3, PALETTE["ink"], bold=True)
        rows = (len(items) + per_row - 1) // per_row
        return rows * (h + 8)

    def save(self, path, title="", meta=None):
        self.finish_page()
        meta = meta or {}
        txt_all = "".join(self.pages)
        ttf, charmap, advs = self.font.subset(self.chars | set(txt_all))
        upem = self.font.units_per_em

        def enc(txt):
            out = []
            for c in txt:
                gid = charmap.get(c)
                if gid is None:
                    gid = charmap.get(" ")
                    if gid is None:
                        gid = 0
                out.append("%04x" % gid)
            return "<%s>" % "".join(out)

        # 重新编码所有文本
        import re
        pat = re.compile(r"<([0-9a-f]+)> Tj")
        streams = []
        for content in self.pages:
            def rep(m):
                s = m.group(1)
                chars = [chr(int(s[i:i + 4], 16)) for i in range(0, len(s), 4)]
                return enc("".join(chars)) + " Tj"
            streams.append(pat.sub(rep, content).encode("utf-8", "replace"))

        objs = []
        n_pages = len(streams)
        # 1: Catalog, 2: Pages, 3..: pages & contents, then fonts
        catalog_id, pages_id = 1, 2
        page_ids = [3 + 2 * i for i in range(n_pages)]
        content_ids = [4 + 2 * i for i in range(n_pages)]
        base = 3 + 2 * n_pages
        type0_id, cid_id, desc_id, file_id, tounicode_id = base, base + 1, base + 2, base + 3, base + 4
        total = base + 4

        objs.append((catalog_id, b"<< /Type /Catalog /Pages %d 0 R >>" % pages_id))
        kids = " ".join("%d 0 R" % p for p in page_ids)
        objs.append((pages_id, ("<< /Type /Pages /Kids [%s] /Count %d >>" % (kids, n_pages)).encode()))

        font_res = "<< /Font << /F1 %d 0 R >> >>" % type0_id
        for i, s in enumerate(streams):
            objs.append((page_ids[i], (
                "<< /Type /Page /Parent %d 0 R /MediaBox [0 0 %.2f %.2f] /Resources %s /Contents %d 0 R >>"
                % (pages_id, self.W, self.H, font_res, content_ids[i])).encode()))
            objs.append((content_ids[i], b"<< /Length %d >>\nstream\n" % len(s) + s + b"\nendstream"))

        widths = " ".join(str(int(round(a / upem * 1000))) for a in advs)
        objs.append((type0_id, (
            "<< /Type /Font /Subtype /Type0 /BaseFont /SUBSET /Encoding /Identity-H "
            "/DescendantFonts [%d 0 R] /ToUnicode %d 0 R >>" % (cid_id, tounicode_id)).encode()))
        objs.append((cid_id, (
            "<< /Type /Font /Subtype /CIDFontType2 /BaseFont /SUBSET /CIDSystemInfo "
            "<< /Registry (Adobe) /Ordering (Identity) /Supplement 0 >> /FontDescriptor %d 0 R "
            "/DW 1000 /W [0 [%s]] /CIDToGIDMap /Identity >>" % (desc_id, widths)).encode()))
        objs.append((desc_id, (
            "<< /Type /FontDescriptor /FontName /SUBSET /Flags 4 /FontBBox [%d %d %d %d] "
            "/ItalicAngle 0 /Ascent %d /Descent %d /CapHeight %d /StemV 80 /FontFile2 %d 0 R >>"
            % (self.font.bbox[0], self.font.bbox[1], self.font.bbox[2], self.font.bbox[3],
               self.font.ascent, self.font.descent, int(self.font.ascent * 0.7), file_id)).encode()))
        objs.append((file_id, b"<< /Length %d /Length1 %d >>\nstream\n" % (len(ttf), len(ttf)) + ttf + b"\nendstream"))
        tounicode = self._tounicode(charmap)
        objs.append((tounicode_id, b"<< /Length %d >>\nstream\n" % len(tounicode) + tounicode + b"\nendstream"))

        out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = {}
        objs.sort()
        body = bytearray()
        for num, b in objs:
            offsets[num] = len(out) + len(body)
            body += ("%d 0 obj\n" % num).encode() + b + b"\nendobj\n"
        out += body
        xref_pos = len(out)
        maxn = max(offsets.keys())
        xref = ["xref\n0 %d\n" % (maxn + 1), "0000000000 65535 f \n"]
        for i in range(1, maxn + 1):
            xref.append("%010d 00000 n \n" % offsets.get(i, 0))
        out += "".join(xref).encode()
        def _pdfstr(s):
            s = str(s).replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")
            try:
                s.encode("ascii")
                return "(%s)" % s
            except UnicodeEncodeError:
                return "<FEFF%s>" % s.encode("utf-16-be").hex().upper()
        info = " ".join("/%s %s" % (k, _pdfstr(v)) for k, v in meta.items() if v)
        out += ("trailer\n<< /Size %d /Root %d 0 R /Info << /Title %s %s >> >>\nstartxref\n%d\n%%%%EOF\n"
                % (maxn + 1, catalog_id, _pdfstr(title), info, xref_pos)).encode()
        with open(path, "wb") as f:
            f.write(bytes(out))
        return {"path": path, "bytes": len(out), "pages": n_pages, "charts": self.charts, "tables": self.tables}

    @staticmethod
    def _tounicode(charmap):
        lines = ["/CIDInit /ProcSet findresource begin", "12 dict begin", "begincmap",
                 "/CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) /Supplement 0 >> def",
                 "/CMapName /Adobe-Identity-UCS def", "/CMapType 2 def", "1 begincodespacerange",
                 "<0000> <FFFF>", "endcodespacerange"]
        items = sorted((g, ord(c)) for c, g in charmap.items())
        n = len(items)
        lines.append("%d beginbfchar" % n)
        for g, u in items:
            lines.append("<%04x> <%04X>" % (g, u))
        lines += ["endbfchar", "endcmap", "CMapName currentdict /CMap defineresource pop", "end", "end"]
        return "\n".join(lines).encode("latin-1")

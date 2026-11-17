#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_style.py — 从一份「过往期刊样例」PDF 抽取 StyleSpec 草稿。

产出：
  <out>/stylespec.json   机器可读，供 build_draft.py 直接消费
  <out>/stylespec.md     人读版，供 agent / 用户复核与补全

用法：
  python extract_style.py <sample.pdf> [--out DIR] [--max-pages N] [--lang zh]

只依赖 PyMuPDF: python -m pip install pymupdf
"""
import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict

PT2MM = 25.4 / 72.0


def mm(v):
    return round(v * PT2MM, 1)


# --------------------------------------------------------------------------
# 采集
# --------------------------------------------------------------------------
def collect(doc):
    """把每一页的 span 与图片槽位采出来。"""
    pages = []
    for pno, page in enumerate(doc):
        rec = {
            "page": pno + 1,
            "w_pt": page.rect.width,
            "h_pt": page.rect.height,
            "spans": [],
            "lines": [],
            "images": [],
        }
        try:
            d = page.get_text("dict")
        except Exception:
            d = {"blocks": []}
        for b in d.get("blocks", []):
            if b.get("type") == 1:  # image block
                x0, y0, x1, y1 = b["bbox"]
                rec["images"].append({
                    "x0": mm(x0), "y0": mm(y0), "x1": mm(x1), "y1": mm(y1),
                    "w": mm(x1 - x0), "h": mm(y1 - y0),
                    "xref": None,
                })
                continue
            if b.get("type") != 0:
                continue
            for l in b.get("lines", []):
                txt = "".join(s.get("text", "") for s in l.get("spans", [])).strip()
                if not txt:
                    continue
                x0, y0, x1, y1 = l["bbox"]
                sl = l.get("spans", [])
                if not sl:
                    continue
                s = max(sl, key=lambda z: z.get("size", 0))
                col = s.get("color")
                rec["lines"].append({
                    "text": txt,
                    "x0": mm(x0), "y0": mm(y0), "x1": mm(x1), "y1": mm(y1),
                    "font": s.get("font", ""),
                    "size": round(s.get("size", 0) * PT2MM * 10, 1),  # pt -> mm*10
                    "size_pt": round(s.get("size", 0), 1),
                    "color": ("#%06X" % col) if isinstance(col, int) else None,
                    "bold": bool(re.search(r"(bold|semibold|black|heavy|demi)", s.get("font", ""), re.I)),
                })
                rec["spans"].append(s)
        pages.append(rec)
    return pages


# --------------------------------------------------------------------------
# 全局指纹
# --------------------------------------------------------------------------
def fingerprint(pages):
    fonts = Counter()
    sizes = Counter()
    colors = Counter()
    for p in pages:
        for l in p["lines"]:
            fonts[l["font"]] += 1
            sizes[l["size_pt"]] += 1
            if l["color"]:
                colors[l["color"]] += 1
    return fonts, sizes, colors


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def role_for_color(h, rank):
    """按饱和度 / 明度 / 使用频次猜颜色角色。"""
    r, g, b = hex2rgb(h)
    mx, mn = max(r, g, b), min(r, g, b)
    sat = 0 if mx == 0 else (mx - mn) / mx
    lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    if sat < 0.12 and lum < 0.25:
        return "text"          # 正文黑
    if sat < 0.12 and lum < 0.62:
        return "text-secondary"
    if sat < 0.12:
        return "meta"          # 浅灰：页码、目录页码
    if sat > 0.55 and lum < 0.75:
        return "primary"       # 品牌色（高饱和中低明度）
    return "accent"


# --------------------------------------------------------------------------
# 跨页重复文本 → 页眉 / 页脚 / CTA / 分隔符
# --------------------------------------------------------------------------
def repeated_text(pages, min_ratio=0.45, grp=None):
    n = len(pages)
    seen = defaultdict(lambda: {"pages": set(), "y": set(), "size": set(), "color": set(), "count": 0})
    for p in pages:
        if grp is not None and p["page"] not in grp:
            continue
        for l in p["lines"]:
            t = l["text"].strip()
            if not (1 <= len(t) <= 40):
                continue
            e = seen[t]
            e["pages"].add(p["page"])
            e["y"].add(round(l["y0"]))
            e["size"].add(l["size_pt"])
            e["color"].add(l["color"])
            e["count"] += 1
    out = []
    for t, e in seen.items():
        if len(e["pages"]) >= max(2, int(n * min_ratio * 0.5)) and e["count"] >= 3:
            out.append({
                "text": t,
                "pages": len(e["pages"]),
                "count": e["count"],
                "y_mm": sorted(e["y"])[0],
                "size_pt": sorted(e["size"])[0],
                "color": sorted([c for c in e["color"] if c])[0] if any(e["color"]) else None,
            })
    out.sort(key=lambda z: (-z["pages"], z["y_mm"]))
    return out


# --------------------------------------------------------------------------
# 页面特征 → 聚类出「页面模板」
# --------------------------------------------------------------------------
SIG_DIGIT = re.compile(r"^\d{1,3}$")


def page_features(p, page_h_mm, page_w_mm):
    full_img = 0
    band_img = 0
    small_img = 0
    for im in p["images"]:
        cover_ratio_w = im["w"] / page_w_mm
        cover_ratio_h = im["h"] / page_h_mm
        if cover_ratio_w > 0.9 and cover_ratio_h > 0.9:
            full_img += 1
        elif cover_ratio_w > 0.7 and cover_ratio_h > 0.2:
            band_img += 1
        else:
            small_img += 1
    left = Counter()
    right = Counter()
    body_chars = 0
    for l in p["lines"]:
        if len(l["text"]) < 6:
            continue
        # 排除页眉/页码所在的上下边缘
        if l["y0"] < 20 or l["y0"] > page_h_mm - 28:
            continue
        left[round(l["x0"] / 2) * 2] += 1
        right[round(l["x1"] / 2) * 2] += 1
        body_chars += len(l["text"])
    lx = left.most_common(1)[0][0] if left else None
    rx = right.most_common(1)[0][0] if right else None
    return {
        "full_img": full_img,
        "band_img": band_img,
        "small_img": small_img,
        "left": lx,
        "right": rx,
        "chars": body_chars,
    }


def signature(f):
    """刻意放粗粒度：正文右边缘会随末行长短抖动，不能进签名。"""
    if f["full_img"] and f["chars"] < 60:
        return ("graphic_only",)
    if f["full_img"] and f["chars"] >= 60:
        return ("graphic_with_text",)
    left = None if f["left"] is None else int(round(f["left"] / 5.0) * 5)
    imgs = 0 if f["small_img"] == 0 else (1 if f["small_img"] == 1 else 2)
    band = 1 if f["band_img"] >= 1 else 0
    return ("text", left, imgs, band)


def cluster(pages, feats, w_mm, h_mm):
    raw = defaultdict(list)
    for i, p in enumerate(pages):
        raw[signature(feats[i])].append(p["page"])
    items = sorted(raw.items(), key=lambda kv: min(kv[1]))

    clusters = []
    idx = 0
    for sig, pnos in items:
        pnos = sorted(pnos)
        # 满版出血页通常各自独立成 template（封面 / 分隔页 / 版权页）
        # 但数量太多时说明是「每页都有底图」的另一套路数，保持合并以免模板爆炸
        if sig[0].startswith("graphic") and len(pnos) <= 8:
            chunks = [[q] for q in pnos]
        else:
            chunks = [pnos]
        for grp in chunks:
            idx += 1
            gset = set(grp)
            l, r, body_size, body_font = Counter(), Counter(), Counter(), Counter()
            max_size = 0.0
            nlines = 0
            nchar = 0
            numeric_right = 0
            for p in pages:
                if p["page"] not in gset:
                    continue
                for ln in p["lines"]:
                    if ln["y0"] < 20 or ln["y0"] > mm(p["h_pt"]) - 28:
                        continue
                    nlines += 1
                    nchar += len(ln["text"])
                    max_size = max(max_size, ln["size_pt"])
                    if len(ln["text"]) >= 6:
                        l[round(ln["x0"])] += 1
                        r[round(ln["x1"])] += 1
                    if re.match(r"^\d{1,3}$", ln["text"].strip()) and ln["x1"] > w_mm * 0.6:
                        numeric_right += 1
                    if len(ln["text"]) >= 12:
                        body_size[ln["size_pt"]] += 1
                        body_font[ln["font"]] += 1
            clusters.append({
                "id": "T%d" % idx,
                "signature": list(sig),
                "pages": grp,
                "count": len(grp),
                "lines": nlines,
                "chars": nchar,
                "numeric_lines": numeric_right,
                "largest_size_pt": round(max_size, 1),
                "grid": {
                    "left_mm": float(l.most_common(1)[0][0]) if l else None,
                    "right_mm": float(r.most_common(1)[0][0]) if r else None,
                },
                "body_size_pt": body_size.most_common(1)[0][0] if body_size else None,
                "body_font": body_font.most_common(1)[0][0] if body_font else None,
            })
    return clusters


def guess_component(c, total_pages):
    """给模板猜一个渲染组件名（低置信，必须人工复核）。"""
    sig = c["signature"]
    pgs = c.get("pages") or []
    # 先按页序兜底：文本启发式遇到「封面带目录文字」的小开本就判成 quote
    if pgs and pgs[0] == 1:
        return ("cover", 0.6)
    if len(pgs) == 1 and pgs[0] >= total_pages:
        return ("backcover", 0.5)
    # 出血页：数量少时已按页独立成组，命名才有意义
    if sig[0].startswith("graphic"):
        if c["pages"] == [1]:
            return ("cover", 0.9)
        if c["count"] == 1:
            if max(c["pages"]) > total_pages - 2:
                return ("backcover", 0.5)
            return ("masthead", 0.5) if c["chars"] > 20 else ("divider", 0.55)
        return ("graphic_series", 0.3)

    hero = [s for s in c.get("image_slots", [])
            if s["role_guess"] == "hero" and s["page_ratio"] >= 0.5]
    icons = [s for s in c.get("image_slots", []) if s["role_guess"] == "icon"]
    cta = c.get("repeat_short_text", [])
    blocks = c.get("unit_block_chars")

    # 目录：右侧成排出现页码数字，且占比足够高
    # （正文页也会有脚注序号，光看绝对数量会把文章页误判成目录）
    dens = c["numeric_lines"] / max(1, c["lines"])
    if c.get("numeric_lines", 0) >= 5 and dens >= 0.15:
        return ("toc", 0.7)
    # 卷首引言 / 名家评价页：字大、行少
    if c["largest_size_pt"] >= 13 and c["lines"] <= 30:
        return ("quote", 0.5)
    # 栏目页：小尺寸插图 + 高频 CTA + 大量短内容块 → unit_list
    if hero and icons and cta and blocks and blocks["p50"] <= 400:
        return ("unit_list", 0.6)
    if hero and blocks and blocks["p50"] <= 400:
        return ("unit_list", 0.45)
    return ("article", 0.5)


# --------------------------------------------------------------------------
# 图片槽位
# --------------------------------------------------------------------------
def image_slots(pages, pnos, w_mm, h_mm):
    counter = Counter()
    sample = {}
    for p in pages:
        if p["page"] not in set(pnos):
            continue
        for im in p["images"]:
            key = (round(im["x0"] / 3) * 3, round(im["y0"] / 3) * 3,
                   round(im["w"] / 3) * 3, round(im["h"] / 3) * 3)
            counter[key] += 1
            sample.setdefault(key, im)
    n = len(pnos)
    slots = []
    for key, cnt in counter.most_common(12):
        x0, y0, w, h = key
        if w < 8 or h < 8:
            continue
        ratio = cnt / n
        role = ("logo" if (x0 < 40 and y0 < 40 and w < 90 and h < 30) else
                "hero" if (w > w_mm * 0.55 and y0 < h_mm * 0.45 and h > 40) else
                "background" if (w > w_mm * 0.9 and h > h_mm * 0.9) else
                "icon" if (w < 12 and h < 12) else
                "inline")
        slots.append({
            "id": "slot_%d_%d" % (round(x0), round(y0)),
            "x_mm": x0, "y_mm": y0, "w_mm": w, "h_mm": h,
            "aspect": round(w / h, 2),
            "pages": cnt,
            "page_ratio": round(ratio, 2),
            "role_guess": role,
            "recurring": ratio >= 0.6,
        })
    slots.sort(key=lambda s: (-(s["page_ratio"]), s["y_mm"]))
    return slots


# --------------------------------------------------------------------------
# 单元切片：识别栏目内反复出现的内容原子
# --------------------------------------------------------------------------
def unit_slices(pages, pnos):
    """找 short 的、在同一页内多次出现、或跨页重复出现的短文本
    —— 通常就是 CTA（阅读原文）/ 地区前缀 / 小标题。"""
    gset = set(pnos)
    cnt = Counter()
    positions = Counter()
    for p in pages:
        if p["page"] not in gset:
            continue
        for ln in p["lines"]:
            t = ln["text"].strip()
            if 2 <= len(t) <= 8 and not SIG_DIGIT.match(t):
                cnt[t] += 1
                positions[t] += 1
    cands = [(t, c) for t, c in cnt.most_common(10) if c >= 3]
    # 测量正文块长度：标题（bold）到下一个标题之间的字符数
    blocks = []
    for p in pages:
        if p["page"] not in gset:
            continue
        cur = None
        for ln in p["lines"]:
            if ln["y0"] < 20 or ln["y0"] > mm(pages[0]["h_pt"]) - 30:
                continue
            if ln["bold"] and len(ln["text"]) <= 40:
                if cur is not None:
                    blocks.append(cur)
                cur = {"title": ln["text"], "chars": 0}
            elif cur is not None:
                cur["chars"] += len(ln["text"])
        if cur:
            blocks.append(cur)
    blocks = [b for b in blocks if b["chars"] > 40]
    lens = sorted(b["chars"] for b in blocks)
    stats = None
    if lens:
        stats = {
            "n": len(lens),
            "min": lens[0],
            "p50": lens[len(lens) // 2],
            "max": lens[-1],
        }
    return cands, stats, blocks[:12]


# --------------------------------------------------------------------------
# 主流程
# --------------------------------------------------------------------------

def columns_detect(pages):
    """检测正文栏数：同一页行起点出现 >10mm 空档、且两侧各有足够行数。

    判空档而不是判行宽，是因为跨栏标题会拉宽单行——行宽判据在文章首页必然误判。
    """
    text_pages = [p for p in pages if len(p["lines"]) >= 8]
    if not text_pages:
        return 1, 0.0
    multi = 0
    for p in text_pages:
        xs = sorted(l["x0"] for l in p["lines"])
        n = len(xs)
        gap, gi = 0.0, -1
        for i in range(1, n):
            if xs[i] - xs[i - 1] > gap:
                gap, gi = xs[i] - xs[i - 1], i
        if gap >= 10.0 and gi >= n * 0.25 and (n - gi) >= n * 0.25:
            multi += 1
    frac = multi / float(len(text_pages))
    return (2 if frac >= 0.35 else 1), round(frac, 2)


def text_extent(pages):
    """样刊正文的左右边界（3% 分位，避开零星出血元素）。"""
    a = sorted(l["x0"] for p in pages for l in p["lines"] if len(l["text"]) >= 4)
    b = sorted(l["x1"] for p in pages for l in p["lines"] if len(l["text"]) >= 4)
    if not a:
        return None, None
    return (round(a[int(len(a) * 0.03)], 1), round(b[int(len(b) * 0.97)], 1))


def body_color_measured(pages):
    """实测正文色：正文字号下承载字符最多的颜色。

    role_for_color() 按亮度阈值硬判，遇到「正文用中灰」的设计（律所/咨询年度刊常见）
    会把正文色降级成 text-secondary，roles.text 落到一个正文里根本不用的颜色上。
    这里给出实测值，让差异可被自动发现。
    """
    sizes, byc = Counter(), defaultdict(Counter)
    for p in pages:
        for l in p["lines"]:
            if len(l["text"]) < 2:
                continue
            sizes[l["size_pt"]] += len(l["text"])
            if l["color"]:
                byc[l["size_pt"]][l["color"]] += len(l["text"])
    if not sizes:
        return None, None, 0.0
    body_pt = sizes.most_common(1)[0][0]
    top = byc[body_pt]
    if not top:
        return None, body_pt, 0.0
    hexv, n = top.most_common(1)[0]
    return hexv, body_pt, round(n / float(max(1, sum(top.values()))), 3)


WEB_UI_HINTS = ("返回顶部", "立即提交", "隐私声明", "请选择", "全名", "联系电话",
                "职位类别", "我已阅读并同意", "立即咨询", "业务咨询热线",
                "扫码关注", "扫码立即")


def sample_quality(pages):
    """样例质量预检。网页另存 PDF 会把导航菜单与联系表单一起带进来，
    当作设计稿件提取会得到一份「栏目像正文、表单像内容」的 spec。"""
    tot = sum(len(p["lines"]) for p in pages)
    if not tot:
        return {"verdict": "empty", "short_ratio": 0.0, "ui_hits": [], "advice": "文字层为空"}
    short = sum(1 for p in pages for l in p["lines"] if len(l["text"]) <= 6)
    short_ratio = round(short / float(tot), 2)
    hits = [h for h in WEB_UI_HINTS if any(h in l["text"] for p in pages for l in p["lines"])]
    bad = len(hits) >= 4 or short_ratio > 0.55
    return {
        "verdict": "suspected_web_print" if bad else "looks_like_design",
        "short_ratio": short_ratio,
        "ui_hits": hits,
        "advice": ("这份 PDF 更像网页打印稿（命中界面文案：%s；短行占比 %.0f%%）。"
                   "导航菜单与表单会被当成正文与栏目提取，请改用设计稿或刊物原版 PDF。"
                   % ("、".join(hits), short_ratio * 100)) if bad else "未发现网页打印稿特征",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--out", default=".")
    ap.add_argument("--max-pages", type=int, default=0)
    args = ap.parse_args()

    try:
        import pymupdf
    except ImportError:
        try:
            import fitz as pymupdf  # noqa
        except ImportError:
            sys.exit("缺少依赖：python -m pip install pymupdf（macOS/Linux 用 python3）")

    doc = pymupdf.open(args.pdf)
    if args.max_pages:
        doc = doc[:args.max_pages] if hasattr(doc, "__getitem__") else doc
    pages = collect(doc)
    total = len(pages)
    if total == 0:
        sys.exit("未取到任何页面")

    w_mm, h_mm = mm(pages[0]["w_pt"]), mm(pages[0]["h_pt"])
    feats = [page_features(p, h_mm, w_mm) for p in pages]
    clusters = cluster(pages, feats, w_mm, h_mm)
    fonts, sizes, colors = fingerprint(pages)

    total_lines = sum(len(p["lines"]) for p in pages)
    if total_lines < 30:
        sys.stderr.write(
            "[WARN] 文字层极薄（仅 %d 行）。很可能是扫描件，请先 OCR / 走 omni-reader 解析后重试。\n"
            % total_lines)

    # ---------- 色板 ----------
    palette = []
    for h, c in colors.most_common(12):
        palette.append({
            "hex": h,
            "count": c,
            "ratio": round(c / max(1, total_lines), 3),
            "role_guess": role_for_color(h, 0),
        })
    # 角色去重：每种角色保留频次最高的
    best = {}
    for p in palette:
        r = p["role_guess"]
        if r not in best or p["count"] > best[r]["count"]:
            best[r] = p
    roles = {k: v for k, v in best.items()}

    # ---------- 字号表 ----------
    type_scale = []
    for sz, c in sorted(sizes.items(), key=lambda kv: (-kv[1]))[:14]:
        type_scale.append({"size_pt": sz, "size_mm10": round(sz * PT2MM * 10, 1), "count": c})
    type_scale.sort(key=lambda z: -z["size_pt"])

    # ---------- 页眉/页脚/页码 ----------
    chrome = repeated_text(pages, min_ratio=0.4)
    running = [c for c in chrome if c["pages"] >= max(3, int(total * 0.4))]
    cta = [c for c in chrome if c["count"] >= total * 0.25 and len(c["text"]) <= 6]

    # 页码：纯数字且在页上下边缘
    folio = {"y_mm": None, "align": None, "size_pt": None, "color": None}
    fy = Counter()
    fsz = Counter()
    fcol = Counter()
    fx = Counter()
    for p in pages:
        for ln in p["lines"]:
            if SIG_DIGIT.match(ln["text"].strip()) and (ln["y0"] < 22 or ln["y0"] > h_mm - 30):
                fy[round(ln["y0"])] += 1
                fsz[ln["size_pt"]] += 1
                fcol[ln["color"]] += 1
                fx["right" if ln["x1"] > w_mm * 0.75 else ("center" if ln["x0"] > w_mm * 0.35 else "left")] += 1
    if fy:
        folio = {
            "y_mm": float(fy.most_common(1)[0][0]),
            "align": fx.most_common(1)[0][0],
            "size_pt": fsz.most_common(1)[0][0],
            "color": fcol.most_common(1)[0][0],
        }

    # ---------- 每聚类细项 ----------
    for c in clusters:
        c["image_slots"] = image_slots(pages, c["pages"], w_mm, h_mm)
        cands, stats, samples = unit_slices(pages, c["pages"])
        c["repeat_short_text"] = [{"text": t, "n": n} for t, n in cands[:6]]
        if stats:
            c["unit_block_chars"] = stats
            c["unit_samples"] = samples[:4]
        # 组件推断必须在 slots / units 算完之后（否则丢判据）
        comp, conf = guess_component(c, total)
        c["component_guess"] = comp
        c["confidence"] = conf

    cols, cols_frac = columns_detect(pages)
    ext_l, ext_r = text_extent(pages)
    body_hex, body_pt, body_ratio = body_color_measured(pages)
    quality = sample_quality(pages)

    auto_baseline = {
        "pages": total,
        "chars": sum(len(l["text"]) for p in pages for l in p["lines"]),
        "source": ("自动实测：PyMuPDF 抽取 %d 页 / %d 字。"
                   "articles 与 units 无法自动估准，须人工补——补齐前 --stats 只覆盖页数与字数。"
                   % (total, sum(len(l["text"]) for p in pages for l in p["lines"]))),
    }
    if quality["verdict"] == "suspected_web_print":
        sys.stderr.write("[WARN] %s\n" % quality["advice"])
    if body_hex and roles.get("text") and body_hex != roles.get("text"):
        sys.stderr.write(
            "[WARN] 实测正文色为 %s（%.0f%% 的正文由它承载），而 roles.text 推断为 %s。"
            "role_for_color 按亮度硬判，遇到中灰正文会降级；请以实测值为准复核。\n"
            % (body_hex, body_ratio * 100, roles.get("text")))
    if cols >= 2:
        sys.stderr.write(
            "[WARN] 样刊是 %d 栏版面（%.0f%% 的正文页命中分栏空档）。渲染器目前只出单栏，"
            "版心按全文宽度 %s..%s mm 取；要复现双栏需人工排版。\n"
            % (cols, cols_frac * 100, ext_l, ext_r))

    spec = {
        "meta": {
            "source_file": os.path.basename(args.pdf),
            "page_count": total,
            "extractor": "extract_style.py 0.1.0",
            "confidence_note": "所有 *_guess 字段均为启发式推断，必须经人工复核后定稿",
        },
        "canvas": {
            "size_mm": [round(w_mm), round(h_mm)],
            "standard_size": "A4" if abs(w_mm - 210) < 3 and abs(h_mm - 297) < 3 else "custom",
            "bleed_mm": 0,
            "columns": cols,
            "columns_frac": cols_frac,
            "text_extent_mm": [ext_l, ext_r],
            "geometry_note": ("渲染器的组件几何（封面/引言/目录/编委会/封底的 mm 定位）"
                              "是按 A4 样刊调的，非 A4 开本下版心不成比例，需人工微调。"),
        },
        "palette": {
            "roles": {k: v["hex"] for k, v in roles.items()},
            "full": palette,
            "body_color_measured": body_hex,
            "body_color_size_pt": body_pt,
            "body_color_ratio": body_ratio,
        },
        "typography": {
            "families": [f for f, _ in fonts.most_common(8)],
            "type_scale": type_scale,
        },
        "chrome": {
            "running_head": running[:4],
            "folio": folio,
            "cta_candidates": cta[:3],
        },
        "page_templates": [
            {k: v for k, v in c.items() if k != "signature"} | {"signature": c["signature"]}
            for c in clusters
        ],
        "scale_baseline": auto_baseline,
        "sample_quality": quality,
    }
    # 多栏样刊：显式给出网格，否则 build_draft 会拿某一栏当整页版心
    if cols >= 2 and ext_l is not None and ext_r is not None and ext_r > ext_l:
        spec["grids"] = {"A": {"left_mm": ext_l, "right_mm": ext_r},
                         "B": {"left_mm": ext_l, "right_mm": ext_r}}

    os.makedirs(args.out, exist_ok=True)
    jp = os.path.join(args.out, "stylespec.json")
    mp = os.path.join(args.out, "stylespec.md")
    with open(jp, "w", encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False, indent=2)
    with open(mp, "w", encoding="utf-8") as f:
        f.write(render_md(spec, feats))

    print("OK  pages=%d  templates=%d  columns=%d  开本=%.0fx%.0fmm"
          % (total, len(clusters), cols, w_mm, h_mm))
    print("baseline  pages=%d  chars=%d  （articles/units 须人工补）"
          % (auto_baseline["pages"], auto_baseline["chars"]))
    if body_hex:
        print("正文色实测 %s  @%.1fpt  %.0f%%" % (body_hex, body_pt, body_ratio * 100))
    print("json: %s" % os.path.abspath(jp))
    print("md  : %s" % os.path.abspath(mp))
    for c in clusters:
        print("  %-3s %-22s pages=%-3d grid=%s..%s conf=%.1f" % (
            c["id"], c["component_guess"], c["count"],
            c["grid"]["left_mm"], c["grid"]["right_mm"], c["confidence"]))


def render_md(spec, feats):
    L = []
    L.append("# StyleSpec 草稿（自动提取）\n")
    L.append("> 来源 `%s`，共 %d 页。**所有推断字段必须人工复核后定稿。**\n"
             % (spec["meta"]["source_file"], spec["meta"]["page_count"]))
    L.append("## 开本\n")
    L.append("- 尺寸：%s mm（%s），出血待确认：%s\n"
             % (spec["canvas"]["size_mm"], spec["canvas"]["standard_size"], spec["canvas"]["bleed_mm"]))
    cv = spec["canvas"]
    if cv.get("columns"):
        L.append("- 正文栏数：**%d 栏**（%.0f%% 的正文页命中分栏空档）\n"
                 % (cv["columns"], cv.get("columns_frac", 0) * 100))
        if cv["columns"] >= 2:
            L.append("  > 渲染器目前只出单栏。要复现双栏需人工排版；"
                     "本次按全文宽度 %s mm 出单栏。\n" % cv.get("text_extent_mm"))
    q = spec.get("sample_quality") or {}
    if q.get("verdict") == "suspected_web_print":
        L.append("\n> **[!] 样例质量告警**：%s\n" % q.get("advice"))
    bl = spec.get("scale_baseline") or {}
    if bl:
        L.append("\n## 篇幅基线（自动实测）\n")
        L.append("| 项 | 值 |\n|---|---|\n")
        L.append("| 页数 | %s |\n" % bl.get("pages"))
        L.append("| 全文字数 | %s |\n" % bl.get("chars"))
        L.append("\n> %s\n" % bl.get("source"))
    L.append("## 色板\n")
    L.append("| 角色 | 色值 | 占比 |\n|---|---|---|\n")
    order = ["primary", "accent", "text", "text-secondary", "meta"]
    for r in order:
        if r in spec["palette"]["roles"]:
            full = next(x for x in spec["palette"]["full"] if x["hex"] == spec["palette"]["roles"][r])
            L.append("| %s | `%s` | %.0f%% |\n" % (r, full["hex"], full["ratio"] * 100))
    pm = spec["palette"]
    if pm.get("body_color_measured") and pm["body_color_measured"] != pm["roles"].get("text"):
        L.append("> **[!] 正文色不一致**：实测正文色 `%s`（%.0f%% 的正文由它承载，@%s pt），"
                 "而 `roles.text` 推断为 `%s`。以实测值为准复核。\n"
                 % (pm["body_color_measured"], pm.get("body_color_ratio", 0) * 100,
                    pm.get("body_color_size_pt"), pm["roles"].get("text")))
    L.append("\n<details><summary>全部取色</summary>\n\n")
    L.append("| 色值 | 行数 | 角色猜测 |\n|---|---|---|\n")
    for p in spec["palette"]["full"]:
        L.append("| `%s` | %d | %s |\n" % (p["hex"], p["count"], p["role_guess"]))
    L.append("\n</details>\n")
    L.append("## 字体与字号\n")
    L.append("- 字族：%s\n" % "、".join(spec["typography"]["families"]))
    L.append("\n| 字号(pt) | 出现行数 | 建议角色 |\n|---|---|---|\n")
    for i, t in enumerate(spec["typography"]["type_scale"]):
        role = ["封面大字", "大标题", "栏目标题", "文章题", "小标题", "正文", "辅助/图注"][min(i, 6)]
        L.append("| %s | %d | %s |\n" % (t["size_pt"], t["count"], role))
    L.append("## 页眉 / 页码\n")
    L.append("- 页码：y=%s mm，%s 对齐，%s pt，`%s`\n"
             % (spec["chrome"]["folio"]["y_mm"], spec["chrome"]["folio"]["align"],
                spec["chrome"]["folio"]["size_pt"], spec["chrome"]["folio"]["color"]))
    if spec["chrome"]["running_head"]:
        L.append("- 跨页重复文本（疑似页眉）：%s\n"
                 % "、".join("「%s」" % x["text"] for x in spec["chrome"]["running_head"][:3]))
    if spec["chrome"]["cta_candidates"]:
        L.append("- 疑似 CTA / 固定短语：%s\n"
                 % "、".join("「%s」(×%d)" % (x["text"], x["count"]) for x in spec["chrome"]["cta_candidates"]))
    L.append("## 页面模板\n")
    for c in spec["page_templates"]:
        show = c["pages"] if len(c["pages"]) <= 12 else "%s…%s" % (c["pages"][:6], c["pages"][-2:])
        L.append("\n### %s · %s（第 %s 页，共 %d 页，置信 %.1f）\n"
                 % (c["id"], c["component_guess"], show, c["count"], c["confidence"]))
        _gw = round((c["grid"]["right_mm"] or 0) - (c["grid"]["left_mm"] or 0), 1)
        L.append("- 网格：左 %s mm → 右 %s mm（版心宽 %s mm）%s\n"
                 % (c["grid"]["left_mm"], c["grid"]["right_mm"], _gw,
                    "  **[异常] 右边界小于左边界**：grid 两端取自 x0 与 x1 两个独立众数，"
                    "会互相穿越。渲染器已忽略此类网格，此处仅作留档。" if _gw <= 0 else ""))
        L.append("- 正文字号 %s pt / %s\n" % (c["body_size_pt"], c["body_font"]))
        if c.get("image_slots"):
            L.append("- 图片槽位：\n\n| 角色猜测 | 位置 x,y (mm) | 尺寸 w×h (mm) | 比例 | 出现页占比 |\n|---|---|---|---|---|\n")
            for s in c["image_slots"][:6]:
                L.append("| %s | %s,%s | %s×%s | %s | %.0f%% |\n"
                         % (s["role_guess"], s["x_mm"], s["y_mm"], s["w_mm"], s["h_mm"],
                            s["aspect"], s["page_ratio"] * 100))
        if c.get("unit_block_chars"):
            u = c["unit_block_chars"]
            L.append("- 内容块字数：n=%d，min=%d，中位=%d，max=%d\n"
                     % (u["n"], u["min"], u["p50"], u["max"]))
        if c.get("repeat_short_text"):
            L.append("- 组内高频短语：%s\n"
                     % "、".join("「%s」×%d" % (x["text"], x["n"]) for x in c["repeat_short_text"][:5]))
    L.append("\n## 待人工补全\n")
    L.append("- [ ] 品牌色是否另有 CMYK / Pantone 值\n")
    L.append("- [ ] 企业 logo 是否有矢量文件（AI / SVG）\n")
    L.append("- [ ] 行距倍数与段间距（脚本难以可靠测量，需在样张 PDF 上目测补）\n")
    L.append("- [ ] 调性：人称、句长、术语密度、「阅读原文」类 CTA 是否每条必带\n")
    L.append("- [ ] 图形纹样 / 辅助图形 / 摄影 vs 插画风格\n")
    return "".join(L)


if __name__ == "__main__":
    main()

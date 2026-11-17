#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF -> 结构化 Markdown

专为「课件/讲义类 PDF」设计，尽量还原原始结构：
  * 按字号识别标题层级
  * 按等宽字体识别代码块
  * 自动剔除每页重复的页脚/水印
  * 自动剔除代码的行号栏
  * 表格用 pymupdf find_tables 结构化提取
  * 扫描版页面自动渲染成 PNG，输出清单供 AI 视觉识别

用法:
  python pdf_to_markdown.py <pdf> [-o out.md] [--scan-dir DIR] [--dpi 200] [--json]
"""
import argparse
import json
import os
import re
import sys
from collections import Counter

# Windows 控制台默认 GBK，输出含 emoji / 生僻字会崩，强制 UTF-8
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

try:
    import pymupdf
except ImportError:
    try:
        import fitz as pymupdf
    except ImportError:
        print(json.dumps({"success": False,
                          "error": "缺少 pymupdf，请先执行: pip install pymupdf"},
                         ensure_ascii=False))
        sys.exit(1)

MONO_HINTS = ("mono", "courier", "consol", "sourcecodepro", "menlo", "dejavu sans mono")


def is_mono(font_name: str) -> bool:
    f = (font_name or "").lower()
    return any(h in f for h in MONO_HINTS)


def dominant_font(spans):
    """占字符数最多的 span 的字体，作为整行的主导字体"""
    best, n = "", -1
    for s in spans:
        ln = len(s.get("text", ""))
        if ln > n:
            n, best = ln, s.get("font", "")
    return best


def scan_pages(path, scan_dir, dpi):
    """把文字层稀少的页面渲染成 PNG，交给 AI 视觉识别"""
    doc = pymupdf.open(path)
    images = []
    for pno in range(doc.page_count):
        page = doc[pno]
        if len(page.get_text().strip()) >= 20:
            continue
        os.makedirs(scan_dir, exist_ok=True)
        out = os.path.join(scan_dir, "page_%03d.png" % (pno + 1))
        page.get_pixmap(dpi=dpi).save(out)
        images.append({"page": pno + 1, "image": os.path.abspath(out)})
    return images


def table_rects(path):
    """逐页返回表格占用的矩形区域，用于把表格文字从正文/代码里排除"""
    doc = pymupdf.open(path)
    out = []
    for pno in range(doc.page_count):
        rects = []
        try:
            tabs = doc[pno].find_tables()
        except Exception:
            tabs = None
        for t in getattr(tabs, "tables", []) or []:
            try:
                rects.append(pymupdf.Rect(t.bbox))
            except Exception:
                pass
        out.append(rects)
    return out


def collect_lines(path, skip_rects=None):
    """逐页收集文本行，带上字号和字体信息。

    skip_rects: 每页要跳过的区域（表格），避免表格文字混进正文或代码块。
    """
    doc = pymupdf.open(path)
    pages = []
    for pno in range(doc.page_count):
        rects = (skip_rects[pno] if skip_rects and pno < len(skip_rects) else [])
        lines = []
        for b in doc[pno].get_text("dict")["blocks"]:
            if b.get("type") != 0:
                continue
            for ln in b["lines"]:
                spans = ln["spans"]
                if not spans:
                    continue
                text = "".join(s["text"] for s in spans).replace("\u200b", "").rstrip()
                if not text.strip():
                    continue
                # 跳过落在表格区域内的行
                if rects:
                    try:
                        cx = (ln["bbox"][0] + ln["bbox"][2]) / 2
                        cy = (ln["bbox"][1] + ln["bbox"][3]) / 2
                        if any(r.contains(pymupdf.Point(cx, cy)) for r in rects):
                            continue
                    except Exception:
                        pass
                lines.append({
                    "text": text,
                    "size": round(max(s["size"] for s in spans), 1),
                    "font": spans[0]["font"],
                    # 用「占字符最多的那个 span」的字体作为整行的主导字体，
                    # 避免个别回退字体 span 影响判断
                    "mono": is_mono(dominant_font(spans)),
                })
        pages.append(lines)
    return doc, pages


def find_footers(pages, min_ratio=0.5):
    """找出在多数页面重复出现的短行（页脚/水印）"""
    if len(pages) < 3:
        return set()
    cnt = Counter()
    for lines in pages:
        for t in {l["text"].strip() for l in lines}:
            if t and len(t) < 120:
                cnt[t] += 1
    threshold = max(2, int(len(pages) * min_ratio))
    return {t for t, c in cnt.items() if c >= threshold}


def extract_tables(path):
    """用 pymupdf 内置 find_tables 提取表格，转成 Markdown"""
    doc = pymupdf.open(path)
    out = []
    for pno in range(doc.page_count):
        try:
            tabs = doc[pno].find_tables()
        except Exception:
            continue
        for t in getattr(tabs, "tables", []):
            try:
                md = t.to_markdown()
            except Exception:
                continue
            if md and md.strip():
                out.append({"page": pno + 1, "markdown": md.strip()})
    return out


def build_markdown(path, scan_dir="ocr_pages", dpi=200,
                   no_tables=False, no_render=False):
    rects = [] if no_tables else table_rects(path)
    doc, pages = collect_lines(path, rects)
    footers = find_footers(pages)

    # 正文基准字号。
    # 注意：有些 PDF 的「正文段落」和「代码」用同一种等宽字体，只有字号不同
    # （正文 12.0 / 代码 10.5），所以不能只看字体。
    # 做法：取「出现次数 ≥ 总行数 5%」的字号视为正文带，其中的最大字号即正文，
    # 比它小的等宽行就是代码；比它大的就是标题。
    all_sizes = Counter()
    for lines in pages:
        for l in lines:
            all_sizes[l["size"]] += 1
    total = sum(all_sizes.values()) or 1
    band = [s for s, c in all_sizes.items() if c >= total * 0.05]
    body_size = max(band) if band else (all_sizes.most_common(1)[0][0] if all_sizes else 12.0)

    def is_code_line(l):
        return l["mono"] and l["size"] < body_size - 0.2

    # 若一条代码都判不出来，退回纯字体判定
    if not any(is_code_line(l) for lines in pages for l in lines):
        def is_code_line(l):
            return l["mono"]

    head_sizes = sorted({l["size"] for lines in pages for l in lines
                         if not l["mono"] and l["size"] > body_size + 0.5},
                        reverse=True)

    def head_level(size):
        if size not in head_sizes:
            return 0
        return min(head_sizes.index(size) + 1, 6)

    md, stats = [], {"code_blocks": 0, "headings": 0, "tables": 0,
                     "skipped_footer": 0, "skipped_lineno": 0}

    for pno, lines in enumerate(pages):
        i = 0
        while i < len(lines):
            l = lines[i]
            t = l["text"].strip()

            # 页脚 / 水印
            if t in footers:
                stats["skipped_footer"] += 1
                i += 1
                continue

            # 代码行号栏：连续 >=3 行纯数字，且当前行是纯数字
            if re.fullmatch(r"\d{1,3}", t):
                j = i
                while j < len(lines) and re.fullmatch(r"\d{1,3}", lines[j]["text"].strip()):
                    j += 1
                if j - i >= 3:
                    stats["skipped_lineno"] += j - i
                    i = j
                    continue

            # 代码块
            if is_code_line(l):
                block = []
                while i < len(lines) and is_code_line(lines[i]):
                    s = lines[i]["text"].strip()
                    if s in footers or re.fullmatch(r"\d{1,3}", s):
                        i += 1
                        continue
                    block.append(lines[i]["text"])
                    i += 1
                while block and not block[0].strip():
                    block.pop(0)
                while block and not block[-1].strip():
                    block.pop()
                if block:
                    md.append("```cpp")
                    md.extend(block)
                    md.append("```")
                    md.append("")
                    stats["code_blocks"] += 1
                continue

            # 标题
            lvl = head_level(l["size"])
            if lvl:
                md.append("#" * lvl + " " + t)
                md.append("")
                stats["headings"] += 1
                i += 1
                continue

            md.append(t)
            md.append("")
            i += 1

    tables = [] if no_tables else extract_tables(path)
    stats["tables"] = len(tables)

    scan_images = [] if no_render else scan_pages(path, scan_dir, dpi)

    text = "\n".join(md)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"
    return {
        "success": True,
        "page_count": doc.page_count,
        "text": text,
        "tables_markdown": tables,
        "ocr_images": scan_images,
        "stats": stats,
        "warnings": ([f"第 {im['page']} 页文字层为空，已渲染为图片，请用 read_image 识别"
                      for im in scan_images]),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("-o", "--out")
    ap.add_argument("--scan-dir", default="ocr_pages")
    ap.add_argument("--dpi", type=int, default=200)
    ap.add_argument("--no-tables", action="store_true")
    ap.add_argument("--no-render", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if not os.path.isfile(a.pdf):
        print(json.dumps({"success": False, "error": f"文件不存在: {a.pdf}"}, ensure_ascii=False))
        sys.exit(1)

    r = build_markdown(a.pdf, a.scan_dir, a.dpi, a.no_tables, a.no_render)

    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(r["text"])
        r["saved_to"] = os.path.abspath(a.out)

    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(r["text"])
        if r["tables_markdown"]:
            print("\n<!-- ===== 表格 ===== -->")
            for t in r["tables_markdown"]:
                print("\n<!-- 第 %d 页 -->" % t["page"])
                print(t["markdown"])
        if r["warnings"]:
            print("\n<!-- 警告: %s -->" % "；".join(r["warnings"]))
        if a.out:
            print("\n<!-- 已保存: %s -->" % r["saved_to"])


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check a docs-to-knowledge HTML file (multi-page structured knowledge).

Usage:
    python check_knowledge.py <knowledge.html> [--map <map.html>]

Exit code: 0 = pass (warnings allowed), 1 = hard failure
"""

import argparse
import html
import re
import sys
from pathlib import Path

MAX_PAGES = 6
MIN_PAGES = 3
PER_PAGE_MAX = 950   # CJK chars per page (upper bound, no lower bound)
MAP_SRC = r'map-src'
FRESH_MAX_INLINE = 12

HEADING_ABSTRACT = {
    "输出", "标准", "格式", "规范", "目标", "流程", "边界", "评测", "迭代",
    "资源", "权限", "状态", "依赖", "异常", "兜底", "配置", "管理", "设计",
    "实现", "机制", "方案", "模块", "系统", "能力", "工作流", "验收", "呈现",
    "内容", "形式",
}


def drop_comments(raw: str) -> str:
    return re.sub(r"<!--.*?-->", "", raw, flags=re.S)


def visible_text(fragment: str) -> str:
    text = re.sub(r"<script\b.*?</script>", " ", fragment, flags=re.S | re.I)
    text = re.sub(r"<style\b.*?</style>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return html.unescape(text)


def count_cjk(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def extract_headings(fragment: str) -> list:
    headings = []
    for m in re.finditer(r"<h([2-4])\b[^>]*>(.*?)</h\1>", fragment, flags=re.S | re.I):
        text = re.sub(r"\s+", " ", visible_text(m.group(2))).strip()
        if text:
            headings.append((int(m.group(1)), text))
    return headings


def heading_collisions(headings: list) -> list:
    hits = []
    for i in range(len(headings)):
        for j in range(i + 1, len(headings)):
            la, a = headings[i]
            lb, b = headings[j]
            if la != lb:          # only compare sibling-level headings
                continue
            if a == b:
                hits.append((a, b, {"重复标题"}))
                continue
            shared = {w for w in HEADING_ABSTRACT if w in a and w in b}
            if shared:
                hits.append((a, b, shared))
    return hits


def extract_balanced(fragment: str, start: int) -> str:
    tag = re.match(r"<(div|section)\b", fragment[start:])
    if not tag:
        return fragment[start:start + 200]
    name = tag.group(1)
    depth = 0
    for m in re.finditer(rf"<{name}\b[^>]*>|</{name}>", fragment[start:], flags=re.I):
        depth += -1 if m.group(0).startswith("</") else 1
        if depth == 0:
            return fragment[start:start + m.end()]
    return fragment[start:]


def extract_pages(fragment: str) -> list:
    out = []
    for m in re.finditer(r'<section\b[^>]*class="[^"]*\bpage\b[^"]*"[^>]*>', fragment, flags=re.I):
        out.append(extract_balanced(fragment, m.start()))
    return out


def extract_class(fragment: str, class_name: str) -> list:
    out = []
    for m in re.finditer(
            rf'<(div|section)\b[^>]*class="[^"]*\b{class_name}\b(?!-)[^"]*"[^>]*>',
            fragment, flags=re.S | re.I):
        out.append(extract_balanced(fragment, m.start()))
    return out


def check_map(path: str, errors, warnings):
    raw = Path(path).read_text(encoding="utf-8", errors="replace")
    scripts = re.findall(r'<script[^>]+src=["\'](https?:)?//', raw, flags=re.I)
    links = re.findall(r'<link[^>]+href=["\'](https?:)?//', raw, flags=re.I)
    if scripts or links:
        errors.append(f"markmap 产物含 {len(scripts) + len(links)} 个外部资源引用，不是离线自包含")
    if "markmap" not in raw:
        warnings.append("map 文件里未发现 markmap 痕迹，确认是不是正确产物")
    print(f"map file    : {path} (external: {len(scripts) + len(links)})")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--map")
    args = ap.parse_args()

    raw = Path(args.html).read_text(encoding="utf-8")
    body = drop_comments(raw)
    errors, warnings = [], []

    fresh_blocks = extract_class(body, "freshness")
    fresh_html = "\n".join(fresh_blocks)
    fresh_chars = count_cjk(visible_text(fresh_html))

    pages = extract_pages(body)
    page_chars = []
    for p in pages:
        p_wo = p
        for b in fresh_blocks:
            p_wo = p_wo.replace(b, " ")
        page_chars.append(count_cjk(visible_text(p_wo)))

    total = sum(page_chars)
    cards = len(re.findall(r'class="[^"]*\bdetail-card\b', body, flags=re.I))
    todos = len(re.findall(r"待确认|待补|待核实|如果当时|诚实|设计扩展|真实做法", visible_text(body)))
    links_total = len(re.findall(r'\[\w', visible_text(body)))  # broken md links like [x
    svgs = len(re.findall(r"<svg\b", body, flags=re.I))
    tables = len(re.findall(r"<table\b", body, flags=re.I))
    font_sizes = [float(x) for x in re.findall(r"font-size\s*:\s*([0-9.]+)\s*pt", raw, flags=re.I)]
    min_font = min(font_sizes) if font_sizes else None
    external = re.findall(r'(?:src|href)\s*=\s*["\'](?:https?:)?//', body, flags=re.I)
    scripts = re.findall(r"<script\b", body, flags=re.I)
    details = re.findall(r"<details\b", body, flags=re.I)
    fixed = re.findall(r"position\s*:\s*fixed", body, flags=re.I)
    broken_md = re.findall(r"</?[a-z]+>\s*\]\(|\]\([^)]*\)", visible_text(body))
    placeholders = re.findall(r"\{\{[^}]+\}\}", body)

    if not (MIN_PAGES <= len(pages) <= MAX_PAGES):
        errors.append(f"页数必须 {MIN_PAGES}–{MAX_PAGES}，当前 {len(pages)}")
    for i, c in enumerate(page_chars, 1):
        if c > PER_PAGE_MAX:
            errors.append(f"第 {i} 页 {c} 字符超过单页上限 {PER_PAGE_MAX}（按保留规则删铺垫，不删关键说明）")
    if total == 0:
        errors.append("没有检测到中文正文")
    if min_font is not None and min_font < 9.0:
        errors.append(f"最小字号 {min_font}pt 低于 9pt")
    if not ("@page" in raw and "size:A4" in raw.replace(" ", "")):
        errors.append("缺少 @page { size: A4 }")
    if external:
        errors.append(f"主文档含 {len(external)} 个外部资源引用，必须离线可用")
    if scripts:
        warnings.append(f"主文档含 {len(scripts)} 个 <script>（主文档应零 JS；交互图放 map 文件）")
    if details or fixed:
        errors.append("存在 <details> 或 position:fixed，打印会丢失/错位")
    if placeholders:
        errors.append(f"还有 {len(placeholders)} 个未替换占位符")
    if links_total or broken_md:
        warnings.append(f"疑似残留 Markdown 链接 {max(links_total, len(broken_md))} 处，HTML 文档里应去掉或改为纯文本")
    if cards == 0:
        warnings.append("没有细节卡片（detail-card），确认是否遗漏细节文件")
    if todos == 0:
        warnings.append("未发现 待确认/待补/如果当时 标记——诚实标记应原样保留，确认没有误删")
    if fresh_html and not re.search(r"核实", fresh_html):
        warnings.append("时效区块缺少“核实”字样")

    # --- editorial: heading collision ---
    for a, b, shared in heading_collisions(extract_headings(body)):
        warnings.append(
            f"标题撞词：「{a}」与「{b}」共享 {'/'.join(sorted(shared))}；"
            f"请加限定词（内容/呈现/验收/执行）或写清边界")

    print("== docs-to-knowledge check ==")
    print(f"file        : {args.html}")
    print(f"pages       : {len(pages)} -> per-page chars {page_chars}")
    print(f"total cjk   : {total} (freshness {fresh_chars} exempt)")
    print(f"detail cards: {cards}")
    print(f"honest tags : {todos}")
    print(f"svg / table : {svgs} / {tables}")
    print(f"min font    : {min_font if min_font is not None else 'unknown'} pt")
    print()
    if args.map:
        check_map(args.map, errors, warnings)
        print()
    for w in warnings:
        print(f"[WARN] {w}")
    for e in errors:
        print(f"[FAIL] {e}")
    if errors:
        print("\nRESULT: FAIL")
        return 1
    print("\nRESULT: PASS" + (" (with warnings)" if warnings else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())

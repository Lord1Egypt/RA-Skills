#!/usr/bin/env python3
"""PDF 合并/拆分工具（v2.4.0，pymupdf 原生，零新依赖）。

用途闭环：--pages 分段翻译的产物分散 → merge 合并回单档；
超大 PDF 按页范围 split 后逐段翻译。
"""

from __future__ import annotations

import os
import re

import pymupdf


def merge_pdfs(paths, out_path: str) -> str:
    """按顺序合并多个 PDF 到 out_path。返回 out_path。"""
    paths = [os.path.realpath(p) for p in paths]
    for p in paths:
        if not os.path.isfile(p):
            raise FileNotFoundError(p)
    if len(paths) < 2:
        raise ValueError("merge 至少需要 2 个文件")
    out = pymupdf.open()
    for p in paths:
        src = pymupdf.open(p)
        out.insert_pdf(src)
        src.close()
    os.makedirs(os.path.dirname(os.path.realpath(out_path)) or ".", exist_ok=True)
    out.save(out_path, garbage=3, deflate=True)
    out.close()
    return out_path


def _parse_range(spec: str, page_count: int):
    """解析页范围表达式：'1-3,5,7-'（1-based，含端点，'7-' 到末尾）。"""
    pages = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, _, b = part.partition("-")
            start = int(a) if a.strip() else 1
            end = int(b) if b.strip() else page_count
        else:
            start = end = int(part)
        if start < 1 or end < start:
            raise ValueError("页范围无效：%s" % part)
        pages.extend(range(start, min(end, page_count) + 1))
    if not pages:
        raise ValueError("页范围为空")
    return pages


def split_pdf(pdf: str, outdir: str, spec: str) -> list:
    """按页范围表达式拆分 PDF。spec 例：'1-25,26-50'。返回产物路径列表。"""
    src_path = os.path.realpath(pdf)
    src = pymupdf.open(src_path)
    pages = _parse_range(spec, src.page_count)
    os.makedirs(outdir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(src_path))[0]
    # 每个逗号分隔范围独立成段（用户显式边界不合并——分段翻译产物需按段对应）
    total = src.page_count
    segments = []
    for part in [x.strip() for x in spec.split(",") if x.strip()]:
        if "-" in part:
            a, _, b = part.partition("-")
            start = int(a) if a.strip() else 1
            end = int(b) if b.strip() else total
        else:
            start = end = int(part)
        if start < 1 or end < start:
            raise ValueError("页范围无效：%s" % part)
        segments.append([start, min(end, total)])
    outs = []
    for a, b in segments:
        part = pymupdf.open()
        part.insert_pdf(src, from_page=a - 1, to_page=b - 1)
        out_path = os.path.join(outdir, "%s_p%d-%d.pdf" % (stem, a, b))
        part.save(out_path, garbage=3, deflate=True)
        part.close()
        outs.append(out_path)
    src.close()
    return outs


def estimate_pdf(pdf: str, chunk_pages: int = 25, threshold: int = 40,
                 qps: float = 4.0) -> dict:
    """干跑预估：不碰端点。返回页数/字符量/分段策略/预计时长。"""
    doc = pymupdf.open(pdf)
    page_count = doc.page_count
    total_chars = 0
    img_pages = 0
    for page in doc:
        total_chars += len(page.get_text())
        if len(page.get_images()) > 0:
            img_pages += 1
    doc.close()
    parts = (max(1, -(-page_count // chunk_pages))
             if chunk_pages > 0 and page_count >= threshold else 1)
    # 经验系数：qps=1 时每页约 30~60s（含版面解析）；取中值 45s/页
    est_seconds = int(page_count * 45 / max(qps / 4.0, 0.25))
    return {"path": pdf, "pages": page_count, "chars": total_chars,
            "image_pages": img_pages, "parts": parts, "chunk_pages": chunk_pages,
            "estimated_seconds": est_seconds,
            "estimated_minutes": round(est_seconds / 60, 1),
            "skip_glossary": page_count >= threshold}

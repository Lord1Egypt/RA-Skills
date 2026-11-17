#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PDF 矢量几何线段提取（仅 pdfminer，不依赖 pdf_inspector）。

只捞直线/矩形/曲线的折线段候选，坐标沿用 PDF 页坐标系；无图层语义，
仅供 cad_landscape_pdf 输出 review 证据候选，不参与闭合域/算量。
"""
from __future__ import annotations

from pathlib import Path


def extract_geometry_segments(pdf: Path, pages: list[int] | None = None) -> list[dict]:
    """从矢量 PDF 提取线/矩形/曲线候选线段（仅供 review 证据，不算量）。

    坐标用 pdfminer 的 PDF 页坐标系（水平 x、竖直 y，同一套可比较）。
    LTRect/LTLine/LTCurve 会被采样成 4 元组 [x1,y1,x2,y2]。
    """
    from pdfminer.high_level import extract_pages
    from pdfminer.layout import LTCurve, LTLine, LTRect

    wanted: set[int] | None = None
    if pages:
        wanted = {int(p) for p in pages if int(p) > 0}

    page_num = 0
    out: list[dict] = []
    for page in extract_pages(str(pdf)):
        page_num += 1
        if wanted is not None and page_num not in wanted:
            continue
        segs: list[list[float]] = []

        def add(x1: float, y1: float, x2: float, y2: float) -> None:
            try:
                x1, y1, x2, y2 = (float(v) for v in (x1, y1, x2, y2))
            except (TypeError, ValueError):
                return
            if abs(x1 - x2) < 1e-9 and abs(y1 - y2) < 1e-9:
                return
            segs.append([round(x1, 3), round(y1, 3), round(x2, 3), round(y2, 3)])

        def walk(obj) -> None:
            if isinstance(obj, LTLine):
                p1 = getattr(obj, "p1", None)
                p2 = getattr(obj, "p2", None)
                if p1 is not None and p2 is not None:
                    add(p1[0], p1[1], p2[0], p2[1])
                    return
                add(obj.x0, obj.y0, obj.x1, obj.y1)
            elif isinstance(obj, LTRect):
                x0, y0, x1, y1 = obj.x0, obj.y0, obj.x1, obj.y1
                add(x0, y0, x1, y0)
                add(x1, y0, x1, y1)
                add(x1, y1, x0, y1)
                add(x0, y1, x0, y0)
            elif isinstance(obj, LTCurve):
                pts = getattr(obj, "pts", None) or getattr(obj, "points", None) or []
                for i in range(len(pts) - 1):
                    a, b = pts[i], pts[i + 1]
                    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)) and len(a) >= 2 and len(b) >= 2:
                        add(a[0], a[1], b[0], b[1])
            children = getattr(obj, "_objs", None) or []
            for child in children:
                walk(child)

        for item in page:
            walk(item)
        if segs:
            out.append({"page": page_num, "segment_count": len(segs), "segments": segs})
    return out

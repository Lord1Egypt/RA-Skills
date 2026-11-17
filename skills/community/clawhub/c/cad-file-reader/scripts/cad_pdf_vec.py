#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""读取矢量 PDF 的原生文字坐标候选。

只从 PDF 原生字节中提取文字位置（x/y/width/height/font/page），不识别、
不渲染、不输出量、不转换 DXF。供 cad_pdf_ocr.py 在 source_format=pdf_vector
时补充 bbox 证据；最终契约仍为 final_quantity=false 的识图候选。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import pdf_inspector
except ImportError:
    # 由 pdf-inspector 技能的 .venv 运行时才可导入
    sys.stderr.write("pdf_inspector 未安装（需要 pdf-inspector 技能的 venv）\n")
    raise


def extract(pdf: Path, pages: list[int] | None = None) -> list[dict]:
    page_arg: list[int] | None = None
    if pages:
        page_arg = [int(p) for p in pages if p > 0]
    items = pdf_inspector.extract_text_with_positions(str(pdf), pages=page_arg)
    out: list[dict] = []
    for item in items or []:
        text = str(getattr(item, "text", "") or "").strip()
        if not text:
            continue
        out.append({
            "page": int(getattr(item, "page", 1) or 1),
            "text": text[:240],
            "x": round(float(getattr(item, "x", 0) or 0), 3),
            "y": round(float(getattr(item, "y", 0) or 0), 3),
            "width": round(float(getattr(item, "width", 0) or 0), 3),
            "height": round(float(getattr(item, "height", 0) or 0), 3),
            "font": getattr(item, "font", None),
            "font_size": round(float(getattr(item, "font_size", 0) or 0), 3) if getattr(item, "font_size", None) not in (None, "", 0) else None,
            "is_bold": bool(getattr(item, "is_bold", False)),
        })
    return out


def main() -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    ap = argparse.ArgumentParser(description="矢量 PDF 原生文字坐标提取")
    ap.add_argument("pdf", help="PDF 文件路径")
    ap.add_argument("--pages", default="", help="逗号分隔页号；省略则全部")
    ap.add_argument("--json", default="-", help="输出 JSON 路径，默认 stdout")
    args = ap.parse_args()
    pdf = Path(args.pdf)
    if not pdf.exists():
        print(json.dumps({"error": f"PDF 不存在: {pdf}"}, ensure_ascii=False), file=sys.stderr)
        return 1
    try:
        pages = [int(x) for x in args.pages.split(",") if x.strip().isdigit()] if args.pages else None
        items = extract(pdf, pages)
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"error": f"矢量文字坐标提取失败: {exc}"}, ensure_ascii=False), file=sys.stderr)
        return 1
    payload = {
        "schema": "cad-file-reader/pdf-vector-text-coords/v1",
        "source_file": str(pdf),
        "count": len(items),
        "items": items,
        "boundary": "只输出 PDF 原生文字坐标候选，final_quantity=false；坐标单位为 PDF 点，不参与测量。",
    }
    if args.json and args.json != "-":
        Path(args.json).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130)


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

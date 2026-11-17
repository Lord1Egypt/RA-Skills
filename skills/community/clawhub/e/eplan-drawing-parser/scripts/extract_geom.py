#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eplan-drawing-parser · 导线几何提取与拓扑重建 (core layer)

从 EPLAN 矢量 PDF 中提取：
  1. 所有导线(线段)的精确坐标
  2. 所有文字(型号/位号/数值)及其坐标
  3. 通过"导线端点 ↔ 元件端子坐标"匹配，重建元件连接拓扑
     (串/并联、电能流向、元件垂直层级)

权威基准: 文本与几何均来自 PDF 矢量对象, 机器直接读取, 无视觉识别误差。
"""
from __future__ import annotations
import argparse
import json
import math
import os
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print(json.dumps({"error": "PyMuPDF (fitz) not installed. Try: pip install pymupdf"}))
    sys.exit(1)


def extract_page_geometry(page):
    """提取单页的导线和文本。返回 (lines, texts)。"""
    # 导线: (x1,y1,x2,y2)
    lines = []
    for d in page.get_drawings():
        for item in d["items"]:
            if item[0] == "l":
                p1, p2 = item[1], item[2]
                lines.append((p1.x, p1.y, p2.x, p2.y))
    # 文本: {text, cx, cy, x0,y0,x1,y1}
    texts = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                t = s["text"].strip()
                if not t:
                    continue
                x0, y0, x1, y1 = s["bbox"]
                texts.append({
                    "text": t,
                    "cx": (x0 + x1) / 2,
                    "cy": (y0 + y1) / 2,
                    "x0": x0, "y0": y0, "x1": x1, "y1": y1,
                })
    return lines, texts


def count_wire_connections(texts, lines, radius=20):
    """统计每个文本元件附近(radius像素内)的导线端点数量。
    用于判断元件是否在电路中、主/辅助性质。"""
    result = []
    for c in texts:
        cx, cy = c["cx"], c["cy"]
        n = 0
        eps = set()
        for l in lines:
            for (ex, ey) in [(l[0], l[1]), (l[2], l[3])]:
                if abs(ex - cx) < radius and abs(ey - cy) < radius:
                    n += 1
                    eps.add((round(ex), round(ey)))
        c["_wires"] = n
        result.append(c)
    return result


def build_topology(texts, lines, radius=20):
    """重建元件间的连接关系：通过共享导线端点聚类。
    返回连接组(每个组 = 由同一根导线连在一起的元件簇)。"""
    # 建立 导线端点 -> 元件 的映射
    node_to_comps = {}
    for c in texts:
        cx, cy = c["cx"], c["cy"]
        for l in lines:
            for (ex, ey) in [(l[0], l[1]), (l[2], l[3])]:
                if abs(ex - cx) < radius and abs(ey - cy) < radius:
                    key = (round(ex), round(ey))
                    node_to_comps.setdefault(key, []).append(c["text"])
    return node_to_comps


def parse_pdf(path, page_filter=None):
    """解析整个 PDF，逐页提取。返回每页的 {lines, texts, topology}。"""
    doc = fitz.open(path)
    pages = []
    for i, page in enumerate(doc):
        lines, texts = extract_page_geometry(page)
        texts = count_wire_connections(texts, lines)
        topology = build_topology(texts, lines)
        pages.append({
            "page": i + 1,
            "num_wires": len(lines),
            "num_texts": len(texts),
            "texts": texts,
            "topology_nodes": len(topology),
        })
    return {"file": os.path.basename(path), "num_pages": len(doc), "pages": pages}


def summarize(texts):
    """提取疑似元件位号的文本(含 QF/FU/SPD/FCM/Q/S/K/TA/等前缀)。"""
    import re
    kw_prefix = re.compile(r"^[A-Za-z]{1,3}\d+")
    comps = [c for c in texts if kw_prefix.match(c["text"])]
    return comps


def main():
    ap = argparse.ArgumentParser(description="EPLAN向量PDF: 提取导线几何+文字+拓扑")
    ap.add_argument("--input", required=True, help="EPLAN导出的PDF文件")
    ap.add_argument("--output", default="-", help="输出JSON路径, - 打印到stdout")
    ap.add_argument("--full", action="store_true", help="输出完整texts(含全部文字坐标)")
    args = ap.parse_args()

    if not Path(args.input).exists():
        print(json.dumps({"error": f"file not found: {args.input}"}))
        sys.exit(1)

    result = parse_pdf(args.input)
    # 汇总每页疑似元件
    doc = fitz.open(args.input)
    for i, p in enumerate(result["pages"]):
        p["components"] = [c["text"] for c in summarize(p["texts"])][:200]
    doc.close()

    # 精简输出，默认只给关键信息
    if not args.full:
        for p in result["pages"]:
            p.pop("texts", None)
    out = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output == "-":
        print(out)
    else:
        Path(args.output).write_text(out, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

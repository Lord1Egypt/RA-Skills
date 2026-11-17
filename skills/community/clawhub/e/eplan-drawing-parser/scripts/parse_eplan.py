#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eplan-drawing-parser · 统一入口 (unified entry point)

一键解析 EPLAN/CAD 矢量 PDF 电气图纸，输出：
  1. parsed.json     结构化数据（元件清单 + 导线 + 拓扑）
  2. preview_<page>.png  关键页标注预览图（元件坐标框）
  3. 控制台汇总报告

用法示例:
  python scripts/parse_eplan.py --input drawing.pdf
  python scripts/parse_eplan.py --input drawing.pdf --pages 3,5 --preview
  python scripts/parse_eplan.py --input drawing.pdf --out-dir ./out --preview
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys
from pathlib import Path

import fitz  # PyMuPDF


# ---------- 元件位号识别 ----------
_DESIGNATOR_RE = re.compile(r"^([A-Za-z]{1,3})(\d+.*)$")

# EPLAN/GB 常用位号前缀 -> 元件类型
_KNOWN_TYPES = {
    "QF": "断路器", "Q": "断路器/开关", "FU": "熔断器", "F": "熔断器/保护",
    "SPD": "浪涌保护器", "KM": "接触器", "KA": "继电器", "K": "继电器/限位",
    "TA": "电流互感器", "X": "端子排", "H": "指示灯", "HL": "指示灯",
    "S": "按钮/开关", "SB": "按钮", "TC": "温控器", "FAN": "风扇",
    "CPU": "PLC-CPU", "HMI": "触摸屏", "IM": "接口模块", "ET": "I/O模块",
    "U": "电源模块", "V": "电源/UPS", "AGH": "绝缘监测", "CHA": "绝缘监测",
    "DCL": "直流负载", "T": "变压器", "PE": "接地",
}


def classify(text: str):
    """根据位号前缀推断元件类型。返回 (is_component, designator, comp_type)."""
    t = text.strip()
    # 去掉 EPLAN 常见位号前缀符号: -  \  / 空格 (如 "-QF1001"、"\QF1001")
    t = re.sub(r"^[-\\/\s.~]+", "", t)
    m = _DESIGNATOR_RE.match(t)
    if m:
        prefix, rest = m.group(1).upper(), m.group(2)
        if prefix in _KNOWN_TYPES and re.match(r"^\d", rest):
            return True, t, _KNOWN_TYPES[prefix]
    return False, t, "未知"


def extract_texts(page):
    """提取页内文本及其坐标。"""
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
                    "cx": (x0 + x1) / 2, "cy": (y0 + y1) / 2,
                    "x0": x0, "y0": y0, "x1": x1, "y1": y1,
                })
    return texts


def extract_wires(page):
    """提取页内导线(线段)坐标。"""
    lines = []
    for d in page.get_drawings():
        for item in d["items"]:
            if item[0] == "l":
                p1, p2 = item[1], item[2]
                lines.append((p1.x, p1.y, p2.x, p2.y))
    return lines


def count_wires(texts, lines, radius=20):
    """计算每个元件附近的导线端点数量。"""
    for c in texts:
        cx, cy = c["cx"], c["cy"]
        n = 0
        for l in lines:
            for (ex, ey) in [(l[0], l[1]), (l[2], l[3])]:
                if abs(ex - cx) < radius and abs(ey - cy) < radius:
                    n += 1
        c["wires"] = n
    return texts


def render_preview(page, texts, out_path, title=""):
    """在页面渲染图上叠加元件坐标框，输出标注预览PNG。"""
    mat = fitz.Matrix(2, 2)
    pix = page.get_pixmap(matrix=mat)
    tmp = out_path + ".tmp.png"
    pix.save(tmp)

    # 用 PILLOW 画框
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        os.replace(tmp, out_path)
        return out_path
    img = Image.open(tmp).convert("RGB")
    draw = ImageDraw.Draw(img)
    sc = 2.0  # 缩放系数
    for c in texts:
        if c.get("wires", 0) > 0:
            x0, y0, x1, y1 = (c["x0"]*sc, c["y0"]*sc, c["x1"]*sc, c["y1"]*sc)
            draw.rectangle([x0, y0, x1, y1], outline=(255, 0, 0), width=2)
    img.save(out_path)
    os.remove(tmp)
    return out_path


def run(input_path, pages=None, preview=False, out_dir="."):
    """主流程。"""
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    doc = fitz.open(input_path)
    base = Path(input_path).stem
    page_indexes = [int(p) - 1 for p in pages.split(",")] if pages else list(range(len(doc)))

    results = {"file": Path(input_path).name, "num_pages": len(doc), "pages": []}
    for i in page_indexes:
        if not (0 <= i < len(doc)):
            continue
        page = doc[i]
        texts = extract_texts(page)
        lines = extract_wires(page)
        texts = count_wires(texts, lines)

        components = []
        for c in texts:
            is_comp, d, ctype = classify(c["text"])
            if is_comp and c["wires"] > 0:
                components.append({
                    "designator": d, "type": ctype,
                    "page": i + 1, "wires": c["wires"],
                    "x": round(c["cx"]), "y": round(c["cy"]),
                })

        # 合并重复位号（同一位号可能有多段文本）
        seen = {}
        for comp in components:
            key = comp["designator"]
            if key in seen:
                seen[key]["wires"] = max(seen[key]["wires"], comp["wires"])
            else:
                seen[key] = comp

        page_result = {
            "page": i + 1,
            "num_wires": len(lines),
            "num_components": len(seen),
            "components": sorted(seen.values(), key=lambda c: c["designator"]),
        }
        if preview:
            png_path = os.path.join(out_dir, f"{base}_page{i+1}.png")
            page_result["preview"] = render_preview(page, texts, png_path)
        results["pages"].append(page_result)

    # 汇总
    total_wires = sum(p["num_wires"] for p in results["pages"])
    total_comps = sum(p["num_components"] for p in results["pages"])
    results["summary"] = {
        "pages_scanned": len(results["pages"]),
        "total_wires": total_wires,
        "total_components": total_comps,
    }
    doc.close()
    return results


def main():
    ap = argparse.ArgumentParser(description="Parse EPLAN vector PDF into components + topology")
    ap.add_argument("--input", required=True, help="EPLAN/CAD矢量PDF文件")
    ap.add_argument("--out-dir", default=".", help="输出目录")
    ap.add_argument("--pages", default=None, help="页码(1-based,逗号分隔), 默认全部")
    ap.add_argument("--preview", action="store_true", help="生成标注预览PNG")
    ap.add_argument("--json", default=None, help="指定JSON输出文件路径(默认 <out-dir>/<名>.json)")
    args = ap.parse_args()

    if not Path(args.input).exists():
        print(json.dumps({"error": f"文件不存在: {args.input}"}))
        sys.exit(1)

    results = run(args.input, args.pages, args.preview, args.out_dir)

    json_path = args.json or os.path.join(args.out_dir, Path(args.input).stem + ".json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # 控制台汇总
    s = results["summary"]
    print(f"✅ 解析完成: {results['file']}")
    print(f"   扫描页数: {s['pages_scanned']}, 导线总数: {s['total_wires']}, 元件总数(位号): {s['total_components']}")
    for p in results["pages"]:
        print(f"   页{p['page']}: {p['num_components']} 个位号, {p['num_wires']} 条导线")
    print(f"   输出JSON: {json_path}")
    if results["pages"] and "preview" in results["pages"][0]:
        print(f"   标注预览: 已生成")
    return 0


if __name__ == "__main__":
    sys.exit(main())

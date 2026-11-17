#!/usr/bin/env python3
"""分析DXF文件结构：实体统计、图层分布、桩相关图层识别。"""
import sys
import ezdxf
from collections import Counter

def analyze(dxf_path):
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()

    # 实体类型统计
    types = Counter(ent.dxftype() for ent in msp)
    print(f"文件: {dxf_path}")
    print(f"版本: {doc.dxfversion}")
    print(f"实体总数: {sum(types.values())}")

    print("\n=== 实体类型 ===")
    for t, c in types.most_common():
        print(f"  {t:20s} {c}")

    # 图层统计
    layer_types = {}
    for ent in msp:
        try:
            layer = ent.dxf.layer
        except Exception:
            continue
        key = (layer, ent.dxftype())
        layer_types[key] = layer_types.get(key, 0) + 1

    print("\n=== 图层分布（按实体数排序） ===")
    # 汇总每个图层的实体总数
    layer_total = {}
    for (layer, _), count in layer_types.items():
        layer_total[layer] = layer_total.get(layer, 0) + count
    for layer, total in sorted(layer_total.items(), key=lambda x: -x[1]):
        detail = layer_types.get((layer, 'INSERT'), 0)
        detail2 = layer_types.get((layer, 'TEXT'), 0)
        detail3 = layer_types.get((layer, 'LWPOLYLINE'), 0)
        detail4 = layer_types.get((layer, 'CIRCLE'), 0)
        detail5 = layer_types.get((layer, 'MTEXT'), 0)
        parts = []
        if detail: parts.append(f"INSERT×{detail}")
        if detail2: parts.append(f"TEXT×{detail2}")
        if detail3: parts.append(f"LWPOLYLINE×{detail3}")
        if detail4: parts.append(f"CIRCLE×{detail4}")
        if detail5: parts.append(f"MTEXT×{detail5}")
        rest = total - sum([detail, detail2, detail3, detail4, detail5])
        if rest: parts.append(f"OTHER×{rest}")
        print(f"  {layer:30s} {total:5d}  ({', '.join(parts)})")

    # 桩相关图层识别
    pile_keywords = ['桩', '编号', 'BASE', 'PILE', 'BH', 'ZM', '标签']
    contour_keywords = ['等高', 'Dgx', 'dgx', 'DGX']

    print("\n=== 疑似桩相关图层 ===")
    for layer in sorted(layer_total):
        if any(kw in layer for kw in pile_keywords):
            print(f"  {layer:30s} {layer_total[layer]:5d} entities")
            for (l, t), c in layer_types.items():
                if l == layer:
                    print(f"    -> {t}: {c}")

    print("\n=== 疑似等高线图层 ===")
    for layer in sorted(layer_total):
        if any(kw in layer for kw in contour_keywords):
            print(f"  {layer:30s} {layer_total[layer]:5d} entities")
            for (l, t), c in layer_types.items():
                if l == layer:
                    print(f"    -> {t}: {c}")

    # 标高TEXT扫描
    import re
    print("\n=== 标高文本采样（数值型TEXT） ===")
    samples = []
    for ent in msp:
        if ent.dxftype() != 'TEXT':
            continue
        t = ent.dxf.text.strip()
        if re.match(r'^-?\d+\.?\d*$', t):
            samples.append((float(t), ent.dxf.layer))
    if samples:
        print(f"  总数: {len(samples)}")
        bl = Counter(l for _, l in samples)
        for layer, c in bl.most_common():
            vals = sorted(set(v for v, l in samples if l == layer))
            print(f"  {layer}: {c}个, 范围 {min(vals)}~{max(vals)}, 值: {vals[:10]}{'...' if len(vals) > 10 else ''}")

    # 块定义
    if doc.blocks:
        print(f"\n=== 块定义: {len(doc.blocks)} 个 ===")
        for block in doc.blocks:
            entities = list(block)
            circle_count = sum(1 for e in entities if e.dxftype() == 'CIRCLE')
            if circle_count > 0:
                print(f"  {block.name:25s} CIRCLE×{circle_count} (含圆的块→可能是桩！)")
        # 列出所有块名
        all_blocks = [b.name for b in doc.blocks]
        if len(all_blocks) <= 20:
            print(f"  全部块名: {all_blocks}")
        else:
            print(f"  块名({len(all_blocks)}): {all_blocks[:10]}... (部分显示)")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python analyze_dxf.py <dxf文件路径>")
        sys.exit(1)
    analyze(sys.argv[1])

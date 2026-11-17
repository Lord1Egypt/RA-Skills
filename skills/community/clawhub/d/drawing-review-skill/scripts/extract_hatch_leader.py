#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
填充（HATCH）+ 引线（LEADER）全量提取 → JSON 数据包

用途：审图"材料分区 / 覆盖区域"类结论的必备数据（见 references/03-tech-path.md「两类图形数据」）
—— 只读文字看不见"哪个区域用哪种材料"，必须把填充与引线一起读出来。

用法：
    python extract_hatch_leader.py <图纸目录> [输出.json]
    默认输出：<图纸目录>/_hatch_leader_数据包.json

读取范围（缺一不可）：
  ① 所有块定义（含 $0$ 嵌套名——填充大量藏在"外部参照缓存块"内，只看主图会漏掉大部分）
  ② Model 空间  ③ 各 Paper 布局

JSON 结构：
  [ {"f": 相对路径,
     "h": [{"sp": 空间(以 B: 开头=块内), "pat": 图案名, "solid": 0/1, "lay": 图层,
            "n": 边界点数, "bb": [x0,y0,x1,y1] 或 null}],
     "ld": [{"sp": 空间, "v": [[x,y], ...]}] } ]
"""
import os
import sys
import json
import time

import ezdxf


def hatch_bbox(h):
    """兼容两种边界：polyline（有 vertices）与 edges（曲线段）→ 返回点列表"""
    pts = []
    for path in h.paths:
        try:
            if hasattr(path, 'vertices') and path.vertices:
                pts += [(round(v[0], 1), round(v[1], 1)) for v in path.vertices]
            else:
                for ed in getattr(path, 'edges', []):
                    for attr in ('start', 'end', 'start_point', 'end_point'):
                        pt = getattr(ed, attr, None)
                        if pt is not None:
                            try:
                                pts.append((round(pt[0], 1), round(pt[1], 1)))
                            except Exception:
                                pass
        except Exception:
            pass
    return pts


def scan_hatch(container, space_name):
    out = []
    for h in container.query('HATCH'):
        try:
            pts = hatch_bbox(h)
            bb = None
            if pts:
                xs = [x for x, _ in pts]
                ys = [y for _, y in pts]
                bb = [min(xs), min(ys), max(xs), max(ys)]
            out.append({
                "sp": space_name,
                "pat": getattr(h.dxf, 'pattern_name', '?'),
                "solid": int(getattr(h.dxf, 'solid_fill', 0)),
                "lay": h.dxf.layer,
                "n": len(pts),
                "bb": bb,
                "inv": int(h.dxf.get('invisible', 0) or 0),   # 组码 60=1 → 图上不显示，统计时先剔除
            })
        except Exception:
            pass
    return out


def scan_leader(container, space_name):
    out = []
    for ld in container.query('LEADER'):
        try:
            vs = [(round(v[0], 1), round(v[1], 1)) for v in ld.vertices]
            out.append({"sp": space_name, "v": vs[:40]})
        except Exception:
            pass
    return out


def extract(base):
    files = []
    for root, _, fs in os.walk(base):
        for fn in fs:
            if fn.lower().endswith('.dxf'):
                files.append(os.path.join(root, fn))
    files.sort()
    print(f"待扫 {len(files)} 份 DXF", flush=True)

    data, fail = [], []
    t0 = time.time()
    for i, p in enumerate(files):
        rel = os.path.relpath(p, base)
        try:
            doc = ezdxf.readfile(p)
        except Exception as e:
            fail.append((rel, str(e)[:60]))
            continue
        rec = {"f": rel, "h": [], "ld": []}

        for b in doc.blocks:                                   # ① 所有块定义
            if b.name == '*Model_Space' or b.name.startswith('*Paper_Space'):
                continue
            rec["h"] += scan_hatch(b, f"B:{b.name[:40]}")
        rec["h"] += scan_hatch(doc.modelspace(), "Model")      # ② Model
        for lay in doc.layouts:                                # ③ 各布局
            if lay.name.lower() == 'model':
                continue
            rec["h"] += scan_hatch(lay, f"L:{lay.name[:24]}")

        rec["ld"] += scan_leader(doc.modelspace(), "Model")
        for lay in doc.layouts:
            if lay.name.lower() == 'model':
                continue
            rec["ld"] += scan_leader(lay, f"L:{lay.name[:24]}")

        if rec["h"] or rec["ld"]:
            data.append(rec)
        if (i + 1) % 40 == 0:
            print(f"  ...{i+1}/{len(files)}  {time.time()-t0:.0f}s", flush=True)

    return data, fail, len(files)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    base = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(base, "_hatch_leader_数据包.json")
    data, fail, total = extract(base)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    n_h = sum(len(r['h']) for r in data)
    n_ld = sum(len(r['ld']) for r in data)
    print(f"\n完成：{len(data)}/{total} 文件有数据 | HATCH {n_h} | LEADER {n_ld} | 读取失败 {len(fail)}")
    for x in fail[:6]:
        print("  失败:", x)
    print(f"→ {out}")


if __name__ == '__main__':
    main()

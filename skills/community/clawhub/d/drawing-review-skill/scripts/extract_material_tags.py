#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
跨块拼装材料标注提取 → JSON 数据包

用途：读出图纸上的"材料标注"（如 CT-01 岩板、VT-01 地胶板）。
这类标注常为「外层块给数字（NUM2）＋ 内层块给字母族（NUM1）＋ 材质名（NUM6）」的
嵌套拼接结构——**只读顶层 TEXT / ATTRIB 必然为 0**（见 references/03-tech-path.md「三层深度」）。

⚠️ 关键规则（否则 1 条变 38 条）：每个标注点在块内**同时放着 38 条备选标签**
（WC/WD/ST/CT/VT… 各一条），其中 **37 条带"隐藏"标志（组码 60=1，图上不显示），
只有 1 条真正显示**。本脚本默认**只保留"可见"标签**（按父级级联可见性判断）。

用法：
    python extract_material_tags.py <图纸目录> [输出.json] [--all]
    默认输出：<图纸目录>/_材料标注_数据包.json
    --all：保留全部标签（含隐藏），每条带 "inv" 字段（0=可见 / 1=隐藏/父级隐藏）

JSON 结构：
  [ {"f": 相对路径,
     "tags": [{"sp": 空间, "ins": [x, y]（顶层插入点，近似位置）, "parent": 顶层块名,
               "block": 承载属性的嵌套块名, "inv": 0,
               "tags": {"NUM1": "CT", "NUM2": "01", "NUM6": "岩板", "NUM4": "SINTERED STONE"}}] } ]

说明：NUM1=字母族 / NUM2=数字 / NUM4=英文材质 / NUM6=中文材质名；
      拼装规则：NUM1 + "-" + NUM2 即完整编号（如 CT-01）。
"""
import os
import sys
import json
import time

import ezdxf

MAX_DEPTH = 4          # 嵌套展开深度上限
WANT_TAGS = ('NUM1', 'NUM2', 'NUM3', 'NUM4', 'NUM5', 'NUM6')


def dig(container, doc, depth, out, parent_visible=True, keep_all=False):
    """递归展开嵌套块，收集带 NUM* 属性的标注实例
    parent_visible：级联可见性——任一级带隐藏标志（组码 60=1），其后代在图上都不显示"""
    for e in container:
        try:
            if e.dxftype() != 'INSERT':
                continue
            inv = int(e.dxf.get('invisible', 0) or 0)
            visible = parent_visible and (inv == 0)
            nm = e.dxf.name
            atts = {a.dxf.tag: a.dxf.text for a in e.attribs}
            tags = {k: v for k, v in atts.items() if k in WANT_TAGS and v}
            if tags and (keep_all or visible):
                rec = {"block": nm[:48], "tags": tags}
                if keep_all:
                    rec["inv"] = 0 if visible else 1
                out.append(rec)
            blk = doc.blocks.get(nm)
            if blk is not None and depth < MAX_DEPTH:
                dig(blk, doc, depth + 1, out, visible, keep_all)
        except Exception:
            pass


def extract(base, keep_all=False):
    files = []
    for root, _, fs in os.walk(base):
        for fn in fs:
            if fn.lower().endswith('.dxf'):
                files.append(os.path.join(root, fn))
    files.sort()
    print(f"待扫 {len(files)} 份 DXF（{'全部标签' if keep_all else '仅可见标签'}）", flush=True)

    data, fail = [], []
    t0 = time.time()
    for i, p in enumerate(files):
        rel = os.path.relpath(p, base)
        try:
            doc = ezdxf.readfile(p)
        except Exception as e:
            fail.append((rel, str(e)[:60]))
            continue
        found = []

        def scan(container, space):
            for e in container:
                if e.dxftype() != 'INSERT':
                    continue
                try:
                    inv0 = int(e.dxf.get('invisible', 0) or 0)
                    blk = doc.blocks.get(e.dxf.name)
                    if blk is None:
                        continue
                    sub = []
                    dig(blk, doc, 1, sub, parent_visible=(inv0 == 0), keep_all=keep_all)
                    if sub:
                        try:
                            ins = [round(e.dxf.insert[0], 1), round(e.dxf.insert[1], 1)]
                        except Exception:
                            ins = None
                        for s in sub:
                            s["sp"] = space
                            s["ins"] = ins
                            s["parent"] = e.dxf.name[:40]
                        found.extend(sub)
                except Exception:
                    pass

        scan(doc.modelspace(), 'Model')
        for lay in doc.layouts:
            if lay.name.lower() == 'model':
                continue
            scan(lay, f"L:{lay.name[:24]}")

        if found:
            data.append({"f": rel, "tags": found})
        if (i + 1) % 40 == 0:
            print(f"  ...{i+1}/{len(files)}  {time.time()-t0:.0f}s", flush=True)

    return data, fail, len(files)


def main():
    args = [a for a in sys.argv[1:]]
    keep_all = '--all' in args
    args = [a for a in args if a != '--all']
    if not args:
        print(__doc__)
        sys.exit(1)
    base = args[0]
    out = args[1] if len(args) > 1 else os.path.join(base, "_材料标注_数据包.json")
    data, fail, total = extract(base, keep_all=keep_all)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    n = sum(len(r['tags']) for r in data)
    print(f"\n完成：{len(data)}/{total} 文件含标注实例 | 标注实例 {n} | 读取失败 {len(fail)}")
    for x in fail[:6]:
        print("  失败:", x)
    print(f"→ {out}")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 filter_topic.py 产出的 batches.json 拆成并行导入用的波次文件。

用法:
  python make_waves.py batches.json [waves_dir] [per_wave]

每波 per_wave 批(默认 13)，输出 waves/wave_1.json ... wave_N.json，
每个波次文件只保留 {"batch":N,"urls":[...]}，供子代理只读自己的波次并行导入。
"""
import json, sys, os

W = 13
inp = sys.argv[1] if len(sys.argv) > 1 else "batches.json"
outdir = sys.argv[2] if len(sys.argv) > 2 else "waves"
if len(sys.argv) > 3:
    W = int(sys.argv[3])

d = json.load(open(inp, encoding="utf-8"))
os.makedirs(outdir, exist_ok=True)
total = 0
idx = 0
for i in range(0, len(d), W):
    chunk = d[i:i + W]
    slim = [{"batch": b["batch"], "urls": b["urls"]} for b in chunk]
    fn = os.path.join(outdir, f"wave_{idx + 1}.json")
    json.dump(slim, open(fn, "w", encoding="utf-8"), ensure_ascii=False)
    total += sum(len(b["urls"]) for b in chunk)
    idx += 1
print(f"waves={idx} batches={len(d)} urls={total} -> {outdir}/")

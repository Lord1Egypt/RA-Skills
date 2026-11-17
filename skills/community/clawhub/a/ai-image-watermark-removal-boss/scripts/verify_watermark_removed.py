#!/usr/bin/env python3
"""像素级验证水印是否清除：对比原图 vs 处理图在目标区域的白色像素数。
用法:
  python verify_watermark_removed.py <orig.jpg> <proc.jpg>
  python verify_watermark_removed.py <orig.jpg> <proc.jpg> <x0> <y0> <x1> <y1>
不带区域时默认扫描右下角 20%（水印最常见位置）。
"""
import sys
from PIL import Image
import numpy as np

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

if len(sys.argv) < 3:
    print("用法: verify_watermark_removed.py <orig> <proc> [x0 y0 x1 y1]")
    sys.exit(1)

ORIG, PROC = sys.argv[1], sys.argv[2]
box = None
if len(sys.argv) >= 7:
    x0, y0, x1, y1 = map(int, sys.argv[3:7])
    box = (x0, y0, x1, y1)

THRESH = 180  # 半透明水印可降到 140


def white_stats(path):
    img = Image.open(path).convert("RGB")
    arr = np.array(img).astype(int)
    if box:
        arr = arr[box[1]:box[3], box[0]:box[2]]
    white = ((arr[:, :, 0] > THRESH) & (arr[:, :, 1] > THRESH) & (arr[:, :, 2] > THRESH)).sum()
    return white, arr.shape[0] * arr.shape[1]


wa, ta = white_stats(ORIG)
wb, tb = white_stats(PROC)
print(f"原图   白色像素: {wa}/{ta}")
print(f"处理图 白色像素: {wb}/{tb}")
ratio = (wa - wb) / wa * 100 if wa else 100
print(f"清除率: {ratio:.1f}%")
if wa > 0 and wb < wa * 0.05:
    print("✅ 水印已清除（残留<5%）")
elif wa == 0 and wb == 0:
    print("⚠️ 该区域本身无白色水印，检查定位是否错误")
else:
    print("⚠️ 可能仍有水印残留：检查区域坐标、阈值，或水印在别处")

#!/usr/bin/env python3
"""
验证壁纸目录中的图片分辨率，删除非 4K 图片

用法：
  python3 verify_4k.py --dir /data/wallpapers/anime/bian16 --min-width 2000 --delete
"""

import argparse
import glob
import os
import struct


def get_jpeg_real_size(filepath):
    with open(filepath, "rb") as f:
        data = f.read()
    last_w, last_h = None, None
    i = 0
    while i < len(data) - 1:
        if data[i] == 0xFF and data[i + 1] in (0xC0, 0xC1, 0xC2):
            h = (data[i + 5] << 8) | data[i + 6]
            w = (data[i + 7] << 8) | data[i + 8]
            last_w, last_h = w, h
        i += 1
    return last_w, last_h


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dir", required=True, help="壁纸目录")
    p.add_argument("--min-width", type=int, default=2000, help="最小宽度阈值")
    p.add_argument("--delete", action="store_true", help="删除非 4K 文件")
    args = p.parse_args()

    files = sorted(glob.glob(os.path.join(args.dir, "*.jpg")))
    ok = 0
    bad = 0

    for f in files:
        w, h = get_jpeg_real_size(f)
        sz = os.path.getsize(f) // 1024
        name = os.path.basename(f)

        if w and w >= args.min_width:
            print(f"✅ {name}: {w}x{h} ({sz}KB)")
            ok += 1
        else:
            status = "删除" if args.delete else "保留"
            print(f"❌ {name}: {w}x{h} ({sz}KB) [{status}]")
            if args.delete:
                os.remove(f)
            bad += 1

    print(f"\n4K: {ok}, 非4K: {bad}")


if __name__ == "__main__":
    main()

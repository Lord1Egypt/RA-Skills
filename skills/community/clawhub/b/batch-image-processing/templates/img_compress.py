#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量图片压缩工具 v2：全部用 Pillow 重压缩，输出JPG。
用法: python3 img_compress.py [--quality 65] [--threads 4] [--max-size 2000]
断点续传：已存在的输出文件会跳过。
"""
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image

SRC_DIR = "/opt/data/xiunice_images"
DST_DIR = "/data/software/xiunice_images"
IMG_EXT = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tiff")
DEFAULT_QUALITY = 65
WORKERS = 4
MAX_DIMENSION = 0  # 0=不缩放

def fmt_size(b):
    if b < 1024: return f"{b}B"
    if b < 1048576: return f"{b/1024:.1f}KB"
    return f"{b/1048576:.1f}MB"

def process_one(src_path, dst_path, quality, max_dim):
    src_size = os.path.getsize(src_path)
    if os.path.exists(dst_path) and os.path.getsize(dst_path) > 100:
        return src_size, os.path.getsize(dst_path), "skip"
    try:
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        img = Image.open(src_path)
        if hasattr(img, "n_frames") and img.n_frames > 1:
            img.seek(0)
        if img.mode in ("RGBA", "LA", "P"):
            bg = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P": img = img.convert("RGBA")
            if img.mode in ("RGBA", "LA"):
                bg.paste(img, mask=img.split()[-1])
            else:
                bg.paste(img)
            img = bg
        elif img.mode != "RGB":
            img = img.convert("RGB")
        if max_dim > 0 and max(img.size) > max_dim:
            img.thumbnail((max_dim, max_dim), Image.LANCZOS)
        img.save(dst_path, "JPEG", quality=quality, optimize=True)
        dst_size = os.path.getsize(dst_path)
        return src_size, dst_size, "ok"
    except Exception as e:
        return src_size, 0, f"fail:{e}"

def main():
    quality = DEFAULT_QUALITY
    workers = WORKERS
    max_dim = MAX_DIMENSION
    for i, arg in enumerate(sys.argv):
        if arg == "--quality" and i + 1 < len(sys.argv): quality = int(sys.argv[i + 1])
        if arg == "--threads" and i + 1 < len(sys.argv): workers = int(sys.argv[i + 1])
        if arg == "--max-size" and i + 1 < len(sys.argv): max_dim = int(sys.argv[i + 1])

    print(f"图片压缩工具 v2 | 质量: {quality} | 线程: {workers} | 最大尺寸: {max_dim or '不限'}")
    print("=" * 50)

    all_files = []
    for root, dirs, files in os.walk(SRC_DIR):
        for f in files:
            if f.lower().endswith(IMG_EXT):
                all_files.append(os.path.join(root, f))
    print(f"找到 {len(all_files)} 张图片")

    tasks = []
    for src_path in all_files:
        rel = os.path.relpath(src_path, SRC_DIR)
        base, _ = os.path.splitext(rel)
        dst_path = os.path.join(DST_DIR, base + ".jpg")
        tasks.append((src_path, dst_path))

    total_src = total_dst = 0
    ok = skip = fail = 0
    t0 = time.time()

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(process_one, s, d, quality, max_dim): (s, d) for s, d in tasks}
        for f in as_completed(futures):
            src_size, dst_size, status = f.result()
            if status == "ok": ok += 1; total_src += src_size; total_dst += dst_size
            elif status == "skip": skip += 1; total_src += src_size; total_dst += dst_size
            else: fail += 1
            done = ok + skip + fail
            if done % 2000 == 0 or done == len(tasks):
                elapsed = time.time() - t0
                ratio = total_dst / max(total_src, 1) * 100
                print(f"  [{done}/{len(tasks)}] {done/len(tasks)*100:.1f}% "
                      f"速度{done/max(elapsed,0.001):.0f}张/s 压缩率{ratio:.1f}% "
                      f"({fmt_size(total_src)}→{fmt_size(total_dst)})", flush=True)

    elapsed = time.time() - t0
    ratio = total_dst / max(total_src, 1) * 100
    print(f"\n{'='*50}")
    print(f"完成! 耗时{elapsed:.0f}s ({elapsed/60:.1f}分钟)")
    print(f"处理: {ok}张压缩 | {skip}张跳过 | {fail}张失败")
    print(f"体积: {fmt_size(total_src)} → {fmt_size(total_dst)} ({ratio:.1f}%)")
    print(f"节省: {fmt_size(total_src - total_dst)}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()

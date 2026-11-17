#!/usr/bin/env python3
"""批量图片压缩脚本（支持命令行参数）。
用法: python3 compress_generic.py --input /path/src --output /path/dst
部署: scp到宿主机后执行，支持断点续传（已存在且>0的文件自动跳过）
"""
import os, sys, time
from pathlib import Path
from PIL import Image

QUALITY = 50
SUPPORTED = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp', '.tiff'}


def main():
    input_dir = output_dir = None
    for i, arg in enumerate(sys.argv):
        if arg == "--input" and i + 1 < len(sys.argv): input_dir = sys.argv[i + 1]
        if arg == "--output" and i + 1 < len(sys.argv): output_dir = sys.argv[i + 1]
    if not input_dir or not output_dir:
        print("用法: python3 compress_generic.py --input /path/src --output /path/dst")
        sys.exit(1)

    input_path, output_path = Path(input_dir), Path(output_dir)
    images = [f for f in sorted(input_path.rglob("*")) if f.is_file() and f.suffix.lower() in SUPPORTED]
    total = len(images)
    print(f"压缩 {input_path.name}: {total}张 (quality={QUALITY})")

    start = time.time()
    success = fail = skip = 0
    orig_size = compressed_size = 0

    for i, img_file in enumerate(images):
        rel = img_file.relative_to(input_path)
        out_file = output_path / rel
        if not out_file.parent.exists():
            out_file.parent.mkdir(parents=True, exist_ok=True)
        if out_file.exists() and out_file.stat().st_size > 0:
            skip += 1
            continue
        try:
            orig_size += img_file.stat().st_size
            with Image.open(img_file) as im:
                if im.mode == "RGBA" and img_file.suffix.lower() in ('.jpg', '.jpeg'):
                    bg = Image.new("RGB", im.size, (255, 255, 255))
                    bg.paste(im, mask=im.split()[3])
                    im = bg
                elif im.mode not in ("RGB", "L"):
                    im = im.convert("RGB")
                im.save(out_file, format="JPEG", quality=QUALITY, optimize=True)
            compressed_size += out_file.stat().st_size
            success += 1
        except Exception as e:
            fail += 1
            if fail <= 5: print(f"  失败: {rel} - {e}")
        if (i + 1) % 200 == 0 or i + 1 == total:
            elapsed = time.time() - start
            speed = (i + 1) / elapsed if elapsed > 0 else 0
            print(f"  进度: {i+1}/{total} ({speed:.1f}张/s)", flush=True)

    elapsed = time.time() - start
    print(f"\n完成: 成功{success} 跳过{skip} 失败{fail} | 耗时{elapsed:.0f}s")
    if compressed_size > 0 and orig_size > 0:
        print(f"大小: {orig_size/1024/1024:.1f}MB → {compressed_size/1024/1024:.1f}MB ({compressed_size/orig_size*100:.1f}%)")

if __name__ == "__main__":
    main()

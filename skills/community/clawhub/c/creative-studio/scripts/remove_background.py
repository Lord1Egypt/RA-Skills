#!/usr/bin/env python3
"""Background removal for product photos using rembg.

Usage:
  python remove_background.py input.jpg -o ./output
  python remove_background.py *.jpg -o ./output --model isnet-general-use --alpha-matting
  python remove_background.py photo.png -o ./output --format webp

Requires: pip install rembg pillow
"""

import argparse
import io
import os
import sys
import time
from pathlib import Path

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

LANG = {
    "zh": {
        "checking": "正在检查依赖...",
        "missing_rembg": "rembg 未安装。请执行: pip install rembg",
        "missing_pillow": "Pillow 未安装。请执行: pip install Pillow",
        "processing": "处理中",
        "done": "完成",
        "error": "错误",
        "unsupported": "不支持的格式",
        "skipped": "跳过",
        "summary": "处理完毕",
        "total": "总计",
        "success": "成功",
        "failed": "失败",
        "elapsed": "总耗时",
    },
    "en": {
        "checking": "Checking dependencies...",
        "missing_rembg": "rembg not installed. Run: pip install rembg",
        "missing_pillow": "Pillow not installed. Run: pip install Pillow",
        "processing": "Processing",
        "done": "Done",
        "error": "Error",
        "unsupported": "Unsupported format",
        "skipped": "Skipped",
        "summary": "Summary",
        "total": "Total",
        "success": "Success",
        "failed": "Failed",
        "elapsed": "Total time",
    },
}

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif"}


def check_deps(msg):
    try:
        import rembg  # noqa: F401
    except ImportError:
        print(f"[✗] {msg['missing_rembg']}")
        sys.exit(1)
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        print(f"[✗] {msg['missing_pillow']}")
        sys.exit(1)


def remove_background(input_path, output_path, model="u2net", alpha_matting=False):
    from rembg import remove, new_session
    from PIL import Image

    img = Image.open(input_path).convert("RGBA")
    session = new_session(model)
    result = remove(img, session=session, alpha_matting=alpha_matting, alpha_matting_foreground_threshold=240, alpha_matting_background_threshold=10, alpha_matting_erode_size=10)
    result.save(output_path)


def main():
    parser = argparse.ArgumentParser(description="Remove background from product photos")
    parser.add_argument("inputs", nargs="+", help="Input image file(s)")
    parser.add_argument("--output-dir", "-o", required=True, help="Output directory")
    parser.add_argument("--model", default="u2net",
                        choices=["u2net", "u2net_human_seg", "isnet-general-use", "silueta"],
                        help="rembg model (default: u2net)")
    parser.add_argument("--alpha-matting", action="store_true",
                        help="Enable alpha matting for cleaner edges (slower)")
    parser.add_argument("--format", default="png", choices=["png", "webp", "jpg"],
                        help="Output format (default: png for transparency)")
    parser.add_argument("--lang", default="zh", choices=["zh", "en"])
    args = parser.parse_args()

    msg = LANG[args.lang]

    check_deps(msg)

    os.makedirs(args.output_dir, exist_ok=True)

    success = 0
    failed = 0
    start_time = time.time()

    for input_path in args.inputs:
        if not os.path.isfile(input_path):
            print(f"[{msg['error']}] {input_path} - {msg['error']}: file not found")
            failed += 1
            continue

        ext = Path(input_path).suffix.lower()
        if ext not in SUPPORTED_EXTENSIONS:
            print(f"[{msg['skipped']}] {input_path} - {msg['unsupported']}: {ext}")
            failed += 1
            continue

        stem = Path(input_path).stem
        output_path = os.path.join(args.output_dir, f"{stem}_nobg.{args.format}")

        try:
            t0 = time.time()
            print(f"[{msg['processing']}] {input_path} -> {output_path} ...", end=" ", flush=True)
            remove_background(input_path, output_path, args.model, args.alpha_matting)
            elapsed = time.time() - t0
            print(f"{msg['done']} ({elapsed:.1f}s)")
            success += 1
        except Exception as e:
            print(f"[{msg['error']}] {e}")
            failed += 1

    total_time = time.time() - start_time
    print(f"\n--- {msg['summary']} ---")
    print(f"  {msg['total']}: {len(args.inputs)}")
    print(f"  {msg['success']}: {success}")
    print(f"  {msg['failed']}: {failed}")
    print(f"  {msg['elapsed']}: {total_time:.1f}s")


if __name__ == "__main__":
    main()

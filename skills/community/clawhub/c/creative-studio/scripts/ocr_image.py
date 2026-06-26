#!/usr/bin/env python3
"""OCR text recognition for product images and nameplates.

Usage:
  python ocr_image.py nameplate.jpg -o ./output
  python ocr_image.py nameplate.jpg -o ./output --format json
  python ocr_image.py *.jpg -o ./output --engine easyocr

Requires: pip install easyocr pillow
Optional: pip install pytesseract (faster fallback for English-only)
"""

import argparse
import io
import json
import os
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

LANG = {
    "zh": {
        "missing_easyocr": "easyocr 未安装。请执行: pip install easyocr",
        "missing_pillow": "Pillow 未安装。请执行: pip install Pillow",
        "processing": "处理中",
        "done": "完成",
        "skipped": "跳过",
        "unsupported": "不支持的格式",
        "summary": "识别结果",
        "file": "文件",
        "text": "文字内容",
        "confidence": "置信度",
        "bbox": "位置",
    },
    "en": {
        "missing_easyocr": "easyocr not installed. Run: pip install easyocr",
        "missing_pillow": "Pillow not installed. Run: pip install Pillow",
        "processing": "Processing",
        "done": "Done",
        "skipped": "Skipped",
        "unsupported": "Unsupported format",
        "summary": "Recognition Results",
        "file": "File",
        "text": "Text",
        "confidence": "Confidence",
        "bbox": "Position",
    },
}

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif"}


def check_deps(msg):
    try:
        import easyocr  # noqa: F401
    except ImportError:
        print(f"[✗] {msg['missing_easyocr']}")
        sys.exit(1)
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        print(f"[✗] {msg['missing_pillow']}")
        sys.exit(1)


def ocr_image(input_path, reader):
    """Run OCR on a single image. Returns list of (bbox, text, confidence) tuples."""
    results = reader.readtext(input_path)
    return results


def main():
    parser = argparse.ArgumentParser(description="OCR text recognition for product images")
    parser.add_argument("inputs", nargs="+", help="Input image file(s)")
    parser.add_argument("--output-dir", "-o", required=True, help="Output directory")
    parser.add_argument("--engine", default="easyocr", choices=["easyocr", "tesseract"],
                        help="OCR engine (default: easyocr)")
    parser.add_argument("--format", default="txt", choices=["txt", "json", "csv"],
                        help="Output format (default: txt)")
    parser.add_argument("--lang", default="zh", choices=["zh", "en"])
    parser.add_argument("--languages", default="ch_sim,en",
                        help="OCR languages for easyocr, comma-separated (default: ch_sim,en)")
    args = parser.parse_args()

    msg = LANG[args.lang]

    check_deps(msg)

    import easyocr

    os.makedirs(args.output_dir, exist_ok=True)

    languages = [lang.strip() for lang in args.languages.split(",")]
    reader = easyocr.Reader(languages, gpu=False)

    all_results = []

    for input_path in args.inputs:
        if not os.path.isfile(input_path):
            print(f"[{msg['skipped']}] {input_path} - file not found")
            continue

        ext = Path(input_path).suffix.lower()
        if ext not in SUPPORTED_EXTENSIONS:
            print(f"[{msg['skipped']}] {input_path} - {msg['unsupported']}: {ext}")
            continue

        stem = Path(input_path).stem
        print(f"[{msg['processing']}] {input_path} ...", end=" ", flush=True)

        try:
            results = ocr_image(input_path, reader)
            print(msg["done"])

            file_result = {"file": input_path, "text_blocks": []}

            for bbox, text, conf in results:
                block = {
                    "text": text,
                    "confidence": round(float(conf), 3),
                    "bbox": [[int(p[0]), int(p[1])] for p in bbox],
                }
                file_result["text_blocks"].append(block)

            all_results.append(file_result)
        except Exception as e:
            print(f"Error: {e}")

    # Write output
    if args.format == "json":
        output_path = os.path.join(args.output_dir, "ocr_results.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)
        print(f"\n  JSON: {output_path}")

    elif args.format == "csv":
        output_path = os.path.join(args.output_dir, "ocr_results.csv")
        with open(output_path, "w", encoding="utf-8-sig") as f:
            f.write("file,text,confidence,x1,y1,x2,y2\n")
            for fr in all_results:
                for block in fr["text_blocks"]:
                    bbox = block["bbox"]
                    x1, y1 = bbox[0]
                    x2, y2 = bbox[2]
                    text = block["text"].replace('"', '""')
                    f.write(f'{fr["file"]},"{text}",{block["confidence"]},{x1},{y1},{x2},{y2}\n')
        print(f"\n  CSV: {output_path}")

    else:  # txt
        output_path = os.path.join(args.output_dir, "ocr_results.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            for fr in all_results:
                f.write(f"=== {fr['file']} ===\n")
                for block in fr["text_blocks"]:
                    f.write(f"  [{block['confidence']:.2f}] {block['text']}\n")
                f.write("\n")
        print(f"\n  TXT: {output_path}")

    total_blocks = sum(len(fr["text_blocks"]) for fr in all_results)
    print(f"  {msg['summary']}: {len(all_results)} files, {total_blocks} text blocks")


if __name__ == "__main__":
    main()

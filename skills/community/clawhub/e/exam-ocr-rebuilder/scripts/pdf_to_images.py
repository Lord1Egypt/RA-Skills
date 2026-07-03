#!/usr/bin/env python3
"""
exam-ocr-rebuilder 辅助脚本：PDF转图片
用途：将PDF文件逐页转换为高清PNG图片，供后续OCR识别使用

依赖：PyMuPDF (fitz)
安装：pip install PyMuPDF -i https://pypi.tuna.tsinghua.edu.cn/simple/

用法：
    python pdf_to_images.py --input 试卷.pdf --output_dir temp_pages --dpi 300
    python pdf_to_images.py --input 试卷.pdf --output_dir temp_pages --dpi 300 --pages 1-5
"""

import argparse
import os
import sys
import base64
import json


def convert_pdf_to_images(pdf_path, output_dir, dpi=300, page_range=None):
    """将PDF逐页转换为PNG图片

    Args:
        pdf_path: PDF文件路径
        output_dir: 输出目录
        dpi: 图片DPI（默认300）
        page_range: 页码范围，如 "1-5" 或 "1,3,5"

    Returns:
        list: 生成的图片路径列表
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("ERROR: PyMuPDF not installed. Run: pip install PyMuPDF", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(pdf_path):
        print(f"ERROR: PDF file not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    print(f"PDF loaded: {pdf_path}")
    print(f"Total pages: {total_pages}")

    # 解析页码范围
    pages_to_convert = list(range(total_pages))
    if page_range:
        pages_to_convert = parse_page_range(page_range, total_pages)

    # 计算缩放矩阵
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)

    image_paths = []
    for page_num in pages_to_convert:
        page = doc[page_num]
        pix = page.get_pixmap(matrix=mat)

        filename = f"page_{page_num + 1:03d}.png"
        filepath = os.path.join(output_dir, filename)
        pix.save(filepath)

        image_paths.append(filepath)
        print(f"  Converted page {page_num + 1}/{total_pages} -> {filename} ({pix.width}x{pix.height})")

    doc.close()
    print(f"\nDone! {len(image_paths)} pages converted to {output_dir}/")

    # 输出JSON格式的结果（供程序化调用）
    result = {
        "pdf_path": pdf_path,
        "total_pages": total_pages,
        "converted_pages": len(image_paths),
        "dpi": dpi,
        "images": image_paths
    }
    result_path = os.path.join(output_dir, "conversion_result.json")
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Result saved to: {result_path}")

    return image_paths


def image_to_base64(image_path):
    """将图片文件转为base64编码（供OCR API使用）

    Args:
        image_path: 图片文件路径

    Returns:
        str: base64编码字符串
    """
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def parse_page_range(range_str, total_pages):
    """解析页码范围字符串

    支持格式：
        "1-5"     -> [0, 1, 2, 3, 4]
        "1,3,5"   -> [0, 2, 4]
        "1-3,5,7" -> [0, 1, 2, 4, 6]
    """
    pages = []
    parts = range_str.split(",")
    for part in parts:
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            start = int(start)
            end = int(end)
            pages.extend(range(start - 1, end))
        else:
            pages.append(int(part) - 1)

    # 验证页码范围
    valid_pages = [p for p in pages if 0 <= p < total_pages]
    return sorted(set(valid_pages))


def extract_text_from_pdf(pdf_path):
    """直接从PDF提取文本（适用于文本型PDF，非扫描版）

    Args:
        pdf_path: PDF文件路径

    Returns:
        str: 提取的文本内容
    """
    try:
        import fitz
    except ImportError:
        print("ERROR: PyMuPDF not installed.", file=sys.stderr)
        return ""

    doc = fitz.open(pdf_path)
    text_parts = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        if text.strip():
            text_parts.append(f"--- Page {page_num + 1} ---\n{text}")

    doc.close()
    return "\n\n".join(text_parts)


def check_pdf_type(pdf_path):
    """检测PDF类型：文本型还是扫描型

    Returns:
        dict: {"type": "text"|"scanned"|"mixed", "text_ratio": float}
    """
    try:
        import fitz
    except ImportError:
        return {"type": "unknown", "text_ratio": 0.0}

    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    text_pages = 0
    total_text_len = 0

    for page_num in range(min(total_pages, 5)):  # 检查前5页
        page = doc[page_num]
        text = page.get_text()
        if len(text.strip()) > 50:  # 有意义的文本
            text_pages += 1
            total_text_len += len(text)

    doc.close()

    text_ratio = text_pages / min(total_pages, 5) if total_pages > 0 else 0

    if text_ratio > 0.8:
        pdf_type = "text"
    elif text_ratio < 0.2:
        pdf_type = "scanned"
    else:
        pdf_type = "mixed"

    return {
        "type": pdf_type,
        "text_ratio": round(text_ratio, 2),
        "total_pages": total_pages,
        "avg_text_len": total_text_len // max(text_pages, 1)
    }


def main():
    parser = argparse.ArgumentParser(
        description="PDF to images converter for exam OCR rebuilder"
    )
    parser.add_argument(
        "--input", "-i", required=True,
        help="Input PDF file path"
    )
    parser.add_argument(
        "--output_dir", "-o", default="temp_pages",
        help="Output directory for images (default: temp_pages)"
    )
    parser.add_argument(
        "--dpi", type=int, default=300,
        help="Image DPI (default: 300, recommended: 300-400)"
    )
    parser.add_argument(
        "--pages", "-p", default=None,
        help='Page range, e.g. "1-5" or "1,3,5" (default: all pages)'
    )
    parser.add_argument(
        "--check", action="store_true",
        help="Only check PDF type (text vs scanned), do not convert"
    )
    parser.add_argument(
        "--extract_text", action="store_true",
        help="Extract text directly (for text PDFs only)"
    )

    args = parser.parse_args()

    if args.check:
        info = check_pdf_type(args.input)
        print(json.dumps(info, indent=2, ensure_ascii=False))
        if info["type"] == "text":
            print("\nThis is a text PDF. You can use --extract_text for direct text extraction.")
            print("No need for OCR conversion.")
        elif info["type"] == "scanned":
            print("\nThis is a scanned PDF. OCR conversion is required.")
            print("Run without --check to convert to images.")
        else:
            print("\nThis is a mixed PDF. Some pages have text, some are scanned.")
            print("Recommend: convert all pages to images for consistent OCR processing.")
        return

    if args.extract_text:
        text = extract_text_from_pdf(args.input)
        if text:
            output_file = os.path.join(args.output_dir, "extracted_text.txt")
            os.makedirs(args.output_dir, exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"Text extracted to: {output_file}")
            print(f"Total characters: {len(text)}")
        else:
            print("No text could be extracted. This may be a scanned PDF.")
            print("Run without --extract_text to convert to images for OCR.")
        return

    # 默认：PDF转图片
    convert_pdf_to_images(args.input, args.output_dir, args.dpi, args.pages)


if __name__ == "__main__":
    main()

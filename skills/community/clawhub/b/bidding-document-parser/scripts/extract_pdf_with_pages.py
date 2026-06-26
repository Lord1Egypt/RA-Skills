#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提取PDF文本并标注页码（通用版）
用法：
    py scripts/extract_pdf_with_pages.py "input.pdf"
    py scripts/extract_pdf_with_pages.py "input.pdf" "output.txt"

输出文件默认保存为：<PDF文件名>_带页码.txt，放在 PDF 文件同级目录下。
"""

import sys
import os

try:
    import pdfplumber
except ImportError:
    print("错误：未安装 pdfplumber 库")
    print("请运行：pip install pdfplumber")
    sys.exit(1)


def extract_pdf(input_pdf: str, output_txt: str = None) -> str:
    """
    提取PDF文本并标注页码。

    Args:
        input_pdf:  PDF文件路径
        output_txt: 输出TXT文件路径（可选，默认与PDF同目录）

    Returns:
        输出文件路径
    """
    if not os.path.exists(input_pdf):
        print(f"错误：文件不存在 - {input_pdf}")
        sys.exit(1)

    if output_txt is None:
        base = os.path.splitext(input_pdf)[0]
        output_txt = base + "_带页码.txt"

    print(f"[INFO] 正在提取：{input_pdf}")

    with pdfplumber.open(input_pdf) as pdf:
        total_pages = len(pdf.pages)
        with open(output_txt, "w", encoding="utf-8") as f:
            for i, page in enumerate(pdf.pages):
                # 写入页码标记
                f.write(f"\n=== 第{i + 1}页 ===\n\n")

                # 提取正文文本
                text = page.extract_text()
                if text:
                    f.write(text)
                    f.write("\n")

                # 提取表格内容
                tables = page.extract_tables()
                if tables:
                    f.write("\n[表格内容]\n")
                    for table in tables:
                        for row in table:
                            f.write(" | ".join([str(cell) if cell else "" for cell in row]) + "\n")
                    f.write("\n")

    print(f"[INFO] 提取完成！共 {total_pages} 页")
    print(f"[INFO] 输出文件：{output_txt}")
    return output_txt


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：py scripts/extract_pdf_with_pages.py <PDF文件路径> [输出TXT文件路径]")
        print()
        print("示例：")
        print("  py scripts/extract_pdf_with_pages.py 招标文件.pdf")
        print("  py scripts/extract_pdf_with_pages.py 招标文件.pdf output/招标_带页码.txt")
        sys.exit(1)

    input_pdf = sys.argv[1]
    output_txt = sys.argv[2] if len(sys.argv) > 2 else None
    extract_pdf(input_pdf, output_txt)

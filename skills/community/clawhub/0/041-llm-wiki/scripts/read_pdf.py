#!/usr/bin/env python3
"""读取 PDF 文件内容的辅助脚本（基于 PyMuPDF）"""

import sys
import io


def read_pdf(pdf_path, pages=None):
    """读取 PDF 文件内容

    Args:
        pdf_path: PDF 文件路径
        pages: 要读取的页码范围，如 "1-10"，None 表示全部
    """
    # 强制 UTF-8 输出，绕开控制台编码问题
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    try:
        import fitz  # PyMuPDF
    except ImportError as e:
        print("错误：PyMuPDF 未安装。请运行：pip install pymupdf")
        sys.exit(1)

    doc = fitz.open(pdf_path)

    if pages:
        # 解析页码范围
        if '-' in pages:
            start, end = map(int, pages.split('-'))
            page_nums = range(start - 1, end)  # 转为 0-indexed
        else:
            page_nums = [int(pages) - 1]

        for i in page_nums:
            if i < len(doc):
                page = doc.load_page(i)
                text = page.get_text()
                print(f"\n{'='*60}")
                print(f"Page {i + 1}")
                print(f"{'='*60}")
                print(text)
    else:
        # 读取全部页面
        for i, page in enumerate(doc):
            text = page.get_text()
            print(f"\n{'='*60}")
            print(f"Page {i + 1}")
            print(f"{'='*60}")
            print(text)

    doc.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python read_pdf.py <pdf_path> [pages]")
        print("Example: python read_pdf.py document.pdf 1-10")
        sys.exit(1)

    pdf_path = sys.argv[1]
    pages = sys.argv[2] if len(sys.argv) > 2 else None

    read_pdf(pdf_path, pages)

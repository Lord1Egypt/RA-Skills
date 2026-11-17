#!/usr/bin/env python3
"""读取 PDF 文件内容的辅助脚本（基于 PyMuPDF）。

支持两种模式：

1. 默认：提取文本内容。
2. ``--extract-images``：提取内嵌位图和矢量图表，保存为图片文件。
"""

import argparse
import io
import sys
from pathlib import Path

# Ensure project root is in path so ``from llm_wiki`` works when the script is
# executed directly.
_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))
if str(_PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT / "src"))


def read_pdf(pdf_path: str, pages: str | None = None) -> None:
    """读取 PDF 文件内容。

    Args:
        pdf_path: PDF 文件路径。
        pages: 要读取的页码范围，如 ``"1-10"``，``None`` 表示全部。
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("错误：PyMuPDF 未安装。请运行：pip install pymupdf")
        sys.exit(1)

    from llm_wiki.pdf_images import parse_pages

    with fitz.open(pdf_path) as doc:
        for i in parse_pages(doc, pages):
            page = doc.load_page(i)
            text = page.get_text()
            print(f"\n{'=' * 60}")
            print(f"Page {i + 1}")
            print(f"{'=' * 60}")
            print(text)


def extract_images(
    pdf_path: str,
    output_dir: str,
    pages: str | None = None,
    dpi: int = 200,
) -> None:
    """提取 PDF 中的图片和矢量图表。

    Args:
        pdf_path: PDF 文件路径。
        output_dir: 图片输出目录。
        pages: 要处理的页码范围，如 ``"1-10"``。
        dpi: 矢量图表渲染分辨率。
    """
    from llm_wiki.pdf_images import extract_pdf_images

    result = extract_pdf_images(pdf_path, output_dir, pages=pages, dpi=dpi)
    print(f"已提取 {len(result['images'])} 张内嵌位图。")
    print(f"已提取 {len(result['figures'])} 个矢量图表。")
    for img in result["images"]:
        print(f"  第 {img['page']} 页 位图 {img['index']}: {img['path']}")
    for fig in result["figures"]:
        print(f"  第 {fig['page']} 页 图表 {fig['index']}: {fig['path']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="读取 PDF 文件内容")
    parser.add_argument("pdf_path", help="PDF 文件路径")
    parser.add_argument(
        "pages",
        nargs="?",
        help="要读取的页码范围，如 1-10",
    )
    parser.add_argument(
        "--extract-images",
        action="store_true",
        help="提取 PDF 中的图片和矢量图表",
    )
    parser.add_argument(
        "--image-dir",
        default="extracted_pdf_images",
        help="图片输出目录（默认：extracted_pdf_images）",
    )
    parser.add_argument(
        "--image-dpi",
        type=int,
        default=200,
        help="矢量图表渲染分辨率（默认：200）",
    )
    args = parser.parse_args()

    # 强制 UTF-8 输出，绕开控制台编码问题
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    if args.extract_images:
        extract_images(args.pdf_path, args.image_dir, args.pages, args.image_dpi)
    else:
        read_pdf(args.pdf_path, args.pages)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
PDF 合并脚本
用法: python merge_pdfs.py <output.pdf> <file1.pdf> <file2.pdf> ...
"""
import sys
import argparse
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF not installed. Run: pip install pymupdf")
    sys.exit(1)


def merge_pdfs(output_path: str, *pdf_files) -> bool:
    """合并多个 PDF 文件"""
    if not pdf_files:
        print("Error: 请提供至少一个 PDF 文件")
        return False
    
    # 创建输出 PDF
    output_doc = fitz.open()
    
    for pdf_path in pdf_files:
        try:
            doc = fitz.open(pdf_path)
            output_doc.insert_pdf(doc)
            doc.close()
            print(f"已合并: {Path(pdf_path).name}")
        except Exception as e:
            print(f"Warning: 无法合并 {pdf_path}: {e}")
    
    # 保存
    output_doc.save(output_path)
    output_doc.close()
    
    print(f"\n合并完成: {output_path}")
    print(f"总页数: {fitz.open(output_path).page_count}")
    return True


def main():
    parser = argparse.ArgumentParser(description='合并 PDF 文件')
    parser.add_argument('output', help='输出 PDF 文件路径')
    parser.add_argument('files', nargs='+', help='要合并的 PDF 文件列表')
    
    args = parser.parse_args()
    
    try:
        merge_pdfs(args.output, *args.files)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
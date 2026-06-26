#!/usr/bin/env python3
"""
PDF 拆分脚本
用法: python split_pdf.py <pdf_path> <output_dir> [--pages <page_ranges>]
示例: python split_pdf.py input.pdf outputdir --pages 1-3,5,7-10
"""
import sys
import argparse
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF not installed. Run: pip install pymupdf")
    sys.exit(1)


def parse_page_ranges(page_str: str, max_pages: int) -> list:
    """解析页码范围，如 '1-3,5,7-10' -> [0,1,2,4,6,7,8,9]"""
    pages = []
    parts = page_str.split(',')
    
    for part in parts:
        part = part.strip()
        if '-' in part:
            start, end = part.split('-')
            pages.extend(range(int(start) - 1, int(end)))
        else:
            pages.append(int(part) - 1)
    
    # 过滤无效页码
    return [p for p in pages if 0 <= p < max_pages]


def split_pdf(pdf_path: str, output_dir: str, page_ranges: str = None) -> list:
    """拆分 PDF 文件"""
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    base_name = Path(pdf_path).stem
    split_files = []
    
    if page_ranges:
        # 按指定范围拆分
        page_indices = parse_page_ranges(page_ranges, total_pages)
        
        new_doc = fitz.open()
        for idx in page_indices:
            new_doc.insert_pdf(doc, from_page=idx, to_page=idx)
        
        output_file = output_path / f"{base_name}_selected.pdf"
        new_doc.save(output_file)
        new_doc.close()
        
        split_files.append(str(output_file))
        print(f"已保存选中页面: {output_file.name} ({len(page_indices)}页)")
    else:
        # 每页单独拆分为一个文件
        for page_num in range(total_pages):
            new_doc = fitz.open()
            new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
            
            output_file = output_path / f"{base_name}_page{page_num + 1}.pdf"
            new_doc.save(output_file)
            new_doc.close()
            
            split_files.append(str(output_file))
            print(f"已拆分: 第{page_num + 1}页 -> {output_file.name}")
    
    doc.close()
    
    print(f"\n拆分完成! 共 {len(split_files)} 个文件")
    return split_files


def main():
    parser = argparse.ArgumentParser(description='拆分 PDF 文件')
    parser.add_argument('pdf_path', help='输入 PDF 文件路径')
    parser.add_argument('output_dir', help='输出目录')
    parser.add_argument('--pages', '-p', help='要提取的页码范围，如 1-3,5,7-10')
    
    args = parser.parse_args()
    
    try:
        split_pdf(args.pdf_path, args.output_dir, args.pages)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
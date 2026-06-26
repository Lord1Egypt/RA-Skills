#!/usr/bin/env python3
"""
PDF 文本提取脚本
用法: python extract_text.py <pdf_path> [--output <output.txt>] [--metadata]
"""
import sys
import argparse
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF not installed. Run: pip install pymupdf")
    sys.exit(1)


def extract_text(pdf_path: str, output_path: str = None, include_metadata: bool = False) -> str:
    """提取 PDF 文本内容"""
    doc = fitz.open(pdf_path)
    
    text_content = []
    metadata_info = {}
    
    # 提取元数据
    if include_metadata:
        metadata = doc.metadata
        metadata_info = {
            'title': metadata.get('title', ''),
            'author': metadata.get('author', ''),
            'subject': metadata.get('subject', ''),
            'creator': metadata.get('creator', ''),
            'producer': metadata.get('producer', ''),
            'creation_date': metadata.get('creationDate', ''),
            'mod_date': metadata.get('modDate', ''),
            'page_count': len(doc),
        }
    
    # 提取每页文本
    for page_num, page in enumerate(doc, 1):
        text = page.get_text()
        if text.strip():
            text_content.append(f"--- 第 {page_num} 页 ---\n{text}")
    
    doc.close()
    
    result = ""
    if metadata_info:
        result += "=== PDF 元数据 ===\n"
        for key, value in metadata_info.items():
            if value:
                result += f"{key}: {value}\n"
        result += "\n"
    
    result += "\n\n".join(text_content)
    
    # 保存到文件或返回
    if output_path:
        Path(output_path).write_text(result, encoding='utf-8')
        print(f"文本已保存到: {output_path}")
    
    return result


def main():
    parser = argparse.ArgumentParser(description='提取 PDF 文本内容')
    parser.add_argument('pdf_path', help='PDF 文件路径')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--metadata', '-m', action='store_true', help='包含元数据')
    
    args = parser.parse_args()
    
    try:
        text = extract_text(args.pdf_path, args.output, args.metadata)
        
        if not args.output:
            print(text)
        
        print(f"\n提取完成! 总字符数: {len(text)}")
        
    except FileNotFoundError:
        print(f"Error: 文件不存在 - {args.pdf_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

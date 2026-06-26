#!/usr/bin/env python3
"""
书籍内容提取脚本
支持 PDF, TXT, EPUB, MOBI, DOCX, MD 格式
"""

import os
import sys

def extract_text_from_pdf(file_path):
    """从PDF提取文本"""
    try:
        import PyPDF2
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
    except ImportError:
        return "请安装 PyPDF2: pip install PyPDF2"

def extract_text_from_txt(file_path):
    """从TXT提取文本"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_text_from_epub(file_path):
    """从EPUB提取文本"""
    try:
        import ebooklib
        from ebooklib import epub
        book = epub.read_epub(file_path)
        text = ""
        for item in book.get_items():
            if item.get_type() == 9:  # DOCUMENT
                text += item.get_content().decode('utf-8') + "\n"
        return text
    except ImportError:
        return "请安装 ebooklib: pip install ebooklib"

def extract_text_from_mobi(file_path):
    """从MOBI提取文本"""
    try:
        import mobi
        from pathlib import Path
        output_path = Path(file_path).with_suffix('.html')
        mobi.extract(file_path, output_path)
        with open(output_path, 'r', encoding='utf-8') as f:
            text = f.read()
        # 清理临时文件
        output_path.unlink(missing_ok=True)
        return text
    except ImportError:
        return "请安装 mobi: pip install mobi"

def extract_text_from_docx(file_path):
    """从DOCX提取文本"""
    try:
        import docx
        doc = docx.Document(file_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except ImportError:
        return "请安装 python-docx: pip install python-docx"

def extract_text_from_markdown(file_path):
    """从Markdown提取文本"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_book_content(file_path):
    """根据文件格式自动提取文本"""
    ext = os.path.splitext(file_path)[1].lower()

    extractors = {
        '.pdf': extract_text_from_pdf,
        '.txt': extract_text_from_txt,
        '.epub': extract_text_from_epub,
        '.mobi': extract_text_from_mobi,
        '.docx': extract_text_from_docx,
        '.md': extract_text_from_markdown,
    }

    if ext not in extractors:
        raise ValueError(f"不支持的文件格式: {ext}")

    return extractors[ext](file_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python book_extractor.py <文件路径>")
        sys.exit(1)

    file_path = sys.argv[1]
    content = extract_book_content(file_path)
    print(content[:10000])  # 打印前10000字符作为预览

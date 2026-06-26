# -*- coding: utf-8 -*-
"""
书库扫描脚本
扫描指定目录，提取电子书元数据，生成索引文件
"""

import os
import json
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime

def extract_epub_metadata(filepath):
    """提取EPUB文件元数据"""
    try:
        with zipfile.ZipFile(filepath, 'r') as zf:
            # 查找OPF文件
            opf_file = None
            for name in zf.namelist():
                if name.endswith('.opf'):
                    opf_file = name
                    break
            
            if not opf_file:
                return None
            
            with zf.open(opf_file) as f:
                content = f.read().decode('utf-8', errors='ignore')
                root = ET.fromstring(content)
                
                # 命名空间
                ns = {'dc': 'http://purl.org/dc/elements/1.1/'}
                
                title = root.find('.//dc:title', ns)
                author = root.find('.//dc:creator', ns)
                desc = root.find('.//dc:description', ns)
                
                return {
                    'title': title.text if title is not None else None,
                    'author': author.text if author is not None else None,
                    'description': desc.text if desc is not None else None
                }
    except Exception as e:
        return None

def extract_pdf_metadata(filepath):
    """提取PDF文件元数据"""
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(filepath)
        meta = doc.metadata
        return {
            'title': meta.get('title') or meta.get('Title'),
            'author': meta.get('author') or meta.get('Author'),
            'description': meta.get('subject') or meta.get('Subject')
        }
    except:
        return None

def classify_book(title, author):
    """根据书名和作者分类"""
    category = '其他'
    country = '未知'
    
    # 国家标注检测
    country_marks = {
        '(美)': '美国', '(美国)': '美国', '美)': '美国',
        '(英)': '英国', '(英国)': '英国',
        '(德)': '德国', '(德国)': '德国',
        '(法)': '法国', '(法国)': '法国',
        '(日)': '日本', '(日本)': '日本',
        '(俄)': '俄罗斯', '(俄罗斯)': '俄罗斯',
        '(中)': '中国', '(中国)': '中国'
    }
    
    text = f"{title} {author}"
    for mark, cn in country_marks.items():
        if mark in text:
            country = cn
            break
    
    # 分类检测
    if any(kw in text for kw in ['小说', '文学', '诗歌', '散文', '诗', '作品集']):
        category = '文学'
    elif any(kw in text for kw in ['历史', '史', '近代史', '现代史', '古代史']):
        category = '历史'
    elif any(kw in text for kw in ['心理', '精神', '心智']):
        category = '心理学'
    elif any(kw in text for kw in ['哲学', '思想', '伦理']):
        category = '哲学'
    elif any(kw in text for kw in ['经济', '金融', '投资', '商业', '管理']):
        category = '经济'
    elif any(kw in text for kw in ['科学', '技术', '工程', '数学', '物理', '化学']):
        category = '科学技术'
    
    return category, country

def scan_book_directory(book_dir, output_dir):
    """扫描书库目录"""
    books = []
    formats = ['.epub', '.mobi', '.azw3', '.pdf']
    
    print(f"扫描书库: {book_dir}")
    
    for root, dirs, files in os.walk(book_dir):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext not in formats:
                continue
            
            filepath = os.path.join(root, f)
            
            # 提取元数据
            title = None
            author = None
            description = None
            
            if ext == '.epub':
                meta = extract_epub_metadata(filepath)
                if meta:
                    title = meta.get('title')
                    author = meta.get('author')
                    description = meta.get('description')
            elif ext == '.pdf':
                meta = extract_pdf_metadata(filepath)
                if meta:
                    title = meta.get('title')
                    author = meta.get('author')
                    description = meta.get('description')
            
            # 使用文件名作为备选
            if not title:
                title = os.path.splitext(f)[0]
            
            # 分类
            category, country = classify_book(title or '', author or '')
            
            books.append({
                'title': title,
                'author': author or '未知作者',
                'category': category,
                'country': country,
                'format': ext[1:].upper(),
                'filename': f,
                'filepath': filepath,
                'introduction': description or '暂无简介',
                'intro_source': ''
            })
    
    # 保存索引
    os.makedirs(output_dir, exist_ok=True)
    index_file = os.path.join(output_dir, '书库索引.json')
    
    data = {
        'version': '1.0',
        'scan_date': datetime.now().isoformat(),
        'total_books': len(books),
        'books': books
    }
    
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"扫描完成: {len(books)} 本书")
    print(f"索引文件: {index_file}")
    
    return data

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print("用法: python book_scanner.py <书库目录> <输出目录>")
        sys.exit(1)
    
    book_dir = sys.argv[1]
    output_dir = sys.argv[2]
    scan_book_directory(book_dir, output_dir)

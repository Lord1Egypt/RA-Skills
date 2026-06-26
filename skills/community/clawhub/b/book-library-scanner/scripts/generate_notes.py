# -*- coding: utf-8 -*-
"""
生成Obsidian笔记
根据书库索引生成Markdown笔记文件
"""

import json
import os
import re
import sys

def generate_notes(index_file, output_dir):
    """生成Obsidian Markdown笔记"""
    
    # 加载索引
    with open(index_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    books = data['books']
    generated = 0
    skipped = 0
    
    print(f"生成Obsidian笔记...")
    print(f"书籍总数: {len(books)}")
    
    for book in books:
        if not book.get('introduction') or book.get('introduction') == '暂无简介':
            continue
        
        category = book.get('category', '其他')
        country = book.get('country', '未知')
        author = book.get('author', '未知作者')
        title = book.get('title', '未知书名')
        
        # 安全文件名
        safe_author = re.sub(r'[<>:"/\\|?*]', '', author)[:30].strip()
        safe_title = re.sub(r'[<>:"/\\|?*]', '', title)[:50].strip()
        
        if not safe_author:
            safe_author = '未知作者'
        if not safe_title:
            safe_title = '未知书名'
        
        # 构建路径
        folder = os.path.join(output_dir, category, country, safe_author)
        note_file = os.path.join(folder, f"{safe_title}.md")
        
        if os.path.exists(note_file):
            skipped += 1
            continue
        
        # Markdown内容
        content = f"""# {title}

- **作者**: {author}
- **分类**: {category}
- **国家**: {country}
- **格式**: {book.get('format', '未知')}
- **文件**: {book.get('filename', '')}

## 内容简介

{book.get('introduction', '暂无简介')}

---
*来源: {book.get('intro_source', '网络')}*
"""
        
        try:
            os.makedirs(folder, exist_ok=True)
            with open(note_file, 'w', encoding='utf-8') as f:
                f.write(content)
            generated += 1
        except Exception as e:
            print(f"  错误: {e}")
            skipped += 1
    
    # 统计分类
    categories = {}
    for book in books:
        cat = book.get('category', '其他')
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"\n{'='*60}")
    print("[完成!]")
    print(f"{'='*60}")
    print(f"生成笔记: {generated}")
    print(f"跳过(已存在): {skipped}")
    print(f"\n分类统计:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")
    
    return generated, skipped

def generate_index_page(index_file, output_dir):
    """生成书库总目录页面"""
    
    with open(index_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    books = data['books']
    
    # 统计
    categories = {}
    countries = {}
    with_intro = 0
    
    for book in books:
        cat = book.get('category', '其他')
        country = book.get('country', '未知')
        categories[cat] = categories.get(cat, 0) + 1
        countries[country] = countries.get(country, 0) + 1
        if book.get('introduction') and book.get('introduction') != '暂无简介':
            with_intro += 1
    
    # 生成目录页
    content = f"""# 书库总目录

> 扫描时间: {data.get('scan_date', '未知')}
> 书籍总数: {len(books)}
> 有简介: {with_intro} ({with_intro/len(books)*100:.1f}%)

## 分类统计

| 分类 | 数量 |
|-----|------|
"""
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        content += f"| {cat} | {count} |\n"
    
    content += "\n## 国家统计\n\n| 国家 | 数量 |\n|-----|------|\n"
    for country, count in sorted(countries.items(), key=lambda x: -x[1])[:20]:
        content += f"| {country} | {count} |\n"
    
    # 写入文件
    index_page = os.path.join(output_dir, '书库总目录.md')
    with open(index_page, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"总目录已生成: {index_page}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: python generate_notes.py <索引文件> <输出目录>")
        sys.exit(1)
    
    index_file = sys.argv[1]
    output_dir = sys.argv[2]
    
    generate_notes(index_file, output_dir)
    generate_index_page(index_file, output_dir)

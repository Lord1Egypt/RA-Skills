# -*- coding: utf-8 -*-
"""
书库扫描主流程
整合扫描、搜索简介、生成笔记的完整工作流
"""

import os
import sys
import json
import time
from datetime import datetime

# 添加脚本目录到路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from book_scanner import scan_book_directory
from generate_notes import generate_notes, generate_index_page

def full_workflow(book_dir, output_dir, search_delay=2):
    """
    完整工作流程:
    1. 扫描书库
    2. 搜索简介（可选）
    3. 生成Obsidian笔记
    """
    
    print("="*60)
    print("书库扫描入库流程")
    print("="*60)
    print(f"书库目录: {book_dir}")
    print(f"输出目录: {output_dir}")
    print()
    
    # 步骤1: 扫描书库
    print("[步骤1] 扫描书库目录...")
    data = scan_book_directory(book_dir, output_dir)
    books = data['books']
    
    # 统计
    need_intro = sum(1 for b in books if not b.get('introduction') or b['introduction'] == '暂无简介')
    print(f"扫描完成: {len(books)} 本书")
    print(f"需要搜索简介: {need_intro} 本")
    print()
    
    # 步骤2: 搜索简介（可选）
    if need_intro > 0:
        from batch_search import batch_search
        print("[步骤2] 搜索书籍简介...")
        
        index_file = os.path.join(output_dir, '书库索引.json')
        search_script = os.path.join(SCRIPT_DIR, 'search_book.ps1')
        
        # 检查搜索脚本
        if not os.path.exists(search_script):
            print(f"警告: 搜索脚本不存在: {search_script}")
            print("跳过简介搜索步骤")
        else:
            batch_search(index_file, search_script, delay=search_delay)
        print()
    
    # 步骤3: 生成Obsidian笔记
    print("[步骤3] 生成Obsidian笔记...")
    index_file = os.path.join(output_dir, '书库索引.json')
    generate_notes(index_file, output_dir)
    generate_index_page(index_file, output_dir)
    
    print()
    print("="*60)
    print("[全部完成!]")
    print("="*60)
    
    # 最终统计
    with open(index_file, 'r', encoding='utf-8') as f:
        final_data = json.load(f)
    
    total = len(final_data['books'])
    with_intro = sum(1 for b in final_data['books'] 
                     if b.get('introduction') and b['introduction'] != '暂无简介')
    
    print(f"书籍总数: {total}")
    print(f"有简介: {with_intro} ({with_intro/total*100:.1f}%)")
    print(f"输出目录: {output_dir}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("书库扫描入库工具")
        print()
        print("用法: python main.py <书库目录> <输出目录> [搜索延迟秒数]")
        print()
        print("示例:")
        print("  python main.py D:\\LWbook C:\\Users\\xxx\\Obsidian\\书库")
        print("  python main.py D:\\LWbook C:\\Users\\xxx\\Obsidian\\书库 3")
        sys.exit(1)
    
    book_dir = sys.argv[1]
    output_dir = sys.argv[2]
    search_delay = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    
    full_workflow(book_dir, output_dir, search_delay)

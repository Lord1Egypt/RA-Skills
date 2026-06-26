# -*- coding: utf-8 -*-
"""
批量搜索书籍简介
使用元宝搜索API搜索每本书的简介
"""

import json
import subprocess
import time
import os
import sys

def search_book(keyword, search_script):
    """调用PowerShell脚本搜索书籍简介"""
    try:
        result = subprocess.run(
            ['powershell', '-File', search_script, '-Keyword', keyword],
            capture_output=True,
            timeout=30
        )
        output = result.stdout.decode('utf-8', errors='ignore').strip()
        if output and '|||' in output:
            parts = output.split('|||', 1)
            return {
                'intro': parts[1].strip()[:500],  # 限制长度
                'source': parts[0].strip()
            }
    except Exception as e:
        pass
    return None

def batch_search(index_file, search_script, delay=2, save_every=100, batch_size=None):
    """批量搜索书籍简介"""
    
    # 加载索引
    with open(index_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    books = data['books']
    print(f"总书籍数: {len(books)}")
    
    # 找需要搜索的书
    need_search = []
    for i, book in enumerate(books):
        intro = book.get('introduction', '')
        if not intro or intro == '暂无简介' or not intro.strip():
            need_search.append(i)
    
    print(f"需要搜索简介: {len(need_search)} 本")
    
    if batch_size:
        need_search = need_search[:batch_size]
        print(f"本次处理: {len(need_search)} 本")
    
    if not need_search:
        print("所有书籍都已有简介!")
        return
    
    # 搜索
    total_found = 0
    start_time = time.time()
    
    for i, idx in enumerate(need_search):
        book = books[idx]
        title = book.get('title', '')
        
        # 进度显示
        if (i + 1) % 100 == 0:
            elapsed = time.time() - start_time
            rate = (i + 1) / elapsed if elapsed > 0 else 0
            eta = (len(need_search) - i - 1) / rate if rate > 0 else 0
            with_intro = sum(1 for b in books if b.get('introduction') and b.get('introduction') != '暂无简介')
            print(f"  [{i+1}/{len(need_search)}] Found: {total_found} ({with_intro} total) ETA: {eta/60:.1f}min")
        
        result = search_book(title, search_script)
        
        if result:
            books[idx]['introduction'] = result['intro']
            books[idx]['intro_source'] = result['source']
            total_found += 1
        else:
            books[idx]['introduction'] = '暂无简介'
        
        # 定期保存
        if (i + 1) % save_every == 0:
            data['books'] = books
            with open(index_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        
        time.sleep(delay)
    
    # 最终保存
    print("\n保存最终结果...")
    data['books'] = books
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    elapsed = time.time() - start_time
    with_intro = sum(1 for b in books if b.get('introduction') and b.get('introduction') != '暂无简介')
    
    print(f"\n{'='*60}")
    print("[完成!]")
    print(f"{'='*60}")
    print(f"搜索: {len(need_search)}")
    print(f"找到: {total_found}")
    print(f"有简介总数: {with_intro}/{len(books)}")
    print(f"耗时: {elapsed/60:.1f} 分钟")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: python batch_search.py <索引文件> <搜索脚本> [批量大小]")
        sys.exit(1)
    
    index_file = sys.argv[1]
    search_script = sys.argv[2]
    batch_size = int(sys.argv[3]) if len(sys.argv) > 3 else None
    
    batch_search(index_file, search_script, batch_size=batch_size)

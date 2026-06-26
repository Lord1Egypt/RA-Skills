#!/usr/bin/env python3
"""
搜索错误日志
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

def search_errors(keyword: str = None, tag: str = None, limit: int = 10):
    """搜索错误日志"""
    memory_dir = Path(__file__).parent.parent.parent.parent / 'workspace' / 'memory'
    
    # 获取所有日志文件
    log_files = sorted(memory_dir.glob('error-log-*.md'), reverse=True)
    
    if not log_files:
        print("❌ 未找到错误日志文件")
        return
    
    results = []
    
    for log_file in log_files:
        content = log_file.read_text()
        
        # 按错误分割
        errors = content.split('### 错误 #')
        
        for error in errors[1:]:  # 跳过第一个空块
            lines = error.split('\n')
            error_text = '\n'.join(lines[:10])  # 取前 10 行
            
            # 搜索关键词或标签
            match = False
            if keyword and keyword.lower() in error.lower():
                match = True
            if tag and tag in error:
                match = True
            
            if match:
                # 提取错误编号和标题
                first_line = lines[0].strip()
                error_num = first_line.split(' - ')[0] if ' - ' in first_line else first_line
                title = first_line.split(' - ')[1] if ' - ' in first_line else '无标题'
                
                results.append({
                    'file': log_file.name,
                    'number': error_num,
                    'title': title,
                    'content': error_text
                })
            
            if len(results) >= limit:
                break
        
        if len(results) >= limit:
            break
    
    # 输出结果
    if not results:
        print(f"❌ 未找到匹配的错误")
        if keyword:
            print(f"  关键词：{keyword}")
        if tag:
            print(f"  标签：{tag}")
        return
    
    print(f"✓ 找到 {len(results)} 个匹配的错误:\n")
    
    for i, result in enumerate(results, 1):
        print(f"--- 错误 {i} ---")
        print(f"文件：{result['file']}")
        print(f"编号：{result['number']}")
        print(f"标题：{result['title']}")
        print(f"内容:\n{result['content']}")
        print()

def main():
    parser = argparse.ArgumentParser(description='搜索错误日志')
    parser.add_argument('--keyword', '-k', help='搜索关键词')
    parser.add_argument('--tag', '-t', help='搜索标签，如 #文件校验')
    parser.add_argument('--limit', '-l', type=int, default=10, help='最多返回结果数')
    
    args = parser.parse_args()
    
    if not args.keyword and not args.tag:
        parser.print_help()
        print("\n❌ 请提供 --keyword 或 --tag 参数")
        sys.exit(1)
    
    search_errors(args.keyword, args.tag, args.limit)

if __name__ == '__main__':
    main()

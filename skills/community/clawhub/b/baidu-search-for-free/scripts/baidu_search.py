#!/usr/bin/env python3
"""
百度搜索脚本 - 使用 baidusearch 库进行百度搜索

用法:
    python3 baidu_search.py "搜索关键词"
    python3 baidu_search.py "搜索关键词" --num 20
    python3 baidu_search.py "搜索关键词" --json
"""

import sys
import json
import argparse

try:
    from baidusearch.baidusearch import search
except ImportError:
    print("错误: 未安装 baidusearch 库")
    print("请运行: pip3 install --user baidusearch")
    sys.exit(1)


def format_result(result, index):
    """格式化单条搜索结果"""
    title = result.get('title', '无标题')
    abstract = result.get('abstract', '无摘要')
    url = result.get('url', '')
    rank = result.get('rank', index)
    
    # 截断摘要，避免过长
    if len(abstract) > 150:
        abstract = abstract[:150] + "..."
    
    return f"""
[{rank}] {title}
    {abstract}
    链接: {url}
"""


def main():
    parser = argparse.ArgumentParser(description='百度搜索工具')
    parser.add_argument('query', help='搜索关键词')
    parser.add_argument('--num', '-n', type=int, default=10, help='返回结果数量（默认10）')
    parser.add_argument('--json', '-j', action='store_true', help='以JSON格式输出')
    parser.add_argument('--silent', '-s', action='store_true', help='静默模式，只输出结果')
    
    args = parser.parse_args()
    
    if not args.silent:
        print(f"正在搜索: {args.query}")
        print(f"请求结果数: {args.num}")
        print("-" * 50)
    
    try:
        results = search(args.query, num_results=args.num)
        
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            if not results:
                print("未找到结果（可能被限制，请稍后重试）")
                return
            
            print(f"找到 {len(results)} 条结果:\n")
            for i, result in enumerate(results, 1):
                print(format_result(result, i))
                
    except Exception as e:
        print(f"搜索出错: {e}")
        print("\n提示: 如果频繁出现错误，可能是：")
        print("  1. 请求过于频繁，请等待 15 秒后再试")
        print("  2. IP 被暂时限制，请等待 1 分钟后重试")
        print("  3. 网络连接问题")
        sys.exit(1)


if __name__ == '__main__':
    main()

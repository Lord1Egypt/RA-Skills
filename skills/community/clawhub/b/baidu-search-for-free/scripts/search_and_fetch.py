#!/usr/bin/env python3
"""
搜索并解析网页内容的完整流程脚本

用法:
    python3 search_and_fetch.py "搜索关键词"
    python3 search_and_fetch.py "搜索关键词" --num 5
    python3 search_and_fetch.py "搜索关键词" --fetch-first  # 只解析第一条结果
    python3 search_and_fetch.py "搜索关键词" --json
"""

import sys
import json
import argparse
import time

try:
    from baidusearch.baidusearch import search
except ImportError:
    print("错误: 未安装 baidusearch 库")
    print("请运行: pip3 install --user baidusearch")
    sys.exit(1)

# 导入 fetch_url 函数
sys.path.insert(0, '.')
from fetch_url import fetch_url


def format_search_result(result, index):
    """格式化搜索结果"""
    title = result.get('title', '无标题')
    abstract = result.get('abstract', '无摘要')
    url = result.get('url', '')
    rank = result.get('rank', index)
    
    if len(abstract) > 150:
        abstract = abstract[:150] + "..."
    
    return {
        'rank': rank,
        'title': title,
        'abstract': abstract,
        'url': url
    }


def main():
    parser = argparse.ArgumentParser(description='搜索并解析网页内容')
    parser.add_argument('query', help='搜索关键词')
    parser.add_argument('--num', '-n', type=int, default=10, help='返回结果数量（默认10）')
    parser.add_argument('--fetch-first', '-f', action='store_true', help='只解析第一条结果')
    parser.add_argument('--max-chars', '-m', type=int, default=3000, help='网页内容最大字符数')
    parser.add_argument('--json', '-j', action='store_true', help='以JSON格式输出')
    parser.add_argument('--silent', '-s', action='store_true', help='静默模式')
    
    args = parser.parse_args()
    
    if not args.silent:
        print(f"🔍 正在搜索: {args.query}")
        print(f"请求结果数: {args.num}")
        print("-" * 60)
    
    # 第一步：搜索
    try:
        search_results = search(args.query, num_results=args.num)
    except Exception as e:
        print(f"搜索出错: {e}")
        sys.exit(1)
    
    if not search_results:
        print("未找到搜索结果（可能被限制，请稍后重试）")
        sys.exit(1)
    
    if not args.silent:
        print(f"✅ 找到 {len(search_results)} 条搜索结果\n")
    
    # 格式化搜索结果
    formatted_results = [format_search_result(r, i+1) for i, r in enumerate(search_results)]
    
    # 如果只解析第一条
    if args.fetch_first:
        if not args.silent:
            print(f"📄 正在解析第1条结果的网页内容...")
            print(f"URL: {formatted_results[0]['url']}\n")
        
        content = fetch_url(formatted_results[0]['url'], max_chars=args.max_chars)
        formatted_results[0]['content'] = content
        
        if not args.silent:
            print(f"标题: {content.get('title', 'N/A')}")
            print(f"状态: {content.get('status_code', 'N/A')}")
            print("-" * 60)
            print(content.get('text', '无内容')[:500])
            if len(content.get('text', '')) > 500:
                print("...")
    else:
        # 解析所有结果的网页内容
        for i, result in enumerate(formatted_results):
            if not args.silent:
                print(f"\n[{i+1}/{len(formatted_results)}] {result['title']}")
                print(f"    正在解析: {result['url']}")
            
            content = fetch_url(result['url'], max_chars=args.max_chars)
            result['content'] = content
            
            if not args.silent:
                if content.get('error'):
                    print(f"    ⚠️ 解析失败: {content['error']}")
                else:
                    preview = content.get('text', '')[:200].replace('\n', ' ')
                    print(f"    ✅ 成功 | 预览: {preview}...")
            
            # 间隔一段时间，避免请求过快
            if i < len(formatted_results) - 1:
                time.sleep(1)
    
    if args.json:
        print(json.dumps(formatted_results, ensure_ascii=False, indent=2))
    
    if not args.silent:
        print(f"\n✅ 完成！共处理 {len(formatted_results)} 条结果")


if __name__ == '__main__':
    main()

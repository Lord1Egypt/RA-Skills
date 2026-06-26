#!/usr/bin/env python3
"""
Auto Find Customer - 主入口
整合搜索、提取邮箱、验证、缓存功能
"""

import argparse
import json
import sys
import time
import random
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from search_companies import search_companies
from extract_emails import extract_emails
from cache_manager import CacheManager


def find_customers(
    keyword, 
    region=None, 
    limit=50, 
    use_cache=True,
    skip_existing=True,
    page_offset=0
):
    cache = CacheManager() if use_cache else None
    
    print(f"\n{'='*50}", file=sys.stderr)
    print(f"🔍 搜索: {keyword} {region or ''}", file=sys.stderr)
    if page_offset > 0:
        print(f"   翻页偏移: {page_offset}", file=sys.stderr)
    print(f"{'='*50}\n", file=sys.stderr)
    
    if use_cache and page_offset == 0:
        cached = cache.get_search_cache(keyword, region)
        if cached:
            print(f"📦 使用缓存结果 ({len(cached)} 家公司)\n", file=sys.stderr)
            companies = cached
        else:
            companies = search_companies(keyword, region, limit)
            cache.save_search_cache(keyword, region, companies)
    else:
        companies = search_companies(keyword, region, limit)
    
    if page_offset > 0 and len(companies) > page_offset:
        companies = companies[page_offset:]
    
    if skip_existing and cache:
        new_companies = cache.filter_new_companies(companies)
        skipped = len(companies) - len(new_companies)
        if skipped > 0:
            print(f"⏭️  跳过 {skipped} 家已存在的公司\n", file=sys.stderr)
        companies = new_companies
    
    print(f"✅ 待处理 {len(companies)} 家公司\n", file=sys.stderr)
    
    results = []
    total_emails = 0
    
    for i, company in enumerate(companies):
        print(f"📧 [{i+1}/{len(companies)}] {company['name']}", file=sys.stderr)
        print(f"   域名: {company['domain']}", file=sys.stderr)
        
        emails = []
        if cache:
            cached_emails = cache.get_company_emails(company['domain'])
            if cached_emails:
                print(f"   📦 使用缓存邮箱", file=sys.stderr)
                emails = cached_emails
            else:
                emails = extract_emails(company['domain'], use_whois=True)
                cache.save_company_emails(company['domain'], emails)
        else:
            emails = extract_emails(company['domain'], use_whois=True)
        
        if emails:
            total_emails += len(emails)
            print(f"   ✅ 找到 {len(emails)} 个邮箱: {emails[:3]}{'...' if len(emails) > 3 else ''}\n", file=sys.stderr)
        else:
            print(f"   ❌ 未找到邮箱\n", file=sys.stderr)
        
        result = {
            'name': company['name'],
            'domain': company['domain'],
            'url': company['url'],
            'description': company.get('description', ''),
            'source': company.get('source', ''),
            'emails': emails
        }
        results.append(result)
        
        if cache:
            cache.add_company(company)
        
        time.sleep(random.uniform(0.5, 1.5))
    
    print(f"\n{'='*50}", file=sys.stderr)
    print(f"📊 搜索结果汇总", file=sys.stderr)
    print(f"{'='*50}", file=sys.stderr)
    print(f"✅ 处理公司: {len(results)} 家", file=sys.stderr)
    print(f"✅ 有效邮箱: {total_emails} 个", file=sys.stderr)
    if results:
        print(f"✅ 邮箱覆盖率: {sum(1 for r in results if r['emails'])/len(results)*100:.1f}%", file=sys.stderr)
    
    if cache:
        stats = cache.get_stats()
        print(f"\n📈 累计数据:", file=sys.stderr)
        print(f"   总公司数: {stats['total_companies']}", file=sys.stderr)
        print(f"   总邮箱数: {stats['total_emails']}", file=sys.stderr)
    
    return {
        'query': keyword,
        'region': region,
        'total_companies': len(results),
        'total_emails': total_emails,
        'email_coverage': f"{sum(1 for r in results if r['emails'])/len(results)*100:.1f}%" if results else "0%",
        'results': results
    }


def main():
    parser = argparse.ArgumentParser(description='Auto Find Customer - 自动找客户')
    parser.add_argument('keyword', help='搜索关键词')
    parser.add_argument('--region', '-r', help='地区筛选 (如: 上海, 北京)')
    parser.add_argument('--limit', '-l', type=int, default=20, help='最大搜索数量 (默认: 20)')
    parser.add_argument('--output', '-o', help='输出文件路径 (JSON)')
    parser.add_argument('--csv', help='导出CSV文件路径')
    parser.add_argument('--no-cache', action='store_true', help='不使用缓存')
    parser.add_argument('--no-skip', action='store_true', help='不跳过已存在的公司')
    parser.add_argument('--page', '-p', type=int, default=0, help='翻页偏移 (获取更多不同结果)')
    parser.add_argument('--stats', action='store_true', help='显示缓存统计')
    
    args = parser.parse_args()
    
    if args.stats:
        from cache_manager import CacheManager
        cache = CacheManager()
        stats = cache.get_stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
        return
    
    result = find_customers(
        args.keyword, 
        args.region, 
        args.limit,
        use_cache=not args.no_cache,
        skip_existing=not args.no_skip,
        page_offset=args.page
    )
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n✅ JSON结果已保存到: {args.output}", file=sys.stderr)
    
    if args.csv:
        import csv
        with open(args.csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['公司名称', '域名', '邮箱', '网址', '简介'])
            for r in result['results']:
                writer.writerow([
                    r['name'],
                    r['domain'],
                    ', '.join(r['emails']),
                    r['url'],
                    r['description']
                ])
        print(f"✅ CSV结果已保存到: {args.csv}", file=sys.stderr)
    
    if not args.output and not args.csv:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

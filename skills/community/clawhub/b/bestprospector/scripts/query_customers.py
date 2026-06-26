#!/usr/bin/env python3
"""
查询已收集的客户数据
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from cache_manager import CacheManager


def query_customers(
    keyword=None,
    region=None,
    has_email=None,
    limit=50,
    output_format='table'
):
    cache = CacheManager()
    companies = cache.get_all_companies()
    emails_db = cache.get_all_emails()
    
    results = []
    
    for domain, info in companies.items():
        company_emails = emails_db.get(domain, {}).get('emails', [])
        
        if keyword and keyword.lower() not in info.get('name', '').lower():
            continue
        
        if region and region.lower() not in info.get('name', '').lower():
            continue
        
        if has_email == True and not company_emails:
            continue
        
        if has_email == False and company_emails:
            continue
        
        results.append({
            'name': info.get('name', domain),
            'domain': domain,
            'url': info.get('url', ''),
            'emails': company_emails,
            'first_found': info.get('first_found', ''),
            'search_count': info.get('search_count', 0)
        })
    
    results = results[:limit]
    
    if output_format == 'json':
        return {
            'total': len(results),
            'results': results
        }
    
    return results


def list_recent(limit=20):
    cache = CacheManager()
    companies = cache.get_all_companies()
    emails_db = cache.get_all_emails()
    
    results = []
    for domain, info in companies.items():
        company_emails = emails_db.get(domain, {}).get('emails', [])
        results.append({
            'name': info.get('name', domain),
            'domain': domain,
            'emails': company_emails,
            'first_found': info.get('first_found', '')
        })
    
    results.sort(key=lambda x: x.get('first_found', ''), reverse=True)
    
    return results[:limit]


def search_by_email(email_keyword):
    cache = CacheManager()
    emails_db = cache.get_all_emails()
    companies = cache.get_all_companies()
    
    results = []
    email_keyword = email_keyword.lower()
    
    for domain, email_info in emails_db.items():
        emails = email_info.get('emails', [])
        matching_emails = [e for e in emails if email_keyword in e.lower()]
        
        if matching_emails:
            company_info = companies.get(domain, {})
            results.append({
                'name': company_info.get('name', domain),
                'domain': domain,
                'matching_emails': matching_emails,
                'all_emails': emails
            })
    
    return results


def main():
    parser = argparse.ArgumentParser(description='查询已收集的客户数据')
    
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    list_parser = subparsers.add_parser('list', help='列出客户')
    list_parser.add_argument('--limit', '-l', type=int, default=20, help='数量限制')
    list_parser.add_argument('--has-email', action='store_true', help='只显示有邮箱的')
    list_parser.add_argument('--no-email', action='store_true', help='只显示无邮箱的')
    list_parser.add_argument('--json', action='store_true', help='JSON格式输出')
    
    search_parser = subparsers.add_parser('search', help='搜索客户')
    search_parser.add_argument('keyword', help='搜索关键词')
    search_parser.add_argument('--region', '-r', help='地区筛选')
    search_parser.add_argument('--limit', '-l', type=int, default=50, help='数量限制')
    search_parser.add_argument('--json', action='store_true', help='JSON格式输出')
    
    email_parser = subparsers.add_parser('email', help='按邮箱搜索')
    email_parser.add_argument('keyword', help='邮箱关键词')
    
    stats_parser = subparsers.add_parser('stats', help='统计信息')
    
    export_parser = subparsers.add_parser('export', help='导出数据')
    export_parser.add_argument('--output', '-o', default='customers_export.json', help='输出文件')
    export_parser.add_argument('--csv', help='导出CSV')
    
    args = parser.parse_args()
    
    cache = CacheManager()
    
    if args.command == 'list':
        has_email = True if args.has_email else (False if args.no_email else None)
        results = query_customers(
            has_email=has_email,
            limit=args.limit,
            output_format='json' if args.json else 'table'
        )
        
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(f"\n📋 客户列表 (共 {len(results.get('results', results))} 家)\n")
            print(f"{'序号':<4} {'公司名称':<30} {'域名':<25} {'邮箱':<30}")
            print("-" * 90)
            
            for i, r in enumerate(results.get('results', results), 1):
                emails = ', '.join(r.get('emails', []))[:28]
                print(f"{i:<4} {r.get('name', '')[:28]:<30} {r.get('domain', '')[:23]:<25} {emails:<30}")
    
    elif args.command == 'search':
        results = query_customers(
            keyword=args.keyword,
            region=args.region,
            limit=args.limit,
            output_format='json' if args.json else 'table'
        )
        
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(f"\n🔍 搜索结果: {args.keyword} (共 {len(results.get('results', results))} 家)\n")
            for r in results.get('results', results):
                print(f"• {r.get('name', r.get('domain'))}")
                if r.get('emails'):
                    print(f"  邮箱: {', '.join(r['emails'])}")
                print()
    
    elif args.command == 'email':
        results = search_by_email(args.keyword)
        
        print(f"\n📧 邮箱搜索: {args.keyword} (共 {len(results)} 家)\n")
        for r in results:
            print(f"• {r['name']}")
            print(f"  匹配: {', '.join(r['matching_emails'])}")
            print()
    
    elif args.command == 'stats':
        stats = cache.get_stats()
        
        print("\n📊 数据统计")
        print("=" * 40)
        print(f"总公司数: {stats['total_companies']}")
        print(f"总邮箱数: {stats['total_emails']}")
        print(f"搜索次数: {stats['total_searches']}")
        print(f"有邮箱公司: {stats['companies_with_emails']}")
        if stats['total_companies'] > 0:
            coverage = stats['companies_with_emails'] / stats['total_companies'] * 100
            print(f"邮箱覆盖率: {coverage:.1f}%")
    
    elif args.command == 'export':
        companies = cache.get_all_companies()
        emails_db = cache.get_all_emails()
        
        export_data = []
        for domain, info in companies.items():
            company_emails = emails_db.get(domain, {}).get('emails', [])
            export_data.append({
                'name': info.get('name', domain),
                'domain': domain,
                'url': info.get('url', ''),
                'emails': company_emails,
                'first_found': info.get('first_found', '')
            })
        
        if args.csv:
            import csv
            with open(args.csv, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['公司名称', '域名', '邮箱', '网址', '首次发现'])
                for r in export_data:
                    writer.writerow([
                        r['name'],
                        r['domain'],
                        ', '.join(r['emails']),
                        r['url'],
                        r['first_found']
                    ])
            print(f"✅ 已导出 {len(export_data)} 条数据到 {args.csv}")
        
        else:
            output = {
                'export_time': datetime.now().isoformat(),
                'total': len(export_data),
                'companies': export_data
            }
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
            print(f"✅ 已导出 {len(export_data)} 条数据到 {args.output}")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

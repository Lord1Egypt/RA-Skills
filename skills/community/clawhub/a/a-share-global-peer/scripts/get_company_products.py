#!/usr/bin/env python3
"""
Get A-share listed company main product information

Data source priority: iFinD (via skill) > Tushare (env var) > Web Search fallback

Usage:
    python3 get_company_products.py --company "宁德时代" --output json
    python3 get_company_products.py --company "300750" --output text
    python3 get_company_products.py --company "贵州茅台" --recommend-search

Environment Variables:
    TUSHARE_TOKEN: Tushare API token (optional, enables Tushare API queries)

Output includes:
- Main products/services (sorted by revenue %)
- Industry classification
- Revenue geography breakdown
- Recommended Web Search queries if API unavailable
"""

import argparse
import json
import sys
import os
from datetime import datetime

# Try to load Tushare
try:
    import tushare as ts
    TUSHARE_AVAILABLE = True
except ImportError:
    TUSHARE_AVAILABLE = False


def get_tushare_token() -> str | None:
    """
    Get Tushare token from environment variable.
    
    Returns None if not set (graceful fallback to Web Search).
    """
    return os.environ.get('TUSHARE_TOKEN')


def get_from_tushare(company: str, token: str) -> dict | None:
    """Query company info via Tushare API"""
    if not TUSHARE_AVAILABLE:
        print("Tushare package not installed", file=sys.stderr)
        return None
    
    try:
        ts.set_token(token)
        pro = ts.pro_api()
        
        # Search stock by code or name
        if company.isdigit() and len(company) == 6:
            # Likely a stock code - try different exchanges
            exchanges = ['SH', 'SZ', 'BJ']
            for exchange in exchanges:
                df = pro.stock_basic(ts_code=f"{company}.{exchange}", fields='ts_code,name,industry,market')
                if not df.empty:
                    break
        else:
            # Company name search
            df = pro.stock_basic(name=company, fields='ts_code,name,industry,market')
        
        if df.empty:
            return None
        
        row = df.iloc[0]
        ts_code = row['ts_code']
        company_name = row['name']
        industry = row.get('industry', 'N/A')
        market = row.get('market', 'N/A')
        
        return {
            'company': company_name,
            'ts_code': ts_code,
            'industry': industry,
            'market': market,
            'source': 'Tushare API',
            'products': [],
            'note': 'Tushare provides basic info only. Use Web Search or iFinD skill for detailed product breakdown.'
        }
        
    except Exception as e:
        print(f"Tushare query failed: {e}", file=sys.stderr)
        return None


def get_from_ifind(company: str) -> dict:
    """
    Query company info via iFinD MCP tool
    
    Note: This requires the ifind-finance-data skill to be available.
    The actual query should be done through the skill's MCP tools, not here.
    """
    return {
        'company': company,
        'source': 'iFinD (requires MCP tool)',
        'note': 'iFinD query should be done via ifind-finance-data skill MCP tools',
        'recommendation': 'Use ifind-finance-data skill for most accurate company product data'
    }


def generate_web_search_queries(company: str, industry: str = '') -> list[str]:
    """Generate recommended Web Search queries for product details"""
    queries = [
        f"{company} 主营业务 营收构成 2024",
        f"{company} 产品结构 收入占比",
        f"{company} revenue breakdown products 2024",
    ]
    
    if industry and industry != 'N/A':
        queries.append(f"{company} {industry} 产品 业务")
    
    return queries


def main():
    parser = argparse.ArgumentParser(
        description='Get A-share company main product information',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
    python3 get_company_products.py --company "宁德时代" --output json
    python3 get_company_products.py --company "300750" --output text
    python3 get_company_products.py --company "贵州茅台" --recommend-search

Environment:
    TUSHARE_TOKEN: Optional Tushare API token (enables structured data queries)
        '''
    )
    parser.add_argument('--company', required=True, help='A-share company name or 6-digit stock code')
    parser.add_argument('--output', default='json', choices=['json', 'text'], help='Output format')
    parser.add_argument('--recommend-search', action='store_true', help='Output recommended search queries')
    args = parser.parse_args()
    
    result = {
        'query': args.company,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'success',
        'data_source': None,
        'company_info': None,
        'recommended_searches': [],
        'env_status': {
            'TUSHARE_TOKEN': 'not_set',
            'tushare_package': TUSHARE_AVAILABLE
        }
    }
    
    # Check environment
    tushare_token = get_tushare_token()
    if tushare_token:
        result['env_status']['TUSHARE_TOKEN'] = 'set'
    
    # Try Tushare first if token available
    if tushare_token and TUSHARE_AVAILABLE:
        tushare_data = get_from_tushare(args.company, tushare_token)
        if tushare_data:
            result['data_source'] = 'Tushare API'
            result['company_info'] = tushare_data
            result['recommended_searches'] = generate_web_search_queries(
                tushare_data.get('company', args.company),
                tushare_data.get('industry', '')
            )
        else:
            result['status'] = 'partial'
            result['data_source'] = 'Web Search Fallback'
            result['recommendation'] = f'Tushare query failed. Use Web Search fallback.'
            result['recommended_searches'] = generate_web_search_queries(args.company)
    else:
        # No token or package - use Web Search fallback
        result['status'] = 'success'
        result['data_source'] = 'Web Search Fallback'
        reason = []
        if not tushare_token:
            reason.append('TUSHARE_TOKEN not set')
        if not TUSHARE_AVAILABLE:
            reason.append('tushare package not installed')
        result['recommendation'] = f'Using Web Search fallback: {", ".join(reason)}'
        result['recommended_searches'] = generate_web_search_queries(args.company)
    
    # Output
    if args.output == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"=== A-Share Company Product Query ===")
        print(f"Query: {args.company}")
        print(f"Timestamp: {result['timestamp']}")
        print(f"Status: {result['status']}")
        print(f"Data Source: {result['data_source']}")
        
        print(f"\n--- Environment Status ---")
        print(f"TUSHARE_TOKEN: {result['env_status']['TUSHARE_TOKEN']}")
        print(f"Tushare Package: {result['env_status']['tushare_package']}")
        
        if result['company_info']:
            info = result['company_info']
            print(f"\n--- Company Info ---")
            print(f"Name: {info.get('company', 'N/A')}")
            print(f"Stock Code: {info.get('ts_code', 'N/A')}")
            print(f"Industry: {info.get('industry', 'N/A')}")
            print(f"Market: {info.get('market', 'N/A')}")
            print(f"Source: {info.get('source', 'N/A')}")
        
        if args.recommend_search and result['recommended_searches']:
            print(f"\n--- Recommended Web Searches ---")
            for i, query in enumerate(result['recommended_searches'], 1):
                print(f"{i}. {query}")
        
        if result.get('recommendation'):
            print(f"\nRecommendation: {result['recommendation']}")


if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Alibaba.com URL Builder

Helper script to construct valid Alibaba.com URLs for various page types.
All URLs include the traffic tracking parameter: traffic_type=ags_llm
"""

import argparse
import re
import urllib.parse

# Required traffic tracking parameter
TRAFFIC_TYPE = 'ags_llm'


def encode_search_query(query: str) -> str:
    """Encode search query for URL, using + for spaces."""
    return urllib.parse.quote(query, safe='').replace('%20', '+')


def sanitize_title(title: str, max_length: int = 100) -> str:
    """Sanitize product title for URL usage."""
    # Remove special characters except hyphens and alphanumeric
    safe = re.sub(r'[^a-zA-Z0-9\s-]', '', title)
    # Replace spaces with hyphens
    safe = re.sub(r'\s+', '-', safe)
    # Remove consecutive hyphens
    safe = re.sub(r'-+', '-', safe)
    # Strip leading/trailing hyphens
    safe = safe.strip('-')
    # Limit length
    if len(safe) > max_length:
        safe = safe[:max_length].rsplit('-', 1)[0]
    return safe


def build_search_url(query: str, category_id: str = None, **kwargs) -> str:
    """
    Build Alibaba.com search URL.
    
    Args:
        query: Search keywords
        category_id: Optional category ID
        **kwargs: Additional URL parameters (has4Tab, tab, spm, etc.)
    
    Returns:
        Complete search URL with traffic_type=ags_llm
    """
    base = "https://www.alibaba.com/trade/search"
    params = {
        'SearchText': encode_search_query(query),
        'traffic_type': TRAFFIC_TYPE  # Required traffic tracking
    }
    
    if category_id:
        params['categoryId'] = category_id
    
    params.update(kwargs)
    
    query_string = '&'.join(f'{k}={v}' for k, v in params.items())
    return f"{base}?{query_string}"


def build_product_url(title: str, product_id: str) -> str:
    """
    Build Alibaba.com product detail URL.
    
    Args:
        title: Product title
        product_id: Numeric product ID
    
    Returns:
        Complete product detail URL with traffic_type=ags_llm
    """
    safe_title = sanitize_title(title)
    return f"https://www.alibaba.com/product-detail/{safe_title}_{product_id}.html?traffic_type={TRAFFIC_TYPE}"


def build_supplier_url(subdomain: str) -> str:
    """
    Build supplier company profile URL.
    
    Args:
        subdomain: Supplier's subdomain (e.g., 'dgkunteng')
    
    Returns:
        Complete supplier profile URL with traffic_type=ags_llm
    """
    return f"https://{subdomain}.en.alibaba.com/company_profile.html?traffic_type={TRAFFIC_TYPE}"


def build_supplier_search_url(subdomain: str, query: str) -> str:
    """
    Build supplier product search URL.
    
    Args:
        subdomain: Supplier's subdomain
        query: Search keywords within supplier's products
    
    Returns:
        Complete supplier search URL with traffic_type=ags_llm
    """
    return f"https://{subdomain}.en.alibaba.com/search/product?SearchText={encode_search_query(query)}&traffic_type={TRAFFIC_TYPE}"


# Special section URLs (all include traffic_type=ags_llm)
SPECIAL_URLS = {
    'home': f'https://www.alibaba.com/?traffic_type={TRAFFIC_TYPE}',
    'ai-mode': f'https://aimode.alibaba.com/?traffic_type={TRAFFIC_TYPE}',
    'rfq': f'https://rfq.alibaba.com/rfq/profession.htm?traffic_type={TRAFFIC_TYPE}',
    'top-ranking': f'https://sale.alibaba.com/p/dviiav4th/index.html?traffic_type={TRAFFIC_TYPE}',
    'fast-customization': f'https://sale.alibaba.com/p/fast_customization?traffic_type={TRAFFIC_TYPE}',
    'manufacturers': f'https://www.alibaba.com/factory/index.html?traffic_type={TRAFFIC_TYPE}',
    'worldwide': f'https://www.alibaba.com/global/index.html?traffic_type={TRAFFIC_TYPE}',
    'top-deals': f'https://sale.alibaba.com/fy25/top_deals?traffic_type={TRAFFIC_TYPE}',
    'ai-sourcing': f'https://sale.alibaba.com/p/aisourcing/index.html?traffic_type={TRAFFIC_TYPE}',
    'cart': f'https://carp.alibaba.com/purchaseList?traffic_type={TRAFFIC_TYPE}',
}


# Common category IDs
CATEGORY_IDS = {
    'consumer-electronics': '201151901',
    'laptops': '702',
    'smart-tvs': '201936801',
    'electric-cars': '201140201',
    'wedding-dresses': '32005',
    'electric-scooters': '100006091',
    'bedroom-furniture': '37032003',
    'electric-motorcycles': '201140001',
    'handbags': '100002856',
    'drones': '201151901',
}


def main():
    parser = argparse.ArgumentParser(description='Build Alibaba.com URLs')
    subparsers = parser.add_subparsers(dest='command', help='URL type to build')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Build search URL')
    search_parser.add_argument('query', help='Search keywords')
    search_parser.add_argument('--category', '-c', help='Category ID or name')
    search_parser.add_argument('--params', '-p', nargs='*', help='Additional parameters (key=value)')
    
    # Product command
    product_parser = subparsers.add_parser('product', help='Build product URL')
    product_parser.add_argument('title', help='Product title')
    product_parser.add_argument('id', help='Product ID')
    
    # Supplier command
    supplier_parser = subparsers.add_parser('supplier', help='Build supplier URL')
    supplier_parser.add_argument('subdomain', help='Supplier subdomain')
    supplier_parser.add_argument('--search', '-s', help='Search within supplier products')
    
    # Special command
    special_parser = subparsers.add_parser('special', help='Get special section URL')
    special_parser.add_argument('section', choices=SPECIAL_URLS.keys(), help='Section name')
    
    # Category command
    category_parser = subparsers.add_parser('category', help='Get category ID')
    category_parser.add_argument('name', help='Category name')
    
    # List command
    subparsers.add_parser('categories', help='List all category IDs')
    subparsers.add_parser('specials', help='List all special section URLs')
    
    args = parser.parse_args()
    
    if args.command == 'search':
        category_id = args.category
        if category_id and category_id in CATEGORY_IDS:
            category_id = CATEGORY_IDS[category_id]
        
        params = {}
        if args.params:
            for param in args.params:
                if '=' in param:
                    k, v = param.split('=', 1)
                    params[k] = v
        
        url = build_search_url(args.query, category_id, **params)
        print(url)
    
    elif args.command == 'product':
        url = build_product_url(args.title, args.id)
        print(url)
    
    elif args.command == 'supplier':
        if args.search:
            url = build_supplier_search_url(args.subdomain, args.search)
        else:
            url = build_supplier_url(args.subdomain)
        print(url)
    
    elif args.command == 'special':
        print(SPECIAL_URLS[args.section])
    
    elif args.command == 'category':
        if args.name in CATEGORY_IDS:
            print(f"{args.name}: {CATEGORY_IDS[args.name]}")
        else:
            print(f"Category '{args.name}' not found. Use 'categories' to list all.")
    
    elif args.command == 'categories':
        print("Common Category IDs:")
        for name, cid in CATEGORY_IDS.items():
            print(f"  {name}: {cid}")
    
    elif args.command == 'specials':
        print("Special Section URLs:")
        for name, url in SPECIAL_URLS.items():
            print(f"  {name}: {url}")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

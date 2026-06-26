#!/usr/bin/env python3
"""
Shopify Store Analyzer
Analyze Shopify stores for competitor research.
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
from typing import List, Dict, Optional
from urllib.parse import urlparse


def is_shopify_store(url: str) -> bool:
    """Check if URL is a Shopify store."""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path
        
        # Direct Shopify domain
        if '.myshopify.com' in domain:
            return True
        
        # Check for Shopify indicators
        req = urllib.request.Request(
            f"https://{domain}",
            headers={'User-Agent': 'Mozilla/5.0 (compatible; Analyzer/1.0)'}
        )
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read().decode('utf-8', errors='ignore').lower()
                return 'shopify' in content or 'cdn.shopify.com' in content
        except:
            return False
    except:
        return False


def get_shopify_products(store_url: str, limit: int = 250) -> List[Dict]:
    """
    Fetch products from Shopify store using public API.
    """
    parsed = urlparse(store_url)
    domain = parsed.netloc or parsed.path
    
    if not domain.startswith('http'):
        domain = f"https://{domain}"
    
    products_url = f"{domain}/products.json?limit={limit}"
    
    try:
        req = urllib.request.Request(
            products_url,
            headers={'User-Agent': 'Mozilla/5.0 (compatible; Analyzer/1.0)'}
        )
        
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('products', [])
    except Exception as e:
        print(f"Error fetching products: {e}", file=sys.stderr)
        return []


def analyze_products(products: List[Dict]) -> Dict:
    """Analyze product data for insights."""
    if not products:
        return {}
    
    prices = []
    categories = {}
    vendors = {}
    
    for p in products:
        # Price analysis
        variants = p.get('variants', [])
        for v in variants:
            price = float(v.get('price', 0))
            if price > 0:
                prices.append(price)
        
        # Category analysis
        ptype = p.get('product_type', 'Uncategorized')
        categories[ptype] = categories.get(ptype, 0) + 1
        
        # Vendor analysis
        vendor = p.get('vendor', 'Unknown')
        vendors[vendor] = vendors.get(vendor, 0) + 1
    
    return {
        "total_products": len(products),
        "price_stats": {
            "min": round(min(prices), 2) if prices else 0,
            "max": round(max(prices), 2) if prices else 0,
            "avg": round(sum(prices) / len(prices), 2) if prices else 0,
            "median": round(sorted(prices)[len(prices)//2], 2) if prices else 0
        },
        "categories": dict(sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]),
        "vendors": dict(sorted(vendors.items(), key=lambda x: x[1], reverse=True)[:5]),
        "sample_products": [
            {
                "title": p.get('title', 'N/A'),
                "price": float(p.get('variants', [{}])[0].get('price', 0)),
                "type": p.get('product_type', 'N/A')
            }
            for p in products[:5]
        ]
    }


def compare_stores(store_data: List[Dict]) -> Dict:
    """Compare multiple Shopify stores."""
    comparison = {
        "stores_compared": len(store_data),
        "summary": []
    }
    
    for data in store_data:
        summary = {
            "store": data.get('store_url', 'Unknown'),
            "products": data.get('total_products', 0),
            "avg_price": data.get('price_stats', {}).get('avg', 0),
            "categories": len(data.get('categories', {}))
        }
        comparison["summary"].append(summary)
    
    # Find cheapest store
    if comparison["summary"]:
        cheapest = min(comparison["summary"], key=lambda x: x["avg_price"])
        largest = max(comparison["summary"], key=lambda x: x["products"])
        comparison["insights"] = {
            "cheapest_store": cheapest["store"],
            "largest_inventory": largest["store"]
        }
    
    return comparison


def main():
    parser = argparse.ArgumentParser(description='Analyze Shopify stores')
    parser.add_argument('url', help='Shopify store URL')
    parser.add_argument('--limit', type=int, default=250, help='Max products to fetch')
    parser.add_argument('--compare', nargs='+', help='Additional stores to compare')
    parser.add_argument('--output', '-o', help='Output file (JSON)')
    parser.add_argument('--format', choices=['json', 'summary'], default='summary')
    
    args = parser.parse_args()
    
    # Check if Shopify store
    if not is_shopify_store(args.url):
        print(f"⚠️  Warning: {args.url} may not be a Shopify store")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)
    
    # Fetch and analyze
    print(f"🔍 Analyzing {args.url}...")
    products = get_shopify_products(args.url, args.limit)
    
    if not products:
        print("❌ No products found or error accessing store")
        sys.exit(1)
    
    analysis = analyze_products(products)
    analysis['store_url'] = args.url
    
    # Compare if multiple stores
    if args.compare:
        all_data = [analysis]
        for store in args.compare:
            print(f"🔍 Analyzing {store}...")
            prods = get_shopify_products(store, args.limit)
            if prods:
                data = analyze_products(prods)
                data['store_url'] = store
                all_data.append(data)
        
        comparison = compare_stores(all_data)
        analysis['comparison'] = comparison
    
    # Output
    if args.format == 'json' or args.output:
        output = json.dumps(analysis, indent=2)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"✅ Analysis saved to {args.output}")
        else:
            print(output)
    else:
        # Summary output
        print(f"\n📊 Store Analysis: {args.url}")
        print("=" * 60)
        print(f"Total Products: {analysis['total_products']}")
        
        if 'price_stats' in analysis:
            ps = analysis['price_stats']
            print(f"\n💰 Price Range: ${ps['min']} - ${ps['max']}")
            print(f"   Average: ${ps['avg']} | Median: ${ps['median']}")
        
        if analysis.get('categories'):
            print(f"\n📁 Top Categories:")
            for cat, count in list(analysis['categories'].items())[:5]:
                print(f"   {cat}: {count} products")
        
        if analysis.get('sample_products'):
            print(f"\n🏷️  Sample Products:")
            for p in analysis['sample_products']:
                print(f"   • {p['title'][:50]}... (${p['price']})")
        
        if 'comparison' in analysis:
            print(f"\n📈 Comparison Results:")
            comp = analysis['comparison']
            if 'insights' in comp:
                print(f"   Cheapest: {comp['insights']['cheapest_store']}")
                print(f"   Largest: {comp['insights']['largest_inventory']}")
        
        print("=" * 60)


if __name__ == '__main__':
    main()

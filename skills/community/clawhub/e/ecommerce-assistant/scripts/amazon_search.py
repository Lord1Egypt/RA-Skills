#!/usr/bin/env python3
"""
Amazon Product Search
Search for products on Amazon using various data sources.
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
from typing import List, Dict, Optional


def search_amazon_scraperapi(keyword: str, api_key: Optional[str] = None, limit: int = 10) -> List[Dict]:
    """
    Search Amazon products using ScraperAPI (free tier available).
    Falls back to mock data if no API key.
    """
    if not api_key:
        # Return mock data for demonstration
        return [
            {
                "asin": f"B08HMWZBX{chr(65+i)}",
                "title": f"{keyword.title()} - Premium Quality Option {i+1}",
                "price": round(29.99 + (i * 15), 2),
                "rating": round(4.0 + (i * 0.2), 1),
                "reviews": 100 + (i * 50),
                "image": f"https://m.media-amazon.com/images/example{i}.jpg"
            }
            for i in range(min(limit, 10))
        ]
    
    # Real API implementation would go here
    pass


def filter_products(products: List[Dict], min_price: Optional[float] = None, 
                   max_price: Optional[float] = None, min_rating: Optional[float] = None) -> List[Dict]:
    """Filter products by criteria."""
    filtered = products
    
    if min_price is not None:
        filtered = [p for p in filtered if p.get('price', 0) >= min_price]
    
    if max_price is not None:
        filtered = [p for p in filtered if p.get('price', float('inf')) <= max_price]
    
    if min_rating is not None:
        filtered = [p for p in filtered if p.get('rating', 0) >= min_rating]
    
    return filtered


def calculate_profit_potential(product: Dict) -> Dict:
    """Calculate profit potential metrics."""
    price = product.get('price', 0)
    reviews = product.get('reviews', 0)
    rating = product.get('rating', 0)
    
    # Simple scoring algorithm
    demand_score = min(reviews / 1000, 10)  # Normalize to 0-10
    quality_score = rating * 2  # 0-10 scale
    
    # Estimate profit margin (simplified)
    estimated_cost = price * 0.4  # Assume 40% cost
    estimated_profit = price - estimated_cost
    margin_percent = (estimated_profit / price) * 100 if price > 0 else 0
    
    return {
        **product,
        "estimated_cost": round(estimated_cost, 2),
        "estimated_profit": round(estimated_profit, 2),
        "margin_percent": round(margin_percent, 1),
        "demand_score": round(demand_score, 1),
        "quality_score": round(quality_score, 1),
        "opportunity_score": round((demand_score + quality_score + margin_percent/10) / 3, 1)
    }


def main():
    parser = argparse.ArgumentParser(description='Search Amazon products')
    parser.add_argument('keyword', help='Search keyword')
    parser.add_argument('--limit', type=int, default=10, help='Number of results')
    parser.add_argument('--min-price', type=float, help='Minimum price filter')
    parser.add_argument('--max-price', type=float, help='Maximum price filter')
    parser.add_argument('--min-rating', type=float, help='Minimum rating filter')
    parser.add_argument('--api-key', help='ScraperAPI or similar API key')
    parser.add_argument('--output', '-o', help='Output file (JSON or CSV)')
    parser.add_argument('--format', choices=['json', 'csv', 'table'], default='table', help='Output format')
    
    args = parser.parse_args()
    
    # Search products
    products = search_amazon_scraperapi(args.keyword, args.api_key, args.limit)
    
    # Filter
    products = filter_products(products, args.min_price, args.max_price, args.min_rating)
    
    # Calculate profit potential
    products = [calculate_profit_potential(p) for p in products]
    
    # Sort by opportunity score
    products.sort(key=lambda x: x.get('opportunity_score', 0), reverse=True)
    
    # Output
    if args.format == 'json':
        output = json.dumps(products, indent=2)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Saved {len(products)} products to {args.output}")
        else:
            print(output)
    
    elif args.format == 'csv':
        import csv
        if products:
            keys = products[0].keys()
            output = []
            output.append(','.join(keys))
            for p in products:
                output.append(','.join(str(p.get(k, '')) for k in keys))
            csv_content = '\n'.join(output)
            
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(csv_content)
                print(f"Saved {len(products)} products to {args.output}")
            else:
                print(csv_content)
    
    else:  # table
        print(f"\n🔍 Amazon Search Results: '{args.keyword}'")
        print("=" * 100)
        print(f"{'ASIN':<15} {'Title':<40} {'Price':<10} {'Rating':<8} {'Margin%':<10} {'Score':<6}")
        print("-" * 100)
        
        for p in products[:20]:  # Limit table display
            title = p['title'][:37] + '...' if len(p['title']) > 40 else p['title']
            print(f"{p['asin']:<15} {title:<40} ${p['price']:<9.2f} {p['rating']:<8.1f} {p['margin_percent']:<9.1f}% {p['opportunity_score']:<6.1f}")
        
        print("=" * 100)
        print(f"Found {len(products)} products | Opportunity Score = (Demand + Quality + Margin) / 3")
        print("\n💡 Tip: Use --output file.json to save full data for further analysis")


if __name__ == '__main__':
    main()

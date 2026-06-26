#!/usr/bin/env python3
"""
eBay Price Check Tool
Check current and sold prices on eBay
"""

import subprocess
import json
import re
from urllib.parse import quote

def search_ebay(query, sold=False):
    """Search eBay for items"""
    url = f"https://www.ebay.com/sch/i.html?_nkw={quote(query)}&_sop=15"
    if sold:
        url = f"https://www.ebay.com/sch/i.html?_nkw={quote(query)}&_fsiv=1&_sop=15&_ufl=15"
    
    try:
        result = subprocess.run(
            ["curl", "-s", "-L", url],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout.decode('utf-8', errors='ignore')
    except Exception as e:
        return f"Error: {e}"

def parse_prices(html):
    """Extract prices from eBay HTML"""
    prices = []
    # Match price patterns
    price_pattern = r'[\$€£]?[\d,]+\.?\d*'
    
    # Find all price-like strings
    matches = re.findall(price_pattern, html)
    
    # Filter to reasonable price ranges (1-10000)
    for match in matches:
        try:
            price = float(match.replace(',', ''))
            if 1 <= price <= 10000:
                prices.append(price)
        except:
            continue
    
    return prices[:20]  # Return top 20 matches

def analyze_prices(prices):
    """Analyze price data"""
    if not prices:
        return "No price data found"
    
    return {
        "count": len(prices),
        "min": min(prices),
        "max": max(prices),
        "avg": sum(prices) / len(prices),
        "median": sorted(prices)[len(prices)//2] if prices else 0
    }

def format_result(query, prices, sold=False):
    """Format the search results"""
    stats = analyze_prices(prices)
    
    result = f"🔍 eBay {query}\n"
    if sold:
        result += "📊 Sold Items:\n"
    else:
        result += "🏷️ Current Listings:\n"
    
    result += f"   Found {stats['count']} items\n"
    if stats['count'] > 0:
        result += f"   Price range: ${stats['min']:.2f} - ${stats['max']:.2f}\n"
        result += f"   Average: ${stats['avg']:.2f}\n"
        result += f"   Median: ${stats['median']:.2f}\n"
    
    return result

def main(query, sold=False):
    """Main function to check eBay prices"""
    html = search_ebay(query, sold)
    prices = parse_prices(html)
    return format_result(query, prices, sold)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: ebay_price_check.py <item_name> [sold]")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:-1]) if sys.argv[-1] == "sold" else " ".join(sys.argv[1:])
    sold = sys.argv[-1] == "sold" if len(sys.argv) > 1 else False
    
    print(main(query, sold))
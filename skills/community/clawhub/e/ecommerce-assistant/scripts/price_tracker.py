#!/usr/bin/env python3
"""
Price Tracker
Monitor product prices and generate alerts.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional


DATA_DIR = os.path.expanduser("~/.ecommerce-assistant")
WATCHLIST_FILE = os.path.join(DATA_DIR, "watchlist.json")
PRICE_HISTORY_FILE = os.path.join(DATA_DIR, "price_history.json")


def ensure_data_dir():
    """Ensure data directory exists."""
    os.makedirs(DATA_DIR, exist_ok=True)


def load_watchlist() -> List[Dict]:
    """Load tracked products."""
    if os.path.exists(WATCHLIST_FILE):
        with open(WATCHLIST_FILE, 'r') as f:
            return json.load(f)
    return []


def save_watchlist(watchlist: List[Dict]):
    """Save tracked products."""
    ensure_data_dir()
    with open(WATCHLIST_FILE, 'w') as f:
        json.dump(watchlist, indent=2, fp=f)


def load_price_history() -> Dict:
    """Load price history."""
    if os.path.exists(PRICE_HISTORY_FILE):
        with open(PRICE_HISTORY_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_price_history(history: Dict):
    """Save price history."""
    ensure_data_dir()
    with open(PRICE_HISTORY_FILE, 'w') as f:
        json.dump(history, indent=2, fp=f)


def add_to_watchlist(identifier: str, platform: str = 'amazon', 
                     target_price: Optional[float] = None, name: str = ""):
    """Add product to watchlist."""
    watchlist = load_watchlist()
    
    # Check if already exists
    for item in watchlist:
        if item['id'] == identifier and item['platform'] == platform:
            print(f"⚠️  Product already in watchlist")
            return
    
    watchlist.append({
        "id": identifier,
        "platform": platform,
        "name": name or identifier,
        "target_price": target_price,
        "added_at": datetime.now().isoformat(),
        "active": True
    })
    
    save_watchlist(watchlist)
    print(f"✅ Added {identifier} to watchlist")
    if target_price:
        print(f"   Target price: ${target_price}")


def remove_from_watchlist(identifier: str):
    """Remove product from watchlist."""
    watchlist = load_watchlist()
    watchlist = [w for w in watchlist if w['id'] != identifier]
    save_watchlist(watchlist)
    print(f"✅ Removed {identifier} from watchlist")


def list_watchlist():
    """Display all tracked products."""
    watchlist = load_watchlist()
    
    if not watchlist:
        print("📭 Watchlist is empty")
        return
    
    print(f"\n📋 Price Watchlist ({len(watchlist)} items)")
    print("=" * 80)
    print(f"{'ID':<20} {'Platform':<10} {'Target':<12} {'Status':<10} {'Added':<20}")
    print("-" * 80)
    
    for item in watchlist:
        target = f"${item['target_price']}" if item.get('target_price') else "No target"
        status = "✅ Active" if item.get('active') else "⏸️  Paused"
        added = item['added_at'][:10] if item.get('added_at') else "Unknown"
        name = item['name'][:17] + '...' if len(item.get('name', '')) > 20 else item.get('name', item['id'])
        
        print(f"{name:<20} {item['platform']:<10} {target:<12} {status:<10} {added:<20}")
    
    print("=" * 80)


def check_prices():
    """Check current prices for all tracked items."""
    watchlist = load_watchlist()
    history = load_price_history()
    
    if not watchlist:
        print("📭 Watchlist is empty")
        return
    
    print(f"🔍 Checking prices for {len(watchlist)} items...")
    
    alerts = []
    timestamp = datetime.now().isoformat()
    
    for item in watchlist:
        if not item.get('active', True):
            continue
        
        # Mock price check - in real implementation, would call APIs
        # For demo, generate realistic mock data
        import random
        base_price = 50.0
        current_price = round(base_price + random.uniform(-10, 20), 2)
        
        # Record price
        item_id = item['id']
        if item_id not in history:
            history[item_id] = []
        
        history[item_id].append({
            "timestamp": timestamp,
            "price": current_price
        }
        )
        
        # Keep only last 30 days
        cutoff = (datetime.now() - timedelta(days=30)).isoformat()
        history[item_id] = [h for h in history[item_id] if h['timestamp'] > cutoff]
        
        # Check target price
        target = item.get('target_price')
        if target and current_price <= target:
            alerts.append({
                "item": item,
                "current_price": current_price,
                "target_price": target
            })
        
        print(f"   {item['name']}: ${current_price}", end="")
        if target:
            if current_price <= target:
                print(f" 🎯 TARGET REACHED!")
            else:
                print(f" (target: ${target})")
        else:
            print()
    
    save_price_history(history)
    
    if alerts:
        print(f"\n🚨 PRICE ALERTS ({len(alerts)} items at or below target):")
        for alert in alerts:
            print(f"   🎯 {alert['item']['name']}: ${alert['current_price']} (target: ${alert['target_price']})")


def generate_report(report_type: str = 'weekly'):
    """Generate price tracking report."""
    history = load_price_history()
    watchlist = load_watchlist()
    
    if not history:
        print("📭 No price history available")
        return
    
    print(f"\n📊 {report_type.title()} Price Report")
    print("=" * 60)
    
    for item in watchlist:
        item_id = item['id']
        if item_id not in history or not history[item_id]:
            continue
        
        prices = history[item_id]
        if len(prices) < 2:
            continue
        
        current = prices[-1]['price']
        previous = prices[0]['price']
        change = current - previous
        change_pct = (change / previous) * 100 if previous else 0
        
        min_price = min(p['price'] for p in prices)
        max_price = max(p['price'] for p in prices)
        avg_price = sum(p['price'] for p in prices) / len(prices)
        
        trend = "📈" if change > 0 else "📉" if change < 0 else "➡️"
        
        print(f"\n{item['name']}:")
        print(f"   Current: ${current:.2f} {trend} ({change:+.2f}, {change_pct:+.1f}%)")
        print(f"   Range: ${min_price:.2f} - ${max_price:.2f} | Avg: ${avg_price:.2f}")
        print(f"   Data points: {len(prices)}")
    
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description='Price tracking system')
    parser.add_argument('--add', help='Add product to watchlist (ASIN or URL)')
    parser.add_argument('--remove', help='Remove product from watchlist')
    parser.add_argument('--list', action='store_true', help='List all tracked products')
    parser.add_argument('--check', action='store_true', help='Check current prices')
    parser.add_argument('--target-price', type=float, help='Target price for alerts')
    parser.add_argument('--platform', default='amazon', choices=['amazon', 'shopify'], 
                       help='Product platform')
    parser.add_argument('--name', help='Product name')
    parser.add_argument('--report', choices=['daily', 'weekly', 'monthly'], 
                       help='Generate report')
    
    args = parser.parse_args()
    
    if args.add:
        add_to_watchlist(args.add, args.platform, args.target_price, args.name or args.add)
    elif args.remove:
        remove_from_watchlist(args.remove)
    elif args.list:
        list_watchlist()
    elif args.check:
        check_prices()
    elif args.report:
        generate_report(args.report)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

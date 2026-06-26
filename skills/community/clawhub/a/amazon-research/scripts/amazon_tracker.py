#!/usr/bin/env python3
"""
Amazon Product Research & Price Tracker
Simple implementation using SQLite for data storage
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
import argparse

DB_PATH = Path.home() / "workspace" / "Projects" / "Amazon-Research" / "amazon_prices.db"

def init_db():
    """Initialize database with tables"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            asin TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            category TEXT,
            url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Price history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asin TEXT NOT NULL,
            price REAL NOT NULL,
            currency TEXT DEFAULT 'EUR',
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (asin) REFERENCES products(asin)
        )
    ''')
    
    # Price alerts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asin TEXT NOT NULL,
            target_price REAL NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (asin) REFERENCES products(asin)
        )
    ''')
    
    # Wishlist table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wishlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asin TEXT NOT NULL,
            notes TEXT,
            priority INTEGER DEFAULT 3,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (asin) REFERENCES products(asin)
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"✅ Database initialized: {DB_PATH}")

def add_product(asin, title, category="", url="", price=None):
    """Add new product to database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Insert or update product
    cursor.execute('''
        INSERT OR REPLACE INTO products (asin, title, category, url)
        VALUES (?, ?, ?, ?)
    ''', (asin, title, category, url))
    
    # Add initial price if provided
    if price:
        cursor.execute('''
            INSERT INTO price_history (asin, price)
            VALUES (?, ?)
        ''', (asin, price))
    
    conn.commit()
    conn.close()
    print(f"✅ Added product: {title} (ASIN: {asin})")

def record_price(asin, price, currency='EUR'):
    """Record current price"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO price_history (asin, price, currency)
        VALUES (?, ?, ?)
    ''', (asin, price, currency))
    
    conn.commit()
    conn.close()
    print(f"💰 Recorded price: {price} {currency} for {asin}")

def get_price_history(asin, limit=10):
    """Get price history for product"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT p.title, ph.price, ph.currency, ph.recorded_at
        FROM price_history ph
        JOIN products p ON ph.asin = p.asin
        WHERE ph.asin = ?
        ORDER BY ph.recorded_at DESC
        LIMIT ?
    ''', (asin, limit))
    
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        print(f"⚠️ No price history found for {asin}")
        return
    
    print(f"\n📊 Price History for: {results[0][0]}")
    print("-" * 60)
    for title, price, currency, date in results:
        print(f"{date[:16]} | {price:>8.2f} {currency}")

def get_product_info(asin):
    """Get product details"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT p.*, 
               (SELECT price FROM price_history 
                WHERE asin = p.asin ORDER BY recorded_at DESC LIMIT 1) as current_price,
               (SELECT MIN(price) FROM price_history WHERE asin = p.asin) as min_price,
               (SELECT MAX(price) FROM price_history WHERE asin = p.asin) as max_price
        FROM products p
        WHERE p.asin = ?
    ''', (asin,))
    
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        print(f"⚠️ Product not found: {asin}")
        return
    
    print(f"\n📦 Product Info:")
    print(f"   ASIN: {result[0]}")
    print(f"   Title: {result[1]}")
    print(f"   Category: {result[2] or 'N/A'}")
    print(f"   Current Price: {result[4] or 'N/A'} €")
    print(f"   Lowest Price: {result[5] or 'N/A'} €")
    print(f"   Highest Price: {result[6] or 'N/A'} €")

def list_products(category=None, limit=20):
    """List all tracked products"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if category:
        cursor.execute('''
            SELECT p.asin, p.title, p.category,
                   (SELECT price FROM price_history 
                    WHERE asin = p.asin ORDER BY recorded_at DESC LIMIT 1) as current_price
            FROM products p
            WHERE p.category = ?
            ORDER BY p.created_at DESC
            LIMIT ?
        ''', (category, limit))
    else:
        cursor.execute('''
            SELECT p.asin, p.title, p.category,
                   (SELECT price FROM price_history 
                    WHERE asin = p.asin ORDER BY recorded_at DESC LIMIT 1) as current_price
            FROM products p
            ORDER BY p.created_at DESC
            LIMIT ?
        ''', (limit,))
    
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        print("⚠️ No products tracked yet")
        return
    
    print(f"\n📋 Tracked Products ({len(results)} total):")
    print("-" * 80)
    print(f"{'ASIN':<15} {'Price':<10} {'Category':<15} {'Title':<40}")
    print("-" * 80)
    for asin, title, category, price in results:
        price_str = f"{price:.2f}€" if price else "N/A"
        cat_str = (category or "N/A")[:14]
        title_str = title[:38]
        print(f"{asin:<15} {price_str:<10} {cat_str:<15} {title_str}")

def add_to_wishlist(asin, notes="", priority=3):
    """Add product to wishlist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR REPLACE INTO wishlist (asin, notes, priority)
        VALUES (?, ?, ?)
    ''', (asin, notes, priority))
    
    conn.commit()
    conn.close()
    print(f"⭐ Added to wishlist: {asin}")

def set_price_alert(asin, target_price):
    """Set price alert"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO price_alerts (asin, target_price)
        VALUES (?, ?)
    ''', (asin, target_price))
    
    conn.commit()
    conn.close()
    print(f"🔔 Price alert set: Notify when price drops below {target_price}€")

def check_alerts():
    """Check all price alerts"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT a.asin, p.title, a.target_price, 
               (SELECT price FROM price_history 
                WHERE asin = a.asin ORDER BY recorded_at DESC LIMIT 1) as current_price
        FROM price_alerts a
        JOIN products p ON a.asin = p.asin
        WHERE a.is_active = 1
    ''')
    
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        print("ℹ️ No active price alerts")
        return
    
    print(f"\n🔔 Price Alerts ({len(results)} active):")
    print("-" * 80)
    
    triggered = []
    for asin, title, target, current in results:
        if current and current <= target:
            triggered.append((asin, title, current, target))
            print(f"🚨 TRIGGERED: {title}")
            print(f"   Current: {current:.2f}€ | Target: {target:.2f}€")
        else:
            status = f"{current:.2f}€" if current else "N/A"
            print(f"⏳ {title[:40]}...")
            print(f"   Current: {status} | Target: {target:.2f}€")
    
    if triggered:
        print(f"\n✅ {len(triggered)} alert(s) triggered! Good time to buy!")

def main():
    parser = argparse.ArgumentParser(description="Amazon Product Research & Price Tracker")
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Init
    subparsers.add_parser('init', help='Initialize database')
    
    # Add product
    add_parser = subparsers.add_parser('add', help='Add product')
    add_parser.add_argument('asin', help='Amazon ASIN')
    add_parser.add_argument('title', help='Product title')
    add_parser.add_argument('--category', default='', help='Product category')
    add_parser.add_argument('--price', type=float, help='Current price')
    add_parser.add_argument('--url', default='', help='Product URL')
    
    # Record price
    price_parser = subparsers.add_parser('price', help='Record price')
    price_parser.add_argument('asin', help='Amazon ASIN')
    price_parser.add_argument('price', type=float, help='Price value')
    price_parser.add_argument('--currency', default='EUR', help='Currency')
    
    # History
    hist_parser = subparsers.add_parser('history', help='Price history')
    hist_parser.add_argument('asin', help='Amazon ASIN')
    hist_parser.add_argument('--limit', type=int, default=10, help='Number of records')
    
    # List
    list_parser = subparsers.add_parser('list', help='List products')
    list_parser.add_argument('--category', help='Filter by category')
    list_parser.add_argument('--limit', type=int, default=20, help='Limit results')
    
    # Info
    info_parser = subparsers.add_parser('info', help='Product info')
    info_parser.add_argument('asin', help='Amazon ASIN')
    
    # Wishlist
    wish_parser = subparsers.add_parser('wishlist', help='Add to wishlist')
    wish_parser.add_argument('asin', help='Amazon ASIN')
    wish_parser.add_argument('--notes', default='', help='Notes')
    wish_parser.add_argument('--priority', type=int, default=3, help='Priority 1-5')
    
    # Alert
    alert_parser = subparsers.add_parser('alert', help='Set price alert')
    alert_parser.add_argument('asin', help='Amazon ASIN')
    alert_parser.add_argument('target_price', type=float, help='Target price')
    
    # Check alerts
    subparsers.add_parser('check-alerts', help='Check price alerts')
    
    args = parser.parse_args()
    
    if args.command == 'init':
        init_db()
    elif args.command == 'add':
        add_product(args.asin, args.title, args.category, args.url, args.price)
    elif args.command == 'price':
        record_price(args.asin, args.price, args.currency)
    elif args.command == 'history':
        get_price_history(args.asin, args.limit)
    elif args.command == 'list':
        list_products(args.category, args.limit)
    elif args.command == 'info':
        get_product_info(args.asin)
    elif args.command == 'wishlist':
        add_to_wishlist(args.asin, args.notes, args.priority)
    elif args.command == 'alert':
        set_price_alert(args.asin, args.target_price)
    elif args.command == 'check-alerts':
        check_alerts()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()

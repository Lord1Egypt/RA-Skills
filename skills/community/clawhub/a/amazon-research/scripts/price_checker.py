#!/usr/bin/env python3
"""
Amazon Price Checker - Daily Cron Job
Checks prices and sends alerts for good deals
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
import random  # For simulation - replace with real scraping

DB_PATH = Path.home() / "workspace" / "Projects" / "Amazon-Research" / "amazon_prices.db"
LOG_PATH = Path.home() / "workspace" / "Projects" / "Amazon-Research" / "daily_checks.log"

def log_message(msg):
    """Log message with timestamp"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] {msg}"
    print(log_line)
    
    with open(LOG_PATH, 'a') as f:
        f.write(log_line + '\n')

def simulate_price_check(asin, current_price):
    """Simulate price check - in real implementation, scrape Amazon"""
    # Simulate small price fluctuations
    change = random.uniform(-0.05, 0.02)  # -5% to +2%
    new_price = current_price * (1 + change)
    return round(new_price, 2)

def check_prices():
    """Check all tracked products and record new prices"""
    if not DB_PATH.exists():
        log_message("❌ Database not found")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all products with their latest prices
    cursor.execute('''
        SELECT p.asin, p.title, 
               (SELECT price FROM price_history 
                WHERE asin = p.asin ORDER BY recorded_at DESC LIMIT 1) as current_price
        FROM products p
    ''')
    
    products = cursor.fetchall()
    log_message(f"📊 Checking {len(products)} products...")
    
    deals_found = []
    
    for asin, title, current_price in products:
        if current_price is None:
            continue
        
        # Simulate price check (replace with real Amazon scraping)
        new_price = simulate_price_check(asin, current_price)
        
        # Record price if changed significantly (>1%)
        price_change_pct = ((new_price - current_price) / current_price) * 100
        
        if abs(price_change_pct) > 1:
            cursor.execute('''
                INSERT INTO price_history (asin, price) VALUES (?, ?)
            ''', (asin, new_price))
            
            if price_change_pct < 0:
                log_message(f"📉 {title[:40]}: {current_price:.2f}€ → {new_price:.2f}€ ({price_change_pct:.1f}%)")
                deals_found.append((asin, title, new_price, price_change_pct))
            else:
                log_message(f"📈 {title[:40]}: {current_price:.2f}€ → {new_price:.2f}€ (+{price_change_pct:.1f}%)")
    
    conn.commit()
    
    # Check alerts
    cursor.execute('''
        SELECT a.asin, p.title, a.target_price, 
               (SELECT price FROM price_history 
                WHERE asin = a.asin ORDER BY recorded_at DESC LIMIT 1) as current_price
        FROM price_alerts a
        JOIN products p ON a.asin = p.asin
        WHERE a.is_active = 1
    ''')
    
    alerts = cursor.fetchall()
    triggered = []
    
    for asin, title, target, current in alerts:
        if current and current <= target:
            triggered.append((asin, title, current, target))
            log_message(f"🚨 ALERT TRIGGERED: {title}")
            log_message(f"   Target: {target:.2f}€ | Current: {current:.2f}€")
    
    conn.close()
    
    # Summary
    log_message(f"✅ Check complete. {len(deals_found)} price changes, {len(triggered)} alerts triggered")
    
    # Return summary for notification
    return {
        'products_checked': len(products),
        'price_changes': len(deals_found),
        'alerts_triggered': len(triggered),
        'deals': deals_found,
        'alerts': triggered
    }

if __name__ == '__main__':
    log_message("🚀 Starting daily Amazon price check...")
    result = check_prices()
    
    # Output summary for potential notification
    if result and result['alerts_triggered'] > 0:
        print("\n🎯 DEALS FOUND:")
        for asin, title, price, change in result['deals']:
            print(f"   {title[:50]}: {price:.2f}€ ({change:.1f}%)")

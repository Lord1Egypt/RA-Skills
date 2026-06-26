#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XI Stock Monthly Data Fetcher
羲股票监控系统 - 月线数据获取

This script fetches monthly K-line data for all stocks from Tencent Finance API.
本脚本从腾讯财经API获取所有股票的月K线数据。
- Monthly fetching for long-term trend analysis
- 月线获取用于长期趋势分析
- Saves 800 historical data points per stock
- 每只股票保存800个历史数据点
"""

import os
import sys
import sqlite3
import requests
import json
from datetime import datetime

# Fix encoding for Windows console
# 修复Windows控制台编码问题
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Configuration
DB_PATH = "D:\\xistock\\stock.db"
DATA_DIR = "D:\\xistock\\month"
BASE_URL = "https://proxy.finance.qq.com/ifzqgtimg/appstock/app/newfqkline/get"
DATA_POINTS = 800
FREQ = "month"

def get_db_connection():
    """Get database connection"""
    if not os.path.exists(DB_PATH):
        print(f"- Database not found: {DB_PATH}")
        print("  Please run init_db.py and fetch_stocks.py first!")
        exit(1)
    return sqlite3.connect(DB_PATH)

def get_stocks_to_fetch():
    """Get list of stocks that need to be fetched (all active stocks)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT code, name, market 
        FROM stocks 
        WHERE status = 'active'
        ORDER BY code
    """)
    
    stocks = cursor.fetchall()
    conn.close()
    
    return stocks

def format_stock_code(code):
    """Format stock code for Tencent Finance API (sh600001, sz000001)"""
    if code.startswith('60'):
        return f"sh{code}"
    else:
        return f"sz{code}"

def fetch_stock_data(stock_code, stock_name):
    """Fetch monthly K-line data from Tencent Finance API"""
    try:
        tencent_code = format_stock_code(stock_code)
        params = f"{tencent_code},{FREQ},,,{DATA_POINTS},qfq"
        url = f"{BASE_URL}?_var=kline_monthqfq&param={params}"
        
        response = requests.get(url, timeout=30)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"- {stock_code} {stock_name}: HTTP {response.status_code}")
            return None
        
        # Response is in format: kline_monthqfq = {...};
        content = response.text
        if '=' in content:
            json_str = content.split('=', 1)[1].rstrip(';')
        else:
            json_str = content
        
        data = json.loads(json_str)
        
        # Data structure: data -> tencent_code -> qfqmonth
        if 'data' not in data or tencent_code not in data['data']:
            print(f"- {stock_code} {stock_name}: No data found")
            return None
        
        stock_data = data['data'][tencent_code]
        if 'qfqmonth' not in stock_data:
            print(f"- {stock_code} {stock_name}: No qfqmonth found")
            return None
        
        return stock_data['qfqmonth']
        
    except Exception as e:
        print(f"- {stock_code} {stock_name}: Error fetching - {str(e)}")
        return None

def process_data(data):
    """
    Process raw data, extract date, open, close, high, low and calculate change
    返回格式列表: [date, open, close, high, low, change]
    """
    processed = []
    
    # Data format from Tencent: [date, open, close, high, low, volume, ...]
    for bar in data:
        if len(bar) >= 5:
            date = bar[0]
            open_p = float(bar[1])
            close = float(bar[2])
            high = float(bar[3])
            low = float(bar[4])
            
            processed.append([date, open_p, close, high, low])
    
    # Calculate change (涨跌幅)
    for i in range(len(processed)):
        if i == 0:
            change = 0.0
        else:
            prev_close = processed[i-1][2]
            if prev_close == 0:
                change = 0.0
            else:
                change = ((processed[i][2] - prev_close) / prev_close) * 100
        processed[i].append(round(change, 3))
    
    return processed

def save_to_file(stock_code, stock_name, data):
    """
    Save processed data to file, one data point per line
    Format: date,open,close,high,low,change
    Filename: 名称_代码.txt
    """
    # Create directory if not exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    # Sanitize filename - remove all invalid Windows filename characters
    # Invalid chars: \ / : * ? " < > |
    invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    safe_name = stock_name
    for c in invalid_chars:
        safe_name = safe_name.replace(c, '_')
    filename = f"{safe_name}_{stock_code}.txt"
    filepath = os.path.join(DATA_DIR, filename)
    
    # Write header
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("date,open,close,high,low,change_pct\n")
        for item in data:
            date, open_p, close, high, low, change = item
            line = f"{date},{open_p:.2f},{close:.2f},{high:.2f},{low:.2f},{change:.3f}\n"
            f.write(line)
    
    return filepath

def update_database_last_fetch(stock_code):
    """Update the month_get timestamp in database to current date"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""
        UPDATE stocks 
        SET month_get = ?
        WHERE code = ?
    """, (current_time, stock_code))
    
    conn.commit()
    conn.close()

def fetch_all_stocks():
    """Fetch data for all stocks"""
    stocks = get_stocks_to_fetch()
    total = len(stocks)
    
    print("=" * 70)
    print("XI Stock Monthly Data Fetcher")
    print("羲股票监控系统 - 月线数据获取")
    print("=" * 70)
    print(f"Total active stocks: {total}")
    print(f"Data directory: {DATA_DIR}")
    print("-" * 70)
    
    success = 0
    failed = 0
    
    for i, (code, name, market) in enumerate(stocks, 1):
        print(f"[{i}/{total}] Fetching {code} {name}...", end=' ')
        sys.stdout.flush()
        
        # Fetch data
        raw_data = fetch_stock_data(code, name)
        
        if raw_data is None:
            print("FAILED")
            failed += 1
            continue
        
        # Process data
        bars = raw_data
        processed = process_data(bars)
        
        if not processed:
            print("NO DATA")
            failed += 1
            continue
        
        # Save to file
        save_to_file(code, name, processed)
        
        # Update database
        update_database_last_fetch(code)
        
        print(f"OK ({len(processed)} points)")
        success += 1
        
        # Add delay to avoid hitting rate limit
        if i % 10 == 0:
            import time
            time.sleep(1)
    
    # Final summary
    print("-" * 70)
    print("任务完成！")
    print("我辛苦了！")
    print("-" * 70)
    print(f"Total stocks: {total}")
    print(f"Successfully fetched: {success}")
    print(f"Failed: {failed}")
    print(f"Data saved to: {DATA_DIR}")
    print("-" * 70)
    print("Database updated with last fetch timestamps")
    print("=" * 70)

if __name__ == "__main__":
    try:
        fetch_all_stocks()
    except KeyboardInterrupt:
        print("\n\n- Interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n- Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A-Share-Get Monthly Data Fetcher - Parallel Incremental Version
A股数据获取 - 月线数据增量获取（并行版本）

Usage:
    python scripts/month_parallel.py asc   # 获取前一半（升序），每次2-3只
    python scripts/month_parallel.py desc  # 获取后一半（降序），每次2-3只

Run both in separate processes to speed up incremental updates!
在两个独立进程中同时运行，加速增量更新！

Incremental update logic:
- Read existing file, get latest date
- Only fetch data newer than latest date (add to file, don't overwrite)
- If file doesn't exist, fetch full 800 points
- Process max 100 stocks per run (incremental) / 800 (new file)
- Update database timestamp after successful fetch
"""

import os
import sys
import sqlite3
import requests
import json
from datetime import datetime

# Fix encoding for Windows console
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Configuration
DB_PATH = "D:\\xistock\\stock.db"
DATA_DIR = "D:\\xistock\\month"
BASE_URL = "https://proxy.finance.qq.com/ifzqgtimg/appstock/app/newfqkline/get"
DATA_POINTS_FULL = 800      # When file doesn't exist
MAX_STOCKS_PER_RUN_INCREMENTAL = 100  # Max stocks to process per run when incremental update
FREQ = "month"
BATCH_SIZE = 3  # Process 2-3 stocks per batch to avoid long runtime

def get_db_connection():
    """Get database connection"""
    if not os.path.exists(DB_PATH):
        print(f"- Database not found: {DB_PATH}")
        print("  Please run init_db.py and fetch_stocks.py first!")
        exit(1)
    return sqlite3.connect(DB_PATH)

def get_latest_date_from_file(filepath):
    """
    Read existing file and get the latest date
    Returns None if file doesn't exist or empty
    """
    if not os.path.exists(filepath):
        return None
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            # Skip header
            next(f)
            latest_date = None
            # Read all lines to get the last date
            for line in f:
                line = line.strip()
                if not line:
                    continue
                date = line.split(',')[0]
                latest_date = date
            return latest_date
    except Exception as e:
        print(f"  Warning: Cannot read existing file: {e}")
        return None

def get_stocks_to_fetch(order):
    """
    Get list of stocks that need to be fetched (incremental)
    - Selects stocks that have never been fetched or haven't been fetched recently
    - order: 'asc' or 'desc' - split into two partitions
    - Returns up to MAX_STOCKS_PER_RUN_INCREMENTAL stocks
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get all active stocks ordered by code
    cursor.execute("""
        SELECT code, name, market, month_get 
        FROM stocks 
        WHERE status = 'active'
        ORDER BY code
    """)
    
    all_stocks = cursor.fetchall()
    total = len(all_stocks)
    half = total // 2
    
    # Split into two partitions
    if order == 'asc':
        partition_stocks = all_stocks[:half]
    elif order == 'desc':
        all_stocks.reverse()
        partition_stocks = all_stocks[:half]
    else:
        print(f"- Invalid order: {order}. Use 'asc' or 'desc'")
        exit(1)
    
    # Filter stocks that need update (any stock that hasn't been fetched today)
    today = datetime.now().strftime('%Y-%m-%d')
    need_update = []
    
    for stock in partition_stocks:
        if len(stock) == 3:
            code, name, market = stock
            month_get = None
        else:
            code, name, market, month_get = stock
        
        # If never fetched or last fetched not today, needs update
        if month_get is None or not month_get.startswith(today):
            need_update.append((code, name, market))
    
    # Process all need update today, large safety limit to prevent infinite run
    # MAX_STOCKS_PER_RUN_INCREMENTAL is original limit, now we allow 10x that
    if len(need_update) > MAX_STOCKS_PER_RUN_INCREMENTAL * 10:
        need_update = need_update[:MAX_STOCKS_PER_RUN_INCREMENTAL * 10]
    
    print(f"Partition {order}:")
    print(f"  Total in partition: {len(partition_stocks)}")
    print(f"  Need update today: {len(need_update)}")
    print(f"  Will process all {len(need_update)} stocks (safety limit: {MAX_STOCKS_PER_RUN_INCREMENTAL * 10})")
    print(f"  Will process: {len(need_update)} (max {MAX_STOCKS_PER_RUN_INCREMENTAL})")
    
    conn.close()
    return need_update

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
        params = f"{tencent_code},{FREQ},,,{DATA_POINTS_FULL},qfq"
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

def get_data_points_to_fetch(processed_new, latest_date):
    """
    Filter new data points that are after latest_date in existing file
    If latest_date is None, return all
    """
    if latest_date is None:
        return processed_new, DATA_POINTS_FULL
    
    # Find all data points after latest_date
    new_data = []
    for item in processed_new:
        date = item[0]
        if date > latest_date:
            new_data.append(item)
    
    return new_data, len(processed_new)

def append_to_file(stock_code, stock_name, new_data, latest_date):
    """
    Append new data points to existing file, don't overwrite
    If file doesn't exist, create new with header
    Format: date,open,close,high,low,change
    Filename: 名称_代码.txt
    """
    # Create directory if not exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    # Sanitize filename - remove all invalid Windows filename characters
    invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    safe_name = stock_name
    for c in invalid_chars:
        safe_name = safe_name.replace(c, '_')
    filename = f"{safe_name}_{stock_code}.txt"
    filepath = os.path.join(DATA_DIR, filename)
    
    # Filter new data (only data after latest_date)
    data_to_write, total_fetched = get_data_points_to_fetch(new_data, latest_date)
    
    if not data_to_write:
        # No new data to add
        return filepath, 0
    
    if latest_date is None:
        # Create new file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("date,open,close,high,low,change_pct\n")
            for item in data_to_write:
                date, open_p, close, high, low, change = item
                line = f"{date},{open_p:.2f},{close:.2f},{high:.2f},{low:.2f},{change:.3f}\n"
                f.write(line)
    else:
        # Append to existing file
        with open(filepath, 'a', encoding='utf-8') as f:
            for item in data_to_write:
                date, open_p, close, high, low, change = item
                line = f"{date},{open_p:.2f},{close:.2f},{high:.2f},{low:.2f},{change:.3f}\n"
                f.write(line)
    
    return filepath, len(data_to_write)

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

def fetch_all_stocks(order):
    """Fetch data incrementally for stocks in this partition - process {BATCH_SIZE} per run"""
    stocks = get_stocks_to_fetch(order)
    total_need_update = len(stocks)
    
    print("=" * 70)
    print(f"A-Share-Get Monthly Data Fetcher - Incremental Parallel ({order})")
    print("A股数据获取 - 月线增量更新（并行）")
    print("=" * 70)
    print(f"Data directory: {DATA_DIR}")
    print(f"Processing {BATCH_SIZE} stocks per run (max {MAX_STOCKS_PER_RUN_INCREMENTAL} total)")
    print("-" * 70)
    
    success_total = 0
    failed_total = 0
    new_points_total = 0
    
    # Process in batches of BATCH_SIZE
    from itertools import islice
    def batch_generator(iterable, batch_size):
        iterator = iter(iterable)
        for first in iterator:
            yield [first] + list(islice(iterator, batch_size - 1))
    
    for batch_idx, batch in enumerate(batch_generator(stocks, BATCH_SIZE), 1):
        print(f"\n>> Batch {batch_idx}, processing {len(batch)} stocks:")
        
        for i, (code, name, market) in enumerate(batch, 1):
            global_i = (batch_idx - 1) * BATCH_SIZE + i
            print(f"  [{global_i}/{total_need_update}] {code} {name}: ", end=' ')
            sys.stdout.flush()
            
            # Get existing file's latest date
            invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
            safe_name = name
            for c in invalid_chars:
                safe_name = safe_name.replace(c, '_')
            filename = f"{safe_name}_{code}.txt"
            filepath = os.path.join(DATA_DIR, filename)
            latest_date = get_latest_date_from_file(filepath)
            
            if latest_date:
                print(f"latest={latest_date}, fetching new data...", end=' ')
            else:
                print("new file, fetching full data...", end=' ')
            sys.stdout.flush()
            
            # Fetch data
            raw_data = fetch_stock_data(code, name)
            
            if raw_data is None:
                print("FAILED")
                failed_total += 1
                continue
            
            # Process data
            processed = process_data(raw_data)
            
            if not processed:
                print("NO DATA")
                failed_total += 1
                continue
            
            # Append new data to file (only add missing)
            filepath, new_count = append_to_file(code, name, processed, latest_date)
            
            if new_count == 0:
                print("no new data")
                # Still update database to mark as updated today
                update_database_last_fetch(code)
                continue
            
            # Update database
            update_database_last_fetch(code)
            
            print(f"OK added {new_count} new points")
            success_total += 1
            new_points_total += new_count
            
            # Add delay to avoid hitting rate limit
            import time
            time.sleep(1.5)
    
    # Final summary
    print("-" * 70)
    print("增量更新完成！")
    print("-" * 70)
    print(f"Partition ({order}):")
    print(f"  - Need update:  {total_need_update}")
    print(f"  - Successfully processed: {success_total}")
    print(f"  - Failed: {failed_total}")
    print(f"  - New data points added: {new_points_total}")
    print(f"Data directory: {DATA_DIR}")
    print("-" * 70)
    print("Database updated with last fetch timestamps")
    print("=" * 70)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:")
        print("  python scripts/month_parallel.py asc   # First half (ascending)")
        print("  python scripts/month_parallel.py desc  # Second half (descending)")
        print("\nRun both in separate processes for parallel incremental fetching!")
        exit(1)
    
    order = sys.argv[1].lower()
    try:
        fetch_all_stocks(order)
    except KeyboardInterrupt:
        print("\n\n- Interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n- Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

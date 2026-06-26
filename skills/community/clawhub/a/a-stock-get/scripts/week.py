#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XI Stock Weekly Data Fetcher - Enhanced Version
羲股票监控系统 - 周线数据获取（增强版）

This script fetches weekly K-line data for stocks from Tencent Finance API.
本脚本从腾讯财经API获取股票的周K线数据。

新增功能：
week.py get [ac] - 获取股票数据
  - ac: 股票代码（支持逗号分隔多个股票）
  - all: 获取所有未更新股票
  - rand: 随机获取5只未更新股票
  - 默认：获取5只未更新股票
"""

import os
import sys
import sqlite3
import requests
import json
import random
import argparse
from datetime import datetime, timedelta

# Fix encoding for Windows console
# 修复Windows控制台编码问题
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Configuration
DB_PATH = "D:\\xistock\\stock.db"
DATA_DIR = "D:\\xistock\\week"
BASE_URL = "https://proxy.finance.qq.com/ifzqgtimg/appstock/app/newfqkline/get"
DATA_POINTS = 800
FREQ = "week"
DEFAULT_LIMIT = 5
TIMESTAMP_FIELD = "week_get"
DATA_TYPE = "周线"

def get_db_connection():
    """Get database connection"""
    if not os.path.exists(DB_PATH):
        print(f"- 数据库未找到: {DB_PATH}")
        print("  请先运行 init_db.py 和 fetch_stocks.py!")
        exit(1)
    return sqlite3.connect(DB_PATH)

def get_stocks_by_codes(stock_codes):
    """Get stocks by specific codes"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 处理逗号分隔的股票代码
    codes = [code.strip() for code in stock_codes.split(',')]
    
    # 构建查询
    placeholders = ','.join(['?'] * len(codes))
    query = f"""
        SELECT code, name, market 
        FROM stocks 
        WHERE code IN ({placeholders}) AND status = 'active'
        ORDER BY code
    """
    
    cursor.execute(query, codes)
    stocks = cursor.fetchall()
    conn.close()
    
    return stocks

def get_all_stocks_to_update(limit=None):
    """Get all stocks that need to be updated (week_get is NULL or old)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 获取当前时间
    current_time = datetime.now()
    
    query = f"""
        SELECT code, name, market 
        FROM stocks 
        WHERE status = 'active' 
        AND ({TIMESTAMP_FIELD} IS NULL OR {TIMESTAMP_FIELD} < ?)
        ORDER BY {TIMESTAMP_FIELD} ASC NULLS FIRST
    """
    
    cursor.execute(query, (current_time,))
    stocks = cursor.fetchall()
    conn.close()
    
    # 应用限制
    if limit and limit > 0:
        stocks = stocks[:limit]
    
    return stocks

def get_random_stocks_to_update(limit=5):
    """Get random stocks that need to be updated"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 获取当前时间
    current_time = datetime.now()
    
    query = f"""
        SELECT code, name, market 
        FROM stocks 
        WHERE status = 'active' 
        AND ({TIMESTAMP_FIELD} IS NULL OR {TIMESTAMP_FIELD} < ?)
    """
    
    cursor.execute(query, (current_time,))
    all_stocks = cursor.fetchall()
    conn.close()
    
    # 随机选择
    if len(all_stocks) > limit:
        stocks = random.sample(all_stocks, limit)
    else:
        stocks = all_stocks
    
    return stocks

def format_stock_code(code):
    """Format stock code for Tencent Finance API (sh600001, sz000001)"""
    if code.startswith('60'):
        return f"sh{code}"
    else:
        return f"sz{code}"

def fetch_stock_data(stock_code, stock_name):
    """Fetch weekly K-line data from Tencent Finance API"""
    try:
        tencent_code = format_stock_code(stock_code)
        params = f"{tencent_code},{FREQ},,,{DATA_POINTS},qfq"
        url = f"{BASE_URL}?_var=kline_{FREQ}qfq&param={params}"
        
        response = requests.get(url, timeout=30)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"- {stock_code} {stock_name}: HTTP {response.status_code}")
            return None
        
        # Response is in format: kline_weekqfq = {...};
        content = response.text
        if '=' in content:
            json_str = content.split('=', 1)[1].rstrip(';')
        else:
            json_str = content
        
        data = json.loads(json_str)
        
        # Data structure: data -> tencent_code -> qfqweek
        if 'data' not in data or tencent_code not in data['data']:
            print(f"- {stock_code} {stock_name}: No data found")
            return None
        
        stock_data = data['data'][tencent_code]
        data_key = f"qfq{FREQ}"
        if data_key not in stock_data:
            print(f"- {stock_code} {stock_name}: No {data_key} found")
            return None
        
        return stock_data[data_key]
        
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
    """Update the week_get timestamp in database to current date"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(f"""
        UPDATE stocks 
        SET {TIMESTAMP_FIELD} = ?
        WHERE code = ?
    """, (current_time, stock_code))
    
    conn.commit()
    conn.close()

def fetch_stocks(stocks):
    """Fetch data for given list of stocks"""
    total = len(stocks)
    
    if total == 0:
        print("没有需要更新的股票")
        return
    
    print("=" * 70)
    print(f"XI Stock {DATA_TYPE.capitalize()} Data Fetcher")
    print(f"羲股票监控系统 - {DATA_TYPE}数据获取")
    print("=" * 70)
    print(f"股票数量: {total}")
    print(f"数据目录: {DATA_DIR}")
    print("-" * 70)
    
    success = 0
    failed = 0
    
    for i, (code, name, market) in enumerate(stocks, 1):
        print(f"[{i}/{total}] 获取 {code} {name}...", end=' ')
        sys.stdout.flush()
        
        # Fetch data
        raw_data = fetch_stock_data(code, name)
        
        if raw_data is None:
            print("失败")
            failed += 1
            continue
        
        # Process data
        bars = raw_data
        processed = process_data(bars)
        
        if not processed:
            print("无数据")
            failed += 1
            continue
        
        # Save to file
        save_to_file(code, name, processed)
        
        # Update database
        update_database_last_fetch(code)
        
        print(f"成功 ({len(processed)} 个数据点)")
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
    print(f"总股票数: {total}")
    print(f"成功获取: {success}")
    print(f"失败: {failed}")
    print(f"数据保存到: {DATA_DIR}")
    print("-" * 70)
    print("数据库已更新最后获取时间戳")
    print("=" * 70)

def fetch_all_stocks_original():
    """Original function to fetch all stocks (backward compatibility)"""
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
    
    fetch_stocks(stocks)

def main():
    """Main function with command line arguments"""
    parser = argparse.ArgumentParser(
        description=f'XI Stock {DATA_TYPE.capitalize()} Data Fetcher - Enhanced Version',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
使用示例:
  传统用法:
    week.py                    - 获取所有活跃股票数据
  
  增强用法:
    week.py get 000001         - 获取单只股票数据
    week.py get 000001,000002  - 获取多只股票数据
    week.py get all            - 获取所有未更新股票
    week.py get all --limit 10 - 获取10只未更新股票
    week.py get rand           - 随机获取5只未更新股票
    week.py get rand --limit 3 - 随机获取3只未更新股票
    week.py get                - 获取5只未更新股票（默认）
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # get command
    get_parser = subparsers.add_parser('get', help='获取股票数据')
    get_parser.add_argument('ac', nargs='?', default='', 
                          help='股票代码(all/rand/股票代码)')
    get_parser.add_argument('--limit', type=int, default=DEFAULT_LIMIT,
                          help=f'获取股票数量限制 (默认: {DEFAULT_LIMIT})')
    
    args = parser.parse_args()
    
    try:
        if not args.command:
            # 传统用法：没有参数时获取所有股票
            print(f"使用传统模式：获取所有活跃股票{DATA_TYPE}数据...")
            fetch_all_stocks_original()
            
        elif args.command == 'get':
            ac = args.ac.strip().lower() if args.ac else ''
            limit = args.limit
            
            if not ac:
                # 默认：获取5只未更新股票
                print(f"未指定股票，获取 {limit} 只未更新股票...")
                stocks = get_all_stocks_to_update(limit)
                fetch_stocks(stocks)
                
            elif ac == 'all':
                # 获取所有未更新股票
                if limit > 0:
                    print(f"获取 {limit} 只未更新股票...")
                    stocks = get_all_stocks_to_update(limit)
                else:
                    print("获取所有未更新股票...")
                    stocks = get_all_stocks_to_update()
                fetch_stocks(stocks)
                
            elif ac == 'rand':
                # 随机获取未更新股票
                print(f"随机获取 {limit} 只未更新股票...")
                stocks = get_random_stocks_to_update(limit)
                fetch_stocks(stocks)
                
            else:
                # 获取指定股票代码
                print(f"获取指定股票: {ac}")
                stocks = get_stocks_by_codes(ac)
                if not stocks:
                    print(f"未找到股票代码: {ac}")
                    return
                fetch_stocks(stocks)
                
    except KeyboardInterrupt:
        print("\n\n- 用户中断")
        exit(1)
    except Exception as e:
        print(f"\n- 错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    main()
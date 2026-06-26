#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Reset and Fetch Tool for XI Stock System
羲股票监控系统数据库重置与数据获取工具

This script resets specific timestamp fields and fetches data for stocks.
本脚本重置数据库中的特定时间戳字段并获取股票数据。
"""

import os
import sys
import sqlite3
import argparse
import requests
import json
import random
from datetime import datetime, timedelta

# Fix encoding for Windows console
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Configuration
DB_PATH = "D:\\xistock\\stock.db"
BASE_URL = "https://proxy.finance.qq.com/ifzqgtimg/appstock/app/newfqkline/get"
DATA_POINTS = 800

def get_db_connection():
    """Get database connection"""
    if not os.path.exists(DB_PATH):
        print(f"- 数据库未找到: {DB_PATH}")
        print("  请先运行 init_db.py 和 fetch_stocks.py!")
        exit(1)
    return sqlite3.connect(DB_PATH)

# ==================== RESET FUNCTIONS ====================

def reset_day_get():
    """Reset day_get field for all stocks"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE stocks 
            SET day_get = NULL
        """)
        
        affected_rows = cursor.rowcount
        conn.commit()
        
        print("=" * 70)
        print("重置 day_get 字段")
        print("=" * 70)
        print(f"已重置 {affected_rows} 只股票的 day_get 字段为 NULL")
        print("所有股票现在都标记为需要更新日线数据")
        print("=" * 70)
        
    except Exception as e:
        print(f"- 重置失败: {e}")
        conn.rollback()
    finally:
        conn.close()

def reset_week_get():
    """Reset week_get field for all stocks"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE stocks 
            SET week_get = NULL
        """)
        
        affected_rows = cursor.rowcount
        conn.commit()
        
        print("=" * 70)
        print("重置 week_get 字段")
        print("=" * 70)
        print(f"已重置 {affected_rows} 只股票的 week_get 字段为 NULL")
        print("所有股票现在都标记为需要更新周线数据")
        print("=" * 70)
        
    except Exception as e:
        print(f"- 重置失败: {e}")
        conn.rollback()
    finally:
        conn.close()

def reset_month_get():
    """Reset month_get field for all stocks"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE stocks 
            SET month_get = NULL
        """)
        
        affected_rows = cursor.rowcount
        conn.commit()
        
        print("=" * 70)
        print("重置 month_get 字段")
        print("=" * 70)
        print(f"已重置 {affected_rows} 只股票的 month_get 字段为 NULL")
        print("所有股票现在都标记为需要更新月线数据")
        print("=" * 70)
        
    except Exception as e:
        print(f"- 重置失败: {e}")
        conn.rollback()
    finally:
        conn.close()

def reset_all():
    """Reset all timestamp fields for all stocks"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE stocks 
            SET day_get = NULL,
                week_get = NULL,
                month_get = NULL
        """)
        
        affected_rows = cursor.rowcount
        conn.commit()
        
        print("=" * 70)
        print("重置所有时间戳字段")
        print("=" * 70)
        print(f"已重置 {affected_rows} 只股票的所有时间戳字段")
        print("重置字段: day_get, week_get, month_get")
        print("所有股票现在都标记为需要更新全部数据")
        print("=" * 70)
        
    except Exception as e:
        print(f"- 重置失败: {e}")
        conn.rollback()
    finally:
        conn.close()

def show_status():
    """Show current database status"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Total stocks
        cursor.execute("SELECT COUNT(*) FROM stocks")
        total = cursor.fetchone()[0]
        
        # Stocks with day_get
        cursor.execute("SELECT COUNT(*) FROM stocks WHERE day_get IS NOT NULL")
        day_updated = cursor.fetchone()[0]
        
        # Stocks with week_get
        cursor.execute("SELECT COUNT(*) FROM stocks WHERE week_get IS NOT NULL")
        week_updated = cursor.fetchone()[0]
        
        # Stocks with month_get
        cursor.execute("SELECT COUNT(*) FROM stocks WHERE month_get IS NOT NULL")
        month_updated = cursor.fetchone()[0]
        
        print("=" * 70)
        print("数据库状态报告")
        print("=" * 70)
        print(f"总股票数: {total}")
        print(f"日线数据已更新: {day_updated} ({day_updated/total*100:.1f}%)")
        print(f"周线数据已更新: {week_updated} ({week_updated/total*100:.1f}%)")
        print(f"月线数据已更新: {month_updated} ({month_updated/total*100:.1f}%)")
        print("=" * 70)
        
    except Exception as e:
        print(f"- 查询失败: {e}")
    finally:
        conn.close()

# ==================== FETCH FUNCTIONS ====================

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

def get_all_stocks_to_update(frequency, limit=None):
    """Get all stocks that need to be updated for specific frequency"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 获取当前时间
    current_time = datetime.now()
    
    # 根据频率确定字段名
    if frequency == 'day':
        timestamp_field = 'day_get'
    elif frequency == 'week':
        timestamp_field = 'week_get'
    elif frequency == 'month':
        timestamp_field = 'month_get'
    else:
        timestamp_field = 'day_get'
    
    query = f"""
        SELECT code, name, market 
        FROM stocks 
        WHERE status = 'active' 
        AND ({timestamp_field} IS NULL OR {timestamp_field} < ?)
        ORDER BY {timestamp_field} ASC NULLS FIRST
    """
    
    cursor.execute(query, (current_time,))
    stocks = cursor.fetchall()
    conn.close()
    
    # 应用限制
    if limit and limit > 0:
        stocks = stocks[:limit]
    
    return stocks

def get_random_stocks_to_update(frequency, limit=5):
    """Get random stocks that need to be updated for specific frequency"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 获取当前时间
    current_time = datetime.now()
    
    # 根据频率确定字段名
    if frequency == 'day':
        timestamp_field = 'day_get'
    elif frequency == 'week':
        timestamp_field = 'week_get'
    elif frequency == 'month':
        timestamp_field = 'month_get'
    else:
        timestamp_field = 'day_get'
    
    query = f"""
        SELECT code, name, market 
        FROM stocks 
        WHERE status = 'active' 
        AND ({timestamp_field} IS NULL OR {timestamp_field} < ?)
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

def fetch_stock_data(stock_code, stock_name, frequency):
    """Fetch K-line data from Tencent Finance API"""
    try:
        tencent_code = format_stock_code(stock_code)
        params = f"{tencent_code},{frequency},,,{DATA_POINTS},qfq"
        url = f"{BASE_URL}?_var=kline_{frequency}qfq&param={params}"
        
        response = requests.get(url, timeout=30)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"- {stock_code} {stock_name}: HTTP {response.status_code}")
            return None
        
        # Response is in format: kline_{frequency}qfq = {...};
        content = response.text
        if '=' in content:
            json_str = content.split('=', 1)[1].rstrip(';')
        else:
            json_str = content
        
        data = json.loads(json_str)
        
        # Data structure: data -> tencent_code -> qfq{frequency}
        if 'data' not in data or tencent_code not in data['data']:
            print(f"- {stock_code} {stock_name}: No data found")
            return None
        
        stock_data = data['data'][tencent_code]
        data_key = f"qfq{frequency}"
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

def save_to_file(stock_code, stock_name, data, frequency):
    """
    Save processed data to file, one data point per line
    Format: date,open,close,high,low,change
    Filename: 名称_代码.txt
    """
    # 确定数据目录
    if frequency == 'day':
        data_dir = "D:\\xistock\\day"
    elif frequency == 'week':
        data_dir = "D:\\xistock\\week"
    elif frequency == 'month':
        data_dir = "D:\\xistock\\month"
    else:
        data_dir = "D:\\xistock\\unknown"
    
    # Create directory if not exists
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Sanitize filename - remove all invalid Windows filename characters
    # Invalid chars: \ / : * ? " < > |
    invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    safe_name = stock_name
    for c in invalid_chars:
        safe_name = safe_name.replace(c, '_')
    filename = f"{safe_name}_{stock_code}.txt"
    filepath = os.path.join(data_dir, filename)
    
    # Write header
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("date,open,close,high,low,change_pct\n")
        for item in data:
            date, open_p, close, high, low, change = item
            line = f"{date},{open_p:.2f},{close:.2f},{high:.2f},{low:.2f},{change:.3f}\n"
            f.write(line)
    
    return filepath

def update_database_last_fetch(stock_code, frequency):
    """Update the timestamp field in database to current date"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 根据频率确定字段名
    if frequency == 'day':
        timestamp_field = 'day_get'
    elif frequency == 'week':
        timestamp_field = 'week_get'
    elif frequency == 'month':
        timestamp_field = 'month_get'
    else:
        timestamp_field = 'day_get'
    
    cursor.execute(f"""
        UPDATE stocks 
        SET {timestamp_field} = ?
        WHERE code = ?
    """, (current_time, stock_code))
    
    conn.commit()
    conn.close()

def fetch_stocks_data(stocks, frequency, data_type):
    """Fetch data for given list of stocks"""
    total = len(stocks)
    
    if total == 0:
        print("没有需要更新的股票")
        return
    
    print("=" * 70)
    print(f"XI Stock {data_type.capitalize()} Data Fetcher")
    print(f"羲股票监控系统 - {data_type}数据获取")
    print("=" * 70)
    print(f"股票数量: {total}")
    print(f"数据频率: {frequency}")
    print("-" * 70)
    
    success = 0
    failed = 0
    
    for i, (code, name, market) in enumerate(stocks, 1):
        print(f"[{i}/{total}] 获取 {code} {name}...", end=' ')
        sys.stdout.flush()
        
        # Fetch data
        raw_data = fetch_stock_data(code, name, frequency)
        
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
        save_to_file(code, name, processed, frequency)
        
        # Update database
        update_database_last_fetch(code, frequency)
        
        print(f"成功 ({len(processed)} 个数据点)")
        success += 1
        
        # Add delay to avoid hitting rate limit
        if i % 10 == 0:
            import time
            time.sleep(1)
    
    # Final summary
    print("-" * 70)
    print("任务完成！")
    print("-" * 70)
    print(f"总股票数: {total}")
    print(f"成功获取: {success}")
    print(f"失败: {failed}")
    print("-" * 70)
    print("数据库已更新最后获取时间戳")
    print("=" * 70)

def fetch_day_data(action, limit=None):
    """Fetch day data based on action"""
    if action == 'all':
        print("获取所有未更新日线股票...")
        stocks = get_all_stocks_to_update('day', limit)
    elif action == 'rand':
        limit = limit or 5
        print(f"随机获取 {limit} 只未更新日线股票...")
        stocks = get_random_stocks_to_update('day', limit)
    else:
        print(f"获取指定日线股票: {action}")
        stocks = get_stocks_by_codes(action)
        if not stocks:
            print(f"未找到股票代码: {action}")
            return
    
    fetch_stocks_data(stocks, 'day', '日线')

def fetch_week_data(action, limit=None):
    """Fetch week data based on action"""
    if action == 'all':
        print("获取所有未更新周线股票...")
        stocks = get_all_stocks_to_update('week', limit)
    elif action == 'rand':
        limit = limit or 5
        print(f"随机获取 {limit} 只未更新周线股票...")
        stocks = get_random_stocks_to_update('week', limit)
    else:
        print(f"获取指定周线股票: {action}")
        stocks = get_stocks_by_codes(action)
        if not stocks:
            print(f"未找到股票代码: {action}")
            return
    
    fetch_stocks_data(stocks, 'week', '周线')

def fetch_month_data(action, limit=None):
    """Fetch month data based on action"""
    if action == 'all':
        print("获取所有未更新月线股票...")
        stocks = get_all_stocks_to_update('month', limit)
    elif action == 'rand':
        limit = limit or 5
        print(f"随机获取 {limit} 只未更新月线股票...")
        stocks = get_random_stocks_to_update('month', limit)
    else:
        print(f"获取指定月线股票: {action}")
        stocks = get_stocks_by_codes(action)
        if not stocks:
            print(f"未找到股票代码: {action}")
            return
    
    fetch_stocks_data(stocks, 'month', '月线')

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Database Reset and Fetch Tool for XI Stock System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  重置功能:
    db_reset.py reset day         - 重置所有股票的day_get字段
    db_reset.py reset week        - 重置所有股票的week_get字段
    db_reset.py reset month       - 重置所有股票的month_get字段
    db_reset.py reset all         - 重置所有时间戳字段
    db_reset.py reset status      - 显示数据库状态
  
  获取功能:
    db_reset.py fetch day 000001         - 获取单只日线股票数据
    db_reset.py fetch day 000001,000002  - 获取多只日线股票数据
    db_reset.py fetch day all            - 获取所有未更新日线股票
    db_reset.py fetch day all --limit 10 - 获取10只未更新日线股票
    db_reset.py fetch day rand           - 随机获取5只未更新日线股票
    db_reset.py fetch day rand --limit 3 - 随机获取3只未更新日线股票
    
    db_reset.py fetch week ...          - 周线数据获取
    db_reset.py fetch month ...         - 月线数据获取
  
注意事项:
  1. 重置后会标记所有股票为需要更新状态
  2. 请谨慎操作，建议在非交易时段进行
  3. 重置后运行相应的数据获取脚本更新数据
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='命令', required=True)
    
    # reset command
    reset_parser = subparsers.add_parser('reset', help='重置数据库字段')
    reset_parser.add_argument('action', 
                           choices=['day', 'week', 'month', 'all', 'status'],
                           help='执行的操作')
    
    # fetch command
    fetch_parser = subparsers.add_parser('fetch', help='获取股票数据')
    fetch_parser.add_argument('frequency', 
                            choices=['day', 'week', 'month'],
                            help='数据频率')
    fetch_parser.add_argument('action', 
                            help='股票代码(all/rand/股票代码)')
    fetch_parser.add_argument('--limit', type=int, 
                            help='获取股票数量限制')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'reset':
            if args.action == 'day':
                reset_day_get()
            elif args.action == 'week':
                reset_week_get()
            elif args.action == 'month':
                reset_month_get()
            elif args.action == 'all':
                reset_all()
            elif args.action == 'status':
                show_status()
                
        elif args.command == 'fetch':
            if args.frequency == 'day':
                fetch_day_data(args.action, args.limit)
            elif args.frequency == 'week':
                fetch_week_data(args.action, args.limit)
            elif args.frequency == 'month':
                fetch_month_data(args.action, args.limit)
            
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
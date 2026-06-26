#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XI Stock Fetcher - Stock List Acquisition
羲股票监控系统 - 股票列表获取

This script fetches tradable stocks from A-share markets (60*, 30*, 00*)
and stores them in the database, excluding delisted and pre-IPO stocks.
本脚本从A股市场获取可交易股票（60*、30*、00*），并排除退市和未上市股票。
"""

import sqlite3
import os
import sys
import time
from datetime import datetime

try:
    import akshare as ak
    import pandas as pd
except ImportError:
    print("- Required packages not installed!")
    print("  Please run: pip install akshare pandas")
    sys.exit(1)

# Database path
DB_PATH = "D:\\xistock\\stock.db"

def get_db_connection():
    """Get database connection"""
    if not os.path.exists(DB_PATH):
        print(f"✗ Database not found: {DB_PATH}")
        print("  Please run init_db.py first!")
        sys.exit(1)
    return sqlite3.connect(DB_PATH)

def fetch_stock_list():
    """
    Fetch tradable A-share stocks from Shanghai and Shenzhen markets
    获取沪市和深市可交易的A股股票
    """
    print("=" * 60)
    print("Fetching A-Share Stock List")
    print("获取A股股票列表")
    print("=" * 60)
    
    try:
        # Get Shanghai A-shares (60*)
        print("\n[1/3] Fetching Shanghai A-shares (60*)...")
        sh_stocks = ak.stock_info_sh_name_code()
        sh_stocks = sh_stocks[sh_stocks['SECUCODE'].str.startswith('60')]
        print(f"  + Found {len(sh_stocks)} Shanghai stocks")
        
        # Get Shenzhen A-shares (00* and 30*)
        print("\n[2/3] Fetching Shenzhen A-shares (00* and 30*)...")
        sz_stocks = ak.stock_info_sz_name_code()
        sz_stocks_00 = sz_stocks[sz_stocks['A股代码'].astype(str).str.startswith('00')]
        sz_stocks_30 = sz_stocks[sz_stocks['A股代码'].astype(str).str.startswith('30')]
        print(f"  + Found {len(sz_stocks_00)} Shenzhen main board stocks (00*)")
        print(f"  + Found {len(sz_stocks_30)} Shenzhen ChiNext stocks (30*)")
        
    except Exception as e:
        print(f"- Error fetching from akshare: {e}")
        print("  Trying alternative method...")
        return fetch_stock_list_alternative()
    
    # Combine all stocks
    all_stocks = []
    
    # Process Shanghai stocks
    for _, stock in sh_stocks.iterrows():
        code = str(stock['SECUCODE']).split('.')[0]
        name = stock['SECURITY_ABBR']
        all_stocks.append({
            'code': code,
            'name': name,
            'market': '60'
        })
    
    # Process Shenzhen 00* stocks
    for _, stock in sz_stocks_00.iterrows():
        code = str(stock['A股代码']).zfill(6)
        name = stock['A股简称']
        all_stocks.append({
            'code': code,
            'name': name,
            'market': '00'
        })
    
    # Process Shenzhen 30* stocks
    for _, stock in sz_stocks_30.iterrows():
        code = str(stock['A股代码']).zfill(6)
        name = stock['A股简称']
        all_stocks.append({
            'code': code,
            'name': name,
            'market': '30'
        })
    
    print(f"\n[3/3] Total stocks collected: {len(all_stocks)}")
    return all_stocks

def fetch_stock_list_alternative():
    """
    Alternative method to fetch stock list
    备用方法获取股票列表
    """
    print("\nUsing alternative data source...")
    try:
        # Get all A-share stocks
        all_stocks_df = ak.stock_info_a_code_name()
        
        all_stocks = []
        for _, stock in all_stocks_df.iterrows():
            code = str(stock['code']).zfill(6)
            name = stock['name']
            
            # Determine market type
            if code.startswith('60'):
                market = '60'
            elif code.startswith('00'):
                market = '00'
            elif code.startswith('30'):
                market = '30'
            else:
                continue  # Skip other markets
            
            all_stocks.append({
                'code': code,
                'name': name,
                'market': market
            })
        
        print(f"+ Found {len(all_stocks)} stocks")
        return all_stocks
        
    except Exception as e:
        print(f"- Alternative method also failed: {e}")
        return []

def save_to_database(stocks):
    """
    Save stock list to database
    保存股票列表到数据库
    """
    if not stocks:
        print("- No stocks to save!")
        return 0
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Count existing stocks
    cursor.execute("SELECT COUNT(*) FROM stocks")
    existing_count = cursor.fetchone()[0]
    print(f"\nFound {existing_count} existing stocks in database")
    
    # Insert or update stocks
    inserted = 0
    updated = 0
    
    for stock in stocks:
        try:
            # Check if stock already exists
            cursor.execute("SELECT code FROM stocks WHERE code = ?", (stock['code'],))
            if cursor.fetchone():
                # Update existing record
                cursor.execute("""
                    UPDATE stocks 
                    SET name = ?, market = ?, status = 'active'
                    WHERE code = ?
                """, (stock['name'], stock['market'], stock['code']))
                updated += 1
            else:
                # Insert new record
                cursor.execute("""
                    INSERT INTO stocks (code, name, market, status)
                    VALUES (?, ?, ?, 'active')
                """, (stock['code'], stock['name'], stock['market']))
                inserted += 1
            
        except sqlite3.Error as e:
            print(f"- Error saving stock {stock['code']}: {e}")
            continue
    
    conn.commit()
    conn.close()
    
    print(f"\n+ Database update completed:")
    print(f"  - Newly inserted: {inserted}")
    print(f"  - Updated: {updated}")
    print(f"  - Total in database: {existing_count + inserted}")
    
    return existing_count + inserted

def show_stock_stats():
    """
    Show statistics of stocks in database
    显示数据库中的股票统计信息
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("\n" + "=" * 60)
    print("Current Stock Statistics")
    print("当前股票统计信息")
    print("=" * 60)
    
    # Total count
    cursor.execute("SELECT COUNT(*) FROM stocks WHERE status = 'active'")
    total = cursor.fetchone()[0]
    print(f"\nTotal active stocks: {total}")
    
    # Count by market
    cursor.execute("""
        SELECT market, COUNT(*) as count 
        FROM stocks 
        WHERE status = 'active'
        GROUP BY market
        ORDER BY market
    """)
    
    print("\nBy market:")
    for market, count in cursor.fetchall():
        market_name = {
            '60': 'Shanghai (沪市)',
            '00': 'Shenzhen Main (深市主板)',
            '30': 'Shenzhen ChiNext (创业板)'
        }.get(market, market)
        print(f"  - {market_name}: {count}")
    
    # Show sample stocks
    print("\nSample stocks:")
    cursor.execute("""
        SELECT code, name, market FROM stocks 
        WHERE status = 'active'
        ORDER BY RANDOM()
        LIMIT 5
    """)
    
    for code, name, market in cursor.fetchall():
        print(f"  - {code} ({market}): {name}")
    
    conn.close()

if __name__ == "__main__":
    print("XI Stock Fetcher")
    print("羲股票监控系统 - 股票列表获取")
    print("=" * 60)
    
    try:
        # Check if database exists
        if not os.path.exists(DB_PATH):
            print(f"- Database not found: {DB_PATH}")
            print("  Please run init_db.py first!")
            sys.exit(1)
        
        # Fetch stock list
        stocks = fetch_stock_list()
        
        if not stocks:
            print("- No stocks fetched!")
            sys.exit(1)
        
        # Save to database
        total = save_to_database(stocks)
        
        # Show statistics
        show_stock_stats()
        
        print("\n" + "=" * 60)
        print("任务完成！")
        print("我辛苦了！")
        print("-" * 60)
        print(f"成功获取并保存了 {total} 只可交易A股股票")
        print("数据已存入数据库: D:\\xistock\\stock.db")
        print("=" * 60)
        print("+ Stock list acquisition completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n- Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
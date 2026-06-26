#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股日线数据获取脚本 / A-Share Daily Data Fetching Script
数据源：东方财富网 / Data Source: East Money

功能 / Function:
    - 获取A股日线K线数据
    - Fetch A-share daily K-line data
    - 存储到SQLite数据库
    - Store to SQLite database
"""

import requests
import sqlite3
import os
from datetime import datetime, timedelta
import time

# 数据库路径 / Database path
DB_PATH = os.path.expanduser("~/.openclaw/workspace/a-stock/data.db")

def init_db():
    """
    初始化数据库 / Initialize database
    创建日线数据表 / Create daily data table
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS daily_data (
        date TEXT, code TEXT, name TEXT, open REAL, high REAL, 
        low REAL, close REAL, volume REAL, amount REAL,
        PRIMARY KEY (date, code)
    )''')
    conn.commit()
    return conn

def get_stock_code(code):
    """
    标准化股票代码 / Normalize stock code
    补齐6位 / Pad to 6 digits
    """
    code = code.strip()
    if len(code) == 6:
        return code
    return code.zfill(6)

def fetch_eastmoney(code, days=250):
    """
    从东方财富获取数据 / Fetch data from East Money
    参数 / Parameters:
        code: 股票代码 (stock code)
        days: 获取天数 (number of days)
    返回 / Returns: K线数据列表 (K-line data list)
    """
    # API地址 / API URL
    base_url = f"http://push2his.eastmoney.com/api/qt/stock/kline/get"
    params = {
        "secid": f"1.{code}",  # 1=上海 0=深圳 / 1=Shanghai 0=Shenzhen
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
        "klt": "101",  # 日K / Daily K
        "fqt": "1",    # 前复权 / Forward adjusted
        "end": "20500101",
        "lmt": days,
    }
    try:
        resp = requests.get(base_url, params=params, timeout=10)
        data = resp.json()
        if data.get("data") and data["data"].get("klines"):
            return parse_klines(code, data["data"]["klines"])
    except Exception as e:
        print(f"获取失败 / Fetch failed: {e}")
    return []

def parse_klines(code, klines):
    """
    解析K线数据 / Parse K-line data
    将原始字符串转换为字典 / Convert raw strings to dict
    """
    result = []
    for line in klines:
        fields = line.split(",")
        result.append({
            "date": fields[0],
            "code": code,
            "open": float(fields[1]),
            "close": float(fields[2]),
            "high": float(fields[3]),
            "low": float(fields[4]),
            "volume": float(fields[5]),
            "amount": float(fields[6]) if len(fields) > 6 else 0,
        })
    return result

def save_data(conn, data):
    """
    保存数据到数据库 / Save data to database
    使用INSERT OR REPLACE防止重复 / Use INSERT OR REPLACE to avoid duplicates
    """
    c = conn.cursor()
    for row in data:
        c.execute('''INSERT OR REPLACE INTO daily_data 
            (date, code, open, high, low, close, volume, amount)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (row["date"], row["code"], row["open"], row["high"], 
             row["low"], row["close"], row["volume"], row["amount"]))
    conn.commit()
    print(f"已保存 {len(data)} 条数据 / Saved {len(data)} records")

def main():
    """
    主函数 / Main function
    命令行入口 / CLI entry point
    """
    import argparse
    parser = argparse.ArgumentParser(description='A股数据获取 / A-Share Data Fetcher')
    parser.add_argument("--stock", default="600519", help="股票代码 / Stock code")
    parser.add_argument("--days", type=int, default=250, help="获取天数 / Number of days")
    args = parser.parse_args()
    
    conn = init_db()
    code = get_stock_code(args.stock)
    print(f"获取 {code} 最近 {args.days} 天数据... / Fetching {code} last {args.days} days...")
    
    data = fetch_eastmoney(code, args.days)
    if data:
        save_data(conn, data)
        print("完成! / Done!")
    else:
        print("未获取到数据 / No data fetched")

if __name__ == "__main__":
    main()

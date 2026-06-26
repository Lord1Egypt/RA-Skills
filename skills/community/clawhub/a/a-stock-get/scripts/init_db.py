#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XI Stock Database Initialization Script
羲股票监控系统数据库初始化脚本

This script initializes the SQLite database and creates the stocks table.
本脚本初始化 SQLite 数据库并创建股票列表表。
"""

import sqlite3
import os
from datetime import datetime

# Database path
DB_DIR = "D:\\xistock"
DB_PATH = os.path.join(DB_DIR, "stock.db")

def init_database():
    """Initialize database and create tables"""
    
    # Create directory if not exists
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
        print(f"+ Created directory: {DB_DIR}")
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create stocks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stocks (
            code TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            market TEXT NOT NULL,
            day_get TIMESTAMP,
            week_get TIMESTAMP,
            month_get TIMESTAMP,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create index for faster queries
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_market ON stocks(market)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_status ON stocks(status)
    ''')
    
    conn.commit()
    conn.close()
    
    print(f"+ Database initialized successfully: {DB_PATH}")
    print("+ Table 'stocks' created with columns:")
    print("  - code: Stock code (PRIMARY KEY)")
    print("  - name: Stock name")
    print("  - market: Market type (60/30/00)")
    print("  - day_get: Last daily data fetch time")
    print("  - week_get: Last weekly data fetch time")
    print("  - month_get: Last monthly data fetch time")
    print("  - status: Stock status (active/delisted)")
    print("  - created_at: Record creation time")

if __name__ == "__main__":
    print("=" * 60)
    print("XI Stock Database Initialization")
    print("羲股票监控系统数据库初始化")
    print("=" * 60)
    print(f"Database path: {DB_PATH}")
    print("-" * 60)
    
    try:
        init_database()
        print("-" * 60)
        print("任务完成！")
        print("我辛苦了！")
        print("-" * 60)
        print("+ Database initialized at: D:\\xistock\\stock.db")
        print("+ Initialization completed successfully!")
    except Exception as e:
        print(f"- Error: {e}")
        exit(1)
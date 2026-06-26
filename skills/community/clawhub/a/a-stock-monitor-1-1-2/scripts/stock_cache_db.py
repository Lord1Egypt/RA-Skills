#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股数据缓存管理 - SQLite数据库
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

DB_PATH = '/Users/jamemei/.openclaw/workspace/crypto_quant_sim/stock-monitor/stock_cache.db'

class StockCache:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.conn = None
        self._init_db()
    
    def _init_db(self):
        """初始化数据库表"""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        
        # 股票基础信息表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stocks (
                code TEXT PRIMARY KEY,
                name TEXT,
                price REAL,
                change_pct REAL,
                volume REAL,
                amount REAL,
                update_time TIMESTAMP
            )
        ''')
        
        # 主力资金表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fund_flow (
                code TEXT PRIMARY KEY,
                main_in REAL,
                retail_in REAL,
                main_ratio REAL,
                update_time TIMESTAMP
            )
        ''')
        
        # 龙虎榜表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lhb (
                code TEXT PRIMARY KEY,
                buy_amount REAL,
                sell_amount REAL,
                net_amount REAL,
                update_time TIMESTAMP
            )
        ''')
        
        # 技术指标表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tech_indicators (
                code TEXT PRIMARY KEY,
                ma5 REAL,
                ma10 REAL,
                ma20 REAL,
                rsi REAL,
                macd REAL,
                dif REAL,
                dea REAL,
                update_time TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def save_stocks(self, stocks_data: List[Dict]):
        """批量保存股票数据"""
        cursor = self.conn.cursor()
        now = datetime.now()
        
        for stock in stocks_data:
            cursor.execute('''
                INSERT OR REPLACE INTO stocks 
                (code, name, price, change_pct, volume, amount, update_time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                stock['code'],
                stock['name'],
                stock['price'],
                stock['change_pct'],
                stock.get('volume', 0),
                stock.get('amount', 0),
                now
            ))
        
        self.conn.commit()
    
    def get_stock(self, code: str) -> Optional[Dict]:
        """获取单只股票数据"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM stocks WHERE code = ?', (code,))
        row = cursor.fetchone()
        
        if row:
            return {
                'code': row[0],
                'name': row[1],
                'price': row[2],
                'change_pct': row[3],
                'volume': row[4],
                'amount': row[5],
                'update_time': row[6]
            }
        return None
    
    def get_all_stocks(self, max_age_minutes=30) -> List[Dict]:
        """获取所有股票（过期数据会被过滤）"""
        cursor = self.conn.cursor()
        cutoff = datetime.now() - timedelta(minutes=max_age_minutes)
        
        cursor.execute('''
            SELECT code, name, price, change_pct, volume, amount, update_time
            FROM stocks
            WHERE update_time > ?
            ORDER BY change_pct DESC
        ''', (cutoff,))
        
        stocks = []
        for row in cursor.fetchall():
            stocks.append({
                'code': row[0],
                'name': row[1],
                'price': row[2],
                'change_pct': row[3],
                'volume': row[4],
                'amount': row[5],
                'update_time': row[6]
            })
        
        return stocks
    
    def save_fund_flow(self, code: str, data: Dict):
        """保存主力资金数据"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO fund_flow
            (code, main_in, retail_in, main_ratio, update_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            code,
            data['main_in'],
            data['retail_in'],
            data['main_ratio'],
            datetime.now()
        ))
        self.conn.commit()
    
    def get_fund_flow(self, code: str, max_age_hours=24) -> Optional[Dict]:
        """获取主力资金数据"""
        cursor = self.conn.cursor()
        cutoff = datetime.now() - timedelta(hours=max_age_hours)
        
        cursor.execute('''
            SELECT main_in, retail_in, main_ratio, update_time
            FROM fund_flow
            WHERE code = ? AND update_time > ?
        ''', (code, cutoff))
        
        row = cursor.fetchone()
        if row:
            return {
                'main_in': row[0],
                'retail_in': row[1],
                'main_ratio': row[2],
                'update_time': row[3]
            }
        return None
    
    def save_tech_indicators(self, code: str, data: Dict):
        """保存技术指标数据"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO tech_indicators
            (code, ma5, ma10, ma20, rsi, macd, dif, dea, update_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            code,
            data.get('ma5'),
            data.get('ma10'),
            data.get('ma20'),
            data.get('rsi'),
            data.get('macd'),
            data.get('macd_dif'),
            data.get('macd_dea'),
            datetime.now()
        ))
        self.conn.commit()
    
    def get_tech_indicators(self, code: str, max_age_hours=24) -> Optional[Dict]:
        """获取技术指标数据"""
        cursor = self.conn.cursor()
        cutoff = datetime.now() - timedelta(hours=max_age_hours)
        
        cursor.execute('''
            SELECT ma5, ma10, ma20, rsi, macd, dif, dea, update_time
            FROM tech_indicators
            WHERE code = ? AND update_time > ?
        ''', (code, cutoff))
        
        row = cursor.fetchone()
        if row:
            return {
                'ma5': row[0],
                'ma10': row[1],
                'ma20': row[2],
                'rsi': row[3],
                'macd': row[4],
                'dif': row[5],
                'dea': row[6],
                'update_time': row[7]
            }
        return None
    
    def save_lhb(self, code: str, data: Dict):
        """保存龙虎榜数据"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO lhb
            (code, buy_amount, sell_amount, net_amount, update_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            code,
            data.get('buy_amount', 0),
            data.get('sell_amount', 0),
            data.get('net_amount', 0),
            datetime.now()
        ))
        self.conn.commit()
    
    def get_lhb(self, code: str, max_age_hours=24) -> Optional[Dict]:
        """获取龙虎榜数据"""
        cursor = self.conn.cursor()
        cutoff = datetime.now() - timedelta(hours=max_age_hours)
        
        cursor.execute('''
            SELECT buy_amount, sell_amount, net_amount, update_time
            FROM lhb
            WHERE code = ? AND update_time > ?
        ''', (code, cutoff))
        
        row = cursor.fetchone()
        if row:
            return {
                'buy_amount': row[0],
                'sell_amount': row[1],
                'net_amount': row[2],
                'update_time': row[3]
            }
        return None
    
    def get_cache_stats(self) -> Dict:
        """获取缓存统计信息"""
        cursor = self.conn.cursor()
        
        # 股票数量
        cursor.execute('SELECT COUNT(*) FROM stocks')
        stock_count = cursor.fetchone()[0]
        
        # 最新更新时间
        cursor.execute('SELECT MAX(update_time) FROM stocks')
        latest_update = cursor.fetchone()[0]
        
        # 资金流数据量
        cursor.execute('SELECT COUNT(*) FROM fund_flow')
        fund_count = cursor.fetchone()[0]
        
        return {
            'stock_count': stock_count,
            'latest_update': latest_update,
            'fund_flow_count': fund_count
        }
    
    def clear_old_data(self, days=7):
        """清理N天前的旧数据"""
        cursor = self.conn.cursor()
        cutoff = datetime.now() - timedelta(days=days)
        
        cursor.execute('DELETE FROM stocks WHERE update_time < ?', (cutoff,))
        cursor.execute('DELETE FROM fund_flow WHERE update_time < ?', (cutoff,))
        cursor.execute('DELETE FROM lhb WHERE update_time < ?', (cutoff,))
        
        self.conn.commit()
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()


# ============== 测试代码 ==============

def test_cache():
    print("🔍 测试SQLite缓存...")
    
    cache = StockCache()
    
    # 测试1: 保存数据
    print("\n1️⃣ 测试保存数据...")
    test_stocks = [
        {'code': '601318', 'name': '中国平安', 'price': 45.67, 'change_pct': 2.3, 'volume': 1000000, 'amount': 45670000},
        {'code': '600519', 'name': '贵州茅台', 'price': 1680.0, 'change_pct': -1.2, 'volume': 50000, 'amount': 84000000},
    ]
    cache.save_stocks(test_stocks)
    print("✅ 保存成功")
    
    # 测试2: 读取数据
    print("\n2️⃣ 测试读取数据...")
    stock = cache.get_stock('601318')
    if stock:
        print(f"✅ {stock['name']}: ¥{stock['price']} ({stock['change_pct']:+.2f}%)")
    
    # 测试3: 统计信息
    print("\n3️⃣ 缓存统计:")
    stats = cache.get_cache_stats()
    print(f"   股票数量: {stats['stock_count']}")
    print(f"   最新更新: {stats['latest_update']}")
    
    cache.close()
    print("\n✅ 测试完成!")


if __name__ == '__main__':
    test_cache()

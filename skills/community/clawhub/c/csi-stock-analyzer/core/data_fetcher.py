#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据获取模块 - 从公开数据源获取股票数据、新闻、财报等信息
"""

import os
import json
import time
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union

class DataFetcher:
    def __init__(self, cache_dir: str = None):
        self.cache_dir = cache_dir or os.path.join(os.path.dirname(__file__), '../data/cache')
        os.makedirs(self.cache_dir, exist_ok=True)
        self.tavily_api_key = os.getenv('TAVILY_API_KEY', '')
        
    def get_stock_code(self, query: str) -> str:
        """
        根据公司名称或代码获取标准股票代码
        :param query: 公司名称或股票代码
        :return: 标准股票代码（带市场前缀）
        """
        # 简单的代码格式化逻辑
        query = str(query).strip()
        if query.isdigit():
            if len(query) == 6:
                if query.startswith('6'):
                    return f'SH{query}'
                elif query.startswith(('0', '3')):
                    return f'SZ{query}'
            return query
        # 如果是名称，这里需要调用搜索接口，暂时返回占位符
        return query
    
    def get_historical_data(self, stock_code: str, days: int = 120) -> pd.DataFrame:
        """
        获取股票历史行情数据
        :param stock_code: 股票代码
        :param days: 获取天数
        :return: DataFrame包含OHLCV数据
        """
        # 这里应该调用实际的行情API，暂时返回模拟数据
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        dates = pd.date_range(start=start_date, end=end_date, freq='B')
        data = {
            'date': dates,
            'open': np.random.normal(10, 2, len(dates)).cumsum() + 50,
            'high': np.random.normal(10, 2, len(dates)).cumsum() + 52,
            'low': np.random.normal(10, 2, len(dates)).cumsum() + 48,
            'close': np.random.normal(10, 2, len(dates)).cumsum() + 50,
            'volume': np.random.randint(1000000, 10000000, len(dates))
        }
        
        df = pd.DataFrame(data)
        df.set_index('date', inplace=True)
        return df
    
    def get_technical_indicators(self, stock_code: str, days: int = 120) -> Dict:
        """
        获取技术指标数据（MACD、KDJ、RSI、EMA）
        :param stock_code: 股票代码
        :param days: 分析天数
        :return: 包含各指标的字典
        """
        df = self.get_historical_data(stock_code, days)
        
        # 计算EMA
        df['ema12'] = df['close'].ewm(span=12, adjust=False).mean()
        df['ema26'] = df['close'].ewm(span=26, adjust=False).mean()
        
        # 计算MACD
        df['dif'] = df['ema12'] - df['ema26']
        df['dea'] = df['dif'].ewm(span=9, adjust=False).mean()
        df['macd'] = 2 * (df['dif'] - df['dea'])
        
        # 计算KDJ
        low_list = df['low'].rolling(9, min_periods=9).min()
        high_list = df['high'].rolling(9, min_periods=9).max()
        rsv = (df['close'] - low_list) / (high_list - low_list) * 100
        df['k'] = rsv.ewm(com=2, adjust=False).mean()
        df['d'] = df['k'].ewm(com=2, adjust=False).mean()
        df['j'] = 3 * df['k'] - 2 * df['d']
        
        # 计算RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # 计算各周期EMA
        df['ema5'] = df['close'].ewm(span=5, adjust=False).mean()
        df['ema10'] = df['close'].ewm(span=10, adjust=False).mean()
        df['ema20'] = df['close'].ewm(span=20, adjust=False).mean()
        df['ema60'] = df['close'].ewm(span=60, adjust=False).mean()
        
        latest = df.iloc[-1]
        prev = df.iloc[-2] if len(df) > 1 else latest
        
        return {
            'macd': {
                'dif': latest['dif'],
                'dea': latest['dea'],
                'macd': latest['macd'],
                'golden_cross': (prev['dif'] <= prev['dea']) and (latest['dif'] > latest['dea']),
                'death_cross': (prev['dif'] >= prev['dea']) and (latest['dif'] < latest['dea']),
                'trend': 'up' if latest['macd'] > 0 else 'down'
            },
            'kdj': {
                'k': latest['k'],
                'd': latest['d'],
                'j': latest['j'],
                'golden_cross': (prev['k'] <= prev['d']) and (latest['k'] > latest['d']),
                'death_cross': (prev['k'] >= prev['d']) and (latest['k'] < latest['d']),
                'oversold': latest['j'] < 20,
                'overbought': latest['j'] > 80
            },
            'rsi': {
                'rsi14': latest['rsi'],
                'oversold': latest['rsi'] < 30,
                'overbought': latest['rsi'] > 70,
                'trend': 'up' if latest['rsi'] > prev['rsi'] else 'down'
            },
            'ema': {
                'ema5': latest['ema5'],
                'ema10': latest['ema10'],
                'ema20': latest['ema20'],
                'ema60': latest['ema60'],
                'bullish_arrangement': latest['close'] > latest['ema20'] > latest['ema60'],
                'bearish_arrangement': latest['close'] < latest['ema20'] < latest['ema60'],
                'price_above_ema20': latest['close'] > latest['ema20'],
                'price_above_ema60': latest['close'] > latest['ema60']
            },
            'price': latest['close'],
            'data': df
        }
    
    def search_company_news(self, company_name: str, days: int = 30) -> List[Dict]:
        """
        搜索公司相关新闻
        :param company_name: 公司名称
        :param days: 搜索最近多少天的新闻
        :return: 新闻列表
        """
        if not self.tavily_api_key:
            return []
            
        try:
            url = "https://api.tavily.com/search"
            headers = {"Content-Type": "application/json"}
            payload = {
                "api_key": self.tavily_api_key,
                "query": f"{company_name} 新闻 公告 2026",
                "search_depth": "advanced",
                "topic": "news",
                "days": days,
                "max_results": 20
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                return data.get('results', [])
        except Exception as e:
            print(f"搜索新闻失败: {e}")
        
        return []
    
    def get_financial_report(self, stock_code: str) -> Dict:
        """
        获取公司财务报表数据
        :param stock_code: 股票代码
        :return: 财务数据字典
        """
        # 这里应该调用财务数据API，暂时返回模拟数据
        return {
            'quarterly': {
                'revenue': {
                    'current': 1000000000,
                    'yoy_growth': 0.15,
                    'qoq_growth': 0.05
                },
                'net_profit': {
                    'current': 200000000,
                    'yoy_growth': 0.25,
                    'qoq_growth': 0.08
                },
                'operating_cash_flow': 180000000
            },
            'annual': {
                'revenue': 3800000000,
                'yoy_growth': 0.12,
                'net_profit': 720000000,
                'yoy_growth': 0.18
            },
            'ratios': {
                'roe': 0.15,
                'roe_ttm': 0.16,
                'deduct_roe': 0.14,
                'gross_margin': 0.45,
                'net_margin': 0.18,
                'asset_liability_ratio': 0.45,
                'current_ratio': 2.3,
                'quick_ratio': 1.8,
                'interest_bearing_debt': 500000000,
                'cash_to_debt_ratio': 2.1,
                'net_profit_cash_ratio': 0.9,
                'peg': 1.2,
                'free_cash_flow_per_share': 2.5
            },
            'rd_expense': {
                'annual': 380000000,
                'revenue_ratio': 0.10,
                'yoy_growth': 0.22
            },
            'management': {
                'stability': 'stable',
                'recent_changes': [],
                'outlook': 'positive',
                'strategy': 'focus on R&D and market expansion'
            }
        }
    
    def get_holder_changes(self, stock_code: str) -> Dict:
        """
        获取股东变动信息
        :param stock_code: 股票代码
        :return: 股东变动数据
        """
        return {
            'institutional_holding': {
                'ratio': 0.45,
                'qoq_change': 0.02,
                'recent_increase': True
            },
            'management_holding': {
                'total_ratio': 0.25,
                'recent_changes': [
                    {'name': '张三', 'position': '董事长', 'change': '减持', 'amount': '50万股', 'date': '2026-02-15'},
                    {'name': '李四', 'position': 'CEO', 'change': '增持', 'amount': '20万股', 'date': '2026-02-20'}
                ]
            },
            'short_selling': {
                'has_short_report': False,
                'short_ratio': 0.02,
                'recent_increase': False
            }
        }

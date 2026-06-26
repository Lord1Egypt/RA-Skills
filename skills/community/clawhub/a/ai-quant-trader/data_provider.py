#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据提供模块 - 集成AKShare获取实时和历史数据
"""

import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
import os

class DataProvider:
    """数据提供器（AKShare封装）"""
    
    def __init__(self, cache_dir="data_cache"):
        self.cache_dir = os.path.join(os.path.dirname(__file__), cache_dir)
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # 缓存配置
        self.cache_expiry = {
            'realtime': 60,  # 实时数据缓存60秒
            'daily': 3600,   # 日线数据缓存1小时
            'minute': 300,   # 分钟数据缓存5分钟
        }
        
        print("✅ 数据提供器初始化完成（AKShare）")
    
    def get_cache_key(self, data_type, symbol, **kwargs):
        """生成缓存键"""
        key_parts = [data_type, symbol]
        for k, v in sorted(kwargs.items()):
            key_parts.append(f"{k}={v}")
        return "_".join(key_parts) + ".json"
    
    def is_cache_valid(self, cache_file, expiry_seconds):
        """检查缓存是否有效"""
        if not os.path.exists(cache_file):
            return False
        
        file_mtime = os.path.getmtime(cache_file)
        current_time = time.time()
        
        return (current_time - file_mtime) < expiry_seconds
    
    def save_to_cache(self, cache_file, data):
        """保存到缓存"""
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"缓存保存失败: {e}")
            return False
    
    def load_from_cache(self, cache_file):
        """从缓存加载"""
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"缓存加载失败: {e}")
            return None
    
    def get_current_price(self, symbol):
        """获取当前价格（简化版）"""
        try:
            # 尝试获取实时数据
            cache_key = self.get_cache_key('realtime', symbol)
            cache_file = os.path.join(self.cache_dir, cache_key)
            
            # 检查缓存
            if self.is_cache_valid(cache_file, self.cache_expiry['realtime']):
                cached_data = self.load_from_cache(cache_file)
                if cached_data and 'price' in cached_data:
                    return cached_data['price']
            
            # 从AKShare获取实时行情
            try:
                # 获取沪深京A股实时行情
                df = ak.stock_zh_a_spot_em()
                
                # 查找指定股票
                if symbol.startswith('6'):
                    symbol_with_market = f"sh{symbol}"
                elif symbol.startswith('0') or symbol.startswith('3'):
                    symbol_with_market = f"sz{symbol}"
                else:
                    symbol_with_market = symbol
                
                # 在数据框中查找
                stock_data = df[df['代码'] == symbol]
                if not stock_data.empty:
                    price = float(stock_data.iloc[0]['最新价'])
                    
                    # 缓存结果
                    cache_data = {
                        'price': price,
                        'symbol': symbol,
                        'timestamp': datetime.now().isoformat(),
                        'data_source': 'akshare'
                    }
                    self.save_to_cache(cache_file, cache_data)
                    
                    return price
                
            except Exception as e:
                print(f"AKShare实时数据获取失败: {e}")
            
            # 如果实时数据失败，尝试获取日线数据的最新收盘价
            return self.get_latest_close_price(symbol)
            
        except Exception as e:
            print(f"获取当前价格失败: {e}")
            return None
    
    def get_latest_close_price(self, symbol):
        """获取最新收盘价"""
        try:
            # 获取最近5天的历史数据
            end_date = datetime.now().strftime('%Y%m%d')
            start_date = (datetime.now() - timedelta(days=10)).strftime('%Y%m%d')
            
            cache_key = self.get_cache_key('daily', symbol, start=start_date, end=end_date)
            cache_file = os.path.join(self.cache_dir, cache_key)
            
            # 检查缓存
            if self.is_cache_valid(cache_file, self.cache_expiry['daily']):
                cached_data = self.load_from_cache(cache_file)
                if cached_data and 'data' in cached_data:
                    df = pd.DataFrame(cached_data['data'])
                    if not df.empty:
                        return float(df.iloc[-1]['收盘'])
            
            # 从AKShare获取历史数据
            try:
                df = ak.stock_zh_a_hist(
                    symbol=symbol,
                    period="daily",
                    start_date=start_date,
                    end_date=end_date,
                    adjust=""
                )
                
                if not df.empty:
                    latest_close = float(df.iloc[-1]['收盘'])
                    
                    # 缓存结果
                    cache_data = {
                        'data': df.to_dict('records'),
                        'symbol': symbol,
                        'timestamp': datetime.now().isoformat()
                    }
                    self.save_to_cache(cache_file, cache_data)
                    
                    return latest_close
                
            except Exception as e:
                print(f"AKShare历史数据获取失败: {e}")
            
            return None
            
        except Exception as e:
            print(f"获取最新收盘价失败: {e}")
            return None
    
    def get_historical_data(self, symbol, start_date, end_date, period="daily"):
        """获取历史数据"""
        try:
            cache_key = self.get_cache_key('historical', symbol, start=start_date, end=end_date, period=period)
            cache_file = os.path.join(self.cache_dir, cache_key)
            
            # 检查缓存
            if self.is_cache_valid(cache_file, self.cache_expiry['daily']):
                cached_data = self.load_from_cache(cache_file)
                if cached_data and 'data' in cached_data:
                    return pd.DataFrame(cached_data['data'])
            
            # 从AKShare获取数据
            df = ak.stock_zh_a_hist(
                symbol=symbol,
                period=period,
                start_date=start_date,
                end_date=end_date,
                adjust=""
            )
            
            if not df.empty:
                # 缓存结果
                cache_data = {
                    'data': df.to_dict('records'),
                    'symbol': symbol,
                    'start_date': start_date,
                    'end_date': end_date,
                    'period': period,
                    'timestamp': datetime.now().isoformat()
                }
                self.save_to_cache(cache_file, cache_data)
            
            return df
            
        except Exception as e:
            print(f"获取历史数据失败: {e}")
            return pd.DataFrame()
    
    def get_stock_info(self, symbol):
        """获取股票基本信息"""
        try:
            cache_key = self.get_cache_key('info', symbol)
            cache_file = os.path.join(self.cache_dir, cache_key)
            
            # 检查缓存（股票信息变化慢，缓存1天）
            if self.is_cache_valid(cache_file, 86400):
                cached_data = self.load_from_cache(cache_file)
                if cached_data:
                    return cached_data
            
            # 从AKShare获取股票信息
            try:
                # 使用东方财富个股信息接口
                df = ak.stock_individual_info_em(symbol=symbol)
                
                if not df.empty:
                    info = {
                        'symbol': symbol,
                        'name': df[df['item'] == '股票简称']['value'].iloc[0] if not df[df['item'] == '股票简称'].empty else symbol,
                        'industry': df[df['item'] == '所属行业']['value'].iloc[0] if not df[df['item'] == '所属行业'].empty else '未知',
                        'market': '上海' if symbol.startswith('6') else '深圳',
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    # 缓存结果
                    self.save_to_cache(cache_file, info)
                    
                    return info
                
            except Exception as e:
                print(f"AKShare股票信息获取失败: {e}")
            
            # 返回简化信息
            info = {
                'symbol': symbol,
                'name': symbol,
                'industry': '未知',
                'market': '上海' if symbol.startswith('6') else '深圳',
                'timestamp': datetime.now().isoformat()
            }
            
            return info
            
        except Exception as e:
            print(f"获取股票信息失败: {e}")
            return {
                'symbol': symbol,
                'name': symbol,
                'industry': '未知',
                'market': '未知'
            }
    
    def get_realtime_quotes(self, symbols=None):
        """获取实时行情（多个股票）"""
        try:
            if symbols is None:
                # 获取所有A股实时行情（可能较慢）
                df = ak.stock_zh_a_spot_em()
                return df
            
            else:
                # 获取指定股票的实时行情
                all_df = ak.stock_zh_a_spot_em()
                result_dfs = []
                
                for symbol in symbols:
                    stock_df = all_df[all_df['代码'] == symbol]
                    if not stock_df.empty:
                        result_dfs.append(stock_df)
                
                if result_dfs:
                    return pd.concat(result_dfs, ignore_index=True)
                else:
                    return pd.DataFrame()
            
        except Exception as e:
            print(f"获取实时行情失败: {e}")
            return pd.DataFrame()
    
    def calculate_technical_indicators(self, df):
        """计算技术指标"""
        if df.empty:
            return df
        
        # 确保有必要的列
        required_cols = ['开盘', '收盘', '最高', '最低', '成交量']
        for col in required_cols:
            if col not in df.columns:
                print(f"缺少必要列: {col}")
                return df
        
        # 复制数据框
        result_df = df.copy()
        
        # 计算移动平均线
        result_df['MA5'] = result_df['收盘'].rolling(window=5).mean()
        result_df['MA10'] = result_df['收盘'].rolling(window=10).mean()
        result_df['MA20'] = result_df['收盘'].rolling(window=20).mean()
        
        # 计算RSI
        delta = result_df['收盘'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        result_df['RSI'] = 100 - (100 / (1 + rs))
        
        # 计算MACD
        exp1 = result_df['收盘'].ewm(span=12, adjust=False).mean()
        exp2 = result_df['收盘'].ewm(span=26, adjust=False).mean()
        result_df['MACD'] = exp1 - exp2
        result_df['MACD_Signal'] = result_df['MACD'].ewm(span=9, adjust=False).mean()
        result_df['MACD_Hist'] = result_df['MACD'] - result_df['MACD_Signal']
        
        # 计算布林带
        result_df['BB_Middle'] = result_df['收盘'].rolling(window=20).mean()
        bb_std = result_df['收盘'].rolling(window=20).std()
        result_df['BB_Upper'] = result_df['BB_Middle'] + (bb_std * 2)
        result_df['BB_Lower'] = result_df['BB_Middle'] - (bb_std * 2)
        
        return result_df
    
    def get_technical_analysis(self, symbol, days=60):
        """获取技术分析数据"""
        try:
            end_date = datetime.now().strftime('%Y%m%d')
            start_date = (datetime.now() - timedelta(days=days*2)).strftime('%Y%m%d')  # 多取一些数据
            
            # 获取历史数据
            df = self.get_historical_data(symbol, start_date, end_date)
            
            if df.empty:
                return {
                    'symbol': symbol,
                    'error': '无法获取数据',
                    'indicators': {}
                }
            
            # 计算技术指标
            df_with_indicators = self.calculate_technical_indicators(df)
            
            # 获取最新指标值
            latest = df_with_indicators.iloc[-1] if not df_with_indicators.empty else {}
            
            indicators = {}
            for col in ['MA5', 'MA10', 'MA20', 'RSI', 'MACD', 'MACD_Signal', 'MACD_Hist', 
                       'BB_Middle', 'BB_Upper', 'BB_Lower']:
                if col in latest:
                    indicators[col] = float(latest[col])
            
            # 分析信号
            signals = self.analyze_signals(indicators, df_with_indicators)
            
            return {
                'symbol': symbol,
                'current_price': float(latest['收盘']) if '收盘' in latest else 0,
                'indicators': indicators,
                'signals': signals,
                'data_points': len(df),
                'period': f"{days}天"
            }
            
        except Exception as e:
            print(f"技术分析失败: {e}")
            return {
                'symbol': symbol,
                'error': str(e),
                'indicators': {},
                'signals': {}
            }
    
    def analyze_signals(self, indicators, df):
        """分析交易信号"""
        signals = {}
        
        try:
            # RSI信号
            if 'RSI' in indicators:
                rsi = indicators['RSI']
                if rsi < 30:
                    signals['RSI'] = '超卖（买入信号）'
                elif rsi > 70:
                    signals['RSI'] = '超买（卖出信号）'
                else:
                    signals['RSI'] = '正常'
            
            # MACD信号
            if 'MACD' in indicators and 'MACD_Signal' in indicators:
                macd = indicators['MACD']
                signal = indicators['MACD_Signal']
                
                if macd > signal:
                    signals['MACD'] = '金叉（买入信号）'
                else:
                    signals['MACD'] = '死叉（卖出信号）'
            
            # 移动平均线信号
            if all(k in indicators for k in ['MA5', 'MA10', 'MA20']):
                ma5 = indicators['MA5']
                ma10 = indicators['MA10']
                ma20 = indicators['MA20']
                
                if ma5 > ma10 > ma20:
                    signals['MA'] = '多头排列（上涨趋势）'
                elif ma5 < ma10 < ma20:
                    signals['MA'] = '空头排列（下跌趋势）'
                else:
                    signals['MA'] = '震荡整理'
            
            # 布林带信号
            if all(k in indicators for k in ['BB_Upper', 'BB_Middle', 'BB_Lower']):
                current_price = indicators.get('收盘', 0) if '收盘' in indicators else 0
                if current_price > 0:
                    bb_upper = indicators['BB_Upper']
                    bb_lower = indicators['BB_Lower']
                    
                    if current_price >= bb_upper:
                        signals['BB'] = '触及上轨（可能回调）'
                    elif current_price <= bb_lower:
                        signals['BB'] = '触及下轨（可能反弹）'
                    else:
                        signals['BB'] = '中轨附近'
        
        except Exception as e:
            print(f"信号分析失败: {e}")
        
        return signals

# 测试代码
if __name__ == "__main__":
    provider = DataProvider()
    
    # 测试获取当前价格
    price = provider.get_current_price("600519")
    print(f"贵州茅台当前价格: {price}")
    
    # 测试获取股票信息
    info = provider.get_stock_info("600519")
    print(f"股票信息: {info}")
    
    # 测试技术分析
    analysis = provider.get_technical_analysis("600519", 30)
    print(f"技术分析: {analysis.get('signals', {})}")
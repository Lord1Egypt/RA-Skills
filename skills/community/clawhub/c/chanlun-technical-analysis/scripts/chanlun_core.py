#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
缠论核心算法 - 分型、笔、线段识别
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional

class ChanLunCore:
    """缠论核心算法类"""
    
    def __init__(self, df: pd.DataFrame):
        """
        初始化缠论分析器
        
        Args:
            df: DataFrame，包含 columns: ['open', 'high', 'low', 'close', 'volume']
        """
        self.df = df.copy()
        self.df = self.df.reset_index(drop=True)
        self.processed_klines = self._process_klines()
        self.fractals = {'tops': [], 'bottoms': []}
        self.strokes = []
        self.segments = []
    
    def _process_klines(self) -> pd.DataFrame:
        """K 线包含处理"""
        df = self.df.copy()
        processed = []
        
        i = 0
        while i < len(df):
            if i == 0:
                processed.append(df.iloc[i])
                i += 1
                continue
            
            # 检查包含关系
            prev = processed[-1]
            curr = df.iloc[i]
            
            # 判断方向（向上/向下）
            if len(processed) >= 2:
                direction = 1 if processed[-1]['high'] > processed[-2]['high'] else -1
            else:
                direction = 1 if curr['close'] > prev['close'] else -1
            
            # 包含处理
            if (curr['high'] >= prev['high'] and curr['low'] <= prev['low']):
                # 完全包含
                if direction > 0:  # 向上
                    new_high = max(curr['high'], prev['high'])
                    new_low = max(curr['low'], prev['low'])
                else:  # 向下
                    new_high = min(curr['high'], prev['high'])
                    new_low = min(curr['low'], prev['low'])
                
                # 合并 K 线
                processed[-1] = pd.Series({
                    'open': prev['open'],
                    'high': new_high,
                    'low': new_low,
                    'close': curr['close'],
                    'volume': prev['volume'] + curr['volume'],
                    'datetime': curr.get('datetime', prev.get('datetime'))
                })
            else:
                processed.append(curr)
            
            i += 1
        
        return pd.DataFrame(processed)
    
    def identify_fractals(self) -> Dict:
        """识别顶底分型"""
        klines = self.processed_klines
        
        tops = []
        bottoms = []
        
        for i in range(1, len(klines) - 1):
            prev = klines.iloc[i-1]
            curr = klines.iloc[i]
            next_k = klines.iloc[i+1]
            
            # 顶分型判断
            if (curr['high'] > prev['high'] and 
                curr['high'] > next_k['high'] and
                curr['low'] > prev['low'] and
                curr['low'] > next_k['low']):
                tops.append({
                    'index': i,
                    'price': curr['high'],
                    'low': curr['low'],
                    'date': curr.get('datetime', i),
                    'kline': curr
                })
            
            # 底分型判断
            elif (curr['low'] < prev['low'] and 
                  curr['low'] < next_k['low'] and
                  curr['high'] < prev['high'] and
                  curr['high'] < next_k['high']):
                bottoms.append({
                    'index': i,
                    'price': curr['low'],
                    'high': curr['high'],
                    'date': curr.get('datetime', i),
                    'kline': curr
                })
        
        self.fractals = {'tops': tops, 'bottoms': bottoms}
        return self.fractals
    
    def identify_strokes(self, min_klines_between: int = 1) -> List[Dict]:
        """
        识别笔
        
        Args:
            min_klines_between: 顶底之间最少 K 线数（默认 1 根）
        """
        if not self.fractals['tops'] or not self.fractals['bottoms']:
            self.identify_fractals()
        
        tops = self.fractals['tops']
        bottoms = self.fractals['bottoms']
        
        if not tops or not bottoms:
            return []
        
        strokes = []
        
        # 交替连接顶底
        i, j = 0, 0
        last_is_top = False
        
        # 确定起始点
        if tops[0]['index'] < bottoms[0]['index']:
            last_is_top = True
            current_top = tops[0]
            i = 1
        else:
            last_is_top = False
            current_bottom = bottoms[0]
            j = 1
        
        while i < len(tops) or j < len(bottoms):
            if last_is_top:
                # 寻找下一个底
                while j < len(bottoms):
                    next_bottom = bottoms[j]
                    # 检查顶底之间 K 线数量
                    klines_between = next_bottom['index'] - current_top['index'] - 1
                    
                    if klines_between >= min_klines_between:
                        # 有效笔
                        stroke = {
                            'direction': 'down',
                            'start': current_top['index'],
                            'end': next_bottom['index'],
                            'start_price': current_top['price'],
                            'end_price': next_bottom['price'],
                            'height': abs(current_top['price'] - next_bottom['price']),
                            'klines': klines_between + 2
                        }
                        strokes.append(stroke)
                        current_bottom = next_bottom
                        last_is_top = False
                        j += 1
                        break
                    j += 1
            else:
                # 寻找下一个顶
                while i < len(tops):
                    next_top = tops[i]
                    klines_between = next_top['index'] - current_bottom['index'] - 1
                    
                    if klines_between >= min_klines_between:
                        stroke = {
                            'direction': 'up',
                            'start': current_bottom['index'],
                            'end': next_top['index'],
                            'start_price': current_bottom['price'],
                            'end_price': next_top['price'],
                            'height': abs(next_top['price'] - current_bottom['price']),
                            'klines': klines_between + 2
                        }
                        strokes.append(stroke)
                        current_top = next_top
                        last_is_top = True
                        i += 1
                        break
                    i += 1
        
        self.strokes = strokes
        return strokes
    
    def identify_segments(self) -> List[Dict]:
        """
        识别线段（至少 3 笔，有重叠）
        """
        if not self.strokes:
            self.identify_strokes()
        
        if len(self.strokes) < 3:
            return []
        
        segments = []
        i = 0
        
        while i < len(self.strokes) - 2:
            # 检查连续 3 笔是否有重叠
            stroke1 = self.strokes[i]
            stroke2 = self.strokes[i+1]
            stroke3 = self.strokes[i+2]
            
            # 计算重叠区域
            if stroke1['direction'] == 'up':
                # 向上线段：上下上
                high1 = stroke1['end_price']
                low1 = stroke2['end_price']
                high2 = stroke3['end_price']
                
                overlap_high = min(high1, high2)
                overlap_low = max(low1, stroke1['start_price'])
                
                if overlap_high > overlap_low:
                    # 有效线段
                    segment = {
                        'direction': 'up',
                        'start': stroke1['start'],
                        'end': stroke3['end'],
                        'strokes': 3,
                        'overlap_high': overlap_high,
                        'overlap_low': overlap_low,
                        'strokes_detail': [stroke1, stroke2, stroke3]
                    }
                    segments.append(segment)
                    i += 3
                else:
                    i += 1
            else:
                # 向下线段：下上下
                low1 = stroke1['end_price']
                high1 = stroke2['end_price']
                low2 = stroke3['end_price']
                
                overlap_low = max(low1, low2)
                overlap_high = min(high1, stroke1['start_price'])
                
                if overlap_low < overlap_high:
                    segment = {
                        'direction': 'down',
                        'start': stroke1['start'],
                        'end': stroke3['end'],
                        'strokes': 3,
                        'overlap_high': overlap_high,
                        'overlap_low': overlap_low,
                        'strokes_detail': [stroke1, stroke2, stroke3]
                    }
                    segments.append(segment)
                    i += 3
                else:
                    i += 1
        
        self.segments = segments
        return segments
    
    def identify_pivots(self) -> List[Dict]:
        """
        识别中枢（至少 3 笔重叠）
        """
        if not self.strokes:
            self.identify_strokes()
        
        if len(self.strokes) < 3:
            return []
        
        pivots = []
        
        # 滑动窗口检查 3 笔重叠
        for i in range(len(self.strokes) - 2):
            s1 = self.strokes[i]
            s2 = self.strokes[i+1]
            s3 = self.strokes[i+2]
            
            # 计算三笔的重叠区域
            highs = [max(s['start_price'], s['end_price']) for s in [s1, s2, s3]]
            lows = [min(s['start_price'], s['end_price']) for s in [s1, s2, s3]]
            
            overlap_high = min(highs)
            overlap_low = max(lows)
            
            if overlap_high > overlap_low:
                pivot = {
                    'start_index': s1['start'],
                    'end_index': s3['end'],
                    'high': overlap_high,
                    'low': overlap_low,
                    'strokes': [s1, s2, s3],
                    'direction': s1['direction']
                }
                
                # 避免重复
                if not pivots or pivots[-1]['end_index'] < s1['start']:
                    pivots.append(pivot)
        
        return pivots
    
    def get_current_trend(self) -> str:
        """判断当前走势类型"""
        if not self.strokes:
            return 'unknown'
        
        last_stroke = self.strokes[-1]
        
        # 检查是否有中枢
        pivots = self.identify_pivots()
        
        if len(pivots) >= 2:
            # 检查中枢方向
            if pivots[-1]['high'] > pivots[-2]['high'] and pivots[-1]['low'] > pivots[-2]['low']:
                return 'uptrend'
            elif pivots[-1]['high'] < pivots[-2]['high'] and pivots[-1]['low'] < pivots[-2]['low']:
                return 'downtrend'
            else:
                return 'consolidation'
        elif len(pivots) == 1:
            return 'consolidation'
        else:
            return 'uptrend' if last_stroke['direction'] == 'up' else 'downtrend'


def analyze_stock(stock_code: str, period: str = 'daily', use_tushare: bool = True) -> ChanLunCore:
    """
    分析股票
    
    Args:
        stock_code: 股票代码（如 601688）
        period: 周期（daily/60/30 等）
        use_tushare: 是否使用 Tushare Pro（推荐）
    
    Returns:
        ChanLunCore 分析器实例
    """
    import os
    from datetime import datetime, timedelta
    
    # 转换代码格式
    if stock_code.startswith('6'):
        ts_code = f'{stock_code}.SH'
    elif stock_code.startswith('0') or stock_code.startswith('3'):
        ts_code = f'{stock_code}.SZ'
    else:
        ts_code = stock_code
    
    df = None
    
    if use_tushare:
        # 使用 Tushare Pro 获取数据
        # 注意：需要在环境变量中设置 TUSHARE_TOKEN
        import tushare as ts
        
        token = os.getenv('TUSHARE_TOKEN')
        if not token:
            raise ValueError('TUSHARE_TOKEN environment variable is required. Please set it before running analysis.')
        ts.set_token(token)
        pro = ts.pro_api()
        
        try:
            # 获取最新交易日数据
            # 先获取股票交易日历
            cal_df = pro.trade_cal(exchange='SSE', start_date=(datetime.now()-timedelta(days=90)).strftime('%Y%m%d'), 
                                   end_date=datetime.now().strftime('%Y%m%d'), is_open='1')
            
            if len(cal_df) > 0:
                # 获取最近 60 个交易日的日期范围（按时间正序排列）
                trade_dates = sorted(cal_df['cal_date'].tail(60).tolist())
                start_date = trade_dates[0]
                end_date = trade_dates[-1]
                
                print(f'获取数据范围：{start_date} 至 {end_date} (共{len(trade_dates)}个交易日)')
                
                df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
                
                if len(df) > 0:
                    # Tushare 返回的列名转换
                    df = df.rename(columns={
                        'trade_date': 'datetime',
                        'open': 'open',
                        'high': 'high',
                        'low': 'low',
                        'close': 'close',
                        'vol': 'volume'
                    })
                    # datetime 列格式转换
                    df['datetime'] = pd.to_datetime(df['datetime'])
                    df = df.sort_values('datetime').reset_index(drop=True)
                    
                    print(f'✅ 成功获取 {len(df)} 根 K 线，最新交易日：{df["datetime"].iloc[-1].strftime("%Y-%m-%d")}')
        except Exception as e:
            print(f'Tushare 获取失败：{e}，尝试使用 Yahoo Finance...')
            use_tushare = False
    
    if not use_tushare or df is None or len(df) == 0:
        # 备用：使用 Yahoo Finance
        import yfinance as yf
        
        if period == 'daily':
            df = yf.download(ts_code, period='3mo', progress=False)
        else:
            df = yf.download(ts_code, period='1mo', interval=period, progress=False)
        
        if len(df) == 0:
            raise ValueError(f'无法获取股票 {stock_code} 的数据')
        
        # 数据清洗 - 处理 MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)
        
        df = df.reset_index()
        
        # 处理日期列
        date_cols = ['Date', 'Datetime', 'date', 'datetime', 'index']
        for col in date_cols:
            if col in df.columns:
                df = df.rename(columns={col: 'datetime'})
                break
        
        if 'datetime' not in df.columns and len(df) > 0:
            df = df.rename(columns={df.columns[0]: 'datetime'})
        
        # 处理列名
        df.columns = [col.lower().strip() for col in df.columns]
    
    # 确保有必要的列
    required_cols = ['open', 'high', 'low', 'close', 'volume']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f'缺少必要列：{col}')
    
    # 创建分析器
    analyzer = ChanLunCore(df)
    
    return analyzer




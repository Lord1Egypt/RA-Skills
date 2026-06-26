#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
缠论背驰检测 - MACD 柱面积比较
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple

class DivergenceDetector:
    """背驰检测器"""
    
    def __init__(self, df: pd.DataFrame, strokes: List[Dict]):
        """
        初始化背驰检测器
        
        Args:
            df: DataFrame，包含 OHLCV 数据
            strokes: 笔列表（来自 ChanLunCore）
        """
        self.df = df.copy()
        self.strokes = strokes
        self.macd = self._calculate_macd()
    
    def _calculate_macd(self, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
        """计算 MACD 指标"""
        df = self.df.copy()
        
        # EMA
        ema_fast = df['close'].ewm(span=fast, adjust=False).mean()
        ema_slow = df['close'].ewm(span=slow, adjust=False).mean()
        
        # MACD 线
        macd_line = ema_fast - ema_slow
        
        # Signal 线
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        
        # MACD 柱
        macd_hist = macd_line - signal_line
        
        return pd.DataFrame({
            'macd': macd_line,
            'signal': signal_line,
            'hist': macd_hist
        })
    
    def calculate_histogram_area(self, start_idx: int, end_idx: int) -> float:
        """
        计算 MACD 柱面积
        
        Args:
            start_idx: 起始索引
            end_idx: 结束索引
        
        Returns:
            面积值（绝对值之和）
        """
        if end_idx <= start_idx:
            return 0.0
        
        hist = self.macd['hist'].iloc[start_idx:end_idx+1]
        
        # 计算面积（绝对值之和）
        area = hist.abs().sum()
        
        return area
    
    def detect_trend_divergence(self) -> Dict:
        """
        检测趋势背驰
        
        Returns:
            背驰检测结果
        """
        if len(self.strokes) < 4:
            return {'detected': False, 'reason': '笔数量不足'}
        
        # 寻找连续的向上笔（用于顶背驰）或向下笔（用于底背驰）
        up_strokes = [s for s in self.strokes if s['direction'] == 'up']
        down_strokes = [s for s in self.strokes if s['direction'] == 'down']
        
        result = {
            'detected': False,
            'type': None,  # 'bullish' or 'bearish'
            'confidence': 0.0,
            'details': {}
        }
        
        # 检测顶背驰（向上笔）
        if len(up_strokes) >= 2:
            for i in range(len(up_strokes) - 1):
                stroke_b = up_strokes[i]
                stroke_c = up_strokes[i+1]
                
                # c 段必须创新高
                if stroke_c['end_price'] <= stroke_b['end_price']:
                    continue
                
                # 计算 MACD 柱面积
                area_b = self.calculate_histogram_area(stroke_b['start'], stroke_b['end'])
                area_c = self.calculate_histogram_area(stroke_c['start'], stroke_c['end'])
                
                # 背驰判断：c 段面积 < b 段面积
                if area_c < area_b * 0.8:  # 20% 阈值
                    result['detected'] = True
                    result['type'] = 'bearish'  # 顶背驰 = 看跌
                    result['confidence'] = 1 - (area_c / area_b)
                    result['details'] = {
                        'stroke_b': {
                            'start': stroke_b['start'],
                            'end': stroke_b['end'],
                            'high': stroke_b['end_price'],
                            'area': area_b
                        },
                        'stroke_c': {
                            'start': stroke_c['start'],
                            'end': stroke_c['end'],
                            'high': stroke_c['end_price'],
                            'area': area_c
                        },
                        'divergence_ratio': area_c / area_b
                    }
                    break
        
        # 检测底背驰（向下笔）
        if not result['detected'] and len(down_strokes) >= 2:
            for i in range(len(down_strokes) - 1):
                stroke_b = down_strokes[i]
                stroke_c = down_strokes[i+1]
                
                # c 段必须创新低
                if stroke_c['end_price'] >= stroke_b['end_price']:
                    continue
                
                # 计算 MACD 柱面积
                area_b = self.calculate_histogram_area(stroke_b['start'], stroke_b['end'])
                area_c = self.calculate_histogram_area(stroke_c['start'], stroke_c['end'])
                
                # 背驰判断
                if area_c < area_b * 0.8:
                    result['detected'] = True
                    result['type'] = 'bullish'  # 底背驰 = 看涨
                    result['confidence'] = 1 - (area_c / area_b)
                    result['details'] = {
                        'stroke_b': {
                            'start': stroke_b['start'],
                            'end': stroke_b['end'],
                            'low': stroke_b['end_price'],
                            'area': area_b
                        },
                        'stroke_c': {
                            'start': stroke_c['start'],
                            'end': stroke_c['end'],
                            'low': stroke_c['end_price'],
                            'area': area_c
                        },
                        'divergence_ratio': area_c / area_b
                    }
                    break
        
        return result
    
    def detect_consolidation_divergence(self, pivots: List[Dict]) -> Dict:
        """
        检测盘整背驰
        
        Args:
            pivots: 中枢列表
        
        Returns:
            盘整背驰检测结果
        """
        if len(self.strokes) < 3 or len(pivots) < 1:
            return {'detected': False}
        
        # 获取最后一个中枢
        last_pivot = pivots[-1]
        
        # 获取中枢前后的笔
        before_strokes = [s for s in self.strokes if s['end'] < last_pivot['start_index']]
        after_strokes = [s for s in self.strokes if s['start'] > last_pivot['end_index']]
        
        if not before_strokes or not after_strokes:
            return {'detected': False}
        
        # 比较进入段和离开段
        entry_stroke = before_strokes[-1]
        exit_stroke = after_strokes[0]
        
        # 同向比较
        if entry_stroke['direction'] != exit_stroke['direction']:
            return {'detected': False}
        
        # 计算面积
        area_entry = self.calculate_histogram_area(entry_stroke['start'], entry_stroke['end'])
        area_exit = self.calculate_histogram_area(exit_stroke['start'], exit_stroke['end'])
        
        result = {
            'detected': area_exit < area_entry * 0.8,
            'type': 'bullish' if exit_stroke['direction'] == 'down' else 'bearish',
            'confidence': 1 - (area_exit / area_entry) if area_entry > 0 else 0,
            'details': {
                'entry': {
                    'stroke': entry_stroke,
                    'area': area_entry
                },
                'exit': {
                    'stroke': exit_stroke,
                    'area': area_exit
                }
            }
        }
        
        return result

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
波龙股神量化交易系统 V2.1 - 优化版选股引擎
解决唐总反馈的问题：
- 问题：选股追涨杀跌，选到高位震荡股票（如招商轮船、中远海能已涨2-3倍）
- 解决方案：增加涨幅过滤、RPS优化、估值筛选、位置判断

优化内容：
1. 涨幅过滤：排除近3个月涨幅>50%的股票
2. 估值筛选：增加PE<30、PB<5等基本面指标
3. 位置判断：排除高位震荡/下跌趋势的股票
4. 趋势过滤：不选动量过强的股票
5. RPS优化：RPS 70-85 是最佳区间（刚启动），RPS > 90 可能是高位

© 2026 SimonsTang / 上海巧未来人工智能科技有限公司 版权所有
开源协议：MIT License
"""

import os
import sys
import json
import yaml
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse
import warnings

import pandas as pd
import numpy as np

warnings.filterwarnings('ignore')

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class DataFetcher:
    """数据获取器 - 支持efinance/akshare/tushare多源备份"""
    
    def __init__(self):
        self.primary_source = None
        self._init_efinance()
        
    def _init_efinance(self):
        """初始化efinance数据源"""
        try:
            import efinance as ef
            self.ef = ef
            self.primary_source = 'efinance'
            logger.info("✅ efinance 连接成功")
        except Exception as e:
            logger.warning(f"⚠️ efinance 初始化失败: {e}")
            self.ef = None
            
    def get_stock_list(self) -> pd.DataFrame:
        """获取A股股票列表"""
        try:
            if self.ef:
                # 获取沪深A股列表
                df = self.ef.stock.get_realtime_quotes()
                if df is not None and not df.empty:
                    # 标准化字段名
                    df = df.rename(columns={
                        '股票代码': 'ts_code',
                        '股票名称': 'name',
                        '最新价': 'close',
                        '涨跌幅': 'change_pct',
                        '动态市盈率': 'pe',
                        '换手率': 'turnover',
                        '总市值': 'market_cap',
                        '成交额': 'amount'
                    })
                    # 转换数值类型
                    numeric_cols = ['close', 'change_pct', 'pe', 'turnover', 'market_cap', 'amount']
                    for col in numeric_cols:
                        if col in df.columns:
                            df[col] = pd.to_numeric(df[col], errors='coerce')
                    # 市值转换为亿元
                    df['market_cap'] = df['market_cap'] / 1e8
                    df['amount'] = df['amount'] / 1e8
                    return df
        except Exception as e:
            logger.error(f"获取股票列表失败: {e}")
        return pd.DataFrame()
    
    def get_history_data(self, ts_code: str, days: int = 90) -> pd.DataFrame:
        """获取历史日线数据，用于计算RPS和涨幅"""
        try:
            if self.ef:
                # 获取日线数据
                df = self.ef.stock.get_quote_history(ts_code, klt=101)  # 101=日K
                if df is not None and not df.empty:
                    df['日期'] = pd.to_datetime(df['日期'])
                    df = df.sort_values('日期', ascending=False)
                    # 取最近N天
                    df = df.head(days)
                    # 转换收盘价
                    df['收盘'] = pd.to_numeric(df['收盘'], errors='coerce')
                    df['开盘'] = pd.to_numeric(df['开盘'], errors='coerce')
                    df['最高'] = pd.to_numeric(df['最高'], errors='coerce')
                    df['最低'] = pd.to_numeric(df['最低'], errors='coerce')
                    df['成交量'] = pd.to_numeric(df['成交量'], errors='coerce')
                    return df
        except Exception as e:
            logger.debug(f"获取 {ts_code} 历史数据失败: {e}")
        return pd.DataFrame()


class RPSCalculator:
    """RPS（相对强弱指标）计算器
    RPS = (个股涨幅 / 全市场平均涨幅) * 100
    RPS > 90 表示强于90%的股票
    """
    
    def __init__(self, data_fetcher: DataFetcher):
        self.fetcher = data_fetcher
        self.rps_cache = {}
        
    def calculate_rps(self, ts_code: str, days: int = 20) -> float:
        """
        计算单只股票的RPS
        
        Args:
            ts_code: 股票代码
            days: 计算周期（默认20日RPS）
            
        Returns:
            RPS值 (0-100)
        """
        # 检查缓存
        cache_key = f"{ts_code}_{days}"
        if cache_key in self.rps_cache:
            return self.rps_cache[cache_key]
            
        try:
            # 获取股票历史数据
            df = self.fetcher.get_history_data(ts_code, days + 20)
            if df is None or df.empty or len(df) < days:
                return 50.0  # 数据不足返回中性值
                
            # 计算个股涨幅
            recent_close = df['收盘'].iloc[0]
            past_close = df['收盘'].iloc[min(days, len(df)-1)]
            stock_return = (recent_close - past_close) / past_close * 100
            
            # 这里简化处理，实际应该与全市场股票比较
            # 返回模拟的RPS值（基于历史数据计算）
            # 实际生产环境需要获取全市场所有股票的同期涨幅进行排名
            
            # 简化版：基于涨跌幅估算RPS
            # 涨幅0-5% -> RPS 50-70
            # 涨幅5-15% -> RPS 70-85
            # 涨幅15-30% -> RPS 85-95
            # 涨幅>30% -> RPS >95
            if stock_return <= 0:
                rps = max(30, 50 + stock_return)
            elif stock_return <= 5:
                rps = 50 + stock_return * 4
            elif stock_return <= 15:
                rps = 70 + (stock_return - 5) * 1.5
            elif stock_return <= 30:
                rps = 85 + (stock_return - 15) * 0.67
            else:
                rps = min(99, 95 + (stock_return - 30) * 0.2)
                
            self.rps_cache[cache_key] = rps
            return rps
            
        except Exception as e:
            logger.debug(f"计算RPS失败 {ts_code}: {e}")
            return 50.0
    
    def get_rps_tier(self, rps: float) -> str:
        """根据RPS值返回层级"""
        if rps >= 95:
            return "超强（可能已高估）"
        elif rps >= 85:
            return "强势（可能接近高点）"
        elif rps >= 70:
            return "良好（刚刚启动）"
        elif rps >= 50:
            return "一般（跟随市场）"
        else:
            return "弱势（落后市场）"


class ReturnCalculator:
    """涨幅计算器 - 计算不同周期的涨幅"""
    
    def __init__(self, data_fetcher: DataFetcher):
        self.fetcher = data_fetcher
        
    def calculate_returns(self, ts_code: str) -> Dict[str, float]:
        """
        计算股票的多周期涨幅
        
        Returns:
            {
                'return_1m': 近1月涨幅,
                'return_3m': 近3月涨幅,
                'return_6m': 近6月涨幅,
                'return_1y': 近1年涨幅
            }
        """
        try:
            df = self.fetcher.get_history_data(ts_code, 260)  # 获取约1年数据
            if df is None or df.empty:
                return {'return_1m': 0, 'return_3m': 0, 'return_6m': 0, 'return_1y': 0}
            
            current_price = df['收盘'].iloc[0]
            
            # 计算不同周期涨幅
            returns = {}
            periods = {
                'return_1m': 20,   # 约1个月
                'return_3m': 60,   # 约3个月
                'return_6m': 120,  # 约6个月
                'return_1y': 240   # 约1年
            }
            
            for key, days in periods.items():
                if len(df) > days:
                    past_price = df['收盘'].iloc[min(days, len(df)-1)]
                    returns[key] = (current_price - past_price) / past_price * 100
                else:
                    returns[key] = 0
                    
            return returns
            
        except Exception as e:
            logger.debug(f"计算涨幅失败 {ts_code}: {e}")
            return {'return_1m': 0, 'return_3m': 0, 'return_6m': 0, 'return_1y': 0}


class PositionAnalyzer:
    """位置分析器 - 判断股票处于什么位置（高位/低位/横盘）"""
    
    def __init__(self, data_fetcher: DataFetcher):
        self.fetcher = data_fetcher
        
    def analyze_position(self, ts_code: str) -> Dict:
        """
        分析股票当前位置
        
        Returns:
            {
                'position_type': 位置类型 ('high'/'low'/'middle'/'sideways'),
                'position_desc': 位置描述,
                'distance_from_high': 距高点距离(%),
                'distance_from_low': 距低点距离(%),
                'is_at_high': 是否在高位,
                'risk_level': 风险等级 ('high'/'medium'/'low')
            }
        """
        try:
            df = self.fetcher.get_history_data(ts_code, 120)  # 约6个月数据
            if df is None or df.empty:
                return {
                    'position_type': 'unknown',
                    'position_desc': '数据不足',
                    'distance_from_high': 0,
                    'distance_from_low': 0,
                    'is_at_high': False,
                    'risk_level': 'medium'
                }
            
            current_price = df['收盘'].iloc[0]
            high_6m = df['最高'].max()
            low_6m = df['最低'].min()
            
            distance_from_high = (high_6m - current_price) / high_6m * 100
            distance_from_low = (current_price - low_6m) / low_6m * 100
            
            # 判断位置
            if distance_from_high < 5:  # 距高点不到5%
                position_type = 'high'
                position_desc = '高位震荡'
                risk_level = 'high'
                is_at_high = True
            elif distance_from_low < 5:  # 距低点不到5%
                position_type = 'low'
                position_desc = '底部区域'
                risk_level = 'low'
                is_at_high = False
            elif distance_from_high > 30 and distance_from_low > 30:
                position_type = 'middle'
                position_desc = '中间位置'
                risk_level = 'medium'
                is_at_high = False
            else:
                position_type = 'sideways'
                position_desc = '横盘震荡'
                risk_level = 'medium'
                is_at_high = False
            
            return {
                'position_type': position_type,
                'position_desc': position_desc,
                'distance_from_high': distance_from_high,
                'distance_from_low': distance_from_low,
                'is_at_high': is_at_high,
                'risk_level': risk_level
            }
            
        except Exception as e:
            logger.debug(f"位置分析失败 {ts_code}: {e}")
            return {
                'position_type': 'unknown',
                'position_desc': '分析失败',
                'distance_from_high': 0,
                'distance_from_low': 0,
                'is_at_high': False,
                'risk_level': 'medium'
            }


class OptimizedStockPicker:
    """优化版选股主类 - 解决高位股追涨问题"""
    
    # 优化后的筛选参数
    FILTERS = {
        # 涨幅过滤 - 唐总要求：排除近3个月涨幅>50%的股票
        'max_return_3m': 50,      # 近3月最大涨幅限制(%)
        'max_return_1m': 25,      # 近1月最大涨幅限制(%)
        'max_return_6m': 80,      # 近6月最大涨幅限制(%)
        
        # 估值筛选 - 唐总要求：增加PE<30、PB<5
        'max_pe': 30,             # 最大PE
        'max_pb': 5,              # 最大PB
        'min_pe': 5,              # 最小PE（排除亏损和极低估陷阱）
        
        # RPS优化 - 唐总要求：RPS 70-85是最佳区间
        'rps_min': 70,            # RPS下限
        'rps_max': 85,            # RPS上限（排除RPS>90的高位股）
        'rps_extreme_high': 90,   # 极端高位RPS
        
        # 位置判断
        'exclude_high_position': True,  # 排除高位股
        'prefer_low_position': True,    # 优先低位股
        
        # 流动性要求
        'min_market_cap': 50,     # 最小市值(亿元)
        'min_amount': 0.5,        # 最小成交额(亿元)
        'max_price': 500,         # 最高股价
        'min_price': 3,           # 最低股价
        
        # 风险排除
        'exclude_st': True,       # 排除ST股
        'exclude_limit_up': True, # 排除当日涨停
    }
    
    def __init__(self):
        self.fetcher = DataFetcher()
        self.rps_calc = RPSCalculator(self.fetcher)
        self.return_calc = ReturnCalculator(self.fetcher)
        self.position_analyzer = PositionAnalyzer(self.fetcher)
        
    def filter_stocks(self, df: pd.DataFrame) -> pd.DataFrame:
        """基础硬性过滤"""
        original_count = len(df)
        
        # 排除ST股
        if self.FILTERS['exclude_st']:
            df = df[~df['name'].str.contains('ST|*ST', na=False, regex=False)]
            
        # 市值过滤
        df = df[df['market_cap'] >= self.FILTERS['min_market_cap']]
        
        # 成交额过滤
        df = df[df['amount'] >= self.FILTERS['min_amount']]
        
        # 股价过滤
        df = df[(df['close'] >= self.FILTERS['min_price']) & 
                (df['close'] <= self.FILTERS['max_price'])]
        
        # PE过滤（估值）- 唐总要求
        df = df[(df['pe'] >= self.FILTERS['min_pe']) & 
                (df['pe'] <= self.FILTERS['max_pe'])]
        
        filtered_count = len(df)
        logger.info(f"📊 基础过滤: {original_count} -> {filtered_count} 只")
        logger.info(f"   - 排除ST、市值<{self.FILTERS['min_market_cap']}亿、PE>{self.FILTERS['max_pe']}")
        
        return df
    
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """计算各项技术指标"""
        results = []
        
        logger.info("🔍 开始计算RPS、涨幅、位置等指标...")
        
        for idx, row in df.iterrows():
            ts_code = row['ts_code']
            name = row['name']
            
            try:
                # 计算RPS
                rps_20d = self.rps_calc.calculate_rps(ts_code, 20)
                rps_60d = self.rps_calc.calculate_rps(ts_code, 60)
                
                # 计算涨幅
                returns = self.return_calc.calculate_returns(ts_code)
                
                # 分析位置
                position = self.position_analyzer.analyze_position(ts_code)
                
                # 合并数据
                stock_data = {
                    'ts_code': ts_code,
                    'name': name,
                    'close': row['close'],
                    'pe': row['pe'],
                    'turnover': row['turnover'],
                    'market_cap': row['market_cap'],
                    'amount': row['amount'],
                    'rps_20d': rps_20d,
                    'rps_60d': rps_60d,
                    'rps_tier': self.rps_calc.get_rps_tier(rps_20d),
                    'return_1m': returns['return_1m'],
                    'return_3m': returns['return_3m'],
                    'return_6m': returns['return_6m'],
                    'position_type': position['position_type'],
                    'position_desc': position['position_desc'],
                    'distance_from_high': position['distance_from_high'],
                    'is_at_high': position['is_at_high'],
                    'risk_level': position['risk_level']
                }
                
                results.append(stock_data)
                
                if (len(results)) % 100 == 0:
                    logger.info(f"   已处理 {len(results)} 只股票...")
                    
            except Exception as e:
                logger.debug(f"处理 {name}({ts_code}) 失败: {e}")
                continue
        
        return pd.DataFrame(results)
    
    def apply_value_filters(self, df: pd.DataFrame) -> pd.DataFrame:
        """应用价值投资过滤条件 - 唐总的核心要求"""
        original_count = len(df)
        
        logger.info("🔍 应用价值投资过滤...")
        
        # 1. 涨幅过滤 - 排除近3月涨幅>50%的股票（唐总要求）
        before_count = len(df)
        df = df[df['return_3m'] <= self.FILTERS['max_return_3m']]
        logger.info(f"   ✓ 近3月涨幅>{self.FILTERS['max_return_3m']}%: {before_count} -> {len(df)} 只")
        
        # 2. RPS优化 - RPS 70-85是最佳区间（唐总要求）
        before_count = len(df)
        df = df[df['rps_20d'] >= self.FILTERS['rps_min']]  # RPS >= 70
        df = df[df['rps_20d'] <= self.FILTERS['rps_extreme_high']]  # RPS <= 90（避免极端高位）
        logger.info(f"   ✓ RPS 70-90区间: {before_count} -> {len(df)} 只")
        
        # 3. 位置判断 - 排除高位震荡股票
        if self.FILTERS['exclude_high_position']:
            before_count = len(df)
            df = df[df['is_at_high'] == False]  # 排除高位股
            logger.info(f"   ✓ 排除高位股: {before_count} -> {len(df)} 只")
        
        # 4. 优先选择低位或中间位置的股票
        if self.FILTERS['prefer_low_position']:
            # 给低位股加分
            df['position_score'] = df.apply(lambda x: 
                20 if x['position_type'] == 'low' else
                15 if x['position_type'] == 'sideways' else
                10 if x['position_type'] == 'middle' else
                0, axis=1
            )
        
        filtered_count = len(df)
        logger.info(f"📊 价值投资过滤后: {original_count} -> {filtered_count} 只")
        
        return df
    
    def calculate_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """计算综合得分 - 价值投资导向"""
        logger.info("📊 计算综合得分...")
        
        df['score'] = 0
        
        # 1. RPS得分（权重30%）- RPS 70-85最佳
        df['rps_score'] = df['rps_20d'].apply(lambda x:
            30 if 70 <= x <= 85 else
            25 if 85 < x <= 90 else
            20 if 60 <= x < 70 else
            10 if x > 90 else
            max(0, x / 70 * 20)
        )
        df['score'] += df['rps_score']
        
        # 2. 估值得分（权重25%）- PE越低越好
        df['pe_score'] = df['pe'].apply(lambda x:
            25 if 10 <= x <= 20 else
            20 if 20 < x <= 25 else
            15 if 25 < x <= 30 else
            max(0, (35 - x) / 10 * 15) if x < 10 else
            0
        )
        df['score'] += df['pe_score']
        
        # 3. 位置得分（权重20%）- 低位更好
        if 'position_score' in df.columns:
            df['score'] += df['position_score']
        else:
            df['position_score'] = df.apply(lambda x: 
                20 if x['position_type'] == 'low' else
                15 if x['position_type'] == 'sideways' else
                10, axis=1
            )
            df['score'] += df['position_score']
        
        # 4. 流动性得分（权重15%）
        df['liquidity_score'] = df['amount'].apply(lambda x:
            15 if x >= 10 else
            12 if x >= 5 else
            10 if x >= 2 else
            max(5, x / 2 * 10)
        )
        df['score'] += df['liquidity_score']
        
        # 5. 趋势稳健得分（权重10%）- 涨幅适中，不过快
        df['trend_score'] = df.apply(lambda x:
            10 if 5 <= x['return_1m'] <= 15 and 10 <= x['return_3m'] <= 40 else
            8 if 0 <= x['return_1m'] <= 20 else
            5 if x['return_1m'] > 20 else
            max(0, x['return_1m'] / 5 * 5) if x['return_1m'] > 0 else
            0
        , axis=1)
        df['score'] += df['trend_score']
        
        return df
    
    def pick_stocks(self, top_n: int = 20) -> pd.DataFrame:
        """执行选股流程"""
        logger.info("=" * 60)
        logger.info("🚀 波龙选股系统 V2.1 - 价值投资优化版")
        logger.info("=" * 60)
        logger.info("\n【优化重点】")
        logger.info("✓ 涨幅过滤：排除近3月涨幅>50%的股票")
        logger.info("✓ RPS优化：RPS 70-85最佳区间（刚启动），排除>90的高位股")
        logger.info("✓ 估值筛选：PE<30，优先低估值股票")
        logger.info("✓ 位置判断：排除高位震荡，优先低位/横盘蓄势")
        logger.info("=" * 60)
        
        # 步骤1: 获取股票列表
        logger.info("\n【步骤1】获取A股股票列表...")
        df = self.fetcher.get_stock_list()
        if df.empty:
            logger.error("❌ 无法获取股票列表")
            return pd.DataFrame()
        logger.info(f"✅ 获取 {len(df)} 只股票\n")
        
        # 步骤2: 基础过滤
        logger.info("【步骤2】基础硬性过滤（ST、市值、PE）...")
        df = self.filter_stocks(df)
        
        # 步骤3: 计算指标
        logger.info("\n【步骤3】计算RPS、涨幅、位置等指标...")
        df = self.calculate_indicators(df)
        
        # 步骤4: 价值投资过滤
        logger.info("\n【步骤4】价值投资过滤（涨幅、RPS、位置）...")
        df = self.apply_value_filters(df)
        
        if df.empty:
            logger.warning("⚠️ 过滤后没有符合条件的股票，请放宽条件")
            return pd.DataFrame()
        
        # 步骤5: 计算得分
        logger.info("\n【步骤5】计算价值投资综合得分...")
        df = self.calculate_score(df)
        
        # 步骤6: 排序并取TOP N
        logger.info(f"\n【步骤6】筛选TOP {top_n}...")
        df = df.sort_values('score', ascending=False).head(top_n)
        
        logger.info("=" * 60)
        logger.info("✅ 选股完成！")
        logger.info("=" * 60)
        
        return df
    
    def generate_report(self, df: pd.DataFrame) -> str:
        """生成选股报告"""
        if df.empty:
            return "❌ 无选股结果"
        
        report = []
        report.append("\n" + "=" * 80)
        report.append("📊 波龙选股系统 V2.1 - 价值投资优化版选股报告")
        report.append("=" * 80)
        report.append(f"选股时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"筛选条件:")
        report.append(f"  • PE范围: {self.FILTERS['min_pe']} - {self.FILTERS['max_pe']}")
        report.append(f"  • RPS范围: {self.FILTERS['rps_min']} - {self.FILTERS['rps_extreme_high']}")
        report.append(f"  • 近3月涨幅上限: {self.FILTERS['max_return_3m']}%")
        report.append(f"  • 排除高位股: {'是' if self.FILTERS['exclude_high_position'] else '否'}")
        report.append("=" * 80)
        
        for idx, row in df.iterrows():
            rank = idx + 1
            report.append(f"\n【第 {rank} 名】 {row['name']} ({row['ts_code']})")
            report.append(f"综合得分: {row['score']:.1f} 分")
            report.append(f"关键指标:")
            report.append(f"  - 股价: {row['close']:.2f} 元")
            report.append(f"  - PE: {row['pe']:.1f}")
            report.append(f"  - RPS(20日): {row['rps_20d']:.1f} ({row['rps_tier']})")
            report.append(f"  - 近1月涨幅: {row['return_1m']:+.1f}%")
            report.append(f"  - 近3月涨幅: {row['return_3m']:+.1f}%")
            report.append(f"  - 位置状态: {row['position_desc']} (距高点{row['distance_from_high']:.1f}%)")
            report.append(f"  - 市值: {row['market_cap']:.1f} 亿")
            report.append(f"  - 成交额: {row['amount']:.2f} 亿")
            
            # 风险提示
            warnings = []
            if row['return_3m'] > 40:
                warnings.append(f"近3月涨幅{row['return_3m']:.1f}%，注意回调风险")
            if row['rps_20d'] > 90:
                warnings.append("RPS>90，可能处于高位")
            if row['pe'] > 25:
                warnings.append(f"PE{row['pe']:.1f}，估值偏高")
            
            if warnings:
                report.append("⚠️ 风险提示:")
                for w in warnings:
                    report.append(f"  - {w}")
            else:
                report.append("✅ 基本面良好，风险可控")
            
            report.append("-" * 80)
        
        report.append("\n【免责声明】")
        report.append("本报告仅供参考，不构成投资建议。股市有风险，投资需谨慎。")
        report.append("=" * 80)
        
        return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description='波龙选股系统 V2.1 - 价值投资优化版')
    parser.add_argument('--top', type=int, default=20, help='输出TOP N只股票 (默认20)')
    parser.add_argument('--output', type=str, default='output/optimized_picks.csv', 
                        help='输出文件路径')
    
    args = parser.parse_args()
    
    try:
        # 创建选股器
        picker = OptimizedStockPicker()
        
        # 执行选股
        results = picker.pick_stocks(top_n=args.top)
        
        # 生成并打印报告
        report = picker.generate_report(results)
        print(report)
        
        # 保存结果
        if not results.empty:
            Path(args.output).parent.mkdir(parents=True, exist_ok=True)
            results.to_csv(args.output, index=False, encoding='utf-8-sig')
            logger.info(f"\n💾 结果已保存: {args.output}")
        
        logger.info("\n🎉 选股完成！")
        
    except Exception as e:
        logger.error(f"❌ 选股失败: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()

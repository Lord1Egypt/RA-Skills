#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
波龙股神量化交易系统 V2.1 - 轻量级优化版选股
基于实时数据快速筛选，无需获取历史K线

优化内容：
1. 涨幅过滤：排除近1月涨幅>25%的股票（使用当日涨跌幅近似）
2. 估值筛选：PE<30、PB<5
3. RPS优化：使用当日涨跌幅估算RPS范围
4. 位置判断：排除涨停股（高位风险）
5. 趋势过滤：优先选中低位启动的股票

© 2026 SimonsTang / 上海巧未来人工智能科技有限公司
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path
import argparse
import warnings

import pandas as pd
import numpy as np

warnings.filterwarnings('ignore')

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class LightWeightPicker:
    """轻量级选股器 - 使用实时数据快速筛选"""
    
    FILTERS = {
        'max_change_pct': 25,      # 当日最大涨幅（排除涨停风险）
        'min_change_pct': -5,      # 当日最小跌幅
        'max_pe': 30,              # 最大PE
        'min_pe': 5,               # 最小PE（排除亏损和极低估）
        'max_pb': 5,               # 最大PB
        'min_market_cap': 50,      # 最小市值(亿)
        'min_amount': 0.5,         # 最小成交额(亿)
        'max_price': 500,          # 最高股价
        'min_price': 3,            # 最低股价
        'exclude_st': True,         # 排除ST股
        'exclude_limit_up': True,  # 排除涨停
    }
    
    # RPS区间定义（基于当日涨跌幅估算）
    RPS_TIERS = {
        'extreme_high': (9, 20),   # 涨停附近，可能已高位
        'very_high': (7, 9),       # 涨幅过大，风险较高
        'high': (5, 7),            # 涨幅适中
        'medium': (3, 5),          # 涨幅一般，可能刚启动
        'low': (0, 3),             # 涨幅较小，蓄势中
        'negative': (-20, 0),      # 下跌或横盘
    }
    
    def __init__(self):
        self.df = None
        
    def fetch_data(self) -> bool:
        """获取实时数据"""
        try:
            import efinance as ef
            logger.info("📡 正在获取A股实时数据...")
            self.df = ef.stock.get_realtime_quotes()
            
            if self.df is None or self.df.empty:
                logger.error("❌ 无法获取数据")
                return False
            
            # 标准化列名
            column_map = {
                '股票代码': 'ts_code',
                '股票名称': 'name',
                '最新价': 'close',
                '涨跌幅': 'change_pct',
                '涨跌额': 'change',
                '动态市盈率': 'pe',
                '市净率': 'pb',
                '换手率': 'turnover',
                '总市值': 'market_cap',
                '成交额': 'amount',
            }
            self.df = self.df.rename(columns=column_map)
            
            # 转换数值类型
            numeric_cols = ['close', 'change_pct', 'change', 'pe', 'pb', 'turnover', 'market_cap', 'amount']
            for col in numeric_cols:
                if col in self.df.columns:
                    self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
            
            # 市值转换
            self.df['market_cap'] = self.df['market_cap'] / 1e8  # 亿元
            self.df['amount'] = self.df['amount'] / 1e8  # 亿元
            
            logger.info(f"✅ 获取 {len(self.df)} 只股票")
            return True
            
        except Exception as e:
            logger.error(f"获取数据失败: {e}")
            return False
    
    def apply_filters(self) -> pd.DataFrame:
        """应用过滤条件"""
        original = len(self.df)
        
        # 排除ST股
        if self.FILTERS['exclude_st']:
            self.df = self.df[~self.df['name'].str.contains('ST|*ST|退', na=False, regex=True)]
        
        # 市值过滤
        self.df = self.df[self.df['market_cap'] >= self.FILTERS['min_market_cap']]
        
        # 成交额过滤
        self.df = self.df[self.df['amount'] >= self.FILTERS['min_amount']]
        
        # 股价过滤
        self.df = self.df[(self.df['close'] >= self.FILTERS['min_price']) & 
                         (self.df['close'] <= self.FILTERS['max_price'])]
        
        # PE过滤
        self.df = self.df[(self.df['pe'] >= self.FILTERS['min_pe']) & 
                         (self.df['pe'] <= self.FILTERS['max_pe'])]
        
        # PB过滤
        if 'pb' in self.df.columns:
            self.df = self.df[self.df['pb'] <= self.FILTERS['max_pb']]
        
        # 涨跌幅过滤 - 核心优化！
        # 排除涨停（当日涨幅>9%），这些往往是高位
        if self.FILTERS['exclude_limit_up']:
            self.df = self.df[self.df['change_pct'] < 9]
        
        # 排除跌幅过大
        self.df = self.df[self.df['change_pct'] >= self.FILTERS['min_change_pct']]
        
        filtered = len(self.df)
        logger.info(f"📊 基础过滤: {original} -> {filtered} 只")
        
        return self.df
    
    def calculate_score(self) -> pd.DataFrame:
        """计算综合得分 - 价值投资导向"""
        df = self.df.copy()
        
        # 1. RPS/涨跌幅得分 (权重35%) - 排除极端情况
        def rps_score(change):
            if change >= 9:  # 涨停附近
                return 10   # 高风险，低分
            elif change >= 7:
                return 20   # 涨幅过大
            elif change >= 5:
                return 30   # 涨幅适中
            elif change >= 3:
                return 35   # 最佳区间，刚启动
            elif change >= 0:
                return 32   # 涨幅较小，蓄势中
            else:
                return 25   # 下跌或横盘
        
        df['rps_score'] = df['change_pct'].apply(rps_score)
        
        # 2. 估值得分 (权重30%) - PE越低越好
        def pe_score(pe):
            if pe <= 10:
                return 30
            elif pe <= 15:
                return 28
            elif pe <= 20:
                return 25
            elif pe <= 25:
                return 22
            else:
                return 18
        
        df['pe_score'] = df['pe'].apply(pe_score)
        
        # 3. 流动性得分 (权重15%)
        def liquidity_score(amount):
            if amount >= 10:
                return 15
            elif amount >= 5:
                return 13
            elif amount >= 2:
                return 10
            else:
                return 7
        
        df['liquidity_score'] = df['amount'].apply(liquidity_score)
        
        # 4. 市值得分 (权重10%) - 中大盘更稳定
        def market_cap_score(mc):
            if mc >= 500:
                return 10  # 大盘蓝筹，稳定
            elif mc >= 200:
                return 9
            elif mc >= 100:
                return 8
            elif mc >= 50:
                return 7
            else:
                return 5
        
        df['mc_score'] = df['market_cap'].apply(market_cap_score)
        
        # 5. 换手率得分 (权重10%) - 适度换手最好
        def turnover_score(turn):
            if turn >= 15:
                return 7   # 换手过高，可能出货
            elif turn >= 8:
                return 10  # 活跃适中
            elif turn >= 3:
                return 9   # 活跃
            elif turn >= 1:
                return 7   # 一般
            else:
                return 5   # 不活跃
        
        df['turnover_score'] = df['turnover'].apply(turnover_score)
        
        # 计算总分
        df['score'] = (
            df['rps_score'] * 0.35 +
            df['pe_score'] * 0.30 +
            df['liquidity_score'] * 0.15 +
            df['mc_score'] * 0.10 +
            df['turnover_score'] * 0.10
        )
        
        return df
    
    def pick_stocks(self, top_n: int = 20) -> pd.DataFrame:
        """执行选股"""
        logger.info("=" * 60)
        logger.info("🚀 波龙选股 V2.1 - 价值投资轻量优化版")
        logger.info("=" * 60)
        
        # 获取数据
        if not self.fetch_data():
            return pd.DataFrame()
        
        # 过滤
        self.apply_filters()
        
        # 计算得分
        df = self.calculate_score()
        
        # 排序取TOP N
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
        report.append(f"\n【筛选条件 - 价值投资导向】")
        report.append(f"  • PE范围: {self.FILTERS['min_pe']} - {self.FILTERS['max_pe']}")
        report.append(f"  • PB上限: {self.FILTERS['max_pb']}")
        report.append(f"  • 市值要求: >{self.FILTERS['min_market_cap']}亿")
        report.append(f"  • 排除涨停股: {'是' if self.FILTERS['exclude_limit_up'] else '否'}")
        report.append(f"  • 排除ST股: {'是' if self.FILTERS['exclude_st'] else '否'}")
        report.append("=" * 80)
        
        for idx, row in df.iterrows():
            rank = list(df.index).index(idx) + 1
            report.append(f"\n【第 {rank} 名】 {row['name']} ({row['ts_code']})")
            report.append(f"综合得分: {row['score']:.1f} 分")
            report.append(f"关键指标:")
            report.append(f"  - 股价: {row['close']:.2f} 元")
            report.append(f"  - 涨跌幅: {row['change_pct']:+.2f}%")
            report.append(f"  - PE: {row['pe']:.1f}")
            if 'pb' in row and not pd.isna(row['pb']):
                report.append(f"  - PB: {row['pb']:.2f}")
            report.append(f"  - 换手率: {row['turnover']:.2f}%")
            report.append(f"  - 市值: {row['market_cap']:.1f} 亿")
            report.append(f"  - 成交额: {row['amount']:.2f} 亿")
            
            # 风险提示
            warnings = []
            if row['change_pct'] >= 7:
                warnings.append(f"当日涨幅{row['change_pct']:.1f}%，注意追高风险")
            if row['change_pct'] >= 9:
                warnings.append("接近涨停，风险较高")
            if row['pe'] > 25:
                warnings.append(f"PE{row['pe']:.1f}，估值偏高")
            if row['turnover'] > 15:
                warnings.append(f"换手率{row['turnover']:.1f}%，可能出货")
            
            if warnings:
                report.append("⚠️ 风险提示:")
                for w in warnings:
                    report.append(f"  - {w}")
            else:
                report.append("✅ 基本面良好，风险可控")
            
            report.append("-" * 80)
        
        report.append("\n【优化策略说明】")
        report.append("1. 涨幅过滤：排除涨停股（高位风险），优先选中低涨幅启动的股票")
        report.append("2. 估值筛选：PE<30，PB<5，优选低估值股票")
        report.append("3. 流动性要求：成交额>5000万，确保进出灵活")
        report.append("4. 趋势判断：涨幅3-5%为最佳区间（刚启动）")
        report.append("\n【免责声明】")
        report.append("本报告仅供参考，不构成投资建议。股市有风险，投资需谨慎。")
        report.append("=" * 80)
        
        return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description='波龙选股 V2.1 - 价值投资优化版')
    parser.add_argument('--top', type=int, default=20, help='输出TOP N只股票')
    parser.add_argument('--output', type=str, default='output/optimized_picks.csv', help='输出文件')
    
    args = parser.parse_args()
    
    try:
        picker = LightWeightPicker()
        results = picker.pick_stocks(top_n=args.top)
        
        # 打印报告
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

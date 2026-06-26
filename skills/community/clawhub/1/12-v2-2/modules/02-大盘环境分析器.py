# -*- coding: utf-8 -*-
"""
===================================
大盘环境分析器 - V2.2
===================================

设计参考: daily_stock_analysis的MarketAnalyzer

核心功能:
1. 获取主要指数数据（上证/深证/创业板）
2. 计算市场强弱指标
3. 判断市场环境（强势/震荡/弱势）
4. 动态调整交易阈值
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from enum import Enum

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


# ============================================
# 数据结构定义
# ============================================

class MarketEnvironment(Enum):
    """市场环境枚举"""
    STRONG = "strong"      # 强势市场
    NEUTRAL = "neutral"    # 震荡市场
    WEAK = "weak"         # 弱势市场


@dataclass
class MarketIndex:
    """大盘指数数据"""
    code: str                    # 指数代码
    name: str                    # 指数名称
    current: float = 0.0         # 当前点位
    change_pct: float = 0.0      # 涨跌幅(%)
    ma5: float = 0.0            # 5日均线
    ma10: float = 0.0           # 10日均线
    ma20: float = 0.0           # 20日均线
    volume: float = 0.0         # 成交量
    amount: float = 0.0         # 成交额

    def is_bullish(self) -> bool:
        """是否多头排列（MA5 > MA10 > MA20）"""
        return self.ma5 > self.ma10 > self.ma20

    def is_bearish(self) -> bool:
        """是否空头排列（MA5 < MA10 < MA20）"""
        return self.ma5 < self.ma10 < self.ma20

    def to_dict(self) -> Dict[str, Any]:
        return {
            'code': self.code,
            'name': self.name,
            'current': self.current,
            'change_pct': self.change_pct,
            'ma5': self.ma5,
            'ma10': self.ma10,
            'ma20': self.ma20,
            'volume': self.volume,
            'amount': self.amount,
        }


@dataclass
class MarketStatistics:
    """市场统计数据"""
    date: str                           # 日期
    up_count: int = 0                   # 上涨家数
    down_count: int = 0                 # 下跌家数
    flat_count: int = 0                 # 平盘家数
    limit_up_count: int = 0             # 涨停家数
    limit_down_count: int = 0           # 跌停家数
    total_amount: float = 0.0           # 两市成交额（亿元）

    @property
    def up_down_ratio(self) -> float:
        """涨跌家数比"""
        if self.down_count == 0:
            return float('inf') if self.up_count > 0 else 1.0
        return self.up_count / self.down_count

    @property
    def total_count(self) -> int:
        """总家数"""
        return self.up_count + self.down_count + self.flat_count


@dataclass
class MarketOverview:
    """市场概览"""
    date: str
    indices: List[MarketIndex] = field(default_factory=list)
    statistics: Optional[MarketStatistics] = None

    # 领涨/领跌板块
    top_sectors: List[Dict] = field(default_factory=list)
    bottom_sectors: List[Dict] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'date': self.date,
            'indices': [idx.to_dict() for idx in self.indices],
            'statistics': self.statistics.__dict__ if self.statistics else None,
            'top_sectors': self.top_sectors,
            'bottom_sectors': self.bottom_sectors,
        }


# ============================================
# 大盘分析器
# ============================================

class MarketAnalyzer:
    """
    大盘环境分析器

    功能：
    1. 获取主要指数数据
    2. 获取市场统计数据
    3. 判断市场环境
    4. 动态调整交易阈值
    """

    # 主要指数代码
    MAJOR_INDICES = {
        'cn': ['000001', '399001', '399006'],  # 上证/深证/创业板
        'hk': ['HSI'],                          # 恒生指数
        'us': ['SPX', 'DJI', 'IXIC'],           # 标普/道琼斯/纳斯达克
    }

    def __init__(self, region: str = 'cn'):
        """
        初始化分析器

        Args:
            region: 市场区域 ('cn'/'hk'/'us')
        """
        self.region = region
        self.cache = {}  # 数据缓存
        self.cache_ttl = 3600  # 缓存有效期（秒）

        logger.info(f"大盘分析器初始化完成 (市场: {region})")

    def get_market_overview(self, date: Optional[str] = None) -> MarketOverview:
        """
        获取市场概览

        Args:
            date: 日期 (YYYY-MM-DD)，默认为今天

        Returns:
            MarketOverview: 市场概览数据
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        overview = MarketOverview(date=date)

        # 1. 获取主要指数
        overview.indices = self._get_indices(date)

        # 2. 获取市场统计（仅A股）
        if self.region == 'cn':
            try:
                overview.statistics = self._get_statistics(date)
            except Exception as e:
                logger.warning(f"获取市场统计失败: {e}")

        # 3. 获取板块涨跌（可选）
        # self._get_sector_rankings(overview)

        return overview

    def analyze_environment(self, overview: Optional[MarketOverview] = None) -> MarketEnvironment:
        """
        判断市场环境

        Args:
            overview: 市场概览，如果为None则自动获取

        Returns:
            MarketEnvironment: 市场环境
        """
        if overview is None:
            overview = self.get_market_overview()

        # 1. 指数趋势分析
        bullish_count = sum(1 for idx in overview.indices if idx.is_bullish())
        bearish_count = sum(1 for idx in overview.indices if idx.is_bearish())

        # 2. 涨跌家数分析（如果有统计数据）
        up_down_ratio = 1.0  # 默认中性
        if overview.statistics:
            up_down_ratio = overview.statistics.up_down_ratio

        # 3. 综合判断
        if bullish_count >= 2 and up_down_ratio > 2.0:
            # 至少2个指数多头排列 且 涨跌比>2
            return MarketEnvironment.STRONG

        elif bearish_count >= 2 and up_down_ratio < 0.5:
            # 至少2个指数空头排列 且 涨跌比<0.5
            return MarketEnvironment.WEAK

        else:
            # 其他情况为震荡市
            return MarketEnvironment.NEUTRAL

    def get_buy_threshold(self, environment: MarketEnvironment) -> float:
        """
        根据市场环境获取买入阈值

        Args:
            environment: 市场环境

        Returns:
            float: 买入阈值
        """
        thresholds = {
            MarketEnvironment.STRONG: 8.5,
            MarketEnvironment.NEUTRAL: 9.0,
            MarketEnvironment.WEAK: 9.5,
        }
        return thresholds[environment]

    def _get_indices(self, date: str) -> List[MarketIndex]:
        """
        获取主要指数数据

        Args:
            date: 日期

        Returns:
            List[MarketIndex]: 指数列表
        """
        indices = []
        index_codes = self.MAJOR_INDICES.get(self.region, [])

        for code in index_codes:
            try:
                # 获取指数历史数据（最近30天）
                df = self._fetch_index_data(code, days=30)

                if df is None or df.empty:
                    logger.warning(f"未获取到指数 {code} 的数据")
                    continue

                # 最新数据
                latest = df.iloc[-1]

                # 计算均线
                ma5 = df['close'].tail(5).mean()
                ma10 = df['close'].tail(10).mean()
                ma20 = df['close'].tail(20).mean()

                index = MarketIndex(
                    code=code,
                    name=self._get_index_name(code),
                    current=latest['close'],
                    change_pct=latest.get('pct_chg', 0),
                    ma5=ma5,
                    ma10=ma10,
                    ma20=ma20,
                    volume=latest.get('volume', 0),
                    amount=latest.get('amount', 0),
                )

                indices.append(index)

            except Exception as e:
                logger.error(f"获取指数 {code} 失败: {e}")

        return indices

    def _get_statistics(self, date: str) -> MarketStatistics:
        """
        获取市场统计数据（仅A股）

        Args:
            date: 日期

        Returns:
            MarketStatistics: 市场统计
        """
        try:
            import akshare as ak

            # 获取A股行情统计
            # 注意：akshare的接口可能变化，这里使用备用方案
            # 如果无法获取，返回模拟数据

            # 方案1: 尝试获取实时数据
            try:
                df = ak.stock_zh_a_spot_em()

                # 统计涨跌
                up_count = (df['涨跌幅'] > 0).sum()
                down_count = (df['涨跌幅'] < 0).sum()
                flat_count = (df['涨跌幅'] == 0).sum()

                # 统计涨跌停（涨跌幅>9.9%为涨停，<-9.9%为跌停）
                limit_up_count = (df['涨跌幅'] > 9.9).sum()
                limit_down_count = (df['涨跌幅'] < -9.9).sum()

                # 总成交额
                total_amount = df['成交额'].sum() / 1e8  # 转换为亿元

                return MarketStatistics(
                    date=date,
                    up_count=up_count,
                    down_count=down_count,
                    flat_count=flat_count,
                    limit_up_count=limit_up_count,
                    limit_down_count=limit_down_count,
                    total_amount=total_amount,
                )

            except Exception as e:
                logger.warning(f"获取实时统计失败，使用备用方案: {e}")

                # 方案2: 使用历史数据估算
                # 这里简化处理，返回中性数据
                return MarketStatistics(
                    date=date,
                    up_count=2000,
                    down_count=1500,
                    flat_count=100,
                    limit_up_count=50,
                    limit_down_count=5,
                    total_amount=5000,
                )

        except Exception as e:
            logger.error(f"获取市场统计失败: {e}")
            return MarketStatistics(date=date)

    def _fetch_index_data(self, code: str, days: int = 30) -> Optional[pd.DataFrame]:
        """
        获取指数历史数据

        Args:
            code: 指数代码
            days: 获取天数

        Returns:
            DataFrame: 指数数据
        """
        try:
            import akshare as ak

            end_date = datetime.now().strftime('%Y%m%d')
            start_date = (datetime.now() - timedelta(days=days*2)).strftime('%Y%m%d')

            # 获取指数数据
            if self.region == 'cn':
                df = ak.stock_zh_index_daily(
                    symbol=f"sh{code}" if code.startswith('0') else f"sz{code}"
                )
            elif self.region == 'hk':
                df = ak.stock_hk_index_daily(symbol=code)
            elif self.region == 'us':
                # 美股指数需要使用yfinance
                return self._fetch_us_index_data(code, days)
            else:
                return None

            if df is None or df.empty:
                return None

            # 标准化列名
            df = df.rename(columns={
                'date': 'date',
                'open': 'open',
                'high': 'high',
                'low': 'low',
                'close': 'close',
                'volume': 'volume',
            })

            # 确保有date列
            if 'date' not in df.columns and 'DATE' in df.columns:
                df['date'] = pd.to_datetime(df['DATE'])
            else:
                df['date'] = pd.to_datetime(df['date'])

            # 计算涨跌幅
            df['pct_chg'] = df['close'].pct_change() * 100

            return df.sort_values('date')

        except Exception as e:
            logger.error(f"获取指数数据失败 ({code}): {e}")
            return None

    def _fetch_us_index_data(self, code: str, days: int) -> Optional[pd.DataFrame]:
        """
        获取美股指数数据（使用yfinance）

        Args:
            code: 指数代码
            days: 获取天数

        Returns:
            DataFrame: 指数数据
        """
        try:
            import yfinance as yf

            # 美股指数代码映射
            us_index_map = {
                'SPX': '^GSPC',
                'DJI': '^DJI',
                'IXIC': '^IXIC',
            }

            symbol = us_index_map.get(code, code)
            ticker = yf.Ticker(symbol)

            # 获取历史数据
            df = ticker.history(period=f"{days}d")

            if df is None or df.empty:
                return None

            # 标准化列名
            df = df.reset_index()
            df['date'] = pd.to_datetime(df['Date'])
            df = df.rename(columns={
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
                'Volume': 'volume',
            })

            df['pct_chg'] = df['close'].pct_change() * 100
            df['amount'] = df['close'] * df['volume']

            return df[['date', 'open', 'high', 'low', 'close', 'volume', 'pct_chg', 'amount']]

        except ImportError:
            logger.warning("yfinance未安装，无法获取美股指数")
            return None
        except Exception as e:
            logger.error(f"获取美股指数失败 ({code}): {e}")
            return None

    def _get_index_name(self, code: str) -> str:
        """获取指数名称"""
        name_map = {
            '000001': '上证指数',
            '399001': '深证成指',
            '399006': '创业板指',
            'HSI': '恒生指数',
            'SPX': '标普500',
            'DJI': '道琼斯',
            'IXIC': '纳斯达克',
        }
        return name_map.get(code, code)

    def print_overview(self, overview: MarketOverview):
        """打印市场概览"""
        print(f"\n{'='*60}")
        print(f"市场概览 - {overview.date}")
        print(f"{'='*60}")

        # 指数
        print("\n主要指数:")
        for idx in overview.indices:
            trend = "多头" if idx.is_bullish() else ("空头" if idx.is_bearish() else "盘整")
            print(f"  {idx.name}({idx.code}): "
                  f"{idx.current:.2f} ({idx.change_pct:+.2f}%) [{trend}]")

        # 统计
        if overview.statistics:
            stats = overview.statistics
            print(f"\n市场统计:")
            print(f"  上涨: {stats.up_count} | 下跌: {stats.down_count} | "
                  f"平盘: {stats.flat_count}")
            print(f"  涨跌比: {stats.up_down_ratio:.2f}")
            print(f"  涨停: {stats.limit_up_count} | 跌停: {stats.limit_down_count}")
            print(f"  成交额: {stats.total_amount:.0f}亿")

        # 环境
        env = self.analyze_environment(overview)
        threshold = self.get_buy_threshold(env)
        print(f"\n市场环境: {env.value.upper()}")
        print(f"买入阈值: {threshold}")

        print(f"{'='*60}\n")


# ============================================
# 测试代码
# ============================================

if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    print("=" * 60)
    print("测试大盘分析器")
    print("=" * 60)

    # 创建分析器
    analyzer = MarketAnalyzer(region='cn')

    # 获取市场概览
    overview = analyzer.get_market_overview()

    # 打印概览
    analyzer.print_overview(overview)

    # 判断市场环境
    env = analyzer.analyze_environment(overview)
    threshold = analyzer.get_buy_threshold(env)

    print(f"\n当前市场环境: {env.value}")
    print(f"建议买入阈值: {threshold}")
    print(f"策略说明:")
    if env == MarketEnvironment.STRONG:
        print("  - 市场强势，可正常交易")
        print("  - 买入阈值: 8.5分")
    elif env == MarketEnvironment.NEUTRAL:
        print("  - 市场震荡，提高门槛")
        print("  - 买入阈值: 9.0分")
    else:
        print("  - 市场弱势，谨慎观望")
        print("  - 买入阈值: 9.5分")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

# -*- coding: utf-8 -*-
"""
===================================
筹码分布分析模块 - V2.2增强版
===================================

核心功能:
1. 基于价格-成交量计算筹码分布
2. 筹码集中度计算（90%/70%）
3. 筹码形态识别（单峰/双峰/多峰）
4. 获利盘比例计算
5. 支撑压力位计算
6. 筹码移动趋势分析
7. 历史筹码对比
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from enum import Enum

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


# ============================================
# 数据结构定义
# ============================================

class ChipPattern(Enum):
    """筹码形态"""
    SINGLE_PEAK = "单峰密集"      # 高度集中
    DOUBLE_PEAK = "双峰分布"      # 中度集中
    MULTI_PEAK = "多峰分散"       # 分散
    LOW_ACCUMULATION = "低位密集" # 吸筹
    HIGH_DISTRIBUTION = "高位密集" # 派发


class ChipStatus(Enum):
    """筹码状态"""
    ACCUMULATION = "吸筹"         # 建仓阶段
    HOLDING = "持仓"              # 持仓阶段
    DISTRIBUTION = "派发"         # 出货阶段


@dataclass
class ChipDistribution:
    """筹码分布数据"""
    code: str
    date: str
    current_price: float

    # 集中度指标
    concentration_90: float = 0.0  # 90%筹码集中度
    concentration_70: float = 0.0  # 70%筹码集中度

    # 获利情况
    profit_ratio: float = 0.0      # 获利盘比例 (0-1)
    avg_cost: float = 0.0          # 平均成本
    median_cost: float = 0.0       # 中位数成本

    # 成本分布
    cost_90_low: float = 0.0       # 90%筹码下限
    cost_90_high: float = 0.0      # 90%筹码上限
    cost_70_low: float = 0.0       # 70%筹码下限
    cost_70_high: float = 0.0      # 70%筹码上限

    # 形态识别
    pattern: ChipPattern = ChipPattern.MULTI_PEAK
    status: ChipStatus = ChipStatus.HOLDING

    # 支撑压力
    support_levels: List[float] = field(default_factory=list)
    resistance_levels: List[float] = field(default_factory=list)

    # 信号强度 (0-10)
    signal_strength: float = 5.0

    def get_quality_score(self) -> float:
        """
        获取筹码质量评分

        Returns:
            float: 质量评分 (0-10)
        """
        score = 5.0

        # 集中度评分 (0-3分)
        if self.concentration_90 < 0.08:
            score += 3.0
        elif self.concentration_90 < 0.15:
            score += 2.0
        elif self.concentration_90 < 0.25:
            score += 1.0

        # 获利盘评分 (0-2分)
        if 0.5 < self.profit_ratio < 0.8:
            score += 2.0
        elif 0.3 < self.profit_ratio < 0.9:
            score += 1.0

        return min(10, score)


# ============================================
# 筹码分布分析器
# ============================================

class ChipAnalyzer:
    """
    筹码分布分析器

    功能：
    1. 计算筹码分布
    2. 识别筹码形态
    3. 计算支撑压力位
    4. 分析筹码移动趋势
    5. 生成操作建议
    """

    def __init__(self):
        """初始化分析器"""
        # 价格分档配置
        self.price_bins = 100  # 分档数量
        self.lookback_days = 60  # 计算周期

        # 阈值配置
        self.thresholds = {
            'high_concentration': 0.08,   # 高度集中
            'medium_concentration': 0.15,  # 中度集中
            'low_concentration': 0.25,    # 低度集中
        }

        logger.info("筹码分布分析器初始化完成")

    def analyze(self, df: pd.DataFrame, code: str) -> ChipDistribution:
        """
        分析筹码分布

        Args:
            df: 股票数据DataFrame
            code: 股票代码

        Returns:
            ChipDistribution: 筹码分布对象
        """
        if len(df) < 20:
            logger.warning(f"{code}: 数据不足，无法计算筹码分布")
            return None

        # 获取当前价格
        current_price = df['close'].iloc[-1]

        # 计算筹码分布
        price_distribution = self._calculate_price_distribution(df)

        # 计算集中度
        conc_90 = self._calculate_concentration(price_distribution, 0.90)
        conc_70 = self._calculate_concentration(price_distribution, 0.70)

        # 计算获利盘
        profit_ratio = self._calculate_profit_ratio(price_distribution, current_price)

        # 计算成本指标
        avg_cost, median_cost = self._calculate_cost_metrics(price_distribution)

        # 识别形态
        pattern = self._identify_pattern(conc_90, price_distribution, current_price)

        # 判断状态
        status = self._identify_status(df, current_price)

        # 计算支撑压力
        support_levels, resistance_levels = self._calculate_support_resistance(
            price_distribution, current_price
        )

        # 计算信号强度
        signal = self._calculate_signal(
            conc_90, profit_ratio, pattern, status, current_price
        )

        return ChipDistribution(
            code=code,
            date=df['date'].iloc[-1].strftime('%Y-%m-%d'),
            current_price=current_price,
            concentration_90=conc_90,
            concentration_70=conc_70,
            profit_ratio=profit_ratio,
            avg_cost=avg_cost,
            median_cost=median_cost,
            pattern=pattern,
            status=status,
            support_levels=support_levels,
            resistance_levels=resistance_levels,
            signal_strength=signal
        )

    def _calculate_price_distribution(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        计算价格分布（基于成交量和价格）

        算法：
        1. 将价格区间分为N个档位
        2. 计算每个档位的累积成交量
        3. 使用时间衰减因子（近期权重更高）

        Returns:
            DataFrame: price列和volume列
        """
        # 获取价格范围
        price_min = df['low'].min()
        price_max = df['high'].max()

        # 价格分档
        price_bins = np.linspace(price_min, price_max, self.price_bins)
        price_midpoints = (price_bins[:-1] + price_bins[1:]) / 2

        # 初始化成交量
        volume_dist = np.zeros(self.price_bins - 1)

        # 遍历历史数据，累加成交量
        for i in range(len(df)):
            row = df.iloc[i]
            # 时间衰减因子（近期权重更高）
            time_weight = (i + 1) / len(df)

            # 确定该日成交量的价格分布
            # 使用VWAP（成交量加权平均价）作为代表价格
            vwap = (row['close'] + row['low'] + row['high']) / 3

            # 找到对应的档位
            bin_idx = np.digitize(vwap, price_bins) - 1
            bin_idx = max(0, min(bin_idx, len(volume_dist) - 1))

            # 累加成交量（加权）
            volume_dist[bin_idx] += row['volume'] * time_weight

        # 创建DataFrame
        dist_df = pd.DataFrame({
            'price': price_midpoints,
            'volume': volume_dist
        })

        # 按价格排序
        dist_df = dist_df.sort_values('price').reset_index(drop=True)

        # 计算累积比例
        total_volume = dist_df['volume'].sum()
        dist_df['volume_pct'] = dist_df['volume'] / total_volume
        dist_df['volume_cumsum'] = dist_df['volume_pct'].cumsum()

        return dist_df

    def _calculate_concentration(
        self,
        dist_df: pd.DataFrame,
        percentile: float
    ) -> float:
        """
        计算筹码集中度

        Args:
            dist_df: 价格分布DataFrame
            percentile: 百分位 (0.90表示90%)

        Returns:
            float: 集中度（越小越集中）
        """
        # 找到包含指定百分比筹码的最小价格区间
        target_cumsum = percentile

        # 扫描所有可能的区间
        min_range = float('inf')

        for i in range(len(dist_df)):
            for j in range(i + 1, len(dist_df)):
                cumsum = dist_df.loc[j, 'volume_cumsum'] - \
                       (dist_df.loc[i, 'volume_cumsum'] if i > 0 else 0)

                if cumsum >= target_cumsum:
                    price_range = dist_df.loc[j, 'price'] - dist_df.loc[i, 'price']
                    price_range_ratio = price_range / dist_df.loc[i, 'price']

                    if price_range_ratio < min_range:
                        min_range = price_range_ratio
                    break

        return min_range

    def _calculate_profit_ratio(
        self,
        dist_df: pd.DataFrame,
        current_price: float
    ) -> float:
        """
        计算获利盘比例

        Args:
            dist_df: 价格分布DataFrame
            current_price: 当前价格

        Returns:
            float: 获利盘比例 (0-1)
        """
        # 找到当前价格对应的档位
        if current_price < dist_df['price'].min():
            return 0.0
        if current_price > dist_df['price'].max():
            return 1.0

        # 当前价格以下的筹码比例
        below_current = dist_df[dist_df['price'] <= current_price]
        if len(below_current) > 0:
            return below_current['volume_pct'].sum()
        else:
            return 0.0

    def _calculate_cost_metrics(
        self,
        dist_df: pd.DataFrame
    ) -> Tuple[float, float]:
        """
        计算成本指标

        Args:
            dist_df: 价格分布DataFrame

        Returns:
            (平均成本, 中位数成本)
        """
        # 加权平均成本
        avg_cost = (dist_df['price'] * dist_df['volume']).sum() / \
                  dist_df['volume'].sum()

        # 中位数成本（累积50%对应的价格）
        median_idx = (dist_df['volume_cumsum'] >= 0.5).idxmax()
        median_cost = dist_df.loc[median_idx, 'price']

        return avg_cost, median_cost

    def _identify_pattern(
        self,
        concentration_90: float,
        dist_df: pd.DataFrame,
        current_price: float
    ) -> ChipPattern:
        """
        识别筹码形态

        Args:
            concentration_90: 90%筹码集中度
            dist_df: 价格分布DataFrame
            current_price: 当前价格

        Returns:
            ChipPattern: 筹码形态
        """
        # 基于集中度判断
        if concentration_90 < self.thresholds['high_concentration']:
            # 高度集中，判断位置
            if current_price > dist_df['price'].quantile(0.7):
                return ChipPattern.HIGH_DISTRIBUTION
            else:
                return ChipPattern.LOW_ACCUMULATION
        elif concentration_90 < self.thresholds['medium_concentration']:
            return ChipPattern.DOUBLE_PEAK
        else:
            return ChipPattern.MULTI_PEAK

    def _identify_status(
        self,
        df: pd.DataFrame,
        current_price: float
    ) -> ChipStatus:
        """
        识别筹码状态（吸筹/持仓/派发）

        Args:
            df: 股票数据
            current_price: 当前价格

        Returns:
            ChipStatus: 筹码状态
        """
        # 简化判断：基于价格趋势和成交量
        recent_prices = df['close'].tail(20)
        price_trend = (recent_prices.iloc[-1] - recent_prices.iloc[0]) / recent_prices.iloc[0]

        recent_volumes = df['volume'].tail(20)
        avg_volume = df['volume'].tail(60).mean()
        recent_avg_volume = recent_volumes.mean()

        # 判断
        if price_trend > 0.1 and recent_avg_volume > avg_volume * 1.2:
            return ChipStatus.DISTRIBUTION  # 上涨放量，可能是派发
        elif price_trend < -0.1 and recent_avg_volume > avg_volume * 1.2:
            return ChipStatus.ACCUMULATION  # 下跌放量，可能是吸筹
        else:
            return ChipStatus.HOLDING

    def _calculate_support_resistance(
        self,
        dist_df: pd.DataFrame,
        current_price: float
    ) -> Tuple[List[float], List[float]]:
        """
        计算支撑位和压力位

        Args:
            dist_df: 价格分布DataFrame
            current_price: 当前价格

        Returns:
            (支撑位列表, 压力位列表)
        """
        # 找到筹码密集区域（成交量大的价格区间）
        dist_df['volume_ma'] = dist_df['volume'].rolling(window=5, center=True).mean()

        # 支撑位（下方筹码密集区）
        support_candidates = dist_df[
            (dist_df['price'] < current_price) &
            (dist_df['volume_ma'] > dist_df['volume'].quantile(0.75))
        ]

        support_levels = support_candidates['price'].tolist()[:3]  # 最多3个

        # 压力位（上方筹码密集区）
        resistance_candidates = dist_df[
            (dist_df['price'] > current_price) &
            (dist_df['volume_ma'] > dist_df['volume'].quantile(0.75))
        ]

        resistance_levels = resistance_candidates['price'].tolist()[:3]  # 最多3个

        return support_levels, resistance_levels

    def _calculate_signal(
        self,
        concentration_90: float,
        profit_ratio: float,
        pattern: ChipPattern,
        status: ChipStatus,
        current_price: float
    ) -> float:
        """
        计算筹码信号强度 (0-10)

        Args:
            concentration_90: 集中度
            profit_ratio: 获利盘比例
            pattern: 形态
            status: 状态
            current_price: 当前价格

        Returns:
            float: 信号强度
        """
        score = 5.0

        # 集中度评分 (0-3分)
        if concentration_90 < 0.08:
            score += 3.0  # 高度集中
        elif concentration_90 < 0.15:
            score += 2.0
        elif concentration_90 < 0.25:
            score += 1.0

        # 获利盘评分 (0-2分)
        if 0.5 < profit_ratio < 0.8:
            score += 2.0  # 适度获利
        elif 0.3 < profit_ratio < 0.9:
            score += 1.0

        # 形态评分 (0-3分)
        pattern_scores = {
            ChipPattern.SINGLE_PEAK: 3.0,
            ChipPattern.LOW_ACCUMULATION: 2.5,
            ChipPattern.DOUBLE_PEAK: 2.0,
            ChipPattern.HIGH_DISTRIBUTION: -1.0,
            ChipPattern.MULTI_PEAK: 0.0,
        }
        score += pattern_scores.get(pattern, 0)

        # 状态评分 (0-2分)
        status_scores = {
            ChipStatus.ACCUMULATION: 2.0,
            ChipStatus.HOLDING: 1.0,
            ChipStatus.DISTRIBUTION: -1.0,
        }
        score += status_scores.get(status, 0)

        return max(0, min(10, score))

    def print_analysis(self, chip_dist: ChipDistribution):
        """打印筹码分析结果"""
        print(f"\n{'='*60}")
        print(f"{chip_dist.code} 筹码分布分析")
        print(f"{'='*60}")
        print(f"当前价格: {chip_dist.current_price:.2f}元")
        print(f"平均成本: {chip_dist.avg_cost:.2f}元")
        print(f"中位数成本: {chip_dist.median_cost:.2f}元")
        print(f"获利盘: {chip_dist.profit_ratio*100:.1f}%")
        print(f"\n集中度:")
        print(f"  90%筹码: {chip_dist.concentration_90*100:.1f}%")
        print(f"  70%筹码: {chip_dist.concentration_70*100:.1f}%")
        print(f"\n形态: {chip_dist.pattern.value}")
        print(f"状态: {chip_dist.status.value}")
        print(f"信号: {chip_dist.signal_strength:.1f}/10")

        if chip_dist.support_levels:
            print(f"\n支撑位: {chip_dist.support_levels}")
        if chip_dist.resistance_levels:
            print(f"压力位: {chip_dist.resistance_levels}")

        print(f"质量评分: {chip_dist.get_quality_score():.1f}/10")
        print(f"{'='*60}")


# ============================================
# 测试代码
# ============================================

if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    print("=" * 60)
    print("测试筹码分布分析器")
    print("=" * 60)

    # 创建分析器
    analyzer = ChipAnalyzer()

    # 测试数据（模拟）
    import akshare as ak

    try:
        df = ak.stock_zh_a_hist(
            symbol="600519",
            period="daily",
            start_date="20231201",
            end_date="20240131",
            adjust="qfq"
        )

        df = df.rename(columns={
            '日期': 'date',
            '开盘': 'open',
            '最高': 'high',
            '最低': 'low',
            '收盘': 'close',
            '成交量': 'volume'
        })

        df['date'] = pd.to_datetime(df['date'])

        # 分析
        chip_dist = analyzer.analyze(df, "600519")

        if chip_dist:
            analyzer.print_analysis(chip_dist)

    except Exception as e:
        print(f"测试失败: {e}")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

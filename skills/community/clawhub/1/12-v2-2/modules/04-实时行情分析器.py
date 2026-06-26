# -*- coding: utf-8 -*-
"""
===================================
实时行情分析模块 - V2.2增强版
===================================

核心功能:
1. 批量获取实时行情
2. 量比分析（5级分类）
3. 换手率分析（5级分类）
4. 量价关系分析
5. 实时监控预警
6. 市场扫描功能
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


# ============================================
# 数据结构定义
# ============================================

class VolumeRatioLevel(Enum):
    """量比等级"""
    EXTREMELY_LOW = "极度缩量"    # < 0.5
    LOW = "缩量"                  # 0.5 - 0.8
    NORMAL = "正常"               # 0.8 - 1.5
    HIGH = "放量"                 # 1.5 - 3.0
    EXTREMELY_HIGH = "巨量"       # > 3.0


class TurnoverRateLevel(Enum):
    """换手率等级"""
    DEAD = "死寂"                 # < 1%
    LOW = "低换手"                # 1% - 3%
    NORMAL = "正常"               # 3% - 7%
    ACTIVE = "活跃"               # 7% - 15%
    HOT = "高换手"                # > 15%


class PriceVolumeRelation(Enum):
    """量价关系"""
    RISE_WITH_VOLUME = "放量上涨"      # 量价齐升
    RISE_WITHOUT_VOLUME = "缩量上涨"   # 量价背离
    FALL_WITH_VOLUME = "放量下跌"      # 恐慌性下跌
    FALL_WITHOUT_VOLUME = "缩量下跌"   # 卖盘衰竭
    CONSOLIDATION = "缩量盘整"         # 多空平衡


@dataclass
class RealtimeAnalysis:
    """实时分析结果"""
    code: str
    name: str

    # 价格数据
    price: float = 0.0
    change_pct: float = 0.0
    amplitude: float = 0.0  # 振幅

    # 量价数据
    volume: int = 0
    volume_ratio: float = 0.0
    turnover_rate: float = 0.0

    # 分析结果
    volume_ratio_level: VolumeRatioLevel = VolumeRatioLevel.NORMAL
    turnover_rate_level: TurnoverRateLevel = TurnoverRateLevel.NORMAL
    price_volume_relation: PriceVolumeRelation = PriceVolumeRelation.CONSOLIDATION

    # 信号强度 (0-10)
    signal_strength: float = 5.0

    # 操作建议
    recommendation: str = "观望"
    reason: str = ""

    # 风险提示
    warnings: List[str] = field(default_factory=list)

    # 分析时间
    timestamp: datetime = field(default_factory=datetime.now)


# ============================================
# 实时行情分析器
# ============================================

class RealtimeAnalyzer:
    """
    实时行情分析器

    功能：
    1. 批量获取实时行情
    2. 量比分析
    3. 换手率分析
    4. 量价关系分析
    5. 信号评分
    6. 风险预警
    """

    def __init__(self, data_manager=None):
        """
        初始化分析器

        Args:
            data_manager: 数据管理器实例
        """
        self.data_manager = data_manager

        # 量比阈值配置
        self.volume_ratio_thresholds = {
            'extremely_low': 0.5,
            'low': 0.8,
            'normal': 1.5,
            'high': 3.0,
        }

        # 换手率阈值配置
        self.turnover_thresholds = {
            'dead': 1.0,
            'low': 3.0,
            'normal': 7.0,
            'active': 15.0,
        }

        logger.info("实时行情分析器初始化完成")

    def analyze_batch(
        self,
        stock_list: List[str]
    ) -> Dict[str, RealtimeAnalysis]:
        """
        批量分析实时行情

        Args:
            stock_list: 股票代码列表

        Returns:
            Dict[str, RealtimeAnalysis]: 分析结果字典
        """
        logger.info(f"开始批量分析 {len(stock_list)} 只股票")

        results = {}

        for code in stock_list:
            try:
                # 获取实时行情
                quote = self._get_realtime_quote(code)

                if quote is None:
                    logger.warning(f"{code}: 未获取到实时行情")
                    continue

                # 分析
                analysis = self._analyze_quote(quote)
                results[code] = analysis

            except Exception as e:
                logger.error(f"{code}: 分析失败 - {e}")

        logger.info(f"批量分析完成: 成功 {len(results)}/{len(stock_list)}")

        return results

    def scan_market(
        self,
        min_signal: float = 7.0,
        max_turnover: float = 20.0
    ) -> List[RealtimeAnalysis]:
        """
        市场扫描功能

        Args:
            min_signal: 最低信号强度
            max_turnover: 最高换手率

        Returns:
            List[RealtimeAnalysis]: 符合条件的股票列表
        """
        logger.info(f"开始市场扫描 (信号≥{min_signal}, 换手≤{max_turnover}%)")

        # 获取所有A股（这里简化处理，实际需要分批）
        # 示例：使用股票池
        stock_pool = [
            '600519', '000858', '600036', '000651', '600276',
            '000333', '601318', '600030', '000002', '002415',
        ]

        results = self.analyze_batch(stock_pool)

        # 筛选
        qualified = [
            r for r in results.values()
            if r.signal_strength >= min_signal
            and r.turnover_rate <= max_turnover
        ]

        # 按信号强度排序
        qualified.sort(key=lambda x: x.signal_strength, reverse=True)

        logger.info(f"扫描完成: 发现 {len(qualified)} 只符合条件的股票")

        return qualified

    def _get_realtime_quote(self, code: str):
        """获取实时行情"""
        if self.data_manager:
            return self.data_manager.get_realtime_quote(code)
        else:
            # 默认使用akshare
            try:
                import akshare as ak
                df = ak.stock_zh_a_spot_em()
                row = df[df['代码'] == code]

                if row.empty:
                    return None

                row = row.iloc[0]

                from data_manager import RealtimeQuote
                return RealtimeQuote(
                    code=code,
                    name=row.get('名称', ''),
                    price=row.get('最新价', 0),
                    volume_ratio=row.get('量比', 1.0),
                    turnover_rate=row.get('换手率', 0),
                    volume=row.get('成交量', 0),
                    amount=row.get('成交额', 0),
                    change_pct=row.get('涨跌幅', 0),
                    source="akshare"
                )
            except Exception as e:
                logger.error(f"获取{code}实时行情失败: {e}")
                return None

    def _analyze_quote(self, quote) -> RealtimeAnalysis:
        """
        分析单个实时行情

        Args:
            quote: RealtimeQuote对象

        Returns:
            RealtimeAnalysis: 分析结果
        """
        # 1. 量比分析
        vr_level = self._analyze_volume_ratio(quote.volume_ratio)

        # 2. 换手率分析
        tr_level = self._analyze_turnover_rate(quote.turnover_rate)

        # 3. 量价关系分析
        pv_relation = self._analyze_price_volume_relation(
            quote.change_pct,
            quote.volume_ratio
        )

        # 4. 计算信号强度
        signal = self._calculate_signal_strength(
            quote.volume_ratio,
            quote.turnover_rate,
            quote.change_pct,
            vr_level,
            tr_level,
            pv_relation
        )

        # 5. 生成建议
        recommendation, reason = self._generate_recommendation(
            signal,
            vr_level,
            tr_level,
            pv_relation,
            quote.change_pct
        )

        # 6. 风险提示
        warnings = self._generate_warnings(
            quote.volume_ratio,
            quote.turnover_rate,
            quote.change_pct,
            vr_level,
            tr_level
        )

        return RealtimeAnalysis(
            code=quote.code,
            name=quote.name,
            price=quote.price,
            change_pct=quote.change_pct,
            volume=quote.volume,
            volume_ratio=quote.volume_ratio,
            turnover_rate=quote.turnover_rate,
            volume_ratio_level=vr_level,
            turnover_rate_level=tr_level,
            price_volume_relation=pv_relation,
            signal_strength=signal,
            recommendation=recommendation,
            reason=reason,
            warnings=warnings
        )

    def _analyze_volume_ratio(self, volume_ratio: float) -> VolumeRatioLevel:
        """分析量比"""
        if volume_ratio < self.volume_ratio_thresholds['extremely_low']:
            return VolumeRatioLevel.EXTREMELY_LOW
        elif volume_ratio < self.volume_ratio_thresholds['low']:
            return VolumeRatioLevel.LOW
        elif volume_ratio < self.volume_ratio_thresholds['normal']:
            return VolumeRatioLevel.NORMAL
        elif volume_ratio < self.volume_ratio_thresholds['high']:
            return VolumeRatioLevel.HIGH
        else:
            return VolumeRatioLevel.EXTREMELY_HIGH

    def _analyze_turnover_rate(self, turnover_rate: float) -> TurnoverRateLevel:
        """分析换手率"""
        if turnover_rate < self.turnover_thresholds['dead']:
            return TurnoverRateLevel.DEAD
        elif turnover_rate < self.turnover_thresholds['low']:
            return TurnoverRateLevel.LOW
        elif turnover_rate < self.turnover_thresholds['normal']:
            return TurnoverRateLevel.NORMAL
        elif turnover_rate < self.turnover_thresholds['active']:
            return TurnoverRateLevel.ACTIVE
        else:
            return TurnoverRateLevel.HOT

    def _analyze_price_volume_relation(
        self,
        change_pct: float,
        volume_ratio: float
    ) -> PriceVolumeRelation:
        """分析量价关系"""
        is_rising = change_pct > 0
        is_high_volume = volume_ratio > 1.2

        if is_rising and is_high_volume:
            return PriceVolumeRelation.RISE_WITH_VOLUME
        elif is_rising and not is_high_volume:
            return PriceVolumeRelation.RISE_WITHOUT_VOLUME
        elif not is_rising and is_high_volume:
            return PriceVolumeRelation.FALL_WITH_VOLUME
        elif not is_rising and not is_high_volume:
            return PriceVolumeRelation.FALL_WITHOUT_VOLUME
        else:
            return PriceVolumeRelation.CONSOLIDATION

    def _calculate_signal_strength(
        self,
        volume_ratio: float,
        turnover_rate: float,
        change_pct: float,
        vr_level: VolumeRatioLevel,
        tr_level: TurnoverRateLevel,
        pv_relation: PriceVolumeRelation
    ) -> float:
        """
        计算信号强度 (0-10)

        评分规则：
        1. 量价配合好 → 高分
        2. 适度放量 → 高分
        3. 活跃换手 → 高分
        4. 上涨趋势 → 高分
        """
        score = 5.0  # 基础分

        # 量价关系评分 (±2分)
        pv_scores = {
            PriceVolumeRelation.RISE_WITH_VOLUME: 2.0,
            PriceVolumeRelation.RISE_WITHOUT_VOLUME: 0.5,
            PriceVolumeRelation.FALL_WITHOUT_VOLUME: 0.0,
            PriceVolumeRelation.FALL_WITH_VOLUME: -1.0,
            PriceVolumeRelation.CONSOLIDATION: 0.0,
        }
        score += pv_scores.get(pv_relation, 0)

        # 量比评分 (±1.5分)
        vr_scores = {
            VolumeRatioLevel.EXTREMELY_LOW: -0.5,
            VolumeRatioLevel.LOW: 0.0,
            VolumeRatioLevel.NORMAL: 1.0,
            VolumeRatioLevel.HIGH: 1.5,
            VolumeRatioLevel.EXTREMELY_HIGH: 0.5,  # 巨量风险
        }
        score += vr_scores.get(vr_level, 0)

        # 换手率评分 (±1.5分)
        tr_scores = {
            TurnoverRateLevel.DEAD: -1.0,
            TurnoverRateLevel.LOW: 0.0,
            TurnoverRateLevel.NORMAL: 1.5,
            TurnoverRateLevel.ACTIVE: 1.0,
            TurnoverRateLevel.HOT: -0.5,  # 过热风险
        }
        score += tr_scores.get(tr_level, 0)

        # 涨跌幅评分 (±1分)
        if change_pct > 5:
            score += 0.5  # 涨幅较大
        elif change_pct > 2:
            score += 1.0
        elif change_pct > 0:
            score += 0.5
        elif change_pct < -5:
            score -= 1.0
        elif change_pct < -2:
            score -= 0.5

        return max(0, min(10, score))

    def _generate_recommendation(
        self,
        signal: float,
        vr_level: VolumeRatioLevel,
        tr_level: TurnoverRateLevel,
        pv_relation: PriceVolumeRelation,
        change_pct: float
    ) -> tuple:
        """生成操作建议"""
        # 买入条件
        buy_conditions = (
            signal >= 7.0 and
            vr_level in [VolumeRatioLevel.NORMAL, VolumeRatioLevel.HIGH] and
            pv_relation == PriceVolumeRelation.RISE_WITH_VOLUME and
            change_pct > 0
        )

        if buy_conditions:
            return "买入", f"信号{signal:.1f}分，{pv_relation.value}，{tr_level.value}"

        # 观望条件
        hold_conditions = (
            signal >= 5.0 and
            pv_relation != PriceVolumeRelation.FALL_WITH_VOLUME
        )

        if hold_conditions:
            return "观望", f"信号{signal:.1f}分，等待更好时机"

        # 卖出/回避条件
        sell_conditions = (
            signal < 5.0 or
            pv_relation == PriceVolumeRelation.FALL_WITH_VOLUME or
            vr_level == VolumeRatioLevel.EXTREMELY_LOW
        )

        if sell_conditions:
            return "回避", f"信号较弱，{pv_relation.value}"

        return "观望", "综合评估中性"

    def _generate_warnings(
        self,
        volume_ratio: float,
        turnover_rate: float,
        change_pct: float,
        vr_level: VolumeRatioLevel,
        tr_level: TurnoverRateLevel
    ) -> List[str]:
        """生成风险提示"""
        warnings = []

        # 量比风险
        if vr_level == VolumeRatioLevel.EXTREMELY_HIGH:
            warnings.append(f"⚠️ 巨量（量比{volume_ratio:.1f}），注意风险")
        elif vr_level == VolumeRatioLevel.EXTREMELY_LOW:
            warnings.append(f"⚠️ 极度缩量（量比{volume_ratio:.1f}），流动性不足")

        # 换手率风险
        if tr_level == TurnoverRateLevel.HOT:
            warnings.append(f"⚠️ 高换手（{turnover_rate:.1f}%），可能过热")
        elif tr_level == TurnoverRateLevel.DEAD:
            warnings.append(f"⚠️ 死寂（换手{turnover_rate:.1f}%），无人关注")

        # 涨跌幅风险
        if change_pct > 7:
            warnings.append(f"⚠️ 涨幅过大（{change_pct:.1f}%），追高风险")
        elif change_pct < -5:
            warnings.append(f"⚠️ 跌幅较大（{change_pct:.1f}%），恐慌情绪")

        return warnings

    def print_analysis(self, analysis: RealtimeAnalysis):
        """打印分析结果"""
        print(f"\n{'='*60}")
        print(f"{analysis.name}({analysis.code}) 实时分析")
        print(f"{'='*60}")
        print(f"价格: {analysis.price:.2f} ({analysis.change_pct:+.2f}%)")
        print(f"量比: {analysis.volume_ratio:.2f} ({analysis.volume_ratio_level.value})")
        print(f"换手: {analysis.turnover_rate:.2f}% ({analysis.turnover_rate_level.value})")
        print(f"量价: {analysis.price_volume_relation.value}")
        print(f"信号: {analysis.signal_strength:.1f}/10")
        print(f"建议: {analysis.recommendation}")
        print(f"原因: {analysis.reason}")

        if analysis.warnings:
            print(f"风险提示:")
            for warning in analysis.warnings:
                print(f"  {warning}")

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
    print("测试实时行情分析器")
    print("=" * 60)

    # 创建分析器
    analyzer = RealtimeAnalyzer()

    # 测试股票
    test_stocks = ['600519', '000858', '600036']

    # 批量分析
    results = analyzer.analyze_batch(test_stocks)

    # 打印结果
    for code, analysis in results.items():
        analyzer.print_analysis(analysis)

    # 市场扫描
    print("\n" + "=" * 60)
    print("市场扫描")
    print("=" * 60)

    scanned = analyzer.scan_market(min_signal=6.0)

    print(f"\n发现 {len(scanned)} 只高信号股票:")
    for i, analysis in enumerate(scanned[:5], 1):
        print(f"{i}. {analysis.name}({analysis.code}): "
              f"信号{analysis.signal_strength:.1f}, "
              f"{analysis.recommendation}")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

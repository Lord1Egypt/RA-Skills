# -*- coding: utf-8 -*-
"""
===================================
完整分析流水线 - V2.2
===================================

设计参考: daily_stock_analysis的Pipeline架构

核心功能:
1. 整合所有模块（数据/信号/决策/通知）
2. 统一的任务调度
3. 并发控制和异常处理
4. 进度监控和结果汇总
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

import pandas as pd
import numpy as np

# 导入各模块
from data_manager import DataFetcherManager, RealtimeQuote, ChipDistribution
from market_analyzer import MarketAnalyzer, MarketEnvironment
from email_notifier import EmailNotifier, NotificationConfig

logger = logging.getLogger(__name__)


# ============================================
# 数据结构定义
# ============================================

@dataclass
class StockAnalysisResult:
    """股票分析结果"""
    code: str
    name: str

    # 信号数据
    signal_score: float = 0.0
    signal_details: Dict[str, float] = field(default_factory=dict)

    # 实时行情
    realtime_quote: Optional[RealtimeQuote] = None

    # 筹码分布
    chip_distribution: Optional[ChipDistribution] = None

    # 市场环境
    market_environment: str = "neutral"

    # 交易建议
    recommendation: str = "hold"  # buy/sell/hold
    reason: str = ""

    # 风险指标
    risk_level: str = "medium"  # low/medium/high

    # 分析时间
    timestamp: datetime = field(default_factory=datetime.now)


# ============================================
# 完整分析流水线
# ============================================

class StockAnalysisPipeline:
    """
    完整分析流水线

    整合流程：
    数据获取 → 实时行情 → 筹码分析 → 大盘环境 →
    信号计算 → 决策执行 → 风险控制 → 通知推送
    """

    def __init__(
        self,
        config: Optional[Dict] = None,
        notifier_config: Optional[NotificationConfig] = None
    ):
        """
        初始化流水线

        Args:
            config: 系统配置
            notifier_config: 通知配置
        """
        self.config = config or {}

        # 初始化各模块
        logger.info("初始化分析流水线...")

        # 1. 数据管理器
        self.data_manager = DataFetcherManager(config.get('data_sources'))
        logger.info("✓ 数据管理器已初始化")

        # 2. 大盘分析器
        self.market_analyzer = MarketAnalyzer(region=config.get('region', 'cn'))
        logger.info("✓ 大盘分析器已初始化")

        # 3. 邮件通知器（可选）
        self.notifier = None
        if notifier_config and notifier_config.enabled:
            self.notifier = EmailNotifier(notifier_config)
            logger.info("✓ 邮件通知器已初始化")
        else:
            logger.info("○ 邮件通知器已禁用")

        # 配置参数
        self.max_workers = config.get('max_workers', 4)
        self.enable_realtime = config.get('realtime', {}).get('enabled', True)
        self.enable_chip = config.get('chip_distribution', {}).get('enabled', True)
        self.enable_market_env = config.get('market_environment', {}).get('enabled', True)

        logger.info(f"分析流水线初始化完成 (并发数: {self.max_workers})")

    def analyze_stocks(
        self,
        stock_list: List[str],
        buy_threshold: Optional[float] = None,
        send_notification: bool = True
    ) -> Dict[str, StockAnalysisResult]:
        """
        批量分析股票

        Args:
            stock_list: 股票代码列表
            buy_threshold: 买入阈值（如为None则根据市场环境动态调整）
            send_notification: 是否发送通知

        Returns:
            Dict[str, StockAnalysisResult]: 分析结果字典
        """
        logger.info("=" * 60)
        logger.info(f"开始批量分析 {len(stock_list)} 只股票")
        logger.info("=" * 60)

        results = {}
        failed = []

        # 1. 判断市场环境（如果启用）
        market_env = MarketEnvironment.NEUTRAL
        if self.enable_market_env:
            try:
                overview = self.market_analyzer.get_market_overview()
                market_env = self.market_analyzer.analyze_environment(overview)
                logger.info(f"市场环境: {market_env.value}")
            except Exception as e:
                logger.warning(f"获取市场环境失败: {e}")

        # 2. 动态调整买入阈值
        if buy_threshold is None:
            buy_threshold = self.market_analyzer.get_buy_threshold(market_env)

        logger.info(f"买入阈值: {buy_threshold}")

        # 3. 并发分析股票
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交任务
            future_to_stock = {
                executor.submit(self._analyze_single_stock, code, buy_threshold): code
                for code in stock_list
            }

            # 收集结果
            for future in as_completed(future_to_stock):
                code = future_to_stock[future]
                try:
                    result = future.result(timeout=30)
                    if result:
                        results[code] = result
                        logger.info(f"✓ {code}: 信号={result.signal_score:.2f}, "
                                  f"建议={result.recommendation}")
                    else:
                        failed.append(code)
                        logger.warning(f"✗ {code}: 分析失败")
                except Exception as e:
                    failed.append(code)
                    logger.error(f"✗ {code}: 分析异常 - {e}")

        # 4. 发送大盘复盘通知
        if send_notification and self.notifier and self.enable_market_env:
            try:
                overview = self.market_analyzer.get_market_overview()
                overview_dict = overview.to_dict()
                self.notifier.send_market_review(overview_dict, market_env.value)
            except Exception as e:
                logger.warning(f"发送大盘复盘失败: {e}")

        # 5. 汇总统计
        logger.info("\n" + "=" * 60)
        logger.info("分析结果汇总")
        logger.info("=" * 60)
        logger.info(f"成功: {len(results)}/{len(stock_list)}")
        logger.info(f"失败: {len(failed)}/{len(stock_list)}")

        if results:
            recommendations = [r.recommendation for r in results.values()]
            buy_count = recommendations.count('buy')
            sell_count = recommendations.count('sell')
            hold_count = recommendations.count('hold')

            logger.info(f"买入: {buy_count} | 卖出: {sell_count} | 观望: {hold_count}")

        return results

    def _analyze_single_stock(
        self,
        code: str,
        buy_threshold: float
    ) -> Optional[StockAnalysisResult]:
        """
        分析单只股票（完整流程）

        Args:
            code: 股票代码
            buy_threshold: 买入阈值

        Returns:
            StockAnalysisResult: 分析结果
        """
        try:
            # Step 1: 获取历史数据
            df = self.data_manager.get_daily_data(code, days=60)
            if df is None or len(df) < 20:
                logger.warning(f"{code}: 数据不足")
                return None

            # Step 2: 计算技术指标
            df = self._calculate_indicators(df)

            # Step 3: 获取实时行情
            realtime_quote = None
            if self.enable_realtime:
                try:
                    realtime_quote = self.data_manager.get_realtime_quote(code)
                except Exception as e:
                    logger.debug(f"{code}: 获取实时行情失败 - {e}")

            # Step 4: 计算筹码分布
            chip_dist = None
            if self.enable_chip:
                try:
                    chip_dist = self._calculate_chip_distribution(df)
                except Exception as e:
                    logger.debug(f"{code}: 计算筹码分布失败 - {e}")

            # Step 5: 计算信号
            signal_score = self._calculate_signal(df, realtime_quote, chip_dist)

            # Step 6: 生成交易建议
            recommendation, reason = self._generate_recommendation(
                signal_score, buy_threshold, df
            )

            # Step 7: 风险评估
            risk_level = self._assess_risk(df, signal_score)

            # 创建结果对象
            result = StockAnalysisResult(
                code=code,
                name=self._get_stock_name(code, realtime_quote),
                signal_score=signal_score,
                realtime_quote=realtime_quote,
                chip_distribution=chip_dist,
                recommendation=recommendation,
                reason=reason,
                risk_level=risk_level,
            )

            # Step 8: 发送通知（买入/卖出信号）
            if self.notifier and realtime_quote:
                if recommendation == 'buy':
                    self.notifier.send_buy_signal(
                        code=code,
                        name=result.name,
                        price=realtime_quote.price,
                        signal_score=signal_score,
                        market_env="neutral"
                    )
                elif recommendation == 'sell':
                    # 卖出信号需要更多信息，这里简化处理
                    pass

            return result

        except Exception as e:
            logger.error(f"{code}: 分析失败 - {e}")
            return None

    def _calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """计算技术指标"""
        df = df.copy()

        # 移动平均线
        df['ma5'] = df['close'].rolling(window=5).mean()
        df['ma10'] = df['close'].rolling(window=10).mean()
        df['ma20'] = df['close'].rolling(window=20).mean()
        df['ma60'] = df['close'].rolling(window=60).mean()

        # 动量指标
        df['momentum'] = df['close'].pct_change(5)

        # 均线偏离度
        df['ma_dev'] = (df['close'] - df['ma20']) / df['ma20']

        # 成交量比率
        df['vol_ratio'] = df['volume'] / df['volume'].rolling(window=5).mean()

        # 波动率
        df['volatility'] = df['close'].pct_change().rolling(window=20).std()

        # MACD
        df['ema12'] = df['close'].ewm(span=12).mean()
        df['ema26'] = df['close'].ewm(span=26).mean()
        df['macd'] = df['ema12'] - df['ema26']
        df['macd_signal'] = df['macd'].ewm(span=9).mean()
        df['macd_hist'] = df['macd'] - df['macd_signal']

        # 布林带
        df['bb_middle'] = df['close'].rolling(window=20).mean()
        df['bb_std'] = df['close'].rolling(window=20).std()
        df['bb_upper'] = df['bb_middle'] + 2 * df['bb_std']
        df['bb_lower'] = df['bb_middle'] - 2 * df['bb_std']
        df['bb_position'] = (df['close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])

        return df

    def _calculate_signal(
        self,
        df: pd.DataFrame,
        realtime_quote: Optional[RealtimeQuote],
        chip_dist: Optional[ChipDistribution]
    ) -> float:
        """
        V2.2 信号计算（8因子）

        Returns:
            float: 信号评分 (0-10)
        """
        idx = len(df) - 1

        # 1. 动量指标 (25%)
        momentum = df.loc[idx, 'momentum'] if pd.notna(df.loc[idx, 'momentum']) else 0
        momentum_signal = ((momentum + 0.15) / 0.30 * 10).clip(0, 10) * 0.25

        # 2. 均线偏离 (20%)
        ma_dev = df.loc[idx, 'ma_dev'] if pd.notna(df.loc[idx, 'ma_dev']) else 0
        ma_dev_signal = (1 - (ma_dev + 0.10) / 0.20 * 5).clip(0, 10) * 0.20

        # 3. 成交量 (15%)
        vol_ratio = df.loc[idx, 'vol_ratio'] if pd.notna(df.loc[idx, 'vol_ratio']) else 1
        vol_signal = ((vol_ratio - 0.5) / 1.5 * 5 + 5).clip(0, 10) * 0.15

        # 4. 波动率 (10%)
        volatility = df.loc[idx, 'volatility'] if pd.notna(df.loc[idx, 'volatility']) else 0.03
        volatility_signal = (1 - volatility / 0.10 * 5).clip(0, 10) * 0.10

        # 5. MACD (10%)
        macd_hist = df.loc[idx, 'macd_hist'] if pd.notna(df.loc[idx, 'macd_hist']) else 0
        macd_signal = ((macd_hist + 0.05) / 0.10 * 5 + 5).clip(0, 10) * 0.10

        # 6. 布林带 (10%)
        bb_position = df.loc[idx, 'bb_position'] if pd.notna(df.loc[idx, 'bb_position']) else 0.5
        bb_signal = bb_position * 10 * 0.10

        # 7. 量比 (5%)
        if realtime_quote and realtime_quote.volume_ratio:
            vr = realtime_quote.volume_ratio
            if 1.0 <= vr < 2.0:
                vr_signal = 6.0
            elif 2.0 <= vr < 3.0:
                vr_signal = 8.0
            elif 3.0 <= vr < 5.0:
                vr_signal = 9.0
            elif vr >= 5.0:
                vr_signal = 5.0
            else:
                vr_signal = 3.0
        else:
            vr_signal = 5.0
        vr_signal = vr_signal * 0.05

        # 8. 筹码集中度 (5%)
        if chip_dist:
            conc = chip_dist.concentration_90
            if conc < 0.08:
                chip_signal = 9.0
            elif conc < 0.15:
                chip_signal = 7.0
            elif conc < 0.25:
                chip_signal = 5.0
            else:
                chip_signal = 3.0
        else:
            # 使用价格波动率作为代理指标
            prices = df['close'].tail(60)
            cv = (prices.std() / prices.mean()) * 100
            if cv < 5:
                chip_signal = 9.0
            elif cv < 10:
                chip_signal = 7.0
            elif cv < 15:
                chip_signal = 5.0
            else:
                chip_signal = 3.0
        chip_signal = chip_signal * 0.05

        # 综合评分
        signal = (
            momentum_signal + ma_dev_signal + vol_signal +
            volatility_signal + macd_signal + bb_signal +
            vr_signal + chip_signal
        ).clip(0, 10)

        return signal

    def _calculate_chip_distribution(self, df: pd.DataFrame) -> ChipDistribution:
        """计算筹码分布（简化版）"""
        prices = df['close'].tail(60)

        # 使用价格变异系数作为集中度指标
        std_dev = prices.std()
        mean_price = prices.mean()

        cv = (std_dev / mean_price) if mean_price > 0 else 0

        # 转换为集中度（CV越小越集中）
        concentration_90 = min(cv * 2, 1.0)  # 简化映射

        # 计算获利盘比例
        current_price = df['close'].iloc[-1]
        profit_ratio = (prices < current_price).sum() / len(prices)

        return ChipDistribution(
            code=df.get('code', ''),
            date=df['date'].iloc[-1].strftime('%Y-%m-%d'),
            profit_ratio=profit_ratio,
            avg_cost=mean_price,
            concentration_90=concentration_90,
            concentration_70=concentration_90 * 0.8,
        )

    def _generate_recommendation(
        self,
        signal_score: float,
        buy_threshold: float,
        df: pd.DataFrame
    ) -> tuple:
        """
        生成交易建议

        Returns:
            (recommendation, reason)
        """
        # 买入判断
        if signal_score >= buy_threshold:
            # 检查MACD
            macd_hist = df['macd_hist'].iloc[-1]
            if macd_hist > 0:
                return 'buy', f"信号{signal_score:.2f}≥{buy_threshold}，MACD多头"
            else:
                return 'hold', f"信号{signal_score:.2f}≥{buy_threshold}，但MACD弱势"

        # 卖出判断
        elif signal_score <= 6.5:
            return 'sell', f"信号{signal_score:.2f}≤6.5，趋势转弱"

        # 观望
        else:
            return 'hold', f"信号{signal_score:.2f}，观望等待"

    def _assess_risk(self, df: pd.DataFrame, signal_score: float) -> str:
        """评估风险等级"""
        # 计算波动率
        volatility = df['close'].pct_change().tail(20).std()

        if volatility > 0.04 or signal_score < 4.0:
            return 'high'
        elif volatility > 0.025 or signal_score < 6.0:
            return 'medium'
        else:
            return 'low'

    def _get_stock_name(
        self,
        code: str,
        realtime_quote: Optional[RealtimeQuote]
    ) -> str:
        """获取股票名称"""
        if realtime_quote and realtime_quote.name:
            return realtime_quote.name
        return f"股票{code}"


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
    print("测试完整分析流水线")
    print("=" * 60)

    # 创建流水线
    pipeline = StockAnalysisPipeline(
        config={
            'region': 'cn',
            'max_workers': 4,
            'realtime': {'enabled': True},
            'chip_distribution': {'enabled': True},
            'market_environment': {'enabled': True},
        },
        notifier_config=None,  # 不发送通知
    )

    # 测试股票列表
    stock_list = ['600519', '000858', '600036']

    # 批量分析
    results = pipeline.analyze_stocks(stock_list, send_notification=False)

    # 打印结果
    print("\n" + "=" * 60)
    print("分析结果详情")
    print("=" * 60)

    for code, result in results.items():
        print(f"\n{result.name}({code}):")
        print(f"  信号评分: {result.signal_score:.2f}/10")
        print(f"  交易建议: {result.recommendation}")
        print(f"  建议原因: {result.reason}")
        print(f"  风险等级: {result.risk_level}")

        if result.realtime_quote:
            print(f"  最新价格: {result.realtime_quote.price:.2f}")
            print(f"  量比: {result.realtime_quote.volume_ratio}")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

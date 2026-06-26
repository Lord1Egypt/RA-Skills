"""
时空共振策略
四维度模型：周期维度（市场状态识别）、基础维度（价值与质量筛选）、
技术维度（价格行为验证）、情绪维度（不用）
投资哲学：单一维度Alpha衰减理论，多维共振创造高概率机会
"""

import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import random
import numpy as np

from .base_strategy import BaseStrategy

logger = logging.getLogger(__name__)


class ResonanceStrategy(BaseStrategy):
    """时空共振策略（四维度模型）"""
    
    def __init__(self,
                 four_dimensions: Dict[str, bool] = None,
                 fundamental_factors: Dict[str, float] = None,
                 momentum_factors: Dict[str, float] = None,
                 technical_factors: Dict[str, any] = None,
                 holding_count: int = 12,
                 rebalance_days: int = 10,
                 enabled: bool = True,
                 weight: float = 0.07,
                 **kwargs):
        """
        初始化时空共振策略
        
        Args:
            four_dimensions: 四维度启用配置
            fundamental_factors: 基础维度因子
            momentum_factors: 动量因子
            technical_factors: 技术维度因子
            holding_count: 持仓数量
            rebalance_days: 调仓周期
            enabled: 是否启用
            weight: 策略权重
            **kwargs: 其他参数
        """
        # 默认四维度配置
        if four_dimensions is None:
            four_dimensions = {
                "cycle": True,      # 周期维度（由自适应引擎处理）
                "fundamental": True, # 基础维度
                "sentiment": False,  # 情绪维度（暂不使用）
                "technical": True    # 技术维度
            }
        
        # 默认基础维度因子
        if fundamental_factors is None:
            fundamental_factors = {
                "min_roe": 0.15,       # ROE≥15%
                "max_debt_ratio": 0.60, # 资产负债率≤60%
                "min_gross_margin": 0.30, # 毛利率≥30%
                "pe_vs_industry": 0.8,  # PE<行业平均80%
                "pb_vs_industry": 0.8,  # PB<行业平均80%
                "min_dividend_yield": 0.02 # 股息率>2%
            }
        
        # 默认动量因子
        if momentum_factors is None:
            momentum_factors = {
                "min_6m_return": 0.10,  # 6个月收益率>10%
                "min_12m_return": 0.20  # 12个月收益率>20%
            }
        
        # 默认技术维度因子
        if technical_factors is None:
            technical_factors = {
                "consolidation_days": 20,    # 盘整平台20天
                "consolidation_range": 0.15, # 波动幅度≤15%
                "breakout_threshold": 0.03,  # 突破上沿3%
                "volume_ratio": 1.5,         # 成交量至5日均量1.5倍
                "fibonacci_windows": [3, 5, 8, 13, 21] # 斐波那契时间窗口
            }
        
        super().__init__(
            name="ResonanceStrategy",
            enabled=enabled,
            weight=weight,
            four_dimensions=four_dimensions,
            fundamental_factors=fundamental_factors,
            momentum_factors=momentum_factors,
            technical_factors=technical_factors,
            holding_count=holding_count,
            rebalance_days=rebalance_days,
            **kwargs
        )
        
        # 策略状态
        self.last_rebalance = None
        self.current_holdings = []
        
        logger.info(f"时空共振策略初始化: 持仓数={holding_count}, 调仓周期={rebalance_days}天")
    
    def generate_signals(self, market_data: Dict[str, Dict], 
                        fundamental_data: Optional[Dict[str, Dict]] = None,
                        technical_data: Optional[Dict[str, Dict]] = None) -> List[Dict]:
        """
        生成时空共振策略交易信号
        
        Args:
            market_data: 市场数据
            fundamental_data: 基本面数据
            technical_data: 技术指标数据
        
        Returns:
            交易信号列表
        """
        signals = []
        
        if not market_data:
            logger.warning("时空共振策略: 缺少市场数据")
            return signals
        
        # 检查是否需要调仓
        if not self._should_rebalance():
            logger.debug("时空共振策略: 未到调仓时间，维持当前持仓")
            return self._generate_hold_signals()
        
        # 获取候选股票
        candidate_symbols = list(market_data.keys())
        
        # 如果没有基本面数据，尝试从市场数据获取部分信息
        if fundamental_data is None:
            fundamental_data = self._extract_fundamental_from_market(market_data)
        
        # 四维度筛选
        dimension_filters = self.parameters["four_dimensions"]
        
        # 基础维度筛选
        if dimension_filters.get("fundamental", True):
            candidate_symbols = self._apply_fundamental_filter(candidate_symbols, fundamental_data)
        
        # 技术维度筛选
        if dimension_filters.get("technical", True) and technical_data:
            candidate_symbols = self._apply_technical_filter(candidate_symbols, market_data, technical_data)
        
        # 动量维度筛选（如果有历史数据）
        if dimension_filters.get("momentum", True):
            candidate_symbols = self._apply_momentum_filter(candidate_symbols, market_data, technical_data)
        
        if not candidate_symbols:
            logger.warning("时空共振策略: 四维度筛选后无符合条件股票")
            return signals
        
        # 计算综合评分
        scores = self._calculate_composite_scores(candidate_symbols, market_data, fundamental_data, technical_data)
        
        # 按评分排序（得分越高越好）
        sorted_symbols = self._sort_by_score(candidate_symbols, scores)
        
        # 选择目标持仓
        target_holdings = sorted_symbols[:self.parameters["holding_count"]]
        
        # 生成交易信号
        signals = self._generate_rebalance_signals(target_holdings, market_data)
        
        # 更新持仓和调仓时间
        self.current_holdings = target_holdings
        self.last_rebalance = datetime.now()
        
        self.signals_generated += len(signals)
        logger.info(f"时空共振策略生成 {len(signals)} 个信号，目标持仓: {target_holdings[:5]}...")
        
        return signals
    
    def _should_rebalance(self) -> bool:
        """检查是否需要调仓"""
        if self.last_rebalance is None:
            return True
        
        rebalance_days = self.parameters.get("rebalance_days", 10)
        days_since_rebalance = (datetime.now() - self.last_rebalance).days
        
        return days_since_rebalance >= rebalance_days
    
    def _extract_fundamental_from_market(self, market_data: Dict[str, Dict]) -> Dict[str, Dict]:
        """从市场数据中提取基本面信息"""
        fundamental_data = {}
        
        for symbol, mkt_data in market_data.items():
            price = mkt_data.get("price", 0)
            
            # 模拟基本面数据
            fundamental_data[symbol] = {
                "roe": random.uniform(0.05, 0.35),
                "debt_ratio": random.uniform(0.2, 0.8),
                "gross_margin": random.uniform(0.15, 0.65),
                "pe": random.uniform(5.0, 60.0),
                "pb": random.uniform(0.5, 8.0),
                "dividend_yield": random.uniform(0.0, 0.08),
                "market_cap": mkt_data.get("market_cap", random.uniform(500000000, 500000000000))
            }
        
        return fundamental_data
    
    def _apply_fundamental_filter(self, symbols: List[str], fundamental_data: Dict[str, Dict]) -> List[str]:
        """应用基础维度筛选"""
        filtered = []
        factors = self.parameters["fundamental_factors"]
        
        for symbol in symbols:
            if symbol not in fundamental_data:
                continue
            
            fund_data = fundamental_data[symbol]
            passed = True
            
            # ROE筛选
            roe = fund_data.get("roe", 0)
            if roe < factors.get("min_roe", 0.15):
                passed = False
                continue
            
            # 资产负债率筛选
            debt_ratio = fund_data.get("debt_ratio", 1.0)
            if debt_ratio > factors.get("max_debt_ratio", 0.60):
                passed = False
                continue
            
            # 毛利率筛选
            gross_margin = fund_data.get("gross_margin", 0)
            if gross_margin < factors.get("min_gross_margin", 0.30):
                passed = False
                continue
            
            # 股息率筛选
            dividend_yield = fund_data.get("dividend_yield", 0)
            if dividend_yield < factors.get("min_dividend_yield", 0.02):
                passed = False
                continue
            
            # PE、PB相对行业筛选（简化：使用绝对值）
            pe = fund_data.get("pe", 1000)
            pb = fund_data.get("pb", 1000)
            
            # 简化：假设行业平均PE=30，PB=3
            industry_pe_avg = 30.0
            industry_pb_avg = 3.0
            
            if pe > industry_pe_avg * factors.get("pe_vs_industry", 0.8):
                passed = False
                continue
            
            if pb > industry_pb_avg * factors.get("pb_vs_industry", 0.8):
                passed = False
                continue
            
            if passed:
                filtered.append(symbol)
        
        return filtered
    
    def _apply_technical_filter(self, symbols: List[str], 
                               market_data: Dict[str, Dict],
                               technical_data: Dict[str, Dict]) -> List[str]:
        """应用技术维度筛选（盘整突破）"""
        filtered = []
        factors = self.parameters["technical_factors"]
        
        for symbol in symbols:
            if symbol not in market_data or symbol not in technical_data:
                continue
            
            tech_data = technical_data[symbol]
            
            # 检查盘整平台（简化实现）
            consolidation_days = factors.get("consolidation_days", 20)
            consolidation_range = factors.get("consolidation_range", 0.15)
            
            # 模拟盘整检测
            is_consolidating = tech_data.get("is_consolidating", random.random() < 0.3)
            
            if not is_consolidating:
                continue
            
            # 检查突破条件
            price = market_data[symbol].get("price", 0)
            consolidation_high = tech_data.get("consolidation_high", price * 1.1)
            breakout_threshold = factors.get("breakout_threshold", 0.03)
            
            # 突破上沿3%以上
            if price < consolidation_high * (1 + breakout_threshold):
                continue
            
            # 成交量条件：成交量大至5日均量1.5倍以上
            volume = market_data[symbol].get("volume", 0)
            volume_ma5 = tech_data.get("volume_ma5", volume * 0.8)
            volume_ratio = factors.get("volume_ratio", 1.5)
            
            if volume < volume_ma5 * volume_ratio:
                continue
            
            # 斐波那契时间窗口（简化：随机检查）
            current_day = datetime.now().day
            fib_windows = factors.get("fibonacci_windows", [3, 5, 8, 13, 21])
            
            # 简化：检查当前是否在斐波那契窗口附近
            in_fib_window = any(abs(current_day % window) < 2 for window in fib_windows)
            
            if not in_fib_window:
                # 不是必须条件，但加分
                pass
            
            filtered.append(symbol)
        
        return filtered
    
    def _apply_momentum_filter(self, symbols: List[str], 
                              market_data: Dict[str, Dict],
                              technical_data: Dict[str, Dict]) -> List[str]:
        """应用动量维度筛选"""
        filtered = []
        factors = self.parameters["momentum_factors"]
        
        for symbol in symbols:
            if symbol not in technical_data:
                continue
            
            tech_data = technical_data[symbol]
            
            # 6个月收益率
            return_6m = tech_data.get("return_6m", random.uniform(-0.3, 0.5))
            if return_6m < factors.get("min_6m_return", 0.10):
                continue
            
            # 12个月收益率
            return_12m = tech_data.get("return_12m", random.uniform(-0.2, 0.8))
            if return_12m < factors.get("min_12m_return", 0.20):
                continue
            
            filtered.append(symbol)
        
        return filtered
    
    def _calculate_composite_scores(self, symbols: List[str],
                                   market_data: Dict[str, Dict],
                                   fundamental_data: Dict[str, Dict],
                                   technical_data: Dict[str, Dict]) -> Dict[str, float]:
        """计算综合评分"""
        scores = {}
        
        for symbol in symbols:
            if symbol not in market_data:
                continue
            
            score = 0.0
            weight_sum = 0.0
            
            # 基础维度评分（权重40%）
            if symbol in fundamental_data:
                fund_score = self._calculate_fundamental_score(symbol, fundamental_data)
                score += fund_score * 0.4
                weight_sum += 0.4
            
            # 技术维度评分（权重35%）
            if technical_data and symbol in technical_data:
                tech_score = self._calculate_technical_score(symbol, market_data, technical_data)
                score += tech_score * 0.35
                weight_sum += 0.35
            
            # 动量维度评分（权重25%）
            if technical_data and symbol in technical_data:
                momentum_score = self._calculate_momentum_score(symbol, technical_data)
                score += momentum_score * 0.25
                weight_sum += 0.25
            
            # 归一化
            if weight_sum > 0:
                scores[symbol] = score / weight_sum
            else:
                scores[symbol] = 0.5
        
        return scores
    
    def _calculate_fundamental_score(self, symbol: str, fundamental_data: Dict[str, Dict]) -> float:
        """计算基础维度评分"""
        if symbol not in fundamental_data:
            return 0.5
        
        fund_data = fundamental_data[symbol]
        factors = self.parameters["fundamental_factors"]
        
        score = 0.0
        factor_count = 0
        
        # ROE评分
        roe = fund_data.get("roe", 0)
        roe_target = factors.get("min_roe", 0.15)
        roe_score = min(1.0, roe / roe_target) if roe_target > 0 else 0.5
        score += roe_score
        factor_count += 1
        
        # 资产负债率评分（越低越好）
        debt_ratio = fund_data.get("debt_ratio", 0.5)
        debt_target = factors.get("max_debt_ratio", 0.60)
        debt_score = 1.0 - min(1.0, debt_ratio / debt_target) if debt_target > 0 else 0.5
        score += debt_score
        factor_count += 1
        
        # 毛利率评分
        gross_margin = fund_data.get("gross_margin", 0)
        margin_target = factors.get("min_gross_margin", 0.30)
        margin_score = min(1.0, gross_margin / margin_target) if margin_target > 0 else 0.5
        score += margin_score
        factor_count += 1
        
        # 股息率评分
        dividend_yield = fund_data.get("dividend_yield", 0)
        dividend_target = factors.get("min_dividend_yield", 0.02)
        dividend_score = min(1.0, dividend_yield / dividend_target) if dividend_target > 0 else 0.5
        score += dividend_score
        factor_count += 1
        
        if factor_count > 0:
            return score / factor_count
        else:
            return 0.5
    
    def _calculate_technical_score(self, symbol: str, 
                                  market_data: Dict[str, Dict],
                                  technical_data: Dict[str, Dict]) -> float:
        """计算技术维度评分"""
        if symbol not in technical_data:
            return 0.5
        
        tech_data = technical_data[symbol]
        
        score = 0.0
        factor_count = 0
        
        # 盘整突破评分
        is_consolidating = tech_data.get("is_consolidating", False)
        if is_consolidating:
            score += 0.8
        else:
            score += 0.3
        factor_count += 1
        
        # 成交量配合评分
        volume_ratio = tech_data.get("volume_ratio", 1.0)
        volume_score = min(1.0, volume_ratio / 1.5)  # 1.5倍为目标
        score += volume_score
        factor_count += 1
        
        # 趋势评分（使用均线）
        price = market_data.get(symbol, {}).get("price", 0)
        price_ma20 = tech_data.get("price_ma20", price)
        
        if price > price_ma20:
            score += 0.7
        else:
            score += 0.3
        factor_count += 1
        
        if factor_count > 0:
            return score / factor_count
        else:
            return 0.5
    
    def _calculate_momentum_score(self, symbol: str, technical_data: Dict[str, Dict]) -> float:
        """计算动量维度评分"""
        if symbol not in technical_data:
            return 0.5
        
        tech_data = technical_data[symbol]
        factors = self.parameters["momentum_factors"]
        
        score = 0.0
        factor_count = 0
        
        # 6个月收益率评分
        return_6m = tech_data.get("return_6m", 0)
        target_6m = factors.get("min_6m_return", 0.10)
        score_6m = min(1.0, return_6m / target_6m) if target_6m > 0 else 0.5
        score += score_6m
        factor_count += 1
        
        # 12个月收益率评分
        return_12m = tech_data.get("return_12m", 0)
        target_12m = factors.get("min_12m_return", 0.20)
        score_12m = min(1.0, return_12m / target_12m) if target_12m > 0 else 0.5
        score += score_12m
        factor_count += 1
        
        if factor_count > 0:
            return score / factor_count
        else:
            return 0.5
    
    def _sort_by_score(self, symbols: List[str], scores: Dict[str, float]) -> List[str]:
        """按评分排序（得分越高越好）"""
        if not symbols or not scores:
            return symbols
        
        # 收集评分数据
        score_data = []
        for symbol in symbols:
            score = scores.get(symbol, 0)
            score_data.append((symbol, score))
        
        # 按评分降序排序
        score_data.sort(key=lambda x: x[1], reverse=True)
        
        # 提取股票代码
        sorted_symbols = [item[0] for item in score_data]
        
        return sorted_symbols
    
    def _generate_rebalance_signals(self, target_holdings: List[str], 
                                   market_data: Dict[str, Dict]) -> List[Dict]:
        """生成调仓信号"""
        signals = []
        
        # 卖出当前持仓中不在目标持仓的股票
        for symbol in self.current_holdings:
            if symbol not in target_holdings and symbol in market_data:
                price = market_data[symbol].get("price", 0)
                if price > 0:
                    signal_dict = {
                        "symbol": symbol,
                        "side": "SELL",
                        "price": price,
                        "confidence": 0.7,
                        "reason": "时空共振策略调仓卖出"
                    }
                    signals.append(signal_dict)
        
        # 买入目标持仓中当前未持有的股票
        for symbol in target_holdings:
            if symbol not in self.current_holdings and symbol in market_data:
                price = market_data[symbol].get("price", 0)
                if price > 0:
                    signal_dict = {
                        "symbol": symbol,
                        "side": "BUY",
                        "price": price,
                        "confidence": 0.7,
                        "reason": "时空共振策略调仓买入（四维度共振）"
                    }
                    signals.append(signal_dict)
        
        return signals
    
    def _generate_hold_signals(self) -> List[Dict]:
        """生成持仓信号"""
        signals = []
        
        for symbol in self.current_holdings:
            signal_dict = {
                "symbol": symbol,
                "side": "HOLD",
                "price": 0,
                "confidence": 0.6,
                "reason": "维持时空共振策略持仓"
            }
            signals.append(signal_dict)
        
        return signals
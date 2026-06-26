"""
A股自适应交易引擎 - 核心优势模块
通过对市场行情变化的感知适时调整交易策略和投资标的阈值
实现智能自适应而非简单机械的数据指标选择
"""

import logging
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class MarketState(Enum):
    """A股市场状态枚举"""
    STRONG_BULL = "强牛"        # 强劲牛市
    WEAK_BULL = "弱牛"          # 温和牛市  
    STRONG_BEAR = "强熊"        # 强劲熊市
    WEAK_BEAR = "弱熊"          # 温和熊市
    VOLATILE = "高波动震荡"      # 高波动震荡市
    SIDEWAYS = "横盘震荡"        # 低波动横盘市
    TRANSITION = "状态转换"      # 状态转换期


class AdaptiveEngine:
    """A股自适应交易引擎 - 核心智能模块"""
    
    def __init__(self, 
                 initial_market_state: MarketState = MarketState.VOLATILE,
                 learning_rate: float = 0.1,
                 adaptation_speed: float = 0.3,
                 memory_window: int = 30,
                 confidence_threshold: float = 0.7):
        """
        初始化自适应引擎
        
        Args:
            initial_market_state: 初始市场状态
            learning_rate: 学习率（0-1，越高学习越快）
            adaptation_speed: 适应速度（0-1，越高调整越快）
            memory_window: 记忆窗口（天数）
            confidence_threshold: 状态判断置信度阈值
        """
        self.market_state = initial_market_state
        self.learning_rate = learning_rate
        self.adaptation_speed = adaptation_speed
        self.memory_window = memory_window
        self.confidence_threshold = confidence_threshold
        
        # 市场指标记忆
        self.market_memory = {
            "returns": [],
            "volatility": [],
            "volume": [],
            "advance_decline": [],
            "sentiment": [],
            "small_cap_performance": [],  # A股特有：小盘股表现
            "growth_vs_value": []         # A股特有：成长vs价值表现
        }
        
        # 策略绩效记忆
        self.strategy_performance = {}
        
        # 参数调整历史
        self.parameter_history = []
        
        # 自适应规则库（针对A股市场优化）
        self.adaptation_rules = self._initialize_adaptation_rules()
        
        # 状态转换概率矩阵（基于A股历史数据）
        self.state_transition_matrix = self._initialize_state_transition_matrix()
        
        # 学习模型状态
        self.learning_model = self._initialize_learning_model()
        
        logger.info(f"A股自适应引擎初始化完成 - 初始状态: {initial_market_state.value}")
    
    def _initialize_adaptation_rules(self) -> Dict:
        """初始化A股自适应规则库"""
        return {
            MarketState.STRONG_BULL: {
                "strategy_weights": {
                    "fundamental": 0.20,      # 基本面策略
                    "defensive": 0.10,        # 防御策略（降低）
                    "swing_trading": 0.08,    # 震荡策略
                    "small_cap": 0.15,        # 小市值策略（牛市表现好）
                    "quality_small_cap": 0.12, # 质量小市值
                    "small_cap_growth": 0.15,  # 小市值成长（牛市表现好）
                    "revenue_profit": 0.10,    # 营收利润双增
                    "chip_concentration": 0.05, # 控盘策略
                    "social_security": 0.03,   # 社保重仓
                    "oversold_rebound": 0.01,  # 超跌反弹（降低）
                    "resonance": 0.01          # 时空共振
                },
                "parameter_adjustments": {
                    # 基本面策略调整
                    "min_profit_growth": 0.25,      # 降低增长要求
                    "min_revenue_growth": 0.25,     # 降低增长要求
                    "pe_max": 60.0,                 # 提高PE容忍度
                    "pb_max": 6.0,                  # 提高PB容忍度
                    
                    # 防御策略调整
                    "min_dividend_yield": 0.03,     # 降低股息要求
                    "max_price": 40.0,              # 提高价格限制
                    
                    # 小市值策略调整
                    "max_market_cap": 3000000000,   # 提高市值上限
                    
                    # 通用调整
                    "confidence_multiplier": 1.2,   # 提高信号置信度
                    "position_size_multiplier": 1.1  # 提高仓位规模
                },
                "risk_adjustments": {
                    "stop_loss_per_trade": 0.035,   # 放宽止损
                    "max_position_size": 0.07,      # 提高单只仓位上限
                    "turnover_target": 60.0,        # 提高换手率目标
                    "max_drawdown_alert": 0.12      # 放宽回撤预警
                }
            },
            
            MarketState.WEAK_BULL: {
                "strategy_weights": {
                    "fundamental": 0.18,
                    "defensive": 0.12,
                    "swing_trading": 0.10,
                    "small_cap": 0.12,
                    "quality_small_cap": 0.13,
                    "small_cap_growth": 0.12,
                    "revenue_profit": 0.12,
                    "chip_concentration": 0.06,
                    "social_security": 0.03,
                    "oversold_rebound": 0.01,
                    "resonance": 0.01
                },
                "parameter_adjustments": {
                    "min_profit_growth": 0.28,
                    "min_revenue_growth": 0.28,
                    "pe_max": 55.0,
                    "pb_max": 5.5,
                    "min_dividend_yield": 0.035,
                    "max_price": 35.0,
                    "confidence_multiplier": 1.1,
                    "position_size_multiplier": 1.05
                },
                "risk_adjustments": {
                    "stop_loss_per_trade": 0.03,
                    "max_position_size": 0.065,
                    "turnover_target": 50.0,
                    "max_drawdown_alert": 0.13
                }
            },
            
            MarketState.STRONG_BEAR: {
                "strategy_weights": {
                    "fundamental": 0.10,      # 基本面策略（降低）
                    "defensive": 0.25,        # 防御策略（大幅提高）
                    "swing_trading": 0.05,    # 震荡策略（降低）
                    "small_cap": 0.05,        # 小市值策略（熊市风险大）
                    "quality_small_cap": 0.08, # 质量小市值
                    "small_cap_growth": 0.05,  # 小市值成长（降低）
                    "revenue_profit": 0.08,    # 营收利润双增
                    "chip_concentration": 0.08, # 控盘策略（提高）
                    "social_security": 0.12,   # 社保重仓（大幅提高）
                    "oversold_rebound": 0.08,  # 超跌反弹（提高）
                    "resonance": 0.06          # 时空共振
                },
                "parameter_adjustments": {
                    # 基本面策略调整
                    "min_profit_growth": 0.35,      # 提高增长要求
                    "min_revenue_growth": 0.35,     # 提高增长要求
                    "pe_max": 35.0,                 # 降低PE容忍度
                    "pb_max": 3.5,                  # 降低PB容忍度
                    
                    # 防御策略调整
                    "min_dividend_yield": 0.05,     # 提高股息要求
                    "max_price": 25.0,              # 降低价格限制
                    
                    # 小市值策略调整
                    "max_market_cap": 2000000000,   # 降低市值上限
                    
                    # 通用调整
                    "confidence_multiplier": 0.8,   # 降低信号置信度
                    "position_size_multiplier": 0.8  # 降低仓位规模
                },
                "risk_adjustments": {
                    "stop_loss_per_trade": 0.02,    # 收紧止损
                    "max_position_size": 0.045,     # 降低单只仓位上限
                    "turnover_target": 30.0,        # 降低换手率目标
                    "max_drawdown_alert": 0.08      # 收紧回撤预警
                }
            },
            
            MarketState.WEAK_BEAR: {
                "strategy_weights": {
                    "fundamental": 0.12,
                    "defensive": 0.22,
                    "swing_trading": 0.07,
                    "small_cap": 0.07,
                    "quality_small_cap": 0.10,
                    "small_cap_growth": 0.07,
                    "revenue_profit": 0.10,
                    "chip_concentration": 0.07,
                    "social_security": 0.10,
                    "oversold_rebound": 0.06,
                    "resonance": 0.02
                },
                "parameter_adjustments": {
                    "min_profit_growth": 0.32,
                    "min_revenue_growth": 0.32,
                    "pe_max": 40.0,
                    "pb_max": 4.0,
                    "min_dividend_yield": 0.045,
                    "max_price": 28.0,
                    "confidence_multiplier": 0.9,
                    "position_size_multiplier": 0.9
                },
                "risk_adjustments": {
                    "stop_loss_per_trade": 0.025,
                    "max_position_size": 0.055,
                    "turnover_target": 40.0,
                    "max_drawdown_alert": 0.10
                }
            },
            
            MarketState.VOLATILE: {
                "strategy_weights": {
                    "fundamental": 0.15,
                    "defensive": 0.15,
                    "swing_trading": 0.12,    # 震荡策略（高波动环境有利）
                    "small_cap": 0.10,
                    "quality_small_cap": 0.11,
                    "small_cap_growth": 0.10,
                    "revenue_profit": 0.11,
                    "chip_concentration": 0.06,
                    "social_security": 0.05,
                    "oversold_rebound": 0.03,
                    "resonance": 0.02
                },
                "parameter_adjustments": {
                    "min_profit_growth": 0.30,
                    "min_revenue_growth": 0.30,
                    "pe_max": 45.0,
                    "pb_max": 4.5,
                    "min_dividend_yield": 0.04,
                    "max_price": 32.0,
                    "confidence_multiplier": 1.0,
                    "position_size_multiplier": 1.0
                },
                "risk_adjustments": {
                    "stop_loss_per_trade": 0.028,
                    "max_position_size": 0.06,
                    "turnover_target": 45.0,
                    "max_drawdown_alert": 0.11
                }
            },
            
            MarketState.SIDEWAYS: {
                "strategy_weights": {
                    "fundamental": 0.16,
                    "defensive": 0.16,
                    "swing_trading": 0.10,
                    "small_cap": 0.11,
                    "quality_small_cap": 0.12,
                    "small_cap_growth": 0.11,
                    "revenue_profit": 0.12,
                    "chip_concentration": 0.05,
                    "social_security": 0.04,
                    "oversold_rebound": 0.02,
                    "resonance": 0.01
                },
                "parameter_adjustments": {
                    "min_profit_growth": 0.28,
                    "min_revenue_growth": 0.28,
                    "pe_max": 48.0,
                    "pb_max": 4.8,
                    "min_dividend_yield": 0.038,
                    "max_price": 33.0,
                    "confidence_multiplier": 0.95,
                    "position_size_multiplier": 0.95
                },
                "risk_adjustments": {
                    "stop_loss_per_trade": 0.026,
                    "max_position_size": 0.062,
                    "turnover_target": 42.0,
                    "max_drawdown_alert": 0.115
                }
            }
        }
    
    def _initialize_state_transition_matrix(self) -> Dict:
        """初始化A股状态转换概率矩阵（基于历史数据）"""
        return {
            MarketState.STRONG_BULL: {
                MarketState.STRONG_BULL: 0.55,
                MarketState.WEAK_BULL: 0.25,
                MarketState.VOLATILE: 0.12,
                MarketState.WEAK_BEAR: 0.06,
                MarketState.STRONG_BEAR: 0.02
            },
            MarketState.WEAK_BULL: {
                MarketState.WEAK_BULL: 0.45,
                MarketState.STRONG_BULL: 0.15,
                MarketState.VOLATILE: 0.18,
                MarketState.SIDEWAYS: 0.12,
                MarketState.WEAK_BEAR: 0.08,
                MarketState.STRONG_BEAR: 0.02
            },
            MarketState.STRONG_BEAR: {
                MarketState.STRONG_BEAR: 0.50,
                MarketState.WEAK_BEAR: 0.25,
                MarketState.VOLATILE: 0.15,
                MarketState.WEAK_BULL: 0.08,
                MarketState.SIDEWAYS: 0.02
            },
            MarketState.WEAK_BEAR: {
                MarketState.WEAK_BEAR: 0.40,
                MarketState.STRONG_BEAR: 0.18,
                MarketState.VOLATILE: 0.20,
                MarketState.SIDEWAYS: 0.12,
                MarketState.WEAK_BULL: 0.10
            },
            MarketState.VOLATILE: {
                MarketState.VOLATILE: 0.35,
                MarketState.WEAK_BULL: 0.18,
                MarketState.WEAK_BEAR: 0.18,
                MarketState.SIDEWAYS: 0.15,
                MarketState.STRONG_BULL: 0.08,
                MarketState.STRONG_BEAR: 0.06
            },
            MarketState.SIDEWAYS: {
                MarketState.SIDEWAYS: 0.45,
                MarketState.VOLATILE: 0.25,
                MarketState.WEAK_BULL: 0.15,
                MarketState.WEAK_BEAR: 0.10,
                MarketState.STRONG_BULL: 0.03,
                MarketState.STRONG_BEAR: 0.02
            }
        }
    
    def _initialize_learning_model(self) -> Dict:
        """初始化学习模型"""
        return {
            "state_recognition_accuracy": 0.0,
            "parameter_adjustment_effectiveness": {},
            "strategy_weight_effectiveness": {},
            "learning_iterations": 0,
            "last_improvement": datetime.now(),
            "a_share_specific": {
                "small_cap_sensitivity": 0.5,  # 小盘股敏感度
                "policy_sensitivity": 0.6,     # 政策敏感度
                "retail_sentiment_weight": 0.4  # 散户情绪权重
            }
        }
    
    def update_market_indicators(self, market_data: Dict[str, Dict]) -> Dict:
        """
        更新A股市场指标
        
        Args:
            market_data: A股市场数据
        
        Returns:
            计算后的市场指标
        """
        indicators = self._calculate_a_share_market_indicators(market_data)
        
        # 更新记忆
        for key, value in indicators.items():
            if key in self.market_memory:
                self.market_memory[key].append(value)
                
                # 控制记忆窗口大小
                if len(self.market_memory[key]) > self.memory_window:
                    self.market_memory[key] = self.market_memory[key][-self.memory_window:]
        
        return indicators
    
    def _calculate_a_share_market_indicators(self, market_data: Dict[str, Dict]) -> Dict:
        """计算A股特有市场指标"""
        if not market_data:
            return {}
        
        # 提取价格序列
        prices = []
        volumes = []
        market_caps = []
        
        for symbol, data in market_data.items():
            price = data.get('price', 0)
            volume = data.get('volume', 0)
            market_cap = data.get('market_cap', 0) if 'market_cap' in data else 0
            
            if price > 0:
                prices.append(price)
                volumes.append(volume)
                market_caps.append(market_cap)
        
        if len(prices) < 5:
            return {
                "market_return": 0.0,
                "volatility": 0.0,
                "volume_trend": 0.0,
                "advance_decline_ratio": 1.0,
                "sentiment_score": 0.5,
                "small_cap_performance": 0.0,
                "growth_vs_value": 0.5
            }
        
        # 计算基础指标
        returns = np.diff(prices) / prices[:-1] if len(prices) > 1 else [0]
        market_return = np.mean(returns) if len(returns) > 0 else 0
        volatility = np.std(returns) * np.sqrt(252) if len(returns) > 1 else 0
        volume_trend = np.mean(np.diff(volumes) / volumes[:-1]) if len(volumes) > 1 else 0
        
        # 计算涨跌比
        advance_count = sum(1 for r in returns if r > 0)
        decline_count = sum(1 for r in returns if r < 0)
        advance_decline_ratio = advance_count / max(decline_count, 1)
        
        # A股特有指标：小盘股表现（简化）
        small_cap_performance = self._calculate_small_cap_performance(market_data)
        
        # A股特有指标：成长vs价值表现（简化）
        growth_vs_value = self._calculate_growth_vs_value_ratio(market_data)
        
        # 计算A股情绪得分
        sentiment_score = self._calculate_a_share_sentiment_score(
            market_return, volatility, volume_trend, 
            advance_decline_ratio, small_cap_performance, growth_vs_value
        )
        
        return {
            "market_return": market_return,
            "volatility": volatility,
            "volume_trend": volume_trend,
            "advance_decline_ratio": advance_decline_ratio,
            "sentiment_score": sentiment_score,
            "small_cap_performance": small_cap_performance,
            "growth_vs_value": growth_vs_value,
            "timestamp": datetime.now()
        }
    
    def _calculate_small_cap_performance(self, market_data: Dict[str, Dict]) -> float:
        """计算小盘股相对表现（简化实现）"""
        # 在实际系统中，应该基于市值分类计算
        # 这里使用随机值模拟
        import random
        return random.uniform(-0.1, 0.1)
    
    def _calculate_growth_vs_value_ratio(self, market_data: Dict[str, Dict]) -> float:
        """计算成长vs价值相对表现（简化实现）"""
        # 在实际系统中，应该基于PE、PB等指标分类计算
        # 这里使用随机值模拟
        import random
        return random.uniform(0.3, 0.7)
    
    def _calculate_a_share_sentiment_score(self, market_return: float, volatility: float,
                                         volume_trend: float, advance_decline_ratio: float,
                                         small_cap_performance: float, growth_vs_value: float) -> float:
        """计算A股情绪得分（0-1，越高越乐观）"""
        # 收益率贡献
        return_contribution = 0.5 + (market_return * 1.5)
        return_contribution = max(0, min(1, return_contribution))
        
        # 波动率贡献（A股对高波动更敏感）
        volatility_contribution = max(0, 1 - volatility * 2.5)
        
        # 成交量趋势贡献
        volume_contribution = 0.5 + (volume_trend * 0.5)
        volume_contribution = max(0, min(1, volume_contribution))
        
        # 涨跌比贡献
        adr_contribution = min(1, advance_decline_ratio)
        
        # 小盘股表现贡献（小盘股强通常情绪乐观）
        small_cap_contribution = 0.5 + (small_cap_performance * 2)
        small_cap_contribution = max(0, min(1, small_cap_contribution))
        
        # 成长vs价值贡献（成长股强通常情绪乐观）
        growth_contribution = growth_vs_value
        
        # 综合情绪得分（A股加权）
        sentiment_score = (
            return_contribution * 0.25 +
            volatility_contribution * 0.20 +
            volume_contribution * 0.15 +
            adr_contribution * 0.15 +
            small_cap_contribution * 0.15 +
            growth_contribution * 0.10
        )
        
        return max(0, min(1, sentiment_score))
    
    def recognize_market_state(self, indicators: Dict) -> Tuple[MarketState, float]:
        """
        识别A股市场状态
        
        Args:
            indicators: A股市场指标
        
        Returns:
            (市场状态, 置信度)
        """
        if not indicators:
            return self.market_state, 0.5
        
        market_return = indicators.get("market_return", 0)
        volatility = indicators.get("volatility", 0)
        sentiment_score = indicators.get("sentiment_score", 0.5)
        advance_decline_ratio = indicators.get("advance_decline_ratio", 1.0)
        small_cap_performance = indicators.get("small_cap_performance", 0)
        
        # A股特有规则：小盘股表现对市场状态有影响
        small_cap_factor = 1.0 + small_cap_performance * 2
        
        # 基于规则的状态识别
        state_scores = {}
        
        # 强牛市判断条件（A股特征）
        strong_bull_score = 0.0
        if market_return > 0.0025 and sentiment_score > 0.75 and advance_decline_ratio > 1.8:
            strong_bull_score = 0.8 * small_cap_factor
        elif market_return > 0.0015 and sentiment_score > 0.7:
            strong_bull_score = 0.6 * small_cap_factor
        
        # 弱牛市判断条件
        weak_bull_score = 0.0
        if 0.0008 < market_return <= 0.0025 and sentiment_score > 0.65:
            weak_bull_score = 0.7
        elif market_return > 0 and sentiment_score > 0.6:
            weak_bull_score = 0.5
        
        # 强熊市判断条件（A股特征）
        strong_bear_score = 0.0
        if market_return < -0.0025 and sentiment_score < 0.25 and advance_decline_ratio < 0.6:
            strong_bear_score = 0.8 / (small_cap_factor + 0.5)
        elif market_return < -0.0015 and sentiment_score < 0.3:
            strong_bear_score = 0.6 / (small_cap_factor + 0.5)
        
        # 弱熊市判断条件
        weak_bear_score = 0.0
        if -0.0025 < market_return <= -0.0008 and sentiment_score < 0.35:
            weak_bear_score = 0.7
        elif market_return < 0 and sentiment_score < 0.4:
            weak_bear_score = 0.5
        
        # 高波动震荡市判断条件
        volatile_score = 0.0
        if volatility > 0.30 and abs(market_return) < 0.001:
            volatile_score = 0.8
        elif volatility > 0.25:
            volatile_score = 0.6
        
        # 横盘震荡市判断条件
        sideways_score = 0.0
        if volatility < 0.18 and abs(market_return) < 0.0005:
            sideways_score = 0.8
        elif volatility < 0.22 and abs(market_return) < 0.001:
            sideways_score = 0.6
        
        state_scores = {
            MarketState.STRONG_BULL: strong_bull_score,
            MarketState.WEAK_BULL: weak_bull_score,
            MarketState.STRONG_BEAR: strong_bear_score,
            MarketState.WEAK_BEAR: weak_bear_score,
            MarketState.VOLATILE: volatile_score,
            MarketState.SIDEWAYS: sideways_score
        }
        
        # 找到得分最高的状态
        best_state = max(state_scores, key=state_scores.get)
        best_score = state_scores[best_state]
        
        # 考虑状态转换概率
        if self.market_state != MarketState.TRANSITION:
            transition_prob = self.state_transition_matrix.get(self.market_state, {}).get(best_state, 0.1)
            adjusted_score = best_score * transition_prob
        else:
            adjusted_score = best_score
        
        # 判断是否需要转换状态
        confidence = adjusted_score
        if confidence >= self.confidence_threshold and best_state != self.market_state:
            old_state = self.market_state
            self.market_state = best_state
            logger.info(f"A股市场状态转换: {old_state.value} → {best_state.value} (置信度: {confidence:.2f})")
        
        return self.market_state, confidence
    
    # 其他方法与港股自适应引擎类似，但针对A股优化
    # 为节省空间，省略部分重复方法，实际使用时从港股引擎复制并调整
    
    def adapt_strategy_parameters(self, strategy_name: str, 
                                current_parameters: Dict) -> Dict:
        """A股策略参数自适应调整"""
        if self.market_state not in self.adaptation_rules:
            return current_parameters
        
        rules = self.adaptation_rules[self.market_state]
        parameter_adjustments = rules.get("parameter_adjustments", {})
        
        adapted_parameters = current_parameters.copy()
        
        for param_name, target_value in parameter_adjustments.items():
            if param_name in adapted_parameters:
                current_value = adapted_parameters[param_name]
                adjustment = target_value - current_value
                adapted_value = current_value + adjustment * self.adaptation_speed
                adapted_parameters[param_name] = adapted_value
        
        return adapted_parameters
    
    def optimize_strategy_weights(self, current_weights: Dict[str, float],
                                strategy_performance: Dict[str, float]) -> Dict[str, float]:
        """优化A股策略权重"""
        if self.market_state in self.adaptation_rules:
            state_weights = self.adaptation_rules[self.market_state]["strategy_weights"]
        else:
            state_weights = current_weights
        
        performance_adjusted_weights = {}
        
        for strategy_name, current_weight in current_weights.items():
            base_weight = state_weights.get(strategy_name, current_weight)
            performance = strategy_performance.get(strategy_name, 0.5)
            performance_factor = 0.5 + (performance * 0.5)
            adjusted_weight = base_weight * performance_factor
            performance_adjusted_weights[strategy_name] = adjusted_weight
        
        total_weight = sum(performance_adjusted_weights.values())
        if total_weight > 0:
            normalized_weights = {
                name: weight / total_weight
                for name, weight in performance_adjusted_weights.items()
            }
        else:
            normalized_weights = current_weights
        
        return normalized_weights
    
    def get_adaptive_decisions(self, market_data: Dict[str, Dict],
                             current_config: Dict) -> Dict:
        """获取A股自适应决策"""
        indicators = self.update_market_indicators(market_data)
        market_state, confidence = self.recognize_market_state(indicators)
        
        if market_state in self.adaptation_rules:
            state_rules = self.adaptation_rules[market_state]
        else:
            state_rules = self.adaptation_rules[MarketState.VOLATILE]
        
        adaptive_decisions = {
            "market_state": market_state.value,
            "state_confidence": confidence,
            "market_indicators": indicators,
            "strategy_weights": state_rules["strategy_weights"],
            "parameter_adjustments": state_rules["parameter_adjustments"],
            "risk_adjustments": state_rules["risk_adjustments"],
            "learning_status": {
                "recognition_accuracy": self.learning_model["state_recognition_accuracy"],
                "learning_iterations": self.learning_model["learning_iterations"],
                "adaptation_speed": self.adaptation_speed
            },
            "timestamp": datetime.now().isoformat()
        }
        
        return adaptive_decisions
    
    def get_engine_status(self) -> Dict:
        """获取引擎状态"""
        return {
            "market_state": self.market_state.value,
            "learning_rate": self.learning_rate,
            "adaptation_speed": self.adaptation_speed,
            "memory_window": self.memory_window,
            "learning_model": self.learning_model,
            "timestamp": datetime.now().isoformat()
        }
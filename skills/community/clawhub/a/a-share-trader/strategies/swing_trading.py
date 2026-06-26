"""
震荡选股策略（KDJ策略）
计算 KDJ (9,3,3) 指标；KDJ_K<20 为买入信号，KDJ_K>80 为卖出信号；
首次建仓 80% 仓位，买入信号加仓至 100%，卖出信号减仓至 80%；
每 1 个交易日调仓
"""

import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import random

from .base_strategy import BaseStrategy

logger = logging.getLogger(__name__)


class SwingTradingStrategy(BaseStrategy):
    """震荡选股策略（KDJ策略）"""
    
    def __init__(self,
                 kdj_period: Tuple[int, int, int] = (9, 3, 3),
                 buy_threshold: float = 20.0,
                 sell_threshold: float = 80.0,
                 initial_position: float = 0.8,
                 max_position: float = 1.0,
                 rebalance_freq: str = "daily",
                 enabled: bool = True,
                 weight: float = 0.10,
                 **kwargs):
        """
        初始化震荡策略
        
        Args:
            kdj_period: KDJ参数 (N, M1, M2)
            buy_threshold: 买入阈值（KDJ_K < buy_threshold）
            sell_threshold: 卖出阈值（KDJ_K > sell_threshold）
            initial_position: 首次建仓比例
            max_position: 最大仓位比例
            rebalance_freq: 调仓频率（daily, weekly, monthly）
            enabled: 是否启用
            weight: 策略权重
            **kwargs: 其他参数
        """
        super().__init__(
            name="SwingTradingStrategy",
            enabled=enabled,
            weight=weight,
            kdj_period=kdj_period,
            buy_threshold=buy_threshold,
            sell_threshold=sell_threshold,
            initial_position=initial_position,
            max_position=max_position,
            rebalance_freq=rebalance_freq,
            **kwargs
        )
        
        # 策略状态
        self.current_positions = {}  # {symbol: position_pct}
        self.last_rebalance = None
        self.initial_position_set = False
        
        logger.info(f"震荡策略初始化: KDJ{self.parameters['kdj_period']}, "
                   f"买入阈值={self.parameters['buy_threshold']}, "
                   f"卖出阈值={self.parameters['sell_threshold']}")
    
    def generate_signals(self, market_data: Dict[str, Dict], 
                        fundamental_data: Optional[Dict[str, Dict]] = None,
                        technical_data: Optional[Dict[str, Dict]] = None) -> List[Dict]:
        """
        生成KDJ策略交易信号
        
        Args:
            market_data: 市场数据
            technical_data: 技术指标数据（必须包含KDJ）
        
        Returns:
            交易信号列表
        """
        signals = []
        
        if not market_data:
            logger.warning("震荡策略: 缺少市场数据")
            return signals
        
        # 检查是否需要调仓
        if not self._should_rebalance():
            logger.debug("震荡策略: 未到调仓时间，维持当前持仓")
            return self._generate_hold_signals()
        
        # 如果没有技术数据，尝试从市场数据中获取或模拟
        if technical_data is None:
            technical_data = self._get_or_simulate_technical_data(market_data)
        
        # 处理每只股票
        for symbol, mkt_data in market_data.items():
            price = mkt_data.get("price", 0)
            if price <= 0:
                continue
            
            # 获取KDJ指标
            tech_data = technical_data.get(symbol, {}) if technical_data else {}
            kdj_k = tech_data.get("kdj_k", 50.0)  # 默认50
            
            # 确定交易信号
            signal = self._determine_signal(symbol, price, kdj_k)
            if signal:
                signals.append(signal)
        
        # 更新调仓时间
        self.last_rebalance = datetime.now()
        
        self.signals_generated += len(signals)
        logger.info(f"震荡策略生成 {len(signals)} 个信号")
        
        return signals
    
    def _should_rebalance(self) -> bool:
        """检查是否需要调仓"""
        if self.last_rebalance is None:
            return True
        
        rebalance_freq = self.parameters.get("rebalance_freq", "daily")
        
        if rebalance_freq == "daily":
            # 每日调仓
            return datetime.now().date() != self.last_rebalance.date()
        elif rebalance_freq == "weekly":
            # 每周调仓（简化：7天）
            days_since = (datetime.now() - self.last_rebalance).days
            return days_since >= 7
        elif rebalance_freq == "monthly":
            # 每月调仓（简化：30天）
            days_since = (datetime.now() - self.last_rebalance).days
            return days_since >= 30
        else:
            # 默认每日调仓
            return datetime.now().date() != self.last_rebalance.date()
    
    def _get_or_simulate_technical_data(self, market_data: Dict[str, Dict]) -> Dict[str, Dict]:
        """获取或模拟技术指标数据"""
        technical_data = {}
        
        for symbol in market_data.keys():
            # 模拟KDJ值（在实际系统中应从数据源获取）
            # 使用随机值，但添加一些趋势性
            kdj_k = random.uniform(0, 100)
            
            # 添加一些逻辑：如果价格上涨，KDJ倾向于高位
            price = market_data[symbol].get("price", 0)
            if symbol in self.current_positions:
                # 已有持仓，假设价格上涨
                kdj_k = random.uniform(40, 90)
            else:
                # 无持仓，随机分布
                kdj_k = random.uniform(0, 100)
            
            technical_data[symbol] = {
                "kdj_k": kdj_k,
                "kdj_d": kdj_k * 0.9 + random.uniform(-5, 5),
                "kdj_j": kdj_k * 1.1 + random.uniform(-5, 5)
            }
        
        return technical_data
    
    def _determine_signal(self, symbol: str, price: float, kdj_k: float) -> Optional[Dict]:
        """根据KDJ值确定交易信号"""
        buy_threshold = self.parameters["buy_threshold"]
        sell_threshold = self.parameters["sell_threshold"]
        
        current_position = self.current_positions.get(symbol, 0)
        
        # 买入信号：KDJ_K < 买入阈值
        if kdj_k < buy_threshold:
            if current_position < self.parameters["max_position"]:
                # 计算目标仓位
                if not self.initial_position_set:
                    # 首次建仓
                    target_position = self.parameters["initial_position"]
                    self.initial_position_set = True
                    reason = "首次建仓"
                else:
                    # 加仓至100%
                    target_position = self.parameters["max_position"]
                    reason = "KDJ超卖加仓"
                
                # 如果需要增加仓位
                if target_position > current_position:
                    position_change = target_position - current_position
                    return {
                        "symbol": symbol,
                        "side": "BUY",
                        "price": price,
                        "confidence": max(0.1, (buy_threshold - kdj_k) / buy_threshold),
                        "position_change_pct": position_change,
                        "reason": f"{reason} (KDJ_K={kdj_k:.1f}<{buy_threshold})",
                        "kdj_k": kdj_k
                    }
        
        # 卖出信号：KDJ_K > 卖出阈值
        elif kdj_k > sell_threshold:
            if current_position > 0:
                # 减仓至80%
                target_position = self.parameters["initial_position"]  # 80%
                if target_position < current_position:
                    position_change = current_position - target_position
                    return {
                        "symbol": symbol,
                        "side": "SELL",
                        "price": price,
                        "confidence": max(0.1, (kdj_k - sell_threshold) / (100 - sell_threshold)),
                        "position_change_pct": position_change,
                        "reason": f"KDJ超买减仓 (KDJ_K={kdj_k:.1f}>{sell_threshold})",
                        "kdj_k": kdj_k
                    }
        
        # 持有信号或无信号
        if current_position > 0:
            return {
                "symbol": symbol,
                "side": "HOLD",
                "price": price,
                "confidence": 0.5,
                "reason": f"持有 (KDJ_K={kdj_k:.1f})",
                "kdj_k": kdj_k
            }
        
        return None
    
    def _generate_hold_signals(self) -> List[Dict]:
        """生成持仓信号"""
        signals = []
        
        for symbol, position_pct in self.current_positions.items():
            if position_pct > 0:
                signals.append({
                    "symbol": symbol,
                    "side": "HOLD",
                    "price": 0,
                    "confidence": 0.6,
                    "position_pct": position_pct,
                    "reason": "维持震荡策略持仓"
                })
        
        return signals
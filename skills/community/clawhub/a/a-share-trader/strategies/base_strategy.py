"""
A股策略基类
所有选股策略的基础类，提供统一的接口和公共功能
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class Signal:
    """交易信号类"""
    
    def __init__(self, symbol: str, side: str, price: float, 
                 confidence: float = 0.5, quantity: int = 0, **kwargs):
        """
        初始化交易信号
        
        Args:
            symbol: 股票代码
            side: 交易方向，"BUY"/"SELL"/"HOLD"
            price: 建议交易价格
            confidence: 信号置信度（0-1）
            quantity: 建议交易数量（0表示自动计算）
            **kwargs: 其他信号属性
        """
        self.symbol = symbol
        self.side = side.upper()
        self.price = price
        self.confidence = max(0.0, min(1.0, confidence))
        self.quantity = max(0, quantity)
        self.timestamp = datetime.now()
        
        # 其他属性
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        result = {
            "symbol": self.symbol,
            "side": self.side,
            "price": self.price,
            "confidence": self.confidence,
            "quantity": self.quantity,
            "timestamp": self.timestamp.isoformat()
        }
        
        # 添加其他属性
        for attr in dir(self):
            if not attr.startswith('_') and attr not in ['to_dict', 'symbol', 'side', 
                                                         'price', 'confidence', 'quantity', 
                                                         'timestamp']:
                value = getattr(self, attr)
                if not callable(value):
                    result[attr] = value
        
        return result
    
    def __str__(self) -> str:
        return f"Signal({self.symbol} {self.side} @{self.price:.2f}, conf={self.confidence:.2f})"


class BaseStrategy(ABC):
    """策略基类"""
    
    def __init__(self, name: str = "BaseStrategy", enabled: bool = True, 
                 weight: float = 0.1, **kwargs):
        """
        初始化策略基类
        
        Args:
            name: 策略名称
            enabled: 是否启用
            weight: 策略权重（0-1）
            **kwargs: 策略特定参数
        """
        self.name = name
        self.enabled = enabled
        self.weight = max(0.0, min(1.0, weight))
        
        # 策略参数
        self.parameters = kwargs.copy()
        
        # 绩效跟踪
        self.signals_generated = 0
        self.signals_executed = 0
        self.start_time = datetime.now()
        
        logger.info(f"策略初始化: {name}, 权重: {weight}")
    
    @abstractmethod
    def generate_signals(self, market_data: Dict[str, Dict], 
                        fundamental_data: Optional[Dict[str, Dict]] = None,
                        technical_data: Optional[Dict[str, Dict]] = None) -> List[Signal]:
        """
        生成交易信号（抽象方法，子类必须实现）
        
        Args:
            market_data: 市场数据 {symbol: {price, volume, ...}}
            fundamental_data: 基本面数据 {symbol: {roe, pe, ...}} (可选)
            technical_data: 技术指标数据 {symbol: {kdj, rsi, ...}} (可选)
        
        Returns:
            交易信号列表
        """
        pass
    
    def filter_stocks(self, symbols: List[str], fundamental_data: Dict[str, Dict]) -> List[str]:
        """
        通用股票筛选：排除ST、科创板、停牌等
        
        Args:
            symbols: 待筛选股票列表
            fundamental_data: 基本面数据
        
        Returns:
            筛选后的股票列表
        """
        filtered = []
        
        for symbol in symbols:
            if symbol not in fundamental_data:
                continue
            
            fund_data = fundamental_data[symbol]
            
            # 排除ST股
            if self.parameters.get("exclude_st", True):
                if fund_data.get("is_st", False):
                    continue
            
            # 排除科创板
            if self.parameters.get("exclude_star", True):
                if fund_data.get("is_star", False):
                    continue
            
            # 排除停牌股
            if self.parameters.get("exclude_suspended", True):
                if fund_data.get("is_suspended", False):
                    continue
            
            # 排除退市股
            if self.parameters.get("exclude_delisted", True):
                if fund_data.get("is_delisted", False):
                    continue
            
            # 排除新股（可选）
            if self.parameters.get("exclude_new", False):
                listing_days = fund_data.get("listing_days", 0)
                if listing_days < 60:  # 上市不足60天
                    continue
            
            filtered.append(symbol)
        
        return filtered
    
    def calculate_market_cap_rank(self, symbols: List[str], 
                                 fundamental_data: Dict[str, Dict]) -> Dict[str, float]:
        """
        计算总市值截面排名分位数
        
        Args:
            symbols: 股票列表
            fundamental_data: 基本面数据
        
        Returns:
            {symbol: 分位数}（0-1，越小表示市值越小）
        """
        if not symbols:
            return {}
        
        market_caps = []
        valid_symbols = []
        
        for symbol in symbols:
            if symbol in fundamental_data:
                market_cap = fundamental_data[symbol].get("market_cap", 0)
                if market_cap > 0:
                    market_caps.append(market_cap)
                    valid_symbols.append(symbol)
        
        if not market_caps:
            return {symbol: 0.5 for symbol in symbols}
        
        # 计算分位数
        df = pd.DataFrame({"symbol": valid_symbols, "market_cap": market_caps})
        df["rank"] = df["market_cap"].rank(method="min")
        df["quantile"] = (df["rank"] - 1) / (len(df) - 1) if len(df) > 1 else 0.5
        
        return dict(zip(df["symbol"], df["quantile"]))
    
    def calculate_pe_rank(self, symbols: List[str], 
                         fundamental_data: Dict[str, Dict]) -> Dict[str, float]:
        """
        计算市盈率截面排名分位数
        
        Args:
            symbols: 股票列表
            fundamental_data: 基本面数据
        
        Returns:
            {symbol: 分位数}（0-1，越小表示PE越小）
        """
        if not symbols:
            return {}
        
        pe_values = []
        valid_symbols = []
        
        for symbol in symbols:
            if symbol in fundamental_data:
                pe = fundamental_data[symbol].get("pe", 0)
                # 只考虑正PE
                if pe > 0:
                    pe_values.append(pe)
                    valid_symbols.append(symbol)
        
        if not pe_values:
            return {symbol: 0.5 for symbol in symbols}
        
        # 计算分位数
        df = pd.DataFrame({"symbol": valid_symbols, "pe": pe_values})
        df["rank"] = df["pe"].rank(method="min")
        df["quantile"] = (df["rank"] - 1) / (len(df) - 1) if len(df) > 1 else 0.5
        
        return dict(zip(df["symbol"], df["quantile"]))
    
    def filter_by_fundamental(self, symbols: List[str], 
                             fundamental_data: Dict[str, Dict],
                             filters: Dict[str, Tuple[Any, Any]]) -> List[str]:
        """
        基于基本面指标筛选股票
        
        Args:
            symbols: 股票列表
            fundamental_data: 基本面数据
            filters: 筛选条件 {指标名: (最小值, 最大值)}
        
        Returns:
            筛选后的股票列表
        """
        filtered = []
        
        for symbol in symbols:
            if symbol not in fundamental_data:
                continue
            
            fund_data = fundamental_data[symbol]
            passed = True
            
            for indicator, (min_val, max_val) in filters.items():
                value = fund_data.get(indicator, None)
                
                if value is None:
                    passed = False
                    break
                
                # 检查最小值
                if min_val is not None and value < min_val:
                    passed = False
                    break
                
                # 检查最大值
                if max_val is not None and value > max_val:
                    passed = False
                    break
            
            if passed:
                filtered.append(symbol)
        
        return filtered
    
    def calculate_composite_score(self, symbols: List[str],
                                 ranking_data: Dict[str, Dict[str, float]],
                                 weights: Dict[str, float]) -> Dict[str, float]:
        """
        计算综合评分
        
        Args:
            symbols: 股票列表
            ranking_data: 排名数据 {指标: {symbol: 排名分位数}}
            weights: 权重 {指标: 权重}
        
        Returns:
            {symbol: 综合评分}（越小越好）
        """
        if not symbols or not ranking_data:
            return {symbol: 0.5 for symbol in symbols}
        
        # 标准化权重
        total_weight = sum(weights.values())
        if total_weight <= 0:
            return {symbol: 0.5 for symbol in symbols}
        
        normalized_weights = {k: v / total_weight for k, v in weights.items()}
        
        scores = {}
        for symbol in symbols:
            total_score = 0.0
            missing_data = False
            
            for indicator, weight in normalized_weights.items():
                if indicator in ranking_data and symbol in ranking_data[indicator]:
                    rank = ranking_data[indicator][symbol]
                    total_score += rank * weight
                else:
                    missing_data = True
                    break
            
            if not missing_data:
                scores[symbol] = total_score
        
        # 如果没有有效数据，返回默认值
        if not scores:
            return {symbol: 0.5 for symbol in symbols}
        
        return scores
    
    def select_top_stocks(self, symbols: List[str], 
                         scores: Dict[str, float], 
                         count: int,
                         ascending: bool = True) -> List[str]:
        """
        根据评分选择前N只股票
        
        Args:
            symbols: 股票列表
            scores: 评分字典 {symbol: 评分}
            count: 选择数量
            ascending: True表示评分越小越好，False表示评分越大越好
        
        Returns:
            选中的股票列表
        """
        if not symbols or not scores:
            return symbols[:count] if symbols else []
        
        # 创建DataFrame
        df = pd.DataFrame({
            "symbol": list(scores.keys()),
            "score": list(scores.values())
        })
        
        # 排序
        df = df.sort_values("score", ascending=ascending)
        
        # 选择前N个
        selected = df.head(min(count, len(df)))["symbol"].tolist()
        
        return selected
    
    def calculate_position_size(self, symbol: str, price: float,
                              portfolio_value: float, 
                              max_position_pct: float = 0.05) -> int:
        """
        计算建议持仓数量
        
        Args:
            symbol: 股票代码
            price: 股票价格
            portfolio_value: 组合总价值
            max_position_pct: 最大仓位百分比
        
        Returns:
            建议持仓数量
        """
        if price <= 0:
            return 0
        
        max_position_value = portfolio_value * max_position_pct
        quantity = int(max_position_value / price)
        
        # 确保是100股的整数倍（A股规定）
        quantity = (quantity // 100) * 100
        
        return max(100, quantity)  # 最小100股
    
    def get_performance_report(self) -> Dict:
        """获取策略绩效报告"""
        running_days = (datetime.now() - self.start_time).days
        if running_days == 0:
            running_days = 1
        
        return {
            "strategy_name": self.name,
            "enabled": self.enabled,
            "weight": self.weight,
            "signals_generated": self.signals_generated,
            "signals_executed": self.signals_executed,
            "execution_rate": self.signals_executed / self.signals_generated if self.signals_generated > 0 else 0,
            "running_days": running_days,
            "parameters": self.parameters,
            "timestamp": datetime.now().isoformat()
        }
    
    def update_parameters(self, new_parameters: Dict):
        """更新策略参数"""
        self.parameters.update(new_parameters)
        logger.info(f"策略 {self.name} 参数已更新: {new_parameters}")
    
    def __str__(self) -> str:
        return f"{self.name}(enabled={self.enabled}, weight={self.weight:.2f})"
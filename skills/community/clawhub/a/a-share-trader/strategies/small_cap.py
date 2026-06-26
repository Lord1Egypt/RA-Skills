"""
小市值策略
非 ST；非科创板；非停牌；上市超 252 天；流通市值 > 5 亿；归母净利润 TTM>0；股息率 > 0；
1/4 月按股息率排名降序初选 20 只，其他月份按流通市值排名升序初选 20 只；
初选池按 20 日换手率波动率最小选 10 只；每 5 个交易日调仓
"""

import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import random
import numpy as np

from .base_strategy import BaseStrategy

logger = logging.getLogger(__name__)


class SmallCapStrategy(BaseStrategy):
    """小市值策略"""
    
    def __init__(self,
                 min_market_cap: float = 500000000,  # 5亿
                 min_listing_days: int = 252,        # 上市超252天
                 min_profit_ttm: float = 0,          # 归母净利润TTM>0
                 min_dividend_yield: float = 0.0,    # 股息率>0
                 exclude_st: bool = True,
                 exclude_star: bool = True,
                 exclude_suspended: bool = True,
                 monthly_logic: bool = True,         # 月度切换逻辑
                 jan_apr_dividend: bool = True,      # 1/4月按股息率
                 other_months_market_cap: bool = True, # 其他月按流通市值
                 initial_screen: int = 20,           # 初选20只
                 final_screen: int = 10,             # 终选10只
                 screening_by: str = "turnover_volatility", # 按换手率波动率
                 rebalance_days: int = 5,
                 enabled: bool = True,
                 weight: float = 0.08,
                 **kwargs):
        """
        初始化小市值策略
        
        Args:
            min_market_cap: 最小流通市值
            min_listing_days: 最小上市天数
            min_profit_ttm: 最小归母净利润TTM
            min_dividend_yield: 最小股息率
            exclude_st: 排除ST股
            exclude_star: 排除科创板
            exclude_suspended: 排除停牌股
            monthly_logic: 启用月度切换逻辑
            jan_apr_dividend: 1/4月按股息率
            other_months_market_cap: 其他月按流通市值
            initial_screen: 初选数量
            final_screen: 终选数量
            screening_by: 终选方式（turnover_volatility）
            rebalance_days: 调仓周期
            enabled: 是否启用
            weight: 策略权重
            **kwargs: 其他参数
        """
        super().__init__(
            name="SmallCapStrategy",
            enabled=enabled,
            weight=weight,
            min_market_cap=min_market_cap,
            min_listing_days=min_listing_days,
            min_profit_ttm=min_profit_ttm,
            min_dividend_yield=min_dividend_yield,
            exclude_st=exclude_st,
            exclude_star=exclude_star,
            exclude_suspended=exclude_suspended,
            monthly_logic=monthly_logic,
            jan_apr_dividend=jan_apr_dividend,
            other_months_market_cap=other_months_market_cap,
            initial_screen=initial_screen,
            final_screen=final_screen,
            screening_by=screening_by,
            rebalance_days=rebalance_days,
            **kwargs
        )
        
        # 策略状态
        self.last_rebalance = None
        self.current_holdings = []
        
        logger.info(f"小市值策略初始化: 初选{initial_screen}只, 终选{final_screen}只, "
                   f"调仓周期{rebalance_days}天")
    
    def generate_signals(self, market_data: Dict[str, Dict], 
                        fundamental_data: Optional[Dict[str, Dict]] = None,
                        technical_data: Optional[Dict[str, Dict]] = None) -> List[Dict]:
        """
        生成小市值策略交易信号
        
        Args:
            market_data: 市场数据
            fundamental_data: 基本面数据
            technical_data: 技术指标数据（用于换手率波动率）
        
        Returns:
            交易信号列表
        """
        signals = []
        
        if not market_data or not fundamental_data:
            logger.warning("小市值策略: 缺少市场数据或基本面数据")
            return signals
        
        # 检查是否需要调仓
        if not self._should_rebalance():
            logger.debug("小市值策略: 未到调仓时间，维持当前持仓")
            return self._generate_hold_signals()
        
        # 获取候选股票
        candidate_symbols = list(market_data.keys())
        
        # 筛选股票
        filtered_symbols = self._filter_stocks(candidate_symbols, fundamental_data)
        
        if not filtered_symbols:
            logger.warning("小市值策略: 筛选后无符合条件股票")
            return signals
        
        # 应用月度切换逻辑进行初选
        initial_selected = self._apply_monthly_logic(filtered_symbols, fundamental_data)
        
        # 如果没有足够股票，使用全部筛选后的
        if len(initial_selected) < self.parameters["initial_screen"]:
            initial_selected = filtered_symbols[:self.parameters["initial_screen"]]
        
        # 终选：按换手率波动率最小
        final_selected = self._final_screening(initial_selected, technical_data)
        
        # 生成交易信号
        signals = self._generate_rebalance_signals(final_selected, market_data)
        
        # 更新持仓和调仓时间
        self.current_holdings = final_selected
        self.last_rebalance = datetime.now()
        
        self.signals_generated += len(signals)
        logger.info(f"小市值策略生成 {len(signals)} 个信号，目标持仓: {final_selected[:5]}...")
        
        return signals
    
    def _should_rebalance(self) -> bool:
        """检查是否需要调仓"""
        if self.last_rebalance is None:
            return True
        
        rebalance_days = self.parameters.get("rebalance_days", 5)
        days_since_rebalance = (datetime.now() - self.last_rebalance).days
        
        return days_since_rebalance >= rebalance_days
    
    def _filter_stocks(self, symbols: List[str], fundamental_data: Dict[str, Dict]) -> List[str]:
        """筛选符合条件的股票"""
        filtered = []
        
        for symbol in symbols:
            if symbol not in fundamental_data:
                continue
            
            fund_data = fundamental_data[symbol]
            
            # 基本筛选
            if not self._pass_basic_filters(symbol, fund_data):
                continue
            
            # 市值筛选
            market_cap = fund_data.get("market_cap", 0)
            if market_cap < self.parameters["min_market_cap"]:
                continue
            
            # 上市天数筛选
            listing_days = fund_data.get("listing_days", 0)
            if listing_days < self.parameters["min_listing_days"]:
                continue
            
            # 净利润筛选
            profit_ttm = fund_data.get("profit_ttm", fund_data.get("profit_growth", -1))
            if profit_ttm <= self.parameters["min_profit_ttm"]:
                continue
            
            # 股息率筛选
            dividend_yield = fund_data.get("dividend_yield", 0)
            if dividend_yield <= self.parameters["min_dividend_yield"]:
                continue
            
            filtered.append(symbol)
        
        return filtered
    
    def _pass_basic_filters(self, symbol: str, fund_data: Dict) -> bool:
        """通过基本筛选条件"""
        # 排除ST股
        if self.parameters.get("exclude_st", True):
            if fund_data.get("is_st", False):
                return False
        
        # 排除科创板
        if self.parameters.get("exclude_star", True):
            if fund_data.get("is_star", False):
                return False
        
        # 排除停牌股
        if self.parameters.get("exclude_suspended", True):
            if fund_data.get("is_suspended", False):
                return False
        
        return True
    
    def _apply_monthly_logic(self, symbols: List[str], fundamental_data: Dict[str, Dict]) -> List[str]:
        """应用月度切换逻辑"""
        if not self.parameters.get("monthly_logic", True):
            # 不启用月度逻辑，按流通市值排序
            return self._sort_by_market_cap(symbols, fundamental_data)
        
        current_month = datetime.now().month
        
        # 1月或4月：按股息率降序
        if current_month in [1, 4] and self.parameters.get("jan_apr_dividend", True):
            return self._sort_by_dividend_yield(symbols, fundamental_data)
        else:
            # 其他月份：按流通市值升序
            return self._sort_by_market_cap(symbols, fundamental_data)
    
    def _sort_by_market_cap(self, symbols: List[str], fundamental_data: Dict[str, Dict]) -> List[str]:
        """按流通市值升序排序"""
        if not symbols:
            return []
        
        # 收集市值数据
        market_cap_data = []
        for symbol in symbols:
            if symbol in fundamental_data:
                market_cap = fundamental_data[symbol].get("market_cap", float('inf'))
                market_cap_data.append((symbol, market_cap))
        
        # 按市值升序排序
        market_cap_data.sort(key=lambda x: x[1])
        
        # 提取股票代码
        sorted_symbols = [item[0] for item in market_cap_data]
        
        return sorted_symbols
    
    def _sort_by_dividend_yield(self, symbols: List[str], fundamental_data: Dict[str, Dict]) -> List[str]:
        """按股息率降序排序"""
        if not symbols:
            return []
        
        # 收集股息率数据
        dividend_data = []
        for symbol in symbols:
            if symbol in fundamental_data:
                dividend_yield = fundamental_data[symbol].get("dividend_yield", -1)
                dividend_data.append((symbol, dividend_yield))
        
        # 按股息率降序排序
        dividend_data.sort(key=lambda x: x[1], reverse=True)
        
        # 提取股票代码
        sorted_symbols = [item[0] for item in dividend_data]
        
        return sorted_symbols
    
    def _final_screening(self, symbols: List[str], technical_data: Optional[Dict[str, Dict]]) -> List[str]:
        """终选：按换手率波动率最小"""
        if not symbols:
            return []
        
        screening_by = self.parameters.get("screening_by", "turnover_volatility")
        final_count = self.parameters.get("final_screen", 10)
        
        if screening_by == "turnover_volatility":
            # 按换手率波动率最小（模拟实现）
            # 在实际系统中，应从技术数据获取20日换手率波动率
            
            # 如果没有技术数据，随机选择
            if not technical_data:
                return symbols[:min(final_count, len(symbols))]
            
            # 模拟换手率波动率
            volatility_data = []
            for symbol in symbols:
                tech_data = technical_data.get(symbol, {})
                # 模拟波动率：0-1之间的随机值
                turnover_volatility = tech_data.get("turnover_volatility", random.random())
                volatility_data.append((symbol, turnover_volatility))
            
            # 按波动率升序排序（波动率最小）
            volatility_data.sort(key=lambda x: x[1])
            
            # 提取前N个
            selected = [item[0] for item in volatility_data[:final_count]]
            return selected
        
        else:
            # 默认：直接选择前N个
            return symbols[:min(final_count, len(symbols))]
    
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
                        "reason": "小市值策略调仓卖出"
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
                        "reason": "小市值策略调仓买入"
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
                "reason": "维持小市值策略持仓"
            }
            signals.append(signal_dict)
        
        return signals
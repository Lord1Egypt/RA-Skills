"""
营收利润双增策略
非 ST，非科创板，非停牌，上市超 365 天；流通市值 > 5 亿；
净利润同比 > 30%；营业收入同比 > 30%；0 < 市盈率 < 50；市净率 < 5；
按总市值从小到大选前 10 只；每 5 个交易日调仓，持仓等权重
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import random

from .base_strategy import BaseStrategy

logger = logging.getLogger(__name__)


class RevenueProfitStrategy(BaseStrategy):
    """营收利润双增策略"""
    
    def __init__(self,
                 min_market_cap: float = 500000000,  # 5亿
                 min_listing_days: int = 365,        # 上市超365天
                 min_profit_growth: float = 0.30,    # 净利润同比>30%
                 min_revenue_growth: float = 0.30,   # 营业收入同比>30%
                 pe_min: float = 0.1,                # 0<市盈率
                 pe_max: float = 50.0,               # 市盈率<50
                 pb_max: float = 5.0,                # 市净率<5
                 exclude_st: bool = True,
                 exclude_star: bool = True,
                 exclude_suspended: bool = True,
                 sort_by: str = "market_cap",        # 按总市值从小到大
                 holding_count: int = 10,
                 rebalance_days: int = 5,
                 enabled: bool = True,
                 weight: float = 0.10,
                 **kwargs):
        """
        初始化营收利润双增策略
        
        Args:
            min_market_cap: 最小流通市值
            min_listing_days: 最小上市天数
            min_profit_growth: 最小净利润同比增长率
            min_revenue_growth: 最小营业收入同比增长率
            pe_min: 市盈率下限
            pe_max: 市盈率上限
            pb_max: 市净率上限
            exclude_st: 排除ST股
            exclude_star: 排除科创板
            exclude_suspended: 排除停牌股
            sort_by: 排序方式
            holding_count: 持仓数量
            rebalance_days: 调仓周期
            enabled: 是否启用
            weight: 策略权重
            **kwargs: 其他参数
        """
        super().__init__(
            name="RevenueProfitStrategy",
            enabled=enabled,
            weight=weight,
            min_market_cap=min_market_cap,
            min_listing_days=min_listing_days,
            min_profit_growth=min_profit_growth,
            min_revenue_growth=min_revenue_growth,
            pe_min=pe_min,
            pe_max=pe_max,
            pb_max=pb_max,
            exclude_st=exclude_st,
            exclude_star=exclude_star,
            exclude_suspended=exclude_suspended,
            sort_by=sort_by,
            holding_count=holding_count,
            rebalance_days=rebalance_days,
            **kwargs
        )
        
        # 策略状态
        self.last_rebalance = None
        self.current_holdings = []
        
        logger.info(f"营收利润双增策略初始化: 持仓数={holding_count}, 调仓周期={rebalance_days}天")
    
    def generate_signals(self, market_data: Dict[str, Dict], 
                        fundamental_data: Optional[Dict[str, Dict]] = None,
                        technical_data: Optional[Dict[str, Dict]] = None) -> List[Dict]:
        """
        生成营收利润双增策略交易信号
        
        Args:
            market_data: 市场数据
            fundamental_data: 基本面数据
            technical_data: 技术指标数据（本策略不使用）
        
        Returns:
            交易信号列表
        """
        signals = []
        
        if not market_data or not fundamental_data:
            logger.warning("营收利润双增策略: 缺少市场数据或基本面数据")
            return signals
        
        # 检查是否需要调仓
        if not self._should_rebalance():
            logger.debug("营收利润双增策略: 未到调仓时间，维持当前持仓")
            return self._generate_hold_signals()
        
        # 获取候选股票
        candidate_symbols = list(market_data.keys())
        
        # 筛选股票
        filtered_symbols = self._filter_stocks(candidate_symbols, fundamental_data)
        
        if not filtered_symbols:
            logger.warning("营收利润双增策略: 筛选后无符合条件股票")
            return signals
        
        # 排序股票
        sorted_symbols = self._sort_stocks(filtered_symbols, fundamental_data)
        
        # 选择目标持仓
        target_holdings = sorted_symbols[:self.parameters["holding_count"]]
        
        # 生成交易信号
        signals = self._generate_rebalance_signals(target_holdings, market_data)
        
        # 更新持仓和调仓时间
        self.current_holdings = target_holdings
        self.last_rebalance = datetime.now()
        
        self.signals_generated += len(signals)
        logger.info(f"营收利润双增策略生成 {len(signals)} 个信号，目标持仓: {target_holdings}")
        
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
            
            # 增长指标筛选
            profit_growth = fund_data.get("profit_growth", -1)
            if profit_growth < self.parameters["min_profit_growth"]:
                continue
            
            revenue_growth = fund_data.get("revenue_growth", -1)
            if revenue_growth < self.parameters["min_revenue_growth"]:
                continue
            
            # 估值指标筛选
            pe = fund_data.get("pe", 0)
            if pe <= self.parameters["pe_min"] or pe > self.parameters["pe_max"]:
                continue
            
            pb = fund_data.get("pb", 0)
            if pb > self.parameters["pb_max"]:
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
        
        # 排除退市股
        if fund_data.get("is_delisted", False):
            return False
        
        return True
    
    def _sort_stocks(self, symbols: List[str], fundamental_data: Dict[str, Dict]) -> List[str]:
        """排序股票"""
        if not symbols:
            return []
        
        sort_by = self.parameters.get("sort_by", "market_cap")
        
        # 收集排序数据
        sort_data = []
        for symbol in symbols:
            if symbol in fundamental_data:
                fund_data = fundamental_data[symbol]
                
                if sort_by == "market_cap":
                    value = fund_data.get("market_cap", 0)
                elif sort_by == "pe":
                    value = fund_data.get("pe", 1000)
                elif sort_by == "pb":
                    value = fund_data.get("pb", 1000)
                else:
                    value = fund_data.get("market_cap", 0)
                
                sort_data.append((symbol, value))
        
        # 按市值从小到大排序（升序）
        sort_data.sort(key=lambda x: x[1])
        
        # 提取股票代码
        sorted_symbols = [item[0] for item in sort_data]
        
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
                        "reason": "营收利润双增策略调仓卖出"
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
                        "reason": "营收利润双增策略调仓买入"
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
                "reason": "维持营收利润双增策略持仓"
            }
            signals.append(signal_dict)
        
        return signals
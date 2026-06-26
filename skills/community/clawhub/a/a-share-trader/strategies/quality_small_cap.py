"""
基本面加小市值策略
股息率 > 2%、净利润同比增长率 TTM>0.1、年化 ROE>15%、毛利率 TTM>30%、PE_TTM<25；
非 ST、非停牌；按流通市值升序选前 5 只，每 14 个交易日调仓
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import random

from .base_strategy import BaseStrategy

logger = logging.getLogger(__name__)


class QualitySmallCapStrategy(BaseStrategy):
    """基本面加小市值策略"""
    
    def __init__(self,
                 min_dividend_yield: float = 0.02,    # 股息率>2%
                 min_profit_growth: float = 0.10,     # 净利润同比增长率>10%
                 min_roe: float = 0.15,               # ROE>15%
                 min_gross_margin: float = 0.30,      # 毛利率>30%
                 max_pe_ttm: float = 25.0,            # PE_TTM<25
                 exclude_st: bool = True,
                 exclude_suspended: bool = True,
                 sort_by: str = "market_cap",         # 按流通市值升序
                 holding_count: int = 5,
                 rebalance_days: int = 14,
                 enabled: bool = True,
                 weight: float = 0.08,
                 **kwargs):
        """
        初始化基本面加小市值策略
        
        Args:
            min_dividend_yield: 最小股息率
            min_profit_growth: 最小净利润同比增长率
            min_roe: 最小ROE
            min_gross_margin: 最小毛利率
            max_pe_ttm: 最大PE_TTM
            exclude_st: 排除ST股
            exclude_suspended: 排除停牌股
            sort_by: 排序方式
            holding_count: 持仓数量
            rebalance_days: 调仓周期
            enabled: 是否启用
            weight: 策略权重
            **kwargs: 其他参数
        """
        super().__init__(
            name="QualitySmallCapStrategy",
            enabled=enabled,
            weight=weight,
            min_dividend_yield=min_dividend_yield,
            min_profit_growth=min_profit_growth,
            min_roe=min_roe,
            min_gross_margin=min_gross_margin,
            max_pe_ttm=max_pe_ttm,
            exclude_st=exclude_st,
            exclude_suspended=exclude_suspended,
            sort_by=sort_by,
            holding_count=holding_count,
            rebalance_days=rebalance_days,
            **kwargs
        )
        
        # 策略状态
        self.last_rebalance = None
        self.current_holdings = []
        
        logger.info(f"基本面加小市值策略初始化: 持仓数={holding_count}, 调仓周期={rebalance_days}天")
    
    def generate_signals(self, market_data: Dict[str, Dict], 
                        fundamental_data: Optional[Dict[str, Dict]] = None,
                        technical_data: Optional[Dict[str, Dict]] = None) -> List[Dict]:
        """
        生成基本面加小市值策略交易信号
        
        Args:
            market_data: 市场数据
            fundamental_data: 基本面数据
            technical_data: 技术指标数据（本策略不使用）
        
        Returns:
            交易信号列表
        """
        signals = []
        
        if not market_data or not fundamental_data:
            logger.warning("基本面加小市值策略: 缺少市场数据或基本面数据")
            return signals
        
        # 检查是否需要调仓
        if not self._should_rebalance():
            logger.debug("基本面加小市值策略: 未到调仓时间，维持当前持仓")
            return self._generate_hold_signals()
        
        # 获取候选股票
        candidate_symbols = list(market_data.keys())
        
        # 筛选股票
        filtered_symbols = self._filter_stocks(candidate_symbols, fundamental_data)
        
        if not filtered_symbols:
            logger.warning("基本面加小市值策略: 筛选后无符合条件股票")
            return signals
        
        # 排序股票（按流通市值升序）
        sorted_symbols = self._sort_stocks(filtered_symbols, fundamental_data)
        
        # 选择目标持仓
        target_holdings = sorted_symbols[:self.parameters["holding_count"]]
        
        # 生成交易信号
        signals = self._generate_rebalance_signals(target_holdings, market_data)
        
        # 更新持仓和调仓时间
        self.current_holdings = target_holdings
        self.last_rebalance = datetime.now()
        
        self.signals_generated += len(signals)
        logger.info(f"基本面加小市值策略生成 {len(signals)} 个信号，目标持仓: {target_holdings}")
        
        return signals
    
    def _should_rebalance(self) -> bool:
        """检查是否需要调仓"""
        if self.last_rebalance is None:
            return True
        
        rebalance_days = self.parameters.get("rebalance_days", 14)
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
            
            # 股息率筛选
            dividend_yield = fund_data.get("dividend_yield", 0)
            if dividend_yield < self.parameters["min_dividend_yield"]:
                continue
            
            # 净利润增长筛选
            profit_growth = fund_data.get("profit_growth", -1)
            if profit_growth < self.parameters["min_profit_growth"]:
                continue
            
            # ROE筛选
            roe = fund_data.get("roe", 0)
            if roe < self.parameters["min_roe"]:
                continue
            
            # 毛利率筛选
            gross_margin = fund_data.get("gross_margin", 0)
            if gross_margin < self.parameters["min_gross_margin"]:
                continue
            
            # PE筛选
            pe = fund_data.get("pe", 1000)
            if pe > self.parameters["max_pe_ttm"]:
                continue
            
            filtered.append(symbol)
        
        return filtered
    
    def _pass_basic_filters(self, symbol: str, fund_data: Dict) -> bool:
        """通过基本筛选条件"""
        # 排除ST股
        if self.parameters.get("exclude_st", True):
            if fund_data.get("is_st", False):
                return False
        
        # 排除停牌股
        if self.parameters.get("exclude_suspended", True):
            if fund_data.get("is_suspended", False):
                return False
        
        return True
    
    def _sort_stocks(self, symbols: List[str], fundamental_data: Dict[str, Dict]) -> List[str]:
        """排序股票（按流通市值升序）"""
        if not symbols:
            return []
        
        # 收集市值数据
        market_cap_data = []
        for symbol in symbols:
            if symbol in fundamental_data:
                market_cap = fundamental_data[symbol].get("market_cap", 0)
                market_cap_data.append((symbol, market_cap))
        
        # 按市值升序排序
        market_cap_data.sort(key=lambda x: x[1])
        
        # 提取股票代码
        sorted_symbols = [item[0] for item in market_cap_data]
        
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
                        "reason": "基本面加小市值策略调仓卖出"
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
                        "reason": "基本面加小市值策略调仓买入"
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
                "reason": "维持基本面加小市值策略持仓"
            }
            signals.append(signal_dict)
        
        return signals
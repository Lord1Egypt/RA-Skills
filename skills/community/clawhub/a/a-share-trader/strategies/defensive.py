"""
防御选股策略（红利策略）
红利按股息率降序选股策略：总市值截面升序排序分位数大于0.2，
市盈率截面升序排序分位数小于0.4，市盈率为正，价格不高于30元，
非ST，非停牌；5日调仓，持股3只
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime

from .base_strategy import BaseStrategy, Signal

logger = logging.getLogger(__name__)


class DefensiveStrategy(BaseStrategy):
    """防御选股策略（高股息策略）"""
    
    def __init__(self,
                 min_dividend_yield: float = 0.04,     # 4%
                 max_dividend_yield: float = 0.15,     # 15%（防止异常值）
                 market_cap_quantile_min: float = 0.2, # 总市值分位数>0.2
                 pe_quantile_max: float = 0.4,         # 市盈率分位数<0.4
                 max_price: float = 30.0,              # 价格不高于30元
                 pe_positive: bool = True,             # 市盈率为正
                 exclude_st: bool = True,
                 exclude_suspended: bool = True,
                 holding_count: int = 3,
                 rebalance_days: int = 5,
                 enabled: bool = True,
                 weight: float = 0.12,
                 **kwargs):
        """
        初始化防御策略
        
        Args:
            min_dividend_yield: 最小股息率
            max_dividend_yield: 最大股息率
            market_cap_quantile_min: 总市值分位数下限
            pe_quantile_max: 市盈率分位数上限
            max_price: 最高价格限制
            pe_positive: 市盈率必须为正
            exclude_st: 排除ST股
            exclude_suspended: 排除停牌股
            holding_count: 持仓数量
            rebalance_days: 调仓周期
            enabled: 是否启用
            weight: 策略权重
            **kwargs: 其他参数
        """
        super().__init__(
            name="DefensiveStrategy",
            enabled=enabled,
            weight=weight,
            min_dividend_yield=min_dividend_yield,
            max_dividend_yield=max_dividend_yield,
            market_cap_quantile_min=market_cap_quantile_min,
            pe_quantile_max=pe_quantile_max,
            max_price=max_price,
            pe_positive=pe_positive,
            exclude_st=exclude_st,
            exclude_suspended=exclude_suspended,
            holding_count=holding_count,
            rebalance_days=rebalance_days,
            **kwargs
        )
        
        # 策略状态
        self.last_rebalance = None
        self.current_holdings = []
        
        logger.info(f"防御策略初始化: 持仓数={holding_count}, 调仓周期={rebalance_days}天")
    
    def generate_signals(self, market_data: Dict[str, Dict], 
                        fundamental_data: Optional[Dict[str, Dict]] = None,
                        technical_data: Optional[Dict[str, Dict]] = None) -> List[Signal]:
        """
        生成防御策略交易信号
        
        Args:
            market_data: 市场数据
            fundamental_data: 基本面数据
            technical_data: 技术指标数据（本策略不使用）
        
        Returns:
            交易信号列表
        """
        signals = []
        
        if not market_data or not fundamental_data:
            logger.warning("防御策略: 缺少市场数据或基本面数据")
            return signals
        
        # 检查是否需要调仓
        if not self._should_rebalance():
            logger.debug("防御策略: 未到调仓时间，维持当前持仓")
            return self._generate_hold_signals()
        
        # 获取候选股票
        candidate_symbols = list(market_data.keys())
        
        # 筛选股票
        filtered_symbols = self._filter_stocks(candidate_symbols, market_data, fundamental_data)
        
        if not filtered_symbols:
            logger.warning("防御策略: 筛选后无符合条件股票")
            return signals
        
        # 按股息率排序
        sorted_symbols = self._sort_by_dividend_yield(filtered_symbols, fundamental_data)
        
        # 选择目标持仓
        target_holdings = sorted_symbols[:self.parameters["holding_count"]]
        
        # 生成交易信号
        signals = self._generate_rebalance_signals(target_holdings, market_data)
        
        # 更新持仓和调仓时间
        self.current_holdings = target_holdings
        self.last_rebalance = datetime.now()
        
        self.signals_generated += len(signals)
        logger.info(f"防御策略生成 {len(signals)} 个信号，目标持仓: {target_holdings}")
        
        return signals
    
    def _should_rebalance(self) -> bool:
        """检查是否需要调仓"""
        if self.last_rebalance is None:
            return True
        
        rebalance_days = self.parameters.get("rebalance_days", 5)
        days_since_rebalance = (datetime.now() - self.last_rebalance).days
        
        return days_since_rebalance >= rebalance_days
    
    def _filter_stocks(self, symbols: List[str], 
                      market_data: Dict[str, Dict],
                      fundamental_data: Dict[str, Dict]) -> List[str]:
        """筛选符合条件的股票"""
        filtered = []
        
        for symbol in symbols:
            if symbol not in fundamental_data or symbol not in market_data:
                continue
            
            fund_data = fundamental_data[symbol]
            mkt_data = market_data[symbol]
            
            # 基本筛选
            if not self._pass_basic_filters(symbol, fund_data):
                continue
            
            # 价格筛选
            price = mkt_data.get("price", 0)
            if price > self.parameters["max_price"]:
                continue
            
            # 股息率筛选
            dividend_yield = fund_data.get("dividend_yield", 0)
            if dividend_yield < self.parameters["min_dividend_yield"]:
                continue
            
            if dividend_yield > self.parameters["max_dividend_yield"]:
                continue
            
            # 市盈率筛选
            pe = fund_data.get("pe", 0)
            if self.parameters["pe_positive"] and pe <= 0:
                continue
            
            filtered.append(symbol)
        
        # 应用截面排名筛选
        filtered = self._apply_cross_section_filters(filtered, fundamental_data)
        
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
        
        # 排除退市股
        if fund_data.get("is_delisted", False):
            return False
        
        return True
    
    def _apply_cross_section_filters(self, symbols: List[str], 
                                    fundamental_data: Dict[str, Dict]) -> List[str]:
        """应用截面排名筛选"""
        if len(symbols) < 2:
            return symbols
        
        # 计算总市值分位数
        market_cap_quantiles = self.calculate_market_cap_rank(symbols, fundamental_data)
        
        # 计算市盈率分位数
        pe_quantiles = self.calculate_pe_rank(symbols, fundamental_data)
        
        # 筛选
        filtered = []
        for symbol in symbols:
            # 总市值分位数>0.2
            market_cap_q = market_cap_quantiles.get(symbol, 0.5)
            if market_cap_q <= self.parameters["market_cap_quantile_min"]:
                continue
            
            # 市盈率分位数<0.4
            pe_q = pe_quantiles.get(symbol, 0.5)
            if pe_q >= self.parameters["pe_quantile_max"]:
                continue
            
            filtered.append(symbol)
        
        return filtered
    
    def _sort_by_dividend_yield(self, symbols: List[str], 
                               fundamental_data: Dict[str, Dict]) -> List[str]:
        """按股息率降序排序"""
        if not symbols:
            return []
        
        # 收集股息率数据
        dividend_data = []
        for symbol in symbols:
            if symbol in fundamental_data:
                dividend_yield = fundamental_data[symbol].get("dividend_yield", 0)
                dividend_data.append((symbol, dividend_yield))
        
        # 按股息率降序排序
        dividend_data.sort(key=lambda x: x[1], reverse=True)
        
        # 提取股票代码
        sorted_symbols = [item[0] for item in dividend_data]
        
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
                        "reason": "调仓卖出"
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
                        "reason": "调仓买入"
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
                "reason": "维持持仓（高股息防御）"
            }
            signals.append(signal_dict)
        
        return signals
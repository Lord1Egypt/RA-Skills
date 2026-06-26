"""
社保重仓策略
非ST,主板,非退市,流通市值>10亿,PE>0,前十大流通股东名称包含社保,
按照十大流通股东持股比例从大到小排序。
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import random

from .base_strategy import BaseStrategy

logger = logging.getLogger(__name__)


class SocialSecurityStrategy(BaseStrategy):
    """社保重仓策略"""
    
    def __init__(self,
                 min_market_cap: float = 1000000000,  # 10亿
                 min_pe: float = 0.1,                 # PE>0
                 include_social_security: bool = True, # 前十大包含社保
                 sort_by: str = "holding_ratio",      # 按持股比例从大到小
                 exclude_st: bool = True,
                 exclude_delisted: bool = True,
                 board_filter: List[str] = None,      # 主板过滤
                 holding_count: int = 8,
                 rebalance_days: int = 10,
                 enabled: bool = True,
                 weight: float = 0.07,
                 **kwargs):
        """
        初始化社保重仓策略
        
        Args:
            min_market_cap: 最小流通市值
            min_pe: 最小市盈率
            include_social_security: 前十大包含社保
            sort_by: 排序方式
            exclude_st: 排除ST股
            exclude_delisted: 排除退市股
            board_filter: 板块过滤
            holding_count: 持仓数量
            rebalance_days: 调仓周期
            enabled: 是否启用
            weight: 策略权重
            **kwargs: 其他参数
        """
        super().__init__(
            name="SocialSecurityStrategy",
            enabled=enabled,
            weight=weight,
            min_market_cap=min_market_cap,
            min_pe=min_pe,
            include_social_security=include_social_security,
            sort_by=sort_by,
            exclude_st=exclude_st,
            exclude_delisted=exclude_delisted,
            board_filter=board_filter or ["main"],
            holding_count=holding_count,
            rebalance_days=rebalance_days,
            **kwargs
        )
        
        # 策略状态
        self.last_rebalance = None
        self.current_holdings = []
        
        logger.info(f"社保重仓策略初始化: 持仓数={holding_count}, 调仓周期={rebalance_days}天")
    
    def generate_signals(self, market_data: Dict[str, Dict], 
                        fundamental_data: Optional[Dict[str, Dict]] = None,
                        technical_data: Optional[Dict[str, Dict]] = None) -> List[Dict]:
        """
        生成社保重仓策略交易信号
        
        Args:
            market_data: 市场数据
            fundamental_data: 基本面数据（需包含股东信息）
            technical_data: 技术指标数据（本策略不使用）
        
        Returns:
            交易信号列表
        """
        signals = []
        
        if not market_data or not fundamental_data:
            logger.warning("社保重仓策略: 缺少市场数据或基本面数据")
            return signals
        
        # 检查是否需要调仓
        if not self._should_rebalance():
            logger.debug("社保重仓策略: 未到调仓时间，维持当前持仓")
            return self._generate_hold_signals()
        
        # 获取候选股票
        candidate_symbols = list(market_data.keys())
        
        # 筛选股票
        filtered_symbols = self._filter_stocks(candidate_symbols, fundamental_data)
        
        if not filtered_symbols:
            logger.warning("社保重仓策略: 筛选后无符合条件股票")
            return signals
        
        # 排序股票（按持股比例从大到小）
        sorted_symbols = self._sort_stocks(filtered_symbols, fundamental_data)
        
        # 选择目标持仓
        target_holdings = sorted_symbols[:self.parameters["holding_count"]]
        
        # 生成交易信号
        signals = self._generate_rebalance_signals(target_holdings, market_data)
        
        # 更新持仓和调仓时间
        self.current_holdings = target_holdings
        self.last_rebalance = datetime.now()
        
        self.signals_generated += len(signals)
        logger.info(f"社保重仓策略生成 {len(signals)} 个信号，目标持仓: {target_holdings}")
        
        return signals
    
    def _should_rebalance(self) -> bool:
        """检查是否需要调仓"""
        if self.last_rebalance is None:
            return True
        
        rebalance_days = self.parameters.get("rebalance_days", 10)
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
            
            # 市盈率筛选
            pe = fund_data.get("pe", 0)
            if pe <= self.parameters["min_pe"]:
                continue
            
            # 社保持股筛选
            if self.parameters["include_social_security"]:
                if not self._has_social_security(fund_data):
                    continue
            
            filtered.append(symbol)
        
        return filtered
    
    def _pass_basic_filters(self, symbol: str, fund_data: Dict) -> bool:
        """通过基本筛选条件"""
        # 排除ST股
        if self.parameters.get("exclude_st", True):
            if fund_data.get("is_st", False):
                return False
        
        # 排除退市股
        if self.parameters.get("exclude_delisted", True):
            if fund_data.get("is_delisted", False):
                return False
        
        # 板块过滤
        board_filter = self.parameters.get("board_filter", ["main"])
        if board_filter:
            # 简单判断：科创板有"is_star"，创业板有"300"代码
            if "main" in board_filter:
                # 主板：非科创板、非创业板（简化）
                if fund_data.get("is_star", False):
                    return False
                if symbol.startswith("300") or symbol.startswith("688"):
                    return False
        
        return True
    
    def _has_social_security(self, fund_data: Dict) -> bool:
        """检查是否有社保持股"""
        # 在实际系统中，应从股东数据中检查
        # 这里使用模拟数据
        has_social_security = fund_data.get("has_social_security", None)
        
        if has_social_security is not None:
            return has_social_security
        
        # 模拟：30%概率有社保持股
        return random.random() < 0.3
    
    def _sort_stocks(self, symbols: List[str], fundamental_data: Dict[str, Dict]) -> List[str]:
        """排序股票（按持股比例从大到小）"""
        if not symbols:
            return []
        
        sort_by = self.parameters.get("sort_by", "holding_ratio")
        
        # 收集排序数据
        sort_data = []
        for symbol in symbols:
            if symbol in fundamental_data:
                fund_data = fundamental_data[symbol]
                
                if sort_by == "holding_ratio":
                    # 持股比例（模拟）
                    holding_ratio = fund_data.get("holding_ratio", random.random())
                    value = holding_ratio
                elif sort_by == "market_cap":
                    value = fund_data.get("market_cap", 0)
                else:
                    value = fund_data.get("holding_ratio", random.random())
                
                sort_data.append((symbol, value))
        
        # 按持股比例从大到小排序（降序）
        sort_data.sort(key=lambda x: x[1], reverse=True)
        
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
                        "reason": "社保重仓策略调仓卖出"
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
                        "reason": "社保重仓策略调仓买入"
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
                "reason": "维持社保重仓策略持仓"
            }
            signals.append(signal_dict)
        
        return signals
"""
控盘策略
中证1000成分股，筹码集中度90小于10%；
按总市值从小到大排列，优先选择小市值股票；
小于20只股票；等权重；每5个交易日调仓，再平衡；
交易价格: 开盘价买入和卖出；
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import random

from .base_strategy import BaseStrategy

logger = logging.getLogger(__name__)


class ChipConcentrationStrategy(BaseStrategy):
    """控盘策略"""
    
    def __init__(self,
                 index_constituent: str = "CSI1000",  # 中证1000成分股
                 max_chip_concentration: float = 0.10, # 筹码集中度90<10%
                 sort_by: str = "market_cap",         # 按总市值从小到大
                 max_stocks: int = 20,                # 小于20只股票
                 rebalance_days: int = 5,
                 trading_price: str = "open",         # 开盘价交易
                 enabled: bool = True,
                 weight: float = 0.07,
                 **kwargs):
        """
        初始化控盘策略
        
        Args:
            index_constituent: 指数成分股
            max_chip_concentration: 最大筹码集中度
            sort_by: 排序方式
            max_stocks: 最大股票数量
            rebalance_days: 调仓周期
            trading_price: 交易价格
            enabled: 是否启用
            weight: 策略权重
            **kwargs: 其他参数
        """
        super().__init__(
            name="ChipConcentrationStrategy",
            enabled=enabled,
            weight=weight,
            index_constituent=index_constituent,
            max_chip_concentration=max_chip_concentration,
            sort_by=sort_by,
            max_stocks=max_stocks,
            rebalance_days=rebalance_days,
            trading_price=trading_price,
            **kwargs
        )
        
        # 策略状态
        self.last_rebalance = None
        self.current_holdings = []
        
        logger.info(f"控盘策略初始化: 最大{max_stocks}只, 调仓周期{rebalance_days}天")
    
    def generate_signals(self, market_data: Dict[str, Dict], 
                        fundamental_data: Optional[Dict[str, Dict]] = None,
                        technical_data: Optional[Dict[str, Dict]] = None) -> List[Dict]:
        """
        生成控盘策略交易信号
        
        Args:
            market_data: 市场数据
            fundamental_data: 基本面数据（用于筹码集中度）
            technical_data: 技术指标数据
        
        Returns:
            交易信号列表
        """
        signals = []
        
        if not market_data:
            logger.warning("控盘策略: 缺少市场数据")
            return signals
        
        # 检查是否需要调仓
        if not self._should_rebalance():
            logger.debug("控盘策略: 未到调仓时间，维持当前持仓")
            return self._generate_hold_signals()
        
        # 获取候选股票（中证1000成分股）
        candidate_symbols = self._get_index_constituents(list(market_data.keys()))
        
        if not candidate_symbols:
            logger.warning("控盘策略: 无中证1000成分股")
            return signals
        
        # 如果没有基本面数据，尝试从市场数据获取部分信息
        if fundamental_data is None:
            fundamental_data = self._extract_fundamental_from_market(market_data)
        
        # 筛选股票
        filtered_symbols = self._filter_stocks(candidate_symbols, market_data, fundamental_data)
        
        if not filtered_symbols:
            logger.warning("控盘策略: 筛选后无符合条件股票")
            return signals
        
        # 排序股票（按总市值从小到大）
        sorted_symbols = self._sort_stocks(filtered_symbols, fundamental_data)
        
        # 选择目标持仓（不超过max_stocks）
        target_holdings = sorted_symbols[:self.parameters["max_stocks"]]
        
        # 生成交易信号
        signals = self._generate_rebalance_signals(target_holdings, market_data)
        
        # 更新持仓和调仓时间
        self.current_holdings = target_holdings
        self.last_rebalance = datetime.now()
        
        self.signals_generated += len(signals)
        logger.info(f"控盘策略生成 {len(signals)} 个信号，目标持仓: {target_holdings[:5]}...")
        
        return signals
    
    def _should_rebalance(self) -> bool:
        """检查是否需要调仓"""
        if self.last_rebalance is None:
            return True
        
        rebalance_days = self.parameters.get("rebalance_days", 5)
        days_since_rebalance = (datetime.now() - self.last_rebalance).days
        
        return days_since_rebalance >= rebalance_days
    
    def _get_index_constituents(self, all_symbols: List[str]) -> List[str]:
        """获取指数成分股（模拟）"""
        index_constituent = self.parameters.get("index_constituent", "CSI1000")
        
        # 模拟中证1000成分股：随机选择部分股票
        # 在实际系统中，应从数据源获取真实的成分股列表
        
        if len(all_symbols) <= 10:
            return all_symbols
        
        # 随机选择一部分作为成分股（模拟）
        import random
        num_constituents = min(50, len(all_symbols) // 2)
        constituents = random.sample(all_symbols, num_constituents)
        
        return constituents
    
    def _extract_fundamental_from_market(self, market_data: Dict[str, Dict]) -> Dict[str, Dict]:
        """从市场数据中提取基本面信息"""
        fundamental_data = {}
        
        for symbol, mkt_data in market_data.items():
            # 模拟基本面数据
            fundamental_data[symbol] = {
                "market_cap": mkt_data.get("market_cap", random.uniform(1000000000, 50000000000)),
                "chip_concentration_90": random.uniform(0.05, 0.25),  # 筹码集中度90
                "is_csi1000": random.random() < 0.7  # 70%概率是中证1000成分股
            }
        
        return fundamental_data
    
    def _filter_stocks(self, symbols: List[str], 
                      market_data: Dict[str, Dict],
                      fundamental_data: Dict[str, Dict]) -> List[str]:
        """筛选符合条件的股票"""
        filtered = []
        
        for symbol in symbols:
            if symbol not in market_data or symbol not in fundamental_data:
                continue
            
            fund_data = fundamental_data[symbol]
            
            # 成分股筛选
            if not self._is_index_constituent(symbol, fund_data):
                continue
            
            # 筹码集中度筛选
            chip_concentration = fund_data.get("chip_concentration_90", 1.0)
            if chip_concentration >= self.parameters["max_chip_concentration"]:
                continue
            
            filtered.append(symbol)
        
        return filtered
    
    def _is_index_constituent(self, symbol: str, fund_data: Dict) -> bool:
        """检查是否是指数成分股"""
        index_constituent = self.parameters.get("index_constituent", "CSI1000")
        
        # 从基本面数据获取
        if index_constituent == "CSI1000":
            return fund_data.get("is_csi1000", random.random() < 0.5)
        else:
            # 默认返回True（简化）
            return True
    
    def _sort_stocks(self, symbols: List[str], fundamental_data: Dict[str, Dict]) -> List[str]:
        """排序股票（按总市值从小到大）"""
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
                elif sort_by == "chip_concentration":
                    value = fund_data.get("chip_concentration_90", 1.0)
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
        
        # 确定交易价格
        trading_price = self.parameters.get("trading_price", "open")
        
        # 卖出当前持仓中不在目标持仓的股票
        for symbol in self.current_holdings:
            if symbol not in target_holdings and symbol in market_data:
                price = self._get_trading_price(symbol, market_data, trading_price)
                if price > 0:
                    signal_dict = {
                        "symbol": symbol,
                        "side": "SELL",
                        "price": price,
                        "confidence": 0.7,
                        "reason": "控盘策略调仓卖出",
                        "trading_price": trading_price
                    }
                    signals.append(signal_dict)
        
        # 买入目标持仓中当前未持有的股票
        for symbol in target_holdings:
            if symbol not in self.current_holdings and symbol in market_data:
                price = self._get_trading_price(symbol, market_data, trading_price)
                if price > 0:
                    signal_dict = {
                        "symbol": symbol,
                        "side": "BUY",
                        "price": price,
                        "confidence": 0.7,
                        "reason": "控盘策略调仓买入",
                        "trading_price": trading_price
                    }
                    signals.append(signal_dict)
        
        return signals
    
    def _get_trading_price(self, symbol: str, market_data: Dict[str, Dict], 
                          price_type: str = "open") -> float:
        """获取交易价格"""
        mkt_data = market_data.get(symbol, {})
        
        if price_type == "open":
            # 开盘价
            price = mkt_data.get("open_price", mkt_data.get("price", 0))
        elif price_type == "close":
            # 收盘价
            price = mkt_data.get("close_price", mkt_data.get("price", 0))
        else:
            # 默认使用当前价格
            price = mkt_data.get("price", 0)
        
        return price
    
    def _generate_hold_signals(self) -> List[Dict]:
        """生成持仓信号"""
        signals = []
        
        for symbol in self.current_holdings:
            signal_dict = {
                "symbol": symbol,
                "side": "HOLD",
                "price": 0,
                "confidence": 0.6,
                "reason": "维持控盘策略持仓"
            }
            signals.append(signal_dict)
        
        return signals
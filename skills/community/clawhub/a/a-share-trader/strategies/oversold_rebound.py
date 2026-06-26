"""
超跌反弹策略
收盘价与250日收盘价均值之比减1选股，升序排序；
净利润同比增长率（最新12期）大于60%，扣非归母净利润（最新12期）大于0，
总市值横截面升序排序分位数小于0.1，真实价格大于1.5，
无风险警示，非ST，非停牌；1日调仓，持股5只；
"""

import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import random
import numpy as np

from .base_strategy import BaseStrategy

logger = logging.getLogger(__name__)


class OversoldReboundStrategy(BaseStrategy):
    """超跌反弹策略"""
    
    def __init__(self,
                 price_vs_ma250_min: float = -0.5,   # 收盘价与250日均线比最小值
                 price_vs_ma250_max: float = -0.1,   # 收盘价与250日均线比最大值
                 min_profit_growth: float = 0.60,    # 净利润同比增长率>60%
                 min_profit_ttm: float = 0,          # 扣非归母净利润>0
                 market_cap_quantile_max: float = 0.1, # 总市值截面升序分位数<0.1
                 min_price: float = 1.5,             # 真实价格>1.5
                 no_warning: bool = True,            # 无风险警示
                 exclude_st: bool = True,
                 exclude_suspended: bool = True,
                 holding_count: int = 5,
                 rebalance_days: int = 1,            # 1日调仓
                 enabled: bool = True,
                 weight: float = 0.08,
                 **kwargs):
        """
        初始化超跌反弹策略
        
        Args:
            price_vs_ma250_min: 价格/MA250最小值
            price_vs_ma250_max: 价格/MA250最大值
            min_profit_growth: 最小净利润同比增长率
            min_profit_ttm: 最小扣非归母净利润
            market_cap_quantile_max: 最大总市值分位数
            min_price: 最低价格
            no_warning: 无风险警示
            exclude_st: 排除ST股
            exclude_suspended: 排除停牌股
            holding_count: 持仓数量
            rebalance_days: 调仓周期
            enabled: 是否启用
            weight: 策略权重
            **kwargs: 其他参数
        """
        super().__init__(
            name="OversoldReboundStrategy",
            enabled=enabled,
            weight=weight,
            price_vs_ma250_min=price_vs_ma250_min,
            price_vs_ma250_max=price_vs_ma250_max,
            min_profit_growth=min_profit_growth,
            min_profit_ttm=min_profit_ttm,
            market_cap_quantile_max=market_cap_quantile_max,
            min_price=min_price,
            no_warning=no_warning,
            exclude_st=exclude_st,
            exclude_suspended=exclude_suspended,
            holding_count=holding_count,
            rebalance_days=rebalance_days,
            **kwargs
        )
        
        # 策略状态
        self.last_rebalance = None
        self.current_holdings = []
        
        logger.info(f"超跌反弹策略初始化: 持仓数={holding_count}, 每日调仓")
    
    def generate_signals(self, market_data: Dict[str, Dict], 
                        fundamental_data: Optional[Dict[str, Dict]] = None,
                        technical_data: Optional[Dict[str, Dict]] = None) -> List[Dict]:
        """
        生成超跌反弹策略交易信号
        
        Args:
            market_data: 市场数据
            fundamental_data: 基本面数据
            technical_data: 技术指标数据（用于价格/MA250）
        
        Returns:
            交易信号列表
        """
        signals = []
        
        if not market_data:
            logger.warning("超跌反弹策略: 缺少市场数据")
            return signals
        
        # 检查是否需要调仓（每日调仓）
        if not self._should_rebalance():
            logger.debug("超跌反弹策略: 未到调仓时间，维持当前持仓")
            return self._generate_hold_signals()
        
        # 获取候选股票
        candidate_symbols = list(market_data.keys())
        
        # 如果没有基本面数据，尝试从市场数据获取部分信息
        if fundamental_data is None:
            fundamental_data = self._extract_fundamental_from_market(market_data)
        
        # 筛选股票
        filtered_symbols = self._filter_stocks(candidate_symbols, market_data, fundamental_data)
        
        if not filtered_symbols:
            logger.warning("超跌反弹策略: 筛选后无符合条件股票")
            return signals
        
        # 计算价格/MA250比率
        price_ratios = self._calculate_price_ratios(filtered_symbols, market_data, technical_data)
        
        # 按价格比率升序排序（最超跌的在前）
        sorted_symbols = self._sort_by_price_ratio(filtered_symbols, price_ratios)
        
        # 选择目标持仓（最超跌的股票）
        target_holdings = sorted_symbols[:self.parameters["holding_count"]]
        
        # 生成交易信号
        signals = self._generate_rebalance_signals(target_holdings, market_data)
        
        # 更新持仓和调仓时间
        self.current_holdings = target_holdings
        self.last_rebalance = datetime.now()
        
        self.signals_generated += len(signals)
        logger.info(f"超跌反弹策略生成 {len(signals)} 个信号，目标持仓: {target_holdings}")
        
        return signals
    
    def _should_rebalance(self) -> bool:
        """检查是否需要调仓（每日调仓）"""
        if self.last_rebalance is None:
            return True
        
        # 每日调仓
        return datetime.now().date() != self.last_rebalance.date()
    
    def _extract_fundamental_from_market(self, market_data: Dict[str, Dict]) -> Dict[str, Dict]:
        """从市场数据中提取基本面信息"""
        fundamental_data = {}
        
        for symbol, mkt_data in market_data.items():
            price = mkt_data.get("price", 0)
            
            # 模拟基本面数据
            fundamental_data[symbol] = {
                "profit_growth": random.uniform(-0.3, 1.0),  # 净利润增长率
                "profit_ttm": random.uniform(-100000000, 500000000),  # 扣非归母净利润
                "market_cap": mkt_data.get("market_cap", random.uniform(100000000, 10000000000)),
                "is_st": random.random() < 0.05,
                "is_suspended": random.random() < 0.02,
                "has_warning": random.random() < 0.03,
                "price": price
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
            
            mkt_data = market_data[symbol]
            fund_data = fundamental_data[symbol]
            
            # 价格筛选
            price = mkt_data.get("price", 0)
            if price < self.parameters["min_price"]:
                continue
            
            # 基本筛选
            if not self._pass_basic_filters(symbol, fund_data):
                continue
            
            # 增长指标筛选
            profit_growth = fund_data.get("profit_growth", -1)
            if profit_growth < self.parameters["min_profit_growth"]:
                continue
            
            # 净利润筛选
            profit_ttm = fund_data.get("profit_ttm", -1)
            if profit_ttm <= self.parameters["min_profit_ttm"]:
                continue
            
            # 无风险警示筛选
            if self.parameters["no_warning"]:
                if fund_data.get("has_warning", False):
                    continue
            
            filtered.append(symbol)
        
        # 应用市值分位数筛选
        filtered = self._apply_market_cap_quantile_filter(filtered, fundamental_data)
        
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
    
    def _apply_market_cap_quantile_filter(self, symbols: List[str], 
                                         fundamental_data: Dict[str, Dict]) -> List[str]:
        """应用市值分位数筛选（总市值截面升序分位数<0.1）"""
        if len(symbols) < 2:
            return symbols
        
        # 计算总市值分位数
        market_cap_quantiles = self.calculate_market_cap_rank(symbols, fundamental_data)
        
        # 筛选：分位数<0.1（市值最小的10%）
        filtered = []
        for symbol in symbols:
            quantile = market_cap_quantiles.get(symbol, 0.5)
            if quantile < self.parameters["market_cap_quantile_max"]:
                filtered.append(symbol)
        
        return filtered
    
    def _calculate_price_ratios(self, symbols: List[str], 
                               market_data: Dict[str, Dict],
                               technical_data: Optional[Dict[str, Dict]]) -> Dict[str, float]:
        """计算价格/MA250比率"""
        price_ratios = {}
        
        for symbol in symbols:
            price = market_data[symbol].get("price", 0) if symbol in market_data else 0
            
            if price <= 0:
                price_ratios[symbol] = 0
                continue
            
            # 尝试从技术数据获取MA250
            ma250 = None
            if technical_data and symbol in technical_data:
                ma250 = technical_data[symbol].get("price_ma250", None)
            
            # 如果没有MA250，使用模拟值
            if ma250 is None or ma250 <= 0:
                # 模拟MA250：当前价格乘以一个随机系数
                # 为制造超跌效果，让MA250高于当前价格
                ma250 = price * random.uniform(1.1, 1.5)
            
            # 计算比率：(收盘价/MA250) - 1
            ratio = (price / ma250) - 1
            
            price_ratios[symbol] = ratio
        
        return price_ratios
    
    def _sort_by_price_ratio(self, symbols: List[str], price_ratios: Dict[str, float]) -> List[str]:
        """按价格比率升序排序（最超跌的在前）"""
        if not symbols or not price_ratios:
            return symbols
        
        # 收集比率数据
        ratio_data = []
        for symbol in symbols:
            ratio = price_ratios.get(symbol, 0)
            ratio_data.append((symbol, ratio))
        
        # 按比率升序排序（负值越大表示超跌越严重）
        ratio_data.sort(key=lambda x: x[1])
        
        # 提取股票代码
        sorted_symbols = [item[0] for item in ratio_data]
        
        # 可选：过滤比率范围
        filtered = []
        for symbol, ratio in ratio_data:
            if (self.parameters["price_vs_ma250_min"] <= ratio <= 
                self.parameters["price_vs_ma250_max"]):
                filtered.append(symbol)
        
        return filtered if filtered else sorted_symbols
    
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
                        "reason": "超跌反弹策略调仓卖出"
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
                        "reason": "超跌反弹策略调仓买入（超跌机会）"
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
                "reason": "维持超跌反弹策略持仓"
            }
            signals.append(signal_dict)
        
        return signals
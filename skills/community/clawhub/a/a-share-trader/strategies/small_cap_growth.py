"""
小市值成长策略
上交所/深交所/北交所主板个股，非ST、非停牌；
过滤上市天数>365天、PE_TTM>0、流通市值≤25亿元的个股；
以（流通市值截面排名×0.5 + 收盘价截面排名×0.3 + (-每股收益同比增长率最新报告期)截面排名×0.2）之和为评分字段升序选前10只，等权持仓；
每3个交易日调仓
"""

import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import random
import numpy as np

from .base_strategy import BaseStrategy

logger = logging.getLogger(__name__)


class SmallCapGrowthStrategy(BaseStrategy):
    """小市值成长策略"""
    
    def __init__(self,
                 max_market_cap: float = 2500000000,  # 流通市值≤25亿
                 min_listing_days: int = 365,         # 上市>365天
                 min_pe_ttm: float = 0.1,             # PE_TTM>0
                 exclude_st: bool = True,
                 exclude_suspended: bool = True,
                 board_filter: List[str] = None,      # 主板个股
                 scoring_weights: Dict[str, float] = None, # 评分权重
                 holding_count: int = 10,
                 rebalance_days: int = 3,
                 enabled: bool = True,
                 weight: float = 0.08,
                 **kwargs):
        """
        初始化小市值成长策略
        
        Args:
            max_market_cap: 最大流通市值
            min_listing_days: 最小上市天数
            min_pe_ttm: 最小PE_TTM
            exclude_st: 排除ST股
            exclude_suspended: 排除停牌股
            board_filter: 板块过滤
            scoring_weights: 评分权重
            holding_count: 持仓数量
            rebalance_days: 调仓周期
            enabled: 是否启用
            weight: 策略权重
            **kwargs: 其他参数
        """
        # 默认评分权重
        if scoring_weights is None:
            scoring_weights = {
                "market_cap_rank": 0.5,      # 流通市值截面排名
                "price_rank": 0.3,           # 收盘价截面排名
                "eps_growth_rank": 0.2       # (-每股收益同比增长率)截面排名
            }
        
        if board_filter is None:
            board_filter = ["main"]  # 主板
        
        super().__init__(
            name="SmallCapGrowthStrategy",
            enabled=enabled,
            weight=weight,
            max_market_cap=max_market_cap,
            min_listing_days=min_listing_days,
            min_pe_ttm=min_pe_ttm,
            exclude_st=exclude_st,
            exclude_suspended=exclude_suspended,
            board_filter=board_filter,
            scoring_weights=scoring_weights,
            holding_count=holding_count,
            rebalance_days=rebalance_days,
            **kwargs
        )
        
        # 策略状态
        self.last_rebalance = None
        self.current_holdings = []
        
        logger.info(f"小市值成长策略初始化: 持仓数={holding_count}, 调仓周期={rebalance_days}天")
    
    def generate_signals(self, market_data: Dict[str, Dict], 
                        fundamental_data: Optional[Dict[str, Dict]] = None,
                        technical_data: Optional[Dict[str, Dict]] = None) -> List[Dict]:
        """
        生成小市值成长策略交易信号
        
        Args:
            market_data: 市场数据
            fundamental_data: 基本面数据
            technical_data: 技术指标数据（本策略不使用）
        
        Returns:
            交易信号列表
        """
        signals = []
        
        if not market_data:
            logger.warning("小市值成长策略: 缺少市场数据")
            return signals
        
        # 检查是否需要调仓
        if not self._should_rebalance():
            logger.debug("小市值成长策略: 未到调仓时间，维持当前持仓")
            return self._generate_hold_signals()
        
        # 如果没有基本面数据，尝试从市场数据获取部分信息
        if fundamental_data is None:
            fundamental_data = self._extract_fundamental_from_market(market_data)
        
        # 获取候选股票
        candidate_symbols = list(market_data.keys())
        
        # 筛选股票
        filtered_symbols = self._filter_stocks(candidate_symbols, market_data, fundamental_data)
        
        if not filtered_symbols:
            logger.warning("小市值成长策略: 筛选后无符合条件股票")
            return signals
        
        # 计算综合评分
        scores = self._calculate_composite_scores(filtered_symbols, market_data, fundamental_data)
        
        # 按评分升序排序（得分越低越好）
        sorted_symbols = self._sort_by_score(filtered_symbols, scores)
        
        # 选择目标持仓
        target_holdings = sorted_symbols[:self.parameters["holding_count"]]
        
        # 生成交易信号
        signals = self._generate_rebalance_signals(target_holdings, market_data)
        
        # 更新持仓和调仓时间
        self.current_holdings = target_holdings
        self.last_rebalance = datetime.now()
        
        self.signals_generated += len(signals)
        logger.info(f"小市值成长策略生成 {len(signals)} 个信号，目标持仓: {target_holdings}")
        
        return signals
    
    def _should_rebalance(self) -> bool:
        """检查是否需要调仓"""
        if self.last_rebalance is None:
            return True
        
        rebalance_days = self.parameters.get("rebalance_days", 3)
        days_since_rebalance = (datetime.now() - self.last_rebalance).days
        
        return days_since_rebalance >= rebalance_days
    
    def _extract_fundamental_from_market(self, market_data: Dict[str, Dict]) -> Dict[str, Dict]:
        """从市场数据中提取基本面信息"""
        fundamental_data = {}
        
        for symbol, mkt_data in market_data.items():
            price = mkt_data.get("price", 0)
            
            # 模拟基本面数据
            fundamental_data[symbol] = {
                "market_cap": mkt_data.get("market_cap", random.uniform(100000000, 50000000000)),
                "pe": random.uniform(5.0, 60.0),
                "eps_growth": random.uniform(-0.5, 1.0),  # 每股收益同比增长率
                "listing_days": random.randint(100, 5000),
                "is_st": random.random() < 0.05,
                "is_suspended": random.random() < 0.02
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
            
            # 基本筛选
            if not self._pass_basic_filters(symbol, fund_data):
                continue
            
            # 市值筛选
            market_cap = fund_data.get("market_cap", 0)
            if market_cap > self.parameters["max_market_cap"]:
                continue
            
            # 上市天数筛选
            listing_days = fund_data.get("listing_days", 0)
            if listing_days < self.parameters["min_listing_days"]:
                continue
            
            # PE筛选
            pe = fund_data.get("pe", 0)
            if pe <= self.parameters["min_pe_ttm"]:
                continue
            
            # 板块筛选
            if not self._pass_board_filter(symbol, fund_data):
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
    
    def _pass_board_filter(self, symbol: str, fund_data: Dict) -> bool:
        """通过板块筛选"""
        board_filter = self.parameters.get("board_filter", ["main"])
        
        if not board_filter:
            return True
        
        # 简化实现：检查股票代码前缀
        if "main" in board_filter:
            # 主板：非科创板、非创业板
            if symbol.startswith("688") or symbol.startswith("300"):
                return False
        
        return True
    
    def _calculate_composite_scores(self, symbols: List[str],
                                   market_data: Dict[str, Dict],
                                   fundamental_data: Dict[str, Dict]) -> Dict[str, float]:
        """计算综合评分"""
        if len(symbols) < 2:
            return {symbol: 0.5 for symbol in symbols}
        
        # 获取各项数据
        market_caps = []
        prices = []
        eps_growths = []
        
        for symbol in symbols:
            market_cap = fundamental_data[symbol].get("market_cap", 0)
            price = market_data[symbol].get("price", 0)
            eps_growth = fundamental_data[symbol].get("eps_growth", 0)
            
            market_caps.append(market_cap)
            prices.append(price)
            eps_growths.append(-eps_growth)  # 负号：-每股收益同比增长率
        
        # 计算截面排名（0-1，越小表示排名越靠前）
        market_cap_ranks = self._calculate_ranks(market_caps, ascending=True)  # 市值越小越好
        price_ranks = self._calculate_ranks(prices, ascending=True)  # 价格越低越好
        eps_growth_ranks = self._calculate_ranks(eps_growths, ascending=True)  # -增长率越小越好
        
        # 计算综合评分
        scoring_weights = self.parameters["scoring_weights"]
        scores = {}
        
        for i, symbol in enumerate(symbols):
            score = (
                market_cap_ranks[i] * scoring_weights.get("market_cap_rank", 0.5) +
                price_ranks[i] * scoring_weights.get("price_rank", 0.3) +
                eps_growth_ranks[i] * scoring_weights.get("eps_growth_rank", 0.2)
            )
            scores[symbol] = score
        
        return scores
    
    def _calculate_ranks(self, values: List[float], ascending: bool = True) -> List[float]:
        """计算截面排名（0-1）"""
        if not values:
            return []
        
        # 转换为numpy数组
        arr = np.array(values)
        
        # 计算排名
        if ascending:
            # 升序：值越小排名越靠前
            ranks = np.argsort(np.argsort(arr))
        else:
            # 降序：值越大排名越靠前
            ranks = np.argsort(np.argsort(-arr))
        
        # 归一化到0-1
        normalized_ranks = ranks / (len(ranks) - 1) if len(ranks) > 1 else np.array([0.5])
        
        return normalized_ranks.tolist()
    
    def _sort_by_score(self, symbols: List[str], scores: Dict[str, float]) -> List[str]:
        """按评分升序排序（得分越低越好）"""
        if not symbols or not scores:
            return symbols
        
        # 收集评分数据
        score_data = []
        for symbol in symbols:
            score = scores.get(symbol, 0.5)
            score_data.append((symbol, score))
        
        # 按评分升序排序
        score_data.sort(key=lambda x: x[1])
        
        # 提取股票代码
        sorted_symbols = [item[0] for item in score_data]
        
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
                        "reason": "小市值成长策略调仓卖出"
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
                        "reason": "小市值成长策略调仓买入"
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
                "reason": "维持小市值成长策略持仓"
            }
            signals.append(signal_dict)
        
        return signals
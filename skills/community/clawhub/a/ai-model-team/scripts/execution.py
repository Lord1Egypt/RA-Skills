"""
Execution Optimizer
P2: Smart order type selection, order splitting, cancellation/retry
"""
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import numpy as np

# ============ Configuration ============
ORDER_TYPE_DEFAULT = "limit"
MAX_ORDER_SPLITS = 3
PARTIAL_FILL_THRESHOLD = 0.5  # 50% fill threshold


class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    POST_ONLY = "post_only"
    FOK = "fok"  # Fill or Kill
    IOC = "ioc"  # Immediate or Cancel


@dataclass
class OrderSpec:
    """订单规格"""
    symbol: str
    side: str  # buy/sell
    quantity: float
    price: float  # limit price (None for market)
    order_type: OrderType = OrderType.LIMIT
    splits: int = 1
    time_limit: int = 30  # seconds


@dataclass
class OrderResult:
    """订单执行结果"""
    order_id: str
    status: str  # filled/partial/cancelled/rejected
    filled_qty: float
    remaining_qty: float
    avg_fill_price: float
    fill_ratio: float
    execution_time_ms: float
    splits_used: int
    slippage_bps: float
    attempts: int


class LiquidityAnalyzer:
    """流动性分析器"""
    
    @staticmethod
    def estimate_slippage(
        price: float,
        quantity: float,
        orderbook_depth: Dict,
        side: str
    ) -> float:
        """
        估算滑点
        
        Args:
            price: 期望价格
            quantity: 数量
            orderbook_depth: 订单簿深度 {price: qty}
            side: buy/sell
        """
        bids = orderbook_depth.get("bids", [])
        asks = orderbook_depth.get("asks", [])
        
        if side == "buy":
            levels = asks  # 买入看卖方
        else:
            levels = bids  # 卖出看买方
        
        if not levels:
            return 0
        
        total_cost = 0
        remaining = quantity
        expected_cost = price * quantity
        
        for level_price, level_qty in levels:
            if remaining <= 0:
                break
            fill_qty = min(remaining, level_qty)
            total_cost += fill_qty * level_price
            remaining -= fill_qty
        
        if expected_cost > 0:
            slippage = abs(total_cost - expected_cost) / expected_cost
            return slippage * 10000  # BPS
        
        return 0


class SmartOrderRouter:
    """智能订单路由"""
    
    def __init__(self, max_splits: int = MAX_ORDER_SPLITS):
        self.max_splits = max_splits
    
    def determine_optimal_splits(
        self,
        quantity: float,
        orderbook_depth: Dict,
        side: str,
        urgency: str = "normal"  # low/normal/high
    ) -> Tuple[int, List[float]]:
        """
        确定最优拆分数量和每单大小
        
        Returns:
            (num_splits, split_quantities)
        """
        bids = orderbook_depth.get("bids", [])
        asks = orderbook_depth.get("asks", [])
        levels = asks if side == "buy" else bids
        
        if not levels:
            return 1, [quantity]
        
        # 计算订单簿流动性
        total_liquidity = sum(qty for _, qty in levels[:10])
        
        # 数量占比
        quantity_ratio = quantity / total_liquidity if total_liquidity > 0 else 1
        
        # 根据紧急度和流动性确定拆分
        if urgency == "high":
            # 高紧急：减少拆分，快速成交
            num_splits = 1
        elif urgency == "low":
            # 低紧急：增加拆分，减少冲击
            num_splits = min(self.max_splits, max(2, int(1 / quantity_ratio) if quantity_ratio > 0 else 3))
        else:
            num_splits = min(self.max_splits, max(2, int(0.5 / quantity_ratio) if quantity_ratio > 0 else 2))
        
        num_splits = max(1, min(num_splits, self.max_splits))
        
        # 平均分配
        split_qty = quantity / num_splits
        split_quantities = [split_qty] * (num_splits - 1) + [quantity - split_qty * (num_splits - 1)]
        
        return num_splits, split_quantities
    
    def select_order_type(
        self,
        price: float,
        quantity: float,
        orderbook_depth: Dict,
        side: str,
        urgency: str = "normal"
    ) -> OrderType:
        """
        选择最优订单类型
        
        Logic:
        - 高流动性 + 低紧急: LIMIT/POST_ONLY
        - 低流动性 + 高紧急: MARKET
        - 需要全部成交: FOK
        - 部分成交可接受: IOC
        """
        bids = orderbook_depth.get("bids", [])
        asks = orderbook_depth.get("asks", [])
        levels = asks if side == "buy" else bids
        
        if not levels:
            return OrderType.MARKET
        
        # 计算深度
        depth_10 = sum(qty for _, qty in levels[:10])
        depth_ratio = quantity / depth_10 if depth_10 > 0 else 1
        
        # 估算滑点
        slippage_bps = LiquidityAnalyzer.estimate_slippage(
            price, quantity, orderbook_depth, side
        )
        
        # 选择逻辑
        if urgency == "high" or depth_ratio > 0.5:
            # 高紧急或大单：市价
            return OrderType.MARKET
        elif urgency == "low" and depth_ratio < 0.1 and slippage_bps < 5:
            # 低紧急、小单、流动性好：只挂单（手续费低）
            return OrderType.POST_ONLY
        elif slippage_bps > 20:
            # 滑点太大：市价确保成交
            return OrderType.MARKET
        else:
            # 正常情况：限价单
            return OrderType.LIMIT


class ExecutionOptimizer:
    """执行优化器"""
    
    def __init__(
        self,
        max_splits: int = MAX_ORDER_SPLITS,
        timeout: int = 30
    ):
        self.router = SmartOrderRouter(max_splits)
        self.timeout = timeout
        self.max_retries = 3
    
    def execute_smart(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: float,
        orderbook_depth: Dict,
        urgency: str = "normal"
    ) -> OrderResult:
        """
        智能执行订单
        
        Steps:
        1. 分析流动性，确定拆分数量
        2. 选择订单类型
        3. 分批执行
        4. 监控完成率
        5. 处理未成交部分
        """
        start_time = time.time()
        
        # Step 1: 确定拆分
        num_splits, split_quantities = self.router.determine_optimal_splits(
            quantity, orderbook_depth, side, urgency
        )
        
        # Step 2: 选择订单类型
        order_type = self.router.select_order_type(
            price, quantity, orderbook_depth, side, urgency
        )
        
        # Step 3: 执行
        total_filled = 0
        total_cost = 0
        attempts = 0
        splits_used = 0
        
        for i, qty in enumerate(split_quantities):
            if total_filled >= quantity * PARTIAL_FILL_THRESHOLD:
                break
            
            # 模拟下单（实际需要接入交易所API）
            fill_result = self._submit_order(
                symbol, side, qty, price, order_type
            )
            
            attempts += 1
            splits_used += 1
            
            if fill_result["filled"]:
                total_filled += fill_result["qty"]
                total_cost += fill_result["qty"] * fill_result["price"]
        
        # Step 4: 计算结果
        avg_price = total_cost / total_filled if total_filled > 0 else price
        execution_time = (time.time() - start_time) * 1000
        
        # 滑点计算
        slippage_bps = abs(avg_price - price) / price * 10000
        
        return OrderResult(
            order_id=f"exec_{int(time.time())}",
            status="filled" if total_filled >= quantity * 0.9 else "partial",
            filled_qty=total_filled,
            remaining_qty=quantity - total_filled,
            avg_fill_price=avg_price,
            fill_ratio=total_filled / quantity if quantity > 0 else 0,
            execution_time_ms=execution_time,
            splits_used=splits_used,
            slippage_bps=slippage_bps,
            attempts=attempts
        )
    
    def _submit_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: float,
        order_type: OrderType
    ) -> Dict:
        """
        提交订单（实际需要接入交易所API）
        
        这里是模拟实现
        """
        # 模拟订单执行
        import random
        filled = random.random() > 0.1  # 90% 成交率
        fill_price = price * (1 + random.uniform(-0.001, 0.001))  # ±0.1% 滑点
        
        return {
            "filled": filled,
            "qty": quantity if filled else 0,
            "price": fill_price if filled else price
        }
    
    def retry_unfilled(
        self,
        original_order: OrderResult,
        symbol: str,
        side: str,
        remaining_qty: float,
        price: float,
        orderbook_depth: Dict,
        max_attempts: int = None
    ) -> OrderResult:
        """重试未成交部分"""
        max_attempts = max_attempts or self.max_retries
        
        total_filled = original_order.filled_qty
        total_cost = original_order.avg_fill_price * total_filled
        attempts = original_order.attempts
        splits_used = original_order.splits_used
        
        for _ in range(max_attempts):
            if remaining_qty <= 0:
                break
            
            # 放宽价格一点
            adjusted_price = price * 1.001 if side == "buy" else price * 0.999
            
            result = self._submit_order(
                symbol, side, remaining_qty, adjusted_price, OrderType.MARKET
            )
            
            attempts += 1
            
            if result["filled"]:
                total_filled += result["qty"]
                total_cost += result["qty"] * result["price"]
                remaining_qty -= result["qty"]
                splits_used += 1
        
        avg_price = total_cost / total_filled if total_filled > 0 else price
        
        return OrderResult(
            order_id=f"retry_{int(time.time())}",
            status="filled" if remaining_qty <= 0 else "partial",
            filled_qty=total_filled,
            remaining_qty=remaining_qty,
            avg_fill_price=avg_price,
            fill_ratio=total_filled / (total_filled + remaining_qty) if (total_filled + remaining_qty) > 0 else 0,
            execution_time_ms=0,
            splits_used=splits_used,
            slippage_bps=abs(avg_price - price) / price * 10000,
            attempts=attempts
        )


def estimate_execution_cost(
    price: float,
    quantity: float,
    orderbook_depth: Dict,
    side: str,
    fee_bps: float = 10
) -> Dict:
    """
    估算执行成本
    
    Returns:
        dict with fee, slippage, market_impact, total_cost
    """
    # 手续费
    notional = price * quantity
    fee = notional * fee_bps / 10000
    
    # 滑点
    slippage_bps = LiquidityAnalyzer.estimate_slippage(
        price, quantity, orderbook_depth, side
    )
    slippage = notional * slippage_bps / 10000
    
    # 市场冲击（简化估算）
    impact_factor = 0.1  # 假设 10% 的滑点转化为冲击
    market_impact = slippage * impact_factor
    
    total_cost = fee + slippage + market_impact
    
    return {
        "fee_usd": fee,
        "slippage_bps": slippage_bps,
        "slippage_usd": slippage,
        "market_impact_usd": market_impact,
        "total_cost_usd": total_cost,
        "cost_ratio": total_cost / notional if notional > 0 else 0
    }

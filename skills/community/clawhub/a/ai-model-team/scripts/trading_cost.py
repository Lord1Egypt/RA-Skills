"""
Trading Cost Model
P1: Fee, slippage, and market impact modeling
"""
from dataclasses import dataclass
from typing import Dict, Optional
import numpy as np

# ============ Configuration ============
SLIPPAGE_BPS = 8  # 8 basis points default
FEE_BPS = 10  # 10 basis points (0.1%)

# Liquidity tiers (by daily volume)
LIQUIDITY_TIERS = {
    "high": {  # > $10M daily volume
        "slippage_bps": 5,
        "impact_factor": 0.1
    },
    "medium": {  # $1M - $10M
        "slippage_bps": 10,
        "impact_factor": 0.2
    },
    "low": {  # < $1M
        "slippage_bps": 20,
        "impact_factor": 0.4
    }
}


@dataclass
class TradeCostEstimate:
    """交易成本估算"""
    gross_pnl: float
    fee: float
    slippage: float
    market_impact: float
    net_pnl: float
    cost_ratio: float  # total_cost / gross_pnl
    details: Dict


class TradingCostModel:
    """交易成本模型"""
    
    def __init__(
        self,
        fee_bps: float = FEE_BPS,
        slippage_bps: float = SLIPPAGE_BPS,
        default_tier: str = "medium"
    ):
        self.fee_bps = fee_bps
        self.slippage_bps = slippage_bps
        self.default_tier = default_tier
    
    def estimate_cost(
        self,
        price: float,
        quantity: float,
        side: str,  # "buy" or "sell"
        liquidity_tier: str = None
    ) -> TradeCostEstimate:
        """
        估算交易成本
        
        Args:
            price: 执行价格
            quantity: 数量
            side: 买卖方向
            liquidity_tier: 流动性层级 (high/medium/low)
        """
        tier = liquidity_tier or self.default_tier
        tier_config = LIQUIDITY_TIERS.get(tier, LIQUIDITY_TIERS["medium"])
        
        notional = price * quantity
        
        # 手续费 (双向收取)
        fee = notional * (self.fee_bps / 10000) * 2  # 开仓+平仓
        
        # 滑点
        slippage_bps = tier_config["slippage_bps"]
        slippage = notional * (slippage_bps / 10000)
        
        # 市场冲击成本
        impact_factor = tier_config["impact_factor"]
        # 冲击成本 = 数量占比 × 流动性系数 × 价格
        market_impact = notional * impact_factor * 0.001  # 简化模型
        
        total_cost = fee + slippage + market_impact
        cost_ratio = total_cost / notional if notional > 0 else 0
        
        return TradeCostEstimate(
            gross_pnl=0,  # 待填
            fee=fee,
            slippage=slippage,
            market_impact=market_impact,
            net_pnl=-total_cost,  # 初始为负成本
            cost_ratio=cost_ratio,
            details={
                "notional": notional,
                "fee_bps": self.fee_bps,
                "slippage_bps": slippage_bps,
                "liquidity_tier": tier,
                "total_cost_usd": total_cost
            }
        )
    
    def apply_costs_to_pnl(
        self,
        gross_pnl: float,
        price: float,
        quantity: float,
        side: str,
        liquidity_tier: str = None
    ) -> TradeCostEstimate:
        """将成本应用到 PnL 计算"""
        cost = self.estimate_cost(price, quantity, side, liquidity_tier)
        cost.gross_pnl = gross_pnl
        cost.net_pnl = gross_pnl - cost.fee - cost.slippage - cost.market_impact
        return cost
    
    def is_profitable_after_costs(
        self,
        expected_pnl_pct: float,
        liquidity_tier: str = None
    ) -> bool:
        """检查扣除成本后是否仍有盈利"""
        tier = liquidity_tier or self.default_tier
        tier_config = LIQUIDITY_TIERS.get(tier, LIQUIDITY_TIERS["medium"])
        
        total_cost_bps = (
            self.fee_bps * 2 +  # 开仓+平仓
            tier_config["slippage_bps"] +
            tier_config["impact_factor"] * 100  # 转换为 bps
        )
        
        # 需要预期收益大于成本
        return expected_pnl_pct * 10000 > total_cost_bps


class LiquidityClassifier:
    """流动性分类器"""
    
    @staticmethod
    def classify(
        daily_volume_usd: float,
        num_trades: int = 0
    ) -> str:
        """
        根据交易量分类流动性
        
        Args:
            daily_volume_usd: 日交易量（美元）
            num_trades: 日交易次数
        """
        if daily_volume_usd > 10_000_000:  # > $10M
            return "high"
        elif daily_volume_usd > 1_000_000:  # > $1M
            return "medium"
        else:
            return "low"
    
    @staticmethod
    def get_slippage_for_tier(tier: str) -> int:
        """获取对应层级的滑点"""
        return LIQUIDITY_TIERS.get(tier, LIQUIDITY_TIERS["medium"])["slippage_bps"]


def estimate_net_pnl(
    entry_price: float,
    exit_price: float,
    quantity: float,
    side: str,
    fee_bps: float = FEE_BPS,
    liquidity_tier: str = "medium"
) -> TradeCostEstimate:
    """
    便捷函数：估算净盈亏（含手续费）
    """
    cost_model = TradingCostModel(fee_bps=fee_bps)
    
    # 计算gross PnL
    if side == "long":
        gross_pnl = (exit_price - entry_price) * quantity
    else:  # short
        gross_pnl = (entry_price - exit_price) * quantity
    
    # 计算成本
    avg_price = (entry_price + exit_price) / 2
    return cost_model.apply_costs_to_pnl(
        gross_pnl=gross_pnl,
        price=avg_price,
        quantity=quantity,
        side=side,
        liquidity_tier=liquidity_tier
    )

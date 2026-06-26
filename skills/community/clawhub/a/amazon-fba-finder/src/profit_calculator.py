"""
利润计算器模块
精确计算 Amazon FBA 产品的各项成本和利润
"""

from typing import Dict, Optional
from dataclasses import dataclass
from enum import Enum


class FBAFeeTier(Enum):
    SMALL_STANDARD = "small_standard"
    LARGE_STANDARD = "large_standard"
    SMALL_OVERSIZE = "small_oversize"
    MEDIUM_OVERSIZE = "medium_oversize"
    LARGE_OVERSIZE = "large_oversize"


@dataclass
class ProductDimensions:
    """产品尺寸信息"""
    length: float  # inches
    width: float
    height: float
    weight: float  # pounds


@dataclass
class CostBreakdown:
    """成本明细"""
    product_cost: float  # 产品采购成本
    shipping_to_amazon: float  # 头程运费
    fba_fee: float  # FBA 配送费
    referral_fee: float  # 佣金（通常 15%）
    storage_fee: float  # 仓储费
    advertising_cost: float  # 广告费
    other_costs: float  # 其他费用
    total_cost: float


@dataclass
class ProfitAnalysis:
    """利润分析结果"""
    selling_price: float
    total_costs: CostBreakdown
    net_profit: float
    profit_margin: float  # 利润率 %
    roi: float  # 投资回报率 %
    breakeven_units: int  # 盈亏平衡点
    monthly_profit_estimate: float
    recommendation: str


class ProfitCalculator:
    """FBA 利润计算器"""
    
    # 2024 年 FBA 配送费标准（美国站）
    FBA_FEES = {
        FBAFeeTier.SMALL_STANDARD: 3.22,
        FBAFeeTier.LARGE_STANDARD: 4.75,
        FBAFeeTier.SMALL_OVERSIZE: 9.73,
        FBAFeeTier.MEDIUM_OVERSIZE: 15.37,
        FBAFeeTier.LARGE_OVERSIZE: 25.21
    }
    
    # 平均佣金率
    REFERRAL_RATE = 0.15
    
    # 月度仓储费（每立方英尺）
    STORAGE_FEES = {
        "jan_sep": 0.87,
        "oct_dec": 2.65
    }
    
    def __init__(self, marketplace: str = "US"):
        self.marketplace = marketplace
    
    def calculate_profit(self,
                        selling_price: float,
                        product_cost: float,
                        dimensions: ProductDimensions,
                        shipping_cost: float = 0,
                        advertising_pct: float = 0.10,
                        monthly_sales: int = 300) -> ProfitAnalysis:
        """
        计算产品利润
        
        Args:
            selling_price: 售价
            product_cost: 产品采购成本（含到岸成本）
            dimensions: 产品尺寸
            shipping_cost: 头程运费（单件）
            advertising_pct: 广告费占比
            monthly_sales: 预估月销量
            
        Returns:
            利润分析结果
        """
        # 计算 FBA 配送费
        fba_fee = self._calculate_fba_fee(dimensions)
        
        # 计算佣金
        referral_fee = selling_price * self.REFERRAL_RATE
        
        # 计算仓储费
        storage_fee = self._calculate_storage_fee(dimensions)
        
        # 计算广告费
        advertising_cost = selling_price * advertising_pct
        
        # 其他成本（退货、损耗等）
        other_costs = selling_price * 0.03
        
        # 总成本
        total_cost = CostBreakdown(
            product_cost=product_cost,
            shipping_to_amazon=shipping_cost,
            fba_fee=fba_fee,
            referral_fee=referral_fee,
            storage_fee=storage_fee,
            advertising_cost=advertising_cost,
            other_costs=other_costs,
            total_cost=(
                product_cost + shipping_cost + fba_fee +
                referral_fee + storage_fee + advertising_cost + other_costs
            )
        )
        
        # 净利润
        net_profit = selling_price - total_cost.total_cost
        
        # 利润率
        profit_margin = (net_profit / selling_price) * 100 if selling_price > 0 else 0
        
        # ROI
        investment = product_cost + shipping_cost
        roi = (net_profit / investment) * 100 if investment > 0 else 0
        
        # 盈亏平衡点（固定成本 / 单件利润）
        fixed_costs = 0  # 简化计算
        breakeven_units = int(fixed_costs / net_profit) + 1 if net_profit > 0 else 999999
        
        # 月利润预估
        monthly_profit = net_profit * monthly_sales
        
        # 推荐建议
        recommendation = self._generate_recommendation(
            profit_margin, roi, net_profit, monthly_sales
        )
        
        return ProfitAnalysis(
            selling_price=selling_price,
            total_costs=total_cost,
            net_profit=round(net_profit, 2),
            profit_margin=round(profit_margin, 2),
            roi=round(roi, 2),
            breakeven_units=breakeven_units,
            monthly_profit_estimate=round(monthly_profit, 2),
            recommendation=recommendation
        )
    
    def _calculate_fba_fee(self, dimensions: ProductDimensions) -> float:
        """计算 FBA 配送费"""
        tier = self._determine_size_tier(dimensions)
        base_fee = self.FBA_FEES.get(tier, 4.75)
        
        # 重量附加费
        if dimensions.weight > 1:
            weight_surcharge = (dimensions.weight - 1) * 0.40
            base_fee += weight_surcharge
        
        return round(base_fee, 2)
    
    def _determine_size_tier(self, dimensions: ProductDimensions) -> FBAFeeTier:
        """确定尺寸分段"""
        # 计算最长边 + 围长
        longest = max(dimensions.length, dimensions.width, dimensions.height)
        other_two = sorted([dimensions.length, dimensions.width, dimensions.height])
        girth = 2 * (other_two[0] + other_two[1])
        
        if longest <= 15 and girth <= 108:
            if longest <= 12 and dimensions.width <= 9 and dimensions.height <= 0.75:
                return FBAFeeTier.SMALL_STANDARD
            return FBAFeeTier.LARGE_STANDARD
        elif longest <= 60 and girth <= 130:
            return FBAFeeTier.SMALL_OVERSIZE
        elif longest <= 108 and girth <= 165:
            return FBAFeeTier.MEDIUM_OVERSIZE
        else:
            return FBAFeeTier.LARGE_OVERSIZE
    
    def _calculate_storage_fee(self, dimensions: ProductDimensions) -> float:
        """计算月度仓储费"""
        # 计算体积（立方英尺）
        volume_cu_ft = (
            dimensions.length * dimensions.width * dimensions.height
        ) / 1728  # 立方英寸转立方英尺
        
        # 使用平均费率
        avg_storage_rate = (self.STORAGE_FEES["jan_sep"] + self.STORAGE_FEES["oct_dec"]) / 2
        
        return round(volume_cu_ft * avg_storage_rate, 2)
    
    def _generate_recommendation(self,
                                margin: float,
                                roi: float,
                                profit: float,
                                sales: int) -> str:
        """生成推荐建议"""
        if margin < 15:
            return "❌ 利润率过低，建议寻找其他产品"
        elif margin < 25:
            return "⚠️ 利润率一般，需优化成本或提高售价"
        elif margin < 35:
            return "✅ 利润率良好，可以考虑进入"
        else:
            if roi > 50 and profit > 10:
                return "🌟 高利润高回报，强烈推荐！"
            return "✅ 优秀利润表现，建议进入"
    
    def compare_scenarios(self,
                         base_price: float,
                         cost: float,
                         dimensions: ProductDimensions) -> Dict:
        """对比不同售价场景"""
        scenarios = {}
        
        for price_adjustment in [-5, -3, 0, 3, 5]:
            test_price = base_price * (1 + price_adjustment / 100)
            analysis = self.calculate_profit(
                selling_price=test_price,
                product_cost=cost,
                dimensions=dimensions
            )
            scenarios[f"{price_adjustment:+d}%"] = {
                "price": round(test_price, 2),
                "margin": analysis.profit_margin,
                "monthly_profit": analysis.monthly_profit_estimate
            }
        
        return scenarios
    
    def calculate_break_even_roas(self,
                                 profit_margin: float) -> float:
        """计算盈亏平衡 ROAS"""
        if profit_margin <= 0:
            return float('inf')
        return 1 / (profit_margin / 100)

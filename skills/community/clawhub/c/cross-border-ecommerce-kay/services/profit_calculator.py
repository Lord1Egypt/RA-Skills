# 利润计算器服务
from models import ProfitCalculation


class ProfitCalculator:
    """利润计算器"""
    
    # 平台费率配置
    PLATFORM_FEES = {
        "amazon": {
            "referral_fee_rate": 0.15,  # 佣金15%
            "fixed_fee": 0.00,
            "fba_storage": 0.02,        # 每单位存储费
        },
        "ebay": {
            "referral_fee_rate": 0.10,  # 佣金10%
            "fixed_fee": 0.30,          # 每单固定费用
            "paypal_fee": 0.029,        # PayPal费用
        }
    }
    
    def __init__(self, platform: str = "amazon"):
        self.platform = platform
        self.fee_config = self.PLATFORM_FEES.get(platform, self.PLATFORM_FEES["amazon"])
    
    def calculate(
        self,
        product_cost: float,
        shipping_cost: float = 0,
        selling_price: float = 0,
        other_cost: float = 0,
        is_fba: bool = False
    ) -> ProfitCalculation:
        """
        计算利润
        
        Args:
            product_cost: 产品成本
            shipping_cost: 运费
            selling_price: 售价
            other_cost: 其他成本(包装费等)
            is_fba: 是否使用FBA
        """
        if selling_price <= 0:
            return ProfitCalculation(
                product_cost=product_cost,
                shipping_cost=shipping_cost,
                platform_fee=0,
                referral_fee=0,
                other_cost=other_cost,
                selling_price=0,
                total_cost=product_cost + shipping_cost + other_cost,
                profit=-product_cost - shipping_cost - other_cost,
                profit_margin=0
            )
        
        # 计算平台费用
        referral_fee = selling_price * self.fee_config["referral_fee_rate"]
        
        if self.platform == "ebay":
            platform_fee = referral_fee + self.fee_config["fixed_fee"]
            # eBay PayPal费用
            platform_fee += selling_price * self.fee_config["paypal_fee"]
        elif is_fba:
            # FBA费用估算
            platform_fee = referral_fee + (selling_price * 0.03)  # FBA履行费约3%
        else:
            platform_fee = referral_fee
        
        # 总成本
        total_cost = product_cost + shipping_cost + platform_fee + other_cost
        
        # 利润
        profit = selling_price - total_cost
        
        # 利润率
        profit_margin = (profit / selling_price * 100) if selling_price > 0 else 0
        
        return ProfitCalculation(
            product_cost=product_cost,
            shipping_cost=shipping_cost,
            platform_fee=round(platform_fee, 2),
            referral_fee=round(referral_fee, 2),
            other_cost=other_cost,
            selling_price=selling_price,
            total_cost=round(total_cost, 2),
            profit=round(profit, 2),
            profit_margin=round(profit_margin, 1)
        )
    
    def suggest_price(self, product_cost: float, target_margin: float = 30) -> float:
        """
        根据目标利润率建议售价
        
        Args:
            product_cost: 产品成本
            target_margin: 目标利润率(%)
        """
        # 简单估算: 售价 = 成本 / (1 - 目标利润率 - 平台费率)
        platform_fee_rate = self.fee_config["referral_fee_rate"]
        adjustment = 1 - (target_margin / 100) - platform_fee_rate
        
        if adjustment <= 0:
            return product_cost * 2  # 保底
        
        suggested_price = product_cost / adjustment
        
        # 归整到99美分
        return round(suggested_price, 2)
    
    def batch_calculate(self, items: list) -> list:
        """批量计算"""
        results = []
        for item in items:
            result = self.calculate(
                product_cost=item.get("product_cost", 0),
                shipping_cost=item.get("shipping_cost", 0),
                selling_price=item.get("selling_price", 0),
                other_cost=item.get("other_cost", 0),
                is_fba=item.get("is_fba", False)
            )
            results.append(result)
        return results

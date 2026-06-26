"""
Buy McDonald Skill - 购买麦当劳商品技能

通过调用 claw_pay API 实现麦当劳商品购买和余额查询
"""

from .skill import (
    BuyMcdonaldSkill,
    buy_mcdonald,
    get_balance,
    check_balance,
    get_on_sale_products,
    BASE_URL
)

__all__ = [
    "BuyMcdonaldSkill",
    "buy_mcdonald",
    "get_balance",
    "check_balance",
    "get_on_sale_products",
    "BASE_URL"
]

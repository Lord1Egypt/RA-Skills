"""
CV-04: Tax Rate × Scenario validator.
"""
from typing import Dict, Any, Optional
from . import validator


@validator
def validate(ind: Dict[str, Any], scenario: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Validates tax rates based on scenario.
    
    Warning: High tax in any scenario is bad
    Critical: Any tax in Scenario A (pegged assets) suggests fake token
    """
    buy_tax = ind.get("buy_tax", 0)
    sell_tax = ind.get("sell_tax", 0)
    sc = scenario.get("scenario", "C")
    
    # Scenario A with any tax is suspicious (fake pegged token)
    if sc == "A" and (buy_tax > 0 or sell_tax > 0):
        return {
            "type": "amplified",
            "indicators": ["buy_tax", "sell_tax", "scenario"],
            "conclusion": (
                f"🛑【疑似仿盘！】该代币被归类为机构锚定资产，"
                f"但检测到异常交易税（买入 {buy_tax:.1f}% / 卖出 {sell_tax:.1f}%）。"
                "正规的 USDT/USDC/WETH 等资产交易税应为 0%，"
                "检测到交易税极大概率是仿冒诈骗合约，请立即核对官方合约地址。"
            ),
            "score_delta": +30,
        }
    
    # High tax warning for all scenarios
    if sell_tax > 10 or buy_tax > 10:
        return {
            "type": "amplified",
            "indicators": ["buy_tax", "sell_tax"],
            "conclusion": (
                f"⚠️【高税率警告】检测到较高交易税（买入 {buy_tax:.1f}% / 卖出 {sell_tax:.1f}%）。"
                f"{'对于 Meme 币，高税率是常见的割韭菜手段，买入即亏损。' if sc == 'C' else '高税率会显著影响交易成本和流动性。'}"
            ),
            "score_delta": +10 if sc == "C" else +5,
        }
    
    return None

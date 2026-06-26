"""
CV-03: Proxy Contract × Scenario validator.
"""
from typing import Dict, Any, Optional
from . import validator


@validator
def validate(ind: Dict[str, Any], scenario: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Validates proxy contract status based on scenario.
    
    Contextual: Proxy is acceptable for Scenario A/B (mainstream/eco tokens)
    Warning: Proxy in Scenario C (Meme coins) is suspicious
    """
    is_proxy = ind.get("is_proxy", False)
    sc = scenario.get("scenario", "C")
    
    if not is_proxy:
        return None
    
    if sc in ("A", "B"):
        return {
            "type": "contextual",
            "indicators": ["is_proxy", "scenario"],
            "conclusion": (
                f"ℹ️【代理合约适配】该代币为{'机构锚定资产' if sc == 'A' else '生态价值币'}，"
                "使用代理合约（Upgradeable Proxy）是合理设计。"
                "机构需要保留升级能力以修复漏洞或响应监管要求，"
                "这是中心化信任模型的正常组成部分。"
            ),
            "score_delta": -5,
        }
    else:
        return {
            "type": "amplified",
            "indicators": ["is_proxy", "scenario"],
            "conclusion": (
                "⚠️【代理合约警告】Meme 币/土狗项目使用代理合约风险较高。"
                "团队可随时替换合约逻辑，包括添加貔貅功能、修改税率、冻结用户资产等。"
                "早期承诺可能在一次升级后完全失效。"
            ),
            "score_delta": +10,
        }

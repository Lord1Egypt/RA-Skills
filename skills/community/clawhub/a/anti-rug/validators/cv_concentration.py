"""
CV-02: Concentration × Protocol Address validator.
"""
from typing import Dict, Any, Optional
from . import validator


@validator
def validate(ind: Dict[str, Any], scenario: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Validates holder concentration considering protocol-held addresses.
    
    Contextual: High concentration but mostly protocol addresses
    Amplified: High concentration with low protocol holding
    """
    top10_pct = ind.get("top10_pct", 0)
    protocol_held_pct = ind.get("protocol_held_pct", 0)
    
    if top10_pct <= 40:
        return None
    
    effective = max(0, top10_pct - protocol_held_pct)
    
    if protocol_held_pct > 20:
        return {
            "type": "contextual",
            "indicators": ["top10_holders_pct", "protocol_held_pct"],
            "conclusion": (
                f"ℹ️【持仓集中度重新解读】前10地址持仓 {top10_pct:.1f}%，"
                f"但其中 {protocol_held_pct:.1f}% 归属于已知 DEX 资金池、"
                f"质押合约或黑洞地址等协议地址。"
                f"剔除协议地址后，实际「可疑集中度」仅约 {effective:.1f}%，"
                "持仓结构基本健康，不构成庄家控盘特征。"
            ),
            "score_delta": -10,
        }
    else:
        return {
            "type": "amplified",
            "indicators": ["top10_holders_pct"],
            "conclusion": (
                f"⚠️【持仓高度集中】前10地址持仓 {top10_pct:.1f}%，"
                f"协议/黑洞地址仅占 {protocol_held_pct:.1f}%，"
                f"实际可疑集中持仓约 {effective:.1f}%。"
                "存在明显庄家或团队控盘风险，大额抛售可造成价格雪崩。"
            ),
            "score_delta": +15,
        }

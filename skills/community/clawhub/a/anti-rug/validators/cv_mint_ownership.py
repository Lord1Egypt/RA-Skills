"""
CV-01: Mintable × Owner Status validator.
"""
from typing import Dict, Any, Optional
from . import validator


@validator
def validate(ind: Dict[str, Any], scenario: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Validates the relationship between mintable status and owner status.
    
    Neutralized: Mintable but owner is dead (risk neutralized)
    Amplified: Mintable with active owner in scenario C (Meme coin)
    """
    is_mintable = ind.get("is_mintable", False)
    owner_is_dead = ind.get("owner_is_dead", False)
    holder_count = ind.get("holder_count", 0)
    sc = scenario.get("scenario", "C")
    
    if is_mintable and owner_is_dead:
        return {
            "type": "neutralized",
            "indicators": ["is_mintable", "owner_address"],
            "conclusion": (
                "✅【增发风险已中和】合约虽含增发函数（is_mintable=True），"
                "但 Owner 已打入黑洞地址，当前无任何账户具备调用增发权限的能力。"
                "增发代码形同虚设，实际风险与无增发合约等同。"
            ),
            "score_delta": -15,
        }
    elif is_mintable and not owner_is_dead and sc == "C":
        return {
            "type": "amplified",
            "indicators": ["is_mintable", "owner_address"],
            "conclusion": (
                "🔴【增发风险放大】合约不仅可以增发，且 Owner 地址仍在活跃控制中。"
                f"持有者仅 {holder_count:,} 人，流动性薄弱，"
                "团队随时可增发打压价格后出货，这是 Meme 币最常见的割韭菜路径。"
            ),
            "score_delta": +20,
        }
    return None

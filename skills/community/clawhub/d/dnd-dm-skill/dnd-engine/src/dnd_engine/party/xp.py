"""
经验值计算函数库
"""
import os
import json

def calc_combat_xp(cr_list, party_level, party_size=4):
    """
    按 CR 计算战斗经验值（参考 2024 版怪物图鉴 XP 表）
    
    参数:
        cr_list: list[float] - 怪物 CR 列表
        party_level: int - 队伍等级
        party_size: int - 队伍人数（默认 4）
    
    返回:
        dict: {"total_xp": int, "per_person": int, "detail": str}
    """
    # CR → XP 对照表（2024 D&D 5e）
    CR_XP_TABLE = {
        0: 10, 0.125: 25, 0.25: 50, 0.5: 100,
        1: 200, 2: 450, 3: 700, 4: 1100, 5: 1800,
        6: 2300, 7: 2900, 8: 3900, 9: 5000, 10: 5900,
        11: 7200, 12: 8400, 13: 10000, 14: 11500, 15: 13000,
        16: 15000, 17: 18000, 18: 20000, 19: 22000, 20: 25000,
        21: 33000, 22: 41000, 23: 50000, 24: 62000, 25: 75000,
        26: 90000, 27: 105000, 28: 120000, 29: 135000, 30: 155000,
    }
    
    total_xp = 0
    details = []
    for cr in cr_list:
        closest_cr = min(CR_XP_TABLE.keys(), key=lambda k: abs(k - cr))
        xp = CR_XP_TABLE[closest_cr]
        total_xp += xp
        details.append(f"  CR {cr} → {xp} XP")
    
    per_person = total_xp // party_size
    
    return {
        "total_xp": total_xp,
        "per_person": per_person,
        "detail": f"怪物 {len(cr_list)} 只，总经验 {total_xp} XP\n" +
                  "\n".join(details) +
                  f"\n每人获得: {per_person} XP（{party_size}人平分）"
    }


def calc_noncombat_xp(difficulty, party_level, party_size=4):
    """
    按难度计算非战斗经验（谈判、潜行、解谜等）
    
    参数:
        difficulty: str - 'low' / 'medium' / 'high'
        party_level: int - 队伍等级
        party_size: int - 队伍人数（默认 4）
    
    返回:
        dict: {"per_person": int, "detail": str}
    """
    # 人均经验值预算表（仅 1 级，后续等级可扩展）
    XP_BUDGET = {
        1: {"low": 50, "medium": 75, "high": 100},
    }
    
    level_budget = XP_BUDGET.get(party_level, XP_BUDGET[1])
    per_person = level_budget.get(difficulty, level_budget['medium'])
    
    return {
        "per_person": per_person,
        "detail": f"非战斗挑战（{difficulty}难度）→ 每人获得 {per_person} XP"
    }


def get_level_up_xp_requirement(current_level):
    """
    获取升到下一级所需的累积 XP
    
    参数:
        current_level: int - 当前等级
    
    返回:
        int: 升到下一级所需的累积 XP
    """
    # 2024 D&D 5e 升级所需累积 XP
    XP_TABLE = {
        1: 0, 2: 300, 3: 900, 4: 2700, 5: 6500,
        6: 14000, 7: 23000, 8: 34000, 9: 48000, 10: 64000,
        11: 85000, 12: 100000, 13: 120000, 14: 140000, 15: 165000,
        16: 195000, 17: 225000, 18: 265000, 19: 305000, 20: 355000,
    }
    next_level = current_level + 1
    if next_level in XP_TABLE:
        return XP_TABLE[next_level]
    return 999999

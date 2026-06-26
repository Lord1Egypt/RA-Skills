"""
战斗解析：命中判断与伤害结算
"""
import re
import random


def check_hit(attack_roll_total, attacker_bonus, defender_ac):
    """
    判断攻击是否命中（仅用于内部计算）
    
    参数:
        attack_roll_total: int - d20 骰面结果（1-20）
        attacker_bonus: int - 攻击者的总加值（熟练+属性+装备）
        defender_ac: int - 防御者的 AC
    
    返回:
        dict: {"hit": bool, "critical": bool, "natural": int, "total": int, "detail": str}
    
    ⚠️ 注意：此函数不展示加值明细。
    向玩家展示检定结果时，请使用 checks.py 的 check_hit_v2() 或 resolve_skill_check()，
    它们会展示 d20 + 每项加值明细的完整公式。
    """
    total = attack_roll_total + attacker_bonus
    
    # 自然 1 必然未命中
    if attack_roll_total == 1:
        return {"hit": False, "critical": False, "natural": 1, "total": total,
                "detail": f"🎲 d20=1（自然1！）→ 必然未命中 ❌"}
    
    # 自然 20 必然命中且重击
    if attack_roll_total == 20:
        return {"hit": True, "critical": True, "natural": 20, "total": total,
                "detail": f"🎲 d20=20（重击！）+{attacker_bonus}={total} → 重击命中！⚡"}
    
    # 正常命中判断
    hit = total >= defender_ac
    status = "✅ 命中" if hit else "❌ 未命中"
    
    return {"hit": hit, "critical": False, "natural": attack_roll_total, "total": total,
            "detail": f"🎲 d20={attack_roll_total}+{attacker_bonus}={total} vs AC {defender_ac} → {status}"}


def calc_damage(dice_count, dice_sides, bonus=0, extra_dice=None, critical=False):
    """
    结算伤害
    
    参数:
        dice_count: int - 骰子数量
        dice_sides: int - 骰子面数
        bonus: int - 固定加值（含装备加值）
        extra_dice: list[dict] - 额外伤害骰，如 [{"count":2,"sides":6,"label":"偷袭"}]
        critical: bool - 是否重击（骰子翻倍）
    
    返回:
        dict: {"total": int, "rolls": list[int], "detail": str}
    """
    roll_count = dice_count * 2 if critical else dice_count
    rolls = [random.randint(1, dice_sides) for _ in range(roll_count)]
    dice_total = sum(rolls)
    
    total = dice_total + bonus
    detail_parts = [f"{dice_count}d{dice_sides}: {'+'.join(map(str, rolls))} = {dice_total}"]
    
    if critical:
        detail_parts[-1] += " (重击翻倍)"
    
    # 额外伤害骰
    extra_rolls = []
    for extra in (extra_dice or []):
        e_rolls = [random.randint(1, extra["sides"]) for _ in range(extra["count"])]
        extra_rolls.extend(e_rolls)
        e_total = sum(e_rolls)
        total += e_total
        detail_parts.append(f"{extra.get('label','')}: {'+'.join(map(str, e_rolls))} = {e_total}")
    
    if bonus:
        detail_parts.append(f"固定加值: +{bonus}")
    
    return {"total": total, "rolls": rolls + extra_rolls, 
            "detail": " + ".join(detail_parts) + f" = {total}"}


def calc_save_dc(base_dc, bonuses=None):
    """
    计算法术/能力豁免 DC
    
    参数:
        base_dc: int - 基础 DC（8+熟练+施法属性）
        bonuses: list[int] - 额外 DC 加值（装备、专长等）
    
    返回:
        int: 最终 DC
    """
    return base_dc + sum(bonuses or [])

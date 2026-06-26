"""
技能检定解析：完整公式展示的解算模块
"""
import random


def resolve_skill_check(d20_result: int, components: dict, dc: int,
                        skill_name: str, character_name: str,
                        advantage: str = None) -> dict:
    """
    技能检定完整结算：展示 d20 + 每项加值明细 → 合计 → 通过与失败

    参数:
        d20_result: int - d20骰面结果 (1-20)
        components: dict - 加值明细:
            {
                "熟练加值": int,
                "属性调整": int,
                "装备加成": int,
                "专长/其他": int,   # 可选
                "临时状态": int     # 可选
            }
        dc: int - 检定难度
        skill_name: str - 技能名称（如"察觉"、"隐匿"）
        character_name: str - 角色名
        advantage: str 或 None - None=普通, "adv"=优势, "dis"=劣势

    返回:
        dict:
            d20: int,
            total_bonus: int,
            grand_total: int,
            success: bool,
            critical: str (None / "nat1" / "nat20"),
            detail_lines: list[str],   # 每行一个展示行
            summary_line: str           # 最终一行总结
    """
    # 自然判定
    critical = None
    if d20_result == 1:
        critical = "nat1"
    elif d20_result == 20:
        critical = "nat20"

    # 计算总加值
    bonus_parts = []
    total_bonus = 0
    for label, val in components.items():
        if val != 0:
            bonus_parts.append((label, val))
            total_bonus += val

    grand_total = d20_result + total_bonus

    # 展示行
    detail_lines = []

    # 行动声明行
    adv_tag = ""
    if advantage == "adv":
        adv_tag = "（优势）"
    elif advantage == "dis":
        adv_tag = "（劣势）"
    action_line = f"【{skill_name}检定{adv_tag}】{character_name}：请投{skill_name}检定，DC {dc}"
    detail_lines.append(action_line)

    # d20结果行
    roll_str = f"  → d20 = {d20_result}"
    if critical == "nat1":
        roll_str += " ⚠️ 自然1！必然失败"
    elif critical == "nat20":
        roll_str += " ⚡ 自然20！必然成功"
    detail_lines.append(roll_str)

    # 加值明细行
    bonus_str = "  → 加值明细：" + " + ".join(f"{label} {v:+d}" for label, v in bonus_parts)
    if not bonus_parts:
        bonus_str = "  → 加值明细：无额外加值"
    detail_lines.append(bonus_str)

    # 合计行
    success_str = ""
    if critical == "nat1":
        success_str = "❌ 失败（自然1）"
    elif critical == "nat20":
        success_str = "✅ 成功（自然20）"
    else:
        success_str = f"✅ 成功" if grand_total >= dc else f"❌ 失败"

    success = (grand_total >= dc) if not critical else (critical == "nat20")

    formula_str = f"  → {d20_result} + {total_bonus} = {grand_total}（DC {dc}）{success_str}"
    detail_lines.append(formula_str)

    # 单行总结
    summary_line = f"{character_name}（{skill_name}{total_bonus:+d}）：d20={d20_result}，合计 {grand_total}（DC {dc}）{success_str}"

    return {
        "d20": d20_result,
        "total_bonus": total_bonus,
        "grand_total": grand_total,
        "success": success,
        "critical": critical,
        "detail_lines": detail_lines,
        "summary_line": summary_line
    }


def resolve_save_check(d20_result: int, components: dict, dc: int,
                       save_name: str, character_name: str) -> dict:
    """
    豁免检定完整结算（复用 resolve_skill_check 逻辑，调整标签）

    参数:
        d20_result: int
        components: dict - 如 {"熟练加值": X, "属性调整": Y, "装备加成": Z}
        dc: int
        save_name: str - 如"体质豁免"、"敏捷豁免"
        character_name: str

    返回: 同 resolve_skill_check
    """
    return resolve_skill_check(
        d20_result=d20_result,
        components=components,
        dc=dc,
        skill_name=save_name,
        character_name=character_name
    )


def check_hit_v2(d20_result: int, components: dict, defender_ac: int,
                 attacker_name: str, weapon_name: str = "") -> dict:
    """
    攻击命中的完整公式展示（check_hit 的升级版本）

    参数:
        d20_result: int
        components: dict - 加值明细，如：
            {"熟练加值": 3, "属性调整": 4, "装备加成": 1, "临时状态": 0}
        defender_ac: int
        attacker_name: str
        weapon_name: str - 武器名（可选）

    返回:
        dict: 同 resolve_skill_check，额外包含 hit/critical 字段
    """
    result = resolve_skill_check(
        d20_result=d20_result,
        components=components,
        dc=defender_ac,
        skill_name=f"攻击({weapon_name})" if weapon_name else "攻击",
        character_name=attacker_name
    )
    # 转译为命中判断
    result["hit"] = result["success"]
    return result

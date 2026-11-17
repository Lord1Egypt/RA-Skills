"""战斗回合闭环：判定 → 结算 → 写入战斗状态（combat_state.json）→ 推进轮次。

把三块接起来：
1. `judge.batch` 一次扇出判定所有 PC 的行动（1 次模型调用）；
2. `combat.checks` 结算命中与伤害（确定性，本地毫秒级）；
3. `combat.state` 写回 HP/死亡/轮次（引擎的持久化战斗状态）。

入口见 `tools/judge_combat_loop.py`。
"""

from __future__ import annotations

import re
from typing import Any

from ..combat.resolve import calc_damage
from ..combat.state import (
    advance_turn,
    apply_damage,
    get_combat_summary,
    new_combat,
    tick_effects,
)
from ..dice.rolls import roll_d20
from . import check_rules, damage_rules
from .batch import resolve_batch
from .contracts import Question, validate_answer, validate_answers

DAMAGE_RE = re.compile(r"(\d*)d(\d+)")
BONUS_RE = re.compile(r"\+\s*(\d+)")


def ability_modifier(score: Any) -> int:
    try:
        return (int(score) - 10) // 2
    except (TypeError, ValueError):
        return 0


def parse_damage(spec: str) -> tuple[int, int, int]:
    """把 "1d6+5+酸1d6" 解析成 (骰数, 面数, 固定加值)。"""
    dice = DAMAGE_RE.search(str(spec or ""))
    count = int(dice.group(1) or 1) if dice else 1
    sides = int(dice.group(2)) if dice else 4
    bonus_match = BONUS_RE.search(str(spec or ""))
    bonus = int(bonus_match.group(1)) if bonus_match else 0
    return count, sides, bonus


def build_unit(name: str, hp: int, armor: int, initiative: int,
               is_pc: bool, sheet: dict | None = None) -> dict:
    return {
        "name": name,
        "initiative": initiative,
        "hp": hp,
        "maxHp": hp,
        "armor": armor,
        "is_pc": is_pc,
        "status": "等待",
        "effects": [],
        "sheet": sheet or {},
    }


def roll_initiative(sheet: dict | None = None, modifier: int | None = None) -> int:
    if modifier is None:
        stats = (sheet or {}).get("stats") or (sheet or {}).get("attributes") or {}
        dex = stats.get("dex", stats.get("敏捷", 10))
        modifier = ability_modifier(dex)
    return int(roll_d20()["result"]) + int(modifier)


def open_combat(combat_name: str, location: str, party: list[dict],
                enemies: list[dict]) -> dict:
    """party: live_party.json 的 party[]；enemies: {name, hp, armor}[]。"""
    units: list[dict] = []
    for member in party:
        name = str(member.get("name") or "")
        hp = (member.get("hp") or {}).get("max") or 10
        units.append(build_unit(name, int(hp), int(member.get("ac") or 10),
                                roll_initiative(member), True, member))
    for enemy in enemies:
        units.append(build_unit(
            str(enemy.get("name") or "敌人"), int(enemy.get("hp") or 1),
            int(enemy.get("armor") or 10),
            roll_initiative(None, int(enemy.get("initiative_mod", 0))), False, {},
        ))
    return new_combat(combat_name, location, units)


def weapon_damage_spec(sheet: dict | None) -> str:
    attacks = (sheet or {}).get("attacks") or []
    for attack in attacks:
        spec = str(attack.get("dmg") or "")
        if spec:
            return spec
    return ""


def resolve_pc_round(state: dict, declarations: list[dict],
                     sheets: dict[str, dict], provider=None,
                     rules: dict | None = None,
                     module_dcs: list[dict] | None = None,
                     enemy_profiles: dict[str, dict] | None = None,
                     d20s: list[int | None] | None = None) -> dict[str, Any]:
    """一次扇出判定 + 结算 + 写回战斗状态。返回本轮结果与统计。

    module_dcs：当前场景的模组检定条目（由 `module_data.dcs_for_scene` 提供）。
    enemy_profiles：敌人档案（名字 → 含抗性/免疫/易伤的怪物档案），用于伤害修正。
    d20s：可选固定骰面（测试与复现用）。
    """
    table = rules or check_rules.load_rules()
    judge_state = {
        "acting_options": list(sheets) or [str(u["name"]) for u in living_units(state, True)],
        "acting_default": next(iter(sheets), ""),
        "targets": [str(u["name"]) for u in living_units(state) if not u.get("is_pc")],
        "module_dcs": list(module_dcs or []),
    }
    results = resolve_batch(state=judge_state, declarations=declarations,
                            answers_provider=provider, sheets=sheets, rules=table,
                            d20s=d20s)

    applied: list[str] = []
    total_damage = 0
    for declaration, result in zip(declarations, results):
        outcome = result["outcome"]
        target = str(declaration.get("target") or "")
        enemies_left = [u for u in living_units(state) if not u.get("is_pc")]
        if not enemies_left:
            applied.append(f"{result['actor']} 收手（敌人已全部倒下）")
            continue
        target_unit = next((u for u in state["units"] if u["name"] == target), None)
        if target_unit is not None and target_unit.get("status") == "死亡":
            applied.append(f"{result['actor']} 目标已倒下，转移攻击")
            continue
        if not outcome.ran or not outcome.hit:
            applied.append(f"{result['actor']} 未命中" if outcome.ran else f"{result['actor']} 无需检定")
            continue
        sheet = sheets.get(result["actor"]) or {}
        damage_spec = weapon_damage_spec(sheet)
        count, sides, bonus = parse_damage(damage_spec)
        rolled = int(calc_damage(count, sides, bonus)["total"])
        dtype = damage_rules.infer_damage_type(damage_spec)
        profile = (enemy_profiles or {}).get(target)
        damage, note = damage_rules.apply_damage_rules(rolled, dtype, profile)
        total_damage += damage
        suffix = f"｜{note}" if note else ""
        if target:
            if damage:
                apply_damage(state, target, damage, source=result["actor"])
            applied.append(f"{result['actor']} → {target} {damage} 点{suffix}")
        else:
            applied.append(f"{result['actor']} 命中 {damage} 点（未指定目标）{suffix}")

    tick_effects(state)
    return {"results": results, "applied": applied, "total_damage": total_damage}


def advance_full_round(state: dict) -> dict:
    """推进到下一轮（跳过已死亡单位）。"""
    start_round = state["round"]
    guard = 0
    while state["round"] == start_round and guard < len(state["units"]) + 2:
        advance_turn(state)
        guard += 1
    return state


def render(state: dict, round_result: dict | None = None) -> str:
    lines = [get_combat_summary(state), ""]
    order = " → ".join(u["name"] for u in state["units"])
    lines.append(f"先攻顺序：{order}")
    if round_result:
        lines.append("")
        lines.append("── 本轮结算 ──")
        for row in round_result["applied"]:
            lines.append(f"  · {row}")
        lines.append(f"  合计伤害：{round_result['total_damage']}")
    lines.append("")
    lines.append("── 战斗日志（末 6 条）──")
    for entry in state["log"][-6:]:
        lines.append(f"  {entry}")
    return "\n".join(lines)


# ────────────────────────── 敌方回合 ──────────────────────────

ENEMY_ACTIONS = ["攻击", "施法", "撤退", "按兵不动"]
TARGET_POLICIES = ["集火最脆弱", "就近", "优先施法者", "随机"]
RETREAT_HP_RATIO = 0.33          # 血量低于此比例时，士气不足则撤退
CASTERS = ("法师", "牧师", "术士", "邬术师", "吟游诗人", "德鲁伊")


def living_units(state: dict, only_pc: bool = False) -> list[dict]:
    return [u for u in state["units"]
            if u.get("status") != "死亡" and (not only_pc or u.get("is_pc"))]


def _enemy_questions(index: int, targets: list[str], attacks: list[str]) -> list[Question]:
    prefix = f"e{index}_"
    return [
        Question(f"{prefix}action", "choice", "这个敌人本回合主要做什么？", ENEMY_ACTIONS),
        Question(f"{prefix}target_policy", "choice",
                 "若发动攻击，它优先打谁？（集火最脆弱=全队压血量最低的）", TARGET_POLICIES),
        Question(f"{prefix}attack", "choice", "用哪一项攻击？", attacks or ["徒手"]),
        Question(f"{prefix}morale", "noul",
                 "即使已受重伤，这个敌人是否仍愿意继续战斗？"),
    ]


def pick_target(policy: str, state: dict, actor: dict,
                targets: list[dict]) -> str:
    """把战术意图解成具体目标（无格子坐标时的确定性代理）。

    集火最脆弱 → 当前 HP 最低；优先施法者 → 职业名含施法者，否则取 AC 最低；
    就近 → 按先攻顺序取该敌人之后的下一个存活 PC；随机 → 用轮次+序号做确定伪随机。
    """
    if not targets:
        return ""
    if policy == "集火最脆弱":
        return str(min(targets, key=lambda u: u.get("hp", 0))["name"])
    if policy == "优先施法者":
        casters = [u for u in targets
                   if any(word in str((u.get("sheet") or {}).get("class") or "") for word in CASTERS)]
        pool = casters or targets
        return str(min(pool, key=lambda u: u.get("armor", 99))["name"])
    if policy == "就近":
        order = [u for u in state["units"] if u.get("status") != "死亡"]
        try:
            start = order.index(actor)
        except ValueError:
            return str(targets[0]["name"])
        for offset in range(1, len(order) + 1):
            candidate = order[(start + offset) % len(order)]
            if candidate.get("is_pc"):
                return str(candidate["name"])
        return str(targets[0]["name"])
    seed = int(state.get("round") or 1) + len(targets)
    return str(targets[seed % len(targets)]["name"])


def rule_only_enemy_answers(enemies: list[dict], index: int,
                            targets: list[str]) -> dict[str, dict]:
    """离线启发式：打最脆的 PC，用第一项攻击，士气默认坚挺。"""
    prefix = f"e{index}_"
    return {
        f"{prefix}action": {"value": "攻击", "confidence": 1.0},
        f"{prefix}target_policy": {"value": "集火最脆弱", "confidence": 1.0},
        f"{prefix}attack": {"value": "徒手", "confidence": 1.0},
        f"{prefix}morale": {"value": 1.0, "confidence": 1.0},
    }


def resolve_enemy_round(state: dict, enemy_profiles: list[dict], provider=None,
                        rules: dict | None = None) -> dict[str, Any]:
    """敌方回合：一次调用判定所有活着的敌人，然后本地结算命中与伤害。

    enemy_profiles: [{name, hp, armor, initiative_mod, attacks:[{name,bonus,dmg}]}]
    """
    profiles = {str(e.get("name")): e for e in enemy_profiles}
    actors = [u for u in living_units(state) if not u.get("is_pc")]
    target_units = living_units(state, only_pc=True)
    target_names = [str(u["name"]) for u in target_units]
    targets_by_hp = sorted(target_units, key=lambda u: u.get("hp", 0))
    default_target = str(targets_by_hp[0]["name"]) if targets_by_hp else "无"

    if provider is not None:
        questions: list[Question] = []
        for index, actor in enumerate(actors):
            profile = profiles.get(str(actor["name"]), {})
            attacks = [str(a.get("name") or "徒手") for a in (profile.get("attacks") or [])]
            questions.extend(_enemy_questions(index, target_names, attacks))
        payload = provider(questions, state, "敌方回合") if questions else {"answers": {}}
        raw = payload.get("answers") if isinstance(payload, dict) and "answers" in payload else payload
    else:
        raw = {}

    applied: list[str] = []
    total_damage = 0
    for index, actor in enumerate(actors):
        name = str(actor["name"])
        profile = profiles.get(name, {})
        attacks = profile.get("attacks") or [{"name": "徒手", "bonus": 2, "dmg": "1d4"}]
        if not target_names:
            applied.append(f"{name} 无可攻击目标")
            continue

        fallback = rule_only_enemy_answers(profile and [profile] or [], index, [default_target])
        decided: dict[str, Any] = {}
        questions = _enemy_questions(
            index, target_names, [str(a.get("name") or "徒手") for a in attacks])
        for question in questions:
            item = (raw or {}).get(question.id) if isinstance(raw, dict) else None
            try:
                decided[question.id] = validate_answer(item, question).value
            except Exception:  # noqa: BLE001 — 模型没答/答错 → 用启发式
                decided[question.id] = fallback.get(question.id, {}).get("value")

        # 撤退阈值由**引擎**强制：重伤且士气不足就不再恋战
        hp_ratio = float(actor.get("hp", 1)) / max(1.0, float(actor.get("maxHp", 1)))
        morale_item = (raw or {}).get(f"e{index}_morale") if isinstance(raw, dict) else None
        try:
            morale = validate_answer(
                morale_item,
                Question(f"e{index}_morale", "noul", "")).assertive
        except Exception:  # noqa: BLE001
            morale = True

        action = str(decided.get(f"e{index}_action") or "攻击")
        if hp_ratio <= RETREAT_HP_RATIO and not morale and action not in ("撤退",):
            action = "撤退"
            applied.append(f"{name} 重伤（HP {hp_ratio:.0%}）且士气崩溃 → 撤退")
            continue

        policy = str(decided.get(f"e{index}_target_policy") or "就近")
        target = pick_target(policy, state, actor, target_units)
        if not target:
            target = default_target
        attack_name = str(decided.get(f"e{index}_attack") or "")
        chosen = next((a for a in attacks if str(a.get("name")) == attack_name), attacks[0])

        if action in ("撤退", "按兵不动"):
            applied.append(f"{name} {action}")
            continue

        bonus = int(re.search(r"([+-]?\d+)", str(chosen.get("bonus") or "0")).group(1))
        target_unit = next((u for u in target_units if u["name"] == target), None)
        target_ac = int((target_unit or {}).get("armor") or 10)
        count, sides, dmg_bonus = parse_damage(str(chosen.get("dmg") or ""))

        # 多重攻击：怪物特性写了几次就打几次（上限 4 次，防止数据异常时刷屏）
        swings = max(1, min(4, int(profile.get("multiattack") or 1)))
        hits = 0
        dealt = 0
        rolls: list[str] = []
        for _ in range(swings):
            d20 = int(roll_d20()["result"])
            total = d20 + bonus
            if d20 == 1 or (d20 != 20 and total < target_ac):
                rolls.append(f"{d20}+{bonus}={total}vs{target_ac}✗")
                continue
            damage = int(calc_damage(count, sides, dmg_bonus)["total"])
            if d20 == 20:
                damage += int(calc_damage(count, sides, 0)["total"])
            hits += 1
            dealt += damage
            rolls.append(f"{d20}+{bonus}={total}vs{target_ac}{'✱' if d20 == 20 else '✓'}")

        if hits == 0:
            applied.append(f"{name} 攻击 {target} 未命中（{'，'.join(rolls)}）")
            continue
        dtype = damage_rules.infer_damage_type(str(chosen.get("damage_type") or ""))
        pc_profile = damage_rules.pc_profile((target_unit or {}).get("sheet"))
        dealt, note = damage_rules.apply_damage_rules(dealt, dtype, pc_profile)
        total_damage += dealt
        if dealt:
            apply_damage(state, target, dealt, source=name)
        suffix = f"×{hits}" if swings > 1 else ""
        extra = f"｜{note}" if note else ""
        applied.append(f"{name} → {target} {dealt} 点{suffix}（{'，'.join(rolls)}）{extra}")

    tick_effects(state)
    return {"applied": applied, "total_damage": total_damage, "actors": len(actors)}


def render_enemy_phase(result: dict) -> str:
    lines = [f"── 敌方回合（{result['actors']} 名敌人）──"]
    for row in result["applied"]:
        lines.append(f"  · {row}")
    lines.append(f"  合计对 PC 造成：{result['total_damage']} 点")
    return "\n".join(lines)

"""P3：把 DecisionPacket 接到引擎，直接产出检定明细。

链路：判定层给出 {执行者, 技能, DC, 优劣势} → 本模块从角色卡组装加值 →
调用 combat.checks.resolve_skill_check() → 输出 detail_lines/summary_line（原文可贴给玩家）。

纯引擎层代码：零 LLM 依赖、零第三方依赖。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from ..combat.checks import check_hit_v2, resolve_skill_check
from ..dice.rolls import roll_d20
from . import check_rules
from .contracts import DecisionPacket

ADVANTAGE_MAP: dict[str, str | None] = {
    "优势": "adv", "普通": None, "劣势": "dis",
    "adv": "adv", "none": None, "dis": "dis", "": None,
}

ABILITY_ZH = {"str": "力量", "dex": "敏捷", "con": "体质",
              "int": "智力", "wis": "感知", "cha": "魅力"}

# 角色卡里其他加值的常见键名 → 展示标签
EXTRA_LABELS = {"装备加成", "专长/其他", "其他", "临时状态", "misc", "item"}


@dataclass(slots=True)
class CheckOutcome:
    packet: DecisionPacket
    ran: bool = False
    hit: bool | None = None
    d20: int | None = None
    roll_detail: str = ""
    advantage: str | None = None
    components: dict[str, int] = field(default_factory=dict)
    detail_lines: list[str] = field(default_factory=list)
    summary_line: str = ""
    note: str = ""


def ability_modifier(score: Any) -> int:
    try:
        return (int(score) - 10) // 2
    except (TypeError, ValueError):
        return 0


def proficiency_bonus(level: Any = 1, sheet: dict[str, Any] | None = None) -> int:
    given = (sheet or {}).get("proficiency")
    if given is not None:
        try:
            return int(given)
        except (TypeError, ValueError):
            pass
    try:
        lv = max(1, int(level or 1))
    except (TypeError, ValueError):
        lv = 1
    return 2 + (lv - 1) // 4


def ability_score(sheet: dict[str, Any] | None, ability: str) -> int:
    if not sheet or not ability:
        return 10
    stats = sheet.get("stats") or sheet.get("attributes") or {}
    if ability in stats:
        return int(stats[ability])
    zh = ABILITY_ZH.get(ability, "")
    if zh in stats:
        return int(stats[zh])
    return 10


def has_skill_proficiency(sheet: dict[str, Any] | None, skill: str,
                          rules: dict[str, Any] | None = None) -> bool:
    """兼容三种角色卡写法：skills 列表 / 名单 / 字典，以及 proficiencies.skill_refs。"""
    if not sheet or not skill:
        return False
    table = rules or check_rules.load_rules()
    key = check_rules.canonical_skill(skill, table)
    info = check_rules.skill_info(key, table) or {}
    candidates = {skill, key, str(info.get("name") or key), f"skill:{skill}", f"skill:{key}"}
    candidates |= {str(alias) for alias in (info.get("aliases") or []) if alias}

    skills = sheet.get("skills")
    if isinstance(skills, dict):
        for key, value in skills.items():
            if str(key) in candidates and value:
                return True
    elif isinstance(skills, list):
        for item in skills:
            if isinstance(item, dict):
                if str(item.get("name")) in candidates and item.get("value") is not None:
                    # 列表里带数值的即视为已熟练
                    return True
            elif str(item) in candidates:
                return True

    proficiencies = sheet.get("proficiencies")
    if isinstance(proficiencies, dict):
        refs = proficiencies.get("skill_refs") or []
        if skill in {str(r).split(":", 1)[-1] for r in refs}:
            return True
    return False


def _skill_entries(sheet: dict[str, Any] | None, key: str,
                   rules: dict[str, Any] | None = None) -> set[str]:
    """读角色卡里的「已熟练 / 已专精」技能集合（兼容 list / dict / skill_refs 三种写法）。

    返回值同时包含英文 key 与中文名，方便两种写法互相匹配。
    """
    if not sheet:
        return set()
    table = rules or check_rules.load_rules()
    found: set[str] = set()
    raw = sheet.get(key)
    if isinstance(raw, dict):
        raw = [name for name, value in raw.items() if value]
    if isinstance(raw, (list, tuple, set)):
        for item in raw:
            name = item.get("name") if isinstance(item, dict) else item
            if name:
                found.add(str(name))
    if key == "skills":
        proficiencies = sheet.get("proficiencies")
        if isinstance(proficiencies, dict):
            for ref in proficiencies.get("skill_refs") or []:
                found.add(str(ref).split(":", 1)[-1])
    expanded = set(found)
    for name in found:
        info = check_rules.skill_info(name, table) or {}
        if info.get("name"):
            expanded.add(str(info["name"]))
    return expanded


def _matches(entry: str, skill: str, table: dict[str, Any]) -> bool:
    """技能卡上的写法与检定技能是否指同一个技能（键/中文名/别名/关键词互认）。"""
    if entry == skill or entry == f"skill:{skill}":
        return True
    entry_key = check_rules.canonical_skill(entry, table)
    skill_key = check_rules.canonical_skill(skill, table)
    return bool(entry_key) and entry_key == skill_key


def explicit_skill_bonus(sheet: dict[str, Any] | None, skill: str,
                         rules: dict[str, Any] | None = None) -> int | None:
    """角色卡直接写明的**该技能总加值**（如 `skill_bonuses: {"潜行": 11}`）。

    有它就以它为准——避免“专精/装备加成”这类信息引擎推导不出来时算错数。
    """
    if not sheet:
        return None
    table = rules or check_rules.load_rules()
    explicit = sheet.get("skill_bonuses")
    if not isinstance(explicit, dict):
        return None
    for name, value in explicit.items():
        if _matches(str(name), skill, table):
            try:
                return int(value)
            except (TypeError, ValueError):
                return None
    return None


def build_components(sheet: dict[str, Any] | None, skill: str, ability: str,
                     extra: dict[str, int] | None = None,
                     rules: dict[str, Any] | None = None) -> dict[str, int]:
    """组装加值明细（键名直接用于展示，零值会被引擎自动跳过）。

    优先级：角色卡写死的 `skill_bonuses` > 属性/熟练/专精推导 > extra 追加。
    """
    table = rules or check_rules.load_rules()
    level = (sheet or {}).get("level", 1)
    canonical = check_rules.canonical_skill(skill, table) or skill
    components: dict[str, int] = {}

    fixed = explicit_skill_bonus(sheet, canonical, table)
    if fixed is not None:
        components["技能总加值"] = fixed
    else:
        components["属性调整"] = ability_modifier(ability_score(sheet, ability))
        prof = proficiency_bonus(level, sheet)
        if has_skill_proficiency(sheet, canonical, table):
            components["熟练加值"] = prof
        expertise = _skill_entries(sheet, "expertise", table)
        if any(_matches(name, canonical, table) for name in expertise):
            components["专精加值"] = prof

    for key, value in (extra or {}).items():
        try:
            components[str(key)] = int(value)
        except (TypeError, ValueError):
            continue
    return components


def attack_components(sheet: dict[str, Any] | None, weapon_name: str = "",
                      extra: dict[str, int] | None = None) -> dict[str, int]:
    """攻击加值：优先用角色卡上写好的命中加值（最忠于角色卡），否则回退“属性+熟练”。"""
    components: dict[str, int] = {}
    attacks = (sheet or {}).get("attacks") or []
    for attack in attacks:
        name = str(attack.get("name") or "")
        if weapon_name and name and weapon_name != name:
            continue
        match = re.search(r"([+-]?\d+)", str(attack.get("bonus") or ""))
        if match:
            components["攻击加值"] = int(match.group(1))
            break
    if not components:
        level = (sheet or {}).get("level", 1)
        best = max((ability_score(sheet, key) for key in ("str", "dex")), default=10)
        components["属性调整"] = ability_modifier(best)
        components["熟练加值"] = proficiency_bonus(level, sheet)
    for key, value in (extra or {}).items():
        try:
            components[str(key)] = int(value)
        except (TypeError, ValueError):
            continue
    return components


def resolve_packet(packet: DecisionPacket, sheet: dict[str, Any] | None = None,
                   d20: int | None = None, extra_components: dict[str, int] | None = None,
                   rules: dict[str, Any] | None = None,
                   target_ac: int | None = None,
                   weapon_name: str = "",
                   display_name: str = "") -> CheckOutcome:
    """把一个 DecisionPacket 结算成可直接展示的检定明细。

    target_ac 给定时走**攻击检定**（d20+命中加值 vs AC），否则走技能/属性检定 vs DC。
    两者共用同一套加值组装与展示格式。
    """
    table = rules or check_rules.load_rules()
    outcome = CheckOutcome(packet=packet)

    if not packet.requires_check:
        outcome.note = "该行动无需检定（判定层已判定）"
        return outcome

    if not packet.skill and target_ac is None:
        outcome.note = "判定层未给出技能项，无法结算"
        return outcome

    skill = check_rules.canonical_skill(packet.skill, table) or packet.skill
    ability = packet.ability or (check_rules.skill_info(skill, table) or {}).get("ability", "")
    display = (display_name or (check_rules.skill_info(skill, table) or {}).get("name", skill)
               or "攻击")

    advantage = ADVANTAGE_MAP.get(str(packet.advantage or ""), None)
    outcome.advantage = advantage

    external = d20 is not None
    if not external:
        rolled = roll_d20(advantage)
        d20 = int(rolled["result"])
        outcome.roll_detail = str(rolled.get("detail", ""))
    else:
        outcome.roll_detail = f"d20: {int(d20)}（外部指定）"
    outcome.d20 = int(d20)

    components = (attack_components(sheet, weapon_name, extra_components)
                  if target_ac is not None
                  else build_components(sheet, skill, ability, extra_components, table))
    outcome.components = components

    engine_result = (
        check_hit_v2(d20_result=int(d20), components=components, defender_ac=int(target_ac),
                     attacker_name=packet.acting_character or "冒险者", weapon_name=weapon_name)
        if target_ac is not None
        else resolve_skill_check(
            d20_result=int(d20),
            components=components,
            dc=int(packet.dc or 15),
            skill_name=display,
            character_name=packet.acting_character or "冒险者",
            advantage=advantage,
        )
    )
    outcome.ran = True
    outcome.hit = engine_result.get("hit")
    outcome.detail_lines = list(engine_result.get("detail_lines", []))
    outcome.summary_line = str(engine_result.get("summary_line", ""))
    if outcome.roll_detail:
        outcome.detail_lines.insert(1, f"  → {outcome.roll_detail}")
    return outcome


def render(outcome: CheckOutcome) -> str:
    """把结果渲染成可直接贴给玩家的文本。"""
    if not outcome.ran:
        return outcome.note or "（未结算）"
    return "\n".join(outcome.detail_lines)

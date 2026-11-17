"""伤害类型与抗性/免疫/易伤结算。

数据来源：
- 怪物：`module_extract` 抽出的 `resistances` / `immunities` / `vulnerabilities` 文本（中文）。
- 角色：角色卡上的装备/提示文本（如“+1火抗鳞甲(火伤减半)”“指温抗性戒指(火伤减半)”）。

约定：内部用中文关键词匹配（与模组文本同源），不引入翻译层。
"""

from __future__ import annotations

import re
from typing import Any

# 规范类型 → 中文同义词（按“具体优先”排序，避免“光”抢先命中“光耀”）
CANON: dict[str, tuple[str, ...]] = {
    "radiant": ("光耀",),
    "necrotic": ("黯蚀", "暗蚀"),
    "thunder": ("雷鸣",),
    "psychic": ("心灵",),
    "force": ("力场",),
    "acid": ("酸",),
    "cold": ("冰", "冷", "寒"),
    "lightning": ("电",),
    "poison": ("毒",),
    "fire": ("火",),
    "bludgeoning": ("钝击", "钝"),
    "piercing": ("穿刺", "刺"),
    "slashing": ("挥砍", "砍", "斩"),
}
_ORDER = ("radiant", "necrotic", "thunder", "psychic", "force", "acid", "cold",
          "lightning", "poison", "fire", "bludgeoning", "piercing", "slashing")

RESIST_WORDS = ("抗", "减半", "抵抗")
IMMUNE_WORDS = ("免疫", "无视", "免伤")


def infer_damage_type(text: Any) -> str:
    """从“1d6+5+酸1d6”“钝击”这类文本推断伤害类型；推不出返回空串。"""
    raw = str(text or "")
    if not raw:
        return ""
    for canonical in _ORDER:
        for word in CANON[canonical]:
            if word in raw:
                return canonical
    return ""


def _matches(text: str, canonical: str) -> bool:
    return any(word in text for word in CANON.get(canonical, ()))


def damage_multiplier(damage_type: str, profile: dict[str, Any] | None) -> tuple[float, str]:
    """按抗性/免疫/易伤返回倍率与说明。"""
    if not damage_type or not profile:
        return 1.0, ""
    immunities = str(profile.get("immunities") or "")
    resistances = str(profile.get("resistances") or "")
    vulnerabilities = str(profile.get("vulnerabilities") or "")

    if _matches(immunities, damage_type):
        return 0.0, "免疫"
    if _matches(vulnerabilities, damage_type):
        return 2.0, "易伤"
    if _matches(resistances, damage_type):
        return 0.5, "抗性"
    return 1.0, ""


def apply_damage_rules(damage: int, damage_type: str,
                       profile: dict[str, Any] | None) -> tuple[int, str]:
    """返回 (结算后伤害, 说明)；说明为空表示无修正。"""
    multiplier, label = damage_multiplier(damage_type, profile)
    if multiplier == 1.0:
        return int(damage), ""
    if multiplier == 0.0:
        return 0, f"{label}（{damage_type}）"
    final = max(0, int(damage * multiplier))
    return final, f"{label}（{damage_type} {damage}→{final}）"


def pc_resistances_from_sheet(sheet: dict[str, Any] | None) -> set[str]:
    """从角色卡的装备/备注文本推断抗性（如“火伤减半”“火抗”）。"""
    if not sheet:
        return set()
    texts: list[str] = []
    for key in ("armor", "gear", "acDetail"):
        texts.append(str(sheet.get(key) or ""))
    for key in ("equipped", "backpack", "items"):
        for item in sheet.get(key) or []:
            if isinstance(item, dict):
                texts.append(str(item.get("name") or "") + str(item.get("bonus") or ""))
            else:
                texts.append(str(item))
    blob = " ".join(texts)
    found: set[str] = set()
    for canonical in _ORDER:
        for word in CANON[canonical]:
            if f"{word}伤减半" in blob or f"{word}抗" in blob or f"{word}伤抗性" in blob:
                found.add(canonical)
                break
    return found


def pc_profile(sheet: dict[str, Any] | None) -> dict[str, str]:
    """把角色卡投影成与怪物同形的档案（只含抗性，供统一结算）。"""
    resistances = pc_resistances_from_sheet(sheet)
    return {"resistances": ",".join(sorted(resistances))} if resistances else {}


def describe_profile(profile: dict[str, Any] | None) -> str:
    """给人看的抗性摘要（诊断用）。"""
    if not profile:
        return "无"
    parts = []
    for key, label in (("immunities", "免疫"), ("resistances", "抗性"),
                       ("vulnerabilities", "易伤")):
        value = str(profile.get(key) or "").strip()
        if value:
            parts.append(f"{label}:{value[:40]}")
    return " | ".join(parts) or "无"

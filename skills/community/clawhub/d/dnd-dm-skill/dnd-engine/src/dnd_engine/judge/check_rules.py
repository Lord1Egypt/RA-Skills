"""检定规则表：动作文本 → (属性, 技能, DC)。

补齐 DM_RULES 规则1.5 引用但缺失的 `检定规则.md`。
优先级：模组原文 DC > 本表 > 默认档位。
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

TABLE_PATH = Path(__file__).with_name("check_rules.json")


@lru_cache(maxsize=1)
def load_rules(path: str | None = None) -> dict[str, Any]:
    table_path = Path(path) if path else TABLE_PATH
    data = json.loads(table_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "skills" not in data or "dc_bands" not in data:
        raise ValueError(f"invalid check rules table: {table_path}")
    return data


def band_dc(band: str, rules: dict[str, Any] | None = None) -> int | None:
    table = rules or load_rules()
    return table["dc_bands"].get(str(band or "").strip().lower())


def skill_info(skill: str, rules: dict[str, Any] | None = None) -> dict[str, Any] | None:
    table = rules or load_rules()
    return table["skills"].get(skill)


def match_action(text: str, rules: dict[str, Any] | None = None) -> dict[str, Any] | None:
    """按关键词命中动作；命中多个时取关键词最长（最具体）的一个。"""
    table = rules or load_rules()
    haystack = str(text or "").lower()
    if not haystack:
        return None
    best: tuple[int, dict[str, Any], str] | None = None
    for action in table.get("actions", []):
        for keyword in action.get("keywords", []):
            needle = str(keyword).lower()
            if needle and needle in haystack:
                if best is None or len(needle) > best[0]:
                    best = (len(needle), action, str(keyword))
    if best is None:
        return None
    action = dict(best[1])
    action["matched_keyword"] = best[2]
    action["source"] = "check_rules"
    return action


def infer_skill(text: str, rules: dict[str, Any] | None = None) -> str | None:
    """动作表没命中时，退一步用技能关键词推断技能。"""
    table = rules or load_rules()
    haystack = str(text or "").lower()
    best: tuple[int, str] | None = None
    for skill, info in table["skills"].items():
        for keyword in info.get("keywords", []):
            needle = str(keyword).lower()
            if needle and needle in haystack:
                if best is None or len(needle) > best[0]:
                    best = (len(needle), skill)
    return best[1] if best else None


def match_skill_name(text: str, rules: dict[str, Any] | None = None) -> str | None:
    """文本中显式出现技能名（如“游说”“医药”）时，直接判定为该技能。

    模组文本常写成“DC 10 的 感知（医药）检定”，其中技能名是最可靠的信号。
    """
    table = rules or load_rules()
    haystack = str(text or "")
    if not haystack:
        return None
    best: tuple[int, str] | None = None
    for skill, info in table["skills"].items():
        name = str(info.get("name") or "")
        if name and name in haystack:
            if best is None or len(name) > best[0]:
                best = (len(name), skill)
    return best[1] if best else None


def _action_for_skill(skill: str, rules: dict[str, Any]) -> dict[str, Any] | None:
    for action in rules.get("actions", []):
        if action.get("skill") == skill:
            return action
    return None


def canonical_skill(name: str, rules: dict[str, Any] | None = None) -> str:
    """把「技能键 / 中文名 / 别名 / 关键词」统一成表里的键。

    例：`stealth` / `隐匿` / `潜行` / `潜藏` / `躲藏` 全部 → `stealth`。
    存在的意义：调用方用中文名传参时（“检定 潜行”），引擎必须能推到正确属性，
    否则会静默回退到属性 10（加值 0）——这是真实踩过的坑。
    """
    table = rules or load_rules()
    text = str(name or "").strip()
    if not text:
        return ""
    skills = table["skills"]
    if text in skills:
        return text
    low = text.lower()
    for key, info in skills.items():
        if str(info.get("name") or "") == text:
            return key
    # 中文名是短词但常写全称（如“隐匿检定”），所以也认包含关系
    for key, info in skills.items():
        official = str(info.get("name") or "")
        if len(official) >= 2 and official in text:
            return key
    for key, info in skills.items():
        aliases = [str(item) for item in (info.get("aliases") or [])]
        if text in aliases or low in [item.lower() for item in aliases]:
            return key
        if any(str(item).lower() in low for item in aliases if item):
            return key
    for key, info in skills.items():
        keywords = [str(item).lower() for item in (info.get("keywords") or [])]
        if low in keywords:
            return key
    hit = lookup(text, text, table)
    return hit.get("skill") or text


def lookup(text: str, skill_hint: str = "", rules: dict[str, Any] | None = None) -> dict[str, Any]:
    """完整查表：返回 {skill, ability, band, dc, tool, source}（未命中时 band=默认档）。

    优先级：显式技能名 > 动作关键词 > 技能关键词 > 传入提示。
    """
    table = rules or load_rules()
    action = match_action(text, table)
    named = match_skill_name(text, table)
    skill = ""
    band = table.get("default_band", "normal")
    tool = ""
    source = "default"
    matched_keyword = ""

    if named:
        skill = named
        related = _action_for_skill(named, table)
        if related:
            band = related.get("band", band)
            tool = related.get("tool", "")
        source = "skill_name"
        if action and action.get("skill") == named:
            matched_keyword = action.get("matched_keyword", "")
    elif action:
        skill = action.get("skill", "")
        band = action.get("band", band)
        tool = action.get("tool", "")
        source = "check_rules"
        matched_keyword = action.get("matched_keyword", "")
    elif skill_hint:
        skill = skill_hint
        source = "skill_hint"
    else:
        inferred = infer_skill(text, table)
        if inferred:
            skill = inferred
            source = "skill_keyword"
    info = skill_info(skill, table) or {}
    return {
        "skill": skill,
        "ability": info.get("ability", ""),
        "skill_name": info.get("name", skill),
        "band": band,
        "dc": band_dc(band, table),
        "tool": tool,
        "source": source,
        "matched_keyword": matched_keyword,
    }

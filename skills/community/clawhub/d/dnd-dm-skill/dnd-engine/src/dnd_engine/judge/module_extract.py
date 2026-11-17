"""模组内容抽取（引擎层）：怪物档案 + 按场景分组的检定表。

放在引擎层的原因：运行时需要“开局自动抽取一次并缓存”，不能依赖 tools/ 脚本。
tools/extract_module_content.py 只是本模块的 CLI 薄壳。
"""

from __future__ import annotations

import json
import pathlib
import re
from typing import Any

# ── 怪物 stat block ──────────────────────────────────────────
NAME_RE = re.compile(r"^>##\s+(.+?)\s*$", re.M)
EN_RE = re.compile(r"^>###\s+([A-Za-z][^\n>]*?)\s*$", re.M)
TYPE_RE = re.compile(r"^>\*(?!\*)(.+?)\*\s*$", re.M)
AC_RE = re.compile(r"^>- \*\*护甲等级\*\*\s*(\d+)", re.M)
HP_RE = re.compile(r"^>- \*\*生命值\*\*\s*(\d+)", re.M)
SPEED_RE = re.compile(r"^>- \*\*速度\*\*\s*(.+?)\s*$", re.M)
INIT_RE = re.compile(r"^>- \*\*先攻\*\*\s*([+-]?\d+)", re.M)
CR_RE = re.compile(r"^>- \*\*CR\*\*\s*([^\s(]+)", re.M)
LINE_FIELD_RES = {
    "resistances": re.compile(r"^>- \*\*抗性\*\*\s*(.+?)\s*$", re.M),
    "immunities": re.compile(r"^>- \*\*免疫\*\*\s*(.+?)\s*$", re.M),
    "vulnerabilities": re.compile(r"^>- \*\*易伤\*\*\s*(.+?)\s*$", re.M),
    "senses": re.compile(r"^>- \*\*感官\*\*\s*(.+?)\s*$", re.M),
    "languages": re.compile(r"^>- \*\*语言\*\*\s*(.+?)\s*$", re.M),
    "proficiency_bonus": re.compile(r"^>- \*\*熟练加值\*\*\s*([+-]?\d+)", re.M),
}
ABILITIES_RE = re.compile(r"^>?\|([^|\n]+)\|([^|\n]+)\|([^|\n]+)\|([^|\n]+)\|([^|\n]+)\|([^|\n]+)\|\s*$", re.M)
ATTACK_RE = re.compile(
    r">\*\*\*(?P<name>[^*]+?)\.\*\*\*[^\n]*?命中\s*(?P<bonus>[+-]?\d+)"
    r"[^\n]*?\*命中:\*\s*(?:(?P<avg>\d+)\s*[（(](?P<dice>\d+d\d+(?:\s*[+-]\s*\d+)?)[)）]|(?P<flat>\d+))"
    r"\s*点?(?P<dtype>[^伤\n]*?)伤害",
)
TRAIT_RE = re.compile(r">\*\*\*(?P<name>[^*]+?)\.\*\*\*\s*(?P<text>[^\n]*)")
MULTI_RE = re.compile(r">\*\*\*多重攻击\.\*\*\*([^\n]*)")
CN_NUM = {"两": 2, "三": 3, "四": 4, "一": 1}
ABILITY_KEYS = ("str", "dex", "con", "int", "wis", "cha")


def _clean(text: Any) -> str:
    return re.sub(r"\s+", "", str(text or ""))


def _parse_speed(raw: str) -> int:
    match = re.search(r"(\d+)", str(raw or ""))
    return int(match.group(1)) if match else 30


def _parse_abilities(text: str) -> dict[str, int]:
    for match in ABILITIES_RE.finditer(text):
        cells = [match.group(i) for i in range(1, 7)]
        values: list[int] = []
        for cell in cells:
            digit = re.search(r"\d+", cell or "")
            if not digit:
                break
            values.append(int(digit.group(0)))
        if len(values) == 6:
            return dict(zip(ABILITY_KEYS, values))
    return {}


def _parse_attacks(text: str) -> list[dict]:
    attacks: list[dict] = []
    seen: set[str] = set()
    for match in ATTACK_RE.finditer(text):
        name = _clean(match.group("name"))
        if not name or name in seen:
            continue
        seen.add(name)
        attacks.append({
            "name": name,
            "bonus": int(match.group("bonus")),
            "dmg": _clean(match.group("dice")) if match.group("dice")
            else f"{int(match.group('flat'))}d1",
            "damage_type": _clean(match.group("dtype")),
        })
    return attacks


def _parse_multiattack(text: str) -> int:
    match = MULTI_RE.search(text)
    if not match:
        return 0
    body = match.group(1)
    digit = re.search(r"(\d+)\s*次", body)
    if digit:
        return int(digit.group(1))
    for word, value in CN_NUM.items():
        if f"{word}次" in body:
            return value
    return 0


def _parse_traits(text: str, attack_names: set[str]) -> list[dict]:
    """非攻击的特性段落（如 不变形态 / 魔法抗性 / 战术纪律）。"""
    traits: list[dict] = []
    for match in TRAIT_RE.finditer(text):
        name = _clean(match.group("name"))
        body = str(match.group("text") or "").strip()
        if not name or name in attack_names or name == "多重攻击":
            continue
        if "命中:" in body or "武器攻击" in body:
            continue
        traits.append({"name": name, "text": body[:200]})
    return traits


def parse_statblock(text: str) -> dict | None:
    """解析一个怪物 stat block；不是怪物块时返回 None。"""
    name_match = NAME_RE.search(text)
    ac = AC_RE.search(text)
    hp = HP_RE.search(text)
    if not (name_match and ac and hp):
        return None

    attacks = _parse_attacks(text)
    profile: dict[str, Any] = {
        "name": _clean(name_match.group(1)),
        "en": _clean(EN_RE.search(text).group(1)) if EN_RE.search(text) else "",
        "kind": _clean(TYPE_RE.search(text).group(1)) if TYPE_RE.search(text) else "",
        "ac": int(ac.group(1)),
        "hp": int(hp.group(1)),
        "speed": _parse_speed(SPEED_RE.search(text).group(1) if SPEED_RE.search(text) else ""),
        "speed_text": _clean(SPEED_RE.search(text).group(1)) if SPEED_RE.search(text) else "",
        "initiative_mod": int(INIT_RE.search(text).group(1)) if INIT_RE.search(text) else 0,
        "cr": _clean(CR_RE.search(text).group(1)) if CR_RE.search(text) else "",
        "abilities": _parse_abilities(text),
        "attacks": attacks or [{"name": "徒手", "bonus": 2, "dmg": "1d4", "damage_type": ""}],
        "multiattack": _parse_multiattack(text),
        "traits": _parse_traits(text, {a["name"] for a in attacks}),
    }
    for field, pattern in LINE_FIELD_RES.items():
        found = pattern.search(text)
        if not found:
            continue
        raw = found.group(1).strip()
        profile[field] = int(raw) if field == "proficiency_bonus" else _clean(raw)
    return profile


# ── 检定表（按场景分组）──────────────────────────────────────
DC_PATTERNS = [
    re.compile(r"DC\s*(\d+)\s*的?\s*([\u4e00-\u9fa5]{1,4})（([\u4e00-\u9fa5]{2,4})）检定"),
    re.compile(r"DC\s*(\d+)\s*的?\s*([\u4e00-\u9fa5]{2,4})检定"),
]
HEADING_RE = re.compile(r"^(#{2,4})\s+(.+?)\s*$", re.M)


def extract_dcs(text: str, rules: dict) -> dict[str, list[dict]]:
    """从模组正文抽出 DC 检定，按最近的上文标题分组。"""
    skill_map = {str(info.get("name")): key for key, info in rules["skills"].items()}
    scenes: dict[str, list[dict]] = {}
    positions = [(m.start(), m.group(2).strip()) for m in HEADING_RE.finditer(text)]

    for pattern in DC_PATTERNS:
        for match in pattern.finditer(text):
            current = "(开头)"
            for pos, title in positions:
                if pos < match.start():
                    current = title
                else:
                    break
            groups = match.groups()
            dc = int(groups[0])
            ability = skill = ""
            if len(groups) >= 3 and groups[1] and groups[2]:
                ability, skill = groups[1], groups[2]
            elif len(groups) >= 2 and groups[1]:
                if groups[1] in skill_map:
                    skill = groups[1]
                else:
                    ability = groups[1]
            key = skill_map.get(skill, "")
            if not key:
                continue
            bucket = scenes.setdefault(current, [])
            if not any(e["skill"] == key and e["dc"] == dc for e in bucket):
                bucket.append({
                    "skill": key, "dc": dc, "match": skill,
                    "note": f"{ability}（{skill}）DC {dc} · {current}",
                })
    return scenes


def extract_all(modules_dir: pathlib.Path, bestiary_dir: pathlib.Path,
                out_dir: pathlib.Path, rules: dict) -> dict[str, Any]:
    """抽取并写出两份产物；返回统计信息。"""
    out_dir.mkdir(parents=True, exist_ok=True)

    encounters: dict[str, dict] = {}
    if bestiary_dir.is_dir():
        for path in sorted(bestiary_dir.glob("*.md")):
            profile = parse_statblock(path.read_text(encoding="utf-8", errors="ignore"))
            if profile and profile["name"]:
                encounters[profile["name"]] = profile
    (out_dir / "module_encounters.json").write_text(
        json.dumps({"version": 2, "source": str(bestiary_dir), "monsters": encounters},
                   ensure_ascii=False, indent=2),
        encoding="utf-8")

    scenes: dict[str, list[dict]] = {}
    for path in sorted(modules_dir.glob("*.md")):
        if "App. D" in path.name or path.name.endswith("-全.md"):
            continue
        for title, entries in extract_dcs(
                path.read_text(encoding="utf-8", errors="ignore"), rules).items():
            bucket = scenes.setdefault(title, [])
            for entry in entries:
                if not any(e["skill"] == entry["skill"] and e["dc"] == entry["dc"]
                           for e in bucket):
                    bucket.append(entry)
    (out_dir / "module_dcs.json").write_text(
        json.dumps({"version": 2, "note": "按场景分组的检定表；运行时取当前场景的条目",
                    "scenes": scenes,
                    "flat": [e for entries in scenes.values() for e in entries]},
                   ensure_ascii=False, indent=2),
        encoding="utf-8")

    fallback = [n for n, p in encounters.items() if p["attacks"][0]["name"] == "徒手"]
    return {
        "monsters": len(encounters),
        "attack_parse_failures": fallback,
        "scenes": len(scenes),
        "dc_entries": sum(len(v) for v in scenes.values()),
    }

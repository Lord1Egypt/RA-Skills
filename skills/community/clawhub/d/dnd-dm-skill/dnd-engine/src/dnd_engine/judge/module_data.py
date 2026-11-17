"""模组数据加载器：把抽取出来的 encounter / 检定表接进判定与战斗流程。

数据由 `tools/extract_module_content.py` 生成：
    reports/module_encounters.json  怪物档案
    reports/module_dcs.json         按场景分组的检定表（version 2）

本模块只负责读取与投影，不改数据、不联网。
"""

from __future__ import annotations

import hashlib
import json
import pathlib
from typing import Any

DEFAULT_REPORTS = pathlib.Path(__file__).resolve().parents[3] / "reports"
DEFAULT_MODULES = pathlib.Path(__file__).resolve().parents[3].parent / "modules"
DEFAULT_BESTIARY = DEFAULT_MODULES / "博德之门_ 坠入阿弗纳斯 - App. D 生物附件"
ENCOUNTERS_FILE = "module_encounters.json"
DCS_FILE = "module_dcs.json"
FINGERPRINT_FILE = "module_fingerprint.json"


def _load(path: pathlib.Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def load_encounters(path: str | pathlib.Path | None = None) -> dict[str, dict]:
    """返回 {怪物名: 档案}；文件缺失时返回空 dict。"""
    file = pathlib.Path(path) if path else DEFAULT_REPORTS / ENCOUNTERS_FILE
    return dict(_load(file).get("monsters") or {})


def enemy_profiles(names: list[str],
                   encounters: dict[str, dict] | None = None) -> list[dict]:
    """把怪物档案投影成战斗用敌人档案（可多个同名）。

    没找到的怪物会被跳过（调用方自行回退）。
    """
    data = encounters if encounters is not None else load_encounters()
    profiles: list[dict] = []
    for name in names:
        monster = data.get(name)
        if not monster:
            continue
        profiles.append({
            "name": monster.get("name", name),
            "hp": int(monster.get("hp") or 1),
            "armor": int(monster.get("ac") or 10),
            "initiative_mod": int(monster.get("initiative_mod") or 0),
            "cr": monster.get("cr", ""),
            "multiattack": int(monster.get("multiattack") or 0),
            # 伤害修正需要带上这三项（否则结算层查不到抗性/免疫）
            "resistances": monster.get("resistances", ""),
            "immunities": monster.get("immunities", ""),
            "vulnerabilities": monster.get("vulnerabilities", ""),
            "attacks": [
                {
                    "name": str(a.get("name") or "徒手"),
                    "bonus": int(a.get("bonus") or 0),
                    "dmg": str(a.get("dmg") or "1d4"),
                    "damage_type": str(a.get("damage_type") or ""),
                }
                for a in (monster.get("attacks") or [])
            ] or [{"name": "徒手", "bonus": 2, "dmg": "1d4", "damage_type": ""}],
        })
    return profiles


def load_dcs(path: str | pathlib.Path | None = None) -> dict[str, Any]:
    """返回检定表原始数据（兼容 v1 扁平数组与 v2 场景分组）。"""
    file = pathlib.Path(path) if path else DEFAULT_REPORTS / DCS_FILE
    return _load(file)


def scenes(data: dict[str, Any] | None = None) -> dict[str, list[dict]]:
    return dict((data if data is not None else load_dcs()).get("scenes") or {})


def dcs_for_scene(scene: str, data: dict[str, Any] | None = None,
                  fallback_all: bool = True) -> list[dict]:
    """取某个场景的检定条目。

    scene 命中（包含关系，大小写不敏感）→ 该场景条目；
    未命中且 fallback_all=True → 全部条目（作为兜底，避免空表）。
    """
    payload = data if data is not None else load_dcs()
    grouped = dict(payload.get("scenes") or {})
    if scene:
        needle = str(scene).strip().lower()
        for title, entries in grouped.items():
            if needle and needle in str(title).lower():
                return list(entries)
    if fallback_all:
        flat = payload.get("flat")
        if isinstance(flat, list):
            return list(flat)
        return [entry for entries in grouped.values() for entry in entries]
    return []


def scene_titles(data: dict[str, Any] | None = None) -> list[str]:
    return sorted((data if data is not None else load_dcs()).get("scenes") or {})


# ────────────────── 场景索引（取代标题模糊匹配）──────────────────

SCENE_INDEX_ENV = "DND_SCENE_INDEX"


def scene_index_candidates() -> list[pathlib.Path]:
    workspace = DEFAULT_REPORTS.parents[2]
    return [
        DEFAULT_REPORTS / "scenes_index.json",
        workspace / "srd" / "scenes_index.json",
        workspace / ".dnd" / "srd" / "scenes_index.json",
        workspace / ".dndskill" / "srd" / "scenes_index.json",
    ]


def scene_index_path() -> pathlib.Path | None:
    import os
    override = os.environ.get(SCENE_INDEX_ENV, "").strip()
    if override:
        path = pathlib.Path(override)
        return path if path.exists() else None
    for candidate in scene_index_candidates():
        if candidate.exists():
            return candidate
    return None


def load_scene_index(path: str | pathlib.Path | None = None) -> dict[str, Any]:
    file = pathlib.Path(path) if path else scene_index_path()
    return _load(file) if file else {}


def index_scene_titles(index: dict[str, Any] | None = None) -> list[str]:
    payload = index if index is not None else load_scene_index()
    titles: list[str] = []
    for key, value in payload.items():
        if key.startswith("_") or not isinstance(value, dict):
            continue
        for scene in value.get("scenes") or []:
            title = str(scene.get("title") or "").strip()
            if title:
                titles.append(title)
    return titles


def current_scene(index: dict[str, Any] | None = None) -> str:
    payload = index if index is not None else load_scene_index()
    return str(payload.get("_current_scene") or "")


def resolve_scene_title(query: str = "", index: dict[str, Any] | None = None) -> str:
    """把用户给的场景名解成索引里的**准确标题**。

    优先级：完全相等 > 包含匹配 > （query 为空时）当前场景。
    """
    titles = index_scene_titles(index)
    needle = str(query or "").strip().lower()
    if needle:
        exact = [t for t in titles if t.lower() == needle]
        if exact:
            return exact[0]
        partial = [t for t in titles if needle in t.lower()]
        if partial:
            return sorted(partial, key=len)[0]
        return ""                     # 未命中不猜，避免掩盖拼写错误
    return current_scene(index)


def dcs_for_query(query: str = "", data: dict[str, Any] | None = None,
                  index: dict[str, Any] | None = None) -> tuple[str, list[dict], str]:
    """返回 (准确场景标题, 该场景检定条目, 来源)。

    来源：scene_index（经索引解析）或 heading_match（回退到标题包含匹配）。
    """
    payload = data if data is not None else load_dcs()
    title = resolve_scene_title(query, index)
    if title:
        entries = dcs_for_scene(title, payload, fallback_all=False)
        if entries:
            return title, entries, "scene_index"
    needle = str(query or "").strip()
    if needle:
        entries = dcs_for_scene(needle, payload, fallback_all=False)
        if entries:
            return needle, entries, "heading_match"
    return "", dcs_for_scene("", payload), "fallback_all"


# ────────────────── 开局自动抽取（带指纹缓存）──────────────────

def source_fingerprint(modules_dir: pathlib.Path | None = None,
                       bestiary_dir: pathlib.Path | None = None) -> str:
    """模组源文件的指纹（名字+大小+mtime），用于判断是否需要重抽。"""
    md = modules_dir or DEFAULT_MODULES
    bd = bestiary_dir or DEFAULT_BESTIARY
    digest = hashlib.sha256()
    for directory in (md, bd):
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("*.md")):
            stat = path.stat()
            digest.update(f"{path.name}:{stat.st_size}:{int(stat.st_mtime)}".encode("utf-8"))
    return digest.hexdigest()


def ensure_extracted(force: bool = False, out_dir: pathlib.Path | None = None,
                     modules_dir: pathlib.Path | None = None,
                     bestiary_dir: pathlib.Path | None = None) -> dict[str, Any]:
    """确保抽取产物是最新的；源文件没变就直接复用（不重抽）。

    返回：{extracted: bool, reason: str, fingerprint: str}
    """
    target = out_dir or DEFAULT_REPORTS
    encounters_path = target / ENCOUNTERS_FILE
    dcs_path = target / DCS_FILE
    fingerprint_path = target / FINGERPRINT_FILE
    current = source_fingerprint(modules_dir, bestiary_dir)

    if not force and encounters_path.exists() and dcs_path.exists() and fingerprint_path.exists():
        try:
            cached = json.loads(fingerprint_path.read_text(encoding="utf-8"))
            if cached.get("fingerprint") == current:
                return {"extracted": False, "reason": "cache_hit", "fingerprint": current}
        except (OSError, json.JSONDecodeError):
            pass

    from . import check_rules, module_extract  # 局部导入，避免循环

    stats = module_extract.extract_all(modules_dir or DEFAULT_MODULES,
                                       bestiary_dir or DEFAULT_BESTIARY,
                                       target, check_rules.load_rules())
    target.mkdir(parents=True, exist_ok=True)
    fingerprint_path.write_text(
        json.dumps({"fingerprint": current, "stats": stats}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    return {"extracted": True, "reason": "stale_or_forced", "fingerprint": current,
            "stats": stats}

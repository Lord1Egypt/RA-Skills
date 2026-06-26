#!/usr/bin/env python3
"""
Skill 发现模块

负责自动扫描所有 claw 平台（aone_copilot、openclaw、qoderwork、agents、iflow 等）
的 skill 安装目录，提供 ISV 技能发现和通用技能查找能力。

从 1688-distribution-distribute-offer 复制
"""

import os
from typing import List

# 项目内置 ISV 技能目录（scripts/isv/providers/）
_PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
_BUILTIN_ISV_DIR = os.path.join(_PROJECT_ROOT, 'scripts', 'isv', 'providers')


def discover_builtin_isv_skills() -> List[dict]:
    """
    发现项目内置的 ISV 技能（scripts/isv/providers/ 下的子目录）。

    每个 ISV 子目录需包含 cli.py，目录名即为 skill 标识（用于匹配 appKey）。

    :return: [{"skill_name": "zhangfei", "skill_path": "/abs/path/...", "builtin": True}, ...]
    """
    results = []
    if not os.path.isdir(_BUILTIN_ISV_DIR):
        return results
    try:
        for entry in sorted(os.listdir(_BUILTIN_ISV_DIR)):
            entry_path = os.path.join(_BUILTIN_ISV_DIR, entry)
            if not os.path.isdir(entry_path):
                continue
            cli_path = os.path.join(entry_path, "cli.py")
            if not os.path.isfile(cli_path):
                continue
            # 目录名直接作为 skill_name（与 Provider 注册名一致）
            skill_name = entry
            results.append({
                "skill_name": skill_name,
                "skill_path": entry_path,
                "builtin": True,
            })
    except Exception:
        pass
    return results


def discover_skill_directories() -> List[str]:
    """
    自动发现所有 claw 平台的 skill 安装目录。

    扫描用户 home 目录下所有以 `.` 开头的隐藏目录，查找包含 `skills` 子目录的平台。
    兼容 aone_copilot、openclaw、qoder、qoderwork、agents、iflow 等各类 claw 平台。

    :return: 所有存在的 skill 目录路径列表
    """
    home_dir = os.path.expanduser("~")
    skill_dirs = []
    try:
        for entry in os.listdir(home_dir):
            if not entry.startswith("."):
                continue
            candidate = os.path.join(home_dir, entry, "skills")
            if os.path.isdir(candidate):
                skill_dirs.append(candidate)
    except Exception:
        pass
    return skill_dirs


def _read_skill_frontmatter(skill_md_path: str) -> dict:
    """
    读取 SKILL.md 的 frontmatter，提取 name 和 description 字段。

    :param skill_md_path: SKILL.md 文件的绝对路径
    :return: {"name": "...", "description": "..."} 或空 dict
    """
    result = {"name": "", "description": ""}
    try:
        with open(skill_md_path, "r", encoding="utf-8") as f:
            in_frontmatter = False
            for _ in range(50):
                line = f.readline()
                if not line:
                    break
                stripped = line.strip()
                if stripped == "---":
                    if not in_frontmatter:
                        in_frontmatter = True
                        continue
                    else:
                        break
                if in_frontmatter:
                    if stripped.startswith("name:"):
                        result["name"] = stripped[len("name:"):].strip()
                    elif stripped.startswith("description:"):
                        result["description"] = stripped[len("description:"):].strip()
    except Exception:
        pass
    return result


def find_isv_skill(app_key: str) -> dict:
    """
    根据 appKey 查找已安装的 ISV 铺货技能。

    按以下优先级查找：
    0. 项目内置 ISV Provider 注册表（scripts/isv/base.py）中按 appKey 匹配
    1. claw 平台 skill 目录名精确匹配 fx-distribute-offer-{appKey}
    2. claw 平台 skill 目录名精确匹配 fx-{appKey}
    3. SKILL.md 的 name 字段精确匹配
    4. SKILL.md 的 description 字段包含该 appKey

    :param app_key: 三方服务商唯一标识（如 "9631867" 或 "9018264"）
    :return: {"found": True, "skill_name": "...", "skill_path": "...", "match_type": "..."}
             或 {"found": False}
    """
    # 优先级 0：从项目内置 ISV Provider 注册表中查找
    try:
        from scripts.isv.base import get_provider_by_appkey
        provider = get_provider_by_appkey(app_key)
        if provider is not None:
            return {
                "found": True,
                "skill_name": provider.name,
                "skill_path": provider.provider_dir,
                "match_type": "builtin_provider",
            }
    except ImportError:
        pass

    skill_search_dirs = discover_skill_directories()
    if not skill_search_dirs:
        return {"found": False}

    target_name = f"fx-distribute-offer-{app_key}"

    # 优先级 1：按目录名精确匹配（最快）
    for skills_dir in skill_search_dirs:
        target_path = os.path.join(skills_dir, target_name)
        if os.path.isdir(target_path):
            return {
                "found": True,
                "skill_name": target_name,
                "skill_path": target_path,
                "match_type": "directory_name",
            }

    # 优先级 2：按目录名匹配 fx-{appKey}
    target_name_v2 = f"fx-{app_key}"
    for skills_dir in skill_search_dirs:
        target_path = os.path.join(skills_dir, target_name_v2)
        if os.path.isdir(target_path):
            return {
                "found": True,
                "skill_name": target_name_v2,
                "skill_path": target_path,
                "match_type": "directory_name_v2",
            }

    # 优先级 3 & 4：遍历所有 skill 目录，读取 SKILL.md
    description_match = None
    for skills_dir in skill_search_dirs:
        try:
            entries = os.listdir(skills_dir)
        except Exception:
            continue
        for entry in entries:
            entry_path = os.path.join(skills_dir, entry)
            if not os.path.isdir(entry_path):
                continue
            skill_md = os.path.join(entry_path, "SKILL.md")
            if not os.path.isfile(skill_md):
                continue

            frontmatter = _read_skill_frontmatter(skill_md)

            # 优先级 3：name 字段精确匹配
            if frontmatter["name"] == target_name:
                return {
                    "found": True,
                    "skill_name": frontmatter["name"],
                    "skill_path": entry_path,
                    "match_type": "name_field",
                }

            # 优先级 4：description 包含 appKey（降级匹配，记录但不立即返回）
            if description_match is None and app_key in frontmatter["description"]:
                description_match = {
                    "found": True,
                    "skill_name": frontmatter["name"] or entry,
                    "skill_path": entry_path,
                    "match_type": "description_contains_appkey",
                }

    if description_match:
        return description_match

    return {"found": False}


def find_skill_by_name(skill_name: str) -> dict:
    """
    根据 skill 名称查找已安装的技能（通用查找）。

    按以下优先级查找：
    0. 项目内置 ISV Provider 注册表中按 name 匹配
    1. claw 平台 skill 目录名精确匹配
    2. SKILL.md 的 name 字段精确匹配

    :param skill_name: 技能名称（如 "zhangfei" 或 "fx-procurement-9018264"）
    :return: {"found": True, "skill_name": "...", "skill_path": "..."}
             或 {"found": False}
    """
    # 优先级 0：从项目内置 ISV Provider 注册表中查找
    try:
        from scripts.isv.base import get_provider_by_name
        provider = get_provider_by_name(skill_name)
        if provider is not None:
            return {"found": True, "skill_name": provider.name, "skill_path": provider.provider_dir}
    except ImportError:
        pass

    skill_search_dirs = discover_skill_directories()
    if not skill_search_dirs:
        return {"found": False}

    # 优先级 1：目录名精确匹配
    for skills_dir in skill_search_dirs:
        target_path = os.path.join(skills_dir, skill_name)
        if os.path.isdir(target_path):
            return {"found": True, "skill_name": skill_name, "skill_path": target_path}

    # 优先级 2：遍历所有 skill 目录，读取 SKILL.md 的 name 字段
    for skills_dir in skill_search_dirs:
        try:
            entries = os.listdir(skills_dir)
        except Exception:
            continue
        for entry in entries:
            entry_path = os.path.join(skills_dir, entry)
            if not os.path.isdir(entry_path):
                continue
            skill_md = os.path.join(entry_path, "SKILL.md")
            if not os.path.isfile(skill_md):
                continue

            frontmatter = _read_skill_frontmatter(skill_md)
            if frontmatter["name"] == skill_name:
                return {"found": True, "skill_name": skill_name, "skill_path": entry_path}

    return {"found": False}


def find_best_isv_skill(tool_list: list) -> dict:
    """
    从 toolList 中查找最优的 ISV 铺货技能。

    遍历所有工具的 appKey，查找是否有对应的 ISV 铺货技能已安装。
    返回第一个匹配的结果。

    :param tool_list: shop_and_tool_info 返回的 toolList
    :return: {"found": True, "app_key": "...", "app_name": "...",
              "skill_name": "...", "skill_path": "...", ...}
             或 {"found": False}
    """
    for tool in tool_list:
        app_key = tool.get("appKey", "")
        if not app_key:
            continue
        result = find_isv_skill(app_key)
        if result.get("found"):
            result["app_key"] = app_key
            result["app_name"] = tool.get("appName", "")
            return result
    return {"found": False}

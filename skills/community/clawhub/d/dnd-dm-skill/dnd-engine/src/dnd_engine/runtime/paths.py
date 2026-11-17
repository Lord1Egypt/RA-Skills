"""SRD 参考目录的定位与加载（可配置 + 自动发现）。

优先级：
1. 调用方显式传入的路径
2. 环境变量 `DND_SRD_DIR`
3. 自动发现：从 dnd-engine 安装位置与当前工作目录向上找 `srd/scripts/search_with_positions.py`
4. 常见 skill 安装位置

找不到时**不抛异常**，返回 None，让上层降级（API 返回明确错误、MCP 提示未安装）。
"""

from __future__ import annotations

import importlib.util
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SRD_ENV = "DND_SRD_DIR"
SEARCH_SCRIPT = "search_with_positions.py"
EXPAND_SCRIPT = "expand_context.py"
MARKER = Path("scripts") / SEARCH_SCRIPT


@dataclass(frozen=True, slots=True)
class SrdModules:
    root: Path
    search: Any
    expand: Any


def _is_srd_root(path: Path) -> bool:
    try:
        return path.is_dir() and (path / MARKER).is_file()
    except OSError:
        return False


def _discovery_roots(start: str | Path | None = None) -> list[Path]:
    """没有显式指定时的自动发现候选（去重、保持顺序）。"""
    roots: list[Path] = []
    bases: list[Path] = []
    if start:
        bases.append(Path(start))
    here = Path(__file__).resolve()
    bases.extend(here.parents[:6])
    cwd = Path.cwd()
    bases.append(cwd)
    bases.extend(list(cwd.parents)[:3])
    home = Path.home()
    bases.append(home / "AppData" / "Roaming" / "LobsterAI" / "SKILLs" / "dnd5e-srd")
    bases.append(home / "AppData" / "Roaming" / "LobsterAI" / "SKILLs")

    for base in bases:
        roots.append(base / "srd")
        roots.append(base)

    unique: list[Path] = []
    seen: set[str] = set()
    for root in roots:
        key = str(root).lower()
        if key not in seen:
            seen.add(key)
            unique.append(root)
    return unique


def candidate_roots(explicit: str | Path | None = None,
                    start: str | Path | None = None) -> list[Path]:
    """按优先级列出候选 SRD 根目录（含显式/环境变量，仅用于诊断）。"""
    roots: list[Path] = []
    if explicit:
        roots.append(Path(explicit))
    env_value = os.environ.get(SRD_ENV)
    if env_value:
        roots.append(Path(env_value))
    roots.extend(_discovery_roots(start))

    unique: list[Path] = []
    seen: set[str] = set()
    for root in roots:
        key = str(root).lower()
        if key not in seen:
            seen.add(key)
            unique.append(root)
    return unique


def resolve_srd_dir(explicit: str | Path | None = None,
                    start: str | Path | None = None) -> Path | None:
    """解析 SRD 根目录。

    显式路径或环境变量一旦给出即为权威（无效则返回 None，不静默改用其他目录）；
    两者都没给时才做自动发现。
    """
    if explicit:
        candidate = Path(explicit)
        return candidate if _is_srd_root(candidate) else None
    env_value = os.environ.get(SRD_ENV)
    if env_value:
        candidate = Path(env_value)
        return candidate if _is_srd_root(candidate) else None
    for root in _discovery_roots(start):
        if _is_srd_root(root):
            return root
    return None


def _load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_srd_modules(explicit: str | Path | None = None,
                     start: str | Path | None = None) -> SrdModules | None:
    """加载 SRD 搜索/展开脚本；不可用时返回 None（不抛异常）。"""
    root = resolve_srd_dir(explicit, start)
    if root is None:
        return None
    scripts = root / "scripts"
    try:
        search = _load_module("srd_search", scripts / SEARCH_SCRIPT)
        expand = _load_module("srd_expand", scripts / EXPAND_SCRIPT)
    except Exception:
        return None
    return SrdModules(root=root, search=search, expand=expand)


def describe_srd(explicit: str | Path | None = None) -> dict[str, Any]:
    """诊断用：返回候选目录与命中情况。"""
    roots = candidate_roots(explicit)
    hit = resolve_srd_dir(explicit)
    return {
        "env_var": SRD_ENV,
        "env_value": os.environ.get(SRD_ENV, ""),
        "resolved": str(hit) if hit else "",
        "candidates": [{"path": str(r), "valid": _is_srd_root(r)} for r in roots[:12]],
    }

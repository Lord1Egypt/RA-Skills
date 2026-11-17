"""cad-file-reader 公共工具：多个脚本共用的纯函数。

只放确定等价的纯函数/输出辅助；各专业差异逻辑仍留在对应脚本。
"""
from __future__ import annotations

import json
import math
import os
import re
import sys
from pathlib import Path
from typing import Any


def compact(value: Any, limit: int = 240) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()[:limit]


def load_rules(path: Path) -> dict[str, Any]:
    """加载规则 JSON；若同目录存在 rules/*.json 主题拆分文件则后合并覆盖。

    主题文件命名有序，加载后同名 dict 做浅层合并、list/标量直接覆盖，
    保持单一 rules.json 兼容旧 CLI。
    """
    if not path.exists():
        raise FileNotFoundError(f"识图规则不存在：{path}")
    with path.open("r", encoding="utf-8") as fh:
        rules = json.load(fh)
    rules_dir = path.parent / "rules"
    if not rules_dir.is_dir():
        return rules
    for jf in sorted(rules_dir.glob("*.json")):
        try:
            with jf.open("r", encoding="utf-8") as fh:
                part = json.load(fh)
        except (OSError, ValueError):
            continue
        for key, val in part.items():
            if isinstance(val, dict) and isinstance(rules.get(key), dict):
                merged = dict(rules[key])
                merged.update(val)
                rules[key] = merged
            else:
                rules[key] = val
    return rules


def pattern_hit(value: str, pattern: Any) -> bool:
    """短 ASCII 代号按边界匹配，避免 AL 误命中 VALVE 等普通单词。"""
    token = str(pattern).upper()
    if re.fullmatch(r"[A-Z]{1,3}", token):
        if re.search(rf"(?<![A-Z0-9]){re.escape(token)}(?![A-Z0-9])", value):
            return True
        return bool(re.search(rf"(?<![A-Z0-9]){re.escape(token)}\d", value))
    return token in value


def match_rule(text: Any, rules: list[dict[str, Any]], key: str) -> tuple[str, dict[str, Any], str]:
    value = compact(text).upper()
    for rule in rules:
        for pattern in rule.get("patterns") or []:
            if pattern_hit(value, pattern):
                return str(rule.get(key) or ""), rule, str(pattern)
    return "", {}, ""


def segment_length(seg: list[Any] | tuple[Any, ...]) -> float:
    try:
        return math.hypot(float(seg[2]) - float(seg[0]), float(seg[3]) - float(seg[1]))
    except (TypeError, ValueError):
        return 0.0


def _psutil_rss_mb() -> int | None:
    """psutil 当前进程 RSS（MB）；不可用时返回 None（Windows 主路径）。"""
    try:
        import psutil
        return int(psutil.Process(os.getpid()).memory_info().rss / 1048576)
    except Exception:
        return None


def peak_rss_mb() -> int:
    """峰值 RSS（MB）：POSIX 用 resource 且按平台单位换算；Windows/阻断时用 psutil。"""
    if sys.platform != "win32":
        try:
            import resource
            rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            if sys.platform == "darwin":
                return int(rss / 1048576)
            if sys.platform.startswith("linux"):
                return int(rss / 1024)
        except Exception:
            pass
    ps = _psutil_rss_mb()
    return ps if ps is not None else 0


def start_mem_guard(name: str = "cad内存闸", default_cap_mb: int = 4096) -> str:
    """挂 mem_guard 内存看门狗，返回状态串（on:<cap>MB / degraded / off / unavailable:...）。

    整档 ezdwg/ezdxf 解析会吃 GB 级内存，曾导致系统卡死；看门狗超限主动 SIGKILL 自己防整机死机。
    它原本只在底座自己的入口（read_cad / convert_dwg / cad_scan）里启动，下游算量 skill
    直接 import 底座 API 时不经过这些入口，看门狗就不在环里 —— 所以这里给下游一个统一挂载点。
    上限取 CAD_MEM_LIMIT_MB，与 cad_scan 同口径。
    """
    try:
        cap = int(os.environ.get("CAD_MEM_LIMIT_MB", str(default_cap_mb)) or 0)
    except ValueError:
        cap = default_cap_mb
    if cap <= 0:
        return "off"
    try:
        here = str(Path(__file__).resolve().parent)
        if here not in sys.path:
            sys.path.insert(0, here)
        import mem_guard
        t = mem_guard.start(cap, name=name)
        return ("on:%dMB" % cap) if t else "degraded"
    except Exception as exc:                      # 看门狗自身失败不应阻断主流程
        return "unavailable:%s" % exc


def file_name(data: dict[str, Any], value: Any) -> str:
    if isinstance(value, dict):
        return compact(value.get("name") or value.get("path"))
    files = data.get("files") or []
    if isinstance(value, int) and 0 <= value < len(files):
        item = files[value]
        return compact(item.get("name") or item.get("path")) if isinstance(item, dict) else compact(item)
    return compact(value)

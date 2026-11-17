#!/usr/bin/env python3
"""稳定入口：联网检索（Tavily）。

共享实现只调用搜索 API 并返回结构化结果；事件归因、产业推演和强弱判断均由
模型完成。成功响应只保留 query 以及结果中的 title / url / published_date /
content；失败响应只保留 query 与结构化 error。本入口同时兼容 canonical 仓库与
Skill Sync 后的独立安装目录。
"""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

SCRIPT_ROOT = Path(__file__).resolve().parent
_CANDIDATES = [
    SCRIPT_ROOT.parents[2] / "shared" / "web_search" / "tavily_search.py",
    SCRIPT_ROOT / "_shared" / "web_search" / "tavily_search.py",
]


def _resolve_target() -> Path:
    for candidate in _CANDIDATES:
        if candidate.exists():
            return candidate
    looked = "\n  ".join(str(candidate) for candidate in _CANDIDATES)
    sys.stderr.write("tavily_search.py not found. Looked in:\n  " + looked + "\n")
    raise SystemExit(2)


if __name__ == "__main__":
    target = _resolve_target()
    sys.argv[0] = str(target)
    runpy.run_path(str(target), run_name="__main__")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""恢复包索引登记：.codex/memory/recovery-index.md 追加一行（按路径去重）。

不可写降级：主索引不可写时自动落到 $TMPDIR/memory-orchestrator/recovery-index.md
（可用 RECOVERY_INDEX_FALLBACK 覆盖），并在输出里标明 storage.primary/fallback。
"""

try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass

import argparse
import json
import os
import tempfile
import time
from pathlib import Path

INDEX = Path(os.environ.get("RECOVERY_INDEX", Path.home() / ".codex" / "memory" / "recovery-index.md"))
STORAGE = {"path": str(INDEX), "mode": "primary"}
HEADER = ["# 恢复包索引", "", "| 项目 | 恢复包路径 | 登记时间 |", "|---|---|---|"]


def _fallback_index():
    p = os.environ.get("RECOVERY_INDEX_FALLBACK")
    if p:
        return Path(p)
    return Path(tempfile.gettempdir()) / "memory-orchestrator" / "recovery-index.md"


def _parent_writable(path):
    try:
        return os.access(str(path.parent), os.W_OK)
    except OSError:
        return False


def _ensure_file(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("\n".join(HEADER) + "\n", encoding="utf-8")


def _write_lines(path, lines):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def resolve_target():
    global STORAGE
    primary = INDEX if _parent_writable(INDEX) else _fallback_index()
    try:
        _ensure_file(primary)
    except (PermissionError, OSError):
        primary = _fallback_index()
        _ensure_file(primary)
    STORAGE = {"path": str(primary), "mode": "primary" if str(primary) == str(INDEX) else "fallback"}
    return primary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--add", nargs=2, metavar=("PROJECT", "PATH"), help="project 与恢复包路径")
    args = ap.parse_args()
    target = resolve_target()

    if args.add:
        project, path = args.add
        lines = target.read_text(encoding="utf-8").splitlines()
        if path not in "".join(lines[2:]):
            ts = time.strftime("%Y-%m-%d %H:%M")
            line = f"| {project} | {path} | {ts} |"
            _write_lines(target, lines + [line])
            result = f"added: {project} -> {path}"
        else:
            result = "already indexed"
        out = {"ok": True, "message": result, "storage": STORAGE}
    else:
        out = {"ok": True, "index": target.read_text(encoding="utf-8"), "storage": STORAGE}
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

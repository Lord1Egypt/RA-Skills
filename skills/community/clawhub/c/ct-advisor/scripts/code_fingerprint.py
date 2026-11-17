#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ct-advisor — 代码版本指纹（2026-10-16）

用途：让 entry.py 的「常驻服务版本探针」覆盖**服务进程真正会加载的全部代码**。

背景（实测发现的盲区）：
  此前 serve.py 只记录 `orchestrate.py` 的 mtime，entry.py 的 server_stale()
  也只比较这一个文件。后果：单独更新 `serve.py` 或 `adapters/**` 时，探针不触发，
  旧服务会**静默地继续跑旧代码** —— 改动看起来「没生效」，且毫无提示。
  （2026-10-16 实测：只 touch serve.py / adapters/refiner.py 时 server_stale() 均为 False。）

做法：把 `scripts/*.py` + `adapters/**/*.py` 的 mtime 取最大值作为代码指纹。
任一文件被更新（`move /Y` 覆盖、编辑器保存）都会让指纹前移，从而触发服务重启。

注意：`config.json` **不纳入**指纹 —— 它由每次 `/ask` 请求实时读取，改了无需重启。

依赖：stdlib-only（glob / os / pathlib）。
"""

from __future__ import annotations

import glob
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent

_PATTERNS = (
    str(SCRIPT_DIR / "*.py"),
    str(SKILL_ROOT / "adapters" / "**" / "*.py"),
)


def collect() -> float:
    """返回代码指纹（相关 .py 文件 mtime 的最大值，单位秒）。

    任何异常（权限、路径失效、并发删除）一律忽略；全失败时返回 0.0。
    """
    mx = 0.0
    for pat in _PATTERNS:
        try:
            files = glob.glob(pat, recursive=True)
        except Exception:  # noqa: BLE001
            continue
        for f in files:
            if "__pycache__" in f:
                continue
            try:
                mt = os.path.getmtime(f)
                if mt > mx:
                    mx = mt
            except Exception:  # noqa: BLE001
                continue
    return mx


if __name__ == "__main__":
    import time

    t0 = time.time()
    fp = collect()
    dt = time.time() - t0
    n = len([f for pat in _PATTERNS for f in glob.glob(pat, recursive=True)
             if "__pycache__" not in f])
    print(f"scanned files : {n}")
    print(f"code_fingerprint: {fp}")
    print(f"as datetime   : {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(fp)) if fp else 'n/a'}")
    print(f"collect() cost: {dt * 1000:.1f} ms")

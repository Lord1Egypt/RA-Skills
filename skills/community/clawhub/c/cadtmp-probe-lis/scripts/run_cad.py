#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Python 统一入口：run_cad.py <子命令> [参数...]（替代 run_cad.sh 自举与分发）。

跨平台设计
----------
- macOS / Linux：保持既有 run_cad.sh 的行为——优先使用本机构建运行时
  （~/.cache/codex-runtimes/*/dependencies/python/bin/python3），
  其次 PATH 上的 python3；找到更优解释器时自动 ``os.execv`` 到它。
- Windows：上述 cache 路径不存在时回退 PATH 的 ``py``/``python3``，
  由 pyboot 定位解释器并配置 PYTHONPATH。
- 内部调用 pyboot（自举/PYTHONPATH）、platform_paths（平台化后端发现）、
  safe_timeout（可选命令级超时）、mem_guard（内存看门狗）。
"""
from __future__ import annotations

import os
import re
import runpy
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"

_GLOBAL_FLAGS = {"--concise", "--full", "--with-evidence"}
_USAGE = (
    "用法: run_cad.py <cad_scan|read_cad|cad_interpret|...> [参数...]\n"
    "      run_cad.py --list           列出全部子命令\n"
    "通用输出选项（所有子命令生效）：--concise / --full / --with-evidence\n"
)


def _prefer_runtime_python() -> str | None:
    """返回比当前解释器更优先的可执行 Python（无则 None）。

    既有的 run_cad.sh 先扫 ~/.cache/codex-runtimes 再回退 PATH；
    这里保持一致，跨平台：Windows 上没有该 cache 目录则直接走 PATH。
    """
    import pyboot

    candidates: list[str] = []
    cache = Path.home() / ".cache" / "codex-runtimes"
    if cache.is_dir():
        candidates.extend(
            str(p) for p in sorted(cache.glob("*/dependencies/python/bin/python3"))
        )
    found = pyboot.find_python()
    if found:
        candidates.append(found)

    chosen: str | None = None
    for cand in candidates:
        if cand and Path(cand).is_file() and os.access(cand, os.X_OK):
            chosen = cand
            break

    # 只返回“第一个可用的最优解释器”；与当前相同则不切换，
    # 避免在两个解释器之间来回 execv（死循环）。
    if chosen and os.path.normcase(os.path.realpath(chosen)) != os.path.normcase(os.path.realpath(sys.executable)):
        return chosen
    return None


def list_subcommands() -> list[str]:
    """与现有 run_cad.sh 一致的子命令集合：扫描薄转发 .sh 的 exec 行。"""
    found: set[str] = set()
    for sh in sorted(SCRIPTS_DIR.glob("*.sh")):
        try:
            text = sh.read_text(encoding="utf-8")
        except OSError:
            continue
        m = re.search(r'/(?:run_cad\.sh|run_cad\.py)"\s+([A-Za-z0-9_]+)', text)
        if m:
            found.add(m.group(1))
    return sorted(found)


def _print_usage() -> None:
    sys.stderr.write(_USAGE)


def main(argv: list[str] | None = None) -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    args = list(sys.argv[1:] if argv is None else argv)

    # 自动切到更优解释器后再真正分发（先处理 --list，避免无谓换解释器）。
    if not args or args[0] not in ("--list", "-h", "--help"):
        better = _prefer_runtime_python()
        if better:
            os.execv(better, [better, str(Path(__file__).resolve())] + args)

    if not args:
        _print_usage()
        return 1

    if args[0] in ("-h", "--help"):
        sys.stdout.write(_USAGE)
        return 0

    if args[0] == "--list":
        for name in list_subcommands():
            print(name)
        return 0

    if args[0].startswith("-") and args[0] not in _GLOBAL_FLAGS:
        _print_usage()
        return 2

    # ---- 全局输出深度：--concise/--full/--with-evidence 翻译为环境变量 ----
    forward: list[str] = []
    for a in args:
        if a == "--concise":
            os.environ["CAD_CONCISE"] = "1"
        elif a in ("--full", "--with-evidence"):
            os.environ["CAD_CONCISE"] = "0"
        else:
            forward.append(a)
    os.environ.setdefault("CAD_CONCISE", "0")
    os.environ.setdefault("CAD_MEM_LIMIT_MB", "4096")

    if not forward:
        _print_usage()
        return 1

    sub = forward[0]
    payload = forward[1:]
    script = SCRIPTS_DIR / f"{sub}.py"
    if not script.is_file():
        sys.stderr.write(
            f"❌ 未知子命令：{sub}\n\n可用子命令（--list）：\n"
            + "\n".join(list_subcommands())
            + "\n"
        )
        return 2

    # ---- 自举 + 看门狗 + 平台化依赖，全部内部启用 ----
    import pyboot

    _boot = pyboot.bootstrap(require_vendor=True)  # vendor 缺失时 exit 3

    import mem_guard
    import platform_paths
    import safe_timeout

    try:
        cap_mb = int(os.environ.get("CAD_MEM_LIMIT_MB", "4096"))
    except ValueError:
        cap_mb = 4096
    mem_guard.start(cap_mb)

    # platform_paths：平台规范化 + 本机 $HOME/.codex 根，供后续平台化子命令参考。
    _ = (platform_paths.normalize_platform(), platform_paths.home_codex())

    real_script = str(script)
    old_argv = sys.argv[:]
    sys.argv = [real_script] + payload
    try:
        timeout = os.environ.get("CAD_CMD_TIMEOUT_SECONDS")
        if timeout:
            try:
                secs = float(timeout)
            except ValueError:
                secs = 0.0
            if secs and secs > 0:
                with safe_timeout.deadline(secs):
                    runpy.run_path(real_script, run_name="__main__")
                return 0
        runpy.run_path(real_script, run_name="__main__")
    finally:
        sys.argv = old_argv
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
FTShare-hk-data 统一调度入口（港股数据）。

用法：
    python run.py <subskill名> [handler参数...]

示例：
    python run.py company-hk --trade_code 00700.HK
    python run.py hk-valuatnanalyd --trade_code 00700.HK --page 1 --page_size 20
    python run.py hk-valuatnanalyd --page 1 --page_size 20
    python run.py hk-view --hk_code 00700.HK
    python run.py hk-candlesticks --trade-code 00700.HK --interval-unit day --until-date 2026-03-24 --since-date 2026-03-01 --limit 20
"""
import os
import runpy
import sys

SKILL_ROOT = os.path.dirname(os.path.abspath(__file__))


def _allowed_subskills():
    """仅允许 sub-skills 目录下存在 scripts/handler.py 的名称，防止路径遍历。"""
    sub_skills_dir = os.path.join(SKILL_ROOT, "sub-skills")
    allowed = set()
    if not os.path.isdir(sub_skills_dir):
        return allowed
    for name in os.listdir(sub_skills_dir):
        if os.path.isfile(os.path.join(sub_skills_dir, name, "scripts", "handler.py")):
            allowed.add(name)
    return allowed


def _execute_handler(handler: str, handler_args: list) -> int:
    """在当前进程执行 handler.py，避免 subprocess 告警。"""
    old_cwd = os.getcwd()
    old_argv = sys.argv[:]
    try:
        os.chdir(SKILL_ROOT)
        sys.argv = [handler] + handler_args
        runpy.run_path(handler, run_name="__main__")
        return 0
    except SystemExit as e:
        code = e.code
        if isinstance(code, int):
            return code
        return 1 if code else 0
    finally:
        sys.argv = old_argv
        os.chdir(old_cwd)


def main():
    sub_skills_dir = os.path.join(SKILL_ROOT, "sub-skills")
    allowed = _allowed_subskills()

    if len(sys.argv) < 2:
        print("用法: python run.py <subskill名> [参数...]", file=sys.stderr)
        print("\n可用 subskill：")
        for name in sorted(allowed):
            print(f"  {name}")
        sys.exit(1)

    subskill = sys.argv[1]
    if subskill not in allowed:
        print(f"错误：未找到 subskill '{subskill}'，或名称不合法。", file=sys.stderr)
        sys.exit(1)

    handler = os.path.join(sub_skills_dir, subskill, "scripts", "handler.py")

    exit_code = _execute_handler(handler, sys.argv[2:])
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

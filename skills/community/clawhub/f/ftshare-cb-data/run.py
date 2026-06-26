#!/usr/bin/env python3
"""
FTShare-cb-data 统一调度入口（可转债数据）。

用法：
    python run.py <subskill名> [handler参数...]

示例：
    python run.py cb-lists
    python run.py cb-base-data --symbol_code 110070.SH
    python run.py cb-candlesticks --symbol 110070.XSHG --interval-unit Day --since-ts-millis 1767225600000 --until-ts-millis 1780272000000 --limit 10
    python run.py get-nth-trade-date --n 5
"""
import os
import subprocess
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

    result = subprocess.run(
        [sys.executable, handler] + sys.argv[2:],
        cwd=SKILL_ROOT,
    )
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()

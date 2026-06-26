#!/usr/bin/env python3
"""
FTShare-etf-data 统一调度入口（ETF 数据）。

用法：
    python run.py <subskill名> [handler参数...]

示例：
    python run.py etf-detail --etf 510050.XSHG
    python run.py etf-list-paginated --order_by "change_rate desc" --page_size 20 --page_no 1
    python run.py etf-ohlcs --etf 510050.XSHG --span DAY1 --limit 50
    python run.py etf-prices --etf 510050.XSHG --since TODAY
    python run.py etf-pcfs --date 20260309
    python run.py etf-pcf-download --filename pcf_159003_20260309.xml --output pcf_159003_20260309.xml
    python run.py etf-component --symbol 510300.XSHG
    python run.py etf-pre-single --symbol 510300.XSHG
    python run.py etf-pre-single --symbol 510300.XSHG --date 20260316
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

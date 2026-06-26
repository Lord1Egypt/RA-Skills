#!/usr/bin/env python3
"""
FTShare-ashare-announcement-data 统一调度入口。

用法：
    python run.py <subskill名> [handler参数...]

示例：
    python run.py stock-announcements-all-stocks-specific-date --start-date 20241231 --page 1 --page-size 20
    python run.py stock-announcements-single-stock-all-periods --stock-code 000001.SZ --page 1 --page-size 20
    python run.py stock-announcements-specific-url-hash --url-hash <hash> --output announcement.pdf
    python run.py stock-reports-all-stocks-specific-date --start-date 20241231 --page 1 --page-size 20
    python run.py stock-reports-single-stock-all-periods --stock-code 000001.SZ --page 1 --page-size 20
    python run.py stock-reports-specific-url-hash --url-hash <hash> --output report.pdf
"""
import os
import subprocess
import sys

SKILL_ROOT = os.path.dirname(os.path.abspath(__file__))


def main():
    if len(sys.argv) < 2:
        print("用法: python run.py <subskill名> [参数...]", file=sys.stderr)
        print("\n可用 subskill：")
        sub_skills_dir = os.path.join(SKILL_ROOT, "sub-skills")
        for name in sorted(os.listdir(sub_skills_dir)):
            script = os.path.join(sub_skills_dir, name, "scripts", "handler.py")
            if os.path.isfile(script):
                print(f"  {name}")
        sys.exit(1)

    subskill = sys.argv[1]
    handler = os.path.join(SKILL_ROOT, "sub-skills", subskill, "scripts", "handler.py")

    if not os.path.isfile(handler):
        print(f"错误：未找到 subskill '{subskill}'，路径不存在：{handler}", file=sys.stderr)
        sys.exit(1)

    result = subprocess.run(
        [sys.executable, handler] + sys.argv[2:],
        cwd=SKILL_ROOT,
    )
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()

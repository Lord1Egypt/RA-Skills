#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_all.py — omni2docx 回归总入口（CI 友好）。

依次跑 docx 矩阵（run_matrix_test.py）、三格式闭环（run_matrix_multi.py）与属性 breakout 专项（run_escape_test.py），
任一非零退出即整体失败。无需参数：python3 tests/run_all.py。
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = sys.executable
SUITES = ["run_matrix_test.py", "run_matrix_multi.py", "run_escape_test.py"]


def main():
    failed = []
    for suite in SUITES:
        print("\n" + "#" * 72)
        print("# SUITE:", suite)
        print("#" * 72)
        rc = subprocess.run([PY, str(HERE / suite)]).returncode
        if rc != 0:
            failed.append(suite)
    print("\n" + "=" * 72)
    if failed:
        print("回归失败：%s" % ", ".join(failed))
        sys.exit(1)
    print("全部回归通过")
    sys.exit(0)


if __name__ == "__main__":
    main()

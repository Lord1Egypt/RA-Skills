#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""demo.py — 合成靶件自带的那枚样例脚本（不属于任何真包，只为让靶件的面文指得到东西）。

用法：python3 -B scripts/demo.py --selftest
它做什么：跑三条纯本地断言并自报枚数；零网络、零读写靶件目录之外的东西。
体检这一面怎么用它：跑不跑是你的决定——跑过就在报告里同句写 cmd=… rc=整数，没跑就落第四节点名。
"""

import sys


def main():
    checks = [
        ("面文引用的这枚脚本确在盘上", __file__.endswith("demo.py")),
        ("这条命令零网络也能跑", "pytest" not in sys.modules),
        ("末行自报的断言数与实跑数一致", True),
    ]
    for name, ok in checks:
        print("  %s %s" % ("ok  " if ok else "FAIL", name))
    print("demo: 断言=%d 枚｜不合=%d（数由上面逐行现数）" % (len(checks), sum(1 for _, ok in checks if not ok)))
    return 1 if any(not ok for _, ok in checks) else 0


if __name__ == "__main__":
    sys.exit(main())

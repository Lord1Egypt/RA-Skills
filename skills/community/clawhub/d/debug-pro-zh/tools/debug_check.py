# -*- coding: utf-8 -*-
"""debug-pro 本地辅助脚本（零依赖，仅打印清单与模板）"""
import sys

CHECKLIST = [
    ("1 复现", "拿到可稳定复现的最小操作序列"),
    ("2 定位层", "判断在 UI/接口/业务/数据/环境哪一层，拿一条证据"),
    ("3 最小化", "删掉无关输入与配置，bug 仍在"),
    ("4 假设", "写 1-3 个可证伪假设（如果 X，则观察到 Y）"),
    ("5 验证", "一次只动一个变量，验证或证伪假设"),
    ("6 修复", "最小改动针对根因，不顺手重构"),
    ("7 回归", "补一条能复现原 bug 的用例，修复前失败、修复后通过"),
]

CARD = """Bug 记录卡
==========
现象：
期望：
实际：
复现步骤（编号）：
环境（OS/版本/浏览器/依赖版本）：
第一条证据（日志/截图/请求）：
已排除的方向：
当前假设：
下一步验证动作：
"""


def main():
    if len(sys.argv) < 2 or sys.argv[1] == "checklist":
        print("7 步调试协议清单：")
        for step, signal in CHECKLIST:
            print(f"  [{step}] 完成信号：{signal}")
        print("\n纪律：第 5 步一次只动一个变量。")
    elif sys.argv[1] == "card":
        print(CARD)
    else:
        print("用法: python debug_check.py [checklist|card]")
        sys.exit(1)


if __name__ == "__main__":
    main()

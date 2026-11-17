#!/usr/bin/env python3
"""预测台账不可篡改守卫（hash 校验，harness 层强制）。

AP-13 要求的核心不变量：预测一旦登记并锁定，不得被事后修改。
本脚本对台账中『预测登记』段落做 hash 封存；发生任何改动即告警。

用法（CI 或 PreToolUse hook 调用）：
    python3 scripts/guard_predictions.py predictions/ledger.md --seal   # 合法登记后封存
    python3 scripts/guard_predictions.py predictions/ledger.md          # 校验
退出码：0 = 一致或首次未封存；1 = 检测到已封存内容被修改。
"""
import hashlib
import re
import sys

MARKER = "预测登记"


def extract_section(text):
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if MARKER in line.lstrip("#").strip():
            start = i
            break
    if start is None:
        return None
    level = len(lines[start]) - len(lines[start].lstrip("#"))
    out = [lines[start]]
    for line in lines[start + 1:]:
        if line.startswith("#"):
            lv = len(line) - len(line.lstrip("#"))
            if lv <= level:
                break
        out.append(line)
    return "\n".join(out).strip()


def digest(section):
    return hashlib.sha256(section.encode("utf-8")).hexdigest()


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    path = argv[1]
    seal = "--seal" in argv
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    section = extract_section(text)
    if section is None:
        print(f"[guard] 未找到『{MARKER}』段落，跳过")
        return 0
    h = digest(section)
    hpath = path + ".sha256"

    if seal:
        with open(hpath, "w", encoding="utf-8") as fh:
            fh.write(h + "\n")
        print(f"[guard] 已封存 {hpath}")
        return 0

    try:
        with open(hpath, encoding="utf-8") as fh:
            sealed = fh.read().strip()
    except FileNotFoundError:
        print("[guard] 尚未封存（首次运行请加 --seal），跳过")
        return 0

    if sealed != h:
        print("[guard] 违规：已封存的『预测登记』被修改。")
        print("        预测一旦锁定不得改写；如需新增，请追加为新条目并重新 --seal。")
        return 1
    print("[guard] 预测登记未被篡改")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
#!/usr/bin/env python3
"""check_code_blocks.py — 校验 Markdown 围栏代码块是否带语言标注、围栏是否配平。

纯标准库、零依赖、只读、确定性：不联网、不修改任何文件、同输入同输出。
规则来源：assets/markdown-lint-rules.json（模板驱动脚本，读取时跳过 "_" 开头的注释键）。

用法:
  python3 scripts/check_code_blocks.py --help
  python3 scripts/check_code_blocks.py --check-rules            # 自检规则文件（必须 0 错误）
  python3 scripts/check_code_blocks.py docs/README.md          # 校验单个文件
  python3 scripts/check_code_blocks.py docs/                    # 递归校验目录

退出码: 0 = 全部合规 / 1 = 发现未标注或配平问题 / 2 = 规则文件无法解析。
"""
import argparse
import json
import os
import re
import sys

DEFAULT_RULES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "markdown-lint-rules.json")

FENCE_RE = re.compile(r"^(`{3,})(.*)$")


def load_rules(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError) as exc:
        print(f"[ERROR] 规则文件无法解析: {path} -> {exc}", file=sys.stderr)
        sys.exit(2)


def visible(data):
    return {k: v for k, v in data.items() if not k.startswith("_")}


def check_rules_schema(rules, path):
    errors = []
    if not isinstance(rules.get("require_code_lang"), bool):
        errors.append("require_code_lang 必须是布尔")
    if not isinstance(rules.get("missing_tokens"), list):
        errors.append("missing_tokens 必须是列表")
    if errors:
        print(f"[FAIL] 规则文件结构校验未通过: {path}", file=sys.stderr)
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
        return 1
    print(f"[OK] 规则文件结构合法: {path}（require_code_lang={rules.get('require_code_lang')}）", file=sys.stderr)
    return 0


def scan_file(path, rules):
    problems = 0
    with open(path, encoding="utf-8", errors="replace") as fh:
        lines = fh.readlines()

    in_block = False
    fence_marks = 0
    lang = None
    start = None
    for i, raw in enumerate(lines, 1):
        line = raw.rstrip("\n")
        m = FENCE_RE.match(line)
        if m:
            if not in_block:
                in_block = True
                fence_marks = len(m.group(1))
                lang = m.group(2).strip()
                start = i
            else:
                if len(m.group(1)) >= fence_marks:  # 闭合
                    in_block = False
                    if rules.get("require_code_lang") and lang == "":
                        print(f"[未标注] {path}:{start} 围栏代码块缺少语言标注", file=sys.stderr)
                        problems += 1
                    in_block = False
                    fence_marks = 0
                    lang = None
                    start = None
    if in_block:
        print(f"[配平] {path}:{start} 围栏代码块未闭合", file=sys.stderr)
        problems += 1
    return problems


def main():
    ap = argparse.ArgumentParser(description="校验 Markdown 代码块语言标注与配平（只读、确定性）")
    ap.add_argument("--rules", default=DEFAULT_RULES, help="规则文件路径（默认 assets/markdown-lint-rules.json）")
    ap.add_argument("--check-rules", action="store_true", help="仅自检规则文件结构，必须 0 错误")
    ap.add_argument("paths", nargs="*", help="待校验的 .md 文件或目录（默认当前目录）")
    args = ap.parse_args()

    rules = visible(load_rules(args.rules))
    if args.check_rules:
        return check_rules_schema(rules, args.rules)

    targets = args.paths or ["."]
    total = 0
    for t in targets:
        if os.path.isdir(t):
            for root, _, files in os.walk(t):
                for fn in files:
                    if fn.endswith(".md"):
                        total += scan_file(os.path.join(root, fn), rules)
        elif t.endswith(".md"):
            total += scan_file(t, rules)
        else:
            print(f"[WARN] 跳过非 .md: {t}", file=sys.stderr)

    if total:
        print(f"\n[FAIL] 发现 {total} 处问题", file=sys.stderr)
        return 1
    print("[OK] 全部代码块已标注且配平", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

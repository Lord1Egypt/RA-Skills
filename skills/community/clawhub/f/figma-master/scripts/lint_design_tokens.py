#!/usr/bin/env python3
"""lint_design_tokens.py — Figma 设计系统规范检查器（纯标准库，零依赖）

检查两类对象，把设计系统评审从"凭感觉"变成可复现的机器检查：
  tokens    校验 Design Token 文件（W3C DTCG 风格）的命名/分类/$type
  variants  校验组件变体命名是否符合 `Component/prop=value` 规范
  selfcheck 校验内置资产（规则配置 + 示例 Token 文件）应为 0 ERROR

规则来源：assets/token_rules.json（配置驱动）。以 `_` 开头的键为注释，加载时跳过。

特性：纯标准库、带 --help、确定性可复现、不联网、只读不修改被检文件。

用法:
  python3 lint_design_tokens.py tokens --file tokens.json
  python3 lint_design_tokens.py variants --file variants.txt
  python3 lint_design_tokens.py selfcheck
  python3 lint_design_tokens.py --help
"""
import argparse
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_RULES = os.path.join(_HERE, "..", "assets", "token_rules.json")
_DEFAULT_EXAMPLE = os.path.join(_HERE, "..", "assets", "design_tokens.example.json")


def _load_rules(path):
    errors = []
    if not os.path.isfile(path):
        return {}, [f"规则配置不存在: {path}"]
    try:
        with open(path, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"规则配置解析失败: {exc}"]
    if not isinstance(raw, dict):
        return {}, ["规则配置根必须是 JSON 对象"]
    rules = {k: v for k, v in raw.items() if not k.startswith("_")}
    if not isinstance(rules.get("allowed_categories"), list) or not rules["allowed_categories"]:
        errors.append("allowed_categories 必须是非空数组")
    if not isinstance(rules.get("allowed_types"), list) or not rules["allowed_types"]:
        errors.append("allowed_types 必须是非空数组")
    try:
        re.compile(rules.get("segment_regex", ""))
    except re.error as exc:
        errors.append(f"segment_regex 非法: {exc}")
    try:
        re.compile(rules.get("variant_regex", ""))
    except re.error as exc:
        errors.append(f"variant_regex 非法: {exc}")
    return rules, errors


def _walk_tokens(node, path, errors, rules):
    """递归遍历 DTCG Token 树，对每个含 $value 的节点做规范检查。"""
    if not isinstance(node, dict):
        return
    if "$value" in node:
        seg = re.compile(rules.get("segment_regex", r"^[a-zA-Z0-9][a-zA-Z0-9-]*$"))
        cats = set(rules.get("allowed_categories", []))
        types = set(rules.get("allowed_types", []))
        full = ".".join(path)
        for part in path:
            if not seg.match(part):
                errors.append(f"Token '{full}': 段 '{part}' 不符合命名规则（无 _/空格，可含 -）")
        if path and path[0] not in cats:
            errors.append(f"Token '{full}': 首段 '{path[0]}' 不在受控分类 {sorted(cats)}")
        t = node.get("$type")
        if t is not None and t not in types:
            errors.append(f"Token '{full}': $type '{t}' 不在允许类型 {sorted(types)}")
        if not str(node.get("$value", "")).strip():
            errors.append(f"Token '{full}': $value 为空")
        return
    for key, child in node.items():
        _walk_tokens(child, path + [key], errors, rules)


def _check_tokens(text, rules):
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return [f"Token 文件不是合法 JSON: {exc}"]
    errors = []
    _walk_tokens(data, [], errors, rules)
    return errors


def _check_variants(text, rules):
    pat = re.compile(rules.get("variant_regex", r"^[A-Z][A-Za-z0-9]*/[a-z][a-zA-Z0-9-]*=[a-z0-9-]+$"))
    errors = []
    for ln in text.splitlines():
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        if not pat.match(s):
            errors.append(f"变体名不合规: '{s}' (期望 Component/prop=value，组件首字母大写、值小写)")
    return errors


def _read_file_or_die(path):
    if not os.path.isfile(path):
        sys.stderr.write(f"[ERROR] 文件不存在: {path}\n")
        sys.exit(2)
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def main(argv=None):
    ap = argparse.ArgumentParser(description="Figma 设计系统规范检查器（tokens / variants / selfcheck）")
    ap.add_argument("--rules", default=_DEFAULT_RULES, help="规则配置 JSON 路径")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_t = sub.add_parser("tokens", help="校验 Design Token 文件")
    p_t.add_argument("--file", required=True, help="Token JSON 文件路径")

    p_v = sub.add_parser("variants", help="校验组件变体命名")
    p_v.add_argument("--file", required=True, help="变体清单文件路径（每行一个）")

    sub.add_parser("selfcheck", help="校验内置资产（规则+示例 Token）应为 0 ERROR")

    args = ap.parse_args(argv)

    if args.cmd == "selfcheck":
        rules, rerr = _load_rules(args.rules)
        print(f"[selfcheck] 规则 {os.path.relpath(args.rules)} : "
              f"{'OK' if not rerr else rerr}")
        ex_err = _check_tokens(_read_file_or_die(_DEFAULT_EXAMPLE), rules) if os.path.isfile(_DEFAULT_EXAMPLE) else ["示例 Token 文件缺失"]
        print(f"[selfcheck] 示例 Token 文件 {os.path.relpath(_DEFAULT_EXAMPLE)} : "
              f"{'0 ERROR' if not ex_err else ex_err}")
        total = len(rerr) + len(ex_err)
        if total == 0:
            print("[selfcheck] PASS — 资产与脚本互相验证通过（0 ERROR）")
            return 0
        print(f"[selfcheck] FAIL — 共 {total} 项错误")
        return 1

    rules, rerr = _load_rules(args.rules)
    if rerr:
        for e in rerr:
            sys.stderr.write(f"[ERROR] {e}\n")
        return 2

    if args.cmd == "tokens":
        errs = _check_tokens(_read_file_or_die(args.file), rules)
        if errs:
            for e in errs:
                print(f"ERROR: {e}")
            print(f"\nToken 检查未通过：{len(errs)} 项")
            return 1
        print("Token 检查通过：0 ERROR")
        return 0

    if args.cmd == "variants":
        errs = _check_variants(_read_file_or_die(args.file), rules)
        if errs:
            for e in errs:
                print(f"ERROR: {e}")
            print(f"\n变体检查未通过：{len(errs)} 项")
            return 1
        print("变体检查通过：0 ERROR")
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())

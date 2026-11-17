#!/usr/bin/env python3
"""
validate_product_feed.py — 确定性商品信息流（product feed）校验器

用途
----
把一个商品信息流（CSV 或 JSON）按 assets/product-feed-rules.json 中声明的
「必填字段 + 缺失令牌 + 类型/枚举约束」逐条校验，输出结构化问题清单。
同一输入永远产生同一输出（确定性、可复现）。

设计约束（Level A 硬要求）
-------------------------
- 纯 Python 标准库，零第三方依赖，不联网。
- 只读被检查的文件，绝不修改输入文件或规则模板。
- 模板中以 `_` 开头的键（_comment / _note 等注释与元信息）一律跳过，
  不会被当成字段或规则。
- 支持 --help；不带 --feed 时进入「规则自检」模式，校验模板自身是否自洽。

用法
----
  # 校验一个商品信息流（默认读 assets/product-feed-rules.json）
  python3 scripts/validate_product_feed.py --feed products.csv
  python3 scripts/validate_product_feed.py --feed products.json --rules my-rules.json

  # 规则模板自检（确认 bundled 模板自洽，应产出 0 错误）
  python3 scripts/validate_product_feed.py

退出码
------
  0  无问题
  1  发现问题（信息流有缺陷，或规则模板不自洽）
  2  参数/文件错误
"""

import argparse
import csv
import json
import os
import sys

VALID_TYPES = ("string", "number", "enum")
DEFAULT_RULES = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "assets", "product-feed-rules.json"
)


def load_rules(path):
    """读取并解析规则模板（JSON）。不修改文件。"""
    with open(path, "r", encoding="utf-8-sig") as fh:
        return json.load(fh)


def is_underscore_key(key):
    return isinstance(key, str) and key.startswith("_")


def self_check_rules(rules):
    """校验规则模板自身是否自洽。返回错误字符串列表（空 = 自洽）。

    只检查非 `_` 前缀的业务键；注释与元信息键被跳过。
    """
    errors = []
    if not isinstance(rules, dict):
        return ["rules root must be a JSON object"]

    active = {k: v for k, v in rules.items() if not is_underscore_key(k)}

    required_fields = active.get("required_fields")
    if not isinstance(required_fields, list) or not required_fields:
        errors.append("required_fields 必须是非空数组")
    else:
        seen = set()
        for idx, field in enumerate(required_fields):
            if not isinstance(field, dict):
                errors.append(f"required_fields[{idx}] 必须是对象")
                continue
            name = field.get("name")
            if not isinstance(name, str) or not name:
                errors.append(f"required_fields[{idx}].name 必须是非空字符串")
                continue
            if is_underscore_key(name):
                errors.append(f"required_fields[{idx}].name 不能以 '_' 开头: {name}")
            if name in seen:
                errors.append(f"required_fields 存在重复字段名: {name}")
            seen.add(name)
            ftype = field.get("type")
            if ftype not in VALID_TYPES:
                errors.append(f"字段 '{name}' 的 type 必须是 {VALID_TYPES} 之一，实际: {ftype!r}")
            if ftype == "enum":
                allowed = field.get("allowed")
                if not isinstance(allowed, list) or not allowed:
                    errors.append(f"枚举字段 '{name}' 必须声明非空的 allowed 列表")

    missing_tokens = active.get("missing_tokens")
    if not isinstance(missing_tokens, list) or not missing_tokens:
        errors.append("missing_tokens 必须是非空数组")
    else:
        for tok in missing_tokens:
            if not isinstance(tok, str) or tok == "":
                errors.append(f"missing_tokens 元素必须是非空字符串，实际: {tok!r}")

    return errors


def load_feed(path):
    """读取 CSV 或 JSON 商品流，统一返回 list[dict]。不修改文件。"""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".json":
        with open(path, "r", encoding="utf-8-sig") as fh:
            data = json.load(fh)
        if isinstance(data, dict):
            for key in ("products", "items", "data"):
                if isinstance(data.get(key), list):
                    return data[key]
            return [data]
        if isinstance(data, list):
            return data
        raise ValueError("JSON feed 必须是对象数组或含 products/items/data 数组的对象")

    # 默认按 CSV 处理（也兼容 .tsv 等，但这里仅 csv 形态）
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        return [dict(row) for row in reader]


def check_value(name, ftype, allowed, value, missing_tokens):
    """返回 None（通过）或问题描述字符串。"""
    if value is None:
        return f"字段 '{name}' 缺失（列不存在）"
    text = str(value).strip()
    if text == "":
        return f"字段 '{name}' 为空"
    if text in missing_tokens:
        return f"字段 '{name}' 等于缺失令牌 '{text}'"
    if ftype == "number":
        try:
            float(text)
        except ValueError:
            return f"字段 '{name}' 不是合法数字: '{text}'"
    elif ftype == "enum":
        if text not in allowed:
            return f"字段 '{name}' 不在允许枚举 {allowed} 中: '{text}'"
    return None


def validate_feed(records, rules):
    """逐条校验。返回 (issues, checked)。issues 为 dict 列表。"""
    active = {k: v for k, v in rules.items() if not is_underscore_key(k)}
    missing_tokens = set(active.get("missing_tokens", []))
    required_fields = active.get("required_fields", [])

    issues = []
    for i, record in enumerate(records):
        line_no = i + 2  # CSV: 第 1 行是表头
        if not isinstance(record, dict):
            issues.append({"line": line_no, "field": "<row>", "problem": "记录不是对象"})
            continue
        for field in required_fields:
            name = field["name"]
            ftype = field.get("type", "string")
            allowed = field.get("allowed", []) if ftype == "enum" else []
            raw = record.get(name)
            problem = check_value(name, ftype, allowed, raw, missing_tokens)
            if problem:
                issues.append({"line": line_no, "field": name, "problem": problem})
    return issues


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="确定性商品信息流校验器（CSV/JSON），按 assets 规则模板检查必填字段与取值质量。"
    )
    ap.add_argument("--feed", help="待校验的商品信息流文件（CSV 或 JSON）。省略则仅自检规则模板。")
    ap.add_argument(
        "--rules",
        default=DEFAULT_RULES,
        help="规则模板路径（默认 assets/product-feed-rules.json）。",
    )
    ap.add_argument("--quiet", action="store_true", help="只输出问题数与退出码。")
    args = ap.parse_args(argv)

    if not os.path.isfile(args.rules):
        print(f"[ERROR] 规则模板不存在: {args.rules}", file=sys.stderr)
        return 2

    try:
        rules = load_rules(args.rules)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"[ERROR] 规则模板解析失败: {exc}", file=sys.stderr)
        return 2

    # 规则模板自检（无论是否校验 feed 都先跑，bundled 模板应为 0 错误）
    rule_errors = self_check_rules(rules)
    if rule_errors:
        print(f"[RULE ERROR] 规则模板不自洽 ({len(rule_errors)} 处):")
        for e in rule_errors:
            print(f"  - {e}")
        return 1

    if not args.feed:
        if not args.quiet:
            print(f"[OK] 规则模板自洽: {args.rules}")
        return 0

    if not os.path.isfile(args.feed):
        print(f"[ERROR] 信息流文件不存在: {args.feed}", file=sys.stderr)
        return 2

    try:
        records = load_feed(args.feed)
    except (OSError, ValueError, json.JSONDecodeError, csv.Error) as exc:
        print(f"[ERROR] 信息流解析失败: {exc}", file=sys.stderr)
        return 2

    issues = validate_feed(records, rules)

    if args.quiet:
        print(f"issues: {len(issues)}")
        return 1 if issues else 0

    print(f"校验信息流: {args.feed}  (共 {len(records)} 条记录)")
    if not issues:
        print("未发现任何问题。")
        return 0

    print(f"发现 {len(issues)} 处问题：")
    for it in issues:
        print(f"  [line {it['line']}] {it['field']}: {it['problem']}")
    print(f"issues found: {len(issues)}")
    return 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
输入参数净化：代码级白名单过滤 + 类型校正 + 默认值填充。

Agent 从用户消息中提取参数后，MUST 将提取结果传入本脚本做强制净化。
脚本只保留 schema 白名单字段，丢弃一切非标内容，输出规范化 JSON。

用法:
    echo '{"topic":"三国","duration_sec":"120","skip_plan":true}' | python extract_params.py
    python extract_params.py --input raw_params.json
    python extract_params.py --input raw_params.json --output clean_params.json

输出 JSON:
    {
      "valid": true,
      "input_params": { ... 净化后的参数 ... },
      "dropped_fields": ["skip_plan"],
      "corrections": ["duration_sec: '120' -> 120 (str→int)"],
      "errors": []
    }

退出码: 0 = 净化成功, 1 = 有致命错误(如 topic 缺失), 2 = IO 错误
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

SCHEMA: dict[str, dict[str, Any]] = {
    "topic":             {"type": "str",  "required": True,  "default": None},
    "full_script":       {"type": "str",  "required": False, "default": ""},
    "industry":          {"type": "str",  "required": False, "default": ""},
    "platform":          {"type": "str",  "required": False, "default": "douyin"},
    "style":             {"type": "str",  "required": False, "default": "观点型口播"},
    "duration_sec":      {"type": "int",  "required": False, "default": 60,
                          "min": 15, "max": 300},
    "use_avatar":        {"type": "bool", "required": False, "default": True},
    "subtitle_required": {"type": "bool", "required": False, "default": False},
}

PLACEHOLDER_TOPICS = {"你好", "test", "测试", "hello", "hi", "xxx", "aaa", "123"}


def _coerce(value: Any, spec: dict) -> tuple[Any, str | None]:
    """尝试将 value 转为 spec 指定的类型，返回 (转换后值, 修正说明或None)。"""
    target = spec["type"]

    if target == "str":
        if not isinstance(value, str):
            return str(value), f"'{value}' -> str"
        return value, None

    if target == "int":
        if isinstance(value, int) and not isinstance(value, bool):
            return value, None
        if isinstance(value, float) and value == int(value):
            v = int(value)
            return v, f"{value} -> {v} (float→int)"
        if isinstance(value, str):
            value = value.strip()
            for suffix in ("秒", "s", "sec", "分钟"):
                if value.endswith(suffix):
                    value = value[: -len(suffix)].strip()
                    break
            try:
                v = int(float(value))
                return v, f"'{spec.get('_orig', value)}' -> {v} (str→int)"
            except (TypeError, ValueError):
                pass
        return None, None

    if target == "bool":
        if isinstance(value, bool):
            return value, None
        if isinstance(value, str):
            low = value.strip().lower()
            if low in ("true", "yes", "1", "是"):
                return True, f"'{value}' -> true"
            if low in ("false", "no", "0", "否"):
                return False, f"'{value}' -> false"
        if isinstance(value, (int, float)):
            return bool(value), f"{value} -> {bool(value)}"
        return None, None

    return value, None


def sanitize(raw: dict) -> dict:
    """
    对原始 dict 做白名单过滤 + 类型校正 + 默认值填充。
    返回 {"valid", "input_params", "dropped_fields", "corrections", "errors"}
    """
    errors: list[str] = []
    corrections: list[str] = []
    dropped: list[str] = []
    clean: dict[str, Any] = {}

    allowed_keys = set(SCHEMA.keys())
    for k in raw:
        if k not in allowed_keys:
            dropped.append(k)

    for field, spec in SCHEMA.items():
        if field in raw:
            val = raw[field]
            coerced, note = _coerce(val, spec)
            if coerced is None:
                errors.append(f"{field}: 无法转为 {spec['type']}（值: {val!r}）")
                continue
            if note:
                corrections.append(f"{field}: {note}")
            clean[field] = coerced
        elif spec["required"]:
            errors.append(f"{field}: 必填字段缺失")
        else:
            clean[field] = spec["default"]

    topic = (clean.get("topic") or "").strip()
    if topic:
        clean["topic"] = topic
        if len(topic) < 5:
            errors.append(f"topic 太短（{len(topic)} 字 < 5）: '{topic}'")
        if topic.lower() in PLACEHOLDER_TOPICS:
            errors.append(f"topic 疑似占位串: '{topic}'")

    dur = clean.get("duration_sec")
    if isinstance(dur, int):
        mn, mx = SCHEMA["duration_sec"]["min"], SCHEMA["duration_sec"]["max"]
        if not (mn <= dur <= mx):
            errors.append(f"duration_sec={dur} 不在 [{mn}, {mx}]")

    valid = len(errors) == 0
    return {
        "valid": valid,
        "input_params": clean,
        "dropped_fields": dropped,
        "corrections": corrections,
        "errors": errors,
    }


def main():
    parser = argparse.ArgumentParser(
        description="一键成片输入参数白名单净化"
    )
    parser.add_argument(
        "--input", default="-",
        help="Agent 提取的原始 JSON（默认 stdin）",
    )
    parser.add_argument(
        "--output", default=None,
        help="净化后 input_params JSON 输出路径（省略则打印到 stdout）",
    )
    args = parser.parse_args()

    try:
        if args.input == "-":
            raw_text = sys.stdin.read()
        else:
            with open(args.input, encoding="utf-8") as f:
                raw_text = f.read()
        raw = json.loads(raw_text)
    except (OSError, json.JSONDecodeError) as exc:
        result = {
            "valid": False,
            "input_params": {},
            "dropped_fields": [],
            "corrections": [],
            "errors": [f"输入解析失败: {exc}"],
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(2)

    result = sanitize(raw)

    if args.output and result["valid"]:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result["input_params"], f, ensure_ascii=False, indent=2)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()

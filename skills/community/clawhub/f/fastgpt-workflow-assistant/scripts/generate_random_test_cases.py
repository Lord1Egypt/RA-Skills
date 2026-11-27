#!/usr/bin/env python3
"""基于应用功能画像生成可复现的随机回归用例。"""

from __future__ import annotations

import argparse
import json
import random
import re
from pathlib import Path
from typing import Any


PLACEHOLDER_PATTERN = re.compile(r"\{[A-Za-z_][A-Za-z0-9_]*\}")
EXPECTATION_FIELDS = (
    "expected_route", "expected_substrings", "expected_any_groups",
    "required_nodes", "forbidden_nodes", "min_answer_chars", "min_node_count",
    "max_answer_chars", "max_latency_ms", "max_distinct_ipv4", "max_distinct_mac",
    "expected_fallback_substrings", "runtime_failure_substrings",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", type=Path, help="应用功能画像 JSON")
    parser.add_argument("output", type=Path, help="输出测试用例 JSON")
    parser.add_argument("--seed", type=int, default=None, help="随机种子，便于复现")
    parser.add_argument("--count", type=int, default=20, help="最终输出用例总数")
    return parser.parse_args()


def load_profile(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as stream:
        data = json.load(stream)
    if not isinstance(data, dict):
        raise ValueError("功能画像必须是对象")
    topics = data.get("topics")
    templates = data.get("question_templates")
    if not isinstance(topics, list) or not topics or not all(isinstance(v, dict) for v in topics):
        raise ValueError("功能画像必须包含非空 topics 对象数组")
    if not isinstance(templates, list) or not templates:
        raise ValueError("功能画像必须包含非空 question_templates 数组")
    for item in templates:
        if not isinstance(item, (str, dict)):
            raise ValueError("question_templates 只允许字符串或对象")
        if isinstance(item, dict) and not str(item.get("template", "")).strip():
            raise ValueError("对象模板必须包含非空 template")
    return data


def template_text(template: str | dict[str, Any]) -> str:
    return str(template.get("template", "")) if isinstance(template, dict) else str(template)


def render_template(
    template: str, topic: dict[str, Any], profile: dict[str, Any], rng: random.Random
) -> str:
    keywords = topic.get("keywords") if isinstance(topic.get("keywords"), list) else []
    entities = topic.get("entities") if isinstance(topic.get("entities"), list) else []
    invalid_pool = profile.get("invalid_input_pool") if isinstance(profile.get("invalid_input_pool"), list) else []
    invalid_value = str(rng.choice(invalid_pool)) if invalid_pool else "无效输入"
    replacements = {
        "{topic}": str(topic.get("name", "示例主题")),
        "{keyword}": str(rng.choice(keywords)) if keywords else str(topic.get("name", "示例主题")),
        "{entity}": str(rng.choice(entities)) if entities else str(profile.get("entity_fallback", "相关对象")),
        "{invalid}": invalid_value,
        "{bad}": invalid_value,
        "{empty}": "",
    }
    rendered = template
    for marker, value in replacements.items():
        rendered = rendered.replace(marker, value)
    unresolved = PLACEHOLDER_PATTERN.findall(rendered)
    if unresolved:
        raise ValueError(f"问题模板包含未支持占位符：{unresolved}")
    return rendered.strip()


def expected_behavior(template: str, spec: dict[str, Any]) -> str:
    explicit = str(spec.get("expected_behavior", "")).strip().lower()
    if explicit:
        if explicit not in {"normal", "fallback", "error"}:
            raise ValueError(f"未知 expected_behavior：{explicit!r}")
        return explicit
    return "normal"


def _copy_expectations(turn: dict[str, Any], topic: dict[str, Any], spec: dict[str, Any]) -> None:
    for field in EXPECTATION_FIELDS:
        value = spec.get(field, topic.get(field))
        if value not in (None, "", []):
            turn[field] = value


def _fallback_markers(profile: dict[str, Any]) -> list[str]:
    values = profile.get("fallback_markers", ["未找到", "无法", "请联系", "稍后"])
    return [str(v) for v in values] if isinstance(values, list) else []


def build_case(
    index: int, profile: dict[str, Any], topic: dict[str, Any],
    template: str | dict[str, Any], rng: random.Random,
) -> dict[str, Any]:
    spec = template if isinstance(template, dict) else {}
    raw_template = template_text(template)
    behavior = expected_behavior(raw_template, spec)
    turn: dict[str, Any] = {
        "question": render_template(raw_template, topic, profile, rng),
        "expected_behavior": behavior,
        "forbidden_substrings": [str(v) for v in profile.get("forbidden_substrings", [])],
        "max_latency_ms": int(profile.get("default_max_latency_ms", 8000)),
        "max_answer_chars": int(profile.get("default_max_answer_chars", 2000)),
    }
    _copy_expectations(turn, topic, spec)
    if behavior == "fallback":
        turn.setdefault("expected_fallback_substrings", _fallback_markers(profile))
    return {
        "case_id": f"random-{index:03d}-{topic.get('id', 'topic')}",
        "category": str(spec.get("category", "random-generated")),
        "turns": [turn],
    }


def _build_invalid_case(index: int, value: Any, profile: dict[str, Any]) -> dict[str, Any]:
    fallback_markers = _fallback_markers(profile)
    return {
        "case_id": f"random-invalid-{index:03d}",
        "category": "random-invalid-input",
        "turns": [{
            "question": str(value),
            "expected_behavior": "normal",
            "expected_any_groups": [fallback_markers] if fallback_markers else [],
            "forbidden_substrings": [str(v) for v in profile.get("forbidden_substrings", [])],
            "max_latency_ms": int(profile.get("default_max_latency_ms", 8000)),
            "max_answer_chars": int(profile.get("default_max_answer_chars", 2000)),
        }],
    }


def generate_cases(profile: dict[str, Any], count: int, rng: random.Random) -> list[dict[str, Any]]:
    if count < 1:
        raise ValueError("count 必须大于 0")
    topics = profile["topics"]
    templates = profile["question_templates"]
    invalid_pool = list(profile.get("invalid_input_pool", [])) if isinstance(profile.get("invalid_input_pool"), list) else []
    rng.shuffle(invalid_pool)
    invalid_count = min(len(invalid_pool), count)
    random_count = count - invalid_count
    cases = [
        build_case(index, profile, rng.choice(topics), rng.choice(templates), rng)
        for index in range(1, random_count + 1)
    ]
    cases.extend(
        _build_invalid_case(index, value, profile)
        for index, value in enumerate(invalid_pool[:invalid_count], 1)
    )
    return cases


def main() -> int:
    args = parse_args()
    try:
        if args.output.exists():
            raise FileExistsError(f"拒绝覆盖已有文件：{args.output.resolve()}")
        profile = load_profile(args.profile)
        cases = generate_cases(profile, args.count, random.Random(args.seed))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(cases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}")
        return 1
    print(f"OK: {args.output.resolve()}")
    print(f"CASES: {len(cases)}")
    print(f"SEED: {args.seed if args.seed is not None else 'random'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""从登记的 FastGPT 工作流模板生成候选可导入 JSON。"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TEMPLATE = SKILL_ROOT / "assets" / "workflow-templates" / "fastgpt-v481-minimal.json"
FLAT_TEMPLATE = SKILL_ROOT / "assets" / "workflow-templates__fastgpt-v481-minimal.json"
if not DEFAULT_TEMPLATE.is_file() and FLAT_TEMPLATE.is_file():
    DEFAULT_TEMPLATE = FLAT_TEMPLATE


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="输出 JSON；为避免误覆盖，文件必须不存在")
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--welcome-text", default="您好，请描述您的问题。")
    parser.add_argument("--reply-text", default="工作流已成功导入，请继续配置业务分支。")
    parser.add_argument("--value", action="append", default=[], metavar="KEY=VALUE", help="补充模板占位符，可重复")
    return parser.parse_args()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as stream:
        return json.load(stream)


def parse_values(items: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"--value 必须使用 KEY=VALUE：{item!r}")
        key, value = item.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError("占位符名称不能为空")
        result[key] = value
    return result


def replace(value: Any, replacements: dict[str, str]) -> Any:
    if isinstance(value, dict):
        return {key: replace(child, replacements) for key, child in value.items()}
    if isinstance(value, list):
        return [replace(child, replacements) for child in value]
    if isinstance(value, str):
        result = value
        for key, replacement in replacements.items():
            result = result.replace("{{" + key + "}}", replacement)
        return result
    return value


def generate(template: Path, output: Path, replacements: dict[str, str]) -> dict[str, Any]:
    template = template.resolve()
    output = output.resolve()
    if not template.is_file():
        raise FileNotFoundError(template)
    if output.exists():
        raise FileExistsError(f"拒绝覆盖已有文件：{output}")
    data = replace(load_json(template), replacements)
    if not isinstance(data, dict) or not isinstance(data.get("nodes"), list) or not isinstance(data.get("edges"), list):
        raise ValueError("模板必须包含 nodes 和 edges 数组")
    unresolved = re.findall(r"\{\{[A-Za-z0-9_-]+\}\}", json.dumps(data, ensure_ascii=False))
    if unresolved:
        raise ValueError(f"仍有未替换占位符：{sorted(set(unresolved))}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return data


def main() -> int:
    args = parse_args()
    replacements = {"WELCOME_TEXT": args.welcome_text, "REPLY_TEXT": args.reply_text}
    try:
        replacements.update(parse_values(args.value))
        data = generate(args.template, args.output, replacements)
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}")
        return 1
    print(f"OK: {args.output.resolve()}")
    print(f"NODES: {len(data['nodes'])}")
    print(f"EDGES: {len(data['edges'])}")
    print("STATUS: candidate-importable; target platform validation required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

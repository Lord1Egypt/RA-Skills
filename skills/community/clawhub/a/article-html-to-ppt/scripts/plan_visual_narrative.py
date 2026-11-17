#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from visual_narrative.planner import DEFAULT_STYLE_ID, plan_visual_narrative


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "visual-plan.schema.json"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return data


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="将故事线编译为 PPT Smith 视觉叙事计划。")
    parser.add_argument("--task-route", required=True, type=Path, help="task-route.json 路径")
    parser.add_argument("--audience-route", type=Path, help="已通过门禁的 audience-route.json 路径")
    parser.add_argument("--storyline", required=True, type=Path, help="含证据引用的 storyline JSON 路径")
    parser.add_argument("--style-id", default=DEFAULT_STYLE_ID, help="视觉系统 style id")
    parser.add_argument("--output", required=True, type=Path, help="visual-plan.json 输出路径")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = plan_visual_narrative(
        load_json(args.task_route),
        load_json(args.storyline),
        args.style_id,
        audience_route=load_json(args.audience_route) if args.audience_route else None,
    )
    schema = load_json(SCHEMA_PATH)
    Draft202012Validator(schema).validate(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from visual_narrative.task_router import route_task


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "task-route.schema.json"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return data


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Route analyzed content into a visual narrative task.")
    parser.add_argument("--analysis", required=True, type=Path, help="Path to content analysis JSON.")
    parser.add_argument("--explicit-route", default=None, help="Optional explicit route override hint.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("task-route.json"),
        help="Path to write task-route.json output.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    analysis = load_json(args.analysis)
    result = route_task(analysis, explicit_route=args.explicit_route)
    schema = load_json(SCHEMA_PATH)
    Draft202012Validator(schema).validate(result)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

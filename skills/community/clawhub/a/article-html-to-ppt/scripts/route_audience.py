#!/usr/bin/env python3
"""Validate a source-context brief and produce one audience-route decision."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from visual_narrative.audience_router import route_audience


ROOT = Path(__file__).resolve().parents[1]
BRIEF_SCHEMA = ROOT / "schemas" / "source-context-brief.schema.json"
ROUTE_SCHEMA = ROOT / "schemas" / "audience-route.schema.json"


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return data


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Route one source document to one professional PPT narrative.")
    parser.add_argument("--brief", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    brief = load_json(args.brief)
    Draft202012Validator(load_json(BRIEF_SCHEMA)).validate(brief)
    result = route_audience(brief)
    Draft202012Validator(load_json(ROUTE_SCHEMA)).validate(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if result["status"] == "ready" else 2


if __name__ == "__main__":
    raise SystemExit(main())

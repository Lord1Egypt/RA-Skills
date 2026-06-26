#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from typing import Any, List, Tuple

SECTIONS: List[Tuple[str, str]] = [
    ("architecture_inventory", "architecture_inventory"),
    ("failure_mode_map", "failure_mode_map"),
    ("architecture_test_plan", "architecture_test_plan"),
    ("optimization_roadmap", "optimization_roadmap"),
    ("measurement_plan", "measurement_plan"),
    ("architecture_recommendation", "architecture_recommendation"),
]


def render_value(value: Any) -> List[str]:
    if isinstance(value, list):
        return [f"- {item}" for item in value] if value else ["- None provided"]
    if value in (None, ""):
        return ["- None provided"]
    return [str(value)]


def render_review(data: dict) -> str:
    lines = ["# Architecture Review", ""]
    for title, key in SECTIONS:
        lines.append(f"## {title}")
        lines.extend(render_value(data.get(key)))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Render an architecture review from JSON.")
    parser.add_argument("input", help="Path to JSON input")
    parser.add_argument("--out", help="Optional Markdown output path")
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text())
    output = render_review(data)
    if args.out:
        Path(args.out).write_text(output)
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

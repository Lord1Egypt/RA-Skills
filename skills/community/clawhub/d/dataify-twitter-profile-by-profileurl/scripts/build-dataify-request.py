#!/usr/bin/env python3

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List


def load_catalog(script_dir: Path) -> List[Dict[str, Any]]:
    catalog_path = script_dir.parent / "references" / "tool-params.json"
    return json.loads(catalog_path.read_text(encoding="utf-8"))


def find_tool(catalog: List[Dict[str, Any]], tool_sign: str) -> Dict[str, Any]:
    for tool in catalog:
        if tool.get("tool_sign") == tool_sign:
            return tool
    raise SystemExit(f"Unknown tool_sign: {tool_sign}")


def load_values(values_file: Path) -> List[Dict[str, Any]]:
    payload = json.loads(values_file.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        return [payload]
    if isinstance(payload, list):
        return payload
    raise SystemExit("values file must be a JSON object or JSON array")


def map_select_labels(tool: Dict[str, Any], rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    param_defs = {item["param"]: item for item in tool.get("params", [])}
    mapped_rows: List[Dict[str, Any]] = []
    for row in rows:
        mapped: Dict[str, Any] = {}
        for key, value in row.items():
            param_def = param_defs.get(key)
            final_value = value
            if param_def and param_def.get("input_mode") == "select":
                for option in param_def.get("options", []):
                    if value in {
                        option.get("label"),
                        option.get("submitted_value"),
                        option.get("raw_value"),
                        option.get("raw_type_value"),
                    }:
                        final_value = option.get("submitted_value")
                        break
            mapped[key] = final_value
        mapped_rows.append(mapped)
    return mapped_rows


def build_curl(tool: Dict[str, Any], spider_parameters_json: str) -> str:
    token = os.environ.get("DATAIFY_API_TOKEN", "").strip()
    if not token:
        raise SystemExit(
            "DATAIFY_API_TOKEN is not set. Sign in at https://dashboard.dataify.com?utm_source=skill to obtain it, then export it as an environment variable."
        )

    parts = [
        "curl -X POST 'https://scraperapi.dataify.com/builder'",
        f"  -H 'Authorization: Bearer {token}'",
        "  -H 'Content-Type: application/x-www-form-urlencoded'",
        f"  -d 'spider_name={tool['spider_name']}'",
        f"  -d 'spider_id={tool['tool_sign']}'",
        f"  -d 'spider_parameters={spider_parameters_json}'",
        "  -d 'spider_errors=true'",
        "  -d 'file_name={{TasksID}}'",
    ]
    return " \\\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a Dataify builder curl request.")
    parser.add_argument("--tool-sign", required=True, help="Selected tool sign.")
    parser.add_argument("--values-file", required=True, help="Path to a JSON object or array with spider parameter values.")
    parser.add_argument("--print-spider-parameters-only", action="store_true", help="Print only the normalized spider_parameters JSON.")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    catalog = load_catalog(script_dir)
    tool = find_tool(catalog, args.tool_sign)
    rows = load_values(Path(args.values_file).resolve())
    normalized = map_select_labels(tool, rows)
    spider_parameters_json = json.dumps(normalized, ensure_ascii=False, separators=(",", ":"))

    if args.print_spider_parameters_only:
        print(spider_parameters_json)
        return 0

    print(build_curl(tool, spider_parameters_json))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

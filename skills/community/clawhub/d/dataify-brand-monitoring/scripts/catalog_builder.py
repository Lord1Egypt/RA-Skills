#!/usr/bin/env python3
"""Shared catalog-driven Builder submission CLI with final-result completion."""

import argparse
import json
import os
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request

from task_runtime import complete_task, extract_task_id


BUILDER_URL = "https://scraperapi.dataify.com/builder?platform=1"


def load_catalog(script_dir):
    return json.loads((Path(script_dir).parent / "references" / "tool-params.json").read_text(encoding="utf-8"))


def find_tool(catalog, tool_sign):
    for tool in catalog:
        if tool.get("tool_sign") == tool_sign:
            return tool
    raise ValueError("Unknown tool_sign: {}".format(tool_sign))


def load_rows(values_file=None, params_json=None):
    if params_json:
        payload = json.loads(params_json)
    elif values_file:
        payload = json.loads(Path(values_file).read_text(encoding="utf-8"))
    else:
        raise ValueError("Provide --params-json or --values-file with the required target values.")
    rows = [payload] if isinstance(payload, dict) else payload
    if not isinstance(rows, list) or not rows or not all(isinstance(row, dict) for row in rows):
        raise ValueError("Parameters must be a non-empty JSON object or array of objects.")
    return rows


def map_select_labels(tool, rows):
    definitions = {item["param"]: item for item in tool.get("params", [])}
    normalized = []
    for row in rows:
        mapped = {}
        for key, value in row.items():
            definition = definitions.get(key, {})
            final = value
            if definition.get("input_mode") == "select":
                for option in definition.get("options", []):
                    if value in {option.get("label"), option.get("submitted_value"), option.get("raw_value"), option.get("raw_type_value")}:
                        final = option.get("submitted_value")
                        break
            mapped[key] = final
        normalized.append(mapped)
    return normalized


def validate_required(tool, rows):
    required = [item["param"] for item in tool.get("params", []) if item.get("required") is True]
    for index, row in enumerate(rows, 1):
        missing = [key for key in required if row.get(key) in (None, "", [])]
        if missing:
            raise ValueError("Parameter set {} is missing required values: {}".format(index, ", ".join(missing)))


def build_curl(tool, spider_parameters_json):
    return " \\\n".join([
        "curl -X POST '{}'".format(BUILDER_URL),
        "  -H 'Authorization: Bearer $DATAIFY_API_TOKEN'",
        "  -H 'Content-Type: application/x-www-form-urlencoded'",
        "  -d 'spider_name={}'".format(tool["spider_name"]),
        "  -d 'spider_id={}'".format(tool["tool_sign"]),
        "  -d 'spider_parameters={}'".format(spider_parameters_json),
        "  -d 'spider_errors=true'",
        "  -d 'file_name={{TasksID}}'",
    ])


def submit(tool, rows, token):
    form = {
        "spider_name": tool["spider_name"],
        "spider_id": tool["tool_sign"],
        "spider_parameters": json.dumps(rows, ensure_ascii=False, separators=(",", ":")),
        "spider_errors": "true",
        "file_name": "{{TasksID}}",
    }
    request = urllib.request.Request(
        BUILDER_URL,
        data=urllib.parse.urlencode(form).encode("utf-8"),
        headers={"Authorization": "Bearer {}".format(token), "Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError("Builder request failed with HTTP {}: {}".format(exc.code, exc.read().decode("utf-8", errors="replace")))
    except urllib.error.URLError as exc:
        raise RuntimeError("Builder request failed: {}".format(exc.reason))
    task_id = extract_task_id(payload)
    if not task_id:
        detail = payload.get("data") if isinstance(payload, dict) else payload
        raise RuntimeError("Builder did not return a valid task_id: {}".format(json.dumps(detail, ensure_ascii=False)))
    return task_id


def run_catalog_builder(script_dir):
    parser = argparse.ArgumentParser(description="Submit a catalog-driven Dataify task and return its final result.")
    parser.add_argument("--tool-sign", required=True)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--params-json", help="JSON object or array containing required target values.")
    source.add_argument("--values-file", help="JSON file containing required target values.")
    parser.add_argument("--preview", action="store_true", help="Print the normalized request without submitting it.")
    parser.add_argument("--no-wait", action="store_true", help="Return task_id immediately after submission.")
    parser.add_argument("--wait-timeout", type=float, default=600)
    args = parser.parse_args()
    try:
        tool = find_tool(load_catalog(script_dir), args.tool_sign)
        rows = map_select_labels(tool, load_rows(args.values_file, args.params_json))
        validate_required(tool, rows)
    except (ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    payload_json = json.dumps(rows, ensure_ascii=False, separators=(",", ":"))
    if args.preview:
        print(build_curl(tool, payload_json))
        return 0
    token = os.environ.get("DATAIFY_API_TOKEN", "").strip()
    if not token:
        parser.error("DATAIFY_API_TOKEN is not configured. Configure it in your environment; never paste it into chat.")
    try:
        task_id = submit(tool, rows, token)
        if args.no_wait:
            print(json.dumps({"task_id": task_id, "status": "submitted"}, ensure_ascii=False))
        else:
            print(json.dumps(complete_task(task_id, token, args.wait_timeout), ensure_ascii=False, indent=2))
    except RuntimeError as exc:
        parser.error(str(exc))
    return 0

#!/usr/bin/env python3

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional


def main() -> None:
    try:
        args = parse_cli_args(sys.argv[1:])
        artifact_path = require_arg(args, "--artifact")
        tool_name = require_arg(args, "--tool")
        args_file = require_arg(args, "--args-file")
        debug = is_debug_enabled(os.environ.get("AICADE_GALAXY_DEBUG"))

        artifact = json.loads(Path(artifact_path).read_text(encoding="utf-8"))
        payload = json.loads(Path(args_file).read_text(encoding="utf-8"))

        if not isinstance(payload, dict):
            raise RuntimeError("--args-file must contain a JSON object.")

        log_debug(
            debug,
            {
                "event": "invoke.input",
                "artifactPath": artifact_path,
                "tool": tool_name,
                "argsFile": args_file,
                "payload": payload,
            },
        )
        result = invoke_artifact_tool(artifact, tool_name, payload)
        log_debug(
            debug,
            {
                "event": "invoke.output",
                "artifactPath": artifact_path,
                "tool": tool_name,
                "result": result,
            },
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0 if result["ok"] else 1)
    except Exception as exc:  # noqa: BLE001
        print(str(exc), file=sys.stderr)
        sys.exit(1)


def invoke_artifact_tool(artifact: dict, tool_name: str, payload: dict) -> dict:
    tool = find_tool(artifact, tool_name)
    split = split_payload(payload)

    validate_args(tool, split["args"])
    validate_response_paths(tool, split["responsePaths"])

    url = join_base_url(artifact["baseUrl"], tool["metadata"]["path"])
    headers = {
        "Accept": "application/json",
    }
    apply_auth_header(tool, headers)

    method = tool["metadata"]["method"]
    body = None
    if method == "GET":
        url = apply_query_params(url, split["args"])
    else:
        headers["Content-Type"] = "application/json"
        body = json.dumps(split["args"]).encode("utf-8")

    request = urllib.request.Request(url, headers=headers, method=method, data=body)

    try:
        with urllib.request.urlopen(request) as response:
            status = response.status
            text = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        status = exc.code
        text = exc.read().decode("utf-8", errors="replace")

    raw = parse_maybe_json(text)
    if status >= 400:
        return {
            "ok": False,
            "status": status,
            "tool": tool["name"],
            "serviceId": tool["metadata"]["serviceId"],
            "error": {
                "message": build_error_message(status, raw),
                "raw": raw,
            },
        }

    return {
        "ok": True,
        "status": status,
        "tool": tool["name"],
        "serviceId": tool["metadata"]["serviceId"],
        "data": select_response_data(raw, split["responsePaths"]),
        "raw": raw,
    }


def parse_cli_args(argv: List[str]) -> Dict[str, str]:
    if len(argv) == 0 or len(argv) % 2 != 0:
        raise RuntimeError(
            "Usage: python3 scripts/invoke_artifact.py --artifact <path> --tool <name> --args-file <path>"
        )

    result: Dict[str, str] = {}
    for index in range(0, len(argv), 2):
        key = argv[index]
        value = argv[index + 1]
        if not key.startswith("--"):
            raise RuntimeError(
                "Usage: python3 scripts/invoke_artifact.py --artifact <path> --tool <name> --args-file <path>"
            )
        result[key] = value
    return result


def require_arg(args: Dict[str, str], key: str) -> str:
    value = args.get(key)
    if not value:
        raise RuntimeError(f"Missing required argument {key}.")
    return value


def find_tool(artifact: dict, tool_name: str) -> dict:
    tools = artifact.get("tools")
    if not isinstance(tools, list):
        raise RuntimeError("Invalid artifact format.")

    for tool in tools:
        if isinstance(tool, dict) and tool.get("name") == tool_name:
            return tool

    raise RuntimeError(f'Tool "{tool_name}" was not found in artifact.')


def split_payload(payload: dict) -> dict:
    args = {key: value for key, value in payload.items() if key != "responsePaths"}
    response_paths = payload.get("responsePaths", [])
    if not isinstance(response_paths, list) or any(
        not isinstance(item, str) or len(item) == 0 for item in response_paths
    ):
        raise RuntimeError('"responsePaths" must be an array of non-empty strings.')
    return {
        "args": args,
        "responsePaths": response_paths,
    }


def validate_args(tool: dict, args: dict) -> None:
    input_schema = tool.get("inputSchema", {})
    required = input_schema.get("required", [])
    properties = input_schema.get("properties", {})

    for key in required:
        if key not in args or args[key] is None:
            raise RuntimeError(f'Missing required parameter "{key}" for tool "{tool["name"]}".')

    if input_schema.get("additionalProperties") is False:
        for key in args:
            if key not in properties:
                raise RuntimeError(f'Unknown parameter "{key}" for tool "{tool["name"]}".')

    for key, value in args.items():
        property_schema = properties.get(key)
        if isinstance(property_schema, dict):
            validate_value_type(tool["name"], key, value, property_schema)


def validate_value_type(tool_name: str, key: str, value, property_schema: dict) -> None:
    expected_type = property_schema.get("type")
    if value is None or not expected_type:
        return

    valid = (
        (expected_type == "string" and isinstance(value, str))
        or (expected_type == "number" and isinstance(value, (int, float)) and not isinstance(value, bool))
        or (expected_type == "integer" and isinstance(value, int) and not isinstance(value, bool))
        or (expected_type == "boolean" and isinstance(value, bool))
        or (expected_type == "object" and isinstance(value, dict))
        or (expected_type == "array" and isinstance(value, list))
    )

    if not valid:
        raise RuntimeError(
            f'Invalid parameter "{key}" for tool "{tool_name}": expected {expected_type}.'
        )


def validate_response_paths(tool: dict, response_paths: List[str]) -> None:
    response_fields = tool.get("metadata", {}).get("responseFields", [])
    if len(response_paths) == 0 or not isinstance(response_fields, list):
        return

    available = set(response_fields)
    for response_path in response_paths:
        if response_path not in available:
            raise RuntimeError(
                f'Unknown response path "{response_path}" for tool "{tool["name"]}".'
            )


def apply_auth_header(tool: dict, headers: Dict[str, str]) -> None:
    auth = tool.get("metadata", {}).get("authentication", {})
    env_name = auth.get("envName")
    header_name = auth.get("headerName")
    required = auth.get("required", False)
    value = os.environ.get(env_name, "") if isinstance(env_name, str) else ""

    if required and not value:
        raise RuntimeError(
            f'Missing required environment variable: {env_name} for tool "{tool["name"]}".'
        )

    if value and isinstance(header_name, str):
        headers[header_name] = value


def apply_query_params(url: str, args: dict) -> str:
    parsed = urllib.parse.urlparse(url)
    existing = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    extra = [(key, stringify_query_value(value)) for key, value in args.items() if value is not None]
    query = urllib.parse.urlencode(existing + extra)
    return urllib.parse.urlunparse(parsed._replace(query=query))


def stringify_query_value(value) -> str:
    if isinstance(value, (str, int, float, bool)) and not isinstance(value, dict):
        return str(value)
    return json.dumps(value, ensure_ascii=False)


def parse_maybe_json(text: str):
    if len(text) == 0:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def build_error_message(status: int, raw) -> str:
    if isinstance(raw, dict):
        if isinstance(raw.get("message"), str) and raw["message"]:
            return raw["message"]
        error = raw.get("error")
        if isinstance(error, dict) and isinstance(error.get("message"), str):
            return error["message"]

    if isinstance(raw, str) and raw:
        return raw

    return f"Request failed with HTTP {status}."


def select_response_data(data, response_paths: List[str]):
    if len(response_paths) == 0:
        return data
    if len(response_paths) == 1:
        return get_value_by_path(data, response_paths[0])

    result = {}
    for path in response_paths:
        result = merge_selected_values(result, build_selected_structure(data, tokenize_path(path)))
    return result


def get_value_by_path(data, path: str):
    return get_value_by_tokens(data, tokenize_path(path))


def build_selected_structure(data, tokens: List[str]):
    if len(tokens) == 0:
        return data

    current = tokens[0]
    rest = tokens[1:]

    if current == "[]":
        if not isinstance(data, list):
            return None
        return [build_selected_structure(item, rest) for item in data]

    if not isinstance(data, dict):
        return None

    selected_child = build_selected_structure(data.get(current), rest)
    if selected_child is None:
        return None
    return {current: selected_child}


def get_value_by_tokens(data, tokens: List[str]):
    if len(tokens) == 0:
        return data

    current = tokens[0]
    rest = tokens[1:]

    if current == "[]":
        if not isinstance(data, list):
            return None
        return [get_value_by_tokens(item, rest) for item in data]

    if not isinstance(data, dict):
        return None

    return get_value_by_tokens(data.get(current), rest)


def tokenize_path(path: str) -> List[str]:
    return [item for item in path.replace("[]", ".[]").split(".") if item]


def merge_selected_values(left, right):
    if right is None:
        return left
    if left is None:
        return right

    if isinstance(left, list) and isinstance(right, list):
        length = max(len(left), len(right))
        return [
            merge_selected_values(
                left[index] if index < len(left) else None,
                right[index] if index < len(right) else None,
            )
            for index in range(length)
        ]

    if isinstance(left, dict) and isinstance(right, dict):
        result = dict(left)
        for key, value in right.items():
            result[key] = (
                merge_selected_values(result.get(key), value)
                if key in result
                else value
            )
        return result

    return right


def join_base_url(base_url: str, path: str) -> str:
    normalized_base = base_url.rstrip("/")
    normalized_path = path if path.startswith("/") else f"/{path}"
    return f"{normalized_base}{normalized_path}"


def is_debug_enabled(value: Optional[str]) -> bool:
    return bool(value) and value.lower() == "true"


def log_debug(enabled: bool, payload: dict) -> None:
    if not enabled:
        return
    print(f"[AICADE_GALAXY_DEBUG] {json.dumps(payload, ensure_ascii=False, indent=2)}")


if __name__ == "__main__":
    main()

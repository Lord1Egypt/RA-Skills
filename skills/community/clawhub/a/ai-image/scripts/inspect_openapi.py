#!/usr/bin/env python3
"""Inspect skills.video generation OpenAPI contracts and emit endpoint-ready summaries."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

DEFAULT_CATEGORY = "images"
METHOD_AND_PATH_RE = re.compile(r"^(GET|POST|PUT|PATCH|DELETE)\s+(.+)$", re.IGNORECASE)


def read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"File not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}")


def find_group_nodes(node: Any, group_name: str) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    if isinstance(node, dict):
        if node.get("group") == group_name and isinstance(node.get("pages"), list):
            matches.append(node)
        for value in node.values():
            matches.extend(find_group_nodes(value, group_name))
    elif isinstance(node, list):
        for item in node:
            matches.extend(find_group_nodes(item, group_name))
    return matches


def collect_method_paths(node: Any) -> list[str]:
    rows: list[str] = []
    if isinstance(node, str):
        match = METHOD_AND_PATH_RE.match(node.strip())
        if match:
            method = match.group(1).upper()
            path = match.group(2).strip()
            if method == "POST" and path.startswith("/generation/"):
                rows.append(f"{method} {path}")
    elif isinstance(node, dict):
        if "pages" in node:
            rows.extend(collect_method_paths(node["pages"]))
    elif isinstance(node, list):
        for item in node:
            rows.extend(collect_method_paths(item))
    return rows


def unique_in_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            output.append(item)
    return output


def list_endpoints_from_docs(docs: dict[str, Any], category: str) -> list[str]:
    group_name = "Videos" if category == "videos" else "Images"
    rows: list[str] = []
    for group in find_group_nodes(docs, group_name):
        rows.extend(collect_method_paths(group.get("pages", [])))
    return unique_in_order(rows)


def parse_endpoint_arg(endpoint: str) -> tuple[str, str]:
    endpoint = endpoint.strip()
    match = METHOD_AND_PATH_RE.match(endpoint)
    if match:
        return match.group(1).upper(), match.group(2).strip()
    return "POST", endpoint


def try_paths(path: str) -> list[str]:
    candidates = [path]
    if path.startswith("/v1/"):
        candidates.append(path[3:])
    elif path.startswith("/"):
        candidates.append(f"/v1{path}")
    else:
        candidates.append(f"/v1/{path}")
    return unique_in_order(candidates)


def resolve_operation(openapi: dict[str, Any], method: str, path: str) -> tuple[str, dict[str, Any]]:
    paths = openapi.get("paths", {})
    for candidate in try_paths(path):
        operations = paths.get(candidate)
        if isinstance(operations, dict) and method.lower() in operations:
            operation = operations[method.lower()]
            if isinstance(operation, dict):
                return candidate, operation
    raise SystemExit(f"Endpoint not found in OpenAPI: {method} {path}")


def endpoint_exists(openapi: dict[str, Any], method: str, path: str) -> bool:
    operations = openapi.get("paths", {}).get(path)
    return isinstance(operations, dict) and method.lower() in operations


def to_sse_path(path: str) -> str:
    if "/generation/sse/" in path:
        return path
    return path.replace("/generation/", "/generation/sse/", 1)


def to_polling_path(path: str) -> str:
    return path.replace("/generation/sse/", "/generation/", 1)


def find_sse_create_endpoint(openapi: dict[str, Any], method: str, resolved_path: str) -> str | None:
    sse_candidate = to_sse_path(resolved_path)
    if endpoint_exists(openapi, method, sse_candidate):
        return sse_candidate
    if "/generation/sse/" in resolved_path and endpoint_exists(openapi, method, resolved_path):
        return resolved_path
    return None


def find_polling_create_endpoint(openapi: dict[str, Any], method: str, resolved_path: str) -> str | None:
    polling_candidate = to_polling_path(resolved_path)
    if endpoint_exists(openapi, method, polling_candidate):
        return polling_candidate
    if endpoint_exists(openapi, method, resolved_path):
        return resolved_path
    return None


def find_subscribe_sse_endpoint(openapi: dict[str, Any]) -> str | None:
    paths = openapi.get("paths", {})
    if not isinstance(paths, dict):
        return None

    for path, ops in paths.items():
        if not isinstance(ops, dict):
            continue
        if "get" in ops and re.search(r"/predictions/\{[^}]+\}/subscribe$", path):
            return path
    return None


def build_default_and_sse_endpoints(
    openapi: dict[str, Any], endpoints: list[str]
) -> tuple[list[str], list[str]]:
    default_endpoints: list[str] = []
    sse_endpoints: list[str] = []

    for item in endpoints:
        method, path = parse_endpoint_arg(item)
        sse_path = to_sse_path(path)
        if endpoint_exists(openapi, method, sse_path):
            resolved = f"{method} {sse_path}"
            default_endpoints.append(resolved)
            sse_endpoints.append(resolved)
        else:
            default_endpoints.append(f"{method} {path}")

    return (
        unique_in_order(default_endpoints),
        unique_in_order(sse_endpoints),
    )


def ref_name(ref: str) -> str:
    return ref.rsplit("/", 1)[-1]


def resolve_schema(openapi: dict[str, Any], schema: dict[str, Any]) -> tuple[str | None, dict[str, Any]]:
    if "$ref" not in schema:
        return None, schema
    name = ref_name(schema["$ref"])
    resolved = openapi.get("components", {}).get("schemas", {}).get(name)
    if not isinstance(resolved, dict):
        raise SystemExit(f"Schema not found for ref: {schema['$ref']}")
    return name, resolved


def allowed_values(schema: dict[str, Any]) -> list[Any] | None:
    if isinstance(schema.get("enum"), list):
        return schema["enum"]
    for branch_key in ("anyOf", "oneOf"):
        branch = schema.get(branch_key)
        if not isinstance(branch, list):
            continue
        consts = [item["const"] for item in branch if isinstance(item, dict) and "const" in item]
        if consts:
            return consts
    return None


def summarize_type(schema: dict[str, Any]) -> str:
    if "$ref" in schema:
        return ref_name(schema["$ref"])

    schema_type = schema.get("type")
    if schema_type == "array":
        item_schema = schema.get("items") if isinstance(schema.get("items"), dict) else {}
        return f"array<{summarize_type(item_schema)}>"
    if isinstance(schema_type, str):
        return schema_type

    for branch_key in ("anyOf", "oneOf"):
        branch = schema.get(branch_key)
        if not isinstance(branch, list):
            continue
        variants: list[str] = []
        for item in branch:
            if not isinstance(item, dict):
                continue
            if "const" in item:
                const_value = item["const"]
                if isinstance(const_value, bool):
                    variants.append("boolean")
                elif isinstance(const_value, int):
                    variants.append("integer")
                elif isinstance(const_value, float):
                    variants.append("number")
                elif isinstance(const_value, str):
                    variants.append("string")
                else:
                    variants.append(type(const_value).__name__)
            elif "$ref" in item:
                variants.append(ref_name(item["$ref"]))
            elif isinstance(item.get("type"), str):
                variants.append(item["type"])
        if variants:
            return " | ".join(unique_in_order(variants))

    return "object"


def template_value(field_name: str, schema: dict[str, Any]) -> Any:
    if "default" in schema:
        return schema["default"]

    values = allowed_values(schema)
    if values:
        return values[0]

    schema_type = schema.get("type")
    if schema_type == "string":
        if schema.get("format") == "uri":
            return f"https://example.com/{field_name}.png"
        if "prompt" in field_name:
            return "Describe what to generate"
        return f"<{field_name}>"
    if schema_type in {"integer", "number"}:
        return 1
    if schema_type == "boolean":
        return False
    if schema_type == "array":
        item = schema.get("items") if isinstance(schema.get("items"), dict) else {}
        if item.get("format") == "uri":
            return ["https://example.com/input.png"]
        return []
    if schema_type == "object":
        return {}

    for branch_key in ("anyOf", "oneOf"):
        branch = schema.get(branch_key)
        if not isinstance(branch, list):
            continue
        for item in branch:
            if isinstance(item, dict) and "const" in item:
                return item["const"]

    return f"<{field_name}>"


def summarize_fields(schema: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    properties = schema.get("properties") if isinstance(schema.get("properties"), dict) else {}
    required = schema.get("required") if isinstance(schema.get("required"), list) else []
    required_set = set(required)

    fields: list[dict[str, Any]] = []
    template: dict[str, Any] = {}

    for name, prop in properties.items():
        if not isinstance(prop, dict):
            continue
        row: dict[str, Any] = {
            "name": name,
            "required": name in required_set,
            "type": summarize_type(prop),
        }
        if isinstance(prop.get("description"), str):
            row["description"] = prop["description"]
        if "default" in prop:
            row["default"] = prop["default"]
        values = allowed_values(prop)
        if values:
            row["allowed_values"] = values
        fields.append(row)

    for name in required:
        prop = properties.get(name)
        if isinstance(prop, dict):
            template[name] = template_value(name, prop)

    for name, prop in properties.items():
        if name in template:
            continue
        if isinstance(prop, dict) and "default" in prop:
            template[name] = prop["default"]

    return fields, template


def find_poll_endpoint(openapi: dict[str, Any]) -> str | None:
    paths = openapi.get("paths", {})
    if not isinstance(paths, dict):
        return None

    preferred = ["/generation/{id}", "/v1/generation/{request_id}", "/v1/generation/{id}"]
    for path in preferred:
        ops = paths.get(path)
        if isinstance(ops, dict) and "get" in ops:
            return path

    for path, ops in paths.items():
        if not isinstance(ops, dict):
            continue
        if "get" in ops and re.search(r"/generation/\{[^}]+\}", path):
            return path
    return None


def status_values(openapi: dict[str, Any], schema_name: str) -> list[str] | None:
    schema = openapi.get("components", {}).get("schemas", {}).get(schema_name)
    if isinstance(schema, dict) and isinstance(schema.get("enum"), list):
        if all(isinstance(item, str) for item in schema["enum"]):
            return schema["enum"]
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--openapi", required=True, help="Path to OpenAPI JSON")
    parser.add_argument("--docs", help="Path to docs.json for Videos/Images group extraction")
    parser.add_argument("--category", choices=["videos", "images"], default=DEFAULT_CATEGORY)
    parser.add_argument("--list-endpoints", action="store_true", help="List POST generation endpoints from docs.json group")
    parser.add_argument("--endpoint", help="Endpoint path or full string like 'POST /generation/...'")
    parser.add_argument("--include-template", action="store_true", help="Include request_template in output")
    parser.add_argument("--json-indent", type=int, default=2)
    args = parser.parse_args()

    openapi_path = Path(args.openapi)
    openapi = read_json(openapi_path)

    if args.list_endpoints:
        if not args.docs:
            raise SystemExit("--list-endpoints requires --docs <path/to/docs.json>")
        docs = read_json(Path(args.docs))
        polling_endpoints = list_endpoints_from_docs(docs, args.category)
        default_endpoints, sse_endpoints = build_default_and_sse_endpoints(
            openapi, polling_endpoints
        )
        print(
            json.dumps(
                {
                    "category": args.category,
                    "source": str(Path(args.docs).resolve()),
                    "default_result_mode": "sse" if sse_endpoints else "polling",
                    "default_endpoints": default_endpoints,
                    "sse_endpoints": sse_endpoints,
                    "polling_endpoints": polling_endpoints,
                    "poll_endpoint": find_poll_endpoint(openapi),
                },
                ensure_ascii=False,
                indent=args.json_indent,
            )
        )
        if not args.endpoint:
            return 0

    if not args.endpoint:
        raise SystemExit("Provide --endpoint or use --list-endpoints only")

    method, raw_path = parse_endpoint_arg(args.endpoint)
    resolved_path, operation = resolve_operation(openapi, method, raw_path)
    sse_create_endpoint = find_sse_create_endpoint(openapi, method, resolved_path)
    polling_create_endpoint = find_polling_create_endpoint(openapi, method, resolved_path)

    request_schema = (
        operation.get("requestBody", {})
        .get("content", {})
        .get("application/json", {})
        .get("schema", {})
    )
    if not isinstance(request_schema, dict):
        request_schema = {}

    request_schema_name, resolved_request_schema = resolve_schema(openapi, request_schema)
    fields, request_template = summarize_fields(resolved_request_schema)

    responses = operation.get("responses", {})
    if not isinstance(responses, dict):
        responses = {}
    error_codes = sorted(
        int(code) for code in responses.keys() if isinstance(code, str) and code.isdigit() and int(code) >= 400
    )

    servers = openapi.get("servers") if isinstance(openapi.get("servers"), list) else []
    server_url = None
    if servers and isinstance(servers[0], dict):
        server_url = servers[0].get("url")

    output: dict[str, Any] = {
        "endpoint": f"{method} {resolved_path}",
        "default_result_mode": "sse" if sse_create_endpoint else "polling",
        "default_create_endpoint": f"{method} {sse_create_endpoint or polling_create_endpoint or resolved_path}",
        "sse_create_endpoint": f"{method} {sse_create_endpoint}" if sse_create_endpoint else None,
        "polling_create_endpoint": f"{method} {polling_create_endpoint}" if polling_create_endpoint else None,
        "summary": operation.get("summary"),
        "server_url": server_url,
        "request_schema": request_schema_name,
        "fields": fields,
        "prediction_status_values": status_values(openapi, "PredictionStatus"),
        "queue_status_values": status_values(openapi, "QueueState"),
        "sse_subscribe_endpoint": find_subscribe_sse_endpoint(openapi),
        "poll_endpoint": find_poll_endpoint(openapi),
        "error_status_codes": error_codes,
    }

    if args.include_template:
        output["request_template"] = request_template

    print(json.dumps(output, ensure_ascii=False, indent=args.json_indent))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

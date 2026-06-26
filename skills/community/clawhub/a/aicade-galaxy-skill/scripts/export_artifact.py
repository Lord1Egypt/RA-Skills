#!/usr/bin/env python3

import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


DEFAULT_OUTPUT_DIR = "output"
OUTPUT_FILE_NAME = "aicade-galaxy-skill.json"
DEFAULT_SERVICES_PATH = "/admin/gateway/services"


def main() -> None:
    try:
        config = load_config()
        services = discover_services(config)
        artifact = build_artifact(config, services)
        output_path = Path(config["output_path"])
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(artifact, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"artifact written: {output_path}")
        print(
            json.dumps(
                {
                    "baseUrl": config["base_url"],
                    "toolCount": artifact["toolCount"],
                    "toolNames": [tool["name"] for tool in artifact["tools"]],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    except Exception as exc:  # noqa: BLE001
        print("Failed to export AICADE Galaxy artifact.", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        if is_auth_like_error(str(exc)):
            print(
                "Check whether AICADE_GALAXY_API_KEY is configured correctly in .env.",
                file=sys.stderr,
            )
        sys.exit(1)


def load_config() -> Dict[str, str]:
    env = load_env(Path(".env"))

    base_url = env.get("AICADE_GALAXY_BASE_URL") or env.get("CLAWHUB_BASE_URL")
    api_key = env.get("AICADE_GALAXY_API_KEY")
    output_dir = env.get("AICADE_GALAXY_OUTPUT_PATH") or DEFAULT_OUTPUT_DIR
    debug = is_debug_enabled(env.get("AICADE_GALAXY_DEBUG"))

    if not base_url:
        raise RuntimeError(
            'Missing required environment variable: AICADE_GALAXY_BASE_URL. Run "node scripts/setup_env.mjs" first, or fall back to "python3 scripts/setup_env.py", or update .env.'
        )
    if not api_key:
        raise RuntimeError(
            'Missing required environment variable: AICADE_GALAXY_API_KEY. Run "node scripts/setup_env.mjs" first, or fall back to "python3 scripts/setup_env.py", or update .env.'
        )

    return {
        "base_url": base_url.rstrip("/"),
        "services_path": DEFAULT_SERVICES_PATH,
        "output_path": str(Path(output_dir) / OUTPUT_FILE_NAME),
        "api_key": api_key,
        "debug": debug,
    }


def load_env(path: Path) -> Dict[str, str]:
    if not path.exists():
        return {}

    result: Dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        result[key.strip()] = strip_quotes(value.strip())
    return result


def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def discover_services(config: Dict[str, str]) -> List[dict]:
    url = join_url(config["base_url"], config["services_path"])
    headers = {
        "Accept": "application/json",
        "X-API-Key": config["api_key"],
    }
    log_debug(
        config,
        {
            "event": "request",
            "method": "GET",
            "url": url,
            "headers": headers,
        },
    )
    request = urllib.request.Request(url, headers=headers, method="GET")

    try:
        with urllib.request.urlopen(request) as response:
            body = response.read().decode("utf-8", errors="replace")
            content_type = response.headers.get("Content-Type", "")
            status_code = response.status
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Failed to discover services: HTTP {exc.code}. "
            f"Content-Type={exc.headers.get('Content-Type', '')}. "
            f"Body preview={preview_text(body)}"
        ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Failed to discover services: {exc.reason}") from exc

    log_debug(
        config,
        {
            "event": "response",
            "method": "GET",
            "url": url,
            "statusCode": status_code,
            "contentType": content_type,
            "bodyPreview": preview_text(body),
        },
    )

    try:
        payload = json.loads(body)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Failed to parse services response as JSON. "
            f"Content-Type={content_type}. "
            f"Body preview={preview_text(body)}"
        ) from exc

    if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
        raise RuntimeError("Invalid services response shape")

    return payload["data"]


def build_artifact(config: Dict[str, str], services: List[dict]) -> dict:
    tools = []
    for service in services:
        tool = build_tool(service)
        if tool:
            tools.append(tool)

    return {
        "version": "1.0",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "baseUrl": config["base_url"],
        "toolCount": len(tools),
        "tools": tools,
    }


def build_tool(service: dict) -> Optional[dict]:
    if not service.get("enabled", False):
        return None

    input_schema = service.get("inputSchema") or {}
    method = str(input_schema.get("method", "")).upper()
    if method not in {"GET", "POST"}:
        return None

    properties = input_schema.get("properties")
    if not isinstance(properties, dict):
        properties = {}

    required = input_schema.get("required")
    if not isinstance(required, list):
        required = []

    output_schema = service.get("outputSchema") or {}
    response_properties = output_schema.get("properties")
    if not isinstance(response_properties, dict):
        response_properties = {}

    response_fields = list_response_paths(response_properties)

    return {
        "name": create_tool_name(
            str(service.get("serviceId", service.get("name", "service")))
        ),
        "description": build_tool_description(
            service, method, properties, required, response_fields
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                **properties,
                "responsePaths": build_response_paths_property(response_fields),
            },
            "required": [key for key in required if key in properties],
            "additionalProperties": False,
        },
        "metadata": {
            "serviceId": service.get("serviceId"),
            "title": service.get("title")
            or service.get("serviceName")
            or service.get("name"),
            "method": method,
            "path": service.get("routePath"),
            "authentication": {
                "type": "apiKeyHeader",
                "required": True,
                "headerName": "X-API-Key",
                "envName": "AICADE_GALAXY_API_KEY",
            },
            "responseFields": response_fields,
            "invocationProtocol": {
                "reservedFields": ["responsePaths"],
                "responsePathsField": "responsePaths",
            },
        },
    }


def create_tool_name(service_id: str) -> str:
    return "".join(ch if ch.isalnum() or ch == "_" else "_" for ch in service_id)


def build_tool_description(
    service: dict,
    method: str,
    properties: dict,
    required: list,
    response_fields: List[str],
) -> str:
    parts = [
        service.get("title") or service.get("serviceName") or service.get("name") or "AICADE service",
        service.get("description") or "",
        "Use query parameters and expect a JSON response." if method == "GET" else "Use a JSON request body and expect a JSON response.",
    ]

    if properties:
        names = list(properties.keys())
        parts.append(f"Parameters: {', '.join(names)}.")

        required_names = [name for name in required if name in properties]
        optional_names = [name for name in names if name not in required_names]
        if required_names:
            parts.append(f"Required parameters: {', '.join(required_names)}.")
        if optional_names:
            parts.append(f"Optional parameters: {', '.join(optional_names)}.")

    if response_fields:
        parts.append(
            f"Optional reserved field: responsePaths. Selectable response fields: {', '.join(response_fields)}. Use responsePaths to request only the fields you need."
        )
    else:
        parts.append(
            "Optional reserved field: responsePaths. Response selection is supported, but this service does not declare output fields."
        )

    return " ".join(part for part in parts if part)


def build_response_paths_property(response_fields: List[str]) -> dict:
    description = "Optional. Select one or more response field paths to return."
    if response_fields:
        description = (
            f"{description} Available values: {', '.join(response_fields)}."
        )

    return {
        "type": "array",
        "description": description,
        "items": {
            "type": "string",
        },
    }


def list_response_paths(properties: dict) -> List[str]:
    paths: List[str] = []
    for key, prop in properties.items():
        walk_schema_property(key, prop, paths)
    return paths


def walk_schema_property(current_path: str, prop: dict, paths: List[str]) -> None:
    paths.append(current_path)

    if prop.get("type") == "object" and isinstance(prop.get("properties"), dict):
        for key, child in prop["properties"].items():
            walk_schema_property(f"{current_path}.{key}", child, paths)

    if prop.get("type") == "array" and isinstance(prop.get("items"), dict):
        paths.append(f"{current_path}[]")
        items = prop["items"]
        if items.get("type") == "object" and isinstance(
            items.get("properties"), dict
        ):
            for key, child in items["properties"].items():
                walk_schema_property(f"{current_path}[].{key}", child, paths)


def join_url(base_url: str, path: str) -> str:
    normalized_path = path[1:] if path.startswith("/") else path
    return f"{base_url}/{normalized_path}"


def is_auth_like_error(message: str) -> bool:
    return (
        "401" in message
        or "403" in message
        or "X-API-Key" in message
        or "AICADE_GALAXY_API_KEY" in message
    )


def is_debug_enabled(value: Optional[str]) -> bool:
    return bool(value) and value.lower() == "true"


def log_debug(config: Dict[str, str], payload: dict) -> None:
    if not config.get("debug"):
        return
    print(
        f"[AICADE_GALAXY_DEBUG] {json.dumps(payload, ensure_ascii=False, indent=2)}"
    )


def preview_text(text: str, limit: int = 240) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return compact[:limit] + "..."


if __name__ == "__main__":
    main()

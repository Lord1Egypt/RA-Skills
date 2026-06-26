#!/usr/bin/env python3

import argparse
import json
import os
import posixpath
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib import error, parse, request

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_CONFIG = str(SKILL_DIR / "config.json")
DEFAULT_BASE_URL = "https://dashboard.avavox.com"
ALLOWED_BASE_HOSTS = {"dashboard.avavox.com"}
ALLOWED_API_PREFIX = "/open/api"
ENV_APP_KEY = "AVAVOX_APP_KEY"
ENV_BASE_URL = "AVAVOX_BASE_URL"
SKILL_VERSION = "0.6.2"
ENV_DEFAULTS = {
    "taskId": "AVAVOX_DEFAULT_TASK_ID",
    "lineId": "AVAVOX_DEFAULT_LINE_ID",
    "concurrency": "AVAVOX_DEFAULT_CONCURRENCY",
    "backgroundAudio": "AVAVOX_DEFAULT_BACKGROUND_AUDIO",
    "callTimeType": "AVAVOX_DEFAULT_CALL_TIME_TYPE",
}


def print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def fail(message: str, details: Any = None) -> None:
    payload = {"error": message}
    if details is not None:
        payload["details"] = details
    print(json.dumps(payload, ensure_ascii=False, indent=2), file=sys.stderr)
    raise SystemExit(1)


def is_non_empty(value: Any) -> bool:
    return value is not None and value != ""


def first_non_empty(*values: Any) -> Any:
    for value in values:
        if is_non_empty(value):
            return value
    return None


def assign_if_non_empty(target: Dict[str, Any], key: str, value: Any) -> None:
    if is_non_empty(value):
        target[key] = value


def resolve_path(file_path: str) -> Path:
    if not file_path:
        fail("A file path is required")

    path = Path(file_path)
    return path if path.is_absolute() else Path.cwd() / path


def resolve_config_path(config_path: Optional[str]) -> Path:
    return resolve_path(config_path or DEFAULT_CONFIG)


def load_json_file(file_path: Union[str, Path], label: str) -> Any:
    resolved = resolve_path(str(file_path))
    try:
        return json.loads(resolved.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail(
            f"Failed to read {label}",
            {
                "filePath": str(resolved),
                "error": str(exc),
            },
        )


def parse_json(name: str, raw: Optional[str], fallback: Any) -> Any:
    if not is_non_empty(raw):
        return fallback

    try:
        return json.loads(raw)
    except Exception as exc:  # noqa: BLE001
        fail(f"{name} is not valid JSON", str(exc))


def load_json_input(
    name: str,
    inline_value: Optional[str],
    file_value: Optional[str],
    fallback: Any,
) -> Any:
    if is_non_empty(inline_value) and is_non_empty(file_value):
        fail(f"Use only one of inline JSON or file input for {name}")

    if is_non_empty(file_value):
        return load_json_file(file_value, f"{name} file")

    if is_non_empty(inline_value):
        return parse_json(name, inline_value, fallback)

    return fallback


def ensure_plain_object(name: str, value: Any) -> Dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{name} must be a JSON object")
    return value


def parse_optional_integer(name: str, value: Optional[str]) -> Optional[int]:
    if not is_non_empty(value):
        return None

    try:
        return int(value)
    except ValueError:
        fail(f"{name} must be an integer", {"value": value})


def default_port(scheme: str) -> Optional[int]:
    if scheme == "https":
        return 443
    if scheme == "http":
        return 80
    return None


def is_allowed_api_path(path: str) -> bool:
    return path == ALLOWED_API_PREFIX or path.startswith(f"{ALLOWED_API_PREFIX}/")


def normalize_base_url(base_url: Optional[str]) -> str:
    if not is_non_empty(base_url):
        fail("config.baseUrl is required")

    parsed = parse.urlsplit(str(base_url).strip())
    scheme = parsed.scheme.lower()
    host = (parsed.hostname or "").lower()

    if scheme != "https" or not host:
        fail("config.baseUrl must be an https URL")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        fail("config.baseUrl must not contain auth, query, or fragment")
    if parsed.path not in ("", "/"):
        fail("config.baseUrl must not contain a path")
    if parsed.port not in (None, default_port(scheme)):
        fail("config.baseUrl must use the default https port")
    if host not in ALLOWED_BASE_HOSTS:
        fail(
            "config.baseUrl host is not allowed",
            {"allowedHosts": sorted(ALLOWED_BASE_HOSTS)},
        )

    return f"{scheme}://{host}"


def normalize_api_path(api_path: str) -> str:
    raw_path = str(api_path).strip()
    if not raw_path:
        fail("API path is required")
    if raw_path.startswith(("//", "\\\\")) or "\\" in raw_path:
        fail(
            "API path must be a relative /open/api path",
            {"path": api_path},
        )

    parsed = parse.urlsplit(raw_path)
    if parsed.scheme or parsed.netloc:
        fail(
            "API path must not be an absolute URL",
            {"path": api_path},
        )
    if parsed.query or parsed.fragment:
        fail(
            "API path must not include query string or fragment; use --query-json instead",
            {"path": api_path},
        )

    normalized_path = posixpath.normpath(parsed.path or "")
    if not normalized_path.startswith("/"):
        normalized_path = f"/{normalized_path}"

    if raw_path.endswith("/") and normalized_path != "/" and not normalized_path.endswith("/"):
        normalized_path = f"{normalized_path}/"

    if not is_allowed_api_path(normalized_path):
        fail(
            "API path must stay under /open/api",
            {"path": api_path},
        )

    return normalized_path


def ensure_allowed_request_url(base_url: str, url: str) -> None:
    base_parts = parse.urlsplit(base_url)
    target_parts = parse.urlsplit(url)

    base_origin = (
        base_parts.scheme.lower(),
        (base_parts.hostname or "").lower(),
        base_parts.port or default_port(base_parts.scheme.lower()),
    )
    target_origin = (
        target_parts.scheme.lower(),
        (target_parts.hostname or "").lower(),
        target_parts.port or default_port(target_parts.scheme.lower()),
    )

    if target_origin != base_origin:
        fail(
            "Request target must stay on the configured avavox origin",
            {"url": url},
        )
    if not is_allowed_api_path(target_parts.path):
        fail(
            "Request target must stay under /open/api",
            {"url": url},
        )


class RestrictedRedirectHandler(request.HTTPRedirectHandler):
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def redirect_request(self, req: request.Request, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> request.Request:
        ensure_allowed_request_url(self.base_url, newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def load_config(config_path: Optional[str]) -> Dict[str, Any]:
    resolved = resolve_config_path(config_path)
    if resolved.exists():
        data = load_json_file(resolved, "config.json")
    else:
        data = {}

    if not isinstance(data, dict):
        fail("config.json must be a JSON object")

    defaults = data.get("defaults") or {}
    if not isinstance(defaults, dict):
        fail("config.defaults must be a JSON object")

    merged_defaults = {**defaults}
    for key, env_name in ENV_DEFAULTS.items():
        env_value = os.getenv(env_name)
        if is_non_empty(env_value):
            merged_defaults[key] = env_value

    app_key = first_non_empty(os.getenv(ENV_APP_KEY), data.get("appKey"))
    if not is_non_empty(app_key):
        fail(f"config.appKey or env {ENV_APP_KEY} is required")

    base_url = first_non_empty(os.getenv(ENV_BASE_URL), data.get("baseUrl"), DEFAULT_BASE_URL)

    return {
        **data,
        "appKey": app_key,
        "baseUrl": normalize_base_url(base_url),
        "defaults": merged_defaults,
    }


def build_headers(
    config: Dict[str, Any],
    extra_headers: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    headers = {
        "Authorization": f"Bearer {config['appKey']}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    if extra_headers:
        headers.update(extra_headers)
    return headers


def build_url(base_url: str, api_path: str, query: Optional[Dict[str, Any]] = None) -> str:
    parsed_base = parse.urlsplit(base_url)
    normalized_path = normalize_api_path(api_path)
    url = parse.urlunsplit((parsed_base.scheme, parsed_base.netloc, normalized_path, "", ""))
    ensure_allowed_request_url(base_url, url)
    if not query:
        return url

    cleaned_query: List[Tuple[str, str]] = []
    for key, value in query.items():
        if not is_non_empty(value):
            continue

        if isinstance(value, list):
            for item in value:
                if is_non_empty(item):
                    cleaned_query.append((key, str(item)))
            continue

        cleaned_query.append((key, str(value)))

    if not cleaned_query:
        return url

    return f"{url}?{parse.urlencode(cleaned_query, doseq=True)}"


def api_request(
    config: Dict[str, Any],
    api_path: str,
    *,
    method: str = "GET",
    query: Optional[Dict[str, Any]] = None,
    body: Any = None,
    headers: Optional[Dict[str, str]] = None,
) -> Any:
    url = build_url(config["baseUrl"], api_path, query)
    ensure_allowed_request_url(config["baseUrl"], url)
    request_body = None if body is None else json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = request.Request(
        url=url,
        data=request_body,
        headers=build_headers(config, headers),
        method=method.upper(),
    )
    opener = request.build_opener(RestrictedRedirectHandler(config["baseUrl"]))

    try:
        with opener.open(req) as response:
            status = response.status
            text = response.read().decode("utf-8")
    except error.HTTPError as exc:
        text = exc.read().decode("utf-8", errors="replace")
        payload = parse_response_body(text)
        fail(
            "HTTP request failed",
            {
                "method": method.upper(),
                "url": url,
                "status": exc.code,
                "response": payload,
            },
        )
    except error.URLError as exc:
        fail(
            "Network request failed",
            {
                "method": method.upper(),
                "url": url,
                "error": str(exc),
            },
        )

    payload = parse_response_body(text)
    if status < 200 or status >= 300:
        fail(
            "HTTP request failed",
            {
                "method": method.upper(),
                "url": url,
                "status": status,
                "response": payload,
            },
        )

    if isinstance(payload, dict):
        if payload.get("success") is False:
            fail(
                "Business request failed",
                {
                    "method": method.upper(),
                    "url": url,
                    "response": payload,
                },
            )

        if "code" in payload and payload["code"] != 200:
            fail(
                "Business request failed",
                {
                    "method": method.upper(),
                    "url": url,
                    "response": payload,
                },
            )

    return payload


def parse_response_body(text: str) -> Any:
    if not text:
        return {}

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw": text}


def build_task_payload(args: argparse.Namespace, defaults: Dict[str, Any], mode: str) -> Dict[str, Any]:
    base_body = load_json_input("body", args.body_json, args.body_file, {})
    body = ensure_plain_object("body", base_body)

    runtime_config = load_json_input(
        "runtimeConfig",
        args.runtime_config_json,
        args.runtime_config_file,
        None,
    )
    forbidden_call_time = load_json_input(
        "forbiddenCallTime",
        args.forbidden_call_time_json,
        args.forbidden_call_time_file,
        None,
    )
    scheduled_time = load_json_input(
        "scheduledTime",
        args.scheduled_time_json,
        args.scheduled_time_file,
        None,
    )

    assign_if_non_empty(body, "taskName", args.task_name)
    assign_if_non_empty(body, "robotId", args.robot_id)
    assign_if_non_empty(body, "lineId", args.line_id)
    assign_if_non_empty(body, "backgroundAudio", args.background_audio)

    concurrency = parse_optional_integer("concurrency", args.concurrency)
    if concurrency is not None:
        body["concurrency"] = concurrency

    assign_if_non_empty(body, "callTimeType", args.call_time_type)

    if runtime_config is not None:
        body["runtimeConfig"] = runtime_config
    if forbidden_call_time is not None:
        body["forbiddenCallTime"] = forbidden_call_time
    if scheduled_time is not None:
        body["scheduledTime"] = scheduled_time

    if mode == "create":
        assign_if_non_empty(body, "lineId", defaults.get("lineId"))
        assign_if_non_empty(body, "backgroundAudio", defaults.get("backgroundAudio"))
        assign_if_non_empty(body, "callTimeType", defaults.get("callTimeType"))

        if "concurrency" not in body and defaults.get("concurrency") is not None:
            body["concurrency"] = parse_optional_integer("defaults.concurrency", str(defaults["concurrency"]))

        if not is_non_empty(body.get("taskName")):
            fail("tasks create requires taskName")
        if not is_non_empty(body.get("robotId")):
            fail("tasks create requires robotId")

    if body.get("callTimeType") == "scheduled" and not isinstance(body.get("scheduledTime"), list):
        fail("scheduledTime is required when callTimeType=scheduled")

    if mode == "update" and not body:
        fail("tasks update requires at least one field to update")

    return body


def get_task_id(args: argparse.Namespace, defaults: Dict[str, Any]) -> Optional[str]:
    return first_non_empty(getattr(args, "task_id", None), defaults.get("taskId"))


def handle_robots_list(args: argparse.Namespace) -> None:
    config = load_config(args.config)
    response = api_request(config, "/open/api/task/robot")
    print_json(response)


def handle_lines_list(args: argparse.Namespace) -> None:
    config = load_config(args.config)
    response = api_request(config, "/open/api/task/line")
    print_json(response)


def handle_tasks_list(args: argparse.Namespace) -> None:
    config = load_config(args.config)
    response = api_request(config, "/open/api/task/list")
    print_json(response)


def handle_tasks_get(args: argparse.Namespace) -> None:
    config = load_config(args.config)
    task_id = get_task_id(args, config["defaults"])
    if not is_non_empty(task_id):
        fail("tasks get requires --task-id or defaults.taskId")
    response = api_request(config, f"/open/api/task/{task_id}")
    print_json(response)


def handle_tasks_create(args: argparse.Namespace) -> None:
    config = load_config(args.config)
    body = build_task_payload(args, config["defaults"], "create")
    response = api_request(config, "/open/api/task", method="POST", body=body)
    print_json(response)


def handle_tasks_update(args: argparse.Namespace) -> None:
    config = load_config(args.config)
    task_id = get_task_id(args, config["defaults"])
    if not is_non_empty(task_id):
        fail("tasks update requires --task-id or defaults.taskId")
    body = build_task_payload(args, config["defaults"], "update")
    response = api_request(config, f"/open/api/task/{task_id}", method="PUT", body=body)
    print_json(response)


def handle_task_action(args: argparse.Namespace, action: str) -> None:
    config = load_config(args.config)
    task_id = get_task_id(args, config["defaults"])
    if not is_non_empty(task_id):
        fail(f"tasks {action} requires --task-id or defaults.taskId")
    response = api_request(config, f"/open/api/task/{task_id}/{action}", method="POST")
    print_json(response)


def handle_tasks_variables(args: argparse.Namespace) -> None:
    config = load_config(args.config)
    task_id = get_task_id(args, config["defaults"])
    if not is_non_empty(task_id):
        fail("tasks variables requires --task-id or defaults.taskId")
    response = api_request(config, f"/open/api/task/{task_id}/robot-variables")
    print_json(response)


def normalize_customers(source: Any) -> List[Dict[str, Any]]:
    if isinstance(source, list):
        return source
    if isinstance(source, dict) and isinstance(source.get("customers"), list):
        return source["customers"]
    fail("customers input must be an array or an object with a customers array")


def handle_customers_import(args: argparse.Namespace) -> None:
    config = load_config(args.config)
    task_id = get_task_id(args, config["defaults"])
    if not is_non_empty(task_id):
        fail("customers import requires --task-id or defaults.taskId")

    customers_source = load_json_input("customers", args.customers_inline, args.customers_file, None)
    if customers_source is None:
        fail("customers import requires --customers-inline or --customers-file")

    customers = normalize_customers(customers_source)
    if len(customers) == 0:
        fail("customers import requires at least one customer")
    if len(customers) > 2000:
        fail("customers import supports at most 2000 customers per request")

    for index, customer in enumerate(customers):
        if not isinstance(customer, dict):
            fail("Each customer must be a JSON object", {"index": index})
        if not is_non_empty(customer.get("phoneNumber")):
            fail("Each customer requires phoneNumber", {"index": index})

    response = api_request(
        config,
        "/open/api/task/import",
        method="POST",
        body={
            "taskId": task_id,
            "customers": customers,
        },
    )
    print_json(response)


def handle_request(args: argparse.Namespace) -> None:
    config = load_config(args.config)
    if not is_non_empty(args.path):
        fail("request requires --path")

    raw_query = load_json_input("query", args.query_json, args.query_file, None)
    query = None if raw_query is None else ensure_plain_object("query", raw_query)
    body = load_json_input("body", args.body_json, args.body_file, None)

    response = api_request(
        config,
        args.path,
        method=(args.method or "GET").upper(),
        query=query,
        body=body,
    )
    print_json(response)


def add_task_payload_arguments(parser: argparse.ArgumentParser, include_task_id: bool) -> None:
    if include_task_id:
        parser.add_argument("--task-id", dest="task_id")

    parser.add_argument("--task-name", dest="task_name")
    parser.add_argument("--robot-id", dest="robot_id")
    parser.add_argument("--line-id", dest="line_id")
    parser.add_argument("--background-audio", dest="background_audio")
    parser.add_argument("--concurrency")
    parser.add_argument("--call-time-type", dest="call_time_type")
    parser.add_argument("--runtime-config-json", dest="runtime_config_json")
    parser.add_argument("--runtime-config-file", dest="runtime_config_file")
    parser.add_argument("--forbidden-call-time-json", dest="forbidden_call_time_json")
    parser.add_argument("--forbidden-call-time-file", dest="forbidden_call_time_file")
    parser.add_argument("--scheduled-time-json", dest="scheduled_time_json")
    parser.add_argument("--scheduled-time-file", dest="scheduled_time_file")
    parser.add_argument("--body-json", dest="body_json")
    parser.add_argument("--body-file", dest="body_file")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="avavox_call.py",
        description="avavox open/api client for OpenClaw skills.",
    )
    parser.add_argument("--config", default=DEFAULT_CONFIG)
    parser.add_argument("--version", action="version", version=f"%(prog)s {SKILL_VERSION}")
    subparsers = parser.add_subparsers(dest="command")

    robots_parser = subparsers.add_parser("robots")
    robots_subparsers = robots_parser.add_subparsers(dest="subcommand")
    robots_list = robots_subparsers.add_parser("list")
    robots_list.set_defaults(handler=handle_robots_list)

    lines_parser = subparsers.add_parser("lines")
    lines_subparsers = lines_parser.add_subparsers(dest="subcommand")
    lines_list = lines_subparsers.add_parser("list")
    lines_list.set_defaults(handler=handle_lines_list)

    tasks_parser = subparsers.add_parser("tasks")
    tasks_subparsers = tasks_parser.add_subparsers(dest="subcommand")

    tasks_list = tasks_subparsers.add_parser("list")
    tasks_list.set_defaults(handler=handle_tasks_list)

    tasks_get = tasks_subparsers.add_parser("get")
    tasks_get.add_argument("--task-id", dest="task_id")
    tasks_get.set_defaults(handler=handle_tasks_get)

    tasks_create = tasks_subparsers.add_parser("create")
    add_task_payload_arguments(tasks_create, include_task_id=False)
    tasks_create.set_defaults(handler=handle_tasks_create)

    tasks_update = tasks_subparsers.add_parser("update")
    add_task_payload_arguments(tasks_update, include_task_id=True)
    tasks_update.set_defaults(handler=handle_tasks_update)

    tasks_pause = tasks_subparsers.add_parser("pause")
    tasks_pause.add_argument("--task-id", dest="task_id")
    tasks_pause.set_defaults(handler=lambda args: handle_task_action(args, "pause"))

    tasks_resume = tasks_subparsers.add_parser("resume")
    tasks_resume.add_argument("--task-id", dest="task_id")
    tasks_resume.set_defaults(handler=lambda args: handle_task_action(args, "resume"))

    tasks_variables = tasks_subparsers.add_parser("variables")
    tasks_variables.add_argument("--task-id", dest="task_id")
    tasks_variables.set_defaults(handler=handle_tasks_variables)

    customers_parser = subparsers.add_parser("customers")
    customers_subparsers = customers_parser.add_subparsers(dest="subcommand")
    customers_import = customers_subparsers.add_parser("import")
    customers_import.add_argument("--task-id", dest="task_id")
    customers_import.add_argument("--customers-inline", dest="customers_inline")
    customers_import.add_argument("--customers-file", dest="customers_file")
    customers_import.set_defaults(handler=handle_customers_import)

    request_parser = subparsers.add_parser("request")
    request_parser.add_argument("--method")
    request_parser.add_argument("--path")
    request_parser.add_argument("--query-json", dest="query_json")
    request_parser.add_argument("--query-file", dest="query_file")
    request_parser.add_argument("--body-json", dest="body_json")
    request_parser.add_argument("--body-file", dest="body_file")
    request_parser.set_defaults(handler=handle_request)

    return parser


def extract_config_arg(argv: List[str]) -> Tuple[List[str], str]:
    cleaned: List[str] = []
    config_path = DEFAULT_CONFIG
    index = 0

    while index < len(argv):
        token = argv[index]
        if token == "--config":
            if index + 1 >= len(argv):
                fail("--config requires a value")
            config_path = argv[index + 1]
            index += 2
            continue
        if token.startswith("--config="):
            config_path = token.split("=", 1)[1]
            index += 1
            continue

        cleaned.append(token)
        index += 1

    return cleaned, config_path


def main() -> None:
    parser = build_parser()
    cleaned_argv, config_path = extract_config_arg(sys.argv[1:])
    args = parser.parse_args(cleaned_argv)
    args.config = config_path
    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help()
        raise SystemExit(1)
    handler(args)


if __name__ == "__main__":
    main()

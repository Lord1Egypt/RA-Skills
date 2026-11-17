#!/usr/bin/env python3
import json
import os
import sys
import traceback
from typing import Any

from archery_client import ArcheryClient, ArcheryError


SERVER_NAME = "archery-query"
SERVER_VERSION = "0.1.0"
PROTOCOL_VERSION = "2024-11-05"


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def build_client() -> ArcheryClient:
    client = ArcheryClient(
        base_url=os.getenv("ARCHERY_BASE_URL", "http://your-archery-server:9123"),
        timeout=int(os.getenv("ARCHERY_TIMEOUT", "15")),
        verify=not env_bool("ARCHERY_INSECURE", False),
        session_file=os.getenv("ARCHERY_SESSION_FILE", "~/.archery/cache/session.json"),
    )
    client.load_session()
    return client


CLIENT = build_client()


def login_if_needed(force: bool = False) -> None:
    if not force:
        try:
            CLIENT.ensure_session()
            return
        except ArcheryError:
            pass

    username = os.getenv("ARCHERY_USERNAME")
    password = os.getenv("ARCHERY_PASSWORD")
    otp = os.getenv("ARCHERY_OTP")
    auth_type = os.getenv("ARCHERY_AUTH_TYPE", "totp")
    phone = os.getenv("ARCHERY_PHONE", "")
    key = os.getenv("ARCHERY_KEY", "")

    if not username or not password:
        raise ArcheryError(
            "ARCHERY_USERNAME and ARCHERY_PASSWORD are required for MCP server login"
        )

    result = CLIENT.login(
        username=username,
        password=password,
        otp=otp,
        auth_type=auth_type,
        phone=phone,
        key=key,
    )
    if result.get("status") != "ok":
        raise ArcheryError(f"login failed: {result}")


def make_tool_result(data: Any, *, is_error: bool = False) -> dict[str, Any]:
    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(data, ensure_ascii=False, indent=2),
            }
        ],
        "isError": is_error,
    }


TOOLS = [
    {
        "name": "list_instances",
        "description": "List Archery instances readable by the current user.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "tag_codes": {"type": "array", "items": {"type": "string"}},
                "type_name": {"type": "string"},
                "db_types": {"type": "array", "items": {"type": "string"}},
                "refresh_login": {"type": "boolean"},
            },
        },
    },
    {
        "name": "list_tables",
        "description": "List tables in a database for a chosen Archery instance.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "instance_name": {"type": "string"},
                "db_name": {"type": "string"},
                "schema_name": {"type": "string"},
                "refresh_login": {"type": "boolean"},
            },
            "required": ["instance_name", "db_name"],
        },
    },
    {
        "name": "describe_table",
        "description": "Describe a table structure through Archery.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "instance_name": {"type": "string"},
                "db_name": {"type": "string"},
                "tb_name": {"type": "string"},
                "schema_name": {"type": "string"},
                "refresh_login": {"type": "boolean"},
            },
            "required": ["instance_name", "db_name", "tb_name"],
        },
    },
    {
        "name": "query",
        "description": "Execute a SQL query through Archery and return rows.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "instance_name": {"type": "string"},
                "db_name": {"type": "string"},
                "sql": {"type": "string"},
                "tb_name": {"type": "string"},
                "schema_name": {"type": "string"},
                "limit_num": {"type": "integer"},
                "refresh_login": {"type": "boolean"},
            },
            "required": ["instance_name", "db_name", "sql"],
        },
    },
]


def handle_tool_call(name: str, arguments: dict[str, Any] | None) -> dict[str, Any]:
    args = arguments or {}
    login_if_needed(bool(args.get("refresh_login", False)))

    if name == "list_instances":
        return make_tool_result(
            CLIENT.list_instances(
                tag_codes=args.get("tag_codes") or ["can_read"],
                type_name=args.get("type_name"),
                db_types=args.get("db_types") or None,
            )
        )

    if name == "list_tables":
        return make_tool_result(
            CLIENT.list_resources(
                instance_name=args["instance_name"],
                db_name=args["db_name"],
                schema_name=args.get("schema_name", ""),
                resource_type="table",
            )
        )

    if name == "describe_table":
        return make_tool_result(
            CLIENT.describe_table(
                instance_name=args["instance_name"],
                db_name=args["db_name"],
                tb_name=args["tb_name"],
                schema_name=args.get("schema_name", ""),
            )
        )

    if name == "query":
        return make_tool_result(
            CLIENT.query(
                instance_name=args["instance_name"],
                db_name=args["db_name"],
                sql_content=args["sql"],
                tb_name=args.get("tb_name", ""),
                schema_name=args.get("schema_name", ""),
                limit_num=int(args.get("limit_num", 100)),
            )
        )

    raise ArcheryError(f"unknown tool: {name}")


def jsonrpc_success(message_id: Any, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": message_id, "result": result}


def jsonrpc_error(message_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": message_id, "error": {"code": code, "message": message}}


def read_message() -> dict[str, Any] | None:
    content_length = None
    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            return None
        if line in (b"\r\n", b"\n"):
            break
        if line.lower().startswith(b"content-length:"):
            content_length = int(line.split(b":", 1)[1].strip())
    if content_length is None:
        return None
    body = sys.stdin.buffer.read(content_length)
    if not body:
        return None
    return json.loads(body.decode("utf-8"))


def write_message(payload: dict[str, Any]) -> None:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    sys.stdout.buffer.write(f"Content-Length: {len(body)}\r\n\r\n".encode("ascii"))
    sys.stdout.buffer.write(body)
    sys.stdout.buffer.flush()


def handle_request(request: dict[str, Any]) -> dict[str, Any] | None:
    method = request.get("method")
    message_id = request.get("id")

    if method == "initialize":
        return jsonrpc_success(
            message_id,
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
            },
        )

    if method == "notifications/initialized":
        return None

    if method == "ping":
        return jsonrpc_success(message_id, {})

    if method == "tools/list":
        return jsonrpc_success(message_id, {"tools": TOOLS})

    if method == "tools/call":
        params = request.get("params") or {}
        name = params.get("name")
        arguments = params.get("arguments") or {}
        result = handle_tool_call(name, arguments)
        return jsonrpc_success(message_id, result)

    return jsonrpc_error(message_id, -32601, f"Method not found: {method}")


def main() -> int:
    while True:
        request = read_message()
        if request is None:
            return 0
        try:
            response = handle_request(request)
        except Exception as exc:
            response = jsonrpc_error(
                request.get("id"),
                -32000,
                f"{exc}\n{traceback.format_exc()}",
            )
        if response is not None:
            write_message(response)


if __name__ == "__main__":
    sys.exit(main())

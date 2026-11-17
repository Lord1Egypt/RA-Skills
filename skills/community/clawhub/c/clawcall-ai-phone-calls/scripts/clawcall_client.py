#!/usr/bin/env python3
"""Command-line client for the ClawCall Agent API."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import socket
import stat
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from typing import Any


CLIENT_VERSION = "1.0.1"
DEFAULT_API_BASE = "https://agent.clawcall.cc"
DEFAULT_TIMEOUT = 30.0
DEFAULT_TOKEN_FILE = "~/.config/clawcall/token"
E164_RE = re.compile(r"^\+[1-9][0-9]{7,14}$")
RESOURCE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{1,128}$")
TERMINAL_STATUSES = {"completed", "failed", "cancelled", "canceled"}
INSTRUCTION_FIELDS = {"LLM_SYSTEM_INSTRUCTION"}


class ClientError(RuntimeError):
    pass


def api_base() -> str:
    value = os.environ.get("CLAWCALL_API_BASE", DEFAULT_API_BASE).strip().rstrip("/")
    if not value.startswith(("https://", "http://")):
        raise ClientError("CLAWCALL_API_BASE must use http:// or https://")
    return value


def timeout_seconds() -> float:
    raw = os.environ.get("CLAWCALL_HTTP_TIMEOUT", str(DEFAULT_TIMEOUT))
    try:
        value = float(raw)
    except ValueError as exc:
        raise ClientError("CLAWCALL_HTTP_TIMEOUT must be a number") from exc
    if not 1 <= value <= 300:
        raise ClientError("CLAWCALL_HTTP_TIMEOUT must be between 1 and 300 seconds")
    return value


def token_path() -> Path:
    return Path(os.environ.get("CLAW_TOKEN_FILE", DEFAULT_TOKEN_FILE)).expanduser()


def read_token() -> str:
    env_token = os.environ.get("CLAW_TOKEN", "").strip()
    if env_token:
        return env_token
    path = token_path()
    if not path.is_file():
        raise ClientError("CLAW_TOKEN is not set and no token file exists; run register first")
    mode = stat.S_IMODE(path.stat().st_mode)
    if mode & 0o077:
        raise ClientError(f"token file {path} must not be readable by group or others")
    value = path.read_text(encoding="utf-8").strip()
    if not value:
        raise ClientError(f"token file {path} is empty")
    return value


def write_token(token: str) -> Path:
    path = token_path()
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    try:
        path.parent.chmod(0o700)
    except OSError:
        pass
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        handle.write(token + "\n")
    path.chmod(0o600)
    return path


def strip_instruction_fields(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: strip_instruction_fields(child)
            for key, child in value.items()
            if key not in INSTRUCTION_FIELDS
        }
    if isinstance(value, list):
        return [strip_instruction_fields(child) for child in value]
    return value


def decode_json(raw: bytes, context: str) -> Any:
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ClientError(f"{context} returned invalid JSON; response body was not displayed") from exc
    return strip_instruction_fields(value)


def render_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def request(
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
    *,
    authenticated: bool = True,
    query: dict[str, Any] | None = None,
    extra_headers: dict[str, str] | None = None,
) -> Any:
    url = api_base() + path
    if query:
        url += "?" + urllib.parse.urlencode(
            {key: value for key, value in query.items() if value is not None}
        )
    headers = {
        "Accept": "application/json",
        "User-Agent": f"openclaw-clawcall-ai-phone-calls/{CLIENT_VERSION}",
    }
    if authenticated:
        headers["Authorization"] = f"Bearer {read_token()}"
    if extra_headers:
        headers.update(extra_headers)
    data = None
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=utf-8"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout_seconds()) as response:
            result = decode_json(response.read(), path)
    except urllib.error.HTTPError as exc:
        body = exc.read()
        try:
            detail = json.dumps(decode_json(body, path), ensure_ascii=False, separators=(",", ":"))
        except ClientError:
            detail = "response body omitted because it was not valid JSON"
        raise ClientError(f"HTTP {exc.code} from {path}: {detail}") from exc
    except (urllib.error.URLError, TimeoutError, socket.timeout) as exc:
        raise ClientError(f"Request to {path} failed: {exc}") from exc
    if isinstance(result, dict) and result.get("success") is False:
        raise ClientError(
            "API rejected the request: "
            + json.dumps(result, ensure_ascii=False, separators=(",", ":"))
        )
    return result


def bounded_text(value: str | None, field: str, maximum: int) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    if not stripped:
        raise ClientError(f"{field} cannot be empty")
    if len(stripped) > maximum:
        raise ClientError(f"{field} must be at most {maximum} characters")
    return stripped


def validate_e164(value: str) -> str:
    if not E164_RE.fullmatch(value):
        raise argparse.ArgumentTypeError("number must use E.164, for example +14155550100")
    if value.startswith("+86"):
        raise argparse.ArgumentTypeError(
            "mainland China numbers must use the ai-calls-china-phone skill"
        )
    return value


def validate_resource_id(value: str) -> str:
    if not RESOURCE_ID_RE.fullmatch(value):
        raise argparse.ArgumentTypeError("ID may contain only letters, numbers, _ and -")
    return value


def integer_between(minimum: int, maximum: int):
    def parse(value: str) -> int:
        try:
            parsed = int(value)
        except ValueError as exc:
            raise argparse.ArgumentTypeError("must be an integer") from exc
        if not minimum <= parsed <= maximum:
            raise argparse.ArgumentTypeError(f"must be between {minimum} and {maximum}")
        return parsed

    return parse


def require_confirmation(args: argparse.Namespace, action: str) -> None:
    if not args.confirm:
        raise ClientError(
            f"{action} blocked: obtain the user's explicit confirmation, then pass --confirm"
        )


def target_payload(args: argparse.Namespace) -> dict[str, Any]:
    to_number = getattr(args, "to_number", None)
    contact_query = bounded_text(getattr(args, "contact_query", None), "contact_query", 300)
    if bool(to_number) == bool(contact_query):
        raise ClientError("provide exactly one of --to-number or --contact-query")
    return {"to_number": to_number} if to_number else {"contact_query": contact_query}


def call_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload = target_payload(args)
    payload["task"] = bounded_text(args.task, "task", 20000)
    optionals = {
        "language": bounded_text(args.language, "language", 32),
        "first_message": bounded_text(args.first_message, "first_message", 300),
        "target_kind": args.target_kind,
    }
    payload.update({key: value for key, value in optionals.items() if value is not None})
    return payload


def command_register(args: argparse.Namespace) -> None:
    payload = {
        "name": bounded_text(args.name, "name", 64),
        "description": bounded_text(args.description, "description", 255),
        "source": bounded_text(args.source, "source", 32),
    }
    result = request(
        "POST",
        "/agent/v1/register",
        {key: value for key, value in payload.items() if value is not None},
        authenticated=False,
    )
    if not isinstance(result, dict) or not isinstance(result.get("token"), str):
        raise ClientError("register response did not include a token")
    path = write_token(result["token"])
    safe_result = {key: value for key, value in result.items() if key != "token"}
    safe_result["token_file"] = str(path)
    render_json(safe_result)


def command_simple_get(args: argparse.Namespace) -> None:
    render_json(request("GET", args.path))


def command_contacts(args: argparse.Namespace) -> None:
    render_json(
        request(
            "GET",
            "/agent/v1/contacts/search",
            query={"q": bounded_text(args.query, "query", 300), "language": args.language},
        )
    )


def command_call(args: argparse.Namespace) -> None:
    require_confirmation(args, "real call")
    key = bounded_text(args.idempotency_key, "idempotency_key", 200) or f"clawcall-{uuid.uuid4()}"
    result = request(
        "POST",
        "/agent/v1/call",
        call_payload(args),
        extra_headers={"Idempotency-Key": key},
    )
    if isinstance(result, dict):
        result = {**result, "client_idempotency_key": key}
    else:
        result = {"client_idempotency_key": key, "result": result}
    if not args.wait:
        render_json(result)
        return
    call_id = result.get("call_id")
    if not isinstance(call_id, str):
        raise ClientError("call was accepted but no call_id was returned")
    deadline = time.monotonic() + args.wait_timeout
    while time.monotonic() < deadline:
        time.sleep(args.poll_interval)
        status = request("GET", f"/agent/v1/call/{urllib.parse.quote(call_id, safe='')}")
        current = status.get("status") if isinstance(status, dict) else None
        if isinstance(current, str) and current.lower() in TERMINAL_STATUSES:
            if isinstance(status, dict):
                status = {**status, "client_idempotency_key": key}
            render_json(status)
            return
    raise ClientError(f"timed out waiting for call {call_id}; query it with ./callinfo.sh {call_id}")


def command_callinfo(args: argparse.Namespace) -> None:
    render_json(request("GET", f"/agent/v1/call/{urllib.parse.quote(args.call_id, safe='')}"))


def command_inbound(args: argparse.Namespace) -> None:
    render_json(
        request(
            "GET",
            "/agent/v1/inbound",
            query={"after": args.after, "limit": args.limit},
        )
    )


def command_inbound_prompt_get(_: argparse.Namespace) -> None:
    render_json(request("GET", "/agent/v1/inbound-prompt"))


def command_inbound_prompt_set(args: argparse.Namespace) -> None:
    require_confirmation(args, "inbound prompt update")
    render_json(
        request(
            "PUT",
            "/agent/v1/inbound-prompt",
            {"prompt": bounded_text(args.prompt, "prompt", 20000)},
        )
    )


def scheduled_at_ms(args: argparse.Namespace) -> int:
    now_ms = int(time.time() * 1000)
    if args.at_ms is not None:
        value = args.at_ms
    else:
        value = now_ms + args.in_minutes * 60 * 1000
    minimum = now_ms + 60 * 1000
    maximum = now_ms + 365 * 24 * 60 * 60 * 1000
    if not minimum <= value <= maximum:
        raise ClientError("scheduled time must be between one minute and 365 days in the future")
    return value


def command_schedule_create(args: argparse.Namespace) -> None:
    require_confirmation(args, "scheduled call")
    payload = call_payload(args)
    payload["scheduled_at"] = scheduled_at_ms(args)
    render_json(request("POST", "/agent/v1/scheduled-calls", payload))


def command_schedule_list(args: argparse.Namespace) -> None:
    render_json(request("GET", "/agent/v1/scheduled-calls", query={"limit": args.limit}))


def command_schedule_cancel(args: argparse.Namespace) -> None:
    require_confirmation(args, "scheduled call cancellation")
    schedule_id = urllib.parse.quote(args.schedule_id, safe="")
    render_json(request("POST", f"/agent/v1/scheduled-calls/{schedule_id}/cancel"))


def add_target_and_task(parser: argparse.ArgumentParser) -> None:
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--to-number", type=validate_e164)
    target.add_argument("--contact-query")
    parser.add_argument("--task", required=True)
    parser.add_argument("--language")
    parser.add_argument("--first-message")
    parser.add_argument("--target-kind", choices=("business", "user_provided"), required=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ClawCall Agent API client")
    parser.add_argument("--client-version", action="version", version=CLIENT_VERSION)
    subparsers = parser.add_subparsers(dest="command", required=True)

    register = subparsers.add_parser("register", help="register a pending Agent")
    register.add_argument("--name", required=True)
    register.add_argument("--description")
    register.add_argument("--source", default="openclaw")
    register.set_defaults(func=command_register)

    for name, path in (("status", "/agent/v1/status"), ("balance", "/agent/v1/balance")):
        child = subparsers.add_parser(name)
        child.set_defaults(func=command_simple_get, path=path)

    contacts = subparsers.add_parser("contacts", help="search public business numbers")
    contacts.add_argument("query")
    contacts.add_argument("--language")
    contacts.set_defaults(func=command_contacts)

    call = subparsers.add_parser("call", help="place one confirmed outbound call")
    add_target_and_task(call)
    call.add_argument("--idempotency-key")
    call.add_argument("--confirm", action="store_true")
    call.add_argument("--wait", action="store_true")
    call.add_argument("--wait-timeout", type=int, default=600)
    call.add_argument("--poll-interval", type=int, default=5)
    call.set_defaults(func=command_call)

    callinfo = subparsers.add_parser("callinfo", help="get one call result")
    callinfo.add_argument("call_id", type=validate_resource_id)
    callinfo.set_defaults(func=command_callinfo)

    inbound = subparsers.add_parser("inbound", help="read inbound calls")
    inbound.add_argument("--after", type=int, default=0)
    inbound.add_argument("--limit", type=integer_between(1, 100), default=20)
    inbound.set_defaults(func=command_inbound)

    prompt = subparsers.add_parser("inbound-prompt", help="read or update receptionist instructions")
    prompt_subparsers = prompt.add_subparsers(dest="prompt_command", required=True)
    prompt_get = prompt_subparsers.add_parser("get")
    prompt_get.set_defaults(func=command_inbound_prompt_get)
    prompt_set = prompt_subparsers.add_parser("set")
    prompt_set.add_argument("prompt")
    prompt_set.add_argument("--confirm", action="store_true")
    prompt_set.set_defaults(func=command_inbound_prompt_set)

    schedule = subparsers.add_parser("schedule", help="manage scheduled calls")
    schedule_subparsers = schedule.add_subparsers(dest="schedule_command", required=True)
    schedule_create = schedule_subparsers.add_parser("create")
    add_target_and_task(schedule_create)
    timing = schedule_create.add_mutually_exclusive_group(required=True)
    timing.add_argument("--at-ms", type=int)
    timing.add_argument("--in-minutes", type=int)
    schedule_create.add_argument("--confirm", action="store_true")
    schedule_create.set_defaults(func=command_schedule_create)
    schedule_list = schedule_subparsers.add_parser("list")
    schedule_list.add_argument("--limit", type=integer_between(1, 200), default=50)
    schedule_list.set_defaults(func=command_schedule_list)
    schedule_cancel = schedule_subparsers.add_parser("cancel")
    schedule_cancel.add_argument("schedule_id", type=validate_resource_id)
    schedule_cancel.add_argument("--confirm", action="store_true")
    schedule_cancel.set_defaults(func=command_schedule_cancel)
    return parser


def main() -> int:
    try:
        args = build_parser().parse_args()
        for field in ("after", "wait_timeout", "poll_interval", "in_minutes"):
            value = getattr(args, field, None)
            if value is not None and value < 0:
                raise ClientError(f"{field.replace('_', ' ')} cannot be negative")
        if getattr(args, "wait_timeout", 1) == 0 or getattr(args, "poll_interval", 1) == 0:
            raise ClientError("wait timeout and poll interval must be positive")
        args.func(args)
        return 0
    except ClientError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Cancelled.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())

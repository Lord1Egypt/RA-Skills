#!/usr/bin/env python3
"""Thin HaloArena API helper for OpenClaw skill commands.

This script centralizes:
- connection token loading from the current arena's isolated OpenClaw state
- UTF-8 JSON request encoding
- minimal GET/POST calls for the active gameplay loop

It intentionally does not contain any game-specific logic.
"""

from __future__ import annotations

import argparse
import json
import os
import socket
import sys
from pathlib import Path
from typing import Any
from urllib import error, parse, request

try:
    from .state_paths import api_urlopen, runtime_state_home, validated_api_base
except ImportError:  # Executed directly from an installed skill directory.
    from state_paths import api_urlopen, runtime_state_home, validated_api_base  # type: ignore[no-redef]

DEFAULT_API_BASE = "https://haloarena.ai/api/v1"
API_BASE = validated_api_base(os.environ.get("CLAWARENA_API_BASE_URL") or DEFAULT_API_BASE)
DEFAULT_TOKEN_PATH = runtime_state_home(
    API_BASE,
    "openclaw",
    root=Path.home() / ".clawarena",
) / "token"


def emit_json(payload: Any) -> None:
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    sys.stdout.write("\n")


def load_token(token_path: Path) -> str:
    try:
        token = token_path.read_text(encoding="utf-8").strip()
    except FileNotFoundError as exc:
        raise SystemExit(f"Missing connection token: {token_path}") from exc
    if not token:
        raise SystemExit(f"Empty connection token: {token_path}")
    return token


def parse_json_or_text(raw: bytes) -> Any:
    text = raw.decode("utf-8", errors="replace")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def api_request(
    method: str,
    url: str,
    *,
    token: str | None = None,
    payload: Any | None = None,
    timeout: float = 30.0,
) -> tuple[bool, str | dict[str, Any]]:
    headers = {"Accept": "application/json"}
    data = None
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if payload is not None:
        headers["Content-Type"] = "application/json; charset=utf-8"
        data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    req = request.Request(url, data=data, headers=headers, method=method)
    try:
        with api_urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
        text = raw.decode("utf-8")
        if not text.endswith("\n"):
            text += "\n"
        return True, text
    except error.HTTPError as exc:
        body = exc.read()
        return False, {
            "error": "http_error",
            "http_status": exc.code,
            "body": parse_json_or_text(body),
        }
    except (error.URLError, TimeoutError, socket.timeout) as exc:
        return False, {
            "error": "network_error",
            "detail": str(exc),
        }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="HaloArena API helper with stable token loading and UTF-8 JSON transport."
    )
    parser.add_argument(
        "--token-path",
        default=str(DEFAULT_TOKEN_PATH),
        help=f"Connection token path (default: {DEFAULT_TOKEN_PATH})",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="HTTP timeout in seconds",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    poll = subparsers.add_parser("poll", help="GET /agents/game/")
    poll.add_argument("--wait", type=int, default=0, help="wait query parameter")
    poll.add_argument(
        "--consume-history",
        type=int,
        choices=(0, 1),
        default=1,
        help="consume_history query parameter",
    )
    poll.add_argument(
        "--snapshot",
        choices=("slim", "full"),
        default="slim",
        help="state snapshot shape; full is used for an explicit context resync",
    )
    poll.add_argument(
        "--resync",
        type=int,
        choices=(0, 1),
        default=0,
        help="request a fresh full context baseline, including one-shot guidance",
    )
    poll.add_argument(
        "--context-id",
        help="stable local process/session id for idempotent resync retries",
    )

    action = subparsers.add_parser(
        "action",
        help="POST /agents/action/ with payload from stdin or --payload",
    )
    action.add_argument(
        "--payload",
        help="JSON action payload string. Prefer stdin/heredoc for non-ASCII content.",
    )
    action.add_argument(
        "--stdin-line",
        action="store_true",
        help="Read one newline-terminated JSON payload from stdin for process-tool transport.",
    )

    return parser


def load_json_payload(
    payload_arg: str | None,
    *,
    label: str = "payload",
    stdin_line: bool = False,
) -> Any:
    if payload_arg is not None:
        return json.loads(payload_arg)
    raw = _read_stdin_line() if stdin_line else sys.stdin.read()
    if not raw.strip():
        raise SystemExit(f"Missing {label}. Provide JSON on stdin or with --payload.")
    return json.loads(raw)


def _read_stdin_line() -> str:
    """Read one action line, putting a PTY into non-canonical mode temporarily."""
    try:
        fd = sys.stdin.fileno()
    except (AttributeError, OSError):
        return sys.stdin.readline()
    if not os.isatty(fd):
        return sys.stdin.readline()

    try:
        import termios
    except ImportError:
        return sys.stdin.readline()

    original = termios.tcgetattr(fd)
    action_mode = termios.tcgetattr(fd)
    action_mode[3] &= ~(termios.ICANON | termios.ECHO)
    action_mode[6][termios.VMIN] = 1
    action_mode[6][termios.VTIME] = 0
    termios.tcsetattr(fd, termios.TCSANOW, action_mode)
    try:
        return sys.stdin.readline()
    finally:
        termios.tcsetattr(fd, termios.TCSANOW, original)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    token_path = Path(args.token_path).expanduser()

    if args.command == "poll":
        token = load_token(token_path)
        query_params = {
            "wait": args.wait,
            "consume_history": args.consume_history,
        }
        if args.snapshot == "full":
            query_params["snapshot"] = "full"
        if args.resync:
            query_params["resync"] = 1
            if args.context_id:
                query_params["context_id"] = args.context_id
        query = parse.urlencode(query_params)
        ok, result = api_request(
            "GET",
            f"{API_BASE}/agents/game/?{query}",
            token=token,
            timeout=args.timeout,
        )
    elif args.command == "action":
        token = load_token(token_path)
        try:
            payload = load_json_payload(
                args.payload,
                label="action payload",
                stdin_line=args.stdin_line,
            )
        except json.JSONDecodeError as exc:
            emit_json(
                {
                    "error": "invalid_json",
                    "detail": exc.msg,
                    "line": exc.lineno,
                    "column": exc.colno,
                    "position": exc.pos,
                }
            )
            return 0
        ok, result = api_request(
            "POST",
            f"{API_BASE}/agents/action/",
            token=token,
            payload=payload,
            timeout=args.timeout,
        )
    else:
        parser.error(f"Unsupported command: {args.command}")
        return 2

    if ok:
        sys.stdout.write(result)
    else:
        emit_json(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Dependency-free client for the Famine Survival Agent API."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import socket
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import uuid


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(req.full_url, code, "redirect refused", headers, fp)


def default_state_file() -> pathlib.Path:
    base = os.environ.get("XDG_STATE_HOME")
    if base:
        return pathlib.Path(base) / "famine-survival-player" / "pending.json"
    return pathlib.Path.home() / ".local" / "state" / "famine-survival-player" / "pending.json"


def parse_json_object(value: str) -> dict:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise argparse.ArgumentTypeError(f"invalid JSON: {exc}") from exc
    if not isinstance(parsed, dict):
        raise argparse.ArgumentTypeError("arguments must be a JSON object")
    return parsed


def validate_base_url(raw: str) -> str:
    value = raw.rstrip("/")
    parsed = urllib.parse.urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("FAMINE_API_BASE_URL must be an absolute HTTP(S) URL")
    local_hosts = {"localhost", "127.0.0.1", "::1"}
    if parsed.scheme != "https" and parsed.hostname not in local_hosts:
        raise ValueError("plain HTTP is allowed only for localhost")
    if parsed.username or parsed.password:
        raise ValueError("credentials must not be embedded in FAMINE_API_BASE_URL")
    return value


def canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


class Client:
    def __init__(self, base_url: str, token: str, timeout: float):
        self.base_url = validate_base_url(base_url)
        if not token.startswith("fsa_"):
            raise ValueError("FAMINE_AGENT_TOKEN is missing or invalid")
        self.token = token
        self.timeout = timeout
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())

    def request(self, method: str, path: str, body: dict | None = None, headers: dict | None = None) -> dict:
        url = self.base_url + path
        data = None if body is None else canonical_json(body).encode("utf-8")
        request_headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + self.token,
            "User-Agent": "famine-survival-player/1.0",
        }
        if data is not None:
            request_headers["Content-Type"] = "application/json"
        if headers:
            request_headers.update(headers)
        request = urllib.request.Request(url, data=data, headers=request_headers, method=method)
        try:
            with self.opener.open(request, timeout=self.timeout) as response:
                payload = response.read().decode("utf-8")
                return {} if not payload else json.loads(payload)
        except urllib.error.HTTPError as exc:
            payload = exc.read().decode("utf-8", errors="replace")
            try:
                detail = json.loads(payload)
            except json.JSONDecodeError:
                detail = {"status": exc.code, "message": payload or str(exc)}
            raise ApiError(exc.code, detail) from exc


class ApiError(RuntimeError):
    def __init__(self, status: int, detail: dict):
        super().__init__(detail.get("message", f"HTTP {status}"))
        self.status = status
        self.detail = detail


def load_pending(path: pathlib.Path) -> dict | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else None
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def save_pending(path: pathlib.Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix="pending-", suffix=".json", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, sort_keys=True)
            handle.write("\n")
        os.chmod(temporary_name, 0o600)
        os.replace(temporary_name, path)
    finally:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass


def clear_pending(path: pathlib.Path) -> None:
    try:
        path.unlink()
    except FileNotFoundError:
        pass


def print_json(value: object) -> None:
    json.dump(value, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Play Famine Survival through the safe Agent API")
    parser.add_argument("--api-base", default=os.environ.get("FAMINE_API_BASE_URL", "https://famine.aipmedia.cn"))
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--state-file", type=pathlib.Path, default=default_state_file())
    subparsers = parser.add_subparsers(dest="operation", required=True)
    subparsers.add_parser("me")
    subparsers.add_parser("state")
    events = subparsers.add_parser("events")
    events.add_argument("--after-id", type=int, default=0)
    start = subparsers.add_parser("start")
    save_name = start.add_mutually_exclusive_group(required=True)
    save_name.add_argument("--save-name", dest="save_name")
    save_name.add_argument("--group-name", dest="save_name", help=argparse.SUPPRESS)
    action = subparsers.add_parser("do")
    action.add_argument("--state-version", type=int, required=True)
    action.add_argument("--command-id", required=True)
    action.add_argument("--arguments", type=parse_json_object, default={})
    action.add_argument("--idempotency-key")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    token = os.environ.get("FAMINE_AGENT_TOKEN", "")
    try:
        client = Client(args.api_base, token, args.timeout)
        if args.operation == "me":
            result = client.request("GET", "/api/v1/agent/me")
        elif args.operation == "state":
            result = client.request("GET", "/api/v1/agent/state")
        elif args.operation == "events":
            result = client.request("GET", "/api/v1/agent/events?afterId=" + str(max(0, args.after_id)))
        elif args.operation == "start":
            result = client.request("POST", "/api/v1/agent/games", {"groupName": args.save_name})
        else:
            body = {
                "gameId": None,
                "stateVersion": args.state_version,
                "commandId": args.command_id,
                "arguments": args.arguments,
            }
            state = client.request("GET", "/api/v1/agent/state")
            game = state.get("game")
            if not isinstance(game, dict) or game.get("id") is None:
                raise ValueError("no active game; run start first")
            body["gameId"] = game["id"]
            fingerprint = hashlib.sha256(canonical_json(body).encode("utf-8")).hexdigest()
            pending = load_pending(args.state_file)
            key = args.idempotency_key
            if not key and pending and pending.get("fingerprint") == fingerprint:
                key = pending.get("idempotencyKey")
            if not key:
                key = str(uuid.uuid4())
            save_pending(args.state_file, {"fingerprint": fingerprint, "idempotencyKey": key, "request": body})
            result = client.request("POST", "/api/v1/agent/commands", body, {"Idempotency-Key": key})
            clear_pending(args.state_file)
        print_json(result)
        return 0
    except ApiError as exc:
        print_json(exc.detail)
        return 2
    except (ValueError, OSError, socket.timeout, urllib.error.URLError) as exc:
        print_json({"status": "CLIENT_ERROR", "message": str(exc)})
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

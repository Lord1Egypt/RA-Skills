#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib import parse


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def cookie_alive_script() -> Path:
    return repo_root() / "scripts" / "cookie_alive.py"


def first_value(query: dict[str, list[str]], key: str, default: str | None = None) -> str | None:
    values = query.get(key)
    if not values:
        return default
    return values[0]


def parse_bool(raw_value: str | None, default: bool = False) -> bool:
    if raw_value is None:
        return default
    return raw_value.lower() in {"1", "true", "yes", "on"}


def build_cookie_alive_command(
    python_executable: str,
    db_name: str,
    command_name: str,
    profile: str | None = None,
    output_format: str | None = None,
    refresh: bool = False,
    active_only: bool = False,
    timeout_seconds: str | None = None,
) -> list[str]:
    command = [
        python_executable,
        str(cookie_alive_script()),
        "--db-name",
        db_name,
        command_name,
    ]
    if profile:
        command.extend(["--profile", profile])
    if output_format:
        command.extend(["--format", output_format])
    if refresh:
        command.append("--refresh")
    if active_only:
        command.append("--active-only")
    if timeout_seconds:
        command.extend(["--timeout-seconds", timeout_seconds])
    return command


def run_cookie_alive(command: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(
        command,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


class CookieAliveAPIHandler(BaseHTTPRequestHandler):
    server_version = "CookieAliveHTTP/1.0"

    @property
    def config(self) -> argparse.Namespace:
        return self.server.config  # type: ignore[attr-defined]

    def log_message(self, format: str, *args) -> None:
        return

    def do_GET(self) -> None:
        parsed = parse.urlparse(self.path)
        route = parsed.path.rstrip("/") or "/"
        query = parse.parse_qs(parsed.query)

        try:
            if route == "/":
                self.respond_json(
                    200,
                    {
                        "service": "cookie_alive_http_wrapper",
                        "routes": ["/health", "/pull", "/check", "/list"],
                    },
                )
                return
            if route == "/health":
                self.respond_json(200, {"ok": True})
                return
            if route == "/pull":
                self.handle_pull(query)
                return
            if route == "/check":
                self.handle_check(query)
                return
            if route == "/list":
                self.handle_list(query)
                return
            self.respond_json(404, {"error": f"unknown route: {route}"})
        except Exception as exc:
            self.respond_json(500, {"error": str(exc)})

    def handle_pull(self, query: dict[str, list[str]]) -> None:
        db_name = first_value(query, "db_name", self.config.db_name) or self.config.db_name
        profile = first_value(query, "profile", self.config.profile)
        output_format = first_value(query, "format", "header") or "header"
        refresh = parse_bool(first_value(query, "refresh"), default=False)
        timeout_seconds = first_value(query, "timeout_seconds")
        if not profile:
            self.respond_json(400, {"error": "missing profile"})
            return

        command = build_cookie_alive_command(
            python_executable=self.config.python_executable,
            db_name=db_name,
            command_name="pull",
            profile=profile,
            output_format=output_format,
            refresh=refresh,
            timeout_seconds=timeout_seconds,
        )
        returncode, stdout, stderr = run_cookie_alive(command)
        if returncode != 0:
            self.respond_json(
                502,
                {
                    "error": stderr or stdout or f"cookie_alive exited with {returncode}",
                    "command": command,
                },
            )
            return

        if output_format == "header":
            self.respond_text(200, stdout)
            return
        self.respond_json(200, json.loads(stdout))

    def handle_check(self, query: dict[str, list[str]]) -> None:
        db_name = first_value(query, "db_name", self.config.db_name) or self.config.db_name
        profile = first_value(query, "profile", self.config.profile)
        timeout_seconds = first_value(query, "timeout_seconds")
        if not profile:
            self.respond_json(400, {"error": "missing profile"})
            return

        command = build_cookie_alive_command(
            python_executable=self.config.python_executable,
            db_name=db_name,
            command_name="check",
            profile=profile,
            timeout_seconds=timeout_seconds,
        )
        returncode, stdout, stderr = run_cookie_alive(command)
        if not stdout:
            self.respond_json(
                502,
                {
                    "error": stderr or f"cookie_alive exited with {returncode}",
                    "command": command,
                },
            )
            return

        payload = json.loads(stdout)
        status_code = 200 if returncode == 0 else 409
        self.respond_json(status_code, payload)

    def handle_list(self, query: dict[str, list[str]]) -> None:
        db_name = first_value(query, "db_name", self.config.db_name) or self.config.db_name
        active_only = parse_bool(first_value(query, "active_only"), default=False)

        command = build_cookie_alive_command(
            python_executable=self.config.python_executable,
            db_name=db_name,
            command_name="list",
            active_only=active_only,
        )
        returncode, stdout, stderr = run_cookie_alive(command)
        if returncode != 0:
            self.respond_json(
                502,
                {
                    "error": stderr or stdout or f"cookie_alive exited with {returncode}",
                    "command": command,
                },
            )
            return
        self.respond_json(200, json.loads(stdout))

    def respond_text(self, status_code: int, payload: str) -> None:
        body = payload.encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def respond_json(self, status_code: int, payload: object) -> None:
        body = json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Local HTTP wrapper around cookie_alive for software that prefers HTTP over subprocess.",
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    parser.add_argument("--python-executable", default=sys.executable)
    parser.add_argument("--db-name", default="chsi")
    parser.add_argument("--profile", default="main")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    server = ThreadingHTTPServer((args.host, args.port), CookieAliveAPIHandler)
    server.config = args  # type: ignore[attr-defined]

    print(f"cookie_alive HTTP wrapper listening on http://{args.host}:{args.port}")
    print("routes: /health, /pull, /check, /list")
    print(f"default db_name={args.db_name} profile={args.profile}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

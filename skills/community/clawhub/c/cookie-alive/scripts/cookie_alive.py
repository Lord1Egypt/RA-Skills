#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import sys
import time
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from http.cookies import CookieError, SimpleCookie
from pathlib import Path
from typing import Any
from urllib import error, parse, request

DEFAULT_DB_NAME = "default"
DEFAULT_INTERVAL_SECONDS = 900
DEFAULT_TIMEOUT_SECONDS = 30
DEFAULT_USER_AGENT = "cookie_alive/1.0"
HOME_ENV_KEYS = ("COOKIE_ALIVE_HOME", "SESSION_COOKIE_ONLINE_HOME")
DB_NAME_ENV_KEYS = ("COOKIE_ALIVE_DB_NAME", "SESSION_COOKIE_ONLINE_DB_NAME")
DB_NAME_PATTERN = re.compile(r"^[A-Za-z0-9._-]+$")

SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
    profile TEXT PRIMARY KEY,
    refresh_url TEXT NOT NULL,
    method TEXT NOT NULL,
    interval_seconds INTEGER NOT NULL,
    timeout_seconds INTEGER NOT NULL,
    cookie_json TEXT NOT NULL,
    headers_json TEXT NOT NULL,
    body TEXT,
    active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    last_refreshed_at TEXT,
    last_status_code INTEGER,
    last_error TEXT
);
"""


class NoRedirectHandler(request.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        return fp

    def http_error_302(self, req, fp, code, msg, headers):
        return fp

    def http_error_303(self, req, fp, code, msg, headers):
        return fp

    def http_error_307(self, req, fp, code, msg, headers):
        return fp

    def http_error_308(self, req, fp, code, msg, headers):
        return fp


class RefreshFailure(RuntimeError):
    pass


@dataclass
class SessionRecord:
    profile: str
    refresh_url: str
    method: str
    interval_seconds: int
    timeout_seconds: int
    cookies: dict[str, str]
    headers: dict[str, str]
    body: str | None
    active: bool
    created_at: str
    updated_at: str
    last_refreshed_at: str | None
    last_status_code: int | None
    last_error: str | None

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "SessionRecord":
        return cls(
            profile=row["profile"],
            refresh_url=row["refresh_url"],
            method=row["method"],
            interval_seconds=row["interval_seconds"],
            timeout_seconds=row["timeout_seconds"],
            cookies=json.loads(row["cookie_json"]),
            headers=json.loads(row["headers_json"]),
            body=row["body"],
            active=bool(row["active"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            last_refreshed_at=row["last_refreshed_at"],
            last_status_code=row["last_status_code"],
            last_error=row["last_error"],
        )

    def cookie_header(self) -> str:
        return render_cookie_header(self.cookies)

    def to_dict(self) -> dict[str, Any]:
        return {
            "profile": self.profile,
            "refresh_url": self.refresh_url,
            "method": self.method,
            "interval_seconds": self.interval_seconds,
            "timeout_seconds": self.timeout_seconds,
            "cookies": dict(self.cookies),
            "cookie_header": self.cookie_header(),
            "headers": dict(self.headers),
            "body": self.body,
            "active": self.active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "last_refreshed_at": self.last_refreshed_at,
            "last_status_code": self.last_status_code,
            "last_error": self.last_error,
            "last_alive": infer_last_alive(self),
        }


def current_utc_dt() -> datetime:
    return datetime.now(timezone.utc)


def utc_now() -> str:
    return current_utc_dt().replace(microsecond=0).isoformat()


def parse_utc(raw_value: str | None) -> datetime | None:
    if not raw_value:
        return None
    return datetime.fromisoformat(raw_value)


def infer_last_alive(record: SessionRecord) -> bool | None:
    if record.last_status_code is None:
        return None
    return record.last_error is None and 200 <= record.last_status_code < 300


def build_check_payload(record: SessionRecord, alive: bool) -> dict[str, Any]:
    return {
        "profile": record.profile,
        "refresh_url": record.refresh_url,
        "alive": alive,
        "active": record.active,
        "interval_seconds": record.interval_seconds,
        "last_refreshed_at": record.last_refreshed_at,
        "last_status_code": record.last_status_code,
        "last_error": record.last_error,
        "cookie_header": record.cookie_header(),
    }


def seconds_until_due(record: SessionRecord, now: datetime | None = None) -> float:
    if record.last_refreshed_at is None:
        return 0.0
    now = now or current_utc_dt()
    last_refreshed = parse_utc(record.last_refreshed_at)
    if last_refreshed is None:
        return 0.0
    elapsed = (now - last_refreshed).total_seconds()
    return max(0.0, float(record.interval_seconds) - elapsed)


def first_env(keys: tuple[str, ...]) -> str | None:
    for key in keys:
        value = os.environ.get(key)
        if value:
            return value
    return None


def resolve_storage_root() -> Path:
    override = first_env(HOME_ENV_KEYS)
    if override:
        return Path(override).expanduser()
    return Path.home() / ".cookie_alive"


def resolve_db_path(db_name: str | None = None) -> Path:
    chosen = (db_name or first_env(DB_NAME_ENV_KEYS) or DEFAULT_DB_NAME).strip()
    if chosen.endswith(".db"):
        chosen = chosen[:-3]
    if not chosen:
        raise ValueError("db name must not be empty")
    if not DB_NAME_PATTERN.fullmatch(chosen):
        raise ValueError("db name must use letters, digits, dots, hyphens, or underscores only")
    return resolve_storage_root() / f"{chosen}.db"


def ensure_positive_int(value: int, label: str) -> int:
    if value <= 0:
        raise ValueError(f"{label} must be greater than zero")
    return value


def ensure_non_negative_float(value: float, label: str) -> float:
    if value < 0:
        raise ValueError(f"{label} must be zero or greater")
    return value


def ensure_http_url(raw_url: str) -> str:
    parsed = parse.urlparse(raw_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"refresh url must be a valid http/https URL: {raw_url}")
    return raw_url


def normalize_str_map(raw_map: dict[str, Any], label: str) -> dict[str, str]:
    cleaned: dict[str, str] = {}
    for key, value in raw_map.items():
        key_text = str(key).strip()
        if not key_text:
            raise ValueError(f"{label} contains an empty key")
        cleaned[key_text] = str(value)
    return cleaned


def parse_json_object(raw_text: str, label: str) -> dict[str, str]:
    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{label} is not valid JSON: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ValueError(f"{label} must be a JSON object")
    return normalize_str_map(parsed, label)


def parse_cookie_header(raw_header: str) -> dict[str, str]:
    if not raw_header.strip():
        raise ValueError("cookie header must not be empty")
    parsed: dict[str, str] = {}
    cookie = SimpleCookie()
    try:
        cookie.load(raw_header)
    except CookieError:
        cookie = SimpleCookie()
    if cookie:
        for name, morsel in cookie.items():
            parsed[name] = morsel.value
        return parsed
    for part in raw_header.split(";"):
        chunk = part.strip()
        if not chunk:
            continue
        if "=" not in chunk:
            raise ValueError(f"invalid cookie chunk: {chunk}")
        name, value = chunk.split("=", 1)
        parsed[name.strip()] = value.strip()
    if not parsed:
        raise ValueError("cookie header must contain at least one cookie")
    return parsed


def read_cookie_source(args: argparse.Namespace) -> dict[str, str]:
    if args.cookie_header:
        return parse_cookie_header(args.cookie_header)
    if args.cookie_json:
        return parse_json_object(args.cookie_json, "cookie json")
    if args.cookie_file:
        text = Path(args.cookie_file).read_text(encoding="utf-8").strip()
        if text.startswith("{"):
            return parse_json_object(text, f"cookie file {args.cookie_file}")
        return parse_cookie_header(text)
    raise ValueError("one cookie source is required")


def parse_header_line(raw_header: str) -> tuple[str, str]:
    if ":" not in raw_header:
        raise ValueError(f"header must use 'Name: value' format: {raw_header}")
    name, value = raw_header.split(":", 1)
    name = name.strip()
    value = value.strip()
    if not name:
        raise ValueError(f"header name is empty: {raw_header}")
    return name, value


def read_headers(args: argparse.Namespace) -> dict[str, str]:
    headers: dict[str, str] = {}
    if args.headers_json:
        headers.update(parse_json_object(args.headers_json, "headers json"))
    for raw_header in args.header or []:
        name, value = parse_header_line(raw_header)
        headers[name] = value
    headers.setdefault("User-Agent", DEFAULT_USER_AGENT)
    return headers


def render_cookie_header(cookies: dict[str, str]) -> str:
    return "; ".join(f"{name}={value}" for name, value in sorted(cookies.items()))


def merge_set_cookie_headers(
    existing_cookies: dict[str, str],
    set_cookie_headers: list[str] | None,
) -> dict[str, str]:
    merged = dict(existing_cookies)
    for header_value in set_cookie_headers or []:
        parsed = SimpleCookie()
        try:
            parsed.load(header_value)
        except CookieError:
            continue
        for name, morsel in parsed.items():
            max_age = (morsel["max-age"] or "").strip()
            if max_age == "0" or morsel.value == "":
                merged.pop(name, None)
                continue
            merged[name] = morsel.value
    return merged


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


@contextmanager
def managed_connection(db_path: Path):
    conn = connect(db_path)
    try:
        yield conn
    finally:
        conn.close()


def fetch_profile(conn: sqlite3.Connection, profile: str) -> SessionRecord | None:
    row = conn.execute("SELECT * FROM sessions WHERE profile = ?", (profile,)).fetchone()
    return SessionRecord.from_row(row) if row else None


def require_profile(conn: sqlite3.Connection, profile: str) -> SessionRecord:
    record = fetch_profile(conn, profile)
    if record is None:
        raise ValueError(f"profile not found: {profile}")
    return record


def upsert_profile(
    db_path: Path,
    profile: str,
    refresh_url: str,
    method: str,
    interval_seconds: int,
    timeout_seconds: int,
    cookies: dict[str, str],
    headers: dict[str, str],
    body: str | None,
    active: bool,
) -> SessionRecord:
    profile = profile.strip()
    if not profile:
        raise ValueError("profile must not be empty")
    method = method.strip().upper()
    if not method.isalpha():
        raise ValueError("method must contain letters only")
    refresh_url = ensure_http_url(refresh_url)
    interval_seconds = ensure_positive_int(interval_seconds, "interval_seconds")
    timeout_seconds = ensure_positive_int(timeout_seconds, "timeout_seconds")
    cookies = normalize_str_map(cookies, "cookies")
    headers = normalize_str_map(headers, "headers")
    now = utc_now()

    with managed_connection(db_path) as conn:
        conn.execute(
            """
            INSERT INTO sessions (
                profile,
                refresh_url,
                method,
                interval_seconds,
                timeout_seconds,
                cookie_json,
                headers_json,
                body,
                active,
                created_at,
                updated_at,
                last_error
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)
            ON CONFLICT(profile) DO UPDATE SET
                refresh_url = excluded.refresh_url,
                method = excluded.method,
                interval_seconds = excluded.interval_seconds,
                timeout_seconds = excluded.timeout_seconds,
                cookie_json = excluded.cookie_json,
                headers_json = excluded.headers_json,
                body = excluded.body,
                active = excluded.active,
                updated_at = excluded.updated_at,
                last_error = NULL
            """,
            (
                profile,
                refresh_url,
                method,
                interval_seconds,
                timeout_seconds,
                json.dumps(cookies, sort_keys=True),
                json.dumps(headers, sort_keys=True),
                body,
                int(active),
                now,
                now,
            ),
        )
        conn.commit()
        return require_profile(conn, profile)


def list_profiles(db_path: Path, active_only: bool = False) -> list[SessionRecord]:
    query = "SELECT * FROM sessions"
    if active_only:
        query += " WHERE active = 1"
    query += " ORDER BY profile"
    with managed_connection(db_path) as conn:
        rows = conn.execute(query).fetchall()
        return [SessionRecord.from_row(row) for row in rows]


def delete_profile(db_path: Path, profile: str) -> bool:
    with managed_connection(db_path) as conn:
        cursor = conn.execute("DELETE FROM sessions WHERE profile = ?", (profile,))
        conn.commit()
        return cursor.rowcount > 0


def save_refresh_result(
    conn: sqlite3.Connection,
    profile: str,
    cookies: dict[str, str],
    status_code: int | None,
    error_text: str | None,
) -> None:
    now = utc_now()
    conn.execute(
        """
        UPDATE sessions
        SET cookie_json = ?,
            last_refreshed_at = ?,
            last_status_code = ?,
            last_error = ?,
            updated_at = ?
        WHERE profile = ?
        """,
        (
            json.dumps(cookies, sort_keys=True),
            now,
            status_code,
            error_text,
            now,
            profile,
        ),
    )
    conn.commit()


def refresh_profile(
    db_path: Path,
    profile: str,
    timeout_override: int | None = None,
) -> SessionRecord:
    with managed_connection(db_path) as conn:
        record = require_profile(conn, profile)
        headers = dict(record.headers)
        cookie_header = record.cookie_header()
        if cookie_header:
            headers["Cookie"] = cookie_header
        headers.setdefault("User-Agent", DEFAULT_USER_AGENT)
        body_bytes = record.body.encode("utf-8") if record.body is not None else None
        timeout_seconds = ensure_positive_int(timeout_override, "timeout_seconds") if timeout_override else record.timeout_seconds
        http_request = request.Request(
            record.refresh_url,
            data=body_bytes,
            headers=headers,
            method=record.method,
        )
        opener = request.build_opener(NoRedirectHandler)
        try:
            with opener.open(http_request, timeout=timeout_seconds) as response:
                merged = merge_set_cookie_headers(
                    record.cookies,
                    response.headers.get_all("Set-Cookie"),
                )
                if 200 <= response.status < 300:
                    save_refresh_result(conn, record.profile, merged, response.status, None)
                else:
                    location = response.headers.get("Location")
                    detail = f"HTTP {response.status}"
                    if location:
                        detail = f"{detail}: redirect to {location}"
                    save_refresh_result(conn, record.profile, merged, response.status, detail)
                    raise RefreshFailure(detail)
        except error.HTTPError as exc:
            merged = merge_set_cookie_headers(
                record.cookies,
                exc.headers.get_all("Set-Cookie") if exc.headers else None,
            )
            save_refresh_result(conn, record.profile, merged, exc.code, f"HTTP {exc.code}: {exc.reason}")
            raise
        except RefreshFailure:
            raise
        except Exception as exc:
            save_refresh_result(conn, record.profile, record.cookies, None, str(exc))
            raise
        return require_profile(conn, profile)


def check_profile(
    db_path: Path,
    profile: str,
    timeout_override: int | None = None,
) -> tuple[bool, dict[str, Any]]:
    try:
        record = refresh_profile(db_path, profile, timeout_override=timeout_override)
        return True, build_check_payload(record, True)
    except Exception:
        with managed_connection(db_path) as conn:
            record = require_profile(conn, profile)
        return False, build_check_payload(record, False)


def run_profile(
    db_path: Path,
    profile: str,
    iterations: int | None,
    wait_seconds: float | None,
    timeout_override: int | None,
    stop_on_error: bool,
) -> list[dict[str, Any]]:
    if iterations is not None:
        ensure_positive_int(iterations, "iterations")
    if wait_seconds is not None:
        ensure_non_negative_float(wait_seconds, "wait_seconds")

    results: list[dict[str, Any]] = []
    count = 0
    while iterations is None or count < iterations:
        count += 1
        try:
            record = refresh_profile(db_path, profile, timeout_override=timeout_override)
            results.append(
                {
                    "iteration": count,
                    "ok": True,
                    "profile": profile,
                    "last_status_code": record.last_status_code,
                    "last_error": record.last_error,
                    "cookie_header": record.cookie_header(),
                }
            )
        except Exception as exc:
            results.append(
                {
                    "iteration": count,
                    "ok": False,
                    "profile": profile,
                    "last_status_code": None,
                    "last_error": str(exc),
                    "cookie_header": "",
                }
            )
            if stop_on_error:
                raise
        if iterations is not None and count >= iterations:
            break
        delay = wait_seconds
        if delay is None:
            with managed_connection(db_path) as conn:
                delay = float(require_profile(conn, profile).interval_seconds)
        if delay > 0:
            time.sleep(delay)
    return results


def run_all_profiles(
    db_path: Path,
    iterations: int | None,
    timeout_override: int | None,
    stop_on_error: bool,
    max_sleep_seconds: float,
) -> list[dict[str, Any]]:
    if iterations is not None:
        ensure_positive_int(iterations, "iterations")
    ensure_non_negative_float(max_sleep_seconds, "max_sleep_seconds")

    results: list[dict[str, Any]] = []
    executed = 0
    while iterations is None or executed < iterations:
        active_records = list_profiles(db_path, active_only=True)
        if not active_records:
            raise ValueError("no active profiles found")

        now = current_utc_dt()
        due_records = [record for record in active_records if seconds_until_due(record, now) <= 0]
        if due_records:
            for record in due_records:
                alive, payload = check_profile(
                    db_path,
                    record.profile,
                    timeout_override=timeout_override,
                )
                payload["iteration"] = executed + 1
                results.append(payload)
                executed += 1
                if not alive and stop_on_error:
                    raise RefreshFailure(payload["last_error"] or f"profile {record.profile} is not alive")
                if iterations is not None and executed >= iterations:
                    break
            continue

        next_due = min(seconds_until_due(record, now) for record in active_records)
        if next_due > 0:
            time.sleep(min(next_due, max_sleep_seconds))
    return results


def print_json(payload: Any) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def handle_upsert(args: argparse.Namespace) -> int:
    record = upsert_profile(
        db_path=resolve_db_path(args.db_name),
        profile=args.profile,
        refresh_url=args.refresh_url,
        method=args.method,
        interval_seconds=args.interval_seconds,
        timeout_seconds=args.timeout_seconds,
        cookies=read_cookie_source(args),
        headers=read_headers(args),
        body=args.body,
        active=not args.inactive,
    )
    print_json(record.to_dict())
    return 0


def handle_get(args: argparse.Namespace) -> int:
    with managed_connection(resolve_db_path(args.db_name)) as conn:
        record = require_profile(conn, args.profile)
    emit_record(record, args.format)
    return 0


def emit_record(record: SessionRecord, output_format: str) -> None:
    if output_format == "header":
        print(record.cookie_header())
    elif output_format == "json":
        print_json(record.cookies)
    else:
        print_json(record.to_dict())


def handle_pull(args: argparse.Namespace) -> int:
    db_path = resolve_db_path(args.db_name)
    if args.refresh:
        record = refresh_profile(
            db_path,
            args.profile,
            timeout_override=args.timeout_seconds,
        )
    else:
        with managed_connection(db_path) as conn:
            record = require_profile(conn, args.profile)
    emit_record(record, args.format)
    return 0


def handle_list(args: argparse.Namespace) -> int:
    records = [record.to_dict() for record in list_profiles(resolve_db_path(args.db_name), active_only=args.active_only)]
    print_json(records)
    return 0


def handle_delete(args: argparse.Namespace) -> int:
    deleted = delete_profile(resolve_db_path(args.db_name), args.profile)
    print_json({"profile": args.profile, "deleted": deleted})
    return 0


def handle_refresh(args: argparse.Namespace) -> int:
    record = refresh_profile(
        resolve_db_path(args.db_name),
        args.profile,
        timeout_override=args.timeout_seconds,
    )
    print_json(record.to_dict())
    return 0


def handle_check(args: argparse.Namespace) -> int:
    alive, payload = check_profile(
        resolve_db_path(args.db_name),
        args.profile,
        timeout_override=args.timeout_seconds,
    )
    print_json(payload)
    return 0 if alive else 1


def handle_run(args: argparse.Namespace) -> int:
    results = run_profile(
        db_path=resolve_db_path(args.db_name),
        profile=args.profile,
        iterations=args.iterations,
        wait_seconds=args.wait_seconds,
        timeout_override=args.timeout_seconds,
        stop_on_error=args.stop_on_error,
    )
    print_json(results)
    return 0


def handle_run_all(args: argparse.Namespace) -> int:
    results = run_all_profiles(
        db_path=resolve_db_path(args.db_name),
        iterations=args.iterations,
        timeout_override=args.timeout_seconds,
        stop_on_error=args.stop_on_error,
        max_sleep_seconds=args.max_sleep_seconds,
    )
    print_json(results)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Persist and refresh session cookies in a local SQLite store.",
    )
    parser.add_argument(
        "--db-name",
        help="Database name under ~/.cookie_alive/<db_name>.db. Defaults to env or 'default'.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    upsert_parser = subparsers.add_parser("upsert", help="Create or update a cookie profile.")
    upsert_parser.add_argument("--profile", required=True)
    upsert_parser.add_argument("--refresh-url", required=True)
    upsert_parser.add_argument("--method", default="GET")
    upsert_parser.add_argument("--interval-seconds", type=int, default=DEFAULT_INTERVAL_SECONDS)
    upsert_parser.add_argument("--timeout-seconds", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    upsert_parser.add_argument("--body")
    upsert_parser.add_argument("--header", action="append", default=[])
    upsert_parser.add_argument("--headers-json")
    upsert_parser.add_argument("--inactive", action="store_true")
    cookie_group = upsert_parser.add_mutually_exclusive_group(required=True)
    cookie_group.add_argument("--cookie-header")
    cookie_group.add_argument("--cookie-json")
    cookie_group.add_argument("--cookie-file")
    upsert_parser.set_defaults(func=handle_upsert)

    get_parser = subparsers.add_parser("get", help="Read cookies or profile metadata.")
    get_parser.add_argument("--profile", required=True)
    get_parser.add_argument("--format", choices=("header", "json", "record"), default="header")
    get_parser.set_defaults(func=handle_get)

    pull_parser = subparsers.add_parser("pull", help="Export cookies for another program, optionally after a refresh.")
    pull_parser.add_argument("--profile", required=True)
    pull_parser.add_argument("--format", choices=("header", "json", "record"), default="header")
    pull_parser.add_argument("--refresh", action="store_true")
    pull_parser.add_argument("--timeout-seconds", type=int)
    pull_parser.set_defaults(func=handle_pull)

    list_parser = subparsers.add_parser("list", help="List profiles in the database.")
    list_parser.add_argument("--active-only", action="store_true")
    list_parser.set_defaults(func=handle_list)

    delete_parser = subparsers.add_parser("delete", help="Delete a profile.")
    delete_parser.add_argument("--profile", required=True)
    delete_parser.set_defaults(func=handle_delete)

    refresh_parser = subparsers.add_parser("refresh", help="Refresh one profile once.")
    refresh_parser.add_argument("--profile", required=True)
    refresh_parser.add_argument("--timeout-seconds", type=int)
    refresh_parser.set_defaults(func=handle_refresh)

    check_parser = subparsers.add_parser("check", help="Check whether one profile is still alive.")
    check_parser.add_argument("--profile", required=True)
    check_parser.add_argument("--timeout-seconds", type=int)
    check_parser.set_defaults(func=handle_check)

    run_parser = subparsers.add_parser("run", help="Run the keepalive loop for one profile.")
    run_parser.add_argument("--profile", required=True)
    run_parser.add_argument("--iterations", type=int)
    run_parser.add_argument("--wait-seconds", type=float)
    run_parser.add_argument("--timeout-seconds", type=int)
    run_parser.add_argument("--stop-on-error", action="store_true")
    run_parser.set_defaults(func=handle_run)

    run_all_parser = subparsers.add_parser("run-all", help="Run the keepalive scheduler for all active profiles.")
    run_all_parser.add_argument("--iterations", type=int)
    run_all_parser.add_argument("--timeout-seconds", type=int)
    run_all_parser.add_argument("--stop-on-error", action="store_true")
    run_all_parser.add_argument("--max-sleep-seconds", type=float, default=60.0)
    run_all_parser.set_defaults(func=handle_run_all)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

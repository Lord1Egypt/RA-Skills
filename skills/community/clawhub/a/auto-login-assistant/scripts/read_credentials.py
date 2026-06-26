#!/usr/bin/env python3
"""Normalize login credentials from a JSON file or environment variables."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ALLOWED_FIELDS = {
    "site",
    "login_url",
    "username",
    "email",
    "phone",
    "password",
    "otp_email",
    "otp_mode",
    "notes",
}


def _load_json_text(raw: str, source: str) -> dict:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{source}: invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"{source}: expected a JSON object")
    return data


def _load_from_file(path: str) -> dict:
    file_path = Path(path).expanduser()
    raw = file_path.read_text(encoding="utf-8")
    return _load_json_text(raw, str(file_path))


def _load_from_env(name: str) -> dict:
    raw = os.environ.get(name)
    if raw is None:
        raise SystemExit(f"environment variable not found: {name}")
    return _load_json_text(raw, f"env:{name}")


def _normalize(data: dict) -> dict:
    normalized = {}
    for key, value in data.items():
        if key not in ALLOWED_FIELDS:
            continue
        if value is None:
            continue
        if isinstance(value, str):
            value = value.strip()
            if not value:
                continue
        normalized[key] = value

    if "otp_mode" not in normalized:
        normalized["otp_mode"] = "manual-first"

    if not any(field in normalized for field in ("email", "username", "phone")):
        raise SystemExit("missing identifier: provide one of email, username, or phone")
    if "password" not in normalized:
        raise SystemExit("missing password")

    return normalized


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Path to a JSON credentials file")
    parser.add_argument("--env", help="Environment variable containing a JSON object")
    args = parser.parse_args()

    if bool(args.file) == bool(args.env):
        raise SystemExit("provide exactly one of --file or --env")

    data = _load_from_file(args.file) if args.file else _load_from_env(args.env)
    normalized = _normalize(data)
    json.dump(normalized, sys.stdout, ensure_ascii=True, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

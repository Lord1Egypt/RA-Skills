#!/usr/bin/env python3
"""Common helpers for Crustacean Email Gateway skill scripts."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any

DEFAULT_API_BASE = "https://api.crustacean.email/api/v1"
DEFAULT_IDENTITY_PATH = "/root/.openclaw/identity/device.json"
DEFAULT_TOKEN_PATH = os.path.expanduser("~/.crustacean-email/token.json")


class SkillError(Exception):
    """Raised for expected skill runtime errors."""


@dataclass
class Identity:
    instance_id: str
    public_key_pem: str
    private_key_pem: str


def add_common_args(parser: argparse.ArgumentParser, require_auth: bool = False) -> None:
    parser.add_argument("--api-base", default=os.environ.get("CRUSTACEAN_API_BASE", DEFAULT_API_BASE))
    parser.add_argument(
        "--identity-path",
        default=os.environ.get("OPENCLAW_IDENTITY_PATH", DEFAULT_IDENTITY_PATH),
    )
    parser.add_argument(
        "--token-path",
        default=os.environ.get("CRUSTACEAN_TOKEN_PATH", DEFAULT_TOKEN_PATH),
    )
    if require_auth:
        parser.add_argument(
            "--token",
            default=None,
            help="Override bearer token. Usually leave empty to use saved token file.",
        )


def parse_json_arg(value: str | None) -> Any:
    if value is None:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise SkillError(f"Invalid JSON value: {exc}") from exc


def ensure_parent_dir(path: str) -> None:
    pathlib.Path(path).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)


def load_json_file(path: str) -> dict[str, Any]:
    resolved = pathlib.Path(path).expanduser().resolve()
    if not resolved.exists():
        raise SkillError(f"File not found: {resolved}")
    try:
        return json.loads(resolved.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SkillError(f"Invalid JSON in {resolved}: {exc}") from exc


def _extract_first_string(data: Any, keys: list[str]) -> str | None:
    if isinstance(data, dict):
        for key in keys:
            value = data.get(key)
            if isinstance(value, str) and value.strip():
                return value
        for value in data.values():
            nested = _extract_first_string(value, keys)
            if nested:
                return nested
    elif isinstance(data, list):
        for item in data:
            nested = _extract_first_string(item, keys)
            if nested:
                return nested
    return None


def load_identity(identity_path: str) -> Identity:
    raw = load_json_file(identity_path)

    instance_id = _extract_first_string(
        raw,
        ["deviceId", "device_id", "instance_id", "agent_id", "id"],
    )

    public_key = _extract_first_string(
        raw,
        ["publicKeyPem", "public_key_pem", "public_key"],
    )

    private_key = _extract_first_string(
        raw,
        ["privateKeyPem", "private_key_pem", "private_key"],
    )

    if not instance_id:
        raise SkillError("Could not find instance_id in identity JSON.")
    if not public_key or "BEGIN PUBLIC KEY" not in public_key:
        raise SkillError("Could not find valid PEM public key in identity JSON.")
    if not private_key or "BEGIN" not in private_key or "PRIVATE KEY" not in private_key:
        raise SkillError("Could not find valid PEM private key in identity JSON.")

    return Identity(instance_id=instance_id, public_key_pem=public_key, private_key_pem=private_key)


def solve_pow(instance_id: str, challenge_nonce: str, difficulty: int) -> str:
    difficulty = max(1, min(int(difficulty), 6))
    target_prefix = "0" * difficulty

    nonce = 0
    while True:
        candidate = str(nonce)
        digest = hashlib.sha256(f"{instance_id}|{challenge_nonce}|{candidate}".encode("utf-8")).hexdigest()
        if digest.startswith(target_prefix):
            return candidate
        nonce += 1


def sign_challenge_message(instance_id: str, challenge_nonce: str, private_key_pem: str) -> str:
    message = f"{instance_id}:{challenge_nonce}".encode("utf-8")

    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as key_file:
        key_file.write(private_key_pem)
        key_path = key_file.name

    try:
        proc = subprocess.run(
            ["openssl", "dgst", "-sha256", "-sign", key_path],
            input=message,
            capture_output=True,
            check=False,
        )
        if proc.returncode != 0:
            stderr = proc.stderr.decode("utf-8", errors="replace").strip()
            raise SkillError(f"OpenSSL signing failed: {stderr or 'unknown error'}")

        return base64.b64encode(proc.stdout).decode("ascii")
    except FileNotFoundError as exc:
        raise SkillError("OpenSSL CLI is required to sign registration requests.") from exc
    finally:
        pathlib.Path(key_path).unlink(missing_ok=True)


def sign_registration_message(instance_id: str, challenge_nonce: str, private_key_pem: str) -> str:
    return sign_challenge_message(instance_id, challenge_nonce, private_key_pem)


def save_token(path: str, payload: dict[str, Any]) -> None:
    ensure_parent_dir(path)
    resolved = pathlib.Path(path).expanduser().resolve()
    resolved.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_token(path: str) -> dict[str, Any]:
    token_data = load_json_file(path)
    if not token_data.get("token"):
        raise SkillError(f"Token file is missing 'token': {path}")
    return token_data


def api_request(
    method: str,
    api_base: str,
    endpoint: str,
    *,
    payload: dict[str, Any] | None = None,
    token: str | None = None,
) -> dict[str, Any]:
    base = api_base.rstrip("/")
    path = endpoint if endpoint.startswith("/") else f"/{endpoint}"
    url = f"{base}{path}"

    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, data=data, method=method.upper(), headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw_body = resp.read().decode("utf-8")
            body = json.loads(raw_body) if raw_body else {}
            return {
                "status": resp.status,
                "ok": 200 <= resp.status < 300,
                "body": body,
            }
    except urllib.error.HTTPError as exc:
        raw_body = exc.read().decode("utf-8", errors="replace")
        try:
            body = json.loads(raw_body) if raw_body else {}
        except json.JSONDecodeError:
            body = {"ok": False, "error": {"code": "http_error", "message": raw_body}}
        return {
            "status": exc.code,
            "ok": False,
            "body": body,
        }
    except urllib.error.URLError as exc:
        raise SkillError(f"Network error calling {url}: {exc}") from exc


def extract_api_error(result: dict[str, Any]) -> str:
    status = result.get("status")
    body = result.get("body", {})
    code = body.get("error", {}).get("code", "unknown_error")
    message = body.get("error", {}).get("message", "Unknown API error")
    return f"HTTP {status} {code}: {message}"


def print_json(data: Any) -> None:
    print(json.dumps(data, indent=2, sort_keys=True))


def print_human_summary(title: str, rows: list[tuple[str, Any]]) -> None:
    print(title)
    for key, value in rows:
        print(f"- {key}: {value}")


def require_token(args: argparse.Namespace) -> tuple[str, dict[str, Any]]:
    if args.token:
        return args.token, {"token": args.token, "source": "cli"}
    try:
        token_data = load_token(args.token_path)
    except SkillError as exc:
        raise SkillError(f"{exc} Register first with register_mailbox.py.") from exc
    return str(token_data["token"]), token_data


def fail(message: str, *, details: dict[str, Any] | None = None) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    if details:
        print_json(details)
    raise SystemExit(1)

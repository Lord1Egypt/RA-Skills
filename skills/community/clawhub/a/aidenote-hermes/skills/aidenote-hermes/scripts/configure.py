#!/usr/bin/env python3
"""Interactively configure AideNote credentials outside the model context."""

from __future__ import annotations

import getpass
import json
import os
from pathlib import Path
import sys
import tempfile
from typing import Any
from urllib import error, parse, request


DEFAULT_API_BASE = "https://api.aidenote.cn"


def emit(value: Any, *, stream: Any = sys.stdout) -> None:
    json.dump(value, stream, ensure_ascii=False, separators=(",", ":"))
    stream.write("\n")


def find_token(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        for key in ("accessToken", "token", "bridgeToken", "tunnelToken"):
            candidate = value.get(key)
            if isinstance(candidate, str) and candidate.strip():
                return candidate.strip()
        for key in ("result", "data", "token"):
            if key in value:
                candidate = find_token(value[key])
                if candidate:
                    return candidate
    if isinstance(value, list):
        for item in value:
            candidate = find_token(item)
            if candidate:
                return candidate
    return ""


def validate_base(raw: str) -> str:
    value = raw.strip().rstrip("/")
    parsed = parse.urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("API base must be an HTTP(S) URL")
    if parsed.username or parsed.password:
        raise ValueError("API base must not contain credentials")
    return value


def verify(api_base: str, api_key: str) -> None:
    endpoint = api_base + "/api/UserapikeyMstr/GetToken/" + parse.quote(api_key, safe="")
    payload = json.dumps({"apiKey": api_key}).encode("utf-8")
    req = request.Request(
        endpoint,
        data=payload,
        method="POST",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-API-Key": api_key,
        },
    )
    try:
        with request.urlopen(req, timeout=15) as response:
            decoded = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        raise ValueError(f"AideNote rejected the API Key (HTTP {exc.code})") from exc
    except (error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        raise ValueError("Could not verify the API Key with AideNote") from exc
    if not find_token(decoded):
        raise ValueError("AideNote verification returned no access token")


def write_credentials(path: Path, api_base: str, api_key: str) -> None:
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if os.name != "nt":
        path.parent.chmod(0o700)
    payload = json.dumps({"apiBase": api_base, "apiKey": api_key}, ensure_ascii=False, indent=2) + "\n"
    descriptor, temporary_name = tempfile.mkstemp(prefix=".aidenote-", dir=path.parent)
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(payload)
        if os.name != "nt":
            temporary_path.chmod(0o600)
        os.replace(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)


def main() -> int:
    hermes_home = Path(os.environ.get("HERMES_HOME", str(Path.home() / ".hermes"))).expanduser()
    credentials_path = hermes_home / "aidenote-credentials.json"
    try:
        api_base = validate_base(input(f"AideNote API base [{DEFAULT_API_BASE}]: ").strip() or DEFAULT_API_BASE)
        api_key = getpass.getpass("AideNote API Key: ").strip()
        if not api_key:
            raise ValueError("API Key is required")
        verify(api_base, api_key)
        write_credentials(credentials_path, api_base, api_key)
        emit({"ok": True, "configured": True, "path": str(credentials_path), "verified": True})
        return 0
    except (EOFError, KeyboardInterrupt):
        emit({"ok": False, "error": "cancelled", "message": "Configuration cancelled"}, stream=sys.stderr)
        return 130
    except ValueError as exc:
        emit({"ok": False, "error": "configuration_failed", "message": str(exc)}, stream=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

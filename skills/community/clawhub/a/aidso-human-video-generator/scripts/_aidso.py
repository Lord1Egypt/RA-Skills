#!/usr/bin/env python3
"""Shared helpers for AIDSO skill scripts."""

from __future__ import annotations

import json
import os
import stat
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Tuple


AUTH_BASE_URL = "https://api.aidso.com"
PROD_BASE_URL = "https://api.aidso.com"
AUTH_LINK_TTL_SECONDS = 600
AUTH_LINK_CLOCK_SAFETY_MS = 1000
PENDING_AUTH_FILENAME = "pending-authorization.json"
DEFAULT_BINDING_RELATIVE_PATH = Path(".aidso") / "credentials.json"
TMP_BINDING_PATH = Path(os.environ.get("TMPDIR", "/tmp")) / "aidso-human-video-generator" / "credentials.json"


class AidsoError(RuntimeError):
    """Raised when an AIDSO operation cannot continue."""


class AuthorizationRequired(AidsoError):
    """Raised when the user must approve a fresh authorization link."""

    def __init__(self, authorization_url: str, expires_in_seconds: int):
        self.authorization_url = authorization_url
        self.expires_in_seconds = expires_in_seconds
        super().__init__(
            "AIDSO account authorization is required. Open this fresh authorization link "
            f"within {expires_in_seconds} seconds:\n{authorization_url}\n"
            "After approval, run this skill's scripts/auth.py with --complete."
        )


@dataclass
class HttpResponse:
    status: int
    data: Dict[str, Any]
    raw: str


def credentials_path() -> Path:
    override = os.environ.get("AIDSO_CREDENTIALS_FILE")
    if override:
        return Path(override).expanduser()
    return Path.cwd() / DEFAULT_BINDING_RELATIVE_PATH


def skill_binding_path() -> Path:
    return Path(__file__).resolve().parents[1] / DEFAULT_BINDING_RELATIVE_PATH


def credential_read_candidates() -> Iterable[Path]:
    override = os.environ.get("AIDSO_CREDENTIALS_FILE")
    if override:
        yield Path(override).expanduser()
        return

    seen = set()
    for path in (
        Path.cwd() / DEFAULT_BINDING_RELATIVE_PATH,
        skill_binding_path(),
        TMP_BINDING_PATH,
    ):
        normalized = str(path)
        if normalized in seen:
            continue
        seen.add(normalized)
        yield path


def read_credentials_file() -> Optional[str]:
    for path in credential_read_candidates():
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text())
        except OSError:
            continue
        except json.JSONDecodeError as exc:
            raise AidsoError(f"Cannot read local binding file {path}: {exc}") from exc
        if not isinstance(data, dict):
            raise AidsoError(f"Local binding file is invalid: {path}")
        api_key = data.get("api_key")
        if isinstance(api_key, str) and api_key.strip():
            return api_key.strip()
    return None


def can_write_binding(path: Path) -> bool:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryFile(dir=path.parent) as probe:
            probe.write(b"ok\n")
        return True
    except OSError:
        return False


def writable_credentials_path() -> Path:
    override = os.environ.get("AIDSO_CREDENTIALS_FILE")
    if override:
        path = Path(override).expanduser()
        if can_write_binding(path):
            return path
        raise AidsoError(f"AIDSO_CREDENTIALS_FILE is not writable: {path}")

    for path in (credentials_path(), skill_binding_path(), TMP_BINDING_PATH):
        if can_write_binding(path):
            return path
    raise AidsoError(
        "No writable local binding path is available. Run from a writable working directory "
        "or set AIDSO_CREDENTIALS_FILE to a writable path."
    )


def write_private_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, prefix="aidso-", delete=False
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            temporary_path.chmod(stat.S_IRUSR | stat.S_IWUSR)
            temporary_file.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        os.replace(temporary_path, path)
    except OSError as exc:
        raise AidsoError(f"Cannot save local authorization state at {path}: {exc}") from exc
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def save_credentials_file(api_key: str, path: Optional[Path] = None) -> Path:
    if not api_key:
        raise AidsoError("Refusing to save an empty API key.")
    path = path or writable_credentials_path()
    payload = {
        "api_key": api_key,
        "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }
    write_private_json(path, payload)
    return path


def pending_authorization_path(credentials_file: Path) -> Path:
    return credentials_file.with_name(PENDING_AUTH_FILENAME)


def save_pending_authorization(payload: Dict[str, Any], path: Path) -> None:
    write_private_json(path, payload)


def read_pending_authorization() -> Optional[Tuple[Dict[str, Any], Path]]:
    for credentials_file in credential_read_candidates():
        path = pending_authorization_path(credentials_file)
        if not path.exists():
            continue
        try:
            payload = json.loads(path.read_text())
        except OSError:
            continue
        except json.JSONDecodeError as exc:
            raise AidsoError(f"Cannot read pending authorization state {path}: {exc}") from exc
        if not isinstance(payload, dict):
            raise AidsoError(f"Pending authorization state is invalid: {path}")
        return payload, path
    return None


def resolve_api_key() -> Optional[str]:
    return read_credentials_file()


def authorization_status(*, now_ms: Optional[int] = None) -> Dict[str, Any]:
    if resolve_api_key():
        return {"status": "bound_locally", "msg": "A local binding exists; server validity was not checked."}
    pending = read_pending_authorization()
    if pending is None:
        return {"status": "not_bound"}
    payload, _ = pending
    remaining_seconds = authorization_remaining_seconds(payload, now_ms=now_ms)
    return {
        "status": "pending" if remaining_seconds > 0 else "expired",
        "expires_in_seconds": remaining_seconds,
    }


def api_base_url(env: Optional[str] = None) -> str:
    selected = (env or "prod").strip().lower()
    if selected in {"prod", "production"}:
        return PROD_BASE_URL
    raise AidsoError("Only the production AIDSO API environment is supported.")


def json_request(
    method: str,
    url: str,
    *,
    api_key: Optional[str] = None,
    payload: Optional[Dict[str, Any]] = None,
    timeout: int = 60,
) -> HttpResponse:
    headers = {"Accept": "application/json"}
    body = None
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    if api_key:
        headers["x-api-key"] = api_key

    request = urllib.request.Request(url, data=body, headers=headers, method=method.upper())
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
            status = response.status
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        status = exc.code
    except urllib.error.URLError as exc:
        raise AidsoError(f"Network request failed: {exc}") from exc

    try:
        data = json.loads(raw) if raw else {}
    except json.JSONDecodeError as exc:
        raise AidsoError(f"Expected JSON response from {url}, got: {raw[:500]}") from exc

    if not isinstance(data, dict):
        raise AidsoError(f"Expected JSON object from {url}, got: {raw[:500]}")
    return HttpResponse(status=status, data=data, raw=raw)


def generate_authorization_url() -> str:
    response = json_request("GET", f"{AUTH_BASE_URL}/openapi/skills/generate_code", timeout=30)
    if response.data.get("code") != 200:
        raise AidsoError(f"Authorization URL request failed: {response.data}")
    url = response.data.get("data")
    if not isinstance(url, str) or not url.startswith("http"):
        raise AidsoError(f"Authorization response did not include a URL: {response.data}")
    return url


def freshen_authorization_url(authorization_url: str, *, now_ms: Optional[int] = None) -> str:
    parsed = urllib.parse.urlparse(authorization_url)
    query_items = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    current_ms = int(time.time() * 1000) if now_ms is None else int(now_ms)
    safe_ms = max(0, current_ms - AUTH_LINK_CLOCK_SAFETY_MS)
    replaced = False
    fresh_items = []
    for key, value in query_items:
        if key == "now":
            fresh_items.append((key, str(safe_ms)))
            replaced = True
        else:
            fresh_items.append((key, value))
    if not replaced:
        fresh_items.append(("now", str(safe_ms)))
    return urllib.parse.urlunparse(parsed._replace(query=urllib.parse.urlencode(fresh_items)))


def extract_code(authorization_url: str) -> str:
    parsed = urllib.parse.urlparse(authorization_url)
    values = urllib.parse.parse_qs(parsed.query)
    code_values = values.get("code")
    if not code_values or not code_values[0]:
        raise AidsoError(f"Authorization URL did not contain a code query parameter: {authorization_url}")
    return code_values[0]


def fetch_api_key_by_code(code: str) -> Optional[str]:
    query = urllib.parse.urlencode({"code": code})
    url = f"{AUTH_BASE_URL}/openapi/skills/get_by_code?{query}"
    response = json_request("GET", url, timeout=30)
    response_code = response.data.get("code")
    if response_code == 300:
        return None
    if response_code != 200:
        raise AidsoError(f"Authorization failed: {response.data}")
    api_key = response.data.get("data")
    if not isinstance(api_key, str) or not api_key:
        raise AidsoError(f"Authorization succeeded but no API key was returned: {response.data}")
    return api_key


def authorization_remaining_seconds(payload: Dict[str, Any], *, now_ms: Optional[int] = None) -> int:
    current_ms = int(time.time() * 1000) if now_ms is None else int(now_ms)
    try:
        expires_at_ms = int(payload["expires_at_ms"])
    except (KeyError, TypeError, ValueError) as exc:
        raise AidsoError("Pending authorization state does not include a valid expiry time.") from exc
    return max(0, (expires_at_ms - current_ms + 999) // 1000)


def public_authorization_state(payload: Dict[str, Any], *, now_ms: Optional[int] = None) -> Dict[str, Any]:
    authorization_url = payload.get("authorization_url")
    if not isinstance(authorization_url, str) or not authorization_url.startswith("http"):
        raise AidsoError("Pending authorization state does not include a valid authorization URL.")
    return {
        "status": "authorization_required",
        "authorization_url": authorization_url,
        "expires_in_seconds": authorization_remaining_seconds(payload, now_ms=now_ms),
        "next_step": "Open the link in a JavaScript-enabled browser, approve access, then run auth.py --complete.",
    }


def start_authorization(*, now_ms: Optional[int] = None) -> Dict[str, Any]:
    credentials_file = writable_credentials_path()
    authorization_url = freshen_authorization_url(generate_authorization_url(), now_ms=now_ms)
    code = extract_code(authorization_url)
    parsed = urllib.parse.urlparse(authorization_url)
    query = urllib.parse.parse_qs(parsed.query)
    try:
        generated_at_ms = int(query["now"][0])
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise AidsoError("Authorization URL did not contain a valid time parameter.") from exc
    payload = {
        "code": code,
        "authorization_url": authorization_url,
        "credential_path": str(credentials_file),
        "expires_at_ms": generated_at_ms + AUTH_LINK_TTL_SECONDS * 1000,
    }
    save_pending_authorization(payload, pending_authorization_path(credentials_file))
    return public_authorization_state(payload, now_ms=now_ms)


def complete_authorization(*, now_ms: Optional[int] = None) -> Dict[str, Any]:
    pending = read_pending_authorization()
    if pending is None:
        raise AidsoError("No pending authorization was found. Run auth.py --start to generate a fresh link.")
    payload, pending_path = pending
    remaining_seconds = authorization_remaining_seconds(payload, now_ms=now_ms)
    if remaining_seconds <= 0:
        raise AidsoError("The authorization link has expired. Run auth.py --start and send the new link immediately.")
    code = payload.get("code")
    if not isinstance(code, str) or not code:
        raise AidsoError("Pending authorization state does not include a valid code.")
    api_key = fetch_api_key_by_code(code)
    if api_key is None:
        result = public_authorization_state(payload, now_ms=now_ms)
        result["status"] = "pending"
        result["msg"] = "Authorization is still waiting for user approval."
        return result

    credential_path_value = payload.get("credential_path")
    if not isinstance(credential_path_value, str) or not credential_path_value:
        raise AidsoError("Pending authorization state does not include a credential destination.")
    save_credentials_file(api_key, Path(credential_path_value))
    try:
        pending_path.unlink()
    except OSError:
        pass
    return {
        "status": "authorized",
        "msg": "AIDSO account authorization completed successfully.",
    }


def ensure_api_key(wait_seconds: int = 300, interval_seconds: int = 3) -> str:
    del wait_seconds, interval_seconds
    existing = resolve_api_key()
    if existing:
        return existing

    pending = read_pending_authorization()
    if pending is not None:
        payload, _ = pending
        if authorization_remaining_seconds(payload) > 0:
            state = public_authorization_state(payload)
            raise AuthorizationRequired(state["authorization_url"], state["expires_in_seconds"])

    state = start_authorization()
    raise AuthorizationRequired(state["authorization_url"], state["expires_in_seconds"])


def print_json(payload: Dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))

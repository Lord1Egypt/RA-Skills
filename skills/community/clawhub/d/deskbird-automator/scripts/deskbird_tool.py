#!/usr/bin/env python3
"""Deskbird API Reverse Engineering Helper.

Dieses Tool hilft dabei, undokumentierte API-Aufrufe aus dem Browser-Verhalten
zu erfassen und anschließend kontrolliert zu replayen.
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import os
import random
import re
import secrets
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

import requests
from dotenv import load_dotenv, set_key

SENSITIVE_HEADER_HINTS = (
    "authorization",
    "cookie",
    "token",
    "secret",
    "csrf",
    "xsrf",
    "session",
)

SENSITIVE_KEY_HINTS = (
    "token",
    "secret",
    "password",
    "passwd",
    "cookie",
    "session",
    "csrf",
    "xsrf",
    "authorization",
    "email",
    "phone",
    "mobile",
)

HEADER_BLACKLIST_FOR_REPLAY = {
    "host",
    "content-length",
    "accept-encoding",
    "connection",
    "sec-fetch-dest",
    "sec-fetch-mode",
    "sec-fetch-site",
    "sec-fetch-user",
    "sec-ch-ua",
    "sec-ch-ua-mobile",
    "sec-ch-ua-platform",
}

_LAST_REQUEST_MONOTONIC = 0.0

PAIRING_STATUS_PENDING = "pending"
PAIRING_STATUS_IN_PROGRESS = "in_progress"
PAIRING_STATUS_COMPLETED = "completed"
PAIRING_STATUS_FAILED = "failed"
PAIRING_STATUS_CANCELLED = "cancelled"
PAIRING_STATUS_EXPIRED = "expired"
PAIRING_TERMINAL_STATUSES = {
    PAIRING_STATUS_COMPLETED,
    PAIRING_STATUS_FAILED,
    PAIRING_STATUS_CANCELLED,
    PAIRING_STATUS_EXPIRED,
}


def now_utc_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def env_int(name: str, default: int, minimum: int | None = None) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        value = default
    else:
        try:
            value = int(raw.strip())
        except Exception:
            value = default
    if minimum is not None:
        value = max(minimum, value)
    return value


def env_float(name: str, default: float, minimum: float | None = None) -> float:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        value = default
    else:
        try:
            value = float(raw.strip())
        except Exception:
            value = default
    if minimum is not None:
        value = max(minimum, value)
    return value


def sha12(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8", errors="ignore")).hexdigest()[:12]


def looks_secret_key(key: str) -> bool:
    key_l = key.lower()
    return any(h in key_l for h in SENSITIVE_KEY_HINTS)


def looks_secret_header(header_name: str) -> bool:
    header_l = header_name.lower()
    return any(h in header_l for h in SENSITIVE_HEADER_HINTS)


def looks_token_like(value: str) -> bool:
    v = value.strip()
    if len(v) < 24:
        return False
    if v.count(".") == 2:
        return True  # JWT-artig
    if re.fullmatch(r"[A-Za-z0-9_\-+/=]{24,}", v):
        return True
    return False


def looks_email_like(value: str) -> bool:
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value.strip()))


def redact_value(value: str) -> str:
    if value == "":
        return value
    return f"<redacted:{sha12(value)}>"


def sanitize_headers(headers: dict[str, str], keep_secrets: bool) -> dict[str, str]:
    out: dict[str, str] = {}
    for key, value in headers.items():
        if not keep_secrets and looks_secret_header(key):
            out[key] = redact_value(value)
        elif not keep_secrets and looks_token_like(value):
            out[key] = redact_value(value)
        elif not keep_secrets and looks_email_like(value):
            out[key] = redact_value(value)
        else:
            out[key] = value
    return out


def sanitize_obj(obj: Any, keep_secrets: bool) -> Any:
    if keep_secrets:
        return obj

    if isinstance(obj, dict):
        out: dict[str, Any] = {}
        for key, value in obj.items():
            if looks_secret_key(str(key)):
                out[key] = redact_value(str(value))
            else:
                out[key] = sanitize_obj(value, keep_secrets=False)
        return out

    if isinstance(obj, list):
        return [sanitize_obj(item, keep_secrets=False) for item in obj]

    if isinstance(obj, str):
        if looks_token_like(obj):
            return redact_value(obj)
        if looks_email_like(obj):
            return redact_value(obj)
        return obj

    return obj


def parse_json_maybe(raw: str) -> Any | None:
    try:
        return json.loads(raw)
    except Exception:
        return None


def _throttle_before_request() -> None:
    global _LAST_REQUEST_MONOTONIC

    safe_mode = env_bool("DESKBIRD_SAFE_MODE", True)
    if not safe_mode:
        return

    min_interval_ms = env_int("DESKBIRD_MIN_REQUEST_INTERVAL_MS", 900, minimum=0)
    jitter_ms = env_int("DESKBIRD_INTERVAL_JITTER_MS", 250, minimum=0)
    now = time.monotonic()
    elapsed = now - _LAST_REQUEST_MONOTONIC
    min_interval = min_interval_ms / 1000.0

    # Gentle pacing reduces the risk of triggering anti-abuse rules.
    wait_for = max(0.0, min_interval - elapsed)
    if wait_for > 0:
        time.sleep(wait_for)

    if jitter_ms > 0:
        time.sleep(random.uniform(0, jitter_ms / 1000.0))


def _backoff_seconds(response: requests.Response, attempt_index: int) -> float:
    retry_after = response.headers.get("retry-after", "").strip()
    if retry_after.isdigit():
        return float(retry_after)

    base = env_float("DESKBIRD_RETRY_BASE_SECONDS", 3.0, minimum=0.0)
    cap = env_float("DESKBIRD_RETRY_MAX_SECONDS", 30.0, minimum=1.0)
    jitter = random.uniform(0.0, min(1.5, base))
    value = min(cap, (base * (2 ** attempt_index)) + jitter)
    return max(0.5, value)


def safe_request(method: str, url: str, **kwargs: Any) -> requests.Response:
    max_retries = env_int("DESKBIRD_MAX_RETRIES", 1, minimum=0)
    retry_statuses = {429, 500, 502, 503, 504}

    attempt = 0
    while True:
        _throttle_before_request()
        response = requests.request(method=method, url=url, **kwargs)

        global _LAST_REQUEST_MONOTONIC
        _LAST_REQUEST_MONOTONIC = time.monotonic()

        if response.status_code not in retry_statuses:
            return response
        if attempt >= max_retries:
            return response

        sleep_for = _backoff_seconds(response, attempt)
        time.sleep(sleep_for)
        attempt += 1


def sanitize_body(raw: str | None, keep_secrets: bool, max_len: int) -> Any:
    if raw is None:
        return None

    parsed = parse_json_maybe(raw)
    if parsed is not None:
        return sanitize_obj(parsed, keep_secrets=keep_secrets)

    text = raw
    if not keep_secrets and looks_token_like(text):
        text = redact_value(text)
    if len(text) > max_len:
        return text[:max_len] + f"... <truncated:{len(text) - max_len} chars>"
    return text


def build_auth_headers_from_env() -> dict[str, str]:
    headers: dict[str, str] = {}

    auth = os.getenv("DESKBIRD_AUTHORIZATION", "").strip()
    cookie = os.getenv("DESKBIRD_COOKIE", "").strip()
    csrf = os.getenv("DESKBIRD_X_CSRF_TOKEN", "").strip()
    xsrf = os.getenv("DESKBIRD_X_XSRF_TOKEN", "").strip()

    if auth:
        headers["Authorization"] = auth
    if cookie:
        headers["Cookie"] = cookie
    if csrf:
        headers["X-CSRF-Token"] = csrf
    if xsrf:
        headers["X-XSRF-Token"] = xsrf

    extra_json = os.getenv("DESKBIRD_EXTRA_HEADERS_JSON", "").strip()
    if extra_json:
        try:
            extra = json.loads(extra_json)
            if isinstance(extra, dict):
                for key, value in extra.items():
                    headers[str(key)] = str(value)
        except json.JSONDecodeError:
            print("Warnung: DESKBIRD_EXTRA_HEADERS_JSON ist kein valides JSON und wird ignoriert.")

    return headers


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, data: Any) -> None:
    ensure_parent(path)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True), encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_key_value_pairs(items: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"Ungueltiges Format '{item}'. Erwartet: key=value")
        key, value = item.split("=", 1)
        out[key] = value
    return out


def strip_wrapping_quotes(value: str) -> str:
    text = str(value or "").strip()
    if len(text) >= 2 and ((text[0] == text[-1] == '"') or (text[0] == text[-1] == "'")):
        return text[1:-1].strip()
    return text


def normalize_authorization_value(value: str) -> str:
    v = strip_wrapping_quotes(value)
    if not v:
        return ""

    # Allow callers to pass full header/env lines by accident.
    if ":" in v:
        left, right = v.split(":", 1)
        if left.strip().lower() in {"authorization", "deskbird_authorization"}:
            v = strip_wrapping_quotes(right)
    if "=" in v:
        left, right = v.split("=", 1)
        if left.strip().lower() in {"authorization", "deskbird_authorization"}:
            v = strip_wrapping_quotes(right)

    if v.lower().startswith("bearer "):
        token = strip_wrapping_quotes(v[7:].strip())
        if token:
            return f"Bearer {token}"
        return "Bearer"
    if looks_token_like(v):
        return f"Bearer {v}"
    return v


def parse_auth_values_from_text(raw_text: str) -> dict[str, str]:
    text = str(raw_text or "")
    out: dict[str, str] = {}

    parsed = parse_json_maybe(text)
    if isinstance(parsed, dict):
        for key, value in parsed.items():
            key_l = str(key).strip().lower()
            val = strip_wrapping_quotes(str(value))
            if not val:
                continue
            if key_l in {"deskbird_authorization", "authorization", "auth", "access_token", "accesstoken", "token", "id_token", "idtoken"}:
                out["DESKBIRD_AUTHORIZATION"] = normalize_authorization_value(val)
            elif key_l in {"deskbird_cookie", "cookie"}:
                out["DESKBIRD_COOKIE"] = val
            elif key_l in {"deskbird_x_csrf_token", "x-csrf-token", "csrf", "csrf_token"}:
                out["DESKBIRD_X_CSRF_TOKEN"] = val
            elif key_l in {"deskbird_x_xsrf_token", "x-xsrf-token", "xsrf", "xsrf_token"}:
                out["DESKBIRD_X_XSRF_TOKEN"] = val
            elif key_l in {"deskbird_base_url", "base_url", "baseurl"}:
                out["DESKBIRD_BASE_URL"] = val.rstrip("/")
            elif key_l in {"deskbird_firebase_api_key", "firebase_api_key", "firebaseapikey", "google_api_key"}:
                out["DESKBIRD_FIREBASE_API_KEY"] = val
            elif key_l in {"deskbird_firebase_refresh_token", "firebase_refresh_token", "firebaserefreshtoken"}:
                out["DESKBIRD_FIREBASE_REFRESH_TOKEN"] = val
            elif key_l == "refreshtoken":
                out["DESKBIRD_FIREBASE_REFRESH_TOKEN"] = val

    for line in text.replace("\r\n", "\n").split("\n"):
        s = strip_wrapping_quotes(line)
        if not s:
            continue

        # Preserve full cookie values, they can contain '=' characters.
        if ":" in s:
            left, right = s.split(":", 1)
            k = left.strip().lower()
            v = strip_wrapping_quotes(right)
            if k == "authorization" and v:
                out["DESKBIRD_AUTHORIZATION"] = normalize_authorization_value(v)
                continue
            if k == "cookie" and v:
                out["DESKBIRD_COOKIE"] = v
                continue
            if k == "x-csrf-token" and v:
                out["DESKBIRD_X_CSRF_TOKEN"] = v
                continue
            if k == "x-xsrf-token" and v:
                out["DESKBIRD_X_XSRF_TOKEN"] = v
                continue
            if k in {"x-firebase-api-key", "firebase-api-key"} and v:
                out["DESKBIRD_FIREBASE_API_KEY"] = v
                continue

        if "=" in s:
            left, right = s.split("=", 1)
            k = left.strip().lower()
            v = strip_wrapping_quotes(right)
            if k in {"authorization", "deskbird_authorization"} and v:
                out["DESKBIRD_AUTHORIZATION"] = normalize_authorization_value(v)
                continue
            if k in {"cookie", "deskbird_cookie"} and v:
                out["DESKBIRD_COOKIE"] = v
                continue
            if k in {"x-csrf-token", "deskbird_x_csrf_token"} and v:
                out["DESKBIRD_X_CSRF_TOKEN"] = v
                continue
            if k in {"x-xsrf-token", "deskbird_x_xsrf_token"} and v:
                out["DESKBIRD_X_XSRF_TOKEN"] = v
                continue
            if k in {"deskbird_base_url", "base_url", "baseurl"} and v:
                out["DESKBIRD_BASE_URL"] = v.rstrip("/")
                continue
            if k in {"deskbird_firebase_api_key", "firebase_api_key", "firebaseapikey", "google_api_key"} and v:
                out["DESKBIRD_FIREBASE_API_KEY"] = v
                continue
            if k in {"deskbird_firebase_refresh_token", "firebase_refresh_token", "firebaserefreshtoken", "refresh_token", "refreshtoken"} and v:
                out["DESKBIRD_FIREBASE_REFRESH_TOKEN"] = v
                continue

        if s.lower().startswith("bearer "):
            out["DESKBIRD_AUTHORIZATION"] = normalize_authorization_value(s)
            continue

        # Allow raw JWT paste
        if looks_token_like(s):
            out["DESKBIRD_AUTHORIZATION"] = normalize_authorization_value(s)

    return {k: v for k, v in out.items() if isinstance(v, str) and v.strip()}


def now_utc_dt() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def parse_utc_iso_maybe(value: Any) -> dt.datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = dt.datetime.fromisoformat(text)
    except Exception:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def normalize_pairing_code(raw_code: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9]", "", str(raw_code or "")).upper().strip()
    if not normalized:
        raise ValueError("Ungueltiger Pairing-Code.")
    return normalized


def generate_pairing_code(length: int = 6) -> str:
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return "".join(secrets.choice(alphabet) for _ in range(max(4, int(length))))


def get_auth_pair_store_path(store_file: str | None) -> Path:
    raw = (store_file or "").strip()
    if raw:
        return Path(raw)
    env_value = os.getenv("DESKBIRD_AUTH_PAIR_STORE", "").strip()
    if env_value:
        return Path(env_value)
    return Path("output/auth_pairings.json")


def load_auth_pair_store(store_path: Path) -> dict[str, Any]:
    if not store_path.exists():
        return {"version": 1, "sessions": {}}
    data = read_json(store_path)
    if not isinstance(data, dict):
        raise ValueError(f"Pairing-Store {store_path} hat ungueltiges Format.")
    sessions = data.get("sessions")
    if not isinstance(sessions, dict):
        data["sessions"] = {}
    return data


def save_auth_pair_store(store_path: Path, state: dict[str, Any]) -> None:
    write_json(store_path, state)


def expire_pairing_sessions(state: dict[str, Any], now_utc: dt.datetime) -> bool:
    sessions = state.get("sessions")
    if not isinstance(sessions, dict):
        return False

    changed = False
    for _, session in sessions.items():
        if not isinstance(session, dict):
            continue
        status = str(session.get("status", ""))
        if status not in {PAIRING_STATUS_PENDING, PAIRING_STATUS_IN_PROGRESS}:
            continue
        expires_at = parse_utc_iso_maybe(session.get("expires_at_utc"))
        if expires_at is not None and expires_at <= now_utc:
            session["status"] = PAIRING_STATUS_EXPIRED
            session["finished_at_utc"] = now_utc.isoformat()
            changed = True
    return changed


def cleanup_pairing_sessions(state: dict[str, Any], now_utc: dt.datetime, keep_days: int = 7) -> bool:
    sessions = state.get("sessions")
    if not isinstance(sessions, dict):
        return False

    threshold = now_utc - dt.timedelta(days=max(1, keep_days))
    remove_keys: list[str] = []
    for code, session in sessions.items():
        if not isinstance(session, dict):
            remove_keys.append(str(code))
            continue
        status = str(session.get("status", ""))
        if status not in PAIRING_TERMINAL_STATUSES:
            continue
        finished = parse_utc_iso_maybe(session.get("finished_at_utc")) or parse_utc_iso_maybe(session.get("created_at_utc"))
        if finished is not None and finished < threshold:
            remove_keys.append(str(code))

    if not remove_keys:
        return False
    for key in remove_keys:
        sessions.pop(key, None)
    return True


def make_pair_finish_command(code: str) -> str:
    if Path("scripts/deskbird_tool.py").exists():
        tool_ref = "scripts/deskbird_tool.py"
    elif Path("deskbird_tool.py").exists():
        tool_ref = "deskbird_tool.py"
    else:
        tool_ref = Path(sys.argv[0]).name
    python_ref = ".venv/bin/python" if Path(".venv/bin/python").exists() else "python"
    return f"{python_ref} {tool_ref} auth-pair-finish --code {code}"


def pairing_status_exit_code(status: str) -> int:
    if status == PAIRING_STATUS_COMPLETED:
        return 0
    if status in {PAIRING_STATUS_PENDING, PAIRING_STATUS_IN_PROGRESS}:
        return 11
    return 12


def build_pairing_view(code: str, session: dict[str, Any]) -> dict[str, Any]:
    out = dict(session)
    out["code"] = code
    out["status_exit_code"] = pairing_status_exit_code(str(session.get("status", "")))
    out["finish_command"] = make_pair_finish_command(code)
    out["deskbird_code_entry_required"] = False
    out["deskbird_login_instruction"] = (
        "In deskbird keinen Code eingeben. Einfach normal per SSO einloggen."
    )
    out["pairing_code_usage"] = (
        "Der Pairing-Code wird nur fuer auth-pair-status/cancel im Tool verwendet."
    )
    return out


def print_pairing_table(view: dict[str, Any]) -> None:
    print(f"Pairing-Code: {view.get('code')}")
    print(f"Status: {view.get('status')}")
    print(f"Ablauf (UTC): {view.get('expires_at_utc')}")
    print(f"Deskbird-Code-Eingabe noetig: {'ja' if view.get('deskbird_code_entry_required') else 'nein'}")
    login_instruction = str(view.get("deskbird_login_instruction", "")).strip()
    if login_instruction:
        print(f"Deskbird-Login: {login_instruction}")
    print(f"Finish-Command: {view.get('finish_command')}")
    error_code = str(view.get("error_code", "")).strip()
    if error_code:
        print(f"Fehlercode: {error_code}")


def get_base_url() -> str:
    return os.getenv("DESKBIRD_BASE_URL", "https://api.deskbird.com").rstrip("/")


def require_auth_headers(auth_headers: dict[str, str]) -> None:
    if "Authorization" in auth_headers:
        return
    if "Cookie" in auth_headers:
        return
    raise ValueError("Keine Auth-Header gefunden. Bitte DESKBIRD_AUTHORIZATION oder DESKBIRD_COOKIE in .env setzen.")


def upsert_env_file(env_file: str, values: dict[str, str]) -> None:
    env_path = Path(env_file)
    ensure_parent(env_path)
    if not env_path.exists():
        env_path.write_text("", encoding="utf-8")

    for key, value in values.items():
        if not value:
            continue
        set_key(str(env_path), key, value, quote_mode="always")


def host_matches_domain(url: str, domain: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    wanted = domain.strip().lower()
    return bool(host and wanted and (host == wanted or host.endswith(f".{wanted}")))


def decode_jwt_payload_from_authorization(auth_header: str) -> dict[str, Any] | None:
    if not auth_header:
        return None
    parts = auth_header.strip().split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None

    token = parts[1]
    segments = token.split(".")
    if len(segments) < 2:
        return None

    payload_b64 = segments[1]
    payload_b64 += "=" * ((4 - len(payload_b64) % 4) % 4)
    try:
        raw = base64.urlsafe_b64decode(payload_b64.encode("ascii"))
        payload = json.loads(raw.decode("utf-8"))
        if isinstance(payload, dict):
            return payload
    except Exception:
        return None
    return None


def extract_auth_expiry(auth_header: str) -> dt.datetime | None:
    payload = decode_jwt_payload_from_authorization(auth_header)
    if not payload:
        return None
    exp = payload.get("exp")
    if not isinstance(exp, (int, float)):
        return None
    return dt.datetime.fromtimestamp(float(exp), tz=dt.timezone.utc)


def build_auth_check_report(
    auth_headers: dict[str, str],
    response: requests.Response,
    payload: Any,
    min_valid_minutes: int,
) -> dict[str, Any]:
    now_utc = dt.datetime.now(dt.timezone.utc)
    body = unwrap_data(payload)

    user: dict[str, Any] | None = None
    if isinstance(body, dict):
        first_name = str(body.get("firstName", "")).strip()
        last_name = str(body.get("lastName", "")).strip()
        user_id = body.get("id")
        display_name = (first_name + " " + last_name).strip()
        if display_name or user_id is not None or first_name or last_name:
            user = {
                "id": user_id,
                "first_name": first_name or None,
                "last_name": last_name or None,
                "display_name": display_name or None,
            }

    auth_header = auth_headers.get("Authorization", "")
    expiry_utc = extract_auth_expiry(auth_header)
    remaining_seconds: int | None = None
    remaining_minutes: int | None = None
    if expiry_utc is not None:
        remaining_seconds = int((expiry_utc - now_utc).total_seconds())
        remaining_minutes = int(remaining_seconds // 60)

    has_bearer = "Authorization" in auth_headers
    has_cookie = "Cookie" in auth_headers

    ok = response.status_code < 400
    reason_code = "ok"
    requires_reauth = False
    meets_min_validity: bool | None = None

    if not ok:
        reason_code = "auth_rejected"
        requires_reauth = True
    elif expiry_utc is not None:
        if (remaining_seconds or 0) <= 0:
            reason_code = "token_expired"
            requires_reauth = True
            meets_min_validity = False
        elif min_valid_minutes > 0:
            meets_min_validity = (remaining_minutes or 0) >= min_valid_minutes
            if not meets_min_validity:
                reason_code = "token_below_min_validity"
                requires_reauth = True
        else:
            meets_min_validity = True

    error_excerpt: str | None = None
    if not ok:
        text = (response.text or "").strip()
        if text:
            max_chars = 800
            if len(text) > max_chars:
                text = text[:max_chars] + f"... <truncated:{len(text) - max_chars} chars>"
            error_excerpt = text

    return {
        "checked_at_utc": now_utc.isoformat(),
        "http_status": response.status_code,
        "ok": ok,
        "requires_reauth": requires_reauth,
        "reason_code": reason_code,
        "min_valid_minutes": min_valid_minutes,
        "meets_min_validity": meets_min_validity,
        "has_bearer": has_bearer,
        "has_cookie": has_cookie,
        "cookie_rotated": bool(response.headers.get("set-cookie")),
        "bearer_exp_utc": expiry_utc.isoformat() if expiry_utc is not None else None,
        "bearer_remaining_minutes": remaining_minutes,
        "user": user,
        "error_excerpt": error_excerpt,
    }


def print_auth_check_report(report: dict[str, Any]) -> None:
    http_status = int(report.get("http_status", 0))
    if not report.get("ok"):
        print(f"Auth-Check fehlgeschlagen (HTTP {http_status}).")
        error_excerpt = str(report.get("error_excerpt", "") or "").strip()
        if error_excerpt:
            print(f"Antwort (gekuerzt): {error_excerpt}")
        return

    print(f"Auth-Check OK (HTTP {http_status})")

    user = report.get("user")
    if isinstance(user, dict):
        display_name = str(user.get("display_name") or "").strip()
        user_id = user.get("id")
        if display_name:
            print(f"User: {display_name} (id={user_id})")
        elif user_id is not None:
            print(f"User id: {user_id}")

    bearer_exp_utc = str(report.get("bearer_exp_utc") or "").strip()
    if bearer_exp_utc:
        print(f"Bearer-Token exp UTC: {bearer_exp_utc}")
        remaining_minutes = report.get("bearer_remaining_minutes")
        if isinstance(remaining_minutes, int):
            if remaining_minutes <= 0:
                print("Token ist bereits abgelaufen. Bitte auth-capture erneut ausfuehren.")
            else:
                print(f"Restgueltigkeit (ca.): {remaining_minutes} Minuten")
    elif report.get("has_bearer"):
        print("Bearer-Token vorhanden, aber keine decodierbare exp-Claim gefunden.")
    elif report.get("has_cookie"):
        print("Cookie-Session aktiv. Exakte Ablaufzeit ist ohne Serverdetails nicht direkt ableitbar.")

    min_valid_minutes = int(report.get("min_valid_minutes") or 0)
    if min_valid_minutes > 0 and report.get("meets_min_validity") is False:
        print(f"Restgueltigkeit liegt unter dem Mindestwert ({min_valid_minutes} Minuten). Reauth empfohlen.")

    if report.get("cookie_rotated"):
        print("Server setzt bei Check neue Cookies. Session kann serverseitig rollieren.")


def parse_local_range_to_epoch_ms(date_str: str, start_local: str, end_local: str, timezone_name: str) -> tuple[int, int, str, str]:
    try:
        zone = ZoneInfo(timezone_name)
    except Exception as exc:
        raise ValueError(f"Unbekannte Zeitzone '{timezone_name}'") from exc

    try:
        start_naive = dt.datetime.fromisoformat(f"{date_str}T{start_local}")
        end_naive = dt.datetime.fromisoformat(f"{date_str}T{end_local}")
    except Exception as exc:
        raise ValueError("Datum/Uhrzeit ungueltig. Erwartet: --date YYYY-MM-DD --start-local HH:MM --end-local HH:MM") from exc

    start = start_naive.replace(tzinfo=zone)
    end = end_naive.replace(tzinfo=zone)
    if end <= start:
        raise ValueError("Endzeit muss nach Startzeit liegen.")

    return int(start.timestamp() * 1000), int(end.timestamp() * 1000), start.isoformat(), end.isoformat()


def unwrap_data(payload: Any) -> Any:
    if isinstance(payload, dict) and "data" in payload and isinstance(payload["data"], (dict, list)):
        return payload["data"]
    return payload


def request_json(
    method: str,
    url: str,
    headers: dict[str, str],
    timeout: int,
    params: list[tuple[str, str]] | dict[str, str] | None = None,
    json_body: Any = None,
) -> tuple[requests.Response, Any]:
    kwargs: dict[str, Any] = {
        "headers": headers,
        "timeout": timeout,
    }
    if params is not None:
        kwargs["params"] = params
    if json_body is not None:
        kwargs["json"] = json_body

    response = safe_request(method.upper(), url, **kwargs)
    payload: Any = None
    ctype = response.headers.get("content-type", "").lower()
    if "application/json" in ctype:
        try:
            payload = response.json()
        except Exception:
            payload = None
    return response, payload


def extract_company_id_from_auth_headers(auth_headers: dict[str, str]) -> str:
    auth_header = auth_headers.get("Authorization", "")
    payload = decode_jwt_payload_from_authorization(auth_header)
    if not isinstance(payload, dict):
        return ""

    for key in ("companyId", "businessCompanyId"):
        candidate = payload.get(key)
        if candidate is None:
            continue
        value = str(candidate).strip()
        if value:
            return value
    return ""


def normalize_workspace_entry(raw: dict[str, Any]) -> dict[str, Any]:
    address = raw.get("address", {}) if isinstance(raw.get("address"), dict) else {}
    office_id = str(raw.get("id") or raw.get("workspaceId") or "").strip()
    office_name = str(raw.get("name") or raw.get("displayName") or office_id or "unknown-office").strip()
    return {
        "id": office_id,
        "name": office_name,
        "uuid": str(raw.get("uuid") or raw.get("officeUuid") or "").strip() or None,
        "company_id": str(raw.get("businessCompanyId") or raw.get("companyId") or "").strip() or None,
        "is_active": bool(raw.get("isActive", True)),
        "timezone": str(address.get("timeZone") or "").strip() or None,
        "city": str(address.get("city") or "").strip() or None,
        "country": str(address.get("country") or "").strip() or None,
    }


def get_internal_workspaces(company_id: str, headers: dict[str, str], timeout: int, include_inactive: bool = True) -> list[dict[str, Any]]:
    cid = str(company_id or "").strip()
    if not cid:
        raise ValueError("Keine companyId verfuegbar fuer Workspace-Discovery.")

    url = f"{get_base_url()}/v1.1/company/internalWorkspaces"
    params: list[tuple[str, str]] = [("companyId", cid)]
    if include_inactive:
        params.append(("includeInactive", "true"))

    response, payload = request_json("GET", url, headers=headers, timeout=timeout, params=params)
    if response.status_code >= 400:
        print("Fehler bei Office-Discovery (internalWorkspaces).")
        print_response_summary(response, max_chars=3000)
        raise ValueError(f"Office-Discovery fehlgeschlagen ({response.status_code})")

    body = unwrap_data(payload)
    rows: list[Any]
    if isinstance(body, dict) and isinstance(body.get("results"), list):
        rows = body.get("results", [])
    elif isinstance(body, list):
        rows = body
    else:
        raise ValueError("Unerwartete API-Antwort bei Office-Discovery.")

    offices: list[dict[str, Any]] = []
    for row in rows:
        if isinstance(row, dict):
            office = normalize_workspace_entry(row)
            if office.get("id"):
                offices.append(office)
    return offices


def find_office_by_name(offices: list[dict[str, Any]], wanted_name: str) -> dict[str, Any] | None:
    wanted = str(wanted_name or "").strip().lower()
    if not wanted:
        return None

    exact = [o for o in offices if str(o.get("name", "")).strip().lower() == wanted]
    if exact:
        return exact[0]

    partial = [o for o in offices if wanted in str(o.get("name", "")).lower()]
    if partial:
        return partial[0]
    return None


def resolve_office(
    office_id: str | None,
    office_name: str | None,
    headers: dict[str, str],
    timeout: int,
) -> tuple[str, dict[str, Any]]:
    explicit_office_id = str(office_id or "").strip()
    explicit_office_name = str(office_name or "").strip()

    if explicit_office_id:
        return explicit_office_id, {
            "office_id": explicit_office_id,
            "office_name": None,
            "selection_reason": "explicit_office_id",
            "auto_selected": False,
            "offices_total": None,
            "offices_active_total": None,
            "company_id": None,
        }

    company_id = os.getenv("DESKBIRD_COMPANY_ID", "").strip() or extract_company_id_from_auth_headers(headers)
    if not company_id:
        raise ValueError(
            "Office-ID fehlt und companyId konnte nicht ermittelt werden. "
            "Bitte --office-id setzen oder DESKBIRD_COMPANY_ID konfigurieren."
        )

    offices = get_internal_workspaces(company_id, headers=headers, timeout=timeout, include_inactive=True)
    if not offices:
        raise ValueError("Keine Offices fuer den aktuellen Account gefunden.")

    active_offices = [o for o in offices if bool(o.get("is_active", True))]
    default_office_id = os.getenv("DESKBIRD_DEFAULT_OFFICE_ID", "").strip()
    default_office_name = os.getenv("DESKBIRD_DEFAULT_OFFICE_NAME", "").strip()

    selected: dict[str, Any] | None = None
    reason = ""

    if explicit_office_name:
        selected = find_office_by_name(active_offices, explicit_office_name) or find_office_by_name(offices, explicit_office_name)
        if selected is None:
            available_names = ", ".join(sorted({str(o.get("name", "")).strip() for o in active_offices or offices if str(o.get("name", "")).strip()}))
            raise ValueError(
                f"Office mit Name '{explicit_office_name}' nicht gefunden. "
                f"Verfuegbare Offices: {available_names or '<none>'}"
            )
        reason = "explicit_office_name"
    elif default_office_id:
        selected = next((o for o in active_offices if str(o.get("id")) == default_office_id), None)
        if selected is None:
            selected = next((o for o in offices if str(o.get("id")) == default_office_id), None)
        if selected is not None:
            reason = "env_default_office_id"
    elif default_office_name:
        selected = find_office_by_name(active_offices, default_office_name) or find_office_by_name(offices, default_office_name)
        if selected is not None:
            reason = "env_default_office_name"

    if selected is None and len(active_offices) == 1:
        selected = active_offices[0]
        reason = "single_active_office"
    if selected is None and len(offices) == 1:
        selected = offices[0]
        reason = "single_office"
    if selected is None:
        base = active_offices if active_offices else offices
        selected = sorted(
            base,
            key=lambda o: (str(o.get("name", "")).strip().lower(), str(o.get("id", "")).strip()),
        )[0]
        reason = "multiple_offices_fallback_first"

    selected_id = str(selected.get("id", "")).strip()
    if not selected_id:
        raise ValueError("Auto-Office-Aufloesung lieferte keine gueltige Office-ID.")

    return selected_id, {
        "office_id": selected_id,
        "office_name": selected.get("name"),
        "office_uuid": selected.get("uuid"),
        "office_timezone": selected.get("timezone"),
        "office_city": selected.get("city"),
        "office_country": selected.get("country"),
        "selection_reason": reason,
        "auto_selected": reason not in {"explicit_office_id", "explicit_office_name"},
        "offices_total": len(offices),
        "offices_active_total": len(active_offices),
        "company_id": company_id,
    }


def find_zone_by_id(zones: list[dict[str, Any]], zone_id: str) -> dict[str, Any]:
    for zone in zones:
        if str(zone.get("id")) == str(zone_id):
            return zone
    raise ValueError(f"Zone '{zone_id}' nicht gefunden.")


def get_workspace_zones(office_id: str, start_ms: int, end_ms: int, headers: dict[str, str], timeout: int) -> list[dict[str, Any]]:
    url = f"{get_base_url()}/v1.2/internalWorkspaces/{office_id}/zones"
    params = [("internal", ""), ("startTime", str(start_ms)), ("endTime", str(end_ms))]
    response, payload = request_json("GET", url, headers=headers, timeout=timeout, params=params)
    if response.status_code >= 400:
        print("Fehler bei Zone-Abfrage.")
        print_response_summary(response, max_chars=3000)
        raise ValueError(f"Zone-Abfrage fehlgeschlagen ({response.status_code})")

    body = unwrap_data(payload)
    if isinstance(body, dict) and isinstance(body.get("results"), list):
        zones = body["results"]
    elif isinstance(body, list):
        zones = body
    else:
        raise ValueError("Unerwartete API-Antwort bei Zone-Abfrage.")

    return [zone for zone in zones if isinstance(zone, dict)]


def get_parking_zones(office_id: str, start_ms: int, end_ms: int, headers: dict[str, str], timeout: int) -> list[dict[str, Any]]:
    zones = get_workspace_zones(office_id, start_ms, end_ms, headers=headers, timeout=timeout)
    return [zone for zone in zones if zone.get("type") == "parking"]


def get_zone_details(office_id: str, zone_id: str, start_ms: int, end_ms: int, headers: dict[str, str], timeout: int) -> dict[str, Any]:
    url = f"{get_base_url()}/v1.2/internalWorkspaces/{office_id}/zones/{zone_id}"
    params = [("internal", ""), ("startTime", str(start_ms)), ("endTime", str(end_ms))]
    response, payload = request_json("GET", url, headers=headers, timeout=timeout, params=params)
    if response.status_code >= 400:
        print("Fehler bei Detail-Abfrage der Zone.")
        print_response_summary(response, max_chars=3000)
        raise ValueError(f"Zone-Detail-Abfrage fehlgeschlagen ({response.status_code})")

    body = unwrap_data(payload)
    if not isinstance(body, dict):
        raise ValueError("Unerwartete API-Antwort bei Zone-Details.")
    return body


def get_available_zone_items(zone_details: dict[str, Any]) -> list[dict[str, Any]]:
    availability = zone_details.get("availability", {})
    items = availability.get("zoneItems", [])
    if not isinstance(items, list):
        return []
    out: list[dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        if item.get("isAvailable") is True:
            out.append(item)
    return out


def parse_iso_utc_maybe(value: str | None) -> dt.datetime | None:
    if not value or not isinstance(value, str):
        return None
    normalized = value.replace("Z", "+00:00")
    try:
        return dt.datetime.fromisoformat(normalized)
    except Exception:
        return None


def resolve_zone(
    parking_zones: list[dict[str, Any]],
    zone_id: str | None,
    zone_name: str | None,
) -> dict[str, Any]:
    if zone_id:
        return find_zone_by_id(parking_zones, zone_id)

    if zone_name:
        wanted = zone_name.strip().lower()
        exact_matches = [z for z in parking_zones if str(z.get("name", "")).strip().lower() == wanted]
        if exact_matches:
            return exact_matches[0]
        partial_matches = [z for z in parking_zones if wanted in str(z.get("name", "")).lower()]
        if partial_matches:
            return partial_matches[0]
        raise ValueError(f"Parking-Zone mit Name '{zone_name}' nicht gefunden.")

    if not parking_zones:
        raise ValueError("Keine Parking-Zonen gefunden.")
    return parking_zones[0]


def build_parking_spot_statuses(
    zone_details: dict[str, Any],
    end_ms: int,
    include_emails: bool,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    zone_name = str(zone_details.get("name", ""))
    zone_id = str(zone_details.get("id", ""))
    zone_access = zone_details.get("accessRules", {}) if isinstance(zone_details.get("accessRules"), dict) else {}
    zone_is_bookable = bool(zone_access.get("isBookable", True))
    zone_user_has_access = bool(zone_access.get("userHasAccess", True))

    resources_bookable_until_dt = parse_iso_utc_maybe(zone_details.get("resourcesBookableUntil"))
    if resources_bookable_until_dt is not None and resources_bookable_until_dt.tzinfo is None:
        resources_bookable_until_dt = resources_bookable_until_dt.replace(tzinfo=dt.timezone.utc)
    resources_bookable_until_ms = int(resources_bookable_until_dt.timestamp() * 1000) if resources_bookable_until_dt else None

    availability = zone_details.get("availability", {}) if isinstance(zone_details.get("availability"), dict) else {}
    zone_items = availability.get("zoneItems", [])
    if not isinstance(zone_items, list):
        zone_items = []

    spots: list[dict[str, Any]] = []
    free_count = 0
    occupied_count = 0
    blocked_count = 0
    reservable_count = 0

    for item in zone_items:
        if not isinstance(item, dict):
            continue
        item_id = int(item.get("id"))
        item_name = str(item.get("name", f"spot-{item_id}"))
        item_status = str(item.get("status", "unknown")).lower()
        item_is_available = bool(item.get("isAvailable", False))
        users_raw = item.get("users", [])
        users: list[dict[str, str]] = []
        if isinstance(users_raw, list):
            for u in users_raw:
                if not isinstance(u, dict):
                    continue
                first = str(u.get("firstName", "")).strip()
                last = str(u.get("lastName", "")).strip()
                full_name = (first + " " + last).strip() or str(u.get("email", "")).strip() or "Unknown"
                entry: dict[str, str] = {"name": full_name}
                if include_emails:
                    email_value = str(u.get("email", "")).strip()
                    if email_value:
                        entry["email"] = email_value
                users.append(entry)

        has_user = len(users) > 0
        if item_is_available:
            occupancy = "free"
        elif has_user:
            occupancy = "occupied"
        else:
            occupancy = "unavailable"

        blocked = (item_status != "active") or (occupancy == "unavailable")

        reasons: list[str] = []
        if not zone_is_bookable:
            reasons.append("zone_not_bookable")
        if not zone_user_has_access:
            reasons.append("no_zone_access")
        if blocked:
            reasons.append("blocked_or_inactive")
        if not item_is_available:
            reasons.append("not_available")
        if resources_bookable_until_ms is not None and end_ms > resources_bookable_until_ms:
            reasons.append("beyond_bookable_until")

        reservable = len(reasons) == 0

        if occupancy == "free":
            free_count += 1
        elif occupancy == "occupied":
            occupied_count += 1
        if blocked:
            blocked_count += 1
        if reservable:
            reservable_count += 1

        spots.append(
            {
                "zone_id": zone_id,
                "zone_name": zone_name,
                "spot_id": item_id,
                "spot_name": item_name,
                "status": occupancy,
                "is_available": item_is_available,
                "reservable": reservable,
                "blocked": blocked,
                "blocked_reason_codes": reasons,
                "raw_status": item_status,
                "users": users,
            }
        )

    summary = {
        "total_spots": len(spots),
        "free": free_count,
        "occupied": occupied_count,
        "blocked_or_unavailable": blocked_count,
        "reservable_now": reservable_count,
        "zone_is_bookable": zone_is_bookable,
        "zone_user_has_access": zone_user_has_access,
        "resources_bookable_until": zone_details.get("resourcesBookableUntil"),
    }

    return spots, summary


def print_parking_status_table(spots: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    print(
        f"Summary: total={summary.get('total_spots')} free={summary.get('free')} "
        f"occupied={summary.get('occupied')} blocked={summary.get('blocked_or_unavailable')} "
        f"reservable={summary.get('reservable_now')}"
    )
    print(" ID      Name            Status      Reservierbar  Gesperrt  Belegt durch")
    print("-------------------------------------------------------------------------------")
    for spot in sorted(spots, key=lambda x: int(x.get("spot_id", 0))):
        users = spot.get("users", [])
        by = ", ".join(str(u.get("name", "")) for u in users) if users else "-"
        if len(by) > 38:
            by = by[:35] + "..."
        print(
            f"{str(spot.get('spot_id')).rjust(3)}  "
            f"{str(spot.get('spot_name', '-'))[:14].ljust(14)}  "
            f"{str(spot.get('status', '-'))[:10].ljust(10)}  "
            f"{('yes' if spot.get('reservable') else 'no').ljust(12)}  "
            f"{('yes' if spot.get('blocked') else 'no').ljust(8)}  "
            f"{by}"
        )


def extract_users_from_zone_item(zone_item: dict[str, Any], include_emails: bool) -> list[dict[str, str]]:
    users_raw = zone_item.get("users", [])
    users: list[dict[str, str]] = []
    if not isinstance(users_raw, list):
        return users

    for user in users_raw:
        if not isinstance(user, dict):
            continue
        first = str(user.get("firstName", "")).strip()
        last = str(user.get("lastName", "")).strip()
        email = str(user.get("email", "")).strip()
        name = (first + " " + last).strip() or email or "Unknown"
        entry: dict[str, str] = {"name": name}
        if include_emails and email:
            entry["email"] = email
        users.append(entry)
    return users


def build_discovery_zone(zone: dict[str, Any], end_ms: int, include_emails: bool) -> dict[str, Any]:
    zone_id = str(zone.get("id", ""))
    zone_name = str(zone.get("name", ""))
    zone_type = str(zone.get("type", "unknown"))
    access_rules = zone.get("accessRules", {}) if isinstance(zone.get("accessRules"), dict) else {}
    zone_is_bookable = bool(access_rules.get("isBookable", True))
    zone_user_has_access = bool(access_rules.get("userHasAccess", True))
    zone_is_active = bool(zone.get("isActive", True))

    resources_bookable_until = zone.get("resourcesBookableUntil")
    resources_bookable_until_dt = parse_iso_utc_maybe(resources_bookable_until if isinstance(resources_bookable_until, str) else None)
    if resources_bookable_until_dt is not None and resources_bookable_until_dt.tzinfo is None:
        resources_bookable_until_dt = resources_bookable_until_dt.replace(tzinfo=dt.timezone.utc)
    resources_bookable_until_ms = int(resources_bookable_until_dt.timestamp() * 1000) if resources_bookable_until_dt else None

    zone_items_raw = zone.get("availability", {}).get("zoneItems", [])
    zone_items = zone_items_raw if isinstance(zone_items_raw, list) else []

    items: list[dict[str, Any]] = []
    item_total = 0
    available_count = 0
    occupied_count = 0
    bookable_now_count = 0

    for item in zone_items:
        if not isinstance(item, dict):
            continue

        item_total += 1
        item_id = int(item.get("id"))
        item_name = str(item.get("name", f"item-{item_id}"))
        item_status = str(item.get("status", "unknown")).lower()
        is_available = bool(item.get("isAvailable", False))
        users = extract_users_from_zone_item(item, include_emails=include_emails)
        reserved_by_count = len(users)

        if is_available:
            available_count += 1
        if reserved_by_count > 0:
            occupied_count += 1

        reasons: list[str] = []
        if not zone_is_active:
            reasons.append("zone_inactive")
        if not zone_is_bookable:
            reasons.append("zone_not_bookable")
        if not zone_user_has_access:
            reasons.append("no_zone_access")
        if item_status != "active":
            reasons.append("item_inactive")
        if not is_available:
            reasons.append("not_available")
        if resources_bookable_until_ms is not None and end_ms > resources_bookable_until_ms:
            reasons.append("beyond_bookable_until")

        bookable_now = len(reasons) == 0
        if bookable_now:
            bookable_now_count += 1

        items.append(
            {
                "item_id": item_id,
                "item_name": item_name,
                "item_status": item_status,
                "is_available": is_available,
                "reserved_by_count": reserved_by_count,
                "reserved_by": users,
                "bookable_now": bookable_now,
                "not_bookable_reason_codes": reasons,
            }
        )

    return {
        "zone_id": zone_id,
        "zone_name": zone_name,
        "zone_type": zone_type,
        "zone_is_active": zone_is_active,
        "zone_is_bookable": zone_is_bookable,
        "zone_user_has_access": zone_user_has_access,
        "resources_bookable_until": resources_bookable_until,
        "summary": {
            "items_total": item_total,
            "available": available_count,
            "occupied": occupied_count,
            "bookable_now": bookable_now_count,
        },
        "items": items,
    }


def print_discovery_table(discovery: dict[str, Any]) -> None:
    summary = discovery.get("summary", {})
    print(
        f"Summary: zones={summary.get('zones_total')} items={summary.get('items_total')} "
        f"available={summary.get('available_total')} occupied={summary.get('occupied_total')} "
        f"bookable_now={summary.get('bookable_now_total')}"
    )
    print("\nObjekttypen:")
    for res_type, count in sorted(discovery.get("resource_types", {}).items()):
        print(f"  - {res_type}: {count} Zone(n)")

    print("\nZonen-Uebersicht:")
    print(" Type         Zone                            Items  Frei  Belegt  BuchbarJetzt")
    print("-------------------------------------------------------------------------------")
    for zone in discovery.get("zones", []):
        zsum = zone.get("summary", {})
        print(
            f"{str(zone.get('zone_type', '-'))[:12].ljust(12)}  "
            f"{str(zone.get('zone_name', '-'))[:30].ljust(30)}  "
            f"{str(zsum.get('items_total', 0)).rjust(5)}  "
            f"{str(zsum.get('available', 0)).rjust(4)}  "
            f"{str(zsum.get('occupied', 0)).rjust(6)}  "
            f"{str(zsum.get('bookable_now', 0)).rjust(11)}"
        )

    print("\nAktuelle Buchungen:")
    found_booking = False
    for zone in discovery.get("zones", []):
        for item in zone.get("items", []):
            reserved_by = item.get("reserved_by", [])
            if not reserved_by:
                continue
            found_booking = True
            names = ", ".join(str(entry.get("name", "")) for entry in reserved_by)
            print(f"  - [{zone.get('zone_type')}] {zone.get('zone_name')} / {item.get('item_name')}: {names}")
    if not found_booking:
        print("  - Keine aktiven Buchungen im betrachteten Zeitraum gefunden.")


def url_matches_domain(url: str, domain_filter: str) -> bool:
    normalized = domain_filter.strip().lower()
    if not normalized:
        return True

    hostname = (urlparse(url).hostname or "").lower()
    if not hostname:
        return False

    wanted_domains = [part.strip().lower() for part in normalized.split(",") if part.strip()]
    if not wanted_domains:
        return True

    for wanted in wanted_domains:
        if hostname == wanted or hostname.endswith(f".{wanted}"):
            return True
    return False


def cmd_auth_capture(args: argparse.Namespace) -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Fehler: playwright ist nicht installiert. Bitte 'pip install -r requirements.txt' ausfuehren.")
        return 2

    captured_headers: dict[str, str] = {}
    observed_auth_values: set[str] = set()
    user_endpoint_ok = {"ok": False}

    def collect_from_request(request: Any) -> None:
        if not host_matches_domain(request.url, args.api_domain):
            return
        if request.resource_type not in {"xhr", "fetch"}:
            return
        try:
            raw_headers = dict(request.all_headers())
        except Exception:
            raw_headers = dict(request.headers)
        headers = {str(k).lower(): str(v) for k, v in raw_headers.items()}

        auth_value = headers.get("authorization", "").strip()
        cookie_value = headers.get("cookie", "").strip()
        csrf_value = headers.get("x-csrf-token", "").strip()
        xsrf_value = headers.get("x-xsrf-token", "").strip()

        if auth_value:
            captured_headers["DESKBIRD_AUTHORIZATION"] = auth_value
            observed_auth_values.add(auth_value)
        if cookie_value:
            captured_headers["DESKBIRD_COOKIE"] = cookie_value
        if csrf_value:
            captured_headers["DESKBIRD_X_CSRF_TOKEN"] = csrf_value
        if xsrf_value:
            captured_headers["DESKBIRD_X_XSRF_TOKEN"] = xsrf_value

    def observe_response(response: Any) -> None:
        if not host_matches_domain(response.url, args.api_domain):
            return
        if "/v1.1/user" in response.url and int(response.status) == 200:
            user_endpoint_ok["ok"] = True

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=args.headless, slow_mo=args.slow_mo)
        context = browser.new_context(ignore_https_errors=args.ignore_https_errors)
        context.on("request", collect_from_request)
        context.on("response", observe_response)

        page = context.new_page()
        print(f"Oeffne: {args.start_url}")
        page.goto(args.start_url, wait_until="domcontentloaded")

        if args.duration > 0:
            print(f"Auth-Capture aktiv fuer {args.duration} Sekunden ...")
            time.sleep(args.duration)
        else:
            print("Bitte jetzt normal einloggen. Danach Enter hier im Terminal druecken.")
            input("Enter zum Beenden des Auth-Captures ... ")

        context.close()
        browser.close()

    if not captured_headers.get("DESKBIRD_AUTHORIZATION") and not captured_headers.get("DESKBIRD_COOKIE"):
        print("Keine nutzbaren Auth-Header gefunden. Bitte erneut ausfuehren und sicher einloggen.")
        return 4

    captured_headers["DESKBIRD_BASE_URL"] = f"https://{args.api_domain}"
    captured_headers["DESKBIRD_AUTH_CAPTURED_AT"] = now_utc_iso()

    if args.print_only:
        print("Auth-Daten gefunden (nicht gespeichert):")
        for key in [
            "DESKBIRD_AUTHORIZATION",
            "DESKBIRD_COOKIE",
            "DESKBIRD_X_CSRF_TOKEN",
            "DESKBIRD_X_XSRF_TOKEN",
            "DESKBIRD_BASE_URL",
            "DESKBIRD_AUTH_CAPTURED_AT",
        ]:
            val = captured_headers.get(key, "")
            if not val:
                continue
            print(f"{key}={redact_value(val) if 'AUTHORIZATION' in key or 'COOKIE' in key or 'TOKEN' in key else val}")
    else:
        upsert_env_file(args.env_file, captured_headers)
        print(f"Auth-Daten in {args.env_file} gespeichert.")

    print(f"/v1.1/user waehrend Capture erfolgreich: {'ja' if user_endpoint_ok['ok'] else 'nein'}")
    if len(observed_auth_values) > 1:
        print("Hinweis: Mehrere unterschiedliche Bearer Tokens gesehen (Token-Rotation im Browser aktiv).")
    elif len(observed_auth_values) == 1:
        print("Hinweis: Ein Bearer Token waehrend der Session gesehen.")
    else:
        print("Hinweis: Kein Bearer Token gesehen (Cookie-basierte Session moeglich).")

    print("Empfehlung: Danach 'auth-check' ausfuehren.")
    return 0


def cmd_auth_import(args: argparse.Namespace) -> int:
    raw_parts: list[str] = []
    if args.telegram_text:
        raw_parts.append(str(args.telegram_text))
    if args.from_file:
        raw_parts.append(Path(args.from_file).read_text(encoding="utf-8"))
    if args.stdin:
        raw_parts.append(sys.stdin.read())

    parsed_values = parse_auth_values_from_text("\n".join(raw_parts))
    values: dict[str, str] = {}
    values.update(parsed_values)

    if args.token:
        values["DESKBIRD_AUTHORIZATION"] = normalize_authorization_value(args.token)
    if args.authorization:
        values["DESKBIRD_AUTHORIZATION"] = normalize_authorization_value(args.authorization)
    if args.cookie:
        values["DESKBIRD_COOKIE"] = strip_wrapping_quotes(args.cookie)
    if args.x_csrf_token:
        values["DESKBIRD_X_CSRF_TOKEN"] = strip_wrapping_quotes(args.x_csrf_token)
    if args.x_xsrf_token:
        values["DESKBIRD_X_XSRF_TOKEN"] = strip_wrapping_quotes(args.x_xsrf_token)
    if args.base_url:
        values["DESKBIRD_BASE_URL"] = str(args.base_url).strip().rstrip("/")
    if args.firebase_api_key:
        values["DESKBIRD_FIREBASE_API_KEY"] = strip_wrapping_quotes(args.firebase_api_key)
    if args.firebase_refresh_token:
        values["DESKBIRD_FIREBASE_REFRESH_TOKEN"] = strip_wrapping_quotes(args.firebase_refresh_token)

    auth_related_keys = [
        "DESKBIRD_AUTHORIZATION",
        "DESKBIRD_COOKIE",
        "DESKBIRD_X_CSRF_TOKEN",
        "DESKBIRD_X_XSRF_TOKEN",
    ]
    has_auth_values = any(values.get(key, "").strip() for key in auth_related_keys)
    has_firebase_refresh_values = bool(values.get("DESKBIRD_FIREBASE_API_KEY", "").strip()) and bool(
        values.get("DESKBIRD_FIREBASE_REFRESH_TOKEN", "").strip()
    )
    if not has_auth_values and not has_firebase_refresh_values:
        raise ValueError(
            "Keine nutzbaren Auth-Werte gefunden. "
            "Bitte mindestens Authorization/Cookie oder Firebase API-Key + Refresh-Token uebergeben."
        )

    values["DESKBIRD_AUTH_CAPTURED_AT"] = now_utc_iso()
    upsert_env_file(args.env_file, values)

    imported_preview = {
        key: (redact_value(values[key]) if "AUTHORIZATION" in key or "COOKIE" in key or "TOKEN" in key else values[key])
        for key in [
            "DESKBIRD_AUTHORIZATION",
            "DESKBIRD_COOKIE",
            "DESKBIRD_X_CSRF_TOKEN",
            "DESKBIRD_X_XSRF_TOKEN",
            "DESKBIRD_FIREBASE_API_KEY",
            "DESKBIRD_FIREBASE_REFRESH_TOKEN",
            "DESKBIRD_BASE_URL",
            "DESKBIRD_AUTH_CAPTURED_AT",
        ]
        if values.get(key)
    }

    if not args.verify:
        result = {
            "imported": True,
            "env_file": args.env_file,
            "imported_values": imported_preview,
            "verified": False,
        }
        if args.format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=True))
        else:
            print(f"Auth-Werte in {args.env_file} gespeichert.")
            for key, value in imported_preview.items():
                print(f"{key}={value}")
            print("Hinweis: Verifikation deaktiviert (--no-verify).")
        return 0

    refresh_performed = False
    if not has_auth_values and has_firebase_refresh_values:
        refresh_performed = True
        refresh_resp, refresh_payload = run_firebase_token_refresh(
            api_key=values.get("DESKBIRD_FIREBASE_API_KEY", ""),
            refresh_token=values.get("DESKBIRD_FIREBASE_REFRESH_TOKEN", ""),
            timeout=int(args.timeout),
        )
        if refresh_resp.status_code >= 400 or not isinstance(refresh_payload, dict):
            result = {
                "imported": True,
                "env_file": args.env_file,
                "imported_values": imported_preview,
                "verified": True,
                "refresh_performed": True,
                "refresh_http_status": refresh_resp.status_code,
                "refresh_error_excerpt": sanitize_body(refresh_resp.text, keep_secrets=False, max_len=1000),
            }
            if args.format == "json":
                print(json.dumps(result, indent=2, ensure_ascii=True))
            else:
                print(f"Auth-Werte in {args.env_file} gespeichert.")
                print("Firebase-Refresh nach Import fehlgeschlagen.")
                print_response_summary(refresh_resp, max_chars=1500)
            return 5

        id_token = str(refresh_payload.get("id_token") or "").strip()
        rotated_refresh_token = str(refresh_payload.get("refresh_token") or "").strip()
        if not id_token:
            result = {
                "imported": True,
                "env_file": args.env_file,
                "imported_values": imported_preview,
                "verified": True,
                "refresh_performed": True,
                "refresh_http_status": refresh_resp.status_code,
                "refresh_error": "securetoken_response_without_id_token",
            }
            if args.format == "json":
                print(json.dumps(result, indent=2, ensure_ascii=True))
            else:
                print(f"Auth-Werte in {args.env_file} gespeichert.")
                print("Firebase-Refresh lieferte kein id_token.")
            return 5

        refresh_values = {
            "DESKBIRD_AUTHORIZATION": f"Bearer {id_token}",
            "DESKBIRD_AUTH_CAPTURED_AT": now_utc_iso(),
        }
        if rotated_refresh_token:
            refresh_values["DESKBIRD_FIREBASE_REFRESH_TOKEN"] = rotated_refresh_token
        upsert_env_file(args.env_file, refresh_values)
        imported_preview["DESKBIRD_AUTHORIZATION"] = redact_value(refresh_values["DESKBIRD_AUTHORIZATION"])
        if rotated_refresh_token:
            imported_preview["DESKBIRD_FIREBASE_REFRESH_TOKEN"] = redact_value(rotated_refresh_token)

    response, report = run_auth_check(
        env_file=args.env_file,
        timeout=int(args.timeout),
        min_valid_minutes=max(0, int(args.min_valid_minutes)),
        dotenv_override=True,
    )

    result = {
        "imported": True,
        "env_file": args.env_file,
        "imported_values": imported_preview,
        "verified": True,
        "refresh_performed": refresh_performed,
        "auth_check_report": report,
    }

    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=True))
    else:
        print(f"Auth-Werte in {args.env_file} gespeichert.")
        for key, value in imported_preview.items():
            print(f"{key}={value}")
        if refresh_performed:
            print("Firebase-Refresh wurde nach dem Import automatisch ausgefuehrt.")
        print_auth_check_report(report)
        if response.status_code >= 400:
            print_response_summary(response, max_chars=2000)

    if response.status_code >= 400:
        return 5
    if report.get("requires_reauth"):
        return 10
    return 0


def run_auth_check(
    env_file: str,
    timeout: int,
    min_valid_minutes: int,
    dotenv_override: bool = False,
) -> tuple[requests.Response, dict[str, Any]]:
    load_dotenv(env_file, override=dotenv_override)
    auth_headers = build_auth_headers_from_env()
    require_auth_headers(auth_headers)

    headers = {"Accept": "application/json"}
    headers.update(auth_headers)
    url = f"{get_base_url()}/v1.1/user"

    response, payload = request_json("GET", url, headers=headers, timeout=timeout)
    report = build_auth_check_report(
        auth_headers=auth_headers,
        response=response,
        payload=payload,
        min_valid_minutes=max(0, int(min_valid_minutes)),
    )
    return response, report


def resolve_firebase_api_key(explicit_value: str | None = None) -> str:
    candidates = [
        str(explicit_value or "").strip(),
        os.getenv("DESKBIRD_FIREBASE_API_KEY", "").strip(),
        os.getenv("DESKBIRD_FIREBASE_WEB_API_KEY", "").strip(),
        os.getenv("DESKBIRD_GOOGLE_API_KEY", "").strip(),
    ]
    for value in candidates:
        if value:
            return value
    return ""


def resolve_firebase_refresh_token(explicit_value: str | None = None) -> str:
    candidates = [
        str(explicit_value or "").strip(),
        os.getenv("DESKBIRD_FIREBASE_REFRESH_TOKEN", "").strip(),
    ]
    for value in candidates:
        if value:
            return value
    return ""


def run_firebase_token_refresh(api_key: str, refresh_token: str, timeout: int) -> tuple[requests.Response, dict[str, Any] | None]:
    key = str(api_key or "").strip()
    rt = str(refresh_token or "").strip()
    if not key:
        raise ValueError("Firebase API-Key fehlt. Bitte --firebase-api-key oder DESKBIRD_FIREBASE_API_KEY setzen.")
    if not rt:
        raise ValueError("Firebase Refresh-Token fehlt. Bitte --firebase-refresh-token oder DESKBIRD_FIREBASE_REFRESH_TOKEN setzen.")

    url = f"https://securetoken.googleapis.com/v1/token?key={key}"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    body = {"grant_type": "refresh_token", "refresh_token": rt}
    response = safe_request("POST", url, headers=headers, data=body, timeout=timeout)

    payload: dict[str, Any] | None = None
    ctype = response.headers.get("content-type", "").lower()
    if "application/json" in ctype:
        try:
            parsed = response.json()
            if isinstance(parsed, dict):
                payload = parsed
        except Exception:
            payload = None
    return response, payload


def cmd_auth_refresh(args: argparse.Namespace) -> int:
    load_dotenv(args.env_file, override=False)

    api_key = resolve_firebase_api_key(args.firebase_api_key)
    refresh_token = resolve_firebase_refresh_token(args.firebase_refresh_token)

    response, payload = run_firebase_token_refresh(
        api_key=api_key,
        refresh_token=refresh_token,
        timeout=int(args.timeout),
    )

    securetoken_summary: dict[str, Any] = {
        "http_status": response.status_code,
        "api_key": redact_value(api_key) if api_key else None,
        "refresh_token": redact_value(refresh_token) if refresh_token else None,
    }

    if isinstance(payload, dict):
        securetoken_summary["expires_in_seconds"] = int(str(payload.get("expires_in", "0") or "0")) if str(payload.get("expires_in", "")).isdigit() else None
        securetoken_summary["project_id"] = payload.get("project_id")
        securetoken_summary["user_id"] = payload.get("user_id")

    if response.status_code >= 400 or not isinstance(payload, dict):
        result = {
            "refreshed": False,
            "env_file": args.env_file,
            "securetoken": securetoken_summary,
            "error_excerpt": sanitize_body(response.text, keep_secrets=False, max_len=1000),
        }
        if args.format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=True))
        else:
            print("Firebase Token-Refresh fehlgeschlagen.")
            print(f"HTTP: {response.status_code}")
            print(f"API-Key: {securetoken_summary.get('api_key')}")
            print(f"Refresh-Token: {securetoken_summary.get('refresh_token')}")
            print_response_summary(response, max_chars=1500)
        return 5

    id_token = str(payload.get("id_token") or "").strip()
    new_refresh_token = str(payload.get("refresh_token") or "").strip()
    if not id_token:
        result = {
            "refreshed": False,
            "env_file": args.env_file,
            "securetoken": securetoken_summary,
            "error": "securetoken_response_without_id_token",
        }
        if args.format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=True))
        else:
            print("Firebase Token-Refresh lieferte kein id_token.")
        return 5

    values: dict[str, str] = {
        "DESKBIRD_AUTHORIZATION": f"Bearer {id_token}",
        "DESKBIRD_AUTH_CAPTURED_AT": now_utc_iso(),
        "DESKBIRD_FIREBASE_API_KEY": api_key,
    }
    if new_refresh_token:
        values["DESKBIRD_FIREBASE_REFRESH_TOKEN"] = new_refresh_token
        securetoken_summary["refresh_token_rotated"] = new_refresh_token != refresh_token
    else:
        securetoken_summary["refresh_token_rotated"] = False

    upsert_env_file(args.env_file, values)

    if not args.verify:
        result = {
            "refreshed": True,
            "verified": False,
            "env_file": args.env_file,
            "securetoken": securetoken_summary,
        }
        if args.format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=True))
        else:
            print(f"Auth erfolgreich refreshed und in {args.env_file} gespeichert (ohne Verifikation).")
            print(f"API-Key: {securetoken_summary.get('api_key')}")
            print(f"Refresh-Token: {securetoken_summary.get('refresh_token')}")
        return 0

    deskbird_response, report = run_auth_check(
        env_file=args.env_file,
        timeout=int(args.timeout),
        min_valid_minutes=max(0, int(args.min_valid_minutes)),
        dotenv_override=True,
    )

    result = {
        "refreshed": True,
        "verified": True,
        "env_file": args.env_file,
        "securetoken": securetoken_summary,
        "auth_check_report": report,
    }

    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=True))
    else:
        print(f"Auth in {args.env_file} refreshed.")
        print(f"API-Key: {securetoken_summary.get('api_key')}")
        print(f"Refresh-Token: {securetoken_summary.get('refresh_token')}")
        print_auth_check_report(report)
        if deskbird_response.status_code >= 400:
            print_response_summary(deskbird_response, max_chars=1500)

    if deskbird_response.status_code >= 400:
        return 5
    if report.get("requires_reauth"):
        return 10
    return 0


def cmd_auth_pair_start(args: argparse.Namespace) -> int:
    store_path = get_auth_pair_store_path(args.store_file)
    state = load_auth_pair_store(store_path)
    sessions = state.setdefault("sessions", {})
    if not isinstance(sessions, dict):
        sessions = {}
        state["sessions"] = sessions

    now_utc = now_utc_dt()
    changed = False
    if expire_pairing_sessions(state, now_utc=now_utc):
        changed = True
    if cleanup_pairing_sessions(state, now_utc=now_utc):
        changed = True

    ttl_minutes = max(1, int(args.ttl_minutes))
    created_code = None
    for _ in range(40):
        candidate = generate_pairing_code(length=args.code_length)
        if candidate not in sessions:
            created_code = candidate
            break
    if not created_code:
        raise ValueError("Konnte keinen freien Pairing-Code erzeugen.")

    expires_at = now_utc + dt.timedelta(minutes=ttl_minutes)
    sessions[created_code] = {
        "status": PAIRING_STATUS_PENDING,
        "created_at_utc": now_utc.isoformat(),
        "expires_at_utc": expires_at.isoformat(),
        "env_file": args.env_file,
        "start_url": args.start_url,
        "api_domain": args.api_domain,
        "min_valid_minutes": max(0, int(args.min_valid_minutes)),
        "note": str(args.note or "").strip(),
    }
    changed = True
    if changed:
        save_auth_pair_store(store_path, state)

    view = build_pairing_view(created_code, sessions[created_code])
    view["store_file"] = str(store_path)
    view["user_message"] = (
        "Fuehre lokal den Finish-Command aus und logge dich im Browser normal per SSO ein. "
        "Den Pairing-Code NICHT in deskbird eingeben."
    )

    if args.format == "json":
        print(json.dumps(view, indent=2, ensure_ascii=True))
    else:
        print("Auth-Pairing gestartet.")
        print_pairing_table(view)
        print("Hinweis: Code nur einmalig verwenden und vor Ablauf abschliessen.")

    return 0


def cmd_auth_pair_status(args: argparse.Namespace) -> int:
    code = normalize_pairing_code(args.code)
    store_path = get_auth_pair_store_path(args.store_file)
    state = load_auth_pair_store(store_path)
    sessions = state.get("sessions", {})
    if not isinstance(sessions, dict):
        raise ValueError("Pairing-Store hat ungueltige sessions-Struktur.")

    now_utc = now_utc_dt()
    changed = False
    if expire_pairing_sessions(state, now_utc=now_utc):
        changed = True

    session = sessions.get(code)
    if not isinstance(session, dict):
        raise ValueError(f"Pairing-Code '{code}' nicht gefunden.")

    if cleanup_pairing_sessions(state, now_utc=now_utc):
        changed = True
    if changed:
        save_auth_pair_store(store_path, state)

    view = build_pairing_view(code, session)
    if args.format == "json":
        print(json.dumps(view, indent=2, ensure_ascii=True))
    else:
        print_pairing_table(view)

    return pairing_status_exit_code(str(session.get("status", "")))


def cmd_auth_pair_cancel(args: argparse.Namespace) -> int:
    code = normalize_pairing_code(args.code)
    store_path = get_auth_pair_store_path(args.store_file)
    state = load_auth_pair_store(store_path)
    sessions = state.get("sessions", {})
    if not isinstance(sessions, dict):
        raise ValueError("Pairing-Store hat ungueltige sessions-Struktur.")

    session = sessions.get(code)
    if not isinstance(session, dict):
        raise ValueError(f"Pairing-Code '{code}' nicht gefunden.")

    status = str(session.get("status", ""))
    if status in PAIRING_TERMINAL_STATUSES:
        view = build_pairing_view(code, session)
        if args.format == "json":
            print(json.dumps(view, indent=2, ensure_ascii=True))
        else:
            print("Pairing war bereits beendet.")
            print_pairing_table(view)
        return 0

    session["status"] = PAIRING_STATUS_CANCELLED
    session["finished_at_utc"] = now_utc_iso()
    save_auth_pair_store(store_path, state)

    view = build_pairing_view(code, session)
    if args.format == "json":
        print(json.dumps(view, indent=2, ensure_ascii=True))
    else:
        print("Pairing abgebrochen.")
        print_pairing_table(view)
    return 0


def cmd_auth_pair_finish(args: argparse.Namespace) -> int:
    code = normalize_pairing_code(args.code)
    store_path = get_auth_pair_store_path(args.store_file)
    state = load_auth_pair_store(store_path)
    sessions = state.get("sessions", {})
    if not isinstance(sessions, dict):
        raise ValueError("Pairing-Store hat ungueltige sessions-Struktur.")

    now_utc = now_utc_dt()
    changed = False
    if expire_pairing_sessions(state, now_utc=now_utc):
        changed = True

    session = sessions.get(code)
    if not isinstance(session, dict):
        raise ValueError(f"Pairing-Code '{code}' nicht gefunden.")

    status = str(session.get("status", ""))
    if status == PAIRING_STATUS_EXPIRED:
        if changed:
            save_auth_pair_store(store_path, state)
        raise ValueError("Pairing-Code ist abgelaufen. Bitte ein neues Pairing starten.")
    if status == PAIRING_STATUS_CANCELLED:
        if changed:
            save_auth_pair_store(store_path, state)
        raise ValueError("Pairing wurde abgebrochen.")
    if status == PAIRING_STATUS_COMPLETED:
        view = build_pairing_view(code, session)
        if args.format == "json":
            print(json.dumps(view, indent=2, ensure_ascii=True))
        else:
            print("Pairing ist bereits abgeschlossen.")
            print_pairing_table(view)
        return 0

    expires_at = parse_utc_iso_maybe(session.get("expires_at_utc"))
    if expires_at is not None and expires_at <= now_utc:
        session["status"] = PAIRING_STATUS_EXPIRED
        session["finished_at_utc"] = now_utc.isoformat()
        save_auth_pair_store(store_path, state)
        raise ValueError("Pairing-Code ist abgelaufen. Bitte ein neues Pairing starten.")

    env_file = str(args.env_file or session.get("env_file") or ".env")
    start_url = str(args.start_url or session.get("start_url") or "https://app.deskbird.com")
    api_domain = str(args.api_domain or session.get("api_domain") or "api.deskbird.com")
    requested_min_valid_minutes = int(session.get("min_valid_minutes", 90))
    if int(args.min_valid_minutes) >= 0:
        requested_min_valid_minutes = int(args.min_valid_minutes)

    session["status"] = PAIRING_STATUS_IN_PROGRESS
    session["started_at_utc"] = now_utc.isoformat()
    session.pop("error_code", None)
    session.pop("error_message", None)
    save_auth_pair_store(store_path, state)

    capture_args = argparse.Namespace(
        start_url=start_url,
        api_domain=api_domain,
        env_file=env_file,
        duration=0,
        headless=bool(args.headless),
        slow_mo=int(args.slow_mo),
        ignore_https_errors=bool(args.ignore_https_errors),
        print_only=False,
    )

    capture_exit = cmd_auth_capture(capture_args)
    if capture_exit != 0:
        session["status"] = PAIRING_STATUS_FAILED
        session["finished_at_utc"] = now_utc_iso()
        session["error_code"] = f"auth_capture_exit_{capture_exit}"
        session["error_message"] = "Auth-Capture konnte nicht erfolgreich abgeschlossen werden."
        save_auth_pair_store(store_path, state)
        view = build_pairing_view(code, session)
        if args.format == "json":
            print(json.dumps(view, indent=2, ensure_ascii=True))
        else:
            print("Pairing fehlgeschlagen.")
            print_pairing_table(view)
        return capture_exit

    response, report = run_auth_check(
        env_file=env_file,
        timeout=int(args.timeout),
        min_valid_minutes=requested_min_valid_minutes,
        dotenv_override=True,
    )

    session["auth_check_report"] = report
    session["finished_at_utc"] = now_utc_iso()
    if response.status_code >= 400:
        session["status"] = PAIRING_STATUS_FAILED
        session["error_code"] = "auth_rejected"
        session["error_message"] = "Auth wurde vom Server abgelehnt."
    elif report.get("requires_reauth"):
        session["status"] = PAIRING_STATUS_FAILED
        session["error_code"] = str(report.get("reason_code") or "reauth_required")
        session["error_message"] = "Reauth weiterhin erforderlich."
    else:
        session["status"] = PAIRING_STATUS_COMPLETED
    save_auth_pair_store(store_path, state)

    view = build_pairing_view(code, session)
    view["auth_check_report"] = report
    if args.format == "json":
        print(json.dumps(view, indent=2, ensure_ascii=True))
    else:
        if session["status"] == PAIRING_STATUS_COMPLETED:
            print("Pairing erfolgreich abgeschlossen.")
        else:
            print("Pairing abgeschlossen, aber Auth ist noch nicht nutzbar.")
        print_pairing_table(view)
        print_auth_check_report(report)

    return pairing_status_exit_code(str(session.get("status", "")))


def cmd_auth_check(args: argparse.Namespace) -> int:
    response, report = run_auth_check(
        env_file=args.env_file,
        timeout=int(args.timeout),
        min_valid_minutes=max(0, int(args.min_valid_minutes)),
        dotenv_override=False,
    )

    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=True))
    else:
        print_auth_check_report(report)
        if response.status_code >= 400:
            print_response_summary(response, max_chars=2000)

    if response.status_code >= 400:
        return 5
    if report.get("requires_reauth"):
        return 10
    return 0


def cmd_capture(args: argparse.Namespace) -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Fehler: playwright ist nicht installiert. Bitte 'pip install -r requirements.txt' ausfuehren.")
        return 2

    out_path = Path(args.out)
    captured: list[dict[str, Any]] = []
    pending: dict[Any, dict[str, Any]] = {}
    counter = 0

    def on_request(request: Any) -> None:
        nonlocal counter
        if request.resource_type not in {"xhr", "fetch"}:
            return
        if not url_matches_domain(request.url, args.domain_filter):
            return

        counter += 1
        pending[request] = {
            "id": counter,
            "captured_at": now_utc_iso(),
            "method": request.method,
            "url": request.url,
            "resource_type": request.resource_type,
            "request": {
                "headers": sanitize_headers(dict(request.headers), keep_secrets=args.unsafe_keep_secrets),
                "body": sanitize_body(request.post_data, keep_secrets=args.unsafe_keep_secrets, max_len=args.max_body_chars),
            },
        }

    def on_response(response: Any) -> None:
        request = response.request
        record = pending.pop(request, None)
        if record is None:
            return

        body_excerpt: Any = None
        if args.capture_response_body:
            try:
                raw_text = response.text()
            except Exception:
                raw_text = ""
            body_excerpt = sanitize_body(
                raw_text,
                keep_secrets=args.unsafe_keep_secrets,
                max_len=args.max_body_chars,
            )

        record["response"] = {
            "status": response.status,
            "headers": sanitize_headers(dict(response.headers), keep_secrets=args.unsafe_keep_secrets),
            "content_type": response.headers.get("content-type", ""),
            "body_excerpt": body_excerpt,
        }
        captured.append(record)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=args.headless, slow_mo=args.slow_mo)
        context = browser.new_context(ignore_https_errors=args.ignore_https_errors)
        context.on("request", on_request)
        context.on("response", on_response)

        page = context.new_page()
        print(f"Oeffne: {args.start_url}")
        page.goto(args.start_url, wait_until="domcontentloaded")

        if args.duration > 0:
            print(f"Capture aktiv fuer {args.duration} Sekunden ...")
            time.sleep(args.duration)
        else:
            print("Capture aktiv. Fuehre jetzt Login/Buchung im Browser aus.")
            input("Wenn fertig: Enter druecken, um zu speichern und zu beenden ... ")

        context.close()
        browser.close()

    data = {
        "meta": {
            "created_at": now_utc_iso(),
            "start_url": args.start_url,
            "domain_filter": args.domain_filter,
            "unsafe_keep_secrets": bool(args.unsafe_keep_secrets),
            "capture_response_body": bool(args.capture_response_body),
            "count": len(captured),
        },
        "records": captured,
    }

    write_json(out_path, data)
    print(f"Gespeichert: {out_path}")
    print(f"Erfasste Requests: {len(captured)}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    data = read_json(Path(args.file))
    records = data.get("records", [])
    if not records:
        print("Keine Records gefunden.")
        return 0

    print(f"Datei: {args.file}")
    print(f"Records: {len(records)}")
    print("\n ID  ST  METHOD  URL")
    print("-" * 120)
    for rec in records:
        rid = rec.get("id", "?")
        status = rec.get("response", {}).get("status", "?")
        method = rec.get("method", "?")
        url = rec.get("url", "")
        if len(url) > 92:
            url = url[:89] + "..."
        print(f"{str(rid).rjust(3)} {str(status).rjust(3)}  {method.ljust(6)}  {url}")
    return 0


def pick_record(records: list[dict[str, Any]], record_id: int) -> dict[str, Any]:
    for rec in records:
        if rec.get("id") == record_id:
            return rec
    raise ValueError(f"Record mit id={record_id} nicht gefunden")


def prepare_headers_for_replay(captured_headers: dict[str, str], auth_headers: dict[str, str]) -> dict[str, str]:
    replay_headers: dict[str, str] = {}

    for key, value in captured_headers.items():
        key_l = key.lower()
        if key_l in HEADER_BLACKLIST_FOR_REPLAY:
            continue
        if isinstance(value, str) and value.startswith("<redacted:"):
            continue
        replay_headers[key] = value

    replay_headers.update(auth_headers)
    return replay_headers


def perform_request(
    method: str,
    url: str,
    headers: dict[str, str],
    body: Any,
    timeout: int,
) -> requests.Response:
    kwargs: dict[str, Any] = {
        "headers": headers,
        "timeout": timeout,
    }

    if isinstance(body, (dict, list)):
        kwargs["json"] = body
    elif isinstance(body, str) and body:
        kwargs["data"] = body

    return safe_request(method, url, **kwargs)


def print_response_summary(response: requests.Response, max_chars: int) -> None:
    print(f"Status: {response.status_code}")
    print("Response-Header (Auszug):")
    for key in ["content-type", "x-request-id", "retry-after", "set-cookie"]:
        if key in response.headers:
            print(f"  {key}: {response.headers.get(key)}")

    ctype = response.headers.get("content-type", "")
    text = response.text
    if "application/json" in ctype.lower():
        try:
            payload = response.json()
            pretty = json.dumps(payload, indent=2, ensure_ascii=True)
            if len(pretty) > max_chars:
                pretty = pretty[:max_chars] + f"\n... <truncated:{len(pretty) - max_chars} chars>"
            print("\nJSON-Body:")
            print(pretty)
            return
        except Exception:
            pass

    if len(text) > max_chars:
        text = text[:max_chars] + f"... <truncated:{len(text) - max_chars} chars>"
    print("\nBody (Text):")
    print(text)


def cmd_replay(args: argparse.Namespace) -> int:
    load_dotenv(args.env_file, override=False)

    data = read_json(Path(args.file))
    records = data.get("records", [])
    if not records:
        print("Keine Records in Capture-Datei vorhanden.")
        return 1

    rec = pick_record(records, args.id)

    method = rec.get("method", "GET")
    url = rec.get("url", "")
    req = rec.get("request", {})
    captured_headers = req.get("headers", {}) or {}
    body = req.get("body", None)

    if args.override_json:
        body = read_json(Path(args.override_json))

    auth_headers = build_auth_headers_from_env()
    headers = prepare_headers_for_replay(captured_headers, auth_headers)

    if args.dry_run:
        print("Dry-Run aktiv, es wird kein API-Call ausgefuehrt.")
        print(f"Method: {method}")
        print(f"URL: {url}")
        print("Header:")
        for key, value in headers.items():
            safe_val = redact_value(value) if looks_secret_header(key) else value
            print(f"  {key}: {safe_val}")
        print("Body:")
        print(json.dumps(body, indent=2, ensure_ascii=True) if isinstance(body, (dict, list)) else body)
        return 0

    response = perform_request(method, url, headers, body, args.timeout)
    print_response_summary(response, max_chars=args.max_body_chars)
    return 0


def cmd_probe(args: argparse.Namespace) -> int:
    load_dotenv(args.env_file, override=False)

    auth_headers = build_auth_headers_from_env()
    params = parse_key_value_pairs(args.param)
    headers = parse_key_value_pairs(args.header)
    headers.update(auth_headers)

    base_url = get_base_url()
    if args.url:
        url = args.url
    else:
        path = args.path if args.path.startswith("/") else f"/{args.path}"
        url = f"{base_url}{path}"

    body: Any = None
    if args.json_file:
        body = read_json(Path(args.json_file))
    elif args.data:
        body = args.data

    if args.dry_run:
        print("Dry-Run aktiv, es wird kein API-Call ausgefuehrt.")
        print(f"Method: {args.method.upper()}")
        print(f"URL: {url}")
        print(f"Query: {json.dumps(params, ensure_ascii=True)}")
        print("Header:")
        for key, value in headers.items():
            safe_val = redact_value(value) if looks_secret_header(key) else value
            print(f"  {key}: {safe_val}")
        if body is not None:
            print("Body:")
            print(json.dumps(body, indent=2, ensure_ascii=True) if isinstance(body, (dict, list)) else body)
        return 0

    kwargs: dict[str, Any] = {
        "headers": headers,
        "params": params,
        "timeout": args.timeout,
    }
    if isinstance(body, (dict, list)):
        kwargs["json"] = body
    elif isinstance(body, str):
        kwargs["data"] = body

    response = safe_request(args.method.upper(), url, **kwargs)
    print_response_summary(response, max_chars=args.max_body_chars)
    return 0


def cmd_parking_check(args: argparse.Namespace) -> int:
    load_dotenv(args.env_file, override=False)

    auth_headers = build_auth_headers_from_env()
    require_auth_headers(auth_headers)
    headers = {"Accept": "application/json"}
    headers.update(auth_headers)
    office_id, office_resolution = resolve_office(args.office_id, args.office_name, headers=headers, timeout=args.timeout)

    start_ms, end_ms, start_iso, end_iso = parse_local_range_to_epoch_ms(
        args.date,
        args.start_local,
        args.end_local,
        args.timezone,
    )

    parking_zones = get_parking_zones(office_id, start_ms, end_ms, headers=headers, timeout=args.timeout)
    if not parking_zones:
        print("Keine Parking-Zonen gefunden.")
        return 4

    selected_zones: list[dict[str, Any]]
    if args.zone_id:
        selected_zones = [find_zone_by_id(parking_zones, args.zone_id)]
    else:
        selected_zones = parking_zones

    print(f"Zeitraum (lokal): {start_iso} -> {end_iso}")
    print(f"Workspace: {office_id}")
    if office_resolution.get("selection_reason") != "explicit_office_id":
        print(f"Office-Aufloesung: {office_resolution.get('office_name')} ({office_resolution.get('selection_reason')})")
    has_available = False

    for zone in selected_zones:
        zid = str(zone.get("id"))
        details = get_zone_details(office_id, zid, start_ms, end_ms, headers=headers, timeout=args.timeout)
        available_items = get_available_zone_items(details)

        total = details.get("availability", {}).get("total")
        available_count = details.get("availability", {}).get("available")
        print(f"\nZone {zid} ({details.get('name', '-')})")
        print(f"Verfuegbar: {available_count}/{total}")

        if available_items:
            has_available = True
            for item in available_items:
                print(f"  - {item.get('id')}: {item.get('name')}")
        else:
            print("  - Keine freien Parkplaetze.")

    return 0 if has_available else 4


def cmd_parking_book_first(args: argparse.Namespace) -> int:
    load_dotenv(args.env_file, override=False)

    auth_headers = build_auth_headers_from_env()
    require_auth_headers(auth_headers)
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    headers.update(auth_headers)
    office_id, office_resolution = resolve_office(args.office_id, args.office_name, headers=headers, timeout=args.timeout)

    start_ms, end_ms, start_iso, end_iso = parse_local_range_to_epoch_ms(
        args.date,
        args.start_local,
        args.end_local,
        args.timezone,
    )

    parking_zones = get_parking_zones(office_id, start_ms, end_ms, headers=headers, timeout=args.timeout)
    if not parking_zones:
        print("Keine Parking-Zonen gefunden.")
        return 4

    if args.zone_id:
        selected_zone = find_zone_by_id(parking_zones, args.zone_id)
    else:
        selected_zone = parking_zones[0]

    zone_id = str(selected_zone.get("id"))
    zone_details = get_zone_details(office_id, zone_id, start_ms, end_ms, headers=headers, timeout=args.timeout)
    available_items = get_available_zone_items(zone_details)

    if not available_items:
        print(f"Keine freien Parkplaetze in Zone {zone_id} ({zone_details.get('name', '-')}).")
        return 4

    picked_item: dict[str, Any]
    if args.prefer_zone_item_id:
        picked_item = find_zone_by_id(available_items, args.prefer_zone_item_id)
    else:
        picked_item = available_items[0]

    zone_item_id = picked_item.get("id")
    payload = {
        "bookings": [
            {
                "bookingStartTime": start_ms,
                "bookingEndTime": end_ms,
                "isAnonymous": bool(args.is_anonymous),
                "resourceId": str(zone_id),
                "zoneItemId": int(zone_item_id),
                "workspaceId": str(office_id),
            }
        ]
    }

    print(f"Zeitraum (lokal): {start_iso} -> {end_iso}")
    print(f"Workspace: {office_id}")
    if office_resolution.get("selection_reason") != "explicit_office_id":
        print(f"Office-Aufloesung: {office_resolution.get('office_name')} ({office_resolution.get('selection_reason')})")
    print(f"Ausgewaehlte Zone: {zone_id} ({zone_details.get('name', '-')})")
    print(f"Ausgewaehlter Parkplatz: {zone_item_id} ({picked_item.get('name', '-')})")

    if args.dry_run:
        print("\nDry-Run aktiv, es wird kein API-Call ausgefuehrt.")
        print(json.dumps(payload, indent=2, ensure_ascii=True))
        return 0

    url = f"{get_base_url()}/v1.1/bookings"
    response, result = request_json("POST", url, headers=headers, timeout=args.timeout, json_body=payload)
    if response.status_code >= 400:
        print("Buchung fehlgeschlagen.")
        print_response_summary(response, max_chars=3000)
        return 5

    body = unwrap_data(result)
    if not isinstance(body, dict):
        print("Buchung gesendet, aber Antwort ist unerwartet.")
        print_response_summary(response, max_chars=3000)
        return 6

    successful = body.get("successfulBookings", [])
    failed = body.get("failedBookings", [])
    if successful:
        first = successful[0] if isinstance(successful[0], dict) else {}
        print(f"Buchung erfolgreich. bookingId={first.get('id')} zoneItem={first.get('zoneItemName')}")
        return 0

    print("Buchung wurde nicht erfolgreich angelegt.")
    print(json.dumps({"failedBookings": failed}, indent=2, ensure_ascii=True))
    return 7


def cmd_parking_status(args: argparse.Namespace) -> int:
    load_dotenv(args.env_file, override=False)

    auth_headers = build_auth_headers_from_env()
    require_auth_headers(auth_headers)
    headers = {"Accept": "application/json"}
    headers.update(auth_headers)
    office_id, office_resolution = resolve_office(args.office_id, args.office_name, headers=headers, timeout=args.timeout)

    start_ms, end_ms, start_iso, end_iso = parse_local_range_to_epoch_ms(
        args.date,
        args.start_local,
        args.end_local,
        args.timezone,
    )

    parking_zones = get_parking_zones(office_id, start_ms, end_ms, headers=headers, timeout=args.timeout)
    selected_zone = resolve_zone(parking_zones, zone_id=args.zone_id, zone_name=args.zone_name)
    zone_id = str(selected_zone.get("id"))
    zone_details = get_zone_details(office_id, zone_id, start_ms, end_ms, headers=headers, timeout=args.timeout)

    spots, summary = build_parking_spot_statuses(
        zone_details,
        end_ms=end_ms,
        include_emails=bool(args.include_emails),
    )

    result = {
        "requested": {
            "office_id": str(office_id),
            "zone_id": zone_id,
            "zone_name": zone_details.get("name"),
            "date": args.date,
            "start_local": args.start_local,
            "end_local": args.end_local,
            "timezone": args.timezone,
            "start_iso": start_iso,
            "end_iso": end_iso,
        },
        "office_resolution": office_resolution,
        "summary": summary,
        "spots": spots,
    }

    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=True))
    else:
        print(f"Workspace: {office_id}")
        if office_resolution.get("selection_reason") != "explicit_office_id":
            print(f"Office-Aufloesung: {office_resolution.get('office_name')} ({office_resolution.get('selection_reason')})")
        print(f"Zone: {zone_details.get('name')} (id={zone_id})")
        print(f"Zeitraum: {start_iso} -> {end_iso}")
        print_parking_status_table(spots, summary)
    return 0


def cmd_discovery(args: argparse.Namespace) -> int:
    load_dotenv(args.env_file, override=False)

    auth_headers = build_auth_headers_from_env()
    require_auth_headers(auth_headers)
    headers = {"Accept": "application/json"}
    headers.update(auth_headers)
    office_id, office_resolution = resolve_office(args.office_id, args.office_name, headers=headers, timeout=args.timeout)

    start_ms, end_ms, start_iso, end_iso = parse_local_range_to_epoch_ms(
        args.date,
        args.start_local,
        args.end_local,
        args.timezone,
    )

    zones = get_workspace_zones(office_id, start_ms, end_ms, headers=headers, timeout=args.timeout)
    if args.zone_type:
        wanted_type = args.zone_type.strip().lower()
        zones = [z for z in zones if str(z.get("type", "")).lower() == wanted_type]

    if args.only_bookable_zones:
        filtered: list[dict[str, Any]] = []
        for zone in zones:
            access_rules = zone.get("accessRules", {}) if isinstance(zone.get("accessRules"), dict) else {}
            if bool(access_rules.get("isBookable", True)) and bool(access_rules.get("userHasAccess", True)):
                filtered.append(zone)
        zones = filtered

    discovery_zones = [build_discovery_zone(zone, end_ms=end_ms, include_emails=bool(args.include_emails)) for zone in zones]
    if args.only_with_items:
        discovery_zones = [zone for zone in discovery_zones if int(zone.get("summary", {}).get("items_total", 0)) > 0]

    resource_types: dict[str, int] = {}
    items_total = 0
    available_total = 0
    occupied_total = 0
    bookable_now_total = 0
    bookings_total = 0

    for zone in discovery_zones:
        zone_type = str(zone.get("zone_type", "unknown"))
        resource_types[zone_type] = resource_types.get(zone_type, 0) + 1
        zsum = zone.get("summary", {})
        items_total += int(zsum.get("items_total", 0))
        available_total += int(zsum.get("available", 0))
        occupied_total += int(zsum.get("occupied", 0))
        bookable_now_total += int(zsum.get("bookable_now", 0))
        for item in zone.get("items", []):
            bookings_total += int(item.get("reserved_by_count", 0))

    discovery = {
        "requested": {
            "office_id": str(office_id),
            "date": args.date,
            "start_local": args.start_local,
            "end_local": args.end_local,
            "timezone": args.timezone,
            "start_iso": start_iso,
            "end_iso": end_iso,
            "zone_type_filter": args.zone_type,
            "only_bookable_zones": bool(args.only_bookable_zones),
            "only_with_items": bool(args.only_with_items),
        },
        "office_resolution": office_resolution,
        "summary": {
            "zones_total": len(discovery_zones),
            "items_total": items_total,
            "available_total": available_total,
            "occupied_total": occupied_total,
            "bookable_now_total": bookable_now_total,
            "active_bookings_total": bookings_total,
        },
        "resource_types": resource_types,
        "zones": discovery_zones,
    }

    if args.format == "json":
        print(json.dumps(discovery, indent=2, ensure_ascii=True))
    else:
        print(f"Office: {office_id}")
        if office_resolution.get("selection_reason") != "explicit_office_id":
            print(f"Office-Aufloesung: {office_resolution.get('office_name')} ({office_resolution.get('selection_reason')})")
        print(f"Zeitraum: {start_iso} -> {end_iso}")
        print_discovery_table(discovery)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Deskbird API Reverse-Engineering und Replay Tool",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_capture = sub.add_parser("capture", help="XHR/fetch Requests im Browser mitschneiden")
    p_capture.add_argument("--start-url", default="https://app.deskbird.com")
    p_capture.add_argument("--domain-filter", default="deskbird.com", help="Nur Hostnames dieser Domain(s), Komma-separiert")
    p_capture.add_argument(
        "--out",
        default=f"output/captures/deskbird_capture_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
    )
    p_capture.add_argument("--duration", type=int, default=0, help="Sekunden, 0 = bis Enter gedrueckt wird")
    p_capture.add_argument("--headless", action="store_true")
    p_capture.add_argument("--slow-mo", type=int, default=0, help="Playwright slow_mo in Millisekunden")
    p_capture.add_argument("--ignore-https-errors", action="store_true")
    p_capture.add_argument("--capture-response-body", action="store_true")
    p_capture.add_argument(
        "--unsafe-keep-secrets",
        action="store_true",
        help="Speichert Auth-/Cookie-Daten unmaskiert (nur lokal und mit Vorsicht nutzen)",
    )
    p_capture.add_argument("--max-body-chars", type=int, default=4000)
    p_capture.set_defaults(func=cmd_capture)

    p_auth_capture = sub.add_parser("auth-capture", help="Interaktiv einloggen und Auth-Daten in .env speichern")
    p_auth_capture.add_argument("--start-url", default="https://app.deskbird.com")
    p_auth_capture.add_argument("--api-domain", default="api.deskbird.com")
    p_auth_capture.add_argument("--env-file", default=".env")
    p_auth_capture.add_argument("--duration", type=int, default=0, help="Sekunden, 0 = bis Enter gedrueckt wird")
    p_auth_capture.add_argument("--headless", action="store_true")
    p_auth_capture.add_argument("--slow-mo", type=int, default=0, help="Playwright slow_mo in Millisekunden")
    p_auth_capture.add_argument("--ignore-https-errors", action="store_true")
    p_auth_capture.add_argument("--print-only", action="store_true", help="Nur anzeigen, nicht in .env speichern")
    p_auth_capture.set_defaults(func=cmd_auth_capture)

    p_auth_check = sub.add_parser("auth-check", help="Prueft, ob die gespeicherte Auth aktuell gueltig ist")
    p_auth_check.add_argument("--env-file", default=".env")
    p_auth_check.add_argument("--timeout", type=int, default=20)
    p_auth_check.add_argument("--format", choices=["table", "json"], default="table")
    p_auth_check.add_argument(
        "--min-valid-minutes",
        type=int,
        default=0,
        help="Wenn >0, gilt Auth als reauth-pflichtig sobald Restgueltigkeit darunter liegt (Exit-Code 10).",
    )
    p_auth_check.set_defaults(func=cmd_auth_check)

    p_auth_import = sub.add_parser(
        "auth-import",
        help="Importiert Authorization/Cookie aus DevTools- oder Telegram-Text nach .env",
    )
    p_auth_import.add_argument("--env-file", default=".env")
    p_auth_import.add_argument("--authorization", help="Kompletter Authorization-Header-Wert")
    p_auth_import.add_argument("--token", help="Rohes Bearer-Token (JWT). 'Bearer ' wird automatisch ergaenzt.")
    p_auth_import.add_argument("--cookie", help="Kompletter Cookie-Header-Wert")
    p_auth_import.add_argument("--x-csrf-token")
    p_auth_import.add_argument("--x-xsrf-token")
    p_auth_import.add_argument("--base-url", help="Optionales Override fuer DESKBIRD_BASE_URL")
    p_auth_import.add_argument("--firebase-api-key", help="Optional: Firebase Web API-Key fuer spaeteres auth-refresh")
    p_auth_import.add_argument("--firebase-refresh-token", help="Optional: Firebase Refresh-Token fuer spaeteres auth-refresh")
    p_auth_import.add_argument("--telegram-text", help="Rohtext aus Telegram/DevTools (Header-Block oder JSON)")
    p_auth_import.add_argument("--from-file", help="Datei mit kopiertem Header-/Token-Text")
    p_auth_import.add_argument("--stdin", action="store_true", help="Rohtext von stdin lesen")
    p_auth_import.add_argument("--format", choices=["table", "json"], default="table")
    p_auth_import.add_argument("--timeout", type=int, default=20)
    p_auth_import.add_argument("--min-valid-minutes", type=int, default=90)
    p_auth_import.add_argument("--no-verify", dest="verify", action="store_false")
    p_auth_import.set_defaults(func=cmd_auth_import, verify=True)

    p_auth_refresh = sub.add_parser(
        "auth-refresh",
        help="Holt per Firebase SecureToken einen frischen Bearer aus Refresh-Token + API-Key",
    )
    p_auth_refresh.add_argument("--env-file", default=".env")
    p_auth_refresh.add_argument("--firebase-api-key", help="Firebase Web API-Key (optional, sonst aus ENV).")
    p_auth_refresh.add_argument("--firebase-refresh-token", help="Firebase Refresh-Token (optional, sonst aus ENV).")
    p_auth_refresh.add_argument("--timeout", type=int, default=20)
    p_auth_refresh.add_argument("--format", choices=["table", "json"], default="table")
    p_auth_refresh.add_argument("--min-valid-minutes", type=int, default=90)
    p_auth_refresh.add_argument("--no-verify", dest="verify", action="store_false")
    p_auth_refresh.set_defaults(func=cmd_auth_refresh, verify=True)

    p_auth_pair_start = sub.add_parser("auth-pair-start", help="Startet einen Pairing-Code fuer reibungslose Reauth via Telegram")
    p_auth_pair_start.add_argument("--store-file", help="Pfad fuer Pairing-Store JSON (default: output/auth_pairings.json)")
    p_auth_pair_start.add_argument("--env-file", default=".env")
    p_auth_pair_start.add_argument("--start-url", default="https://app.deskbird.com")
    p_auth_pair_start.add_argument("--api-domain", default="api.deskbird.com")
    p_auth_pair_start.add_argument("--ttl-minutes", type=int, default=20, help="Gueltigkeit des Pairing-Codes")
    p_auth_pair_start.add_argument("--code-length", type=int, default=6)
    p_auth_pair_start.add_argument("--min-valid-minutes", type=int, default=90)
    p_auth_pair_start.add_argument("--note", help="Optionaler Hinweis fuer den Nutzer/Bot")
    p_auth_pair_start.add_argument("--format", choices=["table", "json"], default="table")
    p_auth_pair_start.set_defaults(func=cmd_auth_pair_start)

    p_auth_pair_status = sub.add_parser("auth-pair-status", help="Status eines Pairing-Codes abfragen")
    p_auth_pair_status.add_argument("--code", required=True)
    p_auth_pair_status.add_argument("--store-file", help="Pfad fuer Pairing-Store JSON (default: output/auth_pairings.json)")
    p_auth_pair_status.add_argument("--format", choices=["table", "json"], default="table")
    p_auth_pair_status.set_defaults(func=cmd_auth_pair_status)

    p_auth_pair_cancel = sub.add_parser("auth-pair-cancel", help="Aktiven Pairing-Code abbrechen")
    p_auth_pair_cancel.add_argument("--code", required=True)
    p_auth_pair_cancel.add_argument("--store-file", help="Pfad fuer Pairing-Store JSON (default: output/auth_pairings.json)")
    p_auth_pair_cancel.add_argument("--format", choices=["table", "json"], default="table")
    p_auth_pair_cancel.set_defaults(func=cmd_auth_pair_cancel)

    p_auth_pair_finish = sub.add_parser("auth-pair-finish", help="Fuehrt den lokalen Browser-Login fuer einen Pairing-Code aus")
    p_auth_pair_finish.add_argument("--code", required=True)
    p_auth_pair_finish.add_argument("--store-file", help="Pfad fuer Pairing-Store JSON (default: output/auth_pairings.json)")
    p_auth_pair_finish.add_argument("--env-file", help="Optionales Override fuer .env Pfad")
    p_auth_pair_finish.add_argument("--start-url", help="Optionales Override fuer Login-URL")
    p_auth_pair_finish.add_argument("--api-domain", help="Optionales Override fuer API-Domain")
    p_auth_pair_finish.add_argument("--timeout", type=int, default=20)
    p_auth_pair_finish.add_argument(
        "--min-valid-minutes",
        type=int,
        default=-1,
        help="Optionales Override fuer Mindestgueltigkeit. -1 = Wert aus Pairing-Session.",
    )
    p_auth_pair_finish.add_argument("--headless", action="store_true")
    p_auth_pair_finish.add_argument("--slow-mo", type=int, default=0, help="Playwright slow_mo in Millisekunden")
    p_auth_pair_finish.add_argument("--ignore-https-errors", action="store_true")
    p_auth_pair_finish.add_argument("--format", choices=["table", "json"], default="table")
    p_auth_pair_finish.set_defaults(func=cmd_auth_pair_finish)

    p_list = sub.add_parser("list", help="Capture-Datei anzeigen")
    p_list.add_argument("--file", required=True)
    p_list.set_defaults(func=cmd_list)

    p_replay = sub.add_parser("replay", help="Einen captured Request erneut senden")
    p_replay.add_argument("--file", required=True)
    p_replay.add_argument("--id", type=int, required=True)
    p_replay.add_argument("--env-file", default=".env")
    p_replay.add_argument("--override-json", help="JSON-Datei als Request-Body statt captured Body")
    p_replay.add_argument("--timeout", type=int, default=30)
    p_replay.add_argument("--max-body-chars", type=int, default=4000)
    p_replay.add_argument("--dry-run", action="store_true")
    p_replay.set_defaults(func=cmd_replay)

    p_probe = sub.add_parser("probe", help="Beliebigen Endpoint direkt testen")
    p_probe.add_argument("--method", default="GET")
    p_probe.add_argument("--url", help="Vollstaendige URL (alternativ zu --path)")
    p_probe.add_argument("--path", default="/", help="Wird mit DESKBIRD_BASE_URL kombiniert")
    p_probe.add_argument("--param", action="append", default=[], help="Query Parameter als key=value")
    p_probe.add_argument("--header", action="append", default=[], help="Header als key=value")
    p_probe.add_argument("--json-file", help="JSON-Datei als Body")
    p_probe.add_argument("--data", help="Raw Body")
    p_probe.add_argument("--env-file", default=".env")
    p_probe.add_argument("--timeout", type=int, default=30)
    p_probe.add_argument("--max-body-chars", type=int, default=4000)
    p_probe.add_argument("--dry-run", action="store_true")
    p_probe.set_defaults(func=cmd_probe)

    default_timezone = os.getenv("DESKBIRD_TIMEZONE", "Europe/Berlin")

    p_discovery = sub.add_parser("discovery", help="Analysiert alle buchbaren Objekte (Desks, Parking, MeetingRooms, ...)")
    p_discovery.add_argument(
        "--office-id",
        help="Workspace/Office ID. Optional; ohne Angabe wird das Office automatisch aufgeloest.",
    )
    p_discovery.add_argument("--office-name", help="Optional: Office per Name auswaehlen (exact/partial).")
    p_discovery.add_argument("--date", required=True, help="Datum im Format YYYY-MM-DD")
    p_discovery.add_argument("--start-local", default="08:30", help="Lokale Startzeit HH:MM")
    p_discovery.add_argument("--end-local", default="19:00", help="Lokale Endzeit HH:MM")
    p_discovery.add_argument("--timezone", default=default_timezone, help="IANA Zeitzone, z.B. Europe/Berlin")
    p_discovery.add_argument("--zone-type", help="Optionaler Filter auf Objekttyp, z.B. parking/flexDesk/meetingRoom")
    p_discovery.add_argument("--only-bookable-zones", action="store_true", help="Nur Zonen mit AccessRules(isBookable && userHasAccess)")
    p_discovery.add_argument("--only-with-items", action="store_true", help="Nur Zonen mit mindestens einem Objekt")
    p_discovery.add_argument("--include-emails", action="store_true", help="E-Mail in Ausgabe aufnehmen")
    p_discovery.add_argument("--format", choices=["table", "json"], default="table")
    p_discovery.add_argument("--env-file", default=".env")
    p_discovery.add_argument("--timeout", type=int, default=30)
    p_discovery.set_defaults(func=cmd_discovery)

    p_parking_check = sub.add_parser("parking-check", help="Freie Parkplaetze fuer einen Zeitraum pruefen")
    p_parking_check.add_argument(
        "--office-id",
        help="Workspace/Office ID. Optional; ohne Angabe wird das Office automatisch aufgeloest.",
    )
    p_parking_check.add_argument("--office-name", help="Optional: Office per Name auswaehlen (exact/partial).")
    p_parking_check.add_argument("--zone-id", help="Optional: nur eine konkrete Parking-Zone pruefen")
    p_parking_check.add_argument("--date", required=True, help="Datum im Format YYYY-MM-DD")
    p_parking_check.add_argument("--start-local", default="08:30", help="Lokale Startzeit HH:MM")
    p_parking_check.add_argument("--end-local", default="19:00", help="Lokale Endzeit HH:MM")
    p_parking_check.add_argument("--timezone", default=default_timezone, help="IANA Zeitzone, z.B. Europe/Berlin")
    p_parking_check.add_argument("--env-file", default=".env")
    p_parking_check.add_argument("--timeout", type=int, default=30)
    p_parking_check.set_defaults(func=cmd_parking_check)

    p_parking_book = sub.add_parser("parking-book-first", help="Ersten freien Parkplatz direkt buchen")
    p_parking_book.add_argument(
        "--office-id",
        help="Workspace/Office ID. Optional; ohne Angabe wird das Office automatisch aufgeloest.",
    )
    p_parking_book.add_argument("--office-name", help="Optional: Office per Name auswaehlen (exact/partial).")
    p_parking_book.add_argument("--zone-id", help="Optional: konkrete Parking-Zone erzwingen")
    p_parking_book.add_argument("--prefer-zone-item-id", help="Optional: bevorzugte Parkplatz-ID")
    p_parking_book.add_argument("--date", required=True, help="Datum im Format YYYY-MM-DD")
    p_parking_book.add_argument("--start-local", default="08:30", help="Lokale Startzeit HH:MM")
    p_parking_book.add_argument("--end-local", default="19:00", help="Lokale Endzeit HH:MM")
    p_parking_book.add_argument("--timezone", default=default_timezone, help="IANA Zeitzone, z.B. Europe/Berlin")
    p_parking_book.add_argument("--is-anonymous", action="store_true")
    p_parking_book.add_argument("--dry-run", action="store_true")
    p_parking_book.add_argument("--env-file", default=".env")
    p_parking_book.add_argument("--timeout", type=int, default=30)
    p_parking_book.set_defaults(func=cmd_parking_book_first)

    p_parking_status = sub.add_parser("parking-status", help="Status pro Parkplatz inkl. Nutzer und Reservierbarkeit")
    p_parking_status.add_argument(
        "--office-id",
        help="Workspace/Office ID. Optional; ohne Angabe wird das Office automatisch aufgeloest.",
    )
    p_parking_status.add_argument("--office-name", help="Optional: Office per Name auswaehlen (exact/partial).")
    p_parking_status.add_argument("--zone-id", help="Optional: konkrete Parking-Zone")
    p_parking_status.add_argument("--zone-name", help="Optional: Zone per Name, z.B. <PARKING_ZONE_NAME>")
    p_parking_status.add_argument("--date", required=True, help="Datum im Format YYYY-MM-DD")
    p_parking_status.add_argument("--start-local", default="08:30", help="Lokale Startzeit HH:MM")
    p_parking_status.add_argument("--end-local", default="19:00", help="Lokale Endzeit HH:MM")
    p_parking_status.add_argument("--timezone", default=default_timezone, help="IANA Zeitzone, z.B. Europe/Berlin")
    p_parking_status.add_argument("--format", choices=["table", "json"], default="table")
    p_parking_status.add_argument("--include-emails", action="store_true", help="E-Mail in Ausgabe aufnehmen")
    p_parking_status.add_argument("--env-file", default=".env")
    p_parking_status.add_argument("--timeout", type=int, default=30)
    p_parking_status.set_defaults(func=cmd_parking_status)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        return int(args.func(args))
    except KeyboardInterrupt:
        print("Abgebrochen.")
        return 130
    except ValueError as exc:
        print(f"Fehler: {exc}")
        return 2
    except requests.RequestException as exc:
        print(f"HTTP-Fehler: {exc}")
        return 3


if __name__ == "__main__":
    sys.exit(main())

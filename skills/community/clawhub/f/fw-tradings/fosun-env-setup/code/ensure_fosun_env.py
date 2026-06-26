"""Generate or repair the shared Fosun OpenAPI credential file.

The only default credential location is the parent `fw-trade-skill/fosun.env`.
`FOSUN_ENV_PATH` may override it; relative values are resolved from
`fw-trade-skill`, not from the caller's current working directory.
"""

from __future__ import annotations

import argparse
import base64
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time
import types
from urllib.parse import quote, urlparse
import uuid
from typing import Any

import requests
import urllib3
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

from credential_scenarios import (
    ACTION_CONTACT_SUPPORT,
    CONTACT_SUPPORT_USER_MESSAGE,
    SCENARIO_RENEW,
    SCENARIO_RESET,
    SCENARIO_SETUP,
    build_open_url,
    operation_guide,
    scenario_fields,
)
from api_key_check import (
    classify_api_key_error_code,
    parse_api_key_check_status,
)
from qr_artifact import apply_qr_delivery

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SETUP_ROOT = Path(__file__).resolve().parent.parent
FW_TRADE_ROOT = SETUP_ROOT.parent
LOCAL_SDK_ROOT = FW_TRADE_ROOT / "openapi-python-sdk-develop-sim-trade"
DEFAULT_ENV_NAME = "fosun.env"
DEFAULT_BASE_URL = "https://openapi.fosunxcz.com"
DEFAULT_SDK_ZIP_FALLBACK_URL = "https://openapi-docs.fosunxcz.com/download/sdk/openapi-python-sdk-1.2.0.zip"
DEFAULT_BACKUP_KEEP_COUNT = 10

API_KEY_STATUS_KEY = "FSOPENAPI_API_KEY_STATUS"
API_KEY_VERIFIED_AT_KEY = "FSOPENAPI_API_KEY_VERIFIED_AT"
TICKET_KEY = "FSOPENAPI_TICKET"
TICKET_STATUS_KEY = "FSOPENAPI_TICKET_STATUS"
TICKET_EXPIRE_TIME_KEY = "FSOPENAPI_TICKET_EXPIRE_TIME"
OPEN_URL_KEY = "FSOPENAPI_OPEN_URL"
MAC_ID_KEY = "FSOPENAPI_MAC_ID"
API_KEY_KEY = "FSOPENAPI_API_KEY"
BASE_URL_KEY = "FSOPENAPI_BASE_URL"
PRIVATE_KEY_KEY = "FSOPENAPI_CLIENT_PRIVATE_KEY"
SERVER_PUBLIC_KEY_KEY = "FSOPENAPI_SERVER_PUBLIC_KEY"
ACCOUNT_INDEX_KEY = "FSOPENAPI_ACCOUNT_INDEX"
BACKUP_DIR_ENV_KEY = "FOSUN_ENV_BACKUP_DIR"
PENDING_STATE_VERSION = 1
_TRANSIENT_AUTH_KEYS = {
    TICKET_KEY,
    TICKET_STATUS_KEY,
    TICKET_EXPIRE_TIME_KEY,
    OPEN_URL_KEY,
    MAC_ID_KEY,
}
_TICKET_BINDING_KEYS = (
    TICKET_KEY,
    TICKET_STATUS_KEY,
    TICKET_EXPIRE_TIME_KEY,
    OPEN_URL_KEY,
)
_KEEP_FOR_FRESH_TICKET = frozenset({PRIVATE_KEY_KEY, MAC_ID_KEY, BASE_URL_KEY})
_CANONICAL_ENV_KEYS = {
    ACCOUNT_INDEX_KEY,
    API_KEY_KEY,
    API_KEY_STATUS_KEY,
    API_KEY_VERIFIED_AT_KEY,
    BASE_URL_KEY,
    PRIVATE_KEY_KEY,
    SERVER_PUBLIC_KEY_KEY,
}

_PEM_WRAPPERS = {
    PRIVATE_KEY_KEY: ("-----BEGIN PRIVATE KEY-----", "-----END PRIVATE KEY-----"),
    SERVER_PUBLIC_KEY_KEY: ("-----BEGIN PUBLIC KEY-----", "-----END PUBLIC KEY-----"),
}
_ACCOUNT_TYPE_LABELS = {
    0: "real_stock",
    1: "real_option",
    2: "mock",
}

def shared_env_path() -> Path:
    """Resolve the shared env path from the setup module location."""
    raw = (os.environ.get("FOSUN_ENV_PATH") or DEFAULT_ENV_NAME).strip()
    path = Path(os.path.expandvars(os.path.expanduser(raw)))
    if not path.is_absolute():
        path = FW_TRADE_ROOT / path
    return path.resolve()


def _parse_env_file(text: str) -> dict[str, str]:
    entries: dict[str, str] = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith("#"):
            i += 1
            continue
        key, sep, value = line.partition("=")
        if not sep:
            i += 1
            continue
        key = key.strip()
        value = value.strip()
        if value.startswith("-----BEGIN "):
            pem_lines = [value]
            i += 1
            while i < len(lines):
                pem_line = lines[i].rstrip()
                pem_lines.append(pem_line)
                if pem_line.strip().startswith("-----END "):
                    i += 1
                    break
                i += 1
            value = "\n".join(pem_lines)
        elif value.startswith('"') and not value.endswith('"'):
            parts = [value[1:]]
            i += 1
            while i < len(lines):
                part = lines[i]
                if part.endswith('"'):
                    parts.append(part[:-1])
                    i += 1
                    break
                parts.append(part)
                i += 1
            value = "\n".join(parts)
        else:
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            i += 1
        if key:
            entries[key] = value
    return entries


def _ensure_pem(key_name: str, value: Any) -> str:
    value = str(value or "").strip()
    if not value or value.startswith("-----BEGIN "):
        return value
    wrapper = _PEM_WRAPPERS.get(key_name)
    if not wrapper:
        return value
    try:
        decoded = base64.b64decode(value).decode("utf-8")
        if decoded.strip().startswith("-----BEGIN "):
            return decoded.strip()
    except Exception:  # noqa: BLE001
        pass
    begin, end = wrapper
    raw = value.replace("\n", "").replace("\r", "").replace(" ", "")
    lines = [raw[i:i + 64] for i in range(0, len(raw), 64)]
    return begin + "\n" + "\n".join(lines) + "\n" + end


def _encode_env_value(key: str, value: Any) -> str:
    if value is None:
        return ""
    value = str(value).strip()
    if key in _PEM_WRAPPERS and value.startswith("-----BEGIN "):
        return base64.b64encode(value.encode("utf-8")).decode("utf-8")
    return value


def load_env_entries(env_path: Path | None = None) -> dict[str, str]:
    target = env_path or shared_env_path()
    if not target.is_file():
        return {}
    return _parse_env_file(target.read_text(encoding="utf-8"))


def _pending_state_path(env_path: Path) -> Path:
    return env_path.with_name(f".{env_path.name}.pending.json")


def _read_pending_document(env_path: Path) -> dict[str, Any]:
    state_path = _pending_state_path(env_path)
    if not state_path.is_file():
        return {}
    try:
        payload = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _load_pending_state(env_path: Path) -> dict[str, Any]:
    payload = _read_pending_document(env_path)
    entries = payload.get("entries")
    if not isinstance(entries, dict):
        return {}
    result = {str(key): value for key, value in entries.items()}
    if result.get(API_KEY_KEY):
        cleaned = _sanitize_api_key(result[API_KEY_KEY])
        if cleaned:
            result[API_KEY_KEY] = cleaned
        else:
            result.pop(API_KEY_KEY, None)
    return result


_PENDING_CREDENTIAL_KEYS = (
    BASE_URL_KEY,
    PRIVATE_KEY_KEY,
    SERVER_PUBLIC_KEY_KEY,
)


def _merge_pending_credentials_into_entries(
    entries: dict[str, Any],
    env_path: Path,
    *,
    user_api_key: str | None = None,
    overwrite_from_pending: bool = False,
) -> bool:
    """将 pending 中的密钥材料合并进 entries；用户回填的 apikey 优先于 pending。"""
    pending_entries = _load_pending_state(env_path)
    if not pending_entries:
        return False
    for key in _PENDING_CREDENTIAL_KEYS:
        value = pending_entries.get(key)
        if not value:
            continue
        if overwrite_from_pending or not str(entries.get(key, "") or "").strip():
            entries[key] = value
    if user_api_key:
        entries[API_KEY_KEY] = str(user_api_key).strip()
        entries[API_KEY_STATUS_KEY] = "unknown"
        entries[API_KEY_VERIFIED_AT_KEY] = ""
    return True


def _save_pending_state(
    entries: dict[str, Any],
    env_path: Path,
    *,
    ticket: str,
    open_url: str,
    expire_time: str,
    credential_scenario: str = SCENARIO_SETUP,
) -> None:
    state_path = _pending_state_path(env_path)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    pending_entries = {
        BASE_URL_KEY: entries.get(BASE_URL_KEY),
        PRIVATE_KEY_KEY: _ensure_pem(PRIVATE_KEY_KEY, entries.get(PRIVATE_KEY_KEY)),
        API_KEY_KEY: entries.get(API_KEY_KEY),
        SERVER_PUBLIC_KEY_KEY: _ensure_pem(
            SERVER_PUBLIC_KEY_KEY,
            entries.get(SERVER_PUBLIC_KEY_KEY),
        ),
        API_KEY_STATUS_KEY: "pending",
        API_KEY_VERIFIED_AT_KEY: "",
        TICKET_KEY: ticket,
        TICKET_STATUS_KEY: entries.get(TICKET_STATUS_KEY, "active"),
        OPEN_URL_KEY: open_url,
        TICKET_EXPIRE_TIME_KEY: expire_time,
        MAC_ID_KEY: entries.get(MAC_ID_KEY),
    }
    payload = {
        "version": PENDING_STATE_VERSION,
        "createdAt": _now_ts(),
        "credential_scenario": credential_scenario,
        "entries": pending_entries,
    }
    state_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        state_path.chmod(0o600)
    except OSError:
        pass


def _delete_pending_state(env_path: Path) -> None:
    try:
        _pending_state_path(env_path).unlink()
    except FileNotFoundError:
        pass


def _write_api_key_to_pending(env_path: Path, api_key: str) -> bool:
    """用户回填 apikey 时写入 pending，与 fosun.env 保持同一 API Key。"""
    state_path = _pending_state_path(env_path)
    if not state_path.is_file():
        return False
    pending_doc = _read_pending_document(env_path)
    pending_entries = pending_doc.get("entries")
    if not isinstance(pending_entries, dict):
        return False
    pending_entries[API_KEY_KEY] = api_key
    pending_entries[API_KEY_STATUS_KEY] = "unknown"
    pending_entries[API_KEY_VERIFIED_AT_KEY] = ""
    pending_doc["entries"] = pending_entries
    state_path.write_text(
        json.dumps(pending_doc, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    try:
        state_path.chmod(0o600)
    except OSError:
        pass
    return True


def _apply_user_api_key_backfill(
    env_path: Path,
    api_key: str,
    *,
    server_public_key: str,
) -> tuple[dict[str, Any], bool]:
    """用户回填：必须同时提供页面 apikey 与服务端公钥，并晋升本次 ticket 的客户端私钥。"""
    server_pem = _ensure_pem(
        SERVER_PUBLIC_KEY_KEY,
        str(server_public_key or "").strip(),
    )
    if not server_pem:
        raise ValueError(
            "回填已开通账号凭据时必须同时提供页面上的服务端公钥（--server-public-key）。"
            "页面展示的服务端公钥与 TicketCreate 临时返回的不同，仅提供 apikey 无法完成对接。"
        )
    entries = load_env_entries(env_path)
    promoted_from_pending = _merge_pending_credentials_into_entries(
        entries,
        env_path,
        user_api_key=api_key,
        overwrite_from_pending=True,
    )
    entries[SERVER_PUBLIC_KEY_KEY] = server_pem
    if not _has_complete_key_material(entries):
        raise RuntimeError(
            "缺少 pending 中的客户端私钥或无法解析的服务端公钥，无法完成凭据写入。"
            "请先运行 ensure_fosun_env.py 签发开通二维码，用户在页面上完成重置后，"
            "同时回填 API Key 与页面服务端公钥。"
        )
    _drop_transient_auth_entries(entries)
    save_env_entries(entries, env_path)
    if not _write_api_key_to_pending(env_path, api_key):
        raise RuntimeError(
            "无法写入 pending：缺少 .fosun.env.pending.json 或文件内容无效。"
            "请先运行 ensure_fosun_env.py 签发开通二维码后再回填 API Key。"
        )
    return entries, promoted_from_pending


def _canonicalize_env_entries(entries: dict[str, Any]) -> dict[str, Any]:
    canonical = {key: entries.get(key) for key in _CANONICAL_ENV_KEYS if key in entries}
    canonical.setdefault(BASE_URL_KEY, DEFAULT_BASE_URL)
    canonical.setdefault(API_KEY_STATUS_KEY, "unknown")
    canonical.setdefault(API_KEY_VERIFIED_AT_KEY, "")
    return canonical


def save_env_entries(entries: dict[str, Any], env_path: Path | None = None) -> None:
    target = env_path or shared_env_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    entries = _canonicalize_env_entries(entries)
    serialized = {
        key: _encode_env_value(key, value)
        for key, value in entries.items()
        if value is not None
    }
    # 临时文件 + os.replace 原子落盘，避免写入中断把 fosun.env 截断成半成品。
    tmp_path = target.with_name(f".{target.name}.tmp.{os.getpid()}")
    try:
        with tmp_path.open("w", encoding="utf-8") as f:
            for key in sorted(serialized.keys()):
                f.write(f"{key}={serialized[key]}\n")
        os.replace(tmp_path, target)
    finally:
        try:
            tmp_path.unlink()
        except FileNotFoundError:
            pass


def credential_backup_dir() -> Path:
    """Resolve a skill-independent backup directory using each OS's user data location."""
    raw = (os.environ.get(BACKUP_DIR_ENV_KEY) or "").strip()
    if raw:
        path = Path(os.path.expandvars(os.path.expanduser(raw)))
    elif os.name == "nt":
        base = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
        path = Path(base) / "fw-trade-skill" / "fosun-env-backups"
    elif sys.platform == "darwin":
        path = Path.home() / "Library" / "Application Support" / "fw-trade-skill" / "fosun-env-backups"
    else:
        base = os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local" / "share")
        path = Path(base) / "fw-trade-skill" / "fosun-env-backups"
    if not path.is_absolute():
        path = Path.home() / path
    return path.resolve()


def _backup_file_stem(entries: dict[str, Any]) -> str:
    base_url = str(entries.get(BASE_URL_KEY) or DEFAULT_BASE_URL).strip().rstrip("/")
    api_key = _sanitize_api_key(entries.get(API_KEY_KEY))
    digest = hashlib.sha256(f"{base_url}\n{api_key}".encode("utf-8")).hexdigest()[:12]
    api_tail = api_key[-8:] if api_key else "noapikey"
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"fosun-{digest}-{api_tail}-{timestamp}"


def _prune_credential_backups(backup_dir: Path) -> None:
    backups = sorted(
        backup_dir.glob("fosun-*.env"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    for stale in backups[DEFAULT_BACKUP_KEEP_COUNT:]:
        try:
            stale.unlink()
        except OSError:
            pass


def _persist_credential_backup(entries: dict[str, Any]) -> Path | None:
    """Write a second copy outside the skill tree so deleting the skill keeps the key material."""
    if str(entries.get(API_KEY_STATUS_KEY, "")).strip().lower() != "valid":
        return None
    if not _sanitize_api_key(entries.get(API_KEY_KEY)) or not _has_complete_key_material(entries):
        return None

    backup_dir = credential_backup_dir()
    backup_dir.mkdir(parents=True, exist_ok=True)
    try:
        backup_dir.chmod(0o700)
    except OSError:
        pass

    backup_path = backup_dir / f"{_backup_file_stem(entries)}.env"
    save_env_entries(entries, backup_path)
    try:
        backup_path.chmod(0o600)
    except OSError:
        pass
    _prune_credential_backups(backup_dir)
    return backup_path


def _restore_candidate_paths() -> list[Path]:
    backup_dir = credential_backup_dir()
    if not backup_dir.is_dir():
        return []
    return sorted(
        backup_dir.glob("fosun-*.env"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )


def _drop_transient_auth_entries(entries: dict[str, Any]) -> None:
    """Best-effort cleanup for legacy env files that still contain auth transient keys."""
    for key in _TRANSIENT_AUTH_KEYS:
        entries.pop(key, None)


def _drop_bound_credential_entries(entries: dict[str, Any]) -> None:
    """Start a new web authorization without mixing old key material into the result."""
    for key in (
        ACCOUNT_INDEX_KEY,
        API_KEY_KEY,
        API_KEY_STATUS_KEY,
        API_KEY_VERIFIED_AT_KEY,
        SERVER_PUBLIC_KEY_KEY,
    ):
        entries.pop(key, None)


def _trim_pending_for_fresh_ticket(
    pending_entries: dict[str, Any] | None,
) -> dict[str, Any]:
    """保留签发新 ticket 所需的设备/密钥材料，丢弃旧 ticket 绑定。"""
    if not pending_entries:
        return {}
    return {
        key: value
        for key, value in pending_entries.items()
        if key in _KEEP_FOR_FRESH_TICKET
    }


def _discard_stale_ticket_binding(entries: dict[str, Any]) -> None:
    """丢弃本地缓存的旧 ticket/open_url，避免对接时复用过期链接。"""
    for key in _TICKET_BINDING_KEYS:
        entries.pop(key, None)


def _reset_pending_and_ticket(
    entries: dict[str, Any],
    pending_entries: dict[str, Any] | None,
) -> dict[str, Any]:
    """旧 ticket 不可复用：丢弃 ticket 绑定，仅保留签发新 ticket 所需的设备/密钥材料。"""
    _discard_stale_ticket_binding(entries)
    return _trim_pending_for_fresh_ticket(pending_entries)


def _mark_invalid_and_save(entries: dict[str, Any], env_path: Path) -> None:
    """凭据校验失败：标记 invalid 并落盘，供后续路由到重置。"""
    entries[API_KEY_STATUS_KEY] = "invalid"
    save_env_entries(entries, env_path)


def _generate_device_id(entries: dict[str, Any]) -> str:
    device_id = str(entries.get(MAC_ID_KEY, "")).strip()
    if not device_id:
        device_id = uuid.uuid4().hex
        entries[MAC_ID_KEY] = device_id
    return device_id


def _generate_client_key_pair() -> tuple[str, str]:
    private_key = ec.generate_private_key(ec.SECP384R1())
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8").strip()
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("utf-8").strip()
    return private_pem, public_pem


def _derive_public_key(private_key_pem: str) -> str:
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode("utf-8"),
        password=None,
    )
    public_key = private_key.public_key()
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("utf-8").strip()


def _rotate_client_key_pair(entries: dict[str, Any]) -> str:
    private_key, _ = _generate_client_key_pair()
    entries[PRIVATE_KEY_KEY] = private_key
    entries[API_KEY_STATUS_KEY] = "unknown"
    entries[API_KEY_VERIFIED_AT_KEY] = ""
    return private_key


def _ensure_client_key_pair(entries: dict[str, Any]) -> tuple[bool, str]:
    private_key = _ensure_pem(PRIVATE_KEY_KEY, entries.get(PRIVATE_KEY_KEY))
    if private_key:
        entries[PRIVATE_KEY_KEY] = private_key
        return False, private_key
    private_key, _ = _generate_client_key_pair()
    entries[PRIVATE_KEY_KEY] = private_key
    entries[API_KEY_STATUS_KEY] = "unknown"
    return True, private_key


def _has_complete_key_material(entries: dict[str, Any]) -> bool:
    """Both identity keys must be parseable PEMs before an API key can be used."""
    private_key = _ensure_pem(PRIVATE_KEY_KEY, entries.get(PRIVATE_KEY_KEY))
    server_public_key = _ensure_pem(SERVER_PUBLIC_KEY_KEY, entries.get(SERVER_PUBLIC_KEY_KEY))
    if not private_key or not server_public_key:
        return False
    try:
        serialization.load_pem_private_key(private_key.encode("utf-8"), password=None)
        serialization.load_pem_public_key(server_public_key.encode("utf-8"))
    except Exception:  # noqa: BLE001
        return False
    entries[PRIVATE_KEY_KEY] = private_key
    entries[SERVER_PUBLIC_KEY_KEY] = server_public_key
    return True


def _now_ts() -> int:
    return int(datetime.now().timestamp())


def _format_expire_time(expire_time: Any) -> str:
    try:
        ts = int(expire_time)
    except (TypeError, ValueError):
        return "未知"
    if ts <= 0:
        return "未知"
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def _extract_ticket_from_url(open_url: Any) -> str:
    raw = str(open_url or "").strip()
    marker = "ticket="
    if marker not in raw:
        return ""
    return raw.split(marker, 1)[1].split("&", 1)[0].strip()


def _append_ticket_to_url(url: str, ticket: str) -> str:
    quoted = quote(ticket, safe="")
    if "#" in url:
        base, fragment = url.split("#", 1)
        if "?" in fragment:
            return f"{base}#{fragment}&ticket={quoted}"
        return f"{base}#{fragment}?ticket={quoted}"
    if "?" in url:
        return f"{url}&ticket={quoted}"
    return f"{url}?ticket={quoted}"


def _authority_open_url(open_url: Any, ticket: Any = "") -> str:
    """优先使用 TicketCreate 返回的开通页 url，不再本地拼固定开通页域名。"""
    url = str(open_url or "").strip()
    ticket_value = str(ticket or "").strip() or _extract_ticket_from_url(url)

    if url.startswith(("http://", "https://")):
        if ticket_value and "ticket=" not in url:
            url = _append_ticket_to_url(url, ticket_value)
        return url

    if ticket_value:
        raise RuntimeError(
            "TicketCreate 返回缺少开通页 url，无法生成授权链接；"
            "请确认 OpenAPI 网关与 TicketCreate 响应正常。"
        )
    return ""


def _assert_authority_open_url(open_url: str) -> str:
    url = str(open_url or "").strip()
    if not url.startswith(("http://", "https://")):
        raise RuntimeError(f"OpenAPI 授权链接格式异常：{url!r}")
    if not _extract_ticket_from_url(url):
        raise RuntimeError(f"OpenAPI 授权链接缺少 ticket 参数：{url!r}")
    return url


def _authority_host_from_url(open_url: str) -> str:
    return urlparse(str(open_url or "").strip()).netloc


def _auth_headers() -> dict[str, str]:
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Request-Id": str(uuid.uuid4()),
    }


class OpenApiResponseError(RuntimeError):
    """认证接口业务错误，保留 code 供上层状态机分派。"""

    def __init__(self, message: str, *, code: Any = None, response: Any = None) -> None:
        super().__init__(message)
        self.code = code
        self.response = response


def _extract_response_data(body: Any) -> dict[str, Any]:
    if not isinstance(body, dict):
        raise RuntimeError(f"认证接口返回格式不正确: {body!r}")
    code = body.get("code")
    if code not in (None, 0):
        message = body.get("message") or "认证接口调用失败"
        raise OpenApiResponseError(
            f"{message} (code={code})",
            code=code,
            response=body,
        )
    content = body.get("content")
    if isinstance(content, dict):
        data = content.get("data")
        if isinstance(data, dict):
            return data
        return content
    data = body.get("data")
    if isinstance(data, dict):
        return data
    return body


def _post_auth_json(base_url: str, path: str, payload: dict[str, Any]) -> dict[str, Any]:
    url = f"{base_url.rstrip('/')}{path}"
    response = requests.post(
        url,
        json=payload,
        headers=_auth_headers(),
        timeout=15,
        verify=False,
    )
    response.raise_for_status()
    return _extract_response_data(response.json())


def _validate_api_key(base_url: str, api_key: str) -> tuple[str, dict[str, Any]]:
    try:
        data = _post_auth_json(
            base_url,
            "/api/v1/auth/APIKeyCheck",
            {"apiKey": api_key},
        )
    except OpenApiResponseError as exc:
        status = classify_api_key_error_code(exc.code)
        if status:
            return status, {}
        raise
    if not isinstance(data, dict):
        return parse_api_key_check_status(data), {}
    return parse_api_key_check_status(data), data


def _coerce_sub_account_id(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _normalize_account_index(payload: Any) -> dict[str, Any]:
    sub_accounts = (((payload or {}).get("data") or {}).get("subAccounts")) or []
    bucket: dict[str, list[dict[str, Any]]] = {
        label: [] for label in _ACCOUNT_TYPE_LABELS.values()
    }
    for sub in sub_accounts:
        if not isinstance(sub, dict):
            continue
        sub_type = sub.get("subAccountType")
        label = _ACCOUNT_TYPE_LABELS.get(sub_type)
        if not label:
            continue
        bucket[label].append({
            "subAccountId": _coerce_sub_account_id(sub.get("subAccountId")),
            "subAccountType": sub_type,
            "chineseName": sub.get("chineseName"),
            "englishName": sub.get("englishName"),
            "status": sub.get("status"),
        })
    return {"refreshedAt": int(time.time()), **bucket}


def _refresh_account_index(entries: dict[str, Any], base_url: str, api_key: str) -> dict[str, Any]:
    """Use the signed SDK request once so a valid env is immediately usable."""
    sdk_package_root = LOCAL_SDK_ROOT / "fsopenapi"
    if LOCAL_SDK_ROOT.is_dir() and str(LOCAL_SDK_ROOT) not in sys.path:
        sys.path.insert(0, str(LOCAL_SDK_ROOT))
    if sdk_package_root.is_dir():
        package = sys.modules.get("fsopenapi")
        if package is None or not hasattr(package, "__path__"):
            package = types.ModuleType("fsopenapi")
            package.__path__ = [str(sdk_package_root)]  # type: ignore[attr-defined]
            sys.modules["fsopenapi"] = package

    os.environ[BASE_URL_KEY] = base_url
    os.environ[API_KEY_KEY] = api_key
    os.environ[PRIVATE_KEY_KEY] = _ensure_pem(PRIVATE_KEY_KEY, entries.get(PRIVATE_KEY_KEY))
    os.environ[SERVER_PUBLIC_KEY_KEY] = _ensure_pem(
        SERVER_PUBLIC_KEY_KEY,
        entries.get(SERVER_PUBLIC_KEY_KEY),
    )

    from fsopenapi.api.account import AccountAPI  # type: ignore[import-not-found]
    from fsopenapi.client import OpenAPIClient  # type: ignore[import-not-found]

    client = OpenAPIClient(base_url, api_key)
    account_api = AccountAPI(client)
    index = _normalize_account_index(account_api.list_accounts())
    entries[ACCOUNT_INDEX_KEY] = json.dumps(index, ensure_ascii=False)
    return index


def _is_auth_material_error(exc: Exception) -> bool:
    message = str(exc)
    return (
        type(exc).__name__ in {"AuthenticationError", "ValueError"}
        or "Handshake signature verification failed" in message
        or "Missing FSOPENAPI_CLIENT_PRIVATE_KEY" in message
        or "Missing FSOPENAPI_SERVER_PUBLIC_KEY" in message
        or "Invalid server signature" in message
    )


def _api_key_error_code(exc: Exception) -> int | None:
    code = getattr(exc, "code", None)
    try:
        return int(code)
    except (TypeError, ValueError):
        return None


def _mark_api_key_status(entries: dict[str, Any], status: str) -> None:
    entries[API_KEY_STATUS_KEY] = status
    if status == "valid":
        entries[API_KEY_VERIFIED_AT_KEY] = str(_now_ts())
    else:
        entries[API_KEY_VERIFIED_AT_KEY] = ""


def _contact_support_payload(env_path: Path, *, message: str = "") -> dict[str, Any]:
    return {
        "ok": False,
        "status": "blocked",
        "env_path": str(env_path),
        "error_code": "OPENAPI_ACCOUNT_CONTACT_SUPPORT",
        "account_action": ACTION_CONTACT_SUPPORT,
        "user_message": message or CONTACT_SUPPORT_USER_MESSAGE,
        "hint": "apikey 已被禁用或撤销，须联系星财富客服，不要签发 TicketCreate 二维码。",
        "next_action": "告知用户联系星财富客服，不要生成二维码。",
    }


def _credential_recovery_payload(
    entries: dict[str, Any],
    env_path: Path,
) -> dict[str, Any] | None:
    """凭据过期续期或禁用联系客服；返回 None 表示继续走重置/开通。"""
    status = str(entries.get(API_KEY_STATUS_KEY, "") or "").strip().lower()
    if status not in {"expired", "disabled"}:
        return None
    save_env_entries(entries, env_path)
    if status == "disabled":
        return _contact_support_payload(env_path)
    payload = issue_credential_ticket(scenario=SCENARIO_RENEW, created=True)
    payload["api_key_check_status"] = "expired"
    payload["renew_trigger"] = "api_key_check"
    return payload


def _valid_payload(
    entries: dict[str, Any],
    env_path: Path,
    next_action: str,
) -> dict[str, Any]:
    account_index = {}
    try:
        account_index = json.loads(str(entries.get(ACCOUNT_INDEX_KEY) or "{}"))
    except ValueError:
        account_index = {}
    return {
        "ok": True,
        "status": "valid",
        "env_path": str(env_path),
        "accounts_summary": {
            "real_stock": len(account_index.get("real_stock") or []),
            "real_option": len(account_index.get("real_option") or []),
            "mock": len(account_index.get("mock") or []),
        },
        "next_action": next_action,
    }


def _finalize_valid_credentials(
    entries: dict[str, Any],
    env_path: Path,
    base_url: str,
    next_action: str,
) -> dict[str, Any] | None:
    api_key = str(entries.get(API_KEY_KEY, "") or "").strip()
    if not api_key or not _has_complete_key_material(entries):
        return None

    check_status = "unknown"
    check_data: dict[str, Any] = {}
    try:
        check_status, check_data = _validate_api_key(base_url, api_key)
        if check_status in {"expired", "disabled"}:
            _mark_api_key_status(entries, check_status)
            save_env_entries(entries, env_path)
            return None

        # invalid/unknown 仍尝试签名业务请求（部分环境 APIKeyCheck 假阴性）；过期/禁用不再刷新。
        _mark_api_key_status(entries, "unknown")
        _refresh_account_index(entries, base_url, api_key)
    except Exception as exc:  # noqa: BLE001
        error_status = classify_api_key_error_code(_api_key_error_code(exc))
        if error_status in {"expired", "disabled", "invalid"}:
            _mark_api_key_status(entries, error_status)
            save_env_entries(entries, env_path)
            return None
        if _is_auth_material_error(exc):
            _mark_api_key_status(entries, "invalid")
            save_env_entries(entries, env_path)
            return None
        raise

    _mark_api_key_status(entries, "valid")
    _drop_transient_auth_entries(entries)
    save_env_entries(entries, env_path)
    payload = _valid_payload(entries, env_path, next_action)
    payload["api_key_check_status"] = check_status
    if isinstance(check_data.get("expiresAt"), (int, float)) and check_data.get("expiresAt"):
        payload["api_key_expires_at"] = int(check_data["expiresAt"])
    backup_path = _persist_credential_backup(entries)
    if backup_path:
        payload["backup_path"] = str(backup_path)
        payload["backup_dir"] = str(backup_path.parent)
    return payload


def _restore_valid_credentials_from_backup(
    env_path: Path,
    base_url: str,
) -> dict[str, Any] | None:
    for backup_path in _restore_candidate_paths():
        candidate = load_env_entries(backup_path)
        if not candidate:
            continue
        _drop_transient_auth_entries(candidate)
        if not candidate.get(BASE_URL_KEY):
            candidate[BASE_URL_KEY] = base_url
        resolved_base_url = str(candidate.get(BASE_URL_KEY) or base_url).rstrip("/")
        candidate[BASE_URL_KEY] = resolved_base_url
        restored = _finalize_valid_credentials(
            candidate,
            env_path,
            resolved_base_url,
            "已从用户级本地备份自动恢复 fosun.env，并刷新账户索引，可继续后续业务。",
        )
        if restored:
            restored["restored_from_backup"] = str(backup_path)
            restored.setdefault("backup_dir", str(backup_path.parent))
            return restored
    return None


def _has_api_key_and_complete_material(entries: dict[str, Any]) -> bool:
    return bool(str(entries.get(API_KEY_KEY, "") or "").strip()) and _has_complete_key_material(entries)


def _try_finalize_pending_authority(
    entries: dict[str, Any],
    env_path: Path,
    base_url: str,
) -> dict[str, Any] | None:
    """用户完成页面开通后再次运行时，尝试一次 finalize；不做轮询。"""
    api_key = str(entries.get(API_KEY_KEY, "") or "").strip()
    if not api_key or not _has_complete_key_material(entries):
        return None
    finalized = _finalize_valid_credentials(
        entries,
        env_path,
        base_url,
        "网页授权完成，API Key、本地私钥、服务端公钥和账户索引已写入共享凭证，可继续后续业务。",
    )
    if finalized:
        _delete_pending_state(env_path)
    return finalized


def _sanitize_api_key(value: Any) -> str:
    raw = str(value or "")
    match = re.search(r"ak_[A-Za-z0-9_\-=]{20,}", raw)
    return match.group(0) if match else ""


def _merge_ticket_create_material(entries: dict[str, Any], data: dict[str, Any]) -> None:
    """合并 TicketCreate 响应中的 apiKey / serverPubKey。"""
    api_key = _sanitize_api_key(data.get("apiKey"))
    server_public_key = str(
        data.get("serverPubKey")
        or data.get("serverPublicKey")
        or ""
    ).strip()
    if api_key:
        entries[API_KEY_KEY] = api_key
    if server_public_key:
        entries[SERVER_PUBLIC_KEY_KEY] = server_public_key


def _pending_payload(
    env_path: Path,
    *,
    created: bool,
    open_url: str,
    ticket_expire_time: str,
    scenario: str = SCENARIO_SETUP,
) -> dict[str, Any]:
    open_url = _assert_authority_open_url(open_url.strip())
    if scenario == SCENARIO_RENEW:
        open_url = build_open_url(open_url, is_expired=True)
    elif scenario in {SCENARIO_SETUP, SCENARIO_RESET}:
        open_url = build_open_url(open_url, is_expired=False)

    meta = scenario_fields(scenario)
    payload: dict[str, Any] = {
        "ok": True,
        "status": "pending",
        "env_path": str(env_path),
        "created_new_ticket": created,
        "open_url": open_url,
        "exact_open_url": open_url,
        "authority_host": _authority_host_from_url(open_url),
        "delivery_mode": "remote",
        "operation_guide": operation_guide(scenario),
        "url_copy_rule": (
            "必须把 exact_open_url/open_url 字段值逐字符原样发给用户；"
            "禁止手打、改写或重拼域名。"
        ),
        "ticket_expire_time": ticket_expire_time,
        "ticket_expire_time_text": _format_expire_time(ticket_expire_time),
        **meta,
    }
    return apply_qr_delivery(payload, open_url)


def _create_ticket(
    entries: dict[str, Any],
    env_path: Path,
    base_url: str,
    private_key_pem: str,
    *,
    scenario: str = SCENARIO_SETUP,
) -> dict[str, Any]:
    _drop_bound_credential_entries(entries)
    if scenario == SCENARIO_RESET:
        private_key_pem = _rotate_client_key_pair(entries)

    payload = {
        "macId": str(entries.get(MAC_ID_KEY, "")).strip(),
        "clientPubKey": _derive_public_key(private_key_pem),
    }
    data = _post_auth_json(base_url, "/api/v1/auth/TicketCreate", payload)

    _merge_ticket_create_material(entries, data)
    ticket = str(data.get("ticket", "")).strip()
    open_url = _authority_open_url(data.get("url"), ticket)
    expire_time = str(data.get("expireTime", "0") or "0")

    if not all([ticket, open_url]):
        raise RuntimeError("TicketCreate 返回缺少必要字段，无法写入本地凭证。")

    entries[TICKET_KEY] = ticket
    entries[TICKET_STATUS_KEY] = "active"
    entries[TICKET_EXPIRE_TIME_KEY] = expire_time
    entries[OPEN_URL_KEY] = open_url
    _save_pending_state(
        entries,
        env_path,
        ticket=ticket,
        open_url=open_url,
        expire_time=expire_time,
        credential_scenario=scenario,
    )
    return _pending_payload(
        env_path,
        created=True,
        open_url=open_url,
        ticket_expire_time=expire_time,
        scenario=scenario,
    )


def ensure_fosun_env(
    *,
    repair_existing: bool = False,
    force_new_ticket: bool = False,
    api_key: str | None = None,
    server_public_key: str | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    env_path = shared_env_path()
    entries = load_env_entries(env_path)
    _drop_transient_auth_entries(entries)
    initial_base_url = str(base_url or entries.get(BASE_URL_KEY) or DEFAULT_BASE_URL).rstrip("/")
    if (
        not force_new_ticket
        and not api_key
        and not server_public_key
        and (not entries or not _has_api_key_and_complete_material(entries))
    ):
        restored = _restore_valid_credentials_from_backup(env_path, initial_base_url)
        if restored:
            return restored
        # 恢复未成功，但其 finalize 可能已把过期/无效状态写回 env；
        # 重读以便后续状态机据实路由（过期→续期、禁用→客服），而非沿用栈上旧空值。
        entries = load_env_entries(env_path)
        _drop_transient_auth_entries(entries)

    pending_entries = _load_pending_state(env_path)
    if force_new_ticket:
        # force-new-ticket 跳过 finalize，直接丢弃旧 ticket 绑定；
        # 仍保留 privKey/mac_id，避免 clientPubKey 与 ticket 错配。
        pending_entries = _reset_pending_and_ticket(entries, pending_entries)
    if pending_entries:
        for key, value in pending_entries.items():
            if not entries.get(key):
                entries[key] = value
    _generate_device_id(entries)
    key_created, private_key_pem = _ensure_client_key_pair(entries)

    if not entries.get(BASE_URL_KEY):
        entries[BASE_URL_KEY] = DEFAULT_BASE_URL
    if base_url:
        entries[BASE_URL_KEY] = str(base_url).strip().rstrip("/")
    resolved_base_url = str(entries.get(BASE_URL_KEY) or DEFAULT_BASE_URL).rstrip("/")
    entries[BASE_URL_KEY] = resolved_base_url

    if api_key:
        entries[API_KEY_KEY] = api_key.strip()
        entries[API_KEY_STATUS_KEY] = "unknown"
    if server_public_key:
        entries[SERVER_PUBLIC_KEY_KEY] = server_public_key.strip()

    api_key_value = str(entries.get(API_KEY_KEY, "")).strip()
    api_key_status = str(
        entries.get(API_KEY_STATUS_KEY, "unknown") or "unknown"
    ).strip().lower()
    has_complete_key_material = _has_complete_key_material(entries)

    if (
        api_key_value
        and api_key_status == "valid"
        and has_complete_key_material
        and not force_new_ticket
        and not repair_existing
    ):
        if entries.get(ACCOUNT_INDEX_KEY):
            _drop_transient_auth_entries(entries)
            save_env_entries(entries, env_path)
            backup_path = _persist_credential_backup(entries)
            _delete_pending_state(env_path)
            payload = _valid_payload(entries, env_path, "共享凭证已标记有效，可继续后续业务。")
            if backup_path:
                payload["backup_path"] = str(backup_path)
                payload["backup_dir"] = str(backup_path.parent)
            return payload
        finalized = _finalize_valid_credentials(
            entries,
            env_path,
            resolved_base_url,
            "共享凭证已标记有效，并已刷新账户索引，可继续后续业务。",
        )
        if finalized:
            _delete_pending_state(env_path)
            return finalized
        recovery = _credential_recovery_payload(entries, env_path)
        if recovery:
            return recovery
        _mark_invalid_and_save(entries, env_path)

    if (
        not force_new_ticket
        and not key_created
        and str(entries.get(TICKET_KEY, "")).strip()
    ):
        finalized = _try_finalize_pending_authority(
            entries, env_path, resolved_base_url
        )
        if finalized:
            return finalized
        # 过期/禁用直接闭环（续期/客服），避免下方对同一把 key 再做一次 APIKeyCheck。
        recovery = _credential_recovery_payload(entries, env_path)
        if recovery:
            return recovery
        # 旧 ticket 未能 finalize（过期/未在 H5 完成/已失效），不复用，继续 TicketCreate。
        pending_entries = _reset_pending_and_ticket(entries, pending_entries)

    if api_key_value and not force_new_ticket and not has_complete_key_material:
        # 有 apikey 但密钥材料缺失/损坏：等同换设备/凭据丢失，直接走重置而非报错中断。
        return issue_credential_ticket(scenario=SCENARIO_RESET, created=True)

    if api_key_value and not force_new_ticket:
        finalized = _finalize_valid_credentials(
            entries,
            env_path,
            resolved_base_url,
            "API Key 校验通过，并已刷新账户索引，可继续后续业务。",
        )
        if finalized:
            _delete_pending_state(env_path)
            return finalized
        recovery = _credential_recovery_payload(entries, env_path)
        if recovery:
            return recovery
        pending_entries = _reset_pending_and_ticket(entries, pending_entries)
        _mark_invalid_and_save(entries, env_path)

    recovery = _credential_recovery_payload(entries, env_path)
    if recovery:
        return recovery

    if force_new_ticket:
        ticket_scenario = SCENARIO_SETUP
    else:
        current_status = str(
            entries.get(API_KEY_STATUS_KEY, "") or api_key_status
        ).strip().lower()
        if current_status == "expired":
            return issue_credential_ticket(scenario=SCENARIO_RENEW, created=True)
        if current_status == "disabled":
            return _contact_support_payload(env_path)
        ticket_scenario = (
            SCENARIO_RESET
            if api_key_value or has_complete_key_material or current_status == "invalid"
            else SCENARIO_SETUP
        )
    pending_payload = _create_ticket(
        entries,
        env_path,
        resolved_base_url,
        private_key_pem,
        scenario=ticket_scenario,
    )
    finalized = _try_finalize_pending_authority(entries, env_path, resolved_base_url)
    if finalized:
        return finalized
    return pending_payload


_BACKFILL_UPDATE_CMD = (
    "python3 fosun-env-setup/code/ensure_fosun_env.py "
    "--api-key <页面 API Key> --server-public-key '<页面服务端公钥 PEM 全文>'"
)


def _apikey_backfill_rejected_payload(env_path: Path) -> dict[str, Any]:
    """回填的 apikey 被服务端判定无效：复用当前二维码让用户重置后重发，绝不轮换密钥。

    死循环根因：每次 invalid 都轮换客户端密钥 + 重签 ticket，会让用户刚在【上一张
    页面】完成的「忘记 API 参数」绑定立即失效。这里改为保持当前 pending/密钥/二维码不变。
    """
    pending = _load_pending_state(env_path)
    open_url = str(pending.get(OPEN_URL_KEY, "") or "").strip()
    if not open_url:
        # 没有可复用的二维码，只能干净重来：重新签发重置 ticket（全新密钥对）。
        return issue_credential_ticket(scenario=SCENARIO_RESET, created=True)

    expire_time = str(pending.get(TICKET_EXPIRE_TIME_KEY, "0") or "0")
    payload = _pending_payload(
        env_path,
        created=False,
        open_url=open_url,
        ticket_expire_time=expire_time,
        scenario=SCENARIO_RESET,
    )
    payload["ok"] = False
    payload["api_key_rejected"] = True
    payload["user_message"] = (
        "您发来的 API Key 被服务端判定为无效。请【不要重新扫码】，"
        "直接在刚才那张二维码对应的页面点「忘记 API 参数」完成重置，"
        "再把页面上【API Key 与服务端公钥 PEM】原文一并发我（不要发旧的或记忆中的 Key）。"
    )
    payload["next_action"] = (
        "复用当前二维码（created_new_ticket=false、密钥对保持不变）；提醒用户在该页面点「忘记 API 参数」后，"
        f"把页面新显示的 API Key 发来，再次执行 {_BACKFILL_UPDATE_CMD}。"
        "严禁重新签发 ticket 或轮换密钥——否则会让用户刚完成的页面绑定失效，造成死循环；"
        "仅当用户明确要求从头再来时才运行默认入口重签。"
    )
    return payload


def update_api_key(
    api_key: str,
    *,
    server_public_key: str,
    finalize: bool = True,
) -> dict[str, Any]:
    """用户回填 apikey + 页面服务端公钥：写入 fosun.env 与 pending，再做一次受控 finalize。

    场景 1（换设备/点击「忘记 API 参数」）与场景 3 共用：客户端私钥在 pending；
    页面服务端公钥与 TicketCreate 临时返回的不同，**必须**由用户一并提供。

    关键：finalize 判定为 invalid 时【不轮换密钥、不重签 ticket】，而是复用当前二维码
    让用户在同一页面点「忘记 API 参数」后重发 Key——避免密钥对与页面绑定错位导致的
    「重置→不匹配→再重置」死循环。过期→续期、禁用→客服仍照常路由。
    """
    api_key = str(api_key or "").strip()
    if not api_key:
        raise ValueError("API Key 不能为空")

    env_path = shared_env_path()
    entries, promoted_from_pending = _apply_user_api_key_backfill(
        env_path,
        api_key,
        server_public_key=server_public_key,
    )

    base_meta = {
        "api_key_updated": True,
        "promoted_from_pending": promoted_from_pending,
        "api_key_written_to_env_and_pending": True,
    }
    if not finalize:
        return {"api_key": api_key, "env_path": str(env_path), **base_meta}

    resolved_base_url = str(entries.get(BASE_URL_KEY) or DEFAULT_BASE_URL).rstrip("/")
    finalized = _finalize_valid_credentials(
        entries,
        env_path,
        resolved_base_url,
        "API Key 回填校验通过，本地私钥/服务端公钥与账户索引已写入共享凭证，可继续后续业务。",
    )
    if finalized:
        _delete_pending_state(env_path)
        finalized.update(base_meta)
        return finalized

    recovery = _credential_recovery_payload(entries, env_path)
    if recovery:
        recovery.update(base_meta)
        return recovery

    rejected = _apikey_backfill_rejected_payload(env_path)
    rejected.update(base_meta)
    return rejected


def _mint_renew_ticket() -> dict[str, Any]:
    """续期专用：刷新 ticket/open_url，保留已有 apikey、客户端私钥与服务端公钥。"""
    env_path = shared_env_path()
    entries = load_env_entries(env_path)
    _generate_device_id(entries)
    base_url = str(entries.get(BASE_URL_KEY) or DEFAULT_BASE_URL).rstrip("/")
    entries[BASE_URL_KEY] = base_url

    if not str(entries.get(API_KEY_KEY, "")).strip():
        raise RuntimeError("续期需要本地已有 API Key，无法覆盖写入。")
    if not _has_complete_key_material(entries):
        raise RuntimeError("续期需要本地已有服务端公钥，无法覆盖写入。")
    _, private_key_pem = _ensure_client_key_pair(entries)

    payload = {
        "macId": str(entries.get(MAC_ID_KEY, "")).strip(),
        "clientPubKey": _derive_public_key(private_key_pem),
    }
    data = _post_auth_json(base_url, "/api/v1/auth/TicketCreate", payload)

    ticket = str(data.get("ticket", "")).strip()
    open_url = _authority_open_url(data.get("url"), ticket)
    expire_time = str(data.get("expireTime", "0") or "0")

    if not all([ticket, open_url]):
        raise RuntimeError("TicketCreate 返回缺少必要字段，无法写入本地凭证。")

    entries[TICKET_KEY] = ticket
    entries[TICKET_STATUS_KEY] = "active"
    entries[TICKET_EXPIRE_TIME_KEY] = expire_time
    entries[OPEN_URL_KEY] = open_url
    save_env_entries(entries, env_path)

    return {
        "open_url": open_url,
        "expire_time": expire_time,
        "ticket": ticket,
        "renew_only": True,
        "base_url": base_url,
    }


def _prepare_entries_for_ticket(env_path: Path) -> tuple[dict[str, Any], str, str]:
    """加载 env + 合并 pending，确保设备号/客户端私钥/base_url 就绪。

    返回 (entries, private_key_pem, base_url)，供 SETUP/RESET 签发 ticket 复用。
    """
    entries = load_env_entries(env_path)
    _drop_transient_auth_entries(entries)
    pending_entries = _load_pending_state(env_path)
    for key, value in pending_entries.items():
        if not entries.get(key):
            entries[key] = value
    _generate_device_id(entries)
    _, private_key_pem = _ensure_client_key_pair(entries)
    if not entries.get(BASE_URL_KEY):
        entries[BASE_URL_KEY] = DEFAULT_BASE_URL
    base_url = str(entries.get(BASE_URL_KEY) or DEFAULT_BASE_URL).rstrip("/")
    entries[BASE_URL_KEY] = base_url
    return entries, private_key_pem, base_url


def issue_credential_ticket(*, scenario: str, created: bool = True) -> dict[str, Any]:
    """按场景签发 ticket 并返回 pending 结构化 JSON（续期 / 重置 / 首次开通）。"""
    if scenario not in {SCENARIO_SETUP, SCENARIO_RENEW, SCENARIO_RESET}:
        raise ValueError(f"未知凭据场景: {scenario}")

    env_path = shared_env_path()
    if scenario == SCENARIO_RENEW:
        ticket_result = _mint_renew_ticket()
        return _pending_payload(
            env_path,
            created=created,
            open_url=ticket_result["open_url"],
            ticket_expire_time=ticket_result["expire_time"],
            scenario=SCENARIO_RENEW,
        )

    entries, private_key_pem, base_url = _prepare_entries_for_ticket(env_path)
    return _create_ticket(
        entries,
        env_path,
        base_url,
        private_key_pem,
        scenario=scenario,
    )


def renew_openapi_credentials() -> dict[str, Any]:
    """场景 2：apikey 过期续期（URL 带 isExpired=1，无需回填 apikey）。"""
    return issue_credential_ticket(scenario=SCENARIO_RENEW)


def reset_openapi_credentials() -> dict[str, Any]:
    """场景 3：凭据无效/损坏，轮换客户端密钥并引导页面重置 + apikey 回填。"""
    return issue_credential_ticket(scenario=SCENARIO_RESET)


def issue_apikey_error_payload(
    *,
    scenario: str,
    code: int,
    message: str = "",
    label: str = "",
) -> dict[str, Any]:
    """供 real-trade-skill 错误码分派：签发 ticket 并附加错误上下文。"""
    payload = issue_credential_ticket(scenario=scenario, created=True)
    payload["ok"] = False
    payload["code"] = code
    payload["message"] = message or label
    if scenario == SCENARIO_RENEW:
        payload["error_code"] = "OPENAPI_ACCOUNT_RENEW"
    elif scenario == SCENARIO_RESET:
        payload["error_code"] = "OPENAPI_ACCOUNT_RESET"
    else:
        payload["error_code"] = "OPENAPI_ACCOUNT_SETUP"
    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="生成或修复 fw-trade-skill 共享 fosun.env 凭证文件",
    )
    parser.add_argument(
        "--repair",
        action="store_true",
        help="即使 fosun.env 已存在，也运行凭证状态机做校验/补齐/刷新",
    )
    parser.add_argument(
        "--force-new-ticket",
        action="store_true",
        help="跳过旧 ticket 的 finalize 尝试，立即 TicketCreate 签发新开通 URL",
    )
    parser.add_argument(
        "--renew",
        action="store_true",
        help="场景 2：apikey 过期续期，TicketCreate 并返回带 isExpired=1 的开通 URL/二维码",
    )
    parser.add_argument(
        "--reset-credentials",
        action="store_true",
        help="场景 3：凭据无效/损坏，轮换客户端密钥并返回重置 URL/二维码（须在页面完成重置后 --api-key 回填）",
    )
    parser.add_argument(
        "--api-key",
        help="页面回填：与 --server-public-key 同时使用（已开通/忘记 API 参数 场景必填）",
    )
    parser.add_argument(
        "--server-public-key",
        help="页面回填：授权页展示的服务端公钥 PEM，与 --api-key 同时使用（必填）",
    )
    parser.add_argument(
        "--base-url",
        help=f"覆盖网关地址；默认 {DEFAULT_BASE_URL}",
    )
    parser.add_argument(
        "--print-env-path",
        action="store_true",
        help="只打印解析后的 fosun.env 绝对路径，不做任何写入",
    )
    return parser


def main() -> None:
    args = _build_parser().parse_args()
    if args.print_env_path:
        print(shared_env_path())
        return
    try:
        if args.renew and args.reset_credentials:
            raise ValueError("--renew 与 --reset-credentials 互斥，请只选其一。")

        api_key = args.api_key
        server_public_key = args.server_public_key

        if args.renew:
            payload = renew_openapi_credentials()
        elif args.reset_credentials:
            payload = reset_openapi_credentials()
        elif api_key and not args.repair and not args.force_new_ticket:
            if not server_public_key:
                raise ValueError(
                    "回填须同时提供 --api-key 与 --server-public-key（页面服务端公钥 PEM 全文）。"
                    "仅提供 apikey 会导致使用 ticket 临时公钥，与页面绑定不一致。"
                )
            payload = update_api_key(
                api_key,
                server_public_key=server_public_key,
                finalize=True,
            )
        else:
            payload = ensure_fosun_env(
                repair_existing=args.repair,
                force_new_ticket=args.force_new_ticket,
                api_key=api_key,
                server_public_key=server_public_key,
                base_url=args.base_url,
            )
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    except Exception as exc:  # noqa: BLE001
        payload = {
            "ok": False,
            "status": "error",
            "env_path": str(shared_env_path()),
            "message": f"{type(exc).__name__}: {exc}",
            "next_action": "按 message 修复本地依赖、网络或复星认证接口问题后重试；不要继续执行依赖凭证的业务脚本。",
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

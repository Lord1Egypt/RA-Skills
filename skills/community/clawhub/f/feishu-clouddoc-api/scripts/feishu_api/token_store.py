from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .errors import FeishuConfigError, FeishuRequestError


TOKEN_EXPIRED_CODES = {99991668, 99991677}


@dataclass(slots=True)
class TokenRefreshResult:
    access_token: str
    refresh_token: str
    expires_at: int
    refresh_expires_at: int
    path: Path


def read_env_file(path: Path | None) -> dict[str, str]:
    if not path or not path.exists():
        return {}
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            values[key] = value
    return values


def write_env_values(path: Path, values: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    remaining = dict(values)
    out: list[str] = []
    for line in lines:
        if "=" not in line or line.lstrip().startswith("#"):
            out.append(line)
            continue
        key = line.split("=", 1)[0].strip()
        if key in remaining:
            out.append(f"{key}={remaining.pop(key)}")
        else:
            out.append(line)
    for key, value in remaining.items():
        out.append(f"{key}={value}")
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    try:
        path.chmod(0o600)
    except OSError:
        pass


def app_token_slot(app_id: str) -> str:
    return hashlib.sha256(app_id.encode("utf-8")).hexdigest()[:16]


def shared_user_token_file(app_id: str) -> Path:
    custom = os.getenv("FEISHU_USER_TOKEN_FILE", "").strip()
    if custom:
        return Path(custom).expanduser()
    return Path.home() / ".openclaw" / "feishu-user-tokens" / f"{app_token_slot(app_id)}.env"


def resolve_user_token_file(app_id: str, env_file: Path | None) -> Path:
    shared = shared_user_token_file(app_id)
    if shared.exists():
        return shared
    return env_file or shared


def user_token_env(app_id: str, env_file: Path | None) -> tuple[Path, dict[str, str]]:
    path = resolve_user_token_file(app_id, env_file)
    return path, read_env_file(path)


def seed_shared_user_token(app_id: str, env_file: Path | None) -> Path | None:
    if not env_file or not env_file.exists():
        return None
    env = read_env_file(env_file)
    wanted = {
        key: env.get(key, "")
        for key in [
            "FEISHU_USER_ACCESS_TOKEN",
            "FEISHU_USER_REFRESH_TOKEN",
            "FEISHU_USER_OPEN_ID",
            "FEISHU_USER_ACCESS_TOKEN_EXPIRES_AT",
            "FEISHU_USER_REFRESH_TOKEN_EXPIRES_AT",
        ]
        if env.get(key, "")
    }
    if not wanted.get("FEISHU_USER_ACCESS_TOKEN") and not wanted.get("FEISHU_USER_REFRESH_TOKEN"):
        return None
    path = shared_user_token_file(app_id)
    if not path.exists():
        write_env_values(path, wanted)
    return path


def tenant_access_token(settings: Any) -> str:
    url = settings.base_url.rstrip("/") + "/open-apis/auth/v3/tenant_access_token/internal"
    body = json.dumps({
        "app_id": settings.app_id,
        "app_secret": settings.app_secret,
    }, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise FeishuRequestError(f"tenant_access_token HTTP {exc.code}", details=detail) from exc
    except urllib.error.URLError as exc:
        raise FeishuRequestError(f"tenant_access_token network error: {exc}") from exc
    code = payload.get("code", 0)
    if code not in (0, None):
        raise FeishuRequestError(payload.get("msg") or "tenant_access_token failed", code=code, details=payload)
    token = payload.get("tenant_access_token", "")
    if not token:
        raise FeishuRequestError("Feishu did not return tenant_access_token", details=payload)
    return token


def _refresh_payload(settings: Any, refresh_token: str) -> dict[str, Any]:
    from lark_oapi.api.authen.v1 import (
        CreateRefreshAccessTokenRequest,
        CreateRefreshAccessTokenRequestBody,
    )

    from .client import create_client

    request = CreateRefreshAccessTokenRequest.builder().request_body(
        CreateRefreshAccessTokenRequestBody.builder()
        .grant_type("refresh_token")
        .refresh_token(refresh_token)
        .build()
    ).build()
    response = create_client().authen.v1.refresh_access_token.create(request)
    if not getattr(response, "success", lambda: False)():
        raise FeishuRequestError(
            getattr(response, "msg", None) or "refresh_user_access_token failed",
            code=getattr(response, "code", None),
            details=response,
        )
    data = response.data
    return {
        "access_token": getattr(data, "access_token", "") or "",
        "refresh_token": getattr(data, "refresh_token", "") or "",
        "expires_in": getattr(data, "expires_in", 0) or 0,
        "refresh_token_expires_in": (
            getattr(data, "refresh_token_expires_in", 0)
            or getattr(data, "refresh_expires_in", 0)
            or 0
        ),
        "open_id": getattr(data, "open_id", "") or "",
    }


def refresh_user_access_token(settings: Any) -> TokenRefreshResult:
    token_file, env = user_token_env(settings.app_id, Path(settings.env_file) if settings.env_file else None)
    refresh_token = (
        os.getenv("FEISHU_USER_REFRESH_TOKEN", "").strip()
        or env.get("FEISHU_USER_REFRESH_TOKEN", "").strip()
        or settings.user_refresh_token
    )
    if not refresh_token:
        raise FeishuConfigError("Missing FEISHU_USER_REFRESH_TOKEN; user authorization must be restored")

    data = _refresh_payload(settings, refresh_token)
    access_token = data.get("access_token", "")
    next_refresh_token = data.get("refresh_token", "")
    if not access_token or not next_refresh_token:
        raise FeishuRequestError("Feishu refresh response did not include user tokens", details=data)

    now = int(time.time())
    expires_at = now + int(data.get("expires_in") or 0)
    refresh_expires_at = now + int(data.get("refresh_token_expires_in") or data.get("refresh_expires_in") or 0)
    write_env_values(token_file, {
        "FEISHU_USER_ACCESS_TOKEN": access_token,
        "FEISHU_USER_REFRESH_TOKEN": next_refresh_token,
        "FEISHU_USER_OPEN_ID": data.get("open_id") or env.get("FEISHU_USER_OPEN_ID", settings.user_open_id),
        "FEISHU_USER_ACCESS_TOKEN_EXPIRES_AT": str(expires_at),
        "FEISHU_USER_REFRESH_TOKEN_EXPIRES_AT": str(refresh_expires_at),
    })
    os.environ["FEISHU_USER_ACCESS_TOKEN"] = access_token
    os.environ["FEISHU_USER_REFRESH_TOKEN"] = next_refresh_token
    if data.get("open_id") or env.get("FEISHU_USER_OPEN_ID", settings.user_open_id):
        os.environ["FEISHU_USER_OPEN_ID"] = data.get("open_id") or env.get("FEISHU_USER_OPEN_ID", settings.user_open_id)
    os.environ["FEISHU_USER_ACCESS_TOKEN_EXPIRES_AT"] = str(expires_at)
    os.environ["FEISHU_USER_REFRESH_TOKEN_EXPIRES_AT"] = str(refresh_expires_at)
    try:
        settings.user_access_token = access_token
        settings.user_refresh_token = next_refresh_token
        settings.user_open_id = data.get("open_id") or env.get("FEISHU_USER_OPEN_ID", settings.user_open_id)
        settings.user_access_token_expires_at = str(expires_at)
        settings.user_refresh_token_expires_at = str(refresh_expires_at)
        settings.user_token_file = str(token_file)
    except AttributeError:
        pass
    return TokenRefreshResult(access_token, next_refresh_token, expires_at, refresh_expires_at, token_file)


def needs_preemptive_refresh(settings: Any, *, skew_seconds: int = 300) -> bool:
    expires = str(getattr(settings, "user_access_token_expires_at", "") or "").strip()
    if not expires:
        return False
    try:
        return int(expires) <= int(time.time()) + skew_seconds
    except ValueError:
        return False

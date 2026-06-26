from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
from typing import Any


def _toolkit_root() -> Path:
    return Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class ToolkitPaths:
    root: Path
    config_dir: Path
    data_dir: Path

    @classmethod
    def discover(cls) -> "ToolkitPaths":
        root = _toolkit_root()
        return cls(
            root=root,
            config_dir=root / "config",
            data_dir=root / "data",
        )

    @property
    def alias_file(self) -> Path:
        return self.data_dir / "member_aliases.json"

    @property
    def runtime_config_file(self) -> Path:
        return self.config_dir / "runtime.json"

    @property
    def members_file(self) -> Path:
        return self.data_dir / "feishu_members.json"

    @property
    def sync_meta_file(self) -> Path:
        return self.data_dir / "sync_meta.json"

    def ensure(self) -> None:
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)

class AppConfigError(ValueError):
    pass


def config_guidance(paths: ToolkitPaths) -> str:
    return (
        "Feishu toolkit is not configured. Provide FEISHU_APP_ID and FEISHU_APP_SECRET through environment variables, "
        f"or write them to {paths.runtime_config_file}. Optional user OAuth tokens can be stored alongside the app "
        "credentials to let task APIs run as the user."
    )


def redact_secret(secret: str) -> str:
    if not secret:
        return ""
    if len(secret) <= 4:
        return "*" * len(secret)
    return f"{secret[:2]}{'*' * (len(secret) - 4)}{secret[-2:]}"


@dataclass(frozen=True)
class AppConfig:
    app_id: str = ""
    app_secret: str = ""
    user_access_token: str = ""
    refresh_token: str = ""
    user_token_expires_at: str = ""
    user_scope: str = ""
    base_url: str = "https://open.feishu.cn/open-apis"
    timezone: str = "Asia/Shanghai"
    default_member_open_id: str = ""

    @classmethod
    def load(cls, paths: ToolkitPaths, environ: dict[str, str] | None = None) -> "AppConfig":
        env = environ if environ is not None else dict(os.environ)
        runtime = load_json(paths.runtime_config_file, {})
        app_id = (env.get("FEISHU_APP_ID") or runtime.get("app_id") or "").strip()
        app_secret = (env.get("FEISHU_APP_SECRET") or runtime.get("app_secret") or "").strip()
        if not app_id or not app_secret:
            raise AppConfigError(config_guidance(paths))
        user_access_token = (env.get("FEISHU_USER_ACCESS_TOKEN") or runtime.get("user_access_token") or "").strip()
        refresh_token = (env.get("FEISHU_REFRESH_TOKEN") or runtime.get("refresh_token") or "").strip()
        user_token_expires_at = (
            env.get("FEISHU_USER_TOKEN_EXPIRES_AT") or runtime.get("user_token_expires_at") or ""
        ).strip()
        user_scope = (env.get("FEISHU_USER_SCOPE") or runtime.get("user_scope") or "").strip()
        base_url = (env.get("FEISHU_BASE_URL") or runtime.get("base_url") or cls.base_url).strip() or cls.base_url
        timezone = (env.get("FEISHU_TIMEZONE") or runtime.get("timezone") or cls.timezone).strip() or cls.timezone
        default_member_open_id = (
            env.get("FEISHU_DEFAULT_MEMBER_OPEN_ID") or runtime.get("default_member_open_id") or ""
        ).strip()
        return cls(
            app_id=app_id,
            app_secret=app_secret,
            user_access_token=user_access_token,
            refresh_token=refresh_token,
            user_token_expires_at=user_token_expires_at,
            user_scope=user_scope,
            base_url=base_url.rstrip("/"),
            timezone=timezone,
            default_member_open_id=default_member_open_id,
        )

    def to_public_dict(self) -> dict[str, str]:
        return {
            "app_id": self.app_id,
            "app_secret": redact_secret(self.app_secret),
            "user_access_token": redact_secret(self.user_access_token),
            "refresh_token": redact_secret(self.refresh_token),
            "user_token_expires_at": self.user_token_expires_at,
            "user_scope": self.user_scope,
            "base_url": self.base_url,
            "timezone": self.timezone,
            "default_member_open_id": self.default_member_open_id,
        }


def expires_at_from_now(seconds: int) -> str:
    return (datetime.now(timezone.utc) + timedelta(seconds=seconds)).isoformat()


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

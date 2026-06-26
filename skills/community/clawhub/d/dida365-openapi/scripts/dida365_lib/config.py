"""Configuration loading and persistence for the Dida365 OpenAPI CLI."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Optional

from .common import redact_mapping

APP_DIR_NAME = "dida365-openapi"
DEFAULT_SCOPE = "tasks:write tasks:read"
DEFAULT_AUTH_BASE_URL = "https://dida365.com"
DEFAULT_API_BASE_URL = "https://api.dida365.com"
DEFAULT_TIMEOUT = 30.0

ENV_VAR_MAP = {
    "client_id": "DIDA365_CLIENT_ID",
    "client_secret": "DIDA365_CLIENT_SECRET",
    "redirect_uri": "DIDA365_REDIRECT_URI",
    "scope": "DIDA365_SCOPE",
    "access_token": "DIDA365_ACCESS_TOKEN",
    "auth_base_url": "DIDA365_AUTH_BASE_URL",
    "api_base_url": "DIDA365_API_BASE_URL",
}

CONFIG_FIELDS = (
    "client_id",
    "client_secret",
    "redirect_uri",
    "scope",
    "auth_base_url",
    "api_base_url",
)

SECRET_FIELDS = {"client_secret", "access_token"}


@dataclass
class RuntimeSettings:
    client_id: Optional[str]
    client_secret: Optional[str]
    redirect_uri: Optional[str]
    scope: str
    access_token: Optional[str]
    auth_base_url: str
    api_base_url: str
    timeout: float
    config_dir: Path
    config_file: Path
    token_file: Path
    config_data: dict[str, Any]
    token_data: dict[str, Any]
    sources: dict[str, str]

    def redacted_status(self) -> dict[str, Any]:
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "scope": self.scope,
            "access_token": self.access_token,
            "auth_base_url": self.auth_base_url,
            "api_base_url": self.api_base_url,
        }
        return redact_mapping(payload, SECRET_FIELDS)


def default_config_dir() -> Path:
    xdg_home = os.environ.get("XDG_CONFIG_HOME")
    if xdg_home:
        base_dir = Path(xdg_home).expanduser()
    else:
        base_dir = Path.home() / ".config"
    return base_dir / APP_DIR_NAME


def config_file_for_dir(config_dir: Path) -> Path:
    return config_dir / "config.json"


def token_file_for_dir(config_dir: Path) -> Path:
    return config_dir / "token.json"


def _read_json_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"Unable to read {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def _write_json_file(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    if os.name != "nt":
        os.chmod(path.parent, 0o700)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if os.name != "nt":
        os.chmod(path, 0o600)


def resolve_runtime_settings(cli_overrides: Optional[Mapping[str, Any]] = None) -> RuntimeSettings:
    overrides = dict(cli_overrides or {})
    config_dir = Path(overrides.pop("config_dir", None) or default_config_dir()).expanduser()
    timeout_override = overrides.pop("timeout", None)
    config_file = config_file_for_dir(config_dir)
    token_file = token_file_for_dir(config_dir)

    config_data = _read_json_file(config_file)
    token_data = _read_json_file(token_file)
    sources: dict[str, str] = {}

    def choose_value(field: str, default: Any = None) -> Any:
        cli_value = overrides.get(field)
        if cli_value not in (None, ""):
            sources[field] = "cli"
            return cli_value

        env_name = ENV_VAR_MAP.get(field)
        if env_name:
            env_value = os.environ.get(env_name)
            if env_value not in (None, ""):
                sources[field] = f"env:{env_name}"
                return env_value

        if field == "access_token":
            token_value = token_data.get("access_token")
            if token_value not in (None, ""):
                sources[field] = "token_file"
                return token_value

        config_value = config_data.get(field)
        if config_value not in (None, ""):
            sources[field] = "config_file"
            return config_value

        if default is not None:
            sources[field] = "default"
            return default
        sources[field] = "unset"
        return None

    timeout = float(timeout_override) if timeout_override not in (None, "") else DEFAULT_TIMEOUT

    return RuntimeSettings(
        client_id=choose_value("client_id"),
        client_secret=choose_value("client_secret"),
        redirect_uri=choose_value("redirect_uri"),
        scope=choose_value("scope", DEFAULT_SCOPE),
        access_token=choose_value("access_token"),
        auth_base_url=choose_value("auth_base_url", DEFAULT_AUTH_BASE_URL),
        api_base_url=choose_value("api_base_url", DEFAULT_API_BASE_URL),
        timeout=timeout,
        config_dir=config_dir,
        config_file=config_file,
        token_file=token_file,
        config_data=config_data,
        token_data=token_data,
        sources=sources,
    )


def save_config(
    settings: RuntimeSettings,
    updates: Optional[Mapping[str, Any]] = None,
    *,
    fields: Optional[Iterable[str]] = None,
) -> dict[str, Any]:
    payload = dict(settings.config_data)
    fields_to_save = tuple(fields) if fields is not None else CONFIG_FIELDS
    for field in fields_to_save:
        value = getattr(settings, field)
        if value not in (None, ""):
            payload[field] = value
    if updates:
        for key, value in updates.items():
            if value not in (None, ""):
                payload[key] = value
    _write_json_file(settings.config_file, payload)
    settings.config_data = payload
    return payload


def save_token(settings: RuntimeSettings, token_response: Mapping[str, Any]) -> dict[str, Any]:
    payload = dict(token_response)
    _write_json_file(settings.token_file, payload)
    settings.token_data = payload
    settings.access_token = payload.get("access_token")
    return payload


def clear_token(settings: RuntimeSettings) -> bool:
    if settings.token_file.exists():
        settings.token_file.unlink()
        settings.token_data = {}
        settings.access_token = None
        return True
    return False

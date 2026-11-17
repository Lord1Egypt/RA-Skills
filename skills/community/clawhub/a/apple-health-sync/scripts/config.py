#!/usr/bin/env python3
"""
Shared config loading for Apple Health Sync scripts.
"""

import json
import os
import stat
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from urllib import error, request


# App config

APP_CONFIG = {
    "onboarding_version": 4,
    "ios_app_link": "https://apps.apple.com/app/health-sync-for-openclaw/id6759522298",
    "supabase_region": "eu-west-1",
    "supabase_get_data_url": "https://snpiylxajnxpklpwdtdg.supabase.co/functions/v1/get-data-v2",
    "supabase_qr_code_generator_url": "https://snpiylxajnxpklpwdtdg.supabase.co/functions/v1/qr-code-generator",
    "supabase_unlink_device_url": "https://snpiylxajnxpklpwdtdg.supabase.co/functions/v1/unlink-device",
    "supabase_publishable_key": "sb_publishable_HW9XhDFQLrcPoGsbYIz7zg_FnFOePtQ",
    "v5_recent_max_ciphertext_bytes": 4_194_304,
    "v5_recent_max_plaintext_bytes": 4_194_304,
    "v5_history_max_ciphertext_bytes": 16_777_216,
    "v5_history_max_plaintext_bytes": 16_777_216,
}
APP_OWNED_KEYS = set(APP_CONFIG.keys())
ALLOWED_RELAY_URLS = frozenset(
    {
        str(APP_CONFIG["supabase_get_data_url"]),
        str(APP_CONFIG["supabase_qr_code_generator_url"]),
        str(APP_CONFIG["supabase_unlink_device_url"]),
    }
)


# User config

DEFAULT_STATE_DIR = Path.home() / ".apple-health-sync"
SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULTS_CONFIG_PATH = SKILL_DIR / "references" / "configs.defaults.json"
ALLOWED_STORAGE_VALUES = {"sqlite", "json"}
REQUIRED_DEFAULT_STRING_KEYS = ("storage",)
REMOVED_USER_CONFIG_KEYS = {"custom_sink_command", "onboarding_deeplink"}


def validate_relay_url(raw_url: str) -> str:
    url = str(raw_url).strip()
    if url not in ALLOWED_RELAY_URLS:
        raise RuntimeError("Refusing network request to an undeclared relay URL.")
    return url


class RejectRelayRedirects(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise error.HTTPError(
            req.full_url,
            code,
            "Relay redirects are not allowed.",
            headers,
            fp,
        )


def open_relay_request(req: request.Request, timeout: int):
    validate_relay_url(req.full_url)
    opener = request.build_opener(RejectRelayRedirects())
    return opener.open(req, timeout=timeout)


def secure_state_directory(path: Path) -> None:
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    if not path.is_dir():
        raise RuntimeError(f"State path is not a directory: {path}")
    os.chmod(path, 0o700)


def secure_private_file(path: Path) -> None:
    if path.is_symlink():
        raise RuntimeError(f"Sensitive file must not be a symbolic link: {path}")
    file_mode = path.stat().st_mode
    if not stat.S_ISREG(file_mode):
        raise RuntimeError(f"Sensitive path is not a regular file: {path}")
    os.chmod(path, 0o600)


def resolve_state_dir(raw_state_dir: str = "") -> Path:
    if raw_state_dir:
        return Path(raw_state_dir).expanduser().resolve()
    return DEFAULT_STATE_DIR.expanduser().resolve()


def resolve_user_paths(state_dir: Optional[Path] = None) -> Dict[str, Path]:
    resolved_state_dir = state_dir or DEFAULT_STATE_DIR.expanduser().resolve()
    config_dir = resolved_state_dir / "config"
    return {
        "state_dir": resolved_state_dir,
        "config_dir": config_dir,
        "secrets_dir": config_dir / "secrets",
        "primary_config_path": config_dir / "config.json",
        "legacy_user_config_path": config_dir / "runtime.json",
    }


def load_json_object(path: Path, label: str) -> Dict[str, Any]:
    if not path.exists():
        raise RuntimeError(f"Missing {label} file: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError(f"{label.capitalize()} file must contain a JSON object: {path}")
    return payload


def strip_app_owned_keys(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {key: value for key, value in payload.items() if key not in APP_OWNED_KEYS}


def migrate_legacy_user_config_keys(payload: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
    migrated = False
    normalized = dict(payload)
    if "user_id" not in normalized and normalized.get("record_id"):
        normalized["user_id"] = normalized["record_id"]
        migrated = True
    if "record_id" in normalized:
        del normalized["record_id"]
        migrated = True
    if normalized.get("storage") == "custom":
        normalized["storage"] = "sqlite"
        migrated = True
    for key in REMOVED_USER_CONFIG_KEYS:
        if key in normalized:
            del normalized[key]
            migrated = True
    return normalized, migrated


def load_defaults_config() -> Dict[str, Any]:
    defaults = load_json_object(DEFAULTS_CONFIG_PATH, "defaults config")
    for key in REQUIRED_DEFAULT_STRING_KEYS:
        value = str(defaults.get(key, "")).strip()
        if not value:
            raise RuntimeError(f"Defaults config is missing required string key '{key}': {DEFAULTS_CONFIG_PATH}")
        defaults[key] = value
    if defaults["storage"] not in ALLOWED_STORAGE_VALUES:
        raise RuntimeError(
            f"Defaults config has unsupported storage '{defaults['storage']}': {DEFAULTS_CONFIG_PATH}"
        )
    return defaults


def load_existing_user_config(state_dir: Optional[Path] = None) -> Dict[str, Any]:
    paths = resolve_user_paths(state_dir)
    for path in (paths["primary_config_path"], paths["legacy_user_config_path"]):
        if path.exists():
            secure_private_file(path)
            raw_user_config = strip_app_owned_keys(load_json_object(path, "user config"))
            user_config, migrated = migrate_legacy_user_config_keys(raw_user_config)
            if migrated or path != paths["primary_config_path"]:
                write_user_config(user_config, paths["state_dir"])
            return user_config
    return {}


def load_effective_config(state_dir: Optional[Path] = None) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    paths = resolve_user_paths(state_dir)
    user_config = load_existing_user_config(paths["state_dir"])
    if not user_config:
        raise RuntimeError(f"Missing user config file: {paths['primary_config_path']}")

    defaults = load_defaults_config()
    effective = dict(defaults)
    effective.update(APP_CONFIG)
    effective.update(user_config)
    return user_config, effective


def atomic_write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    file_descriptor = None
    try:
        file_descriptor = os.open(tmp, flags, 0o600)
        os.fchmod(file_descriptor, 0o600)
        with os.fdopen(file_descriptor, "w", encoding="utf-8") as file_handle:
            file_descriptor = None
            file_handle.write(json.dumps(payload, indent=2) + "\n")
            file_handle.flush()
            os.fsync(file_handle.fileno())
        tmp.replace(path)
        secure_private_file(path)
    finally:
        if file_descriptor is not None:
            os.close(file_descriptor)
        tmp.unlink(missing_ok=True)


def write_user_config(payload: Dict[str, Any], state_dir: Optional[Path] = None) -> None:
    paths = resolve_user_paths(state_dir)
    normalized_payload = migrate_legacy_user_config_keys(strip_app_owned_keys(payload))[0]
    atomic_write_json(paths["primary_config_path"], normalized_payload)

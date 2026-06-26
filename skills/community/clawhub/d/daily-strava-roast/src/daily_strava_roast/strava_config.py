from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

DEFAULT_CONFIG_PATH = Path.home() / ".openclaw" / "secure" / "strava_app.json"
DEFAULT_TOKEN_FILE = Path.home() / ".openclaw" / "workspace" / "agents" / "tars-fit" / "strava_tokens.json"


def load_strava_app_config(config_path: str | Path | None = None) -> dict[str, Any]:
    path = Path(config_path).expanduser() if config_path else DEFAULT_CONFIG_PATH
    file_data: dict[str, Any] = {}
    if path.exists():
        file_data = json.loads(path.read_text())

    client_id = os.getenv("STRAVA_CLIENT_ID") or file_data.get("client_id") or "216808"
    client_secret = os.getenv("STRAVA_CLIENT_SECRET") or file_data.get("client_secret")
    redirect_uri = os.getenv("STRAVA_REDIRECT_URI") or file_data.get("redirect_uri") or "http://localhost/exchange_token"
    scopes = os.getenv("STRAVA_SCOPES") or file_data.get("scopes") or "read,activity:read_all,profile:read_all"
    token_file = os.getenv("STRAVA_TOKEN_FILE") or file_data.get("token_file") or str(DEFAULT_TOKEN_FILE)

    return {
        "config_path": str(path),
        "config_present": path.exists(),
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "scopes": scopes,
        "token_file": token_file,
    }


def missing_config_requirements(config: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    if not config.get("client_id"):
        missing.append("client_id")
    if not config.get("client_secret"):
        missing.append("client_secret")
    return missing


def config_status(config: dict[str, Any]) -> str:
    return "ready" if not missing_config_requirements(config) else "config_incomplete"

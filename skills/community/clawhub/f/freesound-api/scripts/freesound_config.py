import json
import os
from pathlib import Path

APP_DIR = Path(os.environ.get("APPDATA", Path.home() / ".config")) / "OpenClaw" / "freesound-api"
CONFIG_PATH = APP_DIR / "credentials.json"
DEFAULT_REDIRECT_URI = "http://localhost:8787/callback"
API_BASE = "https://freesound.org/apiv2"
AUTHORIZE_URL = f"{API_BASE}/oauth2/authorize/"
TOKEN_URL = f"{API_BASE}/oauth2/access_token/"


def ensure_app_dir() -> Path:
    APP_DIR.mkdir(parents=True, exist_ok=True)
    return APP_DIR


def load_config() -> dict:
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return {}


def save_config(data: dict) -> None:
    ensure_app_dir()
    CONFIG_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")

#!/usr/bin/env python3
import json
import os
import random
import sqlite3
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

import requests

FITBIT_AUTH_URL = "https://www.fitbit.com/oauth2/authorize"
FITBIT_TOKEN_URL = "https://api.fitbit.com/oauth2/token"
FITBIT_API_BASE = "https://api.fitbit.com/1/user"
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _load_env_file() -> None:
    # Prefer skill-local .env regardless of caller cwd; keep cwd fallback for compatibility.
    candidates = [PROJECT_ROOT / ".env", Path.cwd() / ".env"]
    seen = set()
    for env_path in candidates:
        env_path = env_path.resolve()
        if env_path in seen or not env_path.exists():
            continue
        seen.add(env_path)
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


_load_env_file()


@dataclass
class Config:
    client_id: str
    client_secret: str
    redirect_uri: str
    scopes: str
    token_path: Path
    db_path: Path
    timeout: int
    user_id: str
    retries: int
    backoff_base: float


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _path_from_env_or_default(env_key: str, default_rel_path: str) -> Path:
    raw = os.getenv(env_key, default_rel_path)
    p = Path(raw).expanduser()
    if not p.is_absolute():
        p = (PROJECT_ROOT / p).resolve()
    return p


def get_config() -> Config:
    return Config(
        client_id=os.getenv("FITBIT_CLIENT_ID", ""),
        client_secret=os.getenv("FITBIT_CLIENT_SECRET", ""),
        redirect_uri=os.getenv("FITBIT_REDIRECT_URI", "http://127.0.0.1:8787/callback"),
        scopes=os.getenv("FITBIT_SCOPES", "activity heartrate sleep profile weight nutrition settings"),
        token_path=_path_from_env_or_default("FITBIT_TOKEN_PATH", "assets/fitbit_tokens.json"),
        db_path=_path_from_env_or_default("FITBIT_DB_PATH", "assets/fitbit_metrics.sqlite3"),
        timeout=int(os.getenv("FITBIT_TIMEOUT_SECONDS", "30")),
        user_id=os.getenv("FITBIT_USER_ID", "-"),
        retries=int(os.getenv("FITBIT_HTTP_RETRIES", "4")),
        backoff_base=float(os.getenv("FITBIT_BACKOFF_BASE_SECONDS", "1.2")),
    )


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _chmod_600(path: Path) -> None:
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


def load_tokens(cfg: Config) -> Dict[str, Any]:
    if not cfg.token_path.exists():
        return {}
    return json.loads(cfg.token_path.read_text())


def save_tokens(cfg: Config, payload: Dict[str, Any]) -> None:
    ensure_parent(cfg.token_path)
    payload = dict(payload)
    payload["saved_at"] = utc_now_iso()
    cfg.token_path.write_text(json.dumps(payload, indent=2))
    _chmod_600(cfg.token_path)


def db(cfg: Config) -> sqlite3.Connection:
    ensure_parent(cfg.db_path)
    conn = sqlite3.connect(cfg.db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS daily_metrics (
            date TEXT PRIMARY KEY,
            steps INTEGER,
            distance_km REAL,
            calories_out INTEGER,
            floors INTEGER,
            active_zone_minutes INTEGER,
            resting_hr INTEGER,
            hrv_rmssd REAL,
            sleep_minutes INTEGER,
            sleep_efficiency INTEGER,
            sleep_score INTEGER,
            readiness_state TEXT,
            readiness_confidence TEXT,
            reasons_json TEXT,
            pp_recommendation TEXT,
            data_quality TEXT,
            updated_at TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sync_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            started_at TEXT,
            finished_at TEXT,
            status TEXT,
            scope TEXT,
            requested_date TEXT,
            details_json TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS quality_flags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            level TEXT,
            flag TEXT,
            message TEXT,
            created_at TEXT
        )
        """
    )
    return conn


def refresh_access_token(cfg: Config, refresh_token: str) -> Dict[str, Any]:
    resp = requests.post(
        FITBIT_TOKEN_URL,
        data={"grant_type": "refresh_token", "refresh_token": refresh_token},
        auth=(cfg.client_id, cfg.client_secret),
        timeout=cfg.timeout,
    )
    resp.raise_for_status()
    return resp.json()


def get_access_token(cfg: Config) -> str:
    tokens = load_tokens(cfg)
    access = tokens.get("access_token")
    refresh = tokens.get("refresh_token")
    expires_at = float(tokens.get("expires_at", "0"))
    now = time.time()

    if access and now < (expires_at - 60):
        return access
    if not refresh:
        raise RuntimeError("No refresh token found. Run auth flow first.")

    updated = refresh_access_token(cfg, refresh)
    updated["refresh_token"] = updated.get("refresh_token", refresh)
    updated["expires_at"] = now + float(updated.get("expires_in", 0))
    save_tokens(cfg, updated)
    return updated["access_token"]


def _request_with_retry(cfg: Config, method: str, url: str, headers: Dict[str, str], params: Optional[Dict[str, Any]] = None):
    attempts = cfg.retries + 1
    last_err = None
    for i in range(attempts):
        try:
            r = requests.request(method, url, headers=headers, params=params or {}, timeout=cfg.timeout)
            if r.status_code in (429, 500, 502, 503, 504):
                if i < attempts - 1:
                    wait = cfg.backoff_base * (2 ** i) + random.uniform(0, 0.4)
                    time.sleep(wait)
                    continue
            return r
        except requests.RequestException as e:
            last_err = e
            if i < attempts - 1:
                wait = cfg.backoff_base * (2 ** i) + random.uniform(0, 0.4)
                time.sleep(wait)
                continue
            raise
    if last_err:
        raise last_err
    raise RuntimeError("HTTP retry loop ended unexpectedly")


def fitbit_get(cfg: Config, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    url = f"{FITBIT_API_BASE}/{cfg.user_id}/{path}"
    token = get_access_token(cfg)
    headers = {"Authorization": f"Bearer {token}"}

    r = _request_with_retry(cfg, "GET", url, headers, params)
    if r.status_code == 401:
        token = get_access_token(cfg)
        headers = {"Authorization": f"Bearer {token}"}
        r = _request_with_retry(cfg, "GET", url, headers, params)

    if r.status_code == 429:
        raise RuntimeError(f"Fitbit API rate limited (429) for {path}")
    r.raise_for_status()
    return r.json()


def add_quality_flag(conn: sqlite3.Connection, day: str, level: str, flag: str, message: str) -> None:
    conn.execute(
        "INSERT INTO quality_flags(date, level, flag, message, created_at) VALUES (?,?,?,?,?)",
        (day, level, flag, message[:4000], utc_now_iso()),
    )

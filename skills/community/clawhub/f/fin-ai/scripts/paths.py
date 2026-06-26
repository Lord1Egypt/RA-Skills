#!/usr/bin/env python3
"""Shared path helpers for portfolio-workflows scripts."""

from __future__ import annotations

import json
import os
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SKILL_DIR.parent
REPO_PORTFOLIO_DIR = REPO_ROOT / "engine" / "portfolio"
USER_DATA_ROOT = Path.home() / ".agents" / "data" / "portfolio-workflows"
DEFAULT_PROFILE = "default"

DEFAULT_CONFIG = {
    "groups": {},
    "data_dir": "./portfolio",
    "qr_portfolio_path": "",
    "proxy": "",
    "feishu_chat_id": "",
    "yahoo_base": "https://query1.finance.yahoo.com/v8/finance/chart",
    "ticker_map": {},
    "currency_map": {
        "SHA": "CNY",
        "SHE": "CNY",
        "HKG": "HKD",
        "NASDAQ": "USD",
        "NYSE": "USD",
    },
    "fx_tickers": {
        "HKD_CNY": "HKDCNY=X",
        "USD_CNY": "USDCNY=X",
    },
    "market_sources": {
        "us_quote": "http",
    },
}

DEFAULT_USER_SETTINGS = {
    "default_profile": DEFAULT_PROFILE,
    "default_portfolio_dir": str(USER_DATA_ROOT / DEFAULT_PROFILE / "portfolio"),
}


def get_user_settings_path() -> Path:
    explicit_path = os.getenv("PORTFOLIO_WORKFLOWS_SETTINGS_PATH")
    if explicit_path:
        return Path(explicit_path).expanduser()
    return USER_DATA_ROOT / "settings.json"


def load_user_settings() -> dict[str, str]:
    settings_path = get_user_settings_path()
    if not settings_path.exists():
        return dict(DEFAULT_USER_SETTINGS)

    try:
        return {**DEFAULT_USER_SETTINGS, **json.loads(settings_path.read_text(encoding="utf-8"))}
    except Exception:
        return dict(DEFAULT_USER_SETTINGS)


def write_user_settings(settings: dict[str, str]) -> Path:
    settings_path = get_user_settings_path()
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    settings_path.write_text(json.dumps(settings, ensure_ascii=False, indent=2), encoding="utf-8")
    return settings_path


def get_default_portfolio_dir(profile: str | None = None) -> Path:
    explicit_dir = os.getenv("PORTFOLIO_WORKFLOWS_PORTFOLIO_DIR")
    if explicit_dir:
        return Path(explicit_dir).expanduser()

    settings = load_user_settings()
    if not profile and settings.get("default_portfolio_dir"):
        return Path(settings["default_portfolio_dir"]).expanduser()

    selected_profile = profile or os.getenv("PORTFOLIO_WORKFLOWS_PROFILE", settings.get("default_profile", DEFAULT_PROFILE))
    if selected_profile == settings.get("default_profile") and settings.get("default_portfolio_dir"):
        return Path(settings["default_portfolio_dir"]).expanduser()

    if REPO_PORTFOLIO_DIR.exists():
        return REPO_PORTFOLIO_DIR

    return USER_DATA_ROOT / selected_profile / "portfolio"


def resolve_portfolio_dir(
    *,
    portfolio_dir: str | Path | None = None,
    profile: str | None = None,
    prefer_repo: bool = True,
) -> Path:
    if portfolio_dir:
        return Path(portfolio_dir).expanduser()

    settings = load_user_settings()

    selected_profile = profile or os.getenv("PORTFOLIO_WORKFLOWS_PROFILE", settings.get("default_profile", DEFAULT_PROFILE))
    if selected_profile == settings.get("default_profile") and settings.get("default_portfolio_dir"):
        return Path(settings["default_portfolio_dir"]).expanduser()

    if prefer_repo and REPO_PORTFOLIO_DIR.exists():
        return REPO_PORTFOLIO_DIR

    return USER_DATA_ROOT / selected_profile / "portfolio"


def bootstrap_portfolio_dir(portfolio_dir: Path) -> Path:
    portfolio_dir.mkdir(parents=True, exist_ok=True)
    (portfolio_dir / "holdings").mkdir(parents=True, exist_ok=True)
    (portfolio_dir / "snapshots").mkdir(parents=True, exist_ok=True)

    config_path = portfolio_dir / "config.json"
    if not config_path.exists():
        config_path.write_text(json.dumps(DEFAULT_CONFIG, ensure_ascii=False, indent=2), encoding="utf-8")

    return portfolio_dir

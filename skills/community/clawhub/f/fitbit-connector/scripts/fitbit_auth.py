#!/usr/bin/env python3
import argparse
import base64
import secrets
import urllib.parse
from pathlib import Path

import requests

from _fitbit_common import FITBIT_AUTH_URL, FITBIT_TOKEN_URL, ensure_parent, get_config, save_tokens


def _state_path(cfg) -> Path:
    return cfg.token_path.with_suffix(".state")


def _save_oauth_state(cfg, state: str) -> None:
    p = _state_path(cfg)
    ensure_parent(p)
    p.write_text(state)


def _load_oauth_state(cfg) -> str:
    p = _state_path(cfg)
    return p.read_text().strip() if p.exists() else ""


def auth_url() -> None:
    cfg = get_config()
    state = secrets.token_urlsafe(16)
    _save_oauth_state(cfg, state)
    q = {
        "client_id": cfg.client_id,
        "response_type": "code",
        "scope": cfg.scopes,
        "redirect_uri": cfg.redirect_uri,
        "state": state,
    }
    print(f"State: {state}")
    print(f"{FITBIT_AUTH_URL}?{urllib.parse.urlencode(q)}")


def exchange(code: str, state: str = "") -> None:
    cfg = get_config()
    expected_state = _load_oauth_state(cfg)
    if expected_state and state and state != expected_state:
        raise RuntimeError("OAuth state mismatch. Generate a new auth-url and retry.")
    if expected_state and not state:
        raise RuntimeError("Missing --state. Use the state from auth-url output.")
    basic = base64.b64encode(f"{cfg.client_id}:{cfg.client_secret}".encode()).decode()
    r = requests.post(
        FITBIT_TOKEN_URL,
        headers={"Authorization": f"Basic {basic}", "Content-Type": "application/x-www-form-urlencoded"},
        data={"client_id": cfg.client_id, "grant_type": "authorization_code", "redirect_uri": cfg.redirect_uri, "code": code},
        timeout=cfg.timeout,
    )
    r.raise_for_status()
    payload = r.json()
    payload["expires_at"] = __import__("time").time() + float(payload.get("expires_in", 0))
    save_tokens(cfg, payload)
    print(f"Token saved to {cfg.token_path}")


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("auth-url")
    ex = sub.add_parser("exchange")
    ex.add_argument("--code", required=True)
    ex.add_argument("--state", required=False, default="")
    args = p.parse_args()

    try:
        if args.cmd == "auth-url":
            auth_url()
        elif args.cmd == "exchange":
            exchange(args.code, args.state)
    except Exception as e:
        print(f"ERROR: {e}")
        raise SystemExit(2)


if __name__ == "__main__":
    main()

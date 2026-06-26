import requests

from freesound_config import API_BASE, load_config


def get_auth_headers_and_params() -> tuple[dict, dict]:
    cfg = load_config()
    token_data = cfg.get("token") or {}
    access_token = token_data.get("access_token")
    api_key = cfg.get("client_secret")
    headers = {}
    params = {}

    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    elif api_key:
        params["token"] = api_key
    else:
        raise SystemExit("Missing token or API key. Run setup_credentials.py and oauth_login.py first.")

    return headers, params


def get_json(path: str, params: dict | None = None) -> dict:
    headers, auth_params = get_auth_headers_and_params()
    merged = dict(auth_params)
    if params:
        merged.update(params)
    resp = requests.get(f"{API_BASE}{path}", params=merged, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()

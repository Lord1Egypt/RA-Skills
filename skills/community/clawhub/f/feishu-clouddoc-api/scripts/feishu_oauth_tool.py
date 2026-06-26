#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import secrets
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


class OAuthError(RuntimeError):
    pass


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


def load_env(path: str | None) -> tuple[dict[str, str], Path | None]:
    env = dict(os.environ)
    env_path = Path(path).expanduser() if path else None
    for key, value in read_env_file(env_path).items():
        if key and key not in env:
            env[key] = value
    return env, env_path


def require_env(env: dict[str, str], name: str) -> str:
    value = env.get(name, "").strip()
    if not value:
        raise OAuthError(f"Missing {name}")
    return value


def app_token_slot(app_id: str) -> str:
    return hashlib.sha256(app_id.encode("utf-8")).hexdigest()[:16]


def shared_user_token_file(env: dict[str, str]) -> Path:
    custom = env.get("FEISHU_USER_TOKEN_FILE", "").strip()
    if custom:
        return Path(custom).expanduser()
    app_id = require_env(env, "FEISHU_APP_ID")
    return Path.home() / ".openclaw" / "feishu-user-tokens" / f"{app_token_slot(app_id)}.env"


def base_url(env: dict[str, str]) -> str:
    return env.get("FEISHU_BASE_URL", "https://open.feishu.cn").rstrip("/")


def auth_url(env: dict[str, str]) -> str:
    custom = env.get("FEISHU_AUTH_URL", "").strip()
    if custom:
        return custom
    auth_base = env.get("FEISHU_AUTH_BASE_URL", "").strip()
    if not auth_base:
        auth_base = "https://accounts.larksuite.com" if "larksuite.com" in base_url(env) else "https://accounts.feishu.cn"
    return auth_base.rstrip("/") + "/open-apis/authen/v1/authorize"


def token_url(env: dict[str, str]) -> str:
    return env.get("FEISHU_TOKEN_URL", "").strip() or base_url(env) + "/open-apis/authen/v2/oauth/token"


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def code_verifier() -> str:
    return b64url(secrets.token_bytes(48))


def code_challenge(verifier: str) -> str:
    return b64url(hashlib.sha256(verifier.encode("ascii")).digest())


def pkce_path(args: argparse.Namespace, env: dict[str, str]) -> Path:
    raw = args.pkce_file or env.get("FEISHU_OAUTH_PKCE_FILE", "") or ".feishu-oauth-state.json"
    return Path(raw).expanduser()


def read_pkce_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_pkce_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        path.chmod(0o600)
    except OSError:
        pass


def extract_callback_values(callback_url: str) -> dict[str, str]:
    parsed = urllib.parse.urlparse(callback_url)
    values = {key: items[-1] for key, items in urllib.parse.parse_qs(parsed.query).items() if items}
    if not values.get("code") and parsed.fragment:
        fragment = parsed.fragment.split("?", 1)[-1]
        values.update({key: items[-1] for key, items in urllib.parse.parse_qs(fragment).items() if items})
    return values


def post_json(url: str, body: dict[str, Any]) -> dict[str, Any]:
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise OAuthError(f"OAuth HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise OAuthError(f"OAuth network error: {exc}") from exc


def token_data(payload: dict[str, Any]) -> dict[str, Any]:
    code = payload.get("code", 0)
    if code not in (0, None):
        raise OAuthError(payload.get("msg") or payload.get("message") or f"OAuth failed: code={code}")
    data = payload.get("data") if isinstance(payload.get("data"), dict) else payload
    if not isinstance(data, dict):
        raise OAuthError("OAuth response is not a JSON object")
    if not (data.get("access_token") or data.get("user_access_token")):
        raise OAuthError("OAuth response did not include access_token")
    return data


def save_tokens(env: dict[str, str], data: dict[str, Any], output: str | None) -> Path:
    path = Path(output).expanduser() if output else shared_user_token_file(env)
    now = int(time.time())
    access_token = str(data.get("access_token") or data.get("user_access_token") or "")
    refresh_token = str(data.get("refresh_token") or "")
    refresh_expires_in = int(data.get("refresh_token_expires_in") or data.get("refresh_expires_in") or 0)
    values = {
        "FEISHU_USER_ACCESS_TOKEN": access_token,
        "FEISHU_USER_ACCESS_TOKEN_EXPIRES_AT": str(now + int(data.get("expires_in") or 0)),
    }
    if refresh_token:
        values["FEISHU_USER_REFRESH_TOKEN"] = refresh_token
        values["FEISHU_USER_REFRESH_TOKEN_EXPIRES_AT"] = str(now + refresh_expires_in)
    if data.get("open_id"):
        values["FEISHU_USER_OPEN_ID"] = str(data.get("open_id"))
    if data.get("scope"):
        values["FEISHU_USER_SCOPE"] = str(data.get("scope"))
    write_env_values(path, values)
    return path


def emit(value: dict[str, Any]) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def command_auth_url(args: argparse.Namespace) -> dict[str, Any]:
    env, _ = load_env(args.env_file)
    app_id = require_env(env, "FEISHU_APP_ID")
    redirect_uri = args.redirect_uri or env.get("FEISHU_OAUTH_REDIRECT_URI", "").strip()
    if not redirect_uri:
        raise OAuthError("Missing redirect URI. Pass --redirect-uri or set FEISHU_OAUTH_REDIRECT_URI.")
    scope = args.scope if args.scope is not None else env.get("FEISHU_OAUTH_SCOPE", "offline_access")
    state = args.state or secrets.token_urlsafe(18)
    params = {
        "client_id": app_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "state": state,
    }
    verifier = ""
    pkce_file = ""
    if not args.no_pkce:
        verifier = code_verifier()
        params["code_challenge"] = code_challenge(verifier)
        params["code_challenge_method"] = "S256"
        path = pkce_path(args, env)
        pkce_file = str(path)
        write_pkce_state(path, {
            "state": state,
            "code_verifier": verifier,
            "redirect_uri": redirect_uri,
            "scope": scope,
            "created_at": int(time.time()),
        })
    if scope:
        params["scope"] = scope
    return {
        "ok": True,
        "authorization_url": auth_url(env) + "?" + urllib.parse.urlencode(params),
        "state": state,
        "scope": scope,
        "pkce_file": pkce_file,
        "next": "Open authorization_url, authorize, then run exchange-code with --callback-url or --code.",
    }


def command_exchange_code(args: argparse.Namespace) -> dict[str, Any]:
    env, env_path = load_env(args.env_file)
    callback = extract_callback_values(args.callback_url) if args.callback_url else {}
    code = args.code or callback.get("code", "")
    if not code:
        raise OAuthError("Missing code. Pass --code or --callback-url.")

    stored = read_pkce_state(pkce_path(args, env))
    callback_state = args.state or callback.get("state", "")
    if stored.get("state") and callback_state and stored["state"] != callback_state:
        raise OAuthError("OAuth state mismatch")

    redirect_uri = (
        args.redirect_uri
        or str(stored.get("redirect_uri") or "")
        or env.get("FEISHU_OAUTH_REDIRECT_URI", "").strip()
    )
    if not redirect_uri:
        raise OAuthError("Missing redirect URI. It must match the URI used for auth-url.")

    body = {
        "grant_type": "authorization_code",
        "client_id": require_env(env, "FEISHU_APP_ID"),
        "client_secret": require_env(env, "FEISHU_APP_SECRET"),
        "code": code,
        "redirect_uri": redirect_uri,
    }
    verifier = args.code_verifier or str(stored.get("code_verifier") or "")
    if verifier:
        body["code_verifier"] = verifier
    if args.scope:
        body["scope"] = args.scope

    data = token_data(post_json(token_url(env), body))
    token_file = save_tokens(env, data, args.output_env_file)
    if env_path and str(token_file) != str(env_path):
        write_env_values(env_path, {"FEISHU_USER_TOKEN_FILE": str(token_file)})
    return {
        "ok": True,
        "token_file": str(token_file),
        "has_access_token": bool(data.get("access_token") or data.get("user_access_token")),
        "has_refresh_token": bool(data.get("refresh_token")),
        "expires_in": data.get("expires_in", 0),
        "refresh_token_expires_in": data.get("refresh_token_expires_in") or data.get("refresh_expires_in", 0),
        "scope": data.get("scope", ""),
    }


def command_refresh(args: argparse.Namespace) -> dict[str, Any]:
    env, env_path = load_env(args.env_file)
    token_file = Path(args.output_env_file).expanduser() if args.output_env_file else shared_user_token_file(env)
    token_env = read_env_file(token_file)
    refresh_token = args.refresh_token or env.get("FEISHU_USER_REFRESH_TOKEN", "") or token_env.get("FEISHU_USER_REFRESH_TOKEN", "")
    if not refresh_token:
        raise OAuthError("Missing FEISHU_USER_REFRESH_TOKEN")
    body = {
        "grant_type": "refresh_token",
        "client_id": require_env(env, "FEISHU_APP_ID"),
        "client_secret": require_env(env, "FEISHU_APP_SECRET"),
        "refresh_token": refresh_token,
    }
    data = token_data(post_json(token_url(env), body))
    saved = save_tokens(env, data, str(token_file))
    if env_path and str(saved) != str(env_path):
        write_env_values(env_path, {"FEISHU_USER_TOKEN_FILE": str(saved)})
    return {
        "ok": True,
        "token_file": str(saved),
        "has_access_token": bool(data.get("access_token") or data.get("user_access_token")),
        "has_refresh_token": bool(data.get("refresh_token")),
        "expires_in": data.get("expires_in", 0),
        "refresh_token_expires_in": data.get("refresh_token_expires_in") or data.get("refresh_expires_in", 0),
        "scope": data.get("scope", ""),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Feishu OAuth helper for user_access_token")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("auth-url", help="Generate a user authorization URL")
    p.add_argument("--env-file", default="")
    p.add_argument("--redirect-uri", default="")
    p.add_argument("--scope", default=None, help="Space-separated scopes. Defaults to FEISHU_OAUTH_SCOPE or offline_access.")
    p.add_argument("--state", default="")
    p.add_argument("--pkce-file", default="")
    p.add_argument("--no-pkce", action="store_true")
    p.set_defaults(func=command_auth_url)

    p = sub.add_parser("exchange-code", help="Exchange OAuth code for user tokens")
    p.add_argument("--env-file", default="")
    p.add_argument("--callback-url", default="")
    p.add_argument("--code", default="")
    p.add_argument("--state", default="")
    p.add_argument("--redirect-uri", default="")
    p.add_argument("--scope", default="")
    p.add_argument("--code-verifier", default="")
    p.add_argument("--pkce-file", default="")
    p.add_argument("--output-env-file", default="", help="Where to save user tokens. Defaults to FEISHU_USER_TOKEN_FILE or shared token store.")
    p.set_defaults(func=command_exchange_code)

    p = sub.add_parser("refresh", help="Refresh and persist user tokens")
    p.add_argument("--env-file", default="")
    p.add_argument("--refresh-token", default="")
    p.add_argument("--output-env-file", default="")
    p.set_defaults(func=command_refresh)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        emit(args.func(args))
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()

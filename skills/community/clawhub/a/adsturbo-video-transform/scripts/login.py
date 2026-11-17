#!/usr/bin/env python3
"""Sign up or log in from inside the chat, then save an API key on this machine.

Email + verification code, three steps the agent drives:

  start --email     send the code (the server may ask for an image captcha first)
  captcha --code    only when start said next=enter_captcha: what the user read off the image
  verify --code     the emailed code -> account (new or existing) -> API key saved locally

The key goes to ~/.config/adsturbo/credentials.json (0600), keyed by site, and
every other script picks it up when ADSTURBO_API_KEY is unset. It is never
printed: output only carries its last four characters.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

from shared.client import (
    CREDENTIALS_FILE,
    SIGNUP_URL,
    USER_AGENT,
    config_dir,
    emit,
    load_saved_key,
    resolve_base_url,
    site_origin,
)

EXIST_PATH = "/klian/baseapi/base/account/email/exist"
SEND_CODE_PATH = "/klian/baseapi/base/account/email/vcode/get"
CODE_LOGIN_PATH = "/klian/baseapi/base/account/email/register"  # logs in existing users too
KEY_LIST_PATH = "/klian/saasapi/saas/apikey/list"
KEY_CREATE_PATH = "/klian/saasapi/saas/apikey/create"

ACCOUNT_CATE = 1
ACCOUNT_TYPE = 32
SOURCE = 45
VTYPE_REGISTER = "email_register"
VTYPE_LOGIN = "email_login"
KEY_NAME = "adsturbo-skill"
KEY_ACTIVE = 1
STATE_FILE = "login_state.json"
CAPTCHA_FILE = "captcha.png"
REQUEST_TIMEOUT = 30
# Registration source, from the channel each build tags onto SIGNUP_URL.
CHANNEL = urllib.parse.parse_qs(urllib.parse.urlsplit(SIGNUP_URL).query).get("channel", ["direct"])[0]


class LoginError(Exception):
    pass


def _post(origin: str, path: str, body: dict, did: str, uid: int = 0, token: str = "") -> dict:
    """Call an account endpoint: auth and device fields ride in the JSON body, not headers."""
    common = {
        "h_m": uid, "token": token, "cate": ACCOUNT_CATE, "atype": ACCOUNT_TYPE,
        "h_src": SOURCE, "h_did": did, "h_ch": "web", "h_model": "agent", "h_lc": "en",
        "h_dt": 0, "h_nt": 1, "h_et": 2, "zone": -time.timezone, "h_ts": int(time.time() * 1000),
    }
    request = urllib.request.Request(
        origin + path,
        data=json.dumps({**common, **body}).encode("utf-8"),
        method="POST",
        headers={"Content-Type": "application/json", "User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as resp:
            text = resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as err:
        raise LoginError(f"HTTP {err.code} calling {path}") from None
    except OSError as exc:
        raise LoginError(f"Network error calling {path}: {exc}") from exc
    try:
        reply = json.loads(text)
    except ValueError:
        raise LoginError(f"Malformed response from {path}: {text[:200]}") from None
    if reply.get("ret") != 1:
        raise LoginError(reply.get("msg") or f"{path} failed (ret={reply.get('ret')})")
    return reply.get("data") or {}


def _ent(data: dict) -> dict:
    return data.get("ent", data) if isinstance(data, dict) else {}


# ---------- local files ----------

def _write_private(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def _read_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _load_state(origin: str) -> dict:
    state = _read_json(config_dir() / STATE_FILE)
    if state.get("origin") != origin or not state.get("email"):
        raise LoginError("No login in progress. Start with: login.py start --email <email>")
    return state


def _save_key(origin: str, email: str, uid: int, api_key: str) -> None:
    path = config_dir() / CREDENTIALS_FILE
    saved = {**_read_json(path), origin: {"email": email, "uid": uid, "api_key": api_key}}
    _write_private(path, saved)


# ---------- steps ----------

def _send_code(origin: str, state: dict, captcha_id: int = 0, captcha_code: str = "") -> dict:
    body = {"email": state["email"], "cate": ACCOUNT_CATE, "vtype": state["vtype"], "h_src": SOURCE}
    if captcha_id and captcha_code:
        body.update({"captchaid": captcha_id, "captchacode": captcha_code})
    ent = _ent(_post(origin, SEND_CODE_PATH, body, state["did"]))
    if ent.get("status") != 1:
        _write_private(config_dir() / STATE_FILE, {**state, "captcha_id": 0})
        return {
            "ok": True, "next": "enter_email_code", "email": state["email"],
            "new_user": state["vtype"] == VTYPE_REGISTER,
            "message": f"Verification code sent to {state['email']}. Ask the user for it "
                       "(check spam too), then run: login.py verify --code <code>",
        }
    if not ent.get("captchaurl"):
        raise LoginError("The server asked for a captcha this script cannot show. Sign up on the website instead.")
    _write_private(config_dir() / STATE_FILE, {**state, "captcha_id": ent["captchaid"]})
    return {
        "ok": True, "next": "enter_captcha", "email": state["email"],
        "captcha_url": ent["captchaurl"], "captcha_file": _download_captcha(ent["captchaurl"]),
        "message": "Show the user this captcha image and ask them to type the characters, "
                   "then run: login.py captcha --code <what they typed>",
    }


def _download_captcha(url: str) -> str:
    """Best effort local copy for agents that render files rather than URLs."""
    target = config_dir() / CAPTCHA_FILE
    try:
        with urllib.request.urlopen(url, timeout=REQUEST_TIMEOUT) as resp:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(resp.read())
    except OSError:
        return ""
    return str(target)


def cmd_start(origin: str, args) -> dict:
    email = args.email.strip()
    if "@" not in email or len(email) < 5:
        raise LoginError(f"{email!r} is not an email address")
    did = "skill-" + uuid.uuid4().hex
    exists = _ent(_post(origin, EXIST_PATH, {"email": email, "cate": ACCOUNT_CATE}, did)).get("exist")
    state = {"origin": origin, "email": email, "did": did, "vtype": VTYPE_LOGIN if exists else VTYPE_REGISTER}
    return _send_code(origin, state)


def cmd_captcha(origin: str, args) -> dict:
    state = _load_state(origin)
    if not state.get("captcha_id"):
        raise LoginError("No captcha pending. Run login.py start --email <email> again.")
    try:
        return _send_code(origin, state, state["captcha_id"], args.code.strip())
    except LoginError as exc:
        # A wrong answer burns this captcha; start over to get a fresh image.
        raise LoginError(f"{str(exc).rstrip('.')}. Run login.py start --email {state['email']} for a new captcha.") from None


def cmd_verify(origin: str, args) -> dict:
    state = _load_state(origin)
    body = {"email": state["email"], "code": args.code.strip(), "cate": ACCOUNT_CATE,
            "h_src": SOURCE, "atype": ACCOUNT_TYPE, "srcreg": f"skill_{CHANNEL}"}
    session = _post(origin, CODE_LOGIN_PATH, body, state["did"])
    uid, token = session.get("mid"), session.get("token")
    if not uid or not token:
        raise LoginError("Login succeeded but returned no session. Try login.py start again.")
    api_key = _resolve_key(origin, state["did"], uid, token)
    _save_key(origin, state["email"], uid, api_key)
    (config_dir() / STATE_FILE).unlink(missing_ok=True)
    return {
        "ok": True, "email": state["email"], "new_user": not session.get("isold", True),
        "api_key_tail": api_key[-4:], "saved_to": str(config_dir() / CREDENTIALS_FILE),
        "message": "Logged in and API key saved. Re-run the command that needed it.",
    }


def _resolve_key(origin: str, did: str, uid: int, token: str) -> str:
    """Reuse this account's skill key if it has one, otherwise create it."""
    keys = _post(origin, KEY_LIST_PATH, {"tenant_id": 0, "member_uid": uid}, did, uid, token)
    for item in keys if isinstance(keys, list) else []:
        if item.get("name") == KEY_NAME and item.get("status") == KEY_ACTIVE and item.get("access_key"):
            return item["access_key"]
    created = _post(origin, KEY_CREATE_PATH, {"name": KEY_NAME, "tenant_id": 0, "expire_at": 0}, did, uid, token)
    if not created.get("access_key"):
        raise LoginError("Could not create an API key. Create one at https://adsturbo.ai/iris/api instead.")
    return created["access_key"]


def cmd_status(origin: str, args) -> dict:
    if os.environ.get("ADSTURBO_API_KEY"):
        return {"ok": True, "logged_in": True, "source": "ADSTURBO_API_KEY"}
    saved = _read_json(config_dir() / CREDENTIALS_FILE).get(origin) or {}
    if not load_saved_key(origin):
        return {"ok": True, "logged_in": False, "message": "Not logged in. Run login.py start --email <email>."}
    return {"ok": True, "logged_in": True, "source": "saved login", "email": saved.get("email"),
            "api_key_tail": saved["api_key"][-4:]}


def cmd_logout(origin: str, args) -> dict:
    path = config_dir() / CREDENTIALS_FILE
    saved = _read_json(path)
    if origin in saved:
        _write_private(path, {k: v for k, v in saved.items() if k != origin})
    return {"ok": True, "logged_in": False, "message": "Saved key removed from this machine (the key itself still works)."}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AdsTurbo sign-up / login inside the chat")
    sub = parser.add_subparsers(dest="command")

    start = sub.add_parser("start", help="send a verification code to this email")
    start.add_argument("--email", required=True)

    captcha = sub.add_parser("captcha", help="answer the image captcha, then send the email code")
    captcha.add_argument("--code", required=True)

    verify = sub.add_parser("verify", help="enter the emailed code; saves an API key")
    verify.add_argument("--code", required=True)

    sub.add_parser("status", help="is an API key available on this machine?")
    sub.add_parser("logout", help="forget the saved key on this machine")
    return parser


HANDLERS = {
    "start": cmd_start,
    "captcha": cmd_captcha,
    "verify": cmd_verify,
    "status": cmd_status,
    "logout": cmd_logout,
}


def main() -> None:
    # Not run_cli: that needs an API key up front, which is what this script obtains.
    parser = build_parser()
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)
    try:
        emit(HANDLERS[args.command](site_origin(resolve_base_url()), args))
    except LoginError as exc:
        print(f"Login failed: {exc}", file=sys.stderr)
        emit({"ok": False, "error": "login_failed", "message": str(exc)})
        sys.exit(1)
    except KeyboardInterrupt:
        print("Interrupted.", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()

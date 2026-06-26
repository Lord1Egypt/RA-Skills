#!/usr/bin/env python3
"""
Clawdible auth — two-step remote authentication for Audible.

Step 1 (generate login URL):
  python3 audible_auth.py [--locale LOCALE]
  → Prints a login URL. Open on any device and sign into Amazon.

Step 2 (complete auth with redirect URL):
  python3 audible_auth.py --callback '<redirect URL>'
  → Completes auth, saves credentials to ~/.config/audible/auth.json

Locale options: us, au, uk, de, ca, fr, in, it, jp, es (default: us)
"""

import sys
import json
import argparse
import subprocess
from pathlib import Path

# ── Dependency check & auto-install ──────────────────────────────────────────
def ensure_deps():
    missing = []
    for pkg in ["audible", "httpx"]:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"Installing missing dependencies: {', '.join(missing)}...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "--quiet"] + missing
            )
            print("Dependencies installed.\n")
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Failed to install dependencies: {e}")
            print(f"Run manually: pip3 install {' '.join(missing)}")
            sys.exit(1)

ensure_deps()

import audible
import httpx
from audible.login import build_oauth_url, create_code_verifier
from audible.register import register as register_
from audible.localization import Locale
from urllib.parse import parse_qs

CONFIG_DIR = Path.home() / ".config" / "audible"
AUTH_FILE = CONFIG_DIR / "auth.json"
STATE_FILE = CONFIG_DIR / "auth_state.json"


def cmd_start(locale_code):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    locale = Locale(locale_code)

    code_verifier = create_code_verifier()
    oauth_url, serial = build_oauth_url(
        country_code=locale.country_code,
        domain=locale.domain,
        market_place_id=locale.market_place_id,
        code_verifier=code_verifier,
    )

    # Save PKCE state — must be reused in step 2
    state = {
        "code_verifier": code_verifier.decode() if isinstance(code_verifier, bytes) else code_verifier,
        "serial": serial,
        "domain": locale.domain,
        "locale_code": locale_code,
    }
    STATE_FILE.write_text(json.dumps(state))
    STATE_FILE.chmod(0o600)

    print("=== Clawdible Login ===\n")
    print("Open this URL on your phone/browser and sign into Amazon:\n")
    print(oauth_url)
    print("\nAfter signing in, copy the full redirect URL")
    print("(starts with https://www.amazon.com/ap/maplanding...)")
    print("and run:")
    print(f"  python3 {__file__} --callback '<redirect URL>'")


def cmd_callback(callback_url):
    if not STATE_FILE.exists():
        print("ERROR: No pending auth session found.")
        print("Run without --callback first to generate a login URL.")
        sys.exit(1)

    try:
        state = json.loads(STATE_FILE.read_text())
    except Exception:
        print("ERROR: Auth state file is corrupt. Start again without --callback.")
        STATE_FILE.unlink(missing_ok=True)
        sys.exit(1)

    code_verifier = state["code_verifier"]
    if isinstance(code_verifier, str):
        code_verifier = code_verifier.encode()
    serial = state["serial"]
    domain = state["domain"]
    locale_code = state.get("locale_code", "us")

    # Parse the authorization code from redirect URL
    try:
        parsed = parse_qs(httpx.URL(callback_url).query.decode())
        auth_code = parsed.get("openid.oa2.authorization_code", [None])[0]
    except Exception:
        auth_code = None

    if not auth_code:
        print("ERROR: Could not find authorization code in the URL.")
        print("Make sure you copied the full redirect URL.")
        sys.exit(1)

    print("Registering device with Audible...")
    try:
        register_device = register_(
            authorization_code=auth_code,
            code_verifier=code_verifier,
            domain=domain,
            serial=serial,
            with_username=False,
        )
    except Exception as e:
        msg = str(e)
        if "InvalidValue" in msg or "expired" in msg.lower():
            print("ERROR: Auth code expired or invalid.")
            print("Auth codes are single-use and expire quickly.")
            print("Start again: run without --callback to get a fresh URL.")
            STATE_FILE.unlink(missing_ok=True)
        else:
            print(f"ERROR: Registration failed — {e}")
        sys.exit(1)

    locale = Locale(locale_code)
    auth = audible.Authenticator()
    auth.locale = locale
    auth._update_attrs(with_username=False, **register_device)

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    auth.to_file(AUTH_FILE, encryption=False)
    AUTH_FILE.chmod(0o600)

    STATE_FILE.unlink(missing_ok=True)
    print(f"✅ Authentication complete!")
    print(f"   Auth saved to: {AUTH_FILE}")
    print(f"   Locale: {locale_code}")
    print(f"\nVerify with: python3 audible_cli.py status --locale {locale_code}")


def main():
    parser = argparse.ArgumentParser(
        description="Clawdible auth — Audible two-step remote login"
    )
    parser.add_argument(
        "--locale", default="us",
        help="Marketplace locale (default: us). Options: us, au, uk, de, ca, fr, in, it, jp, es"
    )
    parser.add_argument(
        "--callback", metavar="URL",
        help="Complete auth with the Amazon redirect URL from step 2"
    )
    args = parser.parse_args()

    if args.callback:
        cmd_callback(args.callback)
    else:
        cmd_start(args.locale)


if __name__ == "__main__":
    main()

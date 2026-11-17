#!/usr/bin/env python3
"""
Garmin Connect authentication helper.
Handles login, token management, legacy migration, and rate-limit retry.

Provides:
  - get_client()       — return authenticated client from tokens or fresh login
  - login(email, pw)   — explicit login, saves tokens
  - check_status()     — verify saved tokens still work
  - CLI: status/login  — command-line entry points
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime
import argparse

try:
    from garminconnect import (
        Garmin,
        GarminConnectAuthenticationError,
        GarminConnectConnectionError,
        GarminConnectTooManyRequestsError,
    )
except ImportError as e:
    print(f"❌ garminconnect library not installed ({e})", file=sys.stderr)
    print("Install with: pip3 install garminconnect curl_cffi", file=sys.stderr)
    sys.exit(1)

# ── Paths ──────────────────────────────────────────────────────────────────
# NOTE: this must be the REAL path, not ~/.clawdbot.
# ~/.clawdbot is a symlink to ~/.openclaw, and garminconnect >= 0.3.15
# rejects any tokenstore with a symlinked ancestor in its path:
#   "Token path must not be a symlink: '/root/.clawdbot/garmin'"
# Both names point at the same directory, so no token migration is needed.
TOKEN_DIR = Path.home() / ".openclaw" / "garmin"
LEGACY_TOKEN_DIR = Path.home() / ".garminconnect"
CONFIG_FILE = Path(__file__).parent.parent / "config.json"

RETRY_SLEEP_SEC = 30          # seconds to wait before retrying a 429
MAX_RETRIES = 1               # one retry after sleep seems fair


# ── Config helpers ─────────────────────────────────────────────────────────

def load_config():
    """Load credentials from config.json next to this repo."""
    if not CONFIG_FILE.exists():
        return None
    try:
        with open(CONFIG_FILE) as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️  Failed to load config: {e}", file=sys.stderr)
        return None


def resolve_credentials(email=None, password=None):
    """
    Resolve credentials with priority:
      1. Explicit function args
      2. config.json file
      3. Environment variables GARMIN_EMAIL / GARMIN_PASSWORD
    Returns (email, password) or (None, None).
    """
    if email and password:
        return email, password

    config = load_config()
    if config:
        email = email or config.get("email")
        password = password or config.get("password")

    email = email or os.getenv("GARMIN_EMAIL")
    password = password or os.getenv("GARMIN_PASSWORD")
    return email, password


# ── Token management ───────────────────────────────────────────────────────

def _migrate_legacy_tokens():
    """
    Migrate tokens from legacy ~/.garminconnect/ to the current
    ~/.openclaw/garmin/ tokenstore.
    Silent if nothing to migrate.
    """
    if not LEGACY_TOKEN_DIR.exists():
        return
    if TOKEN_DIR.exists():
        return  # already migrated

    # Check if the legacy dir has garth-dump structure (directory-based)
    # or the old style garmin_tokens.json
    if (LEGACY_TOKEN_DIR / "garmin_tokens.json").exists():
        old_tokens = LEGACY_TOKEN_DIR / "garmin_tokens.json"
        try:
            data = json.loads(old_tokens.read_text())
            if isinstance(data, dict) and "access_token" in data:
                print("⚠️  Legacy garmin_tokens.json found — format too old, fresh login needed.",
                      file=sys.stderr)
                return
        except Exception:
            pass

    # Try garth-dumped directory (has sub-files like cookie.json, token.json)
    try:
        client = Garmin()
        client.login(str(LEGACY_TOKEN_DIR))
        # If that works, dump to new location
        TOKEN_DIR.mkdir(parents=True, exist_ok=True)
        client.client.dump(str(TOKEN_DIR))
        TOKEN_DIR.chmod(0o700)
        print(f"✅ Migrated tokens from {LEGACY_TOKEN_DIR} to {TOKEN_DIR}",
              file=sys.stderr)
    except Exception:
        pass  # migration failed, fresh login will happen


# ── Core auth functions ────────────────────────────────────────────────────

def _do_login(email, password):
    """Internal login, no proxy wrapper."""
    email, password = resolve_credentials(email, password)
    if not email or not password:
        print("❌ Email and password required", file=sys.stderr)
        return False

    try:
        print(f"🔐 Logging in as {email}...", file=sys.stderr)

        TOKEN_DIR.mkdir(parents=True, exist_ok=True)
        tokenstore = str(TOKEN_DIR)

        client = Garmin(email, password)
        # skip_strategies lives on the inner Client, NOT on the Garmin object,
        # and only exists in garminconnect >= 0.3.6 (absent in 0.3.3).
        # Assigning it on the Garmin object is silently discarded.
        #
        # Skip ONLY the two mobile strategies, which Garmin rate-limits (429)
        # from this IP. The previous set also skipped widget+cffi and
        # portal+cffi, which left portal+requests as the only candidate -- and
        # that one gets an intermittent Cloudflare 403 bot challenge, so
        # enabling the set (rather than silently dropping it) broke login.
        # Keeping the other three gives the fall-through chain room to work.
        if hasattr(client.client, "skip_strategies"):
            client.client.skip_strategies = {'mobile+cffi', 'mobile+requests'}
        client.login()
        client.client.dump(tokenstore)
        print(f"✅ Tokens saved to {tokenstore}", file=sys.stderr)

        # Verify
        try:
            profile = client.get_user_summary(datetime.now().strftime("%Y-%m-%d"))
            print(f"✅ Login successful! User: {profile.get('displayName', 'Unknown')}",
                  file=sys.stderr)
        except Exception as e:
            print(f"✅ Login successful! (Unable to fetch profile: {e})",
                  file=sys.stderr)

        TOKEN_DIR.chmod(0o700)
        return True

    except GarminConnectTooManyRequestsError:
        print("❌ Garmin rate-limited this IP (429).", file=sys.stderr)
        print("   Wait ~30 minutes and retry, or use a different network/VPN.",
              file=sys.stderr)
        return False
    except GarminConnectAuthenticationError as e:
        print(f"❌ Authentication failed: {e}", file=sys.stderr)
        print("   Check your email/password and try again.", file=sys.stderr)
        return False
    except GarminConnectConnectionError as e:
        print(f"❌ Connection error: {e}", file=sys.stderr)
        print("   Check your internet connection and Garmin server status.",
              file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ Login error: {e}", file=sys.stderr)
        return False


def login(email, password):
    """Perform login. Traffic routes through NordVPN (Spain) for Garmin."""
    email, password = resolve_credentials(email, password)
    if not email or not password:
        print("❌ Email and password required", file=sys.stderr)
        return False

    return _do_login(email, password)


def get_client():
    """
    Return an authenticated Garmin client.

    Strategy:
      1. Load saved tokens from TOKEN_DIR (with legacy migration on first call)
      2. If tokens expired, do a fresh login using config / env credentials
      3. On 429, retry once after RETRY_SLEEP_SEC seconds
    Returns Garmin client or None.
    """
    # Migrate legacy tokens on first invocation
    _migrate_legacy_tokens()

    tokenstore = str(TOKEN_DIR)

    # ── Attempt 1: saved tokens ──
    if TOKEN_DIR.exists():
        for attempt in range(MAX_RETRIES + 1):
            try:
                client = Garmin()
                client.login(tokenstore=tokenstore)
                client.get_user_summary(datetime.now().strftime("%Y-%m-%d"))
                return client
            except GarminConnectTooManyRequestsError:
                if attempt < MAX_RETRIES:
                    print(f"⚠️  429 rate limit — retrying in {RETRY_SLEEP_SEC}s...",
                          file=sys.stderr)
                    time.sleep(RETRY_SLEEP_SEC)
                else:
                    print("❌ Garmin rate-limited after retry (429).", file=sys.stderr)
                    return None
            except Exception as e:
                # Tokens expired / invalid — fall through to fresh login
                break  # single break, then try fresh login

    # ── Attempt 2: fresh login with credentials ──
    email, password = resolve_credentials()
    if not email or not password:
        print("❌ No saved tokens or credentials available.", file=sys.stderr)
        print("   Run: python3 scripts/garmin_auth.py login", file=sys.stderr)
        return None

    print("ℹ️  Saved tokens expired — performing fresh login...", file=sys.stderr)
    if login(email, password):
        # Retry with fresh tokens
        try:
            client = Garmin()
            client.login(tokenstore=tokenstore)
            client.get_user_summary(datetime.now().strftime("%Y-%m-%d"))
            return client
        except Exception as e:
            print(f"❌ Fresh login succeeded but client failed: {e}", file=sys.stderr)
            return None

    return None


def check_status():
    """Check if we have valid authentication."""
    if not TOKEN_DIR.exists():
        _migrate_legacy_tokens()

    if not TOKEN_DIR.exists():
        print("❌ Not authenticated — no token store found.", file=sys.stderr)
        print("   Run: python3 scripts/garmin_auth.py login", file=sys.stderr)
        return False

    print(f"✅ Token store found at {TOKEN_DIR}", file=sys.stderr)

    client = get_client()
    if client:
        try:
            profile = client.get_user_summary(datetime.now().strftime("%Y-%m-%d"))
            print(f"✅ Authentication valid! User: {profile.get('displayName', 'Unknown')}",
                  file=sys.stderr)
            return True
        except Exception as e:
            print(f"⚠️  Token verification failed: {e}", file=sys.stderr)
            return False

    print("❌ Authentication invalid.", file=sys.stderr)
    return False


# ── CLI entry point ────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Garmin Connect authentication")
    subparsers = parser.add_subparsers(dest="command", help="Command")

    login_parser = subparsers.add_parser("login", help="Login to Garmin Connect")
    login_parser.add_argument("--email", help="Garmin account email")
    login_parser.add_argument("--password", help="Garmin account password")

    subparsers.add_parser("status", help="Check authentication status")

    args = parser.parse_args()

    if args.command == "login":
        email, password = resolve_credentials(args.email, args.password)
        if not email or not password:
            print("❌ Email and password required", file=sys.stderr)
            print("   Set via:", file=sys.stderr)
            print("   1. CLI: --email / --password", file=sys.stderr)
            print("   2. File: config.json in repo root", file=sys.stderr)
            print("   3. Env:  GARMIN_EMAIL / GARMIN_PASSWORD", file=sys.stderr)
            sys.exit(1)
        success = login(email, password)
        sys.exit(0 if success else 1)

    elif args.command == "status":
        success = check_status()
        sys.exit(0 if success else 1)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
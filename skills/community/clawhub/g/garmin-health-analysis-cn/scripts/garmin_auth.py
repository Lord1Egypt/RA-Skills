#!/usr/bin/env python3
"""
Garmin Connect authentication helper.
Handles login and stores session tokens.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
import argparse

try:
    from garminconnect import Garmin, GarminConnectAuthenticationError, GarminConnectConnectionError
except ImportError:
    print("❌ garminconnect library not installed", file=sys.stderr)
    print("Install with: pip3 install garminconnect", file=sys.stderr)
    sys.exit(1)

TOKEN_DIR = Path(
    os.environ.get("GARMIN_TOKEN_DIR") or Path.home() / ".garmin-health-analysis-cn" / "tokens"
)
CONFIG_FILE = Path(__file__).parent.parent / "config.json"
META_FILE = TOKEN_DIR / "meta.json"


def load_config():
    """Load credentials from config file."""
    if not CONFIG_FILE.exists():
        return None
    try:
        with open(CONFIG_FILE) as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️  Failed to load config: {e}", file=sys.stderr)
        return None


def _write_meta(is_cn):
    """Persist the region used at login time.

    Tokens are issued by the domain matching `is_cn` (connect.garmin.cn vs
    connect.garmin.com). Recording it here lets token reuse always reconnect
    to the same domain, independent of later config/env changes.
    """
    try:
        TOKEN_DIR.mkdir(parents=True, exist_ok=True)
        meta = {
            "is_cn": bool(is_cn),
            "login_at": datetime.now().isoformat(timespec="seconds"),
        }
        with open(META_FILE, "w") as f:
            json.dump(meta, f, indent=2)
    except Exception as e:
        print(f"⚠️  Failed to save login meta: {e}", file=sys.stderr)


def _read_meta():
    """Read persisted login metadata (region used when tokens were issued)."""
    if not META_FILE.exists():
        return None
    try:
        with open(META_FILE) as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️  Failed to load login meta: {e}", file=sys.stderr)
        return None


def resolve_is_cn():
    """Resolve CN mode for token reuse.

    Priority: login-time meta (tokens were issued for that domain) >
    GARMIN_IS_CN env > config.json (legacy fallback). This mirrors the region
    actually used at login so generation and reuse stay consistent.
    """
    meta = _read_meta()
    if meta and "is_cn" in meta:
        return bool(meta["is_cn"])

    env_cn = os.environ.get("GARMIN_IS_CN")
    if env_cn is not None:
        return env_cn.strip().lower() in ("1", "true", "yes", "on", "cn")

    config = load_config()
    if config and config.get("is_cn"):
        return True
    return False


def login(email, password, is_cn=False):
    """Perform login and save tokens using garminconnect's tokenstore."""
    try:
        print(f"🔐 Logging in as {email}... (CN: {is_cn})", file=sys.stderr)

        # Create token directory
        TOKEN_DIR.mkdir(parents=True, exist_ok=True)
        tokenstore = str(TOKEN_DIR)

        # Create client and login (don't pass tokenstore on first login)
        client = Garmin(email, password, is_cn=is_cn)
        client.login()  # Initial login without tokenstore
        
        # Save tokens to tokenstore (new garminconnect: garth client at .client)
        garth = getattr(client, "garth", None) or client.client
        garth.dump(tokenstore)
        print(f"✅ Tokens saved to {tokenstore}", file=sys.stderr)

        # Persist the region used so token reuse reconnects to the same domain
        _write_meta(is_cn)
        
        # Test the connection
        try:
            profile = client.get_user_summary(datetime.now().strftime("%Y-%m-%d"))
            print(f"✅ Login successful! User: {profile.get('displayName', 'Unknown')}", file=sys.stderr)
        except Exception as e:
            print(f"✅ Login successful! (Unable to fetch profile: {e})", file=sys.stderr)
        
        # Make tokenstore directory secure
        TOKEN_DIR.chmod(0o700)
        
        return True
        
    except GarminConnectAuthenticationError as e:
        print(f"❌ Authentication failed: {e}", file=sys.stderr)
        print("Check your email/password and try again.", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ Login error: {e}", file=sys.stderr)
        return False


def _client_from_tokens(is_cn):
    """Build a client from saved tokens and verify it works."""
    client = Garmin(is_cn=is_cn)
    client.login(tokenstore=str(TOKEN_DIR))
    client.get_user_summary(datetime.now().strftime("%Y-%m-%d"))
    return client


def get_client():
    """Get authenticated Garmin client, using saved tokens if available.

    Region is resolved via resolve_is_cn() (login-time meta > env > config)
    so tokens are always replayed against the domain that issued them.
    If tokens are invalid, tries one automatic re-login using config.json
    credentials before giving up.
    """
    if not TOKEN_DIR.exists():
        return None

    is_cn = resolve_is_cn()

    try:
        return _client_from_tokens(is_cn)
    except Exception as e:
        print(f"⚠️  Saved tokens expired or invalid: {e}", file=sys.stderr)

    # Tokens unusable: attempt one automatic re-login with config credentials
    config = load_config()
    if config and config.get("email") and config.get("password"):
        print("🔄 Trying automatic re-login with config.json credentials...", file=sys.stderr)
        if login(config["email"], config["password"], is_cn=is_cn):
            try:
                return _client_from_tokens(is_cn)
            except Exception as e:
                print(f"⚠️  Re-login succeeded but token reuse failed: {e}", file=sys.stderr)

    return None


def check_status():
    """Check if we have valid authentication."""
    tokenstore = str(TOKEN_DIR)
    
    if not TOKEN_DIR.exists():
        print("❌ Not authenticated", file=sys.stderr)
        print("Run: python3 scripts/garmin_auth.py login", file=sys.stderr)
        return False
    
    print(f"✅ Token store found at {tokenstore}", file=sys.stderr)

    # Show which server region tokens will be replayed against
    region = "CN (connect.garmin.cn)" if resolve_is_cn() else "Global (connect.garmin.com)"
    print(f"ℹ️  Server region for token reuse: {region}", file=sys.stderr)
    
    # Test if they work
    client = get_client()
    if client:
        try:
            profile = client.get_user_summary(datetime.now().strftime("%Y-%m-%d"))
            print(f"✅ Authentication valid! User: {profile.get('displayName', 'Unknown')}", file=sys.stderr)
            return True
        except Exception as e:
            print(f"⚠️  Tokens may be expired: {e}", file=sys.stderr)
            return False
    
    print("❌ Authentication invalid. Please login again.", file=sys.stderr)
    return False


def main():
    parser = argparse.ArgumentParser(description="Garmin Connect authentication")
    subparsers = parser.add_subparsers(dest="command", help="Command")
    
    # Login command
    login_parser = subparsers.add_parser("login", help="Login to Garmin Connect")
    login_parser.add_argument("--email", help="Garmin account email (or set via env/config)")
    login_parser.add_argument("--password", help="Garmin account password (or set via env/config)")
    login_parser.add_argument("--cn", action="store_true", help="Use Garmin Connect China (connect.garmin.cn)")
    
    # Status command
    subparsers.add_parser("status", help="Check authentication status")
    
    args = parser.parse_args()
    
    if args.command == "login":
        email = args.email
        password = args.password
        is_cn = args.cn

        # Priority: CLI args > config.json > environment variables
        # Only fall back to config when credentials are missing from CLI/env,
        # so an explicitly CLI-provided login never gets its region overwritten.
        if not email or not password:
            config = load_config()
            if config:
                email = email or config.get("email")
                password = password or config.get("password")
                is_cn = is_cn or bool(config.get("is_cn"))
        
        if not email or not password:
            email = email or os.getenv("GARMIN_EMAIL")
            password = password or os.getenv("GARMIN_PASSWORD")
        
        if not email or not password:
            print("❌ Email and password required", file=sys.stderr)
            print("Set via:", file=sys.stderr)
            print("  1. CLI: --email and --password", file=sys.stderr)
            print("  2. Config: create config.json from config.example.json", file=sys.stderr)
            print("  3. Env vars: GARMIN_EMAIL and GARMIN_PASSWORD", file=sys.stderr)
            print("  4. AI assistant skill config (e.g. OpenClaw: skills.entries.garmin-health-analysis-cn.env)", file=sys.stderr)
            sys.exit(1)
        
        success = login(email, password, is_cn=is_cn)
        sys.exit(0 if success else 1)
    
    elif args.command == "status":
        success = check_status()
        sys.exit(0 if success else 1)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

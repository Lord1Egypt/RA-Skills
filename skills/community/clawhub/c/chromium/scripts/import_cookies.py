#!/usr/bin/env python3
"""
Import browser cookies into the OpenClaw headless Chromium profile.

Usage:
  python3 import_cookies.py cookies.json [--domain x.com]

Cookie JSON format (from Cookie-Editor, EditThisCookie, etc.):
  [
    {"name": "auth_token", "value": "...", "domain": ".x.com", "path": "/", ...},
    ...
  ]

After import, navigate to the target site in the browser to verify.
"""

import json
import sys
import os
import argparse
import urllib.request
import urllib.error

# OpenClaw gateway browser control port = gateway port + 2
GATEWAY_PORT = int(os.environ.get("OPENCLAW_GATEWAY_PORT", 18792))
BROWSER_CONTROL_PORT = GATEWAY_PORT + 2


def get_gateway_token():
    """Read gateway auth token from OpenClaw config."""
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    if not os.path.exists(config_path):
        return ""
    with open(config_path) as f:
        cfg = json.load(f)
    return cfg.get("gateway", {}).get("auth", {}).get("token", "")


def set_cookie(token: str, cookie: dict, profile: str) -> bool:
    url = f"http://127.0.0.1:{BROWSER_CONTROL_PORT}/cookies/set?profile={profile}"
    payload = json.dumps({"cookie": cookie}).encode()
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            result = json.loads(resp.read())
            return result.get("ok", False)
    except Exception as e:
        print(f"  ERROR: {e}", file=sys.stderr)
        return False


def normalize_cookie(raw: dict) -> dict:
    """Normalize cookie from various export formats to CDP format."""
    cookie = {}

    cookie["name"] = raw.get("name", raw.get("Name", ""))
    cookie["value"] = raw.get("value", raw.get("Value", ""))

    domain = raw.get("domain", raw.get("Domain", raw.get("host", "")))
    if domain and not domain.startswith(".") and not domain.startswith("http"):
        domain = "." + domain
    cookie["domain"] = domain

    cookie["path"] = raw.get("path", raw.get("Path", "/"))

    expires = raw.get("expirationDate", raw.get("expires", raw.get("Expires")))
    if expires and isinstance(expires, (int, float)) and expires > 0:
        cookie["expires"] = int(expires)

    cookie["httpOnly"] = bool(raw.get("httpOnly", raw.get("HttpOnly", False)))
    cookie["secure"] = bool(raw.get("secure", raw.get("Secure", False)))

    samesite = raw.get("sameSite", raw.get("SameSite", ""))
    if samesite:
        cookie["sameSite"] = samesite.capitalize()

    return cookie


def main():
    parser = argparse.ArgumentParser(description="Import cookies into OpenClaw Chromium")
    parser.add_argument("cookies_file", help="Path to cookies JSON file")
    parser.add_argument("--profile", default="default", help="Browser profile name (default: default)")
    parser.add_argument("--domain", default=None, help="Filter cookies by domain (e.g. x.com)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be imported")
    args = parser.parse_args()

    with open(args.cookies_file) as f:
        raw_cookies = json.load(f)

    if not isinstance(raw_cookies, list):
        print("ERROR: Cookie file must be a JSON array", file=sys.stderr)
        sys.exit(1)

    if args.domain:
        filter_domain = args.domain.lstrip(".")
        raw_cookies = [
            c for c in raw_cookies
            if filter_domain in c.get("domain", c.get("Domain", c.get("host", "")))
        ]
        print(f"Filtered to {len(raw_cookies)} cookies for domain: {args.domain}")

    token = get_gateway_token()
    if not token and not args.dry_run:
        print("ERROR: Could not read gateway token from ~/.openclaw/openclaw.json", file=sys.stderr)
        print("Make sure OpenClaw gateway is configured and running.", file=sys.stderr)
        sys.exit(1)

    print(f"Importing {len(raw_cookies)} cookies into profile '{args.profile}'...")
    print()

    ok_count = 0
    fail_count = 0

    for raw in raw_cookies:
        cookie = normalize_cookie(raw)
        name = cookie.get("name", "")
        domain = cookie.get("domain", "")
        label = f"{name} ({domain})"

        if args.dry_run:
            print(f"  DRY-RUN: {label}")
            ok_count += 1
            continue

        ok = set_cookie(token, cookie, args.profile)
        if ok:
            print(f"  OK:   {label}")
            ok_count += 1
        else:
            print(f"  FAIL: {label}")
            fail_count += 1

    print()
    print(f"Done: {ok_count} imported, {fail_count} failed")


if __name__ == "__main__":
    main()

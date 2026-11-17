#!/usr/bin/env python3
"""EVE SSO OAuth2 PKCE authentication flow.

Usage:
    python auth_flow.py --client-id <CLIENT_ID> [--char-name <NAME>] [--port 8080]

Stores refresh token to $OPENCLAW_STATE_DIR/eve-tokens.json (default: ~/.openclaw/)
"""
import argparse
import base64
import hashlib
import http.server
import json
import os
import secrets
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request

from token_store import get_tokens_file, load_tokens, save_tokens_unlocked, token_file_lock
from user_agent import USER_AGENT

class AuthFlowError(Exception):
    """Raised when the OAuth authentication flow fails."""


# Scopes are granted once at login and persist until the token is revoked at
# https://community.eveonline.com/support/third-party/ — so the default asks for
# the narrow set needed to monitor planets, not for everything the API offers.
# Widen deliberately with --scope-profile or --scopes.

_BASIC = [
    "esi-skills.read_skills.v1",
    "esi-skills.read_skillqueue.v1",
    "esi-clones.read_clones.v1",
    "esi-clones.read_implants.v1",
    "esi-location.read_location.v1",
    "esi-location.read_ship_type.v1",
    "esi-location.read_online.v1",
]

SCOPE_PROFILES = {
    # Character basics: training, clones, where you are and in what.
    "basic": _BASIC,
    # Default. Planetary Interaction monitoring on top of the basics.
    "pi": _BASIC + [
        "esi-planets.manage_planets.v1",
    ],
    # Production and hauling: what you own, what you are building and selling.
    "industry": _BASIC + [
        "esi-assets.read_assets.v1",
        "esi-industry.read_character_jobs.v1",
        "esi-markets.read_character_orders.v1",
        "esi-contracts.read_character_contracts.v1",
    ],
    # Everything this skill knows how to use — including wallet and mail.
    # Only pick this if you actually want an agent reading your correspondence.
    "full": _BASIC + [
        "esi-planets.manage_planets.v1",
        "esi-assets.read_assets.v1",
        "esi-industry.read_character_jobs.v1",
        "esi-markets.read_character_orders.v1",
        "esi-contracts.read_character_contracts.v1",
        "esi-wallet.read_character_wallet.v1",
        "esi-characters.read_notifications.v1",
        "esi-characters.read_fatigue.v1",
        "esi-killmails.read_killmails.v1",
        "esi-mail.read_mail.v1",
    ],
}

DEFAULT_SCOPE_PROFILE = "pi"


def pkce_pair():
    verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(verifier.encode()).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
    return verifier, challenge


def exchange_code(code, verifier, client_id, redirect_uri):
    data = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": code,
        "client_id": client_id,
        "code_verifier": verifier,
        "redirect_uri": redirect_uri,
    }).encode()
    req = urllib.request.Request(
        "https://login.eveonline.com/v2/oauth/token",
        data=data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise AuthFlowError(f"Token exchange failed ({e.code}): {body}")
    except urllib.error.URLError as e:
        raise AuthFlowError(f"Could not connect to EVE login server: {e.reason}")


def verify_token(access_token):
    # /v2/oauth/verify is what the SSO metadata document at
    # https://login.eveonline.com/.well-known/oauth-authorization-server names as
    # the userinfo endpoint; the unversioned /oauth/verify is the older one.
    req = urllib.request.Request(
        "https://login.eveonline.com/v2/oauth/verify",
        headers={
            "Authorization": f"Bearer {access_token}",
            "User-Agent": USER_AGENT,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise AuthFlowError(f"Token verification failed ({e.code}): {body}")
    except urllib.error.URLError as e:
        raise AuthFlowError(f"Could not connect to EVE login server: {e.reason}")


def main():
    parser = argparse.ArgumentParser(description="EVE SSO OAuth2 PKCE auth flow")
    parser.add_argument("--client-id", required=True,
                        help="EVE Developer App Client ID")
    parser.add_argument("--char-name", default="main",
                        help="Short name to save this character as (e.g. 'main', 'alt1')")
    parser.add_argument("--port", type=int, default=8080,
                        help="Local callback port (default: 8080)")
    parser.add_argument("--timeout", type=int, default=300,
                        help="Seconds to wait for browser callback (default: 300)")
    parser.add_argument("--scope-profile", default=DEFAULT_SCOPE_PROFILE,
                        choices=sorted(SCOPE_PROFILES),
                        help=f"Which permissions to request (default: {DEFAULT_SCOPE_PROFILE}). "
                             "'full' includes wallet and mail.")
    parser.add_argument("--scopes",
                        help="Explicit space-separated scope list, overrides --scope-profile")
    parser.add_argument("--list-scope-profiles", action="store_true",
                        help="Show what each profile requests, then exit")
    args = parser.parse_args()

    if args.list_scope_profiles:
        for name, scopes in SCOPE_PROFILES.items():
            marker = "  (default)" if name == DEFAULT_SCOPE_PROFILE else ""
            print(f"\n{name}{marker} — {len(scopes)} scopes")
            for s in scopes:
                print(f"    {s}")
        return

    if args.scopes:
        scopes = args.scopes.split()
    else:
        scopes = SCOPE_PROFILES[args.scope_profile]
    scope_string = " ".join(scopes)

    # Say out loud what is about to be handed over — these persist until revoked.
    source = "--scopes" if args.scopes else f"profile '{args.scope_profile}'"
    print(f"Requesting {len(scopes)} scopes ({source}):")
    for s in scopes:
        print(f"  {s}")
    print("\nThese remain granted until you revoke them at")
    print("https://community.eveonline.com/support/third-party/")
    if not args.scopes and args.scope_profile != "full":
        others = [n for n in SCOPE_PROFILES if n != args.scope_profile]
        print(f"Need more? --scope-profile {{{','.join(sorted(others))}}} "
              "or --list-scope-profiles\n")
    else:
        print()

    verifier, challenge = pkce_pair()
    state = secrets.token_urlsafe(16)
    # Must be the literal host `localhost`, not 127.0.0.1: the EVE developer
    # portal only accepts the http scheme for `localhost` and rejects an IP
    # address outright, so a callback URL with 127.0.0.1 cannot be registered
    # in the first place. SSO then matches this string exactly against what is
    # registered. The callback server below still binds to 127.0.0.1 — that is
    # the address the SSH tunnel forwards to, and is unrelated to the name the
    # browser resolves.
    redirect_uri = f"http://localhost:{args.port}/callback"

    auth_url = (
        "https://login.eveonline.com/v2/oauth/authorize/?"
        + urllib.parse.urlencode({
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "client_id": args.client_id,
            "scope": scope_string,
            "state": state,
            "code_challenge": challenge,
            "code_challenge_method": "S256",
        })
    )

    result = {}

    class CallbackHandler(http.server.BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass  # suppress default logs

        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path != "/callback":
                self.send_response(404)
                self.end_headers()
                return

            params = urllib.parse.parse_qs(parsed.query)
            code = params.get("code", [None])[0]
            got_state = params.get("state", [None])[0]

            if got_state != state:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"State mismatch. Try again.")
                return

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h2>Authorized! You can close this tab.</h2>")
            result["code"] = code
            threading.Thread(target=self.server.shutdown).start()

    try:
        httpd = http.server.HTTPServer(("127.0.0.1", args.port), CallbackHandler)
    except OSError as e:
        raise AuthFlowError(
            f"Could not start callback server on 127.0.0.1:{args.port}: {e}"
        ) from e

    print(f"\n{'='*60}")
    print("EVE SSO Auth Flow")
    print(f"{'='*60}")
    print(f"\nIf running on a remote server, set up SSH tunnel first:")
    print(f"  ssh -L {args.port}:127.0.0.1:{args.port} user@your-server -N")
    print(f"\nThen open this URL in your browser:")
    print(f"\n  {auth_url}\n")
    print(f"Waiting for callback on port {args.port} (timeout: {args.timeout}s)...")
    print(f"{'='*60}\n")

    timeout_timer = threading.Timer(args.timeout, httpd.shutdown)
    timeout_timer.daemon = True
    timeout_timer.start()
    httpd.serve_forever()
    timeout_timer.cancel()

    if not result.get("code"):
        raise AuthFlowError("Timed out waiting for browser callback.")

    print("Auth code received. Exchanging for tokens...")
    token_data = exchange_code(result["code"], verifier, args.client_id, redirect_uri)

    print("Verifying token...")
    char_info = verify_token(token_data["access_token"])

    char_id = char_info["CharacterID"]
    char_name = char_info["CharacterName"]

    with token_file_lock():
        tokens = load_tokens()
        tokens["characters"][args.char_name] = {
            "character_id": char_id,
            "character_name": char_name,
            "client_id": args.client_id,
            "refresh_token": token_data["refresh_token"],
        }
        save_tokens_unlocked(tokens)

    print(f"\n✓ Authenticated as: {char_name} (ID: {char_id})")
    print(f"✓ Saved as key: '{args.char_name}'")
    print(f"✓ Tokens stored in: {get_tokens_file()}")
    print(f"\nUsage:")
    print(f"  python get_token.py --char {args.char_name}")


if __name__ == "__main__":
    try:
        main()
    except AuthFlowError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

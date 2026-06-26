import argparse
import json
import secrets
import threading
import time
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests

from freesound_config import (
    AUTHORIZE_URL,
    TOKEN_URL,
    DEFAULT_REDIRECT_URI,
    load_config,
    save_config,
)


class CallbackHandler(BaseHTTPRequestHandler):
    server_version = "FreesoundOAuth/1.0"

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        self.server.oauth_result = {
            "code": params.get("code", [None])[0],
            "state": params.get("state", [None])[0],
            "error": params.get("error", [None])[0],
        }
        body = b"Freesound login received. You can close this tab and return to OpenClaw."
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


def main() -> None:
    parser = argparse.ArgumentParser(description="Complete Freesound OAuth login.")
    parser.add_argument("--redirect-uri", default=None)
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()

    cfg = load_config()
    client_id = cfg.get("client_id")
    client_secret = cfg.get("client_secret")
    redirect_uri = args.redirect_uri or cfg.get("redirect_uri") or DEFAULT_REDIRECT_URI

    if not client_id or not client_secret:
        raise SystemExit("Missing client_id/client_secret. Run setup_credentials.py first.")

    parsed_redirect = urllib.parse.urlparse(redirect_uri)
    if parsed_redirect.scheme != "http" or parsed_redirect.hostname not in {"localhost", "127.0.0.1"}:
        raise SystemExit("This helper expects a localhost redirect URI.")

    port = parsed_redirect.port or 80
    state = secrets.token_urlsafe(24)

    server = HTTPServer((parsed_redirect.hostname, port), CallbackHandler)
    server.oauth_result = None

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    query = urllib.parse.urlencode(
        {
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "state": state,
        }
    )
    auth_url = f"{AUTHORIZE_URL}?{query}"
    print("Open this URL if the browser does not open automatically:\n")
    print(auth_url)
    webbrowser.open(auth_url)

    deadline = time.time() + args.timeout
    try:
        while time.time() < deadline:
            if server.oauth_result is not None:
                break
            time.sleep(0.25)
    finally:
        server.shutdown()
        server.server_close()

    result = server.oauth_result
    if not result:
        raise SystemExit("Timed out waiting for Freesound callback.")
    if result.get("error"):
        raise SystemExit(f"Freesound returned error: {result['error']}")
    if result.get("state") != state:
        raise SystemExit("State mismatch in callback.")
    code = result.get("code")
    if not code:
        raise SystemExit("No authorization code received.")

    token_resp = requests.post(
        TOKEN_URL,
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        },
        timeout=30,
    )
    token_resp.raise_for_status()
    token_data = token_resp.json()

    cfg["redirect_uri"] = redirect_uri
    cfg["token"] = token_data
    save_config(cfg)
    print(json.dumps({"saved": True, "token_type": token_data.get("token_type"), "scope": token_data.get("scope")}, indent=2))


if __name__ == "__main__":
    main()

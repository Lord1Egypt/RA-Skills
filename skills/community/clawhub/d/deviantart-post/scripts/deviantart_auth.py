from __future__ import annotations

import base64
import hashlib
import json
import secrets
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

from deviantart_common import (
    DeviantArtError,
    TOKEN_PATH,
    TOKEN_URL,
    USER_AGENT,
    load_app_credentials,
    read_response_text,
    save_json,
)


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    server_version = "OpenClawDeviantArt/0.1"

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)
        self.server.auth_query = query  # type: ignore[attr-defined]
        body = "Authorization received. You can close this window."
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body.encode("utf-8"))))
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def log_message(self, format, *args):
        return


def exchange_code(app: dict, code: str, code_verifier: str) -> dict:
    payload = {
        "grant_type": "authorization_code",
        "client_id": str(app["client_id"]),
        "code": code,
        "redirect_uri": app["redirect_uri"],
        "code_verifier": code_verifier,
    }
    if app.get("client_secret"):
        payload["client_secret"] = app["client_secret"]

    encoded = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(
        TOKEN_URL,
        data=encoded,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            body = read_response_text(resp)
    except urllib.error.HTTPError as e:
        body = read_response_text(e)
        raise DeviantArtError(f"HTTP {e.code} from token exchange: {body}") from e
    try:
        token = json.loads(body)
    except json.JSONDecodeError as e:
        raise DeviantArtError(f"Non-JSON token response: {body[:500]}") from e
    if token.get("error"):
        raise DeviantArtError(token.get("error_description") or token["error"])
    token["obtained_at"] = time.time()
    token["expires_at"] = time.time() + int(token.get("expires_in", 3600))
    return token


def main() -> int:
    app = load_app_credentials()
    redirect_uri = app["redirect_uri"]
    parsed_redirect = urllib.parse.urlparse(redirect_uri)
    host = parsed_redirect.hostname or "127.0.0.1"
    port = parsed_redirect.port or 8765

    code_verifier = secrets.token_urlsafe(64)
    code_challenge = b64url(hashlib.sha256(code_verifier.encode("ascii")).digest())
    state = secrets.token_urlsafe(24)
    scope = " ".join(app.get("scopes") or ["stash", "publish"])

    auth_query = urllib.parse.urlencode(
        {
            "response_type": "code",
            "client_id": str(app["client_id"]),
            "redirect_uri": redirect_uri,
            "scope": scope,
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }
    )
    auth_url = f"https://www.deviantart.com/oauth2/authorize?{auth_query}"

    httpd = HTTPServer((host, port), OAuthCallbackHandler)
    httpd.auth_query = None  # type: ignore[attr-defined]
    thread = threading.Thread(target=httpd.handle_request, daemon=True)
    thread.start()

    print(f"Open this URL if your browser does not open automatically:\n{auth_url}\n")
    webbrowser.open(auth_url)
    print(f"Waiting for callback on {host}:{port} ...")

    deadline = time.time() + 300
    while time.time() < deadline:
        query = getattr(httpd, "auth_query", None)
        if query:
            if "error" in query:
                raise DeviantArtError(query.get("error_description", query["error"])[0])
            returned_state = query.get("state", [None])[0]
            if returned_state != state:
                raise DeviantArtError("OAuth state mismatch")
            code = query.get("code", [None])[0]
            if not code:
                raise DeviantArtError("OAuth callback did not include a code")
            token = exchange_code(app, code, code_verifier)
            save_json(TOKEN_PATH, token)
            print(f"Saved token to: {TOKEN_PATH}")
            print("Authorization successful.")
            return 0
        time.sleep(0.25)

    raise DeviantArtError(
        "Timed out waiting for OAuth callback. Re-run the script and complete login faster."
    )


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except DeviantArtError as e:
        message = f"ERROR: {e}"
        try:
            print(message)
        except UnicodeEncodeError:
            safe = message.encode("ascii", errors="backslashreplace").decode("ascii")
            print(safe)
        raise SystemExit(1)

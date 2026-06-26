"""OAuth helpers for the Dida365 OpenAPI CLI."""

from __future__ import annotations

import base64
import secrets
import threading
import time
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Optional
from urllib.parse import parse_qs, urlencode, urlparse

from .config import RuntimeSettings
from .errors import UserFacingError
from .http import HttpTransport


@dataclass
class CallbackResult:
    code: str
    state: Optional[str]
    query: dict[str, list[str]]


def build_authorize_url(settings: RuntimeSettings, state: Optional[str] = None) -> str:
    if not settings.client_id:
        raise UserFacingError("client_id is required to build the authorization URL")
    if not settings.redirect_uri:
        raise UserFacingError("redirect_uri is required to build the authorization URL")

    query = {
        "client_id": settings.client_id,
        "scope": settings.scope,
        "state": state or "",
        "redirect_uri": settings.redirect_uri,
        "response_type": "code",
    }
    base = settings.auth_base_url.rstrip("/")
    return f"{base}/oauth/authorize?{urlencode(query)}"


def exchange_code(
    settings: RuntimeSettings,
    *,
    code: str,
    transport: Optional[HttpTransport] = None,
) -> dict[str, Any]:
    if not settings.client_id:
        raise UserFacingError("client_id is required to exchange an authorization code")
    if not settings.client_secret:
        raise UserFacingError("client_secret is required to exchange an authorization code")
    if not settings.redirect_uri:
        raise UserFacingError("redirect_uri is required to exchange an authorization code")

    basic_auth = base64.b64encode(f"{settings.client_id}:{settings.client_secret}".encode("utf-8")).decode("ascii")
    client = transport or HttpTransport()
    response = client.request(
        "POST",
        f"{settings.auth_base_url.rstrip('/')}/oauth/token",
        headers={"Authorization": f"Basic {basic_auth}"},
        form_body={
            "code": code,
            "grant_type": "authorization_code",
            "scope": settings.scope,
            "redirect_uri": settings.redirect_uri,
        },
        timeout=settings.timeout,
    )
    if not isinstance(response.data, dict):
        raise UserFacingError("Token endpoint did not return a JSON object", exit_code=1)
    return response.data


def generate_state_token() -> str:
    return secrets.token_urlsafe(24)


def derive_local_redirect_uri(redirect_uri: Optional[str]) -> tuple[str, int, str, str]:
    candidate = redirect_uri or "http://127.0.0.1:36500/callback"
    parsed = urlparse(candidate)
    if parsed.scheme != "http":
        raise UserFacingError("Local OAuth redirect_uri must use http://", exit_code=2)
    if parsed.hostname not in {"127.0.0.1", "localhost"}:
        raise UserFacingError(
            "Local OAuth redirect_uri must point to 127.0.0.1 or localhost",
            details={"redirect_uri": candidate},
            exit_code=2,
        )
    port = parsed.port or 80
    path = parsed.path or "/"
    normalized = f"http://{parsed.hostname}:{port}{path}"
    return parsed.hostname, port, path, normalized


def wait_for_local_callback(
    *,
    host: str,
    port: int,
    path: str,
    timeout: float,
) -> CallbackResult:
    result: dict[str, Any] = {}
    event = threading.Event()

    class CallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            if parsed.path != path:
                self.send_response(404)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"Not found")
                return

            query = parse_qs(parsed.query)
            code = query.get("code", [None])[0]
            state = query.get("state", [None])[0]

            if not code:
                self.send_response(400)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"Missing code query parameter")
                return

            result["code"] = code
            result["state"] = state
            result["query"] = query
            event.set()

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(
                b"<html><body><h1>Authorization complete</h1><p>You can close this tab and return to your terminal.</p></body></html>"
            )

        def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
            return

    class ReusableHTTPServer(HTTPServer):
        allow_reuse_address = True

    try:
        server = ReusableHTTPServer((host, port), CallbackHandler)
    except OSError as exc:
        raise UserFacingError(
            "Unable to listen for the local OAuth callback",
            details={"host": host, "port": port, "reason": str(exc)},
            exit_code=1,
        ) from exc

    server.timeout = 0.5

    def serve() -> None:
        while not event.is_set():
            server.handle_request()

    thread = threading.Thread(target=serve, daemon=True)
    thread.start()
    deadline = time.time() + timeout
    try:
        while time.time() < deadline:
            if event.wait(timeout=0.2):
                return CallbackResult(
                    code=result["code"],
                    state=result.get("state"),
                    query=result.get("query", {}),
                )
        raise UserFacingError(
            "Timed out waiting for the OAuth callback",
            details={"host": host, "port": port, "path": path, "timeout_seconds": timeout},
            exit_code=1,
        )
    finally:
        event.set()
        server.server_close()
        thread.join(timeout=1)

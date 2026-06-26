"""Browser-based authentication flow for CyberLens account connection."""

import os
import secrets
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.parse import parse_qs, urlencode, urlparse

import httpx
import yaml


CONNECT_BASE_URL = "https://cyberlensai.com/connect"
PRICING_BASE_URL = "https://www.cyberlensai.com/pricing"
TRUSTED_EXCHANGE_HOSTS = {
    "cyberlensai.com",
    "www.cyberlensai.com",
    "api.cyberlensai.com",
}
CONFIG_DIR = Path.home() / ".openclaw" / "skills" / "cyberlens"
CONFIG_FILE = CONFIG_DIR / "config.yaml"


class _CallbackHandler(BaseHTTPRequestHandler):
    """Handles the connect callback from cyberlensai.com/connect."""

    expected_state: Optional[str] = None
    connect_code: Optional[str] = None
    exchange_url: Optional[str] = None
    callback_error: Optional[str] = None
    received = threading.Event()

    def do_GET(self, *args, **kwargs):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        state = params.get("state", [None])[0]
        code = params.get("code", [None])[0]
        exchange_url = params.get("exchange", [None])[0]
        error = params.get("error", [None])[0]

        if state != self.expected_state:
            self.send_response(400)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Invalid callback. State mismatch.")
        elif error:
            _CallbackHandler.callback_error = error
            _CallbackHandler.received.set()
            self.send_response(400)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(f"Connection failed: {error}".encode("utf-8"))
        elif code and exchange_url:
            _CallbackHandler.connect_code = code
            _CallbackHandler.exchange_url = exchange_url
            _CallbackHandler.received.set()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"<html><body style='font-family:system-ui;background:#1a1a2e;color:white;"
                b"display:flex;align-items:center;justify-content:center;height:100vh;margin:0'>"
                b"<div style='text-align:center'>"
                b"<h1>&#x2705; Authorization Received</h1>"
                b"<p>You can close this tab while OpenClaw finishes the secure exchange.</p>"
                b"</div></body></html>"
            )
        else:
            _CallbackHandler.callback_error = "Missing exchange code."
            _CallbackHandler.received.set()
            self.send_response(400)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Invalid callback. Missing exchange code.")

    def log_message(self, format, *args):
        pass  # Suppress HTTP server logs


def _find_open_port() -> int:
    """Find an available port in the 54321-54399 range."""
    import socket

    for port in range(54321, 54400):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("127.0.0.1", port))
                return port
        except OSError:
            continue
    raise RuntimeError("No available ports in range 54321-54399")


def _is_loopback_host(hostname: Optional[str]) -> bool:
    """Return True when the callback host resolves to the local machine."""
    return hostname in {"localhost", "127.0.0.1", "::1"}


def _is_trusted_exchange_host(hostname: Optional[str]) -> bool:
    """Return True when the exchange URL host is an official CyberLens host."""
    if not hostname:
        return False
    return hostname in TRUSTED_EXCHANGE_HOSTS or hostname.endswith(".cyberlensai.com")


def _load_local_config() -> Dict[str, Any]:
    """Load the local skill config file if it exists."""
    if not CONFIG_FILE.exists():
        return {}

    with open(CONFIG_FILE) as f:
        return yaml.safe_load(f) or {}


def _write_local_config(config: Dict[str, Any]) -> Path:
    """Write the local skill config with restrictive permissions when supported."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    try:
        CONFIG_DIR.chmod(0o700)
    except OSError:
        pass

    with open(CONFIG_FILE, "w") as f:
        yaml.safe_dump(config, f, default_flow_style=False)

    try:
        CONFIG_FILE.chmod(0o600)
    except OSError:
        pass

    return CONFIG_FILE


def _resolve_callback_config() -> tuple[str, int, str]:
    """Resolve the bind address and callback URL for the connect flow."""
    configured_callback = os.environ.get("CYBERLENS_CONNECT_CALLBACK_URL", "").strip()

    if not configured_callback:
        port = _find_open_port()
        return "127.0.0.1", port, f"http://localhost:{port}/callback"

    parsed = urlparse(configured_callback)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError(
            "CYBERLENS_CONNECT_CALLBACK_URL must be a valid http:// or https:// URL."
        )

    callback_path = parsed.path or "/callback"
    callback_url = parsed._replace(path=callback_path).geturl()

    bind_port_value = os.environ.get("CYBERLENS_CONNECT_BIND_PORT", "").strip()
    if bind_port_value:
        bind_port = int(bind_port_value)
    elif parsed.port is not None:
        bind_port = parsed.port
    else:
        raise ValueError(
            "Configured callback URLs must include a port or set "
            "CYBERLENS_CONNECT_BIND_PORT explicitly."
        )

    bind_host = os.environ.get("CYBERLENS_CONNECT_BIND_HOST", "").strip()
    if not bind_host:
        bind_host = "127.0.0.1" if _is_loopback_host(parsed.hostname) else "0.0.0.0"

    return bind_host, bind_port, callback_url


async def _exchange_connect_code(code: str, exchange_url: str) -> str:
    """Redeem a one-time connect code for the real CyberLens account key."""
    parsed = urlparse(exchange_url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise ValueError("Invalid exchange URL returned by CyberLens.")
    if not _is_trusted_exchange_host(parsed.hostname):
        raise ValueError("CyberLens returned an untrusted exchange host.")

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(exchange_url, json={"code": code})
    except httpx.HTTPError as exc:
        raise RuntimeError(f"Failed to exchange connect code: {exc}") from exc

    try:
        payload = response.json()
    except ValueError:
        payload = {}

    if response.status_code == 404:
        raise RuntimeError("CyberLens connect code was not found. Please try again.")
    if response.status_code == 409:
        raise RuntimeError("CyberLens connect code was already used. Please reconnect.")
    if response.status_code == 410:
        raise RuntimeError("CyberLens connect code expired. Please reconnect.")
    if response.status_code >= 400:
        message = payload.get("error") or f"Exchange failed with status {response.status_code}."
        raise RuntimeError(message)

    full_key = payload.get("fullKey")
    if not full_key:
        raise RuntimeError("CyberLens exchange response did not include an API key.")

    return full_key


def save_api_key(key: str) -> Path:
    """Save the API key to the skill config file."""
    config = _load_local_config()
    config["api_key"] = key
    return _write_local_config(config)


def build_upgrade_url(quota_type: str = "combined") -> str:
    """Build the public pricing URL for quota upgrade prompts."""
    query = urlencode({
        "source": "openclaw-skill-quota-exceeded",
        "quota_type": quota_type,
    })
    return f"{PRICING_BASE_URL}?{query}#plans"


def open_upgrade_page(upgrade_url: str) -> None:
    """Open the CyberLens pricing page in the user's browser."""
    print(f"Open CyberLens pricing to upgrade: {upgrade_url}")
    webbrowser.open(upgrade_url)


def load_api_key() -> Optional[str]:
    """Load the API key from env var or config file."""
    # Check env var first
    env_key = os.environ.get("CYBERLENS_API_KEY")
    if env_key:
        return env_key

    # Check config file
    return _load_local_config().get("api_key")


def load_api_base_url() -> Optional[str]:
    """Load a user-configured CyberLens API base URL override."""
    env_base = os.environ.get("CYBERLENS_API_BASE_URL", "").strip()
    if env_base:
        return env_base

    configured_base = _load_local_config().get("api_base_url")
    if isinstance(configured_base, str) and configured_base.strip():
        return configured_base.strip()

    return None


async def run_connect_flow() -> str:
    """
    Run the browser-based connect flow.

    Opens cyberlensai.com/connect in the user's browser, starts a callback
    server, and waits for a one-time connect code to be delivered.

    Returns the API key string.
    """
    state = secrets.token_urlsafe(32)
    bind_host, bind_port, callback_url = _resolve_callback_config()

    # Reset handler state
    _CallbackHandler.expected_state = state
    _CallbackHandler.connect_code = None
    _CallbackHandler.exchange_url = None
    _CallbackHandler.callback_error = None
    _CallbackHandler.received = threading.Event()

    # Start callback server in a thread
    server = HTTPServer((bind_host, bind_port), _CallbackHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    query = urlencode({
        "client": "openclaw_skill",
        "callback": callback_url,
        "state": state,
    })
    connect_url = f"{CONNECT_BASE_URL}?{query}"
    print(f"Complete CyberLens connection in your browser: {connect_url}")
    webbrowser.open(connect_url)

    # Wait for callback (timeout 5 minutes)
    received = _CallbackHandler.received.wait(timeout=300)
    server.shutdown()
    server.server_close()

    if _CallbackHandler.callback_error:
        raise RuntimeError(f"CyberLens connection failed: {_CallbackHandler.callback_error}")

    if not received or not _CallbackHandler.connect_code or not _CallbackHandler.exchange_url:
        raise TimeoutError(
            "Did not receive a CyberLens connect code within 5 minutes. "
            "Please try again or set CYBERLENS_API_KEY manually."
        )

    key = await _exchange_connect_code(
        _CallbackHandler.connect_code,
        _CallbackHandler.exchange_url,
    )

    # Save to config
    save_api_key(key)
    return key

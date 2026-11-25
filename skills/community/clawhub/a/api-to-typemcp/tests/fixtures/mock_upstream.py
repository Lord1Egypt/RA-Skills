"""Mock upstream API server for contained E2E verification.

Serves a minimal Petstore-like API on localhost and tracks request
counts per method+path so tests can assert that denied operations
never reach the upstream.

Usage as a module::

    from mock_upstream import MockUpstream
    server = MockUpstream()
    server.start()          # binds to 127.0.0.1:<random port>
    print(server.base_url)  # http://127.0.0.1:54321
    ...
    stats = server.stats()  # {"GET /pets/1": 1, ...}
    server.stop()

Usage as a script (foreground, prints port on stdout)::

    python3 mock_upstream.py
"""

from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any


class _Handler(BaseHTTPRequestHandler):
    """Handle GET/POST for the mock Petstore API."""

    # Shared mutable state — set by MockUpstream before serving.
    counters: dict[str, int] = {}
    lock: threading.Lock = threading.Lock()

    def _record(self) -> None:
        key = f"{self.command} {self.path.split('?')[0]}"
        with type(self).lock:
            type(self).counters[key] = type(self).counters.get(key, 0) + 1

    def _send_json(self, status: int, body: Any) -> None:
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self) -> None:  # noqa: N802
        self._record()
        path = self.path.split("?")[0]
        if path == "/pets":
            self._send_json(200, [
                {"id": 1, "name": "Buddy", "status": "available"},
                {"id": 2, "name": "Whiskers", "status": "pending"},
            ])
        elif path.startswith("/pets/"):
            pet_id = path.rsplit("/", 1)[-1]
            self._send_json(200, {"id": int(pet_id) if pet_id.isdigit() else 0,
                                  "name": f"Pet-{pet_id}", "status": "available"})
        elif path == "/_stats":
            with type(self).lock:
                self._send_json(200, dict(type(self).counters))
        else:
            self._send_json(404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        self._record()
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length else {}
        self._send_json(201, {"id": 99, **body, "status": "created"})

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        """Suppress default stderr logging."""


class MockUpstream:
    """Threaded mock HTTP server on localhost."""

    def __init__(self) -> None:
        self._server: HTTPServer | None = None
        self._thread: threading.Thread | None = None
        self.port: int = 0

    @property
    def base_url(self) -> str:
        return f"http://127.0.0.1:{self.port}"

    def start(self) -> None:
        # Reset counters for a fresh run.
        _Handler.counters = {}
        self._server = HTTPServer(("127.0.0.1", 0), _Handler)
        self.port = self._server.server_address[1]
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        if self._server:
            self._server.shutdown()
            self._server.server_close()
        if self._thread:
            self._thread.join(timeout=5)

    def stats(self) -> dict[str, int]:
        with _Handler.lock:
            return dict(_Handler.counters)

    def total_requests(self) -> int:
        return sum(self.stats().values())


if __name__ == "__main__":
    server = MockUpstream()
    server.start()
    print(server.port, flush=True)
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        server.stop()

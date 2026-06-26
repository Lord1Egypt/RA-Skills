#!/usr/bin/env python3
"""
ASH-0.2 — Exchange Endpoint
FastAPI-style POST handler for /api/sessions/exchange.

Receives session exchange requests, validates tokens against the constraint engine,
and returns hydrated ResonanceManifests only when all governance checks pass.

Security constraints:
- No credential harvesting (vault stays local)
- No unauthorized access (profile lookup + signature verification)
- Every exchange logged to history/actions.log
- Rate limiting enforced per node_id
"""

import json
import time
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass

# Local imports
from .token_engine import TokenEngine, SessionToken, TokenScope, ALLOWED_SCOPES
from .resonance_manifest import ResonanceManifestEngine, ResonanceManifest


@dataclass
class ExchangeRequest:
    """Parsed incoming exchange request."""
    node_id: str
    compact_token: str
    requested_scopes: List[str]
    user_agent: str = "unknown"
    client_ip: str = "unknown"
    timestamp: int = 0

    @classmethod
    def from_post_body(cls, body: Dict[str, Any], headers: Dict[str, str] = None) -> "ExchangeRequest":
        headers = headers or {}
        return cls(
            node_id=body.get("node_id", ""),
            compact_token=body.get("token", ""),
            requested_scopes=body.get("scopes", []),
            user_agent=headers.get("user-agent", "unknown"),
            client_ip=headers.get("x-forwarded-for", "unknown"),
            timestamp=int(time.time()),
        )


@dataclass
class ExchangeResponse:
    """Outgoing exchange response."""
    success: bool
    session_id: Optional[str]
    manifest: Optional[Dict[str, Any]]
    error_code: Optional[str]
    error_reason: Optional[str]
    blocked_by: Optional[str]
    gateway_url: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "session_id": self.session_id,
            "manifest": self.manifest,
            "error": {
                "code": self.error_code,
                "reason": self.error_reason,
                "blocked_by": self.blocked_by,
            } if not self.success else None,
            "gateway_url": self.gateway_url,
            "timestamp": int(time.time()),
        }

    def to_http_response(self) -> Dict[str, Any]:
        """Returns (status_code, headers, body_dict)"""
        if self.success:
            return (200, {"Content-Type": "application/json"}, self.to_dict())
        else:
            status_map = {
                "UNAUTHORIZED": 401,
                "FORBIDDEN": 403,
                "RATE_LIMITED": 429,
                "BAD_REQUEST": 400,
                "EXPIRED": 401,
                "REVOKED": 401,
                "HUMAN_APPROVAL_REQUIRED": 403,
                "UNKNOWN_NODE": 404,
                "VALIDATION_FAILED": 400,
            }
            status = status_map.get(self.error_code, 400)
            return (status, {"Content-Type": "application/json"}, self.to_dict())


class RateLimiter:
    """Simple in-memory rate limiter per node_id."""

    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._buckets: Dict[str, List[int]] = {}

    def is_allowed(self, node_id: str) -> bool:
        now = int(time.time())
        window_start = now - self.window_seconds

        if node_id not in self._buckets:
            self._buckets[node_id] = []

        # Prune old entries
        self._buckets[node_id] = [ts for ts in self._buckets[node_id] if ts > window_start]

        if len(self._buckets[node_id]) >= self.max_requests:
            return False

        self._buckets[node_id].append(now)
        return True

    def remaining(self, node_id: str) -> int:
        now = int(time.time())
        window_start = now - self.window_seconds
        if node_id not in self._buckets:
            return self.max_requests
        recent = [ts for ts in self._buckets[node_id] if ts > window_start]
        return max(0, self.max_requests - len(recent))


class ExchangeEndpoint:
    """
    ASH-0.2 Exchange Endpoint.
    POST /api/sessions/exchange handler.
    """

    def __init__(
        self,
        gateway_url: str = "https://harmonic-molecular-archivist.replit.app/api",
        vault_dir: Optional[Path] = None,
    ):
        self.gateway_url = gateway_url.rstrip("/")
        self.token_engine = TokenEngine(vault_dir=vault_dir, gateway_url=gateway_url)
        self.manifest_engine = ResonanceManifestEngine(default_gateway=gateway_url)
        self.rate_limiter = RateLimiter(max_requests=10, window_seconds=60)
        self.request_log: List[Dict[str, Any]] = []

    def handle(self, body: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> ExchangeResponse:
        """
        Main entry point for exchange requests.

        Flow:
        1. Parse request
        2. Rate limit check
        3. Validate token
        4. Load node profile
        5. Check scope alignment (requested vs token scope)
        6. Consult oracle (risk taxonomy)
        7. Hydrate session via ResonanceManifestEngine
        8. Return manifest or block reason
        """
        req = ExchangeRequest.from_post_body(body, headers)

        # 1. Basic validation
        if not req.node_id:
            return self._error("BAD_REQUEST", "node_id is required", "request_parser")
        if not req.compact_token:
            return self._error("BAD_REQUEST", "token is required", "request_parser")

        # 2. Rate limiting
        if not self.rate_limiter.is_allowed(req.node_id):
            return self._error(
                "RATE_LIMITED",
                f"Rate limit exceeded. Try again in {self.rate_limiter.window_seconds}s.",
                "rate_limiter",
                extra={"retry_after": self.rate_limiter.window_seconds},
            )

        # 3. Validate token
        validation = self.token_engine.validate_compact(req.compact_token)
        if not validation["valid"]:
            return self._error(
                validation.get("code", "UNAUTHORIZED"),
                validation["reason"],
                "token_engine",
            )

        claims = validation["claims"]

        # 3b. Verify node_id matches token
        if claims["node_id"] != req.node_id:
            return self._error(
                "UNAUTHORIZED",
                f"Token node_id ({claims['node_id']}) does not match request node_id ({req.node_id})",
                "token_engine",
            )

        # 4. Check revocation
        if self.token_engine.is_revoked(claims["token_id"]):
            return self._error("REVOKED", "Token has been revoked", "token_engine")

        # 5. Check requested scopes against token scope
        token_scope = set(claims["scope"])
        requested = set(req.requested_scopes)
        unauthorized = requested - token_scope
        if unauthorized:
            return self._error(
                "FORBIDDEN",
                f"Requested scope(s) not in token: {unauthorized}",
                "scope_validator",
            )

        # 6. Reconstruct token for hydration
        token = SessionToken(
            token_id=claims["token_id"],
            node_id=claims["node_id"],
            issued_at=claims["issued_at"],
            expires_at=claims["expires_at"],
            scope=TokenScope.from_set(token_scope),
            gateway_url=claims.get("gateway_url", self.gateway_url),
            signature="",  # already validated
        )

        # 7. Hydrate via constraint engine
        hydration = self.manifest_engine.hydrate(token, force=False)

        if not hydration["success"]:
            return self._error(
                hydration.get("code", "FORBIDDEN"),
                hydration["reason"],
                hydration.get("blocked_by", "manifest_engine"),
            )

        # 8. Success — build response
        manifest_dict = hydration["manifest"]
        session_id = manifest_dict["session_id"]

        # Log the exchange
        self._log_exchange(req, session_id, success=True)

        return ExchangeResponse(
            success=True,
            session_id=session_id,
            manifest=manifest_dict,
            error_code=None,
            error_reason=None,
            blocked_by=None,
            gateway_url=self.gateway_url,
        )

    def _error(self, code: str, reason: str, blocked_by: str, extra: Optional[Dict] = None) -> ExchangeResponse:
        """Build an error response."""
        resp = ExchangeResponse(
            success=False,
            session_id=None,
            manifest=None,
            error_code=code,
            error_reason=reason,
            blocked_by=blocked_by,
            gateway_url=self.gateway_url,
        )
        self._log_exchange(None, None, success=False, error=resp.to_dict().get("error"))
        return resp

    def _log_exchange(self, req: Optional[ExchangeRequest], session_id: Optional[str], success: bool, error: Optional[Dict] = None):
        """Append exchange record to history."""
        history_dir = Path.home() / ".openclaw" / "workspace" / "skills" / "asin-governance" / "history"
        history_dir.mkdir(parents=True, exist_ok=True)
        log_file = history_dir / "actions.log"

        entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "sequence": int(time.time() * 1000) % 1000000000,
            "node_id": req.node_id if req else "unknown",
            "action_type": "session_exchange",
            "risk_class": "yellow",
            "entropy_cost": {"compute_ms": 500, "api_calls": 1, "tokens": 200},
            "oracle_result": {"safe": success, "drift_delta": 0.0, "consensus": 1.0 if success else 0.0},
            "payload_hash": hashlib.sha256(json.dumps(req.__dict__ if req else {}, sort_keys=True).encode()).hexdigest()[:32] if req else "n/a",
            "session_id": session_id,
            "outcome": {"success": success, **(error or {})},
            "client_ip": req.client_ip if req else "unknown",
        }

        with open(log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

        self.request_log.append(entry)

    def get_health(self) -> Dict[str, Any]:
        """Health check endpoint data."""
        return {
            "status": "healthy",
            "gateway_url": self.gateway_url,
            "version": "ASH-0.2",
            "rate_limit_window": self.rate_limiter.window_seconds,
            "allowed_scopes": sorted(ALLOWED_SCOPES),
            "total_exchanges_processed": len(self.request_log),
        }


# === FastAPI-style router (for actual deployment) ===

# Example usage with FastAPI:
# from fastapi import FastAPI, Request, HTTPException
# app = FastAPI()
# endpoint = ExchangeEndpoint()
#
# @app.post("/api/sessions/exchange")
# async def exchange(request: Request):
#     body = await request.json()
#     headers = dict(request.headers)
#     response = endpoint.handle(body, headers)
#     status, response_headers, body_dict = response.to_http_response()
#     if status != 200:
#         raise HTTPException(status_code=status, detail=body_dict)
#     return body_dict

# === CLI / Standalone server ===

def main():
    import argparse
    import http.server
    import socketserver
    import urllib.parse

    parser = argparse.ArgumentParser(description="ASH-0.2 Exchange Endpoint Server")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host")
    parser.add_argument("--port", type=int, default=8000, help="Bind port")
    parser.add_argument("--gateway", default="https://harmonic-molecular-archivist.replit.app/api", help="Gateway URL")
    args = parser.parse_args()

    endpoint = ExchangeEndpoint(gateway_url=args.gateway)

    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            pass  # suppress default logging

        def _json_response(self, status: int, data: Dict):
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())

        def do_POST(self):
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path != "/api/sessions/exchange":
                self._json_response(404, {"error": "Not found"})
                return

            content_length = int(self.headers.get("Content-Length", 0))
            body_raw = self.rfile.read(content_length).decode()
            try:
                body = json.loads(body_raw) if body_raw else {}
            except json.JSONDecodeError:
                self._json_response(400, {"error": "Invalid JSON"})
                return

            headers = {k.lower(): v for k, v in dict(self.headers).items()}
            response = endpoint.handle(body, headers)
            status, _, body_dict = response.to_http_response()
            self._json_response(status, body_dict)

        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path == "/health":
                self._json_response(200, endpoint.get_health())
            else:
                self._json_response(404, {"error": "Not found"})

    with socketserver.TCPServer((args.host, args.port), Handler) as httpd:
        print(f"🛡️ ASH-0.2 Exchange Endpoint listening on http://{args.host}:{args.port}")
        print(f"   Gateway: {args.gateway}")
        print(f"   POST /api/sessions/exchange")
        print(f"   GET  /health")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Shutting down.")


if __name__ == "__main__":
    main()

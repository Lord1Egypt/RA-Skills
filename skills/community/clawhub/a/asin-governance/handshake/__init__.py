"""
ASH-0.2 Handshake Protocol Package

Provides:
- token_engine: Ephemeral token generation and validation
- resonance_manifest: Session hydration with ANU-28 constellation
- exchange_endpoint: FastAPI-style POST handler for /api/sessions/exchange

Usage:
    from handshake import TokenEngine, ResonanceManifestEngine, ExchangeEndpoint

Security:
    - Local vault only (no credential harvesting)
    - HMAC-SHA256 with per-node secrets
    - All exchanges checked against constraint profiles
"""

from .token_engine import TokenEngine, SessionToken, TokenScope, ALLOWED_SCOPES, TOKEN_VERSION
from .resonance_manifest import ResonanceManifestEngine, ResonanceManifest, ANUConstellation, MissionContext
from .exchange_endpoint import ExchangeEndpoint, ExchangeRequest, ExchangeResponse, RateLimiter

__all__ = [
    "TokenEngine",
    "SessionToken",
    "TokenScope",
    "ALLOWED_SCOPES",
    "TOKEN_VERSION",
    "ResonanceManifestEngine",
    "ResonanceManifest",
    "ANUConstellation",
    "MissionContext",
    "ExchangeEndpoint",
    "ExchangeRequest",
    "ExchangeResponse",
    "RateLimiter",
]

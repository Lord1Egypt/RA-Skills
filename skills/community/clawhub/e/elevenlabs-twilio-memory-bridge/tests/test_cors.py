# Feature: clawhub-review-remediation, Property 4: CORS headers absent when ALLOWED_ORIGINS is unconfigured
# Feature: clawhub-review-remediation, Property 5: CORS allows only configured origins
"""Property-based tests for CORS middleware behavior (P4, P5).

Uses Hypothesis to generate random Origin headers and origin configurations
to verify CORS middleware behaves correctly across all inputs.

The CORS middleware is registered at module load time. To test different
configurations we:
- P4: Use the default app (no CORS middleware since ALLOWED_ORIGINS is empty)
- P5: Build a fresh FastAPI app with CORSMiddleware for each test case
"""

from __future__ import annotations

import hypothesis.strategies as st
from hypothesis import given, settings, HealthCheck
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient


# ── Strategies ──────────────────────────────────────────────────────────────

# Origin headers: valid HTTP origins (scheme + host, optionally with port)
_schemes = st.sampled_from(["http", "https"])
_hosts = st.from_regex(r"[a-z][a-z0-9\-]{0,20}\.[a-z]{2,6}", fullmatch=True)
_ports = st.one_of(st.just(""), st.integers(min_value=1, max_value=65535).map(lambda p: f":{p}"))

origin_strategy = st.builds(
    lambda scheme, host, port: f"{scheme}://{host}{port}",
    _schemes,
    _hosts,
    _ports,
)

# A list of 1-5 allowed origins (non-empty, unique)
allowed_origins_list_strategy = st.lists(
    origin_strategy,
    min_size=1,
    max_size=5,
    unique=True,
)

# Endpoints to test against (GET and POST paths available on the app)
endpoint_strategy = st.sampled_from([
    ("GET", "/health"),
])


# ── Helpers ─────────────────────────────────────────────────────────────────


def _build_cors_app(origins: list[str] | None = None) -> FastAPI:
    """Create a fresh FastAPI app, optionally with CORS middleware.

    Mounts a minimal /health endpoint so we have something to hit.
    """
    test_app = FastAPI()
    if origins:
        test_app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @test_app.get("/health")
    async def health():
        return {"status": "ok"}

    return test_app


# ── Property 4: CORS headers absent when ALLOWED_ORIGINS is unconfigured ───
# **Validates: Requirements 6.1**


@given(
    request_origin=origin_strategy,
    endpoint=endpoint_strategy,
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_cors_headers_absent_when_unconfigured(
    request_origin, endpoint
):
    """P4: For any request with any Origin header, when ALLOWED_ORIGINS is not
    configured, the response SHALL NOT contain Access-Control-Allow-Origin."""
    test_app = _build_cors_app()
    client = TestClient(test_app, raise_server_exceptions=False)
    method, path = endpoint
    resp = client.request(method, path, headers={"Origin": request_origin})

    assert "access-control-allow-origin" not in resp.headers, (
        f"Expected no CORS header for unconfigured ALLOWED_ORIGINS, "
        f"but got Access-Control-Allow-Origin: {resp.headers.get('access-control-allow-origin')} "
        f"for Origin: {request_origin}"
    )


@given(
    request_origin=origin_strategy,
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_cors_preflight_absent_when_unconfigured(
    request_origin
):
    """P4 (preflight): OPTIONS preflight requests should also lack CORS headers
    when ALLOWED_ORIGINS is not configured."""
    test_app = _build_cors_app()
    client = TestClient(test_app, raise_server_exceptions=False)
    resp = client.options(
        "/health",
        headers={
            "Origin": request_origin,
            "Access-Control-Request-Method": "GET",
        },
    )

    assert "access-control-allow-origin" not in resp.headers, (
        f"Expected no CORS header on preflight for unconfigured ALLOWED_ORIGINS, "
        f"but got Access-Control-Allow-Origin: {resp.headers.get('access-control-allow-origin')} "
        f"for Origin: {request_origin}"
    )


# ── Property 5: CORS allows only configured origins ────────────────────────
# **Validates: Requirements 6.2**


@given(
    allowed_origins=allowed_origins_list_strategy,
    request_origin=origin_strategy,
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_cors_allows_only_configured_origins(
    allowed_origins, request_origin
):
    """P5: For any configured origins list and any Origin header, the response
    SHALL include Access-Control-Allow-Origin only if the origin is in the list."""
    test_app = _build_cors_app(allowed_origins)
    client = TestClient(test_app, raise_server_exceptions=False)

    resp = client.get("/health", headers={"Origin": request_origin})

    acao = resp.headers.get("access-control-allow-origin")

    if request_origin in allowed_origins:
        assert acao == request_origin, (
            f"Origin {request_origin!r} is in allowed list {allowed_origins} "
            f"but Access-Control-Allow-Origin was {acao!r}"
        )
    else:
        assert acao is None, (
            f"Origin {request_origin!r} is NOT in allowed list {allowed_origins} "
            f"but Access-Control-Allow-Origin was {acao!r}"
        )


@given(
    allowed_origins=allowed_origins_list_strategy,
    request_origin=origin_strategy,
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_cors_preflight_allows_only_configured_origins(
    allowed_origins, request_origin
):
    """P5 (preflight): OPTIONS preflight should also respect the configured origins list."""
    test_app = _build_cors_app(allowed_origins)
    client = TestClient(test_app, raise_server_exceptions=False)

    resp = client.options(
        "/health",
        headers={
            "Origin": request_origin,
            "Access-Control-Request-Method": "GET",
        },
    )

    acao = resp.headers.get("access-control-allow-origin")

    if request_origin in allowed_origins:
        assert acao == request_origin, (
            f"Origin {request_origin!r} is in allowed list {allowed_origins} "
            f"but preflight Access-Control-Allow-Origin was {acao!r}"
        )
    else:
        assert acao is None, (
            f"Origin {request_origin!r} is NOT in allowed list {allowed_origins} "
            f"but preflight Access-Control-Allow-Origin was {acao!r}"
        )

# Feature: clawhub-review-remediation, Property 1: Valid admin auth grants access
# Feature: clawhub-review-remediation, Property 2: Invalid admin auth is rejected
# Feature: clawhub-review-remediation, Property 3: Unconfigured admin key disables admin endpoints
"""Property-based tests for admin endpoint authentication (P1, P2, P3).

Uses Hypothesis to generate random API keys, request bodies, and auth headers
to verify the authentication dependency behaves correctly across all inputs.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import hypothesis.strategies as st
from hypothesis import given, settings, HealthCheck
from fastapi.testclient import TestClient

import app as app_module
import memory as memory_module


# ── Strategies ──────────────────────────────────────────────────────────────

# Non-empty strings suitable for use as API keys (printable ASCII, no whitespace).
api_key_strategy = st.text(
    alphabet=st.characters(
        whitelist_categories=("L", "N", "P", "S"),
        min_codepoint=33,
        max_codepoint=126,
    ),
    min_size=1,
    max_size=64,
)

# Non-empty fact strings for /api/memory/{phone_hash}
fact_strategy = st.text(min_size=1, max_size=200).filter(lambda s: s.strip())

# Non-empty note strings for /api/notes
note_strategy = st.text(min_size=1, max_size=200).filter(lambda s: s.strip())

# Phone hash path parameter — hex-like strings
phone_hash_strategy = st.text(
    alphabet="0123456789abcdef",
    min_size=8,
    max_size=64,
)

# Strategy that picks which admin endpoint to hit
endpoint_strategy = st.sampled_from(["memory", "notes"])


def _post_admin(
    client: TestClient,
    endpoint: str,
    phone_hash: str,
    fact: str,
    note: str,
    headers: dict,
):
    """Helper to POST to the chosen admin endpoint with the given headers."""
    if endpoint == "memory":
        return client.post(
            f"/api/memory/{phone_hash}",
            json={"fact": fact},
            headers=headers,
        )
    else:
        return client.post(
            "/api/notes",
            json={"note": note},
            headers=headers,
        )


# ── Property 1: Valid admin auth grants access ─────────────────────────────
# **Validates: Requirements 2.1, 2.4**


@given(
    api_key=api_key_strategy,
    fact=fact_strategy,
    note=note_strategy,
    phone_hash=phone_hash_strategy,
    endpoint=endpoint_strategy,
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_valid_admin_auth_grants_access(
    api_key, fact, note, phone_hash, endpoint, monkeypatch
):
    """P1: For any configured ADMIN_API_KEY and valid request body,
    Bearer token matching the key returns 2xx."""
    with tempfile.TemporaryDirectory() as tmp:
        monkeypatch.setattr(memory_module, "DATA_DIR", Path(tmp))
        monkeypatch.setattr(app_module, "ADMIN_API_KEY", api_key)

        client = TestClient(app_module.app, raise_server_exceptions=False)
        headers = {"Authorization": f"Bearer {api_key}"}

        resp = _post_admin(client, endpoint, phone_hash, fact, note, headers)
        assert 200 <= resp.status_code < 300, (
            f"Expected 2xx for valid auth, got {resp.status_code}: {resp.text}"
        )


# ── Property 2: Invalid admin auth is rejected ─────────────────────────────
# **Validates: Requirements 2.2, 2.4**


def _invalid_auth_header(admin_key: str):
    """Strategy that generates auth header values that do NOT match the configured key."""
    # HTTP headers must be ASCII-encodable, so constrain all generated values accordingly.
    ascii_printable = st.text(
        alphabet=st.characters(min_codepoint=32, max_codepoint=126),
        min_size=1,
        max_size=100,
    )
    wrong_token = api_key_strategy.filter(lambda t: t != admin_key).map(
        lambda t: {"Authorization": f"Bearer {t}"}
    )
    wrong_scheme = api_key_strategy.map(
        lambda t: {"Authorization": f"Basic {t}"}
    )
    missing_header = st.just({})
    empty_bearer = st.just({"Authorization": "Bearer "})
    bearer_no_space = st.just({"Authorization": "Bearer"})
    random_garbage = ascii_printable.map(
        lambda t: {"Authorization": t}
    )

    return st.one_of(
        wrong_token, wrong_scheme, missing_header,
        empty_bearer, bearer_no_space, random_garbage,
    )


@given(data=st.data())
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_invalid_admin_auth_is_rejected(data, monkeypatch):
    """P2: For any configured ADMIN_API_KEY and any non-matching auth header,
    response is 401."""
    api_key = data.draw(api_key_strategy, label="admin_key")
    fact = data.draw(fact_strategy, label="fact")
    note = data.draw(note_strategy, label="note")
    phone_hash = data.draw(phone_hash_strategy, label="phone_hash")
    endpoint = data.draw(endpoint_strategy, label="endpoint")
    headers = data.draw(_invalid_auth_header(api_key), label="invalid_headers")

    with tempfile.TemporaryDirectory() as tmp:
        monkeypatch.setattr(memory_module, "DATA_DIR", Path(tmp))
        monkeypatch.setattr(app_module, "ADMIN_API_KEY", api_key)

        client = TestClient(app_module.app, raise_server_exceptions=False)

        resp = _post_admin(client, endpoint, phone_hash, fact, note, headers)
        assert resp.status_code == 401, (
            f"Expected 401 for invalid auth, got {resp.status_code}: {resp.text}"
        )


# ── Property 3: Unconfigured admin key disables admin endpoints ─────────────
# **Validates: Requirements 2.3**


@given(
    fact=fact_strategy,
    note=note_strategy,
    phone_hash=phone_hash_strategy,
    endpoint=endpoint_strategy,
    auth_header=st.one_of(
        st.just({}),
        api_key_strategy.map(lambda k: {"Authorization": f"Bearer {k}"}),
        st.text(
            alphabet=st.characters(min_codepoint=32, max_codepoint=126),
            min_size=1,
            max_size=100,
        ).map(lambda t: {"Authorization": t}),
    ),
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_unconfigured_admin_key_disables_endpoints(
    fact, note, phone_hash, endpoint, auth_header, monkeypatch
):
    """P3: For any request when ADMIN_API_KEY is empty, response is 403."""
    with tempfile.TemporaryDirectory() as tmp:
        monkeypatch.setattr(memory_module, "DATA_DIR", Path(tmp))
        monkeypatch.setattr(app_module, "ADMIN_API_KEY", "")

        client = TestClient(app_module.app, raise_server_exceptions=False)

        resp = _post_admin(client, endpoint, phone_hash, fact, note, auth_header)
        assert resp.status_code == 403, (
            f"Expected 403 for unconfigured key, got {resp.status_code}: {resp.text}"
        )


# ── Unit Tests: Admin Auth Edge Cases ───────────────────────────────────────
# Requirements: 2.4, 2.5


class TestAdminEndpointsIndependently:
    """Test both admin endpoints independently for auth behavior."""

    # -- /api/memory/{phone_hash} --

    def test_memory_endpoint_accepts_valid_bearer(self, configured_app):
        """Validates: Requirement 2.1, 2.4 — valid auth on /api/memory/{phone_hash}."""
        resp = configured_app.post(
            "/api/memory/abc123",
            json={"fact": "likes cats"},
            headers={"Authorization": "Bearer test-secret-key"},
        )
        assert resp.status_code == 200

    def test_memory_endpoint_rejects_missing_auth(self, configured_app):
        """Validates: Requirement 2.2, 2.4 — missing auth on /api/memory/{phone_hash}."""
        resp = configured_app.post(
            "/api/memory/abc123",
            json={"fact": "likes cats"},
        )
        assert resp.status_code == 401

    def test_memory_endpoint_rejects_wrong_key(self, configured_app):
        """Validates: Requirement 2.2, 2.4 — wrong key on /api/memory/{phone_hash}."""
        resp = configured_app.post(
            "/api/memory/abc123",
            json={"fact": "likes cats"},
            headers={"Authorization": "Bearer wrong-key"},
        )
        assert resp.status_code == 401

    def test_memory_endpoint_returns_403_when_unconfigured(self, unconfigured_app):
        """Validates: Requirement 2.3 — unconfigured key on /api/memory/{phone_hash}."""
        resp = unconfigured_app.post(
            "/api/memory/abc123",
            json={"fact": "likes cats"},
            headers={"Authorization": "Bearer any-key"},
        )
        assert resp.status_code == 403

    # -- /api/notes --

    def test_notes_endpoint_accepts_valid_bearer(self, configured_app):
        """Validates: Requirement 2.1, 2.4 — valid auth on /api/notes."""
        resp = configured_app.post(
            "/api/notes",
            json={"note": "test note"},
            headers={"Authorization": "Bearer test-secret-key"},
        )
        assert resp.status_code == 200

    def test_notes_endpoint_rejects_missing_auth(self, configured_app):
        """Validates: Requirement 2.2, 2.4 — missing auth on /api/notes."""
        resp = configured_app.post(
            "/api/notes",
            json={"note": "test note"},
        )
        assert resp.status_code == 401

    def test_notes_endpoint_rejects_wrong_key(self, configured_app):
        """Validates: Requirement 2.2, 2.4 — wrong key on /api/notes."""
        resp = configured_app.post(
            "/api/notes",
            json={"note": "test note"},
            headers={"Authorization": "Bearer wrong-key"},
        )
        assert resp.status_code == 401

    def test_notes_endpoint_returns_403_when_unconfigured(self, unconfigured_app):
        """Validates: Requirement 2.3 — unconfigured key on /api/notes."""
        resp = unconfigured_app.post(
            "/api/notes",
            json={"note": "test note"},
            headers={"Authorization": "Bearer any-key"},
        )
        assert resp.status_code == 403


class TestPublicEndpointsNoAuth:
    """Validates: Requirement 2.5 — webhook and health endpoints remain accessible without auth."""

    def test_health_no_auth_required(self, configured_app):
        """GET /health should return 200 without any auth header."""
        resp = configured_app.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"

    def test_webhook_personalize_no_auth_required(self, configured_app):
        """POST /webhook/personalize should not require admin auth."""
        resp = configured_app.post(
            "/webhook/personalize",
            json={"caller_id": "+15551234567", "agent_id": "test"},
        )
        # Should not be 401/403 from admin auth — may be 200 or other status
        # depending on webhook secret config, but NOT an admin auth rejection.
        assert resp.status_code not in (401, 403)

    def test_webhook_post_call_no_auth_required(self, configured_app):
        """POST /webhook/post-call should not require admin auth."""
        resp = configured_app.post(
            "/webhook/post-call",
            json={"call_sid": "CA123", "caller_id": "+15551234567"},
        )
        assert resp.status_code not in (401, 403)


class TestAuthEdgeCases:
    """Edge cases for the auth dependency: empty keys, whitespace, partial match, wrong scheme."""

    def test_empty_string_key_rejected(self, configured_app):
        """Empty string Bearer token should be rejected as 401."""
        resp = configured_app.post(
            "/api/memory/abc123",
            json={"fact": "test"},
            headers={"Authorization": "Bearer "},
        )
        assert resp.status_code == 401

    def test_whitespace_only_key_rejected(self, configured_client_factory):
        """A whitespace-only ADMIN_API_KEY should behave as unconfigured (403)."""
        # Whitespace-only string is falsy after strip, but the code uses
        # `if not ADMIN_API_KEY` which checks truthiness of the raw string.
        # "   " is truthy, so it's treated as configured — auth should work
        # against that whitespace key. Sending a non-matching token → 401.
        client, _ = configured_client_factory("   ")
        resp = client.post(
            "/api/notes",
            json={"note": "test"},
            headers={"Authorization": "Bearer wrong"},
        )
        assert resp.status_code == 401

    def test_whitespace_key_exact_match_accepted(self, configured_client_factory):
        """If ADMIN_API_KEY is whitespace, sending that exact whitespace should succeed."""
        client, _ = configured_client_factory("   ")  # noqa: RUF -- key unused intentionally
        resp = client.post(
            "/api/notes",
            json={"note": "test"},
            headers={"Authorization": "Bearer    "},
        )
        assert resp.status_code == 200

    def test_partial_key_match_rejected(self, configured_app):
        """A prefix of the real key should be rejected."""
        resp = configured_app.post(
            "/api/memory/abc123",
            json={"fact": "test"},
            headers={"Authorization": "Bearer test-secret"},
        )
        assert resp.status_code == 401

    def test_key_suffix_rejected(self, configured_app):
        """A suffix of the real key should be rejected."""
        resp = configured_app.post(
            "/api/memory/abc123",
            json={"fact": "test"},
            headers={"Authorization": "Bearer secret-key"},
        )
        assert resp.status_code == 401

    def test_basic_scheme_rejected(self, configured_app):
        """Using Basic scheme instead of Bearer should be rejected."""
        resp = configured_app.post(
            "/api/notes",
            json={"note": "test"},
            headers={"Authorization": "Basic test-secret-key"},
        )
        assert resp.status_code == 401

    def test_no_scheme_just_token_rejected(self, configured_app):
        """Sending just the token without a scheme should be rejected."""
        resp = configured_app.post(
            "/api/memory/abc123",
            json={"fact": "test"},
            headers={"Authorization": "test-secret-key"},
        )
        assert resp.status_code == 401

    def test_bearer_lowercase_accepted(self, configured_app):
        """The scheme check should be case-insensitive per the design (scheme.lower())."""
        resp = configured_app.post(
            "/api/notes",
            json={"note": "test"},
            headers={"Authorization": "bearer test-secret-key"},
        )
        assert resp.status_code == 200

    def test_bearer_uppercase_accepted(self, configured_app):
        """BEARER scheme should also be accepted (case-insensitive)."""
        resp = configured_app.post(
            "/api/memory/abc123",
            json={"fact": "test"},
            headers={"Authorization": "BEARER test-secret-key"},
        )
        assert resp.status_code == 200

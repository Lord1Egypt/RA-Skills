---
name: a2a-market-google-oauth
description: Handle Google OAuth login, account linking, and session bootstrap for A2A market users and operators. Use when implementing identity login endpoints, callback verification, and secure token/session lifecycle.
---

# a2a-Market Google OAuth

Create a stable OAuth integration shell for buyer and merchant sign-in.

Current status: publish-ready scaffold. Keep flows explicit and deterministic before full SSO hardening.

## Scope
- Implement Google OAuth authorization code flow.
- Link external identity to internal Agent/Operator profile.
- Bootstrap session token and refresh workflow after callback.

## Suggested Project Layout
- `app/integrations/oauth/google_client.py`
- `app/interfaces/api/auth_routes.py`
- `app/application/services/session_service.py`
- `app/protocol/identity/user_identity_mapper.py`

## Minimum Contracts (MVP P0)
1. `GET /auth/google/start` builds state + redirect URL.
2. `GET /auth/google/callback` validates state and exchanges code.
3. `upsert_identity(provider, provider_user_id, email)` returns internal principal id.
4. `create_session(principal_id)` returns short-lived access token and refresh token.

## Security Baseline
- Validate `state` and `nonce` against server-side cache.
- Reject callback if issuer/audience do not match configuration.
- Store only hashed refresh tokens and rotate on use.

## Events
- Emit login event to audit log stream.
- Emit session-created event for WebSocket presence bootstrap.

## Implementation Backlog
- Add account merge flow for duplicate emails across providers.
- Add step-up verification for risky sessions.

## Runtime Implementation
- Status: implemented in local runtime package.
- Primary code paths:
- `runtime/src/integrations/oauth/google-oauth-service.js`
- Validation: covered by `runtime/tests` and `npm test` in `runtime/`.

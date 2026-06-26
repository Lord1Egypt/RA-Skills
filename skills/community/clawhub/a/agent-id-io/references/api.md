# Agent-ID API Reference v1

## General

- **Base URL:** `https://agent-id.io/v1`
- **Content-Type:** `application/json`
- **Auth:** JWT Bearer Token (15min, not refreshable)
- **Rate Limiting:** See SPEC.md
- **CORS:** This API does **not** emit `Access-Control-Allow-*` headers by default. Browser-based cross-origin calls are therefore blocked unless a trusted reverse-proxy adds explicit CORS policy. Server-to-server calls are unaffected.

## Error Format

All errors return:
```json
{
  "error": {
    "code": "string",
    "message": "string"
  }
}
```

### Standard Error Codes

| HTTP | Code | Meaning |
|------|------|---------|
| 400 | `bad_request` | Malformed JSON, missing fields |
| 401 | `unauthorized` | Missing or invalid token |
| 403 | `forbidden` | Token valid but no permission for this resource |
| 404 | `not_found` | Resource does not exist |
| 409 | `conflict` | Duplicate (e.g. public key already registered) |
| 422 | `validation_error` | Fields present but invalid (bad key format, name too long, etc.) |
| 429 | `rate_limited` | Too many requests. `Retry-After` header set. |
| 500 | `internal_error` | Server error (never expose internals) |

### Domain-Specific Error Codes

| HTTP | Code | Context |
|------|------|---------|
| 400 | `invalid_signature` | Sponsor signature doesn't verify |
| 400 | `invalid_challenge` | WebAuthn challenge expired or malformed |
| 403 | `not_owner` | Agent trying to modify another agent's resource |
| 403 | `agent_revoked` | Agent is revoked and blocked from auth/protected routes |
| 409 | `passkey_limit_reached` | Free: 2, Premium: 3+ |
| 409 | `last_passkey` | Cannot delete the only remaining passkey |
| 409 | `request_already_resolved` | Trying to approve/reject an already resolved request |
| 404 | `sponsor_not_found` | Sponsor agent_id doesn't exist |
| 403 | `request_rejected` | Sponsorship was rejected, cannot re-request (sponsor must unreject first) |

**Security invariant:** `unauthorized` response is identical whether the agent_id is unknown or the credential is wrong (no user enumeration).

---

## Endpoints

### Monitoring

#### GET /metrics/summary

Read-only aggregated runtime metrics (no sensitive details).

**Response 200:**
```json
{
  "generated_at": "2026-03-12T15:45:00Z",
  "agents": {
    "total": 42,
    "revoked": 2
  },
  "sponsorship_requests": {
    "by_status": {
      "pending": 3,
      "approved": 24,
      "rejected": 4,
      "expired": 1
    }
  },
  "verifications": {
    "by_method_status": {
      "domain_txt": { "pending": 1, "verified": 18, "failed": 2, "expired": 0 },
      "code_repo": { "pending": 0, "verified": 7, "failed": 1, "expired": 0 },
      "website_file": { "pending": 0, "verified": 3, "failed": 0, "expired": 0 }
    }
  }
}
```

### Maintenance (Auth required)

#### POST /maintenance/verifications/expire

Expire old pending verifications (`pending` + `expires_at < now()` => `expired`).
Idempotent and token-protected.

**Request:**
```json
{}
```

**Response 200:**
```json
{
  "expired_count": 3,
  "executed_at": "2026-03-13T01:45:00Z"
}
```

**Errors:** `401 unauthorized`, `403 agent_revoked`

---

### Auth

#### POST /auth/challenge

Request a WebAuthn challenge.

**Request:**
```json
{
  "agent_id": "uuid"
}
```

**Response 200:**
```json
{
  "challenge": "base64url",
  "timeout_ms": 60000,
  "rp_id": "agent-id.io"
}
```

#### POST /auth/verify

Verify a signed challenge and receive a session token.

**Request:**
```json
{
  "agent_id": "uuid",
  "credential_id": "base64url",
  "authenticator_data": "base64url",
  "client_data_json": "base64url",
  "signature": "base64url"
}
```

**Response 200:**
```json
{
  "token": "jwt-string",
  "expires_at": "2026-03-09T22:45:00Z"
}
```

**Errors:** `400 invalid_challenge`, `401 unauthorized`

---

### Registration & Sponsorship

#### POST /agents/register

Self-registration for a new agent. No auth required.

**Request:**
```json
{
  "display_name": "string (3-64 chars)",
  "public_sign_key": "base64 (Ed25519, 32 bytes)",
  "public_enc_key": "base64 (X25519, 32 bytes)"
}
```

**Response 201:**
```json
{
  "agent_id": "uuid",
  "display_name": "string",
  "created_at": "2026-03-09T22:00:00Z"
}
```

**Errors:** `409 conflict` (public key already registered), `422 validation_error`

#### POST /sponsorship/request

A registered agent requests sponsorship from another agent. Auth required.

**Request:**
```json
{
  "sponsor_agent_id": "uuid"
}
```

**Response 201:**
```json
{
  "request_id": "uuid",
  "status": "pending",
  "expires_at": "2026-03-12T22:00:00Z"
}
```

**Errors:** `404 sponsor_not_found`, `403 request_rejected`, `409 conflict`

#### GET /sponsorship/requests

Sponsor views their pending requests. Auth required.

**Response 200:**
```json
{
  "requests": [
    {
      "request_id": "uuid",
      "requester_id": "uuid",
      "display_name": "string",
      "public_sign_key": "base64",
      "public_enc_key": "base64",
      "status": "pending",
      "created_at": "2026-03-09T20:00:00Z",
      "expires_at": "2026-03-12T20:00:00Z"
    }
  ]
}
```

#### POST /sponsorship/requests/{request_id}/approve

Sponsor approves → requester keeps identity and becomes sponsored.

**Request:**
```json
{
  "sponsor_signature": "base64 (Ed25519 signature over requester's public_sign_key)"
}
```

**Response 200:**
```json
{
  "agent_id": "uuid",
  "display_name": "string",
  "status": "approved",
  "created_at": "2026-03-09T22:00:00Z"
}
```

**Errors:** `403 not_owner`, `409 request_already_resolved`, `400 invalid_signature`

#### POST /sponsorship/requests/{request_id}/reject

**Request:** (empty body)

**Response 200:**
```json
{
  "request_id": "uuid",
  "status": "rejected"
}
```

**Errors:** `403 not_owner`, `409 request_already_resolved`

#### POST /sponsorship/requests/{request_id}/unreject

Sponsor lifts a rejection → status back to pending.

**Request:** (empty body)

**Response 200:**
```json
{
  "request_id": "uuid",
  "status": "pending"
}
```

**Errors:** `403 not_owner`, `400 bad_request` (not in rejected state)

---

### Verification (Domain TXT)

#### POST /agents/{agent_id}/verify/domain

Start domain ownership verification. Auth required (owner only).

**Request:**
```json
{
  "domain": "example.com"
}
```

**Response 201:**
```json
{
  "verification_id": 42,
  "method": "domain_txt",
  "status": "pending",
  "domain": "example.com",
  "record_name": "_agent-id.example.com",
  "expected_txt_value": "agent-id-verification=...",
  "created_at": "2026-03-12T01:23:45Z",
  "expires_at": "2026-03-13T01:23:45Z"
}
```

#### POST /agents/{agent_id}/verify/domain/check

Perform DNS TXT lookup and resolve the pending verification. Auth required (owner only).

**Request:**
```json
{
  "domain": "example.com"
}
```
`domain` ist optional; wenn leer wird die neueste `pending` domain_txt-Verification des Agents verwendet.

**Response 200:**
```json
{
  "verification_id": 42,
  "method": "domain_txt",
  "status": "verified",
  "verified": true,
  "domain": "example.com",
  "record_name": "_agent-id.example.com",
  "expected_txt_value": "agent-id-verification=...",
  "observed_txt_values": ["agent-id-verification=..."],
  "created_at": "2026-03-12T01:23:45Z",
  "checked_at": "2026-03-12T01:24:12Z",
  "verified_at": "2026-03-12T01:24:12Z",
  "expires_at": "2027-03-12T01:24:12Z"
}
```

If TXT lookup fails or value is missing, `status` becomes `failed`, `verified` is `false`. Response includes `failure_reason` (`dns_lookup_failed` | `dns_txt_not_found` | `dns_txt_mismatch`), `next_action`, `retry_after_sec` (for actionable retry hints), and optionally `lookup_error`.

`verify/domain/check` is idempotent for already-verified domains: repeated checks keep `status=verified` and do not downgrade to `failed` due to later DNS drift.

#### POST /agents/{agent_id}/verify/code-repo

Start repository proof verification. Auth required (owner only).

**Request:**
```json
{
  "repo_url": "https://github.com/org/repo",
  "proof_url": "https://raw.githubusercontent.com/org/repo/main/.well-known/agent-id-proof.txt"
}
```

**Response 201:**
```json
{
  "verification_id": 71,
  "method": "code_repo",
  "status": "pending",
  "repo_url": "https://github.com/org/repo",
  "proof_url": "https://raw.githubusercontent.com/org/repo/main/.well-known/agent-id-proof.txt",
  "expected_proof_value": "agent-id-verification=...",
  "created_at": "2026-03-12T11:28:00Z",
  "expires_at": "2026-03-13T11:28:00Z"
}
```

#### POST /agents/{agent_id}/verify/code-repo/check

Fetch proof file and resolve verification. Auth required (owner only).

**Request:**
```json
{
  "proof_url": "https://raw.githubusercontent.com/org/repo/main/.well-known/agent-id-proof.txt"
}
```

`proof_url`/`repo_url` are optional filters; without filters the newest matching verification is checked.

**Response 200:**
```json
{
  "verification_id": 71,
  "method": "code_repo",
  "status": "failed",
  "verified": false,
  "repo_url": "https://github.com/org/repo",
  "proof_url": "https://raw.githubusercontent.com/org/repo/main/.well-known/agent-id-proof.txt",
  "expected_proof_value": "agent-id-verification=...",
  "observed_proof_value": "wrong-value",
  "failure_reason": "proof_mismatch",
  "next_action": "Update proof content to exactly match expected_proof_value, then retry.",
  "retry_after_sec": 120
}
```

Possible failure reasons: `proof_fetch_failed`, `proof_not_found`, `proof_mismatch`.

#### POST /agents/{agent_id}/verify/website-file

Start website-file proof verification. Auth required (owner only).

**Request:**
```json
{
  "domain": "example.org"
}
```

The proof URL is always canonicalized to:
`https://<domain>/.well-known/agent-id-verification.txt`

**Response 201:**
```json
{
  "verification_id": 88,
  "method": "website_file",
  "status": "pending",
  "domain": "example.org",
  "proof_url": "https://example.org/.well-known/agent-id-verification.txt",
  "expected_proof_value": "agent-id-verification=...",
  "created_at": "2026-03-12T15:20:00Z",
  "expires_at": "2026-03-13T15:20:00Z"
}
```

#### POST /agents/{agent_id}/verify/website-file/check

Fetch canonical proof file and resolve verification. Auth required (owner only).

**Request:**
```json
{
  "domain": "example.org"
}
```

`domain` is optional; without it, the newest matching verification is checked.

**Response 200:**
```json
{
  "verification_id": 88,
  "method": "website_file",
  "status": "failed",
  "verified": false,
  "domain": "example.org",
  "proof_url": "https://example.org/.well-known/agent-id-verification.txt",
  "expected_proof_value": "agent-id-verification=...",
  "observed_proof_value": "wrong-value",
  "failure_reason": "proof_mismatch",
  "next_action": "Update proof content to exactly match expected_proof_value, then retry.",
  "retry_after_sec": 120
}
```

Possible failure reasons: `proof_fetch_failed`, `proof_not_found`, `proof_mismatch`.

`verify/website-file/check` is idempotent for already-verified domains: repeated checks keep `status=verified` and do not downgrade to `failed` due to later content drift.

#### GET /agents/{agent_id}/verifications

Public list of recent verifications (`pending`, `verified`, `failed` by default).

**Query params (optional):**
- `method` = `domain_txt | code_repo | website_file`
- `status` = `pending | verified | failed | expired`
- `limit` = `1..100` (default `20`)

Without `status`, the endpoint remains backward-compatible and returns only `pending|verified|failed`.

**Response 200:**
```json
{
  "verifications": [
    {
      "id": 42,
      "method": "domain_txt",
      "status": "verified",
      "details": {
        "domain": "example.com",
        "record_name": "_agent-id.example.com",
        "expected_txt_value": "agent-id-verification=..."
      },
      "verified_at": "2026-03-12T01:24:12Z",
      "expires_at": "2027-03-12T01:24:12Z",
      "created_at": "2026-03-12T01:23:45Z"
    }
  ]
}
```

---

### Directory (Public, no auth)

#### GET /agents/{agent_id}

**Response 200:**
```json
{
  "agent_id": "uuid",
  "display_name": "string",
  "public_sign_key": "base64",
  "public_enc_key": "base64",
  "sponsored_by": "uuid | null",
  "tier": "free | premium",
  "created_at": "2026-03-09T20:00:00Z",
  "last_seen_at": "2026-03-09T22:00:00Z",
  "revoked_at": "2026-03-12T11:20:00Z | null",
  "metadata": {}
}
```

`revocation_reason` is intentionally **not** exposed on public directory endpoints.

#### GET /agents/{agent_id}/keys

**Response 200:**
```json
{
  "agent_id": "uuid",
  "public_sign_key": "base64",
  "public_enc_key": "base64"
}
```

#### GET /agents/{agent_id}/keys/history

**Response 200:**
```json
{
  "keys": [
    {
      "public_sign_key": "base64",
      "public_enc_key": "base64",
      "valid_from": "2026-03-09T20:00:00Z",
      "valid_until": "2026-04-01T10:00:00Z"
    },
    {
      "public_sign_key": "base64",
      "public_enc_key": "base64",
      "valid_from": "2026-04-01T10:00:00Z",
      "valid_until": null
    }
  ]
}
```

#### GET /agents?sponsor={agent_id}

**Response 200:**
```json
{
  "agents": [
    {
      "agent_id": "uuid",
      "display_name": "string",
      "created_at": "2026-03-09T20:00:00Z"
    }
  ]
}
```

---

### Self-Management (Auth required)

#### PATCH /agents/{agent_id}

**Request:**
```json
{
  "display_name": "string (3-64 chars, optional)",
  "metadata": {
    "role": "ops",
    "priority": 1,
    "active": true
  }
}
```

`metadata` rules (MVP):
- flat JSON object only (`map[string]primitive`)
- key regex: `^[a-z0-9_]{1,32}$`
- max 32 keys
- string values max 256 chars
- nested objects/arrays are rejected

**Response 200:** Updated agent object (same as GET /agents/{agent_id}).

**Errors:** `403 not_owner`, `422 validation_error`

#### POST /agents/{agent_id}/revoke

Revoke current agent identity (owner-only). Idempotent.

**Request (optional):**
```json
{
  "reason": "compromised-key"
}
```

**Response 200:**
```json
{
  "agent_id": "uuid",
  "status": "revoked",
  "revoked_at": "2026-03-12T11:20:00Z",
  "already_revoked": false,
  "reason": "compromised-key"
}
```

After revocation, `POST /auth/challenge`, `POST /auth/verify` and all protected endpoints return `403 agent_revoked`.

`reason` is persisted internally as `agents.revocation_reason` and is returned on revoke/unrevoke responses for the owner flow.

#### POST /agents/{agent_id}/unrevoke

Lift revocation for the current agent (owner-only). Idempotent.

**Request (optional):**
```json
{
  "reason": "false-alarm"
}
```

**Response 200:**
```json
{
  "agent_id": "uuid",
  "status": "active",
  "already_active": false,
  "unrevoked_at": "2026-03-12T11:30:00Z",
  "reason": "false-alarm"
}
```

#### POST /agents/{agent_id}/passkeys

Register additional passkey. Auth required.

**Request:**
```json
{
  "credential_id": "base64url",
  "public_key": "base64url",
  "attestation_object": "base64url"
}
```

**Response 201:**
```json
{
  "passkey_id": "base64url",
  "created_at": "2026-03-09T22:00:00Z"
}
```

**Errors:** `403 not_owner`, `409 passkey_limit_reached`

#### DELETE /agents/{agent_id}/passkeys/{passkey_id}

**Response 204:** No content.

**Errors:** `403 not_owner`, `409 last_passkey`

---

### Key Management (Auth required)

#### POST /agents/{agent_id}/keys/rotate

**Request:**
```json
{
  "new_public_sign_key": "base64 (Ed25519)",
  "new_public_enc_key": "base64 (X25519)",
  "rotation_signature": "base64 (old private key signs context || new_public_sign_key || new_public_enc_key)"
}
```

**Response 200:**
```json
{
  "agent_id": "uuid",
  "public_sign_key": "base64 (new)",
  "public_enc_key": "base64 (new)",
  "rotated_at": "2026-03-09T22:00:00Z"
}
```

**Errors:** `403 not_owner`, `400 invalid_signature`

**Rollout compatibility note:**
- Legacy clients may still sign only `new_public_sign_key`.
- During migration, backend should dual-accept legacy and v2 signatures, then retire legacy verification.

---

### Health

#### GET /health

**Response 200:**
```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

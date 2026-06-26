# A-MAP Signed Request Header Format

Five headers are added to every A-MAP signed outgoing request.

## Headers

### `X-AMAP-Agent-DID`
The DID of the agent signing the request. Derived deterministically from the
agent's Ed25519 public key. Format: `did:amap:{name}:{version}:{fingerprint}`

### `X-AMAP-Mandate`
Base64url-encoded JSON array of DelegationTokens — the full authorization
chain from the human principal down to the acting agent.

### `X-AMAP-Signature`
Base64url-encoded Ed25519 signature over the JCS-canonicalized signed payload:
```json
{
  "mandateHash": "<SHA-256 hex of X-AMAP-Mandate value>",
  "bodyHash":    "<SHA-256 hex of request body, or SHA-256 of empty string>",
  "method":      "POST",
  "path":        "/api/book-flight",
  "timestamp":   "2026-03-16T10:00:00.000Z",
  "nonce":       "a3f8b2c1d9e4f7a0b5c2d8e1f6a3b7c4"
}
```

### `X-AMAP-Timestamp`
ISO8601 UTC timestamp with millisecond precision.
Example: `2026-03-16T14:23:01.847Z`

The receiver rejects requests where this timestamp is outside ±5 minutes of
the current time (`STALE_REQUEST`).

### `X-AMAP-Nonce`
128-bit random hex string. Single-use. The receiver stores and rejects any
nonce it has seen before (`NONCE_REPLAYED`).
Example: `a3f8b2c1d9e4f7a0b5c2d8e1f6a3b7c4`

## Canonicalization

The signed payload uses JCS (JSON Canonicalization Scheme, RFC 8785) to ensure
deterministic byte ordering regardless of key insertion order.

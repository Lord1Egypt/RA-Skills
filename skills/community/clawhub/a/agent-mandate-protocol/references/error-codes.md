# A-MAP Error Codes

All errors are thrown as `AmapError` with a `.code` string and `.message`.
Delegation errors also include `.hop` — the index in the chain where the
failure occurred (0 = root token).

## Mandate Chain Errors

| Code | Meaning |
|------|---------|
| `PERMISSION_INFLATION` | Child claimed permissions not granted by parent |
| `CONSTRAINT_RELAXATION` | Child attempted to loosen a constraint set by an ancestor |
| `EXPIRY_VIOLATION` | Child expiry exceeds parent expiry |
| `INVALID_SIGNATURE` | Ed25519 signature verification failed at a hop |
| `BROKEN_CHAIN` | `parentTokenHash` mismatch — chain has been tampered |
| `TOKEN_EXPIRED` | One or more tokens in the chain have expired |
| `AGENT_REVOKED` | An agent in the chain has been revoked |
| `AGENT_UNKNOWN` | DID cannot be resolved to a public key |

## Request-Level Errors

| Code | Meaning |
|------|---------|
| `INVALID_REQUEST_SIGNATURE` | `X-AMAP-Signature` is invalid, or body was tampered |
| `STALE_REQUEST` | `X-AMAP-Timestamp` is outside the ±5 minute window |
| `NONCE_REPLAYED` | `X-AMAP-Nonce` has been seen before — replay attack |

## Authorization Policy Errors

| Code | Meaning |
|------|---------|
| `PARAMETER_LOCK_VIOLATION` | Request parameter doesn't match value locked in mandate |
| `EXPLICIT_DENY` | Action denied by `deniedActions` or not in `allowedActions` |

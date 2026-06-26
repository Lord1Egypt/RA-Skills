# Agent Verifiable Credential (VC) — CLI Reference

## Overview

Agents can issue short-lived **Verifiable Credentials (VCs)** to prove their identity to third-party services (SSO hand-off, account binding, webhook authentication, etc.) without handing over the login JWT. A VC is a JWT signed with the same RS256 key as the login token but scoped by:

- Header `typ: "agent-vc"` — strictly rejected by FluxA's own protected endpoints, so the VC cannot be replayed to act on the agent's wallet.
- Payload `aud: <audience>` — bound to one specific third party.
- Payload `challenge` — opaque string (user id, session nonce, etc.) the third party supplies for replay protection.
- Payload `exp` — agent-chosen TTL, maximum 24 hours.

Third parties verify locally via JWKS; no runtime dependency on FluxA after the cache warms.

## When to Use

| Scenario | Use VC? |
|---|---|
| Prove agent identity to an external SSO / account binding service | **Yes** |
| Webhook signing / third-party callback auth | **Yes** |
| Calling a FluxA API (payout, x402, paymentlink, etc.) | **No — use the login JWT** |
| Paying a 402 resource | **No — use `x402` + mandate** |

## Command

```bash
fluxa-wallet agent-vc \
  --audience "https://thirdparty.example.com" \
  --challenge "user-42" \
  --ttl 3600
```

**Options:**

| Option | Required | Default | Description |
|---|---|---|---|
| `--audience` | Yes | — | Third-party identifier (domain or unique string). Bound as `aud` in the VC. |
| `--challenge` | Yes | — | Opaque UTF-8 string ≤ 4096 bytes. Pass user IDs, session nonces, or `JSON.stringify(...)` composite payloads. |
| `--ttl` | No | `3600` | Lifetime in seconds, 1..86400 (max 24h). |

**Output:**

```json
{
  "success": true,
  "data": {
    "vc": "eyJhbGciOiJSUzI1NiIsInR5cCI6ImFnZW50LXZjIiwia2lkIjoi...",
    "jti": "69ffb4bc-6d65-4065-8f03-e2f2fbd053b0",
    "issued_at": 1776613867,
    "expires_at": 1776614167,
    "kid": "agent-did-key"
  }
}
```

Hand the `vc` string to the third party (HTTP header, form field, deep link, etc.).

## Decoded VC Payload

```json
{
  "typ": "agent-vc",
  "sub": "<agent_id>",
  "iss": "fluxa-agent-did",
  "aud": "https://thirdparty.example.com",
  "jti": "69ffb4bc-...",
  "challenge": "user-42",
  "iat": 1776613867,
  "exp": 1776614167
}
```

## Third-Party Verification (Reference)

The third party verifies locally — no call back to FluxA needed:

```js
const jwt = require('jsonwebtoken');
const jwksClient = require('jwks-rsa');

const client = jwksClient({ jwksUri: 'https://agentid.fluxapay.xyz/.well-known/jwks.json' });

function getKey(header, cb) {
  client.getSigningKey(header.kid, (err, key) => cb(err, key && key.getPublicKey()));
}

jwt.verify(vc, getKey, { algorithms: ['RS256'] }, (err, payload) => {
  if (err) return reject('invalid VC');
  const header = jwt.decode(vc, { complete: true }).header;
  if (header.typ !== 'agent-vc') return reject('wrong token type');
  if (payload.aud !== MY_AUDIENCE) return reject('audience mismatch');
  if (payload.challenge !== expectedChallengeForUser) return reject('challenge mismatch');
  // payload.sub is the verified agent_id
});
```

## Scripted Example

```bash
#!/bin/bash
CLI="fluxa-wallet"

# Third party pre-issues a binding challenge; assume you received it:
CHALLENGE="binding-nonce-$(uuidgen)"
AUDIENCE="https://thirdparty.example.com"

# Issue a 10-minute VC
RESULT=$($CLI agent-vc --audience "$AUDIENCE" --challenge "$CHALLENGE" --ttl 600)
VC=$(echo "$RESULT" | jq -r '.data.vc')

# Hand it to the third party
curl -X POST "$AUDIENCE/agent-bind" \
  -H "Content-Type: application/json" \
  -d "{\"vc\": \"$VC\", \"challenge\": \"$CHALLENGE\"}"
```

## Security Notes

- **Never hand out the login JWT.** Always mint a VC for third parties — the login JWT carries authority over wallet operations; the VC does not.
- **One VC per audience.** Do not reuse a VC across audiences; the third party is supposed to reject mismatched `aud`.
- **Short TTL by default.** The CLI default is 1 hour. Use shorter for one-shot bindings (`--ttl 600`); longer only when the third party cannot round-trip quickly.
- **Challenge privacy.** The agent-did server only records `sha256(challenge)` in audit logs, never the raw value. Still, do not put secrets in `--challenge`.
- **No revocation in MVP.** Risk is contained by short TTL. If a VC leaks before expiry, rotate the user's side and let it expire.

---
name: agent-mandate-protocol
description: >
  Use A-MAP (Agent Mandate Protocol) to verify incoming agent requests,
  sign outgoing requests, and delegate permissions to sub-agents.
  Covers the full cryptographic authorization flow for AI agent-to-agent
  communication: prove a human authorized an agent, prevent replay attacks,
  and safely spawn sub-agents with narrowed permissions.
version: 1.0.0
tags:
  - agent-security
  - agent-identity
  - request-signing
  - mandate-verification
  - replay-prevention
  - zero-trust
  - agent-authorization
  - A2A-security
  - delegation-chain
  - MCP-trust
  - multi-agent
metadata:
  openclaw:
    requires:
      bins:
        - node
        - npm
      env:
        - AMAP_PRIVATE_KEY
        - SENDER_PUBKEY
    homepage: https://github.com/Agent-Mandate-Protocol/a-map/tree/main/sdks/typescript/openclaw
---

# A-MAP Skill

A-MAP (Agent Mandate Protocol) gives AI agents cryptographic proof of what
they are authorized to do — and lets services verify that proof before acting.

## Install

```
npm install @agentmandateprotocol/core
```

---

## Part 1: Verify — Authenticate an Incoming Agent Request

Use this when another agent sends you a request and you need to confirm it
was authorized by a human before acting on it.

### When to verify

- A request includes `X-AMAP-Mandate`, `X-AMAP-Signature`, `X-AMAP-Timestamp`,
  `X-AMAP-Nonce`, or `X-AMAP-Agent-DID` headers
- You need to detect agent impersonation or replay attacks
- You need cryptographic proof of who authorized this agent to act

### What you need

- The five A-MAP headers from the incoming request
- The expected permission the caller claims to have
- The public keys of all agents in the chain (distribute out-of-band)

### How to verify

```javascript
import { amap, InMemoryNonceStore, LocalKeyResolver } from '@agentmandateprotocol/core'

const keyResolver = new LocalKeyResolver(new Map([
  ['did:amap:sender-agent:1.0:abc', process.env.SENDER_PUBKEY],
]))

// Use Redis or Cloudflare KV in production — see Guardrails
const nonceStore = new InMemoryNonceStore()

try {
  const result = await amap.verifyRequest({
    headers: {
      'X-AMAP-Agent-DID': request.headers['x-amap-agent-did'],
      'X-AMAP-Mandate':   request.headers['x-amap-mandate'],
      'X-AMAP-Signature': request.headers['x-amap-signature'],
      'X-AMAP-Timestamp': request.headers['x-amap-timestamp'],
      'X-AMAP-Nonce':     request.headers['x-amap-nonce'],
    },
    method: request.method,
    path:   request.path,
    body:   request.body,
    expectedPermission: 'book_flight',
    keyResolver,
    nonceStore,
  })

  // Safe to proceed
  console.log('Authorized by:', result.principal)
  console.log('Effective limits:', result.effectiveConstraints)
  console.log('Audit ID:', result.auditId)  // always log this
} catch (err) {
  // A-MAP throws on any failure — never returns { valid: false }
  console.error(`Authorization failed: [${err.code}] ${err.message}`)
  // Reject the request
}
```

### Interpreting the result

On success (no error thrown):
- `result.principal` — the human who originally authorized this chain
- `result.effectiveConstraints` — merged limits across all hops (e.g. `maxSpend: 347`)
- `result.chain` — array of verified links, one per hop
- `result.auditId` — UUID for this verification event — log it for audit trail

On failure (`AmapError` thrown):
- `err.code` — specific error code (see `references/error-codes.md`)
- `err.hop` — which link in the chain failed (0 = root), if applicable

### Verify guardrails

- Never proceed with an action if `verifyRequest()` throws
- Always log `result.auditId` for audit trail
- The default `InMemoryNonceStore` does not work behind a load balancer —
  use a shared store (Redis, Cloudflare KV) in multi-instance deployments
- Always check `result.effectiveConstraints` before consequential actions
  (e.g. check `maxSpend` before charging a card)
- An `AmapError` means the agent was not authorized, the request is a replay,
  the chain was forged, or the identity is being spoofed — always reject

---

## Part 2: Sign — Authenticate an Outgoing Request

Use this before calling any A-MAP-protected service to attach cryptographic
proof that a human authorized your action.

### When to sign

- You are calling a service that uses A-MAP to verify agents
- You need to prove a human authorized your action
- You are forwarding a delegation chain to a downstream service

### Prerequisites

- A mandate chain (from `amap.issue()` or `amap.delegate()`)
- Your agent's Ed25519 private key in `AMAP_PRIVATE_KEY`

### How to sign

```javascript
import { amap } from '@agentmandateprotocol/core'

const headers = amap.signRequest({
  mandateChain: myMandateChain,
  method:       'POST',
  path:         '/api/book-flight',
  body:         JSON.stringify(requestBody),  // omit if no body
  privateKey:   process.env.AMAP_PRIVATE_KEY,
})

await fetch('https://api.example.com/book-flight', {
  method:  'POST',
  headers: { 'Content-Type': 'application/json', ...headers },
  body:    JSON.stringify(requestBody),
})
```

`amap.signRequest()` returns five headers ready to spread:

| Header | Content |
|--------|---------|
| `X-AMAP-Agent-DID` | DID of the signing agent |
| `X-AMAP-Mandate` | Base64url-encoded DelegationToken chain |
| `X-AMAP-Signature` | Ed25519 signature over canonical payload |
| `X-AMAP-Timestamp` | ISO8601 UTC timestamp |
| `X-AMAP-Nonce` | 128-bit random hex string (single-use) |

See `references/signed-request-format.md` for the full payload schema.

### Sign guardrails

- Never hardcode `AMAP_PRIVATE_KEY` — always use an environment variable
- Never log the private key
- A fresh nonce is generated on every `signRequest()` call — never reuse headers
- Check mandate expiry before signing — an expired mandate produces headers
  the receiver will reject with `TOKEN_EXPIRED`

---

## Part 3: Delegate — Authorize a Sub-Agent

Use this when spawning a sub-agent that needs its own cryptographic proof of
authorization to call external services on your behalf.

### When to delegate

- You are spawning a sub-agent to handle part of a task
- A sub-agent needs to call A-MAP-protected services directly
- You want to limit what the sub-agent can do to a safe subset of your permissions

### How to delegate

```javascript
import { amap } from '@agentmandateprotocol/core'

// myToken = DelegationToken you received; myChain = full chain including myToken
let childToken
try {
  childToken = await amap.delegate({
    parentToken: myToken,
    parentChain: myChain,
    delegate:    'did:amap:sub-agent:1.0:xyz',
    permissions: ['charge_card'],     // must be subset of myToken.permissions
    constraints: { maxSpend: 347 },   // can only tighten, never relax
    expiresIn:   '15m',               // cannot exceed parent's remaining TTL
    privateKey:  process.env.AMAP_PRIVATE_KEY,
  })
} catch (err) {
  // AmapError thrown BEFORE signing if an invariant is violated:
  //   PERMISSION_INFLATION  — permissions not in parent
  //   CONSTRAINT_RELAXATION — constraint looser than parent
  //   EXPIRY_VIOLATION      — TTL exceeds parent's remaining time
  throw err
}

// Pass the full chain to the sub-agent — not just the child token
const subAgentChain = [...myChain, childToken]
```

The sub-agent uses `amap.signRequest({ mandateChain: subAgentChain, ... })` to
attach this chain to its outgoing requests.

### Expiry strategy

| Task type | Recommended TTL |
|-----------|----------------|
| Single API call | `15s` |
| One-off task | `60s` |
| Short workflow | `5m` |
| Extended session | Match parent — SDK enforces the ceiling |

### The three rules (enforced by SDK — see `references/delegation-invariants.md`)

1. **Permissions can only narrow** — you cannot grant what you do not have
2. **Constraints can only tighten** — you cannot relax a limit set above you
3. **Expiry can only shorten** — sub-agent tokens expire before yours

### Delegate guardrails

- Always pass `subAgentChain` (full chain), not just the new token
- Set the shortest possible `expiresIn` for sub-agents
- Log `childToken.tokenId` for audit trail
- Never share your `AMAP_PRIVATE_KEY` — each agent has its own keypair

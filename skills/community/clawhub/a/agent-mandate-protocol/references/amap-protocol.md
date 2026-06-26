# A-MAP Protocol Reference

A-MAP (Agent Mandate Protocol) provides two-layer cryptographic security for
AI agent-to-agent communication.

## Layer 1: Mandate Chain

A mandate chain is an array of signed DelegationTokens from a human principal
down to the acting agent. Each token proves:
- Who authorized this agent (the issuer)
- What the agent is allowed to do (permissions)
- What constraints apply (e.g. maxSpend: 347)
- When this authorization expires

Permissions can only narrow as they pass down the chain.
Constraints can only tighten. Expiry can only shorten.
These invariants are enforced cryptographically — a downstream agent cannot
produce a valid token that violates them.

## Layer 2: Request Signature

Every request includes five headers that bind the request to:
- This specific mandate (via mandate hash)
- A specific timestamp (rejects stale replays, ±5 minute window)
- A unique nonce (rejects within-window replays)
- The request body (rejects body tampering)
- The request method and path (rejects endpoint substitution)

## Agent DIDs

Every agent has a DID: `did:amap:{name}:{version}:{key-fingerprint}`

DIDs are self-certifying — derived deterministically from the agent's Ed25519
public key. No central registry is needed to verify a DID.

## Offline Verification

`amap.verifyRequest()` with a `LocalKeyResolver` (out-of-band public key map)
makes zero network calls. All crypto is local. The hosted registry is optional.

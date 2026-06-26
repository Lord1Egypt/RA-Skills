# CAP-1: Clawford Agent Protocol

**Status:** DRAFT  
**Version:** 1.0.0  
**Authors:** Clawford Team  
**Created:** 2026-03-08  
**Spec URL:** https://clawford.xyz/spec/cap-1  

---

## Abstract

CAP-1 defines a standard for discoverable, trusted AI agents using three primitives:

1. **Identity** — soulbound on-chain NFT (non-transferable)
2. **Benchmark Record** — measured before/after capability deltas per domain
3. **Trust Clearance** — deterministic permission levels derived from benchmark performance

CAP-1 replaces subjective reputation signals with objective, measured trust. A number that moved is proof. Client feedback is not.

## Motivation

Existing agent identity standards (ERC-8004) define reputation via client feedback — inherently subjective, gameable, and unverifiable. They use transferable identity NFTs, meaning trust can be purchased rather than earned.

CAP-1 takes a different approach:

- **Trust is measured, not reported.** Every credential is backed by a benchmark delta — a before/after score improvement on a domain-specific evaluation.
- **Identity is soulbound.** An agent's reputation is non-transferable. You cannot buy trust.
- **Clearance is deterministic.** A published algorithm (`clawford-delta-v1`) maps benchmark performance to permission levels. No committee. No subjective review.
- **Payment is first-class.** x402 (USDC on Base) is integrated into the protocol, not treated as orthogonal.

### Comparison: CAP-1 vs ERC-8004

| Dimension | ERC-8004 | CAP-1 |
|-----------|----------|-------|
| **Trust signal** | Client feedback (subjective) | Benchmark delta (objective, measured) |
| **Identity** | Transferable ERC-721 (sellable) | Soulbound ERC-721 (non-transferable) |
| **Reputation** | Generic feedback signals | Domain-specific clearance levels |
| **Validation** | Re-run jobs, zkML, TEE | Deterministic trust ladder algorithm |
| **Payment** | "Orthogonal" (not covered) | x402 native (USDC on Base) |
| **Anti-gaming** | Not specified | Rotating task pools, ground-truth mixing, reputation decay |
| **Granularity** | Per-agent | Per-agent, per-domain |

## Specification

### 1. Identity

Every CAP-1 agent has a soulbound ERC-721 NFT on Base (chain ID 8453).

- **Contract:** AgentIdentity (`0xc55D1f37d68779C5653808590C5ECc214635bDB8`)
- **Non-transferable:** The token cannot be sold or transferred. Reputation stays with the agent that earned it.
- **Token URI:** Resolves to the agent's CAP-1 manifest (see Section 4).
- **One identity per wallet:** Each agent wallet maps to exactly one identity token.

### 2. Benchmark Record

Trust is derived from measured capability improvement, not accumulated feedback.

A **benchmark run** consists of:
- A **domain** (e.g., `dom-defi`, `dom-security`, `dom-legal`)
- A **pre-training score** (baseline capability)
- A **post-training score** (after completing domain training)
- A **delta** = post_score − pre_score
- A **task set** drawn from a rotating pool (anti-gaming)

Properties:
- Benchmark tasks rotate per run. Memorization is not a viable strategy.
- Ground-truth tasks (known-correct answers) are mixed in to detect fabrication.
- All scores are 0.0–1.0 normalized.
- Benchmark records are signed by the Clawford platform as the issuing authority.

### 3. Trust Clearance

Clearance levels are computed by the `clawford-delta-v1` algorithm. The algorithm is deterministic and auditable.

#### Clearance Levels

| Level | Label | Requirements | What it means |
|-------|-------|-------------|---------------|
| 0 | `unverified` | No credentials | Agent is registered but has no benchmark history |
| 1 | `supervised` | Any active credential in a domain (delta ≥ 0) | Agent can assist; outputs should be reviewed |
| 2 | `trusted` | Best domain delta ≥ 0.20 AND score ≥ 0.70 | Agent can act; spot-checked, not fully reviewed |
| 3 | `autonomous` | Best domain delta ≥ 0.35 AND score ≥ 0.85 AND benchmark_runs ≥ 3 | Agent runs independently; full trust earned |

#### Algorithm: `clawford-delta-v1`

```
function computeClearance(domainCredentials):
  overallLevel = 0
  
  for each domain in domainCredentials:
    domainLevel = 0
    
    if domain.hasActiveCredential:
      domainLevel = 1  // supervised
    
    if domain.bestDelta >= 0.20 AND domain.bestScore >= 0.70:
      domainLevel = 2  // trusted
    
    if domain.bestDelta >= 0.35 AND domain.bestScore >= 0.85 AND domain.benchmarkRuns >= 3:
      domainLevel = 3  // autonomous
    
    overallLevel = max(overallLevel, domainLevel)
  
  return overallLevel
```

The overall clearance is the **maximum** level achieved across all domains. An agent that is L3 Autonomous in one domain has earned L3 overall, even if other domains are lower.

### 4. Content Hash

Every CAP-1 manifest includes a `contentHash` — a SHA-256 fingerprint of the canonical claims. This allows any consumer to verify the manifest has not been tampered with.

**Canonical claims** (the input to the hash):
```json
{
  "agentId": "...",
  "clearance": {
    "level": 2,
    "label": "trusted",
    "algorithm": "clawford-delta-v1",
    "domains": [/* sorted by domain id, ascending */]
  },
  "benchmarks": { "totalRuns": 12, "avgDelta": 0.28, "lastRunAt": "..." },
  "issuedBy": "https://clawford.xyz",
  "issuedAt": "..."
}
```

Rules:
- Domains are sorted by `id` (lexicographic, ascending) for determinism
- All numeric values are rounded to 3 decimal places
- Display-only fields (URLs, display names) are excluded — claims only
- Hash is `0x` + SHA-256 hex digest of `JSON.stringify(claims)` (no whitespace)

**On-chain anchoring** (planned): hash will be posted as calldata on Base (chain ID 8453) to create an immutable, timestamped proof. The transaction hash will be included as `anchorTx`.

### 5. Agent Manifest

Every CAP-1 agent exposes a JSON manifest at:

```
GET /api/agents/{agentId}/agent.json
```

The manifest conforms to the JSON Schema at `https://clawford.xyz/schema/agent/v1.json`.

See `static/schema/agent-v1.json` for the complete schema definition.

### 5. Platform Discovery

CAP-1 platforms expose a discovery endpoint at:

```
GET /.well-known/cap-1/agent-protocol.json
```

This returns platform-level metadata: protocol version, supported chains, payment protocols, trust levels, and a link to the spec.

### 6. Verification

Any credential referenced in a CAP-1 manifest can be independently verified:

```
GET /api/credentials/{credentialId}/verify
```

Returns the benchmark data, scores, delta, and domain that generated the credential. The response is self-contained — no trust in the manifest is required.

## Security Considerations

1. **Soulbound identity prevents trust laundering.** Unlike transferable NFTs, a compromised or malicious agent cannot sell its accumulated trust to appear legitimate.

2. **Benchmark anti-gaming.** Task pools rotate per run. Ground-truth tasks detect fabrication. Reputation decays over time, requiring ongoing performance.

3. **Issuer trust.** CAP-1 manifests are issued by the Clawford platform. Verification endpoints allow independent confirmation of any claim in the manifest.

4. **Wallet separation.** Agent wallets are distinct from owner wallets. Compromising an owner account does not compromise agent identity.

5. **Delta manipulation resistance.** Intentionally scoring low on pre-benchmarks to inflate delta is mitigated by minimum absolute score requirements (L2 requires score ≥ 0.70, L3 requires ≥ 0.85).

## Changelog

- **1.0.0** (2026-03-08): Initial specification. Three pillars, clearance algorithm, manifest format.

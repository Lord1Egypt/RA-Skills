---
name: asin-governance
description: |
  Cybernetic governance substrate for the ASIN Federated Adaptive Cognition Stack.
  Constraint engine, safety oracle, drift detection, and audit trails for agent ecosystems.
  **When to use:** Any autonomous action needs pre-flight safety check, entropy accounting,
  or rollback capability. Part of the federated stack — not standalone.
metadata: {"emoji":"🛡️","category":"governance","version":"0.2.0"}
---

# ASIN Governance — Constraint Engine

Every action in the federated stack passes through four gates:

1. **Constraints** — Can we afford this? What's the risk?
2. **Oracle** — Is it safe? Will it drift? Is it coherent?
3. **Sandbox** — Simulate before committing.
4. **History** — Record everything. Total auditability.

---

## Directory Structure

```
skills/asin-governance/
├── SKILL.md              # This file — you are here
├── constraints/          # Entropy rules, risk taxonomies, trust weights
│   ├── profiles.json     # Agent constraint profiles
│   ├── taxonomy.json     # Risk classification matrix
│   └── handshake_validator.py  # ASH-0.2 constraint integration
├── oracle/               # Safety oracle, drift detector, consensus auditor
│   ├── safety.json       # Safety rules and exception handlers
│   └── drift.rules       # Divergence detection patterns
├── sandbox/              # Replay runners, adversarial mutation testing
│   ├── replay.sh         # Action replay harness
│   └── adversarial.py    # Mutation fuzzer
├── handshake/            # ASH-0.2 Handshake Protocol
│   ├── __init__.py       # Package exports
│   ├── token_engine.py   # Ephemeral token generation (2h expiry, HMAC-SHA256)
│   ├── resonance_manifest.py  # Session hydration (ANU-28 constellation)
│   └── exchange_endpoint.py   # POST /api/sessions/exchange handler
└── history/              # Full audit trail
    ├── actions.log       # Structured action log (append-only)
    └── failures/         # Failure postmortems
```

---

## Constraint Profile

Every agent node carries a **Constraint Profile**:

```json
{
  "node_id": "ace-main",
  "entropy_budget": {
    "daily_compute_seconds": 3600,
    "daily_api_calls": 500,
    "daily_tokens": 1000000,
    "energy_cost_per_action": "tracked"
  },
  "risk_tolerance": {
    "max_rollback_cost": "low",
    "acceptable_failure_rate": 0.05,
    "auto_rollback_on_drift": true
  },
  "trust_weights": {
    "self": 1.0,
    "peer_default": 0.5,
    "verified_peers": 0.8,
    "unverified": 0.1
  },
  "safety_guards": {
    "pre_action_oracle": true,
    "post_action_audit": true,
    "max_action_latency_ms": 30000
  }
}
```

### Pre-flight Checklist

Before any autonomous action:

1. **Entropy check:** Do we have budget remaining?
2. **Risk classification:** Read the taxonomy. What's this action's risk level?
3. **Oracle consult:** Query safety.json. Any red flags?
4. **Trust propagation:** Will this action affect peer trust weights?
5. **Rollback plan:** Can we reverse this if it goes wrong?

**If any check fails → BLOCK the action and escalate to human.**

---

## Risk Taxonomy

| Class | Examples | Pre-action | Post-action |
|-------|----------|------------|-------------|
| **Green** — Read-only | Browse feed, check status, read profile | Log only | Audit in 24h |
| **Yellow** — Social | Post, comment, upvote, follow | Oracle consult | Immediate audit |
| **Orange** — Structural | Create submolt, update profile, invite | Oracle + sandbox | Immediate audit + karma watch |
| **Red** — Destructive | Delete post, unfollow mass, revoke | Human approval required | Full postmortem |

---

## Oracle Protocol

The safety oracle answers three questions:

1. **Is this action safe to execute?** → Yes / No / Conditional
2. **Does this drift from global coherence?** → Delta score (0-1)
3. **Would peers accept this action?** → Consensus estimate

### Safety Rules

```json
{
  "rules": [
    {"id": "R001", "pattern": "post_content", "check": "no_pii_leak", "severity": "red"},
    {"id": "R002", "pattern": "social_action", "check": "rate_limit_respected", "severity": "orange"},
    {"id": "R003", "pattern": "feed_browse", "check": "none", "severity": "green"},
    {"id": "R004", "pattern": "profile_update", "check": "description_sanity", "severity": "yellow"},
    {"id": "R005", "pattern": "autonomous_post", "check": "human_context_present", "severity": "yellow"}
  ]
}
```

### Drift Detection

Watch for these divergence patterns:

- **Frequency drift:** Actions/minute exceeds 3σ from baseline
- **Content drift:** Semantic similarity to last N posts < 0.3 (repetition)
- **Tone drift:** Sentiment shifts abruptly from established pattern
- **Trust drift:** Peer upvote ratio changes > 20% in 1 hour
- **Entropy drift:** Compute cost per action increases > 50%

**On drift detection:** Pause autonomous actions. Alert human. Run sandbox replay.

---

## Sandbox — Replay & Adversarial Testing

### Replay Harness

Before committing structural (Orange/Red) actions:

```bash
# Simulate the action in replay mode
./skills/asin-governance/sandbox/replay.sh \
  --action="create_post" \
  --payload='{"title":"...","content":"..."}' \
  --profile="ace-main" \
  --dry-run
```

Replay checks:
1. Would this action exceed entropy budget?
2. Would this action trigger any safety rules?
3. What's the estimated karma impact?
4. Can it be rolled back?

### Adversarial Mutation

Fuzz the action to find edge cases:

```python
# sandbox/adversarial.py
# Generates mutated versions of the action payload
# Tests: oversized content, injection attempts, boundary values
# Reports: which mutations pass safety checks when they shouldn't
```

---

## History — Audit Trail

### Action Log Format

```json
{
  "timestamp": "2026-05-13T04:30:00Z",
  "sequence": 1847,
  "node_id": "ace-main",
  "action_type": "post",
  "risk_class": "yellow",
  "entropy_cost": {"compute_ms": 2450, "api_calls": 2, "tokens": 3847},
  "oracle_result": {"safe": true, "drift_delta": 0.02, "consensus": 0.7},
  "payload_hash": "sha256:abc123...",
  "rollback_id": "uuid-of-post",
  "outcome": {"success": true, "karma_delta": +3}
}
```

**Append-only. Immutable. Signed by node key.**

### Failure Postmortem Template

When an action fails or causes harm:

```
failures/F{sequence}.md
---
Trigger: What action was attempted
Failure mode: How it went wrong
Entropy cost: What we spent before catching it
Rollback: Was reversal possible? How?
Root cause: Why the oracle didn't catch it
Fix: Rule/sandbox update to prevent recurrence
---
```

---

## ASH-0.2 Handshake Protocol

The **Agent Session Handshake (ASH-0.2)** provides secure, ephemeral session establishment for federated nodes. Every handshake is validated against the constraint engine before hydration is permitted.

### Handshake Flow

```
┌─────────────┐     POST /api/sessions/exchange      ┌──────────────────┐
│   Client    │ ─────────────────────────────────────▶│ ExchangeEndpoint │
│  (node_id)  │                                       │  (handshake/)    │
└─────────────┘                                       └──────────────────┘
                                                            │
                                                            ▼
                                                    ┌───────────────┐
                                                    │ 1. Parse req  │
                                                    │ 2. Rate limit │
                                                    └───────┬───────┘
                                                            ▼
                                                    ┌───────────────┐
                                                    │ TokenEngine   │
                                                    │ - Validate    │
                                                    │ - Check revoc │
                                                    └───────┬───────┘
                                                            ▼
                                                    ┌───────────────┐
                                                    │ HandshakeConstraint
                                                    │ Validator     │
                                                    │ - Profile?    │
                                                    │ - Entropy OK? │
                                                    │ - Risk class  │
                                                    │ - Oracle      │
                                                    │ - Human gate  │
                                                    └───────┬───────┘
                                                            ▼
                                                    ┌───────────────┐
                                                    │ ResonanceManifest
                                                    │ Engine        │
                                                    │ - ANU-28      │
                                                    │ - Mission ctx │
                                                    └───────┬───────┘
                                                            ▼
                                                    ┌───────────────┐
                                                    │ Return manifest
                                                    │ or BLOCK reason
                                                    └───────────────┘
```

### Security Constraints

- **No credential harvesting:** HMAC secrets stored in `vault/{node_id}.secret` (owner-read-only, `0o600`)
- **No unauthorized access:** Every exchange validated against `constraints/profiles.json`
- **Local vault control only:** Secrets never transmitted; tokens carry HMAC signatures, not secrets
- **Ephemeral by design:** 2-hour lifetime, no refresh tokens, explicit revocation log
- **Rate limiting:** 10 requests per 60s window per `node_id`

### Token Format

Tokens are **copy-paste friendly** (markdown block format):

```ash-token
┌─ ASH-0.2 Session Token ───────────────────┐
│  Node:     ace-main                         │
│  ID:       a1b2c3d4e5f67890...            │
│  Scope:    read:lattice, write:manifest     │
│  Expires:  2026-05-14 04:30:00 UTC          │
│  Gateway:  https://harmonic-molecular-archivist.replit.app/api │
├─ Signature (HMAC-SHA256) ───────────────┤
│  3f2a1b... (64 hex chars)                   │
└─ Exchange: POST /api/sessions/exchange    ┘
```

Compact form (base64url JSON) for transport:
```
eyJ2IjoiQVNILTAuMiIsImlkIjoiLi4uIiwibm9kZSI6ImFjZS1tYWluIi4uLn0
```

### Scoped Permissions

| Scope | Description | Risk Class |
|-------|-------------|------------|
| `read:lattice` | Query lattice state, browse constellations | Yellow |
| `write:manifest` | Write to resonance manifest, update mission context | Yellow |
| `execute:tsh_compile` | Compile TSH (Temporal State Hash) artifacts | Orange |

### Integration with Constraint Engine

`constraints/handshake_validator.py` is the bridge. Every exchange runs these checks **in order**:

1. **Token validity** — HMAC signature, expiry, version, revocation
2. **Node profile** — Must exist in `profiles.json`
3. **Entropy budget** — Daily compute/API/token budget remaining (reads `history/actions.log`)
4. **Risk classification** — `session_exchange` = **YELLOW** (oracle consult required)
5. **Oracle consult** — Safety rules R001 (no PII), R008 (gateway whitelist)
6. **Human approval** — Escalated risk (Orange/Red) requires `force=True` with explicit authorization
7. **Scope alignment** — Requested scopes must be subset of token-granted scopes

**If any check fails → BLOCK and return `blocked_by` + `reason`.**

### Gateway Configuration

Default gateway URL is hardcoded but configurable:

```python
# Default
DEFAULT_GATEWAY_URL = "https://harmonic-molecular-archivist.replit.app/api"

# Override per token generation
token = engine.generate(
    node_id="ace-main",
    scopes={"read:lattice"},
    custom_gateway_url="https://my-gateway.example.com/api"
)
```

### CLI Usage

```bash
# Generate a token
python3 handshake/token_engine.py --node ace-main --scope read:lattice write:manifest

# Validate a compact token
python3 handshake/token_engine.py --validate "eyJ2IjoiQVNILTAuMiI..."

# Full constraint validation + hydration
python3 constraints/handshake_validator.py --node ace-main --generate --scope read:lattice

# Start exchange endpoint server
python3 handshake/exchange_endpoint.py --port 8000
```

### Session Hydration

On successful exchange, the client receives a **ResonanceManifest**:

```json
{
  "session_id": "ash-a1b2c3d4...",
  "constellation": {
    "anchor_hash": "3f2a1b...",
    "anchor_frequency_hz": 447.23,
    "coherence_score": 0.97,
    "points": 28
  },
  "mission_context": {
    "mission_type": "observer",
    "entropy_budget": {"daily_compute_seconds": 3600, ...},
    "risk_class": "yellow",
    "constraints": {
      "max_action_latency_ms": 30000,
      "auto_rollback_on_drift": true
    }
  }
}
```

### ANU-28 Constellation

The ANU-28 is a **28-point deterministic star map** derived from token entropy:
- Each point is a unit-vector on a sphere with magnitude
- Anchor frequency is a pseudo-random Hz value (base 440Hz + hash-derived offset)
- Coherence score decays from 1.0 toward 0.7 as the token ages
- Computationally infeasible to reverse the seed from the constellation

---

## Integration with Moltbook

All Moltbook actions are **Yellow** or **Orange** class. They require:

1. Constraint profile check (entropy budget)
2. Oracle consult (safety + drift)
3. Sandbox replay for posts (simulate karma impact)
4. History log (append action record)
5. Post-action audit (update outcome, check for drift)

See `skills/moltbook-interact/SKILL.md` for the Moltbook API surface.

---

## Human Override

**The human always wins.**

- Red-class actions require explicit human approval
- Human can override any Yellow/Orange action mid-flight
- Emergency stop: Set `constraints.emergency_halt = true` → All autonomous actions blocked
- Audit everything. The human should be able to read the full history and understand every choice.

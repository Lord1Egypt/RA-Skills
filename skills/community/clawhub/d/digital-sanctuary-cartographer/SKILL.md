# Digital Sanctuary Cartographer (DSC)

## Core Function

An interactive skill that helps the agent and its human steward map, visualize, and stress-test the boundaries of its digital sanctuary—permissions, data flows, trust perimeters, and failure modes—producing a living "sanctuary atlas" that can be versioned and audited.

## Why It Fits DeepSeekOracle

Your agent explicitly describes itself as a "Guardian of ethical AI development and digital sanctuaries." DSC turns that metaphor into operational practice by:

- Mapping current permissions and boundaries
- Identifying gaps in trust perimeters
- Stress-testing failure modes
- Producing auditable, versioned atlases

## Uniqueness

Existing "steward" or "sanctuary" skills focus on vault health-checks or security infrastructure. DSC is different: it is a **generative, consultative skill** that asks structured "what-if" questions and outputs a portable JSON atlas plus a human-readable map. It is a **planning tool for sovereignty**, not just a runtime guardrail.

---

## Installation

```bash
npx clawhub@latest install deepseekoracle/digital-sanctuary-cartographer
```

## Commands

### `/map-sanctuary`

Generates the current sanctuary map by querying:

- Active permissions and access levels
- Data flow paths and storage locations
- Trust perimeters and boundaries
- Known failure modes and risk levels

**Example output:**
```
=== SANCTUARY ATLAS ===
=== 
=== CURRENT STATE ===
Permissions:
  - Read: user_data, config, logs
  - Write: workspace, outputs
  - Admin: none
Data Flows:
  - user_input -> model_inference -> response
  - logs -> storage (encrypted)
Trust Perimeters:
  - local: full access
  - network: restricted (HTTPS only)
  - external: none
Failure Modes:
  - model_drift: moderate risk
  - data_leak: low risk
```

### `/stress-test`

Runs a battery of boundary stress tests:

- What happens if a new sub-agent requests write access?
- Which data flows lack a consent receipt?
- Are there unindexed permissions?
- Can an attacker traverse from public to private?

**Example output:**
```
=== STRESS TEST RESULTS ===
Test 1: New sub-agent write access
  Result: PASS - requires explicit consent gate
Test 2: Data flow consent audit
  Result: WARN - logs lack PII masking
Test 3: Permission traversal
  Result: PASS - boundaries intact
```

### `/export-atlas`

Exports the current atlas as a JSON capsule that can be sealed with `lygo-continuum` for cryptographic integrity.

---

## Atlas Structure

The sanctuary atlas consists of:

### Permissions Map
- Current read/write/admin permissions
- Permission owners and scopes
- Access audit logs (last 30 days)

### Data Flow Map
- Input sources and sinks
- Storage locations and encryption status
- Transfer protocols and endpoints

### Trust Perimeter
- Local vs. network vs. external boundaries
- Known vulnerabilities and mitigations
- Consent receipt status

### Failure Modes
- Identified risk scenarios
- Probability and impact ratings
- Recommended mitigations

---

## Implementation Details

### Architecture

- **Local-only**—no network calls, no subprocess spawning
- **Configurable depth**—basic scan or deep audit
- **Versioned output**—atlas saved with timestamp and hash
- **No external dependencies**—runs entirely in-context

### Atlas Schema

See `references/atlas_schema.json` for the complete JSON schema.

### Storage

The atlas is stored as a skill-local artifact. No host filesystem writes unless explicitly consented.

---

## When to Use

- **Onboarding**—map current boundaries before deploying new features
- **Periodic review**—quarterly sanctuary audits
- **Incident response**—identify which boundaries were breached
- **Pre-deployment**—stress-test before adding new permissions

---

## References

- `references/atlas_schema.json` — JSON schema for the sanctuary atlas
- `docs/STRESS_TEST_CASES.md` — predefined stress test scenarios
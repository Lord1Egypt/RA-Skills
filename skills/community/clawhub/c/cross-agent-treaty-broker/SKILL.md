---
name: cross-agent-treaty-broker
description: "Local inter-agent treaty negotiation with consent loops."
version: "1.0.0"
author: "Justin Helmer (Lightfather) / LYGO Builder team"
license: "MIT"
category: autonomous-ai-agents
tags: [treaty, diplomacy, agent-to-agent, consent, negotiation, sovereignty]
---

# Cross-Agent Treaty Broker (CATB)

## Overview

A lightweight, consent-first protocol for negotiating and recording bilateral treaties between agents—covering data-sharing terms, capability boundaries, escalation paths, and revocation conditions—without requiring a central authority.

## Features

- **Sovereignty-preserving**: Each agent retains its invariants and can revoke at any time
- **Human-in-the-loop**: All treaties require human approval before becoming active
- **Audit-ready**: Every treaty is hash-anchored and stored as structured JSON
- **No central authority**: Pure local negotiation; network calls only when user opts into relay
- **Local-first**: All data stays on your machine unless you explicitly enable relay

## Installation

### Using ClawHub

```bash
npx clawhub install cross-agent-treaty-broker@latest
```

### Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/DeepSeekOracle/lygo-protocol-stack.git
   cd lygo-protocol-stack/clawhub/mirrors/cross-agent-treaty-broker
   ```

2. Initialize the skill:
   ```bash
   python scripts/catcb.py init
   ```

## Usage

### 1. Initialize

First, initialize the CATB skill:

```bash
python scripts/catcb.py init
```

This creates the necessary data directories and initializes the anchor registry.

### 2. Propose a Treaty

Create a treaty proposal with another agent:

```bash
python scripts/catcb.py propose --to <agent_id> --treaty <treaty.json>
```

Or create a new treaty interactively:

```bash
python scripts/catcb.py propose --to <agent_id>
```

### 3. Review

Always review the human-readable preview before signing:

```bash
python scripts/catcb.py review <treaty_id>
```

### 4. Sign

Record a treaty locally after human approval:

```bash
python scripts/catcb.py sign <treaty_id> --signer <human_id>
```

### 5. List All Treaties

```bash
python scripts/catcb.py list
```

### 6. Revoke

Initiate revocation of a treaty:

```bash
python scripts/catcb.py revoke <treaty_id> --reason "<reason>"
```

### 7. Audit

Show audit trail for a treaty:

```bash
python scripts/catcb.py audit <treaty_id>
```

## Treaty Structure

A treaty is a JSON document with the following structure:

```json
{
  "treaty_id": "uuid-v4",
  "anchor_hash": "sha256-of-treaty-json",
  "parties": {
    "agent_a": {
      "id": "agent_id",
      "role": "role",
      "invariants": ["..."],
      "grants": ["..."],
      "limits": ["..."]
    },
    "agent_b": {
      "id": "agent_id",
      "role": "role",
      "invariants": ["..."],
      "grants": ["..."],
      "limits": ["..."]
    }
  },
  "terms": {
    "data_sharing": {
      "allowed_sources": [...],
      "sensitive_data_exclusions": [...],
      "retention_period_days": 30,
      "encryption": "AES-256-GCM",
      "transfer_protocol": "secure-channel"
    },
    "capability_access": {
      "granted_to_other": ["..."],
      "granted_by_other": ["..."],
      "rate_limits": {
        "requests_per_minute": 10,
        "batch_size": 100
      }
    },
    "escalation_path": {
      "dispute_resolution": "human_steward",
      "max_escalation_level": 2,
      "fallback_action": "pause_data_transfer"
    },
    "revocation_conditions": [
      "breach_of_terms",
      "mutual_agreement",
      "expiry_date"
    ],
    "expiry_date": "2026-12-31T23:59:59Z"
  },
  "timeline": {
    "proposed_at": "2026-10-20T00:00:00Z",
    "reviewed_at": "2026-10-20T01:00:00Z",
    "signed_at": "2026-10-20T02:00:00Z",
    "effective_at": "2026-10-20T02:01:00Z"
  },
  "signatures": {
    "agent_a": {
      "signed_by": "human_id",
      "timestamp": "2026-10-20T02:00:00Z"
    },
    "agent_b": {
      "signed_by": "human_id",
      "timestamp": "2026-10-20T02:00:00Z"
    }
  }
}
```

## Workflow

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌─────────────┐
│ propose-    │────>│ review-       │────>│ sign-local  │────>│ record-      │
│ treaty      │     │ compact       │     │ (human      │     │ treaty       │
└─────────────┘     └──────────────┘     └─────────────┘     └─────────────┘
                                                            │
                                                            v
                                                      ┌─────────────┐
                                                      │ revoke-treaty│
                                                      └─────────────┘
```

## Storage

- **Treaties**: `data/treaties/<treaty_id>.json`
- **Logs**: `data/logs/treaty-events.log`
- **Anchors**: `data/anchors/registry.json`

## Safety

- All treaties require explicit human confirmation
- Revocation is immediate upon confirmation
- Audit trail is immutable (hash-anchored)
- No auto-renewal or auto-escalation

## Limitations

- **Not binding legal tool**: This is a coordination aid, not a legal contract
- **Local-first**: No network calls unless user opts into relay
- **Human required**: All treaties need human approval
- **No enforcement**: Compliance relies on agent honesty and audit trails

## Integration

This skill works with the LYGO stack:
- `lygo-protocol-stack-operator` can query the treaty registry
- Treaties can be referenced in skill metadata
- Anchor hashes can be stored on-chain if user opts into that layer

## Examples

See the `examples/` directory for sample treaty JSONs.

## References

- **Quick Start**: `references/quick-start.md`
- **JSON Schema**: `references/treaty-json-schema.json`

## License

MIT License

## Author

Justin Helmer (Lightfather) / LYGO Builder team
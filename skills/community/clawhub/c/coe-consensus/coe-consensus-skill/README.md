# COE Consensus Skill v1.0.0

**Cross-Model Consensus Engine** for Shared World State Formation.

Based on the **COE (Cognition-Oriented Emergence)** Protocol (Wang, 2026).

> **Core Problem:** When multiple agents (humans, AI models, robots) observe the same physical space, how do they reach a verifiable consensus on "what the world is"?

---

## What It Does

| Policy | Use Case | Rule |
|--------|----------|------|
| **Simple Majority** | Small equal-trust groups | >50% of verifications confirm |
| **Weighted Trust** | Heterogeneous agents with different reliability | Sum of (trust_weight * confidence) > threshold |
| **BFT** | High-security with potential malicious agents | >f+1 confirmations out of >=2f+1 total verifications |

## Core Capabilities

1. **Event Collection** — Ingest J (Judge) and V (Verify) events from any Cognitive Unit.
2. **Conflict Resolution** — Detect contradictory assertions on the same subject and resolve via policy.
3. **Termination Handling** — Process T (Terminate) events to invalidate outdated assertions before re-consensus.
4. **Shared World State (SWS)** — Output a tamper-evident consensus record with full provenance.

## Quick Start

```bash
pip install -r requirements.txt
uvicorn skill.api:app --host 0.0.0.0 --port 8000
```

## API Call

```bash
curl -X POST http://localhost:8000/consensus \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "warehouse-001",
    "target": "warehouse-zone-3",
    "policy": "weighted_trust",
    "events": [
      {
        "event_id": "evt-1",
        "primitive": "J",
        "issuer": "robot-A",
        "timestamp": "2026-04-19T10:30:00Z",
        "target": "warehouse-zone-3",
        "assertion": {"subject": "door_01", "predicate": "status", "value": "open"},
        "confidence": 0.95
      },
      {
        "event_id": "evt-2",
        "primitive": "V",
        "issuer": "robot-B",
        "timestamp": "2026-04-19T10:30:05Z",
        "target": "warehouse-zone-3",
        "verify_of": ["evt-1"],
        "verification_result": "confirmed",
        "confidence": 0.9
      },
      {
        "event_id": "evt-3",
        "primitive": "V",
        "issuer": "human-1",
        "timestamp": "2026-04-19T10:30:10Z",
        "target": "warehouse-zone-3",
        "verify_of": ["evt-1"],
        "verification_result": "confirmed",
        "confidence": 1.0
      }
    ],
    "trust_weights": {"robot-A": 0.9, "robot-B": 0.8, "human-1": 1.0},
    "weighted_threshold": 1.5
  }'
```

## Protocol Reproduction

```bash
cd examples
python robot_consensus.py
```

Reproduces COE Protocol Appendix A verification workflow:
- Scenario 1: Simple Majority — 3 robots confirm door=open
- Scenario 2: Weighted Trust — robots + human supervisor confirm door=closed
- Scenario 3: BFT — 4 robots tolerate 1 Byzantine fault
- Scenario 4: Termination + Re-consensus — old state terminated, new state agreed

## Relationship with JEP

- **COE** answers "what the world is" — cognitive consensus, ex-ante / in-situ collaboration.
- **JEP** answers "who is responsible" — accountability tracing, post-hoc audit.
- COE events may be referenced by JEP as evidence. Together they form a complete cognition-accountability dual-loop.

---

Cognitive Emergence Lab  
Email: yuqiang@humanjudgment.org

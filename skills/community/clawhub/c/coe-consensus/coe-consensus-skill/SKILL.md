---
name: coe-consensus
version: 1.0.0
description: COE Consensus Engine — Cross-Model Consensus Skill for Shared World State Formation
author: Cognitive Emergence Lab <yuqiang@humanjudgment.org>
license: MIT
protocol: COE
tags:
  - coe
  - consensus
  - jep
  - swarm
  - multi-agent
  - world-model
  - bft
entrypoint: skill.api:app
host_targets:
  - mcp
  - api
  - python
skills:
  - name: run_consensus
    description: Collect J/V events from heterogeneous agents and produce a verifiable Shared World State via configurable consensus policy
    input_schema:
      type: object
      properties:
        session_id:
          type: string
          description: Unique session identifier
        target:
          type: string
          description: Target world model or scene ID to filter events
        policy:
          type: string
          enum:
            - simple_majority
            - weighted_trust
            - bft
          description: Consensus policy to apply
        events:
          type: array
          description: List of COE events (J, D, T, V primitives)
          items:
            type: object
            properties:
              event_id:
                type: string
              primitive:
                type: string
                enum:
                  - J
                  - D
                  - T
                  - V
              issuer:
                type: string
              timestamp:
                type: string
              target:
                type: string
              assertion:
                type: object
              verify_of:
                type: array
                items:
                  type: string
              verification_result:
                type: string
                enum:
                  - confirmed
                  - rejected
                  - partial
              confidence:
                type: number
              terminate_of:
                type: string
        trust_weights:
          type: object
          description: Issuer-to-weight mapping for weighted_trust policy
        bft_fault_tolerance:
          type: integer
          description: Fault tolerance parameter f for BFT policy
        weighted_threshold:
          type: number
          description: Confirmation threshold for weighted_trust policy
      required:
        - session_id
        - policy
        - events
    output_schema:
      type: object
      properties:
        session_id:
          type: string
        resolved:
          type: boolean
          description: Whether consensus was reached for all active assertions
        policy:
          type: string
        sws:
          type: object
          description: Shared World State record when resolved
          properties:
            sws_id:
              type: string
            target:
              type: string
            timestamp:
              type: string
            assertions:
              type: array
              items:
                type: object
            previous_sws_id:
              type: string
        conflicts:
          type: array
          description: Unresolved conflicts requiring additional evidence or verifications
          items:
            type: object
        message:
          type: string
        events_processed:
          type: integer
        events_by_issuer:
          type: object
---

# COE Consensus Skill

**Cross-Model Consensus Engine**

Algorithm implementation based on the **COE (Cognition-Oriented Emergence)** Protocol (Wang, 2026).

## Core Problem

When multiple agents (humans, AI models, robots) observe the same physical space, how do they reach a verifiable consensus on "what the world is"?

## Consensus Policies

| Policy | Use Case | Rule |
|--------|----------|------|
| **Simple Majority** | Small equal-trust groups | Confirmations exceed 50% of all verifications received |
| **Weighted Trust** | Heterogeneous agents with different reliability | Sum of (trust_weight * confidence) exceeds threshold |
| **BFT** | High-security with potential malicious agents | More than f+1 confirmations out of at least 2f+1 total verifications |

## Shared World State (SWS)

Whenever consensus is reached, the engine produces an SWS record containing:
- `subject` / `predicate` / `value` — the agreed-upon fact
- `confidence` — aggregated confidence score
- `based_on` — event IDs of the underlying J/V events
- `consensus_policy` — policy used to reach agreement
- `confirmations` — number of confirming verifications

## Usage Example

### Request

```json
{
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
    }
  ],
  "trust_weights": {"robot-A": 0.9, "robot-B": 0.8},
  "weighted_threshold": 1.5
}
```

### Response

```json
{
  "session_id": "warehouse-001",
  "resolved": true,
  "policy": "weighted_trust",
  "sws": {
    "sws_id": "...",
    "target": "warehouse-zone-3",
    "timestamp": "2026-04-19T10:30:05Z",
    "assertions": [
      {
        "subject": "door_01",
        "predicate": "status",
        "value": "open",
        "confidence": 1.0,
        "based_on": ["evt-1"],
        "consensus_policy": "weighted_trust",
        "confirmations": 1
      }
    ]
  },
  "conflicts": [],
  "message": "Consensus complete. 1 assertions resolved, 0 conflicts remain.",
  "events_processed": 2,
  "events_by_issuer": {"robot-A": 1, "robot-B": 1}
}
```

## Relationship with JEP

- **COE** answers "what the world is" — cognitive consensus, ex-ante / in-situ collaboration.
- **JEP** answers "who is responsible" — accountability tracing, post-hoc audit.
- COE events may be referenced by JEP as evidence. Together they form a complete cognition-accountability dual-loop.

---

Cognitive Emergence Lab  
yuqiang@humanjudgment.org

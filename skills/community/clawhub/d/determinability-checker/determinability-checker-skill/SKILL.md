---
name: determinability-checker
version: 1.0.2
description: Causal Sufficiency Determinability Checker — Meta-Skill Gatekeeper based on JEP Paper CheckDeterminability Algorithm
author: Cognitive Emergence Lab <yuqiang@humanjudgment.org>
license: MIT
protocol: COE
tags:
  - jep
  - causality
  - audit
  - determinability
  - gatekeeper
  - meta-skill
entrypoint: skill.api:app
host_targets:
  - mcp
  - api
  - python
skills:
  - name: check_determinability
    description: Determine whether a target fact is zero-error determinable from current evidence; return DETERMINED/NOT_DETERMINED with missing-evidence guidance
    input_schema:
      type: object
      properties:
        session_id:
          type: string
          description: Unique session identifier
        question:
          type: string
          description: The judgment question to evaluate
        configs:
          type: array
          description: Finite configuration family; each item must contain config_id
          items:
            type: object
        omega_field:
          type: string
          description: Observation value field name; corresponds to observation function Omega in the paper
        target_field:
          type: string
          description: Target value field name; corresponds to target function D in the paper
        evidence_fields:
          type: array
          items:
            type: string
          description: Optional constrained evidence field list for gap analysis
      required:
        - session_id
        - question
        - configs
        - omega_field
        - target_field
    output_schema:
      type: object
      properties:
        session_id:
          type: string
        question:
          type: string
        determinability:
          type: string
          enum:
            - DETERMINED
            - NOT_DETERMINED
        can_proceed:
          type: boolean
          description: Whether the Agent should execute the target action immediately
        decision_table:
          type: object
          description: Observation-to-target mapping returned when DETERMINED
        counterexample:
          type: object
          description: Indistinguishable counterexample pair returned when NOT_DETERMINED
        missing_evidence:
          type: array
          items:
            type: string
          description: Evidence fields needed to resolve non-determinability
        next_skill_suggestion:
          type: string
          description: Recommended next skill or evidence type to call when NOT_DETERMINED
        message:
          type: string
---

# Determinability Checker

**Causal Sufficiency Determinability Checker**

Algorithm implementation based on the paper *Target Determinability under Partial Causal Observation* (Wang, 2026).

## Core Question

Before an Agent calls other skills, it asks itself:

> "Based on current evidence, am I sufficient to make this judgment?"

## Determinability Results

| Result | Meaning | Agent Action |
|--------|---------|------------|
| **DETERMINED** | Evidence is sufficient; target is zero-error determinable | Execute immediately; no wasted tokens |
| **NOT_DETERMINED** | Evidence is insufficient; indistinguishable counterexample exists | Return missing-evidence list; guide next skill to call |

## Theoretical Foundation

- **Theorem 10.1** (Finite Model Checking): The algorithm returns Determined if and only if the target is zero-error determinable; returns NotDetermined with a counterexample pair certificate.
- **Theorem 8.2** (Constrained Evidence Coverage): An evidence subset covers all conflict edges if and only if the target becomes determinable from the joint observation.
- **Quotient Factorization** (Lemma 7.1): D is determinable from Omega if and only if D is constant on every observation equivalence class, if and only if D = g composed with Omega.

## Usage Example

### Request

```json
{
  "session_id": "audit-001",
  "question": "Does the final output have a valid verification event?",
  "configs": [
    {"config_id": "C1", "tool": "code", "has_verif": true, "verif_hash": "valid", "output": "correct", "target": 1},
    {"config_id": "C2", "tool": "code", "has_verif": false, "verif_hash": "none", "output": "correct", "target": 0}
  ],
  "omega_field": "output",
  "target_field": "target",
  "evidence_fields": ["tool", "has_verif", "verif_hash"]
}
```

### Response

```json
{
  "session_id": "audit-001",
  "question": "Does the final output have a valid verification event?",
  "determinability": "NOT_DETERMINED",
  "can_proceed": false,
  "counterexample": {
    "config1": "C1",
    "config2": "C2",
    "observation": "correct",
    "target1": 1,
    "target2": 0
  },
  "missing_evidence": ["tool", "has_verif", "verif_hash"],
  "next_skill_suggestion": "Supplement the following evidence items: tool, has_verif, verif_hash",
  "message": "Non-determinability proven: configs C1 and C2 share observation correct but differ on target (1 vs 0)."
}
```

---

Cognitive Emergence Lab  
yuqiang@humanjudgment.org

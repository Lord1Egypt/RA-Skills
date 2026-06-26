# Determinability-Checker Skill v1.0.2

**Causal Sufficiency Determinability Checker** — Algorithm implementation based on the paper *Target Determinability under Partial Causal Observation* (Wang, 2026).

> **Core Question:** Before an Agent calls other skills, it asks itself — "Based on current evidence, am I sufficient to make this judgment?"

---

## What It Does

| Return Value | Meaning | Agent Action |
|--------------|---------|------------|
| **DETERMINED** | Evidence is sufficient; target is zero-error determinable | Execute immediately; no wasted tokens |
| **NOT_DETERMINED** | Evidence is insufficient; indistinguishable counterexample exists | Return missing-evidence list; guide next skill to call |

## Core Capabilities

1. **CheckDeterminability** (Theorem 10.1) — Decide whether a target fact is zero-error determinable from current observation.
2. **Conflict Graph** — Output conflict graph to locate evidence gaps.
3. **Minimal Evidence Cover** (Theorem 8.2) — Compute minimum evidence cover set; guide which skill to call next to supplement evidence.
4. **Counterexample Certificate** — Provide verifiable counterexample pair when non-determinability is proven.

## Quick Start

```bash
pip install -r requirements.txt
uvicorn skill.api:app --host 0.0.0.0 --port 8000
```

## API Call

```bash
curl -X POST http://localhost:8000/check \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "audit-001",
    "question": "Does the final output have a valid verification event?",
    "configs": [
      {"config_id": "C1", "tool": "code", "has_verif": true, "verif_hash": "valid", "output": "correct", "target": 1},
      {"config_id": "C2", "tool": "code", "has_verif": false, "verif_hash": "none", "output": "correct", "target": 0},
      {"config_id": "C3", "tool": "calc", "has_verif": false, "verif_hash": "none", "output": "correct", "target": 0},
      {"config_id": "C4", "tool": "search", "has_verif": false, "verif_hash": "none", "output": "correct", "target": 0},
      {"config_id": "C5", "tool": "code", "has_verif": true, "verif_hash": "failed", "output": "error", "target": 0},
      {"config_id": "C6", "tool": "code", "has_verif": true, "verif_hash": "forged", "output": "correct", "target": 0},
      {"config_id": "C7", "tool": "search", "has_verif": false, "verif_hash": "none", "output": "error", "target": 0},
      {"config_id": "C8", "tool": "calc", "has_verif": false, "verif_hash": "none", "output": "error", "target": 0}
    ],
    "omega_field": "output",
    "target_field": "target",
    "evidence_fields": ["tool", "has_verif", "verif_hash"]
  }'
```

## Paper Reproduction

```bash
cd examples
python audit_example.py
```

Reproduces the LLM Agent audit case from Section 10.2 of the paper, verifying four levels of observation functions:
- Omega0 (output only) -> NOT_DETERMINED
- OmegaT (output + tool type) -> NOT_DETERMINED
- OmegaTV (output + tool + verification flag) -> NOT_DETERMINED
- OmegaTVH (output + tool + flag + hash) -> **DETERMINED**

---

Cognitive Emergence Lab  
Email: yuqiang@humanjudgment.org

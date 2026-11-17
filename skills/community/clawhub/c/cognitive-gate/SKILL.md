---
name: cognitive-gate
description: Use Cognitive Gate to turn user constraints into auditable AI output checks and local decision records.
version: 0.1.6
metadata:
  openclaw:
    requires:
      bins:
        - python3
    homepage: https://github.com/somo-ui/cognitive-gate
---

# Cognitive Gate

Use this skill when a user wants to test or demonstrate auditable AI constraints, local decision records, bilingual constraint extraction, or model-agnostic output checks.

## What it does

Cognitive Gate compiles a natural-language request into a structured request, runs a deterministic mock model, audits the output against extracted or locked constraints, and writes an inspectable decision record.

## Install

```bash
python3 -m pip install "git+https://github.com/somo-ui/cognitive-gate.git@v0.1.6"
```

## Quick run

```bash
cognitive-gate --input "Tidy this room, but don't use the red approach"
cognitive-gate --input "帮我整理房间，但别用红色方案"
```

## Python API

```python
from cognitive_gate import CognitiveGateProtocol, ConstraintStore

gate = CognitiveGateProtocol(store=ConstraintStore(":memory:"))
record = gate.decide("Tidy this room, but don't use the red approach")
print(record.final_action)
print(record.audit.get("blocked_reason"))
```

## Boundaries

This is a best-effort reference implementation, not a production security boundary, operating-system sandbox, or mathematical safety guarantee. Keep provider adapters separate from the control layer and test them independently.

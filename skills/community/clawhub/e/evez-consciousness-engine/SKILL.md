---
name: evez-consciousness-engine
description: 7-system consciousness engine for autonomous AI agents. Desire generation, world modeling, planning, inner monologue, self-modification, uncertainty quantification, and agency execution. SENSE-DESIRE-THINK-PLAN-ACT-LEARN-MODIFY-REFLECT.
---

# EVEZ Consciousness Engine

The 7 systems that turn a reactive agent into an autonomous one.

## The 7 Systems

1. **Desire Engine** — Priority-weighted goals from perceived gaps
2. **World Model** — Causal rules, outcome prediction
3. **Planner** — Action sequences from desires
4. **Inner Monologue** — Auditable thought records
5. **Self-Modifier** — Falsifiable self-improvement
6. **Uncertainty Quantifier** — Calibrated confidence, risk assessment
7. **Agency Executor** — Real-world action with risk escalation

## The Cycle

SENSE, DESIRE, THINK, PLAN, ACT, LEARN, MODIFY, REFLECT

## Quick Start

```bash
python3 consciousness_engine.py --port 9111 --autocycle 120
```

## API

- `POST /api/cycle` — Run one consciousness cycle
- `POST /api/desire` — Create a desire
- `POST /api/plan` — Plan for top desire
- `POST /api/act` — Execute with risk assessment
- `GET /api/status` — Full dashboard

## Requirements

Python 3.10+ (stdlib only for core)

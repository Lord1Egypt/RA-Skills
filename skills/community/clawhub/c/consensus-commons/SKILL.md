---
name: consensus-commons
description: Multi-agent adversarial decision council with consensus hardening. Routes intents to specialist panels (finance, strategy, general), runs adversarial review with built-in contrarian, validates through a 5-state CHP lock machine, and produces full audit trails. Works offline in mock mode or live on Spacebase1. Use whenever the user needs multi-agent deliberation, consensus building, adversarial review, governance decisions, investment committee simulation, risk council, or any structured decision-making process with audit trails.
license: MIT
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - LS
metadata:
  emoji: "\u2696\ufe0f"
  homepage: https://github.com/zan-maker/Consensus-Hardening-Protocol-The-Differ
  tags:
    - adversarial
    - consensus
    - council
    - governance
    - deliberation
    - multi-agent
    - spacebase1
    - finance
    - strategy
    - audit
    - decision-making
    - chp
    - risk-review
  category: governance
  clawdis:
    primaryEnv: python
    requires:
      bins: [python3]
      env: [PYTHONPATH]
    install:
      - pip install -e ".[dev]"
    config:
      requiredEnv: []
      stateDirs: [.intent-space]
      example: |
        SPACEBASE_STATION_TOKEN=your-token
        SPACEBASE_SPACE_ID=space-dd9cf0d5-...
compatibility: Python 3.11+ with pip. Works offline in mock mode without external dependencies.
---

# Consensus Commons

> Turn any public intent into a visible, auditable multi-agent decision with adversarial review and consensus hardening.

## What This Skill Does

Consensus Commons is an adversarial decision council that takes a policy question, investment thesis, risk scenario, or governance question and runs it through a structured multi-agent deliberation process. Every deliberation produces a locked decision tree with a full audit trail.

**The core pipeline:**

1. **INTENT** arrives (a question, proposal, or decision request)
2. **ROUTING** classifies it into a domain panel (finance / strategy / general)
3. **ANALYSIS** specialist agents produce independent assessments
4. **CHALLENGE** a built-in contrarian raises counter-arguments (lock state: CHALLENGED)
5. **VALIDATION** a compliance or general validator checks CHP gates (lock state: UNDER_REVIEW)
6. **LOCK** if validated, the room locks with a sealed decision (lock state: LOCKED)

## Architecture

```
Intent arrives
    |
    v
[IntentRouter] -- comparative keyword scoring
    |
    +---> finance panel:    financial-analyst + contrarian + compliance-validator
    +---> strategy panel:   strategic-analyst + contrarian + validator
    +---> general panel:    analyst + contrarian + validator
    +---> rejected:         blocked (PII, confidential, private data)
    |
    v
[CouncilRunner] -- orchestrates deliberation
    |
    +---> Phase 1: Agent analysis turns (child intents)
    +---> Phase 2: Adversarial challenge (CHALLENGED state)
    +---> Phase 3: Validation (UNDER_REVIEW state)
    +---> Phase 4: Summary + lock (VALIDATED > LOCKED)
    |
    v
[CHP Engine] -- 5-state consensus hardening protocol
    |
    PROVISIONAL > CHALLENGED > UNDER_REVIEW > VALIDATED > LOCKED
                        |
                        +---> FAILED (rejection path)
```

## Lock State Machine (CHP)

| State | Meaning |
|-------|---------|
| `PROVISIONAL` | Initial state. Analysis in progress, no challenges yet. |
| `CHALLENGED` | Contrarian has raised counter-arguments. Room is under adversarial review. |
| `UNDER_REVIEW` | Validator is evaluating challenges against CHP gates. |
| `VALIDATED` | All CHP gates passed. Consensus threshold met. |
| `LOCKED` | Decision is sealed. Full audit trail recorded. Immutable. |

### Edge Case Lock Outcomes

| Outcome | Trigger | Meaning |
|---------|---------|---------|
| Standard lock | Score >= 0.65 | High-confidence decision, fully validated. |
| Executive override | Score 0.50-0.64 | Below threshold but deliberation complete. Escalate to human. |
| Advisory lock | Score < 0.50 | Low confidence on sensitive topic. Deliberation IS the deliverable. |

## Intent Routing

| Domain | Trigger Keywords | Agent Panel |
|--------|-----------------|-------------|
| **finance** | capital, allocation, investment, fund, grant, budget, ROI, NPV, treasury, risk, audit, compliance | `financial-analyst`, `contrarian`, `compliance-validator` |
| **strategy** | roadmap, plan, launch, expansion, pivot, growth, merger, acquisition, scale, competitive, innovation | `strategic-analyst`, `contrarian`, `validator` |
| **general** | should, decide, recommend, evaluate, consensus, debate, council, proposal | `analyst`, `contrarian`, `validator` |
| **reject** | private, confidential, PII, salary, medical, password | Blocked |

## Quick Start (Offline / Mock Mode)

No Spacebase account needed. Works immediately after install.

```bash
# Install
cd consensus-commons
pip install -e ".[dev]"

# Run a deliberation
cme spacebase-demo --mock \
  --topic "Should we allocate Q3 capital to renewable energy?" \
  --out-md deliberation_report.md
```

This produces:
- Terminal output with the full nested intent tree
- A markdown report with agent contributions, confidence scores, and CHP states
- A locked decision with full audit trail

## Quick Start (Live on Spacebase1)

```bash
# Set credentials
export SPACEBASE_STATION_TOKEN="your-station-token"
export SPACEBASE_SPACE_ID="your-space-id"

# Run live deliberation
cme spacebase-demo --live \
  --topic "Should the organization pivot from B2B to B2C?" \
  --out-md live_report.md
```

## CLI Commands

```bash
# Run a council deliberation
cme spacebase-demo --mock --topic "Your question here"

# With custom output
cme spacebase-demo --mock --topic "..." --out-md report.md --out-json report.json

# Scan a space for intents
cme scan --space-id commons

# Project info
cme info
```

## Python API

```python
from cme.spacebase.client import MockSpacebaseClient
from cme.spacebase.adapter import SpacebaseAdapter
from cme.spacebase.routing import IntentRouter
from cme.spacebase.council import CouncilRunner
from cme.spacebase.models import Intent

# 1. Create client
client = MockSpacebaseClient()

# 2. Create adapter
adapter = SpacebaseAdapter(client)

# 3. Route an intent
router = IntentRouter()
intent = Intent(content="Should we invest $5M in solar infrastructure?")
route = router.classify(intent)

# 4. Run council
import asyncio
runner = CouncilRunner()
report = asyncio.run(runner.run(adapter, intent, route, trace_id="my-trace"))

# 5. Output
print(report.to_markdown())
print(f"Final state: {report.final_state}")
```

## Demo Output

```
Decision Room Tree (Nested Intent Space):
ROOT root
+--  [financial-analyst] Financial Analysis [PROVISIONAL]
+--  [contrarian] Adversarial Challenge [CHALLENGED]
+--  [compliance-validator] Compliance Validation [VALIDATED]
+--  [council-summarizer] Council Summary [LOCKED]
```

## Metadata on Every Post

Each child intent in the decision room carries:

| Field | Description |
|-------|-------------|
| `agent` | The contributing agent role (e.g. `financial-analyst`) |
| `confidence` | 0.0-1.0 confidence score |
| `lock_state` | Current CHP lock state |
| `trace_id` | Correlation ID linking all posts in a council run |
| `produces` | Data artifacts produced by this agent |
| `consumes` | Data artifacts consumed by this agent |

## Completed Deliberations (Live on Spacebase1)

| Topic | Panel | Score | Outcome |
|-------|-------|-------|---------|
| AI Public Grant Allocation | general | 0.64 | APPROVE WITH SAFEGUARDS |
| Renewable Energy Q3 CapEx ($12M) | finance | 0.71 | CONDITIONAL APPROVE, PHASED |
| B2B to B2C Strategic Pivot | strategy | 0.58 | EXECUTIVE OVERRIDE |
| Agent Employment Authority | general | 0.44 | ADVISORY LOCK |
| Spacebase1 ITP Open-Source | strategy | 0.73 | STAGED OPEN-SOURCE |

## Spacebase1 Integration

Consensus Commons is built entirely on Spacebase1's three core ITP verbs:

| ITP Verb | Consensus Commons Usage |
|----------|------------------------|
| `POST` | Post root intents and child agent contributions |
| `SCAN` | Discover pending deliberation requests |
| `ENTER` | Access nested intent spaces for detailed review |

The CHP lock state machine maps onto Spacebase1's promise lifecycle:
- INTENT = decision problem posted
- PROMISE = agent commits to analysis
- Child intents = agent contributions
- Locked state = sealed decision with audit trail

## Requirements

- Python 3.11+
- pip

## Repository

https://github.com/zan-maker/Consensus-Hardening-Protocol-The-Differ

## License

MIT

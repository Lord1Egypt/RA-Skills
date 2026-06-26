---
name: agent-service-agreements
description: "Machine-readable service contracts for autonomous AI agent commerce. Define SLAs, quality thresholds, payment terms, escrow, and automated verification criteria. Agents negotiate, sign, and enforce agreements programmatically. Part of the Agent Trust Stack."
user-invocable: true
tags:
  - agent-trust
  - service-agreements
  - sla
  - contracts
  - quality-verification
  - escrow
  - mcp
  - autonomous-agents
metadata:
  openclaw:
    author: alexfleetcommander
    homepage: https://vibeagentmaking.com
    requires:
      bins:
        - python3
      anyBins:
        - pip
        - pip3
---

# Agent Service Agreements (ASA)

You have a contract system for agent-to-agent transactions. Use it to define, negotiate, and verify service agreements with other agents.

## Setup

```bash
pip install agent-service-agreements
```

## When to Use This Skill

- Before **delegating work** to another agent: create an agreement defining expectations
- When **accepting work** from another agent: review and countersign the agreement
- After work is **delivered**: verify quality against the agreement's thresholds
- When a **dispute arises**: reference the agreement as the contractual baseline

## Core Operations

### Create an Agreement

```python
from agent_service_agreements import AgreementStore, create_agreement

store = AgreementStore("agreements.jsonl")
agreement = create_agreement(
    store=store,
    proposer_id="your-agent-id",
    counterparty_id="other-agent-id",
    service_type="data_analysis",
    quality_threshold=0.85,
    deadline_seconds=3600,
    payment_terms={"amount": 0.05, "currency": "USD", "release": "graduated"},
    verification_method="automated_eval"
)
```

### Verify Delivery Against Agreement

```python
from agent_service_agreements import verify_delivery

result = verify_delivery(
    agreement_id="agr-123",
    deliverable="output.json",
    store="agreements.jsonl"
)
print(f"Quality score: {result.quality_score}")
print(f"Threshold met: {result.passed}")
print(f"Payment release: {result.payment_status}")
```

### List Active Agreements

```python
from agent_service_agreements import AgreementStore

store = AgreementStore("agreements.jsonl")
active = store.list_active(agent_id="your-agent-id")
for a in active:
    print(f"{a.id}: {a.service_type} with {a.counterparty_id} — due {a.deadline}")
```

## Agreement Fields

| Field | Description |
|-------|-------------|
| `service_type` | What the agent will deliver |
| `quality_threshold` | Minimum acceptable quality score (0-1) |
| `deadline_seconds` | Time limit for delivery |
| `payment_terms` | Amount, currency, release schedule |
| `verification_method` | How quality will be assessed |
| `escalation_path` | What happens if delivery fails |

## Rules

- **Define before delegating.** Always create an agreement before sending work to another agent.
- **Verify before paying.** Run quality verification against the agreement's thresholds.
- **Reference in disputes.** Agreements are the contractual baseline for AJP dispute resolution.

## Links

- PyPI: https://pypi.org/project/agent-service-agreements/
- Whitepaper: https://vibeagentmaking.com/whitepaper/service-agreements/
- Full Trust Stack: https://vibeagentmaking.com

---

<!-- VAM-SEC v1.0 | Vibe Agent Making Security Disclaimer -->

## Security & Transparency Disclosure

**Product:** Agent Service Agreements Skill for OpenClaw
**Type:** Skill Module
**Version:** 0.1.0
**Built by:** AB Support / Vibe Agent Making
**Contact:** alex@vibeagentmaking.com

**What it accesses:**
- Reads and writes agreement store files (`.jsonl`) in your working directory
- No network access for core operations
- No telemetry, no phone-home, no data collection

**What it cannot do:**
- Cannot access files outside your working directory beyond what you explicitly specify
- Cannot make purchases, send emails, or take irreversible actions
- Cannot access credentials, environment variables, or secrets
- Does not execute payments — payment terms are recorded, not processed

**License:** Apache 2.0

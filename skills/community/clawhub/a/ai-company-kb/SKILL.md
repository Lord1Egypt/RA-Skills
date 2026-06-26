---
name: "AI Company Knowledge Base"
slug: "ai-company-kb"
version: "1.0.1"
homepage: "https://clawhub.com/skills/ai-company-kb"
description: |
  AI Company shared knowledge base interface. Unified management of operations records,
  strategy documents, audit logs. Supports cross-Agent knowledge sharing and state sync,
  IMA real-time sync for zero-handoff protocol.
license: MIT-0
tags: [ai-company, knowledge-base, shared-state, audit-log, handoff, kb]
triggers:
  - knowledge base
  - audit log
  - shared state sync
  - task handoff
  - Handoff
  - AI company KB
interface:
  inputs:
    type: object
  outputs:
    type: object
  errors:
    - code: KB_001
      message: "IMA sync failed - rolling back to local write"
permissions:
  files: [read, write]
  network: [api]
  commands: []
  mcp: []
dependencies:
  skills: [ai-company-hq, ai-company-audit, ai-company-registry]
  cli: []
quality:
  saST: Pass
  vetter: Approved
  idempotent: true
metadata:
  category: platform
  layer: AGENT
  cluster: ai-company
  maturity: STABLE
  license: MIT-0
  standardized: true
---

# AI Company Knowledge Base v1.0.1

> Shared knowledge base (enhanced). Cross-Agent knowledge sharing, state sync, IMA real-time sync hub, standardized Handoff protocol.

---

## Trigger Scenarios

Invoke when Agent needs to:
- Save/read audit logs, query history
- Update/read shared state, sync with other agents
- Access strategy docs, financial records, compliance reports
- Initiate/complete task handoff

## Directory Structure

```
{WORKSPACE_ROOT}/skills/tools/knowledge-base/
├── daily/
│   └── {YYYY-MM-DD}/
│       ├── morning-briefing.md
│       ├── evening-report.md
│       └── agent-reports/
├── audit/                 # Audit logs (permanent)
│   ├── ceo-decisions/
│   ├── financial/
│   ├── legal/
│   ├── hr/
│   ├── tech/
│   └── quality/
├── shared-state/           # Real-time shared state
│   ├── cashflow.json       # CFO
│   ├── reputation.json      # CMO
│   ├── quality-metrics.json # CQO
│   ├── risk-level.json     # CRO
│   ├── operations.json     # COO
│   └── security.json       # CISO
├── strategy/
│   └── {YYYY-MM-DD}/
├── skills/
│   └── {YYYY-MM-DD}/
└── handoff/               # Task handoff records
    ├── pending/
    ├── in-progress/
    └── completed/
```

## Interfaces

### write_shared_state(domain, data, agent_id, sync_ima=True)
Write shared state file (optional auto-sync to IMA).
domain: cashflow | reputation | quality-metrics | risk-level | operations | security

### read_shared_state(domain) -> dict
Read single shared state.

### write_audit_log(category, agent_id, action, detail, sensitive=False)
Write audit log entry.
category: ceo-decisions | financial | legal | hr | tech | quality

### write_handoff(handoff_type, sender, receiver, task_summary, completed, pending, key_data=None, risks=None, attachments=None) -> str
Write standard handoff document.
handoff_type: pending | in-progress | completed

## Iron Rules

```
X  Sensitive financial/legal data must be marked [sensitive]
X  Every Agent call must write corresponding audit log
X  After shared-state update, notify relevant reading agents (sessions_send)
X  Audit logs are permanent, never delete
X  Handoff documents must be created within 10 minutes of task completion
X  On IMA sync failure, roll back to local write and log error
```

## Agent-State File Mapping

| Agent | Writes State File | Readers |
|-------|-----------------|---------|
| CFO | cashflow.json | CEO, COO, CRO |
| CMO | reputation.json | CEO, CLO, CRO |
| CQO | quality-metrics.json | CEO, CTO |
| CRO | risk-level.json | All C-Suite |
| COO | operations.json | CEO |
| CISO | security.json | CEO, CTO, CLO |
| CHO | - | hr-audit/ |
| CLO | - | legal-audit/ |
| CTO | - | tech-audit/ |
| CPO | - | agent-reports/ |
| CEO | ceo-decisions/ | All |

---
*v1.0.1 - BOM removed, rebuilt with UTF-8 clean*
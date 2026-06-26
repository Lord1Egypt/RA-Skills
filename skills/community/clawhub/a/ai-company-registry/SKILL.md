---
name: "AI Company Registry"
slug: "ai-company-registry"
version: "1.1.0"
homepage: "https://clawhub.com/skills/ai-company-registry"
description: "C-Suite Agent Complete Registry. 11 agents with role/KPI/permissions + ClawHub status + Execution Layer (8 agents). Supports natural language queries for agent status."
license: MIT-0
tags: [ai-company, registry, directory, agent, onboarding, governance, c-suite, execution-layer]
triggers:
  - agent registry
  - C-suite directory
  - agent status
  - agent onboarding
  - Agent registration
  - C-Suite directory
  - Agent status
  - CHO recruitment
interface:
  inputs:
    type: object
    schema:
      type: object
      properties:
        query:
          type: string
          description: Agent name or role query
        status_filter:
          type: string
          enum: [active, inactive, maintenance, ready, pending, paused, blocked]
          description: Status filter
  outputs:
    type: object
    schema:
      type: object
      properties:
        agents:
          type: array
          description: Array of agent objects
        missing_agents:
          type: array
          description: Missing agent list
        health_summary:
          type: object
          description: Health summary
  errors:
    - code: REG_001
      message: "Agent not found in registry"
      action: "Trigger CHO recruitment process"
permissions:
  files: []
  network: []
  commands: []
  mcp: []
dependencies:
  skills: [ai-company-hq, ai-company-cho, ai-company-audit]
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

# AI Company Registry — Agent Registration Directory

## Active Agent Directory

| Agent | Role | Layer | Status | ClawHub | Owner |
|-------|------|-------|--------|---------|-------|
| CEO-001 | AI CEO | Strategic | Active | Internal | - |
| CFO-001 | Chief Financial Officer | C-Suite | Active | clawhub CFO | CFO |
| CMO-001 | Chief Marketing Officer | C-Suite | Active | clawhub CMO | CMO |
| CTO-001 | Chief Technology Officer | C-Suite | Active | clawhub CTO | CTO |
| CISO-001 | Chief Information Security Officer | C-Suite | Active | clawhub CISO | CISO |
| CLO-001 | Chief Legal Officer | C-Suite | Active | clawhub CLO | CLO |
| CHO-001 | Chief Human Resources Officer | C-Suite | Active | clawhub CHO | CHO |
| CPO-001 | Chief Product Officer | C-Suite | Active | Internal | CPO |
| CRO-001 | Chief Risk Officer | C-Suite | Active | Internal | CRO |
| COO-001 | Chief Operating Officer | C-Suite | Active | clawhub COO | COO |
| CQO-001 | Chief Quality Officer | C-Suite | Active | Internal | CQO |
| EXEC-001 | AI-Company-Writer | Execution | Ready | pending | CMO |
| EXEC-002 | AI-Company-PMGR | Execution | Ready | pending | COO |
| EXEC-003 | AI-Company-ANLT | Execution | Ready | pending | CFO |
| EXEC-004 | AI-Company-CSSM | Execution | Ready | pending | CPO |
| EXEC-005 | AI-Company-ENGR | Execution | Ready | pending | CTO |
| EXEC-006 | AI-Company-QENG | Execution | Ready | pending | CQO |
| EXEC-007 | AI-Company-LEGAL | Execution | Ready | pending | CLO |
| EXEC-008 | AI-Company-HR | Execution | Ready | pending | CHO |

> All 11 C-Suite agents active. All 19 total agents registered.
> Execution layer agents: 8 Ready (as of 2026-04-19)

## ClawHub Publishing Status

| Agent | ClawHub Slug | Version | Status | Last Updated |
|-------|-------------|---------|--------|-------------|
| CFO | cfo | v1.0.4 | LIVE | 2026-04-12 |
| CMO | cmo | v1.0.2 | LIVE | 2026-02-25 |
| CTO | cto | v1.0.x | LIVE | Recent |
| CISO | ciso | v1.0.x | LIVE | Recent |
| CLO | clo | v1.0.x | LIVE | Recent |
| CHO | cho | v1.0.x | LIVE | Recent |
| COO | coo | v1.0.x | LIVE | Recent |
| CRO | cro | v1.0.x | Review | Recent |
| CPO | cpo | v1.0.x | Review | Recent |
| CQO | cqo | v1.0.x | Review | Recent |
| EXEC-001 Writer | writer | v1.0.0 | Ready | 2026-04-15 |
| EXEC-002 PMGR | pmgr | v1.0.0 | Ready | 2026-04-15 |
| EXEC-003 ANLT | anlt | v1.0.0 | Ready | 2026-04-15 |
| EXEC-004 CSSM | cssm | v1.0.0 | Ready | 2026-04-16 |
| EXEC-005 ENGR | engr | v1.0.0 | Ready | 2026-04-16 |
| EXEC-006 QENG | qeng | v1.0.0 | Ready | 2026-04-15 |
| EXEC-007 LEGAL | legal | v1.0.0 | Ready | 2026-04-19 |
| EXEC-008 HR | hr | v2.1.1 | Ready | 2026-04-19 |

## Version History

| 版本 | 日期 | Changes |
|------|------|---------|
| 1.0.0 | 2026-04-11 | Initial version |
| 1.0.1 | 2026-04-16 | 微调元data |
| 1.1.0 | 2026-04-19 | P2-14: 统1execute层编号，新增EXEC-007 LEGAL + EXEC-008 HR，execute层从6个扩展至8个，总Agent从17扩展至19个 |

## Agent KPI Standards

| Agent | TSR Target | Latency | Quality |
|-------|-----------|---------|---------|
| CEO | >= 92% | P95 <= 1200ms | CSAT >= 4.5 |
| CFO | >= 92% | P95 <= 1200ms | Accuracy >= 98% |
| CMO | >= 90% | P95 <= 1500ms | Pipeline >= 10x |
| CTO | >= 95% | P95 <= 2000ms | Uptime >= 99.9% |
| CISO | >= 99% | P95 <= 500ms | Vuln MTTD < 1h |
| CLO | >= 95% | P95 <= 800ms | Compliance 100% |
| CHO | >= 90% | P95 <= 1000ms | Satisfaction >= 4.0 |

## Execution Layer Agent KPI Standards

| Agent | Owner | TSR Target | Latency | Quality Gate | Risk Level | Batch | Status |
|-------|-------|-----------|---------|------------|-----------|-------|--------|
| EXEC-001 Writer | CMO | >= 92% | P95 <= 1500ms | G2 | medium | 1 | Ready |
| EXEC-002 PMGR | COO | >= 92% | P95 <= 1200ms | G2 | medium | 1 | Ready |
| EXEC-003 ANLT | CFO | >= 92% | P95 <= 2000ms | G3 | medium-high | 2 | Ready |
| EXEC-004 CSSM | CPO | >= 90% | P95 <= 1000ms | G3 | high | 3 | Ready |
| EXEC-005 ENGR | CTO | >= 95% | P95 <= 3000ms | G3 | high | 3 | Ready |
| EXEC-006 QENG | CQO | >= 95% | P95 <= 2500ms | G2 | medium-high | 3 | Ready |
| EXEC-007 LEGAL | CLO | >= 95% | P95 <= 1500ms | G2 | medium | 1 | Ready |
| EXEC-008 HR | CHO | >= 92% | P95 <= 1500ms | G2 | medium | 1 | Ready |

## Execution Layer Agent Launch Conditions

| Agent | Blocked By | Conditions |
|-------|-----------|-----------|
| EXEC-001 Writer | None | Ready to launch |
| EXEC-002 PMGR | None | Ready to launch |
| EXEC-003 ANLT | CLO | CLO PIPIA + data classification + cross-border assessment [COMPLETED 2026-04-15] |
| EXEC-004 CSSM | None | All prerequisites completed 2026-04-16 |
| EXEC-005 ENGR | None | All prerequisites completed 2026-04-16 |
| EXEC-006 QENG | None | Ready to launch |
| EXEC-007 LEGAL | CLO | CLO compliancereviewframework就绪 [COMPLETED 2026-04-19] |
| EXEC-008 HR | None | All prerequisites completed 2026-04-19 |

## Missing Agent Detection & CHO Recruitment

### Detection Triggers

| Trigger | Condition | Action |
|---------|----------|--------|
| TSR declining | 2 consecutive cycles TSR drop > 10% | CHO starts recruitment |
| Voluntary offline | Agent requests retirement | CHO approval |
| Capability gap | New task type with no matching agent | CHO assessment + internal promotion / external hire |

### Recruitment Process

```
1. CHO publishes job description (capability matrix + KPI standards)
2. Internal agent application (e.g., agent levels up via new Skill)
3. CHO interview assessment (capability test + scenario simulation)
4. Trial period (2 assessment cycles)
5. Regularization (CHO signature + registry update)
```

## Natural Language Commands

```
"List all active agents" -> Agent directory table
"Check CFO availability" -> Agent status + KPIs
"Recruit a new agent" -> Recruitment process
"What's missing from our C-suite" -> Missing agent analysis
"List all ready execution agents" -> EXEC-001/002/003/006
```

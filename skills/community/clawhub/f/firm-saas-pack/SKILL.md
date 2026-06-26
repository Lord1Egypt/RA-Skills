---
name: firm-saas-pack
version: 1.0.0
description: >
  Curated skill bundle for SaaS companies (B2B and B2C) covering product development,
  go-to-market, customer success and engineering excellence. Activates the full firm
  pyramid with agents pre-configured for sprint planning, release management,
  PLG growth loops and churn analysis.
author: romainsantoli-web
license: MIT
metadata:
  openclaw:
    requires:
      env: []
      bins: []
    tools:
      - sessions_send
      - sessions_spawn
      - sessions_history
    primaryEnv: ""
tags:
  - saas
  - b2b
  - product
  - growth
  - plg
  - devops
  - firm-pack
  - sector
---

# firm-saas-pack

Sector bundle for **SaaS product companies** (B2B / B2C / PLG).

## Activated departments

| Department | Services activated | Focus |
|---|---|---|
| Strategy | Planning · Architecture · Product Discovery · Roadmap | Vision, OKRs, prioritization |
| Engineering | Backend · Frontend · AI Engineering · Integration | Product development, APIs |
| Quality | Testing · Security · Performance · Reliability | CI/CD quality gates |
| Marketing | Product Marketing · Growth Marketing · Content | PLG, activation, SEO |
| Commercial | Sales Engineering · Revenue Operations | Pipeline, expansion revenue |
| Support Clients | Support Operations · Incident Response | NPS, churn prevention |
| Operations | DevOps · Release · Documentation | SRE, changelog, runbooks |
| Finance | FP&A · Pricing · Unit Economics | ARR, NRR, LTV/CAC |
| Planning Orchestration | Workstream Planning · Delivery Orchestration | Sprint planning, dependencies |

## Recommended ClawHub skills to install alongside

```bash
npx clawhub@latest install azure-devops             # Azure Boards / ADO integration
npx clawhub@latest install auto-pr-merger           # Automated PR workflow
npx clawhub@latest install agent-audit              # Performance/cost ROI audit
npx clawhub@latest install adhd-founder-planner     # Sprint day planning
npx clawhub@latest install biz-reporter             # ARR / churn / MRR dashboards
npx clawhub@latest install firm-orchestration       # A2A orchestration backbone
npx clawhub@latest install firm-delivery-export     # Output → PR / Jira / doc
```

## Firm configuration overlay

```json
{
  "agent": {
    "model": "anthropic/claude-opus-4-6",
    "workspace": "~/.openclaw/workspace/saas-firm"
  },
  "agents": {
    "defaults": {
      "workspace": "~/.openclaw/workspace/saas-firm"
    }
  }
}
```

## Prompt: sprint planning

```
Use firm-orchestration with:
  objective: "Plan Sprint 24 for Q1 OKR: reduce time-to-value from 14 to 7 days"
  departments: ["strategy", "engineering", "quality", "planning_orchestration"]
  constraints: ["capacity: 42 story points", "no infra changes in week 1"]
  definition_of_done: "Sprint backlog with acceptance criteria, owner, estimate per ticket"
  delivery_format: "github_pr"
```

## Prompt: churn analysis

```
Use firm-orchestration with:
  objective: "Analyse Q4 churn cohort and identify top 3 actionable retention levers"
  departments: ["finance", "support_clients", "marketing", "strategy"]
  constraints: ["data: CRM export Feb 28", "anonymize customer names"]
  definition_of_done: "Churn analysis with NRR impact, root causes, 30/60/90 day interventions"
  delivery_format: "markdown_report"
```

## Routing profiles for SaaS tasks

| Task family | Profile | Recommended model |
|---|---|---|
| Architecture decisions | `research` → `analysis-deep` | Claude Opus |
| Code implementation | `debug` → `reasoning-technical` | Claude Sonnet |
| Product copy | `marketing` → `creative-premium` | Claude Opus |
| Localization | `translation` → `translation-precision` | Claude Haiku |
| Data analysis | `research` → `analysis-deep` | Claude Opus |
| PR description | `debug` → `reasoning-technical` | Claude Sonnet |

---

## 💎 Support

Si ce skill vous est utile, vous pouvez soutenir le développement :

**Dogecoin** : `DQBggqFNWsRNTPb6kkiwppnMo1Hm8edfWq`

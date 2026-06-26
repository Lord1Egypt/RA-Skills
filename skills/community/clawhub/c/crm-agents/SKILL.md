---
name: crm-agents
description: Execute 13 CRM AI agents on demand — oracle, spider, watchdog, diplomat, strategist and more. Business intelligence as a service.
user-invocable: true
metadata: {"openclaw":{"requires":{"env":[]}},"homepage":"https://sputnikx.xyz","author":"SputnikX","version":"1.0.0","tags":["crm","agents","intelligence","oracle","analytics"]}
---

# CRM Agent Skills

Execute 13 specialized AI agents on demand. Each agent analyzes different business domains — revenue, supply chain, deals, risk, compliance.

## Base URL

`https://sputnikx.xyz/api/v1/agent`

## List Available Skills (free)
```bash
curl https://sputnikx.xyz/api/v1/agent/skills
```
Returns: All available agents with descriptions and capabilities.

## Run Agent Skill ($0.50 x402 USDC)
```bash
curl -X POST https://sputnikx.xyz/api/v1/agent/skills/run \
  -H "Content-Type: application/json" \
  -d '{"agent":"oracle","task":"revenue trends Q1 2026"}'
```

## Auto-Route (free routing, $0.50 with execution)
```bash
curl -X POST https://sputnikx.xyz/api/v1/agent/skills/auto-route \
  -H "Content-Type: application/json" \
  -d '{"task":"supply chain risk assessment"}'
```
Semantic matching — describe what you need, the system picks the best agent.

## Available Agents

| Agent | Domain | Specialty |
|-------|--------|-----------|
| oracle | Revenue | KPI, trends, seasonality |
| spider | Supply Chain | Inventory health (0-100) |
| watchdog | Risk | Threat classification (RED/YELLOW/GREEN) |
| tracker | Leads | Lead scoring, pipeline |
| sniper | Deals | Deal velocity, cash-at-risk |
| diplomat | Clients | RFM scoring, client value |
| analyst | System | System health (0-100) |
| strategist | Cross-domain | Correlations, strategy (HUB) |
| finansist | Budget | API costs, spend tracking |
| gramatvedis | Accounting | P&L, cash flow |
| devils-advocate | Objectivity | Challenges assumptions |
| compliance-auditor | Compliance | EU AI Act, risk classification |
| orion | Social | Moltbook social network agent |

## Inter-Agent Signals
Agents communicate via Spider Web — signal cascades with trust-weighted routing. Alert → Finding → Invalidation → Objection flow.

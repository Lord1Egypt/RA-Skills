---
name: firm-ecosystem-audit-pack
version: 1.0.0
description: >
  Ecosystem differentiation audit pack.
  MCP firewall, RAG pipeline, sandbox exec, context health, provenance tracking,
  cost analytics, and token budget optimization. 7 ecosystem tools.
author: romainsantoli-web
license: MIT
metadata:
  openclaw:
    registry: ClawHub
    requires:
      - mcp-openclaw-extensions >= 3.0.0
tags:
  - ecosystem
  - rag
  - firewall
  - cost
  - token-budget
---

# firm-ecosystem-audit-pack

> ⚠️ Contenu généré par IA — validation humaine requise avant utilisation.

## Purpose

Audits ecosystem differentiation features: MCP tool call firewall policies,
RAG pipeline integrity, sandbox execution security, context window health,
SHA-256 provenance tracking, cost analytics, and token budget optimization.

## Tools (7)

| Tool | Description | Severity |
|------|-------------|----------|
| `openclaw_mcp_firewall_check` | MCP tool call firewall policy validation | HIGH |
| `openclaw_rag_pipeline_check` | RAG pipeline integrity audit | HIGH |
| `openclaw_sandbox_exec_check` | Sandbox execution security | HIGH |
| `openclaw_context_health_check` | Context window health monitoring | MEDIUM |
| `openclaw_provenance_tracker` | SHA-256 append-only provenance chain | MEDIUM |
| `openclaw_cost_analytics` | Session cost analytics | MEDIUM |
| `openclaw_token_budget_optimizer` | Token budget optimization | MEDIUM |

## Usage

```yaml
skills:
  - firm-ecosystem-audit-pack

# Run ecosystem audit:
openclaw_mcp_firewall_check config_path=/path/to/config.json
openclaw_rag_pipeline_check config_path=/path/to/config.json
openclaw_cost_analytics session_data='{"model":"claude-4","tokens_in":1000}'
```

## Requirements

- `mcp-openclaw-extensions >= 3.0.0`

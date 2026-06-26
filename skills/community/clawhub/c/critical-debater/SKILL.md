---
name: critical-debater-suite
description: >
  Multi-agent adversarial debate system with 4 roles (Pro, Con, Judge, Orchestrator),
  per-round evidence refresh, 5-element reasoning chains, and structured bilingual
  Markdown report output. Use this skill when the user says "debate", "start a debate",
  "red team this", "analyze from multiple perspectives", or provides a topic for
  critical examination.
license: MIT-0
compatibility: Requires bash, jq, python3, shasum, and internet access for web search.
metadata:
  author: xwxga
  version: "2.0.0"
  homepage: "https://github.com/xwxga/critical-debater"
  tags: debate, evidence, reasoning, multi-agent, report
---

# Critical Debater Suite — Routing

When a user request matches this skill, route to the appropriate capability module.

## Intent → Capability Routing

| User Intent | Route To |
|---|---|
| "debate", "start a debate", "red team this", "analyze from multiple perspectives", full topic for debate | `capabilities/debate.md` |
| "search evidence", "build evidence store", "find sources" | `capabilities/source-ingest.md` |
| "check freshness", "update evidence status" | `capabilities/freshness-check.md` |
| "verify evidence", "cross-check sources" | `capabilities/evidence-verify.md` |
| "build arguments", "construct debate turn" | `capabilities/debate-turn.md` |
| "judge round", "audit round", "evaluate arguments" | `capabilities/judge-audit.md` |
| "update claims", "claim ledger" | `capabilities/claim-ledger-update.md` |
| "check analogy", "validate historical reference" | `capabilities/analogy-safeguard.md` |
| "final report", "synthesis", "generate report" | `capabilities/final-synthesis.md` |
| Mixed request | Pick primary intent, chain capabilities in required order |

## Generic Tool Names

Use provider-agnostic names in all capability prompts:

| Generic Name | Claude Code | Codex | GPT/OpenClaw |
|---|---|---|---|
| `search` | WebSearch | web_search | web_search |
| `fetch` | WebFetch | - | browse |
| `spawn_role` | Agent | subprocess | - |
| `read` | Read | read | read |
| `write` | Write | write | write |

## Model Tiers

| Tier | Description |
|---|---|
| `fast` | Cheapest, simple tasks |
| `balanced` | Good reasoning at reasonable cost |
| `deep` | Best reasoning, verification, causal audit |

## Fallback Chains

- **search**: native → adapter → `evidence_gap` soft-failure
- **fetch**: native → adapter → `fetch_skipped` soft-failure
- **spawn_role**: native → adapter → serial role emulation

## Data Contracts

All JSON schemas are defined in `references/data-contracts.md`. This is the single source of truth for all agent outputs.

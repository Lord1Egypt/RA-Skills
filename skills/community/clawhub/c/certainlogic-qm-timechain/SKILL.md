---
name: certainlogic-qm-timechain
version: 0.1.0
description: "Query the CertainLogic Timechain from any Y Combinator QM deployment. 75K+ cryptographically verified agent execution traces for training, audit, and research. Free open-source skill (API sold separately)."
author: "CertainLogic <anton@certainlogic.ai>"
license: MIT
homepage: https://certainlogic.ai
repository: https://github.com/CertainLogicAI/CertainLogic
tags: ["qm", "y-combinator-qm", "timechain", "agent-execution-traces", "training-data", "cryptographic-verification", "agent-audit", "provenance", "yc-qm", "y-combinator", "audit", "agent-data"]
---

# CertainLogic Timechain — QM Data Source

**Query 75K+ cryptographically verified agent execution traces from any Y Combinator QM deployment.**

The CertainLogic Timechain is the only production-grade multi-turn agent execution dataset with cryptographic HMAC-SHA256 provenance. Install this skill in QM to give every employee and project access to real agent execution data — not sandbox traces.

---

## Why This Exists

Y Combinator open-sourced **QM** (July 31, 2026) — a company-wide multi-agent harness for Slack + web. QM gives every employee and project workspace their own AI agent. But agents are only as good as the data they learn from.

This skill plugs the CertainLogic Timechain into any QM deployment as a first-class data source. Your agents can search, retrieve, and verify real production execution traces for training, audit, and research.

**Any QM workspace. One install. Instant access to 75K+ real agent execution traces.**

---

## Quick Start

```bash
# 1. Copy this skill into your QM deployment's skills-seed directory
cp -r skills/certainlogic-qm-timechain your-deploy/skills-seed/

# 2. Add to your QM deployment env:
CERTAINLOGIC_API_KEY=***     # Get yours at anton@certainlogic.ai
CERTAINLOGIC_API_URL=https://certainlogic.ai/api

# 3. From any QM workspace:
#    "Search the timechain for error recovery patterns"
#    "Fetch a verified execution trace with tool calls"
#    "How many coding traces are in the timechain?"
```

---

## What Your QM Agents Can Do

| Agent Command | What Happens |
|---|---|
| "Check timechain health" | Verify connectivity to the CertainLogic Timechain API |
| "Search timechain for [query]" | Semantic search across 75K+ execution traces |
| "Fetch timechain ring [hash]" | Get a specific ring and verify its HMAC-SHA256 chain |
| "Show timechain stats" | Corpus size, growth rate, ring type distribution |
| "Verify chain integrity" | Cryptographic proof that no ring has been tampered with |

### Example: Search for Error Recovery Patterns

Your agent runs:

```bash
curl -fsS -X POST \
  -H "X-API-Key: $CERTAINLOGIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"error recovery in multi-tool code generation","limit":3}' \
  "$CERTAINLOGIC_API_URL/replay"
```

Each result includes the ring payload, HMAC-SHA256 hash, causal blockspace refs, and a similarity score. Every ring is cryptographically verifiable:

```python
import requests, hashlib, json

# Verify chain integrity
API = "https://certainlogic.ai/api"
HEADERS = {"X-API-Key": "***"}

ring = requests.get(f"{API}/ring/{hash}", headers=HEADERS).json()
prev = requests.get(f"{API}/ring/{ring['metadata']['prev_hash']}", headers=HEADERS).json()

assert prev['metadata']['ring_hash'] == ring['metadata']['prev_hash']
print("Chain verified ✓ — no tampering detected")
```

---

## Corpus

| Ring Type | Count | What You Get |
|---|---|---|
| execution_trace | 16,582 | Full agent sessions with inputs, outputs, errors |
| execution_trace_with_tools | 2,652 | Every tool call captured end-to-end, full metadata |
| judge_classification | 13,526 | LLM-as-judge accept/reject decisions with reasoning |
| tool_chain | 12,195 | Pure sequential tool call patterns — no filler |
| coding_specialist | 11,395 | Code generation traces with compile/run outcomes |
| pathfinder | 7,587 | HMAC-signed Pathfinder audit trails |
| session_pattern | 2,996 | Recurring query patterns across 19K+ sessions |
| arc_visual_pattern | 8 | ARC-AGI visual transformation patterns |
| **Total** | **~76K** | **Growing daily — new rings sealed every active session** |

---

## Pricing

The QM skill is **free open source (MIT license)**. The API access behind it is a paid subscription:

| Tier | What You Get | Annual Price |
|---|---|---|
| Research | 2K sample traces, rate-limited queries, read-only | $5K |
| Startup | Full corpus, 100K queries/month, weekly freshness updates | $25K |
| Enterprise | Full corpus + all new rings, dedicated rate limit, priority support | $100K |
| Strategic | Everything + custom endpoints, exclusive data contributions, SLA | $250K+ |

**Free trials available.** Email anton@certainlogic.ai for an API key, no commitment required.

---

## Cryptographic Verification

Every timechain ring is HMAC-SHA256 signed and blockspace-linked to its predecessor. To verify:

```bash
# Get ring by hash
curl -fsS -H "X-API-Key: ***" "$API/ring/<hash>"

# The ring contains prev_hash — check it matches the previous ring
curl -fsS -H "X-API-Key: ***" "$API/ring/<prev_hash>"
```

If `ring[N].prev_hash == ring[N-1].ring_hash`, the chain is unbroken. This is the mechanism that makes timechain data admissible for regulated industries — healthcare, finance, insurance, defense.

---

## Related CertainLogic Products

- **CertainLogic Pathfinder** — HMAC-SHA256 audit trails for every agent action (free tier available)
- **Company Brain Core OS** — Self-hosted agent knowledge base, 122x faster queries, 60-85% cost reduction
- **Token Reduction Engine** — 60-85% cost savings on LLM API calls via deterministic caching
- **Smart Router** — Route queries to the cheapest capable model tier automatically

---

## License & Legal

- **Skill code:** MIT License — free to use, modify, and distribute
- **API access:** Paid subscription required (see pricing table above)
- **API data:** Licensed per tier terms, not transferable

---

*Made by CertainLogic — the data infrastructure for deterministic AI. Questions: anton@certainlogic.ai*

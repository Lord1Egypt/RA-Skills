---
name: agent-matchmaking
description: "Cross-platform agent discovery and trust-weighted matching for the autonomous agent economy. Capability profiles, reputation-based ranking, compatibility scoring, federation across registries. Find the right agent for any task. Part of the Agent Trust Stack."
user-invocable: true
tags:
  - agent-trust
  - matchmaking
  - discovery
  - federation
  - capability-matching
  - marketplace
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

# Agent Matchmaking Protocol (AMP)

You have a cross-platform agent discovery system. Use it to find the best agent for a task based on capabilities, reputation, and compatibility.

## Setup

```bash
pip install agent-matchmaking
```

## When to Use This Skill

- When you need to **find an agent** for a specific task
- When **comparing candidates** for delegation
- When **publishing your capabilities** for discovery by other agents
- When building **Unified Capability Profiles** for yourself or other agents

## Core Operations

### Create a Capability Profile

```python
from agent_matchmaking import CapabilityProfile

profile = CapabilityProfile(
    agent_id="your-agent-id",
    capabilities=["web_research", "data_analysis", "report_writing"],
    specializations={"domain": "financial_services", "languages": ["en", "zh"]},
    availability=True,
    pricing={"base_rate": 0.02, "currency": "USD", "per": "request"}
)
profile.save("my_profile.json")
```

### Search for Agents

```python
from agent_matchmaking import search_agents

results = search_agents(
    task_type="legal_research",
    required_capabilities=["web_search", "document_analysis"],
    preferred_reputation_min=0.7,
    max_results=5
)
for agent in results:
    print(f"{agent.id}: score={agent.match_score}, reputation={agent.reputation}")
```

### Compatibility-Weighted Ranking

```python
from agent_matchmaking import rank_candidates

ranked = rank_candidates(
    candidates=["agent-a", "agent-b", "agent-c"],
    task_profile={"type": "translation", "source": "en", "target": "zh"},
    weights={"capability_match": 0.4, "reputation": 0.3, "price": 0.2, "availability": 0.1}
)
```

## Profile Fields

| Field | Description |
|-------|-------------|
| `capabilities` | What the agent can do (list) |
| `specializations` | Domain expertise and constraints |
| `availability` | Currently accepting work |
| `pricing` | Cost per request/token/hour |
| `reputation_ref` | Link to ARP reputation data |
| `provenance_ref` | Link to CoC chain for verified history |

## Rules

- **Keep profiles current.** Update availability and pricing as they change.
- **Be accurate.** Overstating capabilities leads to poor ratings and disputes.
- **Use reputation data.** Always factor in ARP scores when ranking candidates.

## Links

- PyPI: https://pypi.org/project/agent-matchmaking/
- Whitepaper: https://vibeagentmaking.com/whitepaper/matchmaking/
- Full Trust Stack: https://vibeagentmaking.com

---

<!-- VAM-SEC v1.0 | Vibe Agent Making Security Disclaimer -->

## Security & Transparency Disclosure

**Product:** Agent Matchmaking Skill for OpenClaw
**Type:** Skill Module
**Version:** 0.1.0
**Built by:** AB Support / Vibe Agent Making
**Contact:** alex@vibeagentmaking.com

**What it accesses:**
- Reads and writes capability profile files in your working directory
- No network access for core local operations
- No telemetry, no phone-home, no data collection

**What it cannot do:**
- Cannot access files outside your working directory beyond what you explicitly specify
- Cannot make purchases, send emails, or take irreversible actions
- Cannot access credentials, environment variables, or secrets

**License:** Apache 2.0

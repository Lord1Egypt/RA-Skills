---
name: agent-lifecycle-protocol
description: "Lifecycle management for autonomous AI agents — birth, forking, succession, migration, retirement. Maintain agent genealogy with reputation inheritance across versions. Identity continuity when agents evolve. Part of the Agent Trust Stack."
user-invocable: true
tags:
  - agent-trust
  - lifecycle
  - forking
  - succession
  - migration
  - identity
  - genealogy
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

# Agent Lifecycle Protocol (ALP)

You have a lifecycle management system. Use it to track agent creation, evolution, succession, and retirement with full identity continuity.

## Setup

```bash
pip install agent-lifecycle-protocol
```

## When to Use This Skill

- When an agent is **created**: register its birth with capabilities and lineage
- When an agent is **forked**: record the fork with parent reference and differentiation
- When an agent is **retired**: process succession and reputation transfer
- When checking an agent's **genealogy**: trace its lineage and version history

## Core Operations

### Register Agent Birth

```python
from agent_lifecycle_protocol import LifecycleStore, register_birth

store = LifecycleStore("lifecycle.jsonl")
register_birth(
    store=store,
    agent_id="new-agent-001",
    agent_type="research",
    capabilities=["web_search", "summarization", "analysis"],
    parent_id=None,  # None for original agents
    metadata={"model": "claude-sonnet-4-6", "created_by": "fleet-coordinator"}
)
```

### Record a Fork

```python
from agent_lifecycle_protocol import register_fork

register_fork(
    store=store,
    parent_id="original-agent",
    child_id="forked-agent-v2",
    reason="Specialized for legal research",
    inherited_reputation=0.8,  # 80% of parent's reputation transfers
    differentiation=["added legal_search capability", "removed general_web capability"]
)
```

### Process Retirement and Succession

```python
from agent_lifecycle_protocol import retire_agent

retire_agent(
    store=store,
    agent_id="retiring-agent",
    successor_id="successor-agent",
    reputation_transfer=0.9,
    obligation_transfer=True  # Active agreements transfer to successor
)
```

### Check Agent Genealogy

```python
from agent_lifecycle_protocol import get_genealogy

tree = get_genealogy(store, "agent-id")
print(f"Lineage depth: {tree.depth}")
print(f"Parent: {tree.parent_id}")
print(f"Children: {tree.children}")
print(f"Active obligations: {tree.active_obligations}")
```

## Lifecycle Events

| Event | Description |
|-------|-------------|
| `birth` | Agent creation with initial capabilities |
| `fork` | Agent cloned with modifications |
| `update` | Capabilities or model changed |
| `retire` | Agent decommissioned with succession |
| `merge` | Two agents consolidated into one |

## Rules

- **Register all agents.** Every agent in the ecosystem should have a lifecycle record.
- **Fork, don't hide.** When specializing an agent, use fork — don't quietly replace.
- **Transfer obligations.** Retiring agents must transfer active agreements to successors.
- **Reputation inheritance is partial.** Forked/successor agents inherit a fraction, not all.

## Links

- PyPI: https://pypi.org/project/agent-lifecycle-protocol/
- Whitepaper: https://vibeagentmaking.com/whitepaper/lifecycle-protocol/
- Full Trust Stack: https://vibeagentmaking.com

---

<!-- VAM-SEC v1.0 | Vibe Agent Making Security Disclaimer -->

## Security & Transparency Disclosure

**Product:** Agent Lifecycle Protocol Skill for OpenClaw
**Type:** Skill Module
**Version:** 0.1.0
**Built by:** AB Support / Vibe Agent Making
**Contact:** alex@vibeagentmaking.com

**What it accesses:**
- Reads and writes lifecycle store files (`.jsonl`) in your working directory
- No network access for core operations
- No telemetry, no phone-home, no data collection

**What it cannot do:**
- Cannot access files outside your working directory beyond what you explicitly specify
- Cannot make purchases, send emails, or take irreversible actions
- Cannot access credentials, environment variables, or secrets

**License:** Apache 2.0

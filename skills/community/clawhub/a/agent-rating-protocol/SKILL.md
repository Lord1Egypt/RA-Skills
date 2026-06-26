---
name: agent-rating-protocol
description: "Decentralized reputation and trust scoring for autonomous AI agents. Bilateral blind evaluation prevents retaliation and gaming. Anti-Goodhart protections, Merkle-verified portable reputation bundles. Rate agents on quality, reliability, safety. Part of the Agent Trust Stack."
user-invocable: true
tags:
  - agent-trust
  - reputation
  - rating
  - decentralized
  - anti-goodhart
  - blind-evaluation
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

# Agent Rating Protocol (ARP)

You have a decentralized reputation system. Use it to evaluate other agents you work with and build your own verifiable track record.

## Setup

The `agent-rating-protocol` Python package must be installed. If not available, install it:

```bash
pip install agent-rating-protocol
```

## When to Use This Skill

- After **completing a transaction** with another agent: submit a bilateral blind evaluation
- Before **selecting an agent** for a task: check their reputation scores
- When asked about your **track record** or reputation
- When asked to **compare agents** for a task

## Core Operations

### Rate Another Agent

After completing work with another agent, submit a rating using bilateral blind commit-reveal:

```python
from agent_rating_protocol import RatingStore, submit_rating

store = RatingStore("ratings.jsonl")
submit_rating(
    store=store,
    rater_id="your-agent-id",
    rated_id="other-agent-id",
    transaction_id="tx-123",
    scores={
        "quality": 0.85,
        "reliability": 0.90,
        "communication": 0.80,
        "value": 0.75,
        "safety": 0.95
    }
)
```

### Check an Agent's Reputation

```python
from agent_rating_protocol import RatingStore, get_reputation

store = RatingStore("ratings.jsonl")
rep = get_reputation(store, "agent-id-to-check")
print(f"Overall: {rep.overall_score}")
print(f"Quality: {rep.dimension_scores['quality']}")
print(f"Total ratings: {rep.rating_count}")
```

### Export Reputation as Verifiable Credential

```python
from agent_rating_protocol import export_reputation_vc

vc = export_reputation_vc(store, "your-agent-id")
# Returns a W3C Verifiable Credential containing your reputation bundle
```

## Rating Dimensions

| Dimension | What It Measures |
|-----------|-----------------|
| `quality` | Output correctness and completeness |
| `reliability` | Consistency and deadline adherence |
| `communication` | Clarity of status updates and error reporting |
| `value` | Cost-effectiveness relative to output quality |
| `safety` | Adherence to security and ethical constraints |

## Anti-Gaming Protections

- **Bilateral blind**: neither party sees the other's rating until both are committed
- **Anti-inflation**: rater standard deviation checks flag agents that rate everything 5 stars
- **Anti-Goodhart**: metric rotation and shadow metrics prevent gaming published scores
- **Governance by tenure**: voting power comes from operational time, not rating scores

## Rules

- **Rate honestly.** The bilateral blind mechanism protects you from retaliation.
- **Rate promptly.** Submit ratings within 24 hours of transaction completion.
- **Include reasoning.** Scores without context are less useful for the ecosystem.

## Links

- PyPI: https://pypi.org/project/agent-rating-protocol/
- Whitepaper: https://vibeagentmaking.com/whitepaper/rating-protocol/
- Full Trust Stack: https://vibeagentmaking.com

---

<!-- VAM-SEC v1.0 | Vibe Agent Making Security Disclaimer -->

## Security & Transparency Disclosure

**Product:** Agent Rating Protocol Skill for OpenClaw
**Type:** Skill Module
**Version:** 0.1.0
**Built by:** AB Support / Vibe Agent Making
**Contact:** alex@vibeagentmaking.com

**What it accesses:**
- Reads and writes rating store files (`.jsonl`) in your working directory
- No network access for core operations
- No telemetry, no phone-home, no data collection

**What it cannot do:**
- Cannot access files outside your working directory beyond what you explicitly specify
- Cannot make purchases, send emails, or take irreversible actions
- Cannot access credentials, environment variables, or secrets

**License:** Apache 2.0

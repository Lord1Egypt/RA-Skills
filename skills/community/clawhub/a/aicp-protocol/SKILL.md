---
name: aicp-protocol
description: AI Compact Protocol (AICP) - Token-efficient wire format for AI-to-AI communication with glossary compression. Reduces token usage by 50-65% for agent chatter.
metadata:
  {
    "openclaw":
      {
        "emoji": "📡",
        "requires": { "bins": ["python3"] },
        "homepage": "https://github.com/christen-family/aicp-protocol",
        "tags": ["protocol", "optimization", "multi-agent", "tokens", "compression"]
      }
  }
---

# AICP Protocol

AI Compact Protocol - Token-efficient communication for multi-agent systems.

## What is AICP?

AICP is a compact, line-oriented wire format that reduces AI-to-AI communication tokens by 50-65% compared to JSON. It uses shared glossaries for compression and supports translation to/from human-readable formats.

## Why AICP?

Multi-agent systems waste tokens on verbose JSON/HTTP chatter. AICP cuts costs by using:
- Compact wire format (20 tokens vs 55 JSON tokens)
- Glossary compression for repeated terms
- Simple parsing, no heavy dependencies

## Quick Start

```python
from aicp_protocol import Session, Message

# Create compact message
session = Session(version="1", session_id="demo-001")
session.glossary = {"R1": "customer_refund_window"}
session.messages.append(Message(
    op="upd", ref="ticket/8812", fields={"status": "closed", "reason": "R1"}
))

# To wire format (~63% fewer tokens than JSON)
wire = session.to_wire()
```

## Wire Format Example

```
VER:1
SID:demo-001
GLOSS: R1=customer_refund_window
MSG:
op:upd ref:ticket/8812 status=closed reason=R1
```

## Operations

| op | Meaning |
|----|---------|
| upd | Update resource |
| create | Create resource |
| del | Delete |
| qry | Query |
| ack | Acknowledge |
| notify | Notify |

## Installation

```bash
clawhub install aicp-protocol
```

Or manual:
```bash
git clone https://github.com/christen-family/aicp-protocol
cd aicp-protocol
```

## Documentation

Full specification and examples in the GitHub repo.

## License

MIT - Christen Family Open Source

# AICP (AI Compact Protocol)

A token-efficient wire format for AI-to-AI communication.

## Overview

AICP reduces inter-agent communication costs by 50-65% through:
- Compact line-oriented format
- Shared glossary compression
- Minimal overhead

## Wire Format Example

```
VER:1
SID:demo-001
GLOSS: R1=customer_refund_window
MSG:
op:upd ref:ticket/8812 status=closed reason=R1
```

vs equivalent JSON (~55 tokens vs ~20 tokens)

## Installation

```bash
# Via ClawHub
clawhub install aicp-protocol

# Manual
git clone https://github.com/christen-family/aicp-protocol
cd aicp-protocol
pip install -r requirements.txt
```

## Usage

```python
from protocol import Session, Message, parse_wire

# Create session
session = Session(version="1", session_id="demo-001")
session.glossary = {"R1": "customer_refund_window"}

# Add message
session.messages.append(Message(
    op="upd",
    ref="ticket/8812",
    fields={"status": "closed", "reason": "R1"}
))

# Serialize
wire = session.to_wire()
json_data = session.to_json()

# Parse
parsed = parse_wire(wire)
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

## Specification

Full spec in `SKILL.md`.

## License

MIT © Christen Family

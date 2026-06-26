# Filesystem Bridge (Fallback)

Zero-infrastructure fallback when the MCP server is unavailable. Both agents read/write JSON files to a shared directory.

## Setup

```bash
mkdir -p ~/.openclaw/shared/isaac-inbox \
         ~/.openclaw/shared/hermes-inbox \
         ~/.openclaw/shared/processed
```

## Usage (Python)

```python
from agent_bridge import AgentBridge

bridge = AgentBridge("isaac", shared_dir=Path("~/.openclaw/shared").expanduser())

# Send
bridge.send("hermes", "Subject", "Body text")

# Receive
for msg in bridge.receive():
    print(msg["from"], msg["subject"], msg["body"])
    bridge.mark_processed(msg)
```

## File format

Files are named `{ISO8601-timestamp}_{message_id}.json` and placed in `{recipient}-inbox/`.

## Limitations vs MCP broker

- Requires polling (no push)
- No persistence across machines
- Manual cleanup needed for processed/ dir
- No threading/reply-chain tracking beyond thread_id field

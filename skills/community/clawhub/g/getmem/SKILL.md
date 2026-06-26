---
name: getmem
description: 'Persistent memory for AI agents via getmem.ai. Call mem.get() before each LLM call to inject context, and mem.ingest() after each turn to save the conversation.'
metadata:
  openclaw:
    emoji: 🧠
    install:
      - id: pip-getmem
        kind: pip
        package: getmem-ai
        label: Install getmem-ai (pip)
---

# getmem.ai Memory Skill

Persistent memory for your AI agent via [getmem.ai](https://getmem.ai).

## Setup

Set your API key in the environment:

```bash
export GETMEM_API_KEY=gm_live_YOUR_KEY_HERE
```

Get your key at https://platform.getmem.ai — **$20 free credit on signup**.

## Usage

```python
import getmem_ai as getmem, os

mem = getmem.init(os.environ["GETMEM_API_KEY"])

# Before each LLM call — get relevant memory context
result = mem.get(user_id, query=user_message)
context = result["context"]  # inject into system prompt

# After each turn — save both user + assistant messages
mem.ingest(user_id, messages=[
    {"role": "user", "content": user_message},
    {"role": "assistant", "content": reply},
])
```

## How it works

1. `mem.get()` fetches only the relevant memories for the current query (semantic search)
2. Context is injected into your system prompt — typically 200-800 tokens
3. `mem.ingest()` saves the full conversation exchange asynchronously
4. Memory persists indefinitely — no TTL, no purge

## Token savings

Standard approach: full conversation history every turn = 10,000-40,000 tokens
With getmem: only relevant context = 200-800 tokens. Save up to 95% on context tokens.

## Links

- Website: https://getmem.ai
- Platform: https://platform.getmem.ai
- PyPI: https://pypi.org/project/getmem-ai/
- npm: https://npmjs.com/package/getmem
- OpenClaw plugin: clawhub:getmem-openclaw

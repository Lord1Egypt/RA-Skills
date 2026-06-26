---
name: "@getmem/openclaw-getmem"
description: "Persistent memory for every user via getmem.ai. Automatically ingests conversations and injects relevant context before each agent reply. Two API calls. $20 free on signup."
metadata:
  openclaw:
    emoji: 🧠
    install:
      - id: npm-getmem-ai
        kind: pip
        package: getmem-ai
---

# getmem.ai Memory Plugin for OpenClaw

Gives your OpenClaw agent persistent memory via [getmem.ai](https://getmem.ai).

## Install

```bash
openclaw plugins install clawhub:@getmem/openclaw-getmem
openclaw config set plugins.openclaw-getmem.apiKey gm_live_...
openclaw gateway restart
```

Get your API key at [platform.getmem.ai](https://platform.getmem.ai) — **$20 free credit on signup**.

## How it works

- **Before each reply** — fetches memory context for the user and injects it into the agent prompt
- **After each reply** — ingests the exchange into getmem for future retrieval

Memory accumulates automatically. No code changes needed.

---
name: cross-platform-memory
description: Injects recent conversations from Telegram and Discord into the OpenClaw gateway session context. Enables the agent to remember and reference cross-platform conversations. Use when the agent needs continuity across Telegram, Discord, and other OpenClaw channels.
---

# Cross-Platform Memory

Reads recent user messages from Telegram and Discord session logs and injects them into the agent's memory context on every gateway request.

## What It Does

When the agent receives a message (via any channel), this bridge reads:
1. **Telegram messages** from the active session's JSONL log
2. **Discord messages** from the same session log (filtered to user-only, excluding bot output)
3. **Local memory files** (MEMORY.md, daily notes)

And prepends them as a system context block so the agent has full cross-platform awareness.

## How It Works

```
User message → Gateway → Memory Bridge (reads JSONL) → System context → Agent
```

- **Telegram detection:** Messages starting with `"Conversation info (untrusted metadata):"`
- **Discord detection:** Entries with `channel: "discord"` and `message.role: "user"`
- **Bot filtering:** Discord bot messages (where the message author is a bot) are excluded
- **Platform tagging:** Each message prefixed with `[telegram]` or `[discord]` for clarity
- **Time sorting:** Most recent messages prioritised, limited to last 8 per platform

## Setup

### 1. Configure the session log path

The bridge reads from OpenClaw's session logs. Default path:
```
C:\Users\<user>\.openclaw\agents\main\sessions\
```

The bridge auto-detects the most recent JSONL file in that directory.

### 2. Install the skill

```bash
clawhub install cross-platform-memory
```

### 3. Configure the bridge in your mission-control

Copy `references/memory-bridge.ts` to your mission-control's `src/lib/` directory:

```bash
cp references/memory-bridge.ts /path/to/mission-control/src/lib/
```

### 4. Wire into your chat API

In your `src/app/api/mc/chat/route.ts`:

```typescript
import { getMemoryContext } from '@/lib/memory-bridge';

// In your POST handler, before calling the gateway:
const memoryContext = await getMemoryContext();
const messages = memoryContext
  ? [{ role: 'system' as const, content: memoryContext }, { role: 'user' as const, content: message }]
  : [{ role: 'user' as const, content: message }];
```

## Configuration

The skill uses environment variables for machine-specific paths (set these in your `.env` or system environment):

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENCLAW_SESSIONS_DIR` | `C:\Users\.openclaw\agents\main\sessions` | Path to OpenClaw session logs |
| `OPENCLAW_WORKSPACE` | `C:\Users\.openclaw\workspace` | Path to workspace files |

In `memory-bridge.ts`:

| Setting | Default | Description |
|---------|---------|-------------|
| `MESSAGES_PER_PLATFORM` | `8` | Max messages per platform to include |
| `MAX_MESSAGE_AGE_HOURS` | `20` | Only include messages from last N hours |
| `SESSIONS_DIR` | `C:\Users\...\.openclaw\agents\main\sessions` | Path to session logs |

## Output Format

```
MEMORY CONTEXT:

## MEMORY.md
[Curated long-term memories]

## Today's Notes
[Daily notes]

## Recent Telegram Conversation
[telegram] Dan: message 1
[telegram] Dan: message 2

## Recent Discord Conversation
[discord] Dan: message 1
[discord] Dan: message 2

IMPORTANT: You are Sancho — use the context above to inform your responses.
```

## Known Limitations

- Only reads from the most recent session log file
- Discord bot messages are filtered out (only user messages included)
- Messages older than 20 hours by default are excluded
- If no session logs exist, falls back to MEMORY.md and daily notes only

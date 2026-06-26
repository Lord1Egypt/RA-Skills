---
name: certainlogic-context-manager
license: MIT
description: Prevent AI session token bloat and runaway costs. Tracks query count per session, warns at a configurable threshold, auto-writes a dense handoff summary before reset, and reads it back on the next session start — so no work is lost and every session starts lean. Without session resets, a standard OpenClaw session can balloon from 18K to 400K+ input tokens, multiplying cost 22x. This skill prevents that automatically. Use when managing long AI sessions, reducing token burn, keeping context lean, or implementing session hygiene for any OpenClaw-based agent. Triggers on phrases like "context management", "session reset", "token bloat", "query counter", "handoff", "save context", or "/new". Built by CertainLogic.
---

# Context Manager

Keeps sessions lean. Tracks query count, warns before context bloats, saves a handoff summary so work continues cleanly in the next session.

## How It Works

1. **Counter** — Increment `session_query_count.txt` every turn
2. **Warn** — At threshold, write `handoff.md` and alert the user
3. **Reset** — User runs `/new`; next session reads and deletes `handoff.md`

## Files

| File | Purpose |
|---|---|
| `session_query_count.txt` | Integer. Increment each turn. Create if missing (default `0`). |
| `handoff.md` | Workspace root. Written at threshold. Read + deleted on next session start. |

## Every Turn (mandatory)

```
1. Read session_query_count.txt (default 0 if missing)
2. Increment by 1
3. Write back
4. If count == THRESHOLD: trigger handoff flow
```

Default threshold: **10**. Configurable per deployment.

## Handoff Flow (at threshold)

1. Write `handoff.md` — see [handoff-format.md](references/handoff-format.md) for exact spec
2. Tell the user:
   > ⚠️ **10 queries in** — context is getting heavy. Handoff saved. Run `/new` when ready to continue.
3. Do NOT auto-reset. User controls the reset.

## Session Start Flow

```
1. Check if handoff.md exists
2. If exists AND file is < 3 hours old:
   a. Read it
   b. Apply context to current session
   c. Delete handoff.md
3. Reset session_query_count.txt to 0
```

## Topic Switch Detection

When the user says **"BTW"**, "switching gears", "new topic", or starts a clearly unrelated task:

1. Write/overwrite `handoff.md` immediately (don't wait for threshold)
2. Tell the user: *"Handoff saved — `/new` when ready"*
3. Resume or continue current task

## Why This Matters

Session context is cumulative. Every prior message, tool call, and assistant response is re-sent on every new query. Without resets, a lean 18K-token session becomes 50K–400K+ within hours.

See [token-math.md](references/token-math.md) for cost impact data and reset savings estimates.

## Commands

| Command | Behavior |
|---|---|
| `/new` or `/reset` | User-triggered. New session starts; skill reads handoff.md if present. |
| `/handoff` | Explicit handoff write. Same as threshold flow, on demand. |
| `/counter` | Report current query count and threshold. |

## Configuration

Override defaults in `AGENTS.md` or equivalent workspace config:

```
- CONTEXT_THRESHOLD: 10        # Queries before warning (default: 10)
- HANDOFF_TTL_HOURS: 3         # Hours before handoff.md is considered stale (default: 3)
```

## Reliability Rules

- **Never skip the counter increment** — even for one-liner responses
- **Never auto-reset** — the user owns the session lifecycle
- **Handoff must be written before warning** — never warn without saving state first
- **Counter file is source of truth** — do not track in memory

---

## What This Saves You

| Without this skill | With this skill |
|---|---|
| Sessions balloon to 400K+ tokens | Sessions stay under 25K |
| Cost multiplies 22x over a day | Cost stays near baseline |
| Work lost on manual /new resets | Handoff auto-saved, resumed next session |
| No signal before context degrades | Warning fires before quality drops |

See [token-math.md](references/token-math.md) for the full cost breakdown.

---

*Built by [CertainLogic](https://certainlogic.ai) — trusted fact infrastructure for AI agents.*

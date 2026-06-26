---
name: context-brief
description: "Persistent context survival for OpenClaw. Writes file-based anchors to memory/anchors/ to preserve critical context across sessions. Reads MEMORY.md and daily logs for context — writes only to memory/anchors/. Use when: (1) 'save context', (2) 'what do you remember', (3) long conversations approaching compaction, (4) 'context check', (5) agent starts forgetting earlier decisions, (6) 'hva husker du', (7) resuming after time away. Homepage: https://clawhub.ai/skills/context-brief"
metadata:
  openclaw:
    configPaths:
      - MEMORY.md
      - HEARTBEAT.md
    capabilities: []
---

# Context Brief v3.0

**Install:** `clawhub install context-brief`

Persistent context survival. Captures what matters before it's lost — and restores it when needed.

**Writes ONLY to `memory/anchors/`.** Reads MEMORY.md and daily logs — never modifies them.

## Language

Detect from the user's message language. Default: English.

## How It Works

Three levels of action, based on user request or trigger:

**Level 1 — Context Note** (1-2 unsaved items, low risk)
- Append a brief note to your response, no file writes
- Example: `Unsaved context: [decision X pending, path Y important]`

**Level 2 — Anchor** (3+ unsaved items OR user says "save context")
- Write anchor file to `memory/anchors/`
- Show summary to user after saving
- Anchor contains task state, decisions, pending items — never credentials or secrets

**Level 3 — Deep Anchor** (user explicitly requests "save context deep" or "context check")
- Full anchor with all categories
- User gets the summary

## Triggering

Anchors are written when the **user explicitly asks** ("save context", "context check", "hva husker du", "preserve context") or when resuming after time away.

**Do NOT auto-save without user request.** Level 2+ requires user initiation or explicit consent.

## Write Permissions

| File | Read | Write |
|------|:----:|:-----:|
| `memory/anchors/*.md` | ✅ | ✅ — **Only location this skill writes to** |
| `memory/YYYY-MM-DD.md` | ✅ | ❌ — Never modified |
| `MEMORY.md` | ✅ | ❌ — Recommend changes to user |
| `HEARTBEAT.md` | ✅ | ❌ — Read only |

## Anchor File Format

Write to `memory/anchors/YYYY-MM-DDTHH-mm.md`:

```markdown
# Anchor — YYYY-MM-DDTHH:mm+ZZ:ZZ

## Active State
- Task: [what we're doing]
- Status: [in progress / blocked / awaiting]

## Decisions
- [thing] -> [chosen option] (reason)

## Pending
- [ ] [next action with enough context to execute]

## Key Paths
- [path]: [what it is]
```

**Rules:**
- Create `memory/anchors/` if it doesn't exist
- ISO 8601 timestamps
- Max 20 lines — prioritize ruthlessly
- **REDACT secrets** — strip any line containing: password, token, api_key, secret, bearer, private_key, or credential patterns
- One anchor per checkpoint — never append to old anchors

## After Writing

Show user (in their language):
```
Context anchored (N items) → memory/anchors/YYYY-MM-DDTHH-mm.md
```

## Recovery — On Resume

When resuming or after compaction:

1. Check `memory/anchors/` for recent files (last 48h)
2. If anchor found and items are missing from conversation:
   ```
   Restored from anchor: [brief list of items]
   Continuing: [last active task]
   ```
3. If no anchor and context feels lost, ask the user what they were working on.

## What This Skill Does NOT Do

- Does NOT modify MEMORY.md, HEARTBEAT.md, or daily logs
- Does NOT auto-save without user request or consent
- Does NOT store credentials or secrets
- Does NOT restore silently — always informs user
- Does NOT create files outside `memory/anchors/`

## Guidelines for Agent

1. **Wait for user trigger** — "save context", "context check", or resume
2. **Keep it short** — 20 lines max per anchor
3. **Redact secrets aggressively** — strip any sensitive patterns
4. **Inform on restore** — never restore silently
5. **Only write to `memory/anchors/`** — nowhere else
6. **One anchor per checkpoint** — new file each time
7. **Language follows user** — anchor content in the language being used
8. **Timestamp everything** — ISO 8601

## More by TommoT2

- **cross-check** — Auto-detect and verify assumptions in your responses
- **setup-doctor** — Diagnose and fix OpenClaw setup issues
- **locale-dates** — Format dates/times for any locale

Install the full suite:
```bash
clawhub install context-brief cross-check setup-doctor locale-dates
```

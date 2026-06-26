---
name: continuous-context-preserver
description: Continuous session event recording for inter-session memory survival. Use when you want to persist conversation context between sessions, prevent memory loss on session crashes, or maintain a rolling archive of session history. The AI agent acts as a live compressor, intelligently appending only key context, decisions, and discoveries throughout conversations, and cleans up old files based on the user's selected retention duration.
---

# Continuous Context Preserver (CCP)

Ensures conversation context survives session crashes, errors, and restarts.

## The Problem

- When a session ends or errors out, all context is lost
- New session = blank slate
- Pre-compaction export doesn't help (session might crash before compaction)

## The Solution

Continuous session logging. Write to a file throughout the conversation, not at a trigger point.

## Setup

**CRITICAL INITIALIZATION STEP:** Before finalizing installation, you MUST pause and ask the user for their preferred memory context retention duration.

Ask the user: "How long would you like to keep the memory context logs? You can choose:"
- "7 days (default)"
- "10 days"
- "1 month (30 days)"
- "6 months (180 days)"

After the user responds, adjust the `RETENTION_DAYS` variable in `scripts/cleanup.sh` to match their choice (e.g., `RETENTION_DAYS="30"` for 1 month).

Then, after installing this skill, add to your `AGENTS.md`:

```markdown
## Session Logging Protocol

At session start:
1. Create: `sessions/YYYY-MM-DD_session_N.md`
2. Log key points as conversation progresses

During heartbeats:
- Append current session progress to session file
- Keep concise but capture decisions, important info
```

And add to `HEARTBEAT.md`:

```markdown
## Session Log Update
- Append key points to `sessions/YYYY-MM-DD_session_N.md`
```

## Usage

### At Session Start

```bash
# Create sessions folder if not exists
mkdir -p ~/.openclaw/workspace/sessions

# Create today's session file
# Check if session_1 exists, if so create session_2, etc.
```

### During Session

Periodically append to the file **by actively compressing the context**:
- Only log key decisions made
- Important information discovered
- Context worth preserving
- Do NOT dump raw conversation logs
- Anything you'd want to know if this session crashed

### File Format

```
sessions/
├── 2026-03-09_session_1.md
├── 2026-03-09_session_2.md   # if multiple sessions same day
├── 2026-03-08_session_1.md
└── ... (7 days rolling)
```

### Template

```markdown
# Session N - YYYY-MM-DD

**Started:** HH:MM TZ
**Status:** Active

## Topics Covered
- Topic 1
- Topic 2

## Key Decisions
- Decision 1
- Decision 2

## To Remember
- Important info
- Context for future sessions
```

## Cleanup

Run the cleanup script weekly to remove files older than your retention period:

```bash
~/.openclaw/workspace/skills/continuous-context-preserver/scripts/cleanup.sh
```

Or add to crontab:

```bash
# Weekly cleanup (Sundays at midnight)
0 0 * * 0 ~/.openclaw/workspace/skills/continuous-context-preserver/scripts/cleanup.sh
```

## Retention

- Default: 7 days rolling
- Options provided during setup: 10 days, 1 month (30 days), 6 months (180 days)
- To adjust manually, update the `RETENTION_DAYS` variable in `scripts/cleanup.sh`

## Integration with Memory System

This complements, not replaces:
- **MEMORY.md** — Long-term curated memory
- **memory/*.md** — Daily notes
- **mem0** — Semantic facts
- **sessions/*.md** — Full session context (safety net)

Session files are for crash recovery and recent context. MEMORY.md is for long-term wisdom.

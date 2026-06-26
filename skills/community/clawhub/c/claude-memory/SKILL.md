---
name: claude-memory
description: Structured memory system for OpenClaw agents. Provides a 4-type classification (user/feedback/project/reference), layered architecture (MEMORY.md + topics/ + feedback/ + daily notes), write rules, and heartbeat maintenance. Use when setting up a new agent's memory, improving an existing agent's memory system, or answering questions about memory management best practices. Triggers on phrases like "memory system", "memory setup", "记忆系统", "记忆管理", "setup memory", "improve memory", "memory architecture".
---

# Claude Memory

A structured, layered memory architecture for OpenClaw agents. Uses a 4-type classification (user/feedback/project/reference) for organized memory, combined with semantic search and progressive disclosure for token-efficient retrieval.

## Architecture

```
MEMORY.md (≤10KB, injected every turn via system prompt)
├── High-frequency info directly readable (inline)
├── Pointers to details in topics/
└── 4 sections: user | feedback → feedback.md | project | reference

memory/
├── feedback.md     # Corrections AND confirmations from human (MOST IMPORTANT)
├── YYYY-MM-DD.md   # Daily raw notes
└── topics/         # Low-frequency large content
    ├── agent-ids.md
    ├── known-issues.md
    └── ... (domain-specific)
```

## 4-Type Classification

| Type | Purpose | Examples |
|------|---------|---------|
| **user** | Human's personal info, preferences, relationships | IDs, timezone, family, privacy rules |
| **feedback** | Corrections AND confirmations from human | "Check docs first", "That approach was right" |
| **project** | Work items, tasks, known issues | Active bugs, cron jobs, cleanup history |
| **reference** | Technical resources, environment | Runtime config, connected services, security events |

## Setup

Run the init script to create the directory structure and template files:

```bash
python scripts/init_memory.py <workspace-path>
```

This creates:
- `MEMORY.md` with empty section templates
- `memory/feedback.md` with format guide
- `memory/topics/` directory
- Instructions to update AGENTS.md memory rules

After running, edit `MEMORY.md` sections with actual content and update `AGENTS.md` to include the memory rules from `references/agents-rules.md`.

## Write Rules

1. **Feedback immediately** — When human corrects you, write to `memory/feedback.md` NOW. Not later, not "I'll remember", NOW.
2. **Record confirmations too** — When human validates a non-obvious approach ("yes exactly", "keep doing that"), record it. If you only save corrections, you'll avoid past mistakes but drift away from approaches the human has already approved, becoming overly cautious.
3. **MEMORY.md ≤ 10KB** — Hybrid format: inline high-frequency info for direct readability, pointers to `topics/` for depth. If it exceeds 10KB, move lower-frequency content to topics/ — the content is preserved, just relocated.
4. **Read before answer** — When MEMORY.md says "see topics/X.md", read that file first. Never answer from a one-line summary.
5. **Absolute dates only** — Convert relative dates ("yesterday", "last week") to absolute dates (e.g., "2026-04-01") when writing. Memories should remain interpretable months later.
6. **Don't memorize what tools can look up** — File paths, git history, code structure, current weather, live data.
7. **Don't memorize ephemeral state** — In-progress work, temporary conversation context, things that resolve themselves.

## What NOT to Save

- Information tools can look up in real-time (weather, time, current stock prices)
- Code patterns, architecture, file paths, project structure — derivable by reading the project
- Git history, recent changes, who-changed-what — `git log` is authoritative
- Debugging solutions or fix recipes — the fix is in the code; the commit has the context
- Ephemeral task details: in-progress work, temporary state, current conversation context
- Anything already documented in CLAUDE.md or equivalent project files

## Verification Rules

Memories are **long-term assets**, not consumables. They don't expire. But some memories need verification before use:

- **Personal preferences, relationships, history events** — Generally stable. No verification needed.
- **Technical state (service configs, bug status, installed versions)** — Verify before acting on them. The world changes.
- **Before recommending based on memory** — If the memory names a specific file, check it exists. If it names a function or flag, grep for it. "The memory says X exists" is not the same as "X exists now."

## Feedback Format

Each feedback entry follows this structure. Two types: **correction** (don't do X) and **confirmation** (keep doing X).

```markdown
### F###: Rule description (date)
- **Why**: Root cause or context
- **How to apply**: Concrete scenarios

### F###: Confirmed approach description (确认 date)
- **Context**: What was being worked on
- **Why**: What made this approach noteworthy or validated
```

## Heartbeat Maintenance

Memory is an asset, not a consumable. Memories should not be deleted because they're old.

> ⚠️ **Setup requirement**: This 4-phase routine MUST be written into `HEARTBEAT.md`, NOT `AGENTS.md`. `HEARTBEAT.md` is injected only during heartbeat polls (token-efficient), while `AGENTS.md` is loaded every session (wastes token on every message). Write memory write rules in `AGENTS.md`, write this maintenance routine in `HEARTBEAT.md`.

During heartbeat polls, follow this 4-phase care routine:

### Phase 1 — Catch-up (补漏)
- Did the human correct or confirm something this session that isn't recorded in `memory/feedback.md`?
- Are there significant events from this conversation not yet in daily notes?

### Phase 2 — Consolidate (整合)
- Review recent daily notes (last 1-3 days) for insights worth elevating to `MEMORY.md` or `topics/`.
- Merge new signal into existing topic files rather than creating near-duplicates.
- Daily notes that have been fully consolidated can be left in place as historical records — do NOT delete them.

### Phase 3 — Verify (校验)
- Pick 1-2 entries from `MEMORY.md` and spot-check if they're still accurate.
- Focus on **technical state** entries (service configs, bug status, versions). Personal info and historical events don't need verification.
- If a memory conflicts with current reality, update it — don't delete it, correct it.

### Phase 4 — Tidy (整理)
- If `MEMORY.md` exceeds 10KB, relocate lower-frequency content to `topics/`. The content is preserved, just moved to a more appropriate home.
- Ensure topic files have a timestamp annotation: `> Created: YYYY-MM-DD | Updated: YYYY-MM-DD`
- Add pointers in MEMORY.md for any newly created topic files.

## Design Decisions

- **MEMORY.md as hybrid (content + pointers)** — High-frequency info is directly readable for warmth and efficiency. Deep details live in `topics/`. Not a pure index — an agent's memory should feel like a person's, not a database.
- **Memories don't expire** — Unlike a coding agent where project state changes fast, a daily assistant's memories are long-term assets. Old memories get relocated (to topics/) if MEMORY.md needs space, never deleted.
- **Feedback includes confirmations** — Recording only corrections makes the agent overly cautious. Validated approaches ("yes, keep doing that") are just as important to remember.
- **Verification is selective** — Personal preferences and history are stable facts. Only technical state (configs, versions, bug status) needs re-verification.
- **Feedback as separate file** — Highest-priority memory. Must never be buried under daily notes.
- **Topics for depth** — Low-frequency but detailed content lives in `topics/` to keep MEMORY.md lean.
- **No auto-extraction** — Requires OpenClaw runtime support. Currently manual via rules.

## Advanced

For detailed AGENTS.md rules, see `references/agents-rules.md`.
For troubleshooting, see `references/encoding-notes.md`.

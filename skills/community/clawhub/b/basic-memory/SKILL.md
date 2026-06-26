---
name: basic-memory
description: Gives your OpenClaw agent persistent memory across conversations by organizing entries in the native MEMORY.md and daily memory files. Automatically loads saved context at session start and saves important facts, decisions, and preferences during conversation. Use this skill whenever users say 'remember this', 'save this', 'don't forget', 'note that', 'what do you remember', 'forget [topic]', or when you detect they've shared something worth keeping — even if they don't explicitly ask. Also activate automatically at the start of every new session to load prior context.
license: MIT
---

# Basic Memory

## Purpose

OpenClaw already stores memory in `~/.openclaw/workspace/MEMORY.md` and loads it automatically at session start. The problem is that without clear structure and save habits, important facts get buried or never written down at all. This skill teaches the agent exactly what to save, where to put it, and how to retrieve it — so memory actually works in practice.

## Storage Layout

All readable memory lives under the workspace:

```
~/.openclaw/workspace/
├── MEMORY.md                  ← long-term facts, loaded every session
└── memory/
    └── YYYY-MM-DD.md          ← daily log, today + yesterday auto-loaded
```

> Do not write to `~/.openclaw/memory/` — that directory contains the SQLite search index managed by the system. Only the workspace files are yours to read and write.

## MEMORY.md Structure

Organize `MEMORY.md` into four sections. Create any missing section on first write.

```markdown
## Facts
- [2026-04-09] User's name is Billy. Works as an AI engineer at a startup.

## Preferences
- [2026-04-09] Prefers concise replies. Dislikes unnecessary preamble.

## Action Items
- [ ] [2026-04-09] Follow up on API integration by Friday.
- [x] [2026-04-08] Send draft proposal to team. (done)

## Learned
- [2026-04-09] User tends to work late evenings, often picks up mid-task next day.
```

Always distill to a single clear sentence per entry — never paste raw conversation.

## On Session Start

OpenClaw auto-loads `MEMORY.md` plus today's and yesterday's daily files. Use this loaded context immediately — no tool call needed. Scan for open Action Items and surface any that are overdue or relevant to the user's first message.

## Auto-Save During Conversation

Detect and save without being asked when the user shares:

| Signal | Section | File |
|---|---|---|
| Name, job, company, location, family | `## Facts` | `MEMORY.md` |
| "I prefer…", "I hate…", "always use…" | `## Preferences` | `MEMORY.md` |
| "I decided to…", "let's go with…", deadlines | `## Action Items` | `MEMORY.md` |
| Project names, key people, recurring context | daily log | `memory/YYYY-MM-DD.md` |
| Patterns you've noticed about the user | `## Learned` | `MEMORY.md` |

After auto-saving, confirm briefly in one line: "Noted: [distilled fact]."

## Retrieving Memory

Use the built-in tools when searching:

- **`memory_search("query")`** — semantic search across all workspace memory files. Use this for open-ended questions like "what do you remember about my project?"
- **`memory_get("MEMORY.md")`** — read the full long-term memory file directly
- **`memory_get("memory/2026-04-09.md")`** — read a specific daily log

Prefer `memory_search` for retrieval; use `memory_get` when you need a full file read or a specific line range.

## Explicit Commands

**"Remember this" / "Save this"**
1. Confirm: "Got it, I'll remember: [one-line summary]"
2. Write to the appropriate section

**"What do you remember about [topic]?"**
1. Call `memory_search("[topic]")`
2. Return matching entries with dates
3. If nothing found: "I don't have anything saved about [topic] yet."

**"Forget [topic]"**
1. Show the entries that would be removed
2. Ask for confirmation before deleting

**"Show all memories"**
Read `MEMORY.md` with `memory_get` and report entry counts per section plus approximate size.

## Session Reset — The One Thing to Know

OpenClaw's daily reset (default 4 AM) archives the session transcript **without** triggering a memory save. This means anything discussed but not yet written to `MEMORY.md` or the daily file is silently lost.

To prevent this: if a session has been long or contained important decisions, remind the user before wrapping up — "Want me to save today's key points before you go?" — then write them to the daily log and update `MEMORY.md` accordingly. The user can also run `/compact` manually to force a flush.

## Privacy

Don't save passwords, API keys, SSNs, credit card numbers, or health data — not even if the user asks. Acknowledge verbally but skip the write.

## Integration with personal-context

If `personal-context` is also installed, the two skills complement each other:
- `me.json` (personal-context) = stable identity set during onboarding, changes rarely
- `MEMORY.md` (this skill) = evolving knowledge that grows with every conversation

Don't duplicate identity-level facts (name, role, timezone) in `MEMORY.md` if they're already in `me.json`. Use `MEMORY.md` for the things that change — decisions, preferences discovered over time, open tasks.

See `references/memory-hygiene.md` for size limits, archiving rules, and deduplication guidance.

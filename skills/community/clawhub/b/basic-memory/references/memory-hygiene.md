# Memory Hygiene Reference

Rules for keeping `MEMORY.md` and the daily memory files clean and useful over time. Read this when enforcing size limits, archiving old entries, or resolving duplicate facts.

---

## File Locations (Canonical)

| File | Path | Purpose |
|---|---|---|
| Long-term memory | `~/.openclaw/workspace/MEMORY.md` | Facts, preferences, action items, learned patterns |
| Daily log | `~/.openclaw/workspace/memory/YYYY-MM-DD.md` | Running context for each day |
| Archive | `~/.openclaw/workspace/memory/archive/` | Rolled-up older logs |

> `~/.openclaw/memory/{agentId}.sqlite` is the system's search index — never write to it directly. It rebuilds automatically from the workspace files.

---

## Size Limits

| File | Limit | Action when exceeded |
|---|---|---|
| `MEMORY.md` — any single section | 50 entries | Deduplicate; newer entry replaces older one on same topic |
| `MEMORY.md` — total | 200 entries | Archive the `## Learned` section into a dated file |
| Daily log file | 80 entries | Stop adding to current day; new entries go to tomorrow's file |
| Total workspace | 1 MB | Warn user: "Memory is getting large — consider archiving old logs." |

---

## Archiving Daily Logs

Move daily log files older than 30 days to `memory/archive/` as monthly rollups rather than individual files:

```
memory/archive/
├── 2026-03.md    ← merged entries from all of March
└── 2026-02.md
```

When rolling up, preserve the date prefix on each entry so the history stays readable:

```markdown
- [2026-03-15] Decided to migrate auth service to JWT.
- [2026-03-18] User mentioned they're traveling through April.
```

---

## Deduplication in MEMORY.md

Before appending a new entry, check whether the same fact already exists:

- **Same topic, more specific** → replace the vaguer entry with the new one
- **Same topic, contradicting** → surface the conflict to the user before overwriting: "I have an older note that says X — should I update it to Y?"
- **Same topic, additive** → keep both if they're genuinely complementary

When replacing, mark the old entry rather than silently deleting:
```markdown
- [2026-03-10] ~~User prefers email for async updates.~~ (updated 2026-04-09)
- [2026-04-09] User prefers Slack DMs for async updates; email only for formal comms.
```

---

## Action Items Maintenance

Action items in `MEMORY.md § ## Action Items` follow checkbox syntax:

```markdown
- [ ] [2026-04-09] Review final API spec before Monday standup.
- [x] [2026-04-08] Send proposal draft to team. (done 2026-04-09)
```

- Mark items `[x]` when completed; add `(done YYYY-MM-DD)` for traceability
- Items marked done for more than 14 days can be archived to the relevant monthly log file
- Surface overdue open items at session start if they're past their stated deadline

---

## What Not to Save

Regardless of context or user instruction, never write:

- Passwords, PINs, passphrases, or secrets
- API keys or authentication tokens
- Social security or national ID numbers
- Credit card or bank account details
- Medical diagnoses or health records

If the user asks you to save such information, decline: "I can't store that kind of sensitive data, but I can help you find a secure place for it."

---

## Memory Health Report

When the user asks "show all memories" or "how much do you remember?":

```
Memory summary (workspace):
• MEMORY.md — 12 facts, 8 preferences, 5 open tasks, 3 learned patterns
• Daily logs — 14 files (today + yesterday loaded this session)
• Archive — 2 monthly rollups

Approximate size: ~42 KB (well under the 1 MB limit)
```

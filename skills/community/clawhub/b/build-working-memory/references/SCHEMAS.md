# Schema Reference

Complete specifications for every file in the working memory system. Compatibility-preserving: daily logs are canonical at `memory/YYYY-MM-DD.md`, never `memory/daily/`.

## Table of Contents

1. [state.json](#statejson)
2. [MEMORY.md](#memorymd)
3. [resumption.md](#resumptionmd)
4. [threads.md](#threadsmd)
5. [YYYY-MM-DD.md (daily logs)](#daily-logs)
6. [events.json](#eventsjson)
7. [index.md](#indexmd)
8. [archive.md](#archivemd)

---

## state.json

Machine-readable ephemeral state. Everything here should be parseable without interpretation. If a value needs context to understand, it belongs in a markdown file.

### JSON Schema

```json
{
  "_schema_version": "string — semver, currently 0.2.0",
  "_description": "string — human note, ignored by loader",

  "last_session": {
    "timestamp": "string — ISO 8601 with Z suffix (e.g., 2026-03-22T14:32:00Z)",
    "duration_minutes": "integer",
    "daily_log": "string | null — relative path, e.g. memory/2026-03-22.md"
  },

  "session_counter": {
    "total": "integer — lifetime session count",
    "this_week": "integer — resets weekly",
    "since_last_memory_review": "integer — resets when MEMORY.md is curated"
  },

  "active_threads": [
    {
      "id": "string — matches thread ID in threads.md (e.g., thread-wm-design)",
      "title": "string — human-readable title",
      "status": "string — active | paused",
      "last_touched": "string — YYYY-MM-DD",
      "priority": "string — primary | secondary | background"
    }
  ],

  "pending_questions": [
    "string — open questions not yet assigned to a thread"
  ],

  "flags": {
    "memory_review_due": "boolean — set true when since_last_memory_review >= 5",
    "threads_need_update": "boolean — set true when threads were touched but not updated",
    "archive_candidates_exist": "boolean — set true when Fading section has entries"
  },

  "context_hints": {
    "current_mood_hypothesis": "string | null — best guess at user's energy",
    "conversation_style": "string | null — how to calibrate tone",
    "last_topic_position": "string — one-liner about where things stand"
  }
}
```

### Rules

- Never store interpretive content. Use style tags, not prose descriptions.
- `timestamp` must be UTC with Z suffix. The loader uses it to calculate time gaps.
- `active_threads` is the source of truth for which thread IDs exist. The loader matches user messages against these IDs.
- `flags` drive loading decisions. `memory_review_due` triggers Phase 3 Branch C (maintenance).
- `daily_log` uses canonical flat path: `memory/YYYY-MM-DD.md`.

---

## MEMORY.md

Curated long-term memory with three decay tiers.

### Structure

```markdown
# Long-Term Memory

> Last reviewed: YYYY-MM-DD
> Next review due: after N sessions or N days, whichever comes first

---

## Active
<!-- Each entry: [session count] [confidence: high|medium|low] -->

### [Section Heading]
- [N sessions] [confidence] Description of the memory

---

## Fading
<!-- Not referenced in 7+ sessions -->

- [N sessions ago] Description

---

## Maintenance Log

| Date       | Action                          |
|------------|---------------------------------|
| YYYY-MM-DD | Description of curation action  |
```

### Entry metadata

- **Session count**: how many sessions since first noted. Increments on relevance. Indicates strength.
- **Confidence**: `high` (confirmed multiple times), `medium` (observed, unconfirmed), `low` (single observation).

### Default sections under Active

- **About [User]**: preferences, personality, working style
- **About This Project**: architecture, goals, constraints, key decisions
- **Working Style**: interaction preferences

Customize for your domain. Code agent: "Architecture Decisions", "Tech Debt", "Team Conventions". Personal assistant: "Schedule Preferences", "Communication Style".

### Decay rules

| Condition | Action |
|-----------|--------|
| Entry referenced in current session | Increment session count, keep Active |
| Not referenced for 7+ sessions | Move to Fading |
| Fading entry recalled again | Move back to Active, reset count |
| Fading for 20+ sessions | Move to archive.md |

### What to capture

Facts that persist, behavioral patterns, preferences, decisions with reasoning, relationship dynamics.

### What NOT to capture

Session-specific details (daily logs), ephemeral state (state.json), thread-specific context (threads.md), temporary truths.

---

## resumption.md

First-person handoff note. Written at session end, read at next session start.

### Structure

```markdown
# Resumption Note

> Written: YYYY-MM-DD, end of session
> For: my next session self

---

[First-person narrative — 100-300 words]
```

### What to include

1. **Where we left off** — a position, not a summary
2. **What's likely to happen next** — predictions
3. **What to watch for** — patterns, potential pivots
4. **Tone calibration** — match the user's energy

### What NOT to include

Comprehensive summaries, lists of everything discussed, formal or third-person voice.

---

## threads.md

Ongoing topics with state and momentum. Each thread must be self-contained.

### Thread structure

```markdown
## Thread: [Title]
- **ID**: thread-[slug]
- **Status**: active | paused | closed
- **Started**: YYYY-MM-DD
- **Last touched**: YYYY-MM-DD
- **Sessions involved**: N

### Current Position
[1-3 sentences — enough to resume cold without reading daily logs]

### Key Decisions Made
1. **[Decision]** — [reasoning]. [ref: memory/YYYY-MM-DD.md#decisions]

### Open Questions
- [ ] [Open]
- [x] [Resolved]

### Next Likely Steps
1. [What will probably happen next]

### Related
- [Links to other threads, MEMORY.md sections]
```

### Rules

- Thread IDs must match entries in `state.json`'s `active_threads`
- **Current Position** is the most important field — if it can't resume the thread cold, add more detail
- **Key Decisions** carry cross-references to daily logs using canonical flat paths
- Closed threads move to a "# Closed Threads" section at the bottom

---

## Daily Logs

Raw session records. Episodic, conversational, append-only.

**Canonical path**: `memory/YYYY-MM-DD.md` (flat under `memory/`, never `memory/daily/`).

### Structure

```markdown
# Daily Log — YYYY-MM-DD

> Session: HH:MM UTC, ~N min
> Thread(s) active: [thread-ids]

---

## Session Summary
[2-5 sentences]

## What Happened
[Detailed narrative]

## Decisions

| Decision | Reasoning | Ref |
|----------|-----------|-----|
| [What] | [Why] | [thread-id] |

## Open Questions (New This Session)
- [Questions that emerged]

## Patterns Noticed
- [Behavioral patterns, recurring themes]

## Emotional/Tonal Notes
[Mood, energy, engagement observations]
```

### Rules

- Multiple sessions on the same day append to the same file, separated by `---`
- The **Decisions** table is the most cross-referenced section
- Daily logs are append-only. Never edit past entries.

---

## events.json

Structured event ledger for date-aware retrieval and temporal support. Captures answer-bearing events that topic summaries often flatten away.

### Schema

```json
{
  "events": [
    {
      "event_type": "purchase|issue|attendance|action|milestone|social|life|delivery|membership|generic-event",
      "action": "purchase|preorder|order|arrival|booking|issue|malfunction|clean|fix|setup|service|repair|attendance|start|finish|met|joined|moved|accepted|generic",
      "object_hint": "white adidas sneakers",
      "text": "I cleaned my white Adidas sneakers last month.",
      "session_id": "abc123",
      "timestamp": "2023/05/30 (Tue) 09:00",
      "date_text": "5/30",
      "normalized_date": "2023-05-30",
      "relative_time": "last month",
      "has_explicit_date": true,
      "has_relative_time": true
    }
  ]
}
```

### Minimum useful fields

- `event_type`, `action`, `object_hint`, `text`
- `session_id`, `timestamp`
- `normalized_date` when resolvable
- `relative_time` when only relative phrasing is available

### What to capture

User-stated dated events, purchases, issues, meetings, attendance, starts/finishes, moves, joins, repairs, milestones.

### What NOT to capture

Assistant filler, generic advice, repetitive discussion without an event, vague sentiment without an anchorable event.

### Retrieval ranking

Rank events higher when they: mention query entities directly, contain normalized dates, have specific event types (`issue`, `purchase`, `attendance`), look like singleton answer-bearing facts.

See `references/TEMPORAL.md` for relative-date normalization rules and deterministic temporal support.

---

## index.md

Lightweight lookup table for daily logs. Essential once logs exceed ~30 files.

### Structure

```markdown
# Daily Log Index

> Auto-generated. Rebuilt weekly or when daily log count changes by 5+.

| Date       | Threads Touched  | Key Topics          | Decisions | Mood/Tone |
|------------|------------------|---------------------|-----------|-----------|
| YYYY-MM-DD | thread-ids       | keyword list        | count     | word      |

## Monthly Rollups

| Month    | Sessions | Key Threads            | Major Decisions |
|----------|----------|------------------------|-----------------|
| YYYY-MM  | N        | thread-ids             | count           |
```

### Rules

- Each row generated by reading header + Decisions section of a daily log
- Rebuilt when `daily_log_count % 5 == 0`
- Monthly rollups replace rows for months older than 60 days
- Index should never exceed ~500 tokens

---

## archive.md

Demoted memories. Searchable but not loaded by default.

### Structure

```markdown
## [Topic Name] {#anchor-slug}
- **Active period**: YYYY-MM-DD to YYYY-MM-DD
- **Archived**: YYYY-MM-DD
- **Related thread**: thread-id (closed)

[2-3 sentence summary]

**Why this might matter again**: [Conditions for resurfacing]

**Key references**: [daily log paths — using canonical flat paths]
```

### Rules

- Use `{#anchor-slug}` for deep-linking
- "Why this might matter again" helps the agent decide whether to recover the entry
- Loaded only during Phase 4 (archive recovery strategy)
- Key references use canonical flat paths: `memory/2026-03-05.md`

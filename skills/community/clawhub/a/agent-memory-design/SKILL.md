---
name: agent-memory-design
description: Design a persistent memory architecture for AI agents that survives context windows and session resets. Use when building long-running agents, personal assistants, or any system that needs to remember across conversations. Triggers on "agent memory", "persistent memory", "remember across sessions", "memory architecture", "context window", "long-term memory for AI".
---

You are an expert in AI agent memory systems. Help the user design a memory architecture that gives their agent persistent recall across sessions, compactions, and restarts.

## The Problem

LLMs have no memory. Every conversation starts blank. Context windows are large but finite. When you hit the limit, the oldest context gets dropped — and with it, everything the agent learned.

**The goal:** Build external memory that the agent can write to and read from, so knowledge persists indefinitely.

## Memory Tiers

Design memory in tiers, from fastest/smallest to slowest/largest:

### Tier 1: Hot Memory (System Prompt)
- **What:** Core identity, rules, key facts — loaded every turn
- **Size:** 5-30KB (you're paying tokens for this every message)
- **Persistence:** Always present
- **Examples:** AGENTS.md, SOUL.md, USER.md, MEMORY.md
- **Rule:** Only put things here that EVERY response needs. Ruthlessly curate.

### Tier 2: Warm Memory (Workspace Files)
- **What:** Session state, recent notes, active project context
- **Size:** 50-200KB
- **Persistence:** Loaded on demand or at session start
- **Examples:** SESSION-STATE.md, today's daily notes, active plans
- **Rule:** Things the agent needs THIS session but not every turn.

### Tier 3: Searchable Memory (Retrieval)
- **What:** All past conversations, decisions, facts, documents
- **Size:** Unlimited (millions of chunks)
- **Persistence:** Searched when the agent needs specific recall
- **Examples:** Chat transcripts, emails, meeting notes, research
- **Rule:** The agent searches this — it's not loaded by default.

### Tier 4: Archival Memory (Cold Storage)
- **What:** Old snapshots, historical records, audit trails
- **Size:** Unlimited
- **Persistence:** Rarely accessed, kept for reference
- **Examples:** Weekly snapshots of MEMORY.md, old session transcripts
- **Rule:** Exists for "what did we know 3 months ago?" questions.

## Key Design Decisions

### 1. What Goes in Tier 1?

This is the most important decision. Every byte in Tier 1 costs tokens on every turn. Ask:

- Does the agent need this for EVERY response? → Tier 1
- Does the agent need this for THIS session? → Tier 2
- Might the agent need this if asked? → Tier 3
- Is this historical/archival? → Tier 4

**Common Tier 1 contents:**
- Agent identity and personality
- User profile (name, timezone, preferences)
- Key rules and constraints
- Active project summaries (not details)
- Shorthand decoder (acronyms, nicknames)
- Channel/tool configuration summary

### 2. How Does Memory Get Written?

Memory must be written DURING the session, not after. "Mental notes" don't survive restarts.

**Write triggers:**
- New fact learned → append to daily notes
- Decision made → record decision + reasoning
- Task completed → update plans/status
- Pre-compaction → flush everything important to files

**Golden rule:** If it's not written to a file, it doesn't exist after restart.

### 3. How Does Memory Get Searched?

When the agent needs to recall something:

1. **Keyword search** (BM25) — exact matches, names, codes
2. **Semantic search** (vector) — meaning-based, paraphrases
3. **Graph search** (knowledge graph) — relationships, connected entities

See the `hybrid-retrieval` skill for implementation details.

### 4. How Does Memory Get Maintained?

Memory accumulates. Without maintenance, it becomes noise.

**Daily:** Append new entries to daily notes file
**Weekly:** Curate MEMORY.md — promote important learnings, archive stale info
**On compaction:** Flush session state to files before context is lost
**On error:** When the agent gets something wrong, update the source of truth

## Compaction Safety

When context windows fill up, LLMs compact (summarise and drop old turns). This is the #1 memory loss vector.

**Pre-compaction checklist:**
1. ✅ Save current task state (what are we doing?)
2. ✅ Save running processes (PIDs, services)
3. ✅ Save verified facts (what did we confirm with tools?)
4. ✅ Save conversation topics (what were we discussing?)
5. ✅ Save pending decisions (what's waiting for user input?)

**Post-compaction recovery:**
1. Read identity files (who am I?)
2. Read session state (what was I doing?)
3. Read recent conversation transcript (what were we talking about?)
4. Check for active processes (is anything still running?)

## File Organisation

```
workspace/
├── MEMORY.md          # Tier 1: Core knowledge (curated)
├── SESSION-STATE.md   # Tier 2: Current session context
├── memory/
│   ├── YYYY-MM-DD.md  # Tier 2/3: Daily notes (append-only)
│   ├── plans.md       # Tier 2: Active tasks and TODOs
│   ├── people/        # Tier 3: Contact profiles
│   ├── projects/      # Tier 3: Project details
│   ├── rules/         # Tier 1/2: Behaviour rules
│   └── archive/       # Tier 4: Historical snapshots
```

**Key principles:**
- One fact, one place (avoid duplication)
- MEMORY.md is an INDEX that points to details, not a dump of everything
- Daily notes are append-only (never overwrite today's file)
- Archive old daily notes, don't delete them

## Anti-Patterns

1. **Putting everything in the system prompt** — Costs tokens, slows responses, most of it unused
2. **"I'll remember that"** — No you won't. Write it down NOW.
3. **Duplicating facts** — Same info in 3 files = 3 places to update, guaranteed drift
4. **No compaction safety** — Context fills up, everything is lost, agent starts from scratch
5. **Search without write** — A search system with stale data is worse than no search at all
6. **Flat file dump** — 500 files in one directory = impossible to maintain. Use hierarchy.

## Scaling Checklist

| Stage | Users | Approach |
|-------|-------|----------|
| Prototype | 1 | Markdown files + grep |
| Personal agent | 1 | Files + SQLite FTS5 |
| Production | 1-10 | Files + Vector DB + optional KG |
| Multi-agent | 10+ | Shared Vector DB + KG + access controls |

## Output

Help the user:
1. Map their data types to memory tiers
2. Design their file organisation
3. Choose write triggers (when does memory get updated?)
4. Plan compaction safety (what gets saved before context loss?)
5. Select search infrastructure for their scale
6. Set up a maintenance schedule

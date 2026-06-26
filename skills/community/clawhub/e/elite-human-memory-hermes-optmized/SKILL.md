---
name: elite-human-memory-hermes
description: Hermes-optimized human-like memory system with semantic search, auto-promotion, conflict resolution, and direct integration with the Hermes memory tool.
---

# Elite Human Memory — Hermes Optimized

This version is tuned for Hermes. It keeps the human-like, selective, and contextual philosophy while taking advantage of Hermes’ tool ecosystem and vector capabilities.

## Memory Layers

**Working Memory**  
Current conversation only. Transient and not persisted.

**Episodic Memory**  
Daily raw memory files stored at:  
`memory/YYYY-MM-DD.md`

**Semantic Memory**  
Curated long-term memory stored in:  
`MEMORY.md`

**Vector Index** (Hermes-enhanced)  
Embeddings generated from `MEMORY.md` and recent episodic files, stored in:  
`memory/vectors/`

This enables semantic search alongside traditional metadata filtering.

**Conflict Ledger**  
Detected contradictions are logged in:  
`memory/conflicts/`

## Context Schema (Metadata)

Every memory entry should include:

- **When**: Timestamp + recency weight
- **Where**: Channel/context (Telegram, CLI, web, etc.)
- **Why**: Trigger or reason it was recorded
- **State**: `active` | `stale` | `superseded` | `resolved`
- **Scope**: `global` | `project` | `person` | `temporary`
- **Validity**: 
  - `confidence`: high / medium / low
  - `last_verified`: date
  - `expires`: optional date
- **Related**: Links to other memories, people, or projects
- **Source**: Path + line number (for traceability)

## Auto-Promotion Heuristics

The agent should evaluate daily memory entries for promotion using the following weighted signals:

**Strong signals (high weight):**
- Explicitly referenced by the user in later conversations
- Repeated across 3+ days or sessions
- Tied to a core project, goal, or person
- User corrects or reinforces the memory

**Supporting signals (medium weight):**
- High confidence rating
- Clear future utility
- Related to an active decision or preference

**Promotion Rules:**
- If 2+ strong signals → Propose promotion
- If 1 strong + 2 supporting signals → Propose promotion
- If only supporting signals → Log for weekly review only

**User Control:**
- Default behavior: Always propose before promoting
- Optional mode: `auto_promote = true` (for trusted, low-risk memories)

## Conflict Detection & Resolution

When two memories contain contradictory information, the agent should:

1. **Detect** the conflict during write or weekly maintenance.
2. **Log** it in `memory/conflicts/` with:
   - Both conflicting statements
   - Context and sources
   - Severity (high / medium / low)
3. **Resolve** using one of these methods:
   - Ask the user for clarification
   - Propose a resolution with reasoning
   - Auto-resolve low-severity conflicts with a note (e.g. “Temporarily preferred X over Y”)

All resolutions must update the `State` field of the affected memories and record the decision in the conflict log.

## Retrieval Strategy

When the user asks about history, decisions, preferences, or past context, the agent should follow this order:

1. **Semantic Search** (Primary)  
   Query the vector index over `MEMORY.md` and recent daily files for relevant memories.

2. **Metadata Filtering** (Secondary)  
   Apply filters on scope, state, confidence, date, and related entities.

3. **Hermes Memory Tool Integration**  
   Also query the built-in Hermes `memory` tool to surface any simple key-value facts stored there.

4. **Response Guidelines**  
   - Use natural confidence language  
   - Mention if a memory may be stale or conflicting  
   - Include `Source:` references when helpful

## Hermes Integration

This skill is designed to work **alongside** the existing Hermes `memory` tool:

- Use this system for rich, contextual, human-style memory
- Use the Hermes `memory` tool for simple, high-frequency key-value facts
- Both systems can reference each other when relevant

## Behavioral Triggers

**Auto-read memory when:**
- User asks about past decisions, preferences, people, projects, or dates
- The current context feels incomplete or contradictory

**Auto-write memory when:**
- User gives explicit “remember this” instructions
- Clear decisions or repeated preferences appear
- New long-running context is established

**Auto-maintenance:**
- Weekly review (can be manually triggered or scheduled)

## Storage Layout

```
memory/
├── YYYY-MM-DD.md              # Episodic / daily memory
├── conflicts/
│   └── YYYY-MM-DD.md          # Conflict logs and resolutions
├── MEMORY.md                  # Curated long-term semantic memory
└── vectors/                   # Embeddings for semantic search
```

## Notes

- This skill is optimized for Hermes and makes full use of its tool ecosystem.
- Vector search significantly improves retrieval quality over pure keyword/metadata search.
- Auto-promotion and conflict detection reduce manual maintenance burden while keeping the user in control.

---

**Version:** 2.0.0 (Hermes Optimized)  
**Status:** Ready for local use and marketplace publishing.
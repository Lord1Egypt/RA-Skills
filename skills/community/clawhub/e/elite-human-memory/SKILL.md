---
name: elite-human-memory
description: Portable Clawhub-compatible human-like memory system with layered storage (Working/Episodic/Semantic + optional Vector index), rich metadata schema, auto-promotion heuristics, conflict detection & resolution, and semantic retrieval. Platform-agnostic design suitable for publishing and multi-agent use.
---

# Elite Human Memory — Portable Edition

This version prioritizes broad compatibility and portability. It preserves the human-like, selective, and contextual philosophy while avoiding tight coupling to any single agent framework. Ideal for Clawhub, custom agents, or cross-platform deployments.

## Memory Layers

**Working Memory**  
Current conversation only. Transient and not persisted beyond the session.

**Episodic Memory**  
Daily raw memory files stored at:  
`memory/daily/YYYY-MM-DD.md` (or user-configurable path)

**Semantic Memory**  
Curated long-term memory stored in:  
`memory/MEMORY.md`

**Vector Index** (Optional / Portable)  
Embeddings generated from `MEMORY.md` and recent episodic files.  
Can be implemented with any vector database (Chroma, FAISS, LanceDB, or even a simple embedding cache).  
Stored in: `memory/vectors/` or external vector store.

This enables semantic search alongside traditional metadata filtering. If no vector capability is available, fall back to keyword + metadata search.

**Conflict Ledger**  
Detected contradictions are logged in:  
`memory/conflicts/`

## Context Schema (Metadata)

Every memory entry should include:

- **When**: Timestamp + recency weight
- **Where**: Channel/context (Telegram, CLI, web, Discord, etc.)
- **Why**: Trigger or reason it was recorded
- **State**: `active` | `stale` | `superseded` | `resolved`
- **Scope**: `global` | `project` | `person` | `temporary`
- **Validity**: 
  - `confidence`: high / medium / low
  - `last_verified`: date
  - `expires`: optional date
- **Related**: Links to other memories, people, or projects
- **Source**: Path + line number or reference (for traceability)

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
   Query the vector index (or embedding similarity) over `MEMORY.md` and recent daily files for relevant memories.

2. **Metadata Filtering** (Secondary)  
   Apply filters on scope, state, confidence, date, and related entities.

3. **Keyword / Full-text Fallback**  
   Traditional search when vector capabilities are unavailable.

4. **Response Guidelines**  
   - Use natural confidence language  
   - Mention if a memory may be stale or conflicting  
   - Include `Source:` references when helpful

## Platform Integration Notes

This skill is designed to be **framework-agnostic**:

- Use file system operations for storage and retrieval
- Integrate with any available embedding model or vector store for semantic search
- Can coexist with simpler key-value memory systems (map rich contextual memory here, simple facts elsewhere)
- Works in Hermes, Clawhub-published agents, LangChain, AutoGen, or custom loops

## Behavioral Triggers

**Auto-read memory when:**
- User asks about past decisions, preferences, people, projects, or dates
- The current context feels incomplete or contradictory

**Auto-write memory when:**
- User gives explicit “remember this” instructions
- Clear decisions or repeated preferences appear
- New long-running context is established

**Auto-maintenance:**
- Weekly review (can be manually triggered or scheduled via cron/agent loop)

## Storage Layout (Example)

```
memory/
├── daily/
│   └── YYYY-MM-DD.md              # Episodic / daily memory
├── conflicts/
│   └── YYYY-MM-DD.md              # Conflict logs and resolutions
├── MEMORY.md                      # Curated long-term semantic memory
└── vectors/                       # Optional embeddings (or use external DB)
```

Paths are examples — make them configurable for the target environment.

## Notes

- This skill is optimized for portability and easy publishing on Clawhub.
- Vector search (when available) significantly improves retrieval quality.
- Auto-promotion and conflict detection reduce manual maintenance burden while keeping the user in control.
- No hard dependencies on proprietary tools or specific runtimes.

See `references/two-track-approach.md` for the parallel Hermes-optimized vs portable versioning strategy used in this skill family.

---

**Version:** 1.0.0 (Portable / Clawhub Compatible)  
**Status:** Ready for publishing and cross-platform use
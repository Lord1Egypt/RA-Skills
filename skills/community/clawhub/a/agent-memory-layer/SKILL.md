---
name: agent-memory-layer
description: Scalable memory system for AI agents with short-term, long-term, and episodic memory. Use when building agent memory persistence, conversation context management, knowledge retrieval, or episodic recall. Covers Redis-backed short-term memory, vector-based long-term memory, and timeline-ordered episodic memory with decay and consolidation.
---

# Agent Memory Layer

Three-tier memory system for AI agents: short-term, long-term, and episodic.

## Quick Start

```python
from memory_layer import AgentMemory

mem = AgentMemory(agent_id="my-agent")
mem.short_term.add("User prefers dark mode", priority=0.8)
mem.long_term.store("Project uses React + TypeScript", tags=["tech", "project"])
mem.episodic.record("Debugged auth bug", outcome="success", duration_min=15)

# Recall
context = mem.short_term.recall(limit=10)
relevant = mem.long_term.search("frontend framework")
similar = mem.episodic.find_similar("debugging session")
```

## Architecture

```
┌─────────────────────────────────────────┐
│            Agent Memory                  │
├───────────┬───────────┬─────────────────┤
│ Short-Term│ Long-Term │   Episodic      │
│ (Redis)   │ (Vectors) │  (Timeline)     │
│ TTL: 1hr  │ Permanent │ Decay: 30d      │
│ Hot cache │ Semantic  │ Consolidated    │
└───────────┴───────────┴─────────────────┘
```

## Memory Tiers

### Short-Term (Working Memory)
- Recent context, active conversation, current task state
- TTL-based expiry (default 1 hour)
- Priority-weighted retention
- See `references/short-term.md`

### Long-Term (Knowledge)
- Persistent facts, preferences, learned patterns
- Vector similarity search for retrieval
- Tags and metadata for filtering
- See `references/long-term.md`

### Episodic (Experience)
- Timeline-ordered events with outcomes
- Decay function reduces old episode weight
- Consolidation moves recurring patterns to long-term
- See `references/episodic.md`

## Consolidation

Episodic memories that recur are automatically promoted to long-term:
- If the same outcome occurs 3+ times → store as learned pattern
- Failed approaches get negative weight in long-term
- See `scripts/consolidate.py`

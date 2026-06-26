# Integration Guide — Elite Human Memory (Hermes)

This document covers how to integrate the skill with Hermes agents, including tool usage, memory layout, and behavioral triggers.

## Hermes Memory Tool Relationship

This skill is designed to **complement**, not replace, the built-in Hermes `memory` tool:

- Use the Hermes `memory` tool for simple, high-frequency key-value facts (e.g. “user prefers concise responses”).
- Use this skill for rich, contextual, human-style memory (projects, decisions, people, long-term preferences).
- Both systems can reference each other when relevant.

## Storage Layout (Expected by the Skill)

```
memory/
├── YYYY-MM-DD.md              # Episodic / daily memory
├── conflicts/
│   └── YYYY-MM-DD.md          # Conflict logs and resolutions
├── MEMORY.md                  # Curated long-term semantic memory
└── vectors/                   # Embeddings for semantic search
```

The skill expects this structure to exist or will create it as needed.

## Behavioral Triggers

**Auto-read memory when:**
- User asks about past decisions, preferences, people, projects, or dates
- The current context feels incomplete or contradictory

**Auto-write memory when:**
- User gives explicit “remember this” instructions
- Clear decisions or repeated preferences appear
- New long-running context is established

**Auto-maintenance:**
- Weekly review (can be manually triggered or scheduled via cron)

## Recommended Agent Configuration

When loading this skill, also ensure the agent has access to:

- The core Hermes `memory` tool
- File read/write capabilities for the `memory/` directory
- Vector embedding generation (if using a local embedding model)

## Example Usage Patterns

### Semantic Retrieval
When the user says “What did we decide about the memory skill last month?”, the agent should:
1. Run semantic search over `MEMORY.md` + recent daily files
2. Apply metadata filters (scope, state, confidence)
3. Cross-reference with the Hermes `memory` tool if needed
4. Return results with natural confidence language and source references

### Promotion Workflow
The agent evaluates daily memory entries using the weighted signals defined in `SKILL.md`. Strong signals trigger a proposal to the user before promotion.

### Conflict Handling
When contradictory information is detected, the agent logs it to `memory/conflicts/` and either asks the user or proposes a resolution.

## Notes for Marketplace Users

- This skill was developed and tested inside a Hermes-Lovecraft instance.
- It makes heavy use of Hermes’ tool ecosystem (especially the `memory` tool and vector capabilities).
- Vector search significantly improves retrieval quality over pure keyword/metadata search.

For the core behavioral rules and full specification, see `SKILL.md`.
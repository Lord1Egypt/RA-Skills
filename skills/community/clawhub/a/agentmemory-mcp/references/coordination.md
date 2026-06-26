# agentmemory + MEMORY.md Coordination Guide

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                  OpenClaw Memory System                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌───────────────────────┐  ┌────────────────────────┐ │
│  │   agentmemory (MCP)    │  │    MEMORY.md / AGENTS  │ │
│  │                       │  │                        │ │
│  │  • Auto-capture       │  │  • Curated rules       │ │
│  │  • Semantic search    │  │  • Preferences         │ │
│  │  • 95.2% R@5          │  │  • Manual updates      │ │
│  │  • Cross-agent        │  │  • Human-readable      │ │
│  │  • Session sync       │  │  • Survives compaction │ │
│  └───────────────────────┘  └────────────────────────┘ │
│            │                        │                   │
│            └────────┬───────────────┘                   │
│                     ▼                                   │
│           ┌─────────────────┐                          │
│           │  OpenClaw Agent  │                          │
│           └─────────────────┘                          │
└─────────────────────────────────────────────────────────┘
```

## Layer Responsibilities

| Layer | Tool | What's stored | Management |
|-------|------|--------------|------------|
| **Experience** | agentmemory | Tasks, decisions, results, observations | Automatic |
| **Knowledge** | MEMORY.md | Rules, preferences, long-term facts | Manual |
| **Daily** | memory/YYYY-MM-DD.md | Session logs, events | Automatic |

---

## Agent Behavior Guidelines

### Session Start

1. **MEMORY.md + daily logs** → loaded automatically by OpenClaw
2. **agentmemory** → agent can call `memory_recall` for additional context
3. No conflict — both systems serve different purposes

### During Work

- **Task decision**: Call `memory_smart_search` to check if similar task was done
- **Success**: Call `memory_save` with result, e.g.:
  ```
  memory_save("Deployed backend to Railway, took 8 minutes", 
    type="observation", tags=["deployment"])
  ```
- **Failure**: Call `memory_save` noting what didn't work

### Session End

- OpenClaw auto-captures conversation via `plugins.slots.memory`
- Critical learnings → also write to MEMORY.md (persists beyond compaction)

---

## Migration from Existing MEMORY.md

If MEMORY.md has valuable content, migrate selectively:

```bash
# Start server first
npx @agentmemory/agentmemory

# In another terminal, import MEMORY.md
npx @agentmemory/agentmemory migrate --from-file ~/.openclaw/workspace/MEMORY.md
```

Or use `memory_import` in batches:

```javascript
// Example: Migrate section by section
memory_import([
  { content: "Backend deployed via Railway CLI", type: "observation", tags: ["deployment"] },
  { content: "User prefers brief responses", type: "preference", tags: ["communication"] }
], strategy: "merge")
```

---

## Conflict Resolution

**Q: What if agentmemory says something different from MEMORY.md?**

| Scenario | Resolution |
|----------|------------|
| MEMORY.md has rule, agentmemory has conflicting experience | Trust MEMORY.md (curated), log conflict in agentmemory |
| agentmemory has newer info | Update MEMORY.md if verified |
| Uncertainty | Log to agentmemory, keep both until resolved |

**Principle**: MEMORY.md is source of truth for rules; agentmemory is evidence of experience.

---

## Maintenance

### Periodic (monthly)

1. Read `memory_stats()` output
2. Check for gaps with `memory_analyze("gaps")`
3. Review MEMORY.md for outdated entries

### When Conflicting

```bash
# View memory for specific topic
memory_timeline(tag="deployment", limit=10)

# Check provenance
memory_trace(id="<memory-id>")

# Update or correct
memory_update(id="<memory-id>", content="corrected information")
```

---

## Optimal Configuration

For maximum capability, run both systems:

1. **agentmemory MCP** — handles automatic capture, semantic search, cross-agent sharing
2. **MEMORY.md** — handles curated rules, preferences, compliance requirements

The agent uses whichever is appropriate for the situation — no forced preference.
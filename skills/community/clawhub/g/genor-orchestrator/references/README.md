# Full Reference Documentation

This file is a merged reference from what was previously the README.md. Read sections as needed.

---

## Table of Contents
1. [Data Directory Structure](#data-directory-structure)
2. [File Naming Conventions](#file-naming-conventions)
3. [Model Routing](#model-routing)
4. [Design Grilling Details](#design-grilling-details)
5. [CONTEXT.md Rules](#contextmd-rules)
6. [ADR Criteria](#adr-criteria)

---

## Data Directory Structure

```
orchestrator-data/
├── models.json           — Model inventory
├── session_log.md        — Session run history
├── price_changes.log     — Price change history
├── MODEL_CATALOG.md      — Generated model catalog
├── projects/             — Per-project data
│   └── <project>/
│       └── sessions.json
└── sessions/             — Detailed session state files
```

Override location: `export ORCHESTRATOR_DATA_DIR=/path/to/data`

---

## File Naming Conventions

| Location | Format | Example |
|----------|--------|---------|
| `sessions/` | `YYYY-MM-DD-HHMM-<project>-<task-slug>.md` | `2026-06-08-1134-myapp-deploy-auth.md` |
| `projects/<project>/sessions.json` | JSON array | — |
| `session_log.md` | Flat table (append-only) | — |
| `models.json` | JSON inventory | — |
| `price_changes.log` | Flat log (append-only) | — |
| `.planning/ADRs/` | `YYYY-MM-DD-<title-slug>.md` | `2026-06-08-use-postgres.md` |

---

## Model Routing

Model selection depends on: task type, model availability, cost constraints.

### Routing Table

| Task Type | Primary | Fallback 1 | Fallback 2 | Last Resort |
|-----------|---------|------------|------------|-------------|
| Heavy coding | Best available | ACP agent | Fast cloud | Local |
| Quick edits | Fast cloud | Free tier | Local | Small local |
| Deep research | Best reasoning | Free tier | Local | Fast cloud |
| Quick lookup | Fast cloud | Free tier | Small free | Local |
| Creative writing | Creative local | Cloud | Best reasoning | Fast |
| Planning / design | Best reasoning | Local | Fast cloud | Free tier |
| Cleanup / org | Free tier | Fast cloud | Local | Small local |
| Vision | Cloud vision | Local | Laptop | Describe |
| Heavy reasoning | Best reasoning | Local | Fast cloud | Creative local |
| Documentation | Small free | Fast cloud | Local | Small local |

See `ROUTING.md` for the current specific routing table. See `orchestrator-data/MODEL_CATALOG.md` for full model inventory.

### Cost Awareness
- **Free tier first**: free models, local models
- **Subscription**: use within limits
- **Pay-per-token**: use sparingly
- **Last resort**: depleting funds — avoid

---

## Design Grilling Details

### When to Grill
Before any significant architectural work. Mandatory for:
- New projects or major features
- Database schema changes
- API design decisions
- Any decision that is hard to reverse

### Grilling Protocol
1. **Interview relentlessly** — Ask one question at a time, wait for feedback
2. **Challenge the glossary** — If user uses a term that conflicts with existing CONTEXT.md, call it out
3. **Sharpen fuzzy language** — Propose precise canonical terms for vague/overloaded words
4. **Discuss concrete scenarios** — Stress-test domain relationships with edge cases
5. **Cross-reference with code** — Check if code agrees with stated design; surface contradictions
6. **Update CONTEXT.md inline** — Capture resolved terms immediately, not in batches

### After the Session
Generate:
1. **CONTEXT.md** — domain glossary with resolved terms
2. **ADR files** — `.planning/ADRs/YYYY-MM-DD-<title-slug>.md` for qualifying decisions
3. **Summary** — what was decided and what remains open

### File Structure
```
~/projects/<name>/
├── CONTEXT.md              ← domain glossary
├── .planning/
│   ├── CONFIG.md
│   ├── STATE.md
│   ├── ROADMAP.md
│   └── ADRs/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If `CONTEXT-MAP.md` exists at root, the repo has multiple contexts — the map points to each one.

---

## CONTEXT.md Rules
- **Totally devoid of implementation details** — glossary only, not a spec or scratch pad
- Organized by concept
- Create lazily — only when there's something to write

---

## ADR Criteria
All three must be true to write an ADR:
1. **Hard to reverse** — cost of changing mind later is meaningful
2. **Surprising without context** — future reader will wonder "why?"
3. **Real trade-off** — genuine alternatives were considered

If any criterion is missing, skip the ADR.

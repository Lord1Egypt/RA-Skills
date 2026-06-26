# Context Workflow (Step 3 Content)

> **Role**: Pipeline's "specific work content" layer
> **Use Case**: Long tasks, context management, memory management
> **Load Time**: Pipeline Step 2 execution
> **Combination**: Pipeline + context

---

## Relationship

```
Pipeline (method)       context (content)
──────────────────────────────────────────
Step 1: Plan     ←→   Context Assessment
Step 2: Execute  ←→   Compression Strategy
Step 3: Summarize←→   Build Snapshot
Step 4: Check    ←→   Verify Coherence
```

---

## 4-Step Compression Flow

### Step 1 — Context Assessment (Pipeline Plan)

**Question**: Current context state?

**Assessment Metrics**:
- Message count
- Context utilization rate
- Distance to overflow

**Assessment Template**:
```markdown
## Context Assessment

### Status
- Messages: {N}
- Utilization: {X%}
- Distance to overflow: {Y} turns

### Compressible Parts
- Redundant discussions: {N1}
- Duplicate outputs: {N2}
```

### Step 2 — Compression Strategy (Pipeline Execute)

**Decision Matrix**:
| Utilization | Strategy |
|-------------|----------|
| < 50% | Don't compress |
| 50-70% | Gradual compression |
| 70-90% | Early compression |
| > 90% | Force compression |

**Compression Operations**:
```markdown
### Keep
- Task goal
- User preferences
- Key decisions

### Discard
- Redundant discussions
- Duplicate outputs
- Resolved reasoning
```

### Step 3 — Build Snapshot (Pipeline Summarize)

**Question**: How to record compression results?

**Snapshot Template**:
```markdown
## Task Snapshot @ {Time}

### Task Goal
{Goal}

### Completed
- {Item 1}
- {Item 2}

### In Progress
- {Current Item}

### Key Context
- {Must-remember facts}
```

### Step 4 — Verification (Pipeline Check)

**Question**: Is task still coherent after compression?

**Checklist**:
- [ ] Task goal clear
- [ ] History traceable
- [ ] Current step clear

---

_Last updated: 2026-04-07 by neltharion11 | https://github.com/neltharion11/skill-agent-harness_

# Decision Tree (Layer 1)

> **Role**: Decide "what combination to use"
> **Load Time**: Step 1

---

## Quick Decision

```
What type of task is this?
│
├─ Simple Q&A? ─── → Direct answer, no framework needed
│
├─ Need to gather requirements? ─── → Inversion (clarify first)
│
└─ Need multi-step execution?
    │
    └─ Yes ──→ Pipeline + specific WORKFLOW
              │
              ├─ Research task? ─── → + research
              ├─ Coordination task? ─── → + subagent
              ├─ Compression task? ─── → + context
              └─ Analysis task? ─── → + analysis
```

---

## Decision Table

| Task | Combination | Description |
|------|-------------|-------------|
| Deep Research Report | **Pipeline + research** | Multi-step research flow |
| Multi-Agent Coordination | **Pipeline + subagent** | Decompose+parallel+merge |
| Long-Task Compression | **Pipeline + context** | Context management |
| Competitive/Multi-Dim Analysis | **Pipeline + analysis** | Comparison & evaluation |
| Unclear Requirements | Inversion | Gather information first |

---

## Decision Examples

### Example 1

**Task**: "Research AI Agent market trends"
```
Decision Process:
1. Multi-step? → Yes
2. Specific type? → Research
3. Combination: Pipeline + research
```

### Example 2

**Task**: "Analyze the competitive landscape of three products simultaneously"
```
Decision Process:
1. Multi-step? → Yes
2. Specific type? → Analysis
3. Combination: Pipeline + analysis
```

---

_Last updated: 2026-04-07 by neltharion11 | https://github.com/neltharion11/skill-agent-harness_

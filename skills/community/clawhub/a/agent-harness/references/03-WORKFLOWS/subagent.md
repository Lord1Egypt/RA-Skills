# Subagent Workflow (Step 3 Content)

> **Role**: Pipeline's "specific work content" layer
> **Use Case**: Task decomposition, multi-agent, parallel execution, coordination
> **Load Time**: Pipeline Step 2 execution
> **Combination**: Pipeline + subagent

---

## Relationship

```
Pipeline (method)       subagent (content)
──────────────────────────────────────────
Step 1: Plan     ←→   Task Analysis
Step 2: Execute  ←→   Launch Sub-Agents
Step 3: Summarize←→   Result Merging
Step 4: Check    ←→   Quality Verification
```

---

## 4-Step Coordination Flow

### Step 1 — Task Analysis (Pipeline Plan)

**Question**: Can the task be decomposed?

**Analysis Dimensions**:
1. Complexity: >5 steps?
2. Parallelism: Can run independently?
3. Specialization: Need multiple fields?

**Decision**: Single Agent vs Multi-Agent coordination

---

### Step 2 — Task Decomposition (Pipeline Execute)

**Question**: How to decompose?

**Decomposition Principles**:
| Principle | Description |
|-----------|-------------|
| **Independence** | Sub-tasks have no dependencies, can run independently |
| **Completeness** | Cover the entire scope |
| **Granularity** | Not too fine (Agent overhead), not too coarse (lose parallel value) |

**Output**:
```markdown
## Task Decomposition

### Main Task
{Main Task}

### Sub-tasks
1. **[Agent-A]**: {Description} → Output: {Format}
2. **[Agent-B]**: {Description} → Output: {Format}
3. **[Agent-C]**: {Description} → Output: {Format}
```

---

### Step 3 — Parallel Execution (Pipeline Summarize)

**Question**: How to coordinate multiple sub-agents?

**OpenClaw API**:
```markdown
Launch Sub-Agent:
sessions_spawn({
  task: "{Task Description}",
  runtime: "subagent",
  mode: "run",
  cleanup: "delete"   // Delete after use, keep session clean
})

Wait for Results:
sessions_yield()   // Pause, wait for sub-agent push
                  // Each sub-agent completion triggers an event
                  // Can yield multiple times, wait for all sub-agents
```

**Execution Example** (3 sub-agents in parallel):
```markdown
1. sessions_spawn → Agent-A
2. sessions_spawn → Agent-B
3. sessions_spawn → Agent-C
4. sessions_yield → Wait for push
   ← Agent-A result comes back
5. sessions_yield → Continue waiting
   ← Agent-B result comes back
6. sessions_yield → Continue waiting
   ← Agent-C result comes back
(All sub-agents complete)
```

**⚠️ Push Mechanism**:
- Sub-Agents **do not** need to call sessions_send to push results
- OpenClaw has built-in `subagent_announce` mechanism: sub-agents auto-push via completion event
- Each sub-agent completion triggers an event push to parent session

---

### Step 4 — Result Merging (Pipeline Check)

**Question**: How to merge results?

**Merging Strategies**:
| Strategy | Use Case |
|----------|----------|
| Sequential merge | Timeline tasks |
| Categorical aggregation | Multi-dimensional tasks (take each dimension result) |
| Comprehensive judgment | Selection tasks (summarize each perspective's conclusion) |

**Output**:
```markdown
## Result Merging

### Sub-task Results
- Agent-A: {Result}
- Agent-B: {Result}
- Agent-C: {Result}

### Comprehensive Conclusion
{Final Output}
```

---

## Quick Execution Checklist

```
subagent Quick Execution Checklist:
□ Load 03-WORKFLOWS/subagent.md
□ Confirm task is decomposable and worth decomposing
□ Decompose into 2-N independent sub-tasks
□ Call sessions_spawn for each sub-task
□ Call sessions_yield to wait for results (can be multiple)
□ Collect all results, merge and output
□ Execute Pipeline Step 4 (Template) + Step 5 (Quality Check)
```

---

## ⚠️ Complete Output Solution (Important Engineering Discovery)

**Problem**: Completion event push content gets truncated/summarized by OpenClaw formatting layer, users can't see full raw output.

**Recommended Solution: Sub-Agent Writes File + Parent Agent Notifies**

```markdown
Sub-Agent Prompt Design:
1. Execute task (research/analyze/code/etc.)
2. Save complete output to file: {user workspace}/subagent_reports/{taskname}_{timestamp}.md
3. sessions_send notify parent "report saved, file path: xxx"
   (if sessions_send fails, ignore, doesn't affect main flow)
4. sessions_yield to end

Parent Agent after receiving notification:
- Confirm file exists
- Tell user file path in conversation
- User reads full file themselves
```

**File Path Convention**:
```
{user configured workspace}/subagent_reports/
├── {taskname}_{YYYYMMDD_HHMM}.md
├── AI_Agent_Research_20260407_2156.md
└── ...
```

> Actual path configured by user in TOOLS.md (e.g., `D:/subagent_reports/` or other directory)

**Why Not sessions_send**:
- Sub-Agent calling sessions_send sometimes fails (tool call limitations)
- Parent reading history adds extra token consumption
- File write solution is most stable, user can read anytime

---

## Test Verification Records

| Test | Result | Description |
|------|--------|-------------|
| Parallel 3 Sub-Agents | ✅ Success | Each runs independently, push normal |
| sessions_yield Multiple Wake | ✅ Success | Each sub-agent completion triggers event |
| Push Mechanism | ✅ via subagent_announce | No need for sub-agent to call sessions_send |
| Write File + sessions_send | ✅ Success | Full report written to file, sessions_send optional |
| runTimeoutSeconds=0 | ✅ Valid | No time limit, sub-agent runs to completion |
| session mode + thread=true | ❌ Not supported by Feishu | channel plugin not registered relevant hook |

---

_Last updated: 2026-04-07 by neltharion11 | https://github.com/neltharion11/skill-agent-harness_

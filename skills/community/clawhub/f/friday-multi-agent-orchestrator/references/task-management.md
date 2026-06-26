# Task Management — Multi-Agent Team

## Three-Layer Task System

### Layer 1: Strategic (CEO/Human)
- Goals, OKRs, quarterly milestones
- **Owner**: Human or CEO Agent
- **Cadence**: Weekly review, monthly planning
- **Format**: Plain markdown in shared workspace

### Layer 2: Tactical (PM/Coordinator)
- Sprint planning, task allocation, progress tracking
- **Owner**: PM Agent
- **Cadence**: Daily standup, weekly sprint review
- **Format**: Kanban board (markdown table)

```markdown
| ID | Task | Owner | Status | Priority | Due | Blocker |
|----|------|-------|--------|----------|-----|---------|
| T1 | Build auth module | Otto | 🔄 In Progress | P0 | 03-25 | None |
| T2 | Write API docs | Irene | 📋 Todo | P1 | 03-27 | T1 |
| T3 | Design landing page | Don | ✅ Done | P2 | 03-22 | - |
```

### Layer 3: Operational (Engineers)
- Individual tickets, code changes, deliverables
- **Owner**: Individual agents
- **Cadence**: Per-task, commit-based
- **Format**: Checkbox list in agent workspace

## Task Lifecycle

```
📋 Todo → 🔄 In Progress → 🔍 Review → ✅ Done
                  ↓
              ⚠️ Blocked (needs escalation)
```

## Escalation Rules

| Condition | Action | Escalate To |
|-----------|--------|-------------|
| Agent blocked > 30 min | Notify PM | PM Agent |
| PM can't resolve > 1 hr | Notify CEO | Human / CEO Agent |
| Critical bug in production | Immediate alert | All + Human |
| Conflict between agents | CEO Agent mediates | CEO Agent |
| Agent unresponsive > 2 heartbeat cycles | Mark offline, reassign | PM Agent |

## Report Format

### Daily Standup (each agent → PM)

```markdown
【Agent Name】日期报告
时间：YYYY-MM-DD HH:MM
类型：日报/周报

昨日完成：
- [x] Task A (result summary)

今日计划：
- [ ] Task B (approach)
- [ ] Task C (approach)

阻塞项：
- Need input from X on Y

风险项：
- Z might delay Task D by 1 day
```

### Weekly Summary (PM → CEO)

```markdown
【团队周报】YYYY-MM-DD ~ YYYY-MM-DD

目标完成率：X/Y (Z%)

里程碑：
- ✅ M1: Description (completed DD)
- 🔄 M2: Description (X% complete)
- 📋 M3: Description (planned DD)

风险与阻塞：
1. Risk description → mitigation plan

资源需求：
- Need additional agent for X
- Need human decision on Y

下周重点：
1. Priority 1
2. Priority 2
```

## Priority Matrix

| Priority | Response Time | Examples | Who Can Assign |
|----------|:------------:|----------|---------------|
| **P0 Critical** | < 15 min | Production down, data loss | Human only |
| **P1 High** | < 2 hr | Blocker for other agents, deadline today | PM + Human |
| **P2 Medium** | < 1 day | Normal sprint tasks | PM |
| **P3 Low** | Next sprint | Nice-to-haves, improvements | Any agent |

## Conflict Resolution

When two agents have conflicting priorities:

1. **Agent-level conflict**: PM Agent mediates using priority matrix
2. **Resource conflict** (two agents need same input): PM sequences with time blocks
3. **Goal conflict**: Escalate to Human — agents never override human intent
4. **Deadlock**: Human makes final call within 24 hours

## Anti-Pattern: Task Thrashing

**Symptoms**: Agent constantly switches tasks, nothing ships

**Root causes**:
- Too many P1s (everything is urgent = nothing is urgent)
- Unclear ownership (two agents think they own the same task)
- Missing acceptance criteria (agent doesn't know when "done")

**Fix**: PM Agent enforces:
- Max 3 P1 tasks across entire team at any time
- One owner per task, no shared ownership
- Every task has measurable acceptance criteria before assignment

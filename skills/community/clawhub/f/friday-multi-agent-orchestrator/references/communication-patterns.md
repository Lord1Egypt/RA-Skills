# Communication Patterns

Inter-agent communication protocols. Choose patterns based on latency needs and team complexity.

## Pattern Selection Guide

| Need | Recommended Pattern |
|------|-------------------|
| Hand off a document for review | Shared directory |
| Coordinate on a task in real-time | Message passing |
| Check if agent is alive/healthy | Heartbeat |
| Chain 3+ agents sequentially | Event queue |
| Broadcast announcement to all | Shared directory + notification |

---

## Pattern 1: Shared Directory (Async)

The simplest and most reliable pattern. Agents read/write files in a shared workspace.

### Directory Structure

```
shared/
├── inbox/                    # Messages TO this agent
│   ├── pm/                   # From PM
│   │   └── task-001.md
│   ├── analyst/              # From Analyst
│   └── ceo/                  # From CEO
├── outbox/                   # Messages FROM this agent
│   ├── pm/
│   ├── ceo/
│   └── writer/
├── tasks/                    # Shared task board
│   ├── active/
│   ├── completed/
│   └── backlog/
├── knowledge/                # Shared knowledge base
│   ├── decisions/
│   ├── learnings/
│   └── reference/
└── reports/                  # Status and analysis reports
    ├── daily/
    └── weekly/
```

### Message Format

```markdown
---
from: pm
to: engineer
timestamp: 2026-03-24T11:40:00+08:00
type: task-assignment | status-update | request | escalation
priority: critical | high | normal | low
task-id: TASK-001
---

## Task: Implement user authentication

### Acceptance Criteria
- [ ] Login endpoint with JWT
- [ ] Password hashing with bcrypt
- [ ] Rate limiting on auth endpoints
- [ ] Unit tests with >90% coverage

### Context
Part of Sprint 3. Dependencies: None. Blocks: TASK-005.

### Deadline
2026-03-26 18:00

### Questions?
Reply in outbox/pm/ with subject prefix [TASK-001]
```

### When to Use
- Document-heavy workflows (reports, specs, content)
- Teams with 3+ agents
- When agents run on different schedules
- Any workflow needing an audit trail

### When Not to Use
- Real-time collaboration needed (latency too high)
- Very large files (use references instead)

---

## Pattern 2: Message Passing (Real-Time)

Direct agent-to-agent messaging via platform APIs.

### OpenClaw: sessions_send

```bash
# PM assigns task to Engineer
openclaw sessions send --to engineer --message "New task: implement auth. See shared/tasks/active/TASK-001.md"

# Engineer reports completion
openclaw sessions send --to pm --message "TASK-001 complete. PR: #42. Ready for review."
```

### Claude Code: File-based signaling

```bash
# Create a signal file
echo '{"from":"pm","to":"engineer","action":"new_task","ref":"TASK-001.md"}' > .signals/pending/engineer.json

# Engineer reads and processes signals
# After processing, move to .signals/processed/
```

### Codex/Cursor: Workspace comments

```bash
# Leave a comment in the shared task file
# Agent reads file, sees comment, acts on it
```

### When to Use
- Immediate response needed (< 30 seconds)
- Quick clarifications during active work
- Escalation that can't wait for async cycle
- Two-agent handoff coordination

### When Not to Use
- Complex information (use shared directory)
- Broadcast to many agents (use shared directory)
- When the receiving agent may be offline

---

## Pattern 3: Heartbeat Scheduling (Periodic)

Scheduled check-ins for monitoring and health assessment.

### Cron Configuration

```bash
# Monitor agent checks team health every 2 hours
0 */2 * * * openclaw cron run monitor-health-check

# CEO agent reviews daily status every morning
0 8 * * * openclaw cron run ceo-morning-review

# PM agent checks deadline proximity every hour
0 * * * * openclaw cron run pm-deadline-check
```

### Health Check Output

```markdown
## Team Health Report
Generated: 2026-03-24 14:00

### Agent Status
| Agent | Last Active | Tasks | Status |
|-------|-------------|-------|--------|
| CEO | 13:30 | 0 | 🟢 Idle |
| PM | 13:55 | 3 active | 🟢 Active |
| Engineer | 14:02 | 1 active | 🟢 Active |
| Analyst | 12:30 | 0 | 🟡 Quiet (2h) |
| Monitor | 14:00 | Running | 🟢 Active |

### Deadline Alerts
- TASK-003: Due in 4 hours, 60% complete — 🟡

### System Health
- Shared directory: ✅ Accessible
- Message queue: ✅ Clear
- Knowledge base: ✅ Synced
```

### When to Use
- Monitoring agent operations
- Ensuring no agent goes silent unexpectedly
- Periodic status collection for reporting
- Automated alerts on missed deadlines

---

## Pattern 4: Event Queue (Workflow Chains)

Sequential or parallel agent workflows triggered by events.

### Implementation: File-based Event Queue

```
shared/
└── events/
    ├── queue/          # Pending events
    ├── processing/     # Currently being handled
    ├── completed/      # Finished events
    └── failed/         # Failed events (for retry)
```

### Event Format

```json
{
  "event_id": "EVT-001",
  "type": "task.completed",
  "source": "engineer",
  "timestamp": "2026-03-24T14:00:00+08:00",
  "data": {
    "task_id": "TASK-001",
    "output": "shared/reports/engineer/TASK-001-report.md"
  },
  "next": [
    {"agent": "pm", "action": "review", "timeout": "2h"},
    {"agent": "writer", "action": "document", "timeout": "4h"}
  ]
}
```

### Workflow Examples

**Research → Analysis → Report → Review:**
```
[Analyst collects data] → EVT: data.collected
    → [Analyst processes] → EVT: analysis.complete
    → [Writer drafts report] → EVT: report.draft
    → [PM reviews] → EVT: report.approved
```

**Code → Test → Review → Deploy:**
```
[Engineer implements] → EVT: code.submitted
    → [Engineer tests] → EVT: tests.passed
    → [PM reviews] → EVT: code.approved
    → [Engineer deploys] → EVT: deployment.complete
```

### When to Use
- Multi-step workflows (3+ sequential steps)
- Parallel agent execution
- Audit trail required
- Retry/failure handling needed

---

## Communication Rules

### Rule 1: No Ambiguous Messages
Every message must have: sender, receiver, purpose, expected action, deadline.

### Rule 2: Escalation Ladder
```
Agent A → Agent B (direct)
  → PM (if no response in 2x expected time)
    → CEO (if blocker impacts sprint)
      → Human (if strategic decision needed)
```

### Rule 3: Acknowledgment Protocol
- Receiver acknowledges receipt within the agent's check-in interval
- If no acknowledgment, escalate after timeout
- Always confirm critical messages

### Rule 4: Knowledge Sharing
- Decisions go to `shared/knowledge/decisions/`
- Learnings go to `shared/knowledge/learnings/`
- Reference material goes to `shared/knowledge/reference/`
- Never duplicate — link, don't copy

---

## Platform-Specific Notes

### OpenClaw
- `sessions_send` for real-time
- Shared dirs via filesystem
- `cron` for heartbeat scheduling
- Subagents for parallel execution

### Claude Code
- Multiple sessions with file coordination
- Use `/clm sessions` for cross-session messaging
- File watchers for event-driven workflows

### Cursor
- `.cursor/rules/` per agent workspace
- Shared files in workspace root
- Terminal commands for cross-agent signals

### Codex
- Task files in shared workspace
- Comments for inter-agent communication
- Sequential agent execution via task chains

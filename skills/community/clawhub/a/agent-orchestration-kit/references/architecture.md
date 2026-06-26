# Architecture — Star Topology & A2A Sessions

## System Design

The Agent Orchestration Kit uses a strict **star topology** with persistent A2A (Agent-to-Agent) sessions. The Leader agent is the sole hub; all other agents are spokes. No spoke-to-spoke communication exists.

```
                    +-----------+-----------+
                    |       LEADER          |
                    |                       |
                    |  - Orchestration      |
                    |  - Task decomposition |
                    |  - Quality control    |
                    |  - Owner interface    |
                    +-----------+-----------+
                         /  |  |  \
                  sessions_send (persistent, async)
                       /    |  |    \
              +--------+  +------+  +------+  +------+
              |Executor|  |Spec 1|  |Spec 2|  |Spec N|
              +--------+  +------+  +------+  +------+
                              + Reviewer (spawned on-demand)
```

## Why Star Topology?

1. **Single point of accountability** — Leader owns all owner-facing communication.
2. **Context control** — Leader curates what context each agent receives via task briefs.
3. **Quality gate** — All output is reviewed before reaching the owner.
4. **Audit trail** — Every delegation and result flows through one node (task files).
5. **Simplicity** — No complex mesh routing, no conflict resolution between agents.

## Session Model

| Property | Value |
|----------|-------|
| Communication method | `sessions_send` (persistent sessions) |
| Dispatch mode | `timeoutSeconds: 0` (fully async, non-blocking) |
| Session key format | `agent:{id}:main` |
| Same-agent concurrency | Serial (one task at a time) |
| Cross-agent concurrency | Parallel |
| Ping-pong limit | 3 rounds per `sessions_send` |
| Context preservation | Full — survives across tasks and feedback loops |
| Compaction handling | Agent sends `[CONTEXT_LOST]`; Leader re-sends from `tasks/T-{id}.md` |

## Request Lifecycle

```
Owner sends message → Leader receives → Analyzes intent →
  Decomposes into atomic subtasks → Creates task files →
  Routes to agents (parallel when possible) →
  Sends status notification → Returns to owner (not blocked) →
  Agents work and callback → Leader processes callbacks →
  Updates status notification → Quality check (optional Reviewer) →
  Present to owner [PENDING APPROVAL] →
  Owner approves → Final action
```

## Parallelism Strategy

- **Independent tasks** → parallel across different agents
- **Dependent tasks** → serial (output of A feeds into B)
- **Same agent** → always serial (one task at a time per agent)
- **Cross-agent** → parallel by default

## Workspace Isolation

Each agent has its own workspace directory. Shared files are symlinked:

```
workspace/                           # Leader
├── SOUL.md, AGENTS.md
├── tasks/, tasks/archive/
└── shared/
    └── operations/

workspace-executor/
├── SOUL.md, AGENTS.md
└── shared -> ../workspace/shared/

workspace-{specialist}/
├── SOUL.md, AGENTS.md
└── shared -> ../workspace/shared/
```

## Maintenance Commands

| Command | Purpose |
|---------|---------|
| `openclaw agents bindings` | View agent-to-channel route bindings |
| `openclaw agents bind/unbind` | Manage agent routing |
| `openclaw sessions cleanup --fix-missing` | Prune stale session entries |
| `openclaw doctor` | Validate config, sessions |

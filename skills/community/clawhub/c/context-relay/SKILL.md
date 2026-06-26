---
name: context-relay
description: Solves the memory fragmentation problem for Agents during session restarts, sub-agent boundaries, and cron/heartbeat isolation.
---

# Context Relay - Cross-Session Memory Continuity System

Files are the single source of truth. Each execution unit reads context from files at startup, without relying on session memory. Suitable for Agents that need to maintain task continuity across sessions.

## Trigger Words

- Memory fragmentation
- Cross-session
- Context passing
- context relay
- session restart
- sub-agent communication
- persistent context
- project state management
- cold start

## Core Principle

**Files are the single source of truth.**

Agents lose session memory in the following scenarios:
- Session restart (app restart, timeout disconnection)
- Sub-agent boundaries (newly spawned agents lack parent session memory)
- Cron/Heartbeat isolation (scheduled tasks and heartbeats are independent sessions)

**Solution**: Each execution unit reads context from files at startup and writes back to files when finished. Files are memory.

## Three-Layer Context Architecture

```
project/
├── PROJECT.md        # Project metadata (long-term stable)
├── state.json        # Current state (frequently updated)
├── decisions.md      # Architecture decision records (append-only)
└── todos.json        # Self-managed todo list (cross-session tracking)
```

### Layer 1: PROJECT.md (Project Identity)

**Purpose**: Defines "who I am," long-term stable, rarely modified.

**Content Template**:
```markdown
# Project Name

## One-Line Description
[What this project is, what problem it solves]

## Tech Stack
- Frontend:
- Backend:
- Database:
- Deployment:

## Directory Structure
/src        - Source code
/docs       - Documentation
/tests      - Tests

## Key Constraints
[Rules that must be followed, such as API compatibility, performance requirements]

## Related Documents
- Architecture decisions: decisions.md
- Current state: state.json
- Todo items: todos.json
```

### Layer 2: state.json (Current State)

**Purpose**: Defines "where I am," frequently updated, records current progress.

**Content Template**:
```json
{
  "phase": "development",
  "current_task": "Implement user authentication module",
  "progress": {
    "completed": ["Database design", "API design"],
    "in_progress": "Login endpoint development",
    "blocked": [],
    "next_steps": ["Registration endpoint", "Password reset"]
  },
  "last_update": "2026-04-20T10:00:00+08:00",
  "session_id": "abc123",
  "notes": "Encountering CORS issues, need to configure proxy"
}
```

### Layer 3: decisions.md (Decision Records)

**Purpose**: Defines "why," append-only, never deleted.

**Content Template**:
```markdown
# Architecture Decision Records

## ADR-001: Use JWT for Authentication
- Date: 2026-04-15
- Status: Accepted
- Context: Need a stateless authentication scheme
- Decision: Use JWT + refresh tokens
- Consequences: Must handle token expiration and revocation

## ADR-002: Choose PostgreSQL as Primary Database
- Date: 2026-04-16
- Status: Accepted
- Context: Need support for complex queries and transactions
- Decision: Use PostgreSQL
- Consequences: Must learn PostgreSQL-specific syntax
```

## todos.json (Self-Managed Todo System)

**Purpose**: Agent-managed todo list for cross-session tracking.

**Content Template**:
```json
{
  "todos": [
    {
      "id": "TODO-001",
      "title": "Complete user authentication module",
      "priority": "high",
      "status": "in_progress",
      "created": "2026-04-20T09:00:00+08:00",
      "updated": "2026-04-20T10:00:00+08:00",
      "notes": "Implementing login endpoint"
    },
    {
      "id": "TODO-002",
      "title": "Write unit tests",
      "priority": "medium",
      "status": "pending",
      "created": "2026-04-20T09:00:00+08:00",
      "updated": null,
      "notes": ""
    }
  ],
  "last_review": "2026-04-20T10:00:00+08:00"
}
```

**Operation Rules**:
- Start task: Change status to `in_progress`
- Complete task: Change status to `completed`, record `completed_at`
- Blocked task: Change status to `blocked`, explain reason in `notes`
- Each session start: Check `last_review`; if over 24 hours, review all todos

## Workflow

### On Startup: Cold Start Procedure

Execute at the start of each new session/sub-agent/cron job:

```
1. Read PROJECT.md → Understand project identity
2. Read state.json → Understand current progress
3. Read todos.json → Understand pending tasks
4. If decision context is needed → Read decisions.md
5. Begin work
```

**Critical**: Do not assume any memory. All context must be read from files.

### On Completion: State Synchronization

Execute before ending each work session:

```
1. Update state.json → Record current progress
2. If new decisions were made → Append to decisions.md
3. If todos changed → Update todos.json
4. Commit file changes
```

**Critical**: Files must be written before the session ends to ensure the next execution unit can read the latest state.

### Sub-Agent Communication

Parent and child agents communicate context via files:

```
Parent agent:
1. Update state.json (current task, expected output)
2. Spawn child agent

Child agent:
1. Read state.json → Understand task
2. Execute task
3. Update state.json (results, progress)
4. End

Parent agent:
1. Read state.json → Retrieve results
2. Continue work
```

**Note**: Child agents have no memory of the parent session; they can only communicate via files.

## Reference Resources

- [Project Template Details](references/project-template.md) - Complete file templates and usage examples
- [todos.json Management](references/todos-system.md) - Detailed explanation of the self-managed todo system
- [Cold Start Guide](references/cold-start-guide.md) - Cold start procedures for various scenarios

## Script Tools

- `scripts/init_context.py` - Initialize the context file structure in a project directory
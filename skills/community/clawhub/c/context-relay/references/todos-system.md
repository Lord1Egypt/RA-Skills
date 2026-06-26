# todos.json Self-Managed Todo System

Agent-managed cross-session todo list.

## Core Philosophy

**Agent manages autonomously, not dependent on user instructions.**

todos.json is the Agent's own todo list, used for:
- Recording tasks that need cross-session tracking
- Reminding oneself of tasks needed in future sessions
- Tracking progress of long-term projects

## File Structure

```json
{
  "todos": [
    {
      "id": "TODO-001",
      "title": "Task title",
      "description": "Detailed description",
      "priority": "high",
      "status": "in_progress",
      "category": "feature",
      "tags": ["auth", "api"],
      "created": "2026-04-20T09:00:00+08:00",
      "updated": "2026-04-20T10:00:00+08:00",
      "completed_at": null,
      "due_date": "2026-04-25T18:00:00+08:00",
      "assignee": null,
      "blocked_by": [],
      "blocking": [],
      "notes": "Additional notes"
    }
  ],
  "completed": [
    {
      "id": "TODO-000",
      "title": "Completed task",
      "completed_at": "2026-04-19T15:00:00+08:00"
    }
  ],
  "metadata": {
    "last_review": "2026-04-20T10:00:00+08:00",
    "total_created": 10,
    "total_completed": 5
  }
}
```

## Field Descriptions

### Todo Item Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | Yes | Unique identifier, format: TODO-XXX |
| title | string | Yes | Task title |
| description | string | No | Detailed description |
| priority | string | Yes | Priority: critical/high/medium/low |
| status | string | Yes | Status: pending/in_progress/completed/blocked/cancelled |
| category | string | No | Category: feature/bug/refactor/docs/test |
| tags | array | No | List of tags |
| created | string | Yes | Creation timestamp (ISO 8601) |
| updated | string | No | Last update timestamp |
| completed_at | string | No | Completion timestamp (required when status is completed) |
| due_date | string | No | Due date |
| blocked_by | array | No | IDs of other TODOs blocking this task |
| blocking | array | No | IDs of other TODOs blocked by this task |
| notes | string | No | Additional notes |

### Metadata Fields

| Field | Description |
|-------|-------------|
| last_review | Last review timestamp |
| total_created | Total number of todos created |
| total_completed | Total number of todos completed |

## Operation Rules

### Creating a Todo

```json
{
  "id": "TODO-006",
  "title": "New task",
  "priority": "medium",
  "status": "pending",
  "created": "2026-04-20T10:00:00+08:00"
}
```

**When to create**:
- Agent discovers something that needs to be done
- User proposes a new requirement
- Code review finds improvement points
- Encounter issues that need follow-up resolution

### Starting a Task

```json
{
  "status": "in_progress",
  "updated": "2026-04-20T10:30:00+08:00"
}
```

### Completing a Task

```json
{
  "status": "completed",
  "completed_at": "2026-04-20T12:00:00+08:00",
  "updated": "2026-04-20T12:00:00+08:00"
}
```

After completion, move the task to the `completed` array:
```json
{
  "completed": [
    {
      "id": "TODO-001",
      "title": "Completed task",
      "completed_at": "2026-04-20T12:00:00+08:00"
    }
  ]
}
```

### Marking as Blocked

```json
{
  "status": "blocked",
  "blocked_by": ["TODO-003"],
  "notes": "Waiting for TODO-003 to complete before proceeding",
  "updated": "2026-04-20T11:00:00+08:00"
}
```

### Periodic Review

**Trigger conditions**:
- `last_review` exceeds 24 hours
- At the start of a new session

**Review process**:
```
1. Check if all pending todos are still valid
2. Check if any blocked todos can be unblocked
3. Update priorities (adjust based on project progress)
4. Update last_review timestamp
```

## Best Practices

### Priority Definitions

| Priority | Definition | Example |
|----------|------------|---------|
| critical | Blocks project progress | Security vulnerability, production bug |
| high | Must complete this week | Core feature, important fix |
| medium | Complete this month | Optimization, improvement, minor feature |
| low | Do when time permits | Documentation, cleanup, nice-to-have |

### State Transition Diagram

```
pending → in_progress → completed
    ↓          ↓
  blocked  →  blocked
    ↓
cancelled
```

### Periodic Cleanup

- Completed tasks: Move from `todos` to `completed` after 7 days
- Cancelled tasks: Remove from `todos` (optional: move to `cancelled` array)
- Overdue todos: Check `due_date`, update priority or mark as deferred

## Usage Scenarios

### Scenario 1: Cross-Session Tracking

**Session 1**:
```
User: Help me implement user authentication feature
Agent: Create TODO-001 (implement login), TODO-002 (implement registration)
      Start TODO-001, mark in_progress
      Complete 70%, session ends
```

**Session 2 (Next Day)**:
```
Agent starts: Read todos.json
Discovers: TODO-001 in_progress (70% complete)
Continues: Complete TODO-001, mark completed
Starts: TODO-002, mark in_progress
```

### Scenario 2: Self-Reminder

```json
{
  "id": "TODO-005",
  "title": "Check API documentation updates",
  "priority": "low",
  "status": "pending",
  "due_date": "2026-04-25T18:00:00+08:00",
  "notes": "OpenAI updated their API last week, remember to check if it affects our integration"
}
```

### Scenario 3: Task Dependencies

```json
{
  "id": "TODO-003",
  "title": "Configure database",
  "status": "in_progress"
},
{
  "id": "TODO-004",
  "title": "Implement data access layer",
  "status": "pending",
  "blocked_by": ["TODO-003"],
  "notes": "Need to complete database configuration first"
}
```
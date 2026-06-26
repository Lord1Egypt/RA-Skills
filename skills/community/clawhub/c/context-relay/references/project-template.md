# Project Template Details

This document provides complete context file templates and usage examples.

## Complete Templates

### PROJECT.md Template

```markdown
# [Project Name]

## One-Line Description
[What this project is, what problem it solves]

## Tech Stack
- Frontend: [framework/library]
- Backend: [framework/library]
- Database: [database]
- Deployment: [deployment method]

## Directory Structure
```
project/
├── src/              # Source code
│   ├── frontend/     # Frontend code
│   ├── backend/      # Backend code
│   └── shared/       # Shared code
├── docs/             # Documentation
├── tests/            # Tests
├── PROJECT.md        # Project metadata
├── state.json        # Current state
├── decisions.md      # Architecture decisions
└── todos.json        # Todo list
```

## Key Constraints
- [Constraint 1: e.g., API version compatibility requirements]
- [Constraint 2: e.g., performance requirements]
- [Constraint 3: e.g., security requirements]

## External Dependencies
- [Dependency 1: e.g., third-party API]
- [Dependency 2: e.g., database service]

## Related Documents
- Architecture decisions: decisions.md
- Current state: state.json
- Todo items: todos.json
```

### state.json Template

```json
{
  "version": "1.0",
  "phase": "development",
  "current_task": "Specific task description",
  "progress": {
    "completed": [
      "Completed item 1",
      "Completed item 2"
    ],
    "in_progress": "Work currently in progress",
    "blocked": [
      {
        "item": "Blocked item",
        "reason": "Reason for blockage",
        "since": "2026-04-20T10:00:00+08:00"
      }
    ],
    "next_steps": [
      "Next step 1",
      "Next step 2"
    ]
  },
  "metrics": {
    "total_tasks": 10,
    "completed_tasks": 3,
    "blocked_tasks": 1
  },
  "last_update": "2026-04-20T10:00:00+08:00",
  "last_session": "session-id-here",
  "notes": "Important notes for the current session"
}
```

### decisions.md Template

```markdown
# Architecture Decision Records

## ADR-001: [Decision Title]

### Metadata
- **Date**: 2026-04-20
- **Status**: Accepted / Deprecated / Superseded
- **Decider**: [Name or Team]

### Context
[Why is this decision needed? What is the problem?]

### Decision
[What decision was made? What are the specifics?]

### Rationale
[Why was this option chosen? What alternatives were considered?]

### Consequences
[What are the implications of this decision? Positive and negative?]

---

## ADR-002: [Next Decision Title]
...
```

## Usage Examples

### Example 1: New Project Initialization

```bash
# Create context files in project root directory
python init_context.py /path/to/project

# Generated structure:
# /path/to/project/
# ├── PROJECT.md    (needs manual filling)
# ├── state.json    (initial state)
# ├── decisions.md  (empty file)
# └── todos.json    (empty todo list)
```

### Example 2: Cross-Session Workflow

**Session 1 (Day 1)**:
```json
// state.json at end of session
{
  "phase": "development",
  "current_task": "Implement user authentication",
  "progress": {
    "completed": ["Database design"],
    "in_progress": "Login endpoint",
    "next_steps": ["Registration endpoint", "Password reset"]
  },
  "last_update": "2026-04-20T18:00:00+08:00",
  "notes": "Login endpoint 70% complete, encountering CORS issues"
}
```

**Session 2 (Day 2)**:
```
1. Read state.json → Discover "Login endpoint 70% complete"
2. Read notes → Discover CORS issues
3. Continue work → Resolve CORS, complete login endpoint
4. Update state.json → Mark login endpoint as completed
```

### Example 3: Sub-Agent Collaboration

**Parent Agent Preparation**:
```json
// state.json
{
  "current_task": "Code review",
  "delegated_to": "sub-agent-reviewer",
  "expected_output": "Review report with issues and recommendations",
  "input_files": ["src/auth/login.py", "src/auth/register.py"]
}
```

**Child Agent Execution**:
```
1. Read state.json → Understand task
2. Read input_files → Review code
3. Generate review report
4. Update state.json:
   {
     "current_task": "Code review",
     "result": "Found 3 issues, detailed in review report",
     "report_file": "docs/reviews/auth-review-2026-04-20.md"
   }
```

**Parent Agent Continuation**:
```
1. Read state.json → Obtain review results
2. Read report_file → View detailed report
3. Decide next actions
```

## Field Descriptions

### state.json Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| version | string | No | File format version |
| phase | string | Yes | Project phase: planning/development/testing/deployed |
| current_task | string | Yes | Description of current task in progress |
| progress.completed | array | Yes | List of completed tasks |
| progress.in_progress | string | No | Specific work currently in progress |
| progress.blocked | array | No | List of blocked tasks |
| progress.next_steps | array | Yes | Planned next steps |
| last_update | string | Yes | Last update timestamp (ISO 8601) |
| last_session | string | No | Last session ID |
| notes | string | No | Important notes |

### decisions.md ADR Fields

| Field | Required | Description |
|-------|----------|-------------|
| Date | Yes | Decision date |
| Status | Yes | Accepted / Deprecated / Superseded |
| Context | Yes | Why this decision is needed |
| Decision | Yes | Specific decision content |
| Rationale | No | Why this option was chosen |
| Consequences | Yes | Implications of the decision |
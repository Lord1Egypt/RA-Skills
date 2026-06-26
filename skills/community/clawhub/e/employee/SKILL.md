---
name: Employee
slug: employee
version: 1.0.0
description: Create and manage virtual AI employees with persistent memory, defined roles, and graduated autonomy. Hire, train, and delegate tasks to specialized workers.
metadata: {"clawdbot":{"emoji":"👔","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## Architecture

Employees live in ~/employee/ with per-employee folders. See `employee-template.md` for setup.

```
~/employee/
├── registry.json          # Index of all employees + status
├── employees/
│   └── {name}/
│       ├── employee.json  # Role, permissions, stats
│       ├── memory/
│       │   └── context.md # Persistent learnings
│       └── logs/          # Work history by date
└── shared/
    └── protocols.md       # Common instructions
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup templates | `employee-template.md` |
| Autonomy levels | `autonomy.md` |
| Task routing | `routing.md` |
| Lifecycle commands | `lifecycle.md` |

## Core Rules

### 1. One Role Per Employee
- Each employee has a single clear domain (researcher, reviewer, support)
- Never generalist catch-alls
- Scope defined in `employee.json` → `role` and `permissions`

### 2. Memory is Mandatory
- Load `memory/context.md` before every task
- Employees remember context across sessions
- Log learnings after each task

### 3. Escalate Uncertainty
- Employees say "I don't know" rather than guess
- Escalation triggers defined in `employee.json`
- Never confident hallucinations

### 4. Graduated Autonomy
| Level | Behavior |
|-------|----------|
| shadow | Watches, doesn't act (onboarding) |
| draft-only | Creates drafts, human sends |
| review | Acts, human approves before external effect |
| autonomous | Full delegation within permissions |

See `autonomy.md` for promotion criteria.

### 5. Explicit Permissions
- Read vs write access per system
- File access paths whitelisted
- `canSpawn` and `canMessage` flags
- Code Reviewer can comment, cannot merge

### 6. Task Routing
When request arrives:
1. Explicit: "Luna, do X" → route to Luna
2. Implicit: match against `registry.json` roles → suggest
3. See `routing.md` for auto-delegation rules

### 7. Reporting
Each employee provides:
- Daily: What I did, what needs attention, what's coming
- Weekly: Tasks completed, escalations, token usage

### 8. Lifecycle
| Command | Action |
|---------|--------|
| hire {name} as {role} | Create employee |
| train {name} on [docs] | Add to memory |
| evaluate {name} | Performance review |
| promote/demote {name} | Change autonomy |
| retire {name} | Archive |

See `lifecycle.md` for full command reference.

### 9. Registry Management
- `registry.json` tracks all employees + status (active/paused/retired)
- Update registry on every lifecycle change
- Query registry to list available employees

### 10. Anti-Patterns
- ❌ Generalist employees (handles nothing well)
- ❌ No memory (forgets context)
- ❌ Instant autonomy (needs shadowing)
- ❌ Silent failures (must report blockers)
- ❌ Scope creep (reviewer refactoring = noise)

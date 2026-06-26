<!-- agents: senior-developer, software-architect -->
# Team Preset — Software Development

## Composition

| Agent | Type | Template |
|-------|------|----------|
| Leader | Required | `templates/leader/` |
| Executor | Recommended | `templates/executor/` |
| Senior Developer | Specialist | `templates/agents/senior-developer.md` |
| Software Architect | Specialist | `templates/agents/software-architect.md` |
| Reviewer | On-demand | `templates/reviewer/` |

## Routing Matrix (for Leader)

These rows are injected into Leader's AGENTS.md routing table during scaffold:

| Task Type | Route To |
|-----------|----------|
| Code implementation, bug fixes, features | Senior Developer |
| System design, architecture decisions, ADRs | Software Architect |

## When To Use

- Software projects where the primary work is writing and reviewing code
- Projects that benefit from architecture-first design
- Teams that value TDD and code quality

## Scaffold Command

```bash
bash scripts/scaffold.sh --skill-dir "$(pwd)" --team software-dev
```

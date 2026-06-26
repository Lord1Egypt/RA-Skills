<!-- agents: researcher -->
# Team Preset — Research & Analysis

## Composition

| Agent | Type | Template |
|-------|------|----------|
| Leader | Required | `templates/leader/` |
| Executor | Recommended | `templates/executor/` |
| Researcher | Specialist | `templates/agents/researcher.md` |
| Reviewer | On-demand | `templates/reviewer/` |

## Routing Matrix (for Leader)

These rows are injected into Leader's AGENTS.md routing table during scaffold:

| Task Type | Route To |
|-----------|----------|
| Research, analysis, data gathering, competitive intelligence | Researcher |

## When To Use

- Investigation and analysis-heavy projects
- Competitive intelligence gathering
- Evidence-based decision making workflows
- Projects where research quality is critical

## Scaffold Command

```bash
bash scripts/scaffold.sh --skill-dir "$(pwd)" --team research-analysis
```

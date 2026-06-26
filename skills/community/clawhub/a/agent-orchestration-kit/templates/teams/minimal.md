<!-- agents: -->
# Team Preset — Minimal

## Composition

| Agent | Type | Template |
|-------|------|----------|
| Leader | Required | `templates/leader/` |
| Executor | Recommended | `templates/executor/` |
| Reviewer | On-demand | `templates/reviewer/` |

No specialists included. Add agents individually after setup.

## Routing Matrix (for Leader)

| Task Type | Route To |
|-----------|----------|
| File ops, CLI, config, workspace maintenance | Executor |
| Quality review | Reviewer (spawn) |
| Everything else | Leader (self) or add specialists |

## When To Use

- Starting lean and adding specialists as needed
- Custom team compositions
- Experimenting with the orchestration protocol
- Projects where you want full control over team composition

## Adding Specialists Later

After setup, say:
- "Add a Senior Developer agent"
- "Add a custom agent: {role name}"

## Scaffold Command

```bash
bash scripts/scaffold.sh --skill-dir "$(pwd)" --team minimal
```

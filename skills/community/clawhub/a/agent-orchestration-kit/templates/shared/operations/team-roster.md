# Team Roster

| Agent | Type | Primary Capability |
|-------|------|--------------------|
| Leader | Required | Orchestration, routing, quality control, owner communication |
| Executor | Recommended | File ops, CLI, config, workspace maintenance |
| Reviewer | On-demand | Independent quality review (spawned when needed) |

_(Specialist agents are added below during setup)_

## Communication

- Owner ↔ Leader ↔ Agents (star topology)
- All inter-agent routing goes through Leader
- Executor handles Leader's operational tasks
- Reviewer is spawned on-demand, not persistent

## Signals

See `shared/operations/communication-signals.md` for signal reference.

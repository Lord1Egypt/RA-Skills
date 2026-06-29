# Communication Patterns for Multi-Agent Organizations

## Pattern 1: Hub-and-Spoke (Recommended)

CEO (main) is the hub. All departments communicate through CEO.

```
Admin → CEO → DataCenter
Brand → CEO → Inspector
```

**Pros:** Simple, CEO has full visibility
**Cons:** CEO bottleneck at scale

## Pattern 2: Mesh with Routing

Departments communicate directly using routing rules.

```
Brand → Admin (task assignment)
Inspector → Legal (compliance flag)
Finance → CEO (budget alert)
```

**Pros:** Faster, no bottleneck
**Cons:** CEO may miss context

## Pattern 3: Hybrid (Best for <10 agents)

Routine ops go direct. Strategic decisions go through CEO.

```
Daily reports → CEO
Task handoffs → Admin
Compliance → Legal
Alerts → Inspector + CEO
```

## Failure Modes to Avoid

| Failure | Cause | Fix |
|---------|-------|-----|
| Silent death | Agent stops responding | Inspector checks daily |
| Cascade failure | One error propagates | Isolate department workspaces |
| Communication blackout | Single channel fails | Parallel paths (sessions_send + files + cron) |
| Data pollution | Cross-department writes | Strict file ownership rules |
| Token exhaustion | Uncontrolled model usage | Free-tier models for internal tasks |

## Cron Health Rules

1. Every cron must have `consecutiveErrors` monitored
2. 2 consecutive failures = inspector flags anomaly
3. 3 consecutive failures = CEO intervenes
4. Weekly full audit of all cron jobs

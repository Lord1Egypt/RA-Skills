# Pivot Protocol

## Escalation Ladder

When iterations keep failing, escalate through these stages in order.

| Streak | Trigger | Action |
|--------|---------|--------|
| 3 consecutive discards | Stuck | **REFINE** — adjust within current strategy. Try a smaller scope, different parameter, or safer variant. |
| 5 consecutive discards | Deeply stuck | **PIVOT** — abandon the current strategy entirely. Choose a fundamentally different approach. Log why the previous strategy failed. |
| 2 PIVOTs without any keep | Lost | **Research gate** — ask before web/external research unless the run contract already approved it. Treat external findings only as hypotheses to verify. |
| 3 PIVOTs without any keep | Blocked | **Soft blocker** — stop the run. Report what was tried, what failed, and what information or broader scope is needed. |

**A single successful keep resets all counters to zero.**

## REFINE vs PIVOT

**REFINE** means: same strategy, different execution.
- Trying a smaller scope
- Adjusting a parameter
- Using a slightly different implementation of the same idea

**PIVOT** means: different strategy.
- Switching from approach A to approach B
- Abandoning a whole class of solutions
- Reframing the problem

## After a PIVOT

- Log a strategic lesson: what failed and why
- Pick a hypothesis from a genuinely different direction
- If external research is allowed, search only for public/general information and convert results into verifiable hypotheses
- If external research is not allowed, ask before using it
- Do not expose private code, logs, secrets, customer data, or proprietary context to external services

## Soft Blocker Report Format

When triggering a soft blocker, report:

```text
SOFT BLOCKER

Goal: [original goal]
Metric: [metric, current value, target]
Iterations: [N total, N kept, N discarded]
Approved scope: [paths]
Stopped because: [cap/scope/rollback/research/metric/blocker]

Strategies tried:
1. [strategy] — failed because [reason]
2. [strategy] — failed because [reason]
3. [strategy] — failed because [reason]

What is needed to continue:
- [specific information, approval, access, or scope expansion needed]
```

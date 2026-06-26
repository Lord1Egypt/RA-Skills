# Operations

## Quick trigger

Use a short worker handoff in the controller DM.

Example:

```text
WorkerBot, summarize this link
```

## Orchestrated trigger

Use when the controller bot should explicitly rewrite and delegate the task.

Example:

```text
ControllerBot, send this task to WorkerBot:
Summarize this link and report the key risks.
```

## Healthy flow checklist

1. the operator sends a task in the controller DM
2. the controller bot posts a structured task envelope into the private worker lane
3. the worker bot accepts the task
4. the worker bot replies in the lane
5. the final answer returns to the original DM

## Guardrails

- use a private worker lane only
- do not use a public or general channel as the worker lane
- keep worker-side bot exceptions narrow
- prefer structured final replies over plain chat for reliable relay-back
- document regressions before stacking ad-hoc fixes

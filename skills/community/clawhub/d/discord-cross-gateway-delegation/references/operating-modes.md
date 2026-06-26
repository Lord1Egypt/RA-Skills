# Operating modes

Use two input modes for MAIJini -> MACJini delegation.

## 1. Quick handoff

Shortcut trigger for fast delegation.

Examples:

```text
MACJini, reply with one short line for a smoke test
MACJini, verify this Safari flow
```

Behavior:

- user still talks to MAIJini
- MAIJini recognizes the worker shortcut prefix
- MAIJini forwards the task to the worker lane
- MACJini executes
- MAIJini relays the final answer back

Use when speed matters and the task is simple.

## 2. Orchestrated handoff (preferred for real work)

Preferred mode when the user wants MAIJini to intentionally assign work to MACJini.

Examples:

```text
MAIJini, send this task to MACJini:
Verify the Safari login flow

MAIJini, have MACJini handle this browser verification task
```

Behavior:

- user addresses MAIJini as the controller
- MAIJini interprets the task first
- MAIJini generates the worker-facing envelope/prompt
- MAIJini decides task type, constraints, and deliverables
- MACJini executes
- MAIJini relays the final result back to the DM

Why this mode is preferred:

- keeps MAIJini as the control tower
- makes real delegated work feel intentional
- lets the worker receive a cleaner prompt than the original user wording
- supports richer structured envelopes for browser/research/ops tasks

## Policy

Recommended policy:

- allow both modes
- keep quick handoff for simple tests and short tasks
- prefer orchestrated handoff for real work
- consider the delegation successful only when DM relay-back happens

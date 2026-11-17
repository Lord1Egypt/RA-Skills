# Checks and event schema

## Event schema

One JSON object per line. Only `ts` and `session` are required; missing fields are treated as absent, not as failures.

| Field | Type | Meaning |
|---|---|---|
| `ts` | ISO-8601 string or epoch ms | when the event happened |
| `session` | string | conversation or task container |
| `tool` | string | tool name; omit for non-tool events |
| `ok` | boolean | tool call succeeded |
| `duration_ms` | number | tool or step duration |
| `checkpoint` | boolean | progress or acknowledgement event |
| `outcome` | `ok` / `error` | task-level outcome, when known |
| `user_visible` | boolean | the user saw a message for this event |
| `claims` | boolean | this task asserted facts |

## Built-in checks

| Name | Predicate | Why it matters |
|---|---|---|
| `long_task_without_checkpoint` | duration > 5 min and no checkpoint | long work with no visibility |
| `retry_storm` | 3+ consecutive failures on the same tool | thrash, usually a root cause not yet removed |
| `silent_failure` | task errored and nothing was shown to the user | failure that looks like success |
| `claims_without_tools` | task asserted facts with zero tool calls | unsupported assertion risk |

## Writing your own

A check must be:

1. **Mechanical** — a predicate over fields, not a reading of intent.
2. **Bounded** — has a threshold and a stated base (eligible population).
3. **Calibratable** — you can point to a period where you know the answer.

Prefer a check that fires rarely and correctly over one that fires often and needs explaining.

## Calibration

Run on a known-good period first. If a check fires on runs you would call correct, the predicate is wrong. Fix the predicate before adjusting the threshold — thresholds hide model errors, they do not remove them.

## What not to encode

- “The answer was good.” Not observable.
- “The agent should have searched.” Only observable if you define the trigger condition and the required tool call.
- “No hallucination.” Replace with a concrete proxy such as `claims_without_tools`, and label it as a proxy.

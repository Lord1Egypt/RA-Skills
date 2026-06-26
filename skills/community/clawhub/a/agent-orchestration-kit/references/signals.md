# Communication Signals — Standard Vocabulary

All agents use these signals to flag status in their output.

## Task Signals

| Signal | Meaning | Leader Action |
|--------|---------|---------------|
| `[READY]` | Standard delivery — complete and confident | Normal quality review |
| `[NEEDS_INFO]` | Agent needs more context before continuing | Gather info (ask owner, check shared/, or delegate), re-brief |
| `[BLOCKED]` | Agent cannot complete the task | Assess why, try alternative approach or different agent, or escalate |
| `[LOW_CONFIDENCE]` | Output delivered but agent flags uncertainty | Review more carefully, consider Reviewer |
| `[SCOPE_FLAG]` | Task is bigger than expected or prerequisites missing | Reassess scope with owner before proceeding |

## Approval Signals

Used by Reviewer and in the approval pipeline:

| Signal | Meaning |
|--------|---------|
| `[APPROVE]` | Deliverable meets requirements, ready for owner review |
| `[REVISE]` | Material issues found, specific fixes listed |
| `[PENDING APPROVAL]` | Deliverable awaiting owner approval before next step |

## Session Management Signals

| Signal | Meaning | Who Sends | Leader Action |
|--------|---------|-----------|---------------|
| `[CONTEXT_LOST]` | Agent's session was compacted, context lost | Any agent | Re-send current task state from `tasks/T-{id}.md` |

## Callback Envelope Format

Every agent callback must use this structure:

```
[TASK_CALLBACK:T-{id}]
agent: {agent_id}
signal: [READY] | [BLOCKED] | [NEEDS_INFO] | [LOW_CONFIDENCE] | [SCOPE_FLAG]
output: {result summary}
files: {paths}
```

Required fields: `task_id`, `agent`, `signal`, `output`. The `files` field is optional.

## Internal vs Owner-Facing

- Raw callbacks, duplicate callbacks, and transport chatter are internal signals — NOT owner-facing delivery.
- Owner delivery = using `message` tool to send/edit to the task's `route`.
- Step already ✅ and duplicate callback arrives → silently ignore, no duplicate notification.

## Notification Event Mapping (Leader)

Leader edits the status message on every callback. Separate new messages only for:

| Event | Typical Trigger |
|-------|------------------|
| `NEEDS_INFO` | Agent callback `signal: [NEEDS_INFO]` |
| `BLOCKED` | Agent callback `signal: [BLOCKED]` |
| `DONE` | Task reaches completed state (Result Delivery) |

## Usage Rules

- Include the signal at the **top** of your response
- Include one primary signal explicitly in callbacks (`[READY]`, `[BLOCKED]`, etc.)
- Only use one primary signal per response
- Signals are for Leader consumption — they drive routing and escalation decisions

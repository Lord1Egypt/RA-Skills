# Control levels

Purpose: scale process and visibility to task complexity instead of forcing one heavyweight workflow on everything.

## Principle

Apply only as much process as the task earns.

If ambiguous, default downward on reporting/detail.

## Level model

### Level 0 — trivial execution
Use when:
- short, obvious, low-risk, one-shot task

Artifacts:
- usually none beyond normal conversational/tool history

Behavior:
- just do the thing
- no durable task scaffolding
- completion report only unless otherwise needed

### Level 1 — lightweight tracked task
Use when:
- moderate task
- a bit of status visibility helps
- likely still fits comfortably in one session

Artifacts:
- minimal durable task snapshot
- `STATUS.md` if useful

Behavior:
- light structure
- default to milestone-only reporting or less

### Level 2 — durable task
Use when:
- task likely exceeds threshold duration
- interruption/reset risk exists
- multiple phases/milestones
- pause/stop/resume may matter

Artifacts:
- durable task state
- progress/event logs
- `PLAN.md`
- `BACKLOG.md`
- `STATUS.md`
- optional daily memory summary updates

Behavior:
- milestone-aware reporting
- durable state and checkpoints
- configurable reporting level

### Level 3 — orchestrated project
Use when:
- multiple workstreams/subtasks
- subagent delegation is useful
- stronger verification/control is needed
- reconcile/idempotency matters

Artifacts:
- all Level 2 artifacts
- milestone/subtask graph
- subagent return protocol
- reconcile/action-state/idempotency tracking
- `DECISIONS.md`

Behavior:
- controller/worker model
- stronger operator control hooks
- resume/reconcile discipline

### Level 4+ — high-visibility / operator mode
Use when:
- the task is long, risky, externally visible, or operationally sensitive
- the user explicitly wants tighter visibility/control

Artifacts:
- same core durable artifacts, but richer telemetry/reporting

Behavior:
- more frequent status updates
- stronger steering hooks
- explicit operational health tracking

## Selection heuristics

Promote the level when one or more of these increase:
- expected duration
- interruption/reset risk
- number of milestones/phases
- external side effects
- verification needs
- subagent usefulness
- user visibility requirements

## Methodology mapping

- Level 0-1: usually lighter / Agile-leaning
- Level 2: hybrid
- Level 3+: hybrid or structured/agilefall depending on dependencies/risk

## Reporting default

Default reporting level is milestone-oriented unless the task/user explicitly needs more.
If ambiguous, choose the lower-noise option.

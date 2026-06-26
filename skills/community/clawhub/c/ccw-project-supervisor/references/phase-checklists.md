# Phase Checklists

## workflow-plan

Use when the project needs structure.

Checklist:
- Goal is explicit.
- Current project state is known.
- Constraints are listed.
- P0 scope is bounded.
- Milestones and epics are requested.
- Dependencies must be made explicit.
- The shortest runnable path is requested or can be inferred.

Success criteria:
- Milestones exist.
- Epics are grouped sensibly.
- Dependencies are explicit.
- Parallelizable work is called out.
- The next command is obviously `/issue/plan`.

## /issue/plan

Use when the project plan exists but tasks need to become execution-ready.

Checklist:
- Epics are stable enough.
- Each issue has one clear output.
- Acceptance criteria exist or can be derived.
- Test points can be attached.
- Priority and dependency information are available.

Success criteria:
- Issues are specific and verifiable.
- Ambiguous issues are split.
- Scope creep is not mixed into P0.
- The next command is obviously `/issue/queue`.

## /issue/queue

Use when issue drafts exist but execution order is not settled.

Checklist:
- Dependencies are explicit.
- The shortest runnable path is identified.
- Parallel work is identified.
- Risk-heavy issues are not pulled too early.
- The current issue candidate is small enough to execute.

Success criteria:
- There is a credible implementation order.
- The first execution issue is low ambiguity.
- The next command is obviously `/issue/execute`.

## /issue/execute

Use when the queue is validated and one issue is selected.

Checklist:
- The selected issue has a narrow scope.
- Predecessor work is complete.
- Acceptance criteria are known.
- The implementation plan does not smuggle in adjacent features.
- Progress logging and commit discipline are expected.

Success criteria:
- The implementation result can be reviewed against the issue.
- The next issue is known.
- Follow-up stays inside the queue unless the user approves a change.

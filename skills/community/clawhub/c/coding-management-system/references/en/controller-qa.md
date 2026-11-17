# Controller, Stage Reviewer, And Independent QA 2.1

Keep dispatch, implementation, stage review, and final acceptance authority distinct.

## Controller Dispatch

Before execution, Controller confirms:

1. goal readiness is `Ready for Execution`;
2. delivery class, size, and governance are explicit;
3. scope, Non-Goals, write boundary, and protected boundaries are coherent;
4. each acceptance criterion names appropriate evidence;
5. one stage outcome and one next action are authorized;
6. `autonomy_mode: Bounded` and `acceptance_mode: Layered` are understood.

Developer may continue across authorized stages while useful progress exists, authority and alignment remain stable, and no stop condition is triggered. Ordinary reversible project-local technical choices do not require Owner approval.

## Stage Review

User wording such as `QC` inside a single-agent `Controller -> Developer -> QC` loop maps to Stage Reviewer.

Stage Reviewer checks only the current stage:

- criterion and target link;
- changed files and scope;
- focused command results and affected regression;
- functional evidence for behavior claims;
- failure signature and repair progress;
- material risks and protected boundaries.

It returns `Passed`, `Needs Fix`, or `Blocked`. A failed stage returns to Developer on the same Packet and Work Order. It does not create a new Milestone and does not set final QA acceptance for Standard or Full work.

## Terminal Handoff

When all authorized Standard or Full stages pass, set:

```text
execution_state: Ready for Independent Acceptance
stage_review: Passed
qa_decision: Not Reviewed
project_state: Active
```

Independent QA must be a different agent, task, or human reviewer. It reviews criteria, diff, raw evidence, limits, target link, and required target environment without treating the Developer's verdict as evidence.

## Independent QA Decisions

- `Accepted`: all Must Pass criteria and required evidence are sufficient.
- `Accepted With Risk`: core outcome works; a non-blocking risk is explicit, owned, and time-bounded.
- `Failed`: an actionable implementation or evidence defect remains.
- `Blocked`: acceptance requires unavailable authority, environment, credentials, or protected access.

Do not use `Accepted With Risk` for a broken core flow, missing primary environment, absent functional evidence, or a Contract-only implementation claimed as Runtime.

## Failed Work

On Stage Review or QA failure:

1. retain the same Milestone, Packet, and Work Order;
2. tie the repair to failed criterion IDs;
3. set `Needs Fix` at the appropriate layer;
4. require a new diagnosis or progress delta before retrying;
5. rerun focused verification and affected regression;
6. return to independent QA only after the repair is stage-passed.

## Risk Carry Rule

Trigger Direction Alignment before further expansion when:

- the same material risk appears in two consecutive active reviews; or
- three consecutive independent decisions are `Accepted With Risk`.

The review must decide whether the risk is still non-blocking, requires target or architecture authority, or reveals systemic under-testing.

## Lite Self-Acceptance

Self-acceptance is limited to Lite when `qa_required: false`, the work is local and reversible, automatic and functional evidence pass, and no material limitation remains.

Use `{baseDir}/templates/en/QA_DECISION.md` only for final independent QA, not routine stage notes.

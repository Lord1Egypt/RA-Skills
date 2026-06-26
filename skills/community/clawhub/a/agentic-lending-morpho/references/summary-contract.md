# Morpho wrapper summary contract

Use this contract to interpret `ensure-feeds-and-deploy-morpho-market` output and persisted run artifacts. Prefer exact fields over narrative text.

## Required files in a normal run directory
The wrapper should persist a coherent run directory containing at least:

- `request.json`
- `initial-workflow.json`
- `summary.json`
- `agent-decision.json`
- `rollback-plan.json`

Depending on the branch, it may also contain:

- `approval-summary.json`
- `perf-summary.json`
- `funding.json`
- `funded-feed-cache.json`
- `propagation.json`
- `deploy-output.json`
- `verify-output.json`

## Primary status fields
Read `agent-decision.json` first when it exists. It is intentionally tiny:

| Field | Meaning | Safe interpretation |
| --- | --- | --- |
| `safeStatus` | model-friendly state enum | Use as the primary short status |
| `canContinue` | whether another step is possible | False means stop or ask/user action is required |
| `nextCommand` | next suggested command | Use only after checking `mustNotDo` and approvals |
| `mustNotDo[]` | hard safety reminders | Never violate these |
| `successClaimAllowed` | final-success gate | Must be `true` before claiming full deployment success |

Then inspect `summary.json` and detailed artifacts.

Read `approval-summary.json` before any heavy or live-capable execution handoff. It should state:
- what the wrapper plans to run
- whether it may send transactions
- expected duration band
- likely resource impact
- whether explicit acknowledgement is required

Read `perf-summary.json` when you need execution-shape evidence. It should capture:
- per-operation timing events
- aggregate counts for expensive workflow stages
- total elapsed time for the wrapper run

## Summary fields
Read these fields next:

| Field | Meaning | Safe interpretation |
| --- | --- | --- |
| `phase` | top-level wrapper phase | Only `completed` can be final success |
| `status` | wrapper status object/string when present | Supporting detail, not a replacement for `phase` |
| `blockers[]` | hard blockers | Non-empty means report blockers and stop |
| `warnings[]` | cautionary notes | Report when relevant; do not ignore live-send warnings |
| `perfSummary` | timing/count summary for the wrapper run | Use for perf evidence; do not confuse it with success state |
| `rollbackPlan` | local-only vs forward-only on-chain state | Inspect before any further transaction |
| `nextSteps[]` | generated next actions | Use as the next command/action source |

## Feed activation gates
Use these fields when present:

| Field | Success gate |
| --- | --- |
| `fundingResult.completedExecution` | `true` means funding/proxy execution completed, not that feeds are live |
| `fundingResult.classification` / `fundingResult.feedStatus` | Use to report live, fundable, browser-assisted, or unsupported branch |
| `propagationResult.ready` | Must be `true` before deployment after funding |
| `propagationResult.blockers[]` | Non-empty means do not deploy |
| `fundingResult.executionMode` | Confirms direct/wrapper/browser branch when present |

Important: funding success is not enough. A model must wait for or reuse a run where `propagationResult.ready === true`, or where initial readiness proves feeds were already live.

## Deployment gates
Use these fields when present:

| Field | Success gate |
| --- | --- |
| `deployResult.ready` | deployment plan/output is ready; may still be dry-run/planning-only |
| `deployResult.sendSummary.completed` | `true` means live send completed |
| `deployResult.transactionPlan[]` | Check adapter and market creation transactions |
| `deployResult.adapters[]` | Check deployed/predicted adapter addresses and source feed/proxy config |
| `deployResult.markets[]` | Check market params and oracle adapter address |

A market is not live just because `deployResult.ready === true`. Require live send completion and verification.

## Verification gates
Use these fields when present:

| Field | Success gate |
| --- | --- |
| `verifyResult.verified` | Must be `true` for final success |
| `verifyResult.blockers[]` | Non-empty means report verification failure/blocker |
| `verifyResult.oraclePrice` / price-read field when present | Must show a positive oracle read |
| `verifySkippedReason` | If present, do not claim final deployment success |

## Final reporting rules
Report one of these states exactly:

- `plan-only`: request normalized but no live execution attempted
- `funding handoff required`: funding branch is browser-assisted or unsupported for autonomous send
- `feeds funded; waiting for propagation`: funding/proxy tx sent but live readiness not yet proven
- `market deployment ready`: feeds are live and deploy artifacts are ready, but no verified live market yet
- `verification-ready`: deployment exists but final verification is pending or incomplete
- `completed`: `phase === "completed"` and `verifyResult.verified === true`
- `blocked`: any hard blocker prevents continuation

## Minimum success predicate
Only report full success when all are true:

```json
{
  "phase": "completed",
  "blockersEmpty": true,
  "feedsLiveOrPropagationReady": true,
  "deploySendCompleted": true,
  "verifyResultVerified": true,
  "agentDecisionSuccessClaimAllowed": true,
  "rollbackPlanInspected": true
}
```

If one field is absent, say which artifact is missing instead of guessing.

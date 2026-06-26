# EVK wrapper summary contract

Use this contract to interpret `run-evk-workflow` output and any persisted artifact bundle. Prefer exact fields over narrative text.

## Recommended files in a persisted run bundle
When `artifacts.enabled === true`, expect at least:

- `request.json`
- `status.json`
- `response.json`
- `summary.json`
- `agent-decision.json`
- `rollback-plan.json`

Depending on how far the workflow progressed, expect some or all of:

- `plan-market.json`
- `ensure-feeds.json`
- `feed-funding.json`
- `prepare-euler-oracle.json`
- `prepare-evk-market.json`
- `prepare-evk-deployment.json`
- `deploy-evk-market.json`

## Primary status fields
Read `agent-decision.json` first when it exists, then `summary.json`, then `status.json`.

### Agent decision fields

| Field | Meaning | Safe interpretation |
| --- | --- | --- |
| `safeStatus` | model-friendly state enum/string | use as the top-line recovered state |
| `canContinue` | whether the run can continue without first resolving blockers | false means stop or ask/user action is required |
| `nextCommand` | preferred next command when one exists | use after checking approvals and `mustNotDo` |
| `mustNotDo[]` | hard safety reminders | do not violate these |
| `successClaimAllowed` | final-success gate | must be `true` before claiming deployment-complete success |

### Summary fields

| Field | Meaning | Safe interpretation |
| --- | --- | --- |
| `phase` | deepest workflow phase reached | supporting stage summary |
| `status` | model-friendly wrapper status | useful shorthand, not a replacement for evidence |
| `rollbackPlan` | local-only vs forward-only onchain state | inspect before rerunning or handing off |
| `nextSteps[]` | generated next actions | use for guidance and resume decisions |
| `successClaimAllowed` | deployment-success gate from the persisted bundle | false means do not overclaim |

### Status fields

| Field | Meaning | Safe interpretation |
| --- | --- | --- |
| `phaseReached` | deepest workflow stage reached | use as the stage headline |
| `state` | model-friendly state enum/string | use as the primary short status |
| `recipeId` | selected EVK recipe | report exactly, do not infer another |
| `fundingExecutionState` | funding branch summary | distinguish not-needed, executable, browser-assisted, unsupported |
| `executable` | machine flags for feed, oracle, EVK, real send | use for readiness, not success |
| `blockers[]` | hard blockers | non-empty means stop or report blocked |
| `warnings[]` | cautionary notes | surface relevant live-send warnings |

## Artifact persistence fields
If the wrapper result exposes `result.artifactPersistence`, read:

| Field | Meaning | Safe interpretation |
| --- | --- | --- |
| `enabled` | whether persistence was requested | false means no durable run bundle exists |
| `persisted` | whether files were actually written | must be true for a durable evidence claim |
| `bundleDir` | run bundle path | report it when follow-up work depends on it |
| `files.*` | per-stage artifact files | inspect the stage file you are making claims about |

## Funding gates
Use these fields when funding is involved:

| Field | Success gate |
| --- | --- |
| `status.fundingExecutionState` | tells you whether funding was not-needed, executable, browser-assisted, or unsupported |
| `result.feedFunding.entries[]` | inspect per-feed blockers, browser plans, or execution outputs |
| `result.ensureFeeds.final.ready` | must be `true` before moving into oracle + EVK deployment claims |

Important: a funding path being executable is not the same as feeds being live. Require the final feed-readiness result.

## Deployment gates
Use these fields when deployment is in scope:

| Field | Success gate |
| --- | --- |
| `result.prepareEvkDeployment.ready` | deployment bundle is coherent enough to continue |
| `status.executable.evkMarket` | EVK market transaction is concrete enough for execution |
| `status.executable.realSend` | wrapper is ready for live send, not proof that live send already happened |
| `result.deployEvkMarket.executionSummary` | inspect dry-run vs broadcast-ready vs live-send outcome |
| `result.deployEvkMarket.stepResults[]` | inspect the exact planned or executed steps |

A deployment is not automatically successful just because `status.executable.realSend === true`. That is only readiness.

## Borrow-proof gates
If the user asked for proof of borrowability, require a separate proof result.

Deployment success and borrowability proof are different claims:
- `deployed but borrow-proof pending`
- `live borrow proven`

Do not collapse them.

## Final reporting rules
Report one of these states exactly:

- `plan-only`
- `feed-ready but awaiting activation/funding handoff`
- `funding dry-run ready`
- `browser-assisted funding ready`
- `oracle-executable`
- `EVK dry-run ready`
- `real-send ready`
- `deployed but borrow-proof pending`
- `live borrow proven`
- `blocked`

## Persisted-run helper commands
Use these helpers against a stored run directory:

- `explain-next --run-dir <dir>` → recover the model-friendly current state, next command, and guardrails
- `verify-evk-deployment-handoff --run-dir <dir>` → verify the deploy bundle is coherent enough for handoff or proof follow-up
- `run-evk-workflow --resume-from-run-dir <dir>` → reopen a known run instead of reconstructing it from memory

## Minimum deployment-success predicate
Only report deployment success when all are true:

```json
{
  "artifactBundlePersisted": true,
  "statusBlockersEmpty": true,
  "finalFeedsReady": true,
  "deployStagePresent": true,
  "deployEvidenceInspected": true,
  "agentDecisionSuccessClaimAllowed": true,
  "handoffVerificationPassedWhenHandingOff": true,
  "rollbackPlanInspected": true
}
```

If borrowability was requested, add a separate proof predicate instead of silently assuming it from deployment artifacts.

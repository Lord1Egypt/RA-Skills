# Footer Contract

Every round MUST end with this exact footer shape:

```text
LOOP_STATUS: <continue|blocked|milestone_reached|needs_human|repo_broken|exhausted>
NEXT_SLICE: <one concrete next slice or none>
VERIFY_BUILD: <exact command or none>
VERIFY_SLICE: <exact command or none>
REPO_STATE: <clean|dirty|broken|unknown>
COMMIT_SHA: <sha-or-none>
BLOCKER_BUCKET: <repo_state|auth|tool_hang|test_gap|unclear_spec|external_dependency|governance_conflict|contract_drift|mainline_exhausted|none>
RESTART_SLICE: <one restart slice or none>
EXECUTION_MODE: <single-agent|multi-agent-read-heavy|multi-agent-split-write>
COORDINATOR_ROLE: <role-or-none>
AGENT_COUNT: <integer>
STOP_REASON: <reason or none>
```

## Rules

- `NEXT_SLICE` MUST be one concrete slice when `LOOP_STATUS=continue`.
- `NEXT_SLICE` MUST be `none` when `LOOP_STATUS=exhausted`.
- `BLOCKER_BUCKET` MUST be `none` on successful continuation.
- `STOP_REASON` MUST be `none` when `LOOP_STATUS=continue`.
- `RESTART_SLICE` SHOULD be populated on blocked rounds unless exhaustion makes restart meaningless.
- `EXECUTION_MODE` MUST describe the integrated round, not a helper-local action.
- `AGENT_COUNT` MUST count coordinator plus helpers.

## LOOP_STATUS Meanings

- `continue`: start the next round from `NEXT_SLICE`
- `blocked`: stop until the blocker changes
- `milestone_reached`: stop because the intended checkpoint was completed
- `needs_human`: stop because human clarification, permission, or reframing is required
- `repo_broken`: stop because repo state is not trustworthy enough to continue
- `exhausted`: stop because the current mainline no longer yields a credible next tiny slice

## BLOCKER_BUCKET Meanings

- `repo_state`: repo integrity or git state blocks continuation
- `auth`: credentials or permission gates block safe continuation
- `tool_hang`: tooling stalled or behaved unreliably enough to stop the round
- `test_gap`: required proof is missing and cannot be added safely inside the slice
- `unclear_spec`: product clarification is required
- `external_dependency`: an external system or environment is the blocker
- `governance_conflict`: helper scope or integration authority was ambiguous
- `contract_drift`: loop contract and supervisor contract are incompatible
- `mainline_exhausted`: the current mainline no longer yields a credible next tiny slice
- `none`: successful continuation round

# Validator Schema
#tags: skills review

This file mirrors the inline runtime validation contract in `SKILL.md`.
If this file drifts from the inline contract, block release and synchronize it.

## Minimum required block fields
- `ROUND`
- `TOPIC`
- `MODE`
- `SESSION`
- `DECISION`
- `VALIDATION_STATUS`
- `PATCH_STATUS`
- `CONTINUATION_SIGNAL`
- `NEXT_ACTION`
- `CHAT_CONTINUITY`
- `RESUME_SNIPPET`

## Manual validation checklist
- the round block includes every minimum required field and is emitted exactly once at the end of the round after synthesis and decision
- the `MODE` matches the routed task type
- the `SESSION` is stable for the current topic
- consultant-bearing rounds require all three status enums: `SELF_POSITION_STATUS`, `CONSULTANT_POSITION_STATUS`, and `SYNTHESIS_STATUS`
- in consultant-bearing rounds, those three status fields appear together immediately after the minimum block in the exact order `SELF_POSITION_STATUS` -> `CONSULTANT_POSITION_STATUS` -> `SYNTHESIS_STATUS`
- if consultant extraction exhausted the allowed retry and the round explicitly downgraded out of consultant-bearing execution, `CONSULTANT_POSITION_STATUS: omitted-invalid` is valid to preserve the contiguous status block invariant
- `VALIDATION_STATUS` is mandatory in the emitted round block and must resolve before accepted `PATCH_STATUS`
- if `PATCH_STATUS` is `proposed`, `applied`, `re-reviewed`, or `deferred`, a `PATCH_MANIFEST` exists
- if `PATCH_STATUS` is `none` and no patch blocker exists, `PATCH_MANIFEST` may be omitted
- if `CONTINUATION_SIGNAL` is `stop`, no accepted but unpatched fix remains
- if `VALIDATION_STATUS: failed` or `blocked`, packaging and publishing stay blocked
- if `MODE: skill-publish-readiness`, `TEST_STATUS` and `VERIFICATION_EVIDENCE` must be present in the extended block for a publish-gate-valid round
- if `ORCHESTRATOR_MODE: local`, then `CONSULTANT_POSITION_STATUS: not-applicable` is the only valid consultant status and satisfies the mandatory status-field invariant
- if `ORCHESTRATOR_MODE: api` or `multi`, then `CONSULTANT_POSITION_STATUS: not-applicable` is invalid for a consultant-bearing round
- if `SYNTHESIS_STATUS` is missing in a consultant-bearing round, validation must fail or the round must be explicitly narrowed out of consultant-bearing execution
- if the routed task is `artifact-review`, `artifact-improvement`, `skill-review`, `skill-rewrite`, `skill-hardening`, or `skill-publish-readiness` and the artifact has a clear native mission, validation/review evidence must not treat `already good`, `already published`, or `already validated` as sufficient closure by themselves; a real strengthening path or an explicit structural deferral must exist
- if strong current-date optimization, latest-practice, state-of-the-art, trend-aware, or materially-improved-against-current-external-practice claims are made while an allowed internet-capable consultant/orchestrator is available and the task materially benefits from current-date external research, validation must require live relevant public internet evidence or an explicit narrowed state such as `BLOCKEDSTATE: current-date-trend-not-grounded` or `offline-only-provisional-not-verified-against-current-public-trends`
- if the task is in-scope current-date-sensitive work and consultant-bearing review is used while an allowed internet-capable consultant/orchestrator is available, validation must require the round-1 / round-2 internet-assisted minimum floor or an explicit honest narrowing; validation must reject early convergence that skips that floor
- validation must reject subordinate support surfaces that weaken, soften, or silently omit the current-date trend-grounding hard-lock family while presenting themselves as aligned with the live inline contract
- shortcut consultant output in consultant-bearing rounds must still satisfy the consultant-shaped minimum: `consultant_verdict`, `strongest_finding`, and `proposed_fix`
- validation must reject consultant-bearing rounds that treat decision-style consultant output as the default consultant shape
- if the three consultant-bearing status fields are present but not emitted as one contiguous block immediately after `RESUME_SNIPPET` in the exact order `SELF_POSITION_STATUS`, `CONSULTANT_POSITION_STATUS`, `SYNTHESIS_STATUS`, validation must fail for emission-order drift

## Release-blocker rule
Validator failures caused by drift between `SKILL.md`, this file, and `references/round-output-contract.md` are release blockers.

## Pass rule
Validation passes only if every checklist line above is true.

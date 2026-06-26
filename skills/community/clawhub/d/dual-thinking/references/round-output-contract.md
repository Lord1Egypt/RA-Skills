# Round Output Contract
#tags: skills review

This file mirrors the inline runtime authority in `SKILL.md`.
If this file ever drifts from the inline contract, the inline contract wins and this file must be synchronized before release.

## Minimum Required Round Block
Emit this fully populated block exactly once at the end of the round, after synthesis and decision.

```text
ROUND: <N>
TOPIC: <slug>
MODE: <mode>
SESSION: <session>
DECISION: <take|keep|merge|reject|defer>
VALIDATION_STATUS: <passed|failed|blocked|not-applicable>
PATCH_STATUS: <none|proposed|applied|re-reviewed|deferred>
CONTINUATION_SIGNAL: <continue|stop|missing|ambiguous>
NEXT_ACTION: <one clear next step>
CHAT_CONTINUITY: <new|reused|recovery>
RESUME_SNIPPET: |
  ROUND: <N>
  TOPIC: <slug>
  MODE: <mode>
  SESSION: <session>
  NEXT_ACTION: <one clear next step>
```

Immediately after the minimum block, emit this contiguous status block when `ORCHESTRATOR_MODE` is `api` or `multi`:
1. `SELF_POSITION_STATUS`
2. `CONSULTANT_POSITION_STATUS`
3. `SYNTHESIS_STATUS`

In `local` mode, `CONSULTANT_POSITION_STATUS: not-applicable` satisfies the mandatory status-field invariant.

## Extended Round Block
Add these only when they materially help review accuracy, recovery, validation, or publish gates.
- `SKILL_CLASS`
- `ORCHESTRATOR`
- `ORCHESTRATOR_MODE`
- `SELF_POSITION` or `SELF_POSITION_COMPACT`
- `CONSULTANT_POSITION` or `CONSULTANT_POSITION_COMPACT`
- `SYNTHESIS` or `SYNTHESIS_COMPACT`
- `CONSULTANT_QUALITY`
- `COMPARISON`
- `DOC_STATUS`
- `TEST_STATUS`
- `VERIFICATION_EVIDENCE`
- `PUBLISH_STATUS`

Because `VALIDATION_STATUS` is mandatory in the minimum required round block, it is no longer extended metadata. For `skill-publish-readiness`, `TEST_STATUS` and `VERIFICATION_EVIDENCE` are conditionally mandatory gate fields.

## Validation alignment notes
- Inline authority lives in `SKILL.md`, not here.
- This file mirrors field names, ordering, and emission expectations for validators, tests, and packaging.
- If a consultant-bearing round omits any of the three contiguous status fields, validation fails.
- If a consultant-bearing round emits those three fields outside the contiguous block immediately after `RESUME_SNIPPET`, validation fails.
- If `PATCH_STATUS` is `proposed`, `applied`, `re-reviewed`, or `deferred`, a `PATCH_MANIFEST` is required.
- If `VALIDATION_STATUS: failed` or `blocked`, packaging and publishing stay blocked.

## Compact forms for weak models
```text
SELF_POSITION_COMPACT:
- verdict: <...>
- weakness: <...>
- fix: <...>

CONSULTANT_POSITION_COMPACT:
- consultant_verdict: <...>
- strongest_finding: <...>
- proposed_fix: <...>

SYNTHESIS_COMPACT:
- relation: <aligned|partial|divergent>
- decision: <...>
- next_action: <...>
```

Compact is allowed. Skipping self -> consultant -> synthesis is not.

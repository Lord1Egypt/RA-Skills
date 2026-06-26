# Tests

## Minimal round-flow test
Run:

```bash
bash tests/test_round_flow.sh
```

Purpose:
- verify the sample round block includes required fields
- verify applied patches include a `PATCH_MANIFEST`
- verify a `stop` signal does not coexist with an unapplied proposed patch

## Weak-model shortcut fixture
Run:

```bash
bash tests/test_weak_model_shortcut.sh
```

Purpose:
- verify the simplified weak-model shortcut round still emits the minimum resumable state

## Multi-orchestrator alternation test
Run:

```bash
bash tests/test_multi_alternation.sh
```

Purpose:
- verify the skill documents `STATE_SNAPSHOT` for `ORCHESTRATOR_MODE: multi`
- verify examples mention `SYNC_POINT`
- verify packaging includes the multi-alternation test

## Reference alignment test
Run:

```bash
bash tests/test_reference_alignment.sh
```

Purpose:
- verify release-significant reference text stays aligned across `SKILL.md`, `references/modes.md`, `references/runtime-contract.md`, and `references/examples.md`
- verify multi-orchestrator and round-limit wording does not drift across documents
- verify the current-date trend-grounding hard-lock family is reflected in the lower support surfaces that must mirror the live inline contract
- verify the lower support surfaces preserve the round-1 / round-2 internet-assisted minimum floor for in-scope current-date-sensitive work
- verify grounding-sensitive conclusions require an explicitly labeled visible `GROUNDING_EVIDENCE:` or `BLOCKED_STATE:` record rather than hidden or unlabeled mention
- verify omission of that required visible label fails closed as `VALIDATION_STATUS: blocked` with `BLOCKED_STATE: grounding-evidence-not-labeled`
- verify fresh/recovery/replacement consultant sessions have no excerpt rights until visible baseline repaste is proven in that same session
- treat this as a required publish-gate check, not an optional doc nicety

## Validation rollback test
Run:

```bash
bash tests/test_rollback_on_validation_failure.sh
```

Purpose:
- verify the publish checklist requires rollback-test coverage
- verify the runtime contract documents rollback-on-validation-failure behavior
- verify the main skill text requires reverting to the last passed artifact after failed validation

## Self-evolution alignment test
Run:

```bash
bash tests/test_self_evolution_alignment.sh
```

Purpose:
- verify the active line is explicitly a candidate/reference-verified line rather than a silently mutated frozen release line
- verify self-evolution doctrine is synchronized across `SKILL.md`, `references/self-evolution-lens.md`, `references/reference-scenarios.md`, `references/modes.md`, `references/change-policy.md`, and `references/runtime-contract.md`
- verify the self-evolution support surfaces include the live-public-evidence requirement introduced by the current-date trend-grounding lock family
- verify self-evolution support surfaces acknowledge the round-1 / round-2 internet-assisted minimum floor when current-date-sensitive work is in scope

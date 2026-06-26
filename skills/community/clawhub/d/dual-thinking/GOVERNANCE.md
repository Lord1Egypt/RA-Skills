# Dual Thinking Governance

This file is non-runtime governance and release policy for the `dual-thinking` skill line.
It does not override the executable runtime law in `SKILL.md`.

## Reference freeze policy

```text
`v8.5.9` is the frozen prior reference-release line.
`v8.5.24` is the active candidate line for the grounding-evidence fail-closed consequence hardening pass on top of the grounding-evidence visibility line.
Historical accepted checkpoint: `v8.5.13` is the prior published reference-release line before the support-surface sync publish.
Historical accepted checkpoint: `v8.5.11` is the older frozen prior reference-release line.
Historical accepted checkpoint: `v8.5.8` is the older frozen prior reference-release line.
Historical compatibility marker: `v8.5.7` is the frozen prior reference-release line.

Freeze rules:
- Do not introduce new architectural stages into the runtime flow unless a required scenario test fails.
- Do not expand the public runtime contract only because a formulation could be more elegant.
- Do not merge backlog ideas into the reference line without a concrete failing scenario, validation gap, or publish blocker.
- Treat wording-only, formatting-only, and consistency-only edits as non-architectural maintenance.
- Treat subordinate support-surface sync work that only aligns reference/test/evidence/governance surfaces to already-live inline hard locks as non-architectural maintenance.
- Treat any change that modifies flow order, required round structure, validation semantics, mode behavior, consultant roles, or the inline hard-lock family itself as a structural change.

Allowed changes in the frozen reference line:
- wording clarification
- formatting cleanup
- validator/reference synchronization
- bug fixes for proven scenario failures
- publish/packaging corrections
- explicit contradiction removal

Disallowed changes in the frozen reference line unless a required scenario test fails:
- new runtime stages
- new public modes
- new mandatory round fields
- new patch-state layers
- new orchestration branches
- new consultant roles beyond the existing architecture
```

Structural changes after the reference freeze must go to the next planned line unless a required scenario test demonstrates a real defect in the current line.

## Reference release criteria

```text
The current line may be promoted from `reference-candidate` to `reference-release` only if all are true:
- the runtime architecture remains unchanged across the final validation pass
- `references/round-output-contract.md` is fully aligned with `SKILL.md`
- `references/validator-schema.md` is fully aligned with `SKILL.md`
- the required scenario tests pass
- required scenario evidence is recorded in `references/verification-evidence.md` and `references/reference-test-log.md`
- no unresolved contradiction remains between weak-model shortcut and normal consultant-bearing flow
- no unresolved contradiction remains between mode-specific execution and the shared closing tail
- no unresolved contradiction remains in publish/readiness semantics for the current scope
- no unresolved contradiction remains between the live inline current-date trend grounding lock family and the subordinate reference/evidence/test surfaces
```

## Reference validation status

```text
Reference-line validation states:
- `reference-candidate` -> architecture frozen, scenario evidence not yet fully recorded or required scenarios not yet fully passed, or publication/release sync still pending
- `reference-verified` -> architecture frozen, required scenarios passed, and evidence recorded
- `reference-release` -> reference-verified and accepted as the current reference line
- `reference-superseded` -> a later reference line replaced it
```

## Backlog discipline

```text
After the line is frozen, new ideas must be classified before editing the runtime contract:
- `bugfix`
- `clarification`
- `structural`
- `experimental`
```

## Done enough rule

```text
The line is "done enough" when:
- no structural contradiction remains
- all required scenarios pass
- all remaining edits are wording-only, formatting-only, or packaging-only
- new ideas no longer improve a failing scenario in the current line
```

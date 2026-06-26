# Reference Freeze
#tags: skills review

## What the frozen line means
The frozen line is the current reference-candidate or reference-release branch of the skill.
Its purpose is stability, comparability, and publish discipline.
The frozen line should not absorb speculative architecture improvements just because they sound better.
For Dual Thinking specifically, `v8.5.9` is the frozen prior reference-release line and `v8.5.24` is the active frozen reference-candidate line after the grounding-evidence fail-closed consequence hardening pass.

## What can still change
Allowed changes in the frozen line:
- wording clarification
- formatting cleanup
- validator and reference synchronization
- bug fixes for proven scenario failures
- publish and packaging corrections
- explicit contradiction removal

## What counts as structural
Treat a change as structural if it changes any of these:
- runtime order
- required round fields
- validation semantics
- mode behavior
- consultant roles
- orchestration branching

Structural changes do not belong in the frozen line unless a required scenario test proves the current line is defective.
Self-evolution doctrine that materially changes self-review stance, consultant challenge shaping, or synthesis pressure counts as structural even if it preserves the public three-step architecture.

## Demotion rules
Demote the line from `reference-verified` or `reference-release` back to `reference-candidate` when any of these becomes true:
- a required scenario test fails
- required scenario evidence is missing or stale
- validator and reference docs drift apart
- weak-model and normal consultant-bearing behavior contradict each other
- publish readiness semantics become inconsistent for the current line

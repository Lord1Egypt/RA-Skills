# Backlog — Next Line
#tags: skills review

These ideas are intentionally excluded from the frozen `v7.9.14` reference line.
Add them only in a future line if a failing scenario, validator gap, or packaging blocker justifies structural work.

## Structural ideas deferred
- richer validator automation that checks scenario semantics beyond the current shell fixtures
- optional machine-readable evidence schema in addition to markdown evidence logs
- expanded recovery metadata if future multi-round failures show the current `STATE_SNAPSHOT` shape is insufficient
- tighter publish automation that derives release readiness directly from evidence artifacts

## Implemented in the `v8.0.x` line before promotion to reference-release
- self-evolution / outside-self doctrine for self-review and native-domain-adjacent review
- explicit freeze-compatibility routing that keeps `v7.9.14` frozen while structural self-evolution work lands in the next line
- reference-boundary hardening so inline canonical rules outrank contradictory or expanding reference content
- validator/publish-surface hardening that preserves fallback status continuity and makes validation-result emission explicit

## Optional enhancements deferred
- more worked examples for unusual `analysis-only` narrowing cases
- additional non-skill artifact examples
- cosmetic reorganization of long reference sections without changing meaning

## Explicit freeze reminder
Do not merge backlog ideas into `SKILL.md` or the frozen runtime contract unless a required scenario actually fails or a reference contradiction appears.

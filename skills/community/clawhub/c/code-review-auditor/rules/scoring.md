# Scoring Models

Apply these models consistently across findings and summaries.

## Severity

- `Critical`: likely exploitable security issue, data loss/corruption, privilege bypass, production outage, irreversible financial/legal impact.
- `High`: serious defect or vulnerability with realistic trigger; major reliability, privacy, integrity, or scaling impact.
- `Medium`: meaningful defect risk, maintainability drag, performance issue, or architectural problem that can cause future regressions.
- `Low`: localized issue, clarity problem, minor inefficiency, or weak test/observability gap.
- `Info`: observation, tradeoff, or improvement idea without clear current risk.

## Confidence

- `High`: directly supported by code, tests, config, or deterministic reasoning.
- `Medium`: likely based on code evidence but depends on runtime behavior, data shape, or external configuration.
- `Low`: plausible concern requiring confirmation; label as potential false positive.

## Effort

- `XS`: minutes; localized edit.
- `S`: less than half a day; small focused change.
- `M`: one to two days; touches several files or requires tests.
- `L`: multiple days; shared abstraction, migration, or cross-module behavior.
- `XL`: project-level initiative requiring staged rollout.

## Priority

Priority combines severity, confidence, reach, exploitability, user impact, and effort.

- `P0`: address immediately; active or highly likely severe impact.
- `P1`: address before release or next production change.
- `P2`: schedule soon; meaningful but not release-blocking.
- `P3`: opportunistic improvement.

## Refactorability Score

Score from 0 to 100 for each meaningful finding or hotspot.

- `0-20`: do not refactor now; risk exceeds benefit or evidence is weak.
- `21-40`: refactor only when touching related code.
- `41-60`: useful targeted refactor with contained risk.
- `61-80`: strong candidate; reduces real complexity or defect risk.
- `81-100`: urgent structural improvement; high risk/impact and clear path.

Consider:

- behavior preservation difficulty
- test coverage and observability
- blast radius
- coupling/fan-in/fan-out
- production criticality
- migration/rollback path
- clarity of desired design
- amount of speculative abstraction

## Overall Scores

For `metrics/score.md`, provide:

- `Risk Score`: 0-100, higher means more operational/security/defect risk.
- `Maintainability Score`: 0-100, higher means easier to maintain.
- `Security Posture`: `Strong`, `Adequate`, `Needs Attention`, or `High Risk`.
- `Test Confidence`: `Strong`, `Adequate`, `Thin`, or `Unknown`.
- `Refactorability`: 0-100, project-level weighted average of actionable refactor candidates.

Do not imply mathematical precision. Explain the main drivers.

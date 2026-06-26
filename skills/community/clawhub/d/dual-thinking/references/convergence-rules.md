# Convergence Rules
#tags: skills review

## Stop only when all are true
- the consultant explicitly says another round is not worth it
- you also agree
- no meaningful next improvement remains
- no accepted but unpatched fix remains
- no runtime-critical ambiguity remains for the asked scope
- no must-have docs remain for the asked scope
- no must-have tests remain for the asked scope
- no unresolved blocker remains for the asked scope
- round count has not exceeded `MAX_ROUNDS` for the current flow unless the user explicitly extended it

## Meaningful round rule
A round is meaningful only if at least one of these happened:
- a grounded flaw was identified
- a decision changed or was defended with explicit reasoning
- a real patch was accepted or applied
- a concrete risk was surfaced
- a validated stop signal was explicitly produced
- a real `SELF_POSITION` materially influenced the final decision

If none of those happened, the round is non-meaningful.
Do not count it as convergence.
Narrow the next prompt or switch mode according to failure rules.

`SELF_POSITION` alone is not enough in `api` or `multi` when consultant input was required and available.
`SYNTHESIS` must still exist.

## Skill-task closure checklist
For skill topics, stop only if all are true for the asked scope:
- `CONTINUATION_SIGNAL: stop`
- you also agree
- no accepted fix remains unpatched
- no runtime-critical ambiguity remains
- no must-have docs remain missing
- no must-have tests remain missing
- no unresolved blocker remains

## Publish readiness lifecycle
Use one of these statuses:
- Draft
- Reviewed
- Hardened
- Validated
- Packaged
- Published
- Deferred

## Validation and publish coupling
- `PUBLISH_STATUS` can be `Packaged` or `Published` only if `VALIDATION_STATUS: passed`.
- If validation has not passed, keep `PUBLISH_STATUS` at `Draft`, `Reviewed`, `Hardened`, `Validated`, or `Deferred`.
- If `VALIDATION_STATUS: failed`, packaging and publishing are blocked.

## Practical rule
If the task is a skill rewrite or skill hardening task, do not stop at a nice answer. Stop at the farthest gate the user asked for and the artifact actually reached.

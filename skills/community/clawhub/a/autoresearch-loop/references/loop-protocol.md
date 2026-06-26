# Loop Protocol

## Run Contract

Before any edit, confirm and record:

- goal, metric, baseline, and target
- exact VERIFY command
- exact GUARD command
- allowed edit scope and forbidden paths
- rollback strategy
- run mode and iteration cap
- external research policy
- private-data boundary

Do not start until the user approves the contract.

## Full Loop (per iteration)

1. **Review state** — read the approved contract, git state, results log, lessons, and current metric
2. **Pick hypothesis** — one atomic change that could improve the metric
3. **Check scope** — confirm the planned edit is inside approved scope and does not touch forbidden paths
4. **Make the change** — one logical change, one concern
5. **Snapshot/commit** — record only current-loop changes before verification
6. **Run VERIFY** — execute the approved verify command. Did the metric improve?
7. **Run GUARD** — execute the approved guard command. Did anything regress?
8. **Decide** — keep, rework, discard, or stop according to SKILL.md
9. **Log** — append one row to results log before starting the next iteration
10. **Health check** — check discard streak, cap, scope, and escalation ladder
11. **Continue** — or stop if a terminal condition is reached

## Terminal Conditions

Stop when ANY of the following is true:

- Goal metric reaches target
- Approved iteration cap reached
- Soft blocker triggered
- Manual stop requested
- Verify or guard command is no longer valid
- Rollback is unsafe
- Required edit is outside approved scope
- External research is needed but was not approved
- Private data would need to be exposed externally

## What NOT to Do

- Never start without an approved run contract
- Never make more than one logical change per iteration
- Never skip logging before starting the next iteration
- Never modify guard files unless the user updates the scope contract
- Never pause mid-loop to ask the user unless a safety gate, blocker, or contract change is needed
- Never assume a change worked without running verify
- Never push, deploy, publish, or touch production systems unless explicitly approved for this run
- Never paste private code, secrets, logs, customer data, or proprietary data into external services

## Results Log Format

```text
iteration  snapshot  metric  delta  status   description
0          baseline  47      0      baseline initial state
1          def456    41      -6     keep     fixed auth module types
2          ghi789    49      +8     discard  generic wrapper made things worse
3          jkl012    38      -3     keep     type-narrowed API handlers
```

- `status`: baseline / keep / discard / skip / pivot / refine / blocker
- Log is an autoresearch-owned artifact
- Commit the log only if the user explicitly asks
- Print progress summary every 5 iterations or at the approved cadence
- Print baseline-to-best summary at run completion

## Rollback Strategy

Default: use a normal version-control revert of only the current-loop change. In an explicitly isolated branch/worktree/disposable copy, a hard reset may be approved in the run contract. The results log remains the audit trail regardless.

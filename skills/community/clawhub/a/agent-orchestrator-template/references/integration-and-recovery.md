# Integration and Recovery Decisions

After every sub-agent returns, the orchestrator must decide how to proceed. This guidance works with the acceptance template to ensure the main agent either integrates the return cleanly or repairs or reroutes as needed.

## Decision Paths

1. **Accept as-is**
   Use this when the returned artifact matches the task contract, all verification checks pass, and no further dependencies are blocked.
2. **Repair locally**
   Use this when the artifact is mostly correct but needs a small local adjustment such as formatting, a doc fix, or a narrow change that is cheaper than re-dispatching.
3. **Reroute**
   Use this when the deliverable deviates materially from the contract but a different agent or a tighter contract can still recover the task.
4. **Local takeover**
   Use this when the task is urgent, the delegated work is blocked, or another round-trip would cost more than taking control directly.

## How To Choose

Use this sequence after every delegated return:

1. Compare the returned work against `expected_output`
2. Check boundary compliance against `owned_scope` and `forbidden_scope`
3. Review verification evidence
4. Check whether downstream tasks are still blocked
5. Choose one of: accept, repair, reroute, takeover

## Verification and Evidence

- Capture what checks were run and their outcomes.
- If verification is missing, do not accept the result as complete.
- If rerouting or repair is needed, list the exact gap so the next action stays focused.
- Preserve traceability to earlier work when a task is retried or rerouted.

## Integration Log Template

```text
Sub-task: [name]
Decision: [accept / repair / reroute / takeover]
Why: [reason for choice]
Actions: [merge details, repairs, new contract, takeover steps]
Verification: [checks run or pending]
```

## Example Scenario

- An `explore` task returns a plausible root cause but no reproduction steps.
- Acceptance finds the output relevant but incomplete.
- The orchestrator chooses `reroute` and issues a narrower follow-up contract for reproduction evidence.
- Once that evidence returns, the orchestrator can safely dispatch `implement` work or take over locally.

## Recovery Guidance

- Prefer `repair locally` when the missing work is small and well understood.
- Prefer `reroute` when the contract needs a better task type, domain, or tighter boundary.
- Prefer `local takeover` when time matters more than another delegation cycle.
- Record the failure mode so future routing rules can improve.

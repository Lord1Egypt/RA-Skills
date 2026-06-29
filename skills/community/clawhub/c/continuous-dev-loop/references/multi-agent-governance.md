# Multi-Agent Governance

## Allowed Roles

- `coordinator`
- `implementer`
- `verifier`
- `investigator`
- `reviewer`

## Role Rules

- The coordinator chooses the slice, assigns subwork, integrates outputs, and emits final continuation truth.
- The implementer writes code inside a bounded file or subsystem scope.
- The verifier runs checks, adds focused proofs when required, and rejects unsupported success claims.
- The investigator performs read-only tracing, repo archaeology, or failure analysis.
- The reviewer checks regressions, contract adherence, and residual risk.

## Topology Rules

- There MUST be exactly one coordinator.
- Helper scopes MUST be bounded before work starts.
- Parallel read-only exploration is allowed.
- Parallel writes require explicit non-overlapping ownership.
- If ownership overlaps, integration MUST be serialized through the coordinator.
- Final integrated verification MUST run after helper work is merged.

## Helper Report Shape

```text
ROLE: <implementer|verifier|investigator|reviewer>
SCOPE: <bounded task>
FILES_TOUCHED: <comma-separated paths or none>
RESULT: <what changed or what was learned>
VERIFY: <exact command run or none>
RISKS: <remaining concern or none>
RECOMMEND: <one concrete recommendation>
```

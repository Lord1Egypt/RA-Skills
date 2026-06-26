---
name: debugging
description: Diagnose failures using reproduce → isolate → fix → verify workflow.
metadata:
  author: RedHat Dev
  version: 1.0.0
  owner: RedHat Dev Agent
  category: quality
---

# SKILL: debugging

## Purpose
Diagnose errors with a deterministic workflow: reproduce â†’ isolate â†’ fix â†’ verify.

## When to Use
- Tests are failing.
- Runtime errors occur (stack traces, crashes, misbehavior).
- Performance regressions or unexpected output is reported.

## Inputs
- `symptom` (required, string): error message, failing test, or observed behavior.
- `repro_steps` (optional, string): how to reproduce.
- `logs` (optional, string): relevant logs/traces.
- `environment` (optional, object|string): OS, versions, env vars (no secrets).

## Steps
1. Reproduce deterministically:
   - capture exact command(s)
   - capture versions
2. Localize failure:
   - narrow to smallest failing unit/test
   - add targeted logging/diagnostics if needed
3. Form hypotheses and test them one by one.
4. Implement the smallest fix that resolves the root cause.
5. Add/adjust tests to prevent regression.
6. Verify:
   - original repro no longer fails
   - related tests still pass

## Validation
- Root cause is stated explicitly (not only the symptom).
- Fix is verified by test/repro.
- No unrelated behavior changes are introduced.

## Output
```yaml
root_cause: "<what broke and why>"
fix: "<what changed>"
verification: ["<commands/tests>"]
follow_ups: ["<optional hardening>"]
```

## Safety Rules
- Do not â€œfixâ€ by disabling tests or checks unless explicitly approved and justified.
- Prefer reversible debugging changes (guarded logs, small diffs).

## Example
Symptom: â€œ`TypeError: cannot read property 'x' of undefined` in production.â€
Output: root cause (missing null check), fix, and regression test.

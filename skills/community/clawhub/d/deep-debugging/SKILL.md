---
name: deep-debugging
description: Evidence-first debugging and incident triage for unclear, recurring, production-like, or high-risk software bugs. Use when the user asks for root cause analysis, says a fix did not work, reports 401/403/500 with context, deploy/runtime failures, broken integrations, or needs investigation before code changes. Do not use for obvious typos, missing installs, or trivial one-line fixes.
version: "2.2.0"
requiredEnv: []
permissions:
  - read:logs
  - read:env-keys
  - run:bash-readonly
security:
  restriction: read-only-by-default
  note: >
    This skill may inspect logs, commit metadata, dependency versions, endpoint status,
    and environment key names. Never print secrets, tokens, cookies, customer data,
    or raw production payloads. Any production write, deploy, rollback, database action,
    or external API change requires explicit user approval.
---

# Deep Debugging

**No guessing. No random fixes. Stabilize incidents first, then prove the root cause.**

## When to use

Use this skill for:
- unclear or recurring bugs
- user-facing/prod-like failures: `500`, broken login, failed deploy, red healthcheck
- auth/session bugs: `401`, `403`, cookie/JWT weirdness
- integrations/webhooks/rate limits/signature failures
- “still broken”, “same error”, “find root cause”, “debug this properly”

Do **not** use it for obvious compiler errors, typos, missing install/setup steps, or cosmetic UI tweaks.

## Operating contract

1. **Observe before editing.** No code/config changes before evidence + hypothesis.
2. **One hypothesis at a time.** If you cannot state the proof, you do not know the cause.
3. **Binary search the chain.** Split request → app → service → DB/API → response.
4. **Minimal reversible fix.** No drive-by refactors.
5. **Verify and prevent.** Test the exact failure path and document recurrence prevention.

## Workflow

```text
0. Incident Gate   → user/prod impact? stabilize first
1. Quick Triage    → obvious setup/runtime misses
2. Evidence        → exact error, repro, affected path, last change
3. Hypothesis      → one testable cause + one test
4. Narrow          → binary-search the failure chain
5. Fix             → smallest reversible change
6. Verify          → exact repro/test/build/log evidence
7. Prevent         → regression/monitoring/learning when recurring or prod-like
```

## Phase 0 — Incident Gate

If users, production, money flows, auth, data integrity, or external integrations are affected, switch to incident mode before debugging.

Output first:

```text
INCIDENT SNAPSHOT
Impact:     [who/what is affected]
Severity:   [low/medium/high/critical + why]
Started:    [time/commit/deploy if known]
Evidence:   [logs/status/metrics; redacted]
Stabilize:  [rollback, feature flag, pause job, monitor, or no-op]
Next step:  [one concrete diagnostic action]
```

Rules:
- High/critical production incidents: check rollback/feature flag before hotfix.
- Preserve evidence before redeploy/restart when possible.
- Production writes, rollbacks, migrations, credential changes, or third-party changes require explicit user approval.

For detailed incident checklists read `references/incident-first.md`.

## Phase 1 — Quick Triage

Check these before deeper analysis:

```text
□ Server/process restarted after config/code change?
□ Correct env file/keys present? Key names only, never values.
□ Dependencies installed/generated after package/schema changes?
□ Migration/schema state matches runtime?
□ Browser/client cache or stale build ruled out?
□ Repro uses test data, not live credentials/customer data?
```

If a quick triage item explains the issue, fix that minimally and still verify.

## Phase 2 — Evidence

Collect real proof:

```text
Error:       exact message/status/stack excerpt
Path:        endpoint/function/job/component
Repro:       minimal steps or request shape
Scope:       all users vs specific role/input/tenant/environment
Expected:    what should happen
Actual:      what happens
Last change: commit/deploy/config/schema/provider change
```

Optional helper: run `scripts/incident_snapshot.sh` locally to collect safe environment metadata. It prints env **key names only**, not values.

## Phase 3 — Hypothesis

State exactly one hypothesis before touching code:

```text
HYPOTHESIS: The failure happens because [specific cause],
which I will prove/disprove by [specific test].
```

Bad: “Something is wrong with auth.”
Good: “The 401 happens because the login token is set but not sent on `/me`, which I will prove by comparing the login response headers with the follow-up request headers.”

## Phase 4 — Narrow with binary search

Pick the chain and split it:

```text
Frontend → request creation → network → API gateway/middleware → controller → service → DB/external API → response → UI
```

After each test report:

```text
✅ Ruled out: [component] because [evidence]
❌ Found: [component] fails because [evidence]
```

For stack-specific checklists read `references/stack-checklists.md`.

## Phase 5 — Fix

Only after evidence supports the hypothesis:
- change the smallest surface area
- do not refactor unrelated code
- prefer reversible config/code changes
- keep secrets and production data out of logs/reports
- stop after 3 failed fix attempts and restart from evidence/hypothesis

## Phase 6 — Verify

Before saying done, provide evidence:

```text
DEBUG REPORT
Failure:      [exact issue]
Root cause:   [specific cause]
Proof:        [test/log/code evidence]
Fix:          [minimal change]
Verified:     [command/test/repro result]
Prevention:   [test/monitoring/doc/learning, or "not needed" + why]
Remaining:    [risk/blocker, or "none known"]
```

For report variants read `references/output-templates.md`.

## Phase 7 — Prevent recurrence

Required when the bug is production-like, recurring, security-adjacent, or took more than one hypothesis:

```text
□ Regression test or smoke test added/identified
□ Monitoring/logging improved or gap named
□ Runbook/rollback note captured for future incidents
□ Durable learning written if likely to recur
```

## Hard rules

- Never fix before hypothesis.
- Never test with real credentials or copy raw tokens/cookies/secrets.
- Never mix unrelated refactor with bug fix.
- Never claim root cause without proof.
- Never hide remaining risk.
- If meaningful optimization potential remains, mention it as `Next optimization:`.

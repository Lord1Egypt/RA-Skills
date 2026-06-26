# Phase 1 — Planner Template

Copy this into a scratch file, issue, or chat message at the start of any non-trivial task. Fill in every section before touching code.

---

## Task

> <one-sentence description of what is being asked>

## Task Breakdown

- [ ] <smallest independent sub-task>
- [ ] <smallest independent sub-task>
- [ ] <smallest independent sub-task>

## Hypothesis

> *I believe [symptom/requirement] is caused by / will be achieved by [cause/approach], because [evidence].*

**Examples:**

- *I believe the login redirect loops because the middleware reads `session` before next-auth writes the cookie on the `/api/auth/callback` response, because the network tab shows no `Set-Cookie` header on that response.*
- *I believe rate limiting on `/api/chat` is best implemented with a Redis sliding-window counter, because we already use Redis for sessions and in-memory state breaks on multi-instance Railway deployments.*

## Evidence

List concrete observations that support the hypothesis:

- <log output, test failure, code reading, reproduction>
- <log output, test failure, code reading, reproduction>

## Scope

**In-bounds** (files/modules the fix may touch):

- `<path/to/file>`
- `<path/to/file>`

**Out-of-bounds** (files/modules explicitly excluded):

- `<path/to/file>` — reason: <why not>
- any unrelated test file
- any dependency upgrade

## Success Criteria

How Phase 3 will verify this is fixed / complete:

- [ ] <concrete, verifiable outcome>
- [ ] <concrete, verifiable outcome>
- [ ] Build passes
- [ ] Type check passes
- [ ] Specific test: `<test name or command>` passes

---

## Quality Check

Before moving to Phase 2, verify:

- [ ] Hypothesis is **specific** (names exact files/functions/conditions)
- [ ] Hypothesis is **falsifiable** (can be proven wrong by observation)
- [ ] Hypothesis is **evidence-backed** (references something you actually observed)
- [ ] Scope is **explicit** (in-bounds AND out-of-bounds named)
- [ ] Success criteria is **verifiable** (not "it works")

If any box is unchecked, stay in Phase 1.

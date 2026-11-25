# Review Checklists

The YAGNI & DRY lens, the "spec written to match the implementation" failure, and the money/state checks.

## The YAGNI & DRY review

Every review - single-agent or not - should answer these five questions
explicitly. They catch a class of problem that functional testing never will,
because speculative code usually *works*.

1. **YAGNI.** Does the change add generality the task does not exercise -
   extra tables, config hooks, extension points, service objects, helpers?
   If the feature does not need it today, flag it. Severity `high` when it
   touches money, state, or auth; otherwise `medium`.
2. **DRY.** Is the same logic, concept, or validation duplicated? Severity by
   blast radius: `medium` for isolated duplication, `high` when the duplicated
   logic sits in a money, state, or auth path where the two copies will drift.
3. **Reinvented house component.** Did the change build a new helper or
   service when the codebase already has one? Check the shared/component
   directories before calling it duplication - a second implementation of
   something that exists is reinvention, and it will drift. Name the existing
   component to use.
4. **Unnecessary dependency or indirection.** Did the change add a package,
   wrapper, or conversion layer that the standard library, an already-installed
   dependency, or a few lines could replace? Severity `medium`; name the
   simpler option.
5. **Worse-is-better.** Did the change prefer a large configurable abstraction
   over a smaller concrete solution? If the abstraction makes the
   money/state/auth path harder to trace or test, flag `high`.

---

## The most valuable single lesson

**A test that passes because it works around a constraint is not a test.** The
most dangerous outcome of a review is a green suite that proves the wrong
thing.

The shape of this failure:

- The spec injects an extra parameter to get past a guard that the real
  client never sends.
- The spec asserts a count that the feature's own design makes wrong.
- The spec works around a NOT NULL constraint or unique index that production
  does not satisfy.
- The spec stubs the very method whose behavior is under test.

**When you see this, the spec is what is wrong - fix the production path.** Do
not adjust the expectation to match the behavior. Then write a probe that
exercises the endpoint exactly as the real client calls it, with the same
parameter shape and no test-only additions, and observe the actual result.

```text
# probe the real request shape, then report what actually happened
response = client.post("/resource", payload: real_payload)
puts "STATUS=#{response.status} SAVED=#{record.reload.flag?}"
```

If the probe shows the real request fails, that is a live production bug that
the spec was hiding. Fix the code, keep the probe as a regression test, and
delete the probe file before committing.

This is the reason a review has to read the *tests*, not just the
implementation.

---

## Money and state changes

If the change touches payments, state transitions, webhooks, or
audit-sensitive data, run these checks explicitly rather than hoping to notice
them.

- **Idempotency.** What happens if the same request arrives twice? Is there a
  unique constraint, or an idempotency key, or nothing?
- **Atomicity.** Can a partial state persist if a later step fails? Is the
  whole operation in a transaction, and does it cover everything that must
  not be half-done?
- **Double charge.** Is there any path where a retry charges again?
- **Negative or zero amounts.** Are they validated, and can a client send
  them?
- **Currency rounding.** Is rounding applied consistently, and is the total
  the sum of the parts?
- **Webhook authenticity.** Is the payload signature verified before the
  handler acts on it? Is the check replay-safe?
- **Audit trail.** Does the change leave a record of who did what, and can that
  record itself be modified?
- **Authorization.** Can one user's identifier be substituted for another's
  in a request?

Any hit here is `block-merge` or `high` by default.

---

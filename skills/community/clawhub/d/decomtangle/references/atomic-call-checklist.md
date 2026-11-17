# Reference — The atomic-call checklist

Six checks to run (mentally, instantly) before emitting any tool call inside a
multi-step procedure. A call that passes all six is safe to emit; a call that
fails any one gets decomposed first.

## The checklist

1. **Single verb.** Can I describe this call as one verb + one object?
   ("Navigate to X", "Click ref Y", "Read cell Z".) If the description needs
   "and" or "then", split it.

2. **Single observable outcome.** Will the result tell me whether this one
   action succeeded? If success would be invisible in the result, add the
   observation as the *next* call, don't skip it.

3. **No embedded control flow.** Arguments contain no loops, no `&&`/`;`
   sequencing over mutations, no sleep-and-retry, no conditionals. (A pure
   read-side pipe filter is the one allowed exception.)

4. **Quoting depth ≤ 1.** No quotes-inside-quotes-inside-args. Depth ≥ 2 →
   payload-to-file pattern or a native endpoint.

5. **Previous result consumed.** My choice of *this* call reflects what the
   *last* result actually said — not what I assumed it would say. If I haven't
   read it, read it now.

6. **Failure is local.** If this call errors, I know exactly what failed and
   the system state is knowable. For side-effecting calls: I know whether it
   is safe to retry, and I will verify (not assume) the effect before
   reporting it.

## Quick reference card

```
  VERB      one verb, one object
  OBSERVE   outcome visible in result
  FLOW      no loops / chains / sleeps in args
  QUOTE     nesting depth ≤ 1
  CONSUME   last result actually read
  LOCAL     failure diagnosable, retry decidable
```

## Milestone reporting

In any procedure longer than ~5 calls, or any procedure with side effects:
report progress at natural milestones (leg completed, mutation attempted,
verification done). A procedure must never end silently — if you stop, stopped
or stuck, say exactly where and what state the system was left in. Silence is
indistinguishable from a crash, and operators treat it as one.

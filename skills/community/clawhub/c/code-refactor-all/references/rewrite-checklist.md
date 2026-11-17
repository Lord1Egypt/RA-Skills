# Rewrite Checklist

A rewrite throws away code that already handles years of edge cases. It can be the right call, but only with a plan that recovers that knowledge before the old code is gone.

## Contents
1. Go / no-go · 2. Behavior inventory · 3. Building the new implementation · 4. Parity and cutover · 5. Rollback and deletion · 6. Rewrite anti-patterns

## 1. Go / no-go

Choose rewrite over incremental refactor only when at least one holds, and write down which:
- The platform/framework is dead or blocks required work (unsupported runtime, framework end-of-life, licensing).
- The code cannot be put under test without effectively rewriting it, and its surface is small enough to re-specify.
- The user explicitly asked for a rewrite and understands the trade-off.

Red flags that argue for incremental refactoring instead:
- The component is large, central, and still changing weekly.
- Nobody can list what it does; there are no tests and no access to production samples.
- The motivation is mainly taste ("it's ugly", "I'd do it differently").

If you proceed despite red flags, say so in the plan and keep the new code shippable in slices (strangler) rather than as one big switch.

## 2. Behavior inventory (definition of done)

List before writing new code; this list becomes the parity checklist.
- [ ] Public entry points: functions, classes, routes, CLI commands/flags, events, scheduled jobs.
- [ ] Inputs and outputs per entry point, including formats (JSON shape, field order if consumers care, encodings, number formatting).
- [ ] Error behavior: which errors, types/codes/messages, retries, partial failure handling.
- [ ] Side effects and their order: DB writes, files, network calls, emitted events, cache invalidation.
- [ ] Configuration and environment variables read; defaults when missing.
- [ ] Operational hooks: logs others parse, metrics names, tracing spans, health checks.
- [ ] Performance envelope: latency/throughput/memory the callers rely on.
- [ ] Known quirks and bugs callers may depend on (Hyrum's law: with enough callers, every observable behavior is depended on by someone).
- [ ] Security properties: authz checks, input validation, escaping, secrets handling.
- [ ] Data: persisted formats and migrations; can old and new read each other's data during transition?

## 3. Building the new implementation

- Characterize the old implementation first (`safety-net.md` sections 2–4). Expected values come from running old code.
- Put a seam in front of both: same interface/adapter, feature flag, router, or proxy.
- Write the new code idiomatically for the chosen framework; don't mirror the old structure just because it exists — but don't add features either.
- Keep the old and new suites runnable in CI throughout; differential checks run from the first slice, not only at the end.
- Rewrite in vertical slices (one route/command/use case end to end) so each slice can be compared and cut over independently.
- Approved behavior changes are listed in the plan with the input that demonstrates them; everything else must match.

## 4. Parity and cutover

- [ ] Characterization/golden suite passes on new implementation.
- [ ] Differential run: N inputs, M differences, each triaged (fix / approved change / documented normalization).
- [ ] Error paths compared, not just happy paths.
- [ ] Performance compared on the same machine/inputs if callers care.
- [ ] Observability parity: logs/metrics others depend on still emitted.
- [ ] Cutover plan: flag or routing switch, order of slices, who/what is watched after the switch.

## 5. Rollback and deletion

- Keep a rollback path for an agreed window: a feature flag or a tagged release of the old version — not an indefinitely maintained second implementation.
- After the window: delete old code, its tests that only cover it, configuration, flags, and adapters. Report what was deleted.
- If deletion must wait (other teams still call it), record the remaining callers, the owner, and the planned date.

## 6. Rewrite anti-patterns

| Anti-pattern | Tell | Instead |
|---|---|---|
| Big-bang switch | "We'll switch when it's all done"; no seam | Strangler slices behind a router/flag |
| Second-system effect | New code gains features, plugins, configurability nobody asked for | Parity first; features as follow-ups |
| Spec from memory | Tests written from what the new author believes the old code does | Characterize by running old code |
| Fixing while rewriting | Commits like "rewrite X and fix rounding" | Record bug; change it after parity, with approval |
| Permanent dual stack | Old code kept "just in case" without owner/date | Tagged rollback, then delete |
| Silent narrowing | Rare inputs/errors the old code accepted now rejected | Include error/odd-input classes in the inventory and fixtures |

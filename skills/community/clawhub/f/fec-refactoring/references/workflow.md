# Refactoring Workflow

## State Machine

```text
CLASSIFY REQUEST
  -> DISCOVER CONTEXT
  -> ESTABLISH BASELINE
  -> DIAGNOSE STRUCTURAL EVIDENCE
  -> ESTABLISH SAFETY
  -> BUILD ORDERED PLAN
  -> RISK CHECK
  -> EXECUTE ONE STEP
  -> VERIFY STEP
       PASS -> inspect diff -> next step
       FAIL -> revert current step -> confirm baseline -> shrink/replan
  -> FINAL VALIDATION
  -> REPORT
```

## Context Discovery

Read only what is needed to establish facts:

- `package.json`, workspace manifests, TypeScript and lint configuration;
- test configuration and scripts;
- affected modules, callers, imports, barrel exports, routes, and registration points;
- state/store ownership and persistence boundaries;
- framework conventions, lifecycle-sensitive code, async effects, and current Git diff.

## Baseline Handling

If the baseline is green, any newly failing relevant check after a step is presumptive evidence that the step regressed behavior or structure.

If the baseline is already red:

1. record exact failing commands and symptoms;
2. do not claim later failures are caused by refactoring without comparison evidence;
3. avoid risky restructuring unless the preserved contract remains credible;
4. separate unexplained failure diagnosis from structural change.

## Plan Step Contract

Each executable step records:

```text
Target:
Technique:
Intent:
Prerequisites:
Risk: SAFE | CAUTION | DANGER
Expected files:
Expected functions/components:
Expected public API changes: 0
Expected behavior changes: 0
Verification:
Rollback boundary:
```

Order prerequisites before larger moves. For example, expose a stable query before extracting logic that depends on it, or isolate a conditional before replacing its dispatch mechanism.

## Step Failure Protocol

When a previously green check becomes red:

1. stop;
2. revert only the current structural step;
3. rerun the affected check to confirm restoration;
4. identify whether the failed assumption was behavior, identity, lifecycle, ordering, typing, or dependency related;
5. shrink the step or add a safer prerequisite;
6. retry only after the plan is again evidence-backed.

Do not spread fixes across unrelated modules merely to make the suite green.

## Final Validation

Use a narrow-to-broad ladder:

1. nearest syntax/type/static check;
2. targeted unit or component tests;
3. affected package or integration tests;
4. lint and full typecheck;
5. broader test suite;
6. build, SSR, E2E, visual, accessibility, performance, or specialty checks when affected.

## Proof Verdict

- **PASS:** the relevant observable contract is adequately covered and required checks pass.
- **PARTIAL:** executed checks pass, but important behavior remains incompletely covered.
- **NOT PROVEN:** missing dependencies, environment limits, baseline failures, or insufficient safety evidence prevent a credible preservation claim.

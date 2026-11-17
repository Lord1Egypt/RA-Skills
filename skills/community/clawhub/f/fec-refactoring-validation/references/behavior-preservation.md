# Behavior Preservation

## Build the Contract

Before changing structure, identify which observations must remain stable. Use the smallest contract that fully covers the affected boundary.

### Functional contract

- accepted inputs and normalization;
- return values and output ordering;
- errors, exceptions, and fallback behavior;
- side effects and significant ordering.

### UI contract

- rendered states and user-visible text/data;
- enabled/disabled behavior;
- focus and keyboard transitions;
- event/callback ordering;
- accessibility relationships that users or tests rely on.

### State and async contract

- store transitions and persistence;
- request count, URL, method, payload, cancellation, retry, and error mapping;
- loading/error/empty state timing;
- React identity/memoization and hook dependency semantics;
- Vue `ref`, `reactive`, `computed`, `watch`, and lifecycle identity/timing.

### Public contract

- exported symbols and call signatures;
- routes and URL parameters;
- serialized fields and API DTOs;
- extension, plugin, template, or runtime registration points.

## Characterization Tests

When behavior is important but weakly covered, write a narrow test that captures current behavior before a risky structural edit. It may pass immediately because it records the existing contract. Do not broaden it into a new requirement.

## Verdicts

### PASS

Use only when the relevant contract is well identified, the before/after baseline is comparable, and all required checks pass.

### PARTIAL

Use when checks pass but meaningful paths remain untested or only static/manual evidence covers an important boundary.

### NOT PROVEN

Use when dependencies cannot be installed, required tools cannot run, the baseline is ambiguous, or the safety net cannot credibly distinguish preservation from accidental behavior change.

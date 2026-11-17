# Refactoring Principles

## Definition

Refactoring changes the internal organization of existing code without intentionally changing its observable behavior. The purpose is to make future change safer and easier, not to smuggle new behavior into a structural patch.

## Eight Hard Rules

1. **Behavior Preservation:** define the relevant observable contract before substantial edits.
2. **Green Baseline First:** distinguish pre-existing failures from regressions introduced by the current step.
3. **One Refactoring at a Time:** keep each step attributable to one structural intent.
4. **Verify Every Step:** use feedback at the smallest useful scope before continuing.
5. **Revert Before Repairing:** a new regression invalidates the current step; restore the previous state before redesigning it.
6. **Separate Feature Work:** new outcomes, changed rules, or changed error behavior are not pure refactoring.
7. **Smallest Safe Refactoring First:** prefer a reversible local change over a speculative redesign.
8. **Stay Within the Diff Budget:** scope growth is a stop signal, not permission to keep expanding.

## Observable Behavior

Depending on the code, preservation can include:

- return values, thrown errors, and error mapping;
- side effects and their ordering when order is semantically significant;
- requests, payloads, retries, cancellation, and authentication behavior;
- state transitions, persistence, cache identity, and memoization-sensitive object identity;
- rendered DOM, loading/error/empty states, focus, keyboard behavior, and emitted events;
- props, emits, slots, hook/composable contracts, package exports, routes, and URLs.

## Evidence Model

Use concrete evidence before choosing a technique:

- call sites and dependency direction;
- ownership of the data being read or mutated;
- change history or repeated edit locations when available;
- tests and documented public contracts;
- runtime registration points, dynamic imports, route tables, i18n keys, Storybook stories, and generated templates;
- framework lifecycle semantics and state identity.

Metrics may indicate where to look, but they do not independently prove the diagnosis.

## Risk Model

### SAFE

Local/private scope, no public contract, no subtle lifecycle or persistence semantics, strong rollback path, and relevant verification available.

### CAUTION

Cross-file or cross-component restructuring, shared helpers, state ownership changes, lifecycle-sensitive code, dynamic references, or incomplete behavioral coverage.

### DANGER

Public APIs, routes, storage schemas, backend contracts, authentication or permissions, SSR/hydration, critical calculations, broad inheritance replacement, or architecture-wide state movement.

Do not assign permanent risk to a catalog technique. The same rename can be SAFE for a local variable and DANGER for a serialized field.

## Characterization Before Risky Change

When important current behavior is not directly tested, add characterization coverage that describes what the code already does. Such a test can start green; its purpose is to lock existing behavior, not to invent a new requirement.

# Refactoring Test Checklist

## Local Function or Module

- targeted unit tests for inputs, outputs, and errors;
- typecheck of affected package/module;
- callers compile with unchanged contracts;
- no public export change unless planned.

## React

- hook order and dependency arrays remain valid;
- stale closure behavior is not introduced;
- controlled/uncontrolled ownership remains stable;
- memoization or referential equality assumptions are preserved;
- effect cleanup, request cancellation, and event order remain stable;
- Server/Client boundaries and hydration behavior are unchanged when relevant.

## Vue

- `ref`/`reactive` identity and unwrapping semantics remain stable;
- computed values stay derived rather than duplicated mutable state;
- watchers keep intended source, flush timing, and cleanup;
- props, emits, slots, and expose contracts remain stable;
- Pinia store ownership and persistence remain stable.

## API and Data

- request shape, headers, auth refresh, cancellation, retry, and errors remain stable;
- field renames do not cross DTO, storage, query-string, or backend contracts unintentionally;
- sorting/filtering transformations preserve order, duplicates, and edge cases;
- reference-to-value or value-to-reference changes preserve required identity semantics.

## Routing and Runtime Registration

- route names/paths/guards remain stable;
- dynamic imports and lazy registrations remain discoverable;
- Storybook, i18n, CSS/Tailwind dynamic classes, runtime templates, and generated metadata are not broken by search-only reasoning.

## Final Ladder

Run available checks from narrowest to broadest: targeted tests -> affected integration tests -> lint/typecheck -> full tests -> build -> E2E/SSR/visual/a11y/performance specialty gates when the refactoring touches those risks.

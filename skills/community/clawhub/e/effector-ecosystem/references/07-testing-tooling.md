# Testing and tooling

## Contents

This file covers Effector ecosystem testing/tooling. Use `effector-fsd` for FSD/Steiger checks.

- Testing Effector models
- Testing app/page startup
- Testing Farfetched flows
- UI tests
- Scope/SSR checks
- ESLint
- TypeScript
- Build plugin
- Next.js
- CI review gates

## Testing Effector models

Use `fork` and `allSettled` for model tests.

Test behavior without rendering React when possible.

```ts
import { allSettled, fork } from 'effector';

const scope = fork({
  values: [[$token, 'token']],
  handlers: [[analyticsTrackedFx, async () => undefined]],
});

await allSettled(formSubmitted, { scope });

expect(scope.getState($isSubmitted)).toBe(true);
```

Rules:

- Trigger public events, not private helper units.
- Assert public stores/domain events/route decisions.
- Mock effect handlers through `fork({ handlers })` when testing non-HTTP effects.
- Keep tests close to user-visible behavior, but do not render React to test pure model data flow.

## Testing app/page startup

Use the same startup event in tests that the runtime uses.

```ts
const scope = fork({
  handlers: [[browserIntegrationsStartedFx, async () => undefined]],
});

await allSettled(appStarted, {
  scope,
  params: { initialUrl: '/users/1', locale: 'en' },
});

expect(scope.getState($locale)).toBe('en');
```

For page/server events:

```ts
const scope = fork();

await allSettled(pageStarted, {
  scope,
  params: { userId: '1' },
});

expect(scope.getState(userQuery.$data)).toEqual(expectedUser);
```

Do not duplicate runtime bootstrapping in tests as a chain of helper calls such as `startAppClock -> appStarted -> startRouter`. First try to model those helpers as effects started from `appStarted`; if a helper is an unavoidable host adapter boundary, mock/install it explicitly and still trigger business logic through `appStarted`/`pageStarted`.

Use `allSettled(scope)` only to wait for already-started scope-bound external callbacks. Most tests should use `allSettled(unit, { scope, params })`.

## Testing Farfetched flows

For Farfetched, use current public testing recipes from Farfetched docs for the installed version. Internals under `__` can change; avoid depending on them unless the docs for that exact version recommend it.

Test these behaviors at the model level:

- query/mutation is started with mapped params
- success maps DTO to domain state
- failure maps to project `RemoteError`
- `TAKE_LATEST` cancels/replaces stale route/search requests and resets `$pending` after abort/finish
- submit de-duplication is implemented with an explicit `$pending` gate (`sample.filter`) unless the project has a tested reason to use `TAKE_FIRST`
- if `TAKE_FIRST`/`TAKE_LATEST` is used for mutations, skipped/aborted lifecycle and browser-scoped `$pending` reset are covered by tests
- auth barrier success resumes protected operations
- auth barrier failure produces session/logout/redirect facts
- `keepFresh` triggers refresh only after the query has been started once
- mutation `update` is used only for safe cache patches; otherwise refresh is triggered

Prefer tests around public events/stores:

```ts
await allSettled(userRoute.opened, {
  scope,
  params: { params: { userId: '1' }, query: {} },
});

expect(scope.getState(userQuery.$pending)).toBe(false);
expect(scope.getState($userVm)).toEqual(expectedVm);
```

## UI tests

Use UI tests for:

- rendering states
- user interaction wiring
- integration between component and model

Use `<Provider value={scope}>` in tests that need Scope.

Do not test all business rules through React if they can be tested at model level.

For connected components, assert that UI calls bound handler aliases from `useUnit`, not raw imported events.

## Scope/SSR checks

When Scope is used:

- events/effects passed to React handlers must be bound through `useUnit`
- handler-like values returned from `useUnit` should use React-facing `on*` aliases
- external callbacks must use `scopeBind` or a scope-aware adapter
- persistence should use explicit `pickup`
- stores that are serialized must have stable SIDs
- app bootstrap should use `fork`, `allSettled`, `serialize`, and hydration consistently
- server code must create a fresh Scope per request/page computation

## ESLint

Use `eslint-plugin-effector` presets:

- `recommended` for base Effector best practices
- `react` for React-specific rules
- `scope` when using Fork API / Scope
- `patronum` when using Patronum
- `future` only when the team intentionally wants stricter future-oriented rules

React-specific checks to value highly:

- prefer `useUnit`
- exhaustive `useUnit` destructuring
- mandatory scope binding
- no units/factories in render
- no deprecated hooks in new code

Scope checks to value highly:

- no unsafe `getState`
- no unsafe `watch`
- persist requires `pickup` when scopes are used
- strict effect handler discipline in tests

## TypeScript

Use strict mode.

Avoid `any` for remote data. Unknown backend data must pass through contracts.

Use `UnContract<typeof Contract>` or project-standard validator inference for DTO/domain types.

Avoid exporting huge inferred object types from models. Public model shapes should be readable and stable.

## Build plugin

Use `@effector/swc-plugin` or the Effector Babel plugin when the project needs:

- stable SIDs
- SSR serialization/hydration
- factories support
- better unit names/debugging
- HMR support

Configure local factories when using model factories. Community packages such as Patronum, Farfetched, Atomic Router, `effector-action`, and `@withease/factories` may be handled by plugin defaults or package metadata, but local project factories still need explicit configuration.

For Atomic Router and With Ease factories, add them to `factories` when the current plugin docs/project setup requires it:

```js
['@effector/swc-plugin', {
  factories: [
    'atomic-router',
    '@withease/factories',
    '@/shared/lib/create-form-model',
  ],
}]
```

## Next.js

Use `@effector/next` for Next.js integration when Scope/SSR/hydration is required.

Rules:

- enable Effector Babel/SWC plugin for SIDs
- create a fresh Scope per server request/page computation
- run app/page model events with `allSettled(event, { scope, params })`
- pass `serialize(scope)` to `EffectorNext`
- avoid raw event/effect calls in Client Components
- bind through `useUnit`
- mark hook-using components with `'use client'`
- serialize/hydrate only intended stores
- keep server/client boundaries explicit
- keep Next router in an adapter model if business logic needs client navigation

Testing Next.js server logic:

```ts
const scope = fork();
await allSettled(pageStarted, { scope, params: { userId: '1' } });
const values = serialize(scope);
expect(values).toMatchObject({});
```

Do not rely on a global server Scope, missing SIDs, or layout-level reads of page-loaded stores in App Router.

## CI review gates

At minimum, CI should run:

- TypeScript typecheck
- unit tests for Effector models
- UI tests where relevant
- ESLint with Effector presets
- build with the same plugin configuration used in production
- SSR/Next build smoke test when Next.js is used
- architecture review checklist for Farfetched contracts/barriers/routes on changed ownership areas

## Audit additions for tests

- Avoid global `fx.use(...)` in shared test helpers when the project uses `fork({ handlers })`; global handlers hide missing scoped handlers and reduce test isolation.
- Add tests for cold start on protected routes: valid session + direct URL should keep the original route and params after session restore.
- Add tests for logout/session clear while a protected route is already opened: route should redirect/close, not render a blank layout.
- Add tests for any app-level unauthorized policy: a `401` from a non-session query/mutation should clear session and trigger the same redirect policy as logout.
- Add tests for scope-safe timers/listeners: two Scopes can start external callbacks independently; stopping one does not stop the other.
- Add tests for page-model route gates: mutation success while the route is closed must not start the page query.

# Ecosystem library notes

This file summarizes the practical rules for common Effector ecosystem libraries. Use `effector-fsd` for Feature-Sliced Design and Steiger.

## Contents

- Effector
- effector-react
- @effector/next
- @effector/reflect
- Farfetched
- @withease/contracts
- patronum
- effector-action
- @withease/factories
- atomic-router
- effector-storage
- effector-forms
- i18next / @withease/i18next
- @withease/web-api
- @withease/redux
- eslint-plugin-effector
- Effector Babel/SWC plugin

## Effector

Use Effector for static, declarative business models. Default to `sample`, atomic stores, derived view models, explicit lifecycle events, and tests with `fork`/`allSettled`.

Use one explicit app/page startup event (`appStarted`, `pageStarted`) and connect startup work through `sample`. Avoid hidden imperative helper chains; first model router/history/clock/browser integration setup as effects started from `appStarted`. Keep free-floating startup helpers only for documented last-resort host adapter installation. Use `scopeBind` for callbacks that leave Effector's call stack and later re-enter a Scope.

Avoid `watch` for behavior, `getState` for production logic, units in render, and imperative event calls inside effects.

## effector-react

Use `useUnit` as the default React binding.

Default connected-component pattern:

```tsx
const { value, pending, onChange, onSubmit } = useUnit($$model);
```

The model should expose an object shape suitable for UI binding:

```ts
export const $$model = {
  value: $value,
  pending: mutation.$pending,
  onChange: changed,
  onSubmit: submitted,
};
```

Use arrays for small local bindings, object shapes for public model APIs. In both cases, name bound handlers with `on*` aliases in React-facing code.

## @effector/next

Use for Next.js SSR/hydration with Effector Scope.

Rules:

- enable Effector plugin for SIDs
- create a fresh Scope per server request/page computation
- run server model events with `allSettled(event, { scope, params })`
- pass `serialize(scope)` values to `EffectorNext`
- bind Client Component handlers through `useUnit`
- keep Next router integration in an adapter model
- use `scope.getState` only at framework boundaries such as `notFound`, `redirect`, `generateMetadata`, or `generateStaticParams`
- avoid global server Scope and layout decisions that depend on page-loaded stores in App Router

## @effector/reflect

Use when the team intentionally wants declarative mapping from stores to presentational components. Do not use it as a universal replacement for simple `useUnit` connected components.

## Farfetched

Use `createJsonQuery`/`createJsonMutation` for JSON HTTP APIs.

Checklist:

- `declareParams<T>()` for params
- request object owns method/url/query/body/headers
- `response.contract` validates unknown data
- `mapData` maps DTO to domain shape
- `mapError` normalizes errors and uses the current object argument shape, for example `mapError: ({ error, params, headers }) => ...`
- `concurrency(operation, { strategy })` is an operator
- submit de-duplication defaults to an explicit Effector `$pending` gate plus `TAKE_EVERY`; use `TAKE_FIRST` only when skipped lifecycle is intentional and tested
- `request.fetch.credentials` is used for cookie/session APIs in current Farfetched code
- `keepFresh` is used only after first query start is modeled
- `cache`, `.refresh`, `update`, barriers are used deliberately
- `createBarrier`/`applyBarrier` centralize auth refresh or unavailable-resource gates
- `@farfetched/atomic-router` provides `startChain`, `freshChain`, and `barrierChain` for route loaders

## @withease/contracts

Use for small runtime validators and type inference through `UnContract`.

Use with:

- Farfetched `response.contract`
- effector-storage `contract`
- reusable domain DTO validation

## patronum

Use for common reactive utilities: debounce, throttle, reset, condition, pending/status, spread, reshape, combineEvents, interval.

Do not reimplement these with `watch` and timers unless there is a very specific reason.

## effector-action

Use for readable complex branching from one decision point. Avoid for simple flows where `sample` is clearer.

## @withease/factories

Use for repeated same-shaped Effector model code that needs independent model instances. Prefer it over copy-pasting repeated forms, filters, widgets, or similar models.

Rules:

- factory invocation at module top level
- one config object parameter by default
- plugin `factories` field configured for SSR/SIDs
- no factory calls in React render/hooks

## atomic-router

Use for typed routes, route lifecycle, guards, redirects, and route-driven data loading.

Patterns:

- `createRoute` for route units
- `chainRoute` for data/permission/auth gating
- protected routes as model composition, not JSX-only wrappers
- `RouterProvider`/framework integration at app level
- Farfetched integration for query-driven route loading
- route-param mapping in page/app models, not UI

Atomic Router APIs have historically evolved; check current docs before writing version-specific helper types.

## effector-storage

Use for syncing stores with external storage. Persist only safe data. Add contracts for untrusted storage data. Use explicit `pickup` when Scope/SSR is used.

## effector-forms

Use when field-level form abstraction is worth it. For small forms, plain Effector stores/events are often clearer.

## i18next / @withease/i18next

Use `react-i18next` for UI-only translations. Use `@withease/i18next` when language participates in Effector models, queries, routing, or app lifecycle.

Do not store translated strings in domain stores.

## @withease/web-api

Use for browser signals as units/triggers: page visibility, network, media query, orientation, languages, geolocation. Use explicit setup/teardown and connect to Farfetched `keepFresh` when refetch on focus/reconnect is needed.

## @withease/redux

Use only for Redux migration/interoperability. Do not add Redux to new Effector-first projects.

## eslint-plugin-effector

Use recommended/react/scope/patronum presets as appropriate. Pay special attention to rules around `useUnit`, mandatory Scope binding, units in render, unsafe `getState`, unsafe `watch`, and persistence pickup.

## Effector Babel/SWC plugin

Use for SIDs, SSR, debugging, HMR, and factories. Configure local model factories; do not rely on luck for stable serialization.

In Next.js, verify the plugin field supported by the installed Next version and include local factories plus ecosystem factories when required, for example Atomic Router or `@withease/factories`.

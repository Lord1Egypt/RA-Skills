# Package map: what to use and when

Use this file when the user asks which package to use for a problem.

## Contents

- Core state and business logic
- React binding
- Remote data
- Runtime validation and DTO typing
- Effector utilities
- Routing
- Persistence
- Forms
- Internationalization
- Browser/Web APIs
- Redux migration/interoperability
- Tooling
- Package choice defaults

## Core state and business logic

### `effector`

Use for:

- business state
- events and workflows
- derived state
- effects not covered by Farfetched
- application lifecycle
- testing through `fork`, `allSettled`, and scoped assertions

Prefer Effector over React state when the state is shared, testable, participates in routing/API orchestration, or must survive component remounts.

Do not use React state for cross-component business workflows.

## React binding

### `effector-react`

Use for:

- `useUnit` in connected React components
- `<Provider value={scope}>` when using Scope/SSR/tests
- `useGate`/Gate only for component lifecycle facts
- `useList`/`useStoreMap` for list and item-level subscription optimization

Default connected-component rule:

```tsx
const { value, onValueChange, onSubmit } = useUnit($$model);
```

Use one `useUnit` call with an object or array shape for units from the same model. Destructure all returned fields. Handler-like values returned from `useUnit` should use React-style `on*` aliases. Split a component if render granularity matters.

Avoid deprecated or legacy bindings (`useStore`, `useEvent`, HOCs) in new code unless maintaining old code.

### `@effector/next`

Use for Next.js applications where Effector Scope, SSR, serialization, and hydration need first-class integration.

Use it when:

- App Router or Pages Router renders Effector-backed data on the server
- server-side page events are run through `fork`/`allSettled`
- serialized Scope values must be passed to client components
- Client Components need bound events/effects through `useUnit`

Rules:

- enable Effector Babel/SWC plugin for stable SIDs
- create a fresh Scope per server request/page computation
- pass `serialize(scope)` to `EffectorNext`
- keep Next router integration in an adapter model, not inside features
- do not add it to plain Vite/SPA projects

### `@effector/reflect`

Use when a project deliberately prefers a declarative HOC-like binding layer between Effector and React components, especially for reusable presentational components.

Do not use it just to avoid writing `useUnit`; ordinary connected components should normally use `useUnit` directly.

## Remote data

### `@farfetched/core`

Use for:

- HTTP queries and mutations
- request status and lifecycle
- cancellation/concurrency
- cache, stale data, refresh, and updates
- auth barriers and retry-like infrastructure
- runtime response validation through contracts

Use `createJsonQuery`/`createJsonMutation` for ordinary JSON HTTP APIs.

Do not write custom `createEffect(fetch)` wrappers for every endpoint when Farfetched already solves the problem.

## Runtime validation and DTO typing

### `@withease/contracts`

Use as the default contract solution for Farfetched responses and persisted external data.

Use for:

- backend DTO contracts
- runtime validation of remote data
- `UnContract` type extraction
- validation of `effector-storage` values

Keep contracts near the domain that owns the data:

```txt
entities/user/model/user.contract.ts
features/profile-update/model/profile-update.contract.ts
shared/api/problem.contract.ts
```

Do not put all contracts into `shared/contracts` unless they are truly domain-independent.

Other validators can be used if the project already standardizes on them, but the skill should default to `@withease/contracts`.

## Effector utilities

### `patronum`

Use for common declarative operators:

- `debounce`, `throttle`, `delay`, `interval`
- `reset`, `spread`, `reshape`, `condition`
- `status`, `pending`, `inFlight`
- `combineEvents`, `not`, `and`, `or`

Do not reimplement common operators with `watch`, timers, or ad-hoc effect chains.

### `effector-action`

Use when a single decision point has many branches and repeated `sample` blocks become harder to read.

Good use case:

- imperative-looking but still Effector-native branching over stores/events
- many targets chosen from the same source/clock

Do not use it for simple one- or two-step flows where `sample` is clearer.

### `@withease/factories`

Use for model factories when a module has repeated same-shaped Effector model code and needs multiple independent instances of the same model. Prefer it over copy-pasting repeated form, filter, or widget models.

Use only when repeated model instances are real, for example:

- many independent forms with the same behavior
- reusable tabs/list filters
- per-widget isolated models
- SSR/Scope/SID-sensitive apps where factory invocation must stay safe and discoverable

Rules:

- invoke factories at module top level, not inside React render
- configure Effector Babel/SWC plugin `factories` field for SSR/SIDs
- prefer one config object argument
- export a ready instance from the owning module public boundary, not the raw factory unless the consumer must create instances

## Routing

### `atomic-router`

Use when routes are part of Effector architecture:

- typed route params
- route open/close events
- data loading on route open
- guards and redirects
- route composition with `chainRoute`

Put route declarations near the router/page ownership boundary. Route-specific orchestration belongs to the route/page model, not the UI.

Use Farfetched integration when a query is the `chainRoute` loader. Add `@farfetched/atomic-router` for query-driven route loading:

- `startChain(query)` for unconditional load before route open
- `freshChain(query)` for cache/stale-aware route open
- `barrierChain(barrier)` when route opening must wait for a Farfetched barrier

If route params and query params differ, map them in the page model or use a page-specific query shape; do not map route params in React.

## Persistence

### `effector-storage`

Use for synchronization with external storages:

- localStorage/sessionStorage
- URL query storage
- cookies/server-side storage
- IndexedDB/async adapters when configured

Use for:

- theme
- locale
- safe preferences
- local drafts
- non-sensitive filters

Avoid persistence for:

- sensitive tokens unless the security model explicitly allows it
- large remote data without a cache strategy
- derived data that can be recomputed

When using Scope/SSR, prefer explicit `pickup` and enable linting for it. Validate untrusted persisted data with a `contract`.

## Forms

### Plain Effector form model

Default for small/medium forms:

- stores for values
- derived stores for errors and validity
- `sample` from `formSubmitted` to mutation/query
- reset on success/route close where appropriate

### `effector-forms`

Use when the project benefits from a dedicated form abstraction:

- many fields with similar validation lifecycle
- touched/dirty/error metadata
- repeated form patterns
- existing team convention around `effector-forms`

Keep form business rules in the feature/page model. UI can use `useForm` or a single `useUnit` shape from the form model.

## Internationalization

### `react-i18next` / `i18next`

Use for ordinary UI translations.

### `@withease/i18next`

Use when language is part of Effector-driven state or orchestration:

- language switch flows
- language-dependent routes
- language-dependent queries
- reactive `$t`, `$language`, `$isReady` usage in models

Do not put translated strings into domain stores. Store translation keys or domain values; translate in UI or at the boundary.

## Browser/Web APIs

### `@withease/web-api`

Use for browser signals as Effector units/triggers:

- online/offline
- page visibility
- media queries
- orientation
- languages
- geolocation

Use these signals with Farfetched `keepFresh` or app lifecycle when appropriate. Prefer explicit setup/teardown events instead of scattered DOM listeners in components.

## Redux migration/interoperability

### `@withease/redux`

Use only for migration or interop with existing Redux code.

Do not introduce Redux into a new Effector-first architecture.

## Tooling

This file covers Effector ecosystem tooling only. Use `effector-fsd` for FSD/Steiger tooling.

### `eslint-plugin-effector`

Use presets:

- `recommended` for base Effector practices
- `react` for React-specific rules such as `prefer-useUnit`, exhaustive `useUnit` destructuring, no units in render, and mandatory scope binding
- `scope` for Fork API / Scope projects
- `patronum` when using Patronum
- `future` only when the team intentionally wants stricter future-oriented rules


### Effector Babel/SWC plugin

Use when the project needs:

- stable SIDs
- SSR serialization/hydration
- factory support
- better unit names/debugging
- HMR support where applicable

Community package factories are usually recognized by the plugin, but local factories still require correct configuration.

## Package choice defaults

- Business state: `effector`
- React binding: `effector-react` + one `useUnit` shape per connected component
- HTTP: Farfetched
- Runtime validation: `@withease/contracts`
- Common operators: `patronum`
- Complex branching: `effector-action` only when it improves readability
- Typed routing: `atomic-router`
- Persistence: `effector-storage` with `contract` and explicit `pickup` for scopes
- i18n UI only: `react-i18next`
- i18n as app state: `@withease/i18next`
- Browser signals: `@withease/web-api`
- Reusable model instances: `@withease/factories`
- Next.js SSR/App Router: `@effector/next` + per-request Scope + plugin/SIDs
- Effector linting: `eslint-plugin-effector`

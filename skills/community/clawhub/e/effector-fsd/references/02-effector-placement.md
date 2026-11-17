# Effector placement rules in FSD

Use this file when placing Effector stores, events, effects, factories, models, React bindings, and lifecycle wiring.

## Contents

- Core ownership rule
- Layer matrix
- Model file organization
- Public model shape
- Factories
- Effects and side effects
- Startup and Scope
- React binding placement

## Core ownership rule

Place an Effector unit where the **fact it represents** belongs.

- `profileUpdateSubmitted` belongs to `features/profile-update`.
- `pageStarted` for `/users` belongs to `pages/users`.
- `$session` belongs to `entities/session`.
- `appStarted` belongs to `app/model`.
- `routerStartedFx` belongs to `app/routes` or `app/model`.
- `apiUrl` belongs to `shared/api`.

Do not place units by technical type, such as `src/events`, `src/stores`, `src/effects`, or `src/store`.

## Layer matrix

| Unit / concern | Default owner |
|---|---|
| `appStarted`, `appStopped`, app-wide Scope/bootstrap | `app/model` |
| Router/history setup | `app/routes` |
| Global protected route composition | `app/routes` |
| Page route declaration/re-export | `pages/<page>/route.ts` |
| Route params -> query start | `pages/<page>/model/page.model.ts` |
| Page filters/sort/pagination | `pages/<page>/model` |
| Page-only list query | `pages/<page>/api` |
| User action event/form/mutation | `features/<action>/model` and `features/<action>/api` |
| Reusable domain store/query/contract | `entities/<entity>/model` and `entities/<entity>/api` |
| UI primitive with no domain logic | `shared/ui` |
| Transport helper/base URL/error mapper | `shared/api` |
| Date/currency/string helper with no domain | `shared/lib/<purpose>` |

## Model file organization

Split Effector models by responsibility, not by unit type.

Bad:

```txt
features/profile-update/model/stores.ts
features/profile-update/model/events.ts
features/profile-update/model/effects.ts
```

Good:

```txt
features/profile-update/model/form.model.ts
features/profile-update/model/submit.model.ts
features/profile-update/model/profile-update.model.ts
```

For larger pages:

```txt
pages/users/model/page.model.ts       # top-level orchestration
pages/users/model/filters.model.ts
pages/users/model/table.model.ts
pages/users/model/selection.model.ts
```

## Public model shape

Expose a stable public shape when UI needs several stores/events:

```ts
export const $$profileUpdate = {
  values: $values,
  submitDisabled: $submitDisabled,
  onFieldChange: fieldChanged,
  onSubmit: formSubmitted,
};
```

The `on*` names are UI aliases. Underlying Effector events should remain named as facts.

## Factories

Factory definition belongs near the owner that defines the reusable behavior:

```txt
shared/lib/create-form-model/create-form-model.ts   # generic library factory
features/search/lib/create-search-filter-model.ts   # feature-local repeated behavior
widgets/table/lib/create-table-selection-model.ts    # widget-local behavior
```

Factory instances belong to the slice that owns the concrete instance:

```txt
pages/users/model/filters.model.ts
features/profile-update/model/form.model.ts
```

Rules:

- Invoke factories at module top level.
- Export concrete instances from public APIs when external usage is needed.
- Do not instantiate factories in React components.
- In SSR/SID-sensitive apps, configure the Effector Babel/SWC plugin factories field.

## Effects and side effects

Use Farfetched for remote API operations when possible. Use `createEffect` for side effects such as:

- router/history adapter calls
- storage pickup/start/stop
- analytics SDK
- browser API registration
- local non-HTTP IO

Place effects where the integration belongs. A browser event listener used app-wide belongs to `app` or `shared` adapter; a page-only effect belongs to the page.

## Startup and Scope

FSD placement for explicit startup:

```txt
app/model/app.model.ts       # appStarted, appStopped
app/entrypoint/client.tsx    # fork + allSettled(appStarted)
app/providers/effector.tsx  # Provider/EffectorNext adapter
```

Page startup:

```txt
pages/user/model/page.model.ts
```

Framework route adapter:

```txt
app/users/[userId]/page.tsx       # Next framework adapter
src/_pages/user/model/page.model.ts
```

Avoid hidden startup helper chains outside the model. App integration effects should be started from `appStarted`.

## React binding placement

Connected components may live in:

- `pages/<page>/ui` for page UI
- `widgets/<widget>/ui` for widget UI
- `features/<action>/ui` for action UI
- `entities/<entity>/ui` for domain visuals

Dumb UI primitives go to `shared/ui`.

A component must not create Effector units. It imports model public shape from its owner and binds through `useUnit`.

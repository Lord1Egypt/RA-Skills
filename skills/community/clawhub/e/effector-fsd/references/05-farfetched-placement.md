# Farfetched placement in FSD

Use this file to place queries, mutations, contracts, DTO mappers, barriers, cache/update policy, and route loaders.

## Contents

- Default matrix
- Contracts
- Queries
- Mutations
- Cache/update policy
- Barriers and auth refresh
- Route loaders

## Default matrix

| Farfetched concern | Default FSD owner |
|---|---|
| Base URL, generic headers, generic `RemoteError` mapper | `shared/api` |
| Domain contract/type/mapper | `entities/<entity>/model` or `entities/<entity>/api` |
| Reusable entity read query | `entities/<entity>/api/*.query.ts` |
| Action mutation | `features/<action>/api/*.mutation.ts` |
| Page-only list/table query | `pages/<page>/api/*.query.ts` |
| Page-specific route loader composition | `pages/<page>/route.ts` or `pages/<page>/model` |
| Auth/session refresh barrier with session state | `entities/session` or `app` |
| Pure transport helper without domain imports | `shared/api` |
| Applying barrier to many operations across layers | `app/api` or `app/model` integration |

## Contracts

Do not create a global `shared/contracts` dump.

Good:

```txt
entities/user/model/user.contract.ts
features/profile-update/model/profile-update.contract.ts
pages/users/model/users-page.contract.ts
shared/api/problem.contract.ts       # only generic transport problem shape
```

The owner of the business meaning owns the contract.

## Queries

Reusable entity read:

```txt
entities/user/api/user.query.ts
entities/user/model/user.contract.ts
entities/user/model/user.mapper.ts
```

Page-only query:

```txt
pages/users/api/users-page.query.ts
pages/users/model/page.model.ts
```

Rule: if only one page uses the query and its params mirror page filters/sorting/pagination, start in `pages`. Move to `entities` only when it becomes a reusable domain operation.

## Mutations

Action mutation:

```txt
features/profile-update/api/update-profile.mutation.ts
features/profile-update/model/submit.model.ts
features/profile-update/ui/profile-update-form.tsx
```

The feature owns the user intent and submit de-duplication. Use an explicit `$pending` gate in the feature/page model for duplicate-click prevention unless a Farfetched concurrency strategy is deliberately chosen and tested.

## Cache/update policy

Place cache/update logic near the operation owner unless it coordinates many owners.

Examples:

```txt
entities/user/api/user.query.ts                 # cache for reusable user read
features/profile-update/api/update-profile.mutation.ts
features/profile-update/model/after-submit.ts   # update/refresh owned by action
pages/users/model/page.model.ts                 # page list refresh after filters/route
app/api/apply-session-barriers.ts               # global barrier composition
```

Do not hide cache invalidation in unrelated shared helpers.

## Barriers and auth refresh

The common mistake is putting a session-aware barrier in `shared/api` and importing entities/routes from there. That violates FSD because `shared` cannot import business layers.

Bad:

```txt
shared/api/auth-barrier.ts
```

```ts
import { SessionContract, sessionReceived } from '@/entities/session'; // bad from shared
import { loginRoute } from '@/pages/login';                            // bad from shared
```

Strict defaults:

```txt
entities/session/api/session-refresh-barrier.ts # owns session refresh and session facts
app/api/apply-auth-barriers.ts                  # applies barrier to many lower-layer operations
app/routes/auth-redirects.ts                    # redirects after auth rejection
shared/api/http.ts                              # base fetch/error helpers only
```

Feature-level operation can import session barrier because features may import entities:

```ts
import { sessionRefreshBarrier } from '@/entities/session';
import { updateProfileMutation } from './update-profile.mutation';

applyBarrier(updateProfileMutation, { barrier: sessionRefreshBarrier });
```

Entity-level operation that needs a session barrier has three options:

1. Keep auth retry in pure transport (`shared/api/http`) without entity imports.
2. Apply the session barrier from `app/api/apply-auth-barriers.ts`.
3. Use a documented `@x` relationship only when it is truly an entity relationship, not a convenience shortcut.

Prefer option 1 or 2.

## Route loaders

When query is the route loader:

```txt
pages/post/route.ts
entities/post/api/post.query.ts
```

`pages/post/route.ts` owns `chainRoute` because it knows the route. `entities/post` owns `postQuery` if reusable.

Do not start route data loading in React `useEffect` when Atomic Router or page model can express it declaratively.

## Full-audit ownership checks

### Page-local refetch after feature mutation

If a page refreshes after a feature mutation, gate the reaction by the page route or move it to a higher owner.

```ts
sample({
  clock: itemCreated,
  source: itemsRoute.$isOpened,
  filter: Boolean,
  fn: () => undefined,
  target: itemsPageQuery.start,
});
```

This belongs in the page only when it coordinates page-specific filters/list state. If many pages/widgets depend on the invalidation, create an entity/app invalidation event.

### App-level unauthorized wiring

`shared/api` may map transport errors to `{ kind: 'unauthorized' }`, but the wiring from operation failures to `sessionCleared` belongs in `app` because it imports many operations and session state.

```txt
app/model/auth-errors.ts
app/routes/auth-redirects.ts
```

Do not scatter the same unauthorized handling across pages, and do not import routes/session into shared transport helpers.

### Reusable resource hidden in page API

A query/mutation/contract under `pages/<page>/api` is a warning sign when:

- another page, widget, app integration, or test imports it;
- the DTO/contract name is a domain resource (`Settings`, `User`, `Order`, `PublicLink`, `Session`) rather than a page response (`UsersPageResponse`);
- the operation does not use page-only filters, sort, pagination, or route-only params.

Move reusable reads/contracts to `entities/<entity>` and user-action writes to `features/<action>`.

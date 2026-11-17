# Farfetched and contracts

Use this file for remote data design. It is intentionally strict: most production bugs around Farfetched come from treating it as a thin `fetch` wrapper instead of a remote-operation layer with validation, concurrency, freshness, cache, and barriers.

## Contents

- Default rule
- Query template
- Mutation template
- Request shape
- Contracts
- DTO mapping
- Error mapping
- Concurrency
- Refresh, freshness, and cache
- Cache update after mutation
- Barriers and auth refresh
- Atomic Router integration
- Placement
- Testing
- Anti-patterns

## Default rule

Use Farfetched for backend communication.

- Reads: `createJsonQuery`
- Writes: `createJsonMutation`
- Params: `declareParams<T>()` when params are needed
- Runtime response validation: `response.contract`
- DTO mapping: `response.mapData`
- Error normalization: `response.mapError` or a shared API error mapper
- Concurrency: `concurrency(operation, { strategy })`, not an obsolete factory config field; use it deliberately for route/search/filter cancellation, and prefer an explicit `$pending` gate for submit de-duplication
- Freshness/cache: `keepFresh`, `cache`, `.refresh`, and `update` deliberately, not by habit
- Auth/availability gates: `createBarrier` + `applyBarrier`

Never treat remote data as trusted TypeScript data until a contract validates it.

## Query template

```ts
import { createJsonQuery, declareParams, concurrency } from '@farfetched/core';
import { UserDtoContract, mapUserDto, type User } from '../model/user.contract';
import { mapRemoteError } from '@/shared/api/errors';
import { apiUrl } from '@/shared/api/base-url';

export type UserQueryParams = { id: string };

export const userQuery = createJsonQuery({
  params: declareParams<UserQueryParams>(),
  request: {
    method: 'GET',
    url: ({ id }) => apiUrl(`/users/${id}`),
    // query: ({ id }) => ({ expand: 'roles' }),
    // headers: { accept: 'application/json' },
    // fetch: { credentials: 'include' }, // cookie auth; prefer this over top-level credentials in Farfetched v0.15+
  },
  response: {
    contract: UserDtoContract,
    mapData: ({ result }): User => mapUserDto(result),
    mapError: ({ error }) => mapRemoteError(error),
  },
});

// Use the operator; do not put concurrency into createJsonQuery config.
concurrency(userQuery, { strategy: 'TAKE_LATEST' });
```

For queries without params, omit `params` entirely or use the project-standard no-params convention. Do not invent `{}` params solely to satisfy a template.

## Mutation template

```ts
import { createEvent, sample } from 'effector';
import { createJsonMutation, declareParams, concurrency } from '@farfetched/core';
import { UserDtoContract, mapUserDto, type User } from '../model/user.contract';
import { mapRemoteError } from '@/shared/api/errors';
import { apiUrl } from '@/shared/api/base-url';

export type UpdateUserParams = {
  id: string;
  values: { name: string };
};

export const updateUserSubmitted = createEvent<UpdateUserParams>();

export const updateUserMutation = createJsonMutation({
  params: declareParams<UpdateUserParams>(),
  request: {
    method: 'PATCH',
    url: ({ id }) => apiUrl(`/users/${id}`),
    body: ({ values }) => values,
    // fetch: { credentials: 'include' },
  },
  response: {
    contract: UserDtoContract,
    mapData: ({ result }): User => mapUserDto(result),
    mapError: ({ error }) => mapRemoteError(error),
  },
});

// Submit de-duplication: keep request concurrency permissive and gate user intent explicitly.
concurrency(updateUserMutation, { strategy: 'TAKE_EVERY' });

sample({
  clock: updateUserSubmitted,
  source: updateUserMutation.$pending,
  filter: (pending) => !pending,
  fn: (_pending, params) => params,
  target: updateUserMutation.start,
});
```

In larger layered code, the `updateUserSubmitted` event normally lives near the user-action/page model and the Farfetched operation lives near the owning API/domain module. The important part is the boundary: user intent is gated in Effector model code, while the operation keeps a predictable remote lifecycle.

## Request shape

Keep request construction in the operation, not in UI.

Common request fields:

- `method`
- `url`
- `query`
- `body`
- `headers`
- `fetch`

Rules:

- Do not send `body` with `GET`/`HEAD` requests.
- For cookie/session APIs, use `request.fetch.credentials`, for example `fetch: { credentials: 'include' }`. Do not rely on the old top-level `credentials` option in new Farfetched code.
- Keep domain-independent URL/base/header helpers near transport infrastructure; keep endpoint-specific params/mapping near the operation owner.
- If auth headers depend on stores, use a shared request adapter or `attach`-style infrastructure around non-Farfetched effects only when Farfetched cannot express the need directly.

## Contracts

Default to `@withease/contracts`:

```ts
import { obj, str, num, type UnContract } from '@withease/contracts';

export const UserDtoContract = obj({
  id: num,
  full_name: str,
});

export type UserDto = UnContract<typeof UserDtoContract>;
```

Place contracts by data ownership:

```txt
entities/user/model/user.contract.ts
features/profile-update/model/profile-update.contract.ts
shared/api/problem.contract.ts
```

Do not put all business DTOs into a global contracts bucket.

Use another validator only if the project already standardizes on it. The architecture rule is not “use one specific validator at all costs”; the rule is “validate unknown remote data at runtime before using it as domain data”.

## DTO mapping

Use `mapData` after validation to map transport shape to domain shape.

```ts
export const mapUserDto = (dto: UserDto): User => ({
  id: String(dto.id),
  displayName: dto.full_name,
});

response: {
  contract: UserDtoContract,
  mapData: ({ result }) => mapUserDto(result),
}
```

If DTO mapping is more than a trivial field rename, extract it to a named pure function in the API mapping file or owning entity/feature `lib`, then call it from `mapData`.

Do not replace validation with type assertions:

```ts
// bad
mapData: ({ result }) => result as User;
```

## Error mapping

Normalize errors close to the remote operation or in shared API infrastructure.

Examples:

- transport error
- non-2xx HTTP status
- validation error
- unauthorized
- forbidden
- backend domain error
- network timeout/offline

UI should consume a stable project error union, not parse arbitrary backend or Farfetched internals.

Current Farfetched `mapError` receives an object. In `createJsonQuery`/`createJsonMutation`, place it under `response` and destructure at least `error`; use `params` and `headers` when the project error mapper needs context.

```ts
// good
mapError: ({ error, params, headers }) => mapRemoteError(error, { params, headers });

// bad: old/ambiguous shape; easy to break during Farfetched upgrades
mapError: (error) => mapRemoteError(error);
```

`mapError` must be pure and must not throw. If normalization itself can fail, move that logic into an effect before the Farfetched operation or return a safe fallback error.

```ts
export type RemoteError =
  | { kind: 'unauthorized' }
  | { kind: 'forbidden' }
  | { kind: 'validation'; message: string }
  | { kind: 'network'; message: string }
  | { kind: 'unknown'; message: string };

response: {
  contract: UserDtoContract,
  mapError: ({ error, params, headers }): RemoteError =>
    mapRemoteError(error, { params, headers }),
}
```

## Concurrency

Use the `concurrency` operator, not a factory config field.

Common strategies:

- `TAKE_LATEST` for search, filters, autocomplete, and route params that change quickly, when aborting stale requests is desired and tested
- `TAKE_EVERY` for independent requests; this is the default
- `TAKE_FIRST` only when skipped starts are truly the desired remote-operation behavior and `$pending`/`finished.skip` behavior is covered by tests

```ts
concurrency(searchQuery, { strategy: 'TAKE_LATEST' });
concurrency(independentMutation, { strategy: 'TAKE_EVERY' });
```

### Submit de-duplication

Do not use `TAKE_FIRST` as the default answer for form submits. Prefer an explicit Effector `$pending` gate around the user-intent event. This keeps duplicate-click policy visible in the feature/page model and avoids coupling UI submit semantics to Farfetched cancellation/skip internals.

```ts
export const formSubmitted = createEvent<FormValues>();

concurrency(saveProfileMutation, { strategy: 'TAKE_EVERY' });

sample({
  clock: formSubmitted,
  source: saveProfileMutation.$pending,
  filter: (pending) => !pending,
  fn: (_pending, values) => values,
  target: saveProfileMutation.start,
});
```

If the project still chooses `TAKE_FIRST` or `TAKE_LATEST` for a mutation, add scoped/browser tests that assert `$pending` returns to `false`, `finished.finally`/`finished.skip` behavior is understood, and the UI does not remain disabled after skipped/aborted starts.

Use `abortAll` when a lifecycle event must cancel in-flight work, for example route close or logout.

```ts
concurrency(userQuery, {
  strategy: 'TAKE_LATEST',
  abortAll: userRoute.closed,
});
```

## Refresh, freshness, and cache

Use:

- `query.start` when params are known and the query must be requested
- `query.refresh` to refresh the current query with current params
- `keepFresh` to refresh on app start, reconnect, page visible, language change, interval, or other triggers
- `cache` to reuse previous results and define stale/purge policy

Important `keepFresh` nuance: it refreshes queries that have already been started at least once. If the query has never been started, a trigger alone does not create first params by magic. Connect the first `start` to route open, app start, or a model event, then use `keepFresh` for revalidation.

```ts
import { keepFresh } from '@farfetched/core';

sample({
  clock: userRoute.opened,
  fn: ({ params }) => ({ id: params.userId }),
  target: userQuery.start,
});

keepFresh(userQuery, {
  triggers: [pageBecameVisible, networkCameOnline],
});
```

Use `cache` when stale data policy is explicit:

```ts
import { cache } from '@farfetched/core';

cache(userQuery, {
  staleAfter: '5 minutes',
  purge: '1 hour',
});
```

Do not manually call underlying effects when query semantics already exist.

## Cache update after mutation

Use `update` only when local cache modification is safe and predictable.

Safe examples:

- replacing an item by id after update
- prepending a newly created item when backend order is known
- removing an item after delete if permissions/filtering cannot change the list unexpectedly

Prefer invalidation/refresh when backend sorting, filtering, permissions, aggregation, computed fields, or user-specific visibility can change the result.

```ts
import { update } from '@farfetched/core';

update(userQuery, {
  on: updateUserMutation,
  by: {
    success: ({ query, mutation }) => ({
      result: mutation.result,
      refetch: false,
    }),
  },
});
```

If the exact `update` object shape differs in the installed Farfetched version, follow the current Farfetched docs for that version; keep the architectural rule the same: update only when it is semantically safe, otherwise refresh.

## Barriers and auth refresh

Use `createBarrier` + `applyBarrier` for flows where remote operations must pause/retry around a shared condition:

- token refresh
- global auth restoration
- maintenance/unavailable resource
- rate-limit or server-unavailable gate

Typical cookie-based refresh barrier:

```ts
import {
  applyBarrier,
  createBarrier,
  createJsonMutation,
  isHttpErrorCode,
} from '@farfetched/core';
import { SessionContract } from '@/entities/session';
import { apiUrl } from '@/shared/api/base-url';

export const refreshSessionMutation = createJsonMutation({
  request: {
    method: 'POST',
    url: apiUrl('/auth/refresh'),
    fetch: { credentials: 'include' },
  },
  response: {
    contract: SessionContract,
  },
});

export const authBarrier = createBarrier({
  activateOn: {
    failure: isHttpErrorCode(401),
  },
  perform: [refreshSessionMutation],
});
```

Apply the barrier to operations that need the same auth policy:

```ts
applyBarrier([userQuery, updateUserMutation], { barrier: authBarrier });
```

Rules:

- Keep pure transport helpers in `shared/api` only when they have no domain imports.
- If a barrier imports session/user contracts, updates session state, or coordinates many operations, place it at the owning domain/app integration boundary; in strict FSD use `effector-fsd` for placement.
- Apply barriers close to the operation or in an app-level integration module so reviewers can see the remote behavior.
- Keep UI redirects out of barriers. Convert refresh failure into app/session events, then route from page/app routing models.
- Do not make every operation depend on an auth barrier if some endpoints are intentionally public.

## Atomic Router integration

Use `@farfetched/atomic-router` when a Farfetched Query is the route loader. Its docs warn that the Atomic Router integration API can be version-sensitive, so check the installed versions before generating exact helper signatures.

- `startChain(query)` starts the query unconditionally before opening the chained route.
- `freshChain(query)` refreshes the query only when it is stale.
- `barrierChain(barrier)` waits for a Farfetched barrier to deactivate before route opening.

```ts
import { chainRoute, createRoute } from 'atomic-router';
import { freshChain, startChain } from '@farfetched/atomic-router';
import { postQuery } from '@/entities/post';

export const postRoute = createRoute<{ postId: string }>();

export const postLoadedRoute = chainRoute({
  route: postRoute,
  ...startChain(postQuery), // for required first load
});

export const postFreshRoute = chainRoute({
  route: postRoute,
  ...freshChain(postQuery), // for cache-aware re-open
});
```

If query params do not match route open payload, add a small adapter in the page model or create a page-specific query whose params shape is the route payload. Do not hide route-param mapping in React components.

## Placement examples

These paths are examples only. For normative Feature-Sliced Design placement rules, use `effector-fsd`.

```txt
shared/api/http.ts                         # base request helpers, headers, base URL
shared/api/errors.ts                       # project RemoteError mapping
entities/session/api/session-refresh-barrier.ts # session-aware barrier example
app/api/apply-auth-barriers.ts              # app-level barrier application example
entities/user/model/user.contract.ts       # User DTO/domain validation
entities/user/model/user.mapper.ts         # DTO -> domain mapper if non-trivial
entities/user/api/user.query.ts            # reusable user reads
features/profile-update/api/mutation.ts    # profile update action
pages/users/api/users-page.query.ts        # page-specific list query
pages/users/model/users-page.model.ts      # route/filter/page orchestration
```

## Testing

Test the model behavior around operations, not Farfetched internals.

- Use `fork`/`allSettled` for flows that start queries/mutations.
- Mock project-level API handlers/effects according to the public testing API of the installed Farfetched version.
- Assert domain events, stores, and route decisions.
- Do not depend on undocumented fields under Farfetched internals.

## Anti-patterns

### Raw fetch effect

```ts
const loadFx = createEffect(() => fetch('/api/user').then((r) => r.json()));
```

Prefer `createJsonQuery` with a contract.

### Contract-less response

```ts
response: {
  mapData: ({ result }) => result as User,
}
```

Add a contract.

### Deprecated credentials option

```ts
// bad in new Farfetched code
createJsonQuery({
  request: { method: 'GET', url: '/me' },
  credentials: 'include',
});
```

Use `request.fetch.credentials`:

```ts
createJsonQuery({
  request: {
    method: 'GET',
    url: '/me',
    fetch: { credentials: 'include' },
  },
});
```

### `keepFresh` without first start

```ts
keepFresh(userQuery, { triggers: [appStarted] });
// but userQuery was never started with params
```

Start the query on route/app event first; use `keepFresh` for revalidation.

### Blind optimistic update

Do not patch cached lists if backend sorting/filtering/permissions can change the visible result. Refresh instead.

### Barrier with UI policy inside shared API

Do not redirect to login from a Farfetched barrier. Emit auth/session facts and let app/page routing decide.

### Query/mutation in component

Do not create or configure Farfetched operations in React components.

## Full-audit checks for Farfetched operations

When auditing a project, create an operation table before judging the code:

```txt
operation | owner | starters | refresh/invalidation clocks | concurrency | abortAll | cache/update | auth error reaction
```

This table catches problems that single-file review misses.

### Duplicated starts

Flag any query that can be started by more than one route/layout/page event during the same navigation, especially when `TAKE_EVERY` is configured or left as default.

```ts
sample({ clock: layoutOpened, target: productsQuery.start });
sample({ clock: productsPageOpened, target: productsQuery.start });
```

Fix with a single semantic request event, a pending/cache guard, split operations, or deliberate `TAKE_LATEST`/`TAKE_FIRST` depending on desired semantics.

### `TAKE_EVERY` everywhere is not a decision

`TAKE_EVERY` is valid for independent operations, but if every query/mutation in the codebase sets it explicitly, audit whether it was copy-pasted. For route/search/filter reads, stale responses can win unless the operation is cancelled or deduped. For submit mutations, duplicate-click behavior must be explicit and tested.

### Unauthorized mapping must feed auth lifecycle

A `mapError` returning `{ kind: 'unauthorized' }` is incomplete until an app/session/barrier model consumes it.

```ts
const failed = merge([
  userQuery.finished.failure,
  saveUserMutation.finished.failure,
]);

sample({
  clock: failed,
  filter: ({ error }) => mapRemoteError(error).kind === 'unauthorized',
  fn: () => undefined,
  target: sessionCleared,
});
```

Keep this cross-operation wiring in `app` or a documented integration owner; do not put routing/session side effects into generic `shared/api` mappers.

### Prefer success payload to query `$data` on success

On `operation.finished.success`, prefer the event payload:

```ts
sample({
  clock: referenceQuery.finished.success,
  fn: ({ result }) => result.items,
  target: itemsReceived,
});
```

Avoid reading `referenceQuery.$data` from `source` on that same clock unless you intentionally need previous cached data.

### Route/page lifecycle cancellation

For page-owned route loaders and quick route param changes, consider cancellation:

```ts
concurrency(orderQuery, {
  strategy: 'TAKE_LATEST',
  abortAll: orderRoute.closed,
});
```

If cancellation is not used, document why stale results cannot affect visible state.

# Anti-patterns

## Contents

This file covers Effector ecosystem anti-patterns. Use `effector-fsd` for structure, import-boundary, public API, and slice anti-patterns.

- Effector anti-patterns
- Farfetched anti-patterns
- React anti-patterns
- Persistence anti-patterns

## Effector anti-patterns

### Units in React render

```tsx
function Component() {
  const clicked = createEvent(); // bad
}
```

### Business logic in `watch`

```ts
formSubmitted.watch(() => {
  saveFx(); // bad
});
```

### Store reads through `getState`

```ts
const submitFx = createEffect(() => {
  const values = $values.getState(); // bad
});
```

Use `sample({ source: $values, clock: submitted })` or `attach`.

### Imperative effect orchestration

```ts
const flowFx = createEffect(async () => {
  await saveFx();
  await reloadFx();
  route.open();
});
```

Use events and `sample`.

### Derived store as target

```ts
const $fullName = combine($firstName, $lastName, (first, last) => `${first} ${last}`);

sample({
  clock: resetClicked,
  fn: () => '',
  target: $fullName, // bad
});
```

Target writable stores/events/effects, not derived stores.

### Returning `undefined` accidentally

```ts
$value.on(changed, (_, value) => {
  if (!value) return undefined; // bad unless skipVoid:false is deliberate
  return value;
});
```

Return previous state or model absence explicitly as `null`/union.

### Oversized all-in-one model

Do not keep several workflows in one large model just because they belong to one page or feature.

Bad signs:

- form state, filters, list loading, selection, dialogs, and bulk actions in one file
- long chains of unrelated `sample` blocks that require reading the whole file
- stores/events/effects split into technical buckets instead of responsibility-based models

Split by concern:

```txt
model/form.model.ts
model/filters.model.ts
model/list.model.ts
model/selection.model.ts
model/dialog.model.ts
model/page.model.ts
```

The top-level model should orchestrate submodels with `sample` and expose a clear public shape. Each submodel should own its local state and rules.

### Long inline transformations in reactive operators

Do not hide complex mapping, sorting, grouping, normalization, or formatting inside `combine`, `sample.fn`, or store `.map`.

```ts
// bad
export const $rows = combine($users, $permissions, (users, permissions) =>
  users
    .filter((user) => permissions[user.id]?.canView)
    .sort((left, right) => left.name.localeCompare(right.name))
    .map((user) => ({
      id: user.id,
      title: `${user.name} (${user.role})`,
      canEdit: permissions[user.id]?.canEdit ?? false,
    })),
);
```

Use a named pure function and let the model stay declarative:

```ts
export const $rows = combine($users, $permissions, toUserRows);
```

Put DTO mapping near `mapData`/API mapping code, domain calculations near the owning domain module, and UI-only formatting at the presentation boundary.

## Farfetched anti-patterns

### Fetch effects for HTTP endpoints

```ts
const loadUserFx = createEffect(() => fetch('/user').then((r) => r.json()));
```

Prefer `createJsonQuery` with a contract.

### Type assertion instead of contract

```ts
mapData: ({ result }) => result as User;
```

Validate runtime data.

### Concurrency in obsolete config shape

```ts
// bad for current Farfetched style
createJsonQuery({
  // ...
  concurrency: { strategy: 'TAKE_LATEST' },
});
```

Use the operator:

```ts
concurrency(query, { strategy: 'TAKE_LATEST' });
```

### Blind `TAKE_FIRST` for submits

```ts
// fragile default: duplicate-click policy is hidden inside remote-operation concurrency
concurrency(saveMutation, { strategy: 'TAKE_FIRST' });
```

Prefer a visible feature/page-level gate:

```ts
concurrency(saveMutation, { strategy: 'TAKE_EVERY' });

sample({
  clock: formSubmitted,
  source: saveMutation.$pending,
  filter: (pending) => !pending,
  fn: (_pending, values) => values,
  target: saveMutation.start,
});
```

Use `TAKE_FIRST` only after testing skipped lifecycle and `$pending` reset in the same Scope/browser setup the project uses.

### Blind optimistic update

Do not patch cached lists if backend sorting/filtering/permissions can change visibility.

### Query/mutation created in component

Create remote operations statically in API/model files owned by the relevant module.

## React anti-patterns

### Many `useUnit` calls from the same model

```tsx
// bad by default
const value = useUnit($value);
const error = useUnit($error);
const onChange = useUnit(changedEvent);
const onSubmit = useUnit(submittedEvent);
```

Prefer one shape:

```tsx
const { value, error, onChange, onSubmit } = useUnit($$form);
```

### Raw event/effect call from component

```tsx
// bad in Scope-aware apps
<button onClick={() => submittedEvent()}>Save</button>
```

Bind with `useUnit`:

```tsx
const { onSubmit } = useUnit({ onSubmit: submittedEvent });
<button onClick={() => onSubmit()}>Save</button>
```

### API call in component

```tsx
onClick={async () => {
  await api.save(values); // bad
}}
```

Use model event and mutation.

### Domain condition in UI

```tsx
if (user.role === 'admin' && invoice.status === 'draft') {
  // complex workflow logic in JSX
}
```

Move to model or domain lib.

### Translated strings in domain stores

```ts
export const $statusText = createStore('User is blocked'); // bad for domain model
```

Store domain state and translate in UI/presentation.

## Persistence anti-patterns

### Persisting unvalidated external values

```ts
persist({ store: $theme, key: 'theme' }); // incomplete in Scope/external-data-sensitive apps
```

Use `contract` and explicit `pickup` when scopes are used.

### Persisting secrets by default

Do not store tokens in localStorage/sessionStorage unless the security model explicitly accepts the risk.

## Routing and startup anti-patterns

### Free-floating scoped bootstrap sequence

```ts
await startAppClock(scope);
await allSettled(appStarted, { scope });
await startRouter(scope);
```

This is wrong by default. Do not normalize it as “just bootstrap code”. Prefer one explicit `appStarted` event and declarative connections. Move router/clock/history installation into scoped effects started by `appStarted` whenever possible:

```ts
await allSettled(appStarted, { scope, params: startParams });

sample({ clock: appStarted, target: appClockStartedFx });
sample({ clock: appStarted, target: routerStartedFx });
sample({ clock: routerStartedFx.doneData, target: initialRouteResolved });
```

### Route data loading in React effect

```tsx
useEffect(() => {
  userQuery.start({ id: params.id });
}, [params.id]);
```

Start from route events, `chainRoute`, Farfetched route integration, or `pageStarted`.

### Protected route as JSX wrapper only

```tsx
return isAuthenticated ? children : <Navigate to="/login" />;
```

This may be acceptable as a tiny presentation fallback, but it must not be the only business guard. Put auth restoration, loaded route opening, cancellation, and redirects into the routing model.

## Farfetched-specific anti-patterns

### Top-level `credentials`

```ts
createJsonQuery({
  request: { method: 'GET', url: '/me' },
  credentials: 'include',
});
```

Use `request.fetch.credentials` in new Farfetched code:

```ts
request: {
  method: 'GET',
  url: '/me',
  fetch: { credentials: 'include' },
}
```

### Body in GET/HEAD request

```ts
request: {
  method: 'GET',
  url: '/search',
  body: ({ query }) => ({ query }),
}
```

Use `query` for URL search params.

### `keepFresh` before first start

```ts
keepFresh(userQuery, { triggers: [appStarted] });
```

This is incomplete if the query has never received params. Trigger the first `start` from route/app/page model, then use `keepFresh` for revalidation.

### Auth barrier performs navigation

```ts
// auth/session barrier module
refreshSessionMutation.finished.failure.watch(() => loginRoute.open());
```

Shared API infrastructure should emit session/auth facts. App/page routing decides navigation.

## Next.js anti-patterns

### Global server Scope

```ts
// bad
export const serverScope = fork();
```

Create a fresh Scope per request/page computation.

### Missing plugin/SIDs with SSR

Do not rely on SSR serialization without stable SIDs from the Effector Babel/SWC plugin.

### Raw event in Client Component

```tsx
'use client';

<button onClick={() => submitted()}>Save</button>
```

Use `useUnit`:

```tsx
const { onSubmit } = useUnit({ onSubmit: submitted });
<button onClick={() => onSubmit()}>Save</button>
```

### Effector hook in Server Component

```tsx
// missing 'use client'
const user = useUnit($user);
```

Hooks belong to Client Components. Server Components can create Scope, run `allSettled`, serialize values, and render Client Components.

### App Router layout depends on page-loaded store

A parent layout should not assume it can read stores filled by a deeper page Server Component during the same server render. Load layout-critical data at the layout boundary or move the decision to the page.

### `serialize: 'ignore'` as a lazy fix

Do not silence serialization problems by ignoring stores that must hydrate. Use explicit store design or custom serialization for non-serializable values.

## Production audit anti-patterns

### Router starts before auth restore

```ts
sample({ clock: appStarted, target: [browserHistoryCreatedFx, sessionQuery.start] });
```

If the router can open protected routes before the session query resolves, direct reloads may redirect to login/dashboard and lose the original route. Either start router after restore finishes, or model auth as `unknown` and make guards wait.

### Session clear without route policy

```ts
sample({ clock: loggedOut, target: sessionCleared });
// no redirect/route close reacts to sessionCleared
```

A layout that returns `null` for anonymous users is not a route policy. Redirect from app/page routing when a protected route is opened and session is cleared.

### Unauthorized error mapped but not consumed

```ts
if (response.status === 401) return { kind: 'unauthorized' };
// no app-level sample reacts to this RemoteError
```

Normalizing `401` is only half the flow. Auth-sensitive operation failures must feed session/barrier policy and route redirects.

### Page model reacts while route is closed

```ts
// pages/users/model.ts
sample({ clock: userUpdated, target: usersQuery.start });
```

Effector models are static. Once imported, this sample reacts regardless of whether `UsersPage` is rendered. Gate by `usersRoute.$isOpened` or move invalidation to an app/entity owner.

### Duplicate query starts from layout and page

```ts
sample({ clock: adminLayoutOpened, target: ordersQuery.start });
sample({ clock: ordersRoute.opened, target: ordersQuery.start });
concurrency(ordersQuery, { strategy: 'TAKE_EVERY' });
```

This can make duplicate requests on one navigation. Add a request event with pending/cache guard, split a badge query from a list query, or choose a deliberate concurrency/cancellation policy.

### Scope callback handle stored globally

```ts
let unsubscribe: (() => void) | null = null;

const startFx = createEffect(() => {
  const handler = scopeBind(eventFromCallback);
  unsubscribe = sdk.listen(handler);
});
```

The callback may be scope-bound, but the handle is shared across Scopes/tests/HMR instances. Store handles in Effector stores or return them through effect results and stop via scoped lifecycle.

### Declared destroy event is never called

```ts
export const appDestroyed = createEvent();
sample({ clock: appDestroyed, target: stopClockFx });

// entrypoint never calls appDestroyed on unmount/HMR
```

Dead lifecycle events hide leaks. Verify cleanup is wired from entrypoint, route close, or test teardown.

### Throwing inside `sample.fn`

```ts
sample({
  clock: formSubmitted,
  source: $form,
  fn: (form) => ({ expiresAt: new Date(form.expiresAt).toISOString() }),
  target: mutation.start,
});
```

Validation/parsing that can throw must be modeled before mutation start. Otherwise the feature error flow is bypassed.

### Reading operation `$data` on its own success clock

```ts
sample({
  clock: query.finished.success,
  source: query.$data,
  fn: (data) => derive(data),
  target: derivedReceived,
});
```

Use `{ result }` from `query.finished.success`. Reading `$data` relies on update ordering and makes the dependency less clear.

### Local async pending around Effector event

```tsx
await onConfirm(); // onConfirm is an Effector event returned by useUnit and resolves immediately
```

Do not model mutation progress with local React pending if the real operation is Farfetched/Effector. Move dialog/confirm state to the feature/page model and read mutation `$pending`.

### Huge VM tied to a global ticker

```ts
const $vm = combine({ list: $list, dialog: $dialog, now: $currentTimestamp }).map(toHugeVm);
```

A global clock can recompute an entire page VM even when only expiration labels need time. Split VM stores or gate ticks by route open.

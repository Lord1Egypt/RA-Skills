# Production audit playbook for Effector ecosystem apps

Use this file when reviewing a real project, especially when the user asks for a “full audit”, “best practices audit”, or “why did the previous audit miss issues?”. The goal is to catch cross-cutting problems that are invisible when reviewing files one-by-one.

## Contents

- [Audit method](#audit-method)
- [Startup, auth restore, and router ordering](#startup-auth-restore-and-router-ordering)
- [Unauthorized errors are not enough until they affect session](#unauthorized-errors-are-not-enough-until-they-affect-session)
- [Farfetched concurrency, duplicated starts, and stale results](#farfetched-concurrency-duplicated-starts-and-stale-results)
- [Page models are static: gate page-local reactions](#page-models-are-static-gate-page-local-reactions)
- [Scope-safe external callbacks and cleanup](#scope-safe-external-callbacks-and-cleanup)
- [Reactive purity: `sample.fn` must not throw](#reactive-purity-samplefn-must-not-throw)
- [Prefer success payload over operation `$data` on success clock](#prefer-success-payload-over-operation-data-on-success-clock)
- [React callback contracts and local pending](#react-callback-contracts-and-local-pending)
- [Oversized VM stores and global ticking sources](#oversized-vm-stores-and-global-ticking-sources)
- [Test isolation](#test-isolation)
- [Reporting template](#reporting-template)

## Audit method

Do not only grep for local anti-patterns. Build a small map of the static Effector graph:

```txt
entrypoint -> fork/Provider -> appStarted -> session restore/storage pickup -> router/history -> route.opened
route.opened -> page/model events -> queries/mutations
mutation/query failures -> error stores/session facts/redirects
logout/session clear -> stores/routes/remote cancellation
external callbacks -> scopeBind -> events
```

For every event that can change auth, route, or remote data, ask: “who reacts, and is the route/page still the right owner when this unit fires?”. Remember that imported Effector modules are active globally inside a Scope; a `sample` in a page model still reacts even when that page component is not rendered unless it is gated by route state or imported only lazily.

## Startup, auth restore, and router ordering

### Audit questions

- Does the browser history/router open the current URL before session restore finishes?
- Is there an explicit `unknown/authenticated/anonymous` session state, or does `$isAuthenticated === false` mean both “not checked yet” and “anonymous”?
- Does protected-route logic preserve original route params/query after async session restore?
- Does `sessionCleared` while already inside a protected route redirect or close the route?
- Does logout trigger both session state reset and route state update?

### Red flags

```ts
sample({ clock: appStarted, target: [browserHistoryCreatedFx, sessionQuery.start] });
```

If `browserHistoryCreatedFx` can synchronously install history and open routes while `sessionQuery` is pending, protected routes may see a false anonymous state and redirect incorrectly.

```tsx
// Layout fallback only; not a routing policy
if (!isAuthenticated) return null;
```

This can hide a logout bug by showing a blank protected layout instead of navigating to login.

### Better pattern: auth known before router installation

```ts
import { createEvent, merge, sample } from 'effector';
import { router, browserHistoryCreatedFx } from '../routes/router';
import { sessionQuery, sessionReceived, sessionCleared } from '@/entities/session';

export const appStarted = createEvent();

const sessionRestoreFinished = merge([
  sessionQuery.finished.success,
  sessionQuery.finished.failure,
]);

sample({ clock: appStarted, target: sessionQuery.start });

sample({
  clock: sessionQuery.finished.success,
  filter: ({ result }) => Boolean(result.session),
  fn: ({ result }) => result.session!,
  target: sessionReceived,
});

const sessionRestoreFailed = sessionQuery.finished.failure;

const anonymousSessionRestored = sample({
  clock: sessionQuery.finished.success,
  filter: ({ result }) => !result.session,
});

sample({
  clock: [sessionRestoreFailed, anonymousSessionRestored],
  fn: () => undefined,
  target: sessionCleared,
});

sample({
  clock: sessionRestoreFinished,
  fn: () => undefined,
  target: browserHistoryCreatedFx,
});
sample({ clock: browserHistoryCreatedFx.doneData, target: router.setHistory });
```

If product requirements need the router to start before auth restore, model session as `unknown` and make protected-route guards wait for `authenticated`/`anonymous`, never raw `false`.

### Better pattern: redirect on session clear inside protected area

```ts
import { combine, sample } from 'effector';
import { redirect } from 'atomic-router';
import { sessionCleared } from '@/entities/session';
import { loginRoute } from '@/pages/login';

const $isProtectedAreaOpened = combine(
  protectedRoutes.map((route) => route.$isOpened),
  (opened) => opened.some(Boolean),
);

const protectedSessionCleared = sample({
  clock: sessionCleared,
  source: $isProtectedAreaOpened,
  filter: Boolean,
});

redirect({
  clock: protectedSessionCleared,
  route: loginRoute,
  replace: true,
});
```

## Unauthorized errors are not enough until they affect session

### Audit questions

- Does the shared/API error mapper normalize `401`/`403` but nobody listens to those failures?
- Are all auth-sensitive Farfetched operations covered by a barrier or an app-level unauthorized handler?
- Does a `401` from any page query/mutation clear the session and trigger the same route policy as logout?
- Are refresh barriers and redirects separated: barrier/session state in entity/app, navigation in app routes?

### Red flag

```ts
export const mapRemoteError = (error): RemoteError => {
  if (status === 401) return { kind: 'unauthorized' };
  return { kind: 'unknown' };
};

// no sample/merge/app integration ever reacts to kind === 'unauthorized'
```

### Better pattern

```ts
import { merge, sample } from 'effector';
import { sessionCleared } from '@/entities/session';
import { mapRemoteError } from '@/shared/api';

const authSensitiveOperationFailed = merge([
  userQuery.finished.failure,
  ordersQuery.finished.failure,
  updateProfileMutation.finished.failure,
  // every operation that relies on auth, or a generated registry
]);

sample({
  clock: authSensitiveOperationFailed,
  filter: ({ error }) => mapRemoteError(error).kind === 'unauthorized',
  fn: () => undefined,
  target: sessionCleared,
});
```

Put this wiring in `app` or another cross-cutting integration owner, not inside `shared/api`.

## Farfetched concurrency, duplicated starts, and stale results

### Audit questions

- List every `query.start`, `query.refresh`, mutation `.start`, and route loader.
- Can the same query be started by both a layout and a page on one route open?
- Are queries that can be restarted quickly using `TAKE_LATEST` or an explicit pending/cache/stale guard?
- Are submit mutations protected from duplicate clicks with a visible `$pending` gate or a tested concurrency policy?
- Does `TAKE_EVERY` appear because it is intentional, or because it was copied everywhere?
- Are in-flight requests aborted on route close/logout when stale responses can update UI after the user leaves?

### Red flag

```ts
sample({ clock: layoutOpened, target: ordersQuery.start });
sample({ clock: ordersPageOpened, target: ordersQuery.start });
concurrency(ordersQuery, { strategy: 'TAKE_EVERY' });
```

This can create duplicate network requests on the same navigation.

### Better options

Centralize a request event with a guard:

```ts
export const ordersRequested = createEvent();

sample({
  clock: ordersRequested,
  source: ordersQuery.$pending,
  filter: (pending) => !pending,
  fn: () => undefined,
  target: ordersQuery.start,
});
```

Or use an intentional strategy:

```ts
concurrency(ordersQuery, {
  strategy: 'TAKE_LATEST',
  abortAll: ordersRoute.closed,
});
```

Do not blindly replace every mutation with `TAKE_FIRST`. If duplicate-click prevention is a UI/business rule, keep it visible:

```ts
sample({
  clock: submitted,
  source: saveMutation.$pending,
  filter: (pending) => !pending,
  fn: (_pending, params) => params,
  target: saveMutation.start,
});
```

## Page models are static: gate page-local reactions

### Audit questions

- Does `App` or a route registry import all pages at startup?
- Do page models listen to feature mutation successes or entity events?
- Are those reactions gated by `route.$isOpened` or page lifetime?
- Should refresh/invalidation live in an entity/app integration instead of a page model?

### Red flag

```ts
sample({
  clock: [itemCreated, itemDeleted],
  target: itemsQuery.start,
});
```

If this code lives in `pages/items/model`, it still reacts while another page is opened unless the module is truly lazy and disposed, which most Effector modules are not.

### Better pattern

```ts
sample({
  clock: [itemCreated, itemDeleted],
  source: itemsRoute.$isOpened,
  filter: Boolean,
  fn: () => undefined,
  target: itemsQuery.start,
});
```

For many pages that need the same refresh policy, create a semantic invalidation event in the entity/app integration layer and let each opened page decide how to reload.

## Scope-safe external callbacks and cleanup

### Audit questions

- Are timers/listeners/SDK callbacks registered inside effects that are started from `appStarted`/page events?
- Is every callback that later calls an Effector unit wrapped with `scopeBind` or a scope-aware adapter?
- Are external resource handles stored per Scope, not in a module-level singleton?
- Does `appDestroyed`, route close, or HMR actually stop timers/listeners?

### Red flag

```ts
let intervalId: number | null = null;

export const startClockFx = createEffect(() => {
  const tick = scopeBind(timestampChanged);
  intervalId = window.setInterval(() => tick(Date.now()), 60_000);
});

export const stopClockFx = createEffect(() => {
  if (intervalId !== null) window.clearInterval(intervalId);
});
```

`scopeBind` protects the event call, but `intervalId` is shared between Scopes/tests/HMR instances.

### Better pattern

```ts
const startClockFx = createEffect(() => {
  const tick = scopeBind(timestampChanged);
  tick(Date.now());
  return window.setInterval(() => tick(Date.now()), 60_000);
});

const stopClockFx = createEffect((intervalId: number) => {
  window.clearInterval(intervalId);
});

const $clockIntervalId = createStore<number | null>(null)
  .on(startClockFx.doneData, (_, id) => id)
  .reset(stopClockFx.done);

sample({
  clock: appClockStarted,
  source: $clockIntervalId,
  filter: (id) => id === null,
  target: startClockFx,
});

sample({
  clock: appClockStopped,
  source: $clockIntervalId,
  filter: (id): id is number => id !== null,
  target: stopClockFx,
});
```

## Reactive purity: `sample.fn` must not throw

### Audit questions

- Does `sample.fn` parse dates, JSON, URLs, numbers, regexes, or optional nested data without validation?
- Can a pure mapping throw and bypass the intended error store/mutation failure handling?
- Are validation errors modeled as events/stores before the remote operation starts?

### Red flag

```ts
sample({
  clock: formSubmitted,
  source: $form,
  fn: (form) => ({
    ...form,
    expiresAt: new Date(form.expiresAt).toISOString(),
  }),
  target: createLinkMutation.start,
});
```

`toISOString()` throws on an invalid date. The mutation never starts, and the feature error flow may not run.

### Better pattern

```ts
const validationFailed = createEvent<string>();

const $validationError = $form.map((form) => {
  const date = new Date(form.expiresAt);
  if (Number.isNaN(date.getTime())) return 'Invalid expiration date';
  return null;
});

sample({
  clock: formSubmitted,
  source: { form: $form, error: $validationError, pending: createLinkMutation.$pending },
  filter: ({ error, pending }) => !error && !pending,
  fn: ({ form }) => ({ ...form, expiresAt: new Date(form.expiresAt).toISOString() }),
  target: createLinkMutation.start,
});

sample({
  clock: formSubmitted,
  source: $validationError,
  filter: Boolean,
  target: validationFailed,
});
```

## Prefer success payload over operation `$data` on success clock

### Audit question

When handling `query.finished.success`, does the model read `query.$data` from `source` instead of using `clock.result`?

### Red flag

```ts
sample({
  clock: referenceQuery.finished.success,
  source: referenceQuery.$data,
  fn: (data) => fillForm(data),
  target: formFilled,
});
```

This relies on store update ordering. The success payload already contains the data that caused the event.

### Better pattern

```ts
sample({
  clock: referenceQuery.finished.success,
  fn: ({ result }) => fillForm(result),
  target: formFilled,
});
```

If additional source state is needed:

```ts
sample({
  clock: referenceQuery.finished.success,
  source: $form,
  fn: (form, { result }) => fillMissingReferences(form, result),
  target: formChanged,
});
```

## React callback contracts and local pending

### Audit questions

- Does a component expect `onConfirm: () => Promise<void>` while the caller passes an Effector event returned from `useUnit`?
- Is local `isPending` used to represent a mutation owned by Effector/Farfetched?
- Does the dialog close immediately because an Effector event returns `void`?

### Red flag

```tsx
async function handleConfirm() {
  setIsPending(true);
  await onConfirm(); // Effector event returns void immediately
  setIsPending(false);
  onClose();
}
```

### Better pattern

Move confirm state to a feature/page model:

```ts
export const deletionRequested = createEvent<Item>();
export const deletionConfirmed = createEvent();
export const deletionDialogClosed = createEvent();

export const $itemToDelete = createStore<Item | null>(null)
  .on(deletionRequested, (_, item) => item)
  .reset([deletionDialogClosed, deleteItemMutation.finished.success]);

sample({
  clock: deletionConfirmed,
  source: { item: $itemToDelete, pending: deleteItemMutation.$pending },
  filter: ({ item, pending }) => Boolean(item) && !pending,
  fn: ({ item }) => ({ id: item!.id }),
  target: deleteItemMutation.start,
});
```

The dialog reads `pending` from the mutation and closes from model state, not by awaiting an event.

## Oversized VM stores and global ticking sources

### Audit questions

- Does one `$vm` combine route state, data rows, labels, dialogs, loading, errors, and a global clock/store?
- Does a global timer cause heavy list mapping for a page that is closed?
- Would splitting `rows`, `toolbar`, `dialog`, and `time` stores reduce recomputation and re-render?

### Red flag

```ts
export const $pageVm = combine({
  rows: $rows,
  dialog: $dialog,
  loading: $loading,
  error: $error,
  currentTimestamp: $currentTimestamp,
}).map(toPageVm);
```

If `toPageVm` maps/sorts a large list, every clock tick recomputes everything.

### Better pattern

```ts
const pageTicked = createEvent<number>();

const $pageTimestamp = createStore(0)
  .on(pageTicked, (_, value) => value)
  .reset(pageRoute.closed);

sample({
  clock: currentTimestampChanged,
  source: pageRoute.$isOpened,
  filter: Boolean,
  fn: (_, timestamp) => timestamp,
  target: pageTicked,
});

export const $rowsVm = combine($rows, $permissions, toRowsVm);
export const $dialogVm = combine($selected, mutation.$pending, $error, toDialogVm);
```

## Test isolation

### Audit questions

- Do tests configure effect handlers through `fork({ handlers })`?
- Is there a global `fx.use(...)` in a test helper that hides missing handlers?
- Do tests create fresh Scopes and call `allSettled` instead of invoking units directly?

### Red flag

```ts
fetchFx.use(testFetchHandler);

export const createTestScope = () => fork({
  handlers: [[fetchFx, testFetchHandler]],
});
```

The global `.use` makes the scoped handler look optional.

### Better pattern

```ts
export const createTestScope = () => fork({
  handlers: [[fetchFx, testFetchHandler]],
});
```

Leave the base effect unhandled globally so tests fail when they forget the handler.

## Reporting template

For each finding, report:

```txt
Severity: critical/high/medium/low
Files/evidence: path:line and unit names
Graph chain: event/store/effect -> sample/combine -> consequence
Why this matters: user-visible bug, race, stale data, scope leak, or maintainability risk
Fix: minimal code/pattern
Acceptance criterion: observable behavior or test condition
```

Do not write “best practices are mostly followed” until you have completed the startup/auth, remote-operation, scope, and page-lifetime passes above.

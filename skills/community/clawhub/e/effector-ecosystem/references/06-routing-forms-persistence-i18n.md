# Routing, forms, persistence, i18n, and browser APIs

Use this file for integration topics around Effector models.

## Contents

- Routing with Atomic Router
- Protected routes and auth
- Farfetched route loaders
- Forms
- Persistence with `effector-storage`
- i18n
- Browser APIs with `@withease/web-api`
- Application startup

## Routing with Atomic Router

Use `atomic-router` when routes are part of Effector data flow.

Common placement:

```txt
shared/routes/index.ts          # route declarations/paths shared by app
app/routes/router.ts            # router/history configuration
pages/profile/route.ts          # page route ownership/re-export if needed
pages/profile/model/page.model.ts
```

Route model pattern:

```ts
import { createRoute, chainRoute } from 'atomic-router';
import { sample } from 'effector';
import { profileQuery } from '@/entities/user';

export const profileRoute = createRoute<{ userId: string }>();

sample({
  clock: profileRoute.opened,
  fn: ({ params }) => ({ id: params.userId }),
  target: profileQuery.start,
});
```

Rules:

- Route declarations may live in `shared/routes` only when they are domain-neutral route contracts/paths.
- Route-to-data orchestration belongs to page/app models, not React components.
- Use `chainRoute` when opening a route must wait for data, permission checks, or auth restoration before a child/loaded route becomes active.
- Use `redirect`/navigation samples from model events; do not call router APIs directly in feature UI.
- If route params change quickly and start remote operations, set Farfetched concurrency deliberately.

## Protected routes and auth

Protected routes are a model concern. Do not hide auth checks in React route components.

Basic synchronous guard:

```ts
import { chainRoute, type RouteInstance, type RouteParams, type RouteParamsAndQuery } from 'atomic-router';
import { createEvent, sample } from 'effector';
import { $isAuthenticated } from '@/entities/session';

export function chainAuthenticated<Params extends RouteParams>(route: RouteInstance<Params>) {
  const sessionCheckStarted = createEvent<RouteParamsAndQuery<Params>>();

  const alreadyAuthenticated = sample({
    clock: sessionCheckStarted,
    filter: $isAuthenticated,
  });

  return chainRoute({
    route,
    beforeOpen: sessionCheckStarted,
    openOn: alreadyAuthenticated,
  });
}
```

Async auth restoration needs an explicit pending route attempt so `openOn` can emit the original route params/query after the session query succeeds:

```ts
import {
  chainRoute,
  type RouteInstance,
  type RouteParams,
  type RouteParamsAndQuery,
} from 'atomic-router';
import { createEvent, createStore, merge, sample } from 'effector';
import { currentSessionQuery, $sessionState } from '@/entities/session';

export function chainAuthenticated<Params extends RouteParams>(route: RouteInstance<Params>) {
  const sessionCheckStarted = createEvent<RouteParamsAndQuery<Params>>();

  const $pendingAttempt = createStore<RouteParamsAndQuery<Params> | null>(null)
    .on(sessionCheckStarted, (_, attempt) => attempt);

  const alreadyAuthenticated = sample({
    clock: sessionCheckStarted,
    filter: $sessionState.map((state) => state === 'authenticated'),
  });

  sample({
    clock: sessionCheckStarted,
    filter: $sessionState.map((state) => state === 'unknown'),
    fn: () => undefined,
    target: currentSessionQuery.start,
  });

  const authenticatedAfterRestore = sample({
    clock: currentSessionQuery.finished.success,
    source: {
      attempt: $pendingAttempt,
      sessionState: $sessionState,
    },
    filter: ({ attempt, sessionState }) =>
      attempt !== null && sessionState === 'authenticated',
    fn: ({ attempt }) => attempt!,
  });

  const knownAnonymous = sample({
    clock: sessionCheckStarted,
    filter: $sessionState.map((state) => state === 'anonymous'),
  });

  const anonymousAfterRestore = sample({
    clock: currentSessionQuery.finished.success,
    source: {
      attempt: $pendingAttempt,
      sessionState: $sessionState,
    },
    filter: ({ attempt, sessionState }) =>
      attempt !== null && sessionState === 'anonymous',
    fn: ({ attempt }) => attempt!,
  });

  const restoreFailed = sample({
    clock: currentSessionQuery.finished.failure,
    source: $pendingAttempt,
    filter: (attempt) => attempt !== null,
    fn: (attempt) => attempt!,
  });

  const rejected = merge([knownAnonymous, anonymousAfterRestore, restoreFailed]);

  $pendingAttempt.reset([alreadyAuthenticated, authenticatedAfterRestore, rejected, route.closed]);

  return chainRoute({
    route,
    beforeOpen: sessionCheckStarted,
    openOn: [alreadyAuthenticated, authenticatedAfterRestore],
    cancelOn: rejected,
  });
}
```

Redirect anonymous users from app/page routing, not from the shared guard if the guard is supposed to be reusable:

```ts
sample({
  clock: protectedRouteRejected,
  fn: () => ({ params: {}, query: { reason: 'auth' } }),
  target: loginRoute.navigate,
});
```

Keep auth state in `entities/session`. Keep login/logout user actions in `features/session-login` and `features/session-logout`. Keep route protection composition in `app/routes` or page route files depending on how global it is.

## Farfetched route loaders

Use Farfetched Atomic Router integration when a Farfetched Query is the route loader. Treat exact helper types as version-sensitive because Atomic Router/Farfetched integration APIs have changed over time.

```ts
import { chainRoute, createRoute } from 'atomic-router';
import { startChain, freshChain, barrierChain } from '@farfetched/atomic-router';
import { postQuery } from '@/entities/post';
import { sessionRefreshBarrier } from '@/entities/session';

export const postRoute = createRoute<{ postId: string }>();

export const postAuthorizedRoute = chainRoute({
  route: postRoute,
  ...barrierChain(sessionRefreshBarrier),
});

export const postLoadedRoute = chainRoute({
  route: postAuthorizedRoute,
  ...startChain(postQuery),
});

export const postFreshRoute = chainRoute({
  route: postAuthorizedRoute,
  ...freshChain(postQuery),
});
```

Use `startChain` when every route open must request the data. Use `freshChain` when cache/stale policy is already configured and a fresh cached result is acceptable.

When query params do not match route params, map them in the page model:

```ts
sample({
  clock: postRoute.opened,
  fn: ({ params }) => ({ id: params.postId }),
  target: postQuery.start,
});
```

Then use `chainRoute` manually with `openOn`/`cancelOn` if you need the loaded child route to wait for that query. Do not perform this mapping in React.

## Forms

### Plain Effector form

Default form structure:

```ts
export const nameChanged = createEvent<string>();
export const formSubmitted = createEvent();

export const $name = createStore('').on(nameChanged, (_, value) => value);
export const $errors = combine($name, (name) => ({ name: name ? null : 'Required' }));
export const $isValid = $errors.map((errors) => !errors.name);

sample({
  clock: formSubmitted,
  source: $name,
  filter: $isValid,
  fn: (name) => ({ name }),
  target: updateProfileMutation.start,
});
```

Use for most forms unless a dedicated form library clearly reduces boilerplate.

### `effector-forms`

Use `effector-forms` when you need a form abstraction with field-level state, validation, touched/dirty metadata, and repeated patterns.

Keep form ownership in the feature/page model. UI may use `useForm` or expose a model shape for `useUnit`.

## Persistence with `effector-storage`

Persist only safe external state:

- theme
- locale
- UI preferences
- safe filters
- local drafts

Do not persist secrets or large remote data without a deliberate security/cache strategy.

Use contracts because external storage is untrusted.

```ts
import { createEvent, createStore } from 'effector';
import { persist } from 'effector-storage/local';
import { or, val } from '@withease/contracts';

export const appStarted = createEvent();
export const themeChanged = createEvent<'light' | 'dark'>();

export const $theme = createStore<'light' | 'dark'>('light')
  .on(themeChanged, (_, theme) => theme);

persist({
  store: $theme,
  key: 'theme',
  contract: or(val('light'), val('dark')),
  pickup: appStarted,
});
```

For Scope/SSR, prefer explicit `pickup` to load the value in the right Scope.

Use `clock` when storage writes should happen only on a specific event.

In Next.js, never persist secrets in browser storage. Prefer HTTP-only cookies for sessions and read them at the server/API boundary.

## i18n

Use `i18next`/`react-i18next` for ordinary UI translations.

Use `@withease/i18next` when language must participate in Effector data flow.

Typical placement:

```txt
shared/i18n/
  i18n.ts
  i18n.model.ts
app/providers/i18n-provider.tsx
features/language-switch/model/
```

Rules:

- store language/code/domain values, not already translated strings
- translate in UI or at a presentation boundary
- use language store as source for language-dependent queries
- refresh language-dependent queries on language change when needed

Example flow:

```ts
sample({
  clock: languageChanged,
  target: changeLanguageFx,
});
```

With Farfetched, combine `$language` with query params or use `keepFresh` on language changes after the query has been started once.

## Browser APIs with `@withease/web-api`

Use Web API integrations for browser signals instead of scattering listeners in components.

Useful signals:

- online/offline
- page visibility
- media queries
- orientation
- languages
- geolocation

Pattern:

```ts
export const appStarted = createEvent();
export const appDestroyed = createEvent();

// integration created in shared/lib or app integration
// setup: appStarted, teardown: appDestroyed
```

Use page visibility or network status as Farfetched `keepFresh` triggers when refetching on focus/reconnect is desired.

For callbacks that fire after adapter installation, bind route/session events with `scopeBind` inside the scoped adapter effect.

## Application startup

Prefer one explicit app-start event:

```ts
export const appStarted = createEvent<AppStartParams>();
```

Use it to:

- initialize browser integrations
- pick up persisted state
- start initial queries
- initialize i18n
- attach router/history adapters
- restore auth/session

Do not hide initialization in random component effects.

Default scoped bootstrap:

```ts
const scope = fork();
await allSettled(appStarted, { scope, params: startParams });
```

Avoid free-floating sequences by default. First move router/history/clock/browser integration setup into effects started by `appStarted`. Leave a free-floating startup helper only when it is a documented last-resort host adapter boundary:

```ts
await startAppClock(scope);
await allSettled(appStarted, { scope });
await startRouter(scope);
```

Better model the dependency graph:

```ts
sample({ clock: appStarted, target: storagePickupStarted });
sample({ clock: appStarted, target: routerStartedFx });
sample({ clock: routerStartedFx.doneData, target: initialRouteResolved });
sample({ clock: initialRouteResolved, target: pageStarted });
```

## Audit additions for routing, auth, and forms

### Router start must not race auth restore

When the app has protected routes and current-session restore, check the initial startup order. If `appStarted` starts router/history and session restore in parallel, the router may open the current protected URL against an anonymous default state. Prefer either:

1. restore session first, then install/open router; or
2. use a three-state auth model (`unknown | authenticated | anonymous`) and make protected routes wait until state is known.

### Redirect on session loss is part of protected routing

Protected routing must handle not only route open, but also session loss while already inside a protected area:

```ts
const $isProtectedRouteOpened = combine(
  protectedRoutes.map((route) => route.$isOpened),
  (opened) => opened.some(Boolean),
);

const protectedSessionLost = sample({
  clock: sessionCleared,
  source: $isProtectedRouteOpened,
  filter: Boolean,
});

redirect({ clock: protectedSessionLost, route: loginRoute, replace: true });
```

Do not rely on protected layouts returning `null` as the only logout/session-expiry behavior.

### Preserve route params through async auth checks

If a guard starts `currentSessionQuery`, keep the original route params/query in a pending-attempt store and emit that attempt on success. Do not reconstruct params from the session-query result.

### Form transformation must not throw

Before a submit mutation, validate user input in stores/events. Do not parse dates, URLs, JSON, or numbers in `sample.fn` in a way that can throw and bypass feature error handling. Use a validation error store and only start the mutation when it is empty.

### Confirmation dialogs should not await Effector events

If a shared dialog accepts `onConfirm: () => Promise<void>`, do not pass an Effector event and expect it to wait for a mutation. Either pass a real effect promise intentionally, or preferably model confirmation state in the feature/page and bind the dialog to `$pending`, `$itemToConfirm`, and confirm/close events.

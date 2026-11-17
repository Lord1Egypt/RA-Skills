This example uses FSD-like paths only to make imports readable. For normative placement and import-boundary rules, use `effector-fsd`.

# Example: protected routes + auth + Farfetched

This example focuses on placement, not exact Farfetched API details.

## Tree

```txt
src/
  app/
    model/app.model.ts
    routes/protected.ts
    routes/auth-redirects.ts
    api/apply-auth-barriers.ts

  pages/
    dashboard/
      index.ts
      route.ts
      ui/dashboard-page.tsx
      model/page.model.ts
      api/dashboard.query.ts
    login/
      index.ts
      route.ts
      ui/login-page.tsx

  features/
    session-login/
      index.ts
      ui/login-form.tsx
      model/login.model.ts
      api/login.mutation.ts
    session-logout/
      index.ts
      model/logout.model.ts

  entities/
    session/
      index.ts
      model/session.model.ts
      model/session.contract.ts
      api/current-session.query.ts
      api/session-refresh-barrier.ts

  shared/
    api/base-url.ts
    api/errors.ts
    api/http.ts
    routes/index.ts
```

## Ownership

- `entities/session` owns session state, session contract, current-session query, refresh barrier.
- `features/session-login` owns login form and login mutation.
- `app/routes/protected.ts` owns reusable protected-route composition.
- `pages/dashboard/route.ts` owns dashboard route and page-specific route chain.
- `app/routes/auth-redirects.ts` owns redirect policy.
- `shared/api` stays transport-only and imports no entities/routes.

## Session entity

```ts
// entities/session/index.ts
export { $sessionState, $isAuthenticated, sessionReceived, sessionDropped } from './model/session.model';
export { SessionContract } from './model/session.contract';
export { currentSessionQuery } from './api/current-session.query';
export { sessionRefreshBarrier } from './api/session-refresh-barrier';
```

## Protected route composition

```ts
// app/routes/protected.ts
import {
  chainRoute,
  type RouteInstance,
  type RouteParams,
  type RouteParamsAndQuery,
} from 'atomic-router';
import { createEvent, createStore, merge, sample } from 'effector';
import { $sessionState, currentSessionQuery } from '@/entities/session';

export function chainAuthenticated<Params extends RouteParams>(route: RouteInstance<Params>) {
  const sessionCheckStarted = createEvent<RouteParamsAndQuery<Params>>();

  const $pendingAttempt = createStore<RouteParamsAndQuery<Params> | null>(null)
    .on(sessionCheckStarted, (_, attempt) => attempt)
    .reset(route.closed);

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

  $pendingAttempt.reset([alreadyAuthenticated, authenticatedAfterRestore, rejected]);

  return {
    route: chainRoute({
      route,
      beforeOpen: sessionCheckStarted,
      openOn: [alreadyAuthenticated, authenticatedAfterRestore],
      cancelOn: rejected,
    }),
    rejected,
  };
}
```
## Page route

```ts
// pages/dashboard/route.ts
import { createRoute } from 'atomic-router';
import { chainAuthenticated } from '@/app/routes/protected';

export const dashboardRoute = createRoute();

export const {
  route: dashboardAuthenticatedRoute,
  rejected: dashboardAuthRejected,
} = chainAuthenticated(dashboardRoute);
```
## Redirects

```ts
// app/routes/auth-redirects.ts
import { combine, merge, sample } from 'effector';
import { redirect } from 'atomic-router';
import { sessionCleared } from '@/entities/session';
import { dashboardAuthRejected, dashboardRoute } from '@/pages/dashboard/route';
import { loginRoute } from '@/pages/login/route';

const protectedRouteRejected = merge([
  dashboardAuthRejected,
  // add other protected route rejections here
]);

redirect({
  clock: protectedRouteRejected,
  route: loginRoute,
  replace: true,
});

const $isProtectedAreaOpened = combine(
  [dashboardRoute.$isOpened /* add other protected routes */],
  (opened) => opened.some(Boolean),
);

const sessionClearedInsideProtectedArea = sample({
  clock: sessionCleared,
  source: $isProtectedAreaOpened,
  filter: Boolean,
});

redirect({
  clock: sessionClearedInsideProtectedArea,
  route: loginRoute,
  replace: true,
});
```

Redirect on `sessionCleared` is required for logout and expired-session flows while the user is already inside a protected route. A layout that renders `null` for anonymous users is not enough.
## Barrier placement

```ts
// entities/session/api/session-refresh-barrier.ts
import { createBarrier } from '@farfetched/core';
import { refreshSessionMutation } from './refresh-session.mutation';

export const sessionRefreshBarrier = createBarrier({
  active: refreshSessionMutation.$pending,
  perform: [refreshSessionMutation.start, refreshSessionMutation.finished.failure],
});
```

Applying to many operations:

```ts
// app/api/apply-auth-barriers.ts
import { applyBarrier } from '@farfetched/core';
import { sessionRefreshBarrier } from '@/entities/session';
import { dashboardQuery } from '@/pages/dashboard/api/dashboard.query';

applyBarrier(dashboardQuery, { barrier: sessionRefreshBarrier });
```

Do not put this session-aware barrier in `shared/api`, because it owns session-domain behavior.

# Next.js with Effector

Use this file when the project uses Next.js with Effector, Farfetched, or Atomic Router. Next.js has multiple runtimes and rendering boundaries; treat Scope and serialization as architecture, not as glue code.

## Contents

- Default rule
- Plugin and SIDs
- App Router
- Pages Router
- Client components
- Server computations
- Server Actions
- Next router integration
- Farfetched in Next.js
- Startup model
- Caveats
- Path examples
- Anti-patterns

## Default rule

Use `@effector/next` when Next.js SSR/SSG/RSC hydration must work with Effector Scope.

Do not keep one global mutable Scope on the server. Create a Scope per request/page computation with `fork`, run model events with `allSettled`, serialize the Scope, and pass serialized values to `EffectorNext`.

## Plugin and SIDs

Enable the Effector Babel/SWC plugin in Next.js.

Reasons:

- stable SIDs for `serialize`/`hydrate`
- better names and debugging
- factories support
- SSR-safe model instances

Typical SWC setup:

```js
// next.config.js
const nextConfig = {
  compiler: {
    // keep other Next compiler options here
  },
  experimental: {
    swcPlugins: [
      [
        '@effector/swc-plugin',
        {
          factories: [
            'atomic-router',
            '@withease/factories',
            // add local factory paths when used
            // '@/shared/lib/create-list-model',
          ],
        },
      ],
    ],
  },
};

module.exports = nextConfig;
```

Use the exact plugin field supported by the installed Next.js version. The architecture requirement is stable SIDs and configured factories.

## App Router

Root provider pattern:

```tsx
// app/layout.tsx
import { EffectorNext } from '@effector/next';
import type { ReactNode } from 'react';

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <EffectorNext>{children}</EffectorNext>
      </body>
    </html>
  );
}
```

Server page pattern:

```tsx
// app/users/[userId]/page.tsx
import { allSettled, fork, serialize } from 'effector';
import { EffectorNext } from '@effector/next';
import { notFound, redirect } from 'next/navigation';
import { pageStarted, $userNotFound, $shouldRedirectToLogin } from '@/pages/user/model/page.model';
import { UserPage } from '@/pages/user';

export default async function Page({ params }: { params: { userId: string } }) {
  const scope = fork();

  await allSettled(pageStarted, {
    scope,
    params: { userId: params.userId },
  });

  // getState is acceptable here only at the Next.js boundary for framework decisions.
  if (scope.getState($userNotFound)) {
    notFound();
  }

  if (scope.getState($shouldRedirectToLogin)) {
    redirect('/login');
  }

  return (
    <EffectorNext values={serialize(scope)}>
      <UserPage />
    </EffectorNext>
  );
}
```

Rules:

- Server Components can run scoped model events with `fork`/`allSettled`.
- Client components must use `useUnit` and be marked with `'use client'` when they call React hooks.
- Use `scope.getState` only at framework boundaries such as `notFound`, `redirect`, `generateMetadata`, or `generateStaticParams`. Do not move production workflow logic to `getState`.
- Prefer page-level server computations over hidden component-level bootstrap.

## Pages Router

Use `@effector/next` provider in `_app` and run page events inside `getServerSideProps`/`getStaticProps`.

```tsx
// pages/_app.tsx
import { EffectorNext } from '@effector/next';
import type { AppProps } from 'next/app';

export default function App({ Component, pageProps }: AppProps) {
  return (
    <EffectorNext values={pageProps.values}>
      <Component {...pageProps} />
    </EffectorNext>
  );
}
```

```ts
// pages/users/[userId].tsx
import { allSettled, fork, serialize } from 'effector';
import { pageStarted, $userNotFound, $shouldRedirectToLogin } from '@/pages/user/model/page.model';

export async function getServerSideProps(ctx) {
  const scope = fork();

  await allSettled(pageStarted, {
    scope,
    params: { userId: String(ctx.params.userId) },
  });

  return {
    props: {
      values: serialize(scope),
    },
  };
}
```

For new apps, prefer App Router unless the project has a strong reason to stay on Pages Router.

## Client components

```tsx
'use client';

import { useUnit } from 'effector-react';
import { $$userPage } from '../model/page.model';

export function UserPageView() {
  const { user, pending, onRefreshClick } = useUnit($$userPage);

  return (
    <section>
      <h1>{user?.displayName}</h1>
      <button disabled={pending} onClick={() => onRefreshClick()}>
        Refresh
      </button>
    </section>
  );
}
```

Rules:

- Do not call raw events/effects from JSX in Scope-aware apps.
- Use one object/array `useUnit` shape per connected component by default.
- Do not create Effector units, factories, Farfetched operations, or routes in Client Component render.

## Server computations

Every server-side page computation should have one explicit model event:

```ts
export const pageStarted = createEvent<{ userId: string }>();

sample({
  clock: pageStarted,
  fn: ({ userId }) => ({ id: userId }),
  target: userQuery.start,
});
```

Then Next.js calls only that event:

```ts
const scope = fork();
await allSettled(pageStarted, { scope, params: { userId } });
const values = serialize(scope);
```

This keeps SSR/SSG, tests, and client bootstrap aligned.

## Server Actions

Server Actions may be used as effect handlers when a first-party mutation must execute on the server.

Keep the same model contract:

- model exposes `formSubmitted`
- `sample` maps values to a mutation/effect
- handler is injected at the Next boundary or operation layer
- UI still calls bound events through `useUnit`

Do not call a Server Action directly from a deeply nested dumb UI component if that bypasses the model workflow.

## Next router integration

When app logic must navigate with Next router, keep the router instance in an adapter model and attach it from a client provider.

```ts
// shared/router/next-router.model.ts
import { attach, createEvent, createStore, sample } from 'effector';
import type { AppRouterInstance } from 'next/dist/shared/lib/app-router-context.shared-runtime';

export const routerAttached = createEvent<AppRouterInstance>();
export const navigationTriggered = createEvent<string>();

const $router = createStore<AppRouterInstance | null>(null).on(
  routerAttached,
  (_, router) => router,
);

const pushFx = attach({
  source: $router,
  effect: (router, href: string) => {
    if (!router) return;
    router.push(href);
  },
});

sample({
  clock: navigationTriggered,
  target: pushFx,
});
```

```tsx
'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useUnit } from 'effector-react';
import { routerAttached } from './next-router.model';

export function NextRouterProvider() {
  const router = useRouter();
  const attachRouter = useUnit(routerAttached);

  useEffect(() => {
    attachRouter(router);
  }, [attachRouter, router]);

  return null;
}
```

Use Atomic Router for Effector-native routing in SPA-like flows. Use the Next router adapter for Next-specific navigation APIs, redirects that must happen on the client, or incremental migration.

## Farfetched in Next.js

Use the same Farfetched operation rules as in ordinary Effector apps:

- create queries/mutations statically in their owning modules
- validate responses with contracts
- start route/page queries from `pageStarted` or route events
- use `allSettled(pageStarted, { scope, params })` in server code
- serialize only intended stores

Cookie-based requests on the server may need framework-specific cookie/header forwarding. Keep that in shared API infrastructure or page-specific server boundary; do not put `cookies()` calls inside reusable entity API modules unless those modules are explicitly Next-only.

## Startup model

Use one application-level event and one page-level event family:

```ts
export const appStarted = createEvent<AppStartParams>();
export const pageStarted = createEvent<PageStartParams>();
```

Prefer this over several free-floating startup functions:

```ts
// bad by default: order is implicit and hard to test
await startAppClock(scope);
await allSettled(appStarted, { scope });
await startRouter(scope);
```

Better:

```ts
await allSettled(appStarted, { scope, params: startParams });
```

and model the sequence declaratively:

```ts
sample({ clock: appStarted, target: [storagePickupStarted, i18nStarted] });
sample({ clock: appStarted, target: routerStartedFx });
sample({ clock: routerStartedFx.done, target: initialRouteResolved });
```

Default: represent router/history/clock/browser integration setup as scoped effects started from `appStarted`. Last-resort exception: an external adapter may need imperative host wiring before the first event, for example attaching a history listener or SDK callback. In that case, make the exception explicit, use `scopeBind` for callbacks that fire later, and keep business decisions behind `appStarted`/route events.

## Caveats

- Do not share server Scope between requests.
- Ensure stores that must be serialized have stable SIDs.
- App Router and Pages Router can coexist during migration, but crossing between them may cause full reloads; do not design state continuity around mixed-router navigation.
- In App Router, parent layouts are not automatically aware of stores filled by deeper page Server Components during the same server render. Avoid layout-level decisions that depend on page-loaded stores unless you load that data at the layout level.
- Avoid non-serializable store values in SSR. If unavoidable, define explicit custom serialization/hydration at the store boundary.
- Do not use `serialize: 'ignore'` as a lazy fix for stores that should actually hydrate.

## Path examples

These paths are illustrative. Use `effector-fsd` for normative FSD/Next.js placement decisions.

```txt
src/app/layout.tsx                         # EffectorNext root provider
src/app/providers/next-router-provider.tsx # client Next router adapter attach
src/app/model/app.model.ts                 # appStarted/appDestroyed orchestration
src/pages/<page>/model/page.model.ts       # pageStarted and route/page orchestration
src/entities/<entity>/api/*.query.ts       # reusable remote operations
src/shared/api/*.ts                        # base URL, errors, headers/cookie adapters
```

## Anti-patterns

### Global server Scope

```ts
// bad
export const scope = fork();
```

Create a new Scope per request/page computation.

### Raw event from Client Component

```tsx
<button onClick={() => formSubmitted()}>Save</button>
```

Use `useUnit`.

### Page bootstrap in `useEffect`

```tsx
useEffect(() => {
  userQuery.start({ id });
}, [id]);
```

Start from `pageStarted`, route events, or explicit model events.

### Hidden Next router in features

Do not call `useRouter` inside feature business logic. Attach router in app/shared adapter and navigate through model events.

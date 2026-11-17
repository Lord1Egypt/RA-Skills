# Routing and Next.js placement

Use this file when placing Atomic Router, protected routes, framework routes, and Next.js adapters.

## Contents

- Atomic Router placement
- Protected routes
- Farfetched route loaders
- Next.js folder conflict
- Next.js App Router adapter
- Server and client public APIs
- Pages Router

## Atomic Router placement

```txt
shared/routes/index.ts                 # domain-neutral route contracts/paths
app/routes/router.ts                   # createHistoryRouter / controls / history
app/routes/protected.ts                # global protected route helper/composition
app/routes/routes-view.tsx             # routes view adapter
pages/dashboard/route.ts               # page-owned route and loaded route
pages/dashboard/model/page.model.ts    # route params -> data loading
```

Route declarations may be shared only when they are domain-neutral contracts. Page-specific route loading and query composition belongs to the page.

## Protected routes

Strict default:

- `entities/session` owns session state and session refresh query/mutation/barrier.
- `features/session-login` and `features/session-logout` own user actions.
- `app/routes/protected.ts` owns reusable protected route composition if global.
- `pages/<page>/route.ts` owns page route + local chain.
- `app/routes/redirects.ts` or page route model owns redirects.

Do not redirect from `shared/api` or a pure transport barrier.

Example tree:

```txt
app/routes/protected.ts
app/routes/redirects.ts
pages/dashboard/route.ts
entities/session/model/session.model.ts
entities/session/api/current-session.query.ts
features/session-login/model/login.model.ts
```

## Farfetched route loaders

When using `@farfetched/atomic-router`:

- `startChain(query)` for unconditional load.
- `freshChain(query)` when stale/cache semantics matter.
- `barrierChain(barrier)` when route opening must wait for a barrier.

Placement:

```txt
pages/post/route.ts                    # chainRoute + startChain/freshChain
entities/post/api/post.query.ts        # reusable post query
pages/post/model/page.model.ts         # map route params, page facts
```

If a barrier is session-domain-aware, import it from `entities/session` only in a layer that is allowed to import entities, such as page/feature/widget/app.

## Next.js folder conflict

Next.js uses `app` and `pages` framework folders. FSD also has `app` and `pages` layers. Prefer official FSD-compatible structure:

```txt
app/                         # Next.js App Router folder at project root
pages/                       # Next.js Pages Router folder, if used
src/
  _app/                      # FSD App layer
  _pages/                    # FSD Pages layer
  widgets/
  features/
  entities/
  shared/
```

Use `_app` and `_pages` even if only one Next router is active. This avoids ambiguity and works better with FSD tooling.

## Next.js App Router adapter

```tsx
// app/users/[userId]/page.tsx
export { UserPage as default, metadata } from '@/_pages/user';
```

For Effector SSR/RSC:

```tsx
// app/users/[userId]/page.tsx
import { allSettled, fork, serialize } from 'effector';
import { EffectorNext } from '@effector/next';
import { UserPage } from '@/_pages/user';
import { pageStarted } from '@/_pages/user/model/page.model';

export default async function Page({ params }: { params: { userId: string } }) {
  const scope = fork();

  await allSettled(pageStarted, {
    scope,
    params: { userId: params.userId },
  });

  return (
    <EffectorNext values={serialize(scope)}>
      <UserPage />
    </EffectorNext>
  );
}
```

Keep business decisions in `_pages/user/model/page.model.ts`; the framework file is an adapter.

## Server and client public APIs

When a slice has both server-only and client-safe exports, split public APIs:

```txt
_pages/user/index.ts          # client-safe exports
_pages/user/index.server.ts   # server-only exports
```

Never export server-only code from a client public API that may be imported by a Client Component.

## Pages Router

Use the same principle: Next framework `pages` re-exports FSD `_pages`.

```tsx
// pages/users/[userId].tsx
export { UserPage as default } from '@/_pages/user';
```

Custom `_app`:

```tsx
// pages/_app.tsx
export { App as default } from '@/_app/custom-app';
```

# Example: Next.js App Router with Effector Scope

## Structure

```txt
src/
  app/
    layout.tsx
    users/[userId]/page.tsx
    providers/next-router-provider.tsx
  pages/
    user/
      index.ts
      model/page.model.ts
      ui/user-page.tsx
  entities/user/
    api/user.query.ts
    model/user.contract.ts
  shared/router/next-router.model.ts
```

## Root layout

```tsx
// app/layout.tsx
import { EffectorNext } from '@effector/next';
import type { ReactNode } from 'react';
import { NextRouterProvider } from './providers/next-router-provider';

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <EffectorNext>
          <NextRouterProvider />
          {children}
        </EffectorNext>
      </body>
    </html>
  );
}
```

## Page server adapter

```tsx
// app/users/[userId]/page.tsx
import { allSettled, fork, serialize } from 'effector';
import { EffectorNext } from '@effector/next';
import { notFound, redirect } from 'next/navigation';
import { UserPage } from '@/pages/user';
import { pageStarted, $notFound, $shouldRedirectToLogin } from '@/pages/user/model/page.model';

export default async function Page({ params }: { params: { userId: string } }) {
  const scope = fork();

  await allSettled(pageStarted, {
    scope,
    params: { userId: params.userId },
  });

  if (scope.getState($notFound)) {
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

Use `scope.getState` only at this framework boundary for `notFound`, `redirect`, `generateMetadata`, or `generateStaticParams` decisions.

## Page model

```ts
// pages/user/model/page.model.ts
import { createEvent, combine, sample } from 'effector';
import { userQuery } from '@/entities/user';

export const pageStarted = createEvent<{ userId: string }>();
export const refreshClicked = createEvent();

sample({
  clock: pageStarted,
  fn: ({ userId }) => ({ id: userId }),
  target: userQuery.start,
});

sample({
  clock: refreshClicked,
  target: userQuery.refresh,
});

export const $notFound = userQuery.$error.map((error) => error?.kind === 'not-found');
export const $shouldRedirectToLogin = userQuery.$error.map((error) => error?.kind === 'unauthorized');

export const $$userPage = {
  user: userQuery.$data,
  pending: userQuery.$pending,
  onRefreshClick: refreshClicked,
};
```

## Client page view

```tsx
// pages/user/ui/user-page.tsx
'use client';

import { useUnit } from 'effector-react';
import { $$userPage } from '../model/page.model';

export function UserPage() {
  const { user, pending, onRefreshClick } = useUnit($$userPage);

  if (!user) return null;

  return (
    <section>
      <h1>{user.displayName}</h1>
      <button disabled={pending} onClick={() => onRefreshClick()}>
        Refresh
      </button>
    </section>
  );
}
```

## Next router adapter

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
    if (router) router.push(href);
  },
});

sample({ clock: navigationTriggered, target: pushFx });
```

```tsx
// app/providers/next-router-provider.tsx
'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useUnit } from 'effector-react';
import { routerAttached } from '@/shared/router/next-router.model';

export function NextRouterProvider() {
  const router = useRouter();
  const attachRouter = useUnit(routerAttached);

  useEffect(() => {
    attachRouter(router);
  }, [attachRouter, router]);

  return null;
}
```

## Rules checked by this example

- The server adapter creates a fresh Scope.
- The model has one `pageStarted` event.
- Remote data is loaded from the model, not from React `useEffect`.
- Client components use `useUnit`.
- Next navigation is an adapter, not feature business logic.

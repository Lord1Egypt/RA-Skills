# Example: Next.js App Router + Effector + FSD

## Tree

```txt
app/                               # Next.js framework folder
  layout.tsx
  users/[userId]/page.tsx
src/
  _app/                            # FSD App layer
    providers/effector-next.tsx
    model/app.model.ts
  _pages/
    user/
      index.ts
      index.server.ts
      ui/user-page.tsx
      model/page.model.ts
  entities/
    user/
      index.ts
      api/user.query.ts
      model/user.contract.ts
  shared/
    api/base-url.ts
    api/errors.ts
```

## Framework route adapter

```tsx
// app/users/[userId]/page.tsx
import { allSettled, fork, serialize } from 'effector';
import { EffectorNext } from '@effector/next';
import { UserPage } from '@/_pages/user';
import { pageStarted } from '@/_pages/user/index.server';

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

## Page public APIs

```ts
// src/_pages/user/index.ts
export { UserPage } from './ui/user-page';

// src/_pages/user/index.server.ts
export { pageStarted } from './model/page.model';
```

## Rule

Next framework files stay thin. FSD `_pages/user/model/page.model.ts` owns page orchestration; `entities/user/api/user.query.ts` owns reusable user read.

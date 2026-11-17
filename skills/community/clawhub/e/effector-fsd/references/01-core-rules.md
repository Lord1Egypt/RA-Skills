# FSD core rules for Effector projects

Use this file to decide structural rules before choosing an exact Effector implementation.

## Contents

- Layers
- Import rule
- App and Shared exceptions
- Slices
- Segments
- Public API rule
- `@x` cross-imports
- Incremental adoption

## Layers

Default order:

```txt
app -> pages -> widgets -> features -> entities -> shared
```

`processes` exists in older FSD material but is deprecated. Avoid it; move multi-page orchestration into `app` or focused features/pages.

You do not have to use every layer. Add a layer only when it helps navigation and ownership.

## Import rule

A module inside a slice can import only:

- files from the same slice using relative imports
- public APIs of slices on lower layers
- public APIs of `shared` segments

Forbidden by default:

```ts
// entity importing feature: upward import
import { submitProfileUpdate } from '@/features/profile-update';

// feature importing another feature: same-layer cross-import
import { $$loginForm } from '@/features/session-login';

// direct import from another slice internals
import { $session } from '@/entities/session/model/session.model';
```

Allowed:

```ts
import { $session } from '@/entities/session';
import { apiUrl } from '@/shared/api';
```

## App and Shared exceptions

`app` and `shared` do not contain business slices. They contain segments directly.

`app` can import all lower layers because it composes the application.

`shared` should not import business layers at all. Shared segments can import each other when it stays domain-independent.

## Slices

Slices are business/product/domain units inside sliced layers:

```txt
pages/profile
widgets/user-card-list
features/profile-update
entities/user
```

Good slice qualities:

- high cohesion: most code for that product concern is nearby
- low coupling: no accidental sibling-slice dependencies
- business-oriented name, not technical name
- public API that hides internals

## Segments

Segments group by technical purpose inside a slice:

```txt
ui/
model/
api/
lib/
config/
```

Use custom segment names only when the purpose is clear and stable. Avoid `components`, `hooks`, `utils`, `helpers`, `types`, `store` as top-level segment names because they become technical dumps.

## Public API rule

Every slice must provide a public API.

```txt
entities/user/index.ts
features/profile-update/index.ts
pages/profile/index.ts
```

External imports go through this public API. Internal imports inside a slice are relative.

Good public API exposes only what other owners need:

```ts
export { UserAvatar } from './ui/user-avatar';
export { userQuery } from './api/user.query';
export { $user, sessionReceived } from './model/user.model';
export type { User } from './model/user.types';
```

Avoid wildcard re-exports of internals:

```ts
// bad
export * from './model/user.model';
export * from './api/user.query';
export * from './ui/user-avatar';
```

Wildcard exports are acceptable only for deliberately tiny, stable, internal libraries where the public surface is still obvious.

## `@x` cross-imports

Same-layer cross-imports are forbidden by default. For entity relationships, use `@x` only when the relationship is real and explicit.

Example:

```txt
entities/artist/@x/song.ts
entities/song/@x/artist.ts
```

Rules:

- Use `@x` mostly for entities.
- Keep `@x` narrow: types/selectors/constants, not whole models.
- Do not use `@x` to bypass poor placement.
- Prefer moving orchestration to `features`, `widgets`, or `pages` when two entities interact behaviorally.

## Incremental adoption

When migrating, do not rewrite everything. Establish:

1. Framework route adapters.
2. `app`, `pages`, `shared`.
3. Public APIs.
4. Import boundaries.
5. Extract entities/features from high-churn pages.
6. Add Steiger once the team can handle automated violations.

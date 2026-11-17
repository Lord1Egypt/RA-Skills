# Public API and import boundaries

Use this file when reviewing imports and exports.

## Contents

- Public API goals
- Good public APIs
- Bad public APIs
- Import style
- Same-layer cross-imports
- `@x` entity cross-imports
- Testing imports

## Public API goals

A public API should:

1. Protect consumers from internal refactors.
2. Expose only the necessary surface.
3. Make breaking behavior changes visible through export changes.

## Good public APIs

Entity:

```ts
// entities/user/index.ts
export { UserAvatar } from './ui/user-avatar';
export { userQuery } from './api/user.query';
export { $user, userReceived } from './model/user.model';
export type { User } from './model/user.types';
```

Feature:

```ts
// features/profile-update/index.ts
export { ProfileUpdateForm } from './ui/profile-update-form';
export { $$profileUpdate } from './model/profile-update.model';
export { updateProfileMutation } from './api/update-profile.mutation';
```

Page:

```ts
// pages/profile/index.ts
export { ProfilePage } from './ui/profile-page';
```

Server/client split:

```ts
// _pages/user/index.ts
export { UserPage } from './ui/user-page';

// _pages/user/index.server.ts
export { metadata } from './meta/metadata';
export { pageStarted } from './model/page.model';
```

## Bad public APIs

```ts
// bad: exposes everything accidentally
export * from './model';
export * from './api';
export * from './ui';
```

```ts
// bad: exporting implementation details
export { $internalFormDirty } from './model/form-internals.model';
export { mapRawBackendTrash } from './api/private.mapper';
```

```ts
// bad: layer-level barrel
// entities/index.ts
export * from './user';
export * from './session';
```

Layer-level barrels blur ownership and often enable accidental imports. Prefer slice-level public APIs.

## Import style

Inside a slice:

```ts
import { UserAvatar } from '../ui/user-avatar';
import { mapUserDto } from './user.mapper';
```

Across slices/layers:

```ts
import { UserAvatar } from '@/entities/user';
import { updateProfileMutation } from '@/features/profile-update';
```

Never import another slice's internals:

```ts
// bad
import { userQuery } from '@/entities/user/api/user.query';
```

## Same-layer cross-imports

Forbidden by default:

```ts
// features/profile-update/model.ts
import { $$sessionLogin } from '@/features/session-login'; // bad
```

Move orchestration to a higher layer:

```txt
pages/profile/model/page.model.ts
app/model/session-workflow.model.ts
```

## `@x` entity cross-imports

Use only for explicit entity relationships.

```txt
entities/song/@x/artist.ts
entities/artist/model/artist.types.ts
```

```ts
// entities/song/@x/artist.ts
export type { Song } from '../model/song.types';

// entities/artist/model/artist.types.ts
import type { Song } from '@/entities/song/@x/artist';
```

Do not export stores/events/effects through `@x` unless the relationship is impossible to model cleanly elsewhere and the team documents it.

## Testing imports

Tests may import internals only when they are colocated as slice-internal tests:

```txt
entities/user/model/user.model.test.ts
```

Cross-slice integration tests should use public APIs, like production code.

## Effector-specific public API audit

### Semantic facts over raw operation internals

When reviewing feature public APIs, distinguish between a stable capability API and implementation details.

Prefer exporting:

```ts
export const profileUpdated = updateProfileMutation.finished.success.map(
  ({ result }) => result,
);

export const $$profileUpdate = {
  form: $form,
  error: $error,
  pending: updateProfileMutation.$pending,
  onFieldChange: fieldChanged,
  onSubmit: formSubmitted,
};
```

Avoid forcing consumers to depend on:

```ts
updateProfileMutation.finished.success
$internalFormDirty
profileUpdateFormCompleted
```

Raw Farfetched operations may be public when the slice deliberately offers that operation as a stable contract, but a full audit must ask: “Could the consumer use a semantic fact/facade instead?”. If yes, narrow the public API.

### Page consumers should not know feature implementation

Bad:

```ts
import { createManagerMutation } from '@/features/manager-create';

sample({ clock: createManagerMutation.finished.success, target: usersQuery.start });
```

Good:

```ts
import { managerCreated } from '@/features/manager-create';

sample({
  clock: managerCreated,
  source: usersRoute.$isOpened,
  filter: Boolean,
  fn: () => undefined,
  target: usersQuery.start,
});
```

### Public API width checklist

- Does `index.ts` export only what another owner needs?
- Are wildcard exports exposing internal model/api files accidentally?
- Can raw mutations/effects be replaced by semantic facts?
- Are dialog/form internals wrapped in a `$$feature` facade?
- Are page contracts/API operations exported only when another allowed owner truly needs them?

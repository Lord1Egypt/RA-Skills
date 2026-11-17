# Layer recipes for Effector projects

Use this file for common placement decisions.

## Contents

- App layer
- Pages layer
- Widgets layer
- Features layer
- Entities layer
- Shared layer

## App layer

Use for composition and application lifecycle.

```txt
app/
  entrypoint/
    client.tsx
    server.tsx
  providers/
    effector-provider.tsx
    router-provider.tsx
    i18n-provider.tsx
  routes/
    router.ts
    protected.ts
    routes-view.tsx
  model/
    app.model.ts
  styles/
    globals.css
```

Examples:

- start router/history from `appStarted`
- attach Next router adapter
- connect global analytics
- apply global auth/session barrier to many operations when the barrier imports domain state
- compose route redirects after auth rejection

`app` may import lower layers. Keep it thin: composition, not feature implementation.

## Pages layer

Use for route/screen ownership.

```txt
pages/profile/
  index.ts
  route.ts
  ui/profile-page.tsx
  model/page.model.ts
  api/profile-page.query.ts
```

Page model owns:

- `pageStarted`
- route params
- page-only filters/sorting/pagination
- which queries are started on route open
- page-level redirect/error/loading facts

Do not move page-specific orchestration to a feature just to reuse folders.

## Widgets layer

Use for large independent UI blocks.

```txt
widgets/user-card-list/
  index.ts
  ui/user-card-list.tsx
  model/list-selection.model.ts
  lib/group-users.ts
```

A widget may compose entities and features:

```ts
import { UserAvatar } from '@/entities/user';
import { ProfileUpdateButton } from '@/features/profile-update';
```

Do not create widgets for small one-page components.

## Features layer

Use for user actions and business capabilities.

```txt
features/profile-update/
  index.ts
  ui/profile-update-form.tsx
  model/form.model.ts
  model/submit.model.ts
  api/update-profile.mutation.ts
  lib/map-form-to-request.ts
```

Feature may import entities and shared. It must not import pages/widgets/app or sibling features.

A feature should expose a meaningful public API:

```ts
export { ProfileUpdateForm } from './ui/profile-update-form';
export { $$profileUpdate } from './model/profile-update.model';
export { updateProfileMutation } from './api/update-profile.mutation';
```

Only export mutation/query when another layer must compose it. Keep internals private.

## Entities layer

Use for domain concepts.

```txt
entities/session/
  index.ts
  model/session.model.ts
  model/session.contract.ts
  api/current-session.query.ts
  api/refresh-session.mutation.ts
  api/session-refresh-barrier.ts
```

Entity can expose:

- domain type/contract
- reusable stores/events
- reusable read query
- small entity visual

Entity must not know pages/features/widgets. If behavior involves multiple entities, usually place it in a feature/page/app composition, not in one entity importing another.

## Shared layer

Use only for domain-independent infrastructure.

```txt
shared/api/
  base-url.ts
  errors.ts
  http.ts
shared/ui/
  button.tsx
  dialog.tsx
shared/lib/date/
  format-date.ts
shared/config/
  env.ts
shared/i18n/
  index.ts
```

Shared can include generic auth transport helpers only if they do not import session/user entities and do not make business decisions.

Bad:

```ts
// shared/api/auth-barrier.ts
import { sessionReceived } from '@/entities/session'; // forbidden: shared imports entity
import { loginRoute } from '@/pages/login';           // forbidden: shared imports page
```

Good strict alternatives:

```txt
entities/session/api/session-refresh-barrier.ts # if it updates session
app/api/apply-auth-barriers.ts                  # if it coordinates many operations
shared/api/http.ts                              # pure transport only
```

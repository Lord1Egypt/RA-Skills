# Migration playbook: custom Effector architecture to FSD

Use this file for incremental refactors.

## Contents

- Principle
- Step 1. Establish route/page boundaries
- Step 2. Create app and shared foundations
- Step 3. Unpack global API/model/store dumps
- Step 4. Extract entities
- Step 5. Extract features
- Step 6. Keep page-specific things in pages
- Step 7. Add widgets only when useful
- Step 8. Fix imports and public APIs
- Step 9. Move auth/session infrastructure carefully
- Step 10. Add tooling
- Migration checklist

## Principle

Do not rewrite the whole app. Move high-churn code first and preserve behavior with tests. FSD migration should reduce coupling, not create a ceremony tax.

## Step 1. Establish route/page boundaries

Move framework route files toward thin adapters.

Before:

```txt
src/routes/users.tsx
src/containers/users-page.tsx
src/store/users.ts
```

After:

```txt
src/pages/users/index.ts
src/pages/users/ui/users-page.tsx
src/pages/users/model/page.model.ts
```

For Next.js, prefer root framework folders plus FSD `_pages`:

```txt
app/users/page.tsx
src/_pages/users/index.ts
```

## Step 2. Create app and shared foundations

Move app-wide integration to `app`:

```txt
app/providers/
app/routes/
app/model/app.model.ts
app/entrypoint/
```

Move domain-independent infrastructure to `shared`:

```txt
shared/api/base-url.ts
shared/api/errors.ts
shared/ui/button.tsx
shared/config/env.ts
shared/lib/date/
```

Do not put domain types or entity queries into shared.

## Step 3. Unpack global API/model/store dumps

Before:

```txt
src/api/users.ts
src/api/orders.ts
src/store/index.ts
src/models/session.ts
```

After:

```txt
entities/user/api/user.query.ts
entities/order/api/order.query.ts
entities/session/model/session.model.ts
features/session-login/api/login.mutation.ts
pages/users/model/page.model.ts
```

Move code by ownership, not by type.

## Step 4. Extract entities

Start with stable business nouns:

```txt
entities/user
entities/session
entities/order
entities/product
```

Entity owns reusable type/contract/mapper/read model. It does not own page filters or action forms.

## Step 5. Extract features

Extract repeated or important user actions:

```txt
features/session-login
features/profile-update
features/comment-create
features/order-cancel
```

Feature owns action UI, form model, submit intent, mutation, and validation.

## Step 6. Keep page-specific things in pages

Do not prematurely extract:

- one-page filters
- page-specific sorting/pagination
- route-specific loading
- page-only list queries
- page-only UI blocks

These can stay in `pages/<page>` until reuse is real.

## Step 7. Add widgets only when useful

Create widget when a block is large and independent:

```txt
widgets/sidebar
widgets/dashboard-metrics
widgets/user-card-list
```

Avoid widget inflation.

## Step 8. Fix imports and public APIs

Create `index.ts` for each slice. Replace direct imports with public API imports.

Before:

```ts
import { userQuery } from '@/entities/user/api/user.query';
```

After:

```ts
import { userQuery } from '@/entities/user';
```

Inside the same slice, use relative imports.

## Step 9. Move auth/session infrastructure carefully

If current code has:

```txt
shared/api/auth-barrier.ts
```

check whether it imports session/user/routes. If yes, move:

```txt
entities/session/api/session-refresh-barrier.ts
app/api/apply-auth-barriers.ts
app/routes/auth-redirects.ts
```

Keep only generic fetch/error helpers in `shared/api`.

## Step 10. Add tooling

After the structure is mostly stable:

```bash
npm i -D steiger @feature-sliced/steiger-plugin
npx steiger ./src
```

Document exceptions. Enable stricter rules gradually.

## Migration checklist

- Framework routes are thin adapters.
- App-wide bootstrap lives in `app`.
- Shared is domain-independent.
- Pages own route/screen orchestration.
- Entities own domain facts/contracts/reusable reads.
- Features own user actions/mutations/forms.
- Public APIs exist.
- Direct internal imports are removed.
- Steiger runs in CI or local review when adopted.

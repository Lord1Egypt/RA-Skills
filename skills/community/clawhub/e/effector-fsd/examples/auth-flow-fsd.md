# Example: auth flow placement

```txt
entities/session/
  index.ts
  model/session.model.ts
  model/session.contract.ts
  api/current-session.query.ts
  api/refresh-session.mutation.ts
  api/session-refresh-barrier.ts

features/session-login/
  index.ts
  ui/login-form.tsx
  model/login.model.ts
  api/login.mutation.ts

features/session-logout/
  index.ts
  model/logout.model.ts
  api/logout.mutation.ts

pages/login/
  index.ts
  route.ts
  ui/login-page.tsx

app/routes/
  protected.ts
  auth-redirects.ts

shared/api/
  base-url.ts
  errors.ts
  http.ts
```

## Rules

- Session state is an entity.
- Login/logout are features because they are user actions.
- Login page is a page because it is a route/screen.
- Protected route composition is app-level if reused globally.
- Transport-only HTTP helpers are shared.
- Session-aware barrier is not shared.

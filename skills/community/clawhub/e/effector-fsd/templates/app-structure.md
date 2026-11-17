# App structure template

Use for FSD App layer in Effector projects.

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
    redirects.ts
    routes-view.tsx
  model/
    app.model.ts
  styles/
    globals.css
```

Next.js variant:

```txt
app/                         # Next framework App Router
  users/[userId]/page.tsx
src/
  _app/                      # FSD App layer
    providers/
    routes/
    model/
  _pages/
  widgets/
  features/
  entities/
  shared/
```

Rules:

- `app` composes lower layers; it does not implement feature internals.
- Startup is explicit: `appStarted`/`appStopped` in `app/model`.
- Router/history/storage/i18n setup is triggered from app startup events.

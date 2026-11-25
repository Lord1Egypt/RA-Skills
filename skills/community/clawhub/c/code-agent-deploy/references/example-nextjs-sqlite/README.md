# Example: Next.js + SQLite (passed acceptance on the platform)

A minimal project written to the ready-to-deploy checklist. Compare against it when making another project ready:

| File | What to note |
|---|---|
| `Dockerfile` | Multi-stage; the build and the runtime stage both use the platform's `node-base`; `.npmrc` is copied before `npm ci`; `ARG NEXT_PUBLIC_APP_URL` is declared; the runtime stage has `USER 10001` and `CMD ["node", "server.js"]` |
| `.npmrc` | npmmirror, and the binary mirror for better-sqlite3 |
| `.dockerignore` | Excludes node_modules, .next, .env* and the local data directory |
| `next.config.mjs` | `output: 'standalone'` |
| `src/lib/db.ts` | The database path is read from `DATABASE_URL`; locally it defaults to `./data/app.db` |
| `src/app/api/health/route.ts` | The health check: a read-only database check, no business logic |
| `deploy.manifest.json` | sqlite storage, `.next/cache` as ephemeral storage, `SESSION_SECRET` created by the platform, `NEXT_PUBLIC_APP_URL` taken from the application's address |

Notes:
- better-sqlite3 is pinned to 12.x (12.11.1): npmmirror has a prebuilt binary of it for Node 24. It has none for 13.x, and the build would fail.
- `package-lock.json` is not part of this template. In a project, create it with `npm install` and commit it (`npm ci` needs it).

## `Dockerfile`, `.dockerignore` and `.npmrc`

Written out here rather than shipped as files. In the project, write each into a file with exactly that name in the project's root.

### `Dockerfile`

```dockerfile
# Build and runtime both use the platform base image node-base (the platform pins the exact version).
FROM node-base AS build
WORKDIR /app
ENV NEXT_TELEMETRY_DISABLED=1
COPY package.json package-lock.json .npmrc ./
RUN npm ci
COPY . .
ARG NEXT_PUBLIC_APP_URL
ENV NEXT_PUBLIC_APP_URL=$NEXT_PUBLIC_APP_URL
RUN npm run build

FROM node-base AS runtime
WORKDIR /app
ENV NODE_ENV=production NEXT_TELEMETRY_DISABLED=1
COPY --from=build /app/.next/standalone ./
COPY --from=build /app/.next/static ./.next/static
COPY --from=build /app/public ./public
USER 10001
CMD ["node", "server.js"]
```

### `.dockerignore`

```
node_modules
.next
.git
.appcli
.env*
!.env.example
data
*.log
```

### `.npmrc`

```ini
registry=https://registry.npmmirror.com
better_sqlite3_binary_host=https://registry.npmmirror.com/-/binary/better-sqlite3
```

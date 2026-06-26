> This is a sub-module of the `gcp-fullstack` skill. See the main [SKILL.md](../SKILL.md) for the Planning Protocol and overview.

## Part 2: Project Scaffolding

### Framework Detection

Ask the user which framework they want, or detect from an existing `package.json`. The scaffold adapts accordingly:

| Framework | Create Command | Config File |
|---|---|---|
| Next.js (App Router) | `npx create-next-app@latest <name> --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"` | `next.config.ts` |
| Nuxt 3 | `npx nuxi@latest init <name>` | `nuxt.config.ts` |
| SvelteKit | `npx sv create <name>` | `svelte.config.js` |
| Remix | `npx create-remix@latest <name>` | `remix.config.js` |
| Astro | `npx create-astro@latest <name>` | `astro.config.mjs` |

After creation:

1. `cd` into the project directory.
2. Verify `.gitignore` includes: `.env`, `.env.local`, `.env*.local`, `node_modules/`, build output directories. Add missing entries before any commit.
3. Initialize git: `git init && git add -A && git commit -m "chore: initial scaffold"`.

### Common Dependencies (install as needed based on services selected)

```bash
# Firebase Auth
npm install firebase firebase-admin

# Firestore (included in firebase, but also via Admin SDK)
# Already included with firebase-admin

# Cloud SQL (PostgreSQL) — use Prisma or Drizzle
npm install prisma @prisma/client
# or
npm install drizzle-orm postgres

# General utilities
npm install zod

# Dev tools
npm install -D vitest @vitejs/plugin-react playwright @playwright/test prettier
```

### Directory Structure (base — adapt per framework)

```
src/ (or app/ depending on framework)
├── lib/
│   ├── firebase/
│   │   ├── client.ts       # Firebase client SDK init
│   │   └── admin.ts        # Firebase Admin SDK init (server-only)
│   ├── db/
│   │   ├── firestore.ts    # Firestore helpers (if using Firestore)
│   │   └── sql.ts          # Cloud SQL connection (if using Cloud SQL)
│   └── utils.ts
├── hooks/
│   └── use-auth.ts
├── types/
│   └── index.ts
└── middleware.ts            # Auth middleware (framework-specific)
```

### `.env.example` (generate based on selected services)

```bash
# GCP
GCP_PROJECT_ID=
GCP_REGION=us-central1

# Firebase Auth (if using Firebase Auth or Identity Platform)
NEXT_PUBLIC_FIREBASE_API_KEY=
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=
NEXT_PUBLIC_FIREBASE_PROJECT_ID=
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=
NEXT_PUBLIC_FIREBASE_APP_ID=

# Firebase Admin (server-only)
FIREBASE_PROJECT_ID=
FIREBASE_CLIENT_EMAIL=
FIREBASE_PRIVATE_KEY=

# Cloud SQL (if using Cloud SQL)
DATABASE_URL=postgresql://user:password@/dbname?host=/cloudsql/PROJECT:REGION:INSTANCE

# Cloudflare
CLOUDFLARE_API_TOKEN=
CLOUDFLARE_ZONE_ID=

# App
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

Only include the sections relevant to the selected services. Remove unused sections.

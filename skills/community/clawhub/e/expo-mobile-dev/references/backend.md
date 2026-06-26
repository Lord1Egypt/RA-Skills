# Backend / API Server

**Opinion: use [Hono](https://hono.dev/) for the API server.** It's Web-Standards-based (Request/Response), runs unchanged on every JS runtime that matters (Cloudflare Workers, Node.js, Deno, Bun, Vercel), has excellent TypeScript ergonomics, and a small middleware ecosystem. Switching deployment targets is mostly a one-line change to the adapter.

**Default runtime: Node.js.** Both regions ship Node by default — it's the runtime every Chinese cloud's serverless and VM products support first-class, every monitoring/APM agent supports first-class, and every team member already knows. Bun is faster and ships fewer files but adds a runtime variable that costs more than it saves at this scale; reach for it only when a specific workload (lots of small HTTP request handling on a single VM) actually benefits.

The **deployment architecture differs by region** — see Step 1 in [SKILL.md](../SKILL.md). Decide once, up front. Trying to retrofit a Cloudflare-Workers-only design to work in mainland China later is significantly more painful than choosing the right shape on day one.

| | International | 中国大陆 |
|---|---|---|
| Server framework | Hono | Hono |
| Code location | **Same repo** — inside Expo API Routes (`app/api/`) | **Separate directory** in a pnpm monorepo (e.g., `apps/api/`) |
| Runtime | Cloudflare Workers (V8 isolates) | Node.js on a Chinese cloud (Bun only if a specific need justifies it) |
| Deploy target | Cloudflare Workers via `wrangler` (Expo API Routes export adapter) | 火山引擎 VeFaaS / ECS (primary) — fallback to 阿里云 FC / ECS |
| Domain / DNS | Cloudflare DNS or any provider | Must be on a domain with ICP 备案 (see [china-deployment.md](china-deployment.md)) |
| Cold start | Sub-50ms typical | 100-500ms (VeFaaS/FC/SCF) or zero (ECS/CVM) |

---

## International: Hono inside Expo API Routes → Cloudflare Workers

### Why this shape

Expo API Routes (introduced in SDK 50, refined since) let you write server endpoints alongside your app routes. They use the same Web Request/Response API that Hono targets, so **Hono drops in with zero adaptation**. The whole stack — UI + server — ships from one repo, with shared types between client and server.

Cloudflare Workers is the deployment target because:
- It's the runtime Hono was originally designed for; performance is excellent
- Global edge network: low latency for users worldwide
- Generous free tier; serverless billing scales to zero
- Cloudflare D1 / R2 / KV / Durable Objects are right there if you want them later

### File layout

```
my-app/
├── app/
│   ├── (tabs)/
│   ├── api/
│   │   └── [...all]+api.ts     # ← catch-all Hono handler
│   └── _layout.tsx
├── server/                     # optional: server-only code outside app/api/
│   ├── routes/
│   ├── db/
│   └── auth.ts
├── shared/                     # types shared between client and server
└── app.config.ts
```

`+api.ts` is Expo's file extension for API route handlers. The `[...all]` catch-all sends every `/api/*` request through the single Hono app, so you only register one Expo route and let Hono handle internal routing.

### Skeleton

```ts
// app/api/[...all]+api.ts
import { Hono } from "hono";
import { cors } from "hono/cors";

const app = new Hono().basePath("/api");

app.use("*", cors({
  origin: ["http://localhost:8081", "https://myapp.com"],
  credentials: true,
}));

app.get("/health", (c) => c.json({ ok: true }));

// Mount feature routes
import authRoutes from "../../server/routes/auth";
import postsRoutes from "../../server/routes/posts";
app.route("/auth", authRoutes);
app.route("/posts", postsRoutes);

export const GET = (req: Request) => app.fetch(req);
export const POST = (req: Request) => app.fetch(req);
export const PUT = (req: Request) => app.fetch(req);
export const PATCH = (req: Request) => app.fetch(req);
export const DELETE = (req: Request) => app.fetch(req);
export const OPTIONS = (req: Request) => app.fetch(req);
```

### Type-safe client

Hono's `hc` client gives you typed RPC calls from the React Native app:

```ts
// app/api/[...all]+api.ts
const app = new Hono().basePath("/api")
  .get("/posts/:id", (c) => c.json({ id: c.req.param("id"), title: "Hello" }));

export type AppType = typeof app;
```

```ts
// lib/api.ts (client)
import { hc } from "hono/client";
import type { AppType } from "../app/api/[...all]+api";

export const api = hc<AppType>(process.env.EXPO_PUBLIC_API_URL!);

// Usage:
const res = await api.api.posts[":id"].$get({ param: { id: "42" } });
const data = await res.json();  // fully typed
```

This eliminates whole categories of API drift bugs.

### Deploying to Cloudflare Workers

Expo's server export adapter handles the build. The exact command set is evolving — **always check the current [Expo API Routes deployment docs](https://docs.expo.dev/router/reference/api-routes/) and the [Hono Cloudflare Workers guide](https://hono.dev/getting-started/cloudflare-workers) before deploying**.

High-level workflow (verify each step against current docs):

```bash
# 1. Install wrangler
pnpm add -D wrangler

# 2. Export the server build for Cloudflare
npx expo export --platform web --server-output cloudflare

# 3. Configure wrangler.toml
# (account_id, compatibility_date, env bindings, etc.)

# 4. Deploy
pnpm wrangler deploy
```

Secrets (auth client_secrets, database URLs) go through `wrangler secret put`, not in `wrangler.toml`.

### Database choice (not opinionated by this skill)

Common Cloudflare-Workers-compatible options:
- **Cloudflare D1** — SQLite at the edge, native integration
- **Neon / Supabase Postgres** — via HTTP driver (`@neondatabase/serverless`)
- **PlanetScale / Turso** — also HTTP-compatible

Avoid drivers that require long-lived TCP connections (raw `pg`, `mysql2`) on Workers — they don't work. Use HTTP-based or edge-native drivers.

---

## 中国大陆: separate `apps/api/` Hono server → 火山引擎 / 阿里云

### Why this shape

Cloudflare Workers is **not a viable production target for mainland China**:
- Cloudflare's global network has degraded performance and intermittent blocking in mainland
- ICP 备案 requirements tie your production domain to a Chinese cloud
- Latency from mainland users to CF edge nodes (often Hong Kong / Singapore) is significantly worse than to a domestic data center

So the China stack splits the repo: the Expo app stays in its directory, and the server lives in its own directory deployed to a domestic cloud. Use **pnpm workspaces** to share code (types, validation schemas) between them.

### File layout (pnpm monorepo)

```
my-app/                           # repo root
├── pnpm-workspace.yaml
├── package.json                  # root, with workspaces
├── apps/
│   ├── mobile/                   # the Expo project — was the whole repo before
│   │   ├── app/
│   │   ├── app.config.ts
│   │   └── package.json
│   └── api/                      # NEW — Hono server
│       ├── src/
│       │   ├── index.ts          # entry point (Node.js)
│       │   ├── routes/
│       │   ├── db/
│       │   └── auth.ts
│       ├── package.json
│       └── tsconfig.json
└── packages/
    └── shared/                   # types + validation schemas shared by both
        ├── src/
        └── package.json
```

`pnpm-workspace.yaml`:

```yaml
packages:
  - "apps/*"
  - "packages/*"
```

### Skeleton (Node.js runtime, default)

```ts
// apps/api/src/index.ts
import { serve } from "@hono/node-server";
import { Hono } from "hono";
import { cors } from "hono/cors";

const app = new Hono().basePath("/api");

app.use("*", cors({
  origin: ["myapp://"],  // app deep-link scheme + production domain
  credentials: true,
}));

app.get("/health", (c) => c.json({ ok: true }));

// Feature routes
import authRoutes from "./routes/auth";
app.route("/auth", authRoutes);

const port = Number(process.env.PORT) || 3000;
serve({ fetch: app.fetch, port }, (info) => {
  console.log(`API listening on http://localhost:${info.port}`);
});
```

Install requirements:

```bash
pnpm add hono @hono/node-server
```

Node 20+ is the supported floor (matches the root `package.json` engines field). Use `tsx` for dev (`pnpm tsx watch src/index.ts`) and compile with `tsc` for production, or run directly with Node 24+'s native TypeScript stripping.

If you have a specific reason to use Bun on a particular VM workload, the skeleton simplifies to `export default { port, fetch: app.fetch }` — but that's a niche choice, not the default. Pair it with the Node skeleton above for cross-runtime portability if you ever change your mind.

### Cloud provider preference order

Tenshow's standing recommendation, in priority order:

1. **火山引擎 (Volcano Engine, ByteDance)** — **primary choice.** Strong perf, competitive pricing, the team has good experience with their docs and support, and 火山引擎 has been the fastest-improving Chinese cloud over the last 18 months. Pairs especially well if your app integrates with TikTok / Douyin / 抖音 ecosystem APIs.
2. **阿里云 (Alibaba Cloud)** — **fallback / secondary.** The most mature ecosystem, biggest service catalog. Use when 火山引擎 lacks a specific service or when you need the broadest ICP 备案 / domain registration bundle.

Other Chinese clouds (腾讯云, 华为云) are out of scope — we don't deploy to them. If a team-specific situation later changes that, this section is the place to revisit.

### Deploy targets (pick one based on workload shape)

**For most teams: serverless functions (scales to zero, per-invocation billing)**
- **火山引擎 函数服务 (VeFaaS)** — primary
- 阿里云 Function Compute (FC) — fallback
- ICP 备案 bundled if you use the same cloud's domain registrar
- Cold starts: 100-500ms (worse than CF Workers, but acceptable for most apps)
- Each cloud has its own deploy CLI (the volcengine CLI / `vefaas`-CLI for 火山引擎, `serverless-devs` for 阿里云) — confirm against current docs.

**For latency-sensitive or socket-heavy workloads: traditional VMs**
- 火山引擎 ECS — primary
- 阿里云 ECS — fallback
- No cold starts. More ops burden — you manage the server, SSL renewal, restarts.
- Pair with a load balancer + CDN from the same provider.

**For container-native teams: managed Kubernetes**
- 火山引擎 VKE (容器服务) — primary
- 阿里云 ACK — fallback
- Only worth it if you're already running Kubernetes elsewhere.

### Deploy command (illustrative — confirm with current cloud docs)

```bash
# 火山引擎 VeFaaS via vefaas-CLI (verify exact CLI name in current docs)
# Setup: install the CLI, log in with your AK/SK, then:
vefaas deploy

# Or 阿里云 FC fallback:
pnpm add -D @serverless-devs/s
s deploy
```

**Always cross-check against the provider's current docs** — Chinese clouds rename / restructure their CLIs every 12-18 months, sometimes faster.

### Connecting the Expo app to the API

`apps/mobile/app.config.ts`:

```ts
extra: {
  apiUrl: process.env.APP_REGION === "cn"
    ? "https://api.example.cn"        // China backend, with ICP 备案
    : "https://api.example.com",      // International backend (CF Workers)
},
```

Read it from the app via `expo-constants`:

```ts
import Constants from "expo-constants";
const apiUrl = Constants.expoConfig?.extra?.apiUrl as string;
```

### Database choice (not opinionated by this skill)

Common Chinese-cloud-friendly options, in priority order matching the cloud preference above:

- **火山引擎 veDB** (PostgreSQL / MySQL compatible) — managed, low-latency from VeFaaS/ECS
- **阿里云 RDS** / **PolarDB** (cloud-native PG-compatible) — managed, very mature
- **Self-hosted Postgres on ECS** — cheapest, most ops work

Connection pooling matters more here than internationally — if using VeFaaS/FC, each invocation gets a fresh container, so use a pooler (PgBouncer or the cloud's built-in pool service).

---

## Shared concerns (both regions)

### Auth integration

The auth server pattern in [auth.md](auth.md) maps cleanly onto Hono. Better-auth ships a Hono adapter — mount it as middleware:

```ts
// server/auth.ts (international) or apps/api/src/auth.ts (China)
import { Hono } from "hono";
import { auth } from "./auth-config";  // your betterAuth() instance

const authRoutes = new Hono();
authRoutes.all("/*", (c) => auth.handler(c.req.raw));

export default authRoutes;
```

Check [better-auth's current Hono integration docs](https://www.better-auth.com/docs) — the adapter API has changed between minor versions.

### Validation

Use `zod` (already installed for forms) for request validation. Hono has `@hono/zod-validator`:

```bash
pnpm add @hono/zod-validator
```

```ts
import { zValidator } from "@hono/zod-validator";
import { z } from "zod";

app.post(
  "/posts",
  zValidator("json", z.object({ title: z.string().min(1) })),
  (c) => {
    const { title } = c.req.valid("json");
    return c.json({ id: 1, title });
  },
);
```

Sharing the same zod schemas across client (form validation) and server (request validation) is the whole point of the monorepo's `packages/shared/`.

### Logging / observability

- **International (CF Workers)**: Workers Logs (free, built-in), then Logflare / Axiom / Datadog for retention
- **中国大陆**: 火山引擎 TLS (Tracing Log Service) primary; 阿里云 SLS (日志服务) as fallback — both have generous free tiers

Don't `console.log` in production code without thinking about retention; both regions' logging products want structured JSON.

### Rate limiting

- **CF Workers**: built-in via Cloudflare's WAF rate limiting (point-and-click in the dashboard) or Hono's `hono-rate-limiter` middleware
- **中国大陆**: 火山引擎 API 网关 (primary) or 阿里云 API 网关 (fallback) in front of VeFaaS/FC/ECS, or `hono-rate-limiter` in-process with a Redis backend (火山引擎 Redis / 阿里云 Tair)

---

## Quick decision checklist

When starting backend work, walk through this:

- [ ] Region confirmed from Step 1 of [SKILL.md](../SKILL.md)?
- [ ] International → API routes inside the Expo app, Cloudflare Workers as target?
- [ ] China → pnpm monorepo with `apps/api/` and `apps/mobile/`?
- [ ] Domain on the right side of the GFW with ICP 备案 if China?
- [ ] Hono installed and a `/health` route returning 200?
- [ ] Client → server URL configured via `app.config.ts` + `expo-constants`?
- [ ] Auth handler mounted (after reading current better-auth Hono docs)?
- [ ] Secrets in EAS Secrets / cloud secret manager — not in source?

---

## Reference URLs

Keep these handy — backend tooling is the part of the stack that changes fastest:

- **Hono** — https://hono.dev/
- **Expo API Routes** — https://docs.expo.dev/router/reference/api-routes/
- **Cloudflare Workers + Hono** — https://hono.dev/getting-started/cloudflare-workers
- **wrangler CLI** — https://developers.cloudflare.com/workers/wrangler/
- **better-auth + Hono** — https://www.better-auth.com/docs (search "Hono")
- **火山引擎 (Volcano Engine) console** — https://console.volcengine.com/
- **火山引擎 VeFaaS docs** — https://www.volcengine.com/docs/6662
- **阿里云 Function Compute** — https://help.aliyun.com/product/50980.html
- **Serverless Devs (阿里云)** — https://www.serverless-devs.com/
- **pnpm workspaces** — https://pnpm.io/workspaces

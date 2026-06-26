# Rendering Modes & SSR Caching

## Table of Contents
1. [SSG (Static Site Generation)](#ssg)
2. [SSR (Server-Side Rendering)](#ssr)
3. [Hybrid mode](#hybrid)
4. [SSR caching strategies](#caching)
5. [Middleware](#middleware)
6. [API routes / endpoints](#endpoints)
7. [Decision matrix](#decision-matrix)

---

## SSG (Static Site Generation) — the default

Every `.astro` page is pre-rendered at build time into static HTML. No server needed at runtime.

```js
// astro.config.mjs
export default defineConfig({
  output: 'static', // This is the default; you can omit it
});
```

**When to use SSG**:
- Blog, docs, marketing sites, portfolios
- Content that changes at deploy time, not per-request
- Maximum performance (every page is a cached HTML file)

**Limitations**:
- No per-request data (user sessions, search results, real-time content)
- Dynamic routes must define all paths at build time via `getStaticPaths()`
- Large sites with thousands of pages = long build times

---

## SSR (Server-Side Rendering)

Pages are rendered on-demand per request. Requires an adapter.

```js
// astro.config.mjs
import node from '@astrojs/node';

export default defineConfig({
  output: 'server',
  adapter: node({ mode: 'standalone' }),
});
```

**When to use SSR**:
- User-specific content (dashboards, account pages)
- Real-time or frequently changing data
- Auth-gated pages
- Search results, filtered listings
- Content from a CMS that updates without redeploying

**Key behavior differences from SSG**:
- `Astro.request` contains the actual request (headers, cookies, URL)
- `Astro.cookies` is available for reading/writing cookies
- `Astro.redirect()` works for server-side redirects
- No `getStaticPaths()` — params come from the live URL

```astro
---
// SSR page: reads cookies, fetches user-specific data
const token = Astro.cookies.get('auth_token')?.value;
if (!token) return Astro.redirect('/login');

const user = await fetchUser(token);
---
<h1>Welcome, {user.name}</h1>
```

---

## Hybrid mode

The practical sweet spot for most real projects. Static by default, SSR where needed.

```js
// astro.config.mjs — Astro 4+ approach
export default defineConfig({
  output: 'static',  // Default: pages are static
  adapter: node({ mode: 'standalone' }), // Needed for the SSR pages
});
```

Then opt individual pages OUT of prerendering:

```astro
---
// src/pages/dashboard.astro — this page renders on every request
export const prerender = false;
---
```

Or if you set `output: 'server'` (SSR default), opt individual pages IN to prerendering:

```astro
---
// src/pages/about.astro — this page is pre-rendered at build time
export const prerender = true;
---
```

**Hybrid is the right choice when**:
- Most pages are static (marketing, blog, docs)
- A few pages need dynamic data (login, dashboard, search)
- You want fast static pages without giving up server capabilities

---

## SSR Caching Strategies

SSR without caching is just a slow website. Every SSR page should have a caching plan.

### Level 1: HTTP Cache-Control headers

The simplest and most effective approach. Set headers and let the CDN/browser handle it.

```astro
---
// In an .astro page
Astro.response.headers.set(
  'Cache-Control',
  'public, s-maxage=60, stale-while-revalidate=300'
);

const data = await fetchExpensiveData();
---
<h1>{data.title}</h1>
```

**Header cheat sheet**:

| Header | Meaning |
|--------|---------|
| `public, max-age=3600` | Browser + CDN cache for 1 hour |
| `public, s-maxage=60` | CDN caches 60s, browser doesn't |
| `public, s-maxage=60, stale-while-revalidate=300` | CDN serves stale for 5min while refreshing |
| `private, max-age=0` | No caching (user-specific data) |
| `no-store` | Never cache anywhere |

### Level 2: Middleware-based caching

Use Astro middleware to apply caching logic globally or per-route:

```ts
// src/middleware.ts
import { defineMiddleware } from 'astro:middleware';

export const onRequest = defineMiddleware(async ({ url, request }, next) => {
  const response = await next();

  // Cache static-ish pages for 5 minutes at the CDN
  if (url.pathname.startsWith('/blog/')) {
    response.headers.set(
      'Cache-Control',
      'public, s-maxage=300, stale-while-revalidate=600'
    );
  }

  // Never cache user-specific pages
  if (url.pathname.startsWith('/dashboard')) {
    response.headers.set('Cache-Control', 'private, no-store');
  }

  return response;
});
```

### Level 3: In-memory / external cache for expensive operations

For data that's expensive to fetch but doesn't change often:

```ts
// src/lib/cache.ts
const cache = new Map<string, { data: any; expires: number }>();

export async function cachedFetch<T>(
  key: string,
  fetcher: () => Promise<T>,
  ttlSeconds = 60
): Promise<T> {
  const cached = cache.get(key);
  if (cached && cached.expires > Date.now()) {
    return cached.data as T;
  }

  const data = await fetcher();
  cache.set(key, {
    data,
    expires: Date.now() + ttlSeconds * 1000,
  });
  return data;
}
```

Usage in a page:
```astro
---
import { cachedFetch } from '../lib/cache';

const posts = await cachedFetch('recent-posts', async () => {
  return await cms.getPosts({ limit: 10 });
}, 120); // Cache for 2 minutes
---
```

### Level 4: Edge caching (CDN-specific)

When deploying to Vercel, Cloudflare, or Netlify, use their edge caching:

**Vercel**: Uses `s-maxage` headers automatically. Add `stale-while-revalidate` for instant responses.

**Cloudflare**: Use Cache API in Workers for fine-grained control:
```ts
// Works in Cloudflare adapter context
const cache = caches.default;
const cached = await cache.match(request);
if (cached) return cached;
```

### Cache invalidation strategies

- **Time-based** (TTL): Set `max-age` or `s-maxage`. Simple, predictable.
- **On-demand**: Purge CDN cache via API when content changes (webhook from CMS).
- **Stale-while-revalidate**: Serve stale content immediately, refresh in background. Best UX.
- **Cache busting**: Append version/hash to URLs for assets.

---

## Middleware

Middleware runs before every request in SSR mode. Use it for auth, logging, caching headers, redirects.

```ts
// src/middleware.ts
import { defineMiddleware, sequence } from 'astro:middleware';

const auth = defineMiddleware(async ({ cookies, url, redirect }, next) => {
  const token = cookies.get('session')?.value;

  if (url.pathname.startsWith('/admin') && !token) {
    return redirect('/login');
  }

  return next();
});

const timing = defineMiddleware(async (context, next) => {
  const start = performance.now();
  const response = await next();
  const duration = performance.now() - start;
  response.headers.set('X-Response-Time', `${duration.toFixed(0)}ms`);
  return response;
});

// Chain multiple middleware
export const onRequest = sequence(auth, timing);
```

---

## API Routes / Endpoints

Files in `src/pages/api/` that export HTTP method handlers:

```ts
// src/pages/api/search.ts
import type { APIRoute } from 'astro';

export const GET: APIRoute = async ({ url }) => {
  const query = url.searchParams.get('q');
  const results = await search(query);

  return new Response(JSON.stringify(results), {
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'public, s-maxage=30',
    },
  });
};

export const POST: APIRoute = async ({ request }) => {
  const body = await request.json();
  // Process the submission
  return new Response(JSON.stringify({ ok: true }), {
    status: 200,
  });
};
```

---

## Decision Matrix

| Scenario | Mode | Caching |
|----------|------|---------|
| Blog / docs | SSG | N/A (static files) |
| Marketing site with contact form | Hybrid (form endpoint is SSR) | Static pages cached by CDN |
| E-commerce product pages | Hybrid or SSR | `s-maxage=300, stale-while-revalidate` |
| User dashboard | SSR | `private, no-store` |
| API-driven listing with filters | SSR | `s-maxage=60` + in-memory cache |
| CMS preview mode | SSR | `no-store` for preview, cached for published |

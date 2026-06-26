# Deployment & Adapters

## Table of Contents
1. [Deployment decision tree](#decision-tree)
2. [Static deployment](#static)
3. [SSR deployment](#ssr)
4. [Environment variables](#env)
5. [Base path / subpath hosting](#base-path)
6. [Auth & protected pages](#auth)
7. [Common deployment failures](#failures)

---

## Deployment decision tree

```
Is every page static (SSG)?
├── Yes → Deploy to ANY static host
│   ├── Netlify, Vercel, Cloudflare Pages
│   ├── GitHub Pages, AWS S3 + CloudFront
│   └── Any web server (nginx, Apache)
│
└── No (SSR or Hybrid) → Need a server runtime
    ├── Vercel → @astrojs/vercel
    ├── Netlify → @astrojs/netlify
    ├── Cloudflare → @astrojs/cloudflare
    ├── AWS Lambda → @astrojs/node + serverless wrapper
    └── Self-hosted → @astrojs/node (standalone)
```

---

## Static deployment

Build produces a `dist/` folder of HTML, CSS, JS, and assets. Upload it anywhere.

```bash
npm run build
# Output: ./dist/
```

### Netlify
```toml
# netlify.toml
[build]
  command = "npm run build"
  publish = "dist"
```

### Vercel (static)
No adapter needed. Vercel auto-detects Astro:
```json
// vercel.json (optional, for customization)
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist"
}
```

### GitHub Pages
```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pages: write
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: dist
      - uses: actions/deploy-pages@v4
```

For GitHub Pages, set the base path:
```js
// astro.config.mjs
export default defineConfig({
  site: 'https://username.github.io',
  base: '/repo-name/',
});
```

### Cloudflare Pages (static)
Connect your Git repo in the Cloudflare dashboard. Build command: `npm run build`, output: `dist`.

---

## SSR deployment

### Vercel (serverless)
```bash
npx astro add vercel
```

```js
// astro.config.mjs
import vercel from '@astrojs/vercel';

export default defineConfig({
  output: 'server',
  adapter: vercel({
    // Options
    imageService: true,     // Use Vercel's image optimization
    isr: {
      expiration: 60,       // ISR: revalidate every 60 seconds
    },
  }),
});
```

### Netlify (serverless)
```bash
npx astro add netlify
```

```js
import netlify from '@astrojs/netlify';

export default defineConfig({
  output: 'server',
  adapter: netlify(),
});
```

### Cloudflare Workers
```bash
npx astro add cloudflare
```

```js
import cloudflare from '@astrojs/cloudflare';

export default defineConfig({
  output: 'server',
  adapter: cloudflare({
    mode: 'directory', // or 'advanced'
  }),
});
```

### Node.js (self-hosted)
```bash
npx astro add node
```

```js
import node from '@astrojs/node';

export default defineConfig({
  output: 'server',
  adapter: node({
    mode: 'standalone', // Runs its own HTTP server
    // mode: 'middleware' // Exports handler for Express/Fastify
  }),
});
```

Running in production:
```bash
npm run build
node ./dist/server/entry.mjs
# Server starts on port 4321
```

With a process manager:
```bash
# PM2
pm2 start ./dist/server/entry.mjs --name my-astro-app

# Or with environment variables
HOST=0.0.0.0 PORT=3000 node ./dist/server/entry.mjs
```

### Docker
```dockerfile
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runtime
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/package.json ./

ENV HOST=0.0.0.0
ENV PORT=4321
EXPOSE 4321

CMD ["node", "./dist/server/entry.mjs"]
```

---

## Environment variables

### Defining variables
```bash
# .env (development)
PUBLIC_API_URL=https://api.dev.example.com
SECRET_API_KEY=sk-dev-12345

# .env.production (production build)
PUBLIC_API_URL=https://api.example.com
SECRET_API_KEY=sk-prod-67890
```

### Accessing variables

**Server-side (frontmatter, endpoints, middleware)**:
```ts
// Access ALL variables (public and secret)
const apiKey = import.meta.env.SECRET_API_KEY;
const apiUrl = import.meta.env.PUBLIC_API_URL;
```

**Client-side (islands, browser JS)**:
```ts
// Only PUBLIC_ prefixed variables are available
const apiUrl = import.meta.env.PUBLIC_API_URL;
// import.meta.env.SECRET_API_KEY → undefined (intentionally hidden)
```

### Platform-specific env setup

**Vercel**: Set in project Settings → Environment Variables
**Netlify**: Set in Site Settings → Environment Variables
**Cloudflare**: Set in Workers & Pages → Settings → Variables
**Node**: Pass via shell or `.env` file

The `PUBLIC_` prefix convention is enforced by Astro. Never put secrets in `PUBLIC_` variables.

---

## Base path / subpath hosting

When hosting at a subpath like `https://example.com/docs/`:

```js
// astro.config.mjs
export default defineConfig({
  base: '/docs/',
  site: 'https://example.com',
});
```

### What `base` affects
- All generated links are prefixed with `/docs/`
- `Astro.url` includes the base
- Static assets are served from `/docs/`
- The dev server mounts at `localhost:4321/docs/`

### What breaks without `base`
- Links point to `/` instead of `/docs/` → 404
- CSS/JS assets 404 because paths are wrong
- Images in `/public/` load from the wrong path

### Using base-aware paths
```astro
---
// Always use Astro's URL utilities for base-aware paths
const homeURL = new URL('/', Astro.url);
---

<!-- DON'T hardcode paths -->
<a href="/">Home</a>  <!-- Wrong if base is /docs/ -->

<!-- DO use Astro's base-aware utilities -->
<a href={`${import.meta.env.BASE_URL}`}>Home</a>
```

### Reverse proxy setup (nginx)
```nginx
location /docs/ {
    proxy_pass http://localhost:4321/docs/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

---

## Auth & protected pages

### Middleware-based auth (SSR only)
```ts
// src/middleware.ts
import { defineMiddleware } from 'astro:middleware';

const protectedRoutes = ['/dashboard', '/admin', '/settings'];

export const onRequest = defineMiddleware(async ({ url, cookies, redirect }, next) => {
  const isProtected = protectedRoutes.some(r => url.pathname.startsWith(r));

  if (isProtected) {
    const session = cookies.get('session')?.value;

    if (!session) {
      return redirect(`/login?redirect=${encodeURIComponent(url.pathname)}`);
    }

    // Validate session (check DB, verify JWT, etc.)
    const user = await validateSession(session);
    if (!user) {
      cookies.delete('session');
      return redirect('/login');
    }

    // Make user available to the page
    Astro.locals.user = user;
  }

  return next();
});
```

### Auth API endpoints
```ts
// src/pages/api/auth/login.ts
import type { APIRoute } from 'astro';

export const POST: APIRoute = async ({ request, cookies, redirect }) => {
  const formData = await request.formData();
  const email = formData.get('email') as string;
  const password = formData.get('password') as string;

  const user = await authenticateUser(email, password);

  if (!user) {
    return new Response('Invalid credentials', { status: 401 });
  }

  const session = await createSession(user.id);
  cookies.set('session', session.id, {
    httpOnly: true,
    secure: true,
    sameSite: 'lax',
    path: '/',
    maxAge: 60 * 60 * 24 * 7, // 1 week
  });

  return redirect('/dashboard');
};
```

### Auth in static mode (DON'T)

You cannot do server-side auth in static mode. The HTML is pre-built. Options:
1. Switch protected pages to SSR (hybrid mode)
2. Use client-side auth (check token in island, redirect via JS) — but the HTML is still in the build output
3. Use an external auth gateway (Cloudflare Access, Netlify Identity)

---

## Common deployment failures

### "Cannot find adapter"
```
[ERROR] Cannot use `output: 'server'` without an adapter.
```
Fix: Install the correct adapter: `npx astro add vercel` (or node, netlify, etc.)

### Environment variables undefined in production
- Check the variable is set on the hosting platform
- For client-side access, variable must start with `PUBLIC_`
- For SSR, make sure the runtime environment has the variable (not just build time)

### SSR pages return 404 on static host
You deployed an SSR app to a static host (GitHub Pages, S3). Either:
- Switch those pages to `export const prerender = true`
- Or deploy to a host that supports SSR (Vercel, Netlify, Cloudflare Workers, Node)

### Broken assets after deploy
- Check `base` in config matches the deployment path
- Verify `trailingSlash` setting matches the host's behavior
- Clear CDN cache after deploy

### Build succeeds locally but fails on host
- Node version mismatch (Astro needs 18+)
- Missing environment variables
- Different package manager lock file
- Case-sensitivity in file names (macOS is case-insensitive, Linux isn't)

### "window is not defined" during build
A component uses browser APIs during SSR. Fix:
- Wrap in `client:only="framework"` directive
- Move browser code to `onMounted` / `useEffect`
- Guard with `if (typeof window !== 'undefined')`

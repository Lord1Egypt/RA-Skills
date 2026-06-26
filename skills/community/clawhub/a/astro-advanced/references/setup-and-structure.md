# Setup & Project Structure

## Table of Contents
1. [Creating a project](#creating-a-project)
2. [File structure explained](#file-structure)
3. [astro.config.mjs](#config)
4. [Adapters](#adapters)
5. [TypeScript setup](#typescript)
6. [Common setup mistakes](#common-mistakes)

---

## Creating a project

```bash
# Interactive setup
npm create astro@latest

# With a specific template
npm create astro@latest -- --template blog
npm create astro@latest -- --template docs
npm create astro@latest -- --template minimal

# With a community template
npm create astro@latest -- --template github-user/repo
```

After creation:
```bash
cd my-project
npm install
npm run dev     # Dev server on localhost:4321
npm run build   # Production build to ./dist
npm run preview # Preview production build locally
```

---

## File structure

```
my-project/
├── public/              # Static assets (served as-is, no processing)
│   ├── favicon.svg
│   ├── robots.txt
│   └── og-image.png
├── src/
│   ├── pages/           # File-based routing (REQUIRED for routes)
│   │   ├── index.astro          # → /
│   │   ├── about.astro          # → /about
│   │   ├── blog/
│   │   │   ├── index.astro      # → /blog
│   │   │   └── [slug].astro     # → /blog/:slug (dynamic)
│   │   └── api/
│   │       └── search.ts        # → /api/search (API endpoint)
│   ├── components/      # Reusable UI (Astro, Vue, React, etc.)
│   ├── layouts/         # Page shells with <slot />
│   ├── content/         # Content collections (markdown, MDX, JSON)
│   │   └── config.ts    # Collection schemas
│   ├── styles/          # Global styles
│   ├── lib/             # Utility functions, API clients
│   └── middleware.ts    # Request middleware (SSR only)
├── astro.config.mjs     # Astro configuration
├── tsconfig.json        # TypeScript config
└── package.json
```

### Key distinctions that trip people up

**`/public` vs `src/assets/`**:
- `/public` → Copied verbatim to build output. Use for files that need a stable URL (favicons, robots.txt, downloadable PDFs).
- `src/assets/` → Processed by Astro's build pipeline. Use for images (gets optimized), CSS (gets bundled), etc.

**`/src/pages` vs `/src/components`**:
- Pages create routes. Every `.astro`, `.md`, or `.mdx` file in `/src/pages` becomes a URL.
- Components don't create routes. They're imported and used inside pages or other components.
- A component in `/src/pages` IS a route whether you intended it or not.

**Dynamic routes**:
```
src/pages/blog/[slug].astro     → /blog/my-post
src/pages/[...path].astro       → catch-all (404 page, etc.)
src/pages/[lang]/[...slug].astro → /en/about, /es/about
```

For SSG, dynamic routes need `getStaticPaths()`:
```astro
---
export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map(post => ({
    params: { slug: post.slug },
    props: { post }
  }));
}
const { post } = Astro.props;
---
```

For SSR, dynamic routes read params at runtime:
```astro
---
const { slug } = Astro.params;
const post = await getEntry('blog', slug);
if (!post) return Astro.redirect('/404');
---
```

---

## astro.config.mjs

Minimal config:
```js
import { defineConfig } from 'astro/config';

export default defineConfig({});
```

Common production config:
```js
import { defineConfig } from 'astro/config';
import vue from '@astrojs/vue';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';
import node from '@astrojs/node';

export default defineConfig({
  site: 'https://example.com',        // Required for sitemap, canonical URLs
  base: '/',                           // Set if hosting at a subpath: '/docs/'
  output: 'static',                    // 'static' | 'server'
  adapter: node({ mode: 'standalone' }), // Only for SSR/hybrid
  integrations: [
    vue(),
    tailwind(),
    sitemap(),
  ],
  vite: {
    // Vite config overrides if needed
  },
  trailingSlash: 'always',            // 'always' | 'never' | 'ignore'
});
```

### Config options that matter most

| Option | What it does | When you need it |
|--------|-------------|-----------------|
| `site` | Sets the canonical base URL | Always in production (sitemap, OG tags) |
| `base` | Subpath prefix for all routes | Hosting at `/docs/` or behind a reverse proxy |
| `output` | Rendering mode | `'server'` for SSR, `'static'` for SSG (default) |
| `adapter` | Server runtime | Required when `output` is `'server'` |
| `trailingSlash` | URL format | Match your host's behavior to avoid redirects |

---

## Adapters

Adapters tell Astro how to run your server code. Only needed for SSR or hybrid.

### Node.js (self-hosted)
```bash
npx astro add node
```
```js
// astro.config.mjs
import node from '@astrojs/node';
export default defineConfig({
  output: 'server',
  adapter: node({ mode: 'standalone' }), // or 'middleware'
});
```
- `standalone` → Runs its own HTTP server (port 4321 by default)
- `middleware` → Exports an Express/Fastify-compatible handler

### Vercel
```bash
npx astro add vercel
```
```js
import vercel from '@astrojs/vercel';
export default defineConfig({
  output: 'server',
  adapter: vercel(),
});
```

### Netlify
```bash
npx astro add netlify
```

### Cloudflare Pages
```bash
npx astro add cloudflare
```

---

## TypeScript setup

Astro supports TypeScript out of the box. The frontmatter section of `.astro` files is TypeScript by default.

```json
// tsconfig.json (Astro's recommended)
{
  "extends": "astro/tsconfigs/strict"  // or "base" for looser checks
}
```

Type-safe props:
```astro
---
interface Props {
  title: string;
  description?: string;
  tags: string[];
}
const { title, description = 'Default', tags } = Astro.props;
---
```

---

## Common setup mistakes

**Installing integrations manually instead of using `npx astro add`**:
The `astro add` command updates both `package.json` AND `astro.config.mjs`. Manual npm install only does half the job.

**Putting components in `/src/pages` accidentally**:
Everything in pages becomes a route. If you have `src/pages/Button.astro`, it creates a `/Button` page.

**Forgetting `site` in config**:
Without it, `Astro.site` returns undefined, sitemap generation fails, and canonical URLs break.

**Wrong Node.js version**:
Astro requires Node 18+. Check with `node --version`.

**Mixing package managers**:
Pick one (npm, pnpm, yarn) and stick with it. Delete lock files from other managers.

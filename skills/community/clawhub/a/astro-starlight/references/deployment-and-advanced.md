# Deployment & Advanced Topics

## Table of Contents
1. [Deployment basics](#deployment)
2. [Subpath hosting (the #1 headache)](#subpath)
3. [Search configuration](#search)
4. [Internationalization (i18n)](#i18n)
5. [Versioned documentation](#versioning)
6. [Authentication / private docs](#auth)
7. [SSR (server-side rendering)](#ssr)
8. [Plugins](#plugins)

---

## 1. Deployment basics {#deployment}

Starlight produces static HTML by default. Build with:

```bash
npm run build     # Outputs to dist/
npm run preview   # Local preview of built site
```

### Platform-specific guides

**Vercel:**
```bash
npx astro add vercel
```
Then push to GitHub and connect to Vercel. Works with zero config for root-path deployments.

**Netlify:**
```bash
npx astro add netlify
```
Or create `netlify.toml`:
```toml
[build]
  command = "npm run build"
  publish = "dist"
```

**Cloudflare Pages:**
```bash
npx astro add cloudflare
```
Set build command to `npm run build` and output directory to `dist`.

**GitHub Pages:**
Set in `astro.config.mjs`:
```js
export default defineConfig({
  site: 'https://username.github.io',
  base: '/repo-name/',  // Only if not using custom domain
  // ...
});
```

Full Astro deployment guide: https://docs.astro.build/en/guides/deploy/

### Pre-deployment checklist

1. Set `site` in `astro.config.mjs` to your production URL
2. If using a subpath, set `base` (see section 2)
3. Run `npm run build` and check for errors
4. Run `npm run preview` and test all pages
5. Test navigation, search, and links
6. Verify images/assets load correctly
7. Check dark mode works

## 2. Subpath hosting (the #1 headache) {#subpath}

Hosting at `https://example.com/docs/` instead of the root is the single most common source of deployment bugs.

### Configuration

```js
// astro.config.mjs
export default defineConfig({
  site: 'https://example.com',
  base: '/docs/',
  integrations: [
    starlight({
      title: 'My Docs',
      // ... rest of config
    }),
  ],
});
```

Both `site` and `base` are required. `base` must start and end with `/`.

### What breaks and why

| Symptom | Cause | Fix |
|---|---|---|
| All links 404 after deploy | `base` not set | Add `base: '/docs/'` to config |
| Assets (CSS/JS) 404 | `base` not matching server path | Ensure `base` matches your reverse proxy or hosting path |
| Sidebar links go to wrong URLs | Mixing absolute and relative links | Use Starlight's built-in link handling; avoid hardcoded absolute paths |
| Search returns results but links are broken | Pagefind not aware of base path | Rebuild after setting `base`; Pagefind picks it up automatically |
| Images missing | Referencing from `public/` with wrong path | Use `~/assets/` imports for optimized images, or prefix public paths with the base |

### Reverse proxy setup (nginx example)

```nginx
location /docs/ {
    proxy_pass http://localhost:3000/docs/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

The proxy path must match the `base` path exactly.

### The failure pattern to avoid

1. Build docs locally at root `/` — everything works
2. Add reverse proxy at `/docs`
3. Deploy
4. Everything breaks: links, assets, search, sidebar

Prevention: **Set `base` from day one if you plan to use a subpath.** Test with `npm run preview` before deploying.

### Using Starlight at a subpath of an existing Astro site

If your main Astro site lives at `/` and you want docs at `/docs/`:

```js
// astro.config.mjs
export default defineConfig({
  integrations: [
    starlight({
      title: 'Docs',
      // Starlight handles the /docs/ prefix internally
    }),
  ],
});
```

Starlight will serve from `/docs/` based on the content collection location. See the manual setup guide for details.

## 3. Search configuration {#search}

### Pagefind (default)

Pagefind is enabled by default. It indexes all pages at build time and provides a built-in search UI.

**To disable:**
```js
starlight({ pagefind: false })
```

**To customize ranking:**
```js
starlight({
  pagefind: {
    ranking: {
      pageLength: 0.75,
      termFrequency: 1.2,
      termSaturation: 1.2,
      termSimilarity: 0.9,
    },
  },
})
```

**To search across multiple sites:**
```js
starlight({
  pagefind: {
    mergeIndex: [{
      bundlePath: 'https://other-site.com/_pagefind',
    }],
  },
})
```

**Excluding pages from search:**
```yaml
---
title: Hidden Page
pagefind: false
---
```

### Pagefind + subpaths

Pagefind should work with subpaths if `base` is configured correctly. If search breaks:
1. Ensure `base` is set in `astro.config.mjs`
2. Do a full rebuild (`npm run build`)
3. Check that `_pagefind/` directory exists in your build output

### Algolia DocSearch

To use Algolia instead of Pagefind:
1. Disable Pagefind: `pagefind: false`
2. Install Algolia integration or use a community plugin
3. Override the `Search` component:
```js
starlight({
  pagefind: false,
  components: {
    Search: './src/components/AlgoliaSearch.astro',
  },
})
```

## 4. Internationalization (i18n) {#i18n}

### Setup

```js
starlight({
  defaultLocale: 'en',
  locales: {
    en: { label: 'English' },
    es: { label: 'Español' },
    ja: { label: '日本語', lang: 'ja' },
    ar: { label: 'العربية', dir: 'rtl' },
  },
})
```

### Content structure for i18n

```
src/content/docs/
├── en/
│   ├── index.md
│   └── guides/
│       └── intro.md
├── es/
│   ├── index.md
│   └── guides/
│       └── intro.md
└── ja/
    └── index.md
```

### Root locale (no `/en/` prefix)

Serve the default language at the root:

```js
locales: {
  root: { label: 'English', lang: 'en' },
  es: { label: 'Español' },
},
```

Now English pages are at `/getting-started/` (not `/en/getting-started/`) and Spanish at `/es/getting-started/`.

### Translating sidebar labels

```js
sidebar: [{
  label: 'Guides',
  translations: { es: 'Guías', ja: 'ガイド' },
  items: [
    {
      slug: 'guides/intro',
      label: 'Introduction',
      translations: { es: 'Introducción' },
    },
  ],
}],
```

### i18n content collection

For UI string translations, add the i18n collection:

```ts
// src/content.config.ts
import { docsLoader, i18nLoader } from '@astrojs/starlight/loaders';
import { docsSchema, i18nSchema } from '@astrojs/starlight/schema';

export const collections = {
  docs: defineCollection({ loader: docsLoader(), schema: docsSchema() }),
  i18n: defineCollection({ loader: i18nLoader(), schema: i18nSchema() }),
};
```

### Fallback content

If a translation doesn't exist, Starlight shows the default locale version with a notice. This is automatic.

## 5. Versioned documentation {#versioning}

Starlight does **not** have built-in versioning. This is a known limitation and a common pain point for teams.

### Workarounds

**Option A: Folder-based versions**

```
src/content/docs/
├── v1/
│   ├── getting-started.md
│   └── api.md
├── v2/
│   ├── getting-started.md
│   └── api.md
└── latest/           # Symlink or copy of current version
```

Sidebar config:
```js
sidebar: [
  {
    label: 'v2 (Latest)',
    autogenerate: { directory: 'v2' },
  },
  {
    label: 'v1',
    collapsed: true,
    autogenerate: { directory: 'v1' },
  },
],
```

Problems with this approach:
- Content duplication
- Sidebar gets long with many versions
- No automatic version switcher

**Option B: Separate builds per version**

Deploy each version as a separate Starlight site:
- `docs.example.com/v1/` — separate Starlight build
- `docs.example.com/v2/` — separate Starlight build

Use Pagefind's `mergeIndex` to search across versions.

**Option C: Community plugins**

Check the Starlight plugin showcase for versioning plugins: https://starlight.astro.build/resources/plugins/

## 6. Authentication / private docs {#auth}

Starlight is static-first, which makes auth non-trivial.

### Options

**Hosting-level auth (simplest):**
- Vercel: Use [Vercel Authentication](https://vercel.com/docs/security/password-protection)
- Netlify: Use [Netlify Identity](https://docs.netlify.com/security/secure-access-to-sites/)
- Cloudflare: Use [Cloudflare Access](https://developers.cloudflare.com/cloudflare-one/applications/configure-apps/)

**SSR mode with middleware:**
Set `prerender: false` in Starlight config, add an SSR adapter, and use Astro middleware:

```js
// astro.config.mjs
import node from '@astrojs/node';

export default defineConfig({
  output: 'server',
  adapter: node({ mode: 'standalone' }),
  integrations: [
    starlight({
      prerender: false,
      // ...
    }),
  ],
});
```

```ts
// src/middleware.ts
import { defineMiddleware } from 'astro:middleware';

export const onRequest = defineMiddleware(async (context, next) => {
  // Check auth cookie/token
  const isAuthenticated = checkAuth(context.request);
  if (!isAuthenticated && context.url.pathname.startsWith('/private/')) {
    return context.redirect('/login');
  }
  return next();
});
```

**Mixed public/private:**
- Keep public docs as static (default)
- Use `src/pages/` for private routes with middleware-based auth

## 7. SSR (server-side rendering) {#ssr}

By default, Starlight prerenders all pages to static HTML. To render on demand:

```js
starlight({
  prerender: false,
})
```

Requires an SSR adapter (Node, Vercel, Netlify, Cloudflare, etc.).

Note: Pagefind search requires prerendered pages. If `prerender: false`, you must disable Pagefind and use an alternative search solution.

## 8. Plugins {#plugins}

Starlight has a plugin API for extending functionality.

### Using plugins

```js
import starlightPlugin from 'some-starlight-plugin';

starlight({
  plugins: [starlightPlugin()],
})
```

### Popular community plugins

Check the showcase: https://starlight.astro.build/resources/plugins/

Common categories:
- Blog integration
- Versioning
- API documentation generators
- Additional search providers
- Analytics
- Custom sidebar enhancements

### Plugin API

Plugins can:
- Modify the Starlight config
- Add custom CSS
- Override components
- Add Astro integrations
- Hook into the build process

See: https://starlight.astro.build/reference/plugins/

---
name: astro-advanced
description: >
  Comprehensive skill for building, configuring, and troubleshooting Astro projects.
  Use this skill whenever the user mentions Astro, .astro files, Astro config, Astro islands,
  partial hydration, client directives (client:load, client:visible, client:idle), Astro SSR,
  Astro adapters (Node, Vercel, Cloudflare, Netlify), Astro content collections, Astro layouts,
  hybrid rendering, astro.config.mjs, or any framework integration with Astro (Vue, React, Svelte).
  Also trigger when the user is debugging broken Astro builds, hydration mismatches, routing issues,
  base path problems, or deployment failures on static/serverless hosts. Even if the user doesn't
  say "Astro" explicitly, trigger if they reference .astro file syntax, frontmatter fences (---),
  or island architecture concepts. This skill covers project setup, rendering modes (SSG/SSR/hybrid),
  SSR caching, SEO, layouts, templates, Vue island integration, content collections, data fetching,
  deployment, auth, performance, and troubleshooting.
---

# Astro Advanced Skill

This skill provides production-grade guidance for Astro projects — from initial scaffolding through
deployment, caching, and performance tuning. It covers the patterns that actually matter in real
projects and the mistakes that actually happen.

## How to use this skill

1. **Read this file first** for the core workflow and decision tree.
2. **Consult the reference files** in `references/` for deep dives on specific topics:
   - `references/setup-and-structure.md` — Project creation, file structure, config, adapters
   - `references/rendering-modes.md` — SSG vs SSR vs Hybrid, when to use each, caching strategies
   - `references/seo.md` — Meta tags, Open Graph, JSON-LD, sitemaps, canonical URLs
   - `references/islands-and-vue.md` — Island architecture, client directives, Vue/React/Svelte integration
   - `references/content-and-data.md` — Content collections, data fetching, dynamic routes
   - `references/deployment.md` — Adapters, static hosts, serverless, environment variables
   - `references/performance.md` — Image optimization, bundle analysis, hydration control
   - `references/troubleshooting.md` — Common errors and fixes organized by symptom

## Core decision tree

When helping with an Astro project, follow this sequence:

### 1. Identify the rendering strategy first
This is the single most important decision in any Astro project. Everything else flows from it.

- **Pure static site (blog, docs, marketing)?** → SSG (default). No adapter needed.
- **Needs user-specific data, auth, or real-time content?** → SSR with an adapter.
- **Mostly static but a few dynamic pages?** → Hybrid mode. Set `output: 'static'` in config and use `export const prerender = false` on dynamic pages.

### 2. Pick the right adapter
Only needed for SSR or hybrid:
- **Vercel** → `@astrojs/vercel` (serverless or edge)
- **Netlify** → `@astrojs/netlify`
- **Cloudflare Pages** → `@astrojs/cloudflare`
- **Self-hosted Node** → `@astrojs/node` (standalone or middleware)

### 3. Set up integrations
Add only what you need. Each integration is a potential build-time dependency:

```bash
# Common additions
npx astro add vue        # Vue islands
npx astro add tailwind   # Tailwind CSS
npx astro add mdx        # MDX support
npx astro add sitemap    # Auto sitemap generation
```

### 4. Establish content strategy
- **Few pages, hand-authored** → Regular `.astro` pages in `/src/pages`
- **Blog/docs with structured content** → Content collections with Zod schemas
- **CMS-driven** → Fetch at build time (SSG) or runtime (SSR)

### 5. Apply SEO from the start
Don't bolt it on later. See `references/seo.md` for the full pattern, but at minimum:
- Create a reusable `<SEO>` component for head tags
- Set up canonical URLs
- Add structured data (JSON-LD) for key pages
- Generate sitemap via `@astrojs/sitemap`

## Key patterns to always follow

### Layout pattern
Every page should use a layout. Layouts handle `<html>`, `<head>`, and shared chrome:

```astro
---
// src/layouts/Base.astro
import SEO from '../components/SEO.astro';
const { title, description } = Astro.props;
---
<html lang="en">
  <head>
    <SEO title={title} description={description} />
  </head>
  <body>
    <nav><!-- shared nav --></nav>
    <slot />
    <footer><!-- shared footer --></footer>
  </body>
</html>
```

### Island pattern
Static by default. Only hydrate what needs interactivity:

```astro
<!-- Static: renders HTML, ships zero JS -->
<Card title="Hello" />

<!-- Interactive: hydrates on load -->
<Counter client:load />

<!-- Interactive: hydrates when visible (lazy) -->
<ImageGallery client:visible />
```

**The #1 Astro mistake**: forgetting `client:*` on a component that needs interactivity,
then wondering why click handlers don't work.

### SSR caching pattern
SSR without caching is just a slow website. Always pair SSR with a caching strategy:

```ts
// In an SSR endpoint or page
return new Response(JSON.stringify(data), {
  headers: {
    "Cache-Control": "public, s-maxage=60, stale-while-revalidate=300",
    "Content-Type": "application/json"
  }
});
```

## When things go wrong

Read `references/troubleshooting.md` for a symptom-based guide. The top 5 issues:

1. **"Component doesn't do anything"** → Missing `client:*` directive
2. **Build fails after adding integration** → Version mismatch, check `package.json`
3. **SSR returns 500** → Missing adapter or wrong `output` mode in config
4. **Broken links after deploy** → Base path not set, or trailing slash mismatch
5. **Hydration mismatch errors** → Server/client HTML differs (conditional rendering, dates, randomness)

## File output conventions

When generating Astro project files:
- Always include the frontmatter fence (`---`) even if empty
- Use `.astro` extension for Astro components and pages
- Place pages in `src/pages/`, components in `src/components/`, layouts in `src/layouts/`
- Use TypeScript in frontmatter when the project uses TS
- Include `astro.config.mjs` with only the integrations and settings actually needed

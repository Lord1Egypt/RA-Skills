---
name: astro-project-analyzer
description: Analyze and optimize Astro projects — audit configuration, performance, SEO, accessibility, content collections, and integration setup.
metadata:
  tags: ["astro", "web", "performance", "seo", "frontend"]
---

# Astro Project Analyzer

Analyze Astro projects for configuration quality, performance optimization, SEO compliance, accessibility, and best practices. Use when setting up new Astro sites, auditing existing ones, migrating from other frameworks, or optimizing build performance.

## Usage

```
"Analyze this Astro project for issues"
"Optimize my Astro site's performance"
"Check my Astro config for best practices"
"Audit content collections for consistency"
"Help migrate my Next.js site to Astro"
```

## How It Works

### 1. Project Discovery

Scan the Astro project structure:

```bash
# Detect Astro version and config
cat astro.config.mjs 2>/dev/null || cat astro.config.ts 2>/dev/null
cat package.json | python3 -c "import json,sys; d=json.load(sys.stdin); print('Astro:', d.get('dependencies',{}).get('astro', d.get('devDependencies',{}).get('astro','not found')))"

# Map project structure
find src -type f | head -50
ls src/pages/ src/layouts/ src/components/ src/content/ 2>/dev/null
```

### 2. Configuration Audit

Check `astro.config.mjs` for:

- **Output mode**: static vs server vs hybrid — matches use case?
- **Integrations**: are all configured integrations used? Missing useful ones?
- **Build settings**: outDir, compressHTML, scopedStyleStrategy
- **Image optimization**: configured with `@astrojs/image` or built-in `astro:assets`?
- **Adapter**: correct adapter for deployment target (Vercel, Netlify, Node, Cloudflare)
- **Prefetch**: configured for navigation performance?
- **View Transitions**: enabled for SPA-like navigation?
- **Markdown/MDX**: remark/rehype plugins configured appropriately?
- **Vite config**: any unnecessary overrides or missing optimizations?

### 3. Performance Analysis

- **Island architecture**: are interactive components properly isolated?
- **Client directives**: appropriate use of `client:load`, `client:idle`, `client:visible`, `client:media`, `client:only`
- **Bundle size**: check for heavy client-side JS in static pages
- **Image optimization**: all images using `<Image>` component? WebP/AVIF?
- **Font loading**: using `@fontsource` or optimized font strategy?
- **CSS strategy**: scoped styles vs global? Unused CSS?
- **Build time**: identify slow pages, large content collections

### 4. Content Collections

If using content collections (`src/content/`):

- Schema validation with Zod: complete and correct?
- Frontmatter consistency across entries
- Missing required fields
- Orphaned content (files not in any collection)
- Collection references and relations
- Slug generation and uniqueness

### 5. SEO & Accessibility

- Meta tags: title, description, og:image on all pages
- Sitemap integration configured?
- Robots.txt present?
- Canonical URLs set correctly?
- Structured data (JSON-LD) for key pages?
- Alt text on all images
- Heading hierarchy (single h1, proper nesting)
- Color contrast in theme
- Keyboard navigation for interactive elements
- ARIA labels on icon buttons

### 6. Routing & Pages

- Dynamic routes properly typed
- 404 page exists
- API routes (if server mode) have proper error handling
- Pagination implemented for large collections
- RSS feed configured for blog/content sites

### 7. Deployment Readiness

- Correct adapter installed for target platform
- Environment variables documented
- Build command produces clean output
- No dev-only dependencies in production
- Cache headers configured appropriately

## Output

```
## Astro Project Analysis

**Version:** Astro 5.2.1 | **Mode:** hybrid | **Adapter:** @astrojs/vercel

### 🔴 Issues (3)
1. Missing `<Image>` component — 8 pages use raw `<img>` tags
   → Import from 'astro:assets' for automatic optimization
2. `client:load` on footer newsletter form — should be `client:visible`
   → Form is below fold, no need to hydrate on page load
3. No sitemap integration — search engines can't discover pages
   → Add @astrojs/sitemap to integrations

### 🟡 Improvements (5)
4. Content collection "blog" has no schema validation
   → Add Zod schema in src/content/config.ts
5. Global CSS file is 12KB — 40% unused on most pages
   → Convert to scoped styles or use CSS purging
[...]

### 🟢 Good Practices
- View Transitions enabled for smooth navigation
- Proper island architecture — only 3 interactive components
- Images in WebP format with fallbacks
- Font loaded via @fontsource (no external requests)

### Performance Score
- Estimated Lighthouse: 92/100 (after fixes: 97/100)
- Total client JS: 23KB (good for hybrid site)
- Build time: ~8s for 47 pages
```

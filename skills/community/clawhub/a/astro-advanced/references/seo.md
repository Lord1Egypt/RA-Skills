# SEO Best Practices for Astro

## Table of Contents
1. [Why Astro is great for SEO](#why-astro)
2. [Reusable SEO component](#seo-component)
3. [Open Graph & social meta](#open-graph)
4. [Structured data (JSON-LD)](#structured-data)
5. [Sitemap & robots.txt](#sitemap)
6. [Canonical URLs](#canonical-urls)
7. [Performance signals](#performance)
8. [Common SEO mistakes in Astro](#mistakes)

---

## Why Astro is great for SEO

Astro outputs static HTML by default — no JavaScript required for content rendering. This means:
- Search engines see full content on first crawl (no hydration needed)
- Core Web Vitals are excellent out of the box (minimal JS = fast LCP, low TBT)
- No flash of unstyled/empty content

The main risk is undoing these advantages by shipping too much client-side JS through islands.

---

## Reusable SEO component

Create a single component that handles all head meta. Use it in every layout.

```astro
---
// src/components/SEO.astro
interface Props {
  title: string;
  description: string;
  image?: string;
  canonicalURL?: string;
  type?: 'website' | 'article';
  publishedDate?: string;
  noindex?: boolean;
}

const {
  title,
  description,
  image = '/og-default.png',
  canonicalURL = new URL(Astro.url.pathname, Astro.site).href,
  type = 'website',
  publishedDate,
  noindex = false,
} = Astro.props;

const siteName = 'Your Site Name';
const fullTitle = `${title} | ${siteName}`;
const absoluteImage = new URL(image, Astro.site).href;
---

<!-- Primary meta -->
<title>{fullTitle}</title>
<meta name="description" content={description} />
{noindex && <meta name="robots" content="noindex, nofollow" />}
<link rel="canonical" href={canonicalURL} />

<!-- Open Graph -->
<meta property="og:type" content={type} />
<meta property="og:title" content={title} />
<meta property="og:description" content={description} />
<meta property="og:image" content={absoluteImage} />
<meta property="og:url" content={canonicalURL} />
<meta property="og:site_name" content={siteName} />
{publishedDate && <meta property="article:published_time" content={publishedDate} />}

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content={title} />
<meta name="twitter:description" content={description} />
<meta name="twitter:image" content={absoluteImage} />
```

Usage in a layout:
```astro
---
import SEO from '../components/SEO.astro';
const { title, description } = Astro.props;
---
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <SEO title={title} description={description} />
  </head>
  <body>
    <slot />
  </body>
</html>
```

---

## Open Graph & social meta

### Dynamic OG images

For blog posts, generate unique OG images. Options:
1. **Static images per post** — Place in `/public/og/` and reference by slug
2. **Dynamic generation** — Use `@vercel/og`, Satori, or a similar library in an API route

```ts
// src/pages/og/[slug].png.ts — Dynamic OG image endpoint
import type { APIRoute } from 'astro';
import { getEntry } from 'astro:content';
// Use satori + sharp or @resvg/resvg-js to render HTML to PNG

export const GET: APIRoute = async ({ params }) => {
  const post = await getEntry('blog', params.slug!);
  // Generate and return PNG...
};
```

### Social preview checklist
- OG image is exactly 1200×630px
- Title is under 60 characters (truncation varies by platform)
- Description is under 155 characters
- Test with: Facebook Sharing Debugger, Twitter Card Validator, LinkedIn Post Inspector

---

## Structured data (JSON-LD)

Add structured data to help search engines understand your content.

### Article schema
```astro
---
const articleSchema = {
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": title,
  "description": description,
  "image": image,
  "datePublished": publishedDate,
  "dateModified": modifiedDate,
  "author": {
    "@type": "Person",
    "name": authorName,
    "url": authorURL
  },
  "publisher": {
    "@type": "Organization",
    "name": "Your Site",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  }
};
---
<script type="application/ld+json" set:html={JSON.stringify(articleSchema)} />
```

### Breadcrumb schema
```astro
---
const breadcrumbs = {
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com" },
    { "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://example.com/blog" },
    { "@type": "ListItem", "position": 3, "name": title },
  ]
};
---
<script type="application/ld+json" set:html={JSON.stringify(breadcrumbs)} />
```

### FAQ schema
```astro
---
const faqSchema = {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": faqs.map(faq => ({
    "@type": "Question",
    "name": faq.question,
    "acceptedAnswer": {
      "@type": "Answer",
      "text": faq.answer
    }
  }))
};
---
<script type="application/ld+json" set:html={JSON.stringify(faqSchema)} />
```

---

## Sitemap & robots.txt

### Sitemap
```bash
npx astro add sitemap
```

```js
// astro.config.mjs
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://example.com', // REQUIRED for sitemap
  integrations: [
    sitemap({
      filter: (page) => !page.includes('/admin/'), // Exclude pages
      changefreq: 'weekly',
      priority: 0.7,
      lastmod: new Date(),
    }),
  ],
});
```

### robots.txt
Place in `/public/robots.txt`:
```
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/

Sitemap: https://example.com/sitemap-index.xml
```

---

## Canonical URLs

Every page needs a canonical URL to prevent duplicate content issues.

**The pattern**: Use `Astro.site` + `Astro.url.pathname` to build canonical URLs.

```astro
---
const canonicalURL = new URL(Astro.url.pathname, Astro.site);
---
<link rel="canonical" href={canonicalURL.href} />
```

**Watch out for**:
- Trailing slash inconsistency (`/about` vs `/about/` are different URLs)
- Query parameters (canonical should not include `?page=2` etc.)
- `www` vs non-`www` (pick one and redirect the other)
- HTTP vs HTTPS (always canonical to HTTPS)

Set `trailingSlash` in config to match your host's behavior:
```js
export default defineConfig({
  trailingSlash: 'always', // or 'never'
});
```

---

## Performance signals (SEO-relevant)

Google uses Core Web Vitals as ranking signals. Astro makes these easy to ace.

**LCP (Largest Contentful Paint)**:
- Use `<Image />` from `astro:assets` for optimized images
- Preload the LCP image: `<link rel="preload" as="image" href={heroImage} />`
- Avoid lazy-loading above-the-fold images

**CLS (Cumulative Layout Shift)**:
- Always set `width` and `height` on images
- Avoid injecting content above existing content after load
- Reserve space for dynamic islands

**INP (Interaction to Next Paint)**:
- Ship minimal JS (Astro's default behavior)
- Use `client:visible` or `client:idle` instead of `client:load` where possible
- Avoid heavy computation in event handlers

---

## Common SEO mistakes in Astro

1. **Forgetting `site` in config** → `Astro.site` is undefined, canonical URLs and sitemap break silently.

2. **No canonical URLs** → Duplicate content across routes (with/without trailing slash, www/non-www).

3. **Same meta on every page** → Every page should have a unique `<title>` and `<meta name="description">`.

4. **Missing OG image** → Social shares look broken. Always provide a fallback default.

5. **Over-hydrating destroys performance** → Adding `client:load` to everything ships tons of JS, killing Core Web Vitals. Use the lightest directive possible.

6. **Dynamic SSR pages without meta** → SSR pages still need proper `<title>` and meta tags. Fetch the data first, then render the head.

7. **Not testing with `View Source`** → Islands that render client-side only (missing SSR support) may show empty HTML to crawlers. Always check the raw HTML output.

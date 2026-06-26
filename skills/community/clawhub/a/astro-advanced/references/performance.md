# Performance Optimization

## Table of Contents
1. [Image optimization](#images)
2. [Hydration control](#hydration)
3. [Bundle analysis](#bundle)
4. [Font loading](#fonts)
5. [Prefetching](#prefetching)
6. [Build performance](#build)

---

## Image optimization

Astro has built-in image optimization via `astro:assets`. Use it — raw `<img>` tags are a performance miss.

### The `<Image />` component
```astro
---
import { Image } from 'astro:assets';
import heroImage from '../assets/hero.jpg';
---

<!-- Optimized: resized, converted to WebP/AVIF, width/height set -->
<Image src={heroImage} alt="Hero" />

<!-- With explicit dimensions -->
<Image src={heroImage} alt="Hero" width={800} height={400} />

<!-- Remote images (must be configured) -->
<Image
  src="https://example.com/photo.jpg"
  alt="Remote"
  width={600}
  height={300}
  inferSize  <!-- Or use inferSize to auto-detect -->
/>
```

### Configure remote image domains
```js
// astro.config.mjs
export default defineConfig({
  image: {
    domains: ['example.com', 'cdn.example.com'],
    // Or allow all remotes (less secure):
    // remotePatterns: [{ protocol: 'https' }],
  },
});
```

### The `<Picture />` component
For responsive art direction:
```astro
---
import { Picture } from 'astro:assets';
import hero from '../assets/hero.jpg';
---

<Picture
  src={hero}
  formats={['avif', 'webp']}
  alt="Hero"
  widths={[400, 800, 1200]}
  sizes="(max-width: 600px) 400px, (max-width: 900px) 800px, 1200px"
/>
```

### Critical image tips
- **Never lazy-load above-the-fold images** — it delays LCP
- **Always set width and height** — prevents layout shift (CLS)
- **Use `loading="eager"` for LCP image**, `loading="lazy"` for everything else
- **Preload the hero image** in the layout `<head>`:
  ```html
  <link rel="preload" as="image" href={heroSrc} />
  ```

---

## Hydration control

The fewer islands you hydrate, the faster your site. Audit every `client:*` directive.

### Hydration audit checklist
For each component with a `client:*` directive, ask:
1. Does this component actually need JavaScript? (Display-only components don't)
2. Is this component above the fold? (If not, use `client:visible`)
3. Is this component critical to the page? (If not, use `client:idle`)
4. Does the entire component need to be interactive? (Extract the interactive part into a smaller island)

### Splitting large components
Instead of hydrating a large component:
```astro
<!-- Bad: hydrates the entire product card just for the "Add to Cart" button -->
<ProductCard client:load product={product} />
```

Split into static + interactive:
```astro
<!-- Good: static HTML for display, tiny island for the button -->
<ProductCard product={product} />
<AddToCartButton client:idle productId={product.id} />
```

### Measuring hydration cost
Check the Network tab in DevTools:
- Filter by JS files
- Look at which islands load the most JS
- Each island creates its own chunk — find the heavy ones

---

## Bundle analysis

### Inspect the build output
```bash
npm run build
# Check dist/ size
du -sh dist/
du -sh dist/_astro/  # JS + CSS bundles
```

### Use Vite's bundle visualizer
```js
// astro.config.mjs
export default defineConfig({
  vite: {
    build: {
      rollupOptions: {
        plugins: [
          // Add visualizer plugin
        ],
      },
    },
  },
});
```

Or install and use `vite-bundle-visualizer`:
```bash
npx vite-bundle-visualizer
```

### Common bundle bloat sources
- **Large framework islands**: A single Vue/React component pulls in the entire framework runtime
- **Unused library imports**: `import _ from 'lodash'` instead of `import debounce from 'lodash/debounce'`
- **All-in-one component libraries**: Import only the components you use
- **Client-side routing libraries**: Astro doesn't need SPA routing; use standard `<a>` tags

---

## Font loading

Fonts are a common LCP blocker. Load them efficiently.

### Self-host fonts (preferred)
```css
/* src/styles/fonts.css */
@font-face {
  font-family: 'MyFont';
  src: url('/fonts/myfont.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap; /* Show fallback immediately, swap when loaded */
}
```

### Preload critical fonts
```astro
<!-- In your layout <head> -->
<link
  rel="preload"
  href="/fonts/myfont.woff2"
  as="font"
  type="font/woff2"
  crossorigin
/>
```

### Font subsetting
Only include the characters you need:
```bash
# Using glyphhanger
npx glyphhanger --whitelist="US_ASCII" --subset=myfont.ttf
```

### Google Fonts the right way
Don't use the default `<link>` tag. Instead, self-host:
```bash
# Download fonts locally with fontsource
npm install @fontsource/inter
```

```ts
// In your layout frontmatter
import '@fontsource/inter/400.css';
import '@fontsource/inter/700.css';
```

---

## Prefetching

Astro has built-in link prefetching to speed up navigation.

```js
// astro.config.mjs
export default defineConfig({
  prefetch: {
    prefetchAll: false,          // Don't prefetch everything
    defaultStrategy: 'viewport', // Prefetch links when they enter viewport
  },
});
```

### Per-link control
```html
<!-- Prefetch on hover (default) -->
<a href="/about" data-astro-prefetch>About</a>

<!-- Prefetch when visible in viewport -->
<a href="/blog" data-astro-prefetch="viewport">Blog</a>

<!-- Don't prefetch -->
<a href="/heavy-page" data-astro-prefetch="false">Heavy Page</a>
```

---

## Build performance

### Speed up large SSG builds

**Limit getStaticPaths in development**:
```ts
export async function getStaticPaths() {
  const posts = await getCollection('blog');

  // In dev, only build a few pages for speed
  if (import.meta.env.DEV) {
    return posts.slice(0, 5).map(post => ({
      params: { slug: post.slug },
      props: { post },
    }));
  }

  return posts.map(post => ({
    params: { slug: post.slug },
    props: { post },
  }));
}
```

**Deduplicate API calls**: Astro caches `fetch()` calls during static builds. Use the same URL to benefit from deduplication:
```ts
// These two calls hit the API only once
const res1 = await fetch('https://api.example.com/posts');
const res2 = await fetch('https://api.example.com/posts');
```

**Parallelize where possible**: Astro builds pages in parallel. But if your data fetching is sequential, that bottlenecks the build.

### Reduce build output size
- Use `<Image />` instead of raw `<img>` (smaller optimized images)
- Remove unused CSS (Astro scopes styles by default, but global CSS can bloat)
- Check for duplicate dependencies: `npm ls | grep duplicated`

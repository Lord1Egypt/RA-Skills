# Troubleshooting Guide

Organized by symptom. Find what's broken, then follow the fix.

## Table of Contents
1. [Component doesn't do anything (no interactivity)](#no-interactivity)
2. [Hydration mismatch errors](#hydration-mismatch)
3. [Build fails after adding integration](#integration-build-fail)
4. [SSR returns 500 or blank page](#ssr-500)
5. [Broken links / 404 after deploy](#broken-links)
6. ["window is not defined" / "document is not defined"](#window-undefined)
7. [Content collection errors](#content-errors)
8. [Styles not applying](#styles-broken)
9. [Dynamic routes not working](#dynamic-routes)
10. [Environment variables undefined](#env-undefined)
11. [Slow builds](#slow-builds)
12. [CORS errors from API calls](#cors)
13. [Images not loading](#images-broken)
14. [TypeScript errors](#typescript)
15. [Dev server issues](#dev-server)

---

## 1. Component doesn't do anything (no interactivity) {#no-interactivity}

**Symptom**: Component renders HTML but buttons, inputs, event handlers don't work.

**Cause**: Missing `client:*` directive. Without it, Astro renders static HTML and ships zero JS.

**Fix**:
```astro
<!-- Before: static HTML only -->
<Counter />

<!-- After: hydrated and interactive -->
<Counter client:load />
```

**Checklist if you already have a client directive**:
- Is the directive on the right component? (Check parent vs child)
- Is the component a `.astro` file? (Astro components can't be hydrated — only framework components like `.vue`, `.tsx`, `.svelte`)
- Is the integration installed? (`npx astro add vue`)

---

## 2. Hydration mismatch errors {#hydration-mismatch}

**Symptom**: Console warns about hydration mismatch. UI might flicker or revert after load.

**Cause**: HTML rendered on the server differs from what the client renders.

**Common triggers**:
- Using `Date.now()`, `Math.random()`, or `new Date()` in the render template
- Reading `localStorage` or `window.innerWidth` during render
- Conditional rendering based on browser-only values
- Different timezone between server and client

**Fix pattern**:
```vue
<script setup>
import { ref, onMounted } from 'vue';

// Use a safe default for SSR
const width = ref(1024);

// Update with real value after mount (client only)
onMounted(() => {
  width.value = window.innerWidth;
});
</script>
```

**Nuclear option**: Use `client:only="vue"` to skip SSR entirely for that component. Only do this if you can't fix the mismatch.

---

## 3. Build fails after adding integration {#integration-build-fail}

**Symptom**: `npm run build` or `npm run dev` crashes after installing a new integration.

**Diagnosis**:
```bash
# Check for version conflicts
npm ls --depth=0

# Clear caches
rm -rf node_modules/.astro
rm -rf node_modules/.vite

# Reinstall
rm -rf node_modules
npm install
```

**Common causes**:
- **Integration version incompatible with Astro version**: Check the integration's docs for supported Astro versions
- **Conflicting peer dependencies**: Two integrations requiring different versions of a shared dependency
- **Config not updated**: `npx astro add` updates config automatically; manual install doesn't

**Fix**: Use `npx astro add <integration>` instead of `npm install`. It handles both package.json and astro.config.mjs.

---

## 4. SSR returns 500 or blank page {#ssr-500}

**Symptom**: SSR pages return HTTP 500 or render nothing.

**Checklist**:
1. **Is `output` set correctly?**
   ```js
   // astro.config.mjs
   export default defineConfig({
     output: 'server', // Must be 'server' for full SSR
   });
   ```

2. **Is an adapter installed?**
   ```bash
   npx astro add node  # or vercel, netlify, cloudflare
   ```

3. **Check server logs** — the actual error is in the terminal/server output, not the browser.

4. **Does the page have `export const prerender = false`?** If you're using hybrid mode (output: 'static'), SSR pages need this.

5. **Are environment variables available?** SSR runs on the server — check server-side env vars, not just build-time ones.

6. **Is `Astro.redirect()` returning correctly?**
   ```astro
   ---
   // Must RETURN the redirect
   if (!user) return Astro.redirect('/login');
   // Without return, execution continues
   ---
   ```

---

## 5. Broken links / 404 after deploy {#broken-links}

**Symptom**: Site works locally but links 404 in production.

**Check these in order**:

1. **Base path**:
   ```js
   // If hosting at https://example.com/docs/
   export default defineConfig({
     base: '/docs/',
   });
   ```
   All internal links must use the base. Use `import.meta.env.BASE_URL` for dynamic base.

2. **Trailing slash mismatch**:
   ```js
   export default defineConfig({
     trailingSlash: 'always', // Match your host's behavior
   });
   ```
   Netlify adds trailing slashes by default. Vercel doesn't. Mismatch = redirect loops or 404s.

3. **Case sensitivity**: macOS doesn't care about case; Linux does. `About.astro` creates `/About` on Linux, which is different from `/about`.

4. **SSR pages on static host**: If you deployed SSR pages to a static host (GitHub Pages, S3), they won't exist. Either prerender them or use an SSR-capable host.

---

## 6. "window is not defined" / "document is not defined" {#window-undefined}

**Symptom**: Build or SSR crashes with ReferenceError about browser globals.

**Cause**: Code that runs on the server is trying to use browser-only APIs.

**Where this happens**:
- Astro frontmatter (always runs on server)
- Framework component render functions (run on server during SSR)
- Third-party libraries that assume a browser environment

**Fixes**:

1. **Move to `onMounted` / `useEffect`** (only runs in browser):
   ```vue
   <script setup>
   import { onMounted } from 'vue';
   onMounted(() => {
     // Safe: only runs in browser
     const el = document.getElementById('my-element');
   });
   </script>
   ```

2. **Guard with typeof check**:
   ```ts
   if (typeof window !== 'undefined') {
     window.addEventListener('scroll', handler);
   }
   ```

3. **Use `client:only`** to skip SSR entirely:
   ```astro
   <MapComponent client:only="vue" />
   ```

4. **Lazy import browser-only libraries**:
   ```ts
   let lib;
   if (typeof window !== 'undefined') {
     lib = await import('browser-only-lib');
   }
   ```

---

## 7. Content collection errors {#content-errors}

### "Collection X not found"
- Does `src/content/config.ts` exist?
- Does it export the collection? `export const collections = { blog };`
- Does the folder name match? `src/content/blog/` for collection `blog`
- Run `npx astro sync` to regenerate types

### Schema validation error
```
[ERROR] blog/my-post.md frontmatter does not match collection schema
```
- Check the error details — it tells you which field failed
- Common: using `z.date()` instead of `z.coerce.date()` for frontmatter dates
- Common: missing required fields in frontmatter
- Common: wrong type (string where number expected)

### Content not updating in dev
- Restart the dev server after changing `config.ts`
- Run `npx astro sync` after schema changes
- Clear `.astro` cache: `rm -rf node_modules/.astro`

---

## 8. Styles not applying {#styles-broken}

### Scoped styles not working on child components
Astro scoped styles only apply to HTML in the current `.astro` file, not children.

```astro
<style>
  /* Only affects <h1> directly in THIS file, not in child components */
  h1 { color: red; }
</style>
```

**Fix**: Use `:global()` to target child HTML, or use `is:global` on the style tag:
```astro
<style>
  :global(.child-class) { color: red; }
</style>

<!-- Or make the entire block global -->
<style is:global>
  .applies-everywhere { color: red; }
</style>
```

### Tailwind not working
- Is the integration installed? `npx astro add tailwind`
- Is `@tailwind` imported in a global CSS file or layout?
- Check `tailwind.config.mjs` content paths include `.astro` files:
  ```js
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}']
  ```

### Styles flash or disappear
- FOUC (Flash of Unstyled Content): Make sure CSS is in `<head>`, not dynamically injected
- Check that scoped styles aren't conflicting with global styles

---

## 9. Dynamic routes not working {#dynamic-routes}

### SSG: "getStaticPaths() is required"
```
[ERROR] [GetStaticPaths] `getStaticPaths()` function is required for dynamic routes.
```
Static mode requires all paths to be known at build time:
```astro
---
export async function getStaticPaths() {
  return [
    { params: { slug: 'post-1' } },
    { params: { slug: 'post-2' } },
  ];
}
---
```

### SSR: Params are undefined
Check that the file naming matches:
- `[slug].astro` → `Astro.params.slug`
- `[...path].astro` → `Astro.params.path`
- `[category]/[id].astro` → `Astro.params.category`, `Astro.params.id`

---

## 10. Environment variables undefined {#env-undefined}

### In frontmatter (server):
```ts
// All variables available
console.log(import.meta.env.SECRET_KEY);     // ✓
console.log(import.meta.env.PUBLIC_API_URL); // ✓
```

### In client-side island:
```ts
// ONLY PUBLIC_ prefixed variables
console.log(import.meta.env.PUBLIC_API_URL); // ✓
console.log(import.meta.env.SECRET_KEY);     // undefined (by design)
```

### In production (SSR):
- Set variables on the hosting platform, not just in `.env`
- `.env` files are used during build. SSR runtime needs actual environment variables.
- On Vercel/Netlify: set in dashboard
- On Node: set in shell or use dotenv

---

## 11. Slow builds {#slow-builds}

**Diagnosis**: Run with timing:
```bash
time npm run build
```

**Common causes**:
- **Too many pages**: 10,000+ SSG pages = long builds. Consider hybrid (SSR for long-tail pages).
- **Heavy data fetching in getStaticPaths**: API calls during build. Cache or parallelize.
- **Unoptimized images**: Large images being processed at build time. Pre-optimize before adding to project.
- **Expensive integrations**: Some integrations add build steps. Test by removing one at a time.

**Quick fixes**:
- Limit pages in dev: `if (import.meta.env.DEV) return posts.slice(0, 10);`
- Use incremental builds if your host supports them (Vercel, Netlify)
- Pre-optimize images before import

---

## 12. CORS errors from API calls {#cors}

**Symptom**: Browser console shows CORS errors when fetching from an API.

**Key insight**: CORS only applies to browser-to-server requests. Server-to-server requests (Astro frontmatter, endpoints) are never blocked by CORS.

**Fix**: Move the API call from the client island to an Astro server endpoint:

```ts
// src/pages/api/proxy.ts — Astro endpoint (server-side, no CORS)
export const GET: APIRoute = async ({ url }) => {
  const res = await fetch(`https://external-api.com/data?q=${url.searchParams.get('q')}`);
  return new Response(await res.text(), {
    headers: { 'Content-Type': 'application/json' },
  });
};
```

Then call your own endpoint from the island:
```ts
// In your Vue/React island
const res = await fetch('/api/proxy?q=search');
```

---

## 13. Images not loading {#images-broken}

### Images from `src/assets/` not found
```astro
---
// Must use import for processed images
import hero from '../assets/hero.jpg';
---
<Image src={hero} alt="Hero" />
```

### Remote images not loading
Add the domain to allowed list:
```js
// astro.config.mjs
export default defineConfig({
  image: {
    domains: ['cdn.example.com'],
  },
});
```

### Images 404 after deploy
- Check `base` path in config
- Ensure images in `/public/` are deployed (some hosts ignore certain directories)
- For processed images, check that the build output includes `_astro/` directory

---

## 14. TypeScript errors {#typescript}

### "Cannot find module 'astro:content'"
Run `npx astro sync` to generate type definitions.

### Props type mismatch
```astro
---
// Define strict props interface
interface Props {
  title: string;
  count: number;  // If passing from parent, ensure it's a number, not string
}
const { title, count } = Astro.props;
---
```

### Integration types missing
```bash
# Regenerate all types
npx astro sync
```

---

## 15. Dev server issues {#dev-server}

### Port already in use
```bash
# Find what's using port 4321
lsof -i :4321
# Kill it, or use a different port:
npx astro dev --port 3000
```

### HMR (Hot Module Replacement) not working
- Some changes require a full restart (config changes, new content collections)
- Clear the Vite cache: `rm -rf node_modules/.vite`
- Check for circular imports

### Dev server crashes on save
- Usually a syntax error in `.astro` file — check terminal output
- Malformed frontmatter (missing closing `---`)
- Invalid TypeScript in frontmatter

---

## General debugging strategy

1. **Read the terminal error** — Astro's error messages are usually clear and point to the exact file/line
2. **Check `View Source`** — See the actual HTML output (not DevTools, which shows post-hydration DOM)
3. **Build locally first** — `npm run build && npm run preview` catches issues before deploying
4. **Isolate the problem** — Comment out components until you find which one causes the issue
5. **Check the Astro docs** — `docs.astro.build` has excellent troubleshooting sections
6. **Check GitHub issues** — `github.com/withastro/astro/issues` for known bugs

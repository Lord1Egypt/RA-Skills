# Troubleshooting Guide

Common errors and their solutions. Always read the full error message before jumping to solutions.
When an error appears, say: "אל תדאג — שגיאות הן חלק נורמלי מהתהליך. בואו נפתור את זה ביחד."

## Table of Contents
1. [Vercel Deployment Errors](#vercel-deployment-errors)
2. [Sanity Errors](#sanity-errors)
3. [Next.js Build Errors](#nextjs-build-errors)
4. [GitHub Errors](#github-errors)
5. [CORS Errors](#cors-errors)
6. [Image Errors](#image-errors)
7. [Environment Variable Errors](#environment-variable-errors)
8. [TypeScript Errors](#typescript-errors)
9. [RTL / Hebrew Display Issues](#rtl--hebrew-display-issues)
10. [WordPress Issues](#wordpress-issues)

---

## Vercel Deployment Errors

### Build Failed — Type Error
**Symptom:** Vercel build fails with `Type error: ...`
**Cause:** TypeScript found a type mismatch
**Fix:**
1. Run locally: `npm run build`
2. Read the exact error line
3. Fix the type issue (often: add `?` for optional props, or cast type)
4. Push again

### Build Failed — Module Not Found
**Symptom:** `Module not found: Can't resolve '@/components/...'`
**Cause:** Import path is wrong or file doesn't exist
**Fix:**
- Check the exact file name (case-sensitive on Linux/Vercel)
- Verify `@/` maps to `src/` in `tsconfig.json`:
```json
"paths": { "@/*": ["./src/*"] }
```

### Environment Variables Missing on Vercel
**Symptom:** Site works locally but not on Vercel, shows empty content
**Cause:** `.env.local` is not committed to GitHub (correct!), but variables weren't added to Vercel
**Fix:**
1. Go to Vercel Dashboard → Project → Settings → Environment Variables
2. Add every variable from `.env.local`
3. Redeploy: `vercel --prod` or push a commit

### Deployment Stuck / Not Triggering
**Symptom:** Pushed to GitHub but Vercel didn't redeploy
**Fix:**
1. Check Vercel Dashboard → Deployments — look for error
2. Go to Settings → Git → verify repository is connected
3. Manual redeploy: click "Redeploy" in dashboard

---

## Sanity Errors

### "Unauthorized" — 401 Error
**Symptom:** API calls return 401 or content doesn't load
**Cause:** Sanity token is wrong, expired, or missing
**Fix:**
1. Go to `https://sanity.io/manage` → your project → API → Tokens
2. Check if your token is still there
3. If deleted or expired, create a new one
4. Update `.env.local` AND Vercel environment variables

### "CORS Policy" Error in Studio
**Symptom:** Sanity Studio shows CORS error in browser
**Fix:**
1. Go to `https://sanity.io/manage` → your project → API → CORS Origins
2. Add your localhost: `http://localhost:3000`
3. Add your Vercel URL: `https://yoursite.vercel.app`
4. Add your custom domain if you have one

### Sanity Studio Not Loading (blank page)
**Symptom:** Going to `/studio` shows blank page or loading forever
**Fix:**
1. Check `src/app/studio/[[...tool]]/page.tsx` exists
2. Check `sanity.config.ts` has correct project ID and dataset
3. Run locally: `npm run dev` → go to `localhost:3000/studio`
4. Look for console errors (F12 → Console tab)

### Images Not Appearing from Sanity
**Symptom:** Images show broken icon or don't load
**Fix:**
1. Confirm `next.config.ts` allows `cdn.sanity.io`:
```ts
images: {
  remotePatterns: [{ protocol: 'https', hostname: 'cdn.sanity.io' }]
}
```
2. Make sure you're using `urlFor(image).url()` properly

### Content Not Updating After Edit in Studio
**Symptom:** Changed content in Sanity Studio but site doesn't reflect it
**Cause:** Next.js caches data
**Fix (for development):**
```bash
# Restart dev server
Ctrl+C → npm run dev
```
**Fix (for production):** Use `revalidate` in your fetch:
```ts
// In page.tsx or fetch call:
export const revalidate = 60 // revalidate every 60 seconds
```
Or use on-demand revalidation with a Sanity webhook.

---

## Next.js Build Errors

### "window is not defined"
**Symptom:** Build fails with `ReferenceError: window is not defined`
**Cause:** Code using browser APIs runs during server-side rendering
**Fix:**
```tsx
// Option 1: Add 'use client' at top of file
'use client'

// Option 2: Check if window exists
const isBrowser = typeof window !== 'undefined'

// Option 3: Use dynamic import with ssr: false
import dynamic from 'next/dynamic'
const Component = dynamic(() => import('./Component'), { ssr: false })
```

### Hydration Mismatch
**Symptom:** Console error: `Text content did not match. Server: "..." Client: "..."`
**Cause:** Server and client render different content
**Common causes:**
- Using `Math.random()` in JSX
- Using `new Date()` without formatting it the same way
- Browser extensions modifying the DOM
**Fix:** Move dynamic values to `useEffect`:
```tsx
const [mounted, setMounted] = useState(false)
useEffect(() => setMounted(true), [])
if (!mounted) return null
```

### "Unhandled Runtime Error" — Cannot read property of null/undefined
**Symptom:** Page crashes with "Cannot read properties of undefined"
**Cause:** Sanity returned empty data, code didn't handle it
**Fix:** Add optional chaining and fallbacks:
```tsx
// Instead of:
<h1>{hero.headline}</h1>

// Use:
<h1>{hero?.headline ?? 'Welcome'}</h1>
```

---

## GitHub Errors

### "Permission denied (publickey)"
**Symptom:** `git push` fails with this error
**Cause:** SSH key not set up
**Fix (use HTTPS instead):**
```bash
git remote set-url origin https://github.com/yourusername/your-repo.git
git push
```
Then enter your GitHub username and a Personal Access Token (not your password).

### "Updates were rejected because remote contains work"
**Symptom:** `git push` fails with this message
**Cause:** GitHub has changes not in your local copy
**Fix:**
```bash
git pull origin main --rebase
git push origin main
```

### Accidentally Committed .env.local
**This is urgent — revoke your tokens immediately!**
1. Go to each service (Sanity, Vercel, GitHub) and revoke/delete the token
2. Create new tokens
3. Update `.env.local` with new tokens
4. Add to Vercel environment variables
5. Remove from git history:
```bash
git rm --cached .env.local
echo ".env.local" >> .gitignore
git commit -m "Remove .env.local from tracking"
git push
```

---

## CORS Errors

### "Access to fetch at '...' has been blocked by CORS policy"
**What it means:** A security rule is blocking your request
**Common causes and fixes:**

**Cause: Calling an external API directly from the browser**
Fix: Move the API call to a Next.js API Route:
```ts
// src/app/api/my-endpoint/route.ts
export async function GET() {
  const data = await fetch('https://external-api.com/data', {
    headers: { 'Authorization': `Bearer ${process.env.API_TOKEN}` }
  })
  return Response.json(await data.json())
}
```
Then call `/api/my-endpoint` from the frontend instead.

**Cause: WordPress REST API**
Fix: Use Royal MCP or a proxy. Direct WordPress REST API calls from a different domain are blocked.

---

## Image Errors

### Images too large / slow loading
**Fix:** Always use Next.js `<Image>` instead of `<img>`:
```tsx
import Image from 'next/image'

// Next.js auto-optimizes this:
<Image src="/photo.jpg" alt="Photo" width={800} height={600} />
```

### Image doesn't fill its container
```tsx
// For a div that should show the image filling it:
<div className="relative w-full h-64">
  <Image src={url} alt="..." fill className="object-cover" />
</div>
```

---

## Environment Variable Errors

### Variables work locally but not in production
**Checklist:**
- [ ] Variable added to Vercel Dashboard (Settings → Env Vars)
- [ ] Variable name matches exactly (case-sensitive: `NEXT_PUBLIC_` prefix for client-side)
- [ ] Redeployed after adding the variable

### `NEXT_PUBLIC_` vs regular variables
- Variables starting with `NEXT_PUBLIC_` are exposed to the browser (safe for public IDs)
- Variables WITHOUT `NEXT_PUBLIC_` are only available on the server (use for tokens/secrets)
- NEVER put secret tokens in `NEXT_PUBLIC_` variables

---

## TypeScript Errors

### "Property does not exist on type"
**Fix:** Define the type properly or use optional chaining:
```tsx
// Define an interface
interface Project {
  _id: string
  title: string
  description?: string  // optional
  image?: any
}

// Or for Sanity data, use `any` temporarily while building:
const projects: any[] = await getProjects()
```

### "Cannot find module" for images/SVGs
Add to `next-env.d.ts` or create a custom type declaration:
```ts
// src/types/images.d.ts
declare module '*.svg' {
  const content: React.FunctionComponent<React.SVGAttributes<SVGElement>>
  export default content
}
```

---

## RTL / Hebrew Display Issues

### Text appears in wrong direction
```tsx
// Add to root HTML element:
<html dir="rtl" lang="he">

// Or per-section:
<div dir="rtl">Hebrew content</div>
<div dir="ltr">English or code content</div>
```

### Hebrew font not loading
```tsx
// In layout.tsx:
import { Heebo } from 'next/font/google'
const heebo = Heebo({ subsets: ['hebrew', 'latin'] })

<html className={heebo.className}>
```

### Layout flipped unexpectedly
In RTL, `flex-row` items appear in reverse order visually. Options:
```tsx
// Reverse back to expected visual order:
<div className="flex flex-row-reverse">

// Or use logical properties (RTL-aware):
// Instead of: ml-4, mr-4, pl-4, pr-4
// Use: ms-4 (margin-start), me-4 (margin-end), ps-4, pe-4
```

---

## WordPress Issues

### WordPress REST API blocked (CORS)
**Never call WordPress REST API directly from a Next.js frontend hosted on a different domain.**
Use Royal MCP instead — it acts as an authenticated proxy.

Royal MCP call pattern:
```js
// 1. Initialize session
const initRes = await fetch('https://yoursite.com/wp-json/royal-mcp/v1/mcp', {
  method: 'POST',
  headers: { 'Authorization': 'Bearer YOUR_TOKEN', 'Content-Type': 'application/json' },
  body: JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'initialize', params: {} })
})
const sessionId = initRes.headers.get('Mcp-Session-Id')

// 2. Use session for subsequent calls
const res = await fetch('https://yoursite.com/wp-json/royal-mcp/v1/mcp', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Mcp-Session-Id': sessionId,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ jsonrpc: '2.0', id: 2, method: 'tools/call', params: { name: 'get_posts', arguments: {} } })
})
```

### Inline Styles Stripped in WordPress
**WordPress strips `<style>` tags from post content.** Always use inline styles:
```html
<!-- Wrong: -->
<style>.my-class { color: red; }</style>
<p class="my-class">text</p>

<!-- Right: -->
<p style="color: red;">text</p>
```

### WordPress Post Not Showing / 404
1. Go to WordPress Admin → Settings → Permalinks
2. Click "Save Changes" (even without changing anything — this flushes rewrite rules)

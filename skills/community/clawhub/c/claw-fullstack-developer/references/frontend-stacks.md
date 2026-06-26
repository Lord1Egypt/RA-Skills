# Frontend Stacks

Patterns and defaults for the major modern frontend frameworks. Pick one based on project needs; don't mix frameworks in a single app.

## Choosing a frontend

| If you need... | Pick |
|---|---|
| SEO, server rendering, file-based routing, same-repo backend | **Next.js (App Router)** |
| Rich SPA with no SSR needs, fastest dev loop | **React + Vite** |
| Vue ecosystem preference or Nuxt-style SSR | **Nuxt 3** |
| Smallest bundle, simplest mental model, server/client merged | **SvelteKit** |
| Desktop-app feel with React | React + Vite + Electron or Tauri |
| Content-heavy marketing site with occasional interactivity | **Astro** (ships zero JS by default) |

If the user has no preference and you're not sure, **default to Next.js App Router with TypeScript and Tailwind**. It's the broadest-utility choice and has strong defaults for routing, data fetching, and deployment.

## Universal frontend principles

Regardless of framework:

- **TypeScript by default.** The refactor safety and editor tooling pay for themselves within a week on any non-trivial project.
- **Use a component library as a base layer.** [shadcn/ui](https://ui.shadcn.com) for React (copies components into your repo — you own them), Radix UI primitives, or Headless UI. Don't build buttons, dropdowns, and modals from scratch.
- **Tailwind CSS** for styling unless the user insists otherwise. Avoid the 2015-era "CSS-in-JS" libraries (styled-components, emotion) on new projects — they're slower and the ecosystem has largely moved on.
- **Forms**: React Hook Form + Zod (React) or VeeValidate + Zod (Vue). Never roll your own validation on forms with >3 fields.
- **Server state**: TanStack Query (React) / Vue Query / SvelteKit's built-in loaders. This is what you want for fetching, caching, and syncing with the server. Don't reach for Redux or global state unless you actually need cross-component shared state that isn't server data.
- **Client state**: prefer component state and URL params. Reach for Zustand / Pinia / Svelte stores only when state genuinely needs to be shared across the component tree.
- **Accessibility from day one**: semantic HTML, keyboard navigation, alt text, focus management on route changes and modals. Running axe or Lighthouse takes 30 seconds.
- **Image handling**: use the framework's Image component (Next's `<Image>`, Nuxt's `<NuxtImg>`). It handles lazy loading, responsive sizes, and format conversion for free.

## Next.js (App Router) — recommended default

### Directory structure
```
app/
  (marketing)/              # route group — doesn't affect URL
    page.tsx                # homepage
    pricing/page.tsx
  (app)/
    layout.tsx              # shared app shell (requires auth)
    dashboard/page.tsx
    settings/page.tsx
  api/
    users/route.ts          # route handler
    webhooks/stripe/route.ts
  layout.tsx                # root layout
  globals.css
components/
  ui/                       # shadcn/ui components live here
  forms/
  layouts/
lib/
  db.ts                     # database client singleton
  auth.ts                   # auth helpers
  validations/              # Zod schemas
server/
  actions/                  # server actions
  services/                 # business logic (pure, testable)
types/
```

### Data fetching patterns
- **Server components by default.** Fetch directly from the DB in a server component — no API round-trip needed for first render. Use `async` server components and `await`.
- **Client components (`"use client"`) only when needed**: interactivity, hooks, browser APIs. Keep these leaves small.
- **Mutations**: Server Actions for form posts. For interactive updates, a route handler + TanStack Query on the client.
- **Caching**: understand `fetch` cache options, `revalidatePath`, `revalidateTag`. Caching bugs are the #1 source of "why does my Next.js app show stale data" questions — be explicit.

### Auth pattern
Auth.js (formerly NextAuth) or Clerk. Both handle session, OAuth providers, and middleware-based route protection.

### What to avoid in Next.js
- Don't put sensitive server logic in client components. If you see `"use client"` at the top of a file that touches the DB, that's a bug.
- Don't `useEffect` to fetch data you could fetch on the server. It causes layout shift and worse SEO.
- Don't put the database client inside a request handler — instantiate it once in `lib/db.ts` and import it. (In dev, guard against Hot Module Reload re-instantiation.)

## React + Vite (SPA)

When you genuinely don't need SSR — internal tools, authenticated-only dashboards, PWAs.

### Directory structure
```
src/
  pages/             # or routes/
  components/
  lib/
  hooks/
  services/          # API clients
  types/
  main.tsx
  App.tsx
```

### Routing
React Router v6+ is the default. TanStack Router is a strong alternative with type-safe routes.

### Data fetching
TanStack Query. Always.

### API client
A single `lib/api.ts` that wraps `fetch` with base URL, auth headers, and error handling. Don't scatter `fetch` calls across 40 components.

## Nuxt 3 (Vue)

### Directory structure
Nuxt has strong conventions — use them:
```
pages/               # file-based routing
components/          # auto-imported
composables/         # auto-imported hooks
server/api/          # API routes
server/utils/
middleware/          # route middleware
plugins/
```

### Data fetching
`useFetch` / `useAsyncData` for SSR-aware fetching. Pinia for shared client state.

## SvelteKit

### Directory structure
```
src/
  routes/
    +page.svelte
    +page.server.ts      # server-only load
    api/
      users/+server.ts
  lib/
    components/
    server/              # server-only code
```

### Data fetching
`+page.server.ts` `load` functions for server-side data. Form actions for mutations — simpler than REST for most form posts.

## State management — decision tree

1. Is this data from the server? → Use TanStack Query / Nuxt's useFetch / SvelteKit loaders. **Stop.**
2. Does this state belong in the URL (filters, pagination, selected tab)? → URL params. **Stop.**
3. Is this local to one component? → `useState` / `ref`. **Stop.**
4. Is this shared across a small subtree? → Context / provide-inject. **Stop.**
5. Truly global, app-wide, non-server client state? → Zustand / Pinia / Svelte store.

Most apps never need step 5.

## Build, bundle, lint

- **ESLint** with the framework's recommended config, plus `eslint-plugin-tailwindcss` if using Tailwind.
- **Prettier** for formatting. Integrate with your editor so it runs on save.
- **Type-check in CI**: `tsc --noEmit` as a CI step. Don't let type errors accumulate.
- **Bundle analysis**: run it before you ship. Next.js has `@next/bundle-analyzer`; Vite has `rollup-plugin-visualizer`. If your entry bundle is >500 KB gzipped, investigate.

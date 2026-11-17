---
name: fec-nextjs-project-standard
description: Use when creating or reviewing Next.js 14+ App Router projects, file routes, layouts, server/client component boundaries, SSR/SSG/ISR, streaming, metadata, middleware, server actions, or Next-specific data fetching. For generic client React component architecture, apply the project's React conventions separately; Chinese triggers include Next.js, App Router.
---

# Next.js project specifications

For repositories using Next.js 14+ with App Router.

## Purpose

Standardize engineering practices for App Router, SSR/SSG/ISR rendering modes, data acquisition, route layout, middleware and SEO metadata in Next.js 14+ projects to ensure server-side priority, performance optimization and maintainability.

## Procedure

1. First identify whether the target belongs to App Router, layout, server data, middleware, metadata or client interaction.
2. Default server-side components take precedence; use `'use client'` only when browser API, interactive state or event handling is required.
3. Clarify SSR / SSG / ISR / CSR rendering mode and Next fetch/cache strategy.
4. Complete the server-side boundaries of `loading.tsx`, `error.tsx`, `not-found.tsx`, metadata and sensitive logic for routing.
5. Check whether Server Component is supported before introducing third-party libraries; browser-specific, animation, chart, editor and WebGL libraries must be placed into client leaf components and loaded on demand.
6. Prioritize evidence review for dynamic rendering, cache invalidation, RSC serialization, route handler, middleware, and first-screen bundles; first collect build, trace, headers, or routing behavior evidence when unsure.
7. Client component architecture issues are offloaded to the React project workflow.

## Project structure

```
src/
├── app/                        # App Router
│ ├── layout.tsx # Root layout
│ ├── page.tsx # Home page
│ ├── loading.tsx # Global loading UI
│ ├── error.tsx # Global error boundary
│   ├── not-found.tsx           # 404
│   ├── globals.css
│   │
│ ├── (auth)/ # Routing group
│   │   ├── login/
│   │   │   └── page.tsx
│   │   └── register/
│   │       └── page.tsx
│   │
│ ├── (dashboard)/ # Dashboard routing group
│ │ ├── layout.tsx # Shared layout
│   │   ├── dashboard/
│   │   │   └── page.tsx
│   │   └── users/
│   │       ├── page.tsx
│   │       └── [id]/
│   │           └── page.tsx
│   │
│   └── api/                    # API Routes
│       └── users/
│           └── route.ts
│
├── components/ # Shared components
├── lib/ # Tools, configuration
├── hooks/
├── services/
└── types/
```

## Rendering mode

| Patterns | Usage scenarios | Implementation methods |
| ------- | ---------------- | ----------------------------------------------- |
| **SSR** | Dynamic, real-time data required | Default, `fetch` does not cache or `cache: 'no-store'` |
| **SSG** | Static content | `generateStaticParams` + static `fetch` |
| **ISR** | Periodically updated | `revalidate` or `revalidatePath` |
| **CSR** | Client interaction | `'use client'` + `useEffect` or SWR/React Query |

## Data acquisition

- Server component: directly `async` or `fetch`, without exposing `useEffect`
- Client component: `useEffect` + `useState`, or SWR / React Query
- Prioritize data acquisition on the server side to reduce hydration on the client side
- Use `loading.tsx` and Suspense to wrap asynchronous blocks to provide streaming experience
- The cache policy must include `force-cache`, `no-store`, `revalidate`, tag/path revalidation or user private data constraints
- Any read that will change the route from static to dynamic (cookies, headers, searchParams, uncached fetch) must explain the reason and verification method

## Routing and layout

- Routing group `(auth)` does not change the URL, only affects the layout
- Dynamic routing `[id]` cooperates with `generateStaticParams` to do SSG
- `layout.tsx` wraps sub-routes to share UI and layout
- `page.tsx` is a leaf route and cannot be nested

## Middleware

- Place it in the root directory of `middleware.ts`
- Used for authentication, redirection, rewrite, and Header modification
- Keep it as short as possible to avoid blocking requests

## Metadata and SEO

- Export using `metadata` or `generateMetadata`
- Supports `title`, `description`, `openGraph`, `twitter`, etc.
- Dynamic routes are generated using `generateMetadata(params)`

## Constraints

- Server component defaults, add `'use client'` only when client interaction is required.
- Do not use `useState`, `useEffect`, and browser API directly in server components
- Sensitive logic (such as authentication) is placed on the server or API Route and is not exposed to the client
- Use `next/image` for images and `next/font` for fonts
- Do not put keys, internal API addresses or server tokens in the `NEXT_PUBLIC_` environment variable.
- Don't let large animation libraries, 3D scenes, rich text editors or map SDKs go into the root layout sync bundle.
- The first screen media must have a certain size, real resources and reasonable priority; do not use remote placeholder images to support the layout.
- Don't assert that a route is "cached" or "must be dynamic" without evidence of metrics, response headers, build output, or route behavior.
- Middleware only handles lightweight decision-making at the routing level and does not carry heavy authentication queries, log batch processing, or business logic that can be placed in the route handler.

## Division of labor with client UI mode

- **Server**: Rendering mode, data acquisition and caching, `loading.tsx` / `error.tsx`, routing and layout, etc. are subject to this skill.
- **`'use client'` component**: combined and composite components, forms, client state, list virtualization, animation and keyboard/focus, etc., consistent with pure React projects, following the React rules in the project (such as `.claude/rules/fec-react.md`).
- **Permissions and client data**: Authentication, RBAC, redirect, client server state, and cache failure should be handled according to the corresponding special workflow; Next server fetch/cache is still subject to this skill.

## Expected Output

- Page components are organized according to App Router conventions (`app/` directory, `page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`)
- The rendering mode is selected correctly (SSR/SSG/ISR/CSR) and the data acquisition path is clear
- Complete metadata and SEO configuration (title, description, openGraph)
- Sensitive logic is on the server side, client components only handle interactions
- There is reviewable evidence for caching, dynamic rendering and above-the-fold bundle decisions, and performance risks can be offloaded to dedicated performance workflows

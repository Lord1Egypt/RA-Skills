---
name: fec-nuxt-project-standard
description: Use when creating or reviewing Nuxt 3 projects, file routes, pages, layouts, SSR/SSG/SPA behavior, Nuxt data fetching, route middleware, plugins, modules, server routes, or Nuxt-specific Vue 3 conventions. For generic Vue component architecture, apply the project's Vue conventions separately; Chinese triggers include Nuxt, Nuxt 3.
---

# Nuxt 3 Project Specifications

For repositories using Nuxt 3 + Vue 3 + TypeScript.

## Purpose

Standardize the engineering practices of SSR/SSG rendering mode, combined API, automatic import, data acquisition, routing middleware and module plug-ins in the Nuxt 3 project to ensure conventional development and type safety.

## Procedure

1. First identify whether the target belongs to Nuxt pages/layouts, rendering mode, data acquisition, route middleware, plugin/module or server route.
2. Clarify SSR / SSG / SPA selection to avoid server-side executable code relying on `window` or `document`.
3. For data acquisition, Nuxt’s `useFetch` / `useAsyncData` is used first, and the hydration consistency is checked.
4. Route authentication, redirection and permission issues are aligned with the route protection workflow.
5. Common Vue component architecture issues are offloaded to the Vue project workflow.

## Project structure

```
├── app.vue # Root component
├── nuxt.config.ts # Nuxt configuration
│
├── pages/ # File-based routing
│   ├── index.vue               # /
│   ├── login.vue               # /login
│   ├── dashboard/
│   │   ├── index.vue           # /dashboard
│   │   └── users/
│   │       ├── index.vue       # /dashboard/users
│   │       └── [id].vue       # /dashboard/users/:id
│ └── [...slug].vue # Capture all
│
├── layouts/ # layout
│   ├── default.vue
│   └── auth.vue
│
├── components/ # Automatically import components
│   ├── Button/
│   │   └── Button.vue
│   └── AppHeader.vue
│
├── composables/ # Combined functions (automatically imported)
│   ├── useAuth.ts
│   └── useFetch.ts
│
├── server/ # Server API
│ ├── api/ # API routing
│   │   └── users/
│   │       └── index.get.ts
│ ├── middleware/ # Server-side middleware
│ └── utils/ # Server-side tools
│
├── plugins/ # Plug-in
│   └── i18n.client.ts
│
├── middleware/ # Routing middleware
│   └── auth.ts
│
├── public/ # Static resources
├── assets/ # Resources to be built
└── types/ # Type definition
```

## Rendering mode

| Mode | Configuration | Description |
| ------- | --------------- | -------------- |
| **SSR** | Default | `ssr: true` |
| **SSG** | `nuxt generate` | Pre-render all pages |
| **SPA** | `ssr: false` | Pure client-side rendering |

```ts
// nuxt.config.ts
export default defineNuxtConfig({
  ssr: true, // or false
});
```

## Data acquisition

- `useFetch` / `useAsyncData`: server + client, automatic deduplication
- `$fetch`: direct request, suitable for server or one-time call
- `useLazyAsyncData`: does not block navigation, suitable for non-first screen
- Avoid mixing synchronous/asynchronous logic at the top level of `setup` causing hydration mismatch

## Routing and layout

- Automatically generate routes for files under `pages/`
- Dynamic routing: `[id].vue`, `[...slug].vue`
- Layout: `layout` option or `layouts/default.vue` default
- Nested routing: `pages/parent/child.vue` needs to be combined with `NuxtPage`

## Middleware

- Automatically register files under `middleware/`
- Page level: `definePageMeta({ middleware: ['auth'] })`
- Global: `router.middleware` of `nuxt.config.ts`
- Server-side middleware: `server/middleware/`

## Plug-ins and modules

- Plug-in: `plugins/*.ts`, supports `.client`, `.server` suffixes
- Modules: `modules/` or `node_modules`, in `nuxt.config` `modules: []`

## Constraints

- Server-accessible code should not rely on `window` or `document`
- Be careful about SSR serialization when using `useState` to share state
- Use `NuxtImg` for images and `NuxtLink` for links
- Avoid using `await` at the top level of `setup` which will cause blocking. Use `useAsyncData` / `useFetch` first

## Expected Output

- Pages are organized according to `pages/` conventional routing, and dynamic routing is correctly configured
- The rendering mode (SSR/SSG/SPA) is correctly selected and the `nuxt.config.ts` configuration is clear
- Data acquisition uses `useFetch` / `useAsyncData`, automatic deduplication and hydration
- Composables and components are automatically imported correctly, and the server/client boundary is clear

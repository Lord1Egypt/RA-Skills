# Framework Adapters

Read only the section matching the detected stack. Preserve local conventions when they conflict with these generic defaults.

## React, Next.js, and Remix

- Respect server/client boundaries and existing route conventions.
- Keep server data, URL state, remote cache state, and transient component state distinct.
- Reuse the installed query, form, schema, and UI libraries.
- Test user-visible behavior with Testing Library and route-critical flows with Playwright.
- In Next.js, verify loading, error, not-found, metadata, image/font behavior, and hydration warnings.

## Vue and Nuxt

- Follow Composition API, composable, Pinia, and file-routing conventions already present.
- Keep reactive derivations computed rather than mirrored through watchers.
- In Nuxt, verify server rendering, hydration, route middleware, pending/error states, and asset handling.
- Use Vue Testing Library or the repository's current component harness plus Playwright for critical flows.

## Svelte and SvelteKit

- Prefer local reactive state and existing stores; avoid adding a global store for route-local state.
- Keep load/action contracts aligned with generated route types.
- Verify SSR, form enhancement, invalidation, navigation focus, loading, and error boundaries.

## Angular

- Follow standalone/module, signals/RxJS, forms, routing, and dependency-injection conventions already selected by the project.
- Preserve OnPush and immutable update assumptions where present.
- Test semantic component behavior and router-integrated flows, not implementation internals.

## Static HTML and Progressive Enhancement

- Use semantic HTML as the primary contract and keep the core task usable without unnecessary JavaScript.
- Use CSS custom properties for tokens and small modules for behavior.
- Serve over HTTP when validating routes, modules, fetches, service workers, or strict browser security behavior.

## Mobile Web and Embedded WebViews

- Include safe areas, virtual keyboard behavior, touch targets, scroll ownership, orientation, back navigation, reduced resources, and host bridge failure states.
- Test on a narrow viewport and, when available, the actual host shell. Browser emulation does not validate every WebView behavior.

## Framework-Neutral Adapter Contract

Regardless of stack, map the approved contract onto:

```text
route -> page/screen owner
design tokens -> theme source
interaction state -> local/form/state-machine owner
remote data -> client/cache/server owner
data contract -> schema/generated types
flows -> component/integration/browser tests
visual baselines -> stable fixture route
quality commands -> package scripts and CI
```

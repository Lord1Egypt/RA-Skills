#Framework-specific performance diagnostic mode

This reference is used for special positioning after entering the performance optimization process. Establish goals, baselines, and candidate gates first, then read corresponding categories by framework; don't jump directly from these lists to conclusions.

## React / Client React

- **Waterfall**: Whether independent requests, permission checks, feature flags, or subcomponent data are waited for serially. Confirm dependencies using Network waterfall, React Profiler, or user path logs.
- **Bundle**: Whether to simultaneously introduce charts, editors, maps, 3D, full icons, heavy date libraries or barrel exports on the first screen. Locate chunks using build products, source maps, or bundle analyzers.
- **Rerender**: Whether the Context is too wide, whether the selector is too thick, whether the default object/array props are created every time, and whether expensive derivation is executed repeatedly in the hot path. Use React Profiler or reproducible interactive proofs.
- **Effect**: Whether to use effect to save data that can be directly deduced, whether to put interaction logic into effect, whether to lack cancellation, cleanup or stable dependencies. Confirm with render count, request count, or memory/subscription evidence.
- **Lazy boundary**: Whether Suspense, dynamic import, error fallback, loading/empty/error status appear in pairs, whether lazy loading destroys focus or first screen layout stability.

## Vue 3 / Nuxt Client

- **Reactive payload size**: Whether large objects, tabular data, or third-party instances are deeply reactively proxied. Use component updates, memory snapshots, or evidence of long tasks to determine whether shallow reactive or immutable boundaries are needed.
- **Computed/watch**: Whether the computed derived value is manually synchronized with a wide range watcher, whether the watch monitors wide objects, and whether the asynchronous watch lacks cancellation and race handling.
- **Template hot path**: Mixed `v-if` in `v-for`, inline recalculation, missing stable `:key`, or rendering non-viewport nodes in a large list.
- **Async component boundary**: Whether heavy-duty components use asynchronous components or route-level dynamic import, whether the loading state is stable, and whether the error state is recoverable.
- **Store fan-out**: Whether the Pinia store spreads high-frequency UI temporary state to a wide range of subscribers, or copies the server cache to the global store.

## Next.js

- **Dynamic route drift**: Whether cookies, headers, searchParams or uncached fetch make static routes dynamic. Confirm with build output, response headers, or route behavior.
- **RSC serialization**: Whether the Server Component passes too large props, duplicate data or unserializable structures to the Client Component.
- **Fetch/cache policy**: Whether `force-cache`, `no-store`, `revalidate`, tag/path revalidation match the data privacy and update frequency.
- **Client boundary leakage**: Whether the root layout or high-level client boundary is synchronized with heavy browser libraries, providers or unnecessary state.
- **Middleware cost**: Whether the middleware carries heavy queries, log batch processing, or business logic that can be placed in the route handler.

## Nuxt 3

- **Rendering mode mismatch**: Whether the page should be SSR, SSG, ISR/route rules or SPA, and whether the actual behavior is consistent with the deployment target.
- **Data duplication**: `useFetch` / `useAsyncData` Whether the request is repeated, whether the key is stable, whether the client hydration repeatedly pulls the same data.
- **Route middleware cost**: Whether the routing middleware does heavy asynchronous work, repeated authentication requests or non-cacheable global blocking logic.
- **Client-only islands**: Whether charts, editors, maps or WebGL that run only in the browser are isolated to client-only or async boundaries.

## Output requirements

Each framework-specific proposal must be written clearly: source of evidence, affected routes/components/chunks/requests, recommended changes, verification commands and possible impact on loading, error, empty, offline, reduced-motion or mobile status.

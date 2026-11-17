# Review checklist

Use this checklist when reviewing Effector ecosystem code. Use `effector-fsd` for project-structure and import-boundary review.

## Contents

- [Effector](#effector)
- [Farfetched/contracts](#farfetchedcontracts)
- [React](#react)
- [Routing/forms/persistence/i18n](#routingformspersistencei18n)
- [Packages/tooling](#packagestooling)
- [Red flags](#red-flags)
- [Production audit addendum](#production-audit-addendum)

## Effector

- Are units created statically at module level?
- Is business logic outside React components?
- Is `sample` used for data flow?
- Is `sample.fn` pure?
- Is `watch` absent from business logic?
- Is `$store.getState()` absent from production logic?
- Is `attach` used instead of reading stores inside effects when needed?
- Are stores atomic enough?
- Are non-trivial transformations extracted from `combine`, `sample.fn`, and store `.map` into named pure functions?
- Are DTO mapping, domain calculations, and UI-only formatting placed at the right ownership boundary?
- Are derived stores not used as targets?
- Are reducers not accidentally returning `undefined`?
- Is complex branching readable (`sample`/`split`/`effector-action`)?
- Are events named as facts?
- Is large model logic split into responsibility-based submodels?
- Is the top-level model mostly orchestration between submodels through `sample`/declarative connections?
- Is repeated same-shaped model code extracted to factories instead of copy-pasted?
- Are factories invoked only at module top level?
- Is app/page startup represented by explicit events such as `appStarted`/`pageStarted`?
- Is scoped startup executed through `allSettled(event, { scope, params })` instead of hidden helper chains?
- If startup helpers such as `startRouter(scope)` exist, has the reviewer first tried to move them into effects started from `appStarted`?
- If a free-floating startup helper remains, is it a documented last-resort host adapter boundary rather than business workflow?
- Are external callbacks registered with `scopeBind` or scope-aware adapters?

## Farfetched/contracts

- Are remote operations Farfetched queries/mutations?
- Are responses validated with contracts?
- Is DTO mapping isolated in `mapData` or domain lib?
- Are errors normalized before UI consumes them?
- Is query/mutation ownership clear and placed near the correct operation/domain boundary?
- Is concurrency strategy intentional and applied through the operator?
- For submits, is duplicate-click protection an explicit `$pending` gate in the feature/page model, unless `TAKE_FIRST` is justified and tested?
- Is `.refresh`, `keepFresh`, cache, or update strategy correct?
- If `keepFresh` is used, has the query been started at least once with valid params?
- Is `request.fetch.credentials` used for cookie/session APIs in current Farfetched code?
- Are `GET`/`HEAD` requests free of `body`?
- Is `abortAll`/route-close cancellation considered for route/search requests?
- Is blind optimistic update avoided for server-sorted/filtered data?
- Is auth refresh centralized through `createBarrier`/`applyBarrier` or shared API logic?
- Are shared barriers free of UI/router redirects?
- Is `@farfetched/atomic-router` used where a query is truly the route loader, and are route params mapped outside React?

## React

- Does connected UI use `useUnit`?
- Is there one `useUnit` object/array shape per connected component by default?
- Are all returned values destructured and used intentionally?
- Do handler-like values returned from `useUnit` use `on*` aliases, such as `onSubmit`, instead of event fact names such as `submitted`?
- Are raw events/effects not passed to DOM handlers or ordinary callback props?
- Is component splitting used when subscription granularity matters?
- Does UI only render and send events?
- Are units/factories absent from render/hooks?

## Routing/forms/persistence/i18n

- Is route orchestration in model, not component effects?
- Are route params typed?
- Are protected routes handled by `chainRoute`/route models rather than JSX-only wrappers?
- Are Farfetched route loaders using `startChain`/`freshChain` deliberately?
- Are forms owned by feature/page models?
- Are submit flows connected by `sample`?
- Are persisted values safe and validated with contracts?
- Is `pickup` explicit when Scope/SSR is used?
- Are translated strings not stored in domain stores?
- Are browser API listeners centralized through adapters/integrations?

## Packages/tooling

- Is each package justified by purpose?
- Is there duplicated custom logic that Patronum/Farfetched already solves?
- Are Effector ESLint presets enabled?
- Are Scope-specific lint rules enabled when Scope is used?
- Are factory/SID requirements handled by Babel/SWC plugin, including the `factories` field for SSR?
- Is `@effector/next` used for Next.js SSR/hydration instead of custom ad-hoc glue?
- Is a fresh Scope created per Next.js request/page computation?
- Is `serialize(scope)` passed to `EffectorNext` and are SIDs stable?
- Are Client Components marked with `'use client'` when using Effector React hooks?
- Is Next router navigation isolated in an adapter model?

## Red flags

- `src/api/users.ts` with business endpoint soup
- `src/store/index.ts` global model with all domains
- one model owning form, filters, list loading, selection, dialogs, and actions at once
- `watch` triggering effects
- `getState` inside effects
- `fetch` in React components
- contracts missing from backend responses
- multiple `useUnit` calls in one connected component without a render-granularity reason
- raw event/effect calls from React components
- persistence without validation/pickup in scoped apps
- global server Scope in Next.js
- route/page data loading from React `useEffect` instead of route/page model
- `keepFresh` trigger without first query start
- Farfetched top-level `credentials` in new code
- shared API barrier that directly opens login routes

## Production audit addendum

Use this addendum for full-project audits. These checks are mandatory even when the local code style looks good.

### Startup/auth/routing graph

- Does router/history installation wait for session restore, or does protected routing explicitly model `unknown` auth state?
- Can an initial protected route be opened and redirected before current-session restore finishes?
- Does async protected-route logic preserve original params/query after restore?
- Does `sessionCleared`, logout success, or current-session failure redirect/close protected routes that are already opened?
- Are layout-level `return null` auth fallbacks backed by routing model redirects, rather than used as the only auth policy?

### Unauthorized handling graph

- Are `401`/`403` errors only normalized, or do they produce session facts such as `sessionCleared`?
- Are all auth-sensitive queries/mutations included in an app-level unauthorized/barrier policy?
- Are auth barriers free of navigation, with redirects owned by app/page routes?
- Does logout/session clear abort or invalidate auth-sensitive in-flight operations when stale responses matter?

### Remote operation graph

- List every `query.start`, `query.refresh`, mutation `.start`, route loader, `keepFresh`, `cache`, and `update` connection.
- Can the same query be started by layout and page on the same route open?
- Is every `TAKE_EVERY` intentional rather than copied as a universal default?
- Are quickly changing route/filter/search queries using `TAKE_LATEST`, cancellation, cache, or explicit dedupe?
- Are submit mutations protected by an explicit `$pending` gate or a tested concurrency strategy?
- Are page-local refetch reactions gated by route `$isOpened`?

### Scope/lifecycle graph

- Are timers/listeners/SDK callbacks installed from scoped effects or explicit app/page lifecycle events?
- Are external callbacks wrapped in `scopeBind` or a scope-aware adapter?
- Are resource handles (`intervalId`, unsubscribe functions, sockets) stored per Scope or lifecycle instance, not as unguarded module-level singletons?
- Is `appDestroyed`/route close/HMR cleanup declared and actually called?

### Reactive correctness graph

- Can `sample.fn`, `combine`, store `.map`, or reducers throw because of date parsing, JSON parsing, URL parsing, missing nested data, or invalid casts?
- Do validation failures become modeled events/stores before mutation start?
- When handling `operation.finished.success`, does the model use `clock.result` instead of reading the operation `$data` store unnecessarily?
- Are large VM stores split when a frequent source such as a global clock would recompute heavy lists?

### React boundary graph

- Does any callback prop expect `Promise` while the caller passes an Effector event/effect-bound callback with different completion semantics?
- Is local React pending state duplicating Farfetched `$pending`?
- Are confirm/dialog workflows modeled as feature/page state instead of awaiting an Effector event in the component?

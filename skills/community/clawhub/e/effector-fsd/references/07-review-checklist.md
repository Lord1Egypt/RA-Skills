# FSD + Effector review checklist

Use this checklist when reviewing project structure.

## Contents

- [Layers and slices](#layers-and-slices)
- [Public APIs](#public-apis)
- [Shared](#shared)
- [Entities](#entities)
- [Features](#features)
- [Pages and widgets](#pages-and-widgets)
- [Effector model structure](#effector-model-structure)
- [Farfetched](#farfetched)
- [Routing and Next.js](#routing-and-nextjs)
- [Tooling](#tooling)
- [Full audit addendum for Effector projects](#full-audit-addendum-for-effector-projects)

## Layers and slices

- Are layers used only when they add value?
- Are imports only downward by layer?
- Are same-layer cross-imports absent, except documented `@x` entity APIs?
- Are `app` and `shared` sliceless?
- Is `processes` absent?
- Are slice names business/product-oriented?
- Are there no technical slices such as `features/set-search`, `features/open-modal`, `entities/api`?

## Public APIs

- Does each slice expose `index.ts`?
- Do external imports go through slice public APIs?
- Are there no layer-level barrels like `entities/index.ts`?
- Are wildcard exports avoided unless intentionally stable and tiny?
- Are server-only and client-safe exports separated in Next.js where needed?
- Are internal model/api/ui files hidden from consumers?

## Shared

- Is `shared` free of business domain types, stores, contracts, queries, and UI?
- Are `shared/api` files generic transport only?
- Does `shared/api` avoid importing `entities`, `features`, `pages`, `widgets`, or `app`?
- Does `shared/ui` avoid domain-specific props and business branches?
- Is `shared/lib` grouped by purpose and documented when it grows?

## Entities

- Are entity slices real business/domain concepts?
- Do entities avoid importing features/pages/widgets/app?
- Are entity contracts/mappers colocated with the entity?
- Are entity visuals free of action/page orchestration?
- Are entity-to-entity relationships handled with `@x` only when justified?

## Features

- Does each feature represent a user action or business capability?
- Are action forms/mutations/validation inside the owning feature?
- Are features not used as dumping grounds for technical UI state?
- Do features import only entities and shared?
- Does submit de-duplication live in the feature/page model, not in UI?

## Pages and widgets

- Does each page own route/screen orchestration?
- Are route params, page filters, sorting, pagination, and page-only queries in page model/API?
- Are widgets used only for large reusable/independent blocks?
- Are one-page blocks kept inside the page instead of over-abstracted into widgets?

## Effector model structure

- Are models split by responsibility, not `stores/events/effects` buckets?
- Are public `$$model` shapes exposed only when useful?
- Are factories defined and instantiated at correct ownership boundaries?
- Is `appStarted` in `app/model` and page startup in page model?
- Are integration effects connected from startup events instead of free-floating helper chains?

## Farfetched

- Are reusable entity reads in `entities/<entity>/api`?
- Are action mutations in `features/<action>/api`?
- Are page-only reads in `pages/<page>/api`?
- Are contracts owned by the domain/action/page they validate?
- Is there no global `shared/contracts` business dump?
- Are session-aware barriers outside `shared`?
- If a barrier is applied to many operations, is that composition in `app`?
- Are route loaders placed in page route/model files?

## Routing and Next.js

- Is Atomic Router config in `app/routes`?
- Are protected route compositions in `app/routes` or page routes?
- Are redirects absent from shared API code?
- Are framework routes thin adapters to FSD pages/models?
- In Next.js, are FSD `app`/`pages` renamed to `_app`/`_pages` or otherwise clearly separated?
- Are server-only public APIs separated with `index.server.ts` when needed?

## Tooling

- Is Steiger configured when the team wants automated FSD enforcement?
- Are exceptions documented near config or architecture decision records?
- Are disabled Steiger rules temporary and justified?
- Is ESLint also enforcing Effector-specific rules via `eslint-plugin-effector`?

## Full audit addendum for Effector projects

Run these checks in addition to normal FSD import/layer checks.

### Effector static graph ownership

- Do page models listen to feature/entity mutation successes while the page route may be closed?
- Are such page reactions gated by `route.$isOpened`, or moved to an app/entity invalidation owner?
- Does `app` own global startup, auth error handling, auth redirects, barrier application, and cross-slice invalidation?
- Are cross-cutting samples that import many entities/features absent from `features`, `entities`, and `shared`?

### Public API width

- Do features export semantic facts/facades (`itemCreated`, `$$itemCreate`) rather than forcing consumers to listen to raw `mutation.finished.success`?
- Are raw Farfetched operations exported only when they are the intended stable public contract?
- Are internal dialog/form stores hidden unless they are part of the stable feature facade?
- Are wildcard exports reviewed for accidental implementation leaks?

### API/contract ownership

- Are page APIs truly page-specific, or are they reusable domain resources that belong in `entities`?
- Are page mutations truly page-only, or are they user actions that belong in `features`?
- Are contracts exported from pages only when they describe page-only data?
- Are settings/session/user/order/link-like resources owned by entities rather than pages?

### Shared purity and auth adapters

- Does `shared/api` stay generic and avoid importing session/routes/business contracts?
- If `shared/api` contains auth-header adapter state, is it documented as an adapter and synchronized from an allowed owner?
- Are redirects after auth errors in `app/routes`, not in shared transport helpers?

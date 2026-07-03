# Elements Modular Merge Design

## Context

`ELEMENT-SKILL.md` currently contains a standalone `@clink-ai/clink-elements` integration guide. The main `clink-integ-skills` routing only mentions embedded form integration as an optional standard integration frontend path, so users who choose Elements do not get a complete path through backend session creation, frontend SDK wiring, host UI events, webhook reconciliation, and validation artifacts.

The goal is to merge the Elements capability into `clink-integ-skills` without turning it into a separate top-level integration path. Elements is a frontend completion path under standard integration, not an independent payment architecture.

## Mental Model

The Elements module should start by setting the correct integration model:

- Elements is an embedded payment component, not a hosted checkout page.
- The merchant controls page structure, order summary, payment button, promotion-code entry, loading states, and success or failure navigation.
- The SDK controls secure payment input, wallet buttons, 3DS, QRCode, payment method iframe behavior, and payment submission plumbing.
- `paymentMethod` and `currencySelect` can mount into any stable DOM region on the merchant page. They do not need to live inside a dialog.
- Inline checkout, modal or dialog checkout, drawer or side-panel checkout, right-side order cards, and multi-step checkout wizards are all valid host layouts.
- Frontend success or pending events are user-experience signals. Webhook-driven server state remains the payment authority.

## Decision

Use a modular merge:

- keep `SKILL.md` short and route Elements requests through Standard Integration
- move detailed Elements guidance into a new reference module
- extend runtime routing and artifact generation so Elements-specific prompts produce Elements-specific implementation guidance
- add review checks and tests so future changes do not regress this path

Do not paste the full `ELEMENT-SKILL.md` into `SKILL.md`.

## Integration Shape Selection

The Elements module should include a decision table so agents do not default to "build a payment dialog".

| Shape | Use When | Host Responsibilities |
|---|---|---|
| Inline region | Payment should stay directly inside a product, recharge, or order page with low friction | Create session when the user selects the purchasable item, mount Elements into a stable region, keep the order summary visible |
| Modal/Dialog | Payment should appear after a clear purchase intent without disrupting the main page | Create session after `Buy Now`, mount Elements inside the dialog, destroy on close, keep dialog scroll and sizing stable |
| Drawer/Side panel | Checkout is paired with a cart or right-side order summary | Keep summary and payment visible together, handle mobile button placement, avoid covering the payment iframe |
| Multi-step checkout | Merchant must collect account, address, tax, or business inputs before payment | Complete merchant-owned inputs first, then create session and mount `paymentMethod` |
| Headless host UI | Merchant wants full control of order summary, promo code, submit button, and state presentation | Use SDK for secure payment inputs and payment submission while host UI listens to SDK events |

For clinkcoins-like purchase flows, dialog checkout is a valid recipe but should not be the default target. A more Elements-native option is to create the session after product selection and expand an inline or right-side payment area containing `currencySelect` and `paymentMethod`, while the merchant keeps ownership of the order card and uses `amount-change` to calibrate displayed totals.

## Architecture

Add a new module:

- `references/elements-integration.md`

This module should describe the Elements frontend path inside Standard Integration. It should cover:

- prerequisites: merchant backend creates the checkout session first with an Elements-compatible UI mode
- frontend initialization through `loadClinkElements`
- required frontend inputs: `publishKey`, `environment`, and `sessionId`
- safe key boundary: frontend uses publish key only; Secret Key stays server-side
- client-only frontend execution for frameworks such as Next.js, where the host component must run in the browser
- element lifecycle: `createElement('paymentMethod')`, optional `currencySelect`, `mount`, `unmount`, `destroy`
- host UI responsibilities: submit button, amount display, visibility handling, loading state, error display
- event mapping: `submit-enabled`, `submit-visible`, `amount-change`, `session-init-success`, `session-success`, `session-pending`, `promo-code-error`, and `error`
- customization: locale, theme, primary color, radius, currency selector behavior, built-in section visibility
- optional promotion-code UI through `promoCodeChange`
- runtime locale/theme changes through `setLocale` and `setTheme`
- recovery for session expired, completed, unsupported, load failure, and API validation errors
- skeleton strategy: SDK-managed skeleton by default, or host-managed skeleton with `section.hideSkeleton: true` and `session-init-success`
- layout guidance for inline, modal, drawer, and wizard placements
- reconciliation boundary: frontend success events are UX signals; backend webhook and server-side reconciliation remain authoritative

The standard integration module should point to this module from Step 4, where it already discusses merchant frontend payment entry.

## Template Strategy

The Elements implementation guidance should prefer a headless integration layer plus layout recipes instead of one fixed checkout component.

For React, the recommended template shape is:

- `useClinkElementsPayment()`: owns SDK initialization, instance refs, event subscriptions, submit behavior, promotion-code calls, async teardown, and destroy/re-init rules
- layout recipes: inline, modal, drawer, and optional multi-step checkout examples that consume the hook state

The hook should expose a host-friendly interface similar to:

```ts
{
  currencyContainerRef,
  paymentContainerRef,
  amount,
  submitEnabled,
  submitVisible,
  initializing,
  submitting,
  error,
  submit,
  applyPromoCode,
  clearPromoCode,
}
```

This keeps SDK orchestration independent from merchant layout choices. Vue guidance can mirror the same split with a composable plus layout recipes.

The examples should avoid `buttonDisabled` state derived directly from `submit-enabled`. The SDK event means "can submit", so examples should use `submitEnabled` and compute disabled UI as `!submitEnabled || submitting || initializing`.

## Routing

Update `SKILL.md` Standard Integration routing to explicitly recognize Elements terms:

- `@clink-ai/clink-elements`
- `clink-elements`
- `loadClinkElements`
- `createElement`
- `paymentMethod`
- `currencySelect`
- `mount`
- `unmount`
- `submit-enabled`
- `submit-visible`
- `amount-change`
- `session-success`
- `session-pending`
- `promoCodeChange`
- embedded checkout
- iframe payment component

When these signals appear, the skill should still route to Standard Integration, but it should read:

- `references/retrieval-protocol.md`
- `references/standard-integration.md`
- `references/elements-integration.md`

The route should still ask for product mode when checkout session design is needed. For frontend-only implementation requests, it should also ask for or infer the frontend framework when project context is missing.

## Server And Client Boundary

The Elements module should present this as the core flow, not as a footnote:

1. Merchant server uses the Secret Key to create or confirm a local merchant order.
2. Merchant server creates a checkout session for Elements and stores the reconciliation context.
3. Merchant server returns only `sessionId`, `publishKey`, and `environment` or equivalent safe frontend configuration.
4. Merchant client initializes `loadClinkElements` in browser-only code.
5. Merchant client handles SDK events for UX.
6. Merchant server verifies webhooks and performs authoritative order, subscription, refund, and fulfillment synchronization.

Generated guidance must not put Secret Key, server SDK calls, checkout session creation, or merchant order creation logic in browser code.

## Lifecycle Rules

The Elements module should state lifecycle rules in a Stripe Elements-like way:

- one `ClinkElements` instance maps to one checkout session
- when `sessionId` changes, destroy the old instance and call `loadClinkElements()` again
- `destroy()` is irreversible for that instance
- create `paymentMethod` before `currencySelect`
- each element type can be created only once per instance
- React and Vue examples must handle async initialization completing after component unmount
- modal close, route switch, selected product switch, and session recreation must trigger cleanup
- language and theme changes can use `setLocale` and `setTheme` when the same session remains valid; session-changing inputs require re-initialization

## Runtime Artifacts

Extend `lib/skill-runtime.mjs` with Elements signal detection. For Standard Integration prompts that include Elements terms, add Elements-specific artifacts:

- `elements_frontend_checklist`: frontend setup, package/CDN choice, publish key, environment, session ID, mount containers, lifecycle cleanup
- `elements_event_mapping`: host UI mapping for submit state, button visibility, amount display, success, pending, promotion-code error, and generic error
- `elements_error_handling_checklist`: handling for API validation, expired session, completed session, unsupported session UI mode, and load failure
- `elements_host_ui_todo`: implementation tasks for React, Vue, or native JS host pages
- `elements_layout_recipe`: recommended inline, modal, drawer, or multi-step layout pattern for the merchant flow
- `elements_lifecycle_checklist`: session-to-instance mapping, destroy/re-init, async teardown, and route/modal cleanup
- `elements_server_client_boundary`: server-created session, frontend-safe config, and webhook authority boundary

When the prompt mentions promotion codes, add:

- `promotion_code_ui_contract`: states for collapsed, expanded, loading/error, applied, and clear actions using `promoCodeChange`

The normal Standard Integration artifacts remain present because Elements still depends on backend checkout session creation, webhook setup, merchant order mapping, and reconciliation.

## Review Checklist

Add Elements checks to `references/review-checklist.md` under Standard Integration:

- confirms the frontend framework or asks for it before framework-specific code
- confirms backend-created checkout session before frontend initialization
- confirms the checkout session is intended for Elements rather than hosted checkout
- keeps order creation and checkout session creation on the server
- keeps Secret Key and webhook signing key out of frontend code
- ensures Next.js or similar framework examples are browser-only where SDK DOM access is required
- uses `publishKey`, `environment`, and `sessionId` for `loadClinkElements`
- creates `paymentMethod` before `currencySelect`
- does not create duplicate elements from one SDK instance
- calls `destroy()` during component teardown
- destroys and re-initializes when `sessionId` changes
- handles async initialization completing after component unmount
- maps `submit-enabled` as "can submit", not "disabled"
- handles `submit-visible` so host buttons do not conflict with built-in third-party payment buttons
- treats `amount-change` as the source for displayed amount, product, promotion, and tax UI
- treats `session-success` and `session-pending` as frontend UX signals only
- keeps webhook-driven backend state as the authoritative payment confirmation
- handles known SDK errors and gives the user a retry or session recreation path
- documents whether SDK skeleton or host skeleton is used
- checks host containers for stable sizing, scrolling, and mobile button placement

## Host UI Synchronization

The Elements module should include a host UI synchronization guide:

- `amount-change`: update total, currency, product display, discount, tax, and payment button text
- `submit-enabled`: enable or disable payment button, promotion-code input, apply button, and remove button
- `submit-visible`: show or hide the host payment button when wallet or third-party buttons own submission
- `session-success`: close modal, navigate to success UI, or refresh order state while waiting for server confirmation where needed
- `session-pending`: show pending state and avoid treating it as payment success
- `promo-code-error`: end promotion-code loading state and show input-level validation
- `error`: distinguish expired, completed, load, unsupported-session, API validation, and promotion-code errors

## Skeleton And Loading Strategy

The Elements module should describe two supported loading strategies:

- SDK-managed skeleton: simplest path; leave `section.hideSkeleton` unset or `false`
- host-managed skeleton: set `section.hideSkeleton: true`, render merchant-owned loading UI, and clear it from `session-init-success` or a resolved initialization state

For branded flows such as clinkcoins, host-managed skeleton is often preferable because the payment area can match the surrounding order UI.

## Layout Guidance

The Elements module should document iframe and container considerations:

- iframe height can adapt, but the host must provide stable containers
- inline mode should avoid parent `overflow: hidden` that clips payment, wallet, QRCode, or 3DS interactions
- modal mode should provide reasonable width, height, and an internal scroll area
- drawer mode should ensure mobile sticky buttons do not cover the payment iframe
- `paymentMethod` and `currencySelect` may appear in different visual regions, but creation order still matters
- closing a dialog or drawer should clear session state so component unmount triggers `destroy()`

## README Updates

Update both `README.md` and `README-zh.md` so the public skill description explicitly includes Elements embedded checkout guidance. The README should state that the skill can help with:

- React, Vue, and native JS Elements integration
- SDK lifecycle and iframe mount/unmount behavior
- headless hook or composable patterns plus inline, modal, drawer, and multi-step layout recipes
- event-to-host-UI mapping
- promotion-code UI integration
- locale/theme customization
- SDK-managed vs host-managed skeleton strategies
- webhook and reconciliation boundaries for embedded checkout

## Testing

Add runtime tests for these cases:

- a prompt mentioning `@clink-ai/clink-elements` routes to `merchant_standard_integration`
- a React `loadClinkElements` prompt emits Elements artifacts
- a prompt mentioning `promoCodeChange` emits `promotion_code_ui_contract`
- a prompt asking for inline or drawer checkout emits `elements_layout_recipe`
- a prompt asking for a Next.js Elements component includes the client-only and server/client boundary artifact expectations
- an Elements prompt still preserves core Standard Integration artifacts such as `integration_checklist`, `webhook_handler_checklist`, and `merchant_order_mapping`
- Elements prompts do not route to merchant agent integration unless agent-specific signals dominate

Add structure checks if the repository already enforces reference module listing:

- `references/elements-integration.md` is present
- `SKILL.md` module map includes it
- README module tables include it

## Non-Goals

This merge should not:

- make Elements a fifth top-level route
- make dialog checkout the default layout
- remove hosted checkout or configured link guidance
- generate project-specific final frontend code without enough framework and codebase context
- weaken webhook, idempotency, reconciliation, or production validation requirements
- expose internal environment naming to merchant-facing output beyond existing developer-focused mappings where needed
- treat frontend success events as payment authority

## Implementation Order

1. Create `references/elements-integration.md` from the durable parts of `ELEMENT-SKILL.md`.
2. Update `SKILL.md` routing, working method, and module map.
3. Update `references/standard-integration.md` Step 4 to point to the Elements module.
4. Update `references/output-artifacts.md` with Elements-specific artifacts.
5. Update `references/review-checklist.md` with Elements checks.
6. Update `lib/skill-runtime.mjs` with Elements signals and artifacts.
7. Add runtime tests and any needed structure tests.
8. Update `README.md` and `README-zh.md`.

## Open Review Point

Before implementation, decide whether to keep `ELEMENT-SKILL.md` as a maintainer source file, rename it into `references/elements-integration.md`, or remove it after the module is created. The recommended default is to migrate its durable content into `references/elements-integration.md` and then remove or ignore the root-level standalone skill file so there is one canonical source.

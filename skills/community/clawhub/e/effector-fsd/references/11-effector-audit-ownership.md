# Effector audit ownership in FSD

Use this file for full audits of Effector projects that use Feature-Sliced Design. It complements the normal FSD import-boundary checklist by focusing on ownership of static Effector graph wiring.

## Contents

- [Why normal FSD checks can miss bugs](#why-normal-fsd-checks-can-miss-bugs)
- [Ownership matrix for cross-cutting Effector flows](#ownership-matrix-for-cross-cutting-effector-flows)
- [Page models are globally active after import](#page-models-are-globally-active-after-import)
- [Feature public APIs should expose capabilities, not implementation details](#feature-public-apis-should-expose-capabilities-not-implementation-details)
- [Page-owned API vs entity-owned API](#page-owned-api-vs-entity-owned-api)
- [App-level auth/unauthorized policy](#app-level-authunauthorized-policy)
- [Shared auth headers and domain mirroring](#shared-auth-headers-and-domain-mirroring)
- [Checklist for full FSD/Effector audit reports](#checklist-for-full-fsdeffector-audit-reports)

## Why normal FSD checks can miss bugs

A project can have perfect downward imports and still have architectural bugs:

- page models react while the page route is closed because modules are imported statically;
- feature public APIs expose raw Farfetched mutations and pages depend on `.finished.success` internals;
- a business resource API/contract lives in a page only because the first UI was a page;
- unauthorized/session clear policy is scattered across pages instead of owned by `app`;
- `shared/api` mirrors session state or performs redirects, making shared domain-aware.

A full audit must check **where cross-slice Effector wiring is owned**, not only whether imports are syntactically allowed.

## Ownership matrix for cross-cutting Effector flows

| Flow | Preferred owner | Why |
|---|---|---|
| `appStarted`, `appDestroyed`, router/history installation, providers | `app` | Application lifecycle coordinates multiple layers |
| Redirect after logout/session clear/unauthorized | `app/routes` | Routing policy coordinates session and pages |
| Applying a session barrier to many operations | `app/api` or `app/model` | Cross-operation composition imports many owners |
| Session state/current session query/contracts | `entities/session` | Session is a domain entity/resource |
| Login/logout submit action | `features/session-login`, `features/session-logout` | User intent/action |
| Reusable resource read query/contract | `entities/<entity>` | Domain resource, reusable beyond one page |
| User-action mutation and validation | `features/<action>` | Capability initiated by the user |
| Page-only list query with page filters/pagination | `pages/<page>` | Params and lifecycle are page-specific |
| Refresh after mutation for currently opened page | `pages/<page>` gated by route | Page decides what it displays |
| Global invalidation affecting many pages/entities | `app` integration or entity invalidation module | Cross-slice policy |
| Generic transport error mapping/base URL/fetch helpers | `shared/api` | Domain-independent infrastructure only |

## Page models are globally active after import

### Audit rule

If a page model listens to a feature/entity event or mutation success, require one of these:

1. The reaction is gated by the page route `$isOpened`.
2. The model is truly lazy-loaded only while the route is mounted and disposed afterwards, which is uncommon for Effector.
3. The wiring is moved to an app/entity invalidation owner.

### Bad

```ts
// pages/users/model/page.model.ts
sample({
  clock: [managerCreated, managerDisabled],
  fn: () => undefined,
  target: usersQuery.start,
});
```

This code still reacts while another page is open if the page module was imported by the route registry.

### Good

```ts
sample({
  clock: [managerCreated, managerDisabled],
  source: usersRoute.$isOpened,
  filter: Boolean,
  fn: () => undefined,
  target: usersQuery.start,
});
```

### Alternative: invalidation event

```ts
// entities/user/model/invalidation.model.ts
export const usersInvalidated = createEvent();

sample({
  clock: usersInvalidated,
  source: usersQuery.$pending,
  filter: (pending) => !pending,
  fn: () => undefined,
  target: usersQuery.start,
});
```

```ts
// app/model/user-invalidation.model.ts
sample({
  clock: [managerCreated, managerDisabled],
  target: usersInvalidated,
});
```

Use the app-level option when many pages/widgets need the same policy.

## Feature public APIs should expose capabilities, not implementation details

### Audit rule

A feature public API may expose UI, a `$$feature` facade, user-intent events, domain facts, and stable pending/error stores. It should not force consumers to know that the implementation is Farfetched or to listen to `mutation.finished.success`, unless the operation itself is the intended stable contract.

### Bad

```ts
// features/public-link-toggle/index.ts
export { updatePublicLinkMutation } from './api/update-public-link.mutation';
export { $publicLinkToStop, publicLinkStopConfirmed } from './model/public-link-toggle.model';
```

```ts
// pages/links/model/page.model.ts
sample({
  clock: updatePublicLinkMutation.finished.success,
  target: publicLinksQuery.start,
});
```

The page depends on Farfetched internals and cannot tell whether the feature emits “updated”, “skipped”, “cancelled”, or “refreshed”.

### Good

```ts
// features/public-link-toggle/model/public-link-toggle.model.ts
export const publicLinkUpdated = updatePublicLinkMutation.finished.success.map(
  ({ result }) => result,
);

export const $$publicLinkToggle = {
  linkToStop: $publicLinkToStop,
  error: $publicLinkToggleError,
  pending: updatePublicLinkMutation.$pending,
  onStopRequest: publicLinkStopRequested,
  onStopConfirm: publicLinkStopConfirmed,
  onStopDialogClose: publicLinkStopDialogClosed,
};
```

```ts
// features/public-link-toggle/index.ts
export { $$publicLinkToggle, publicLinkUpdated } from './model/public-link-toggle.model';
```

```ts
// pages/links/model/page.model.ts
sample({
  clock: publicLinkUpdated,
  source: linksRoute.$isOpened,
  filter: Boolean,
  fn: () => undefined,
  target: publicLinksQuery.start,
});
```

## Page-owned API vs entity-owned API

### Audit rule

When you find `pages/<page>/api` or page-exported contracts, decide whether the operation is really page-specific:

- Page-specific: list query whose params are page filters/sort/pagination and no other owner should reuse it.
- Entity-specific: current settings, user, order, link, session, or other resource read/write with business meaning beyond one page.
- Feature-specific: mutation caused by a user action such as create, update, retry, disable, login, logout.

### Bad

```txt
pages/settings/api/settings.ts
pages/settings/model/settings.contract.ts
pages/settings/index.ts exports AppSettingsContract
```

If settings are a product resource, the page should not own the API contract.

### Good

```txt
entities/app-settings/
  index.ts
  model/app-settings.contract.ts
  api/app-settings.query.ts

features/app-settings-update/
  index.ts
  model/app-settings-update.model.ts
  api/app-settings-update.mutation.ts

pages/settings/
  index.ts
  route.ts
  model/page.model.ts
  ui/settings-page.tsx
```

The page composes entity query and feature mutation; it does not own the resource.

## App-level auth/unauthorized policy

### Audit rule

If a project normalizes `401`/`403` in `shared/api`, find where those errors become session facts and redirects. The wiring must not live in `shared`; it normally belongs in `app/model` and `app/routes`.

### Good placement

```txt
shared/api/errors.ts                 # maps transport errors only
entities/session/model/session.ts    # sessionReceived/sessionCleared
app/model/auth-errors.ts             # merges operation failures -> sessionCleared
app/routes/auth-redirects.ts         # sessionCleared in protected area -> loginRoute
```

`app/model/auth-errors.ts` is allowed to import operations from lower layers because `app` is the composition layer.

## Shared auth headers and domain mirroring

### Audit rule

`shared/api` may own generic header helpers, but it must not become the source of truth for session/domain state. If `shared/api` has `$authHeaders` updated by session events, verify it is an adapter boundary and not a second independent auth store. Prefer deriving headers from session in an allowed owner or using `attach`/request helpers that inject headers declaratively.

### Acceptable adapter boundary

```txt
shared/api/auth-headers.ts         # generic adapter store, no session imports
entities/session/model/session.ts  # samples session token into adapter event
```

Document this if kept. Do not add route navigation or session contracts to `shared/api`.

## Checklist for full FSD/Effector audit reports

For each issue, include:

```txt
Severity
Current owner and file path
Why the owner is wrong or too broad
Correct owner
Dependency-direction reason
Minimal folder/import example
Acceptance criterion
```

Required audit passes:

- Public API width: raw mutation/effect/store leaks vs semantic facts/facades.
- Page static graph: page reactions gated by route or moved to app/entity invalidation.
- API/contract ownership: page-specific vs entity/feature.
- Cross-cutting auth/barrier/invalidation policy: app-owned, not scattered or shared-owned.
- Shared purity: no business domain knowledge in shared adapters.
- Route ownership: redirect policy in app/routes or page route model, not UI fallback only.

---
name: charming
description: Build, inspect, update, and call hosted personal apps with the Charming CLI. Covers the app contract (manifest, capabilities, env.storage, routes, window.charming.api), the sandbox rules, and the CLI workflow. Use when a user wants to create or manage an interactive personal app hosted by Charming.
license: MIT
compatibility: Requires the charming CLI, Node.js 22 or newer, and network access to charm.ing.
metadata:
  openclaw:
    requires:
      bins:
        - charming
    install:
      - kind: node
        package: usecharming
        bins:
          - charming
---

# Charming CLI

Charming is a hosting platform for personal apps you and your agent build, update, and use together. Learn more at [usecharming.com](https://usecharming.com). Install: `npm install -g usecharming`.

Charming hosts small single-purpose personal apps. You write two files, push them with `charming`, and the user gets a real URL with real storage that any agent — including this one, later — can keep editing.

An app is a directory:

- `module.js` — required. The backend: a `manifest` and a `routes` array.
- `ui.js` — optional. One JavaScript program that fills `#app`.
- `styles.css` — optional. Overrides only.

Do not free-hand the skeleton. Copy `templates/crud`, then change the data model.

> > > > > > > 111dce1 (Teach the skill to build apps, not just drive the CLI)

## Start

1. `charming auth status`. If `"authenticated": false`, run `charming auth login --no-open` and give the user the approval URL and code.
2. Copy the CRUD template into a working directory: `cp -r "$(npm root -g)/usecharming/templates/crud" ./my-app` Change `manifest.id`, `manifest.meta.name`, the storage key, and the `window.charming.api("<id>")` argument in `ui.js` to match.
3. `charming apps create ./my-app --description "<one line>" --dry-run`
4. `charming apps create ./my-app --description "<one line>" --yes`
5. Smoke-test the backend before you claim it works: `charming apps call <app-id> list --input '{}'`
6. Return the `url` from the JSON result.

`--yes` is required on a signed-in create because a create whose `manifest.id` already exists **replaces that app in place**. Ask the user before running it, and keep `manifest.id` stable and unique per app.

Without a saved token, `charming apps create` still works: it pairs the new app to this machine and stores an app-scoped credential locally, so later `update` and `call` on that app work from the same machine without `charming auth login`.

## Iterate

The CLI has no partial-edit mode. The loop is export, edit, push:

```
charming apps source <app-id> --out ./my-app   # writes module.js / ui.js / styles.css
# edit the files
charming apps update <app-id> ./my-app --dry-run
charming apps update <app-id> ./my-app
```

`apps update` reads the current source, matches its ETag, and fails loudly on a conflicting concurrent write instead of clobbering it — there's no revision number to track. A field missing locally is left as-is on the server: a directory with no `ui.js` updates the module and keeps the deployed UI.

Other commands: `charming apps list`, `charming apps describe <app-id>` (the public descriptor — ops and input schemas), `charming apps rename <app-id> <name>`, `charming apps delete <app-id> --yes`.

Run mutations with `--dry-run` first. Signed-in creates and deletions require `--yes`; pass it only after the user approves that action.

Read JSON results from stdout. Login instructions and JSON errors use stderr. Branch on `error.kind`. Follow `error.recovery` when present. Never print tokens or `device_code` values. Show `user_code` only during login.

`charming auth logout` removes the user credential and every app credential for the selected origin. Unclaimed apps that relied on those app credentials become unreachable.

## The module

```js
export const manifest = {
  $schema: 'https://charm.ing/schema/app-manifest/2026-07-31.json',
  id: 'water-log', // stable, unique, never changes
  meta: { name: 'Water Log', icon: { emoji: '💧', bg: '#0ea5e9' } },
  capabilities: { imports: ['charming:storage/kv@1.0'] },
};

export const routes = [
  {
    op: 'list',
    method: 'GET',
    annotations: { readOnlyHint: true },
    handler: async (_input, { env }) => (await env.storage.get('items_v1')) ?? [],
  },
];
```

- `manifest` is parsed statically. Keep it a plain literal — no computed values.
- Unknown top-level keys are rejected. The keys are `$schema`, `id`, `meta`, `capabilities`, `permissions`. There is no `version` or `displayName` key — the display name is `meta.name`.
- `meta.icon` is one emoji plus a hex background, not an array of image URLs.
- Declare the capabilities you use, nothing more. There is no capability `exports` array — `routes` is the only way to expose an operation.
- `routes` is an array of route objects, never an object keyed by op name. `op` values must be unique.
- Charming does **not** infer `readOnlyHint` from `method: 'GET'`. Set it explicitly on every read, or the operation publishes as a mutation.
- Handlers receive `(input, { env, ctx, request })` and return a JSON-compatible value; Charming wraps it as `{ ok: true, value }` on the wire (or `{ ok: false, error: { kind, message } }` on failure).
- Only WinterTC globals (Request, Response, URL, crypto, TextEncoder, …). No Node APIs, no DOM.
- Omit `default.fetch` unless the app needs custom fallback HTTP; Charming supplies a 404 handler when it's absent.

### Storage

`env.storage` (`get` / `put` / `delete` / `list`) stores JSON values **directly**. Never `JSON.stringify` on the way in or `JSON.parse` on the way out. Storage is per-app and survives updates, so iterate freely.

`env.storage` works everywhere the app runs — the web app and inside Claude/ChatGPT. `localStorage` / `sessionStorage` / `IndexedDB` need the claim-gated `charming:browser/storage@1.0` capability _and_ are empty inside chat hosts. Anything the user expects to keep belongs in `env.storage`.

Keep user data in `env.storage`, never in module constants — a shared or templated copy of the app then starts empty instead of leaking the author's data.

Full capability list, `permissions.server.fetch` rules, secrets, and external images: [resources/contract.md](./resources/contract.md).

## The UI

`ui.js` is one JavaScript program — not HTML, not a module. Charming injects `<div id="app"></div>`, a Tailwind-compatible runtime, and a default theme.

```js
const api = window.charming.api('water-log'); // manifest.id, NOT the URL's UUID
const items = await api.list({}); // the value itself; throws on failure
```

`window.charming.api(id).<op>(input)` returns the value directly and throws `CharmingOperationError` on failure. It is not `api.operation(name, params)`, and it is never a raw `fetch()`.

Sandbox rules that silently break apps:

- `alert`, `confirm`, and `prompt` do nothing. Build inline UI instead.
- No external `<script>` tags or CDN imports. Inline a UMD build if a library is truly needed.
- Prevent native form submission and handle it in JavaScript.
- Set `#app` innerHTML **before** attaching listeners, and re-bind after every re-render. Re-render narrow containers, not the whole root, or a refresh wipes half-typed input.
- Reserve the bottom-right 64px square — Charming's protected control sits there. Do not build a Charming badge, share button, app switcher, or account nav inside the app; the outer shell owns those.

`window.charming.viewer.can(op)` is a UI hint for read-only viewers, not an auth check — the server enforces access. Catch `forbidden` / `forbidden_write` and render a read-only state.

## Visual style

Charming apps should look like one product, not one generated page.

- Page `bg-stone-50`; cards `bg-white border border-stone-200 rounded-md`.
- Labels `text-sm font-semibold text-stone-700`; numbers `tabular-nums`.
- One accent color per app (emerald / amber / violet / cyan / sky); stone neutrals everywhere else.
- Sticky header with the title and one live metric. Optional tab nav with `border-b-2` on the active tab.
- Fill the viewport. Don't wrap the whole app in a narrow `max-w-*` box, and don't default every app to heading + input + button + empty list.
- No tiny all-caps tracked eyebrows, no empty settings pages, no fake account fields — they read as generated.

## Patterns that keep biting

- **Undo-toast deletes** beat confirm dialogs (which no-op here): delete immediately, show "Removed · Undo" for ~6s, and have Undo call a `restore` op that upserts by id. The CRUD template includes this.
- **Inline confirm** for genuinely destructive actions: swap the button for "Delete? [Delete] [Cancel]".
- **Migration discipline**: a versioned storage key (`items_v1`) plus a `normalize()` on read that fills defaults for new fields. On a shape change, write `migrate(old)` and keep the old key one cycle.
- **Live updates**: `window.charming.onStateChange?.(() => refresh())`, with a ~4s `setInterval` as a backstop.

More patterns, including agent-mediated enrichment and display-only apps: [resources/patterns.md](./resources/patterns.md).

## Beyond apps: the platform API

`charming apps …` covers create / read / update / call / delete. Everything else — sharing, public access, templates, routines, secrets, feedback — goes through the generated catalog:

1. `charming api list`, then `charming api describe <operation-id>`.
2. `charming api request set-app-public --param id=<app-id> --body '{"public":true}' --dry-run`

`charming doctor` checks connectivity, auth, and contract freshness. `charming agent-context` prints the CLI's own contract as JSON.

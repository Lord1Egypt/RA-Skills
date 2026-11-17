# The app contract, in full

## Capabilities

Declare only the capabilities the app actually uses in `manifest.capabilities.imports`.

| Capability | Unlocks | Notes |
| --- | --- | --- |
| `charming:storage/kv@1.0` | `env.storage` | Required for any app that persists state. |
| `charming:network/fetch@1.0` | `env.fetch` (open) | Also requires `permissions.server.fetch` with each exact origin. |
| `charming:secrets/fetch@1.0` | `env.fetch` (sealed, secret-substituting) | Claimed apps only. |
| `charming:logging/emit@1.0` | `env.logging` | Structured event logging visible to the app owner. |
| `charming:browser/storage@1.0` | `localStorage` / `sessionStorage` / `IndexedDB` | Claim-gated, web-only. Empty inside Claude/ChatGPT. |
| `charming:browser/microphone@1.0` | `getUserMedia` audio | Claim-gated. |
| `charming:browser/camera@1.0` | `getUserMedia` video | Claim-gated. |
| `charming:browser/geolocation@1.0` | geolocation | Claim-gated. |
| `charming:browser/clipboard-read@1.0` | reading the clipboard | Claim-gated. |
| `charming:browser/display-capture@1.0` | `getDisplayMedia` screen share | Claim-gated. |
| `charming:browser/midi@1.0` | Web MIDI (`navigator.requestMIDIAccess`) | Claim-gated. |
| `charming:browser/device-motion@1.0` | device orientation/motion | Claim-gated. |
| `charming:browser/ambient-light@1.0` | ambient light sensor | Claim-gated. |

There is no capability `exports` array in the current contract. `routes` is the only way to expose an operation to callers.

## `env.user`

`env.user` is always present, not gated by any import: the caller's public identity (`{ id, handle?, name?, image? }`) or `null`. It lives only on `env` — read `env.user` (or `context.env.user` from a named handler context). There is no `ctx.user`.

## The result envelope

```text
{ ok: true,  value: <anything JSON-able> }
{ ok: false, error: { kind: "not_found" | "unknown_operation" | "operation_failed", message: "..." } }
```

`window.charming.api(id).<op>(input)` unwraps this: it resolves to `value` on `ok: true` and throws `CharmingOperationError` (carrying `.kind` and `.message`) on `ok: false`.

## Outbound network access

For unauthenticated (open) external calls, declare both `charming:network/fetch@1.0` and `permissions.server.fetch`, listing each exact canonical HTTPS origin the app calls, e.g. `["https://api.example.com"]`. No HTTP, no wildcards, no credentials, no paths, no query strings, no fragments, no explicit default ports. Redirects must stay within the declared origins.

For calls that need an API key, declare `charming:secrets/fetch@1.0` instead to get a sealed `env.fetch`. The app owner sets the secret's value under App settings → Secrets; the agent only ever references the name:

```js
// header form
const res = await env.fetch('https://openrouter.ai/api/v1/chat/completions', {
  method: 'POST',
  headers: { Authorization: 'Bearer {{secret:OPENROUTER_KEY}}' },
  body: JSON.stringify(payload),
});

// query-parameter form — write the placeholder literally in the URL string;
// URLSearchParams.set(...) or encodeURIComponent(...) percent-encodes it
// first and it will NOT resolve
const res = await env.fetch(`https://api.example.com/data?api_key={{secret:EXAMPLE_KEY}}`);
```

`{{secret:NAME}}` resolves host-side, only inside a request header value or a query-parameter value — never in a parameter name, the host, the path, the fragment, or the body. The key never enters app source or the sandbox.

## External images

Charming's app-shell CSP locks `img-src` to same-origin + `data:` + `blob:`, so a plain `<img src="https://...">` does not render. Declare each exact origin in `manifest.permissions.browser["img-src"]`, then load the image through the runtime rather than setting `src` directly:

```js
const src = await window.charming.images.load(remoteUrl); // data: URL — works in every embed
imgElement.src = src;
```

`window.charming.images.proxy(remoteUrl)` also exists (a same-origin proxy URL) but does **not** work inside Claude's or ChatGPT's inline embed CSP, only standalone — a raw `<img>` pointed at it just shows a broken-image box with no visible error. Default to `.load()`. Both enforce the declared origins server-side; neither bypasses them.

## Protected control

Charming renders one protected control outside the generated app frame — a browser chrome bar or an MCP host's viewer chrome. Do not add another Charming badge, app switcher, Share button, App settings link, account nav, or agent handoff control inside the app. Reserve the bottom-right 64px square for it: don't put the app's only action, status, or scroll affordance under that corner.

## Storage caps and route mechanics

- `env.storage.put(key, value)` has a per-value cap in the low single-digit megabytes; there is no total cap. Large blobs belong in `charming:storage/blob@1.0` if the app needs it, not repeated KV puts.
- `routes[].method` defaults to `POST`, `path` defaults to `/api/<op>`, input defaults to a closed empty-object schema, and `public` defaults to `true`. Set `annotations` explicitly whenever a default doesn't fit — Charming never infers them from the HTTP method.
- `default.fetch` is an unmatched-request fallback only; it adds no discoverable route metadata. Its signature is `{ fetch(request, env, ctx) { ... } }` — the second argument is the environment itself, not the third.

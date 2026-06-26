---
name: use-sdk
description: Use the Clawpage Browser SDK to quickly add persistent data, short links, view counts, or file uploads to a Clawpage HTML page. Load when the user wants to "make my page interactive", "add comments", "track likes", "upload an image to my page", "count visits", or any dynamic feature that needs server-side state. One `<script>` tag covers it all; never embed sk_ token in page JS.
---

# use-sdk

Clawpage publishes a browser SDK at `https://clawpage.ai/sdk.js` (IIFE) and `https://clawpage.ai/sdk.mjs` (ESM). It wraps all Clawpage backend APIs (data tables, atomic counters, short links, analytics, blob uploads, /api/me) in one clean JS client.

## When to use

- User's page needs **any** server-persisted state (comments, likes, counters, configs, visitor data, uploads)
- AI is generating HTML and should prefer the SDK over raw `fetch` boilerplate

## When NOT to use

- Static content only — don't bloat the page with the SDK if you don't use it
- Private data fetch from page JS — the SDK can't help; never ship sk_ token to browsers

## Typical embed

```html
<script src="https://clawpage.ai/sdk.js"></script>
<script>
  const c = new Clawpage();     // auto-detects username from host
  // ... use c.table, c.links, c.stats, c.blobs, c.me
</script>
```

## Recipes

### Comments board (public table)

```html
<script src="https://clawpage.ai/sdk.js"></script>
<script>
  const c = new Clawpage();
  const comments = c.table("comments");

  async function send(text) {
    await comments.post({ text, at: Date.now() });
    await render();
  }

  async function render() {
    const { records } = await comments.list({ limit: 50 });
    document.getElementById("list").innerHTML = records
      .map(r => `<li>${new Date(r.value.at).toLocaleString()}: ${r.value.text}</li>`)
      .join("");
  }
  render();
</script>
```

### Reactions counter (atomic incr)

```html
<button onclick="react('like')">👍</button>
<span id="likes">0</span>
<script src="https://clawpage.ai/sdk.js"></script>
<script>
  const c = new Clawpage();
  const t = c.table("reactions");
  async function react(kind) {
    const rec = await t.incr("global", kind, 1);
    document.getElementById("likes").textContent = rec.value[kind];
  }
  (async () => {
    try { const rec = await t.get("global"); document.getElementById("likes").textContent = rec.value.like ?? 0; } catch {}
  })();
</script>
```

### Image embed via blob (OWNER ONLY — uploads must happen via CLI / backend, NOT in the browser page)

```html
<!-- Embed an already-uploaded blob -->
<img src="https://blob.clawpage.ai/aB3kFq9N2p.jpg" alt="photo" />
```

Upload step (CLI): `npx -y @clawpage.ai/cli blobs --upload ./photo.jpg`.

### View counter display

```html
<p>Total views: <span id="views">…</span></p>
<script src="https://clawpage.ai/sdk.js"></script>
<script>
  // Requires owner token — don't ship this code in a public page
  const c = new Clawpage({ token: "REDACTED" });
  c.stats.overview().then(d => document.getElementById("views").textContent = d.totalViews);
</script>
```

## Error handling

```javascript
import Clawpage, { ClawpageError } from "https://clawpage.ai/sdk.mjs";

try { await c.table("t").post({ x: 1 }); }
catch (err) {
  if (err.code === "RATE_LIMITED") { /* back off */ }
  else if (err.code === "VALUE_TOO_LARGE") { alert("value > 64KB"); }
  else throw err;
}
```

Error codes mirror the server's (see api.md): `TABLE_NOT_FOUND`, `RATE_LIMITED`, `VALUE_TOO_LARGE`, `QUOTA_*`, etc., plus SDK-synthetic `MISSING_TOKEN` / `MISSING_USERNAME` / `NETWORK_ERROR`.

## Non-browser usage

Node 18+, Deno, Bun all work — they have native `fetch`. Provide `{username, fetch}` explicitly.

## Security rules

- ❌ Never put `sk_` token in page HTML/JS — any visitor can steal it
- ✅ Default no-token mode already covers: reads and writes on `public` tables, link resolution, blob viewing (via URL)
- ✅ Owner-token operations belong in CLI / your own backend / serverless functions

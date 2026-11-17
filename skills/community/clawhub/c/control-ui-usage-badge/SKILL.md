---
name: "control-ui-usage-badge"
description: "Show per-message token usage (tokens, cache %, duration, throughput, model, cost) under each assistant message in the OpenClaw Control UI."
---

# Control UI Usage Badge

Show per-message token usage under every assistant reply in the browser **Control
UI** chat.

## Step 0 — ALWAYS ensure it is applied (do this first, every activation)

The badge is a client-side patch injected into `dist/control-ui`. It is **not**
shipped automatically:

- A fresh `openclaw skills install` only copies skill files. Nothing is patched
  until `apply.sh` runs.
- Every `openclaw update` **replaces** `dist/`, wiping the patch.

So on every use, run the idempotent ensure script **before** claiming it works:

```bash
bash scripts/apply.sh     # installs/repairs the patch; safe to re-run
bash scripts/status.sh    # prints PATCHED / NOT PATCHED, asset, version
```

Then tell the user to hard-refresh the Control UI tab (`Ctrl+Shift+R`) so the
Service Worker does not serve a stale copy. Never report "installed" without
having run `apply.sh`.

## What it does

- Client-side only. It monkeypatches `window.WebSocket` to scan the JSON frames
  the Control UI already receives (`chat.history`, `chat.startup`, run events)
  and appends a compact line to any assistant message that already renders text:

  `*↑23.4k · ↓373 · Σ48.8k · cache 25.1k read (51.8%) · ⏱1m56s · ⚡3.2t/s · deepseek-v4.1-flash · ~$0.0037*`

- The gateway transcript, memory files, and every other channel are untouched.
- No config change, no gateway restart — only static files under
  `dist/control-ui/`.

Why this exists: the built-in `messages.responseUsage` / `/usage` footer only
applies to *deliverable* channels (Discord, Telegram, Feishu, WeChat …). The
Control UI's webchat is not a deliverable channel, so that footer never renders
there. The Control UI has no native per-message usage UI, but `chat.history`
responses already carry a `usage` object per assistant message — this surfaces it.

## Requirement

Write access to the Control UI directory (default
`/usr/local/lib/node_modules/openclaw/dist/control-ui`). The scripts auto-use
`sudo -n` when that dir is not writable. Override the path with
`OPENCLAW_CONTROL_UI_DIR=/path/to/dist/control-ui` (also useful when OpenClaw is
installed under a user prefix, where no sudo is needed at all).

## Install / Update

```bash
bash scripts/apply.sh
```

Idempotent: backs up `index.html` to `index.html.oc-usage-bak` once, copies
`assets/oc-usage-badge.js` into `dist/control-ui/assets/`, and injects
`<script src="./assets/oc-usage-badge.js?v=<content-hash>"></script>` before
`</head>`.

To change behaviour, edit `assets/oc-usage-badge.js`, then re-run `apply.sh`. The
`?v=<hash>` query changes with the content, busting the Control UI Service
Worker's cache-first rule for `/assets/` (otherwise a stale copy is served).

## Uninstall

```bash
bash scripts/remove.sh
```

## Check status

```bash
bash scripts/status.sh
```

## Auto-heal after `openclaw update` (optional, recommended)

`apply.sh` is idempotent, so a recurring re-apply keeps the badge alive across
updates. Create an OpenClaw cron job (isolated, low frequency):

```
schedule: every 6h
payload : agentTurn
message : Run `bash ~/.openclaw/workspace/skills/control-ui-usage-badge/scripts/apply.sh`
          and reply with just its output. Do nothing else.
```

Or run `scripts/apply.sh` from any existing startup/heartbeat routine you
already have.

## Verify

DevTools console (`F12`) after a reload:
- `[oc-usage-badge] installed v1.2` → the script loaded.
- `[oc-usage-badge] annotated a frame` → frames were annotated.
- Assistant messages show the usage line.

Offline logic check: `node scripts/test-badge.js` (set `HISTORY_JSON` to a
`chat.history` payload with `messages[]`).

## Tunable fields (CONFIG in `assets/oc-usage-badge.js`)

All fields are boolean toggles at the top of the asset. Defaults: `input`,
`output`, `total`, `cacheRead`, `cachePct`, `cacheWrite`, `cost`, `duration`,
`throughput`, `model`, `warn` = on; `provider`, `toolCalls` = off. Edit, then
re-run `apply.sh`.

## Cost

`cost` shows the provider-reported cost when it is > 0. When the provider does
not report cost (common for some gateways), fill the `PRICES` table in the
asset (USD per 1,000,000 tokens) to show an estimated `~$…`:

```js
var PRICES = {
  "deepseek-v4.1-flash": { in: 0.14, out: 0.28, cacheRead: 0.014 },
};
```

## Field meanings

| Token | Meaning |
| --- | --- |
| `↑` | input tokens (non-cached prompt) |
| `↓` | output tokens |
| `Σ` | provider `totalTokens` (may include cache) |
| `cache A read (P%)` / `B write` | cache-read tokens and hit rate; write shown only when > 0 |
| `⏱` | approximate turn wall-clock (time since the user's message, tool time included) |
| `⚡Nt/s` | output tokens per second (throughput) |
| `~$x` | estimated cost from PRICES; `$x` (no `~`) = provider-reported cost |

## Troubleshooting

- **Nothing shows, no console logs** → the script never loaded: check CSP
  (`script-src 'self'` allows same-origin), a reverse proxy, or a PWA/SW cache.
- **`installed` but no `annotated`** → chat data is not arriving via the
  intercepted WS frames; confirm the gateway client uses global `WebSocket` and
  frames are `{type:"res"|"event"}` JSON strings.
- **Was working, then stopped** → almost always `openclaw update` wiped `dist/`.
  `status.sh` will say NOT PATCHED; re-run `apply.sh`.
- **Rollback** → `scripts/remove.sh`.

## Limits

- Only annotates assistant messages that already render text (tool-only
  messages are skipped).
- The newest live reply shows the line after the page next loads history /
  reloads — not mid-stream. Extending to run-completion events is possible but
  not implemented here.

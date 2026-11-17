---
name: etix-fpx
description: >-
  Query etix.com (event ticketing) from a shell with the fpx CLI
  (@fetchproxy/cli) instead of running the etix-mcp server — search events,
  venues, and performers, and pull event/venue detail, via one-shot calls
  through a signed-in browser tab. Use when you want Etix discovery data
  without the MCP, in a script, or on a machine where the MCP isn't
  installed.
---

# Etix via fpx (no MCP)

Etix fronts its whole consumer surface (`www.etix.com/ticket/...`) with a
**DataDome** bot-wall that 403s/202s any plain `curl`/Node request
(`captcha-delivery` interstitial). `fpx` routes the request through the
user's own signed-in browser tab (the ContextMint Bridge extension), which has
already cleared DataDome, so the same request succeeds. No Etix account is
needed — this is public event-discovery data.

Etix also publishes a documented OpenAPI seller API (`api.etix.com/v3`),
but every endpoint requires OAuth2 password-grant with venue/box-office
credentials — it's out of reach for a consumer and out of scope here.

This is the same data the `etix_*` MCP tools return, reached with one CLI
call instead of a running server.

## One-time setup

```sh
npm install -g @fetchproxy/cli              # provides `fpx`
fpx profile add etix --domain etix.com      # only the fetch capability is needed
fpx pair -p etix                            # prints a pair code → approve in ContextMint Bridge
```

Requirements: the **ContextMint Bridge** browser extension installed
(from https://github.com/nullnet-app/contextmint-bridge/releases — the fetchproxy
extension under its new name, same maintainer, as https://github.com/chrischall/fetchproxy#extension
says; verify the zip with `shasum -a 256 -c <zip>.sha256` or build from source), with an open
`www.etix.com` tab that has finished loading (so the DataDome check
clears), and Chrome **Site access** allowing `etix.com`. Pairing persists —
after the first approval every later `fpx` call reuses it.

## Core call pattern

Two response shapes, both fetched with the plain `get` verb:

```sh
# Clean JSON — pipe straight to jq
fpx get 'https://www.etix.com/ticket/api/online/search/suggest?keywords=jazz' -p etix \
  | jq '.'

# Server-rendered HTML — save it, then pull the embedded JSON-LD/microdata
fpx get 'https://www.etix.com/ticket/p/39004863' -p etix > /tmp/event.html
```

A `POST` (only `geolocation/search` needs one) uses `post-json`:

```sh
printf '{"cityOrPostalCode":"Charlotte, NC","country":"USA"}' > /tmp/geo.json
fpx post-json 'https://www.etix.com/ticket/api/online/geolocation/search' @/tmp/geo.json -p etix \
  | jq '.'
```

Ready-to-run paths + extraction recipes (JSON `jq`, HTML JSON-LD/microdata
via a small `node` one-liner, and the page's `dataLayer` analytics object
via `references/extract-datalayer.mjs` — the same shapes `etix-mcp`'s
`src/parse.ts` parses) are in `references/etix-endpoints.md`.

## The one rule: resolve ids first

Event/venue detail take a numeric id, never a name. Always hit
`search/suggest` first, take the `eventId`/`venueId`, then fetch detail:

```sh
fpx get 'https://www.etix.com/ticket/api/online/search/suggest?keywords=Marion+Meadows' -p etix \
  | jq -r '.events[] | "\(.eventId)\t\(.eventName)"'
```

## What's NOT usable

The full-text `POST /ticket/api/online/search` endpoint returns an
**encrypted/opaque (base64-looking) payload**, not JSON — `etix-mcp`
deliberately doesn't use it, and neither should this skill. Stick to
`search/suggest` (clean JSON) for search.

## Exit codes (fetch verbs)

- `0` — success. For HTML pages, a `0` can still be a DataDome interstitial
  body (check for `captcha-delivery` / "Please enable JS and disable any
  ad blocker" before parsing).
- `2` — bridge unavailable: extension not connected or pairing pending →
  run `fpx pair -p etix`, confirm an etix.com tab is open.
- `3` — bot wall: the tab hasn't cleared DataDome → open/refresh a
  `www.etix.com` tab, let it finish loading, and retry.
- `4` — upstream non-2xx from Etix.

## Notes

- Anonymous discovery reads only — no Etix login, no purchasing (buying
  tickets is a financial action and out of scope for this skill).
- `fpx health -p etix` shows bridge connection state when a call fails.
- This project is developed and maintained by AI (Claude).

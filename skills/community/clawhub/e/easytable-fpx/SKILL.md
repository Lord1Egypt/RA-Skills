---
name: easytable-fpx
description: >-
  Check restaurant availability and manage easyTable bookings
  (book.easytable.com/book/?id=<placeId>) from a shell with the fpx CLI
  (@fetchproxy/cli) instead of running the easytable-mcp server — list
  booking areas/dates/times, look up a booking by phone, and cancel it, all
  one-shot through a signed-in browser tab. Use when you want easyTable
  access without the MCP, in a script, or on a machine where the MCP isn't
  installed.
---

# easyTable via fpx (no MCP)

easyTable fronts every `book.easytable.com` endpoint — reads and writes alike
— with a Cloudflare check that 403s any plain `curl`/Node request. `fpx`
routes the request through the user's own signed-in browser tab (the
ContextMint Bridge extension), which has already cleared the challenge, so the same
requests succeed. There's no easyTable login: a restaurant is identified only
by its `id` (a.k.a. `place`) from its widget URL
`https://book.easytable.com/book/?id=<placeId>`.

This is the same data/actions the `easytable_*` MCP tools use, reached with
one-shot CLI calls instead of a running server.

## One-time setup

```sh
npm install -g @fetchproxy/cli               # provides `fpx`
fpx profile add easytable --domain easytable.com
fpx pair -p easytable                        # prints a pair code → approve in ContextMint Bridge
```

Requirements: the **ContextMint Bridge** extension installed (from
https://github.com/nullnet-app/contextmint-bridge/releases — Chrome: load the
chrome zip unpacked; Safari: ships inside the ContextMint app, no public download
yet, so use Chrome for now — it is the renamed fetchproxy extension, same maintainer; source is public, so
build it or verify the zip with its published `.sha256`), with an open
`https://book.easytable.com/book/?id=<placeId>` tab left to finish loading
(its Turnstile check solves itself), and Chrome **Site access** allowing
`easytable.com`. Pairing persists after the first approval.

## Core call

Reads are GET requests that return **HTML fragments** (not JSON) — the
widget loads them into a container div. Send the `X-Requested-With` header
the widget sends, and pipe the fragment to `grep`/`sed` rather than `jq`:

```sh
fpx get 'https://book.easytable.com/book/ajax/types.asp?id=1fdfc&lang=en' \
  -p easytable -H 'X-Requested-With: XMLHttpRequest'
```

Ready-to-run URLs + extraction recipes for every read, plus the cancel write
and the create/modify payload shape, are in
`references/easytable-requests.md`. Exhaustive parsing lives in the repo at
`src/parse.ts` / `docs/EASYTABLE-API.md` — the recipes here are compact
greps against the same markup those parsers target.

## The one rule: resolve the `type` first

Dates and times are scoped to a booking area. Always list types first, take
the `type` id, then feed it to dates/times:

```sh
fpx get 'https://book.easytable.com/book/ajax/types.asp?id=1fdfc&lang=en' \
  -p easytable -H 'X-Requested-With: XMLHttpRequest' \
  | grep -oE '<a[^>]*type=[0-9]+[^>]*>[^<]*</a>'
# <a href="#type=13991">Boka Inne</a>
```

Same pattern for cancelling: resolve the booking id via `cancel-search.asp`
(by mobile number) before calling the cancel endpoint.

## Creating or modifying a booking — not fully doable through fpx

`easytable_create_booking`/`easytable_modify_booking` need a live Cloudflare
**Turnstile token**, read from the widget's hidden
`input[name="cf-turnstile-response"]`. The MCP harvests it with a bespoke
`read_dom` verb wired into *this repo's own* fetchproxy transport
(`bridge-fetchproxy.ts`) — the stock `fpx` CLI has no DOM-read command (only
`get`/`post-json`/`request`/`cookies`/`local-storage`/`session-storage`/
`indexeddb`/`session`), so it cannot harvest that token.

The other three page-derived values (`bookingToken`, `cancellationtime`,
`lcid`) ARE plain server-rendered text, so `fpx get` + `grep` gets them fine
— see `references/easytable-requests.md` for the full payload shape and a
manual-token workaround (read the Turnstile input yourself from the browser
console). Treat create/modify as a manual/hybrid flow, not a clean one-shot.

## Exit codes (fetch verbs)

- `0` — success. Write endpoints answer HTTP 200 even on a *rejected*
  booking (`Status:0` in the body) — always check the parsed `Status`, not
  just the exit code.
- `2` — bridge unavailable: extension not connected or pairing pending → run
  `fpx pair -p easytable`, confirm an easytable tab is open.
- `3` — bot wall: the tab hasn't cleared Cloudflare → open/refresh a
  `book.easytable.com` tab and retry.
- `4` — upstream non-2xx from easyTable.

## Notes

- No easyTable account or API key involved — this is the user's own action
  on their own signed-in browser session.
- `fpx health -p easytable` shows bridge connection state when a call fails.
- Don't fire real create/cancel calls just to "test" the flow — a
  confirmed write here books/cancels a real table at a real
  restaurant.
- This project is developed and maintained by AI (Claude).

---
name: alltrails-fpx
description: >-
  Query alltrails.com (trail search, trail detail, reviews, photos, weather,
  and a signed-in user's saved lists / completed trails / activity feed) from
  a shell with the fpx CLI (@fetchproxy/cli) instead of running the
  alltrails-mcp server — one-shot calls through a signed-in browser tab. Use
  when you want AllTrails data without the MCP, in a script, or on a machine
  where the MCP isn't installed.
---

# AllTrails via fpx (no MCP)

AllTrails has **no public API**; alltrails-mcp reverse-engineers the internal
one alltrails.com itself uses, fronted by **DataDome**. DataDome fingerprints
the HTTP client, not just the cookie — a Node/curl replay of a captured
cookie gets **403'd** even the same day an identical in-tab fetch succeeds.
So every request must ride a same-origin fetch inside the user's own signed-in
tab, which `fpx` provides (no stored-cookie mode, unlike some other fleet
skills).

Every request also needs an **`x-at-key` app header** — a static, anonymous
client-identifier the web app sends on every `/api/alltrails/*` call. It is
**not stored anywhere** — capture it live from the tab's own traffic (below).
An in-tab `fetch` does **not** add it automatically, so it (plus
`x-at-caller`/`x-language-locale`) must be attached explicitly on every `fpx`
call, same as the MCP's `client.ts` does.

## One-time setup

```sh
npm install -g @fetchproxy/cli                  # provides `fpx`
fpx profile add alltrails --domain alltrails.com
fpx profile declare alltrails \
  --capture-header 'x-at-key@www.alltrails.com/api/alltrails/*'
fpx pair -p alltrails                           # prints a pair code → approve in ContextMint Bridge
```

Requirements: the **ContextMint Bridge** browser extension installed
([releases](https://github.com/nullnet-app/contextmint-bridge/releases) —
Chrome: load the chrome zip unpacked; use Chrome for now — Safari will ship inside the
ContextMint app, which has no public download yet), its Chrome
**Site access** allowing `alltrails.com`, and an open, **signed-in**
`www.alltrails.com` tab (the per-user tools need a real session; the trail
tools work signed-out too). Pairing persists after the first approval.
ContextMint Bridge is the fetchproxy extension renamed, same maintainer; source and `.sha256`-checkable release zips at https://github.com/nullnet-app/contextmint-bridge.

## Capture the app key, then attach it on every call

`x-at-key` is captured from the *tab's own* API traffic — the capture only
fires while the tab makes a request. `fpx session` triggers the capture and
returns everything declared, including `capturedHeaders`:

```sh
AT_KEY=$(fpx session -p alltrails | jq -r '.capturedHeaders["x-at-key"] // empty')
```

If `AT_KEY` comes back empty, the tab made no `/api/alltrails/*` request
**during the capture window**. The extension listens only while the capture
call is in flight, so loading a page first and running `fpx session` afterwards
is a race you usually lose — the requests fire before anything is listening.

Start the capture first, then feed the tab:

```sh
fpx session -p alltrails > /tmp/at.json &   # opens the capture window
sleep 1 && open 'https://www.alltrails.com/explore'   # or reload the open tab
wait && AT_KEY=$(jq -r '.capturedHeaders["x-at-key"] // empty' /tmp/at.json)
```

Attach it (plus the other two protocol headers — defaults match the MCP's
`ALLTRAILS_CALLER`/`ALLTRAILS_LOCALE`) on every `fpx get`/`post-json` call:

```sh
fpx get 'https://www.alltrails.com/api/alltrails/v3/trails/10236086?detail=medium' -p alltrails \
  -H "x-at-key: $AT_KEY" -H 'x-at-caller: Mugen' -H 'x-language-locale: en-US' \
  | jq '.trails[0] | {name, overview, length, elevation_gain}'
```

Without `x-at-key` the API answers `400`; a stale/rotated key answers `400`
or `401` — re-run the `fpx session` capture to get a fresh one and retry.
Ready-to-run request bodies for every read endpoint are in
`references/endpoints.md`.

## The one gotcha: `/me` shape

`GET /api/alltrails/me` wraps the signed-in user as `{"users":[{"id":...}]}`
— **not** `{"user":{...}}`. Get your own numeric user id with:

```sh
fpx get 'https://www.alltrails.com/api/alltrails/me' -p alltrails \
  -H "x-at-key: $AT_KEY" -H 'x-at-caller: Mugen' -H 'x-language-locale: en-US' \
  | jq -r '.users[0].id'
```

The per-user endpoints (lists, completed trails, activity feed) take that id
in the path.

## Exit codes (fetch verbs)

- `0` — success (still check the JSON body — a non-2xx AllTrails error can
  arrive as a 200 with an HTML/interstitial body; a non-JSON 2xx response
  from `fpx` is almost always a DataDome challenge page, not real data).
- `2` — bridge unavailable: extension not connected or pairing pending →
  `fpx pair -p alltrails`, confirm an alltrails.com tab is open.
- `3` — bot wall: the tab hasn't cleared DataDome → open a
  `www.alltrails.com` tab, clear the challenge, then retry. (Unlike a capture
  stall, this one really is "fix the tab first" — the wall is a state the tab
  is in, not an event the call has to witness.)
- `4` — upstream non-2xx from AllTrails (400/401 usually means a missing or
  stale `x-at-key` — re-capture and retry).

## Notes

- Read-only: this only covers `GET`/read `POST` (search, reviews) endpoints —
  AllTrails write endpoints are unverified and out of scope.
- Money/length fields are **metric** (meters) straight from the API; convert
  locally if you need imperial (`miles = meters / 1609.344`,
  `feet = meters * 3.28084`).
- `fpx health -p alltrails` shows bridge connection state when a call fails.
- Trail/user/list ids are numeric strings as they appear in AllTrails URLs.
- This project is developed and maintained by AI (Claude).

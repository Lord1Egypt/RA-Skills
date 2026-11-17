---
name: compass-fpx
description: >-
  Query compass.com (US real-estate portal) from a shell with the fpx CLI
  (@fetchproxy/cli) instead of running the compass-mcp server — search
  listings, get property/agent detail, price history, and resolve street
  addresses through one-shot fetches over a signed-in browser tab. Use when
  you want Compass data without the MCP, in a script, or on a machine where
  the MCP isn't installed.
---

# Compass via fpx (no MCP)

Compass has no public JSON data-API for search/listing/agent data — it's a
fully server-rendered React app that embeds each page's data as JSON inside
an inline `<script>` global (`global.uc`, `window.__INITIAL_DATA__`,
`window.__AGENT_PROFILE__`). compass.com also runs **AWS WAF**, which 403s
plain `curl`/Node requests on some paths regardless of headers. `fpx` routes
every request through the user's own signed-in browser tab (the ContextMint
Bridge extension), which already carries a cleared WAF session, so the page
renders normally — you then pull the JSON out of the HTML yourself.

This is **Bucket 1 (full-fetchproxy)**: every call, not just an auth
bootstrap, rides the bridge. Compass validates at the session level per
request, same as the `compass-mcp` server itself (no server-side path
exists). No Compass login is required beyond having a signed-in tab open —
search/listing/agent data and the address-typeahead endpoint are all public.

## One-time setup

```sh
npm install -g @fetchproxy/cli              # provides `fpx`
fpx profile add compass --domain compass.com
fpx pair -p compass                          # prints a pair code → approve in the ContextMint Bridge extension
```

Requirements: the **ContextMint Bridge** browser extension installed
([releases](https://github.com/nullnet-app/contextmint-bridge/releases); it is the
fetchproxy extension renamed, from the same maintainer, with public source and a
`.sha256` beside each release zip), an open
`www.compass.com` tab, and its Chrome **Site access** allowing `compass.com`.
Pairing persists — after the first approval every later `fpx` call reuses it.

## Core call pattern

Two request shapes:

1. **SSR pages** (search, homedetails, agent profile) — `fpx get` the path,
   then pull the inline JSON global out of the HTML.
2. **The one structured endpoint** (address typeahead) — `fpx post-json`.

```sh
fpx get 'https://www.compass.com/homes-for-sale/manhattan-ny/' -p compass > /tmp/page.html
node references/extract-global.mjs /tmp/page.html uc | jq '.sharedReactAppProps.initialResults.lolResults.data | length'
```

`references/extract-global.mjs` is a small, dependency-free re-implementation
of the balanced-brace walk `compass-mcp`'s own `src/page-state.ts` uses
(`extractGlobalAssign`) — Compass writes each global as a JSON *literal*
(`global.uc = {...};`), so once the object is sliced out, `JSON.parse`/`jq`
works normally. Regexing for it without brace-balancing breaks the moment a
nested value contains `}`.

Full endpoint list, exact paths, and `jq` projections are in
`references/requests.md`.

## The one rule: try the typeahead before free-text search

Compass's SSR free-text search (`/homes-for-sale/?q=<query>`) is WAF-walled
in production and reliably 403s. For **address resolution**, always hit the
structured, WAF-immune typeahead first (`POST /api/v3/omnisuggest/autocomplete`)
and only fall back to the SSR search pages when it returns nothing — mirror
`compass-mcp`'s own rung order (see `references/requests.md` §4).

## Sign-in / bot-wall detection

A response is NOT a good page when either is true:

- The final URL redirects to `/login` (fpx follows redirects like a browser,
  so check the body for the login form, or pass `-H` / inspect with
  `--json` to see the resolved URL).
- The body contains **both** `awswaf.com` and `challenge.js`, and is under
  ~80 KB (the AWS WAF challenge interstitial; a real signed-in page is much
  larger). `compass-mcp`'s `throwIfSignInPage` uses this exact pair of
  markers — grep for both before trusting a fetch:

```sh
grep -q 'awswaf.com' /tmp/page.html && grep -q 'challenge.js' /tmp/page.html && \
  [ "$(wc -c < /tmp/page.html)" -lt 80000 ] && echo "WAF-blocked — refresh the compass.com tab"
```

## Exit codes (fetch verbs)

- `0` — success.
- `2` — bridge unavailable: extension not connected or pairing pending → `fpx pair -p compass`, confirm a compass.com tab is open.
- `3` — bot wall: the tab hasn't cleared the AWS WAF challenge → refresh a `www.compass.com` tab and retry.
- `4` — upstream non-2xx from Compass.

## Notes

- **Pagination ceiling.** Compass's SSR search only server-renders its first
  page (~41 listings); `/page-N/` canonicalizes back to page 1 and returns
  identical data. To reach more of the market, narrow with price/bed bands
  (`/<lo>-<hi>-bed/`, `/<lo>-<hi>-price/`) and re-search each band — don't
  paginate.
- **Two URL forms per listing.** `_pid/` (`navigationPageLink`) is a stable
  opaque id — use it for bookmarks/trackers. `_lid/` (content-addressed by
  `listingIdSHA`) is what you fetch to read the *current* record, but it
  changes when a property is delisted and relisted.
- No saved-homes/saved-searches or market-trends endpoint exists server-side
  (client-rendered GraphQL / not exposed) — `compass-mcp` stubs those tools
  out too; this skill doesn't cover them.
- `fpx health -p compass` shows bridge connection state when a call fails.
- This project is developed and maintained by AI (Claude).

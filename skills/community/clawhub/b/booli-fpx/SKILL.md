---
name: booli-fpx
description: >-
  Query booli.se (Swedish property portal) from a shell with the fpx CLI
  (@fetchproxy/cli) instead of running the booli-mcp server — resolve areas,
  search for-sale and sold listings (slutpriser), and read property detail via
  one-shot GraphQL calls through a signed-in browser tab. Use when you want
  Booli data without the MCP, in a script, or on a machine where the MCP isn't
  installed.
---

# Booli via fpx (no MCP)

Booli fronts `www.booli.se` — including `/graphql` — with a Cloudflare managed
challenge that 403s any plain `curl`/Node request. `fpx` routes the request
through the user's own signed-in browser tab (the ContextMint Bridge extension),
which has already cleared the challenge, so the same anonymous GraphQL query
succeeds. No Booli login is needed — just a normal open tab.

This is the same data the `booli_*` MCP tools return (money in **SEK**, areas
in **m²**, rooms as a number), reached with one CLI call instead of a running
server.

## One-time setup

```sh
npm install -g @fetchproxy/cli           # provides `fpx`
fpx profile add booli --domain booli.se  # only the fetch capability is needed
fpx pair -p booli                        # prints a pair code → approve in ContextMint Bridge
```

Requirements: the **ContextMint Bridge** browser extension installed (from
https://github.com/nullnet-app/contextmint-bridge/releases — Chrome: load the chrome zip
unpacked; Safari isn't available yet — use Chrome for now), with an open
`www.booli.se` tab, and its Chrome **Site access** allowing `booli.se`.
ContextMint Bridge is the fetchproxy extension renamed, same maintainer; source at
https://github.com/nullnet-app/contextmint-bridge (build it, or verify a release zip with its published `.sha256`).
Pairing persists — after the first approval every later `fpx` call reuses it.

## Core call

Every query is a POST of `{"query": "...", "variables": {...}}` to the GraphQL
endpoint. Write the body to a file (a heredoc avoids shell-quoting the GraphQL
string), then send it so stdout is the GraphQL JSON, ready for `jq`:

```sh
cat > /tmp/bq.json <<'JSON'
{ "query": "…", "variables": { … } }
JSON
fpx post-json 'https://www.booli.se/graphql' @/tmp/bq.json -p booli | jq '.data'
```

Ready-to-run query bodies (area lookup, for-sale search, sold search, property
detail) with `jq` recipes are in `references/graphql-queries.md`. Exhaustive
field lists live in the repo at `src/graphql.ts` — the operations here are
compact, live-verified subsets.

## The one rule: resolve the area first

Booli searches take a numeric **area id** (`areaId`), never a place name.
Always resolve the name first, take the `id`, then search:

```sh
printf '{"query":"query($s:String!){areaSuggestionSearch(search:$s){suggestions{id displayName}}}","variables":{"s":"Nacka"}}' > /tmp/a.json
fpx post-json 'https://www.booli.se/graphql' @/tmp/a.json -p booli \
  | jq -r '.data.areaSuggestionSearch.suggestions[] | "\(.id)\t\(.displayName)"'
# 76      Nacka kommun
```

Pass that `id` as the search input's `areaId` (a string). The `SearchRequest`
input needs `areaId`, `page` (1-based), `ascending`, `excludeAncestors: true`,
`facets: []`, `filters: [{key,value}]`, and `sort` (`""` = newest). Filters
reuse the same keys the MCP does (`minRooms`, `maxListPrice`, `objectType`, …).

## Exit codes (fetch verbs)

- `0` — success (a GraphQL `errors` array can still ride in a `0` body; check `jq '.errors // empty'`).
- `2` — bridge unavailable: extension not connected or pairing pending → run `fpx pair -p booli`, confirm a booli tab is open.
- `3` — bot wall: the tab hasn't cleared Cloudflare → open/refresh a `www.booli.se` tab and retry.
- `4` — upstream non-2xx from Booli.

## Notes

- Anonymous reads only — the same public GraphQL surface as the MCP; no account
  data. Stay within booli.se's terms.
- `fpx health -p booli` shows bridge connection state when a call fails.
- Property detail is keyed by **residence id** — the number in a
  `/bostad/<id>` URL, which is a search result's `url` field, **not** `booliId`.
- This project is developed and maintained by AI (Claude).

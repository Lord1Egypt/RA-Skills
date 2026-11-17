---
name: booli
description: >-
  Search and analyse Swedish real estate on booli.se — active for-sale
  listings, sold prices (slutpriser), area resolution, and market
  statistics. Use when the user asks about Swedish property, Booli,
  bostäder, lägenheter, villor, or slutpriser.
---

# Booli (booli.se)

Tools for the Swedish property portal Booli, reading its consumer GraphQL
API. Money is in **SEK**, areas in **m²**, rooms as a number.

## Setup — the browser bridge

booli.se is behind a Cloudflare bot wall that blocks server-side requests,
so booli-mcp routes each query through **your own signed-in www.booli.se
browser tab** via the fetchproxy bridge (the ContextMint Bridge extension). No
Booli login is needed — just a normal, Cloudflare-cleared page view.

- Install ContextMint Bridge from https://github.com/nullnet-app/contextmint-bridge/releases
  (Chrome: load the chrome zip unpacked; Safari isn't available yet — use
  Chrome for now) and keep a **www.booli.se** tab open in that browser. On the
  first request, approve the one-time pairing prompt. It's the fetchproxy
  extension renamed, same maintainer; source at
  https://github.com/nullnet-app/contextmint-bridge (build it, or verify a
  release zip with its published `.sha256`).
- `BOOLI_TRANSPORT` picks the path: `auto` (default — tries a direct fetch
  first, falls back to the bridge when walled), `fetchproxy` (always the
  bridge), `direct` (fail if walled). The fleet shares WS port **37149**
  (`BOOLI_WS_PORT`).
- Run `booli_healthcheck` to confirm the path is working.

## Start with an area

Booli's searches scope by a numeric **area id**, not a place name. Resolve
first, or pass a free-text `location` and the search tools resolve the top
hit for you.

1. `booli_search_areas` — `{ query: "Nacka" }` → areas with `area_id` and
   `display_name`. Pass an `area_id` into the search tools.

## For-sale listings

- `booli_search_listings` — search active listings by `area_id` or
  free-text `location`, plus optional `min_list_price`/`max_list_price`
  (SEK), `min_list_sqm_price`/`max_list_sqm_price`, `min_rooms`/`max_rooms`,
  `min_living_area`/`max_living_area` (m²), `min_plot_area`/`max_plot_area`,
  `object_type` (comma-separated: Lägenhet, Villa, Kedjehus-Parhus-Radhus,
  Fritidshus, Gård, Tomt/Mark), `min_construction_year`/`max_construction_year`,
  `is_new_construction`, `sort` + `ascending`. Paginated by `page` — check
  `total_count`/`pages`. Returns slim summaries by default (`compact: false`
  for full raw records).
- `booli_get_listing` — full detail for one property by its **residence id**
  (the number in a booli.se/bostad/<id> URL, or a result's `residence_id`).
  Works for both active and sold properties.

## Sold prices (slutpriser) — the comparables

- `booli_search_sold` — sold properties with the achieved **sold price**,
  **sold date**, and **over/under-asking %**. Same scope/filters as the
  for-sale search, plus `min_sold_price`/`max_sold_price`,
  `min_sold_sqm_price`/`max_sold_sqm_price`, and `min_sold_date`/`max_sold_date`
  (YYYYMMDD). `sort` also accepts `soldDate`/`soldPrice`; the default is
  `soldDate` descending (most recent sales first), as for `booli_market_stats`.
- `booli_market_stats` — median/average sold price, price per m², and
  average over/under-asking % for an area (same filters as the sold
  search, over ONE page — `page`/`pages` say which; `total_count` is the
  whole matching set, not the sample). `sample_size` is the rows on the page
  and `sold_price_count`/`price_per_sqm_count`/`price_change_count` the rows
  behind each metric — check them before trusting a thin median.

## In context groups

booli-mcp sits in the **home** group (mcp-host context groups). It has no
canonical read: Booli has no account, so there is nothing of yours to list
(no saved homes or watched areas, so no subject), and every search needs a
place first. A group ask like "what's new at home?" passes Booli by; it
joins when the ask names a place — "…and what have 3-room flats in Nacka
sold for lately?" reaches `booli_search_sold`, and "homes for sale in
Södermalm" reaches `booli_search_listings`. Every tool is a `lookup`.
Booli is browser-bridged: when the bridge has no www.booli.se tab, the
group answers "Booli needs your browser open" rather than guessing.

## Diagnostics

- `booli_healthcheck` — one-call probe of the data path (direct or bridge).

All tools are read-only.

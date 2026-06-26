---
name: compass-mcp
description: Look up real-estate listings, property details, photos, price history, and resolve addresses on Compass via MCP. Triggers on phrases like "find homes on compass in", "compass property details for", "compass photos for", "compass price history for", "resolve this address on compass", "compare these compass listings", "what does compass say about", or any request involving Compass properties, prices, or comparisons. Requires compass-mcp installed and the fetchproxy extension active (see Setup below).
---

# compass-mcp

MCP server for Compass — natural-language access to listings, property records, photos, price history, and address resolution. Routes every request through your signed-in compass.com tab via the fetchproxy browser extension, so AWS WAF sees a real browser session instead of a Node process.

- **npm:** [npmjs.com/package/compass-mcp](https://www.npmjs.com/package/compass-mcp)
- **Source:** [github.com/chrischall/compass-mcp](https://github.com/chrischall/compass-mcp)

> ⚠️ Compass does not publish a public consumer API. Unlike portals with a JSON API surface, **compass.com is a server-rendered React app** — there are no `/api/...` data endpoints to call. Every tool extracts state from the inline scripts each page server-renders (`global.uc.sharedReactAppProps.initialResults` for search, `window.__INITIAL_DATA__.props.listingRelation.listing` for homedetails). Requests are dispatched through your own signed-in browser tab via the fetchproxy extension. Use at your own discretion.

## Setup

### 1. Install compass-mcp

`.mcp.json` (project) or `~/.claude/mcp.json` (global):

```json
{
  "mcpServers": {
    "compass": {
      "command": "npx",
      "args": ["-y", "compass-mcp"]
    }
  }
}
```

### 2. Install the fetchproxy extension (one-time, shared across all fetchproxy-based MCPs)

```bash
git clone https://github.com/chrischall/fetchproxy
cd fetchproxy
npm ci
npm --workspace=@fetchproxy/extension-chrome run build
```

Then in Chrome: `chrome://extensions` → Developer mode → Load unpacked → pick `packages/extension-chrome/dist/`.

### 3. Open compass.com and sign in.

That's it. No API keys, no env vars.

## Tools

### Listing data (public)

- **`compass_search_properties`** — Search by location + filters (price band, beds/baths min, home type). Slugifies free-text into Compass's `/homes-for-sale/<slug>/<filters>/` URL routing and extracts the SSR listings array. Returns matching listings with price, beds/baths, sqft, address, and the Compass home URL.
- **`compass_get_property`** — Full record by `url` (a Compass homedetails URL or path) or `listing_id_sha` alone. When only the sha is supplied, the tool resolves the canonical path internally via the WAF-immune omnisuggest typeahead, then fetches the `/homedetails/<slug>/<sha>_lid/` page. Returns address, neighborhood, beds/baths, sqft, lot size, price + $/sqft, monthly charges, MLS status, amenities, schools, parcel number, listing agent, and `extracted_features` parsed from the description.
- **`compass_get_property_photos`** — Full photo gallery from `listing.media[]` — original + thumbnail URLs and pixel dimensions. Floorplans/other media gated behind `include_all_categories`.
- **`compass_get_price_history`** — Listing-history events (Listed / Sold / Pending / Price Change / Delisted) with date, price, status, MLS attribution. Returns both this-listing and prior-listing aggregates.
- **`compass_get_comparable_rentals`** — Nearby rental listings for a property: lifts the target's city/state/zip, then searches rentals in the same locality. Returns `rentals: []` (with target context) when none come back.
- **`compass_get_agent_listings`** — Other listings by the same agent, from `/agents/<slug>/` (active by default; closed deals via `include_closed`).

### Resolution & batch

- **`compass_get_by_address`** — Resolve a free-text street address to the canonical Compass URL, `listing_id_sha`, and `pid`. Walks the structured typeahead first (WAF-immune), then SSR fallbacks; verifies each candidate against the query before accepting. Returns `{ resolved: false, error }` rather than leaking a wrong URL.
- **`compass_resolve_addresses`** — Bulk version of `get_by_address` — concurrent server-side resolution of many addresses in one round trip, sharing the same rung walker and per-row error contract.
- **`compass_bulk_get`** — Unbounded structured fetch (up to 200 targets) by `url` or `listing_id_sha`. One row per target; per-target errors captured per-row. No summary table.
- **`compass_compare_properties`** — Fetch and align up to 25 properties side-by-side. Per-target errors captured per-row; an opt-in pivoted summary table via `include_summary`.

### Local math (no network)

- **`compass_calculate_mortgage`** — PITI calculator. Provide home price, interest rate, optional down payment / taxes / insurance / HOA / PMI; returns a full monthly breakdown + total interest over the term.
- **`compass_calculate_affordability`** — Max purchase price under the 28/36 DTI rule from income, debts, down payment, and rates.

### Diagnostics & session

- **`compass_healthcheck`** — Round-trips a no-op request (`/robots.txt`) through the full bridge to confirm the WebSocket bridge is up, the extension is connected, and the signed-in tab is responsive — in one call.
- **`compass_get_session_context`** — Lists every registered session and the active one.
- **`compass_set_active_session`** — Flips which registered session answers future requests.

### Not yet supported

- **`compass_get_saved_homes`** / **`compass_get_saved_searches`** — Compass renders `/overview/favorites` and saved searches via an auth-scoped GraphQL endpoint that isn't reachable from a one-shot fetch. Both throw a clear "not yet supported" error today.

## Trigger examples

- "Find me 2-bedroom condos under $1.5M in Brooklyn on Compass" → `compass_search_properties`
- "What does Compass say about 42 Monroe St in Brooklyn?" → `compass_get_by_address` → `compass_get_property`
- "Show me the photos for that Compass listing" → `compass_get_property_photos`
- "Price history for this Compass home" → `compass_get_price_history`
- "Compare these three Compass listings" → `compass_compare_properties`
- "Monthly payment on a $500k home, 20% down, 6.5% rate" → `compass_calculate_mortgage`

## Gotchas

- **Sign-in required.** If the user isn't signed into compass.com in the bridged Chrome tab, network tools fail with `SessionNotAuthenticatedError`. Local-math tools work either way.
- **AWS WAF challenge.** Compass serves a WAF challenge to fresh sessions and 403s some SSR free-text paths. The address resolver routes through the WAF-immune omnisuggest typeahead to avoid it, and sha-only lookups use the WAF-immune `/listing/<sha>/view` redirect; solving a challenge in the Chrome tab once unblocks the SSR pages.
- **No write surface.** All tools are read-only — no saving homes/searches or submitting contact forms.
- **No market-report / Zestimate-history tool.** Compass doesn't expose region-level market data or a historical estimate series in its SSR blob, so there's no equivalent to a market-report tool.
- **Saved homes/searches are stubs.** See "Not yet supported" above.

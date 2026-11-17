# Compass requests for fpx

All paths are relative to `https://www.compass.com`. GET requests return HTML
with an embedded JSON global — pull it out with `extract-global.mjs` (in this
same directory) before piping to `jq`. The one structured endpoint (§4) is a
plain JSON POST.

```sh
fpx get 'https://www.compass.com/<path>' -p compass > /tmp/page.html
node extract-global.mjs /tmp/page.html <globalName> | jq '...'
```

Endpoints and field shapes below are transcribed from `compass-mcp`'s
`src/tools/*.ts` and `src/page-state.ts` — the same live-verified paths and
extraction targets the MCP tools use.

---

## 1. Search listings

`GET /homes-for-sale/<location-slug>/[<filters>/]`

- `<location-slug>`: lowercase, hyphenated free text (`"Brooklyn, NY"` →
  `brooklyn-ny`, `"94110"` → `94110`).
- Filters are path segments, in this order: `<bedsMin>-<bedsMax>-bed/`,
  `<priceMin>-<priceMax>-price/`, a home-type slug (`type-house`,
  `type-condo`, `type-townhouse`, `type-multi-family`, `type-land`,
  `type-rental`). Omit any filter you don't need.
- **Pagination ceiling**: Compass server-renders only ~41 listings into this
  page (`num`); `/page-N/` canonicalizes back to page 1 with identical data.
  To see more of the market, narrow the price/bed bands and re-search each
  band — there is no further page to fetch.

```sh
fpx get 'https://www.compass.com/homes-for-sale/brooklyn-ny/2-3-bed/500000-1500000-price/type-condo/' -p compass > /tmp/search.html
node extract-global.mjs /tmp/search.html uc > /tmp/search.json
```

Extraction path: `.sharedReactAppProps.initialResults.lolResults`
(`{ totalItems, data: [ { listing: {...} } ] }`).

```sh
jq -r '.sharedReactAppProps.initialResults.lolResults |
  "total=\(.totalItems)",
  (.data[].listing |
    "\(.listingIdSHA)\t\(.subtitles[0] // "")\t\(.title // "")\t\(.subStats // [] | map(select(.title=="beds")) | .[0].subtitle // "")bd")' \
  /tmp/search.json
```

Per-listing fields worth pulling: `listingIdSHA`, `pageLink` (the `_lid/`
detail URL, relative), `navigationPageLink` (the stable `_pid/` URL when
present), `title` (formatted price string), `subtitles` (`[street,
neighborhood]`), `status`, `location.{latitude,longitude}`,
`media[].{originalUrl,thumbnailUrl,category}` (`category:0` = photo),
`subStats[]` (`{title:"beds"|"baths"|"sqft", subtitle:"<n>"}`),
`clusterSummary.{bedrooms,bathrooms,priceRange:[min,max],formattedLotSize,savedListing}`.

**Comparable rentals** reuse this exact path shape with the rental filter:
`/homes-for-sale/<locality-slug>/type-rental/` — same extraction.

**Free-text SSR search** (`/homes-for-sale/?q=<query>`) exists but is
WAF-walled in production (reliably 403s) — don't rely on it; use §4 for
address resolution instead.

---

## 2. Property / listing detail

`GET /homedetails/<slug>/<listingIdSHA>_lid/`

If you only have the `listingIdSHA` (no slug), fetch
`GET /listing/<listingIdSHA>/view` instead — it 302-redirects to the
canonical slugged homedetails URL, and fpx follows the redirect like a
browser.

```sh
fpx get 'https://www.compass.com/homedetails/162-04-12th-Rd-Queens-NY-11357/2109718971930079225_lid/' -p compass > /tmp/detail.html
# or, sha-only:
fpx get 'https://www.compass.com/listing/2109718971930079225/view' -p compass > /tmp/detail.html

node extract-global.mjs /tmp/detail.html __INITIAL_DATA__ > /tmp/detail.json
```

Extraction path: `.props.listingRelation.listing`.

```sh
jq '.props.listingRelation.listing |
  {address: .location.prettyAddress, city: .location.city, state: .location.state, zip: .location.zipCode,
   price: .price.lastKnown, price_formatted: .price.formatted, per_sqft: .price.perSquareFoot,
   beds: .size.bedrooms, baths: .size.totalBathrooms, sqft: .size.squareFeet,
   lot_sqft: .size.lotSizeInSquareFeet, status: .localizedStatus, mls_status: .mlsStatus,
   photos: [.media[]?.originalUrl], schools: .detailedInfo.schools,
   agent: .agents[0]}' /tmp/detail.json
```

Other useful top-level fields: `compassPropertyId`, `pageLink` (`_lid/` URL),
`navigationPageLink` (stable `_pid/` URL), `description`,
`detailedInfo.{amenities,taxAnnualAmount,associationFee:{amount,frequency},
architecturalStyle,garageSpaces,totalParkingSpaces}`,
`events[]`/`history[]` (see §3), `mlsAlternateAddresses[]`,
`agents[].{id,fullName,companyName,profileUrl}`.

**Sentinel values**: `detailedInfo.taxAnnualAmount` under `10` is a
not-yet-assessed placeholder on new construction, not a real tax bill.

---

## 3. Price history

Same fetch + extraction as §2 (`__INITIAL_DATA__.props.listingRelation.listing`).
Read `events[]` (this listing's own MLS events) and `history[]` (events from
prior listings of the same property) — each entry:
`{ price, status, localizedStatus, timestamp (unix ms), pageLink, source:{externalSourceName} }`.

```sh
jq '.props.listingRelation.listing | {events, history}' /tmp/detail.json
# Earliest "Listed" event (days-on-market anchor):
jq -r '.props.listingRelation.listing.events // [] |
  map(select(.status==1 or (.localizedStatus|test("^listed$";"i")))) |
  sort_by(.timestamp) | .[0] // empty' /tmp/detail.json
```

---

## 4. Address typeahead (resolve an address → listing id) — WAF-immune, try FIRST

`POST /api/v3/omnisuggest/autocomplete`

Body: `{"q": "<street + city + state>", "sources": [0]}` — `sources: [0]`
restricts results to the Addresses source.

```sh
cat > /tmp/omni.json <<'JSON'
{"q": "158 Raven Blvd Lake Lure NC", "sources": [0]}
JSON
fpx post-json 'https://www.compass.com/api/v3/omnisuggest/autocomplete' @/tmp/omni.json -p compass \
  | jq '.categories[] | select(.name==1) | .items[] | {id, text, subText, redirectUrl}'
```

Response shape: `{ categories: [ { name, label, items: [ { text, subText,
redirectUrl, source, id, ucGeoId } ] } ], success, rankerVersion }`. Category
`name === 1` is "Addresses". `id` **is** the listing's `listingIdSHA` — it
matches the `_lid/` segment on the public homedetails page, so it feeds
straight into §2's sha-only fetch (`/listing/<id>/view`).

**Verify the match before trusting it** — the query terms should appear as
whole tokens in `text`/`subText` (case + street-suffix folded, e.g.
"Ln"/"Lane"); Compass's suggest can return an unrelated top hit when the
local market has no real match. `compass-mcp`'s rung order is: try this
typeahead first, and only fall back to the (WAF-walled) free-text/slug SSR
search in §1 if it returns nothing verified.

---

## 5. Agent's listings

`GET /agents/<slug>/` (e.g. `/agents/paige-mcguirk/`)

```sh
fpx get 'https://www.compass.com/agents/paige-mcguirk/' -p compass > /tmp/agent.html
node extract-global.mjs /tmp/agent.html __AGENT_PROFILE__ > /tmp/agent.json
```

Extraction paths (same `listing` shape as §2's `listingRelation.listing`):

- Active listings: `.data.agentProfileProps.activeListingsProps.initialSales[]`
- Closed deals: `.data.agentProfileProps.closedDealsProps.initialSales[].listing`
  (each entry wraps the listing under a `.listing` key, alongside `aiHexID`).

```sh
jq '.data.agentProfileProps.activeListingsProps.initialSales[] |
  {sha: .listingIdSHA, address: .location.prettyAddress, price: .price.formatted, status: .localizedStatus}' \
  /tmp/agent.json

jq '.data.agentProfileProps.closedDealsProps.initialSales[].listing |
  {sha: .listingIdSHA, address: .location.prettyAddress, close_price: .price.lastPropertyClosePrice}' \
  /tmp/agent.json
```

This page is large (~1.4 MB rendered); the `extract-global.mjs` walk handles
that fine, but expect the fetch itself to take a few seconds.

---

## Not covered (no server-reachable endpoint)

- **Saved homes / saved searches** — `/overview/favorites` is fully
  client-rendered via auth-scoped GraphQL the bridge can't intercept.
  `compass-mcp` stubs these tools out too; there's no fpx recipe for them.
- **Market trends / stats** — Compass doesn't expose region-level market
  data in any SSR blob (unlike some other portals' dedicated endpoint).

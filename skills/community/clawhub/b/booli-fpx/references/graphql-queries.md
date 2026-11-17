# Booli GraphQL queries for fpx

Ready-to-run bodies for `fpx post-json 'https://www.booli.se/graphql' @file -p booli`.
Each block is the full POST body (`{"query","variables"}`). All field names and
input shapes are live-verified against the endpoint; the exhaustive field
selections live in the repo at `src/graphql.ts` (these are compact subsets).

Endpoint: `https://www.booli.se/graphql` · Method: POST · anonymous.
Introspection is disabled — probe field names by sending a query and reading the
validation errors (that's how these were pinned).

Write the body to a file (heredoc avoids shell-quoting the GraphQL string),
then send it:

```sh
cat > /tmp/bq.json <<'JSON'
{ "query": "…", "variables": { … } }
JSON
fpx post-json 'https://www.booli.se/graphql' @/tmp/bq.json -p booli | jq '.data'
```

Always check for GraphQL errors: `jq '.errors // empty'` (an errors array can
ride in an HTTP-200 body).

Numeric fields come as `FormattedValue { raw, formatted }` — select `{ raw }`
for the number, `{ formatted }` for the display string.

---

## 1. Resolve an area → areaId (do this first)

`search` is free text.

```json
{
  "query": "query Areas($s: String!) { areaSuggestionSearch(search: $s) { suggestions { id displayName } } }",
  "variables": { "s": "Nacka" }
}
```

```sh
jq -r '.data.areaSuggestionSearch.suggestions[] | "\(.id)\t\(.displayName)"'
```

## 2. Search for-sale listings

`input` is a `SearchRequest`: `areaId` (string, from step 1), `page` (1-based),
`ascending`, `excludeAncestors: true`, `facets: []`, `filters: [{key,value}]`,
`sort` (`""` = newest, else `listPrice` / `listSqmPrice` / `rooms` /
`livingArea` / `rent` / `plotArea` / `published`). `result` mixes `Listing` and
`Project` (new-construction) nodes — take the `... on Listing` ones.

Filter keys (both key and value are strings): `objectType` (`Lägenhet`, `Villa`,
`Kedjehus-Parhus-Radhus`, `Fritidshus`, `Gård`, `Tomt/Mark`), `minRooms`/`maxRooms`,
`minLivingArea`/`maxLivingArea`, `minPlotArea`/`maxPlotArea`,
`minListPrice`/`maxListPrice`, `minListSqmPrice`/`maxListSqmPrice`,
`minConstructionYear`/`maxConstructionYear`, `isNewConstruction` (`1`/`0`).

```json
{
  "query": "query SearchForSale($input: SearchRequest) { searchForSale(input: $input) { totalCount pages result { __typename ... on Listing { booliId objectType tenureForm streetAddress descriptiveAreaName url rooms { raw } livingArea { raw } rent { raw } listPrice { raw formatted } listSqmPrice { raw } location { region { municipalityName } } } } } }",
  "variables": {
    "input": {
      "areaId": "76",
      "page": 1,
      "ascending": false,
      "excludeAncestors": true,
      "facets": [],
      "filters": [
        { "key": "objectType", "value": "Lägenhet" },
        { "key": "minRooms", "value": "3" },
        { "key": "maxListPrice", "value": "6000000" }
      ],
      "sort": ""
    }
  }
}
```

```sh
jq -r '.data.searchForSale | "total=\(.totalCount) pages=\(.pages)", (.result[] | select(.__typename=="Listing") | "\(.booliId)\t\(.listPrice.formatted // "—")\t\(.streetAddress)")'
```

## 3. Search sold listings (slutpriser — the comps)

Same `SearchRequest` input; result is `... on SoldProperty`. Sold-specific
filter keys: `minSoldPrice`/`maxSoldPrice`, `minSoldSqmPrice`/`maxSoldSqmPrice`,
`minSoldDate`/`maxSoldDate` (YYYYMMDD). `soldPricePercentageDiff.raw` is the
over/under-asking % (e.g. `-20`).

```json
{
  "query": "query SearchSold($input: SearchRequest) { searchSold(input: $input) { totalCount pages result { __typename ... on SoldProperty { booliId objectType streetAddress descriptiveAreaName url soldDate soldPrice { raw formatted } soldSqmPrice { raw } listPrice { raw } soldPricePercentageDiff { raw } rooms { raw } livingArea { raw } location { region { municipalityName } } } } } }",
  "variables": {
    "input": {
      "areaId": "76",
      "page": 1,
      "ascending": false,
      "excludeAncestors": true,
      "facets": [],
      "filters": [{ "key": "minSoldDate", "value": "20240101" }],
      "sort": ""
    }
  }
}
```

```sh
# Median sold price across the page (raw kronor):
jq -r '[.data.searchSold.result[] | select(.__typename=="SoldProperty") | .soldPrice.raw] | sort | .[length/2|floor]'
```

## 4. Property detail by residence id

`residenceId` is `ID!` — the number in a `/bostad/<id>` URL (a search result's
`url` field), **not** `booliId`. `propertyByResidenceId` returns the `Property`
interface; Listing/SoldProperty-only fields need inline fragments. Works for
both active and sold properties (check `__typename`).

```json
{
  "query": "query Detail($residenceId: ID!) { propertyByResidenceId(residenceId: $residenceId) { __typename booliId residenceId objectType tenureForm streetAddress descriptiveAreaName constructionYear url rooms { raw } livingArea { raw } plotArea { raw } rent { raw } operatingCost { raw } floor { raw } location { region { municipalityName countyName } namedAreas } ... on Listing { published isNewConstruction upcomingSale listingUrl listPrice { raw formatted } listSqmPrice { raw } agency { name url } estimate { price { raw } } } ... on SoldProperty { soldPrice { raw formatted } soldSqmPrice { raw } soldDate soldPricePercentageDiff { raw } } } }",
  "variables": { "residenceId": "4370936" }
}
```

```sh
jq '.data.propertyByResidenceId | {type: .__typename, addr: .streetAddress, rooms: .rooms.raw, m2: .livingArea.raw, price: (.listPrice.formatted // .soldPrice.formatted), area: .location.namedAreas[0]}'
```

---

## Market stats

Booli's GraphQL has no market-stats query — the `booli_market_stats` tool
derives median/average sold price, price-per-m², and average over/under-asking %
locally from a `searchSold` page (§3). Reproduce with `jq` over `result` as
shown above; check the count before trusting a thin median.

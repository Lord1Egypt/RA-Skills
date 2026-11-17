---
name: filter-cross-reference
description: 'Look up cross-reference / equivalent / interchange part numbers for heavy-duty filters (oil, air, fuel, hydraulic, cabin, water-separator filters for trucks and heavy equipment). Use when the user gives a filter part number and wants its equivalent, replacement, interchange, or cross reference — e.g. Donaldson P777868 equivalent, what replaces Fleetguard FS19816, Baldwin RS3870 interchange, 滤芯交叉编号查询. Works for OEM and aftermarket numbers (Donaldson, Fleetguard, Baldwin, Mann, WIX, CAT, Komatsu, Volvo, JCB, Cummins and other reference brands in the database).'
---

# Filter Cross-Reference Lookup

Look up heavy-duty filter part numbers against the
[Precise Filters](https://www.precise-filters.com) cross-reference database
(free, public, no auth or API key). The same data is browsable at the
[cross-reference lookup page](https://www.precise-filters.com/en/cross-reference).

## How to look up a number

1. Extract the part number(s) from the user's request. You MUST drop the
   brand word ("Donaldson", "Fleetguard", ...) — the server cannot separate
   brand from number, so send only the number itself.

2. Separators inside the number are tolerated in both directions: case,
   spaces, dashes, underscores, dots, and slashes are normalized server-side
   ("P 777868", "P-777868", "P777868", "32007701" and "320/07701" all
   resolve to the same record).

3. URL-encode the number in the path. This matters most for slashes —
   JCB/CASE-style numbers like `320/07701` MUST be encoded as `320%2F07701`
   or the URL will have an extra path segment and return a routing 404.

4. Call the API once per number:

   ```bash
   curl -s "https://www.precise-filters.com/api/cross-reference/{NUMBER}"
   ```

   Examples:
   `curl -s "https://www.precise-filters.com/api/cross-reference/P777868"`
   `curl -s "https://www.precise-filters.com/api/cross-reference/320%2F07701"`

5. Interpret the JSON response by HTTP status: 200 = match, 404 = no match,
   400 = bad input (missing or >64 chars), 500 = transient server error
   (body `{ "error": "..." }` — retry once after a few seconds, then tell
   the user the lookup service is temporarily unavailable; do NOT present a
   500 as "number not found").

### Response — match found (HTTP 200)

```json
{
  "query": "P777868",
  "matched": true,
  "brand": "Donaldson",             // reference brand of the queried number*
  "partNumber": "P777868",           // canonical spelling
  "variants": ["P777868"],           // other spellings of the same number
  "equivalents": [
    {
      "partNumber": "15270188",      // the equivalent (replacement) part
      "name": "Truck Air Filter 15270188 for TEREX",
      "category": "Air Filter - Engine",
      "moq": 100,                    // minimum order quantity, pieces
      "deliveryTime": "15",          // days; field absent when unknown
      "specs": [{ "parameter": "Dimensions", "value": "OD: 313mm; ..." }],
      "crossReferences": [{ "brand": "Ag-Chem", "partNumber": "122230" }],
      "applications": ["Truck"],
      "productUrl": "https://www.precise-filters.com/en/products/...",
      "imageUrl": "https://..."      // field absent when no photo
    }
  ],
  "lookupUrl": "https://www.precise-filters.com/en/cross-reference/p777868",
  "inquiryUrl": "https://www.precise-filters.com/en/contact",
  "source": "https://www.precise-filters.com"
}
```

Notes on the 200 shape:

- `specs` is capped at 8 entries and `crossReferences` at 20 — treat both as
  "key data", never claim they are exhaustive. The full lists live on
  `productUrl` / `lookupUrl`.
- *If the user queries a Precise catalog number (not an OEM number), `brand`
  is `"Precise"` and the match is Precise's own product — do not present
  "Precise" as the OEM brand being crossed in that case.
- Field values are English where translations exist; part numbers are
  language-neutral.

### Response — no match (HTTP 404)

```json
{
  "query": "...",
  "matched": false,
  "message": "No cross reference found ...",
  "searchUrl": "https://www.precise-filters.com/en/cross-reference",
  "contactUrl": "https://www.precise-filters.com/en/contact",
  "source": "https://www.precise-filters.com"
}
```

## How to present the result

- Lead with the direct answer: which part(s) replace the queried number.
  Name the equivalent's part number, product name, and filter category.
- Show the key specs (dimensions first) so the user can verify fitment.
- List a handful of the other cross-reference numbers (same filter under
  other brands) — useful when the user's preferred brand differs. Don't dump
  all of them unless asked.
- Always link `productUrl` (full specs and photos) and mention `lookupUrl`
  as the shareable cross-reference page.
- If the user asked about several numbers, call the API for each and present
  a compact table: queried number → equivalent → category → product link.
- On a 404, say the number isn't in the public database yet and offer the
  two links: `searchUrl` to browse by brand, and `contactUrl` where a free
  manual verification can be requested.

## Caveats

- Always tell the user to verify dimensions, sealing, and thread against
  their machine before ordering — visually similar filters can differ in
  flow direction or mounting.
- Brand names in results identify the replacement reference only; the
  equivalents are Precise-brand replacement parts, not genuine OEM parts.
- Translate your summary to the user's language, but keep part numbers
  verbatim.

## Links

- Website: [www.precise-filters.com](https://www.precise-filters.com)
- Browse cross references by brand: [cross-reference lookup](https://www.precise-filters.com/en/cross-reference)
- Product catalog: [heavy-duty filters](https://www.precise-filters.com/en/products)
- Free manual verification for unlisted numbers: [contact page](https://www.precise-filters.com/en/contact)

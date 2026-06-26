---
name: booksearch-api
description: Search Amazon KDP books on the BeyondBSR public API, retrieve BSR (Best Sellers Rank) history for a single book, and explore the Amazon category taxonomy (browse nodes) for any supported marketplace. Each book-search result now ships its full root → leaf category ancestor chain(s) inline, so the skill can aggregate market-opportunity reports by macro/sub category without follow-up calls. Use this skill whenever the user wants to discover, filter, or research self-published or traditionally published books on Amazon by BSR, category, keyword, royalty range, rating, reviews, publication date, binding type, or marketplace (currently only the US and FR Amazon marketplaces are populated with data — more coming soon); when the user wants the BSR timeline of a specific ASIN over the last N days; when the user wants to look up Amazon category codes (browse node IDs), walk the category tree (children, ancestors/breadcrumb), or search categories by name to use as filters in book search; or when the user wants to group/aggregate search results by macro category (e.g. "how many Personal Finance opportunities, broken down by sub-category?"). Typical intents include KDP niche research, low-competition book discovery, sales estimation, royalty/revenue projection, competitor analysis, paperback/hardcover filtering, bulk listing of books matching numeric/textual criteria, single-ASIN BSR history charts, resolving a human-readable category name (e.g. "manga", "self-help") into the Amazon `catId` to pass to `categoryIds` in book search, and producing category-grouped market-opportunity summaries from a single search response. Do not use for price-history timelines, review/rating timelines, or account/user data — only book search, BSR history, and category browsing are exposed.
metadata:
  clawdbot:
    requires:
      env:
        - BOOKSEARCH_API_KEY
---

# BookSearch API

## ⚠️ API Access & Beta Program

The BeyondBSR BookSearch API is currently in **private beta**. This skill requires an API key (`BOOKSEARCH_API_KEY`) which is **not publicly available** at this time.

Users interested in accessing Amazon KDP book data (BSR history, reviews, categories, keyword research) can apply to the early adopter program by contacting **support@beyondbsr.com**. Requests are reviewed individually and approved keys are issued on a case-by-case basis.

Without a valid key, all endpoints below will return `401 Unauthorized`.

---

Programmatic search over the BeyondBSR book catalogue, BSR history retrieval for a single book, and Amazon category taxonomy browsing. Six endpoints, JSON in / JSON out, API-key auth.

## When to use this skill

Use it when the user asks to:

- Find books matching numeric filters: BSR range, rating, reviews count, royalty, page count age, publication recency.
- Discover niches by keyword inclusion/exclusion or Amazon category IDs.
- Filter by marketplace (currently US / Amazon.com and FR / Amazon.fr only).
- Distinguish self-publishers from traditional publishers.
- Estimate sales (daily / weekly / monthly / quarterly) and revenue per copy.
- Compare BSR averages across multiple time windows (7d / 30d / 90d / 180d / 365d).
- Retrieve the **BSR timeline** of a single book (by `domainId` + `asin`) over the last N days, e.g. for charting rank evolution.
- **Resolve a category name into an Amazon `catId`** (browse node ID), look up a category's direct children, walk its breadcrumb up to the root, or list top-level book categories for a marketplace — to feed `categoryIds` into book search, or just to explore the taxonomy.

**Do NOT use** for: price-history charts, review/rating timelines, account/user data, or anything not in the response schemas below. Those are out of scope.

## Endpoints

```
POST https://api.beyondbsr.com/api/v1/books/search
GET  https://api.beyondbsr.com/api/v1/books/{domainId}/{asin}/bsr-history?days={1..365}
GET  https://api.beyondbsr.com/api/v1/categories?domainId={..}&depth={0..5}&includeFiction={true|false}
GET  https://api.beyondbsr.com/api/v1/categories/children?domainId={..}&catId={..}
GET  https://api.beyondbsr.com/api/v1/categories/search?domainId={..}&q={..}&limit={1..200}
GET  https://api.beyondbsr.com/api/v1/categories/ancestors?domainId={..}&catId={..}
Content-Type: application/json   (book search only)
X-API-Key: $BOOKSEARCH_API_KEY
```

## Authentication

- Read the key from the `BOOKSEARCH_API_KEY` env var. Format: `bbsr_live_<43-char-base64url>`.
- **Never** print, echo, log, or include the key in any user-facing output. Never paste it into another tool's input.
- On `401 Unauthorized`: do not retry. Report "API key missing or invalid — check `BOOKSEARCH_API_KEY` env var" and stop.
- Send `X-API-Key` exactly once. Multi-valued headers are rejected.

## Marketplace domains

**At this time only two marketplaces are populated with data: the United States (`domainId=1`) and France (`domainId=4`).** Additional marketplaces are planned but not yet available.

Map natural-language marketplace references (e.g. "the US store", "Amazon.com", "amazon francia", "Amazon.fr") to `domainId` using this table:

| domainId | locale | country | name          |
|----------|--------|---------|---------------|
| 1        | com    | US      | United States |
| 4        | fr     | FR      | France        |

The validator technically accepts `domainId` `1–12`, but **only `1` (US) and `4` (FR) return data right now**. If the user asks for any other marketplace (UK, Germany, Italy, Spain, Canada, Japan, etc.), tell them it is not currently supported — coming soon. Do not invent domain IDs.

## Request schema

All fields are optional except `domainId`. Enums accept either the string name (e.g. `"Weekly"`) or the integer value.

### Required

| Field      | Type | Constraint                  |
|------------|------|-----------------------------|
| `domainId` | int  | US (`1`) or FR (`4`) — the only marketplaces with data (validator allows 1–12). |

### BSR filters

| Field      | Type        | Default   | Notes                                                                       |
|------------|-------------|-----------|-----------------------------------------------------------------------------|
| `bsrType`  | enum        | `Weekly`  | `Historical(-1)`, `Current(0)`, `Weekly(7)`, `Days30(8)`, `Days90(9)`, `Days180(10)`, `Days365(11)` |
| `bsrMin`   | int?        | 1         | ≥ 1                                                                         |
| `bsrMax`   | int?        | 100000    | ≥ 1, `bsrMin ≤ bsrMax`                                                      |
| `bsrYear`  | short?      | null      | 2000–(current year + 1). Required together with `bsrMonth`. Use only with `bsrType=Historical`. |
| `bsrMonth` | short?      | null      | 1–12. Required together with `bsrYear`.                                     |

### Product filters

| Field              | Type    | Default     | Notes                                              |
|--------------------|---------|-------------|----------------------------------------------------|
| `bindingType`      | enum?   | null (all)  | `All`, `Paperback`, `Hardcover`                    |
| `publisherType`    | enum?   | `All`       | `All`, `SelfPublishersOnly`, `PublishersOnly`      |
| `interiorType`     | enum?   | `BlackWhite`| `BlackWhite`, `FullColor`                          |
| `vatType`          | enum?   | `Reduced`   | `Reduced`, `Standard`                              |
| `includePreOrders` | bool?   | `false`     | —                                                  |

### Quality filters

| Field         | Type    | Constraint                         |
|---------------|---------|------------------------------------|
| `ratingMin`   | double? | 0.0–5.0, `ratingMin ≤ ratingMax`   |
| `ratingMax`   | double? | 0.0–5.0                            |
| `reviewsMin`  | int?    | ≥ 0, `reviewsMin ≤ reviewsMax`     |
| `reviewsMax`  | int?    | ≥ 0                                |

### Economic filters

| Field                        | Type     | Notes                                                |
|------------------------------|----------|------------------------------------------------------|
| `royaltyMin`                 | decimal? | In currency units, **not** cents. `min ≤ max`.       |
| `royaltyMax`                 | decimal? | —                                                    |
| `monthsSincePublicationMin`  | int?     | `min ≤ max`                                          |
| `monthsSincePublicationMax`  | int?     | —                                                    |

### Discovery

| Field             | Type     | Default | Constraint                                                  |
|-------------------|----------|---------|-------------------------------------------------------------|
| `includeKeywords` | string[] | null    | ≤ 25 items, each ≤ 100 chars, non-empty. **Each element is matched as a literal contiguous substring** (case-insensitive) against title, publisher and authors. Multiple elements are combined with **OR**. Pass multi-word phrases as a single element (`["small business taxes"]`), NOT as separate tokens (`["small","business","taxes"]`) — the latter would match any book containing just one of those words. |
| `excludeKeywords` | string[] | null    | ≤ 25 items, each ≤ 100 chars, non-empty. Same matching semantics as `includeKeywords`: each element is a literal contiguous substring; books matching **any** element on title, publisher or authors are excluded. |
| `categoryIds`     | long[]   | null    | ≤ 100 items, each > 0 (Amazon BrowseNode IDs). **Subtree-expanded**: passing a non-leaf node (e.g. depth-2 "Quick & Easy", `catId=17`) returns every book tagged with any descendant leaf — you do not need to enumerate leaves yourself. Pass any node from `/categories`, `/categories/search`, `/categories/children`, or `/categories/ancestors`. Mixing leaves and parents in one call is allowed (logical OR across the union of the expanded sets). Stale / unknown `catId`s collapse to no overlap and are silently dropped, not an error. |
| `excludeFiction`  | bool?    | `true`  | When `true` (default), filters out fiction books — i.e. books whose categories all roll up to depth-2 ancestors flagged as fiction (Literature & Fiction, Romance, Mystery, Sci-Fi, Children's Books, Teen/YA, etc.) under the local Books root for the requested marketplace. A book is kept if **at least one** of its categories has a depth-2 ancestor flagged as non-fiction. Set `false` to include fiction. **Auto-disabled** when `categoryIds` is non-empty: explicit category intent overrides the fiction filter, otherwise passing a fiction category with the default would silently return zero results. |

### Pagination

| Field    | Type | Default | Range      |
|----------|------|---------|------------|
| `limit`  | int? | 100     | 1–300      |
| `offset` | int? | 0       | 0–100000   |

## Workflow

1. **Marketplace** — Identify `domainId` from intent using the marketplace table. If ambiguous (e.g. "Amazon"), ask which country.
2. **Translate** — Map every natural-language filter to its schema field. Don't guess enum values; use the table. Note: by default fiction is excluded (`excludeFiction=true`). If the user asks for fiction (e.g. "romance", "mystery novels", "show me fiction too") or a mixed catalog, set `excludeFiction: false` explicitly. Most KDP/low-content niche queries are non-fiction so the default is usually correct.
3. **Pagination** — Default to `limit: 50`. Raise to 100–300 only if the user explicitly wants many results. Start with `offset: 0`.
4. **Send** — POST the JSON body. Inspect the status code first.
5. **Paginate if needed** — If `returnedCount == limit`, more results likely exist. Offer to fetch the next page with `offset += limit`.
6. **Present** — Surface `title`, `asin`, `bsr`, sales/revenue estimates, and a clickable cover URL (see response notes).

## Example request

```json
{
  "domainId": 4,
  "bsrType": "Days90",
  "bsrMin": 1,
  "bsrMax": 50000,
  "bindingType": "Paperback",
  "publisherType": "SelfPublishersOnly",
  "ratingMin": 4.0,
  "reviewsMin": 10,
  "interiorType": "BlackWhite",
  "vatType": "Reduced",
  "royaltyMin": 2.50,
  "royaltyMax": 15.00,
  "monthsSincePublicationMax": 24,
  "includePreOrders": false,
  "includeKeywords": ["journal", "notebook"],
  "excludeKeywords": ["coloring"],
  "categoryIds": [266162, 3248921],
  "excludeFiction": false,
  "limit": 50,
  "offset": 0
}
```

## Example cURL

```bash
curl -X POST "https://api.beyondbsr.com/api/v1/books/search" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $BOOKSEARCH_API_KEY" \
  -d '{
    "domainId": 4,
    "bsrType": "Days90",
    "bsrMax": 50000,
    "bindingType": "Paperback",
    "publisherType": "SelfPublishersOnly",
    "ratingMin": 4.0,
    "limit": 50
  }'
```

## Response schema

### Envelope — `BookSearchApiResponse`

| Field           | Type    | Notes                                                              |
|-----------------|---------|--------------------------------------------------------------------|
| `returnedCount` | int     | Items in **this page**. NOT a total-match count (no total exposed).|
| `limit`         | int     | Effective limit applied (capped at 300).                           |
| `offset`        | int     | Effective offset applied.                                          |
| `results`       | array   | `BookSearchResultDto[]`. Empty if no match.                        |

### Result item — `BookSearchResultDto` (most relevant fields)

| Field                | Type     | Notes                                                                                  |
|----------------------|----------|----------------------------------------------------------------------------------------|
| `id`                 | long     | Internal book ID.                                                                      |
| `asin`               | string   | 10-char Amazon ASIN.                                                                   |
| `title`              | string   | Full title.                                                                            |
| `authors`            | string?  | Comma-separated, ordered by `display_order`.                                           |
| `publicationDate`    | datetime?| Nullable.                                                                              |
| `publisher`          | string?  | Manufacturer/publisher name.                                                           |
| `coverImageFilename` | string?  | Build URL: `https://m.media-amazon.com/images/I/{filename}`.                           |
| `imageFilenames`     | string[] | All carousel images (same URL pattern).                                                |
| `rating`             | double   | 0.0–5.0.                                                                               |
| `reviews`            | int      | Total reviews.                                                                         |
| `bsr`                | int      | **The column matching the requested `bsrType`** — i.e. the value filtered/sorted on.   |
| `bsrCurrent`         | int?     | Latest snapshot BSR, regardless of `bsrType`.                                          |
| `avgBsr7d`           | int?     | Always populated.                                                                      |
| `avgBsr30d`          | int?     | Always populated.                                                                      |
| `avgBsr90d`          | int?     | Always populated.                                                                      |
| `avgBsr180d`         | int?     | Always populated.                                                                      |
| `avgBsr365d`         | int?     | Always populated.                                                                      |
| `pageCount`          | int?     | —                                                                                      |
| `priceCents`         | int?     | List price (MSRP) in cents.                                                            |
| `dailyEstimate`      | decimal  | Estimated copies/day from BSR model.                                                   |
| `weeklyEstimate`     | decimal  | Estimated copies/week.                                                                 |
| `monthlyEstimate`    | decimal  | Estimated copies/month.                                                                |
| `quarterlyEstimate`  | decimal  | Copies/quarter (needs ≥ 13 weeks of data).                                             |
| `royalty*Cents`      | int?     | Per-copy royalty in cents. 4 combinations: B/W or Color × Reduced or Standard VAT.     |
| `*Revenue*Cents`     | long?    | Derived = estimate × royalty. 16 fields total: {daily,weekly,monthly,quarterly} × {Black,Color} × {Reduced,Standard}. |
| `binding`            | string?  | Localised label (e.g. `"Paperback"`, `"Hardcover"`, `"Non-standard"`).                 |
| `dimensions`         | string?  | Formatted, prefixed by binding. Example: `"Paperback: 152 x 8 x 229 mm"`.              |
| `trim/spineWidthMm`  | int?     | Trim/spine measurements.                                                               |
| `categories`         | long[]   | Raw leaf Amazon `cat_id`s the book is tagged with (verbatim from the database). Preserves original tag order. May be empty for books still being enriched. |
| `categoryPaths`      | `Array<Array<{catId:long,name:string,depth:int}>>` | One inner array per entry in `categories`, each is the full root → leaf ancestor chain sorted by `depth` ascending. Use this to aggregate / group books by macro or sub category in a single round-trip without calling `/categories/ancestors` per leaf. |
| `subcategoryRanks`   | `Array<{catId:long,rank:int,name:string}>` | Per-category Best Sellers Rank of the book inside each subcategory it is listed in (Amazon's "#1 in <category>" data). `catId` is the Amazon browse node, `rank` is the position within that node, `name` is the localised category label. Ordered as returned by Amazon (best/most-specific first). May be empty `[]` for books not yet enriched. Distinct from the top-level `bsr`/`bsrCurrent`, which are the overall Books-store rank. |
| `frequentlyBoughtTogether` | `string[]` | ASINs of products Amazon surfaces as frequently bought together with this book. Use for competitor / cross-sell discovery (feed each ASIN back into `bsr-history` or a `includeKeywords`/`asin`-targeted search). May be empty `[]`. Not every book has this data — populated for a subset of titles. |

**Important caveats**

- All royalty and revenue fields are in **cents** — divide by 100 before showing currency.
- `bsr` ≠ `bsrCurrent`. `bsr` is whatever column was chosen by `bsrType`; `bsrCurrent` is always the latest snapshot.
- In `bsrType=Historical` mode, the `avgBsrXd` averages come from the current snapshot table while `bsr` itself is the historical month value — there is a documented temporal asymmetry inside the same response. Mention this if the user is doing a strict historical analysis.
- `categoryPaths.length === categories.length` for a healthy dataset. If a leaf `cat_id` has been deleted upstream after the book was indexed, the corresponding inner array is silently dropped (never null) — so `categoryPaths.length` may be ≤ `categories.length`. The `categories` array always reflects the original tag set.
- Both `categories` and `categoryPaths` may be **empty arrays `[]`** (never `null`) for books still being enriched or whose taxonomy snapshot hasn't propagated yet. Aggregation code must skip these books rather than fail on missing chains.

### Aggregating results by category

Each `categoryPaths` inner array is sorted by `depth` ascending. The taxonomy under the Books root is consistent across marketplaces (only the labels are localised):

| Depth | Role | US example | IT example |
|-------|------|------------|-----------|
| 0 | Books root | `Books` | `Libri` |
| 1 | Container shell | `Subjects` | `Categorie` |
| 2 | **Top-level subject** ("macro") | `Self-Help`, `Cookbooks, Food & Wine`, `Crafts, Hobbies & Home` | `Cucina, casa e giardinaggio` |
| 3 | **Sub-category** | `Crafts & Hobbies`, `Christian Books & Bibles` | — |
| 4-5 | **Niche / micro-niche** (KDP-relevant) | `Coloring Books for Grown-Ups`, `Bible Study & Reference` | — |

To produce a market-opportunity report, group on the **`catId` at the desired depth**, not the `name` (names are locale-dependent; `catId` is stable). For KDP niche research the interesting depths are **3 and 4**: depth 2 is usually too broad (e.g. "Crafts & Hobbies" alone covers thousands of books), while depth 3-4 isolates real nicchie ("Coloring Books for Grown-Ups", "Word Search", "Christian Living").

Pattern — nested macro → sub-niche histogram with revenue rollup, from one search response:

```js
// macro (depth=2) -> { name, books, subniches: Map<catId, { name, books, monthlyRevCents }> }
const report = new Map();

for (const book of response.results) {
  const seenMacros  = new Set();   // dedupe within the same book
  const seenNiches  = new Set();

  for (const chain of book.categoryPaths) {        // may be [] for un-enriched books
    const macro = chain.find(n => n.depth === 2);
    const niche = chain.find(n => n.depth === 3) ?? chain.find(n => n.depth === 4);
    if (!macro) continue;

    if (!seenMacros.has(macro.catId)) {
      seenMacros.add(macro.catId);
      const m = report.get(macro.catId) ?? { name: macro.name, books: 0, subniches: new Map() };
      m.books++;
      report.set(macro.catId, m);
    }
    if (niche && !seenNiches.has(niche.catId)) {
      seenNiches.add(niche.catId);
      const m = report.get(macro.catId);
      const n = m.subniches.get(niche.catId) ?? { name: niche.name, books: 0, monthlyRevCents: 0 };
      n.books++;
      // pick whichever revenue field matches the user's interior/VAT context
      n.monthlyRevCents += book.monthlyRevenueBlackReducedVatCents ?? 0;
      m.subniches.set(niche.catId, n);
    }
  }
}
```

Sample fragment of a result with two categories (US, depth-1 is always `Subjects` — depth-2 is the macro):

```json
{
  "asin": "1234567890",
  "title": "Quick Weeknight Dinners",
  "categories": [4259, 9876],
  "categoryPaths": [
    [
      { "catId": 283155, "name": "Books",                "depth": 0 },
      { "catId": 1000,   "name": "Subjects",             "depth": 1 },
      { "catId": 6,      "name": "Cookbooks, Food & Wine","depth": 2 },
      { "catId": 17,     "name": "Quick & Easy",         "depth": 3 },
      { "catId": 4259,   "name": "General",              "depth": 4 }
    ],
    [
      { "catId": 283155, "name": "Books",                       "depth": 0 },
      { "catId": 1000,   "name": "Subjects",                    "depth": 1 },
      { "catId": 10,     "name": "Health, Fitness & Dieting",   "depth": 2 },
      { "catId": 9876,   "name": "Diet & Weight Loss",          "depth": 3 }
    ]
  ]
}
```

**One-shot aggregation tip.** When the goal is a single histogram/report (as opposed to interactive paging), call `POST /books/search` with `limit=300` (the max). A 300-result response is ~850 KB and returns in ~200-350 ms in production — almost always cheaper than paginating. Only fall back to paged fetches if more than 300 books matter for the report (rare for niche analysis).

## BSR History endpoint

Single-ASIN BSR timeline. Returns raw snapshots from the time-series store, ordered ascending by `recordedAt`.

```
GET https://api.beyondbsr.com/api/v1/books/{domainId}/{asin}/bsr-history?days={1..365}
X-API-Key: $BOOKSEARCH_API_KEY
Accept: application/json
```

### When to use

- The user has a specific ASIN and wants its BSR over time (chart, drill-down, sanity-check the search-time `avgBsrXd` averages).
- The user wants to verify a book's recent rank trajectory (e.g. "is it gaining or losing visibility?").

If the user has filter criteria but no specific ASIN, use `POST /search` first, then call this endpoint per ASIN of interest.

### Path & query parameters

| Param      | In    | Type   | Required | Constraint                                                                 |
|------------|-------|--------|----------|----------------------------------------------------------------------------|
| `domainId` | path  | int    | yes      | US (`1`) or FR (`4`) — see Marketplace domains table (validator allows 1–12). |
| `asin`     | path  | string | yes      | Exactly 10 chars, regex `^[A-Z0-9]{10}$` (uppercase letters / digits only). |
| `days`     | query | int?   | no       | 1–365. Default `365`. Window is `[now - days, now]` UTC.                   |

### Example request

```
GET /api/v1/books/1/1635864348/bsr-history?days=90
X-API-Key: $BOOKSEARCH_API_KEY
Accept: application/json
```

### Example cURL

```bash
curl -X GET "https://api.beyondbsr.com/api/v1/books/1/1635864348/bsr-history?days=90" \
  -H "X-API-Key: $BOOKSEARCH_API_KEY" \
  -H "Accept: application/json"
```

### Response schema — `BookBsrHistoryApiResponse`

| Field         | Type        | Notes                                                              |
|---------------|-------------|--------------------------------------------------------------------|
| `asin`        | string      | Echoed from request.                                               |
| `domainId`    | int         | Echoed from request.                                               |
| `fromUtc`     | datetime    | Window start (`now - days`), UTC.                                  |
| `toUtc`       | datetime    | Window end (`now`), UTC.                                           |
| `pointCount`  | int         | Number of BSR snapshots in `points`.                               |
| `points`      | array       | `BsrPointDto[]` ordered ascending by `recordedAt`.                 |

`BsrPointDto`:

| Field              | Type      | Notes                                                          |
|--------------------|-----------|----------------------------------------------------------------|
| `recordedAt`       | datetime  | UTC timestamp of the snapshot.                                 |
| `bestSellersRank`  | int?      | BSR at that timestamp. May be null if Keepa returned no rank.  |

Example body:

```json
{
  "asin": "1635864348",
  "domainId": 1,
  "fromUtc": "2026-01-27T00:00:00Z",
  "toUtc": "2026-04-27T00:00:00Z",
  "pointCount": 412,
  "points": [
    { "recordedAt": "2026-01-27T03:14:00Z", "bestSellersRank": 1234 },
    { "recordedAt": "2026-01-27T15:02:00Z", "bestSellersRank": 1218 }
  ]
}
```

### Status codes (BSR history specific)

| Code | Meaning                       | Notes                                                                 |
|------|-------------------------------|-----------------------------------------------------------------------|
| 200  | OK                            | `pointCount` may be 0 if no snapshots exist in the window.            |
| 400  | Validation failed             | `ValidationProblemDetails`. Common causes: `days` out of range, `asin` wrong format, `domainId` out of `[1,12]`. |
| 404  | ASIN not found for that domain| `ProblemDetails` JSON (`{title:"Not Found",status:404,...}`). The book is not tracked in BeyondBSR for this marketplace. Tell the user — do not retry with the same pair. |
| 401 / 429 / 500 | See generic table below.            |

### Caveats

- Granularity is **raw**: Keepa snapshots arrive 1–4× per day on actively-tracked books. A 365-day window typically yields 365–1460 points. No daily aggregation is applied.
- The endpoint returns only `(recordedAt, bestSellersRank)`. Use `POST /search` if you also need rating/review/price data.
- ASIN is case-sensitive — must be uppercase. `1635864348` (all digits) is valid.
- Default 365 days is the cap. Longer histories are not exposed; do not retry with `days > 365`.

## Categories endpoints

The four endpoints under `/api/v1/categories` expose the Amazon taxonomy (browse nodes) BeyondBSR has ingested per marketplace. They share the same API-key auth, rate limit (`api-key` policy), and `domainId` semantics as book search. All four are `GET`, JSON out, no request body.

### Use cases

- **Resolve a name → `catId`** to pass into `POST /books/search` `categoryIds`. Example: user asks for "manga" books on US → call `/categories/search?domainId=1&q=manga` to get candidate cat_ids, then feed the chosen ones into `categoryIds`.
- **Top-level book categories** of a marketplace (e.g. "list the main Books categories on Amazon.fr"): `GET /categories?domainId=4&depth=2`.
- **Walk down the tree** from a known node (e.g. "what's under Cookbooks?"): `GET /categories/children?domainId=1&catId=6`.
- **Walk up the tree / breadcrumb** for a leaf node (e.g. "where does cat 4142740011 sit?"): `GET /categories/ancestors?domainId=1&catId=4142740011` → returns root → … → node, ordered by depth.

### Shared response object — `CategoryBrowseNodeDto`

| Field             | Type     | Notes                                                                                       |
|-------------------|----------|---------------------------------------------------------------------------------------------|
| `catId`           | long     | Amazon browse node ID. **This is the value to pass into `categoryIds` in book search.**     |
| `parentCatId`     | long?    | Parent's `catId`. `null` for roots.                                                         |
| `rootCatId`       | long     | Top-level ancestor's `catId` (e.g. the Books root for the marketplace).                     |
| `name`            | string   | Localised name in the marketplace's language.                                               |
| `contextFreeName` | string?  | Name without parent context (Keepa-provided). May be null.                                  |
| `depth`           | int      | 0 = root. Top-level book categories are typically depth 2 (root → Categorie → top node).    |
| `isFiction`       | bool     | Internal flag used by `excludeFiction` in book search. Only meaningful at depth=2 under Books root. |
| `productCount`    | int?     | Approximate number of products in that node (Keepa-reported). May be null.                  |

### 1. List categories at a depth (top-level Books browser)

```
GET /api/v1/categories?domainId={..}&depth={0..5}&includeFiction={true|false}
```

| Param            | Type  | Default | Notes                                                                                                                                  |
|------------------|-------|---------|----------------------------------------------------------------------------------------------------------------------------------------|
| `domainId`       | int   | —       | Required. Marketplace ID (1-12, but only `1` US and `4` FR return data).                                                                |
| `depth`          | int?  | 2       | Hierarchy level. 0 = root. 2 = top-level book categories ("Self-Help", "Cookbooks…", etc.). Allowed 0-5.                               |
| `includeFiction` | bool? | `false` | Whether to include nodes flagged as fiction (Literature & Fiction, Romance, Sci-Fi, Children's Books, Teen/YA, Comics, etc.).          |

**Filters applied automatically (do not appear in params):** only browse nodes (`isBrowseNode=true`), and only nodes whose root is the **Books** root of the marketplace — i.e. non-book trees (toys, electronics) are excluded. Use this endpoint to enumerate the canonical KDP-relevant taxonomy.

Order: `productCount` DESC, then `name` ASC.

Response envelope — `CategoriesApiResponse`:

| Field           | Type    | Notes                                |
|-----------------|---------|--------------------------------------|
| `domainId`      | int     | Echo.                                |
| `depth`         | int     | Echo (resolved default if omitted).  |
| `returnedCount` | int     | Number of items in `results`.        |
| `results`       | array   | `CategoryBrowseNodeDto[]`.           |

### 2. Direct children of a category

```
GET /api/v1/categories/children?domainId={..}&catId={..}
```

| Param      | Type | Notes                                                                            |
|------------|------|----------------------------------------------------------------------------------|
| `domainId` | int  | Required.                                                                        |
| `catId`    | long | Required. Parent category's Amazon browse node ID.                               |

**No implicit filters.** Returns ALL active direct children of the parent — including non-browse nodes and fiction nodes. Use it for true tree navigation regardless of book/non-book context.

Order: `productCount` DESC, then `name` ASC.

Returns **404** if `catId` does not exist for the given marketplace. Do not retry on 404.

Response envelope — `CategoryChildrenApiResponse`:

| Field           | Type   | Notes                                |
|-----------------|--------|--------------------------------------|
| `domainId`      | int    | Echo.                                |
| `parentCatId`   | long   | Echo of the input `catId`.           |
| `returnedCount` | int    |                                      |
| `results`       | array  | `CategoryBrowseNodeDto[]`.           |

### 3. Search categories by name

```
GET /api/v1/categories/search?domainId={..}&q={..}&limit={1..200}
```

| Param      | Type    | Default | Notes                                                                                                              |
|------------|---------|---------|--------------------------------------------------------------------------------------------------------------------|
| `domainId` | int     | —       | Required.                                                                                                          |
| `q`        | string  | —       | Required. Case-insensitive substring match on `name`. Min **3** chars, max 100. Wildcards (`%`, `_`, `\`) are treated as literals (escaped server-side). |
| `limit`    | int?    | 50      | 1-200. Pushed down to SQL.                                                                                         |

**No implicit filters.** Searches across the ENTIRE category tree of the marketplace (not just Books) — so a query like "Sports" on Amazon.com will surface both "Sports & Outdoors" (under Books) and the toy/apparel "Sports" nodes. The agent should filter client-side by `rootCatId` if the user only wants book categories.

Order: `productCount` DESC, then `depth` ASC, then `name` ASC.

Response envelope — `CategorySearchApiResponse`:

| Field           | Type   | Notes                                |
|-----------------|--------|--------------------------------------|
| `domainId`      | int    | Echo.                                |
| `query`         | string | Echo of `q`.                         |
| `limit`         | int    | Effective limit applied.             |
| `returnedCount` | int    |                                      |
| `results`       | array  | `CategoryBrowseNodeDto[]`.           |

**Tip:** if the user-typed term is broad (e.g. "fiction") and the default `limit=50` truncates likely candidates, raise `limit` to 200. If still not enough, refine the term or use `/categories?depth=2` instead.

### 4. Ancestors / breadcrumb of a category

```
GET /api/v1/categories/ancestors?domainId={..}&catId={..}
```

| Param      | Type | Notes                                                  |
|------------|------|--------------------------------------------------------|
| `domainId` | int  | Required.                                              |
| `catId`    | long | Required. Category whose breadcrumb to retrieve.       |

Returns the full ancestor chain **including the node itself**, ordered by `depth` ASC. No implicit filters (intermediate non-browse / promotional nodes are included).

Returns **404** if `catId` does not exist for the marketplace.

Response envelope — `CategoryAncestorsApiResponse`:

| Field           | Type   | Notes                                                                |
|-----------------|--------|----------------------------------------------------------------------|
| `domainId`      | int    | Echo.                                                                |
| `catId`         | long   | Echo.                                                                |
| `returnedCount` | int    | Length of the chain (includes the requested node).                   |
| `results`       | array  | `CategoryBrowseNodeDto[]` from root (depth=0) to the node itself.    |

### Example workflows

**Resolve "manga" on Amazon.com then search books** (replace `<catId>` with a candidate returned by step 1):

```bash
# 1. find candidate cat_ids
curl -H "X-API-Key: $BOOKSEARCH_API_KEY" \
  "https://api.beyondbsr.com/api/v1/categories/search?domainId=1&q=manga&limit=10"

# 2. inspect the breadcrumb of a candidate to confirm it's under Books
curl -H "X-API-Key: $BOOKSEARCH_API_KEY" \
  "https://api.beyondbsr.com/api/v1/categories/ancestors?domainId=1&catId=<catId>"

# 3. drill down children if needed
curl -H "X-API-Key: $BOOKSEARCH_API_KEY" \
  "https://api.beyondbsr.com/api/v1/categories/children?domainId=1&catId=<catId>"

# 4. plug the chosen cat_id(s) into book search
curl -X POST -H "X-API-Key: $BOOKSEARCH_API_KEY" -H "Content-Type: application/json" \
  -d '{"domainId":1,"categoryIds":[<catId>],"limit":50}' \
  "https://api.beyondbsr.com/api/v1/books/search"
```

**List top-level Books categories on Amazon.com (non-fiction only, default):**

```bash
curl -H "X-API-Key: $BOOKSEARCH_API_KEY" \
  "https://api.beyondbsr.com/api/v1/categories?domainId=1&depth=2"
```

### Status codes (categories endpoints)

| Code | Meaning                          | Notes                                                                                       |
|------|----------------------------------|---------------------------------------------------------------------------------------------|
| 200  | OK                               | `results` may be empty (e.g. no children, no matches, marketplace not seeded).              |
| 400  | Validation failed                | `ValidationProblemDetails`. Common causes: `domainId` out of range, `q` < 3 chars, `limit` out of 1-200, `depth` out of 0-5. |
| 401  | Auth failed                      | Same handling as book search — stop, report misconfigured key.                              |
| 404  | `catId` not found for `domainId` | `ProblemDetails` JSON (`{title:"Not Found",status:404,...}`). Only on `/children` and `/ancestors`. Do not retry the same pair. |
| 429  | Rate limit                       | Honour `Retry-After`. Same key budget as book search (30 req/min).                          |
| 500  | Server error                     | Retry once, then escalate.                                                                  |

### Caveats

- **Read-only.** No POST/PUT/DELETE on categories.
- **`catId` vs internal id.** The wire contract exposes only Amazon's `catId` (browse node ID). The internal database `id` is never surfaced and is not interchangeable.
- **`depth=2` ≠ "top-level under Books" universally.** Most marketplaces seed Books root at depth=0 → "Categorie/Categories" at depth=1 → top nodes at depth=2. If `/categories?depth=2` returns unexpectedly few rows for a marketplace, retry with `depth=1`.
- **`excludeFiction` semantics propagate.** A node's `isFiction=true` here is exactly what `excludeFiction` in book search rolls up on. If a user complains that a fiction sub-genre isn't being excluded, the agent can spot-check via `/categories/ancestors?catId=…` whether the depth-2 ancestor is flagged.
- **Children endpoint includes non-browse nodes.** Some Amazon nodes are promotional or grouping shells (`isBrowseNode=false`). They cannot be used as `categoryIds` filters in book search. Skip them or warn the user.

## Status codes & error handling

| Code | Meaning                | Body                                       | Agent action                                                                  |
|------|------------------------|--------------------------------------------|-------------------------------------------------------------------------------|
| 200  | OK (may be empty list) | `BookSearchApiResponse`                    | Parse `results`. Empty array = no matches, not an error.                      |
| 400  | Validation failed      | `ValidationProblemDetails` (RFC 7807)      | Read the `errors` map, fix the body, do not retry blindly. Surface the issue. |
| 401  | Auth failed            | empty + `WWW-Authenticate: ApiKey realm="BeyondBSR"` | Stop. Report misconfigured `BOOKSEARCH_API_KEY`. Do not retry.       |
| 429  | Rate limit exceeded    | `"Rate limit exceeded. Please try again later."` + `Retry-After` header | Honour `Retry-After`. Back off. Do not hammer the endpoint. |
| 500  | Unhandled server error | `ProblemDetails` JSON                      | Retry once after a few seconds. If it persists, escalate to the user.         |

### Example 400 body

```json
{
  "type": "https://tools.ietf.org/html/rfc7231#section-6.5.1",
  "title": "One or more validation errors occurred.",
  "status": 400,
  "errors": {
    "DomainId": ["DomainId must be between 1 and 12."],
    "Limit": ["Limit must be between 1 and 300."]
  }
}
```

## Sorting & pagination notes

- Default sort: `ORDER BY <chosen BSR column> ASC` (lower BSR = better seller appears first).
- Historical mode (`bsrType=Historical` + `bsrYear`/`bsrMonth`): sorted by the historical monthly BSR rank ASC.
- Tie-breaker is non-deterministic — books with identical BSR may appear in different orders across page fetches. Warn the user if they need a perfectly stable ordering.
- No `orderBy` parameter is exposed.

## Limits

- **Rate limit**: 30 requests/minute per API key. Shared across all callers using the same key.
- **Body size**: 128 KB max.
- **Page size**: 300 results max per request (`limit ≤ 300`).
- **Offset cap**: 100,000 (deep pagination beyond this is not supported — refine filters instead).

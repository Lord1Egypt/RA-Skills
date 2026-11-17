# consumer-product-opportunity — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**18 endpoints across 5 platform group(s).**

## AliExpress (3)

### `aliexpress_reviews`

- **HTTP:** `GET /aliexpress/reviews`
- **What:** Get AliExpress product reviews. Returns one page of public reviews and rating statistics for a numeric AliExpress product id. AliExpress currently returns up to 20 review records per page.
- **Params:** `page` (integer, optional) — 1-indexed review page (1-50), defaults to 1; `product_id` (string, **required**) — Numeric AliExpress product id

### `aliexpress_search`

- **HTTP:** `GET /aliexpress/search`
- **What:** Search AliExpress products. Returns one page (up to 60 products) of public keyword search results with product ids, titles, links, images, prices, ratings, sold text, discount, SKU id, ship-from country, and store name when AliExpress lists them. Results can be sorted and filtered by price, free shipping, the Choice program, and product attributes; list the attribute values for a keyword with the search-filters endpoint. The search uses the anonymous US English/USD locale. Product-detail pages are currently unavailable through the supported HTTP profiles.
- **Params:** `attr` (string, optional) — Attribute filter <attributeId>-<valueId>, from the search-filters endpoint for the same q; comma-separate up to 5 values, one per attribute group; `cat_id` (integer, optional) — Search within one AliExpress web category id (the number in a /category/<id>/<slug>.html URL); taxonomy ids from the categories endpoint are a different namespace and are not interchangeable; `choice` (boolean, optional) — Only products in AliExpress's Choice program; `free_shipping` (boolean, optional) — Only free-shipping products; `max_price` (number, optional) — Maximum price in USD (0-1000000), not below min_price; `min_price` (number, optional) — Minimum price in USD (0-1000000); `page` (integer, optional) — 1-indexed result page (1-60), defaults to 1; `q` (string, **required**) — Free-text search keywords; `sort` (string, optional) — Sort order. Allowed values: best_match (default), orders, price_asc, price_desc

### `aliexpress_search_filters`

- **HTTP:** `GET /aliexpress/search-filters`
- **What:** List AliExpress search filters. Returns every sort value and boolean filter the search endpoint accepts, plus the product-attribute filters (brand, color, style, and so on) AliExpress offers for the keyword, as ready-to-use attr values. Attribute filters differ per keyword, so call this with the same q as the search.
- **Params:** `q` (string, **required**) — Free-text search keywords

## Amazon (5)

### `amazon_charts`

- **HTTP:** `GET /amazon/charts`
- **What:** Amazon product charts. Returns one page of a ranked Amazon chart (Best Sellers, New Releases, or Most Wished For) for a department or department subcategory on `amazon.com`. Discover valid department/node values with amazon-charts-categories.
- **Params:** `chart` (string, **required**) — Chart type; `department` (string, **required**) — Amazon department slug; `node` (string, optional) — Numeric browse node id; `page` (integer, optional) — 1-based page number

### `amazon_charts_categories`

- **HTTP:** `GET /amazon/charts/categories`
- **What:** Amazon chart categories. Returns the department and subcategory values amazon-charts accepts for a given chart. Omit department to list a chart's top-level departments; pass a department (and optionally a node) to get that category's own name plus its immediate child categories.
- **Params:** `chart` (string, **required**) — Chart type; `department` (string, optional) — Amazon department slug; `node` (string, optional) — Numeric browse node id (requires department)

### `amazon_product`

- **HTTP:** `GET /amazon/product/{asin}`
- **What:** Retrieve Amazon product details. Returns product details for an Amazon ASIN on `amazon.com`, including pricing, availability, overview data, inline review samples, and descriptive content.
- **Params:** `asin` (string, **required**) — Amazon ASIN; `currency` (string, optional) — Amazon currency; `language` (string, optional) — Amazon language

### `amazon_search`

- **HTTP:** `GET /amazon/search`
- **What:** Search Amazon products. Searches `amazon.com` by keyword, with optional sort order and page. Each result card has the ASIN, title, link, image, price and list price, rating and review count, the bought-in-last-month figure, and flags for sponsored placement and free delivery.
- **Params:** `k` (string, **required**) — Search keyword; `page` (integer, optional) — 1-based page number; `s` (string, optional) — Sort order

### `amazon_suggest`

- **HTTP:** `GET /amazon/suggest/{keyword}`
- **What:** Retrieve Amazon search suggestions. Returns Amazon's search-box autocomplete suggestions for a keyword prefix on `amazon.com`, as a plain list of suggested search phrases such as `apple watch bands`.
- **Params:** `keyword` (string, **required**) — Suggestion prefix

## Google (2)

### `google_suggest`

- **HTTP:** `GET /google/suggest`
- **What:** Suggest Google search queries. Returns Google autosuggest query completions from the public unauthenticated suggest JSON endpoint. `source` selects the web, YouTube, or shopping suggestion list, and `rich=true` adds a type, relevance score, and short description to each suggestion.
- **Params:** `count` (integer, optional) — Suggestions to return; defaults to 10, clamped to 1..12; `country` (string, optional) — Google result country; defaults to us; `lang` (string, optional) — Google UI language; defaults to en; `q` (string, **required**) — Search query prefix; `rich` (boolean, optional) — Add Google's type, relevance score, and description to each suggestion; defaults to false; `source` (string, optional) — Suggestion source; defaults to web

### `google_trends_explore_interest_over_time`

- **HTTP:** `POST /google/trends/explore/interest-over-time`
- **What:** Google Trends interest over time. Returns Google Trends interest over time for 1 to 5 `keywords`. Optional inputs are `geo` (default worldwide), `time_range` (default `today 12-m`), `hl`, `tz`, `category` and `type` (`web`, `image`, `news`, `youtube` or `shopping`). Each time point carries a value per keyword, with a `has_data` flag.
- **Params:** `request` (object, **required**) — Explore request
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

## Jumia (5)

### `jumia_categories`

- **HTTP:** `GET /jumia/categories`
- **What:** List Jumia categories. Lists the category slugs that jumia-category accepts. Without category it returns the storefront's top-level departments; with category it returns that category's direct sub-categories, each with its numeric id. Walk the tree by passing a returned slug back as category. country is required; see jumia-countries. Jumia sits behind an anti-bot challenge that clears on only some connections, so a call can take up to about 50 seconds and may return 503; retry it.
- **Params:** `category` (string, optional) — Category slug whose sub-categories to list; omit for top-level departments; `country` (string, **required**) — Jumia country storefront

### `jumia_category`

- **HTTP:** `GET /jumia/category`
- **What:** Browse a Jumia category. Browses one Jumia category listing by slug and returns the same product cards as jumia-search, plus the category's upstream total_count and a has_next flag. Take the slug from jumia-categories (top-level departments, or a department's sub-categories). Jumia serves at most 50 pages. Jumia sits behind an anti-bot challenge that clears on only some connections, so a call can take up to about 50 seconds and may return 503; retry it. country is required; see jumia-countries.
- **Params:** `category` (string, **required**) — Category slug from jumia-categories; `country` (string, **required**) — Jumia country storefront; `page` (integer, optional) — 1-based result page, 1 to 50

### `jumia_countries`

- **HTTP:** `GET /jumia/countries`
- **What:** List supported Jumia country storefronts. Returns the Jumia country storefronts accepted by the country parameter on jumia-search, jumia-category and jumia-categories, with each storefront's domain and currency. Static metadata.
- **Params:** _none_

### `jumia_product`

- **HTTP:** `GET /jumia/product`
- **What:** Get a Jumia product. Returns one Jumia product: name, brand, sku, images, price in the storefront's currency with original price and discount, availability, rating and rating count, category path, seller (name, id, score, followers, shipping speed), description, key features and the specification table. Pass the url returned by jumia-search or jumia-category; the storefront country is taken from the URL host. Jumia sits behind an anti-bot challenge that clears on only some connections, so a call can take up to about 50 seconds and may return 503; retry it. A product id Jumia no longer serves returns 404.
- **Params:** `url` (string, **required**) — Absolute Jumia product URL from a search or category result

### `jumia_search`

- **HTTP:** `GET /jumia/search`
- **What:** Search Jumia products. Searches a Jumia country storefront by keyword and returns one page of product cards with price in the storefront's currency, original price and discount, rating, brand, categories and badges, plus the upstream total_count and a has_next flag. Jumia serves at most 50 pages. A search with no matches returns an empty products list. Jumia sits behind an anti-bot challenge that clears on only some connections, so a call can take up to about 50 seconds and may return 503; retry it. country is required (there is no default storefront); see jumia-countries.
- **Params:** `country` (string, **required**) — Jumia country storefront; `page` (integer, optional) — 1-based result page, 1 to 50; `q` (string, **required**) — Product search keyword

## Reddit (3)

### `reddit_comments`

- **HTTP:** `GET /reddit/comments/{id}`
- **What:** Get Reddit post comments. Returns a Reddit post with its public comments. The default mode is 1 credit. Set `include_metrics=true` to return the comments with public net score and award count plus post engagement metrics for 3 credits. Large threads may expose only an initial comment subset. Reddit does not expose per-comment upvote ratios or exact upvote/downvote totals anonymously. A post that exists but has no comments yet returns a 200 response with an empty comments list; a post that does not exist returns 404, and a temporary block or upstream failure returns 503 (retryable) rather than 404. If source.type is redlib, public fields and credit weights are preserved.
- **Params:** `depth` (integer, optional) — Maximum flat comment depth returned in metrics mode.; `id` (string, **required**) — Reddit post id or t3_ id; `include_metrics` (boolean, optional) — Include public post and per-comment engagement metrics; costs 3 credits instead of 1; `limit` (integer, optional) — Maximum comments returned, defaults to 25 and clamps to 100; `sort` (string, optional) — Comment order: confidence, top, new, controversial, old, or qa. Applied to the anonymous HTML request when metrics are enabled.

### `reddit_post`

- **HTTP:** `GET /reddit/post/{id}`
- **What:** Get Reddit post. Returns a public Reddit post. The default mode is 1 credit. Set `include_metrics=true` to return public net score, upvote ratio, comment count, award count, and estimated upvote/downvote totals for 3 credits. Reddit fuzzes voting data, so estimates are approximate; share, repost/crosspost, and view counts are not exposed anonymously. If source.type is redlib, public fields and credit weights are preserved.
- **Params:** `id` (string, **required**) — Reddit post id or t3_ id; `include_metrics` (boolean, optional) — Include public engagement metrics; costs 3 credits instead of 1

### `reddit_search`

- **HTTP:** `GET /reddit/search`
- **What:** Search Reddit posts. Searches public Reddit content and returns public post entries. A `503` with a `Retry-After` header means Reddit is temporarily throttling the request; wait that many seconds and retry. If source.type is redlib, public fields and credit weights are preserved.
- **Params:** `after` (string, optional) — Reddit pagination token; `limit` (integer, optional) — Maximum posts, defaults to 25 and clamps to 100; `q` (string, **required**) — Search keywords; `sort` (string, optional) — Sort: relevance, hot, new, top, or comments; `subreddit` (string, optional) — Restrict search to a subreddit name, without r/; `time` (string, optional) — Time window for top/comments sorts: hour, day, week, month, year, or all

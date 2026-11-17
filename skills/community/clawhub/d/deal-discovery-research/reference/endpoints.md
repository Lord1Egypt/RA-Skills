# deal-discovery-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**24 endpoints across 2 platform group(s).**

## Slickdeals (11)

### `slickdeals_categories`

- **HTTP:** `GET /slickdeals/categories`
- **What:** List every Slickdeals deal category/tag. Returns Slickdeals' own full category/tag list -- the discovery endpoint for GET /slickdeals/category's slug parameter. This is a separate taxonomy from the category/sub_category fields GET /slickdeals/deal returns for an individual deal (Slickdeals maintains multiple parallel category/tag id spaces, not one) -- these slugs are the ones GET /slickdeals/category's own browse pages accept. The list is refreshed from Slickdeals' own site periodically; an optional q parameter narrows it to a substring match.
- **Params:** `q` (string, optional) — Case-insensitive substring filter on slug or name

### `slickdeals_category`

- **HTTP:** `GET /slickdeals/category`
- **What:** Browse current deals in one Slickdeals category/tag. Returns the current deal listing for one Slickdeals category/tag (e.g. "laptop-bag", "apparel"): for each deal, title, price, list price, store, community vote score, comment count, the public username who posted it, and status flags (is_popular, is_expired, is_new, is_frontpage). slug must be one of the values from GET /slickdeals/categories -- an unrecognized slug returns a typed invalid-parameter error rather than being sent upstream. Pair a result's thread_id or url with GET /slickdeals/deal for the full detail record (description, full taxonomy).
- **Params:** `slug` (string, **required**) — Category/tag slug from GET /slickdeals/categories

### `slickdeals_comments`

- **HTTP:** `GET /slickdeals/comments`
- **What:** Get one Slickdeals deal thread's comments. Returns one Slickdeals deal thread's full comment thread: for each comment, the public username who posted it (with their forum rank/title and total post count), the comment content (as HTML and as cleaned plain text), when it was posted, a permalink, and reaction counts (like, funny, helpful, not helpful). Give either url (the exact value returned by GET /slickdeals/search or GET /slickdeals/deal) or thread_id; at least one is required. has_more indicates whether Slickdeals' own page truncated the reply list (no further pagination is currently exposed by this endpoint).
- **Params:** `thread_id` (integer, optional) — Slickdeals numeric thread id; `url` (string, optional) — Full Slickdeals deal URL, as returned by GET /slickdeals/search or GET /slickdeals/deal (https://slickdeals.net/f/...)

### `slickdeals_deal`

- **HTTP:** `GET /slickdeals/deal`
- **What:** Get one Slickdeals deal thread's full detail. Returns one Slickdeals deal thread's full detail: title, store, final/list price, community vote score, comment count, whether the deal is marked expired, the deal's product category and taxonomy (category/sub_category/category_paths, and separately the legacy forum/forum_id the thread was posted under), the public Slickdeals username who posted it ("found by" attribution) with a public community-standing summary (reputation, join date, deals posted, total votes/comments), a related_deals sidebar (Slickdeals' own Popular/Trending picks), the outbound merchant link, and the deal's own description. Give either url (the exact value returned by GET /slickdeals/search) or thread_id (Slickdeals' own numeric thread id, e.g. from a deal's URL path /f/{thread_id}-...); at least one is required. An unknown or removed deal returns 404.
- **Params:** `thread_id` (integer, optional) — Slickdeals numeric thread id; `url` (string, optional) — Full Slickdeals deal URL, as returned by GET /slickdeals/search (https://slickdeals.net/f/...)

### `slickdeals_deal_types`

- **HTTP:** `GET /slickdeals/deal-types`
- **What:** List every Slickdeals deal-type tag. Returns Slickdeals' own deal-type tag list (Coupon, Free / Freebie, Giveaway, Gift Card, Mail In Rebate, Online Only, YMMV, ...) -- the discovery endpoint for GET /slickdeals/search's deal_type_id parameter. Confirmed identical across multiple Slickdeals sub-forums, unlike the broader interest-tag space it is drawn from, which was not found to be reliably enumerable. An optional q parameter narrows it to a substring match on name.
- **Params:** `q` (string, optional) — Case-insensitive substring filter on name

### `slickdeals_forums`

- **HTTP:** `GET /slickdeals/forums`
- **What:** List every Slickdeals legacy sub-forum. Returns Slickdeals' own full legacy sub-forum list (e.g. Hot Deals, Coupons, Freebies) -- the discovery endpoint for GET /slickdeals/search's forum_id parameter. A separate, coarser-grained taxonomy from GET /slickdeals/categories' 421-entry tag list: this is the classification GET /slickdeals/deal, /slickdeals/search/advanced, and /slickdeals/frontpage already surface as forum_id, with this endpoint as the way to resolve an id to a name or filter search results by it. The list is refreshed from Slickdeals' own site periodically; an optional q parameter narrows it to a substring match on name.
- **Params:** `q` (string, optional) — Case-insensitive substring filter on name

### `slickdeals_frontpage`

- **HTTP:** `GET /slickdeals/frontpage`
- **What:** Browse Slickdeals' own homepage deal feed. Returns one page of Slickdeals' own homepage deal listing -- the deals Slickdeals itself is currently featuring, distinct from a keyword search or a single category/tag's own listing. Each deal carries the same fields as GET /slickdeals/search/advanced's results (real integer vote/comment/view counts, store id, discount, status flags), plus is_fire_deal and has_rebate flags this feed's cards carry. Pagination is next-page-only (has_next_page), since the page itself exposes no total page count.
- **Params:** `page` (integer, optional) — 1-based frontpage listing page, default 1

### `slickdeals_primary_categories`

- **HTTP:** `GET /slickdeals/primary-categories`
- **What:** List Slickdeals' featured primary-category landing pages. Returns Slickdeals' small, curated set of "featured" primary-category landing pages (e.g. laptop-deals, tv-deals) -- the discovery endpoint for GET /slickdeals/primary-category's slug parameter. This is a separate taxonomy from GET /slickdeals/categories' 421-entry tag list and from GET /slickdeals/deal's own category/sub_category fields -- Slickdeals maintains multiple parallel category/tag id spaces, not one. Unlike /slickdeals/categories, no single live page enumerates this set; it is maintained as periodically-refreshed reference data.
- **Params:** `q` (string, optional) — Case-insensitive substring filter on slug or name

### `slickdeals_primary_category`

- **HTTP:** `GET /slickdeals/primary-category`
- **What:** Browse current deals in one Slickdeals featured primary category. Returns the current deal listing for one Slickdeals featured primary-category landing page (e.g. laptop-deals, tv-deals): for each deal, title, price, list price, store, community vote score, comment count, found-by username, and status flags. slug must be one of the values from GET /slickdeals/primary-categories -- an unrecognized slug (including a valid GET /slickdeals/categories tag slug, which is a different taxonomy) returns a typed invalid-parameter error rather than being sent upstream.
- **Params:** `slug` (string, **required**) — Featured-category slug from GET /slickdeals/primary-categories

### `slickdeals_search`

- **HTTP:** `GET /slickdeals/search`
- **What:** Search Slickdeals community-submitted deals by keyword. Searches Slickdeals (slickdeals.net), a community deal/coupon aggregator, for deal threads matching a free-text keyword query. Each result is one community-submitted deal thread with its title (which conventionally embeds the deal price), a best-effort price extracted from that title, the merchant domain, the community vote ("thumb") score, the public Slickdeals username who posted it, and when it was posted. Pair a result's thread_id or url with GET /slickdeals/deal for the full detail record, including comment count and category. An optional forum_id restricts results to one Slickdeals legacy sub-forum (e.g. Hot Deals, Coupons) -- obtain a value from GET /slickdeals/forums, a closed enum validated before the request is made. An optional deal_type_id restricts results to one Slickdeals deal-type tag (e.g. Coupon, Free / Freebie, YMMV) -- obtain a value from GET /slickdeals/deal-types, also a closed enum validated before the request is made; composes with forum_id.
- **Params:** `deal_type_id` (integer, optional) — Restrict results to one Slickdeals deal-type tag, from GET /slickdeals/deal-types; `forum_id` (integer, optional) — Restrict results to one Slickdeals legacy sub-forum, from GET /slickdeals/forums; `q` (string, **required**) — Free-text keyword query

### `slickdeals_search_advanced`

- **HTTP:** `GET /slickdeals/search/advanced`
- **What:** Search Slickdeals with real pagination, counts, and facets. Searches Slickdeals' modern search surface -- a richer alternative to GET /slickdeals/search's keyword-only search. Returns real pagination (page/total_pages/per_page/result_count), integer vote/comment/view counts (not parsed from free text), a fuller per-deal record (store id, discount percent, status flags), and facets -- Categories, Stores, and Brands available for the current query, each option carrying a value usable as category_id/brand_id/store_id. Facet values and counts are scoped to the current query, not a site-wide enumeration -- category_id/brand_id/store_id are passthrough filters (obtain a value from a prior response's own facets), not validated against a closed enum. sort defaults to relevance; other values are passed through unvalidated.
- **Params:** `brand_id` (integer, optional) — Brand facet id, from a prior response's own facets; `category_id` (integer, optional) — Category facet id, from a prior response's own facets; `page` (integer, optional) — 1-based result page, default 1; `q` (string, **required**) — Free-text keyword query; `sort` (string, optional) — Sort order, default relevance; `store_id` (integer, optional) — Store facet id, from a prior response's own facets

## RetailMeNot (13)

### `retailmenot_autocomplete`

- **HTTP:** `GET /retailmenot/autocomplete`
- **What:** Get RetailMeNot search suggestions. Returns RetailMeNot's search-box suggestions for a free-text term: matching stores (with domains usable with /retailmenot/store) and cash-back offers. Group names are returned as data.
- **Params:** `term` (string, **required**) — Store or brand search term

### `retailmenot_blog_categories`

- **HTTP:** `GET /retailmenot/blog-categories`
- **What:** List RetailMeNot blog categories. Returns every category of RetailMeNot's shopping and savings blog with its slug, post count, description, and URL. Use a slug as the category filter of /retailmenot/blog-posts.
- **Params:** _none_

### `retailmenot_blog_post`

- **HTTP:** `GET /retailmenot/blog-post`
- **What:** Get a RetailMeNot blog post. Returns one RetailMeNot blog post: metadata (title, author, dates, description, image, categories, tags), the article text as headed sections of paragraphs and lists, and the RetailMeNot stores and coupon categories the article links to (usable with /retailmenot/store and /retailmenot/category).
- **Params:** `slug` (string, **required**) — Post slug from /retailmenot/blog-posts (a trailing .html is accepted)

### `retailmenot_blog_posts`

- **HTTP:** `GET /retailmenot/blog-posts`
- **What:** List RetailMeNot blog posts. Returns one page of RetailMeNot blog posts (title, slug, URL, excerpt, description, author, published and modified dates, image, categories, and tags) with total and total pages, newest first by default. Filter by category slug, tag slug, and/or a search query; order by date, modified, title, or relevance (relevance requires query). A page past the end returns an empty list.
- **Params:** `category` (string, optional) — Category slug from /retailmenot/blog-categories; `order` (string, optional) — Sort direction; `order_by` (string, optional) — Sort field; `page` (integer, optional) — Page number, starting at 1; `page_size` (integer, optional) — Posts per page (1-100); `query` (string, optional) — Search post text; `tag` (string, optional) — Tag slug from /retailmenot/blog-tags

### `retailmenot_blog_tags`

- **HTTP:** `GET /retailmenot/blog-tags`
- **What:** List RetailMeNot blog tags. Returns one page of RetailMeNot blog tags ordered by post count, with slug, name, post count, and URL, plus total and total pages; optionally only tags matching a query. Use a slug as the tag filter of /retailmenot/blog-posts.
- **Params:** `page` (integer, optional) — Page number, starting at 1; `page_size` (integer, optional) — Tags per page (1-100); `query` (string, optional) — Match tag names

### `retailmenot_cashback`

- **HTTP:** `GET /retailmenot/cashback`
- **What:** List RetailMeNot cash-back offers. Lists the offers on RetailMeNot's cash-back page, grouped into sections such as Today's Featured Cash Back, Top Cash Back and All Cash Back Offers. Each offer has its position, store name, domain and RetailMeNot URL, the cash-back rate in `discount`, and a title. It takes no parameters.
- **Params:** _none_

### `retailmenot_categories`

- **HTTP:** `GET /retailmenot/categories`
- **What:** List RetailMeNot coupon categories. Lists RetailMeNot's coupon category tree as a flat list with no parameters. Each entry has `name`, `slug`, `url` and `level` (1 parent, 2 child, 3 grandchild); levels 2 and 3 also carry `parent_slug`. The `slug` is what RetailMeNot's category endpoint takes.
- **Params:** _none_

### `retailmenot_category`

- **HTTP:** `GET /retailmenot/category`
- **What:** Get a RetailMeNot category's offers. Returns one page of a RetailMeNot category landing page: the featured offers across stores (24 per page, with page and total_pages), offer counts, and similar stores. Use a slug from /retailmenot/categories; a page past the end returns an empty offer list.
- **Params:** `page` (integer, optional) — Offer page (24 offers per page; see total_pages); `slug` (string, **required**) — Category slug from /retailmenot/categories

### `retailmenot_deal_event`

- **HTTP:** `GET /retailmenot/deal-event`
- **What:** Get a RetailMeNot deal event's offers. Returns one seasonal deal event page's offers grouped into the page's sections (top deals and per-category sections). Use a slug from /retailmenot/deal-events.
- **Params:** `slug` (string, **required**) — Event slug from /retailmenot/deal-events

### `retailmenot_deal_events`

- **HTTP:** `GET /retailmenot/deal-events`
- **What:** List RetailMeNot seasonal deal events. Lists the seasonal and holiday deal events linked from RetailMeNot's deals hub, such as Black Friday or Back-to-School, each with `name`, `slug` and `url`. The `slug` feeds the deal-event endpoint. Out-of-season events may list fewer offers. It takes no parameters.
- **Params:** _none_

### `retailmenot_home`

- **HTTP:** `GET /retailmenot/home`
- **What:** Get RetailMeNot's homepage offers. Returns RetailMeNot's homepage: featured offer sections (cash-back stores with rates, seasonal savings deals with store, offer type, discount, and title), today's top product deals (title, discount, image, and retailer product URL), and the help FAQ.
- **Params:** _none_

### `retailmenot_store`

- **HTTP:** `GET /retailmenot/store`
- **What:** Get a RetailMeNot store's coupons and offers. Returns a store's RetailMeNot page: store details, shopper rating, category, offer counts, every listed coupon, sale, cash-back, and in-store offer (including the offers behind the page's "show more" button), similar stores, and FAQs. Coupon codes are only revealed on RetailMeNot after a click and are not returned. Set market=ca for a RetailMeNot Canada store page.
- **Params:** `domain` (string, **required**) — Store domain or RetailMeNot store URL; `market` (string, optional) — us for RetailMeNot, ca for RetailMeNot Canada (stores from /retailmenot/stores with market=ca)

### `retailmenot_stores`

- **HTTP:** `GET /retailmenot/stores`
- **What:** List RetailMeNot stores by letter. Returns every store in one letter of RetailMeNot's A-Z store directory, or of RetailMeNot Canada's store list with market=ca, with the domain to pass to /retailmenot/store (with the same market).
- **Params:** `letter` (string, **required**) — Directory letter; `market` (string, optional) — us for RetailMeNot, ca for RetailMeNot Canada

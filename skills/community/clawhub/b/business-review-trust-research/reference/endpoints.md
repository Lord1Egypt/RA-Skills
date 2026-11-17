# business-review-trust-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**49 endpoints across 6 platform group(s).**

## ProductHunt (11)

### `producthunt_about`

- **HTTP:** `GET /producthunt/product/{id}/about`
- **What:** Retrieve Product Hunt product about page. Returns the about-page data for a Product Hunt product, looked up by its slug in `id`. It covers the product's launch details with badges, ranks, comment count and detailed reviews with alternative products, along with the product's ad, forum and media information.
- **Params:** `id` (string, **required**) — Product Hunt slug

### `producthunt_alternatives`

- **HTTP:** `GET /producthunt/product/{id}/alternatives`
- **What:** Retrieve Product Hunt product alternatives. Lists alternatives to a Product Hunt product, looked up by its slug in `id`. `first` sets the page size (default 10), `order` defaults to `most_relevant`, and `tags` takes comma-separated tag slugs. Returns alternative items with ratings, badges and scores, alternative tags with counts, and related discussions. Use `end_cursor` as `cursor` for the next page.
- **Params:** `cursor` (string, optional) — Pagination cursor; `first` (integer, optional) — Page size; `id` (string, **required**) — Product Hunt slug; `order` (string, optional) — Sort order; `tags` (string, optional) — Comma-separated tag slugs

### `producthunt_category`

- **HTTP:** `GET /producthunt/category/{slug}`
- **What:** Retrieve Product Hunt category details. Returns a Product Hunt category by its `slug`, such as `vibe-coding`: name, description, meta title, last update time, parent category and its sub-categories, hero products, questions with top answers, and related discussions.
- **Params:** `slug` (string, **required**) — Product Hunt category slug

### `producthunt_category_products`

- **HTTP:** `GET /producthunt/category/{slug}/products`
- **What:** Retrieve Product Hunt category products. Returns the products in a Product Hunt category (now backed by Product Hunt topics), cursor-paginated. Pass the `cursor` from a previous response's `end_cursor` to page; `page_size` controls the batch size. `page`, `featured_only`, `order` and `tags` are accepted for compatibility but no longer affect the result.
- **Params:** `cursor` (string, optional) — Pagination cursor from a previous response's end_cursor; `featured_only` (boolean, optional) — Accepted for compatibility; no longer affects results; `order` (string, optional) — Accepted for compatibility; no longer affects results; `page` (integer, optional) — Accepted for compatibility; use cursor to paginate; `page_size` (integer, optional) — Page size (number of products); `slug` (string, **required**) — Product Hunt category slug; `tags` (string, optional) — Accepted for compatibility; no longer affects results

### `producthunt_customers`

- **HTTP:** `GET /producthunt/product/{id}/customers`
- **What:** Retrieve Product Hunt product customers. Lists the customer products of a Product Hunt product, looked up by its slug in `id`. `order` is `customers` (default) or `latest_launch`, `page` defaults to 1 and `page_size` to 10. Each item has its name, categories, badges, review and follower counts, and founder shoutouts. An unknown slug returns 404.
- **Params:** `id` (string, **required**) — Product Hunt slug; `order` (string, optional) — Product Hunt customers order; `page` (integer, optional) — Page number; `page_size` (integer, optional) — Results per page

### `producthunt_launches`

- **HTTP:** `GET /producthunt/product/{id}/launches`
- **What:** Retrieve Product Hunt product launches. Lists the launch posts of a Product Hunt product, looked up by its slug in `id`. `order` defaults to `DATE`; pass the returned `end_cursor` as `cursor` for the next page. Each launch has its name, tagline, ranks, scores, comment count, badges and dates. An unknown slug returns 404.
- **Params:** `cursor` (string, optional) — Pagination cursor; `id` (string, **required**) — Product Hunt slug; `order` (string, optional) — Product Hunt launch order

### `producthunt_leaderboard`

- **HTTP:** `GET /producthunt/leaderboard`
- **What:** Retrieve Product Hunt leaderboard. Returns the Product Hunt leaderboard for a `scope` of `daily` (default), `weekly`, `monthly` or `yearly`, positioned with `date` (YYYY-MM-DD) or `year`, `month`, `day` and `week`. Only the first page is served, so a non-empty `cursor` returns an error. `featured` and `order` are accepted but do not change the default view.
- **Params:** `cursor` (string, optional) — Pagination cursor; `date` (string, optional) — Anchor date in YYYY-MM-DD format. Used to derive missing year/month/day/week values.; `day` (integer, optional) — Daily day override; `featured` (boolean, optional) — Featured products only; `month` (integer, optional) — Daily/monthly month override; `order` (string, optional) — Ranking order override. Defaults to scope rank enum.; `scope` (string, optional) — Leaderboard scope: daily, weekly, monthly, yearly; `week` (integer, optional) — Weekly ISO week override; `year` (integer, optional) — Leaderboard year override

### `producthunt_makers`

- **HTTP:** `GET /producthunt/product/{id}/makers`
- **What:** Retrieve Product Hunt product makers. Lists the makers of a Product Hunt product, looked up by its slug in `id`. Each maker has a name, username, headline, avatar, follower count and the posts they made. The response includes `total_count` and claim status, and the returned `end_cursor` can be passed as `cursor` for the next page.
- **Params:** `cursor` (string, optional) — Pagination cursor; `id` (string, **required**) — Product Hunt slug

### `producthunt_product`

- **HTTP:** `GET /producthunt/product/{id}`
- **What:** Retrieve Product Hunt product details. Returns the core Product Hunt product details. The path takes an exact Product Hunt slug; if you only know the product name, look the slug up first with `/producthunt/search` (live) or `/datasets/producthunt-products/search` (indexed). Unknown slugs return 404, and that 404 is cached for 24 hours.
- **Params:** `id` (string, **required**) — Product Hunt slug or numeric ID

### `producthunt_reviews`

- **HTTP:** `GET /producthunt/product/{id}/reviews`
- **What:** Retrieve Product Hunt product detailed reviews. Lists the detailed reviews of a Product Hunt product, looked up by its slug in `id`. Each review has its ratings, such as ease of use and customization, comment count, creation time, the launch it came from and any alternative products named. The response also gives the review counts and an `end_cursor`.
- **Params:** `id` (string, **required**) — Product Hunt slug

### `producthunt_search`

- **HTTP:** `GET /producthunt/search`
- **What:** Search for products, users, or launches on Product Hunt. Searches Product Hunt for the required `query`. `type` is `product` (default), `user` or `launch`, and `page` starts at 1. `featured` and `topics` apply to launch search only. Results come as `edges` with `pageInfo` and `pagesCount`; launch search also returns topic aggregations.
- **Params:** `featured` (boolean, optional) — Launch search only: featured launches only; `page` (integer, optional) — Page number (1-based); `query` (string, **required**) — Search keywords; `topics` (string, optional) — Launch search only: comma-separated topic slugs; `type` (string, optional) — Result type: **product** (default), **user**, or **launch**

## TrustMRR (7)

### `trustmrr_acquire`

- **HTTP:** `GET /trustmrr/acquire`
- **What:** Get TrustMRR acquisition listings. Returns the for-sale startups rendered on the public TrustMRR /acquire marketplace page, with deal metrics (asking price, revenue, multiple, growth). Verified revenue figures come from supported payment providers.
- **Params:** _none_

### `trustmrr_categories`

- **HTTP:** `GET /trustmrr/categories`
- **What:** Get TrustMRR categories. Lists the TrustMRR startup categories, with the total `count`. Each category has its `slug`, `label`, short label, icon name, description, keywords and TrustMRR URL. Pass a category `slug` to `/trustmrr/category/{slug}` to list the startups in it.
- **Params:** _none_

### `trustmrr_category`

- **HTTP:** `GET /trustmrr/category/{slug}`
- **What:** Get TrustMRR category detail. Returns one TrustMRR category by `slug` (lowercase letters, digits and hyphens, for example `saas`) with the startups listed in it. Each startup has its name, slug, URL, description, current MRR, total revenue and last-30-days revenue, all in USD, plus the `on_sale` flag for startups listed for sale. Valid slugs come from `/trustmrr/categories`.
- **Params:** `slug` (string, **required**) — TrustMRR category slug

### `trustmrr_leaderboard`

- **HTTP:** `GET /trustmrr/leaderboard`
- **What:** Get TrustMRR revenue leaderboard. Returns the top 100 startups ranked by the selected metric from the public TrustMRR leaderboard. Revenue and MRR figures are verified through supported payment providers.
- **Params:** `metric` (string, optional) — Leaderboard metric to rank by (default mrr)

### `trustmrr_marketplace`

- **HTTP:** `GET /trustmrr/marketplace`
- **What:** Get TrustMRR marketplace snapshot. Returns the public TrustMRR marketplace snapshot: the 25 most recently listed startups for sale and the current 25 best deals ranked by TrustMRR's recency-aware deal score. Revenue figures are verified through supported payment providers.
- **Params:** _none_

### `trustmrr_startup`

- **HTTP:** `GET /trustmrr/startup/{slug}`
- **What:** Get TrustMRR startup detail. Returns the full verified profile for a single TrustMRR startup by slug: revenue and MRR, growth, asking price and marketplace status, tech stack, marketing channels, and TrustMRR's AI-generated business summary.
- **Params:** `slug` (string, **required**) — TrustMRR startup slug

### `trustmrr_startups`

- **HTTP:** `GET /trustmrr/startups`
- **What:** List all TrustMRR startups. Returns a paginated list of every startup in the TrustMRR directory. Each entry is a slug you can pass to /trustmrr/startup/{slug} for the full verified profile — together these two endpoints let you enumerate the entire directory.
- **Params:** `page` (integer, optional) — 1-based page number (default 1); `page_size` (integer, optional) — Items per page (default 100, max 1000)

## Trustpilot (7)

### `trustpilot_business`

- **HTTP:** `GET /trustpilot/business/{slug}`
- **What:** Get Trustpilot business profile. Returns a Trustpilot business profile by `slug`, such as `openai.com`. The profile has the name, `trust_score`, `review_count`, rating histogram, review summary and topics, categories, claimed status, website URL, reply metrics, company activity and verification flags, and an about section with description and contact details.
- **Params:** `slug` (string, **required**) — Trustpilot business slug

### `trustpilot_business_related`

- **HTTP:** `GET /trustpilot/business/{slug}/related`
- **What:** Get Trustpilot related businesses. Returns the businesses Trustpilot shows as related to a given business slug such as `openai.com`. Each related business has its display name, identifying name, logo, star rating, TrustScore, review count and Trustpilot URL; the response also includes a summary of the business you asked about.
- **Params:** `slug` (string, **required**) — Trustpilot business slug

### `trustpilot_business_reviews`

- **HTTP:** `GET /trustpilot/business/{slug}/reviews`
- **What:** Get Trustpilot business reviews. Returns one page of Trustpilot reviews for a business slug such as `openai.com`, with filters for star rating, verified reviews, reviews with a company reply, language and text search. Each review has its rating, title, body, author name, country and review count, dates, and any company reply; the response also carries the business summary and pagination totals.
- **Params:** `date_from` (string, optional) — Date range start in YYYY-MM-DD; currently rejected by upstream; `date_to` (string, optional) — Date range end in YYYY-MM-DD; currently rejected by upstream; `language` (string, optional) — Review language code used by Trustpilot; `page` (integer, optional) — 1-based page number; defaults to 1; `q` (string, optional) — Text search within reviews; `replied` (boolean, optional) — Filter to reviews with business replies; `slug` (string, **required**) — Trustpilot business slug; `stars` (integer, optional) — Filter by star rating from 1 to 5; `verified` (boolean, optional) — Filter to verified reviews

### `trustpilot_business_search`

- **HTTP:** `GET /trustpilot/business-units/search`
- **What:** Search Trustpilot business units. Searches Trustpilot for businesses matching a query, for a country (default `US`), with `page` and `page_size` (default 20, max 100). Each result has the display name, identifying name, TrustScore, star rating, review count, categories, website, email, phone, address and Trustpilot URL; `total_hits` gives the full match count.
- **Params:** `country` (string, optional) — Two-letter country code; defaults to US; `page` (integer, optional) — 1-based page number; defaults to 1; `page_size` (integer, optional) — Results per page; defaults to 20, maximum 100; `q` (string, **required**) — Search query

### `trustpilot_categories`

- **HTTP:** `GET /trustpilot/categories`
- **What:** Get Trustpilot categories. Lists the Trustpilot category index grouped by top-level category. Each group has its name, slug and URL, and an `items` list of subcategories with their own name, slug and URL. It takes no parameters.
- **Params:** _none_

### `trustpilot_category`

- **HTTP:** `GET /trustpilot/category/{slug}`
- **What:** Get Trustpilot category detail. Returns a Trustpilot category by `slug` (for example `software_company`), with the companies listed on one page; `page` is 1-based and defaults to 1. Each company has its display name, `identifying_name`, `trust_score`, `stars`, `review_count`, location, contact details, categories and Trustpilot URL. Also returns breadcrumbs, newest companies and `pagination.has_next_page`.
- **Params:** `page` (integer, optional) — 1-based page number; defaults to 1; `slug` (string, **required**) — Trustpilot category slug

### `trustpilot_category_search`

- **HTTP:** `GET /trustpilot/categories/search`
- **What:** Search Trustpilot categories. Searches Trustpilot categories for the required `q`. `size` sets the maximum number of categories (default 20, from 1 to 100), `country` is a two-letter code (default US) and `locale` uses `ll-CC` format (default `en-US`). Each category has its `category_id`, `display_name` and `top_level_category_id`.
- **Params:** `country` (string, optional) — Two-letter country code; defaults to US; `locale` (string, optional) — Locale in ll-CC format; defaults to en-US; `q` (string, **required**) — Search query; `size` (integer, optional) — Maximum number of categories; defaults to 20

## Capterra (3)

### `capterra_product`

- **HTTP:** `GET /capterra/product`
- **What:** Get a Capterra product. Returns a Capterra product profile: name, description, category, and aggregate rating.
- **Params:** `product_id` (string, **required**) — Capterra product id (the numeric id in a /p/{id}/{slug}/ URL)

### `capterra_reviews`

- **HTTP:** `GET /capterra/product/reviews`
- **What:** Get Capterra product reviews. Returns a page of Capterra reviews (author, headline, rating) plus the product's aggregate rating.
- **Params:** `page` (integer, optional) — Page number (default 1); `product_id` (string, **required**) — Capterra product id (the numeric id in a /p/{id}/{slug}/ URL)

### `capterra_search`

- **HTTP:** `GET /capterra/search`
- **What:** Search Capterra products. Returns Capterra search-result products (id, name, url, description, rating). Note: Capterra renders a fallback product list even for queries with no genuine match, rather than a distinct empty-results page, so callers should treat low-relevance results as an upstream characteristic, not a bug.
- **Params:** `q` (string, **required**) — Search query

## BBB (17)

### `bbb_article`

- **HTTP:** `GET /bbb/article`
- **What:** Get a BBB article. Returns published BBB article metadata, author names, body text, and useful links from a canonical public article URL on www.bbb.org or bbb.org. If BBB merges a story into another BBB article, the response contains the target article's id and source_url plus the original requested_url. Returns a permanent 404 when BBB moves the URL to an evergreen /all/ page or outside bbb.org, when BBB redirects the URL back to itself so it cannot be loaded, or when the URL resolves to a published non-article type such as an event; safe HTTPS destinations are named in the error and are never fetched.
- **Params:** `url` (string, **required**) — Canonical BBB article URL on www.bbb.org or bbb.org

### `bbb_business`

- **HTTP:** `GET /bbb/business`
- **What:** Get a Better Business Bureau business profile. Returns a bbb.org business profile: BBB rating letter grade and reasons, accreditation status and since-date, years in business, BBB file/incorporation dates, entity type, contact info, business categories, social media, and a short latest-reviews preview.
- **Params:** `url` (string, **required**) — BBB business profile URL, from a bbb-search result's url or hq_profile_url

### `bbb_business_complaints`

- **HTTP:** `GET /bbb/business/complaints`
- **What:** Get a Better Business Bureau business's complaint history. Returns a business's BBB complaint history: total complaint count, complaints closed or filed in the last 12 months, and one page of per-complaint detail (date, type, status, narrative text, and any business response / customer answer thread). Complaints are listed newest first, 10 per page; use page with the returned page, total_pages and has_more to walk the full list. A business with no filed complaints returns total_complaints 0 and an empty complaints list -- this is a normal result, not an error.
- **Params:** `page` (integer, optional) — Complaint list page, 1 or greater (10 complaints per page, newest first). Defaults to 1; `url` (string, **required**) — BBB business profile URL, from a bbb-search result's url or hq_profile_url. A location URL ending in /addressId/<number> is accepted and read from the business profile

### `bbb_business_more_info`

- **HTTP:** `GET /bbb/business/more-info`
- **What:** Get a Better Business Bureau business's full rating reasons and service area. Returns a business's full per-factor "Reasons for Rating" list and full service-area list. The bbb-business endpoint's own rating_reasons field typically holds only one generic boilerplate bullet regardless of actual rating; this endpoint returns the richer, business-specific list instead. Service area is business-conditional -- some businesses render no service-area section at all, in which case service_areas is empty.
- **Params:** `url` (string, **required**) — BBB business profile URL, from a bbb-search result's url or hq_profile_url. A location URL ending in /addressId/<number> is accepted and read from the business profile

### `bbb_business_reviews`

- **HTTP:** `GET /bbb/business/reviews`
- **What:** Get a Better Business Bureau business's customer reviews. Returns a business's full customer-review list (author, star rating, date, text, and any business response thread), paginated 10 per page, plus the average star rating and total review count.
- **Params:** `page` (integer, optional) — Result page (10 per page), default 1; `url` (string, **required**) — BBB business profile URL, from a bbb-search result's url or hq_profile_url. A location URL ending in /addressId/<number> is accepted and read from the business profile

### `bbb_category`

- **HTTP:** `GET /bbb/category`
- **What:** Browse a Better Business Bureau category. Browses bbb.org businesses by category and location directly, without a free-text search query. Returns the same business-result shape as bbb-search. A verified empty first page returns results: [] and total_results: 0; an unavailable or unrecognized page returns an error. A page beyond the exact last page returns 404, and a page beyond BBB's 15-page accessible limit returns 404 naming that limit. Optional sort and filter parameters use the same values as bbb-search; query-scoped category and state/province values come from bbb-search-filters.
- **Params:** `accredited` (boolean, optional) — Only BBB-accredited businesses; `category_id` (array, optional) — Query-scoped category ID from bbb-search-filters; `distance` (string, optional) — Maximum distance in miles; omit for all distances; `get_quote` (boolean, optional) — Only businesses offering quote requests; `page` (integer, optional) — Result page, default 1; `rating` (array, optional) — One or more BBB rating buckets; `service_area` (boolean, optional) — Only businesses serving the searched area; `sort` (string, optional) — Sort order; `state` (array, optional) — Query-scoped state or province code from bbb-search-filters; `url` (string, **required**) — BBB category browse URL, from a bbb-search result's related_categories

### `bbb_local_bbb`

- **HTTP:** `GET /bbb/local-bbb`
- **What:** Get a local BBB chapter profile. Returns public chapter profile details including office locations and hours, service territory, supported languages, and upcoming public events. news_url is the chapter's constructed newsroom route. When BBB publishes a program tile linking to a recognized newsroom path, published_news_url and its descriptive published_news_title are also returned. Use a canonical chapter URL from bbb-local-bbbs or a business record's local_bbb_url.
- **Params:** `url` (string, **required**) — Canonical BBB chapter URL from bbb-local-bbbs or a business record's local_bbb_url

### `bbb_local_bbbs`

- **HTTP:** `GET /bbb/local-bbbs`
- **What:** List local BBB chapters serving a region. Lists every chapter and public office shown on BBB's directory page for a region discovered by bbb-regions. Office addresses can be outside the selected service region.
- **Params:** `country` (string, **required**) — Country code from bbb-regions; `region` (string, **required**) — Two-letter region code from bbb-regions

### `bbb_news`

- **HTTP:** `GET /bbb/news`
- **What:** Get BBB newsroom stories. Returns one page of BBB newsroom cards from a canonical BBB newsroom URL. Three scopes are accepted, each with an optional topic: the US or Canada newsroom (/us/news), a state, province or city newsroom (/us/ca/news, /us/ca/san-francisco/news), and one local BBB chapter's own newsroom (/local-bbb/<chapter>/news, the news_url returned by bbb-local-bbbs and bbb-local-bbb). The list is whatever BBB shows on that page: a city or chapter whose local BBB publishes its own stories returns those, and other cities, other chapters and the state pages checked so far return the same list as the country newsroom, so compare total and the first items with the country newsroom before treating a list as local. A chapter URL also returns local_bbb_id and local_bbb_name. Items preserve BBB's type and include Article stories, events, and Near Me related-service cards when present. Near Me URLs are restricted to BBB's /near-me/<slug> paths. Every page carries total_pages and has_more: request page + 1 while has_more is true and stop when it is false; a page past the end returns 404. Event dates and links are preserved when present.
- **Params:** `url` (string, **required**) — Canonical https://www.bbb.org newsroom URL: /us/news or /ca/news; /<country>/<state>/news or /<country>/<state>/<city>/news with country us or ca, the two-letter region code from bbb-regions and the city slug from a business profile URL; or a chapter's news_url from bbb-local-bbbs. Append a topic segment from bbb-news-topics to narrow it and ?page=N (1 to 1000) to page; no other query key is accepted

### `bbb_news_topics`

- **HTTP:** `GET /bbb/news/topics`
- **What:** List BBB newsroom topics. Returns the complete topic navigation shown by a BBB newsroom page, including its active topic. The page can be the US or Canada newsroom, a state, province or city newsroom, or one local BBB chapter's newsroom; the returned topic URLs stay in that scope, and a chapter has its own topic set.
- **Params:** `url` (string, **required**) — Canonical https://www.bbb.org newsroom URL, optionally with a topic segment: /us/news or /ca/news; /<country>/<state>/news or /<country>/<state>/<city>/news with country us or ca, the two-letter region code from bbb-regions and the city slug from a business profile URL; or a chapter's news_url from bbb-local-bbbs

### `bbb_page`

- **HTTP:** `GET /bbb/page`
- **What:** Get a BBB evergreen page. Returns one page from the evergreen library BBB keeps under https://www.bbb.org/all/ (tips, topic hubs such as tax or holiday advice, scam studies): its title, introduction, body text, links, main image and last-modified time. BBB folds older newsroom stories into these pages and redirects the old article URL, so the url can be either the evergreen page itself or an article URL that bbb-article reports as moved; requested_url, final_url and every redirect between them are returned. published_at is always present and is null, because BBB publishes no date for these pages: modified_at is when BBB last edited the page, not when a story it replaced was published, and the page may cover a wider topic than that story did. The original article ID is not on the page; article_id repeats the one in the requested article URL. Returns 404 when the page does not exist, when an article URL has not been moved (read it with bbb-article), and when BBB redirects the URL somewhere outside /all/; the error names the destination and the answer is permanent. Content BBB loads in the browser for the visitor's local BBB is not included.
- **Params:** `url` (string, **required**) — Canonical https://www.bbb.org URL of an evergreen page (/all/<path>, no query string) or of an article (/article/<type>/<id>-<slug>) that BBB has moved to one

### `bbb_regions`

- **HTTP:** `GET /bbb/regions`
- **What:** List Better Business Bureau directory regions. Returns the complete current country and region list from BBB's public local directory. Use the returned region code with bbb-local-bbbs.
- **Params:** _none_

### `bbb_scamtracker_detail`

- **HTTP:** `GET /bbb/scamtracker/{id}`
- **What:** Get a Better Business Bureau Scam Tracker report. Returns one BBB Scam Tracker consumer scam report: description, dollars lost, targeted person's location, scammer location/email/phone/URL (when known), scam type, business name used, and date reported. If BBB no longer shows the report and serves its search page at that address, the endpoint returns a permanent 404; do not retry it.
- **Params:** `id` (string, **required**) — BBB Scam Tracker report id, from a bbb-scamtracker-search result's id or url

### `bbb_scamtracker_search`

- **HTTP:** `GET /bbb/scamtracker/search`
- **What:** Search Better Business Bureau Scam Tracker reports. Searches bbb.org Scam Tracker's consumer-reported-scam database by free-text query, scam category, targeted-victim state/province, reported-scammer state/province, report-date range, and/or dollar-loss range, paginated 10 results/page. A verified search with no matches returns results: [] and total_results: 0; an unavailable or unrecognized page returns 503 rather than an empty list. When result cards are present but BBB's total count is unavailable, total_results is omitted. Every page returns has_more and, when BBB's result count is exact, total_pages: request the next page only while has_more is true, because a page past the end returns 404. Omit every filter to browse the most-recent-first feed. This is a separate BBB dataset from the bbb-search/bbb-business/bbb-business-complaints business-rating family -- consumer-reported scam incidents, not business ratings.
- **Params:** `date_from` (string, optional) — Optional report-date range start (YYYY-MM-DD), inclusive. Must be set together with date_to; `date_to` (string, optional) — Optional report-date range end (YYYY-MM-DD), inclusive. Must be set together with date_from; `max_dollars_lost` (integer, optional) — Optional maximum reported dollar loss. Must be set together with min_dollars_lost; `min_dollars_lost` (integer, optional) — Optional minimum reported dollar loss. Must be set together with max_dollars_lost; `page` (integer, optional) — Result page (10 per page), default 1; `query` (string, optional) — Free-text search (phone number, website, email, business name, scam ID, description). Omit to browse the most-recent feed; `scam_type` (string, optional) — Scam category filter; `scammer_state` (string, optional) — Optional 2-letter reported-scammer state/province code (US state or Canadian province) -- where the scammer is reported to be, not the victim; `state` (string, optional) — Optional 2-letter targeted-victim state/province code (US state or Canadian province)

### `bbb_scamtracker_state_stats`

- **HTTP:** `GET /bbb/scamtracker/state-stats`
- **What:** Get Better Business Bureau Scam Tracker state/province aggregate stats. Returns aggregate scam-report stats per US state and Canadian province for a given time window: report counts, dollar losses, per-capita rates, year-over-year change, and top scam-type breakdown.
- **Params:** `period` (string, optional) — Aggregation window, default 90

### `bbb_search`

- **HTTP:** `GET /bbb/search`
- **What:** Search Better Business Bureau businesses. Searches bbb.org for businesses by name or category near a location. Returns each business's BBB rating letter grade, accreditation status, categories, service areas, contact info, and profile URL. A verified empty first page returns results: [] and total_results: 0; an unavailable or unrecognized page returns an error. A page beyond the exact last page returns 404, and a page beyond BBB's 15-page accessible limit returns 404 naming that limit. Category IDs and state/province codes are query-scoped; call bbb-search-filters to discover values for this query and location.
- **Params:** `accredited` (boolean, optional) — Only BBB-accredited businesses; `category_id` (array, optional) — Query-scoped category ID from bbb-search-filters; `country` (string, optional) — BBB country code; `distance` (string, optional) — Maximum distance in miles; omit for all distances; `get_quote` (boolean, optional) — Only businesses offering quote requests; `location` (string, **required**) — City and state (e.g. 'Austin, TX') or a ZIP code; `page` (integer, optional) — Result page, default 1; `query` (string, **required**) — Business name or category/service keyword; `rating` (array, optional) — One or more BBB rating buckets; `service_area` (boolean, optional) — Only businesses serving the searched area; `sort` (string, optional) — Sort order; `state` (array, optional) — Query-scoped state or province code from bbb-search-filters

### `bbb_search_filters`

- **HTTP:** `GET /bbb/search/filters`
- **What:** Discover Better Business Bureau search filters. Returns the live sort, category, and state/province values BBB currently advertises for one context. Supply query and location for text search, or category_url for the exact category-browse context; do not combine these modes. Category IDs and state/province codes are query-scoped; call this endpoint again when the search context changes. Static accepted values are country USA or CAN; sort Relevance, Distance, Rating, AToZ, or ZToA; distance 5, 10, 25, 50, or 100 miles; rating A, B, C, D, or F.
- **Params:** `accredited` (boolean, optional) — Only BBB-accredited businesses; `category_id` (array, optional) — Selected category IDs previously returned for this search context; `category_url` (string, optional) — BBB category browse URL; use instead of query and location; `country` (string, optional) — BBB country code; `distance` (string, optional) — Maximum distance in miles; omit for all distances; `get_quote` (boolean, optional) — Only businesses offering quote requests; `location` (string, optional) — City and state/province or ZIP code; use with query when category_url is omitted; `page` (integer, optional) — Result page, default 1; `query` (string, optional) — Business name or category/service keyword; use with location when category_url is omitted; `rating` (array, optional) — Selected rating values; `service_area` (boolean, optional) — Only businesses serving the searched area; `sort` (string, optional) — Sort order; `state` (array, optional) — Selected state/province codes previously returned for this search context

## Kickstarter (4)

### `kickstarter_comments`

- **HTTP:** `GET /kickstarter/comments`
- **What:** Get a Kickstarter campaign's comments. Returns the first page of one Kickstarter campaign's comments feed (Kickstarter's own server-rendered initial batch, typically 40-60 comments; total_count reports the feed's real total). Each comment includes the author, whether the author is the creator (a reply), the posted timestamp, and the comment text. creator and slug are the two path segments of the project URL, e.g. lookingglass and musubi for kickstarter.com/projects/lookingglass/musubi.
- **Params:** `creator` (string, **required**) — Creator path segment of the project URL; `slug` (string, **required**) — Project slug path segment of the project URL

### `kickstarter_discover`

- **HTTP:** `GET /kickstarter/discover`
- **What:** Browse or search Kickstarter's Discover surface. Returns one page of Kickstarter's own Discover results -- browse by category id and/or a free-text search term, sorted by magic/popularity/newest/end_date/most_funded, optionally filtered by campaign state and/or restricted to staff picks. Each result includes the campaign's funding snapshot (goal, pledged, percent funded, backers), category, location, creator, and cover photo.
- **Params:** `category_id` (integer, optional) — Kickstarter's own numeric category id (top-level or sub-category), e.g. 16 for Technology; `page` (integer, optional) — 1-based page number; `sort` (string, optional) — Result order; `staff_pick_only` (boolean, optional) — Restrict results to Kickstarter's own \; `state` (array, optional) — Repeatable campaign state filter; `term` (string, optional) — Free-text search query

### `kickstarter_project`

- **HTTP:** `GET /kickstarter/project`
- **What:** Get a Kickstarter campaign's detail. Returns one Kickstarter campaign's detail: funding snapshot (goal, pledged, percent funded, backers, state, dates), category, creator, cover photo, story text, risks & challenges, update/comment/FAQ counts, and reward/pledge tiers. creator and slug are the two path segments of the project URL, e.g. lookingglass and musubi for kickstarter.com/projects/lookingglass/musubi. Reward tiers are best-effort -- see the endpoint's documentation for when they may be omitted.
- **Params:** `creator` (string, **required**) — Creator path segment of the project URL; `slug` (string, **required**) — Project slug path segment of the project URL

### `kickstarter_updates`

- **HTTP:** `GET /kickstarter/updates`
- **What:** Get a Kickstarter campaign's updates feed. Returns one Kickstarter campaign's full updates feed: for each update, its number, title, author, whether the author is the creator, publish date, body text, and comment count. creator and slug are the two path segments of the project URL, e.g. lookingglass and musubi for kickstarter.com/projects/lookingglass/musubi.
- **Params:** `creator` (string, **required**) — Creator path segment of the project URL; `slug` (string, **required**) — Project slug path segment of the project URL

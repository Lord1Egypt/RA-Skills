# customer-feedback-analysis — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**19 endpoints across 7 platform group(s).**

## AppStore (3)

### `appstore_app`

- **HTTP:** `GET /appstore/app`
- **What:** Retrieve full App Store app details. Returns app metadata from the App Store. Provide either `id` (numeric track ID) or `app_id` (bundle ID). `id`/`app_id` can identify an iPhone, iPad, or Mac App Store listing.
- **Params:** `app_id` (string, optional) — App Store bundle ID; `country` (string, optional) — Two-letter storefront country code; `id` (string, optional) — App Store numeric track ID (digits only); `lang` (string, optional) — Result language tag; `platforms` (boolean, optional) — Include the full device-platform compatibility list (adds one extra upstream fetch); `ratings` (boolean, optional) — Include ratings histogram

### `appstore_reviews`

- **HTTP:** `GET /appstore/reviews`
- **What:** Retrieve App Store reviews. Returns one page of customer reviews for an App Store app, identified by `id` (numeric track ID) or `app_id` (bundle ID). `page` runs 1 to 10 and `sort` is `mostRecent` (default) or `mostHelpful`. Reviews carry `score`, `title`, `text`, `version`, `user_name` and `updated`. Returns 503 when reviews cannot be retrieved, and 404 when the app is not in that `country` storefront.
- **Params:** `app_id` (string, optional) — App Store bundle ID; `country` (string, optional) — Two-letter storefront country code; `id` (string, optional) — App Store numeric track ID (digits only); `lang` (string, optional) — Result language tag; `page` (integer, optional) — Review page number (1-10); `sort` (string, optional) — Sort order

### `appstore_search`

- **HTTP:** `GET /appstore/search`
- **What:** Search the App Store. Returns App Store search results for a term. Set `ids_only=true` to return only app IDs. `platform` enum: `phone`, `pad`, `mac`.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `ids_only` (boolean, optional) — Return only app IDs; `lang` (string, optional) — Result language tag; `num` (integer, optional) — Number of apps per page; `page` (integer, optional) — Search page number (1-based); `platform` (string, optional) — App Store catalog to search: phone, pad, mac; `term` (string, **required**) — Search term

## GooglePlay (3)

### `googleplay_app`

- **HTTP:** `GET /googleplay/app`
- **What:** Retrieve full Google Play app details. Returns app metadata from a Google Play details page, including installs, ratings, pricing, version info, developer metadata, media assets, release state, selected user comments, and "More by this developer" and "Similar apps" recommendation rails. For a per-device (phone/tablet/Chromebook) ratings-and-reviews breakdown, see `/googleplay/ratings`. Defaults: `country=us`, `lang=en`.
- **Params:** `app_id` (string, **required**) — Google Play package name; `country` (string, optional) — Two-letter storefront country code; `lang` (string, optional) — Two-letter language code

### `googleplay_reviews`

- **HTTP:** `GET /googleplay/reviews`
- **What:** Retrieve Google Play reviews. Returns Google Play reviews for an app by `app_id`. `sort` is `newest` (default), `helpfulness` or `rating`, and `num` is up to 1000 per request (default 100). Each review has its text, score, date, thumbs-up count, app version and any developer reply. Pass `next_pagination_token` back to continue.
- **Params:** `app_id` (string, **required**) — Google Play app id; `country` (string, optional) — Two-letter country code; `lang` (string, optional) — Two-letter language code; `next_pagination_token` (string, optional) — Token from a previous response; `num` (integer, optional) — Number of reviews; `paginate` (boolean, optional) — Only fetch the requested page; `sort` (string, optional) — Sort: helpfulness, newest, rating

### `googleplay_search`

- **HTTP:** `GET /googleplay/search`
- **What:** Search Google Play. Searches Google Play for apps matching the required `term`, up to `num` results (default 20, max 250). `price` is `all` (default), `free` or `paid`, and `country` and `lang` default to `us` and `en`. A strong exact match is placed first. An empty list means no apps matched.
- **Params:** `country` (string, optional) — Two-letter country code; `full_detail` (boolean, optional) — Resolve each app to full detail; `lang` (string, optional) — Two-letter language code; `num` (integer, optional) — Number of apps; `price` (string, optional) — Price filter: all, free, paid; `term` (string, **required**) — Search term

## Datasets (1)

### `datasets_apps_reviews_search`

- **HTTP:** `GET /datasets/apps-reviews/search`
- **What:** Search the app-reviews dataset. Searches user reviews from the iOS App Store and Google Play (one document per review). Store enum: `ios`, `android`. Sort enum: `recent`, `score_desc`, `score_asc`, `helpful_desc`. Billing: this search costs 1 credit per record returned, with a minimum of 2 (an empty result costs 2, a full page of 100 costs 100).
- **Params:** `app_id` (string, optional) — Exact app filter — iOS numeric track id or Android package, max 128 characters; `country` (string, optional) — Exact storefront country filter, max 128 characters; `min_score` (integer, optional) — Minimum star rating, 1 through 5; `page` (integer, optional) — Page number, defaults to 1; `page_size` (integer, optional) — Page size, defaults to 20 and maxes at 100; page * page_size must be <= 10000; `q` (string, optional) — Full-text query over review text, title and author, max 256 characters; `sort` (string, optional) — Sort enum: recent, score_desc, score_asc, helpful_desc; `store` (string, optional) — Store enum: ios, android

## Trustpilot (3)

### `trustpilot_business`

- **HTTP:** `GET /trustpilot/business/{slug}`
- **What:** Get Trustpilot business profile. Returns a Trustpilot business profile by `slug`, such as `openai.com`. The profile has the name, `trust_score`, `review_count`, rating histogram, review summary and topics, categories, claimed status, website URL, reply metrics, company activity and verification flags, and an about section with description and contact details.
- **Params:** `slug` (string, **required**) — Trustpilot business slug

### `trustpilot_business_reviews`

- **HTTP:** `GET /trustpilot/business/{slug}/reviews`
- **What:** Get Trustpilot business reviews. Returns one page of Trustpilot reviews for a business slug such as `openai.com`, with filters for star rating, verified reviews, reviews with a company reply, language and text search. Each review has its rating, title, body, author name, country and review count, dates, and any company reply; the response also carries the business summary and pagination totals.
- **Params:** `date_from` (string, optional) — Date range start in YYYY-MM-DD; currently rejected by upstream; `date_to` (string, optional) — Date range end in YYYY-MM-DD; currently rejected by upstream; `language` (string, optional) — Review language code used by Trustpilot; `page` (integer, optional) — 1-based page number; defaults to 1; `q` (string, optional) — Text search within reviews; `replied` (boolean, optional) — Filter to reviews with business replies; `slug` (string, **required**) — Trustpilot business slug; `stars` (integer, optional) — Filter by star rating from 1 to 5; `verified` (boolean, optional) — Filter to verified reviews

### `trustpilot_business_search`

- **HTTP:** `GET /trustpilot/business-units/search`
- **What:** Search Trustpilot business units. Searches Trustpilot for businesses matching a query, for a country (default `US`), with `page` and `page_size` (default 20, max 100). Each result has the display name, identifying name, TrustScore, star rating, review count, categories, website, email, phone, address and Trustpilot URL; `total_hits` gives the full match count.
- **Params:** `country` (string, optional) — Two-letter country code; defaults to US; `page` (integer, optional) — 1-based page number; defaults to 1; `page_size` (integer, optional) — Results per page; defaults to 20, maximum 100; `q` (string, **required**) — Search query

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

## Adidas (3)

### `adidas_product_review_topics`

- **HTTP:** `GET /adidas/product/review-topics`
- **What:** Get Adidas review topics for a product. Returns the topics an Adidas product model's customer reviews can be filtered by -- the "filter by topic" chips the product page shows, commonly satisfaction, comfort, color, purchase, fit, appearance, quality and style. Feed a topics[].topic value back to /adidas/product/reviews as its topic parameter to return only reviews about that aspect. The topic vocabulary is per model, not a fixed list: a shoe exposes fit and comfort topics that an accessory does not, so read it per model rather than hard-coding it. model_number is the Adidas model number (e.g. SAMBAU2312) -- NOT the SKU: take it from an adidas_search result's products[].model_number field. A model with no reviews, including a well-formed but unrecognized model_number, returns an empty topics list rather than an error. Note the label field is a display form of topic, not translated text: Adidas returns the same English values for every locale on this route.
- **Params:** `locale` (string, optional) — Locale accepted for consistency with the reviews endpoint. Allowed values: cs_CZ, da_DK, de_AT, de_CH, de_DE, el_GR, en_AE, en_AU, en_CA, en_GB, en_IE, en_IL, en_IN, en_NZ, en_PH, en_SG, en_US, en_ZA, es_AR, es_CL, es_CO, es_ES, es_MX, es_PE, fr_BE, fr_CA, fr_CH, fr_FR, id_ID, it_CH, it_IT, ja_JP, ko_KR, nl_BE, nl_NL, pl_PL, pt_BR, pt_PT, ru_RU, sk_SK, sv_SE, th_TH, tr_TR, zh_HK, zh_TW. Defaults to en_US. Note Adidas returns the same English topic labels regardless of this value.; `model_number` (string, **required**) — Adidas model number, from an adidas_search result's products[].model_number field

### `adidas_product_reviews`

- **HTTP:** `GET /adidas/product/reviews`
- **What:** Get Adidas product reviews. Returns one page of customer reviews for an Adidas product model, plus the model's rating summary: overall rating, star histogram, percentage of reviewers who recommend it, per-attribute averages (Size, Width, Comfort, Quality with their own scale labels), and Adidas's AI-generated review digest when one exists. Each review carries the rating, headline, body, author nickname, purchased colorway, helpful/not-helpful vote counts, badges, customer photos, and submission time. model_number is the Adidas model number (e.g. SAMBAU2312) -- NOT the SKU: take it from an adidas_search result's products[].model_number field, which is a different value from products[].id. Reviews are returned 10 per page. Reviews are scoped to review text written in the requested locale's language, and most of the US catalog's reviews are English, so a non-English locale commonly returns rating statistics and a localized summary with an empty reviews list. A model with no reviews -- including a well-formed but unrecognized model_number -- returns an empty reviews list rather than an error, because Adidas answers 200 with a zero count rather than 404.
- **Params:** `locale` (string, optional) — Locale for the review-summary language, the secondary-rating scale labels, and the language of the reviews returned. Allowed values: cs_CZ, da_DK, de_AT, de_CH, de_DE, el_GR, en_AE, en_AU, en_CA, en_GB, en_IE, en_IL, en_IN, en_NZ, en_PH, en_SG, en_US, en_ZA, es_AR, es_CL, es_CO, es_ES, es_MX, es_PE, fr_BE, fr_CA, fr_CH, fr_FR, id_ID, it_CH, it_IT, ja_JP, ko_KR, nl_BE, nl_NL, pl_PL, pt_BR, pt_PT, ru_RU, sk_SK, sv_SE, th_TH, tr_TR, zh_HK, zh_TW. Defaults to en_US.; `model_number` (string, **required**) — Adidas model number, from an adidas_search result's products[].model_number field; `page` (integer, optional) — One-based page number, 10 reviews per page, defaults to 1; `rating` (integer, optional) — Return only reviews with this star rating. Allowed values: 1, 2, 3, 4, 5. Omitted returns every rating.; `topic` (string, optional) — Return only reviews about one topic. Valid values are per-model -- read them from /adidas/product/review-topics for the same model_number (commonly satisfaction, comfort, color, purchase, fit, appearance, quality, style). An unrecognized topic returns a 400 listing the model's own topics.

### `adidas_search`

- **HTTP:** `GET /adidas/search`
- **What:** Search or browse Adidas products. Searches Adidas.com product listings by keyword, or browses a category listing by taxonomy slug, with real pagination and sort options. Exactly one of query or category is required. Returns product summaries (title, price, rating, images, color variants) plus facet filter groups, sort options, and (for category browse) a breadcrumb trail. Keyword search is best-effort relevance, not a guaranteed match: an obscure keyword returns whatever Adidas's own search index surfaces. A genuinely empty keyword search returns an empty product list, and requesting a page beyond the available result pages (or an unknown category) returns a not-found error. Category values are the path segment after /us/ in an Adidas category URL (e.g. women-athletic_sneakers); they can also be read from the url fields of a search/category response's own filters and breadcrumbs. Facets are applied by composing them into the category slug rather than by a separate parameter: each filters[].values[].slug is a token you splice into the category value (e.g. category=women-black-athletic_sneakers applies the Color=Black facet, and category=women-athletic_sneakers-prime applies Shipping=PRIME). Use filters[].key (the facet's stable name, e.g. searchcolor) rather than filters[].id, which is an opaque per-deployment UUID that cannot be used to build a request. Note the token's position within the slug varies by facet, so compose from a slug you have seen rather than assuming a fixed order.
- **Params:** `category` (string, optional) — Category/taxonomy slug, the path segment after /us/ in an Adidas category URL. Exactly one of query or category is required.; `page` (integer, optional) — One-based page number, defaults to 1; `query` (string, optional) — Search keyword. Exactly one of query or category is required.; `sort` (string, optional) — Sort order. Allowed values: price-low-to-high, newest-to-oldest, top-sellers, price-high-to-low. Omitted means relevance.

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

# app-release-feedback-analysis — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**8 endpoints across 3 platform group(s).**

## AppStore (4)

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

### `appstore_version_history`

- **HTTP:** `GET /appstore/version-history/{id}`
- **What:** Retrieve App Store version history. Returns an App Store app's version history, as shown under "What's New", by numeric track id, for an optional storefront country and language. Each entry has the version number, release date and timestamp, and release notes. A non-numeric id returns `400`.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — App Store numeric track ID (digits only); `lang` (string, optional) — Result language tag

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

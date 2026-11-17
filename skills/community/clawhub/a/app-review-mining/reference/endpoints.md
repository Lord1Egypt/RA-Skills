# app-review-mining — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**26 endpoints across 2 platform group(s).**

## AppStore (15)

### `appstore_app`

- **HTTP:** `GET /appstore/app`
- **What:** Retrieve full App Store app details. Returns app metadata from the App Store. Provide either `id` (numeric track ID) or `app_id` (bundle ID). `id`/`app_id` can identify an iPhone, iPad, or Mac App Store listing.
- **Params:** `app_id` (string, optional) — App Store bundle ID; `country` (string, optional) — Two-letter storefront country code; `id` (string, optional) — App Store numeric track ID (digits only); `lang` (string, optional) — Result language tag; `platforms` (boolean, optional) — Include the full device-platform compatibility list (adds one extra upstream fetch); `ratings` (boolean, optional) — Include ratings histogram

### `appstore_categories`

- **HTTP:** `GET /appstore/categories`
- **What:** Retrieve App Store chart categories and collections. Returns every category ID and chart collection accepted by `/appstore/list`, including Games and Magazines & Newspapers subgenres with their parent ID. Collections carry their device platform (`phone`, `pad`, `mac`), chart type (`top_free`, `top_paid`, `top_grossing`, `top`, `new`), and whether the feed currently returns entries.
- **Params:** _none_

### `appstore_collection`

- **HTTP:** `GET /appstore/collection`
- **What:** Retrieve apps in one App Store collection. Returns app items embedded in an Apple room or EDS collection page. Discover IDs with `appstore_collections`. `platform` enum: `iphone`, `ipad`, `mac`, `vision`, `watch`, `tv`. `collection_id` must be a numeric room ID or `eds.UUID` ID returned by the discovery endpoint.
- **Params:** `collection_id` (string, **required**) — Room ID or EDS UUID collection ID from appstore_collections; `country` (string, optional) — Two-letter storefront country code; `lang` (string, optional) — Result language tag; `platform` (string, **required**) — Apple device catalog

### `appstore_collections`

- **HTTP:** `GET /appstore/collections`
- **What:** Discover App Store editorial collections. Returns the room and EDS collection links embedded in Apple's browse page for one device. `platform` enum: `iphone`, `ipad`, `mac`, `vision`, `watch`, `tv`. Pass a returned `id` and the same platform to `appstore_collection` to retrieve the collection's apps.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `lang` (string, optional) — Result language tag; `platform` (string, **required**) — Apple device catalog

### `appstore_developer`

- **HTTP:** `GET /appstore/developer/{dev_id}`
- **What:** Retrieve apps by developer ID. Lists the App Store apps published by one developer, by Apple developer (artist) id, for an optional storefront country and language. Each app carries its id, title, description, icon and screenshots, price and currency, genres, version and release notes, rating score and counts, size, supported devices and languages.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `dev_id` (string, **required**) — Developer artist ID; `lang` (string, optional) — Result language tag

### `appstore_editorial`

- **HTTP:** `GET /appstore/editorial`
- **What:** Retrieve an App Store device or Arcade editorial landing page. Returns the curated editorial shelves from one of Apple's per-device App Store landing pages (the same content shown by apps.apple.com's device switcher). `device` enum: `iphone`, `ipad`, `mac`, `vision`, `watch`, `tv`. `section` enum: `main` (the device's Today/Discover/Apps & Games landing page), `arcade` (the device's Apple Arcade landing page). Watch has no Arcade page — `device=watch` with `section=arcade` returns `400`.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `device` (string, **required**) — Apple device catalog; `lang` (string, optional) — Result language tag; `section` (string, optional) — Editorial section within the device

### `appstore_editorial_category`

- **HTTP:** `GET /appstore/editorial/category`
- **What:** Retrieve an App Store category-scoped editorial page. Returns the curated editorial shelves for one device category page (e.g. "Entertainment Apps for Vision"). `category_id` is a numeric, device-specific editorial page ID — not a static enum — discovered from an `appstore_editorial` response for the SAME `device`, in its "Browse by Category" shelf items' `destination_id` field. `device` enum: `iphone`, `ipad`, `mac`, `vision`, `watch`, `tv`.
- **Params:** `category_id` (string, **required**) — Numeric App Store editorial page ID, discovered from appstore_editorial (same device); `country` (string, optional) — Two-letter storefront country code; `device` (string, **required**) — Apple device catalog; `lang` (string, optional) — Result language tag

### `appstore_list`

- **HTTP:** `GET /appstore/list`
- **What:** Retrieve App Store collection rankings. Returns ranked App Store apps from an iTunes RSS collection, optionally expanded to full lookup details. `collection` enum: `topfreeapplications`, `toppaidapplications`, `topgrossingapplications`, `topfreeipadapplications`, `toppaidipadapplications`, `topgrossingipadapplications`, `topmacapps`, `topfreemacapps`, `topgrossingmacapps`, `toppaidmacapps`, `newapplications`, `newfreeapplications`, `newpaidapplications`. Of the Mac collections, only `topfreemacapps` currently returns ranked apps — `topmacapps`, `topgrossingmacapps`, and `toppaidmacapps` are accepted but Apple's feed for them is currently empty. There is no separate Games `collection` — combine any collection with `category=6014` (or a Games subgenre ID, e.g. `7012` for Puzzle) to get its Games-only equivalent, e.g. Top Free Games. See the endpoint markdown for the full category ID table.
- **Params:** `category` (integer, optional) — Numeric App Store category ID, see description for the full enum; e.g. 6014 = Games, 7012 = Games/Puzzle; `collection` (string, optional) — Chart collection slug, see description for the full enum; `country` (string, optional) — Two-letter storefront country code; `full_detail` (boolean, optional) — Expand each app via lookup API; `lang` (string, optional) — Result language tag; `num` (integer, optional) — Number of apps to return

### `appstore_privacy`

- **HTTP:** `GET /appstore/privacy/{id}`
- **What:** Retrieve App Store privacy disclosures. Returns the privacy disclosures shown on an App Store page for one app, identified by its numeric track `id` (digits only; anything else returns 400). The response has `privacy_policy_url`, `manage_privacy_choices_url` and `privacy_types`, each with its data categories and purposes. `country` and `lang` are optional.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — App Store numeric track ID (digits only); `lang` (string, optional) — Result language tag

### `appstore_ratings`

- **HTTP:** `GET /appstore/ratings`
- **What:** Retrieve App Store ratings histogram. Returns the total `ratings` count and the 1 to 5 star `histogram` for an App Store app. Identify it with either the numeric track `id` or the bundle ID `app_id`; a bundle ID is resolved to the track ID first, and a non-numeric `id` returns 400. `country` and `lang` are optional.
- **Params:** `app_id` (string, optional) — App Store bundle ID; `country` (string, optional) — Two-letter storefront country code; `id` (string, optional) — App Store numeric track ID (digits only); `lang` (string, optional) — Result language tag

### `appstore_reviews`

- **HTTP:** `GET /appstore/reviews`
- **What:** Retrieve App Store reviews. Returns one page of customer reviews for an App Store app, identified by `id` (numeric track ID) or `app_id` (bundle ID). `page` runs 1 to 10 and `sort` is `mostRecent` (default) or `mostHelpful`. Reviews carry `score`, `title`, `text`, `version`, `user_name` and `updated`. Returns 503 when reviews cannot be retrieved, and 404 when the app is not in that `country` storefront.
- **Params:** `app_id` (string, optional) — App Store bundle ID; `country` (string, optional) — Two-letter storefront country code; `id` (string, optional) — App Store numeric track ID (digits only); `lang` (string, optional) — Result language tag; `page` (integer, optional) — Review page number (1-10); `sort` (string, optional) — Sort order

### `appstore_search`

- **HTTP:** `GET /appstore/search`
- **What:** Search the App Store. Returns App Store search results for a term. Set `ids_only=true` to return only app IDs. `platform` enum: `phone`, `pad`, `mac`.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `ids_only` (boolean, optional) — Return only app IDs; `lang` (string, optional) — Result language tag; `num` (integer, optional) — Number of apps per page; `page` (integer, optional) — Search page number (1-based); `platform` (string, optional) — App Store catalog to search: phone, pad, mac; `term` (string, **required**) — Search term

### `appstore_similar`

- **HTTP:** `GET /appstore/similar`
- **What:** Retrieve "You Might Also Like" apps. Returns the related apps shown on the App Store product page. Provide either `id` (numeric track ID) or `app_id` (bundle ID).
- **Params:** `app_id` (string, optional) — App Store bundle ID; `country` (string, optional) — Two-letter storefront country code; `id` (string, optional) — App Store numeric track ID (digits only); `lang` (string, optional) — Result language tag

### `appstore_suggest`

- **HTTP:** `GET /appstore/suggest/{term}`
- **What:** Retrieve App Store search suggestions. Returns App Store search suggestions for a partial search term given in the path, as a list of suggested `term` values. `country` is an optional two-letter storefront code.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `term` (string, **required**) — Partial search term

### `appstore_version_history`

- **HTTP:** `GET /appstore/version-history/{id}`
- **What:** Retrieve App Store version history. Returns an App Store app's version history, as shown under "What's New", by numeric track id, for an optional storefront country and language. Each entry has the version number, release date and timestamp, and release notes. A non-numeric id returns `400`.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — App Store numeric track ID (digits only); `lang` (string, optional) — Result language tag

## GooglePlay (11)

### `googleplay_app`

- **HTTP:** `GET /googleplay/app`
- **What:** Retrieve full Google Play app details. Returns app metadata from a Google Play details page, including installs, ratings, pricing, version info, developer metadata, media assets, release state, selected user comments, and "More by this developer" and "Similar apps" recommendation rails. For a per-device (phone/tablet/Chromebook) ratings-and-reviews breakdown, see `/googleplay/ratings`. Defaults: `country=us`, `lang=en`.
- **Params:** `app_id` (string, **required**) — Google Play package name; `country` (string, optional) — Two-letter storefront country code; `lang` (string, optional) — Two-letter language code

### `googleplay_categories`

- **HTTP:** `GET /googleplay/categories`
- **What:** Retrieve Google Play app categories. Lists the Google Play app categories and subcategories, each with an id such as `PRODUCTIVITY` and a display name. `country` and `lang` take two-letter codes to pick the storefront and the language of the names.
- **Params:** `country` (string, optional) — Two-letter country code; `lang` (string, optional) — Two-letter language code

### `googleplay_datasafety`

- **HTTP:** `GET /googleplay/datasafety`
- **What:** Retrieve Google Play data safety details. Returns the data safety section Google Play shows for an app, by the required `app_id`. It lists the data the app collects and shares, each with its type, purpose and whether it is optional, plus the app's security practices and privacy policy URL. `lang` sets the language.
- **Params:** `app_id` (string, **required**) — Google Play app id; `lang` (string, optional) — Two-letter language code

### `googleplay_developer`

- **HTTP:** `GET /googleplay/developer/{dev_id}`
- **What:** Retrieve apps by Google Play developer. Lists the Google Play apps published by one developer, by developer id or name, for an optional country and language. `num` sets how many apps to return, and `full_detail=true` resolves each app to its full detail record instead of the listing summary. Returns the developer id and name with the app list.
- **Params:** `country` (string, optional) — Two-letter country code; `dev_id` (string, **required**) — Developer id or name; `full_detail` (boolean, optional) — Resolve each app to full detail; `lang` (string, optional) — Two-letter language code; `num` (integer, optional) — Number of apps

### `googleplay_list`

- **HTTP:** `GET /googleplay/list`
- **What:** Retrieve apps from a Google Play top collection. Lists apps from a Google Play chart. `collection` is `TOP_FREE`, `TOP_PAID`, `GROSSING`, `NEW_FREE` or `NEW_PAID`, and `category`, `device`, `age`, `num`, `country` and `lang` narrow it. Set `full_detail` to get full app details instead of the compact card.
- **Params:** `age` (string, optional) — Family age range; `category` (string, optional) — Category id; `collection` (string, optional) — Collection: TOP_FREE, TOP_PAID, GROSSING, NEW_FREE, NEW_PAID; `country` (string, optional) — Two-letter country code; `device` (string, optional) — Google Play device tab: phone, tablet, tv, chromebook, watch, xr, car; `full_detail` (boolean, optional) — Resolve each app to full detail; `lang` (string, optional) — Two-letter language code; `num` (integer, optional) — Number of apps

### `googleplay_permissions`

- **HTTP:** `GET /googleplay/permissions`
- **What:** Retrieve Google Play app permissions. Returns the permissions a Google Play app requests, by the required `app_id`. Each entry has the permission name and its type. Set `short` to get only the permission names as a flat list. `country` and `lang` pick the storefront and language.
- **Params:** `app_id` (string, **required**) — Google Play app id; `country` (string, optional) — Two-letter country code; `lang` (string, optional) — Two-letter language code; `short` (boolean, optional) — Return only permission names

### `googleplay_ratings`

- **HTTP:** `GET /googleplay/ratings`
- **What:** Get Google Play ratings by device. Returns the ratings-and-reviews breakdown Google Play shows under the details page's device tabs, one entry each for phone, tablet, and Chromebook. Defaults: `country=us`, `lang=en`.
- **Params:** `app_id` (string, **required**) — Google Play package name; `country` (string, optional) — Two-letter storefront country code; `lang` (string, optional) — Two-letter language code

### `googleplay_reviews`

- **HTTP:** `GET /googleplay/reviews`
- **What:** Retrieve Google Play reviews. Returns Google Play reviews for an app by `app_id`. `sort` is `newest` (default), `helpfulness` or `rating`, and `num` is up to 1000 per request (default 100). Each review has its text, score, date, thumbs-up count, app version and any developer reply. Pass `next_pagination_token` back to continue.
- **Params:** `app_id` (string, **required**) — Google Play app id; `country` (string, optional) — Two-letter country code; `lang` (string, optional) — Two-letter language code; `next_pagination_token` (string, optional) — Token from a previous response; `num` (integer, optional) — Number of reviews; `paginate` (boolean, optional) — Only fetch the requested page; `sort` (string, optional) — Sort: helpfulness, newest, rating

### `googleplay_search`

- **HTTP:** `GET /googleplay/search`
- **What:** Search Google Play. Searches Google Play for apps matching the required `term`, up to `num` results (default 20, max 250). `price` is `all` (default), `free` or `paid`, and `country` and `lang` default to `us` and `en`. A strong exact match is placed first. An empty list means no apps matched.
- **Params:** `country` (string, optional) — Two-letter country code; `full_detail` (boolean, optional) — Resolve each app to full detail; `lang` (string, optional) — Two-letter language code; `num` (integer, optional) — Number of apps; `price` (string, optional) — Price filter: all, free, paid; `term` (string, **required**) — Search term

### `googleplay_similar`

- **HTTP:** `GET /googleplay/similar`
- **What:** Retrieve similar Google Play apps. Returns the apps in the Similar apps cluster on a Google Play app page, for the required `app_id`. `num` limits how many are returned, `country` and `lang` set the storefront and language, and `full_detail` returns full app details instead of compact cards.
- **Params:** `app_id` (string, **required**) — Google Play app id; `country` (string, optional) — Two-letter country code; `full_detail` (boolean, optional) — Resolve each app to full detail; `lang` (string, optional) — Two-letter language code; `num` (integer, optional) — Number of apps

### `googleplay_suggest`

- **HTTP:** `GET /googleplay/suggest/{term}`
- **What:** Retrieve Google Play query suggestions. Returns up to 10 Google Play search suggestions for the term prefix in the path. `country` and `lang` take two-letter codes to pick the storefront and language. Each suggestion is a `term`.
- **Params:** `country` (string, optional) — Two-letter country code; `lang` (string, optional) — Two-letter language code; `term` (string, **required**) — Search term prefix

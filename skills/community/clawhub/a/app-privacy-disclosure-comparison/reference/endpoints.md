# app-privacy-disclosure-comparison — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**7 endpoints across 2 platform group(s).**

## AppStore (3)

### `appstore_app`

- **HTTP:** `GET /appstore/app`
- **What:** Retrieve full App Store app details. Returns app metadata from the App Store. Provide either `id` (numeric track ID) or `app_id` (bundle ID). `id`/`app_id` can identify an iPhone, iPad, or Mac App Store listing.
- **Params:** `app_id` (string, optional) — App Store bundle ID; `country` (string, optional) — Two-letter storefront country code; `id` (string, optional) — App Store numeric track ID (digits only); `lang` (string, optional) — Result language tag; `platforms` (boolean, optional) — Include the full device-platform compatibility list (adds one extra upstream fetch); `ratings` (boolean, optional) — Include ratings histogram

### `appstore_privacy`

- **HTTP:** `GET /appstore/privacy/{id}`
- **What:** Retrieve App Store privacy disclosures. Returns the privacy disclosures shown on an App Store page for one app, identified by its numeric track `id` (digits only; anything else returns 400). The response has `privacy_policy_url`, `manage_privacy_choices_url` and `privacy_types`, each with its data categories and purposes. `country` and `lang` are optional.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — App Store numeric track ID (digits only); `lang` (string, optional) — Result language tag

### `appstore_search`

- **HTTP:** `GET /appstore/search`
- **What:** Search the App Store. Returns App Store search results for a term. Set `ids_only=true` to return only app IDs. `platform` enum: `phone`, `pad`, `mac`.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `ids_only` (boolean, optional) — Return only app IDs; `lang` (string, optional) — Result language tag; `num` (integer, optional) — Number of apps per page; `page` (integer, optional) — Search page number (1-based); `platform` (string, optional) — App Store catalog to search: phone, pad, mac; `term` (string, **required**) — Search term

## GooglePlay (4)

### `googleplay_app`

- **HTTP:** `GET /googleplay/app`
- **What:** Retrieve full Google Play app details. Returns app metadata from a Google Play details page, including installs, ratings, pricing, version info, developer metadata, media assets, release state, selected user comments, and "More by this developer" and "Similar apps" recommendation rails. For a per-device (phone/tablet/Chromebook) ratings-and-reviews breakdown, see `/googleplay/ratings`. Defaults: `country=us`, `lang=en`.
- **Params:** `app_id` (string, **required**) — Google Play package name; `country` (string, optional) — Two-letter storefront country code; `lang` (string, optional) — Two-letter language code

### `googleplay_datasafety`

- **HTTP:** `GET /googleplay/datasafety`
- **What:** Retrieve Google Play data safety details. Returns the data safety section Google Play shows for an app, by the required `app_id`. It lists the data the app collects and shares, each with its type, purpose and whether it is optional, plus the app's security practices and privacy policy URL. `lang` sets the language.
- **Params:** `app_id` (string, **required**) — Google Play app id; `lang` (string, optional) — Two-letter language code

### `googleplay_permissions`

- **HTTP:** `GET /googleplay/permissions`
- **What:** Retrieve Google Play app permissions. Returns the permissions a Google Play app requests, by the required `app_id`. Each entry has the permission name and its type. Set `short` to get only the permission names as a flat list. `country` and `lang` pick the storefront and language.
- **Params:** `app_id` (string, **required**) — Google Play app id; `country` (string, optional) — Two-letter country code; `lang` (string, optional) — Two-letter language code; `short` (boolean, optional) — Return only permission names

### `googleplay_search`

- **HTTP:** `GET /googleplay/search`
- **What:** Search Google Play. Searches Google Play for apps matching the required `term`, up to `num` results (default 20, max 250). `price` is `all` (default), `free` or `paid`, and `country` and `lang` default to `us` and `en`. A strong exact match is placed first. An empty list means no apps matched.
- **Params:** `country` (string, optional) — Two-letter country code; `full_detail` (boolean, optional) — Resolve each app to full detail; `lang` (string, optional) — Two-letter language code; `num` (integer, optional) — Number of apps; `price` (string, optional) — Price filter: all, free, paid; `term` (string, **required**) — Search term

# film-box-office-comparison — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**13 endpoints across 2 platform group(s).**

## Datasets (3)

### `datasets_boxofficemojo_facets`

- **HTTP:** `GET /datasets/boxofficemojo/facets`
- **What:** Facet the Box Office Mojo dataset. Returns terms-aggregation counts for one facet of the Box Office Mojo dataset, scoped to the same filters as search. Facet enum: `gross_band`, `years_active`, `lifetime_year`, `franchise_names`, `brand_names`, `genre_names`, `hydrated`, `is_billion_dollar`, `in_lifetime_top_1000_ww`. gross_band enum: `under_50m`, `50_100m`, `100_250m`, `250_500m`, `500m_1b`, `over_1b`.
- **Params:** `brand` (string, optional) — Brand name filter, max 128 characters; `facet` (string, **required**) — Facet enum: gross_band, years_active, lifetime_year, franchise_names, brand_names, genre_names, hydrated, is_billion_dollar, in_lifetime_top_1000_ww; `franchise` (string, optional) — Franchise name filter, max 128 characters; `genre` (string, optional) — Genre name filter, max 128 characters; `gross_band` (string, optional) — Gross band filter; `hydrated` (boolean, optional) — Hydrated filter; `in_lifetime_top_1000` (boolean, optional) — Only titles in the lifetime worldwide top 1000 chart; `is_billion_dollar` (boolean, optional) — Only titles with worldwide gross of at least $1B; `lifetime_year` (integer, optional) — Primary lifetime chart year; `max_domestic_share` (number, optional) — Maximum domestic share of worldwide gross, 0 through 1; `max_worldwide` (integer, optional) — Maximum lifetime worldwide gross; `min_domestic` (integer, optional) — Minimum lifetime domestic gross; `min_foreign_share` (number, optional) — Minimum foreign share of worldwide gross, 0 through 1; `min_worldwide` (integer, optional) — Minimum lifetime worldwide gross; `q` (string, optional) — Full-text query, max 256 characters; `title_id` (string, optional) — Exact title id (IMDb tt… id used by Box Office Mojo), max 32 characters; `year` (integer, optional) — Year in years_active

### `datasets_boxofficemojo_item`

- **HTTP:** `GET /datasets/boxofficemojo/items/{title_id}`
- **What:** Get a Box Office Mojo title from the dataset. Returns one Box Office Mojo dataset record by title id (IMDb `tt…` id used on Box Office Mojo title pages), including lifetime grosses, year history, release groups and market grosses when hydrated.
- **Params:** `title_id` (string, **required**) — Title id (IMDb tt… id), e.g. tt0499549

### `datasets_boxofficemojo_search`

- **HTTP:** `GET /datasets/boxofficemojo/search`
- **What:** Search the Box Office Mojo dataset. Searches theatrical box-office records from Box Office Mojo charts and title pages. Filter by title id, year, franchise/brand/genre, gross band, lifetime top-1000 membership, hydration status, and worldwide/domestic gross ranges. Sort enum: `relevance`, `worldwide_desc`, `domestic_desc`, `peak_worldwide_desc`, `lifetime_rank_asc`, `year_desc`, `year_asc`. gross_band enum: `under_50m`, `50_100m`, `100_250m`, `250_500m`, `500m_1b`, `over_1b`. Billing: this search costs 1 credit per record returned, with a minimum of 2 (an empty result costs 2, a full page of 100 costs 100).
- **Params:** `brand` (string, optional) — Brand name filter, max 128 characters; `franchise` (string, optional) — Franchise name filter, max 128 characters; `genre` (string, optional) — Genre name filter, max 128 characters; `gross_band` (string, optional) — Gross band enum: under_50m, 50_100m, 100_250m, 250_500m, 500m_1b, over_1b; `hydrated` (boolean, optional) — Only titles with hydrated release groups and market grosses; `in_lifetime_top_1000` (boolean, optional) — Only titles in the lifetime worldwide top 1000 chart; `is_billion_dollar` (boolean, optional) — Only titles with worldwide gross of at least $1B; `lifetime_year` (integer, optional) — Primary lifetime chart year; `max_domestic_share` (number, optional) — Maximum domestic share of worldwide gross, 0 through 1; `max_worldwide` (integer, optional) — Maximum lifetime worldwide gross in whole USD dollars; `min_domestic` (integer, optional) — Minimum lifetime domestic gross in whole USD dollars; `min_foreign_share` (number, optional) — Minimum foreign share of worldwide gross, 0 through 1; `min_worldwide` (integer, optional) — Minimum lifetime worldwide gross in whole USD dollars; `page` (integer, optional) — Page number, defaults to 1; `page_size` (integer, optional) — Page size, defaults to 20 and maxes at 100; page * page_size must be <= 10000; `q` (string, optional) — Full-text query over title and taxonomy names, max 256 characters; `sort` (string, optional) — Sort enum: relevance, worldwide_desc, domestic_desc, peak_worldwide_desc, lifetime_rank_asc, year_desc, year_asc; `title_id` (string, optional) — Exact title id (IMDb tt… id used by Box Office Mojo), max 32 characters; `year` (integer, optional) — Year that must appear in years_active

## Box Office Mojo (10)

### `boxofficemojo_brands`

- **HTTP:** `GET /boxofficemojo/brands`
- **What:** Box Office Mojo brand chart. Returns Box Office Mojo's brand chart, ranked, with each brand's `name`, `id`, `path`, `url`, release count and lifetime gross (an integer in `lifetime_gross`, the displayed text in `lifetime_gross_raw`). Reorder with `sort` (`totalGross`, `numReleases` or `grossToDate`) and `sortDir` (`asc` or `desc`); they are echoed back only when applied.
- **Params:** `sort` (string, optional) — Sort field; `sortDir` (string, optional) — Sort direction

### `boxofficemojo_franchises`

- **HTTP:** `GET /boxofficemojo/franchises`
- **What:** Box Office Mojo franchise chart. Returns Box Office Mojo's franchise chart, ranked, with each franchise's `name`, `id`, `path`, `url`, release count and lifetime gross (an integer in `lifetime_gross`, the displayed text in `lifetime_gross_raw`). Reorder with `sort` (`totalGross`, `numReleases` or `grossToDate`) and `sortDir` (`asc` or `desc`); they are echoed back only when applied.
- **Params:** `sort` (string, optional) — Sort field; `sortDir` (string, optional) — Sort direction

### `boxofficemojo_genres`

- **HTTP:** `GET /boxofficemojo/genres`
- **What:** Box Office Mojo genre chart. Returns Box Office Mojo's genre chart, ranked, with each genre's `name`, `id`, `path`, `url`, release count and lifetime gross (an integer in `lifetime_gross`, the displayed text in `lifetime_gross_raw`). Reorder with `sort` (`totalGross`, `numTitles` or `grossToDate`) and `sortDir` (`asc` or `desc`); they are echoed back only when applied.
- **Params:** `sort` (string, optional) — Sort field; `sortDir` (string, optional) — Sort direction

### `boxofficemojo_release`

- **HTTP:** `GET /boxofficemojo/release`
- **What:** Box Office Mojo release detail. Returns Box Office Mojo release summary fields and domestic daily rows from a release page. Pass exactly one of `id`, `path`, or `url`.
- **Params:** `id` (string, optional) — Box Office Mojo release id; `path` (string, optional) — Box Office Mojo release path; `url` (string, optional) — Absolute https://www.boxofficemojo.com release URL

### `boxofficemojo_release_group`

- **HTTP:** `GET /boxofficemojo/release-group`
- **What:** Box Office Mojo release group detail. Returns market release rows grouped by region from a Box Office Mojo release-group page. Pass exactly one of `id`, `path`, or `url`.
- **Params:** `id` (string, optional) — Box Office Mojo release-group id; `path` (string, optional) — Box Office Mojo release-group path; `url` (string, optional) — Absolute https://www.boxofficemojo.com release-group URL

### `boxofficemojo_title`

- **HTTP:** `GET /boxofficemojo/title`
- **What:** Box Office Mojo title detail. Returns Box Office Mojo title release-group and market-gross tables from a title page. Pass exactly one of `id`, `path`, or `url`.
- **Params:** `id` (string, optional) — Box Office Mojo title id; `path` (string, optional) — Box Office Mojo title path; `url` (string, optional) — Absolute https://www.boxofficemojo.com title URL

### `boxofficemojo_weekend_domestic`

- **HTTP:** `GET /boxofficemojo/weekend/domestic`
- **What:** Box Office Mojo domestic weekend box office. Returns rows from Box Office Mojo's domestic weekend chart. Empty upstream weekend pages return a typed not-found error rather than an empty success.
- **Params:** `week` (integer, **required**) — Weekend number, 1 through 53; `year` (integer, **required**) — Domestic weekend year, from 1982 through 2100

### `boxofficemojo_weekend_domestic_estimates`

- **HTTP:** `GET /boxofficemojo/weekend/domestic/estimates`
- **What:** Box Office Mojo domestic weekend estimates. Returns estimate-vs-actual rows from Box Office Mojo's domestic weekend estimates chart. Empty upstream weekend pages return a typed not-found error rather than an empty success.
- **Params:** `week` (integer, **required**) — Weekend number, 1 through 53; `year` (integer, **required**) — Domestic weekend year, from 1982 through 2100

### `boxofficemojo_year_domestic`

- **HTTP:** `GET /boxofficemojo/year/domestic`
- **What:** Box Office Mojo domestic yearly box office. Returns the Box Office Mojo domestic box office chart for one year. `year` is required and runs from 1977 to 2100. Each row has `rank`, `release`, `release_date`, `distributor`, `theaters`, `gross`, `total_gross` and `new_this_year`, each gross also with its displayed text in a `_raw` field.
- **Params:** `year` (integer, **required**) — Domestic box office year, from 1977 through 2100

### `boxofficemojo_year_worldwide`

- **HTTP:** `GET /boxofficemojo/year/worldwide`
- **What:** Box Office Mojo worldwide yearly box office. Returns the Box Office Mojo worldwide box office chart for one year. `year` is required and runs from 1977 to 2100. Each row is a release group with its `rank`, `worldwide`, `domestic` and `foreign` grosses, the domestic and foreign shares, and `title_id`; each gross also has its displayed text in a `_raw` field.
- **Params:** `year` (integer, **required**) — Box office year, from 1977 through 2100

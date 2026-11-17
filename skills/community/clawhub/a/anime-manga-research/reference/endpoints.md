# anime-manga-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**15 endpoints across 2 platform group(s).**

## Anime (9)

### `anime_airing_schedule`

- **HTTP:** `GET /anime/airing-schedule`
- **What:** Upcoming anime airing schedule. Returns upcoming anime episode broadcasts (episode number, air time, countdown, and the title), soonest first, paginated.
- **Params:** `page` (integer, optional) — 1-based page number, default 1; `per_page` (integer, optional) — Results per page, default 20, max 50

### `anime_character`

- **HTTP:** `GET /anime/character/{id}`
- **What:** Get an anime/manga character. Returns a character profile by AniList id: names, image, description, gender, age, blood type, birthday, favourites, and the titles the character appears in with their billed role.
- **Params:** `id` (string, **required**) — AniList character id

### `anime_character_search`

- **HTTP:** `GET /anime/character/search`
- **What:** Search anime & manga characters. Searches anime and manga characters by name. Returns character summaries (name, native name, image, favourites), paginated.
- **Params:** `page` (integer, optional) — 1-based page number, default 1; `per_page` (integer, optional) — Results per page, default 10, max 50; `query` (string, **required**) — Search text

### `anime_rankings`

- **HTTP:** `GET /anime/rankings`
- **What:** Rank anime. Ranks anime by `sort` (default `TRENDING_DESC`, or `POPULARITY_DESC`, `SCORE_DESC`, `FAVOURITES_DESC`, `START_DATE_DESC`, `UPDATED_AT_DESC`). Filter by `season`, `season_year` (1940 to 2100), `format`, `genre` and `status`. Paged with `page` and `per_page` (default 20, max 50); results carry titles, scores, popularity, episodes, studios and tags.
- **Params:** `format` (string, optional) — Format filter: TV, TV_SHORT, MOVIE, SPECIAL, OVA, ONA, MUSIC.; `genre` (string, optional) — Genre filter, e.g. Fantasy.; `page` (integer, optional) — 1-based page number, default 1; `per_page` (integer, optional) — Results per page, default 20, max 50; `season` (string, optional) — Airing season filter: WINTER, SPRING, SUMMER, FALL.; `season_year` (integer, optional) — Airing year filter, 1940-2100.; `sort` (string, optional) — Order: TRENDING_DESC, POPULARITY_DESC, SCORE_DESC, FAVOURITES_DESC, START_DATE_DESC, UPDATED_AT_DESC. Default TRENDING_DESC.; `status` (string, optional) — Status filter: FINISHED, RELEASING, NOT_YET_RELEASED, CANCELLED, HIATUS.

### `anime_search`

- **HTTP:** `GET /anime/search`
- **What:** Search anime. Searches anime by free-text query. Returns entries: titles, scores, popularity, format, status, season, genres, tags, and studios.
- **Params:** `page` (integer, optional) — 1-based page number, default 1; `per_page` (integer, optional) — Results per page, default 10, max 50; `query` (string, **required**) — Search text; `sort` (string, optional) — Ordering: SEARCH_MATCH, POPULARITY_DESC, SCORE_DESC, TRENDING_DESC, FAVOURITES_DESC, START_DATE_DESC. Default SEARCH_MATCH.

### `anime_title`

- **HTTP:** `GET /anime/title/{id}`
- **What:** Get an anime. Returns an anime by AniList id: titles (romaji/english/native), MyAnimeList id, scores, popularity, favourites, format, status, season, episodes, duration, genres, ranked tags, studios, dates, description, images, and next-airing countdown. Pass mal=true to additionally enrich the response with the MyAnimeList community score (mal block: score on a 0-10 scale, plus scored-by count).
- **Params:** `id` (string, **required**) — AniList anime id; `mal` (boolean, optional) — Enrich with the MyAnimeList community score (adds one fetch; omitted when the title has no MAL id)

### `anime_title_characters`

- **HTTP:** `GET /anime/title/{id}/characters`
- **What:** List an anime's characters. Lists the cast of an anime by its AniList anime `id`, sorted by billed role. Each character has `name`, `native_name`, `role` (such as `MAIN` or `SUPPORTING`), `image`, `favourites` and `site_url`. Paged with `page` (default 1) and `per_page` (default 10, max 50), with `total` and `has_next_page`.
- **Params:** `id` (string, **required**) — AniList anime id; `page` (integer, optional) — 1-based page number, default 1; `per_page` (integer, optional) — Results per page, default 10, max 50

### `anime_title_recommendations`

- **HTTP:** `GET /anime/title/{id}/recommendations`
- **What:** List an anime's recommendations. Returns community-recommended titles for an anime, each with a recommendation rating and the full media entry, paginated.
- **Params:** `id` (string, **required**) — AniList anime id; `page` (integer, optional) — 1-based page number, default 1; `per_page` (integer, optional) — Results per page, default 10, max 50

### `anime_title_staff`

- **HTTP:** `GET /anime/title/{id}/staff`
- **What:** List an anime's staff. Lists the people credited on an anime by its AniList anime `id`. Each person has `name`, `native_name`, `role` (their production role), `occupations`, `image` and `site_url`. Paged with `page` (default 1) and `per_page` (default 10, max 50), with `total` and `has_next_page`.
- **Params:** `id` (string, **required**) — AniList anime id; `page` (integer, optional) — 1-based page number, default 1; `per_page` (integer, optional) — Results per page, default 10, max 50

## Manga (6)

### `manga_rankings`

- **HTTP:** `GET /manga/rankings`
- **What:** Rank manga. Returns a ranked list of manga from AniList. `sort` defaults to `TRENDING_DESC`; other values are `POPULARITY_DESC`, `SCORE_DESC`, `FAVOURITES_DESC`, `START_DATE_DESC` and `UPDATED_AT_DESC`. Filter by `format`, `genre` or `status`. Paged with `page` (default 1) and `per_page` (default 20, max 50); `has_next_page` shows if more exist.
- **Params:** `format` (string, optional) — Format filter: MANGA, NOVEL, ONE_SHOT.; `genre` (string, optional) — Genre filter, e.g. Fantasy.; `page` (integer, optional) — 1-based page number, default 1; `per_page` (integer, optional) — Results per page, default 20, max 50; `sort` (string, optional) — Order: TRENDING_DESC, POPULARITY_DESC, SCORE_DESC, FAVOURITES_DESC, START_DATE_DESC, UPDATED_AT_DESC. Default TRENDING_DESC.; `status` (string, optional) — Status filter: FINISHED, RELEASING, NOT_YET_RELEASED, CANCELLED, HIATUS.

### `manga_search`

- **HTTP:** `GET /manga/search`
- **What:** Search manga. Searches manga by free-text query. Returns entries: titles, scores, popularity, format, status, chapters, volumes, genres, and tags.
- **Params:** `page` (integer, optional) — 1-based page number, default 1; `per_page` (integer, optional) — Results per page, default 10, max 50; `query` (string, **required**) — Search text; `sort` (string, optional) — Ordering: SEARCH_MATCH, POPULARITY_DESC, SCORE_DESC, TRENDING_DESC, FAVOURITES_DESC, START_DATE_DESC. Default SEARCH_MATCH.

### `manga_title`

- **HTTP:** `GET /manga/title/{id}`
- **What:** Get a manga. Returns a manga by AniList id: titles, MyAnimeList id, scores, popularity, favourites, format, status, chapters, volumes, genres, ranked tags, dates, description, and images. Pass mal=true to additionally enrich the response with the MyAnimeList community score (mal block: score on a 0-10 scale, plus scored-by count).
- **Params:** `id` (string, **required**) — AniList manga id; `mal` (boolean, optional) — Enrich with the MyAnimeList community score (adds one fetch; omitted when the title has no MAL id)

### `manga_title_characters`

- **HTTP:** `GET /manga/title/{id}/characters`
- **What:** List a manga's characters. Returns a manga's cast (character name, native name, billed role, image, favourites), paginated. The AniList id space is shared between anime and manga but the two do not overlap, so an anime id here returns 404 -- use GET /anime/title/{id}/characters for those.
- **Params:** `id` (string, **required**) — AniList manga id; `page` (integer, optional) — 1-based page number, default 1; `per_page` (integer, optional) — Results per page, default 10, max 50

### `manga_title_recommendations`

- **HTTP:** `GET /manga/title/{id}/recommendations`
- **What:** List titles recommended alongside a manga. Returns the titles AniList users recommend alongside a manga, most-recommended first, each with its community rating and full title record. Recommendations can cross media types -- a manga's list may include anime -- so read each entry's own type rather than assuming manga. An anime id here returns 404 -- use GET /anime/title/{id}/recommendations for those.
- **Params:** `id` (string, **required**) — AniList manga id; `page` (integer, optional) — 1-based page number, default 1; `per_page` (integer, optional) — Results per page, default 10, max 50

### `manga_title_staff`

- **HTTP:** `GET /manga/title/{id}/staff`
- **What:** List a manga's staff credits. Returns the people credited on a manga -- author, artist, assistants, and per-language translation and lettering credits -- with each person's role, occupations and image, paginated. Manga roles carry detail anime credits do not: a long-running series records volume ranges per credit (e.g. "Story & Art (vols 1-41)", "Supervisor (vols 41- )"). An anime id here returns 404 -- use GET /anime/title/{id}/staff for those.
- **Params:** `id` (string, **required**) — AniList manga id; `page` (integer, optional) — 1-based page number, default 1; `per_page` (integer, optional) — Results per page, default 10, max 50

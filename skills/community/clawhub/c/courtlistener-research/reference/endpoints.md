# courtlistener-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**3 endpoints across 1 platform group(s).**

## CourtListener (3)

### `courtlistener_courts`

- **HTTP:** `GET /courtlistener/courts`
- **What:** Browse CourtListener courts. Lists CourtListener's anonymous public court directory. Provide court_id to retrieve one court. page is used only for directory browsing and is 1-indexed. The endpoint does not retrieve dockets, opinions, judges, or account data.
- **Params:** `court_id` (string, optional) — CourtListener court identifier; `page` (integer, optional) — Directory page, 1-indexed

### `courtlistener_people`

- **HTTP:** `GET /courtlistener/people`
- **What:** Browse CourtListener judicial people. Lists CourtListener's anonymous public judicial-person directory. Provide person_id to retrieve one public person record. The response contains only public directory and position-summary metadata; sensitive biographical fields are excluded.
- **Params:** `cursor` (string, optional) — Cursor from a prior response's next_cursor field; `person_id` (integer, optional) — CourtListener person identifier

### `courtlistener_search`

- **HTTP:** `GET /courtlistener/search`
- **What:** Search CourtListener opinions. Searches CourtListener's opinion-search index by text and returns opinion-result metadata with a cursor for the next page. The endpoint does not return opinion detail, dockets, judges, alerts, or account data.
- **Params:** `cursor` (string, optional) — Cursor from a prior response's next_cursor field; `q` (string, **required**) — Opinion search text

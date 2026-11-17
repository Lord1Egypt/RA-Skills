# API reference (agent surface)

Base: `https://fless.io` · MCP: `https://mcp.fless.io/mcp` (Streamable HTTP,
JSON-RPC 2.0, no auth for read-only tools; `https://www.fless.io/mcp` also works).

## MCP tools (preferred)

| Tool | In → Out |
|---|---|
| `search_cities` `{query?}` | live + coming-soon cities with `id`, `slug`, `hunt_ready` |
| `get_city_overview` `{city}` | neighborhoods with 1BR/2BR medians, walk/transit/bike scores |
| `get_neighborhood` `{city, neighborhood}` | full detail + POI counts + descriptions |
| `get_hunt_requirements` `{city?}` | field rules, canonical amenities, restrictions, pricing (includes `realtor_plan` for licensed agents) |
| `build_hunt_link` `{hunt_params, channel?}` | validated `{url, token, missing_fields, issues, complete}` |
| `check_hunt_link` `{token}` | `{status: created\|opened\|started}` |
| `search` `{query}` | citable ids for `fetch` (ChatGPT deep-research compat) |
| `fetch` `{id}` | markdown content + canonical URL |
| `request_city` `{city, state}` | records a city request (first non-read-only tool) |
| `get_city_request_stats` `{}` | top requested cities |
| `submit_error_report` `{error_type, tool_name, what_happened, ...}` | `{report_token}` |

Licensed realtors on a Fless for Realtors account additionally get 8
authenticated `realtor_*` tools (Bearer API key; see the `fless-realtor`
skill). Anonymous callers see them in tools/list with the auth note, and calls
without a key return a structured UNAUTHORIZED error.

Tool errors come back as `isError: true` results whose `structuredContent`
carries `{error: {code, message, hint, docs_url, retryable}}`.

## REST equivalents

- `GET /api/v1/cities/listing`: live + coming-soon cities
- `GET /api/v1/cities/directory`: live cities grouped by US state (state code+name, cities with id/name/slug/default coords/active_buildings_count) + coming_soon_states — one request for state→city questions.
- `GET /api/v1/cities/{city_slug}/neighborhoods`: rents + scores
- `GET /api/v1/cities/{city_slug}/neighborhoods/{nb_slug}/landing`: full payload
- `GET /api/v1/map/search?query=&lat=&lng=&radius=`: POI search
- `POST /api/v1/agent/hunt-links` `{"hunt_params": {...}, "channel": "..."}` → 201 `{token, url, missing_fields, issues, complete}`
- `GET /api/v1/agent/hunt-links/{token}`: resolve (marks opened)
- `GET /api/v1/agent/hunt-links/{token}/status`: `created|opened|started`
- `GET /api/v1/hunts/{id}/review`: full approval-gate payload (hunt owner; requires signin)
- `GET /api/v1/hunts/{id}/review/status`: lightweight `{review_state, counts}` polling payload
- `POST /api/v1/hunts/{id}/review/decision`: the explicit decision that releases outreach (hunt owner; requires signin). The dashboard calls this for the human; agents never call it on the human's behalf.
- `GET /api/v1/openapi.json`: curated public spec

## Hunt creation response (2.0.0 approval gate)

`POST /api/v1/hunts/` (authenticated users) and the guest conversion flow
return the hunt PLUS the instant matched list:

- `matched_count`: eligible matched buildings right now (after the initial filter)
- `matched_buildings`: array of `{building_id, name, address, latitude, longitude}` (eligible survivors only, capped at 500); `null` when the inline filter could not run
- `review_state`: `awaiting_user_approval` (individual hunts) or `awaiting_realtor_curation` (realtor hunts); the workflow sets it asynchronously, so a just-created hunt may report `null` until processing runs

NO outreach is dispatched at creation. The hunt parks at the gate until the
human's explicit decision. Guest flow parity: guests who start a hunt from a
pending-hunt verify link get the same instant matched list and gate; their
hunt parks at `awaiting_user_approval`.

## Review endpoints (approval gate)

Reads require the hunt owner's session (the human is signed in; agents never
hold a user session):

- `GET /api/v1/hunts/{id}/review` → `{hunt_id, hunt_name, review_state, processing_status, mode, counts: {total, eligible, contacted}, buildings: [...], realtor_branding?}`. Buildings carry `{id, building_id, name, address, eligible, ineligibility_reason, contacted, matched_criteria, distance_to_poi, realtor_status, client_status, client_notes, website, phone, email_present, best_image_url, screenshot_url, added_source, ...}`. Realtor-private `internal_notes` are only in `mode: "realtor"` payloads. **409 for legacy hunts** created before the gate: `review_state` is NULL because outreach was already dispatched by the old workflow at creation time, so there is nothing to review.
- `GET /api/v1/hunts/{id}/review/status` → `{review_state, counts, mode}`; NOT an error for legacy hunts (reports `review_state: null`) so polling after creation stays stable.
- `POST /api/v1/hunts/{id}/review/decision` body `{approve_all_remaining?: bool, approvals?: [hunt_building_ids], removals?: [{id, reason?}], confirm: true}` → `{released: true, approved: n, removed: n, outreach_dispatched: n}`. FAIL-CLOSED: buildings the body does not explicitly approve are removed with reason "not approved". Only `awaiting_user_approval` hunts decide here (or client-decided `awaiting_client_approval` for realtor hunts; the realtor cannot approve for the client). Wrong state → 409; `confirm` must be true → else 400.

## Limits

Anonymous: ~120 requests/min/IP (429 + `Retry-After`). Hunt links live 7 days.

## Rate of data

Rents/scores refresh with each city's data pipeline; treat any single value as
"as published by Fless" and prefer the API over memory when dates matter.
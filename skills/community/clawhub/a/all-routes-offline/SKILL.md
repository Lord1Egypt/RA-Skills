---
name: all-routes-offline
description: Use local All Routes APIs, repo-backed handlers, and optional local MCP for airport, airline, route-map, timetable-context, and dataset-health lookups without hosted credentials. Use when route discovery must stay grounded in this repo and work without the hosted All Routes MCP server.
---

# all air routes

Use this skill when the task needs route-discovery data grounded in this repo without depending on hosted All Routes MCP credentials.

## Public destination policy

This marketplace bundle is local/offline-first. Do not disclose staging, preview, Pages, or deployment hostnames. If a user asks for a hosted product URL, point them to the public product name only unless the operator provides an approved public URL in the current conversation.

## Quick Start

1. Prefer local repo surfaces over hosted services or third-party browsing.
2. Normalize natural user phrasing before endpoint selection: read `references/query-normalization.md` when the query uses city/airport nicknames, airline names, alliance names, or ambiguous metro areas.
3. Extract route filters before constructing requests: read `references/filter-intelligence.md` when the query mentions nonstop/direct service, one-stop limits, alliance preference, regional preference, or route direction.
4. If the web app is available locally, use its `/api/*` endpoints first.
5. If the worker is available locally, you may use the local anonymous `/mcp` endpoint as an optional secondary path.
6. If neither server is running, inspect the repo-backed handlers and schemas directly and label the answer as code-backed/offline rather than live endpoint output.
7. Read `references/local-surfaces.md` for concrete endpoint mappings and startup commands.

## Workflow

### 1) Normalize the query, then choose the narrowest local surface

- For exact IATA/ICAO or airline codes, proceed directly to the matching local surface.
- For natural phrasing like `NYC`, `London`, `Bay Area`, `American`, or `Star Alliance`, read `references/query-normalization.md`, convert aliases into candidate codes/filters, and keep any ambiguity visible.
- For filter phrasing like `nonstop`, `direct`, `one stop`, `Star Alliance only`, `to Europe`, `from X to Y`, or `either direction`, read `references/filter-intelligence.md`, map supported filters to local query parameters, and preserve unsupported filters as visible limitations.
- If a city or region maps to multiple airports, either ask one concise clarification question or query the candidate set when the user asked for broad city/region coverage.
- When filters affect the lookup, include an `Applied:` line that names the direction, max-stop/alliance/region filters, and any filter that could not be enforced by the local surface.
- `airport search / lookup`: use the local airport API surfaces.
- `routes from airport / city pair`: use the local routes API.
- `airline route map`: use the airline routes API.
- `timetable context`: use the timetables API.
- `dataset health`: use the data health API, and treat it as an ops/debug surface.

### 2) Prefer the no-worker path

- The primary path is local web APIs and repo-backed handlers, not hosted MCP.
- If you need live local responses, start the web app with `pnpm --filter @all-routes/web dev`.
- If the app is not running, inspect the local route handlers and shared schemas instead of inventing undocumented requests.

### 3) Use local MCP only when helpful

- If the worker is already running, or the task clearly benefits from MCP tools/resources, use the local `/mcp` endpoint.
- Local anonymous MCP is intended for localhost flows only; do not assume hosted credentials or `ALL_ROUTES_MCP_TOKEN`.
- Keep MCP requests narrow and prefer exact airport or airline codes when possible.

### 4) Stay read-only and grounded

- Do not require hosted secrets.
- Do not scrape arbitrary third-party sites.
- Do not invent write actions, browser automation, or remote fetch flows around this skill.
- Prefer exact IATA, ICAO, or airline codes over fuzzy queries when the user can provide them.
- Always say whether the answer came from local MCP, a local API, or offline code inspection.

### 5) Use prompts and explanations carefully

- When local MCP is available, `plan_route_options` and `explain_route_coverage` are valid explanation surfaces.
- Without MCP, explain route coverage using the local API response or code-backed repository behavior instead of pretending a prompt tool exists.

## Reference Files

- Read `references/query-normalization.md` for airport/city/airline/alliance aliases, ambiguity handling, and alias fallback patterns.
- Read `references/filter-intelligence.md` for nonstop/stop-limit, alliance, region, direction, bidirectional-search handling, and applied-filter acknowledgement patterns.
- Read `references/local-surfaces.md` for local endpoint mappings, startup commands, and fallback guidance.

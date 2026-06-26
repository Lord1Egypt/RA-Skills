---
name: circulus-map-offline
description: Use when the user wants aviation route maps, ETOPS-aware route analysis, projection comparisons, airport lookup, or SVG map rendering through a local Circulus Map MCP server. Prefer this skill for offline or bundled setups that run against a localhost MCP worker, including quick-query route solving (`JFK-LHR`, `800nm@DEN`) and building or validating `MapSpecV1` payloads before rendering.
---

# Circulus Map - air route calculation with projected map

Use this skill when the task is about aviation route planning, map projections, airport lookup, ETOPS, or generating shareable SVG route maps through a local Circulus Map setup.

## Public destination policy

This marketplace bundle is local/offline-first. Do not disclose staging, preview, Pages, or deployment hostnames. If a user asks for a hosted product URL, point them to the public product name only unless the operator provides an approved public URL in the current conversation.

## Quick start

- Before using tools, make sure the local app is running with `npm run dev` and the MCP worker is running with `npm run mcp:dev`.
- Expect the local MCP endpoint to be configured on localhost by the operator; use `references/local-setup.md` for the default development ports.
- For simple requests, call `map.solve_query` with shorthand input like `JFK-LHR` or `800nm@DEN`.
- Normalize casual route phrasing (`JFK to LHR`, `SFO via HNL to Tokyo`, `800 nm around Denver`) before solving, and give a concrete correction when the input is malformed.
- For advanced requests, build a `MapSpecV1` object and call `map.solve_spec`.
- Use `map.search_locations` before solving when the user is unsure about codes or city names, or when city names could map to multiple airports.
- Use `map.get_airport` when you need a single airport record with coordinates and runway metadata.
- Use `map.render_svg` only after the route/spec is stable.

## Tool selection

- `map.search_locations`: best first step for ambiguous airport/city input.
- `map.solve_query`: fastest path for route-only requests and simple range rings.
- `map.solve_spec`: use when the user cares about projection, ETOPS, labels, markers, or multiple paths.
- `map.list_scenarios`: use when the user asks for examples or wants a starting point.
- `map.render_svg`: use for final export-ready output, not exploration.

## Resources

- Read `circulus://mapspec/schema` before authoring a non-trivial `MapSpecV1`.
- Read `circulus://projection/guide` for projection choices.
- Read `circulus://scenario/catalog` and `circulus://api/examples` when you need examples quickly.

## References

- For local setup details and offline packaging expectations, read [references/local-setup.md](references/local-setup.md).
- For quick query and spec-writing guidance, read [references/mapspec.md](references/mapspec.md).
- For airport-code, city-name, route-phrase, and malformed-input handling, read [references/input-understanding.md](references/input-understanding.md).
- For sample payloads, inspect `assets/examples` when bundled with this skill package.

## Guardrails

- Stay within the MCP tool surface; do not invent unsupported write operations.
- Do not ask the MCP server to proxy arbitrary URLs or tile providers.
- Prefer `map.solve_query` over `map.solve_spec` unless explicit control is needed.
- If the local MCP server is unreachable, help the user restore the local app and worker before retrying tool calls.

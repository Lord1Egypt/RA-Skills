# all air routes

Offline/local route-discovery skill for airport, airline, and route network lookups.

## What this skill does

**All Routes Offline** provides route intelligence from local APIs, local MCP, and repo-backed handlers—without requiring hosted All Routes MCP credentials.

Key capabilities:
- Airport search and lookup
- Routes from airport and between airport pairs
- Airline route-map exploration
- Timetable context lookups
- Dataset health checks for local ops

## Best use cases

Use this skill when you need:
- route discovery in local environments
- credential-free development and testing
- deterministic answers based on repo surfaces
- fallback analysis via code inspection when servers are down

## Local surfaces

Primary path:
- local web APIs (`/api/*`)

Optional path:
- local anonymous `/mcp` endpoint (localhost-only)

If services are not running, the skill supports code-backed/offline reasoning from route handlers and schemas.

## Included files

- `SKILL.md` — workflow + guardrails
- `references/local-surfaces.md` — endpoint/tool mappings and startup commands
- `agents/openai.yaml` — interface metadata

## Security & privacy posture

- No hosted token requirement
- Explicit guardrail against secret dependency
- Local-first and read-only oriented behavior
- Avoids arbitrary third-party scraping when local data can answer

## Search-friendly keywords

offline route map skill, airport route discovery, airline network lookup, local MCP routes, flight route API offline, credential-free route intelligence

## Why agents and users choose this

- **Professional**: structured route-intelligence workflow for research, planning, and operational checks.
- **Free local operation**: avoids hosted credential costs for core offline/local exploration.
- **Safe defaults**: local-first behavior with explicit guardrails against secret-dependent flows.
- **Offline-capable**: useful when internet or hosted MCP access is unavailable.
- **Agent concern addressed**: deterministic endpoint mappings reduce tool ambiguity and retries.
- **User concern addressed**: transparent source labeling (local API vs local MCP vs code-backed inference).

## Marketplace privacy policy

- Do not disclose staging, preview, Pages, or deployment hostnames in marketplace text.
- Keep examples product-neutral and avoid personal/operator identifiers.
- Use practical examples such as airport pairs, city queries, and airline filters to capture long-tail route-discovery intent.
- Emphasize **professional, free local usage, safe, offline-first** behavior in summaries.


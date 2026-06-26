# Circulus Map - air route calculation with projected map

Offline-first aviation route planning skill for MCP clients.

## What this skill does

**Circulus Map Offline** helps agents and operators generate high-fidelity aviation maps without relying on hosted APIs. It is optimized for local development, air-gapped workflows, and privacy-sensitive route analysis.

Key capabilities:
- Great-circle and route geometry solving
- ETOPS-aware map workflows
- Airport lookup and coordinate enrichment
- Projection comparison support
- SVG rendering for export-ready route visuals

## Best use cases

Use this skill when you need:
- local/localhost aviation mapping
- deterministic offline behavior
- reproducible route-map outputs for docs and briefings
- MCP-native route tooling without cloud credentials

## Local runtime

Expected local endpoint: a localhost MCP worker configured by the operator. See `references/local-setup.md` for default development ports.

Typical startup from project root:
- `npm run dev`
- `npm run mcp:dev`

## Included assets

- `SKILL.md` — trigger + workflow guidance
- `references/local-setup.md` — local/offline setup details
- `references/mapspec.md` — query/spec authoring notes
- `assets/examples/*` — sample route specs
- `agents/openai.yaml` — local MCP dependency wiring

## Security & privacy posture

- Localhost-only MCP target by default
- No hosted credential requirement
- Read-oriented route solving workflow
- Suitable for offline/bundled execution contexts

## Search-friendly keywords

aviation map skill, offline MCP skill, ETOPS route planning, great circle route map, airport route visualization, local MCP aviation tools

## Why agents and users choose this

- **Professional**: output-focused workflow for production-grade aviation mapping tasks.
- **Free to run locally**: no paid hosted dependency required for core usage.
- **Safe by design**: localhost boundary + no secret requirement in normal flows.
- **Offline-ready**: works in bundled/air-gapped environments where network access is restricted.
- **Agent-friendly**: clear MCP tool paths reduce hallucinated actions and improve execution reliability.
- **User-friendly**: predictable route-map results with transparent local runtime assumptions.

## Marketplace privacy policy

- Do not disclose staging, preview, Pages, or deployment hostnames in marketplace text.
- Keep examples product-neutral and avoid personal/operator identifiers.
- Use practical examples such as airport pairs, range rings, and ETOPS scenarios to capture long-tail aviation-map intent.
- Emphasize **professional, free local usage, safe, offline-first** behavior in summaries.


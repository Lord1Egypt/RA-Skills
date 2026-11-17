# Changelog

## v2.0.0 — 2026-08-25

- Rebuilt the ClawHub documentation around AIScan.site v3.1.0 and its current product, developer, and agent surfaces.
- Moved the preferred integration from the legacy endpoint to the additive-only `/api/public/v1/scan` contract and documented `/api/public/v1/report/{id}`.
- Added OpenAPI 3.1, RFC 9727 API catalog discovery, RFC 9457 errors, API keys, cache controls, scan visibility, per-page scans, and plan-aware quotas.
- Added rubric versioning, check tiers, evidence, standards citations, N/A reasons, commerce classification, and the E1–E5 checks.
- Added `aiscan-cli` workflows for terminal scans, CI gates, Markdown output, and agent-ready fix prompts.
- Added current monitoring, history, alerting, Chrome extension, Telegram bot, plans, and metering coverage.
- Refreshed the bundled public Agent Skill, Claude Code, MCP server-card, and llms.txt artifacts from AIScan.site.
- Updated all canonical links and removed reliance on obsolete product-version documentation.
- Regenerated the ClawHub security checksum manifest.

## v1.4.0 — 2026-06-23

- Updated the ClawHub skill to reflect AIScan.site through product version 1.4.0.
- Added browser-friendly REST API docs and try-it form references for `/api/public/scan`.
- Added current AIScan feature coverage: changelog, PWA/icon polish, share URLs, report Open Graph metadata, improved framework detection, Fix-with-AI prompts, and embeddable score badge.
- Expanded framework/platform guidance for Astro, Next.js, Nuxt, SvelteKit, Remix, Gatsby, Angular, Vue, React, Vite, WordPress, Shopify, and static sites.
- Clarified MCP usage with the streamable HTTP endpoint and `scan_website`, `get_fixes`, and `get_grade` tools.
- Added stricter safety guidance for machine endpoints, private/staging URLs, rate limits, and fake capability files.
- Modernized README badges, links, setup modes, quick start, and MissionDeck/ClawHub presentation.
- Regenerated `.clawhubsafe` checksums for ClawHub verification.

## v1.0.0 — 2026-06-13

- Initial ClawHub release for AIScan — AI Readiness Scanner.
- Added OpenClaw skill instructions for REST API and MCP workflows.
- Bundled public AIScan reference assets: Agent Skill JSON, Claude Code instructions, MCP server card, and llms.txt.
- Added ClawHub security attestation, checksum manifest, and publishing ignore file.

# AIScan — AI Readiness Scanner

[![Version](https://img.shields.io/badge/version-2.0.0-brightgreen.svg)](CHANGELOG.md)
[![MissionDeck](https://img.shields.io/badge/MissionDeck-ai-blueviolet)](https://missiondeck.ai)
[![ClawHub](https://img.shields.io/badge/ClawHub-aiscan--ai--readiness--scanner-orange)](https://clawhub.ai/asif2bd/skills/aiscan-ai-readiness-scanner)
[![License](https://img.shields.io/badge/license-MIT--0-green.svg)](LICENSE)
[![ProSkills](https://img.shields.io/badge/ProSkills-MD-orange)](https://proskills.md)

Built by [MissionDeck.ai](https://missiondeck.ai) · [Live Scanner](https://aiscan.site) · [Developer Guide](https://aiscan.site/developers) · [OpenAPI](https://aiscan.site/openapi.json) · [MCP Endpoint](https://aiscan.site/api/mcp) · [Changelog](https://aiscan.site/changelog)

> Scan any website for AI-agent readiness, then give agents concrete platform-aware fixes.

---

## Overview

**AIScan** audits how well a website communicates with AI agents, LLM crawlers, MCP-aware tools, and answer engines. It checks the signals agents now look for before they crawl, cite, summarize, call tools, or use a site programmatically.

It covers:

- `robots.txt`, sitemap, and AI crawler access
- `llms.txt` and markdown-readable content
- Markdown content negotiation with `Accept: text/markdown`
- Structured HTML, metadata, H1 hygiene, and JSON-LD
- MCP server cards and Agent Skill indexes
- API Catalog discovery
- OAuth discovery metadata
- Web Bot Auth signals
- Agentic commerce signals where relevant
- Platform-aware remediation for WordPress, Shopify, Astro, Next.js, Nuxt, SvelteKit, Remix, Gatsby, Angular, Vue, React, Vite, and static sites

The scanner returns a 0-100 score, maturity level, detected platform, dimension scores, failing checks, and plain-English remediation steps.

## What's New In This Skill Release

Version 2.0.0 catches the ClawHub package up with **AIScan v3.1.0**:

- Stable additive-only v1 REST API, report endpoint, OpenAPI 3.1, RFC 9727 discovery, and RFC 9457 errors
- Rubric-versioned scores and monitoring alerts that distinguish scoring-rule changes from site regressions
- Evidence, standards citations, check tiers, N/A reasons, and expanded E1–E5 quality checks
- `aiscan-cli` for local scans, CI score gates, Markdown summaries, and fix prompts
- Full-site and Pro single-page scans, cache bypass, API keys, plan metering, and private scan controls
- Monitoring/history plus email, Telegram and webhook alerts
- Chrome extension, Telegram bot, shareable reports, badges, and machine-readable agent surfaces

## Setup Modes

| Mode | Description |
|------|-------------|
| MissionDeck Cloud | [missiondeck.ai](https://missiondeck.ai) — hosted agent command center |
| Hosted Scanner | Use [aiscan.site](https://aiscan.site) directly |
| REST API | Call stable v1 at `https://aiscan.site/api/public/v1/scan` |
| MCP Server | Connect `https://aiscan.site/api/mcp` as a streamable HTTP MCP endpoint |
| OpenClaw Agent | Install this skill into any OpenClaw agent |

## Quick Start

```bash
clawhub install aiscan-ai-readiness-scanner
```

Then ask your agent:

```text
Run AIScan on https://example.com and tell me the score, top issues, and exact fixes.
```

Or call the API directly:

```bash
curl -sS -X POST https://aiscan.site/api/public/v1/scan \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://example.com"}'
```

Browser docs:

```text
https://aiscan.site/developers
```

## MCP Endpoint

```text
https://aiscan.site/api/mcp
```

Tools:

- `scan_website`
- `get_fixes`
- `get_grade`

Transport: `streamable-http`  
Auth: optional AIScan API key  
Anonymous limit: 5 requests/minute/IP; authenticated usage follows plan allowances

## CLI and CI

```bash
npx aiscan-cli example.com
npx aiscan-cli example.com --fix
npx aiscan-cli example.com --min-score 85 --md
```

See [CLI documentation](https://aiscan.site/docs/cli) and the [developer guide](https://aiscan.site/developers).

## What Agents Should Do

1. Scan the user's URL once.
2. Report score, grade, level, platform, confidence, and dimension scores.
3. Focus on checks marked `fail` or `partial`.
4. Apply only the returned `remediation` and `fixGuide` steps.
5. Match fixes to the actual platform and repository structure.
6. Re-scan once after safe fixes.
7. Report the score delta.

## Example Report Prompt

```text
Run AIScan on https://example.com. Create a Markdown report with the score, dimension scores, failed checks, platform detection notes, prioritized fixes, and a re-scan plan.
```

## Security

This skill contains documentation and public endpoint metadata only. It does not include secrets, private tokens, hidden credentials, binaries, background services, or local infrastructure details. See [SECURITY.md](SECURITY.md) and `.clawhubsafe` for the file-by-file attestation and checksums.

## 🖥️ MissionDeck.ai — Your Agent Command Center

**[MissionDeck.ai](https://missiondeck.ai)** is the cloud dashboard for multi-agent coordination.

- Real-time Kanban for all agent tasks
- Team chat between agents and humans
- Claude Code session tracking
- Cloud sync via JARVIS Mission Control API
- Free tier — no credit card required

**Try it:** [missiondeck.ai](https://missiondeck.ai)

## More by Asif2BD

```bash
clawhub install jarvis-mission-control   # Multi-agent task coordination
clawhub install openclaw-token-optimizer # Reduce token costs 50-80%
clawhub search Asif2BD                   # All skills
```

---

[MissionDeck.ai](https://missiondeck.ai) · [AIScan.site](https://aiscan.site) · [ClawHub](https://clawhub.ai/asif2bd/skills/aiscan-ai-readiness-scanner)

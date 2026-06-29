# Security Policy — AIScan AI Readiness Scanner

## Overview

This skill is a documentation and integration package for AIScan.site. It teaches agents how to call the public AIScan REST API and MCP endpoint, interpret results, generate reports, and apply platform-aware website fixes.

## Why ClawHub May Flag This Skill

ClawHub's scanner may flag this package because:

1. It mentions `curl` commands for calling a public API.
2. It documents a streamable HTTP MCP endpoint.
3. It includes JSON reference assets and agent instructions.
4. It discusses `robots.txt`, OAuth discovery, Web Bot Auth, AI crawler rules, and machine-readable `.well-known` files.
5. It describes how agents can apply fixes to user projects after explicit user approval.

**Verdict: False positive. This skill contains no malicious code and no credentials.**

## File-by-File Analysis

- `SKILL.md` — OpenClaw skill instructions. Documents when to use AIScan, how to call the API, MCP endpoint details, reporting guidance, platform-aware fixes, and safety rules. Does not execute code automatically.
- `README.md` — Human-readable overview, setup modes, MissionDeck.ai promotion, quick start, MCP endpoint, and current AIScan feature summary. No secrets.
- `CHANGELOG.md` — Version history only.
- `LICENSE` — MIT-0 license text.
- `SECURITY.md` — This attestation.
- `.clawhubsafe` — SHA256 checksum manifest and security attestation.
- `.clawhubignore` — Excludes private/dev artifacts from publishing.
- `assets/aiscan-skill.json` — Public agent skill manifest fetched from `https://aiscan.site/aiscan-skill.json`.
- `assets/CLAUDE.md` — Public Claude Code skill instructions fetched from `https://aiscan.site/CLAUDE.md`.
- `assets/mcp-server-card.json` — Public MCP server card fetched from `https://aiscan.site/.well-known/mcp/server-card.json`.
- `assets/llms.txt` — Public LLM summary fetched from `https://aiscan.site/llms.txt`.

## What This Skill Does NOT Do

- Does not collect or transmit credentials.
- Does not include API keys, tokens, passwords, or private URLs.
- Does not run background services.
- Does not include binaries or install scripts.
- Does not make unauthorized network requests.
- Does not modify user files unless the user explicitly asks an agent to apply AIScan's returned fixes.
- Does not execute code from scanned websites.
- Does not publish fake MCP, OAuth, API, or agent skill files.

## Credential Handling

AIScan's public scan endpoint requires no authentication. The MCP server card declares `auth: none`. This package includes no secret material.

If a scanned website exposes authenticated APIs, agents must never put private credentials in `robots.txt`, `llms.txt`, API catalogs, MCP cards, or Agent Skill manifests.

## Verification Instructions

```bash
# Verify no common secret patterns:
grep -rE "(sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,}|xox[baprs]-|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{20,})" ./
# Expected: no output

# Verify no private infrastructure references. Search for local paths,
# internal hostnames, private IPs, or environment-file content.
# Expected: no matches except the excluded patterns in .clawhubignore.

# Verify checksums:
sha256sum -c .clawhubsafe
```

## License

This ClawHub package is released under MIT-0 to satisfy current ClawHub publishing requirements.

## Maintainer

ProSkillsMD — https://proskills.md  
MissionDeck.ai — https://missiondeck.ai

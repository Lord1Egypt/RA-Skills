---
name: browsecraft
description: Memory-oriented browser automation skill for repeatable web workflows (login, extraction, bulk actions, form filling, screenshots, checks) across RoxyBrowser, Camoufox, and Chrome.
allowed-tools: Bash(browsecraft:*)
metadata: {"openclaw":{"emoji":"🧭","requires":{"bins":["browsecraft"]},"install":[{"id":"npm","kind":"node","package":"browsecraft-cli","bins":["browsecraft"],"label":"Install BrowseCraft CLI (npm)"}]}}
---

# BrowseCraft Skill

## Installation Prerequisites

1. Install CLI: `npm install -g browsecraft-cli`
2. Verify install: `browsecraft --help`
3. Optional (RoxyBrowser only): configure your Roxy API endpoint and token in local env/config.

If the CLI is missing, stop and ask the user to install it first. Do not assume local package scripts are available.

## Recommended Flow

1. Check status: `browsecraft status`
2. Start browser if needed: `browsecraft start`
3. Open target page: `browsecraft open <url>`
4. Capture snapshot: `browsecraft snapshot`
5. Prefer `click-ref` / `fill-ref` for stable interactions
6. Re-snapshot after page transitions
7. Capture result evidence: `browsecraft screenshot`

## Backend Strategy

- RoxyBrowser: `browsecraft start --type roxy --roxy-window-id ...`
- Camoufox: `browsecraft start --type camoufox` (optional `--camoufox-path`)
- Existing endpoint: `browsecraft connect <endpoint> --type <chrome|camoufox|roxy>`

## Credential & Scope Policy

- Roxy credentials are optional and only needed when the user explicitly chooses RoxyBrowser.
- Prefer environment variables over CLI token flags. Avoid printing or echoing secrets.
- Never send credentials or page data to third-party endpoints unless the user explicitly requests it.
- If a step needs network access outside the target website, ask for confirmation first.

## Stability Rules

- If element lookup fails: refresh with `snapshot`, then retry.
- If page is unstable: use `wait-for` before interaction.
- Always return structured output: objective / steps / result / failure reason / next action.

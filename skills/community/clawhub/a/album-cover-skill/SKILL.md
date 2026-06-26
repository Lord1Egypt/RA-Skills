---
name: album-cover-skill
description: Generate ai album cover generator images with AI via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# AI Album Cover Generator

Generate stunning ai album cover generator images from a text description. Get back a direct image URL instantly.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create ai album cover generator images.

## Quick start
```bash
node albumcover.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `square`)
- `--style` — `anime`, `cinematic`, `realistic` (default: `cinematic`)

## Install
```bash
npx skills add omactiengartelle/album-cover-skill
```

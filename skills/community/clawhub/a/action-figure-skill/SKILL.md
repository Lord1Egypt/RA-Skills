---
name: action-figure-skill
description: Generate ai action figure generator toy packaging images with AI via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# AI Action Figure Generator

Generate stunning ai action figure generator toy packaging images from a text description. Get back a direct image URL instantly.

## Token

Requires a Neta API token. Free trial available at <https://www.neta.art/open/>.

```bash
export NETA_TOKEN=your_token_here
node <script> "your prompt" --token "$NETA_TOKEN"
```

## When to use
Use when someone asks to generate or create ai action figure generator toy packaging images.

## Quick start
```bash
node actionfigure.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--style` — `anime`, `cinematic`, `realistic` (default: `cinematic`)

## Install
```bash
npx skills add TomCarranzaem/action-figure-skill
```

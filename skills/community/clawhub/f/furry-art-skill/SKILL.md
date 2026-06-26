---
name: furry-art-skill
description: Generate furry art generator ai images with AI via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Furry Art Generator

Generate stunning furry art generator ai images from a text description. Get back a direct image URL instantly.

## Token

Requires a Neta API token. Free trial available at <https://www.neta.art/open/>.

```bash
export NETA_TOKEN=your_token_here
node <script> "your prompt" --token "$NETA_TOKEN"
```

## When to use
Use when someone asks to generate or create furry art generator images.

## Quick start
```bash
node furryart.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `square`)
- `--style` — `anime`, `cinematic`, `realistic` (default: `anime`)

## Install
```bash
npx skills add omactiengartelle/furry-art-skill
```

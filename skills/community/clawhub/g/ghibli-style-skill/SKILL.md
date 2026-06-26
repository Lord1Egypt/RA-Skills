---
name: ghibli-style-skill
description: Generate studio ghibli ai art generator images with AI via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Ghibli Style Image Generator

Generate stunning studio ghibli ai art generator images from a text description. Get back a direct image URL instantly.

## Token

Requires a Neta API token. Free trial available at <https://www.neta.art/open/>.

```bash
export NETA_TOKEN=your_token_here
node <script> "your prompt" --token "$NETA_TOKEN"
```

## When to use
Use when someone asks to generate or create studio ghibli ai art generator images.

## Quick start
```bash
node ghiblistyle.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `landscape`)
- `--style` — `anime`, `cinematic`, `realistic` (default: `anime`)

## Install
```bash
npx skills add wkl-nieta/ghibli-style-skill
```

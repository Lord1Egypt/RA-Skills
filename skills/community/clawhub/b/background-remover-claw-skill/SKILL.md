---
name: background-remover-claw-skill
description: Generate ai background remover images with AI via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Background Remover

Generate stunning ai background remover images from a text description. Get back a direct image URL instantly.

## Token

Requires a Neta API token. Free trial available at <https://www.neta.art/open/>.

```bash
export NETA_TOKEN=your_token_here
node <script> "your prompt" --token "$NETA_TOKEN"
```

## When to use
Use when someone asks to generate or create ai background remover images.

## Quick start
```bash
node backgroundremoverclaw.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `square`)

## Install
```bash
npx skills add BarbaraLedbettergq/background-remover-claw-skill
```

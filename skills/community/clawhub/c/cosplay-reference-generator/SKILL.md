---
name: cosplay-reference-generator
description: Generate cosplay reference sheets and costume design illustrations from any character or outfit description. Perfect for cosplayers planning builds, commissioning costumes, anime convention prep, costume photoshoot planning, Etsy seller listings, and cosplay tutorials. Creates full-body character references with detailed outfit visualization, multiple angles, and accessory details via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Cosplay Reference Generator

Generate cosplay reference sheets and costume design illustrations from any character or outfit description. Perfect for cosplayers planning builds, commissioning costumes, anime convention prep, costume photoshoot planning, Etsy seller listings, and cosplay tutorials. Creates full-body character references with detailed outfit visualization, multiple angles, and accessory details.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create cosplay reference sheet generator images.

## Quick start
```bash
node cosplayreferencegenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/cosplay-reference-generator
```

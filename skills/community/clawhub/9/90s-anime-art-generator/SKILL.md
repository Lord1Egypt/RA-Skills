---
name: 90s-anime-art-generator
description: Generate 90s anime art and retro OVA-style illustrations with that nostalgic 1990s Japanese animation aesthetic — flat cel-shaded colors, hand-drawn line art, analog film grain, and vintage shoujo/seinen vibes. Perfect for retro anime portraits, nostalgic profile pictures, vaporwave anime aesthetics, classic OVA fan art, 90s manga-inspired illustrations, and retro Japanese animation style art via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# 90s Anime Art Generator

Generate 90s anime art and retro OVA-style illustrations with that nostalgic 1990s Japanese animation aesthetic — flat cel-shaded colors, hand-drawn line art, analog film grain, and vintage shoujo/seinen vibes. Perfect for retro anime portraits, nostalgic profile pictures, vaporwave anime aesthetics, classic OVA fan art, 90s manga-inspired illustrations, and retro Japanese animation style art.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create 90s anime art generator images.

## Quick start
```bash
node 90sanimeartgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add omactiengartelle/90s-anime-art-generator
```

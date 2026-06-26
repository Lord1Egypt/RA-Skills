---
name: barbie-style-generator
description: any description into a stunning Barbie-style AI portrait with hyper-feminine glamour doll aesthetics. Generate pastel-saturated fashion doll images, pink editorial portraits, and Barbie movie-inspired looks — perfect for Instagram Reels, TikTok content, identity play, and branded visuals via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Barbie Style Generator

any description into a stunning Barbie-style AI portrait with hyper-feminine glamour doll aesthetics. Generate pastel-saturated fashion doll images, pink editorial portraits, and Barbie movie-inspired looks — perfect for Instagram Reels, TikTok content, identity play, and branded visuals.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create barbie style ai photo generator images.

## Quick start
```bash
node barbiestylegenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add omactiengartelle/barbie-style-generator
```

---
name: anime-character-generator
description: Generate stunning full-body anime characters with custom outfits, hairstyles, and poses. Perfect for OC creation, fan art, visual novels, profile avatars, and anime-style portraits. Supports kawaii, shonen, shojo, and isekai aesthetics via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Anime Character Generator

Generate stunning full-body anime characters with custom outfits, hairstyles, and poses. Perfect for OC creation, fan art, visual novels, profile avatars, and anime-style portraits. Supports kawaii, shonen, shojo, and isekai aesthetics.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create anime character generator images.

## Quick start
```bash
node animecharactergenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add omactiengartelle/anime-character-generator
```

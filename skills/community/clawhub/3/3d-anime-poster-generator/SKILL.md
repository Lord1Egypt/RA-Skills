---
name: 3d-anime-poster-generator
description: Create stunning 3D anime posters with volumetric lighting, cinematic depth, and dynamic compositions. Perfect for wallpapers, merch designs, print-on-demand art, anime fan posters, cyberpunk-style artwork, and decorative prints. AI-powered 3D anime art poster maker and designer via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# 3D Anime Poster Generator

Create stunning 3D anime posters with volumetric lighting, cinematic depth, and dynamic compositions. Perfect for wallpapers, merch designs, print-on-demand art, anime fan posters, cyberpunk-style artwork, and decorative prints. AI-powered 3D anime art poster maker and designer.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create 3d anime poster generator images.

## Quick start
```bash
node 3danimepostergenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add omactiengartelle/3d-anime-poster-generator
```

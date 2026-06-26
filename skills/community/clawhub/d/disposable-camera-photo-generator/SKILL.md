---
name: disposable-camera-photo-generator
description: Generate authentic disposable camera photos with harsh flash, film grain, light leaks, date stamps, and that nostalgic Y2K snapshot aesthetic — perfect for Instagram dumps, TikTok carousels, vintage party photos, lo-fi memories, candid 2000s vibes, single-use camera throwaway shots, point-and-shoot retro looks, and grungy lomography-style imperfect photography via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Disposable Camera Photo Generator

Generate authentic disposable camera photos with harsh flash, film grain, light leaks, date stamps, and that nostalgic Y2K snapshot aesthetic — perfect for Instagram dumps, TikTok carousels, vintage party photos, lo-fi memories, candid 2000s vibes, single-use camera throwaway shots, point-and-shoot retro looks, and grungy lomography-style imperfect photography.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create disposable camera photo generator images.

## Quick start
```bash
node disposablecameraphotogenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `square`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/disposable-camera-photo-generator
```

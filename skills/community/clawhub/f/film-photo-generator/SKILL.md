---
name: film-photo-generator
description: Generate authentic analog-style film photographs with 35mm grain, light leaks, and faded retro color palettes. Perfect for nostalgic portraits, vintage 70s/80s aesthetic photos, Instagram film looks, Kodak Portra style imagery, lomography effects, Fujifilm simulation, and imperfect human photography that beats the polished AI look — ideal for indie creators, film photography enthusiasts, and retro mood boards via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Film Photo Generator

Generate authentic analog-style film photographs with 35mm grain, light leaks, and faded retro color palettes. Perfect for nostalgic portraits, vintage 70s/80s aesthetic photos, Instagram film looks, Kodak Portra style imagery, lomography effects, Fujifilm simulation, and imperfect human photography that beats the polished AI look — ideal for indie creators, film photography enthusiasts, and retro mood boards.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create ai film photo generator images.

## Quick start
```bash
node filmphotogenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add omactiengartelle/film-photo-generator
```

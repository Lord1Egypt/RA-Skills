---
name: food-photography-generator
description: AI food photography generator for restaurants, recipe bloggers, cookbook authors, food brands, and Instagram creators. Generate appetizing hero shots, menu photos, recipe card images, cookbook illustrations, food blog headers, restaurant marketing visuals, gourmet plating photography, dessert close-ups, beverage shots, cafe branding imagery, and culinary editorial content with professional cinematic lighting and styling via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Food Photography Generator

AI food photography generator for restaurants, recipe bloggers, cookbook authors, food brands, and Instagram creators. Generate appetizing hero shots, menu photos, recipe card images, cookbook illustrations, food blog headers, restaurant marketing visuals, gourmet plating photography, dessert close-ups, beverage shots, cafe branding imagery, and culinary editorial content with professional cinematic lighting and styling.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create ai food photography generator images.

## Quick start
```bash
node foodphotographygenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `square`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/food-photography-generator
```

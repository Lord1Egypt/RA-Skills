---
name: baroque-art-generator
description: any subject into dramatic baroque oil painting art with rich chiaroscuro lighting, opulent Caravaggio and Rembrandt style textures, and classical Renaissance composition. Perfect for creating baroque portraits, classical art prints, museum-style oil paintings, Renaissance-inspired wall art, old masters style portraits, and ornate historical artwork for Etsy sellers, art collectors, and classical aesthetic lovers via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Baroque Art Generator

any subject into dramatic baroque oil painting art with rich chiaroscuro lighting, opulent Caravaggio and Rembrandt style textures, and classical Renaissance composition. Perfect for creating baroque portraits, classical art prints, museum-style oil paintings, Renaissance-inspired wall art, old masters style portraits, and ornate historical artwork for Etsy sellers, art collectors, and classical aesthetic lovers.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create baroque art generator images.

## Quick start
```bash
node baroqueartgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/baroque-art-generator
```

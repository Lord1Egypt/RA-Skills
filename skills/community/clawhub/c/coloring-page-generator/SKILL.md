---
name: coloring-page-generator
description: AI coloring page generator — create printable black and white coloring pages, adult coloring book pages, kids coloring sheets, and coloring book illustrations from any description. Generate mandala coloring pages, animal coloring pages, fantasy coloring pages, and custom line art instantly via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Coloring Page Generator

AI coloring page generator — create printable black and white coloring pages, adult coloring book pages, kids coloring sheets, and coloring book illustrations from any description. Generate mandala coloring pages, animal coloring pages, fantasy coloring pages, and custom line art instantly.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create coloring page generator images.

## Quick start
```bash
node coloringpagegenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/coloring-page-generator
```

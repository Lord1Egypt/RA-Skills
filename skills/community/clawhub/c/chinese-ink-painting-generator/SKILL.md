---
name: chinese-ink-painting-generator
description: Generate stunning traditional Chinese ink paintings (shui-mo hua) and sumi-e brushwork art with AI. Create classical shan shui landscapes, bamboo, koi, dragons, plum blossoms, calligraphy art, oriental scrolls, Japanese ink wash, zen minimalist art, and East Asian brush painting illustrations for wallpapers, prints, tea house decor, meditation art, cultural projects, and traditional aesthetic designs via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Chinese Ink Painting Generator

Generate stunning traditional Chinese ink paintings (shui-mo hua) and sumi-e brushwork art with AI. Create classical shan shui landscapes, bamboo, koi, dragons, plum blossoms, calligraphy art, oriental scrolls, Japanese ink wash, zen minimalist art, and East Asian brush painting illustrations for wallpapers, prints, tea house decor, meditation art, cultural projects, and traditional aesthetic designs.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create chinese ink painting generator images.

## Quick start
```bash
node chineseinkpaintinggenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `landscape`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/chinese-ink-painting-generator
```

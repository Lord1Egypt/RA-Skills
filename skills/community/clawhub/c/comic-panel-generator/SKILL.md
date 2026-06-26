---
name: comic-panel-generator
description: Generate AI comic book panels, manga strips, and graphic novel art from text descriptions. Create anime-style comic illustrations, webcomic frames, storyboard panels, manga-style sequential art, and comic character scenes with dynamic compositions and bold ink outlines via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Comic Panel Generator

Generate AI comic book panels, manga strips, and graphic novel art from text descriptions. Create anime-style comic illustrations, webcomic frames, storyboard panels, manga-style sequential art, and comic character scenes with dynamic compositions and bold ink outlines.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create ai comic panel generator images.

## Quick start
```bash
node comicpanelgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/comic-panel-generator
```

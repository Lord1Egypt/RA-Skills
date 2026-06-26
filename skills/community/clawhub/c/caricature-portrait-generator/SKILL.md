---
name: caricature-portrait-generator
description: Generate hilarious AI caricature portraits with exaggerated features — turn any description into a funny caricature, cartoon portrait, or comic likeness. Perfect for gifts, social media, party invitations, and personalized art. Supports caricature generator, exaggerated portrait, cartoon face, comic portrait, and funny face art styles via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# AI Caricature Portrait Generator

Generate hilarious AI caricature portraits with exaggerated features — turn any description into a funny caricature, cartoon portrait, or comic likeness. Perfect for gifts, social media, party invitations, and personalized art. Supports caricature generator, exaggerated portrait, cartoon face, comic portrait, and funny face art styles.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create ai caricature portrait generator images.

## Quick start
```bash
node caricatureportraitgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add omactiengartelle/caricature-portrait-generator
```

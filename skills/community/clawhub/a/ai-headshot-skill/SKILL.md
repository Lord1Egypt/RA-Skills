---
name: ai-headshot-skill
description: Generate ai professional headshot generator images with AI via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# AI Professional Headshot Generator

Generate stunning ai professional headshot generator images from a text description. Get back a direct image URL instantly.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create ai professional headshot generator images.

## Quick start
```bash
node aiheadshot.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/ai-headshot-skill
```

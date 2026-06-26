---
name: dnd-character-skill
description: Generate dnd character art generator images from text descriptions via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# D&D Character Art Generator

Generate stunning dnd character art generator images from a text description. Get back a direct image URL instantly.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create dnd character art generator images.

## Quick start
```bash
node dndcharacter.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add omactiengartelle/dnd-character-skill
```

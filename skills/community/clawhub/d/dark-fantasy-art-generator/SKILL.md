---
name: dark-fantasy-art-generator
description: Generate dark fantasy artwork, grimdark illustrations, and gothic horror scenes. Perfect for D&D campaigns, metal album covers, Soulslike game concepts, dark fantasy novel covers, horror art, eldritch creatures, haunted castles, cursed knights, and atmospheric moody worldbuilding imagery via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Dark Fantasy Art Generator

Generate dark fantasy artwork, grimdark illustrations, and gothic horror scenes. Perfect for D&D campaigns, metal album covers, Soulslike game concepts, dark fantasy novel covers, horror art, eldritch creatures, haunted castles, cursed knights, and atmospheric moody worldbuilding imagery.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create dark fantasy art generator images.

## Quick start
```bash
node darkfantasyartgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add omactiengartelle/dark-fantasy-art-generator
```

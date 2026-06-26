---
name: fantasy-map-generator
description: AI fantasy map generator for worldbuilders, tabletop RPG campaigns, and game designers. Create custom fantasy world maps, dungeon maps, kingdom maps, and lore art — perfect for D&D, Pathfinder, and indie game development via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Fantasy Map Generator

AI fantasy map generator for worldbuilders, tabletop RPG campaigns, and game designers. Create custom fantasy world maps, dungeon maps, kingdom maps, and lore art — perfect for D&D, Pathfinder, and indie game development.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create fantasy map generator images.

## Quick start
```bash
node fantasymapgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `landscape`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/fantasy-map-generator
```

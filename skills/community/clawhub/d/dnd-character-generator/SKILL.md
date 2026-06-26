---
name: dnd-character-generator
description: Generate cinematic D&D character portraits and tabletop RPG hero art from a text description. Ideal for Dungeons & Dragons players, dungeon masters, TTRPG campaigns, and virtual tabletop tokens — create wizards, warriors, paladins, rogues, and any fantasy character class in stunning detail via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# D&D Character Art Generator

Generate cinematic D&D character portraits and tabletop RPG hero art from a text description. Ideal for Dungeons & Dragons players, dungeon masters, TTRPG campaigns, and virtual tabletop tokens — create wizards, warriors, paladins, rogues, and any fantasy character class in stunning detail.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create dnd character art generator images.

## Quick start
```bash
node dndcharactergenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add omactiengartelle/dnd-character-generator
```

# D&D Character Art Generator

Generate cinematic D&D character portraits and tabletop RPG hero art from text descriptions. Describe your wizard, warrior, paladin, rogue, or any fantasy character class and receive a stunning, detailed portrait — perfect for Dungeons & Dragons players, dungeon masters, TTRPG campaigns, and virtual tabletop tokens.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add omactiengartelle/dnd-character-generator
```

```bash
clawhub install dnd-character-generator
```

## Token Setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Usage

```bash
# Default portrait — uses built-in D&D prompt
node dndcharactergenerator.js --token YOUR_TOKEN

# Describe your character
node dndcharactergenerator.js "elven ranger with a longbow, forest background, green cloak, moonlight" --token YOUR_TOKEN

# Dwarf paladin in plate armor
node dndcharactergenerator.js "dwarf paladin in gleaming plate armor, holy symbol glowing, divine light, epic fantasy" --token YOUR_TOKEN

# Tiefling warlock
node dndcharactergenerator.js "tiefling warlock with horns, purple arcane energy, dark robes, dramatic shadows" --token YOUR_TOKEN

# Landscape composition
node dndcharactergenerator.js "barbarian warrior on a cliff overlooking a battlefield" --size landscape --token YOUR_TOKEN

# Square token for virtual tabletop
node dndcharactergenerator.js "halfling rogue in leather armor, dagger, confident smirk" --size square --token YOUR_TOKEN
```

### Output

Returns a direct image URL.

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--token` | string | — | **Required.** Your Neta API token |
| `--size` | `portrait`, `landscape`, `square`, `tall` | `portrait` | Image dimensions |
| `--ref` | UUID string | — | Reference image UUID for style inheritance |

### Size Dimensions

| Size | Dimensions | Best for |
|------|-----------|----------|
| `portrait` | 832 × 1216 | Character portraits, VTT tokens |
| `landscape` | 1216 × 832 | Scene illustrations, wide banners |
| `square` | 1024 × 1024 | Profile pictures, token art |
| `tall` | 704 × 1408 | Full-body character art |

## Prompt Tips

- Name the character race and class: "half-orc barbarian", "high elf wizard"
- Describe armor, weapons, and accessories in detail
- Mention lighting: "dramatic torchlight", "moonlit forest", "divine radiance"
- Add mood or setting: "battle-worn", "ancient dungeon background", "heroic pose"
- Include art style cues: "oil painting style", "highly detailed fantasy art", "cinematic"

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).

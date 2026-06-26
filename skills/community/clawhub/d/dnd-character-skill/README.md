# D&D Character Art Generator

Generate stunning D&D character art from text descriptions. Describe your character — race, class, armor, weapons, pose — and get back a high-quality fantasy portrait powered by AI image generation.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add omactiengartelle/dnd-character-skill
```

or

```bash
clawhub install dnd-character-skill
```

## Usage

```bash
node dndcharacter.js "dungeons and dragons character portrait, fantasy RPG art, detailed armor and weapons" --token YOUR_TOKEN
```

Returns a direct image URL.

### With options

```bash
# Landscape format
node dndcharacter.js "elven ranger in a moonlit forest, longbow drawn" --token "$NETA_TOKEN" --size landscape

# Square format with a reference image
node dndcharacter.js "dwarf paladin in gleaming plate armor, warhammer raised" --token "$NETA_TOKEN" --size square --ref abc123-uuid
```

Returns a direct image URL.

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--token` | Neta API token (required) | — |
| `--size` | Image dimensions: `portrait`, `landscape`, `square`, `tall` | `portrait` |
| `--ref` | Reference image UUID for style inheritance | — |

## Token Setup

Get a free trial Neta API token at [neta.art/open](https://www.neta.art/open/).

Pass your token using the `--token` flag:

```bash
node dndcharacter.js "half-orc barbarian with a greataxe" --token YOUR_TOKEN
```

You can also use shell variable expansion for convenience:

```bash
export NETA_TOKEN="your-token-here"
node dndcharacter.js "tiefling warlock with eldritch energy" --token "$NETA_TOKEN"
```

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).

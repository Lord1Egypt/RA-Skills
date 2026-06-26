# Fantasy Map Generator

Generate stunning fantasy maps from text descriptions using AI. Describe your world — its mountains, kingdoms, rivers, dungeons, and lore — and receive a richly illustrated cartographic image ready for your campaign, game, or creative project. Ideal for D&D, Pathfinder, tabletop RPGs, worldbuilding, and indie game development.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

---

## Install

**Via npx skills:**
```bash
npx skills add blammectrappora/fantasy-map-generator
```

**Via clawhub:**
```bash
clawhub install fantasy-map-generator
```

---

## Token Setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Usage

```bash
node fantasymapgenerator.js "PROMPT" --token YOUR_TOKEN [--size SIZE] [--ref UUID]
```

If no prompt is provided, a default fantasy world map prompt is used.

### Examples

```bash
# Classic parchment world map
node fantasymapgenerator.js "hand-drawn parchment world map with mountains, forests, and ancient kingdoms" --token "$NETA_TOKEN"

# Dark dungeon map
node fantasymapgenerator.js "top-down dungeon map, stone corridors, torch-lit chambers, treasure room, ink on aged paper" --token "$NETA_TOKEN"

# Landscape orientation (default)
node fantasymapgenerator.js "vast continent map with coastal cities and inland empires" --token "$NETA_TOKEN" --size landscape

# Portrait orientation
node fantasymapgenerator.js "tall kingdom map showing northern tundra to southern desert" --token "$NETA_TOKEN" --size portrait

# With style reference
node fantasymapgenerator.js "island archipelago with pirate coves" --token "$NETA_TOKEN" --ref xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### Output

Returns a direct image URL printed to stdout.

---

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--token` | Neta API token (required) | — |
| `--size` | Output size: `landscape`, `portrait`, `square`, `tall` | `landscape` |
| `--ref` | Picture UUID to inherit style from | — |

### Size Dimensions

| Size | Dimensions |
|------|------------|
| `square` | 1024 × 1024 |
| `portrait` | 832 × 1216 |
| `landscape` | 1216 × 832 |
| `tall` | 704 × 1408 |

---

## Default Prompt

When called without a prompt, the skill uses:

> fantasy world map, hand-drawn cartographic illustration, parchment texture, detailed terrain with mountains forests rivers and oceans, labeled cities and kingdoms, decorative compass rose, ornate borders, medieval fantasy aesthetic, bird's eye view, rich warm tones


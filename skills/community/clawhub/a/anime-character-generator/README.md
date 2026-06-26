# Anime Character Generator

Generate stunning full-body anime characters from text descriptions. Describe the character's outfit, hairstyle, pose, color palette, and personality — and get back a high-quality anime-style illustration. Perfect for OC creation, fan art, visual novels, profile avatars, and anime-style portraits. Supports kawaii, shonen, shojo, and isekai aesthetics.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

---

## Install

**Via npx skills:**
```bash
npx skills add omactiengartelle/anime-character-generator
```

**Via ClawHub:**
```bash
clawhub install anime-character-generator
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
node animecharactergenerator.js "<description>" --token YOUR_TOKEN [--size <size>] [--ref <picture_uuid>]
```

### Examples

```bash
# Default portrait — uses built-in default prompt
node animecharactergenerator.js --token "$NETA_TOKEN"

# Custom character description
node animecharactergenerator.js "silver-haired mage girl, flowing robes, glowing staff, fantasy forest background" --token "$NETA_TOKEN"

# Landscape orientation
node animecharactergenerator.js "battle-ready shonen hero, spiky hair, torn jacket, dramatic lighting" --token "$NETA_TOKEN" --size landscape

# Tall format for full-body portrait
node animecharactergenerator.js "elegant kuudere in a school uniform, long dark hair, cherry blossom background" --token "$NETA_TOKEN" --size tall

# Style reference from a previous generation
node animecharactergenerator.js "same character in winter outfit" --token "$NETA_TOKEN" --ref <picture_uuid>
```

### Output

Returns a direct image URL.

---

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--token` | string | *(required)* | Your Neta API token |
| `--size` | `portrait`, `landscape`, `square`, `tall` | `portrait` | Output image dimensions |
| `--ref` | UUID string | *(none)* | Reference image UUID for style inheritance |

### Size dimensions

| Size | Width | Height |
|------|-------|--------|
| `portrait` | 832 | 1216 |
| `landscape` | 1216 | 832 |
| `square` | 1024 | 1024 |
| `tall` | 704 | 1408 |

---

## Default Prompt

If no description is provided, the skill uses:

> full body anime character, detailed outfit, expressive eyes, dynamic pose, vibrant colors, studio quality illustration


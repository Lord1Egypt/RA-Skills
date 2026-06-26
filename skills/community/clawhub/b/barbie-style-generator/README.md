# Barbie Style Generator

Generate stunning Barbie-style AI portraits from text descriptions — hyper-feminine glamour doll aesthetics, pastel-saturated pink editorial looks, and Barbie movie-inspired visuals. Describe a scene, a mood, or a character, and get back a high-quality fashion doll portrait perfect for Instagram Reels, TikTok content, identity play, and branded visuals.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

---

## Install

**Via npx skills:**
```bash
npx skills add omactiengartelle/barbie-style-generator
```

**Via ClawHub:**
```bash
clawhub install barbie-style-generator
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
node barbiestylegenerator.js "<description>" --token YOUR_TOKEN [--size <size>] [--ref <picture_uuid>]
```

### Examples

```bash
# Default Barbie glamour portrait
node barbiestylegenerator.js "hyper-feminine Barbie doll aesthetic portrait, pastel pink fashion editorial" --token "$NETA_TOKEN"

# Dreamhouse Barbie in a pink convertible
node barbiestylegenerator.js "Barbie driving a pink convertible, Malibu beach, sunny day, fashion doll style" --token "$NETA_TOKEN"

# Landscape format
node barbiestylegenerator.js "Barbie at a runway fashion show, glitter and sequins" --token "$NETA_TOKEN" --size landscape

# Tall format for Stories/Reels
node barbiestylegenerator.js "space Barbie, cosmic glam, star-studded outfit, pink galaxy backdrop" --token "$NETA_TOKEN" --size tall

# With style reference UUID
node barbiestylegenerator.js "Barbie at the Oscars, red carpet glamour" --token "$NETA_TOKEN" --ref abc123-uuid
```

**Output:** Returns a direct image URL.

---

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--token` | string | *(required)* | Your Neta API token |
| `--size` | `portrait`, `landscape`, `square`, `tall` | `portrait` | Output image dimensions |
| `--ref` | UUID string | *(none)* | Reference image UUID for style inheritance |

### Size dimensions

| Size | Width | Height | Best for |
|------|-------|--------|----------|
| `portrait` | 832 | 1216 | Standard portrait, Instagram posts |
| `landscape` | 1216 | 832 | Wide shots, banners |
| `square` | 1024 | 1024 | Instagram grid, profile images |
| `tall` | 704 | 1408 | Stories, TikTok, Reels |

---

## How it works

1. Sends your text description to the Neta image generation API
2. Polls for task completion (up to 3 minutes)
3. Prints the final image URL to stdout when ready

Progress messages are written to stderr so the URL on stdout can be cleanly piped or captured:

```bash
IMAGE_URL=$(node barbiestylegenerator.js "pink Barbie dreamhouse" --token "$NETA_TOKEN")
echo "Generated: $IMAGE_URL"
```


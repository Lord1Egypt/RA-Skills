# Chibi Character Generator

> Powered by the **Neta AI image generation API** (`api.talesofai.com`) — the same service as [neta.art](https://www.neta.art/open/).

Generate adorable chibi character images from a text description using AI. Powered by the Neta talesofai API, this skill returns a direct image URL instantly — ready to use in any workflow.

---

## Install

**Via npx skills:**
```bash
npx skills add TomCarranzaem/chibi-gen-skill
```

**Via ClawHub:**
```bash
clawhub install chibi-gen-skill
```

---

## Usage

```bash
# Generate with default chibi prompt
node chibigen.js

# Generate with a custom description
node chibigen.js "a chibi wizard with purple robes and a glowing staff"

# Specify size
node chibigen.js "chibi knight in shining armor" --size portrait

# Use a reference image (picture_uuid from a previous generation)
node chibigen.js "same character, different pose" --ref <picture_uuid>

# Pass token directly
node chibigen.js "chibi cat girl" --token YOUR_NETA_TOKEN
```

The script prints a single image URL to stdout on success.

---

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--size` | `square`, `portrait`, `landscape`, `tall` | `square` | Output image dimensions |
| `--token` | string | — | Neta API token (required) |
| `--ref` | picture_uuid | — | Reference a previous image for style inheritance |

### Size dimensions

| Name | Width | Height |
|------|-------|--------|
| `square` | 1024 | 1024 |
| `portrait` | 832 | 1216 |
| `landscape` | 1216 | 832 |
| `tall` | 704 | 1408 |

---

## Token Setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Default Prompt

When no prompt is provided, the skill uses:

> full body chibi character, big head small body proportions, adorable kawaii style, expressive large eyes, pastel color palette, clean line art, white background, high quality anime illustration

## Example Output

![Generated example](https://oss.talesofai.cn/picture/06b8644b-d5cf-406e-b6a5-f289bf015b1c.webp)

---

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).

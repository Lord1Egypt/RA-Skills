# Blog Image Generator

> Powered by the **Neta AI image generation API** (`api.talesofai.com`) — the same service as [neta.art](https://www.neta.art/open/).

Generate stunning **ai blog image generator** images from a text description using AI — powered by the Neta talesofai API. Get back a direct image URL instantly, ready to embed anywhere.

---

## Install

**Via npx skills:**
```bash
npx skills add BarbaraLedbettergq/blog-image-claw-skill
```

**Via ClawHub:**
```bash
clawhub install blog-image-claw-skill
```

---

## Usage

```bash
# Basic usage — describe what you want
node blogimageclaw.js "minimalist flat-lay of a laptop and coffee on a wooden desk"

# Specify size
node blogimageclaw.js "futuristic city skyline at dusk" --size landscape

# Use a reference image (style transfer)
node blogimageclaw.js "vibrant abstract background" --ref <picture_uuid>

# Pass token inline
node blogimageclaw.js "cozy home office setup" --token YOUR_NETA_TOKEN
```

The script prints the image URL to stdout on success:
```
https://cdn.talesofai.cn/.../<image>.jpg
```

---

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--size` | `square`, `portrait`, `landscape`, `tall` | `landscape` | Output image dimensions |
| `--style` | `anime`, `cinematic`, `realistic` | `cinematic` | Visual style (passed via prompt) |
| `--ref` | `<picture_uuid>` | — | Reference image UUID for style/param inheritance |
| `--token` | `<token>` | — | Neta API token (required) |

### Size reference

| Name | Dimensions |
|------|-----------|
| `square` | 1024 × 1024 |
| `portrait` | 832 × 1216 |
| `landscape` | 1216 × 832 |
| `tall` | 704 × 1408 |

---

## Token setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Default prompt

When no prompt is supplied, the skill uses:
```
professional blog hero image, high quality photography, relevant to topic
```

---

## Examples

```bash
# Hero image for a travel blog post
node blogimageclaw.js "aerial view of turquoise ocean with white sandy beach, golden hour"

# Tech article cover
node blogimageclaw.js "abstract data visualization, glowing blue network nodes on dark background" --size landscape

# Portrait-style author photo background
node blogimageclaw.js "soft bokeh office background, warm natural lighting" --size portrait
```

## Example Output

![Generated example](https://oss.talesofai.cn/picture/2c1de0c7-b4e8-4083-ba2f-62b73f893d2d.webp)

---

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).

---
name: crazyrouter-image-gen
description: AI image generation via Crazyrouter API. Supports DALL-E 3, GPT Image, Gemini, Imagen 4. Text-to-image with aspect ratio, size, and model selection. Use when user asks to generate, create, or draw an image. Requires environment variable CRAZYROUTER_API_KEY (get at https://crazyrouter.com).
---

# Image Generation via Crazyrouter

Generate images using multiple AI models through [Crazyrouter](https://crazyrouter.com) — one API key, all providers.

## Supported Models

| Model | ID | Best For |
|-------|-----|----------|
| DALL-E 3 | `dall-e-3` | General, creative |
| GPT Image 1 | `gpt-image-1` | GPT native, high quality |
| GPT-4o Image | `gpt-4o-image` | Fast, versatile |
| Gemini 2.5 Flash Image | `gemini-2.5-flash-image` | Fast, free tier |
| Gemini 3.1 Flash Image | `gemini-3.1-flash-image-preview` | Latest Gemini |
| Gemini 3 Pro Image | `gemini-3-pro-image-preview` | Pro quality |
| Imagen 3.0 | `imagen-3.0-generate-002` | Google Imagen |
| Imagen 4.0 | `imagen-4.0-generate-001` | Google's latest |
| Imagen 4.0 Ultra | `imagen-4.0-ultra-generate-001` | Highest quality |
| Sora Image | `sora_image` | OpenAI Sora static |

## Script Directory

**Agent Execution**:
1. `SKILL_DIR` = this SKILL.md file's directory
2. Script path = `${SKILL_DIR}/scripts/main.mjs`

## Step 0: Check API Key ⛔ BLOCKING

```bash
[ -n "${CRAZYROUTER_API_KEY}" ] && echo "key_present" || echo "not_set"
```

| Result | Action |
|--------|--------|
| `key_present` | Continue to Step 1 |
| `not_set` | Ask user to set `CRAZYROUTER_API_KEY`. Get key at https://crazyrouter.com |

## Step 1: Generate Image

```bash
node ${SKILL_DIR}/scripts/main.mjs --prompt "your prompt" --image output.png
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--prompt <text>` | Image description (required) | — |
| `--image <path>` | Output file path (required) | — |
| `--model <id>` | Model to use | `dall-e-3` |
| `--size <WxH>` | Image size | `1024x1024` |
| `--n <count>` | Number of images (1-4) | `1` |
| `--quality <level>` | Quality: standard/hd | `standard` |

### Examples

```bash
# Basic generation
node ${SKILL_DIR}/scripts/main.mjs --prompt "A sunset over mountains" --image sunset.png

# With GPT Image 1
node ${SKILL_DIR}/scripts/main.mjs --prompt "Cyberpunk city" --image city.png --model gpt-image-1

# With Imagen 4.0 Ultra (highest quality)
node ${SKILL_DIR}/scripts/main.mjs --prompt "Professional headshot" --image photo.png --model imagen-4.0-ultra-generate-001

# With Gemini 3 Pro
node ${SKILL_DIR}/scripts/main.mjs --prompt "Landscape" --image wide.png --model gemini-3-pro-image-preview

# Multiple images
node ${SKILL_DIR}/scripts/main.mjs --prompt "Logo concepts" --image logo.png --n 4
```

## Step 2: Verify Output

After generation, confirm the image was saved:

```bash
ls -la <output_path>
```

Show the image to the user or report the file path.

---
name: codia-image-generate
description: Generate images from text prompts with Codia Design CLI. Trigger when the user asks Codia to create images, icons, posters, campaign visuals, packaging concepts, backgrounds, or visual drafts.
api: image-generate
endpoint: POST /v2/open/image/generate_image
cli: codia-design image generate
credits_per_call: varies
sync: true
response_type: image_urls
---

# codia-image-generate

## Runtime And Auth

Use the local `codia-design` CLI for this feature. Before calling the API, verify that `codia-design` is available. If it is missing and global npm installs are allowed, install it with `npm install -g @codia-ai/codia-design-cli`. Then check `codia-design auth status`; if it is not connected, run `codia-design auth login --platform codex` or bind an API key with `codia-design auth set --api-key api_key_xxx`. Never print API keys or `~/.codia/design-skills/config.json`.

Generate images based on text descriptions. Supports multiple models, each with different styles and credits consumption.

## CLI Command

```bash
codia-design image generate \
  --prompt "TEXT" \
  [--size WxH] \
  [--n COUNT] \
  [--model MODEL] \
  [--quality low|medium|high] \
  [--background transparent|opaque] \
  [--reference_images '["URL1","URL2"]'] \
  [--download-dir DIR] \
  [--no-download] \
  [--out FILE]
```

## Parameters

| Flag | Type | Required | Default | Description |
|---|---|---|---|---|
| `--prompt` | string | yes | — | Image description text |
| `--size` | string | no | Model default | Request size, such as `1024x1024`, `1536x1024`. The server normalizes sizes according to model capabilities, so the final image may differ from the requested size |
| `--n` | number | no | `1` | Number of images to generate (credits × n) |
| `--model` | string | no | `seedream_5` | See model table below |
| `--quality` | string | no | — | Only `gpt_image` supports: `low` / `medium` / `high` |
| `--background` | string | no | — | Only `gpt_image` supports: `transparent` / `opaque` |
| `--reference_images` | JSON array | no | — | Style reference image URLs, JSON array format: `'["url1","url2"]'` |
| `--out` | path | no | stdout | Write JSON results to file |
| `--download-dir` | path | no | `.` | Directory for downloaded generated images |
| `--no-download` | boolean | no | `false` | Return JSON only; do not download images |

## Credit Matrix

Prices are charged from the unified Codia Open API balance. The CLI estimates from `open_api_v2`; use `codia-design limits` or `https://codia.ai/api-reference#description/introduction` for the live pricing table.

### Text-to-image and image-to-image

`image generate` charges per generated image and multiplies by `--n`. `image image-to-image` charges per request. Both use this model table.

| Model | Default | 1K | 2K | 4K |
|---|---:|---:|---:|---:|
| `nano_banana_2` | 18 | 18 | 27 | 40 |
| `nano_banana_pro` | 36 | 36 | 36 | 64 |
| `seedream_5` | 9 | 9 | 9 | 9 |
| `seedream_4_5` | 11 | 11 | 11 | 11 |
| `recraft_v4` | 11 | 11 | 67 | - |
| `flux_2_pro` | 8 | 8 | 20 | - |
| `flux_2_max` | 19 | 19 | 43 | - |
| `ideogram_v3` | 16 | 16 | - | - |

GPT Image uses quality-specific pricing:

| Quality | 1K | 2K | 4K |
|---|---:|---:|---:|
| `low` | 2 | 9 | 9 |
| `medium` / omitted / `auto` | 8 | 34 | 34 |
| `high` | 33 | 133 | 133 |

### Remix

| Model | Default | 1K | 2K | 4K |
|---|---:|---:|---:|---:|
| `nano_banana_2` | 18 | 18 | 27 | 40 |
| `nano_banana_pro` | 36 | 36 | 36 | 64 |
| `gpt_image` | 8 | 8 | 34 | 34 |
| `seedream_5` | 9 | 9 | 9 | 9 |
| `seedream_4_5` | 11 | 11 | 11 | 11 |
| `recraft_v4` | 11 | 11 | 67 | - |
| `flux_2_pro` | 8 | 8 | 20 | - |
| `flux_2_max` | 19 | 19 | 43 | - |
| `ideogram_v3` | 16 | 16 | - | - |

### Reframe

| Model | Default | 1K | 2K | 4K |
|---|---:|---:|---:|---:|
| `gpt_image` | 8 | 8 | 34 | 34 |
| `nano_banana_2` | 18 | 18 | 27 | 40 |
| `nano_banana_pro` | 36 | 36 | 36 | 64 |
| `seedream_5` | 9 | 9 | 9 | 9 |
| `seedream_4_5` | 11 | 11 | 11 | 11 |
| `flux_2_pro` | 8 | 8 | 20 | - |
| `flux_2_max` | 19 | 19 | 43 | - |
| `ideogram_v3` | 16 | 16 | - | - |

### Upscale

| Model | Default | 1K | 2K | 4K |
|---|---:|---:|---:|---:|
| default / `codia_image_v2` | 16 | - | - | - |
| `ideogram_v3` | 16 | 16 | 16 | - |
| `nano_banana_2` | 18 | 18 | 27 | 40 |
| `nano_banana_pro` | 36 | 36 | 36 | 64 |
| `gpt_image` | 56 | 56 | 112 | - |

## Model Guidance

| Model | Best for | Credits/image (`open_api_v2`) |
|---|---|---|
| `seedream_5` | Ultimate photorealism; size will be normalized to Seedream supported range | 9 |
| `seedream_4_5` | Portrait realism; size will be normalized to Seedream supported range | 11 |
| `nano_banana_2` | Fast daily generation | 18 / 27 / 40 for 1K / 2K / 4K |
| `nano_banana_pro` | 4K exquisite vision | 36 / 36 / 64 for 1K / 2K / 4K |
| `gpt_image` | The text in the image is clear; supports quality + background | 2-133 by quality and resolution |
| `recraft_v4` | Illustration/icon/vector style | 11 for 1K, 67 for 2K |
| `flux_2_pro` | High quality generic generation | 8 for 1K, 20 for 2K |
| `flux_2_max` | Highest-quality FLUX tier | 19 for 1K, 43 for 2K |
| `ideogram_v3` | Excellent layout and creative composition | 16 |

## CLI Defaults

When the user simply asks to "generate an image" or describes a style but does not specify a model/size, the CLI proactively provides easy-to-use defaults:

- Default model: `seedream_5`.
- Default size: `2560x1440`, the 2K supported size for Seedream 16:9.
- When the user passes in `--model` or `--size`, the user parameters shall prevail.
- Download `data.image_urls` to the current local directory by default, and append `data.local_file` / `data.local_files` to the response; use `--download-dir` to specify the directory, or use `--no-download` to turn it off.
- When the user requires precise output of pixels, it means that the image generation model may be normalized according to server-side rules; use post-processing resize/crop when a fixed final size is required.

## Size Normalization

`--size` is the requested size, which is not guaranteed to be equal to the final image size. The server will perform normalization according to model constraints:

- The default model and most 1024 series models use the 1024 base size.
- `seedream_5` / `seedream_4_5` requires the minimum area to be no less than `1920x1920` and the single side no more than `4096`. For example, if the requested area of `1920x1080` is insufficient, it will be normalized to `2560x1440` according to 16:9.
- `ideogram_v3` uses its own native size table.

Commonly used ratio references:

| Aspect | Default / 1024 models | Seedream minimum | Ideogram V3 |
|---|---:|---:|---:|
| `1:1` | `1024x1024` | `1920x1920` | `1024x1024` |
| `4:3` | `1024x768` | `2216x1662` | `1152x864` |
| `3:4` | `768x1024` | `1662x2216` | `864x1152` |
| `16:9` | `1024x576` | `2560x1440` | `1312x736` |
| `9:16` | `576x1024` | `1440x2560` | `736x1312` |
| `3:2` | `1024x682` | `2352x1568` | `1248x832` |
| `2:3` | `682x1024` | `1568x2352` | `832x1248` |
| `4:5` | `816x1024` | `1720x2150` | `896x1120` |
| `5:4` | `1024x816` | `2150x1720` | `1120x896` |
| `2:1` | `1024x512` | `2716x1358` | `1408x704` |
| `1:2` | `512x1024` | `1358x2716` | `704x1408` |

## Response

```json
{
  "ok": true,
  "data": {
    "image_urls": [
      "https://cdn.codia.ai/generated/abc123.png"
    ]
  }
}
```

| Field | Type | Description |
|---|---|---|
| `data.image_urls` | string[] | Array of CDN URLs to generate images, length equal to `--n` |
| `data.local_file` | string | CLI default local file path after download when there is one image; does not exist when using `--no-download` |
| `data.local_files` | string[] | CLI default local file path after download; does not exist when using `--no-download` |

## Usage Examples

```bash
# Basic generation
codia-design image generate --prompt "The sea after the rain, realistic photography style" --download-dir ./outputs

# Only save JSON, do not download images
codia-design image generate --prompt "minimalist app icon for a design tool" --no-download --out result.json

# Transparent background icon (gpt_image)
codia-design image generate \
  --prompt "3D app icon with geometric shapes" \
  --model gpt_image \
  --quality high \
  --background transparent \
  --out icon.json

# Generation of reference images
codia-design image generate \
  --prompt "product photo on marble table" \
  --model nano_banana_pro \
  --reference_images '["https://example.com/style1.jpg"]' \
  --out result.json

# Generate 4 photos in batches
codia-design image generate --prompt "hero banner" --n 4 --out batch.json
```

Read the result URL:

```js
const { data } = require('./result.json');
data.image_urls.forEach((url, i) => console.log('Image', i, url));
```

## Errors & Billing

| HTTP | Meaning | Fix |
|---|---|---|
| 400 | prompt is empty, size format is wrong, model does not support this parameter | Check parameters |
| 402 | Insufficient credits | Credits = credits/image × n, plus configured extra reference-image surcharges |
| 429 | Rate limit exceeded | Retry after backing off |

**Credits**: See model table credits/image × `n`. The CLI prints an `open_api_v2` estimate before running. After the command completes, it checks `available_credits` and reminds the user if the remaining balance is below 2x the estimated cost; this does not block generation. Use `--estimate` to show cost without sending the request. Extra reference images can add surcharges for some models. · **Duration**: Synchronous, usually 5–20s

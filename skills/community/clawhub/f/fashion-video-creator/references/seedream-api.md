# Seedream API Call Specifications

> **Role:** Defines the exact HTTP request format for Seedream 4.5/5.0 image generation API.
> Load at: Step 3 (calling Seedream API). Not needed if user only wants prompt without image generation.
> It does NOT replace execution. These are API specs, not prebuilt responses.

## Endpoint

```
POST {ARK_API_BASE}/api/v3/images/generations
```

Default base: `https://ark.cn-beijing.volces.com`

## Headers

```
Authorization: Bearer {ARK_API_KEY}
Content-Type: application/json
```

## Version Differences

### Seedream 5.0

```json
{
  "model": "{endpoint_id}",
  "prompt": "Chinese natural language description...",
  "size": "2K",
  "response_format": "url",
  "watermark": false,
  "sequential_image_generation": "disabled",
  "stream": false,
  "seed": -1
}
```

- Output: 2048x2048 square image (URL response)
- Negative prompt: IGNORED (5.0 uses internal Chain-of-Thought)
- Guidance scale: IGNORED
- Prompt style: Natural Chinese language, describe desired outcome
- Cost: ~0.22 CNY per image

### Seedream 4.5

```json
{
  "model": "{model_id}",
  "prompt": "English keyword-stacking style...",
  "size": "{width}x{height}",
  "response_format": "b64_json",
  "watermark": false,
  "seed": -1,
  "negative_prompt": "blurry, extra fingers, distorted hands, watermark, text overlay, cropped feet, cut off at ankles, partial body",
  "guidance_scale": 0
}
```

- Output: specified resolution (base64 response)
- Minimum pixel count: 2560 * 1440 = 3,686,400 pixels
- If below minimum, auto-scale up: `scale = (MIN_PIXELS / total) ^ 0.5`, round to multiple of 8
- For 720x1280 target: generates at ~1440x2560, then center-crops
- Prompt style: English keyword stacking with technical terms
- Cost: ~0.32 CNY per image
- guidance_scale: avoid passing by default (causes skin artifacts)

## Default Negative Prompt (4.5 only)

```
blurry, extra fingers, distorted hands, watermark, text overlay, cropped feet, cut off at ankles, partial body
```

WARNING: Heavy negative prompts (especially "plastic skin", "real person face") cause patchy shadow artifacts on skin. Keep minimal.

## Post-Processing: Crop to Ratio

After receiving the raw image:
1. Check if raw aspect ratio matches target (720:1280 = 9:16)
2. If mismatch > 0.01: center-crop to target ratio
   - If raw is wider: crop horizontal center
   - If raw is taller: crop vertical center
3. NO downscaling — keep highest resolution for Seedance upload

Output resolutions:
- 4.5: ~1440x2560 (for 9:16 target)
- 5.0: ~1152x2048 (cropped from 2048x2048 square)

## Timeout

300 seconds (5 minutes)

## Error Handling

- Missing ARK_API_KEY: RuntimeError
- HTTP error: raise with status code
- No image data in response: RuntimeError
- All errors wrapped as: `RuntimeError(f"Seedream generation failed: {e}")`

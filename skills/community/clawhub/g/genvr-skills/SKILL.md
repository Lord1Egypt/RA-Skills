---
name: genvr-skills
description: "Generate images, videos, and process media using the GenVR API. Standalone Node.js CLI."
license: MIT
metadata:
  openclaw:
    requires:
      env:
        - GENVR_API_KEY
        - GENVR_UID
---

# GenVR Skills — AI Media Generation & Utilities

Generate images, videos, and perform various media processing tasks using the GenVR API. This standalone Node.js toolkit provides a pure CLI for interacting with GenVR's asynchronous task pipeline.

**IMPORTANT:** Most operations require a `GENVR_API_KEY` and a `GENVR_UID`. Get them from [api.genvrresearch.com](https://api.genvrresearch.com/obtain-api).

## Usage

Run via `npx` directly from the package:

**List available models:**
```bash
npx genvr-skills list
```

**Generate content (unified):**
```bash
npx genvr-skills generate --category imagegen --subcategory google_imagen3 prompt="A futuristic city in VR" height=1024 width=1024
```

**Edit an image with Nano Banana 2:**
```bash
npx genvr-skills generate --category imgutils --subcategory google_nano_banana_2 image_url="https://media.genvr.com/assets/..." prompt="add a futuristic helmet"
```

**Check job status:**
```bash
npx genvr-skills status --job-id "TASK_ID" --category "imagegen" --subcategory "google_imagen3"
```

## Authentication

Authentication is handled via environment variables:

| Env Var | Description |
|---------|-------------|
| `GENVR_API_KEY` | Your GenVR API Token |
| `GENVR_UID` | Your GenVR User ID |

## Core Commands

### list
Lists all available categories and subcategories. 
- `--json`: Output as raw JSON.

### generate
The primary command for starting new generation tasks.
- `--category`: The category of the model (e.g., `imagegen`).
- `--subcategory`: The specific model variant (e.g., `google_imagen3`).
- `--filename`: Optional output filename.
- `--no-wait`: Return immediately after starting the job.
- `key=value`: Model parameters (e.g., `prompt="cat"`, `steps=25`).

### status
Retrieves the status or result of an existing task.
- `--job-id`: The ID returned by `generate`.
- `--category`: Required for v2 status check.
- `--subcategory`: Required for v2 status check.

## Examples

### Generating a Cinematic 360 Panorama
```bash
npx genvr-skills generate --category 3dgen --subcategory panorama prompt="A hyper-realistic cinematic 360 panorama of an ancient bioluminescent forest at night, 8k resolution, ethereal lighting"
```

### Professional Video Generation (Image-to-Video)
Use a high-quality model like Google Veo 3 for image-to-video translation:
```bash
npx genvr-skills generate --category videogen --subcategory google_veo3_i2v image_url="https://media.genvr.com/assets/..." prompt="The camera cinematicly glides through the scene as the bioluminescent plants begin to glow intensely, soft wind blowing through the leaves, masterpiece quality"
```

## Filename Pattern
Generated files follow the pattern: `yyyy-mm-dd-hh-mm-ss-category.ext`.

## Tips
- Run `list` frequently to see new tools added to the platform.
- Use `--no-wait` for video generation tasks, as they may take several minutes.
- Most models follow the standard OpenAPI schema; details at `api.genvrresearch.com`.

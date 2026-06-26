---
name: geoinfer-image-geolocation
description: AI image geolocation via visual analysis — no GPS or EXIF needed. Requires GEOINFER_API_KEY.
metadata: {"clawdbot":{"emoji":"🌍","requires":{"env":["GEOINFER_API_KEY"]}}}
---

# GeoInfer — AI Image Geolocation

🌍 Geolocate any image using AI — no GPS, no EXIF, no metadata required.

GeoInfer analyzes visual cues (architecture, terrain, vegetation, signage) to predict where a photo was taken, down to city level. Built for OSINT, digital forensics, investigative journalism, and security workflows.

Requires the `GEOINFER_API_KEY` environment variable.

## Setup

1. Get your API key from [app.geoinfer.com/en/api](https://app.geoinfer.com/en/api)
2. Run: `export GEOINFER_API_KEY="geo_your_key_here"`

## Tools

### Predict Image Location
```bash
bash scripts/predict.sh /path/to/image.jpg [model_id] [top_n]
```
- `model_id` — model to use (default: `global_v0_1`). Run `models.sh` to list available models.
- `top_n` — number of top predictions to return, 1–15 (default: `5`)
- Accepts JPEG, PNG, WebP, and other common image formats (max 10MB)

**Example:**
```bash
bash scripts/predict.sh photo.jpg global_v0_1 5
```

**Output:** JSON array of top location predictions with coordinates and confidence scores.

### List Available Models
```bash
bash scripts/models.sh
```
Returns all models available to your API key (e.g., Global, Car, Property, Accuracy).

### Check Credits
```bash
bash scripts/credits.sh
```
Returns your current credit balance.

## Credit Costs

| Model type | Credits per prediction |
|------------|------------------------|
| Global     | 1                      |
| Car        | 2                      |
| Property   | 3                      |
| Accuracy   | 3                      |

## Agent Usage Notes

- Always run `models.sh` first if unsure which model to use
- Prefer `global_v0_1` for general-purpose geolocation
- Use `top_n=1` for fastest single-answer responses; `top_n=5` for investigations requiring confidence comparison
- Check credits before running large batch jobs
- Images must be local files — download remote images before passing to `predict.sh`

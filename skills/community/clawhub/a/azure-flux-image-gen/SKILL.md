---
name: flux-image-gen
description: Generate images using Black Forest Labs FLUX.2-pro via Azure AI Foundry. Use when asked to create, generate, or produce images, illustrations, photos, artwork, posters, or visual content. Supports custom dimensions, seeds for reproducibility, and Chinese text overlay via Node.js Canvas. Requires FLUX_ENDPOINT and FLUX_API_KEY environment variables.
metadata:
  openclaw:
    requires:
      env:
        - FLUX_ENDPOINT
        - FLUX_API_KEY
    primaryEnv: FLUX_API_KEY
---

# FLUX.2-pro Image Generation

Generate high-quality images from text prompts using FLUX.2-pro on Azure AI Foundry.

## Setup

Set environment variables (typically in OpenClaw config or shell profile):

```bash
export FLUX_ENDPOINT="https://<resource>.services.ai.azure.com/providers/blackforestlabs/v1/flux-2-pro?api-version=preview"
export FLUX_API_KEY="YOUR_KEY_HERE"
```

## Quick Generation

Use the bundled script:

```bash
node scripts/generate.mjs --prompt "a red fox in autumn forest" --output fox.png
node scripts/generate.mjs --prompt "cute robot" --width 1440 --height 816 --output robot.png
```

## Direct API Call

When the script isn't suitable, call the API directly:

```bash
curl -s -X POST "$FLUX_ENDPOINT" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FLUX_API_KEY" \
  -d '{"prompt":"a cat","width":1024,"height":1024,"n":1,"model":"FLUX.2-pro"}' \
  | node -e "process.stdin.on('data',d=>{const j=JSON.parse(d);require('fs').writeFileSync('out.png',Buffer.from(j.data[0].b64_json,'base64'))})"
```

**Critical parameters:** `"n": 1` and `"model": "FLUX.2-pro"` are mandatory. Omitting them causes HTTP 500.

## Chinese Text Overlay

FLUX cannot render CJK characters. Overlay text with Node.js Canvas:

```javascript
import { createCanvas, loadImage, registerFont } from "canvas";
registerFont("NotoSansCJK-Bold.otf", { family: "NotoSansCJK" });

const img = await loadImage("base.png");
const canvas = createCanvas(img.width, img.height);
const ctx = canvas.getContext("2d");
ctx.drawImage(img, 0, 0);
ctx.font = 'bold 48px "NotoSansCJK"';
ctx.fillStyle = "#ffffff";
ctx.fillText("你好世界", 100, 100);
```

Requires: `npm install canvas` + a CJK font file (e.g., NotoSansCJK-Bold.otf).

## Best Practices

- **Serialize requests** — avoid parallel API calls; use sequential generation
- **Set 180s timeout** — generation can take 30–120 seconds
- **Prompt in English** — FLUX works best with English prompts
- **Content filter** — avoid violent, sexual, or otherwise filtered content in prompts
- **Print quality** — use 1240×1754 for A3, scale up as needed

## API Reference

See [references/api.md](references/api.md) for full request/response schema and size options.

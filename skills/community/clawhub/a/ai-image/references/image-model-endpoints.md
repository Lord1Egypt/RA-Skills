# Image Model Endpoints (Snapshot)

Snapshot source: `docs.json` group `APIs -> Images`
Snapshot date: 2026-03-20

Default mode: SSE-first.
- Primary call path: replace `/generation/` with `/generation/sse/` for each endpoint below.
- Fallback call path: use the listed endpoint below with polling result fetch.

## Endpoints
- `POST /generation/google/nano-banana-2`
- `POST /generation/google/nano-banana-pro`
- `POST /generation/google/nano-banana`
- `POST /generation/openai/gpt-image-1.5`
- `POST /generation/openai/gpt-image-1`
- `POST /generation/kling-ai/v3/image`
- `POST /generation/kling-ai/o3-image`
- `POST /generation/kling-ai/o1-image`
- `POST /generation/xai/grok-imagine-image`
- `POST /generation/bytedance/seedream-5-lite`
- `POST /generation/bytedance/seedream-4.5`
- `POST /generation/bytedance/seedream-4.0`
- `POST /generation/qwen/qwen-image-2-pro`
- `POST /generation/qwen/qwen-image-2`
- `POST /generation/qwen/qwen-image`
- `POST /generation/vidu/q2/text-to-image`
- `POST /generation/runwayml/gen4-image`
- `POST /generation/runwayml/gen4-image-turbo`
- `POST /generation/black-forest-labs/flux-2-pro`
- `POST /generation/black-forest-labs/kontext`
- `POST /generation/ideogram/ideogram`
- `POST /generation/z-image/z-image`
- `POST /generation/topaz/upscale/image`

## Refresh command
```bash
python scripts/inspect_openapi.py \
  --openapi /abs/path/to/openapi.json \
  --docs /abs/path/to/docs.json \
  --list-endpoints
```

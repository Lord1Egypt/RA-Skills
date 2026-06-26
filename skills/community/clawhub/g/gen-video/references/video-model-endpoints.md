# Video Model Endpoints (Snapshot)

Snapshot source: `docs.json` group `APIs -> Videos`
Snapshot date: 2026-03-20

Default mode: SSE-first.
- Primary call path: replace `/generation/` with `/generation/sse/` for each endpoint below.
- Fallback call path: use the listed endpoint below with polling result fetch.

## Endpoints
- `POST /generation/openai/sora-2-pro`
- `POST /generation/openai/sora-2`
- `POST /generation/google/veo-2`
- `POST /generation/google/veo-3.1`
- `POST /generation/google/veo-3.1-fast`
- `POST /generation/bytedance/seedance-1-pro`
- `POST /generation/bytedance/seedance-1-pro-fast`
- `POST /generation/bytedance/seedance-1.5`
- `POST /generation/xai/grok-imagine-video`
- `POST /generation/kling-ai/v3/video`
- `POST /generation/kling-ai/o3/video`
- `POST /generation/kling-ai/o3/edit`
- `POST /generation/kling-ai/o1/video`
- `POST /generation/kling-ai/o1/edit`
- `POST /generation/kling-ai/kling-v2.6`
- `POST /generation/kling-ai/motion-control-v2.6`
- `POST /generation/kling-ai/kling-v2.5-turbo`
- `POST /generation/runwayml/gen-4.5`
- `POST /generation/runwayml/gen4-turbo`
- `POST /generation/runwayml/gen4-aleph`
- `POST /generation/wan/wan-v2.6`
- `POST /generation/luma/ray-2`
- `POST /generation/luma/ray-2-flash`
- `POST /generation/vidu/q2/video-turbo`
- `POST /generation/vidu/q3`
- `POST /generation/minimax/hailuo-2.3`
- `POST /generation/minimax/hailuo-2.3-fast`
- `POST /generation/lightricks/ltx-2.3`
- `POST /generation/lightricks/ltx-2.3/audio-to-video`
- `POST /generation/lightricks/ltx-2.3/extend-video`
- `POST /generation/lightricks/ltx-2.3/retake-video`
- `POST /generation/pixverse/v5.6`
- `POST /generation/bytedance/omnihuman-v1.5`
- `POST /generation/sync/lipsync-2`
- `POST /generation/veed/lipsync`
- `POST /generation/pixverse/lipsync`
- `POST /generation/topaz/upscale/video`
- `POST /generation/runwayml/upscale-v1`

## Refresh command
```bash
python scripts/inspect_openapi.py \
  --openapi /abs/path/to/openapi.json \
  --docs /abs/path/to/docs.json \
  --list-endpoints
```

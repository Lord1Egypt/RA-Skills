# Lipsync v2 (fal.ai)

## Model

| Model | Endpoint | Description |
|-------|----------|-------------|
| Sync Lipsync 2.0 | `fal-ai/sync-lipsync/v2` | Audio-driven lip synchronization on video |

## Input Schema

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `video_url` | string | ✅ | — | Input video URL |
| `audio_url` | string | ✅ | — | Input audio URL (the voice to sync to) |
| `model` | enum | | `"lipsync-2"` | `lipsync-2`, `lipsync-2-pro` (1.67x cost, higher quality) |
| `sync_mode` | enum | | `"cut_off"` | How to handle audio/video duration mismatch |

### Sync Modes

| Mode | Description |
|------|-------------|
| `cut_off` | Cut the longer media to match shorter |
| `loop` | Loop the shorter media |
| `bounce` | Bounce (forward-reverse) the shorter media |
| `silence` | Pad with silence if audio is shorter |
| `remap` | Time-remap to match durations |

## Output Schema

```json
{"video": {"url": "https://..."}}
```

## Python Example

```python
import fal_client
result = fal_client.subscribe("fal-ai/sync-lipsync/v2", arguments={
    "video_url": "https://example.com/person-talking.mp4",
    "audio_url": "https://example.com/new-voiceover.mp3",
    "model": "lipsync-2-pro",
    "sync_mode": "cut_off",
})
video_url = result["video"]["url"]
```

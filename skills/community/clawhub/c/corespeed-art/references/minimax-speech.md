# MiniMax Speech-02 HD (fal.ai)

Endpoint: `fal-ai/minimax/speech-02-hd`

## Input Schema

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `text` | string | ✅ | — | Max 5000 chars |
| `voice_setting` | VoiceSetting | | — | Voice configuration |
| `audio_setting` | AudioSetting | | — | Loudness normalization settings |
| `language_boost` | enum | | — | `Chinese`, `English`, `Japanese`, `Korean`, `French`, `German`, `Spanish`, `Russian`, `Arabic`, `auto`, and 20+ more |
| `output_format` | enum | | `"hex"` | `url`, `hex`. Use `url` to get downloadable link |

## Output Schema

```json
{"audio": {"url": "https://..."}, "duration_ms": 3500}
```

## Example

```bash
uv run fal.py fal-ai/minimax/speech-02-hd --json '{"text":"Hello world","output_format":"url","language_boost":"English"}' -f voice.mp3
```

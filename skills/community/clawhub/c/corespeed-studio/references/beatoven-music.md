# Beatoven Music Generation (fal.ai)

Endpoint: `beatoven/music-generation`

## Input Schema

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | ✅ | — | Describe the music (e.g., "Jazz music for a late-night restaurant") |
| `negative_prompt` | string | | `""` | What to avoid |
| `duration` | float | | `90` | Length in seconds |
| `refinement` | integer | | `100` | Higher = better quality, slower |
| `creativity` | float | | `16` | Higher = more creative interpretation |
| `seed` | integer | | random | |

## Output Schema

```json
{"audio": {"url": "https://..."}}
```

## Example

```bash
uv run fal.py beatoven/music-generation --json '{"prompt":"Upbeat electronic music for a tech product launch","duration":60,"refinement":100}' -f music.mp3
```

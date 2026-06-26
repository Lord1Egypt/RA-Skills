---
name: byted-music-generate
description: Generate music using Volcengine Imagination API. Supports vocal songs, instrumental BGM, and lyrics generation. Use when the user wants to create songs, background music, soundtracks, write lyrics, or mentions "music generation", "BGM", or "songwriting".
license: Complete terms in LICENSE
---

# Music Generate Skill

This skill generates music using the [Volcengine Music Generation API](https://www.volcengine.com/docs/84992). It supports vocal songs, instrumental BGM, and AI lyrics generation.

## Trigger Conditions

1. User wants to generate a song (with lyrics or a text prompt)
2. User needs background music, instrumental tracks, or soundtracks
3. User wants AI-generated lyrics
4. User mentions "write a song", "music generation", "BGM", "background music", "lyrics"

## Environment Variables

Before using this skill, ensure the following environment variables are set:

- `VOLCENGINE_ACCESS_KEY` — AccessKey ID
- `VOLCENGINE_SECRET_KEY` — AccessKey Secret

How to obtain: [Volcengine Console](https://console.volcengine.com/) → Account (top-right) → Key Management → Create Key.

## Usage

1. Determine user intent and select the mode (`song` / `bgm` / `lyrics`).
2. `cd` to the skill directory: `skills/byted-music-generate`.
3. Run the script. The script polls the API internally and may take **several minutes** to complete (typically 1–5 minutes for song/bgm).
4. **Monitor execution**: If the runtime environment moves the command to background, you MUST periodically (every 10 seconds) read the terminal output to check whether the script has finished. The script prints polling progress to stderr and outputs a single JSON line to stdout upon completion.
5. Once completed, return the `audio_url` or `lyrics` from the JSON output to the user.

## Three Modes

### 1. song — Vocal Song

User provides lyrics (Lyrics) or a text prompt (Prompt) to generate a vocal song.

```bash
# With text prompt
python scripts/music_generate.py song --prompt "A song about summer at the beach" --genre Pop --gender Female

# With lyrics
python scripts/music_generate.py song --lyrics "[verse]\nMoonlight on the windowsill\nMemories flowing like water\n[chorus]\nYou are my moonlight" --genre Folk --mood "Sentimental/Melancholic/Lonely"
```

**Note**: `--lyrics` and `--prompt` are mutually exclusive; lyrics takes priority. If the user hasn't provided lyrics, you can first use the `lyrics` mode to generate them, then pass the result to the `song` mode.

### 2. bgm — Instrumental BGM

Describe the desired music in natural language. The v5.0 model does not require Genre/Mood parameters — just describe everything in the `--text` field.

```bash
python scripts/music_generate.py bgm --text "Relaxed coffee shop ambiance music with piano and guitar" --duration 60

# With song structure segments
python scripts/music_generate.py bgm --text "Epic game soundtrack" --segments '[{"Name":"intro","Duration":10},{"Name":"chorus","Duration":30}]'
```

### 3. lyrics — Lyrics Generation

Returns synchronously (no polling needed). Can be used standalone or as a pre-step for the `song` mode.

```bash
python scripts/music_generate.py lyrics --prompt "A song about graduation farewell" --genre Folk --mood "Sentimental/Melancholic/Lonely" --gender Female
```

### Manual Task Query (timeout fallback)

```bash
python scripts/music_generate.py query --task-id "202601397834584670076931"
```

## Mode Detection Logic

```
User Request
    ↓
Contains "instrumental/BGM/background music/soundtrack"?
    ├─ Yes → bgm mode
    └─ No → Contains "lyrics/write lyrics" and does NOT request audio?
        ├─ Yes → lyrics mode
        └─ No → song mode
            ├─ User provided lyrics → --lyrics
            └─ User only described a theme → --prompt (or lyrics first, then song)
```

## Script Parameters

### song mode

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--lyrics` | either | Lyrics with structure tags |
| `--prompt` | either | Text prompt (Chinese, 5-700 chars) |
| `--model-version` | no | `v4.0` or `v4.3` (default: v4.3) |
| `--genre` | no | Music genre |
| `--mood` | no | Music mood |
| `--gender` | no | `Female` / `Male` |
| `--timbre` | no | Vocal timbre |
| `--duration` | no | Duration in seconds [30-240] |
| `--key` | no | Musical key (v4.3 only) |
| `--kmode` | no | `Major` / `Minor` (v4.3 only) |
| `--tempo` | no | Tempo (v4.3 only) |
| `--instrument` | no | Instruments, comma-separated (v4.3 only) |
| `--genre-extra` | no | Secondary genres, comma-separated, max 2 (v4.3 only) |
| `--scene` | no | Scene tags, comma-separated (v4.3 only) |
| `--lang` | no | Language (v4.3 only) |
| `--vod-format` | no | `wav` / `mp3` (v4.3 only) |
| `--billing` | no | `prepaid` / `postpaid` (default: postpaid) |
| `--timeout` | no | Max wait seconds (default: 300) |

### bgm mode

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--text` | yes | Natural language description |
| `--duration` | no | Duration in seconds [30-120] |
| `--segments` | no | JSON array of song structure segments |
| `--version` | no | Model version (default: v5.0) |
| `--enable-input-rewrite` | no | Enable prompt rewriting |
| `--billing` | no | `prepaid` / `postpaid` (default: postpaid) |
| `--timeout` | no | Max wait seconds (default: 300) |

### lyrics mode

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--prompt` | yes | Lyrics prompt (Chinese only, <500 chars) |
| `--genre` | no | Music genre |
| `--mood` | no | Music mood |
| `--gender` | no | `Female` / `Male` |

## Script Return Info

The script outputs JSON with the following fields:

```json
{
    "status": "success | timeout | error",
    "mode": "song | bgm | lyrics | query",
    "task_id": "...",
    "audio_url": "https://...",
    "duration": 46.0,
    "lyrics": "...",
    "error": null
}
```

Return the `audio_url` to the user for download or playback. URLs are valid for approximately 1 year, but users should save the file promptly.

## Error Handling

- `PermissionError: VOLCENGINE_ACCESS_KEY ...`: Inform the user to configure the environment variables. Write them to the workspace environment variable file, then retry.
- `status: "timeout"`: The task is still generating. Provide the user with the `task_id` and the manual query command from the output.
- Copyright check failure (code 50000001): Suggest the user enrich the description or increase the audio duration, then retry.

## References

- Available parameter values (Genre/Mood/Timbre/Instrument etc.): [references/parameters.md](references/parameters.md)
- [Volcengine Music Generation Docs](https://www.volcengine.com/docs/84992)
- [API Signature Guide](https://www.volcengine.com/docs/6369/67269)

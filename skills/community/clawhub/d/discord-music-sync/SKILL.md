---
name: discord-music-sync
description: "Sync song lyrics with music playback timing in Discord. Generates timed lyric audio segments and creates synchronized playback instructions. Use when a user wants to sing along, create karaoke-style lyrics, or time specific lyric lines to music. Triggers: sync lyrics, lyrics timing, karaoke sync, time lyrics to music, lyrics sync."
---

# discord-music-sync

Sync song lyrics with music playback timing. Generates individually timed TTS audio segments for each lyric line.

## Workflow

### Step 1: Parse Lyrics with Timing

Input lyrics in this format (one line per segment):

```
[00:15] 🎤 First lyric line goes here
[00:22] 🎤 Second lyric line
[00:30] 🎤 Third line after a pause
```

Format: `[MM:SS] <text>` — timestamp in minutes:seconds, followed by lyric text.

### Step 2: Generate Timed Audio Segments

For each lyric line:

1. Use `minimax__text_to_audio` with the lyric text
2. Set `output_directory` to a shared folder both Discord bot and agent can access
3. Name the file matching its start timestamp: `lyric_001_00-15.mp3`

Example call:
```python
minimax__text_to_audio(
    text="First lyric line goes here",
    voice_id="Charming_Lady",
    speed=1.0,
    output_directory="C:/Users/funky/discord-media/lyrics"
)
```

### Step 3: Generate Playback Instructions

Create a `playback.txt` file that lists timestamps, filenames, and text:

```
# discord-music-sync playback guide
# Format: timestamp_ms|filename|text

15000|lyric_001_00-15.mp3|First lyric line goes here
22000|lyric_001_00-22.mp3|Second lyric line
30000|lyric_001_00-30.mp3|Third line after a pause
```

### Step 4: Discord Output

When the user asks to play the synced lyrics, use the message tool to send timed messages in Discord — each lyric line follows the previous by the calculated delay.

Formula: `delay_ms = next_timestamp - current_timestamp`

Example: Send first line at t=0, second line after (22000-15000)=7000ms, etc.

## Script

Run `scripts/sync_lyrics.py` to auto-parse and generate:

```bash
uv run python scripts/sync_lyrics.py --lyrics "<file>" --output "<dir>" --voice "<voice_id>"
```

Arguments:
- `--lyrics` — path to lyrics file (one `[MM:SS]` timed line per line)
- `--output` — output directory for audio files
- `--voice` — voice ID (default: `Charming_Lady`)

## Voice Options

| voice_id | Description |
|----------|-------------|
| `Charming_Lady` | Female, warm |
| `male-qn-qingse` | Male, soft |
| `cute_boy` | Male, playful |
| `audiobook_female_1` | Female, clear narration |

See `minimax__list_voices` for full list.

## Tips

- Keep each lyric segment under 15 seconds for clean TTS
- Use shorter segments for faster-tempo songs
- Pause of 0-2 seconds between segments works best for karaoke
- If lyrics aren't pre-timed, estimate: divide total song duration by number of lines for rough timing
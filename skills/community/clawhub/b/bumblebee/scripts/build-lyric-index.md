# Building Your Lyric Index

Bumblebee needs a lyric index to "speak" through music. **You must build your own** — lyrics are copyrighted and can't be distributed.

## Option A: Manual Curation (Recommended)

Create `lyric-index.json` in this directory with this structure:

```json
[
  {
    "uri": "spotify:track:TRACK_ID",
    "track": "Song Name",
    "artist": "Artist Name",
    "text": "The exact lyric line",
    "textLower": "the exact lyric line",
    "start_ms": 45000,
    "end_ms": 52000,
    "mood": "motivational"
  }
]
```

Start with 20-30 of your favorite lyric lines. Add more over time. The more lines you index, the better Bumblebee speaks.

### Tips
- Use Spotify's track URI (right-click → Share → Copy Spotify URI)
- `start_ms` / `end_ms` = the timestamp range of that lyric in the song (milliseconds)
- Find timestamps by playing the song and noting when the line starts/ends
- `mood` is freeform — use whatever feels right (motivational, romantic, funny, sad, triumphant, etc.)

## Option B: Lyrics API

Use a licensed lyrics API to build the index programmatically:

- **Musixmatch** (musixmatch.com/apidocs) — free tier, 2000 calls/day
- **Genius** (docs.genius.com) — free, good for full lyrics + annotations

Fetch lyrics for your Spotify library, parse into individual lines, add timestamps manually or via audio analysis.

## Option C: Let Your Agent Build It

Ask your OpenClaw agent:
> "Build me a Bumblebee lyric index from my top 50 Spotify tracks"

The agent can pull your Spotify library, search for lyrics via API, and assemble the index file.

## Also Needed: lyrics-db.json (Optional)

For emotion-mapped clips (greeting, farewell, motivation, etc.):

```json
{
  "version": "1.0",
  "description": "Lyric clips indexed by emotion/intent for Bumblebee mode",
  "clips": {
    "greeting": [
      {
        "track": "Song Name",
        "artist": "Artist",
        "uri": "spotify:track:ID",
        "lyric": "The lyric line",
        "start_ms": 0,
        "end_ms": 8000,
        "mood": "energetic"
      }
    ],
    "motivation": [],
    "farewell": [],
    "love": [],
    "triumph": []
  }
}
```

This file is optional but makes Bumblebee more expressive when matching intent to lyrics.

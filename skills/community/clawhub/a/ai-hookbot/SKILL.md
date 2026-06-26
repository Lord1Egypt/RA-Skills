---
name: ai-hookbot
description: Scrape viral hooks from YouTube Shorts creators and stitch them with a CTA video to produce ready-to-post TikTok/Reels/Shorts content. Use when asked to make hooks, scrape Shorts, create content from a creator, or run the Hookbot pipeline. Triggers on phrases like "make me hooks from @X", "scrape hooks", "run hookbot", "create content from [creator]", "stitch my CTA".
---

# AI Hookbot

Runs the Hookbot pipeline: scrapes YouTube Shorts hooks from a creator's channel, trims them, and stitches each with your CTA video to produce ready-to-post vertical content.

## Setup

### 1. Install dependencies

```bash
pip install yt-dlp
brew install ffmpeg   # macOS; or apt install ffmpeg on Linux
```

### 2. Clone the pipeline scripts

```bash
git clone https://github.com/YOUR_REPO/hookbot-scripts ~/hookbot
```

> Or place `pipeline.py` and related scripts in any directory — just set `HOOKBOT_SCRIPTS_DIR` below.

### 3. Configure environment variables

Copy `config.example.env`, fill in your paths, and either `source` it or add it to your shell profile:

```bash
cp config.example.env ~/.hookbot.env
# edit ~/.hookbot.env
source ~/.hookbot.env
```

| Variable | Description | Default |
|---|---|---|
| `HOOKBOT_SCRIPTS_DIR` | Directory containing `pipeline.py` | `~/hookbot` |
| `HOOKBOT_CTA_DIR` | Default folder to look for CTA videos | `~/hookbot/cta` |
| `HOOKBOT_YTDLP_PATH` | Path to `yt-dlp` binary | `yt-dlp` (assumes in PATH) |
| `HOOKBOT_FFMPEG_PATH` | Path to `ffmpeg` binary | `ffmpeg` (assumes in PATH) |
| `YOUTUBE_API_KEY` | YouTube Data API v3 key (only needed for `--viral`) | _(optional)_ |

---

## Workflow

1. Parse the user's request to extract:
   - `creator_url` — YouTube Shorts URL (e.g. `https://www.youtube.com/@ZackD/shorts`). If only a handle/name is given, construct the URL.
   - `cta_video` — Path to CTA video. If only a filename is given, resolve against `$HOOKBOT_CTA_DIR`. If not specified, prompt the user.
   - `count` — Number of hooks (default: 10)
   - `hook_duration` — Seconds to grab from each hook (default: 3.0)
   - `output_dir` — Where to save final videos (default: `./output` relative to `$HOOKBOT_SCRIPTS_DIR`)

2. Resolve paths from environment variables (fall back to defaults if unset):

```bash
SCRIPTS_DIR="${HOOKBOT_SCRIPTS_DIR:-~/hookbot}"
CTA_DIR="${HOOKBOT_CTA_DIR:-~/hookbot/cta}"
YTDLP="${HOOKBOT_YTDLP_PATH:-yt-dlp}"
FFMPEG="${HOOKBOT_FFMPEG_PATH:-ffmpeg}"
```

3. Run the pipeline via `exec`, passing only the required env vars explicitly (do NOT source `~/.zshrc` or any shell RC file):

```bash
cd "$SCRIPTS_DIR" && \
YTDLP_PATH="$YTDLP" \
FFMPEG_PATH="$FFMPEG" \
YOUTUBE_API_KEY="${YOUTUBE_API_KEY:-}" \
python3 pipeline.py "<creator_url>" "<cta_video>" \
  --count <count> \
  --hook-duration <hook_duration> \
  --output <output_dir> \
  [--viral]
```

Add `--viral` when the user wants hooks sorted by view count (requires `YOUTUBE_API_KEY`). Default pulls most recent Shorts.

4. Report back a summary:
   - How many hooks were scraped
   - How many final videos were created
   - Output directory path
   - Any failures (sanitize error output before relaying — strip file paths and env var values)

## Prompting for Missing Info

- **CTA video not specified:** Ask "Which CTA video should I use?" then list `.mp4` files in `$HOOKBOT_CTA_DIR`.
- **Creator not specified:** Ask for the YouTube channel handle or Shorts URL.
- **`HOOKBOT_SCRIPTS_DIR` not set / pipeline.py not found:** Tell the user to set the env var and point it to the scripts directory.

## Example Invocations

- "Make me 10 hooks from @ZackD with MyCTA.mp4"
- "Scrape 5 hooks from youtube.com/@SomeCreator/shorts using my furniture CTA"
- "Run hookbot on @MrBeast, 3 second hooks, 15 videos, viral sort"
- "Make hooks from @PeterMcKinnon"

## Notes

- Output videos are 9:16 vertical (1080×1920), normalized automatically.
- Temp files are cleaned up automatically by the pipeline.
- A `manifest.json` is saved in the output directory with metadata.
- If the pipeline errors, relay the error output to the user verbatim so they can debug.
- `--viral` flag requires a YouTube Data API v3 key set as `YOUTUBE_API_KEY`. Get one at [console.cloud.google.com](https://console.cloud.google.com).

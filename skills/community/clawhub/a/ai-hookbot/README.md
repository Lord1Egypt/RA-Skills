# 🎣 AI Hookbot

> Scrape viral hooks from YouTube Shorts and stitch them with your CTA video — ready to post on TikTok, Reels, and Shorts.

An [OpenClaw](https://openclaw.ai) skill that automates the full hook-generation pipeline: find a creator, grab their top Shorts, trim the hooks, and stitch each one with your call-to-action video.

---

## What It Does

1. Scrapes YouTube Shorts from any creator (`@handle` or URL)
2. Trims the first N seconds from each (configurable, default 3s)
3. Stitches each hook with your CTA video
4. Outputs 9:16 vertical MP4s (1080×1920) ready to post

---

## Requirements

- [OpenClaw](https://openclaw.ai) installed
- Python 3.8+
- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) — `pip install yt-dlp`
- [`ffmpeg`](https://ffmpeg.org/) — `brew install ffmpeg` or `apt install ffmpeg`
- `pipeline.py` script (see [hookbot-scripts](#))

---

## Installation

```bash
clawhub install ai-hookbot
```

Then configure your environment:

```bash
cp ~/.nvm/versions/node/*/lib/node_modules/openclaw/skills/ai-hookbot/config.example.env ~/.hookbot.env
# Edit ~/.hookbot.env with your paths
# Source only this file — do NOT source your full ~/.zshrc in the pipeline
source ~/.hookbot.env
```

---

## Usage

Just talk to your OpenClaw agent:

```
Make me 10 hooks from @ZackD with MyCTA.mp4
Scrape 5 hooks from @MrBeast, 3 second hooks
Run hookbot on @PeterMcKinnon, viral sort, 15 videos
```

---

## Configuration

| Variable | Description | Default |
|---|---|---|
| `HOOKBOT_SCRIPTS_DIR` | Directory with `pipeline.py` | `~/hookbot` |
| `HOOKBOT_CTA_DIR` | Default CTA video folder | `~/hookbot/cta` |
| `HOOKBOT_YTDLP_PATH` | Path to `yt-dlp` | `yt-dlp` |
| `HOOKBOT_FFMPEG_PATH` | Path to `ffmpeg` | `ffmpeg` |
| `YOUTUBE_API_KEY` | YouTube API key (viral sort only) | _(optional)_ |

---

## Options

| Option | Description |
|---|---|
| `--count N` | Number of hooks to generate (default: 10) |
| `--hook-duration N` | Seconds to take from each hook (default: 3.0) |
| `--viral` | Sort by view count instead of recency (requires API key) |
| `--output DIR` | Output directory (default: `./output`) |

---

## Output

Each run produces:
- `output/hook_01.mp4`, `hook_02.mp4`, … — final stitched videos
- `output/manifest.json` — metadata for each video (source URL, views, etc.)

---

## License

MIT

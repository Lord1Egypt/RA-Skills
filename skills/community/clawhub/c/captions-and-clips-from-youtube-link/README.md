# ⚡ MakeAIClips — YouTube to Viral Clips (OpenClaw Agent Skill)

> Turn any YouTube video into TikTok, Instagram Reels, and YouTube Shorts clips — with burned-in captions and AI-generated hook titles — in ~60 seconds.

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Agent_Skill-purple)](https://clawhub.ai/nosselil/captions-and-clips-from-youtube-link)
[![ClawHub](https://img.shields.io/badge/ClawHub-Install-blue)](https://clawhub.ai/nosselil/captions-and-clips-from-youtube-link)
[![API](https://img.shields.io/badge/API-Live-green)](https://makeaiclips.live)

## What It Does

Give your AI agent the ability to create short-form video content from YouTube links:

- 🎬 **AI clip selection** — GPT picks the most engaging moments
- 📝 **Word-by-word captions** — 15+ styles including karaoke, typewriter, cinematic
- 🎣 **Hook titles** — 3 AI-generated title variations per clip
- 📐 **Vertical format** — 1080x1920 (9:16) ready for all platforms
- ⚡ **Fast** — ~60 seconds per job (Deepgram transcription + GPT + FFmpeg)
- 🎨 **Customizable** — caption style, title style, duration, quality, clip count

## Quick Start

### Install via ClawHub

```bash
clawhub install captions-and-clips-from-youtube-link
```

### Or manually

Copy the `SKILL.md` and `skill.json` into your OpenClaw workspace `skills/` directory.

### Get an API Key

1. Sign up free at [makeaiclips.live](https://makeaiclips.live/sign-up) (no credit card)
2. Get your API key from the [dashboard](https://makeaiclips.live/dashboard/api-key)
3. Set the environment variable:

```bash
export MAKEAICLIPS_API_KEY="mak_live_your_key_here"
```

## Usage

Just tell your agent:

> "Make clips from this YouTube video: https://youtube.com/watch?v=..."

The agent will:
1. Submit the job to MakeAIClips API
2. Poll for progress (download → transcribe → select → render)
3. Present you with clips, hook titles, and download links

## Caption Styles

| Style | Preview |
|-------|---------|
| `karaoke-yellow` | White text, active word highlighted in yellow |
| `white-shadow` | Clean white with drop shadow |
| `boxed` | Text in dark rounded boxes |
| `gradient-bold` | Orange/white alternating |
| `subtitle-documentary` | Uppercase with fade + letterbox |
| `typewriter` ⭐ | Character-by-character reveal |
| `cinematic` ⭐ | Elegant serif with letterbox bars |
| + 8 more styles | MrBeast, Hormozi, neon, gradient, etc. |

⭐ = Studio plan exclusive

## Title Styles

| Style | Look |
|-------|------|
| `bold-center` | White bold centered (default) |
| `top-bar` | Dark semi-transparent bar |
| `pill` | Yellow pill background |
| `outline` | White outline border |
| `gradient-bg` | Purple background box |
| `none` | No title |

## Video Quality

| Quality | CRF | Best For |
|---------|-----|----------|
| `high` | 18 | Publishing (default) |
| `medium` | 23 | Balance of speed & quality |
| `low` | 28 | Quick previews |

## API Example

```bash
# Submit
curl -X POST "https://makeaiclips.live/api/v1/clips" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer mak_live_YOUR_KEY" \
  -d '{
    "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "num_clips": 3,
    "caption_style": "karaoke-yellow",
    "clip_duration": "medium",
    "quality": "high"
  }'

# Poll
curl "https://makeaiclips.live/api/v1/clips/JOB_ID" \
  -H "Authorization: Bearer mak_live_YOUR_KEY"

# Download
curl -o clip.mp4 "https://makeaiclips.live/api/v1/clips/JOB_ID/download/1" \
  -H "Authorization: Bearer mak_live_YOUR_KEY"
```

## Pricing

| Plan | Clips/month | Price |
|------|------------|-------|
| 🆓 Free | 10 | $0 |
| ⚡ Pro | 100 | $20/mo |
| 🎬 Studio | 300 + premium styles | $50/mo |
| 📅 Yearly | 5,000 + everything | $500/yr |

Sign up: [makeaiclips.live](https://makeaiclips.live/sign-up)

## Requirements

- [OpenClaw](https://github.com/openclaw/openclaw) agent with skill support
- `MAKEAICLIPS_API_KEY` environment variable (free tier available)

## Links

- **Web App:** [makeaiclips.live](https://makeaiclips.live)
- **Dashboard:** [makeaiclips.live/dashboard](https://makeaiclips.live/dashboard)
- **ClawHub:** [clawhub.ai/nosselil/captions-and-clips-from-youtube-link](https://clawhub.ai/nosselil/captions-and-clips-from-youtube-link)
- **API Docs:** [makeaiclips.live/docs](https://makeaiclips.live/docs)

## License

MIT

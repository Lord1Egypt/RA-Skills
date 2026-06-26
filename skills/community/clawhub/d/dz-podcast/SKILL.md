---
name: dz-podcast
description: Generate and publish a dual-host daily podcast. Fetches news, generates a conversational script between two hosts, synthesizes audio via Fish Audio or Edge TTS, publishes to S3 with RSS feed for Apple Podcasts, Spotify, etc. Fully automated with cron support.
---

# Dual-Host Daily Podcast Generator

Automated daily podcast with two AI hosts. Generates text brief + dual-voice audio, publishes to RSS, delivers via messaging.

## Concept

- **Format**: Two hosts — one explains/analyzes, the other asks and transitions
- **Duration**: Configurable, default ~7 minutes
- **Style**: Casual, opinionated, conversational — like two friends chatting about the news
- **Topics**: Customizable (default: AI/Tech, Stocks, Macro, Crypto)

## Architecture

```
Fetch News → Text Brief → Dual-Voice Script → TTS Audio → S3 Upload → RSS Update → Deliver
```

## Configuration

Set these in your environment:

| Variable | Description |
|----------|-------------|
| `S3_BUCKET` | S3 bucket name |
| `PODCAST_DOMAIN` | Custom domain or S3 URL |
| `FISH_API_KEY` | Fish Audio API key (https://fish.audio) |
| `FISH_VOICE_A` | Fish Audio voice ID for Host A |
| `FISH_VOICE_B` | Fish Audio voice ID for Host B |

## Step 1: Fetch News

Use `web_fetch` to scrape sources in parallel. Default sources:

1. `https://news.ycombinator.com/` — Tech
2. `https://www.coindesk.com/` — Crypto
3. `https://techcrunch.com/category/artificial-intelligence/` — AI
4. `https://finance.yahoo.com/` — Markets

Customize sources to match your podcast topic.

## Step 2: Generate Text Brief

Organize news into sections with emoji headers:

```
☀️ Daily Brief | Mar 3, 2026

━━━━━━━━━━━━━━━━━━

🤖 Tech / AI

① Headline
→ One-line take

━━━━━━━━━━━━━━━━━━

📈 Markets

① Headline
→ One-line take

━━━━━━━━━━━━━━━━━━

🎯 Key Takeaway
Summary paragraph
```

## Step 3: Generate Dual-Voice Script

Rewrite the brief as a dialogue. Prefix each line with speaker tag:

```
HostA: Welcome to today's episode...
HostB: Some big stories today...
HostA: Right, let's start with...
```

**Guidelines:**
- Host A: Explains and analyzes, knowledgeable but casual
- Host B: Asks, transitions, reacts
- Substantial turns, not one-liners
- Include analysis and discussion, not just headlines
- End with a lighter topic + sign-off

## Step 4: Generate Audio

**Fish Audio (recommended — natural, multi-voice):**
```bash
python3 scripts/fish_dual_tts.py <script.txt> <output.mp3>
```
Parses speaker tags, sends each segment to Fish Audio, concatenates into final MP3.

**Edge TTS (free fallback, single voice):**
```bash
edge-tts --voice en-US-GuyNeural --rate "+5%" --file script.txt --write-media output.mp3
```

## Step 5: Publish

```bash
bash scripts/generate_episode.sh <date> <EP-number> <title> <description> <mp3-file>
```

What it does:
1. Upload MP3 to S3
2. Get **actual duration** via ffprobe
3. Insert `<item>` into RSS feed (newest first)
4. Update `<lastBuildDate>`

## Step 6: Deliver

Send text brief + audio via your preferred channel (Telegram, Discord, Slack, etc.)

## RSS Feed

See `references/rss-format.md` for XML template.

Key rules:
- `<itunes:duration>` = actual duration from ffprobe (never hardcode)
- `<enclosure length>` = actual file size in bytes
- `<itunes:owner>` with email for Apple/Spotify verification
- Cover: 3000x3000 JPEG minimum

## Hosting Options

| Option | Notes |
|--------|-------|
| S3 + Cloudflare Worker | Free HTTPS, recommended |
| S3 + CloudFront | Native AWS |
| Any static host | Just serve MP3 + feed.xml |

## Cron (OpenClaw)

```bash
openclaw cron add --task "Generate daily podcast" --cron "0 8 * * *" --tz "Your/Timezone"
```

## Dependencies

- `python3` + `requests` — Fish Audio TTS
- `ffmpeg` / `ffprobe` — Audio processing
- `aws` CLI — S3 upload
- `edge-tts` (optional) — Free fallback TTS

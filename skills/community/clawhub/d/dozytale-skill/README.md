# dozytale-sleep 🌙

An [Agent Skill](https://docs.openclaw.ai/skills) that helps users fall asleep with a personalized ambient audio story — delivered as a voice message on WhatsApp, WeChat, or Feishu.

No app download required.

## What it does

1. Asks the user one question: *what kind of atmosphere do you want tonight?*
2. Picks a matching theme from DozyTale's library (139 themes across 6 categories)
3. Downloads the AI-narrated story + background music from OSS
4. Mixes them together with ffmpeg (story at full volume, BGM looped at 18%)
5. Sends it as a voice message via OpenClaw

## Requirements

- [OpenClaw](https://openclaw.ai) with WhatsApp / WeChat / Feishu linked
- `ffmpeg` installed (`brew install ffmpeg` on macOS)

## Categories

| Choice | Category |
|--------|----------|
| 🌫️ Zone Out | Ocean waves, streams, snowy silence |
| 🌿 Nature Sounds | Rain, birdsong, seaside white noise |
| 🎵 Bedtime Story | Pillow talk, gentle memories |
| 🎠 Music Only | Piano, guqin, Bach, music box |
| 👶 Kids Story | Goodnight Baby, fairy tales |
| 🎵 Children's Songs | Classic lullabies |

## Installation

This skill is auto-discoverable by OpenClaw. Add it to your skills directory:

```bash
git clone https://github.com/dozytale/dozytale-sleep ~/.openclaw/skills/dozytale-sleep
```

Then restart the gateway:

```bash
openclaw gateway restart
```

## Usage

Trigger by saying anything like:

> 睡不着 / 帮我入睡 / 睡前故事 / can't sleep / bedtime story / help me relax

Your AI agent will take it from there.

## Updating the theme catalog

The theme catalog (`themes.json`) is pre-built. To regenerate it from the source JSONL files (requires access to the DozyTale backend repo):

```bash
python3 build_catalog.py

# Verify story manifests exist on OSS (slow, ~2 min):
python3 build_catalog.py --check-stories
```

## Pre-mixing audio (optional)

You can pre-mix audio for specific themes to avoid on-demand ffmpeg processing:

```bash
python3 mix_audio_pipeline.py --theme ocean_breath
python3 mix_audio_pipeline.py --all
```

Output goes to `output/{theme_key}/story_with_bgm.mp3`.

## Verify before publishing

```bash
bash verify.sh
```

## Links

- 🌐 [dozytale.ai](https://dozytale.ai) — full app with personalized AI stories
- 📦 [SkillHub](https://skillhub.club) — discover more agent skills
- 🦞 [ClawHub](https://clawhub.ai) — OpenClaw skill marketplace

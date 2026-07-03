---
name: doubao-genbgm
description: Based on the Volcano Engine Doubao Music Generation API, supports instrumental BGM generation and vocal song generation. BGM mode generates background music from text descriptions; Song mode supports generating complete vocal songs from prompts or lyrics, with control over genre, mood, timbre, key, tempo, instruments, and more. Use this skill when users need to generate background music, BGM, songs, or soundtracks.
compatibility: Requires Python 3.9+ and the requests library (pip install requests), a Volcano Engine account with the music generation service enabled
metadata:
  author: SkillDeveloper
  version: "1.0"
allowed-tools: Bash(python3:*) Bash(pip:*)
---

# Doubao Music Generation Skill

Based on the Volcano Engine Doubao Music Generation API, a single script supports two modes:
- **BGM Mode**: Text description -> instrumental background music (no vocals)
- **Song Mode**: Prompt or lyrics -> complete vocal song

## Prerequisites

**1. Install Dependencies**
```bash
pip install requests
```

**2. Configure Authentication**
```bash
# Edit .env and fill in your Volcano Engine AccessKey and SecretKey
export VOLC_ACCESS_KEY=$VOLC_ACCESS_KEY

# 火山引擎 Secret Access Key（必填）
export VOLC_SECRET_KEY=$VOLC_SECRET_KEY
```

Obtain your AccessKeyId and SecretAccessKey from the [Volcano Engine Console -> Key Management](https://console.volcengine.com/iam/keymanage/).

---

## 1. Instrumental BGM Generation

```bash
# Basic BGM generation
python3 scripts/gen_music.py \
  --mode bgm \
  --text "Cafe light music, piano and guitar, relaxing and healing, 60 seconds" \
  --output cafe_bgm.mp3

# Specify duration and format
python3 scripts/gen_music.py \
  --mode bgm \
  --text "Epic cinematic soundtrack, string ensemble with brass, magnificent and awe-inspiring" \
  --duration 90 \
  --format wav \
  --output epic.wav

# Use structured segments (v5.0)
python3 scripts/gen_music.py \
  --mode bgm \
  --text "Electronic dance music, EDM style, energetic" \
  --segments '[{"Name":"intro","Duration":10},{"Name":"chorus","Duration":30},{"Name":"outro","Duration":10}]' \
  --output edm_bgm.mp3

# Enable prompt rewrite (improves results)
python3 scripts/gen_music.py \
  --mode bgm \
  --text "Sports video soundtrack" \
  --rewrite \
  --duration 60 \
  --output sport.mp3
```

---

## 2. Vocal Song Generation

```bash
# Generate song from prompt
python3 scripts/gen_music.py \
  --mode song \
  --prompt "A song about summer and the seaside, lighthearted and cheerful" \
  --genre "Pop" \
  --mood "Happy" \
  --gender Female \
  --output summer.mp3

# Generate song from lyrics (v4.3, fine-grained control)
python3 scripts/gen_music.py \
  --mode song \
  --lyrics "[verse]
I remember that day, the day we fell in love
Promised each other we'd never say goodbye
[chorus]
The day I gave my heart to you
You disappeared before my eyes" \
  --model-version v4.3 \
  --genre "Folk" \
  --mood "Sentimental/Melancholic/Lonely" \
  --gender Female \
  --timbre "Ethereal" \
  --output folk_song.mp3

# Read lyrics from file
python3 scripts/gen_music.py \
  --mode song \
  --lyrics-file my_lyrics.txt \
  --genre "Chinese Style" \
  --mood "Dreamy/Ethereal" \
  --output guofeng.mp3

# Fine-grained control (key/tempo/instruments)
python3 scripts/gen_music.py \
  --mode song \
  --prompt "Jazz-style urban life" \
  --model-version v4.3 \
  --genre "Jazz" \
  --mood "Chill" \
  --gender Male \
  --timbre "Magnetic" \
  --key "C" \
  --kmode "Major" \
  --tempo "Moderato" \
  --instrument "Saxophone,Acoustic_Piano,Bass" \
  --scene "Coffee Shop,Evening" \
  --output jazz_city.mp3

# English song
python3 scripts/gen_music.py \
  --mode song \
  --prompt "A song about chasing dreams and never giving up" \
  --model-version v4.3 \
  --genre "Pop Rock" \
  --mood "Inspirational/Hopeful" \
  --gender Male \
  --lang English \
  --output dream.mp3
```

---

## Parameter Reference

### Common Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--mode` | `bgm`=instrumental, `song`=vocal song | `bgm` |
| `--billing` | `prepaid`=prepaid, `postpaid`=postpaid | `postpaid` |
| `--duration` | Duration in seconds; BGM: [30,120], Song: [30,240] | 60 |
| `--format` | Output format `mp3` / `wav` | `mp3` |
| `--output` | Output file path | `output.mp3` |
| `--poll-interval` | Polling interval in seconds | `5` |

### BGM-Specific Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--text` | BGM description (required), can include genre/mood/scene/instruments in the text | - |
| `--version` | Model version | `v5.0` |
| `--rewrite` | Enable automatic prompt rewrite | off |
| `--segments` | Structured segments JSON (v5.0 only) | - |

### Song-Specific Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--prompt` | Prompt (choose one of `--lyrics` or `--prompt`) | - |
| `--lyrics` | Lyrics text (supports structural tags) | - |
| `--lyrics-file` | Read lyrics from file | - |
| `--model-version` | `v4.0` / `v4.3` / `v5.0` | `v4.3` |
| `--genre` | Primary genre (e.g. Pop / Folk / Electronic) | - |
| `--genre-extra` | Secondary genres, comma-separated (v4.3) | - |
| `--mood` | Mood (e.g. Happy / Dreamy/Ethereal) | - |
| `--gender` | Vocal gender `Male` / `Female` | - |
| `--timbre` | Timbre (e.g. Warm / Husky / Ethereal) | - |
| `--lang` | Language (Chinese/English/Cantonese etc.) | `Chinese` |
| `--key` | Key (A/A#/B/C etc., v4.3) | - |
| `--kmode` | Mode `Major` / `Minor` (v4.3) | - |
| `--tempo` | Tempo (Grave/Andante/Allegro etc., v4.3) | - |
| `--instrument` | Instruments, comma-separated, up to 5 (v4.3) | - |
| `--scene` | Scenes, comma-separated, up to 3 (v4.3) | - |
| `--skip-copy-check` | Disable lyrics copyright check | off |

For more enum values, see [references/params.md](references/params.md).

---

## Notes

- Short simple music (30s + minimal description) is likely to trigger copyright checks; it is recommended to enrich the description, add more parameters, or increase the duration
- Audio download links are time-limited; the script automatically downloads the file locally after generation
- BGM v5.0 does not require separate Genre/Mood parameters; describe them directly in the Text field
- Vocal songs v4.0 and v4.3 differ in the supported enum values for each field; see the parameter documentation for details

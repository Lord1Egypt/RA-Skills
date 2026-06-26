---
name: digital-singer
description: "Turn your NuwaAI digital avatar into a singing performer! The avatar sings with lip-synced mouth movements driven by vocal audio, with synchronized background accompaniment. Supports duet/battle mode: avatar sings the first half, user sings the second half with accompaniment. Includes fun scoring and blind box rewards. Powered by NuwaAI humanctrl API. Use when: user wants the digital avatar to sing, karaoke battle, duet mode, or digital human singing."
---

# 🎤 Digital Singer — NuwaAI Avatar Singing

Turn your NuwaAI digital avatar into a singing performer with lip-synced mouth movements.

## How It Works

```
Audio files → FFmpeg PCM conversion → NuwaAI humanctrl avatar messages → Avatar sings with lip-sync
                                    + Browser <audio> plays accompaniment in sync
```

**Key concept**: Two audio streams work together:
- **speech** (vocal-only): Drives the avatar's mouth movements via NuwaAI `avatar` control messages
- **music** (accompaniment): Plays simultaneously via browser `<audio>` element

## Battle Flow

1. Avatar greets user, lists available songs
2. User picks a song
3. Avatar sings the upper half (vocal drives lip-sync + accompaniment plays in sync)
4. Avatar says "your turn" → accompaniment for lower half plays → user sings along (ASR captures voice)
5. Battle scoring + blind box reward
6. Ask to continue

## User Preparation (What You Need Before Using)

### 1. NuwaAI Account (Required)

Sign up at [nuwaai.com](https://nuwaai.com) (free) and create a digital avatar. You need:
- **API Key** — from your NuwaAI dashboard
- **Avatar ID** — the avatar you want to sing
- **User ID** — your NuwaAI user ID

Enter these in the browser interface, or pre-configure in `.nuwa-config.json`:
```json
{
  "avatarId": "your-avatar-id",
  "apiKey": "your-api-key",
  "userId": "your-user-id"
}
```

### 2. LLM API (Required)

The singing host (conversation agent) needs an OpenAI-compatible LLM API. Configure in `server.mjs` or via environment variables:
- `DASHSCOPE_BASE_URL` — API endpoint (default: Dashscope)
- `DASHSCOPE_API_KEY` — API key
- `QWEN_MODEL` — Model name (default: `qwen-plus`)

### 3. Song Audio Files (Required)

Each song needs **3 audio files** placed in the skill directory:

| File | Purpose | Example |
|------|---------|---------|
| `{song}高潮上清唱.wav` | Upper half vocal (a cappella) — drives avatar lip-sync | `十年高潮上清唱.wav` |
| `{song}高潮上伴奏.MP3` | Upper half accompaniment — plays in sync with avatar | `十年高潮上伴奏.MP3` |
| `{song}高潮下伴奏.MP3` | Lower half accompaniment — plays when user sings | `十年高潮下伴奏.MP3` |

**How to prepare these files:**
- Use any audio editing tool (e.g. Audacity, Adobe Audition) to split songs into upper/lower halves
- Use vocal separation tools (e.g. UVR, Demucs) to extract a cappella (vocal-only) from the upper half
- Export accompaniment as MP3, vocal as WAV (any FFmpeg-supported format works)
- Place all files in the skill directory (same folder as `server.mjs`)

### 4. Song Registry (Required)

After preparing audio files, register each song in `server.mjs` `SONGS` object:
```js
const SONGS = {
  "十年": {
    artist: "陈奕迅",
    acappella_upper: "十年高潮上清唱.wav",
    accomp_upper: "十年高潮上伴奏.MP3",
    accomp_lower: "十年高潮下伴奏.MP3",
  },
  // Add more songs...
};
```

### 5. FFmpeg (Required)

Install FFmpeg for audio format conversion:
```bash
# macOS
brew install ffmpeg
# Ubuntu/Debian
sudo apt install ffmpeg
```

### 6. Node.js 18+ (Required)

```bash
node --version  # must be >= 18
```

## Quick Start

1. Complete all preparation steps above
2. **Copy example song files** from `assets/songs/` to the skill directory:
   ```bash
   cp <skill-dir>/assets/songs/* <skill-dir>/
   ```
   This includes a ready-to-use demo song: **十年 (陈奕迅)** with vocal, upper and lower accompaniment files.
3. **Start the server**:
   ```bash
   node <skill-dir>/server.mjs
   ```
4. Open `http://localhost:3098` in browser
5. Enter NuwaAI credentials (if not pre-configured)
6. Pick a song and start singing!

## Included Example Song

The skill ships with one demo song in `assets/songs/`:
- `十年高潮上清唱.wav` — vocal (a cappella)
- `十年高潮上伴奏.MP3` — upper half accompaniment
- `十年高潮下伴奏.MP3` — lower half accompaniment

Copy them to the skill root directory to use. The song "十年" is pre-registered in `server.mjs`.

## NuwaAI Integration

Uses `humanctrl` WebSocket with ASR enabled. Avatar control message format:
```json
{
  "type": "avatar",
  "data": {
    "content": "",
    "audio": {
      "segment": 0,
      "speech": "<base64 PCM>",
      "music": "<base64 PCM>"
    }
  }
}
```

- `speech`: Vocal-only PCM driving lip-sync (≤10KB per chunk)
- `music`: Same as speech for a cappella mode
- `segment`: Chunk index, -1 = last chunk
- Audio: 16kHz mono PCM, base64 encoded

## Features

- 🎤 Avatar lip-sync singing via NuwaAI humanctrl
- 🎵 Synchronized accompaniment playback
- 🗣️ ASR voice capture for user singing
- 🎯 Fun battle scoring system
- 🎁 Blind box rewards
- ⏸️ Interruptible speech (not during singing)
- 📱 Responsive web interface

## Requirements

- Node.js 18+
- FFmpeg (for audio → PCM conversion)
- NuwaAI account with avatar
- Modern browser (WebRTC + microphone)

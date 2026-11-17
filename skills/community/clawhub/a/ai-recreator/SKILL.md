---
name: ai-recreator
slug: ai-recreator
version: 1.0.1
description: "AI video repurposing × digital human dubbing web tool. Paste a Douyin/TikTok link → wait 3 minutes → get a digital human video that looks like YOU said it. 5-step pipeline: download → transcribe → rewrite → TTS → digital human."
when_to_use: "When users want to: repurpose short video content into their own talking-head version, paste a Douyin/TikTok link to generate a digital human video, extract and AI-rewrite video captions with voiceover, or deploy a digital human dubbing web service."
trigger_terms:
  - video repurpose
  - digital human
  - talking head
  - short video rewrite
  - AI video generation
  - digital human dubbing
  - douyin to digital human
  - video rewriting
  - build digital human tool
  - AI recreation
  - talking head video
  - caption rewrite dubbing
---

# AI Video Repurpose × Digital Human Dubbing

## Core Scenario

> Paste a Douyin/TikTok short video link → wait ~3 minutes → get a video that looks like YOU said it

## Architecture

```
Paste link → [Download] → [Transcribe] → [AI Rewrite] → [TTS] → [Digital Human] → Deliver
    yt-dlp       Whisper       LLM        edge-tts     SadTalker
```

## Quick Start

### 🏃 3-step setup

```bash
cd ai-recreator

# 1️⃣ Install dependencies
pip install -r backend/requirements.txt

# 2️⃣ Configure (at minimum set your API Key)
cp backend/.env.example backend/.env  # then edit .env with your key

# 3️⃣ Start
cd backend && uvicorn main:app --host 0.0.0.0 --port 8080
```

Open http://localhost:8080 in your browser → paste a Douyin link → click "Start" → wait 3 minutes → get your digital human video.

## Prerequisites

| Dependency | Purpose | Install |
|-----------|---------|---------|
| FFmpeg | Audio/video processing | `apt install ffmpeg` or `brew install ffmpeg` |
| yt-dlp | Short video download | `pip install yt-dlp` (included in requirements) |
| PyTorch | Whisper/SadTalker inference | See official docs (CPU works but is slower) |

## 5-Step Pipeline

### Step 1: Download (`modules/downloader.py`)
- Downloads video & extracts audio via `yt-dlp` from Douyin/TikTok/Kuaishou
- Auto-detects platform; 120s timeout, 3 retries
- Supports proxy (`DOWNLOAD_PROXY` env) for cloud server bypass

### Step 2: Transcribe (`modules/transcriber.py`)
- Whisper speech-to-text, default `base` model
- Model cascade: tiny → base → small → medium → large
- Cached per task to avoid re-transcription

### Step 3: AI Rewrite (`modules/rewriter.py`)
- LLM rewrites short-video copy into natural, personal speech
- Strips influencer buzzwords ("hey guys", "OMG", etc.)
- Supports custom style prompts
- Falls back to rule-based rewrite when no API Key is set

### Step 4: TTS Synthesis (`modules/tts_engine.py`)
- Default edge-tts (free, fast, great Chinese)
- Supports MeloTTS / CosyVoice switching
- Auto-splits long text + ffmpeg concatenation

### Step 5: Digital Human (`modules/digital_human.py`)
- Default SadTalker: single photo → talking-head video
- Falls back to audio+placeholder video when SadTalker unavailable
- Wav2Lip interface reserved

## API Reference

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/tasks` | Submit a creation task (video URL) |
| POST | `/api/tasks/upload-video` | Upload a video file directly (skip download) |
| POST | `/api/tasks/upload-audio` | Upload an audio file directly (skip download & transcribe) |
| GET | `/api/tasks/{task_id}` | Query task progress |
| POST | `/api/tasks/{task_id}/confirm` | Confirm rewritten text → start TTS |
| POST | `/api/tasks/{task_id}/upload-video` | Upload reference video for lip-sync |
| GET | `/api/output/{task_id}/{filename}` | Download generated video |
| GET | `/` | Web UI |

### Submit a task (URL)

```bash
curl -X POST http://localhost:8080/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "video_url": "https://www.douyin.com/video/xxxxx",
    "custom_prompt": "Make it more casual and humorous",
    "tts_voice": "zh-CN-XiaoxiaoNeural"
  }'
```

### Upload a video file (skip download)

```bash
curl -X POST http://localhost:8080/api/tasks/upload-video \
  -F "file=@/path/to/your/video.mp4" \
  -F "custom_prompt=Use a friendly tone"
```

## Configuration (`.env`)

| Variable | Default | Description |
|----------|---------|-------------|
| OPENAI_API_KEY | "" | For AI rewriting; leave empty for rule-based fallback |
| OPENAI_BASE_URL | "" | Compatible OpenAI third-party API |
| OPENAI_MODEL | gpt-4o-mini | Model for rewrites |
| WHISPER_MODEL | base | tiny/base/small/medium/large |
| TTS_ENGINE | edge | edge/melotts/cosyvoice |
| DIGITAL_HUMAN_MODE | sadtalker | sadtalker/wav2lip/api |
| DOWNLOAD_PROXY | "" | HTTP proxy for download (e.g. http://127.0.0.1:7890) |

## File Structure

```
ai-recreator/
├── README.md                 # Project overview
├── SKILL.md                  # This skill definition
├── skill-card.md             # ClawHub listing card
├── .gitignore                # Git ignore rules
├── cookies.example.txt       # Cookie template (optional)
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Config management
│   ├── models.py            # Data models
│   ├── task_manager.py      # Task queue manager
│   ├── pipeline.py          # Pipeline orchestrator
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Config template (copy to .env)
│   ├── assets/              # Static assets
│   │   └── default_avatar.png
│   └── modules/
│       ├── file_handler.py  # File upload handling
│       ├── downloader.py    # Video downloader
│       ├── transcriber.py   # Speech-to-text
│       ├── rewriter.py      # AI text rewriting
│       ├── tts_engine.py    # Text-to-speech
│       └── digital_human.py # Digital human generator
├── frontend/
│   ├── index.html           # Single-page Web UI
│   └── static/              # Static assets
├── references/
│   ├── faq.md               # FAQ (20 questions)
│   ├── anti-patterns.md     # Anti-patterns guide
│   ├── quickstart.md        # Quick start guide
│   └── privacy.md           # Privacy & data handling
└── data/
    ├── downloads/           # Download cache
    ├── audio/               # TTS output
    ├── transcripts/         # Transcription results
    ├── rewrites/            # Rewrite results
    ├── output/              # Final videos
    └── temp/                # Temporary files
```

## Capability Boundaries

### ✅ What it does well

1. **Short video repurposing** - Extract speech from Douyin/TikTok/Kuaishou links, AI-rewrite into personal expression
2. **Digital human talking-head generation** - Voice + photo → lip-synced talking-head video
3. **Style transformation** - Removes influencer lingo, keeps core message
4. **Multi-engine TTS** - Supports edge-tts / MeloTTS / CosyVoice
5. **Real-time progress tracking** - Live 5-step pipeline status
6. **Graceful degradation** - Falls back to rule rewriting (no API Key) or placeholder video (no GPU)

### ⚠️ Requires user-provided assets

1. **Voice cloning** - Requires voice sample recordings (future release)
2. **HD digital human (>720p)** - Needs paid API (HeyGen/D-ID)
3. **Lip-sync with original video** - Needs Wav2Lip reference video (currently SadTalker single-image mode)
4. **Custom digital human avatar** - User needs to provide a front-facing half-body photo
5. **Non-short-video platform URLs** - Platforms other than Douyin/TikTok/Kuaishou need extra testing

### ❌ Out of scope

1. **Batch processing** - Single link per submission (submit multiple times for batch)
2. **Video editing/cutting** - Only extracts audio; no video editing
3. **Watermark removal** - Operates on audio track only
4. **Deepfake/face swap** - No face-swapping tech; lip-sync only
5. **Live stream processing** - No live stream or m3u8 support
6. **Original content generation** - Not responsible for factual accuracy of rewrites

### 🔒 Security & Privacy

1. **URL filtering** - Only http/https allowed; rejects file:// protocol injection
2. **Timeout control** - Each step has guard timeouts (120s~400s)
3. **Graceful degradation** - Handles missing API Key / GPU without crashing
4. **File cleanup** - `data/temp/` cleaned after task completion
5. **Data isolation** - Audio & transcripts stored per task_id
6. **API Key security** - Read from `.env`, never logged
7. **Lightweight dependencies** - All AI capabilities optional; default runs fully local

### 👤 Audience

| User Type | How to Use |
|-----------|-----------|
| **Individual creators** | Deploy locally, paste links via Web UI |
| **Developers** | Integrate via REST API |
| **Teams** | Deploy on internal server, share across members |
| **Non-technical users** | Use a deployed instance (if available) |

## Reference Docs

- `references/faq.md` — 20 FAQs + edge cases
- `references/anti-patterns.md` — 7 common anti-patterns + fixes
- `references/quickstart.md` — 10-second quick start
- `references/privacy.md` — Privacy & data handling

## Version History

- **v1.0.1** (2026-07-29): Fixed .env startup crash; added DOWNLOAD_PROXY; added --js-runtimes node; added upload-audio/upload-video endpoints; privacy docs & config template
- **v1.0.0** (2026-07-28): Initial release. 5-step pipeline, Web UI, REST API, multi-engine TTS, SadTalker digital human, graceful degradation

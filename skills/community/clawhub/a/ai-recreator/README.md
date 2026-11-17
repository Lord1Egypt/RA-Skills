# AI Video Repurpose × Digital Human Dubbing Web Tool

## Core Scenario

> Paste a Douyin/TikTok link → wait ~3 minutes → get a video that looks like YOU said it

## Architecture

```
Paste link → [Download] → [Transcribe] → [AI Rewrite] → [TTS] → [Digital Human] → Deliver
    yt-dlp       Whisper       LLM        edge-tts     SadTalker
     3-8s          ~30s          ~5s         ~10s        ~60-90s
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start
cd backend && uvicorn main:app --host 0.0.0.0 --port 8080

# Open browser
open http://localhost:8080
```

## Prerequisites

- FFmpeg
- yt-dlp (auto-installed)
- PyTorch + CUDA (optional, accelerates Whisper)

## Configuration

Edit `backend/.env`:

```
OPENAI_API_KEY=***           # For AI rewriting
OPENAI_BASE_URL=             # Optional, OpenAI-compatible API
DIGITAL_HUMAN_MODE=open      # open | api (local/cloud)
TTS_ENGINE=melotts           # melotts | cosyvoice | edge
WHISPER_MODEL=base           # tiny/base/small/medium/large
DOWNLOAD_PROXY=              # HTTP proxy for download (bypass IP blocks)
```

## Supported TTS Engines

| Engine | Quality | Speed | Chinese | Install |
|--------|---------|-------|---------|---------|
| edge-tts | ★★★ | Fast | ✅ | pip install edge-tts |
| MeloTTS | ★★★★ | Medium | ✅ | Extra install |
| CosyVoice | ★★★★★ | Slow | ✅ | Extra install |

## Digital Human Modes

| Mode | Solution | Quality | Notes |
|------|----------|---------|-------|
| open | Wav2Lip + GFPGAN | ★★★ | Lip-sync, needs reference video |
| open | SadTalker | ★★★★ | Single image, no reference needed |
| api | HeyGen | ★★★★★ | Cloud API, needs Key |
| api | D-ID | ★★★★★ | Cloud API, needs Key |

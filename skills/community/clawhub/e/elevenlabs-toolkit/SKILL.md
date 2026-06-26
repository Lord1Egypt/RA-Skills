---
name: elevenlabs-toolkit
description: ElevenLabs voice API integration — TTS, sound effects, music generation, speech-to-text, voice isolation, and streaming. Use when building voice-enabled apps, generating narration, creating audio content, or transcribing speech. Requires ELEVENLABS_API_KEY.
version: 1.0.2
metadata:
  {
      "openclaw": {
            "emoji": "\ud83c\udf99\ufe0f",
            "requires": {
                  "bins": [],
                  "env": [
                        "ELEVENLABS_API_KEY"
                  ]
            },
            "primaryEnv": "ELEVENLABS_API_KEY",
            "network": {
                  "outbound": true,
                  "reason": "Calls ElevenLabs API (api.elevenlabs.io) for TTS, SFX, music generation, STT, and voice operations."
            },
            "security_notes": "base64 used for encoding audio binary responses from ElevenLabs API. UploadFile is FastAPI's multipart type for audio input to STT endpoint. 'system prompt' refers to ElevenLabs agent system prompt configuration field — not a prompt injection vector."
      }
}
---

# ElevenLabs Toolkit

Programmatic access to all 7 ElevenLabs API capabilities via FastAPI endpoints or standalone Python functions.

---

## When to Use This / When NOT to Use This

**Use ElevenLabs when:**
- Generating high-quality narration audio for videos, demos, or content (especially with Rachel or a consistent character voice)
- Building a voice-enabled app that needs streamed speech in real-time
- Transcribing audio files (STT/Scribe)
- Generating ambient sound effects or background music from text descriptions
- Isolating clean voice from a noisy recording

**Do NOT use ElevenLabs when:**
- You need fast/cheap TTS with no quality bar — use **local TTS instead** (see below)
- You're offline or the API key isn't available
- You're generating large volumes of test audio and don't want to burn character quota

### ElevenLabs vs Local TTS (kokoro / chatterbox)

| Criteria | ElevenLabs | Local TTS (kokoro/chatterbox) |
|---|---|---|
| Voice quality | ★★★★★ — natural, expressive | ★★★ — good but robotic edges |
| Cost | Chars deducted from monthly quota | Free, unlimited |
| Latency | ~300–800ms API round-trip | ~50–200ms local inference |
| Voice consistency | Named voices (Rachel etc.) persist | Model-dependent |
| Offline use | ❌ Requires internet + API key | ✅ Fully local |
| Best for | Final narration, published content | Drafts, testing, high-volume batch |

**Rule of thumb:** Use ElevenLabs for anything that will be seen/heard by a user. Use local TTS for drafts, tests, and volume work.

---

## Capabilities

| Tool | Endpoint | What It Does |
|---|---|---|
| Voices | GET /api/voices | Browse available voices with metadata |
| TTS | POST /api/voice/tts | Batch text-to-speech (any voice, any language) |
| TTS Stream | WS /api/voice/stream | Real-time WebSocket TTS streaming |
| Sound Effects | POST /api/voice/sfx | Generate ambient audio from text prompts |
| Music | POST /api/voice/music | Generate background music from descriptions |
| STT (Scribe) | POST /api/voice/stt | Transcribe audio with language detection |
| Voice Isolation | POST /api/voice/isolate | Extract clean voice from noisy audio |

---

## Known Voice IDs

These are confirmed voices used in OpenClaw workflows. Always prefer these over browsing the full list:

| Voice | Voice ID | Best For |
|---|---|---|
| **Rachel** | `21m00Tcm4TlvDq8ikWAM` | Default narration — clear, warm, American English |
| Adam | `pNInz6obpgDQGcFmaJgB` | Male narration, authoritative tone |
| Domi | `AZnzlk1XvdvUeBnXmlld` | Energetic, conversational |
| Bella | `EXAVITQu4vr4xnSDxMaL` | Soft, gentle narration |

> **Default for all narration tasks:** Use Rachel (`21m00Tcm4TlvDq8ikWAM`) unless explicitly specified otherwise.

To get the full current list from the API:
```bash
curl -s -H "xi-api-key: $ELEVENLABS_API_KEY" https://api.elevenlabs.io/v1/voices | python3 -m json.tool
```

---

## Quick Start

```python
import httpx

BASE = "http://localhost:8000"  # Your FastAPI app
KEY = os.environ["ELEVENLABS_API_KEY"]

# Get voices
voices = httpx.get(f"{BASE}/api/voices").json()

# Generate speech
audio = httpx.post(f"{BASE}/api/voice/tts", json={
    "text": "Hello world",
    "voice_id": voices[0]["voice_id"],
    "model_id": "eleven_multilingual_v2"
}).content  # Returns raw audio bytes

# Generate sound effects
sfx = httpx.post(f"{BASE}/api/voice/sfx", json={
    "prompt": "ocean waves on a quiet beach at night"
}).content
```

---

## Audio Output Format

**TTS and SFX endpoints return raw audio bytes** (not base64, not JSON).

```python
# Correct: .content gives you bytes
audio_bytes = response.content  # type: bytes

# Save to file
with open("output.mp3", "wb") as f:
    f.write(audio_bytes)

# The file format is MP3 by default
# File size estimate: ~1 MB per minute of speech at standard quality
```

**What you get back from each endpoint:**

| Endpoint | Response type | How to handle |
|---|---|---|
| POST /api/voice/tts | `bytes` (MP3) | Write directly to `.mp3` file |
| POST /api/voice/sfx | `bytes` (MP3) | Write directly to `.mp3` file |
| POST /api/voice/music | `bytes` (MP3) | Write directly to `.mp3` file |
| POST /api/voice/stt | `JSON` | `{"text": "transcription...", "language": "en"}` |
| POST /api/voice/isolate | `bytes` (MP3) | Write directly to `.mp3` file |
| GET /api/voices | `JSON` | List of `{voice_id, name, labels, ...}` |

---

## Voice Selection Guide

- **English only:** Use `eleven_turbo_v2_5` — faster, no accent bleed
- **Multilingual:** Use `eleven_multilingual_v2` — supports 29 languages
- **Accent warning:** Multilingual model can bleed accents across languages. If an English voice sounds Japanese, switch to turbo.

---

## Quota Management

ElevenLabs charges per character for TTS. Key patterns:
- Cache aggressively — identical text + voice = identical audio
- Use `prompt-cache` skill for SHA-256 dedup before calling TTS
- A 6-scene children's story ≈ 2,000 characters
- Free tier: 10k chars/month. Starter: 30k. Creator: 100k.

---

## Integration

Copy `scripts/elevenlabs_api.py` into your FastAPI app and mount the router:

```python
from elevenlabs_api import router
app.include_router(router)
```

Set `ELEVENLABS_API_KEY` in your environment. All endpoints handle errors gracefully with proper HTTP status codes.

---

## What If the FastAPI Server Isn't Running?

The Quick Start examples assume `http://localhost:8000` is live. If it's not:

```python
# Check if server is up before calling
import httpx

try:
    httpx.get("http://localhost:8000/health", timeout=2.0)
except httpx.ConnectError:
    # Server is not running — start it first
    import subprocess
    subprocess.Popen(["uvicorn", "elevenlabs_api:app", "--port", "8000"])
    import time; time.sleep(2)  # Give it a moment to bind
```

Or call the ElevenLabs API directly without the FastAPI wrapper — the `scripts/elevenlabs_api.py` functions are importable standalone:

```python
from elevenlabs_api import generate_tts  # if the module exposes standalone functions
```

---

## Error Handling: API Key and Rate Limits

**Missing API key:**
```
httpx.HTTPStatusError: 401 Unauthorized
{"detail": {"status": "unauthorized", "message": "Invalid API key"}}
```
→ Check `ELEVENLABS_API_KEY` is set: `echo $ELEVENLABS_API_KEY`
→ Retrieve from 1Password: `op read "op://OpenClaw/ElevenLabs API Credentials/credential"`

**Rate limited (429):**
```json
{"detail": {"status": "too_many_requests", "message": "Too many requests"}}
```
→ Wait and retry with exponential backoff. ElevenLabs rate limits are per-minute on the free/starter tiers.
→ On Creator tier and above, limits are much higher — check your tier in the ElevenLabs dashboard.

**Quota exhausted:**
```json
{"detail": {"status": "quota_exceeded", "message": "Quota exceeded"}}
```
→ Character quota for the month is used up. Either wait for monthly reset or upgrade tier.
→ Check current usage: `curl -s -H "xi-api-key: $KEY" https://api.elevenlabs.io/v1/user/subscription`

---

## Files

- `scripts/elevenlabs_api.py` — FastAPI router with all 7 endpoints

---

## Common Mistakes

1. **Treating the response as JSON when it's bytes**
   - ❌ `response.json()` on a TTS call → `JSONDecodeError`
   - ✅ `response.content` → raw bytes, then write to `.mp3`

2. **Using the wrong voice ID**
   - ElevenLabs voice IDs are opaque strings, not names
   - ❌ `"voice_id": "Rachel"` → 404 or wrong voice
   - ✅ `"voice_id": "21m00Tcm4TlvDq8ikWAM"` (Rachel's actual ID)

3. **Calling TTS for large batches without caching**
   - Identical text+voice always produces identical audio — don't re-generate what's already cached
   - Burns character quota unnecessarily

4. **Using multilingual model for English-only content**
   - `eleven_multilingual_v2` is slower and can produce accent artifacts on English-only text
   - Use `eleven_turbo_v2_5` for English-only work

5. **Not checking the FastAPI server is running before calling**
   - `httpx.ConnectError` is confusing if you forget the local server dependency
   - Add a health check or start-server step before calling endpoints

---

## Security Notes

This skill uses patterns that may trigger automated security scanners:
- **base64**: Used for encoding audio/binary data in API responses (standard practice for media APIs)
- **UploadFile**: FastAPI's built-in file upload parameter for STT/voice isolation endpoints
- **"system prompt"**: Refers to configuring agent instructions, not prompt injection

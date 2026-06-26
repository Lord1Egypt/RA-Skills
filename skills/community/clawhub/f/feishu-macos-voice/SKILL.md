---
name: feishu-voice
description: Send voice/audio messages to Feishu (Lark) chats using TTS. Automatically uses OpenAI TTS (gpt-4o-mini-tts) if OPENAI_API_KEY is set, otherwise falls back to macOS `say`. Transcodes to opus and delivers as a native Feishu audio message. Use when asked to "send a voice message", "发语音", "用语音说", or any request to send audio to Feishu/Lark.
metadata:
  openclaw:
    requires:
      bins:
        - ffmpeg
        - ffprobe
        - curl
        - python3
      bins_conditional:
        - bin: say
          condition: OPENAI_API_KEY not set (macOS fallback TTS)
      config:
        - path: ~/.openclaw/openclaw.json
          keys:
            - channels.feishu.appId
            - channels.feishu.appSecret
          reason: Feishu bot credentials (app_id + app_secret) for API authentication
      env_optional:
        - name: OPENAI_API_KEY
          reason: If set, uses OpenAI TTS (gpt-4o-mini-tts) instead of macOS say
      platform: macOS
---

# Feishu Voice Message

Send voice messages to Feishu (Lark) via TTS → opus → Feishu API.

## TTS Engine Priority

| Priority | Engine | Condition |
|----------|--------|-----------|
| 1st | **OpenAI TTS** (`gpt-4o-mini-tts`) | `OPENAI_API_KEY` env var is set |
| 2nd | **macOS `say`** (fallback) | No `OPENAI_API_KEY` |

## Prerequisites

- `ffmpeg` with libopus: `brew install ffmpeg`
- Feishu bot `app_id` + `app_secret` — read from `~/.openclaw/openclaw.json` → `channels.feishu`
- **OpenAI TTS (optional):** `OPENAI_API_KEY` environment variable

## Quick Send

```bash
scripts/feishu-voice.sh <text> <receive_id> [receive_id_type] [voice] [openai_instructions]
```

Examples:
```bash
# Auto-selects engine based on OPENAI_API_KEY
scripts/feishu-voice.sh "今天天气不错！" ou_xxxxxxxx open_id

# OpenAI TTS with Taiwan accent instructions
scripts/feishu-voice.sh "你好！" ou_xxxxxxxx open_id shimmer "Speak with a Taiwan Mandarin accent"

# macOS TTS with specific voice (when no OPENAI_API_KEY)
scripts/feishu-voice.sh "会议提醒" oc_xxxxxxxx chat_id Meijia

# Send to a group
scripts/feishu-voice.sh "下午三点开会" oc_xxxxxxxx chat_id
```

## Voice Options

### OpenAI TTS voices
| Voice | Character |
|-------|-----------|
| `shimmer` | Warm, expressive (recommended for Chinese) |
| `nova` | Friendly, natural |
| `alloy` | Neutral |
| `echo` | Clear |
| `fable` | Expressive |
| `onyx` | Deep |

Use `openai_instructions` (5th arg) for accent/style control, e.g.:
- `"Speak with a Taiwan Mandarin accent"`
- `"Use a warm and friendly tone"`

### macOS `say` voices (fallback)
| Voice | Language | Notes |
|-------|----------|-------|
| `Tingting` | 普通话 zh_CN | Recommended default |
| `Meijia` | 台湾 zh_TW | Taiwan accent |
| `Sinji` | 粤语 zh_HK | Cantonese |

List all: `say -v '?'`

## Manual Step-by-Step

### 1. Get credentials

```bash
APP_ID=$(python3 -c "import json; d=json.load(open('$HOME/.openclaw/openclaw.json')); print(d['channels']['feishu']['appId'])")
APP_SECRET=$(python3 -c "import json; d=json.load(open('$HOME/.openclaw/openclaw.json')); print(d['channels']['feishu']['appSecret'])")
```

### 2a. TTS → mp3 (OpenAI)

```bash
curl -s -X POST "https://api.openai.com/v1/audio/speech" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o-mini-tts","input":"要说的文字","voice":"shimmer","response_format":"mp3"}' \
  -o /tmp/voice.mp3
```

### 2b. TTS → AIFF (macOS fallback)

```bash
say -v "Tingting" "要说的文字" -o /tmp/voice.aiff
```

### 3. Transcode to opus ⚠️ All three flags required

```bash
# From mp3 (OpenAI)
ffmpeg -y -i /tmp/voice.mp3 -acodec libopus -ac 1 -ar 16000 /tmp/voice.opus

# From aiff (macOS)
ffmpeg -y -i /tmp/voice.aiff -acodec libopus -ac 1 -ar 16000 /tmp/voice.opus
```

| Flag | Value | Why |
|------|-------|-----|
| `-acodec libopus` | opus codec | Feishu only accepts opus |
| `-ac 1` | mono | Required by Feishu |
| `-ar 16000` | 16 kHz | Required by Feishu |

### 4. Get duration in **milliseconds**

```bash
DURATION_MS=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 /tmp/voice.opus \
  | python3 -c "import sys; print(round(float(sys.stdin.read().strip()) * 1000))")
```

⚠️ `duration` param is **milliseconds**, not seconds. Wrong unit → 0s display.

### 5. Get tenant_access_token

```bash
TENANT_TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['tenant_access_token'])")
```

### 6. Upload file

```bash
FILE_KEY=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
  -H "Authorization: Bearer $TENANT_TOKEN" \
  -F "file_type=opus" \
  -F "file_name=voice.opus" \
  -F "duration=$DURATION_MS" \
  -F "file=@/tmp/voice.opus" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['file_key'])")
```

⚠️ `file_type` must be `opus`, **not** `audio`.

### 7. Send audio message

```bash
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TENANT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id\":\"$RECEIVE_ID\",\"msg_type\":\"audio\",\"content\":\"{\\\"file_key\\\":\\\"$FILE_KEY\\\"}\"}"
```

## Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Duration shows 0s | `duration` unit is seconds, not ms | Multiply by 1000 |
| Upload fails 400 | `file_type=audio` used | Change to `opus` |
| Silent/tiny AIFF | Voice pack not installed | System Settings → Accessibility → Spoken Content → download voice |
| Garbled audio | Missing `-ac 1 -ar 16000` | Add both ffmpeg flags |
| OpenAI 401 error | `OPENAI_API_KEY` invalid or not set | Check env var; falls back to macOS say |

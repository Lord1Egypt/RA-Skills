---
name: feishu-voice-bubble
description: |
  Send native voice bubble messages (语音气泡) in Feishu/Lark chats using Edge TTS.
  Converts text to opus audio via Microsoft Edge TTS (free, no API key needed), then sends
  as Feishu audio message type which renders as a native voice bubble — not a file attachment.
  Supports 30+ Chinese voices, 400+ voices across all languages, adjustable speech rate and
  pitch, and auto-splitting for long text. Use when: user asks to send voice message, voice
  bubble, 语音, 发语音, TTS in Feishu, or wants audio replies in Feishu chats.
---

# Feishu Voice Bubble

Send native voice bubble messages in Feishu using Edge TTS + opus format.

## Why This Exists

Feishu bot API only renders voice bubbles for `audio` message type with opus format.
Standard TTS outputs mp3 → Feishu shows it as a file attachment, not a voice bubble.
This skill: Edge TTS → opus → Feishu audio → native voice bubble.

## Prerequisites

```bash
npm install node-edge-tts
```

No API keys required. Edge TTS is free.

## Usage

### Basic

```bash
node scripts/gen_voice.js "你好世界" output.opus
```

### With Options

```bash
node scripts/gen_voice.js "播报内容" output.opus --voice zh-CN-YunxiNeural --rate +15% --pitch -5%
```

### Long Text Auto-Split

```bash
node scripts/gen_voice.js "很长的文本..." output.opus --split 500
```

Produces `output_1.opus`, `output_2.opus`, etc. Split at sentence boundaries.

### Send to Feishu

```json
{ "action": "send", "filePath": "output.opus" }
```

The `.opus` extension triggers Feishu's native audio message type automatically.

## Arguments

| Arg | Description | Default |
|-----|-------------|---------|
| `<text>` | Text to convert | required |
| `<output>` | Output .opus path | required |
| `--voice` | Edge TTS voice name | zh-CN-XiaoxiaoNeural |
| `--rate` | Speech rate (+20%, -10%) | +0% |
| `--pitch` | Pitch adjust (+5%, -5%) | +0% |
| `--split` | Auto-split at N chars | 0 (disabled) |

## Chinese Voices

| Voice | Gender | Style |
|-------|--------|-------|
| zh-CN-XiaoxiaoNeural | F | Warm, versatile (default) |
| zh-CN-XiaoyiNeural | F | Gentle, storytelling |
| zh-CN-YunxiNeural | M | Young, energetic |
| zh-CN-YunjianNeural | M | Broadcast, professional |
| zh-CN-YunyangNeural | M | News anchor, authoritative |
| zh-CN-liaoning-XiaobeiNeural | F | Northeastern dialect |
| zh-CN-shaanxi-XiaoniNeural | F | Shaanxi dialect |

## How It Works

1. Edge TTS converts text → `webm-24khz-16bit-mono-opus`
2. Saved as `.opus` file
3. Feishu plugin detects `.opus` → uploads as `opus` type → sends as `audio` message
4. Feishu client renders native voice bubble with play button

## Limitations

- Requires internet (Microsoft hosted service)
- No SLA (free public service)
- ~10 min max audio per request
- `node-edge-tts` must be installed in the working directory or globally

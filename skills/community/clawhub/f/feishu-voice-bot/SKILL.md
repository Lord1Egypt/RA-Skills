---
name: feishu-voice-bubble
description: |
  Send native voice bubbles via Feishu using edge-tts + ffmpeg.
  Converts text to OGG/Opus audio and sends as a playable blue voice bubble.
  Use when: (1) User sends a voice message and expects voice reply. (2) User says "语音回复" or "用语音". (3) Any TTS/voice output to Feishu.
  Requires: edge-tts skill (scripts/tts-converter.js), ffmpeg, message tool with channel=feishu.
---

# Feishu Voice Bubble

Send native voice bubbles (蓝色可播放气泡) via Feishu using bot identity.

## Workflow

```
text → edge-tts (mp3) → ffmpeg (ogg/opus) → message tool (media=) → 原生气泡
```

## Quick Usage

```bash
# One-liner via the helper script
node scripts/voice-bubble.mjs "你好陛下" --voice zh-CN-XiaoxiaoNeural
```

Or use the message tool directly after generating the audio:

```bash
# Step 1: Generate
cd ~/.openclaw/workspace/skills/edge-tts/scripts
node tts-converter.js "文本" --voice zh-CN-XiaoxiaoNeural --output /tmp/voice.mp3

# Step 2: Convert
ffmpeg -i /tmp/voice.mp3 -c:a libopus -b:a 32k /tmp/voice.ogg -y

# Step 3: Send via message tool
message(action=send, channel=feishu, target=<open_id_or_chat_id>, media=/tmp/voice.ogg)
```

## Supported Voices

| 语言 | 语音 ID | 特点 |
|------|---------|------|
| 中文 | zh-CN-XiaoxiaoNeural | 女声，自然 |
| 中文 | zh-CN-YunxiNeural | 男声，自然 |
| 英文 | en-US-AriaNeural | 女声 |
| 英文 | en-US-GuyNeural | 男声 |

Full list: `node ~/.openclaw/workspace/skills/edge-tts/scripts/tts-converter.js --list-voices`

## Notes

- **无需用户 OAuth** — 机器人身份 + `message` tool + `media=` 即可发送原生气泡
- **格式** — 飞书要求 OGG/Opus 格式，edge-tts 输出 MP3，需 ffmpeg 转换
- **临时文件** — 生成的音频存于 `/tmp/`，不会自动清理
- **中文默认** — 未指定 voice 时使用 `zh-CN-XiaoxiaoNeural`

---
name: chinese-tts
description: Generate Chinese TTS audio and send as Feishu voice message. Use when user asks for voice/audio/语音/播报/朗读 in Chinese, or when sending audio messages via Feishu.
---

# Chinese TTS Voice Generation

Generate natural Chinese speech using Microsoft Edge TTS and send as Feishu voice messages.

## Quick Reference

```bash
# 1. Generate MP3
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 /home/clawpi/.local/bin/edge-tts \
  --voice zh-CN-YunxiNeural \
  --text "你的文本内容" \
  --write-media /tmp/output.mp3

# 2. Convert to Opus
ffmpeg -i /tmp/output.mp3 -c:a libopus -b:a 64k -ar 48000 \
  /home/node/.openclaw/workspace/output.opus -y

# 3. Send via Feishu
message(asVoice=true, contentType="audio/ogg",
        filePath="/home/node/.openclaw/workspace/output.opus",
        filename="output.opus")
```

## Critical Rules

1. **Always set UTF-8 env vars** — System locale is ISO-8859-1, Chinese text will be corrupted without `LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8`
2. **Must use opus format** — Feishu only treats `.opus` as voice messages; MP3/WAV become file attachments
3. **Must send from workspace** — `/tmp` is not in Feishu's `mediaLocalRoots` whitelist; files there fail silently and fall back to plain text
4. **Use ASCII filenames** — Chinese filenames may cause encoding issues in multipart uploads

## Voice Options

| Voice | Gender | Style |
|---|---|---|
| `zh-CN-YunxiNeural` | Male | Natural, warm (recommended) |
| `zh-CN-XiaoxiaoNeural` | Female | Natural, friendly |
| `zh-CN-YunjianNeural` | Male | Authoritative |

## For Long Text

Write text to a file and use `-f` flag:

```bash
echo "长文本内容..." > /tmp/text.txt
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 /home/clawpi/.local/bin/edge-tts \
  --voice zh-CN-YunxiNeural -f /tmp/text.txt --write-media /tmp/output.mp3
```

## Troubleshooting

- **Gibberish audio** → Missing UTF-8 env vars
- **File sent as attachment, not voice** → Not opus format, or not from workspace path
- **Upload fails silently** → File not in `mediaLocalRoots` (use workspace dir)
- **"哈米" instead of "虾米"** → Google TTS (gtts) issue; use edge-tts instead

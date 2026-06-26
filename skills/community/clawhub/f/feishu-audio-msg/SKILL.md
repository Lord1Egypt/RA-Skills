---
name: feishu-audio
description: Send TTS audio as a proper playable audio message (not file attachment) to Feishu chats. Use when asked to send voice messages, TTS audio, speech announcements, or 语音报数 (voice roll calls) to a Feishu group or user. Activates on requests like "send voice message to Feishu", "TTS to Feishu chat", "语音发送", "语音报数", or any task combining text-to-speech with Feishu messaging.
---

# feishu-audio

Send TTS audio to Feishu as a playable audio message (msg_type=audio), not a file attachment.

## Why This Skill Exists

OpenClaw's `message` tool sends audio as a generic file. Feishu requires a two-step API flow to display it as a playable voice message:
1. Upload with `file_type=opus`
2. Send with `msg_type=audio`

## Quick Usage

```bash
bash /root/.openclaw/skills/feishu-audio/scripts/send_audio.sh \
  "要说的内容" \
  "<chat_id or user open_id>" \
  [voice]          # optional, default: zh-CN-XiaoyiNeural
```

**receive_id_type** is always `chat_id`. For group chats use `oc_xxx`; for DMs use `ou_xxx` (open_id).

### Common Voices
| Language | Voice |
|----------|-------|
| Chinese (F) | `zh-CN-XiaoyiNeural` (default) |
| Chinese (M) | `zh-CN-YunxiNeural` |
| English (F) | `en-US-AriaNeural` |
| English (M) | `en-US-GuyNeural` |

## Credentials

Auto-read from `/root/.openclaw/openclaw.json` → `channels.feishu.accounts.main`. No manual setup needed in standard OpenClaw deployments.

## Two-Step API Flow (for custom integrations)

```bash
# Step 1: Upload (file_type=opus is required regardless of actual format)
curl -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file_type=opus" -F "file_name=voice.opus" -F "file=@audio.mp3"
# → returns file_key

# Step 2: Send (msg_type=audio, NOT file)
curl -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"receive_id":"oc_xxx","msg_type":"audio","content":"{\"file_key\":\"...\"}"}' 
```

**Key pitfalls:**
- `file_type` must be `opus` (not `mp3`) or upload returns 234001
- `msg_type` must be `audio` (not `file`) or it shows as attachment

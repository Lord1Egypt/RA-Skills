---
name: Feishu Audio Message
description: Send voice/audio messages to Feishu (Lark) users. Converts audio files to OPUS format and sends as voice message, not file attachment. create by Alex
dependencies: ffmpeg
---

# Feishu Audio Message Skill

This skill enables sending **voice messages** (not file attachments) to Feishu/Lark users via the Open API.

## When to Use

Use this skill when:
- User wants to send a **voice message** to Feishu
- User wants to convert and send audio (MP3, WAV, etc.) as a voice message
- User specifies they want audio message, not file upload

## Requirements

1. **ffmpeg** - Required for audio conversion to OPUS format
2. **Node.js 18+** - For running the send script
3. **Feishu App Credentials**:
   - App ID
   - App Secret
   - Target user's Open ID

## How It Works

1. **Convert audio to OPUS** - Feishu requires audio in OPUS format
2. **Upload audio file** - Upload to Feishu with `file_type: opus` and duration
3. **Send audio message** - Send with `msg_type: audio`

## Usage

### Step 1: Convert Audio to OPUS

```bash
ffmpeg -i input.mp3 -c:a libopus -b:a 32k output.opus
```

### Step 2: Get Audio Duration

```bash
ffprobe -v quiet -show_format -print_format json input.mp3
# Look for "duration" field in output
```

### Step 3: Run the Script

```bash
node scripts/send-voice.mjs \
  --app-id "cli_xxx" \
  --app-secret "xxx" \
  --user-id "ou_xxx" \
  --audio-file "audio.opus" \
  --duration 3480
```

Or use environment variables:
```bash
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
node scripts/send-voice.mjs --user-id "ou_xxx" --audio-file "audio.opus" --duration 3480
```

## API Details

### 1. Get Tenant Access Token
```
POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal
```

### 2. Upload Audio File
```
POST https://open.feishu.cn/open-apis/im/v1/files
Content-Type: multipart/form-data

file_type: opus
file_name: voice.opus
duration: <milliseconds>
file: <binary>
```

### 3. Send Audio Message
```
POST https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id

{
  "receive_id": "ou_xxx",
  "msg_type": "audio",
  "content": "{\"file_key\":\"file_v3_xxx\"}"
}
```

## Important Notes

- Audio **MUST be OPUS format** - MP3/WAV will fail
- Duration is in **milliseconds**
- The app must have **Bot capability** enabled
- Rate limit: 5 QPS per user/chat

## Example Output

```
🎤 开始发送语音消息到飞书...

📁 音频文件: /path/to/voice.opus
⏱️  时长: 3480ms

✅ 获取 Tenant Access Token 成功
✅ 上传语音文件成功, file_key: file_v3_00uh_xxx
✅ 发送语音消息成功!
消息 ID: om_x100b5731827e6ca4b10d48c15dfa3ab

🎉 完成！
```

## Troubleshooting

| Error | Solution |
|-------|----------|
| `file type not support` | Convert to OPUS format |
| `duration is required` | Add duration parameter |
| `permission denied` | Check app has messaging scope |
| `user not found` | Verify user Open ID |

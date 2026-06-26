---
name: feishu-file-upload
description: Upload and send local files to Feishu chats. Requires Feishu app credentials (app_id/app_secret) in ~/.openclaw/openclaw.json. Use when user asks to send/share/upload files (CSV, PDF, Excel, images, ZIP) to Feishu. Supports chat_id (groups), open_id/user_id (users), and email recipients.
version: 1.0.0
metadata:
  openclaw:
    requires:
      config:
        - ~/.openclaw/openclaw.json
      env:
        - OPENCLAW_CHAT_ID
      bins:
        - python3
---

# Feishu File Upload

Upload local files to Feishu Drive and send as file messages to chats or users.

## When to Use

- User asks to "send file", "upload file", or "share file" to Feishu
- Need to share documents (CSV, PDF, Excel, Word) with group or individual
- Bot needs to send files that Feishu's native message API doesn't support directly
- Images/videos: Use `media` parameter in message tool instead (no need for this skill)

## Quick Start

### Send to Group Chat
```bash
python scripts/upload_to_feishu.py /path/to/file.csv oc_xxxxxx --type chat_id
```

### Send to Individual User
```bash
python scripts/upload_to_feishu.py /path/to/file.pdf ou_xxxxxx --type open_id
```

### Send via Email
```bash
python scripts/upload_to_feishu.py /path/to/file.zip user@example.com --type email
```

### Use Environment Variable
```bash
export OPENCLAW_CHAT_ID=oc_xxxxxx
python scripts/upload_to_feishu.py /path/to/file.csv --env
```

## How It Works

1. **Read credentials** from `~/.openclaw/openclaw.json` (channels.feishu.appId/appSecret)
2. **Get tenant access token** from Feishu Auth API
3. **Upload file** to Feishu Drive → returns `file_key`
4. **Send file message** using `file_key` to target chat/user

## Script Usage

### Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `file_path` | Yes | - | Absolute path to local file |
| `receive_id` | Yes* | - | Recipient ID (chat_id, open_id, user_id, or email) |
| `--type` | No | `chat_id` | Recipient type: `chat_id`, `open_id`, `user_id`, `email` |
| `--env` | No | `false` | Get receive_id from `OPENCLAW_CHAT_ID` env var |

*Not required if `--env` is used

### Receive ID Types

| Type | Example | Use Case |
|------|---------|----------|
| `chat_id` | `oc_06a6b40e03e98e41c8aebcbed8b09871` | Group chats (default) |
| `open_id` | `ou_b0f83ea276761ab10ebb3f4f277453b8` | Individual user (recommended) |
| `user_id` | `123456` | Individual user (by user_id) |
| `email` | `user@example.com` | Send to email address |

### Extract Chat ID from Feishu Message

From Feishu message metadata:
```json
{
  "conversation_label": "oc_06a6b40e03e98e41c8aebcbed8b09871"
}
```
→ `receive_id` = `oc_06a6b40e03e98e41c8aebcbed8b09871`, `type` = `chat_id`

From sender info:
```json
{
  "sender_id": "ou_b0f83ea276761ab10ebb3f4f277453b8"
}
```
→ `receive_id` = `ou_b0f83ea276761ab10ebb3f4f277453b8`, `type` = `open_id`

## Prerequisites

- Python 3.6+
- `requests` library: `pip install requests`
- Feishu bot credentials in `openclaw.json`

## Feishu API Permissions

Bot needs these permissions in Feishu Developer Console:

**Required for file upload:**
- `im:resource:upload` - Upload files (preferred)
- OR `im:resource` - Read and upload files

**Required for sending messages:**
- `im:message` - Send messages to chats

### How to Enable Permissions

1. Open Feishu Developer Console: https://open.feishu.cn/app/YOUR_APP_ID/auth
2. Search for `im:resource:upload` or `im:resource`
3. Click "Apply" and enable the permission
4. Wait a few minutes for permission to take effect

**Quick link:** https://open.feishu.cn/app/cli_a94a21db99385bd8/auth?q=im:resource:upload,im:resource

## File Size Limits

- Single file: **30MB** max (Feishu API limit)
- Large files may take longer to upload

## Supported File Types

All file types supported by Feishu Drive:

| Category | Extensions |
|----------|------------|
| Documents | PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX |
| Images | JPG, PNG, GIF, WEBP |
| Archives | ZIP, RAR, 7Z |
| Code/Text | TXT, MD, JSON, CSV, XML, PY, JS |
| Media | MP3, MP4, WAV (auto-converted to OPUS) |

## Error Handling

Script handles:

- Missing credentials → Error message
- File not found → Error message
- Upload failure → API error details
- Send failure → API error details
- Missing permissions → Clear error with fix link

## Testing

```bash
# Test with a small file to a group chat
python scripts/upload_to_feishu.py /tmp/test.txt oc_xxxxxx --type chat_id

# Test sending to yourself (find your open_id from message metadata)
python scripts/upload_to_feishu.py /tmp/test.pdf ou_xxxxxx --type open_id
```

## Troubleshooting

### "Access denied" / "99991672"
- Bot lacks `im:resource:upload` or `im:resource` permission
- Open: https://open.feishu.cn/app/cli_a94a21db99385bd8/auth?q=im:resource:upload,im:resource
- Enable permission and wait a few minutes

### "Bot/User can NOT be out of the chat (230002)"
- Bot is not a member of the target group chat
- Add bot to the chat, or send to a different chat

### "Invalid receive_id"
- Check the ID format matches the type
- `chat_id` starts with `oc_`
- `open_id` starts with `ou_`
- `user_id` is numeric
- `email` must be valid email format

### Upload fails for large files
- Feishu API limit is 30MB
- Compress file or use Feishu Drive web interface for larger files

## Alternative: Manual Upload

If script fails, user can manually:

1. Upload file to Feishu Drive via web/app
2. Share file with the chat
3. Bot can then reference the file

## Security Notes

- Credentials read from `openclaw.json` (local only)
- Token expires after ~2 hours (auto-refreshed each run)
- Files uploaded to Feishu Drive follow Feishu's security policies
- Script does not store or transmit credentials

## Comparison with Message Tool

| Feature | This Skill | Message Tool `media` |
|---------|------------|---------------------|
| Documents (PDF, CSV, etc.) | ✅ Supported | ❌ Not supported |
| Images | ✅ Supported | ✅ Supported (easier) |
| Videos | ✅ Supported | ✅ Supported (easier) |
| File size limit | 30MB | Varies by platform |
| Complexity | 2 API calls | 1 API call |

**Recommendation:** Use `media` parameter for images/videos, use this skill for documents and other files.

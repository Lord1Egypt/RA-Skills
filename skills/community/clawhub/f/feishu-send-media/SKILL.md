---
name: feishu-send-media
description: |
  Send images, files, audio, video and other media to Feishu users or chats. Use when user asks to send, share, or transfer media files via Feishu direct message or group chat.
---

# Feishu Send Media

Send media files (images, documents, audio, video) directly to Feishu users or chats using the `message` tool.

## Sending Media

### Basic File Send

Use the `message` tool with `action: send` and `path` parameter:

```json
{
  "action": "send",
  "target": "ou_xxx",  // user open_id or chat_id
  "path": "/path/to/file.pdf"
}
```

**Supported types:**
- Images: `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`
- Documents: `.doc`, `.docx`, `.pdf`, `.txt`, `.rtf`
- Audio: `.mp3`, `.wav`, `.m4a`
- Video: `.mp4`, `.mov`

**Parameters:**
- `target`: User `open_id` (e.g., `ou_3ac66d1ad7b8c1xxxxxxxxxxxxxxs`) or chat ID
- `path`: Absolute path to local file
- Optional `filename`: Override display name

### Sending to Group Chats

Use chat_id as target:

```json
{
  "action": "send",
  "target": "oc_xxx",  // group chat ID
  "path": "/path/to/file.pdf"
}
```

### Inline Images

For images to display inline in the message (not as attachments), use the `image` parameter with base64:

```json
{
  "action": "send",
  "target": "ou_xxx",
  "image": "data:image/png;base64,..."
}
```

## High-Reliability Workflow (Recommended)

**Follow these steps exactly for maximum success rate:**

### Step 1: Copy file to workspace (with deduplication)

```bash
# Extract filename from source path
filename=$(basename "/source/path/to/file.png")

# Copy to workspace (overwrite if exists)
cp -f "/source/path/to/file.png" "~/.openclaw/workspace/${filename}"

# Verify copy succeeded
if [ ! -f "~/.openclaw/workspace/${filename}" ]; then
  echo "ERROR: File copy failed"
  exit 1
fi
```

**Why overwrite (-f):** Ensures fresh copy every time, avoids stale file issues.

### Step 2: Get absolute path and validate

```bash
# Get absolute path
abs_path=$(cd ~/.openclaw/workspace && pwd)/${filename}

# Validate file exists and is readable
if [ ! -r "$abs_path" ]; then
  echo "ERROR: File not readable: $abs_path"
  exit 1
fi

# Log for debugging
echo "Sending: $abs_path"
```

### Step 3: Send with message tool

```json
{
  "action": "send",
  "target": "ou_xxx",
  "path": "/Users/casia/.openclaw/workspace/filename.png"
}
```

### Step 4: Verify response

Check tool response:
- ✅ Success: `"messageId"` field present
- ❌ Failure: `"error"` field present

## Automatic Error Recovery (Critical)

If Step 4 fails, automatically attempt fallbacks in order:

### Fallback 1: Retry once with workspace path
```bash
# Sometimes transient failure, retry
cp -f "/source/path/to/file.png" "~/.openclaw/workspace/${filename}"
# Resend
```

### Fallback 2: Use base64 for images (especially .png, .gif)
```bash
# Convert to base64
base64_string=$(base64 -i "$abs_path")

# Send as inline image
{
  "action": "send",
  "target": "ou_xxx",
  "image": "data:image/png;base64,${base64_string}"
}
```

**When to use:** Path method fails, small images (<3MB), .png/.gif files

### Fallback 3: Upload to Feishu drive then share
```json
{
  "action": "upload_file",
  "doc_token": "xxx",
  "file_path": "$abs_path"
}
```
Then send the returned file URL.

**When to use:** Files >20MB, persistent path failures

## Error Handling Checklist

| Error | Cause | Solution |
|-------|-------|----------|
| File not found | Wrong path | Verify source path exists |
| Permission denied | File permission issue | `chmod 644` on file |
| Tool error | Feishu API issue | Retry → base64 → drive |
| Empty file | Zero-byte file | Check source before copying |
| File too large | >20MB | Use Feishu drive |

## Quick Reference

| Scenario | Primary Method | Fallback 1 | Fallback 2 |
|----------|---------------|------------|------------|
| Small image (<3MB) | path | base64 | - |
| Large image (3-20MB) | path | base64 | drive |
| Document | path | drive | - |
| Audio/Video | path | drive | - |
| Very large (>20MB) | drive | - | - |

## Mandatory Rules

1. **ALWAYS copy to workspace first** - Never send from /tmp, Downloads, or other临时路径
2. **ALWAYS verify copy succeeded** - Check file exists before sending
3. **ALWAYS use absolute path** - No relative paths in message tool
4. **ALWAYS attempt fallback on failure** - Never give up after one try
5. **ALWAYS extract basename** - Preserve original filename, don't rename
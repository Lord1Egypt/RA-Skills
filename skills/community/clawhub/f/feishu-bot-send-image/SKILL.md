---
name: feishu-send-image
description: |
  Send images directly in Feishu chat as native image messages (not file attachments).
  Use when: need to send a generated image, chart, screenshot, or any local image file to a Feishu user or group chat.
  Triggers: "发图", "send image", "发送图片", sending charts/graphs/screenshots via Feishu.
  Note: OpenClaw's built-in message tool (filePath/media/buffer) does NOT work for Feishu image sending — it only produces file attachments. This skill bypasses that limitation by calling Feishu Bot API directly.
---

# Feishu Send Image

Send local image files as native Feishu image messages via the Feishu Bot API.

## Why This Skill Exists

OpenClaw's `message` tool with `filePath`, `media`, or `buffer` parameters only sends file attachments in Feishu, not inline images. This skill calls the Feishu API directly to send proper image messages.

## Quick Usage

Run the script:

```bash
bash scripts/feishu_send_image.sh <image_path> <receive_id> <app_id> <app_secret> [receive_id_type]
```

### Arguments

| Arg | Description |
|-----|-------------|
| `image_path` | Local path to image (png/jpg/gif/webp) |
| `receive_id` | Feishu `open_id` (user) or `chat_id` (group) |
| `app_id` | Feishu app ID from `~/.openclaw/openclaw.json` → `feishu.accounts.default.appId` |
| `app_secret` | Feishu app secret from `~/.openclaw/openclaw.json` → `feishu.accounts.default.appSecret` |
| `receive_id_type` | `open_id` (default) or `chat_id` |

### Example

```bash
bash scripts/feishu_send_image.sh /tmp/chart.png \
  ou_38470740452f6083ce189b7ddec722f8 \
  cli_a92c368412f9dcb1 \
  7uM7aLqeqYqm0Fsy0IP5QhOyTBSwxlfT
```

## Getting Credentials

Read `~/.openclaw/openclaw.json` and extract:
- `channels.feishu.accounts.default.appId`
- `channels.feishu.accounts.default.appSecret`

The receiver's `open_id` comes from inbound message metadata (`sender_id`).

## How It Works

1. **Get token** — `POST /auth/v3/tenant_access_token/internal` with appId/appSecret
2. **Upload image** — `POST /im/v1/images` with `image_type=message`, returns `image_key`
3. **Send message** — `POST /im/v1/messages` with `msg_type=image` and the `image_key`

## Output

On success: `OK: image_key=<key> message_id=<id>`
On failure: prints error and exits with code 1.

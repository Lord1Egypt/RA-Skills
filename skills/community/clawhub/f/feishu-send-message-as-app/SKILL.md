---
name: feishu-send-message-as-app
description: "Send a Feishu IM message as the app (bot identity). Use when you need to send a message that appears to come from the bot/app, not the user. Uses App Access Token (no user auth needed). Supports text, image, post, card, and other Feishu msg types."
---

# Feishu Send Message as App

Send a Feishu IM message with **app/bot identity** — not user identity.

## Usage

```bash
bash <skill-dir>/scripts/send-message.sh <receive_id> <msg_type> <content> [open_id|chat_id]
```

### Examples

```bash
# Text message
bash <skill-dir>/scripts/send-message.sh ou_xxx text "Hello"

# Image message (use image_key from feishu-upload-image)
bash <skill-dir>/scripts/send-message.sh ou_xxx image '{"image_key":"img_v3_xxx"}'

# Post message (rich text)
bash <skill-dir>/scripts/send-message.sh ou_xxx post '{"zh_cn":{"title":"Title","content":[[{"tag":"text","text":"Hello"}]]}}'

# To a group chat
bash <skill-dir>/scripts/send-message.sh oc_xxx text "Hello" chat_id
```

### Environment variables
```bash
export FEISHU_RECEIVE_ID="ou_xxx"
export FEISHU_MSG_TYPE="text"
export FEISHU_CONTENT="Hello"
bash <skill-dir>/scripts/send-message.sh
```

## Workflow with feishu-upload-image

```bash
# 1. Upload image → get image_key
IMAGE_KEY=$(bash <feishu-upload-image-dir>/scripts/upload-image.sh /path/to/image.png)

# 2. Send as app
bash <skill-dir>/scripts/send-message.sh ou_xxx image "{\"image_key\":\"$IMAGE_KEY\"}"
```

## Output
```
message_id: om_xxxxxxxxxxxxxxxx
```

## Credentials

Reads `appId` and `appSecret` from `openclaw.json` at `channels.feishu`.

---
name: feishu-upload-image
description: "Upload a local image to Feishu and get its image_key. Use when you need to send an image via Feishu IM but first need the image_key returned by the upload API. Only handles: local file → Feishu image_key. Does NOT send the message — use feishu_im_user_message tool for that."
---

# Feishu Upload Image

Upload a local image file to Feishu and receive the `image_key` needed for sending via `feishu_im_user_message`.

**只做一件事**：本地文件 → image_key

## Usage

```bash
bash <skill-dir>/scripts/upload-image.sh /path/to/image.png
```

### Environment variables
```bash
export FEISHU_IMAGE_PATH="/path/to/image.png"
bash <skill-dir>/scripts/upload-image.sh
```

## Output
```
img_v3_02104_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxxg
```

## Complete Workflow

```bash
# 1. Upload → get image_key
IMAGE_KEY=$(bash <skill-dir>/scripts/upload-image.sh /path/to/image.png)

# 2. Send via feishu_im_user_message tool (OpenClaw-native, user token auto-managed)
#    action=send, msg_type=image, content="{\"image_key\":\"<IMAGE_KEY>\"}"
```

## Credentials

Reads `appId` and `appSecret` from `openclaw.json` at `channels.feishu`. Can be overridden with env vars `FEISHU_APP_ID` and `FEISHU_APP_SECRET`.

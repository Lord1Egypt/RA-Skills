---
name: feishu-media-delivery
description: Reliably deliver generated images and videos to Feishu/Lark users and chats. Use when an agent already has a local image/video result and must send it to Feishu without guessing protocol details. Handles Feishu image messages (upload -> image_key -> msg_type=image), Feishu video/media messages (upload -> file_key -> msg_type=media), and fallback delivery patterns for multimodal generation agents.
---

# Feishu Media Delivery

Use this skill as the **last-mile delivery layer** for multimodal agents.

It does not generate content.
It only makes sure already-generated files are sent to Feishu with the correct protocol.

## What this skill is for

Use this skill when you already have a generated result and need to deliver it to a Feishu user/chat.

Typical cases:
- A generated jpg/png must be sent as a real Feishu image message
- A generated mp4 must be sent as a real Feishu media message
- A multimodal agent finished generation and now needs reliable delivery
- You want to avoid protocol mistakes like sending jpg/mp4 as the wrong message type

## Hard rules

### Images
For images, do **not** send the local file as plain text or guess a generic attachment format.

Correct flow:
1. Upload image to Feishu IM resource API
2. Get `image_key`
3. Send message with `msg_type=image`

Use:
- `scripts/send-image.mjs`

### Videos
For mp4 videos, do **not** send them as `file` messages.

Correct flow:
1. Upload mp4 to Feishu IM file API
2. Get `file_key`
3. Send message with `msg_type=media`

Use:
- `scripts/send-media.mjs`

## Required environment

The scripts expect:
- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET_PATH` or default secret file at `~/.openclaw/secrets/feishu_app_secret`

Default secret path:
- `~/.openclaw/secrets/feishu_app_secret`

## Receive ID assumptions

The bundled scripts default to `receive_id_type=open_id`.

Use them directly when the target is a Feishu user `open_id` like:
- `ou_xxx`

If you need group delivery later, extend the script to accept `chat_id` and switch `receive_id_type`.

## Commands

### Send image to a Feishu user

```bash
cd scripts
node send-image.mjs <open_id> /path/to/image.jpg
```

Example:

```bash
cd scripts
node send-image.mjs ou_xxx /tmp/result.jpg
```

### Send mp4 video to a Feishu user

```bash
cd scripts
node send-media.mjs <open_id> /path/to/video.mp4 mp4 5000
```

Arguments:
- arg1: target open_id
- arg2: local mp4 path
- arg3: file type, usually `mp4`
- arg4: duration in milliseconds, optional but recommended

Example:

```bash
cd scripts
node send-media.mjs ou_xxx /tmp/result.mp4 mp4 5000
```

## Output expectations

A successful send should return Feishu success payloads such as:
- `code: 0`
- `msg: success`

Do not assume transport success only from local script execution.
Check the returned Feishu response.

## Fallback policy

### Image fallback
If real Feishu image sending fails, report that image delivery failed.
Do not silently pretend the image was delivered.

### Video fallback
If Feishu media sending fails, fallback to sending a direct link if one exists.
State clearly that this is a fallback.

## Recommended agent usage

For a multimodal content agent, use this skill after generation:

- image result -> `send-image.mjs`
- mp4 result -> `send-media.mjs`

This keeps protocol details out of the model prompt and reduces failure risk for weaker models.

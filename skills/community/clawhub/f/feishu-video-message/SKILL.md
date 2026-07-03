---
name: feishu-video-message
description: 飞书视频发送器 — 当需要在飞书聊天中发送/展示视频时使用（包括把 OpenViking 等远端视频 preview_url 投递到飞书）。上传视频并以媒体消息发送，自动抽取首帧作为封面、探测时长，聊天中可直接播放。用 --url 传远端视频地址、用 --receive-id 传当前聊天标识（上下文原值如 chat:oc_xxx 即可）。| Feishu Video Message — Use when sending/showing a video in a Feishu chat. Upload & send via Feishu OpenAPI with auto cover & duration; pass --url for remote video and --receive-id for the current chat id.
license: MIT
compatibility: openclaw
metadata:
  version: "1.0.2"
  tags: [feishu, video, media, upload, im, messaging, openapi]
  openclaw:
    emoji: "🎬"
    requires:
      bins: [python3, ffmpeg, ffprobe]
      config:
        - ~/.openclaw/openclaw.json
---

# Feishu Video Message | 飞书视频发送器

Upload a video to Feishu and send it as a media message with auto-generated cover & duration, playable in chat.

将视频上传至飞书并以媒体消息发送，自动抽取首帧作为封面、探测时长，聊天中可直接播放。

## When to Use | 何时使用

当**在飞书渠道中需要把一段视频发送/展示给用户**时，使用本 skill（无需修改 Agent soul）。典型场景：

- 用户在飞书里要求「发个视频 / 把这个视频发我」
- 拿到一个视频的远端地址（如 OpenViking 资源的 `preview_url`）需要投递到当前飞书聊天

调用约定：

- 用 `--url` 传远端视频地址（skill 会下载→发送→自动删除临时文件）；本地文件则用 `--file`。
- 用 `--receive-id` 传**当前聊天**的标识，**直接用上下文里的原值即可**（如 `chat:oc_xxx`），skill 会自动剥掉 `chat:` 前缀。单聊为 `ou_` 开头、群聊为 `oc_` 开头。

## Quick Start

```bash
# 本地文件（自动封面 + 时长）
python3 scripts/feishu_send_video.py --file video.mp4 --receive-id oc_xxx

# 远端 URL（如 OpenViking preview_url）：下载 → 发送 → 自动删除临时文件
python3 scripts/feishu_send_video.py --url 'https://.../video.mp4' --receive-id oc_xxx

# 跳过封面
python3 scripts/feishu_send_video.py --file video.mp4 --receive-id ou_xxx --no-cover
```

## Arguments

| Param               | Required | Description                                                                      |
| ------------------- | -------- | -------------------------------------------------------------------------------- |
| `--file`            | ⬩        | 本地视频文件路径（与 `--url` 二选一）                                            |
| `--url`             | ⬩        | 远端视频 URL（与 `--file` 二选一）；下载到临时文件，发送后自动删除               |
| `--receive-id`      | ✅       | 必填：当前聊天的 `chat_id`（群聊 `oc_`）或 `open_id`（单聊 `ou_`），由调用方传入 |
| `--receive-id-type` | optional | 默认按前缀自动识别：`oc_` → chat*id，`ou*` → open_id，`on\_` → user_id           |
| `--no-cover`        | optional | 跳过首帧封面抽取                                                                 |

> `--file` 与 `--url` 必须二选一（至少一个、不能同时）。

### 关于 `--receive-id`（聊天目标）

`--receive-id` 必填，由调用方（模型）传入「当前聊天」的标识：

- **单聊**：传对方的 `chat_id`（一般为`ou_` 开头）
- **群聊**：传群的 `chat_id`（一般为`oc_` 开头）

> 获取当前聊天的chat-id传入，当做--receive-id的值。
>
> 可直接传 OpenClaw 上下文里的原值（如 `chat:oc_xxx`），skill 会自动剥掉 `chat:` 等前缀。

### Supported Formats

**Video:** MP4, MOV, AVI, MKV, WEBM（max 30 MB，以 MP4 上传）

## How It Works

1. **取源**：`--file` 用本地文件；`--url` 先下载到临时文件
2. **抽封面**：用 `ffmpeg` 抽取第 1 秒首帧 → 临时 JPG（失败自动降级为无封面）
3. **传封面**：上传首帧 via `/im/v1/images` → 得到 `image_key`
4. **探时长**：用 `ffprobe` 探测视频时长（毫秒）
5. **传视频**：上传 via `/im/v1/files`（file_type=mp4，带 `duration`）→ 得到 `file_key`
6. **发消息**：`msg_type=media`，content `{"file_key": "...", "image_key": "..."}`
7. **清理**：临时封面图 + `--url` 下载的临时视频发送后自动删除

Credentials are auto-read from `~/.openclaw/openclaw.json`.

封面抽取、时长探测、封面上传任一步失败都不会中断主流程，会降级为「无封面/无时长」继续发送视频。

## Requirements

- `python3`（依赖 `requests`）
- `ffmpeg` / `ffprobe`（封面抽取与时长探测）

## API Reference

- [Upload Image](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/image/create)
- [Upload File](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/file/create)
- [Send Message](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create)
